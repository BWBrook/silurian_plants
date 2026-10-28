# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Validation harness for the F3 compatibility estimator (envelope.py), on simulated unit tables.

    uv run models/f3/validate.py                 # the smoke grid: 6 cells, 200 replicates each
    uv run models/f3/validate.py --reps 10 --cells H0c_f0.3_k2

Each replicate simulates a unit table (units_sim.py), lets the estimator find its own first appearance
and reference window, and records for the reported quantities whether they cover the truth:
- the origin sets under H0c and H0m at each f_min read-out: whether the set contains the true origin t0
  (`cover_set`, the reported grid set with each boundary widened to the next grid point), and whether
  the test at t0 itself does not reject (`cover_exact`; its statistic `lr0` is stored, so other
  critical values can be applied afterwards). `applicable` is the largest read-out for which the
  hypothesis a >= f_min on (tau, t0] is true (none for a comb);
  Sets use the estimator's critical value, envelope.exact_count_crit (5.99 when no older unit detected);
  the summary also applies chi-square(1) (3.84), its one-sided value (2.71) and 5.99 to the stored lr0;
- f*_H(t0) >= the true abar(t0), for the classes H that contain the true history, under the estimator's
  critical value and (suffix _chi2) under chi-square(1) for comparison. A zero-exposure result makes no
  claim and counts as covering: coverage is over all replicates, with no conditioning on where the first
  appearance fell (docs/f3-shape.md); the non-trivial share is reported beside it. The estimator measures
  intensity relative to its reference window, which is wherever the first appearance falls and need not
  have a = 1 when the history is below 1 for some stages after tau0; the truth is therefore
  abar_rel = abar_true / a_ref, with a_ref the exposure-weighted mean of the true path over the realised
  reference units' true ages (both are recorded). A set is valid for t0 where abar_rel's path is at
  least f_min on (tau, t0], read the same way;
- informativeness: unbounded sets, the older endpoint, the share of the domain excluded, and the four
  states of f*_H(t0).
Replicates whose t0 lies at or below the estimated tau are `trivial`: the null is vacuous, the set
contains t0 by construction and f* has zero exposure. Both coverages (all and non-trivial) are reported;
the acceptance rule applies to coverage over all replicates.

Also here: the two-stage acceptance rule for the full grid (stage1, stage2, pass_probability).
Outputs: out/validation_smoke.csv (one row per cell), out/validation_smoke_reps.csv (one row per
replicate) and out/validation_smoke.meta.json (seeds, settings, hashes). Replicate j of cell c descends
from SeedSequence(ROOT_SEED, spawn_key=(c, j)): child 0 simulates, child 1 draws the stage boundaries.
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
AGE_DRAWS = 60
NODES = 48
READOUTS = (1.0, 0.1, 0.01)
CLASSES = ("H0c", "H0m", "H0", "logistic", "H1")
# fixed comparators for the estimator's own critical value (`count`, envelope.exact_count_crit of the older
# detections at t0): chi-square(1), its one-sided value, the rule of three.
CRITS = {"chi2_1": float(stats.chi2.ppf(0.95, 1)), "one_sided": float(stats.chi2.ppf(0.90, 1)), "zero_count": -2 * math.log(0.05)}
FSTAR_TOL = 1e-3
CHI2_CLASSES = ("H0c", "H0m", "H0", "H1")

CELLS = [
    dict(name="H0c_f1.0_k2", history="H0c", f=1.0, k=2.0, scale=0.05),
    dict(name="H0c_f0.3_k2", history="H0c", f=0.3, k=2.0, scale=0.05),
    dict(name="H0c_f0.3_kinf", history="H0c", f=0.3, k=math.inf, scale=0.05),
    dict(name="H0m_f0.3_d6_k2", history="H0m", f=0.3, delay=6.0, k=2.0, scale=0.05),
    dict(name="H0_duty0.3_k2", history="H0", f=0.3, k=2.0, scale=0.05),
    dict(name="logistic_g0.5_h11.6_k2", history="logistic", g=0.5, h=11.6, k=2.0, scale=0.05),
]
for _i, _c in enumerate(CELLS):
    _c.update(id=_i, t0=476.0, tau0=452.8, p=(0.12, 0.04))


# --- the acceptance rule for the full grid -------------------------------------------------------

FLOOR = 0.93


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


def stage2(successes: int, n: int = 2000) -> str:
    """The pooled 2,000 of a borderline cell passes if its lower limit exceeds the floor."""
    return "pass" if lower_limit(successes, n) > FLOOR else "fail"


def pass_probability(coverage: float, n1: int = 1000, n2: int = 1000) -> float:
    """P(a cell with this true coverage passes the two-stage rule)."""
    k1 = np.arange(n1 + 1)
    pm1 = stats.binom.pmf(k1, n1, coverage)
    total = 0.0
    need = next(s for s in range(n1 + n2 + 1) if stage2(s, n1 + n2) == "pass")
    for k, p in zip(k1, pm1):
        verdict = stage1(int(k), n1)
        if verdict == "pass":
            total += p
        elif verdict == "borderline":
            total += p * stats.binom.sf(need - k - 1, n2, coverage)
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
    design = us.Design(p=tuple(cell["p"]), k=cell["k"], scale=cell["scale"])
    spec = ev.Spec(age_draws=AGE_DRAWS, nodes=NODES, cluster_shape_k=cell["k"], readouts=READOUTS)
    return truth, design, spec


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
    s = us.simulate(truth, design, age, sim.child_seed(ss, 0))
    try:
        pr = ev.Problem(s.units, spec, age, sim.child_seed(ss, 1))
    except ev.NoFirstAppearance:
        return dict(no_tau=True)
    T0 = truth.t0
    r_true = s.r[pr.calibrated]
    ref = (s.units.old <= pr.s_star) & (s.units.young >= pr.s_star - spec.reference_stages + 1) & np.isin(s.units.cls, pr.calibrated)
    a_ref = float((s.r[s.units.cls[ref]] * truth.path(s.t_true[ref])).sum() / s.r[s.units.cls[ref]].sum())
    n_det = pr.n_older_detections(T0)
    crit_alt = ev.exact_count_crit(n_det)
    out = dict(
        no_tau=False,
        tau=pr.tau_nom,
        trivial=T0 <= pr.tau_nom,
        n_ref=pr.n_ref,
        n_old=pr.n_old,
        n_dropped=pr.n_dropped_uncalibrated,
        n_old_detected=int(pr.od.sum()),
        n_old_detected_at_t0=n_det,
        crit_alt=crit_alt,
        a_ref=a_ref,
        r_hat_1=pr.r_ref[0],
        r_hat_2=pr.r_ref[1] if pr.n_cls > 1 else math.nan,
    )
    for cls, back in (("H0c", 0.0), ("H0m", max(spec.delays_ma))):
        floor = truth.min_intensity(back, start=pr.tau_nom) / a_ref
        out[f"fmin_applicable_{cls}"] = max((f for f in READOUTS if f <= floor + 1e-9), default=math.nan)
    grid = pr.grid(STEP)
    tab = pr.origin_tables(grid)
    domain = spec.domain_ma[1]
    for cls in ("H0c", "H0m"):
        for f in READOUTS:
            key = f"{cls}_{f:g}"
            o = pr.origin_set(tab, cls, f)
            out[f"cover_set_{key}"] = bool(o.contains(T0))
            lr0 = 0.0 if T0 <= pr.tau_nom else pr.lr_origin(cls, T0, f)
            out[f"lr0_{key}"] = lr0
            out[f"unbounded_{key}"] = bool(o.unbounded)
            out[f"connected_{key}"] = bool(o.connected)
            out[f"endpoint_{key}"] = math.nan if o.unbounded else o.older_endpoint
            out[f"excluded_{key}"] = 0.0 if o.unbounded else (domain - o.older_endpoint) / (domain - pr.tau_nom)
    abar = pr.abar_truth(truth.path, T0, r_true) if not out["trivial"] else math.nan
    out["abar_true"] = abar
    out["abar_rel"] = abar / a_ref
    for cls in CLASSES:
        for suffix, crit in (("", None), ("_chi2", CRITS["chi2_1"])):
            if suffix and cls not in CHI2_CLASSES:
                continue
            b = pr.fstar(cls, T0, crit)
            out[f"fstar{suffix}_{cls}"] = b.value
            out[f"state{suffix}_{cls}"] = b.state
            claim = b.state != "zero-exposure" and np.isfinite(abar)
            covered = bool(b.value >= out["abar_rel"] - FSTAR_TOL) if claim else True
            out[f"fcover{suffix}_{cls}"] = covered if cls in truth.members else None
    b = pr.fstar("H1-no-ceiling", T0)
    out["state_H1-no-ceiling"] = b.state
    out["seconds"] = time.time() - t_start
    return out


# --- summary -------------------------------------------------------------------------------------


def mean(xs) -> float:
    xs = [float(x) for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return float(np.mean(xs)) if xs else math.nan


def median(xs) -> float:
    xs = [float(x) for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return float(np.median(xs)) if xs else math.nan


def summarise(cell: dict, rows: list[dict]) -> dict:
    ok = [r for r in rows if not r["error"] and not r["no_tau"]]
    nt = [r for r in ok if not r["trivial"]]
    out = {k: cell[k] for k in ("name", "history", "t0", "f", "k", "scale") if k in cell}
    out.update(
        delay=cell.get("delay", ""), n_rep=len(rows), n_error=sum(bool(r["error"]) for r in rows),
        n_no_tau=sum(bool(r.get("no_tau")) and not r["error"] for r in rows), n_valid=len(ok),
        frac_nontrivial=len(nt) / len(ok) if ok else math.nan,
        n_nontrivial=len(nt), tau_median=median(r["tau"] for r in ok), n_ref_median=median(r["n_ref"] for r in ok),
        a_ref_median=median(r["a_ref"] for r in ok), n_old_detected_median=median(r["n_old_detected_at_t0"] for r in ok),
        n_old_median=median(r["n_old"] for r in ok), seconds_per_rep=mean(r["seconds"] for r in ok),
    )
    for cls in ("H0c", "H0m"):
        for f in READOUTS:
            key = f"{cls}_{f:g}"
            out[f"cover_set_{key}"] = mean(r[f"cover_set_{key}"] for r in ok)
            out[f"cover_set_nontrivial_{key}"] = mean(r[f"cover_set_{key}"] for r in nt)
            for name, crit in CRITS.items():
                out[f"cover_exact_{name}_{key}"] = mean(r[f"lr0_{key}"] <= crit for r in ok)
                out[f"cover_exact_nontrivial_{name}_{key}"] = mean(r[f"lr0_{key}"] <= crit for r in nt)
            out[f"cover_exact_count_{key}"] = mean(r[f"lr0_{key}"] <= r["crit_alt"] for r in ok)
            out[f"cover_exact_nontrivial_count_{key}"] = mean(r[f"lr0_{key}"] <= r["crit_alt"] for r in nt)
            out[f"unbounded_{key}"] = mean(r[f"unbounded_{key}"] for r in ok)
            out[f"connected_{key}"] = mean(r[f"connected_{key}"] for r in ok)
            out[f"endpoint_median_{key}"] = median(r[f"endpoint_{key}"] for r in ok)
            out[f"excluded_{key}"] = mean(r[f"excluded_{key}"] for r in ok)
        app = [r for r in ok if not math.isnan(r[f"fmin_applicable_{cls}"])]
        out[f"cover_set_applicable_{cls}"] = mean(r[f"cover_set_{cls}_{r[f'fmin_applicable_{cls}']:g}"] for r in app)
        for name, crit in CRITS.items():
            out[f"cover_exact_applicable_{name}_{cls}"] = mean(r[f"lr0_{cls}_{r[f'fmin_applicable_{cls}']:g}"] <= crit for r in app)
            out[f"cover_exact_applicable_nontrivial_{name}_{cls}"] = mean(r[f"lr0_{cls}_{r[f'fmin_applicable_{cls}']:g}"] <= crit for r in app if not r["trivial"])
        out[f"cover_exact_applicable_count_{cls}"] = mean(r[f"lr0_{cls}_{r[f'fmin_applicable_{cls}']:g}"] <= r["crit_alt"] for r in app)
        out[f"cover_exact_applicable_nontrivial_count_{cls}"] = mean(r[f"lr0_{cls}_{r[f'fmin_applicable_{cls}']:g}"] <= r["crit_alt"] for r in app if not r["trivial"])
        out[f"n_applicable_{cls}"] = len(app)
    for cls in CLASSES:
        for suffix in ("", "_chi2") if cls in CHI2_CLASSES else ("",):
            key = f"fcover{suffix}_{cls}"
            out[key] = mean(r[key] for r in ok if r[key] is not None)
            out[f"fcover{suffix}_nontrivial_{cls}"] = mean(r[key] for r in nt if r[key] is not None)
            out[f"n_fcover{suffix}_nontrivial_{cls}"] = sum(r[key] is not None for r in nt)
        if cls in CHI2_CLASSES:
            out[f"fstar_chi2_median_{cls}"] = median(r[f"fstar_chi2_{cls}"] for r in nt if r[f"state_chi2_{cls}"] == "finite")
        for state in ev.STATES:
            out[f"state_{cls}_{state}"] = mean(r[f"state_{cls}"] == state for r in ok)
            out[f"state_nontrivial_{cls}_{state}"] = mean(r[f"state_{cls}"] == state for r in nt)
        out[f"fstar_median_{cls}"] = median(r[f"fstar_{cls}"] for r in nt if r[f"state_{cls}"] == "finite")
    for state in ev.STATES:
        out[f"state_H1-no-ceiling_{state}"] = mean(r["state_H1-no-ceiling"] == state for r in ok)
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
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--cells", nargs="*", default=None)
    ap.add_argument("--tag", default="smoke")
    args = ap.parse_args()
    cells = [c for c in CELLS if args.cells is None or c["name"] in args.cells]
    jobs = [(c, j) for c in cells for j in range(args.reps)]
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
        root_seed=ROOT_SEED, replicate_seed="SeedSequence(root_seed, spawn_key=(cell id, replicate)); child 0 simulates, child 1 draws boundaries",
        reps=args.reps, step_ma=STEP, age_draws=AGE_DRAWS, nodes=NODES, readouts=READOUTS, crits=CRITS, fstar_tol=FSTAR_TOL,
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
