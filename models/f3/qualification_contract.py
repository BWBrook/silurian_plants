"""Integrity contract for real-design qualification artifacts; no estimator or simulator."""

import csv
import gzip
import hashlib
import io
import json
import math
from dataclasses import dataclass
from pathlib import Path

import validate as va

SCHEMA = "f3-real-qualification-v1"
PHASES = ("calibrate", "accept", "stage2", "dev")
DERIVED_TOLERANCE = dict(absolute=1e-8, relative=1e-8)


class EvidenceError(ValueError):
    pass


def normalise(value):
    if isinstance(value, dict):
        return {k: normalise(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalise(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return {"nonfinite": "nan" if math.isnan(value) else "inf" if value > 0 else "-inf"}
    return value


def encoded(value) -> bytes:
    return json.dumps(normalise(value), sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def restored(value):
    if isinstance(value, dict):
        if set(value) == {"nonfinite"}:
            return {"nan": math.nan, "inf": math.inf, "-inf": -math.inf}[value["nonfinite"]]
        return {k: restored(v) for k, v in value.items()}
    if isinstance(value, list):
        return [restored(v) for v in value]
    return value


def digest(value) -> str:
    return hashlib.sha256(encoded(value)).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message: str) -> None:
    if not condition:
        raise EvidenceError(message)


def integer(value, name: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"{name} must be an integer >= {minimum}")
    return value


def finite_shift(value, name: str = "shift") -> float:
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
            f"{name} must be finite and non-negative")
    return float(value)


def protocol(decl: dict) -> dict:
    q = decl["qualification"]
    n = integer(q["target_passing"], "target_passing", 1)
    require(n == va.N1 == va.N2, "binding replicate counts must match the two-stage acceptance rule")
    require(q["max_attempts"] == 20 * n, "binding max_attempts must be 20 times target_passing")
    require(q["calibration_target"] == va.CALIBRATION_TARGET, "calibration target differs from the acceptance contract")
    require(decl["common"]["alpha"] == 0.05, "the two-stage contract requires nominal alpha 0.05")
    seeds = q["root_seeds"]
    require(set(seeds) == {"calibrate", "accept", "stage2"}, "exactly three binding phase seeds are required")
    for phase, seed in seeds.items():
        integer(seed, f"{phase} root seed")
    require(len(set(seeds.values())) == 3, "calibration and acceptance batches require distinct root seeds")
    return dict(target_passing=n, max_attempts=q["max_attempts"], calibration_target=q["calibration_target"],
                root_seeds=seeds, stage1_n=va.N1, stage2_n=va.N2, floor=va.FLOOR,
                stage2_pass=va.STAGE2_PASS, first_rep=0,
                criterion="marginal false-claim frequency among screen-passing replicates; abstentions are non-errors")


def tag(binding: dict) -> str:
    design = binding["design"]
    require(isinstance(design, str) and design and all(c.isalnum() or c in "-_" for c in design),
            "unsafe design identifier")
    return f"{design}_rho{binding['rho']:g}"


def paths(base: Path, binding: dict, phase: str) -> tuple[Path, Path]:
    require(phase in PHASES, "unknown qualification phase")
    stem = f"{tag(binding)}_{phase}"
    return base / f"{stem}.json", base / f"{stem}_reps.csv.gz"


def phase_cells(binding: dict, phase: str, first: dict | None = None, diagnostics: bool = True) -> list[dict]:
    grid = binding["grid"]
    if phase == "stage2":
        require(first is not None and first["complete"], "stage 2 requires a complete stage 1")
        names = first["borderline_cells"]
        require(bool(names), "stage 2 requires an unresolved borderline quantity")
        return [c for c in grid if c["name"] in names]
    if phase == "accept" or (phase == "dev" and not diagnostics):
        return [c for c in grid if c["kind"] == "acceptance"]
    return grid


def check_binding(expected: dict, recorded: dict) -> None:
    expected, recorded = normalise(expected), normalise(recorded)
    require(isinstance(recorded, dict), "missing qualification binding")
    derived = []
    for side in (expected, recorded):
        values = side.pop("fitted_reference_rates", None)
        require(isinstance(values, list), "missing fitted reference rates")
        boundaries = {c["name"]: c.pop("f") for c in side["grid"] if "f_data" in c}
        derived.append(dict(rates=values, boundaries=boundaries))
    require(digest(expected) == digest(recorded), "receipt does not bind the current declaration, inputs, code and quantity grid")
    require(expected.get("derived_tolerance") == DERIVED_TOLERANCE, "undeclared derived-fit tolerance")
    def close(a, b):
        if isinstance(a, list):
            return isinstance(b, list) and len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
        if isinstance(a, dict):
            return isinstance(b, dict) and set(a) == set(b) and all(close(a[k], b[k]) for k in a)
        if type(a) in (int, float):
            return type(b) in (int, float) and math.isclose(a, b, rel_tol=DERIVED_TOLERANCE["relative"],
                                                          abs_tol=DERIVED_TOLERANCE["absolute"])
        return type(a) is type(b) and a == b
    require(close(*derived), "recomputed reference rates or boundary truths exceed the declared tolerance")


def read_replicates(path: Path) -> list[dict]:
    text = gzip.decompress(path.read_bytes()).decode()
    reader = csv.DictReader(io.StringIO(text))
    fields = reader.fieldnames or []
    require(len(fields) == len(set(fields)), "replicate table has duplicate columns")
    require({"cell", "rep", "passed", "error"} <= set(fields), "replicate table lacks required columns")
    strings = {"cell", "error", "abstain_reason", "screen_status"}
    ints = {"rep", "n_old_det", "n_fits", "n_failed", "screen_n_older_detections"}
    floats = {"screen_lr", "screen_crit", "tau", "a_ref", "abar_rel"}
    out = []
    for raw in reader:
        require(None not in raw and all(v is not None for v in raw.values()), "malformed replicate row")
        row = {}
        for key, value in raw.items():
            if key in strings or key.startswith("state_"):
                if value or key == "error":
                    row[key] = value
            elif not value:
                continue
            elif key in {"passed", "trivial", "screen_converged"} or key.startswith("c_"):
                require(value in {"True", "False"}, f"{key} is not a strict Boolean")
                row[key] = value == "True"
            elif key in ints:
                require(value.isdecimal(), f"{key} is not a non-negative integer")
                row[key] = int(value)
            elif key in floats or key.startswith(("m_", "fstar_")):
                try:
                    number = float(value)
                except ValueError as exc:
                    raise EvidenceError(f"{key} is not numeric") from exc
                require(not math.isnan(number), f"{key} is NaN")
                require(key.startswith("m_") or math.isfinite(number), f"{key} is not finite")
                row[key] = number
            else:
                raise EvidenceError(f"unknown replicate column {key}")
        out.append(row)
    return out


def summarise(rows: list[dict], cell: dict, target: int, cap: int, shift: float, calibration_target: float) -> dict:
    name, quantities = cell["name"], cell["quantities"]
    require(bool(quantities) and len(set(quantities)) == len(quantities), f"{name}: invalid quantity roster")
    require(0 < len(rows) <= cap, f"{name}: invalid attempt count")
    require([r.get("rep") for r in rows] == list(range(len(rows))), f"{name}: attempts are missing, duplicated or reordered")
    passing = []
    for row in rows:
        require(row.get("cell") == name, f"{name}: wrong cell in replicate table")
        require(type(row.get("rep")) is int, f"{name}: non-integer replicate index")
        require(type(row.get("passed")) is bool and isinstance(row.get("error"), str), f"{name}: malformed outcome flags")
        status = row.get("screen_status")
        if status == "evaluated":
            require(row.get("screen_converged") is True, f"{name}: screen did not converge")
            n = integer(row.get("screen_n_older_detections"), "screen older-detection count")
            lr, critical = row.get("screen_lr"), row.get("screen_crit")
            require(type(lr) in (int, float) and math.isfinite(lr) and lr >= 0, f"{name}: invalid screen statistic")
            require(type(critical) in (int, float) and critical == va.ev.count_crit(n), f"{name}: wrong screen critical value")
            require(row["passed"] == (lr > critical), f"{name}: screen flag contradicts its statistic")
        else:
            require(not row["passed"] and status in {"no-first-appearance", "error"}, f"{name}: missing or invalid screen status")
            require((status == "error") == bool(row["error"]), f"{name}: screen failure has no error record")
        actual = {k[2:] for k in row if k.startswith("c_")}
        margins = {k[2:] for k in row if k.startswith("m_")}
        if not row["passed"]:
            require(not actual and not margins and "trivial" not in row, f"{name}: unpassed attempt has scored outputs")
            continue
        passing.append(row)
        require(actual == margins == set(quantities), f"{name}: passing attempt lacks exactly the declared quantities")
        require(type(row.get("trivial")) is bool, f"{name}: missing explicit trivial flag")
        for q in quantities:
            covered, margin = row[f"c_{q}"], row[f"m_{q}"]
            require(type(covered) is bool, f"{name}/{q}: coverage is not Boolean")
            require(type(margin) in (int, float) and not math.isnan(margin), f"{name}/{q}: invalid margin")
            if row["error"]:
                require(not covered and margin == math.inf and not row["trivial"], f"{name}/{q}: failed analysis was not counted as failure")
            elif row["trivial"]:
                require(covered and margin == -math.inf, f"{name}/{q}: malformed abstention")
            else:
                require((covered and margin <= shift + 1e-12) or (not covered and margin >= shift - 1e-12),
                        f"{name}/{q}: coverage contradicts the calibrated margin")
    require(len(passing) <= target, f"{name}: more passing replicates than declared")
    reached = len(passing) == target
    require((reached and rows[-1]["passed"]) or (not reached and len(rows) == cap),
            f"{name}: run stopped before its target or attempt cap")
    before_errors = sum(bool(r["error"]) for r in rows if not r["passed"])
    s = dict(cell=name, kind=cell["kind"], attempts=len(rows), passes=len(passing),
             pass_rate=len(passing) / len(rows), complete=reached and before_errors == 0,
             errors=sum(bool(r["error"]) for r in passing),
             errors_before_screen=before_errors)
    for q in quantities:
        claims = [r for r in passing if r["error"] or not r["trivial"]]
        s[f"cover_{q}"] = sum(r[f"c_{q}"] for r in passing)
        s[f"claims_{q}"] = len(claims)
        s[f"claimmiss_{q}"] = sum(not r[f"c_{q}"] for r in claims)
        s[f"delta_{q}"] = va.shift_to_target([r[f"m_{q}"] for r in passing], calibration_target) if passing else math.inf
    return s


def assessment(binding: dict, phase: str, rows: list[dict], target: int, cap: int, shift: float,
               first: dict | None = None, diagnostics: bool = True) -> dict:
    grid = phase_cells(binding, phase, first, diagnostics)
    require(bool(grid), "empty qualification grid")
    require({r.get("cell") for r in rows} == {c["name"] for c in grid}, "replicate evidence has missing or unexpected cells")
    summaries = [summarise([r for r in rows if r["cell"] == c["name"]], c, target, cap, shift,
                           binding["protocol"]["calibration_target"]) for c in grid]
    acceptance = [s for s in summaries if s["kind"] == "acceptance"]
    complete = all(s["complete"] for s in acceptance) and not any(s["errors_before_screen"] for s in summaries)
    result = dict(cells=summaries, complete=complete)
    if phase == "calibrate":
        delta = max(v for s in acceptance for k, v in s.items() if k.startswith("delta_"))
        result["delta"] = delta if complete and math.isfinite(delta) else None
        result["complete"] = complete and result["delta"] is not None
    elif phase in {"accept", "stage2"}:
        counts = {f"{s['cell']}:{k[6:]}": (v, s["passes"], s["complete"])
                  for s in acceptance for k, v in s.items() if k.startswith("cover_")}
        if phase == "accept":
            verdicts = {key: va.stage1(k, n) if done else "incomplete" for key, (k, n, done) in counts.items()}
        else:
            previous = {f"{s['cell']}:{k[6:]}": v for s in first["cells"] for k, v in s.items() if k.startswith("cover_")}
            verdicts = {key: old if old != "borderline" else
                        va.stage2(previous[key] + counts[key][0]) if counts[key][2] else "incomplete"
                        for key, old in first["verdicts"].items()}
        result["verdicts"] = verdicts
        result["borderline_cells"] = sorted({key.split(":")[0] for key, v in verdicts.items() if v == "borderline"})
        result["result"] = ("pass" if all(v == "pass" for v in verdicts.values()) else
                            "fail" if "fail" in verdicts.values() else
                            "incomplete" if "incomplete" in verdicts.values() else "borderline")
    return result


def seal(record: dict) -> dict:
    clean = {k: v for k, v in record.items() if k != "payload_sha256"}
    return normalise(clean | {"payload_sha256": digest(clean)})


def _json_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key}")
        result[key] = value
    return result


def read_record(path: Path) -> dict:
    try:
        record = json.loads(path.read_text(), object_pairs_hook=_json_pairs,
                            parse_constant=lambda v: (_ for _ in ()).throw(EvidenceError(f"invalid JSON number {v}")))
    except (OSError, ValueError) as exc:
        raise EvidenceError(f"cannot read receipt {path}: {exc}") from exc
    require(isinstance(record, dict) and record.get("schema") == SCHEMA, "receipt is historical or has an unsupported schema")
    require(record.get("payload_sha256") == digest({k: v for k, v in record.items() if k != "payload_sha256"}),
            "receipt payload checksum does not match")
    return record


@dataclass
class Verified:
    record: dict
    path: Path
    sha256: str


def load(base: Path, binding: dict, phase: str) -> Verified:
    require(phase != "dev", "development evidence cannot qualify empirical results")
    path, reps = paths(base, binding, phase)
    record = read_record(path)
    check_binding(binding, record.get("binding"))
    require(record.get("binding_sha256") == digest(record["binding"]), "binding checksum does not match")
    p = binding["protocol"]
    require(record.get("phase") == phase and record.get("root") == p["root_seeds"][phase], "receipt phase or seed differs from the protocol")
    require(type(record.get("root")) is int, "root seed must be an integer")
    require(record.get("target") == p["target_passing"] and type(record.get("target")) is int,
            "receipt does not have the binding replicate count")
    require(record.get("cap") == p["max_attempts"] and type(record.get("cap")) is int, "receipt attempt cap differs from the protocol")
    shift, dependencies, first = 0.0, {}, None
    if phase != "calibrate":
        cal = load(base, binding, "calibrate")
        require(cal.record["complete"], "calibration is incomplete")
        shift = finite_shift(cal.record["delta"], "calibration delta")
        require(record["binding_sha256"] == cal.record["binding_sha256"], "acceptance did not retain the calibration's exact resolved truth")
        dependencies["calibrate"] = cal.sha256
        if phase == "stage2":
            acceptance = load(base, binding, "accept")
            first = acceptance.record
            dependencies["accept"] = acceptance.sha256
    require(finite_shift(record.get("shift")) == shift, "receipt used a different calibration shift")
    require(record.get("dependencies") == dependencies, "receipt is attached to another calibration or stage 1")
    require(record.get("replicates") == {"file": reps.name, "sha256": file_hash(reps)}, "replicate file checksum does not match")
    rows = read_replicates(reps)
    again = assessment(record["binding"], phase, rows, p["target_passing"], p["max_attempts"], shift, first)
    for key, value in again.items():
        require(digest(record.get(key)) == digest(value), f"receipt {key} disagrees with its replicate evidence")
    if phase == "calibrate" and record["complete"]:
        finite_shift(record["delta"], "calibration delta")
    return Verified(record, path, file_hash(path))


def write(base: Path, binding: dict, phase: str, rows: list[dict], root: int, target: int, cap: int,
          shift: float, dependencies: dict, runtime: dict, seconds: float, first: dict | None = None,
          diagnostics: bool = True) -> Verified:
    path, reps = paths(base, binding, phase)
    require(not path.exists() and not reps.exists(), f"qualification artifacts already exist: {path.stem}; use a new output directory")
    finite_shift(shift)
    result = assessment(binding, phase, rows, target, cap, shift, first, diagnostics)
    buf = io.StringIO()
    keys = list(dict.fromkeys(k for row in rows for k in row))
    writer = csv.DictWriter(buf, keys, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    payload = gzip.compress(buf.getvalue().encode(), mtime=0)
    record = seal(dict(schema=SCHEMA, binding=normalise(binding), binding_sha256=digest(binding),
                       phase=phase, root=root, shift=shift, target=target, cap=cap,
                       dependencies=dependencies, runtime=runtime, seconds=seconds,
                       replicates=dict(file=reps.name, sha256=hashlib.sha256(payload).hexdigest()), **result))
    base.mkdir(parents=True, exist_ok=True)
    with reps.open("xb") as f:
        f.write(payload)
    with path.open("x") as f:
        json.dump(record, f, indent=2, allow_nan=False)
        f.write("\n")
    return Verified(record, path, file_hash(path))
