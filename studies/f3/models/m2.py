# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""A maximum on frozen real designs (designs/m2.toml, or F3_DESIGNS): the screen, and the empirical read-outs.

    uv run studies/f3/models/m2.py screen            # out/m2_screen.csv: every design, variant, rho and reference minimum
    uv run studies/f3/models/m2.py results [workers]  # out/m2_results.csv at the qualified critical-value shifts

The screen (S0, S1 in m2.toml) is the function `screen`, called unchanged by qualify.py on every simulated
replicate. It uses the unshifted critical value, so it does not depend on the calibration.
"""

import argparse
import csv
import math
from pathlib import Path

import numpy as np

import designs as dz
import envelope as ev
import qualification_contract as qc

OUT = Path(__file__).resolve().parent / "out"


def potential(u: ev.Units, transported: np.ndarray) -> ev.Units:
    """The units the screen sees (amendment 1): transported (older) outcomes set to 0."""
    return ev.Units(u.young, u.old, u.cls, u.cluster, np.where(transported, 0, u.d), u.mult, u.lo_ma, u.hi_ma)


def screen(pr: ev.Problem) -> tuple[bool, float, float]:
    """(passes, statistic at f = 1 with every older unit exposed, unshifted critical value). pr is built on
    potential(units)."""
    if pr.n_old == 0 or pr.exposure(pr.spec.domain_ma[1]) <= 0:
        return False, 0.0, ev.count_crit(0, pr.spec.alpha)
    T = pr.spec.domain_ma[1]
    crit = ev.count_crit(pr.n_older_detections(T), pr.spec.alpha)
    st = pr.lr("H0c", T, 1.0)
    if not st.converged or not math.isfinite(st.value):
        raise RuntimeError("frame-potential statistic failed to converge")
    return bool(st.value > crit), float(st.value), crit


def problem(b: dz.Built, decl: dict, rho: float, cluster_k: float, min_ref: int, shift: float = 0.0,
            screened: bool = False) -> ev.Problem:
    u, _ = b.units(rho)
    if screened:
        u = potential(u, np.array([r.transported for r in b.rows]))
    spec = dz.spec(decl, cluster_k, min_ref)
    spec = ev.Spec(**{**spec.__dict__, "crit_shift": shift})
    return ev.Problem(u, spec, ev.AgeModel.load())


def prefix(decl: dict) -> str:
    return decl["common"]["maximum"].lower()


def vkey(v: dict) -> str:
    return ";".join(f"{k}={v[k]}" for k in sorted(v))


def is_primary(design: dict, v: dict, min_ref: int) -> bool:
    p = design.get("primary", {})
    return bool(p) and all(v.get(k, p[k]) == p[k] for k in p if k != "min_ref_units") and min_ref == p["min_ref_units"]


def analysis_role(design: dict, variant: dict, min_ref: int) -> str:
    if design["id"] == "QB-CO" and variant.get("reading") == "main" and variant.get("bor_unresolved") == "zero":
        return "inadmissible-coding-diagnostic"
    return "primary" if is_primary(design, variant, min_ref) else "sensitivity"


def run_screen() -> list[dict]:
    decl = dz.declarations(dz.DESIGNS)
    rows = []
    for design in decl["design"]:
        for v in dz.variants(design, decl):
            b = dz.build(design, v)
            for min_ref in decl["common"]["min_ref_units"]:
                for rho in decl["common"]["rho"]:
                    row = dict(design=design["id"], variant=vkey(v), min_ref=min_ref, rho=rho,
                               primary=is_primary(design, v, min_ref), analysis_role=analysis_role(design, v, min_ref),
                               admissible=analysis_role(design, v, min_ref) != "inadmissible-coding-diagnostic")
                    try:
                        pr = problem(b, decl, rho, v["cluster_k"], min_ref, screened=True)
                    except ev.NoFirstAppearance as e:
                        rows.append(row | dict(status=f"S0 fails: {e}", passes=False))
                        continue
                    ok, lr, crit = screen(pr)
                    ref = pr.rd
                    rows.append(row | dict(
                        status="passes" if ok else ("S0 fails: no exposed older unit" if pr.n_old == 0 else "S1 fails"),
                        passes=ok, tau=round(pr.tau, 3), n_ref=pr.n_ref, k_ref=int(ref.sum()),
                        r_ref=";".join(f"{r:.4g}" for r in pr.r_ref), n_old=pr.n_old, older_detections=int(pr.od.sum()),
                        dropped_uncalibrated=pr.n_dropped_uncalibrated, lr_f1=round(lr, 4), crit=round(crit, 4)))
    return rows


T_REPORT = (445.2, 452.8, 458.2, 459.1, 464.0, 469.4, 480.0, 560.0)  # [common] report_ma overrides


_QUALIFICATIONS: dict = {}


def shift_for(design_id: str, rho: float, directory: Path | None = None) -> tuple[float | None, str, str, dict]:
    """Validate primary evidence before attaching its calibration or verdict to empirical outputs."""
    import qualify
    return qualify.load_qualification(design_id, rho, directory or OUT / "qual")


def readouts(pr: ev.Problem, common: dict) -> dict:
    out = {}
    for T in common.get("report_ma", T_REPORT):
        if T <= pr.tau:
            continue
        for K in pr.spec.classes:
            b = pr.fstar(K, T)
            out[f"fstar_{K}_{T:g}"] = "" if b.state == "zero-exposure" else round(b.value, 4)
            out[f"state_{K}_{T:g}"] = b.state + ("" if b.converged else " (not converged)")
    grid = pr.grid(common["origin_step_ma"])
    for f in pr.spec.readouts:
        for K in ("H0c", "H0m", "H0"):
            o = pr.origin_set(K, f, grid)
            out[f"origin_{K}_{f:g}"] = "unbounded" if o.unbounded else round(o.older_endpoint, 2)
            out[f"origin_ok_{K}_{f:g}"] = bool(o.ok.all()) and o.connected
        o = pr.origin_set("H0", f, grid, start=common["window_start_ma"])
        out[f"window_{f:g}"] = "unbounded" if o.unbounded else round(o.older_endpoint, 2)
        out[f"window_ok_{f:g}"] = bool(o.ok.all()) and o.connected
    return out


def _result(job: tuple) -> dict:
    design_id, v, min_ref, rho, directory = job
    decl = dz.declarations(dz.DESIGNS)
    design = next(d for d in decl["design"] if d["id"] == design_id)
    if not design.get("qualify", True):
        delta, result, receipt_sha, binding = None, "not qualified", "", {}
    else:
        key = (design_id, rho, str(directory))
        if key not in _QUALIFICATIONS:
            _QUALIFICATIONS[key] = shift_for(design_id, rho, directory)
        delta, result, receipt_sha, binding = _QUALIFICATIONS[key]
    role = analysis_role(design, v, min_ref)
    qualification = result if role == "primary" else "sensitivity-unqualified" if role == "sensitivity" else role
    row = dict(design=design_id, variant=vkey(v), min_ref=min_ref, rho=rho, primary=is_primary(design, v, min_ref),
               analysis_role=role, admissible=role != "inadmissible-coding-diagnostic", qualification=qualification,
               primary_qualification=result, primary_receipt_sha256=receipt_sha,
               qualification_binding_sha256=qc.digest(binding) if binding else "",
               qualified_classes=";".join(binding.get("qualification_classes", [])) if role == "primary" and result == "pass" else "",
               shift="" if delta is None else delta)
    for K in decl["common"]["classes"]:
        row[f"qualification_{K}"] = qualification if role != "primary" or result != "pass" else \
            "pass" if K in binding["qualification_classes"] else "unqualified-class-diagnostic"
    row["qualification_window"] = row["qualification_H0"]
    pr = problem(dz.build(design, v), decl, rho, v["cluster_k"], min_ref, shift=delta or 0.0)
    row.update(tau=pr.tau, n_ref=pr.n_ref, k_ref=int(pr.rd.sum()), n_old=pr.n_old,
               older_detections=int(pr.od.sum()), r_ref=";".join(f"{r:.4g}" for r in pr.r_ref))
    return row | readouts(pr, decl["common"])


def run_results(workers: int = 8, qualification_dir: Path | None = None) -> list[dict]:
    """Read-outs for every variant that passes the screen, at its design's qualified shift for that rho
    (the primary variant's; other variants are labelled by `primary`)."""
    from multiprocessing import Pool
    import qualify
    decl = dz.declarations(dz.DESIGNS)
    inputs = {name: path for d in decl["design"] if dz.variants(d, decl) for name, path in qualify.bound_paths(d["id"]).items()}
    before = qualify.capture(inputs)
    _QUALIFICATIONS.clear()
    screened = {(r["design"], r["variant"], r["min_ref"], r["rho"]): r["passes"] for r in run_screen()}
    jobs = [(design["id"], v, min_ref, rho, qualification_dir or OUT / "qual") for design in decl["design"] for v in dz.variants(design, decl)
            for min_ref in decl["common"]["min_ref_units"] for rho in decl["common"]["rho"]
            if screened[(design["id"], vkey(v), min_ref, rho)]]
    with Pool(workers) as pool:
        rows = pool.map(_result, jobs, chunksize=1)
    qc.require(qualify.capture(inputs) == before, "empirical inputs changed during screening or fitting")
    return rows


def write(path: Path, rows: list[dict]) -> None:
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "x", newline="") as f:
        w = csv.DictWriter(f, keys, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=("screen", "results"))
    ap.add_argument("workers", type=int, nargs="?", default=8)
    ap.add_argument("--out-dir", type=Path, default=OUT)
    ap.add_argument("--qual-dir", type=Path, default=OUT / "qual")
    args = ap.parse_args(argv)
    if args.workers < 1:
        ap.error("workers must be positive")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    path = args.out_dir / f"{prefix(dz.declarations(dz.DESIGNS))}_{args.command}.csv"
    if path.exists():
        ap.error("output already exists; select a fresh --out-dir")
    if args.command == "screen":
        rows = run_screen()
        write(path, rows)
        for r in rows:
            if r["primary"]:
                print({k: r.get(k) for k in ("design", "rho", "status", "n_ref", "k_ref", "n_old", "lr_f1", "crit")})
    else:
        write(path, run_results(args.workers, args.qual_dir))


if __name__ == "__main__":
    main()
