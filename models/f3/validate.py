# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Validation harness for the F3 compatibility estimator (envelope.py), on simulated unit tables.

    uv run models/f3/validate.py --reps 5                          # all 21 cells, a quick development run
    uv run models/f3/validate.py --phase calibrate --reps 1000 --tag cal       # writes out/receipt_cal.json
    uv run models/f3/validate.py --phase accept --receipt out/receipt_cal.json --reps 1000 --tag acc1
    uv run models/f3/validate.py --phase accept --receipt out/receipt_cal.json --reps 1000 --start 1000 --tag acc2

Each replicate simulates a unit table (units_sim.py) and lets the estimator find its own first appearance
and reference window. Per replicate, for each history class that contains the truth (and always H0):
- f*_K at the true origin t0 and at T = 459.1 (Hooper's M2 maximum) when that lies above the estimated tau,
  with the state, and LR_K(abar_rel), the statistic at the true target; abar_rel = abar_true / a_ref.
  Both are weighted by the true rates and integrated over the unit age ranges of the analysis's age model:
  abar_true over the older units' ranges in (tau, t0], a_ref over the reference units' ranges (a_ref_realised,
  the mean at the hidden true ages, is stored as a diagnostic). The target is the expected encounter
  intensity: the path times older_report and (1 - confine) beyond tau0. Where those differ from the nominal
  path the statistic at the nominal target is stored too (lr_nominal_*). f* >= abar_rel - tol is the same
  event as LR_K(abar_rel) <= crit, so the summary applies any shift delta to the stored LR;
- the origin sets for H0c, H0m and H0 at each f_min read-out: whether the set contains t0 (`cover_set`, the
  grid set with each boundary widened to the next grid point), and the exact statistic at t0 (`lr0`).
  `applicable` is the largest read-out for which "a >= f_min" holds on (tau, t0] (H0c, H0) or on
  (tau, t0 - D] (H0m, D = h0m_lag_ma) for the true path relative to a_ref;
- informativeness: unbounded sets, the older endpoint, the share of the domain excluded, the states of f*;
- the convergence of every reported statistic (ok_*): a statistic converged when both its fits did.
Coverage is over every replicate. A replicate whose t0 lies at or below the estimated tau is `trivial` (the
null is vacuous, f* has zero exposure) and covers; so does one with no first appearance, where the analysis
makes no claim. An error, or a failed statistic (ok_* false), does not cover, whatever the shift. Coverage over
non-trivial replicates is a diagnostic, as is every coverage in a cell marked `diagnostic`. An origin read-out
is an acceptance quantity (`ocover_*`) in the cells whose truth satisfies its hypothesis for every possible
tau: the truth is in the class and a >= f_min on (tau0, t0 - D]. Elsewhere `cover_*_applicable` picks the
read-out from the simulated truth and is a diagnostic with its denominator. `delta95` is the smallest shift of
the critical value (not below 0) that brings a coverage to 0.95 in that batch: a tuning quantity, not a
population guarantee.

Phases. `dev` runs at shift 0 on root seed 20261030. `calibrate` runs at shift 0 on its own root seed and
writes a receipt: delta, the largest delta95 over every acceptance quantity of every acceptance cell, with the
code hashes. `accept` runs at the receipt's delta on a third root seed, after checking that the code still
matches the receipt, and gives each acceptance quantity its stage-1 verdict (`--start 1000` is stage 2).

Also here: the two-stage acceptance rule for the full grid (stage1, stage2, pass_probability).
Outputs: out/validation_<tag>.csv (one row per cell), out/validation_<tag>_reps.csv (one row per replicate)
and out/validation_<tag>.meta.json (seeds, settings, hashes). Replicate j of cell c descends from
SeedSequence(root seed of the phase, spawn_key=(c, j)); child 0 simulates.
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
ROOT_SEEDS = {"dev": 20261030, "calibrate": 20261101, "accept": 20261102}
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


def cell_objects(cell: dict, shift: float = 0.0):
    truth = us.Truth(**{k: cell[k] for k in ("history", "t0", "tau0", "f", "delay", "g", "h") if k in cell})
    design = us.Design(
        p=tuple(cell["p"]), class_weights=tuple(cell["class_weights"]), k=cell["k"], scale=cell["scale"],
        **{k: cell[k] for k in ("class_trend", "misassign", "older_report", "confine", "truth_scenario") if k in cell},
    )
    spec = ev.Spec(nodes=cell["nodes"], cluster_shape_k=cell.get("k_analysis", cell["k"]), readouts=READOUTS, crit_shift=shift)
    return truth, design, spec


def evaluated_classes(truth: us.Truth, spec: ev.Spec) -> list[str]:
    return [c for c in spec.classes if c in truth.members or c == "H0"]


def range_mean(path, lo: np.ndarray, hi: np.ndarray, step: float = 0.002) -> np.ndarray:
    """The mean of a path over each age range (lo, hi], by cumulative integration."""
    t = np.arange(lo.min() - step, hi.max() + 2 * step, step)
    cum = np.concatenate([[0.0], np.cumsum(path(t[:-1] + step / 2) * step)])
    return (np.interp(hi, t, cum) - np.interp(lo, t, cum)) / (hi - lo)


def replicate(job: tuple[dict, int, int, float]) -> dict:
    cell, rep, root, shift = job
    row = dict(cell=cell["name"], rep=rep, error="")
    try:
        row.update(_replicate(cell, rep, root, shift))
    except Exception as e:
        row.update(error=f"{type(e).__name__}: {e}", no_tau=False)
    return row


def _replicate(cell: dict, rep: int, root: int, shift: float) -> dict:
    t_start = time.time()
    truth, design, spec = cell_objects(cell, shift)
    ss = np.random.SeedSequence(root, spawn_key=(cell["id"], rep))
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
    a_ref = float(w_ref @ range_mean(effective, age.base[s.units.young[ref] - 1], age.base[s.units.old[ref]]) / w_ref.sum())
    a_ref_realised = float(w_ref @ effective(s.t_true[ref]) / w_ref.sum())
    trivial = T0 <= pr.tau
    n_det = pr.n_older_detections(T0)
    out = dict(
        no_tau=False, tau=pr.tau, trivial=trivial, n_ref=pr.n_ref, n_old=pr.n_old, n_dropped=pr.n_dropped_uncalibrated,
        n_old_detected=int(pr.od.sum()), n_old_detected_at_t0=n_det, crit_t0=pr.crit(T0), a_ref=a_ref, a_ref_realised=a_ref_realised,
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
        out[f"fstar_{cls}"], out[f"state_{cls}"], out[f"ok_fstar_{cls}"] = b.value, b.state, b.converged
        out[f"lr_{cls}"] = out[f"lr_nominal_{cls}"] = None
        out[f"ok_lr_{cls}"] = out[f"ok_lr_nominal_{cls}"] = True
        if not trivial and b.state != "zero-exposure" and np.isfinite(targets["rel"]):
            st = pr.lr(cls, T0, targets["rel"])
            out[f"lr_{cls}"], out[f"ok_lr_{cls}"] = st.value, st.converged
            if differs:
                st = pr.lr(cls, T0, targets["nominal"])
                out[f"lr_nominal_{cls}"], out[f"ok_lr_nominal_{cls}"] = st.value, st.converged
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
            out[f"cover_set_{key}"], out[f"ok_set_{key}"] = bool(o.contains(T0)), bool(o.ok.all())
            st = ev.Statistic(0.0, True, 0.0) if trivial else pr.origin_stat(cls, T0, f)
            out[f"lr0_{key}"], out[f"ok_lr0_{key}"] = st.value, st.converged
            out[f"unbounded_{key}"] = bool(o.unbounded)
            out[f"connected_{key}"] = bool(o.connected)
            out[f"endpoint_{key}"] = math.nan if o.unbounded else o.older_endpoint
            out[f"excluded_{key}"] = 0.0 if o.unbounded else (domain - o.older_endpoint) / (domain - pr.tau)
    out["n_fits"], out["n_flagged"], out["n_failed"] = pr.n_fits, pr.n_flagged, pr.n_failed
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


def coverage(rows: list[dict], covers) -> float:
    """Unconditional coverage over every replicate: no first appearance makes no claim and covers; an error
    does not."""
    return mean((not r["error"]) and (r["no_tau"] or bool(covers(r))) for r in rows)


def margins(rows: list[dict], margin, ok_key: str) -> list[float]:
    """Statistic minus critical value per replicate, for delta95: -inf where no claim is made, +inf for an
    error or a failed statistic (no shift covers them)."""
    return [math.inf if r["error"] else -math.inf if r["no_tau"] else math.inf if not r[ok_key] else margin(r) for r in rows]


def origin_readouts(truth: us.Truth, design: us.Design, spec: ev.Spec) -> dict[str, list[float]]:
    """The read-outs that are acceptance quantities in a cell: the truth is in the class and satisfies
    a >= f_min on (tau0, t0 - D] (D = h0m_lag_ma for H0m, else 0), so the hypothesis holds whatever tau."""
    effective = us.effective_path(truth.path(design), truth, design)
    out = {}
    for cls in ORIGIN_CLASSES:
        floor = us.min_intensity(effective, truth.tau0, truth.t0 - (spec.h0m_lag_ma if cls == "H0m" else 0.0))
        out[cls] = [f for f in READOUTS if cls in truth.members and f <= floor + 1e-9]
    return out


def acceptance_quantities(cell: dict) -> list[tuple[str, str, str]]:
    """(summary column, delta95 column, replicate count) for every acceptance quantity of a cell."""
    truth, design, spec = cell_objects(cell)
    out = [(f"fcover_{c}", f"delta95_f_{c}", c) for c in evaluated_classes(truth, spec) if c in truth.members]
    for cls, fs in origin_readouts(truth, design, spec).items():
        out += [(f"ocover_{cls}_{f:g}", f"delta95_ocover_{cls}_{f:g}", cls) for f in fs]
    return out if cell["kind"] == "acceptance" else []


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
        a_ref_median=median(r["a_ref"] for r in ok), a_ref_realised_median=median(r["a_ref_realised"] for r in ok),
        flagged_share=sum(r["n_flagged"] for r in ok) / fits if fits else math.nan,
        failed_share=sum(r["n_failed"] for r in ok) / fits if fits else math.nan,
        reps_with_failed_fit=sum(r["n_failed"] > 0 for r in ok),
        seconds_per_rep=mean(r["seconds"] for r in ok),
    )
    for cls in evaluated_classes(truth, spec):
        for label, key in (("", f"lr_{cls}"), ("_nominal", f"lr_nominal_{cls}")):
            if label and not any(r.get(key) is not None for r in ok):
                continue
            okk = f"ok_lr{label}_{cls}"
            margin = lambda r: -math.inf if r.get(key) is None else r[key] - r["crit_t0"]
            if cls in truth.members:
                out[f"fcover{label}_{cls}"] = coverage(rows, lambda r: margin(r) <= 0 and r[okk])
                out[f"fcover{label}_nontrivial_{cls}"] = mean(margin(r) <= 0 and r[okk] for r in nt)
                out[f"delta95{label}_f_{cls}"] = delta95(margins(rows, margin, okk))
                out[f"failed{label}_f_{cls}"] = sum(not r[okk] for r in ok)
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
    for cls, fs in origin_readouts(truth, design, spec).items():
        for f in fs:
            key = f"{cls}_{f:g}"
            margin = lambda r: r[f"lr0_{key}"] - r["crit_t0"]
            out[f"ocover_{key}"] = coverage(rows, lambda r: margin(r) <= 0 and r[f"ok_lr0_{key}"])
            out[f"delta95_ocover_{key}"] = delta95(margins(rows, margin, f"ok_lr0_{key}"))
            out[f"failed_ocover_{key}"] = sum(not r[f"ok_lr0_{key}"] for r in ok)
    for cls in ORIGIN_CLASSES:
        app = [r for r in ok if not math.isnan(r[f"fmin_applicable_{cls}"])]
        pick = lambda r, what: r[f"{what}_{cls}_{r[f'fmin_applicable_{cls}']:g}"]
        out[f"n_applicable_{cls}"] = len(app)
        out[f"cover_set_applicable_{cls}"] = mean(pick(r, "cover_set") for r in app)
        out[f"cover_exact_applicable_{cls}"] = mean(pick(r, "lr0") <= r["crit_t0"] for r in app)
        out[f"cover_exact_applicable_nontrivial_{cls}"] = mean(pick(r, "lr0") <= r["crit_t0"] for r in app if not r["trivial"])
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


def code_hashes() -> dict[str, str]:
    here = Path(__file__).resolve().parent
    return {f: sha256(here / f) for f in ("envelope.py", "units_sim.py", "validate.py", "sim.py")} | {
        "timescale.csv": sha256(sim.TIMESCALE_CSV), "effort.csv": sha256(us.EFFORT_CSV)}


def calibrated_shift(summary: list[dict], cells: list[dict]) -> tuple[float, list[dict]]:
    """delta: the largest delta95 over every acceptance quantity of every acceptance cell, with the list."""
    by_name = {s["name"]: s for s in summary}
    parts = [dict(cell=c["name"], quantity=col, delta95=by_name[c["name"]][d]) for c in cells for col, d, _ in acceptance_quantities(c)]
    return max((p["delta95"] for p in parts), default=0.0), parts


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=tuple(ROOT_SEEDS), default="dev")
    ap.add_argument("--receipt", type=Path, help="the calibration receipt (accept phase)")
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--start", type=int, default=0, help="index of the first replicate (stage 2 of acceptance uses 1000)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--cells", nargs="*", default=None)
    ap.add_argument("--tag", default="dev")
    args = ap.parse_args()
    shift, receipt = 0.0, None
    if args.phase == "accept":
        receipt = json.loads(args.receipt.read_text())
        if receipt["sha256"] != code_hashes():
            raise SystemExit("the code or inputs differ from the calibration receipt")
        shift = float(receipt["delta"])
    root = ROOT_SEEDS[args.phase]
    cells = [c for c in CELLS if args.cells is None or c["name"] in args.cells]
    jobs = [(c, j, root, shift) for c in cells for j in range(args.start, args.start + args.reps)]
    t0 = time.time()
    with Pool(args.workers) as pool:
        rows = pool.map(replicate, jobs, chunksize=1)
    elapsed = time.time() - t0
    OUT.mkdir(exist_ok=True)
    summary = [summarise(c, [r for r in rows if r["cell"] == c["name"]]) for c in cells]
    if args.phase == "accept" and args.start == 0 and args.reps == 1000:
        for c, srow in zip(cells, summary):
            for col, _, _ in acceptance_quantities(c):
                srow[f"verdict_{col}"] = stage1(round(srow[col] * args.reps), args.reps)
    write_csv(OUT / f"validation_{args.tag}.csv", summary)
    write_csv(OUT / f"validation_{args.tag}_reps.csv", rows)
    meta = dict(
        phase=args.phase, root_seed=root, replicate_seed="SeedSequence(root_seed, spawn_key=(cell id, replicate)); child 0 simulates",
        crit_shift=shift, receipt=str(args.receipt) if receipt else None,
        reps=args.reps, start=args.start, step_ma=STEP, readouts=READOUTS, m2_max=M2_MAX, spec=asdict(ev.Spec(crit_shift=shift)),
        stage2_pass=STAGE2_PASS, spread_flag=ev.SPREAD_FLAG, repair_iter=ev.REPAIR_ITER,
        cells=[{k: (str(v) if isinstance(v, float) and math.isinf(v) else v) for k, v in c.items()} for c in cells],
        design=asdict(us.Design()), elapsed_seconds=elapsed, workers=args.workers,
        python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, sha256=code_hashes(),
    )
    (OUT / f"validation_{args.tag}.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    if args.phase == "calibrate":
        delta, parts = calibrated_shift(summary, cells)
        rec = dict(delta=delta, calibration=f"validation_{args.tag}", root_seed=root, reps=args.reps, start=args.start,
                   cells=[c["name"] for c in cells], parts=parts, sha256=code_hashes())
        (OUT / f"receipt_{args.tag}.json").write_text(json.dumps(rec, indent=2) + "\n")
        print(f"delta = {delta:.4g} -> {OUT / f'receipt_{args.tag}.json'}")
    print(f"{len(jobs)} replicates in {elapsed:.0f} s -> {OUT / f'validation_{args.tag}.csv'}")


if __name__ == "__main__":
    main()
