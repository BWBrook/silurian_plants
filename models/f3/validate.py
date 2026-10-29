# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Validation harness for the F3 compatibility estimator (envelope.py), on simulated unit tables.

    uv run models/f3/validate.py --reps 5                          # all 21 cells, a quick run
    uv run models/f3/validate.py --reps 1000 --cells A2 A9         # a stage-1 batch of two cells
    uv run models/f3/validate.py --reps 1000 --start 1000 --cells A2 --tag dev_b   # the stage-2 batch

Each replicate simulates a unit table (units_sim.py) and lets the estimator find its own first appearance
and reference window. Per replicate, for each history class that contains the truth (and always H0):
- f*_K at the true origin t0 and at T = 459.1 (Hooper's M2 maximum) when that lies above the estimated tau,
  with the state, and LR_K(abar_rel), the statistic at the true target; abar_rel = abar_true / a_ref, the
  true mean intensity over (tau, t0] relative to the realised reference window (a_ref is the exposure-
  weighted mean of the true path over the realised reference units' true ages). The target is the expected
  encounter intensity: the path times older_report and (1 - confine) beyond tau0. Where those differ from
  the nominal path the statistic at the nominal target is stored too (lr_nominal_*). f* >= abar_rel - tol
  is the same event as LR_K(abar_rel) <= crit, so the summary applies any shift delta to the stored LR;
- the origin sets for H0c, H0m and H0 at each f_min read-out: whether the set contains t0 (`cover_set`, the
  grid set with each boundary widened to the next grid point), and the exact statistic at t0 (`lr0`).
  `applicable` is the largest read-out for which "a >= f_min" holds on (tau, t0] (H0c, H0) or on
  (tau, t0 - D] (H0m, D = h0m_lag_ma) for the true path relative to a_ref;
- informativeness: unbounded sets, the older endpoint, the share of the domain excluded, the states of f*.
Coverage is over all replicates; a replicate whose t0 lies at or below the estimated tau is `trivial` (the
null is vacuous, f* has zero exposure) and counts as covered. Coverage over non-trivial replicates is a
diagnostic, as is every coverage in a cell marked `diagnostic`. `delta95` is the smallest shift of the critical
value (not below 0) that brings a primary coverage to 0.95. Fits are flagged when no start succeeded or the
starts differ by more than 0.05 in log-likelihood.

Also here: the two-stage acceptance rule for the full grid (stage1, stage2, pass_probability).
Outputs: out/validation_<tag>.csv (one row per cell), out/validation_<tag>_reps.csv (one row per replicate)
and out/validation_<tag>.meta.json (seeds, settings, hashes). Replicate j of cell c descends from
SeedSequence(ROOT_SEED, spawn_key=(c, j)); child 0 simulates.
"""

import argparse
import csv
import hashlib
import json
import math
import platform
import time
from dataclasses import asdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

import envelope as ev
import sim
import units_sim as us

OUT = Path(__file__).resolve().parent / "out"
ROOT_SEED = 20261030
STEP = 2.0
READOUTS = (1.0, 0.1, 0.01)
M2_MAX = 459.1
ORIGIN_CLASSES = ("H0c", "H0m", "H0")
TARGET_COVERAGE = 0.95

BASE = dict(t0=476.0, tau0=452.8, p=(0.12, 0.04), class_weights=(0.6, 0.4), k=2.0, scale=0.05, nodes=48)
CELLS = []
for _name, _kind, _kw in [
    ("A1", "acceptance", dict(history="H0c", f=1.0)),
    ("A2", "acceptance", dict(history="H0c", f=0.3)),
    ("A3", "acceptance", dict(history="H0c", f=0.1)),
    ("A4", "acceptance", dict(history="H0c", f=0.3, k=math.inf)),
    ("A5", "acceptance", dict(history="H0c", f=0.3, k=0.8, nodes=64)),
    ("A6", "acceptance", dict(history="step", f=0.3, delay=4.3)),
    ("A7", "acceptance", dict(history="ramp")),
    ("A8", "acceptance", dict(history="logistic", g=0.3, h=7.7)),
    ("A9", "acceptance", dict(history="hide", f=0.3)),
    ("A10", "acceptance", dict(history="hide_h1", f=0.3)),
    ("A11", "acceptance", dict(history="H0c", f=0.3, class_trend=0.8)),
    ("A12", "acceptance", dict(history="hide", f=0.3, class_trend=0.8)),
    ("A13", "acceptance", dict(history="H0c", f=0.3, scale=0.2)),
    ("A14", "acceptance", dict(history="H0c", f=1.0, t0=466.0)),
    ("A15", "acceptance", dict(history="H0c", f=0.3, t0=500.0)),
    ("D1", "diagnostic", dict(history="H0c", f=0.3, misassign=0.1)),
    ("D2", "diagnostic", dict(history="H0c", f=0.3, older_report=0.7)),
    ("D3", "diagnostic", dict(history="H0c", f=0.3, confine=0.5)),
    ("D4", "diagnostic", dict(history="H0c", f=0.3, k=0.8, k_analysis=2.0)),
    ("D5", "diagnostic", dict(history="H0c", f=0.3, truth_scenario="older")),
    ("D6", "diagnostic", dict(history="H0c", f=0.3, truth_scenario="younger")),
]:
    CELLS.append(dict(id=len(CELLS), name=_name, kind=_kind) | BASE | _kw)


# --- the acceptance rule for the full grid -------------------------------------------------------

FLOOR = 0.93
STAGE2_PASS = 1886


def lower_limit(successes: int, n: int, conf: float = 0.95) -> float:
    """One-sided exact (Clopper-Pearson) lower confidence limit of a binomial proportion."""
    return 0.0 if successes == 0 else float(stats.beta.ppf(1 - conf, successes, n - successes + 1))


def upper_limit(successes: int, n: int, conf: float = 0.95) -> float:
    return 1.0 if successes == n else float(stats.beta.ppf(conf, successes + 1, n - successes))


def stage1(successes: int, n: int = 1000) -> str:
    """'pass' if the lower limit exceeds the floor, 'fail' if the upper limit is below it, else 'borderline'."""
    if lower_limit(successes, n) > FLOOR:
        return "pass"
    return "fail" if upper_limit(successes, n) < FLOOR else "borderline"


def stage2(successes: int) -> str:
    """The pooled 2,000 of a borderline cell passes at STAGE2_PASS successes: the threshold that holds the
    overall chance of passing a cell at the floor to 0.05 once the interim look is allowed for."""
    return "pass" if successes >= STAGE2_PASS else "fail"


def pass_probability(coverage: float, n1: int = 1000, n2: int = 1000) -> float:
    """P(a cell with this true coverage passes the two-stage rule)."""
    k1 = np.arange(n1 + 1)
    pm1 = stats.binom.pmf(k1, n1, coverage)
    total = 0.0
    for k, p in zip(k1, pm1):
        verdict = stage1(int(k), n1)
        if verdict == "pass":
            total += p
        elif verdict == "borderline":
            total += p * stats.binom.sf(STAGE2_PASS - k - 1, n2, coverage)
    return float(total)


# --- one replicate -------------------------------------------------------------------------------

_AGE = None


def _age() -> ev.AgeModel:
    global _AGE
    if _AGE is None:
        _AGE = ev.AgeModel.load()
    return _AGE


def cell_objects(cell: dict):
    truth = us.Truth(**{k: cell[k] for k in ("history", "t0", "tau0", "f", "delay", "g", "h") if k in cell})
    design = us.Design(
        p=tuple(cell["p"]), class_weights=tuple(cell["class_weights"]), k=cell["k"], scale=cell["scale"],
        **{k: cell[k] for k in ("class_trend", "misassign", "older_report", "confine", "truth_scenario") if k in cell},
    )
    spec = ev.Spec(nodes=cell["nodes"], cluster_shape_k=cell.get("k_analysis", cell["k"]), readouts=READOUTS)
    return truth, design, spec


def evaluated_classes(truth: us.Truth, spec: ev.Spec) -> list[str]:
    return [c for c in spec.classes if c in truth.members or c == "H0"]


def replicate(job: tuple[dict, int]) -> dict:
    cell, rep = job
    row = dict(cell=cell["name"], rep=rep, error="")
    try:
        row.update(_replicate(cell, rep))
    except Exception as e:
        row.update(error=f"{type(e).__name__}: {e}", no_tau=False)
    return row


def _replicate(cell: dict, rep: int) -> dict:
    t_start = time.time()
    truth, design, spec = cell_objects(cell)
    ss = np.random.SeedSequence(ROOT_SEED, spawn_key=(cell["id"], rep))
    age = _age()
    s = us.simulate(truth, design, sim.child_seed(ss, 0))
    try:
        pr = ev.Problem(s.units, spec, age)
    except ev.NoFirstAppearance:
        return dict(no_tau=True)
    T0 = truth.t0
    nominal = truth.path(design)
    effective = us.effective_path(nominal, truth, design)
    r_true = s.r[pr.calibrated]
    ref = (s.units.old <= pr.s_star) & (s.units.young >= pr.s_star - spec.reference_stages + 1) & np.isin(s.units.cls, pr.calibrated)
    w_ref = s.r[s.cls_true[ref]]
    a_ref = float((w_ref * effective(s.t_true[ref])).sum() / w_ref.sum())
    trivial = T0 <= pr.tau
    n_det = pr.n_older_detections(T0)
    out = dict(
        no_tau=False, tau=pr.tau, trivial=trivial, n_ref=pr.n_ref, n_old=pr.n_old, n_dropped=pr.n_dropped_uncalibrated,
        n_old_detected=int(pr.od.sum()), n_old_detected_at_t0=n_det, crit_t0=pr.crit(T0), a_ref=a_ref,
        r_hat_1=pr.r_ref[0], r_hat_2=pr.r_ref[1] if pr.n_cls > 1 else math.nan,
    )
    targets = {}
    if not trivial:
        for label, path in (("rel", effective), ("nominal", nominal)):
            targets[label] = pr.abar_truth(path, T0, r_true) / a_ref
    out["abar_rel"] = targets.get("rel", math.nan)
    out["abar_nominal_rel"] = targets.get("nominal", math.nan)
    differs = design.older_report != 1.0 or design.confine > 0

    for cls in evaluated_classes(truth, spec):
        b = pr.fstar(cls, T0)
        out[f"fstar_{cls}"], out[f"state_{cls}"] = b.value, b.state
        out[f"lr_{cls}"] = out[f"lr_nominal_{cls}"] = None
        if not trivial and b.state != "zero-exposure" and np.isfinite(targets["rel"]):
            out[f"lr_{cls}"] = pr.lr(cls, T0, targets["rel"]).value
            if differs:
                out[f"lr_nominal_{cls}"] = pr.lr(cls, T0, targets["nominal"]).value
        if M2_MAX > pr.tau:
            b = pr.fstar(cls, M2_MAX)
            out[f"fstar459_{cls}"], out[f"state459_{cls}"] = b.value, b.state
        else:
            out[f"fstar459_{cls}"], out[f"state459_{cls}"] = math.nan, ""
    out["state_H1-no-ceiling"] = pr.fstar("H1-no-ceiling", T0).state

    lag = spec.h0m_lag_ma
    grid = pr.grid(STEP)
    domain = spec.domain_ma[1]
    for cls in ORIGIN_CLASSES:
        back = lag if cls == "H0m" else 0.0
        floor = us.min_intensity(effective, pr.tau, T0 - back) / a_ref
        out[f"fmin_applicable_{cls}"] = max((f for f in READOUTS if f <= floor + 1e-9), default=math.nan)
        for f in READOUTS:
            key = f"{cls}_{f:g}"
            o = pr.origin_set(cls, f, grid)
            out[f"cover_set_{key}"] = bool(o.contains(T0))
            out[f"lr0_{key}"] = 0.0 if trivial else pr.lr_origin(cls, T0, f)
            out[f"unbounded_{key}"] = bool(o.unbounded)
            out[f"connected_{key}"] = bool(o.connected)
            out[f"endpoint_{key}"] = math.nan if o.unbounded else o.older_endpoint
            out[f"excluded_{key}"] = 0.0 if o.unbounded else (domain - o.older_endpoint) / (domain - pr.tau)
    out["n_fits"], out["n_flagged"] = pr.n_fits, pr.n_flagged
    out["seconds"] = time.time() - t_start
    return out


# --- summary -------------------------------------------------------------------------------------


def _clean(xs) -> list[float]:
    return [float(x) for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]


def mean(xs) -> float:
    xs = _clean(xs)
    return float(np.mean(xs)) if xs else math.nan


def median(xs) -> float:
    xs = _clean(xs)
    return float(np.median(xs)) if xs else math.nan


def delta95(margins: list[float]) -> float:
    """The smallest shift of the critical value, not below 0, at which at least 95% of the margins
    (statistic minus critical value; -inf for a replicate that makes no claim) are covered."""
    if not margins:
        return math.nan
    return max(0.0, float(np.sort(margins)[math.ceil(TARGET_COVERAGE * len(margins)) - 1]))


def summarise(cell: dict, rows: list[dict]) -> dict:
    truth, design, spec = cell_objects(cell)
    ok = [r for r in rows if not r["error"] and not r["no_tau"]]
    nt = [r for r in ok if not r["trivial"]]
    out = {k: cell[k] for k in ("name", "kind", "history", "t0", "f", "k", "scale") if k in cell}
    fits = sum(r["n_fits"] for r in ok)
    out.update(
        delay=cell.get("delay", ""), n_rep=len(rows), n_error=sum(bool(r["error"]) for r in rows),
        n_no_tau=sum(bool(r.get("no_tau")) and not r["error"] for r in rows), n_valid=len(ok),
        n_nontrivial=len(nt), frac_nontrivial=len(nt) / len(ok) if ok else math.nan,
        tau_median=median(r["tau"] for r in ok), n_ref_median=median(r["n_ref"] for r in ok),
        n_old_median=median(r["n_old"] for r in ok), n_old_detected_median=median(r["n_old_detected_at_t0"] for r in ok),
        a_ref_median=median(r["a_ref"] for r in ok),
        flagged_share=sum(r["n_flagged"] for r in ok) / fits if fits else math.nan,
        seconds_per_rep=mean(r["seconds"] for r in ok),
    )
    for cls in evaluated_classes(truth, spec):
        for label, key in (("", f"lr_{cls}"), ("_nominal", f"lr_nominal_{cls}")):
            if label and not any(r.get(key) is not None for r in ok):
                continue
            margin = lambda r: -math.inf if r.get(key) is None else r[key] - r["crit_t0"]
            if cls in truth.members:
                out[f"fcover{label}_{cls}"] = mean(margin(r) <= 0 for r in ok)
                out[f"fcover{label}_nontrivial_{cls}"] = mean(margin(r) <= 0 for r in nt)
                out[f"delta95{label}_f_{cls}"] = delta95([margin(r) for r in ok])
        out[f"member_{cls}"] = cls in truth.members
        out[f"outside_{cls}"] = mean(r["abar_rel"] > (spec.h1_ceiling if cls == "H1" else 1.0) + 1e-9 for r in nt)
        for state in ev.STATES:
            out[f"state_{cls}_{state}"] = mean(r[f"state_{cls}"] == state for r in ok)
            out[f"state_nontrivial_{cls}_{state}"] = mean(r[f"state_{cls}"] == state for r in nt)
            out[f"state459_{cls}_{state}"] = mean(r[f"state459_{cls}"] == state for r in ok if r[f"state459_{cls}"])
        out[f"fstar_median_{cls}"] = median(r[f"fstar_{cls}"] for r in nt if r[f"state_{cls}"] == "finite")
        out[f"fstar459_median_{cls}"] = median(r[f"fstar459_{cls}"] for r in ok if r[f"state459_{cls}"] == "finite")
    for state in ev.STATES:
        out[f"state_H1-no-ceiling_{state}"] = mean(r["state_H1-no-ceiling"] == state for r in ok)
    for cls in ORIGIN_CLASSES:
        app = [r for r in ok if not math.isnan(r[f"fmin_applicable_{cls}"])]
        pick = lambda r, what: r[f"{what}_{cls}_{r[f'fmin_applicable_{cls}']:g}"]
        out[f"n_applicable_{cls}"] = len(app)
        out[f"cover_set_applicable_{cls}"] = mean(pick(r, "cover_set") for r in app)
        out[f"cover_exact_applicable_{cls}"] = mean(pick(r, "lr0") <= r["crit_t0"] for r in app)
        out[f"cover_exact_applicable_nontrivial_{cls}"] = mean(pick(r, "lr0") <= r["crit_t0"] for r in app if not r["trivial"])
        out[f"delta95_origin_{cls}"] = delta95([pick(r, "lr0") - r["crit_t0"] if not r["trivial"] else -math.inf for r in app])
        for f in READOUTS:
            key = f"{cls}_{f:g}"
            out[f"unbounded_{key}"] = mean(r[f"unbounded_{key}"] for r in ok)
            out[f"connected_{key}"] = mean(r[f"connected_{key}"] for r in ok)
            out[f"endpoint_median_{key}"] = median(r[f"endpoint_{key}"] for r in ok)
            out[f"excluded_{key}"] = mean(r[f"excluded_{key}"] for r in ok)
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    columns = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, columns, lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6g}" if isinstance(v, float) else v) for k, v in r.items()})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--start", type=int, default=0, help="index of the first replicate (a second batch uses 1000)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--cells", nargs="*", default=None)
    ap.add_argument("--tag", default="dev")
    args = ap.parse_args()
    cells = [c for c in CELLS if args.cells is None or c["name"] in args.cells]
    jobs = [(c, j) for c in cells for j in range(args.start, args.start + args.reps)]
    t0 = time.time()
    with Pool(args.workers) as pool:
        rows = pool.map(replicate, jobs, chunksize=1)
    elapsed = time.time() - t0
    OUT.mkdir(exist_ok=True)
    summary = [summarise(c, [r for r in rows if r["cell"] == c["name"]]) for c in cells]
    write_csv(OUT / f"validation_{args.tag}.csv", summary)
    write_csv(OUT / f"validation_{args.tag}_reps.csv", rows)
    here = Path(__file__).resolve().parent
    meta = dict(
        root_seed=ROOT_SEED, replicate_seed="SeedSequence(root_seed, spawn_key=(cell id, replicate)); child 0 simulates",
        reps=args.reps, start=args.start, step_ma=STEP, readouts=READOUTS, m2_max=M2_MAX, spec=asdict(ev.Spec()),
        stage2_pass=STAGE2_PASS, spread_flag=ev.SPREAD_FLAG,
        cells=[{k: (str(v) if isinstance(v, float) and math.isinf(v) else v) for k, v in c.items()} for c in cells],
        design=asdict(us.Design()), elapsed_seconds=elapsed, workers=args.workers,
        python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
        sha256={f: sha256(here / f) for f in ("envelope.py", "units_sim.py", "validate.py")}
        | {"timescale.csv": sha256(sim.TIMESCALE_CSV), "effort.csv": sha256(us.EFFORT_CSV)},
    )
    (OUT / f"validation_{args.tag}.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{len(jobs)} replicates in {elapsed:.0f} s -> {OUT / f'validation_{args.tag}.csv'}")


if __name__ == "__main__":
    main()
