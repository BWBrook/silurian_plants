# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Validation harness for the F3 compatibility estimator (envelope.py), on simulated unit tables.

    uv run models/f3/validate.py --reps 5                          # all cells, a quick development run
    uv run models/f3/validate.py --phase calibrate --reps 1000 --tag cal       # writes out/receipt_cal.json
    uv run models/f3/validate.py --phase accept --receipt out/receipt_cal.json --reps 1000 --tag acc1
    uv run models/f3/validate.py --phase accept --receipt out/receipt_cal.json --stage1 out/verdicts_acc1.json --tag acc2

Each replicate simulates a unit table (units_sim.py) and lets the estimator find its own first appearance
and reference window. Per replicate, for each history class that contains the truth (and always H0):
- f*_K at the true origin t0 and at T = 459.1 (Hooper's M2 maximum) when that lies above the estimated tau,
  with the state, convergence and spread, and LR_K(abar_rel), the statistic at the true target;
  abar_rel = abar_true / a_ref. Both are weighted by the true rates and integrated over the unit age ranges of
  the analysis's age model: abar_true over the older units' ranges in (tau, t0], a_ref over the reference
  units' ranges (a_ref_realised, the mean at the hidden true ages, is stored as a diagnostic). The target is
  the expected encounter intensity: the path times older_report and (1 - confine) beyond tau0. Where those
  differ from the nominal path the statistic at the nominal target is stored too (lr_nominal_*);
- the origin sets for H0c, H0m and H0 at each f_min read-out: whether the set contains t0 (`cover_set`, the
  grid set with each boundary widened to the next grid point), and the exact statistic at t0 (`lr0`).
  `applicable` is the largest read-out for which "a >= f_min" holds on (tau, t0] (H0c, H0) or on
  (tau, t0 - D] (H0m, D = h0m_lag_ma) for the true path relative to a_ref;
- informativeness: unbounded sets, the older endpoint, the share of the domain excluded, the states of f*;
- the convergence of every reported output (ok_*): a statistic converged when both its fits did, a bound when
  every statistic of its root search did, a set when every grid point did.

Coverage is over every replicate. A replicate whose t0 lies at or below the estimated tau is `trivial` (the
null is vacuous, f* has zero exposure) and covers; so does one with no first appearance, where the analysis
makes no claim. An error, or a failed output, does not cover, whatever the shift. Two coverages are kept apart:
- delivered coverage (`fcover_*`, `ocover_*`, the acceptance quantities): the reported output succeeded and
  contains the truth. For f*, the bound and the statistic at the truth both converged and LR_K(abar_rel) <=
  crit; for the origin set, the set and the statistic at t0 both converged, LR <= crit at t0 and the grid set
  contains t0. f* >= abar_rel is the same event as LR_K(abar_rel) <= crit up to the root tolerance, which is
  what lets the summary shift the critical value on the stored LR; `mismatch_f_*` counts the replicates where
  the two disagree beyond that tolerance, and `mismatch_ocover_*` those where the exact test covers t0 and the
  grid set does not. Both should be zero; `ocover_set_*` is the grid set's own coverage;
- truth-point test coverage (`*_test_*`): the statistic at the truth alone, whatever became of the output.
  A diagnostic of the test, not of the reported interval.
Coverage over non-trivial replicates is a diagnostic, as is every coverage in a cell marked `diagnostic`. An
origin read-out is an acceptance quantity in the cells whose truth satisfies its hypothesis for every possible
tau: the truth is in the class and a >= f_min on (tau0, t0 - D]. Elsewhere `cover_*_applicable` picks the
read-out from the simulated truth and is a diagnostic with its denominator. Medians, shares and states count
converged outputs only, with the failures counted beside them. `delta_*` is the smallest shift of the critical
value (not below 0) that brings a delivered coverage to CALIBRATION_TARGET in that batch: a tuning quantity,
not a population guarantee.

Phases. `dev` runs at shift 0 on root seed 20261030. `calibrate` runs replicates 0..N1-1 of every cell at shift
0 on its own root seed and writes a receipt: delta, the largest delta_* over every acceptance quantity of every
acceptance cell, the protocol and the code hashes. `accept` refuses a receipt that does not match the code, the
protocol or the full set of acceptance quantities, or whose delta is not finite and non-negative; then it runs
at delta on a third root seed. Stage 1 (replicates 0..N1-1) writes out/verdicts_<tag>.json with each acceptance
quantity's count and verdict. Stage 2 (`--stage1`) checks that file against the receipt and the code, reruns
only the cells with a borderline quantity on replicates N1..N1+N2-1, pools the counts and issues the final
verdicts. The grid is accepted when every acceptance quantity passes.

Also here: the two-stage acceptance rule (stage1, stage2, pass_probability).
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
CALIBRATION_TARGET = 0.955
N1, N2 = 1000, 1000
ROOT_TOL = 2e-3

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
    ("D7", "diagnostic", dict(history="H0c", f=0.3, shared_age=True)),
    ("D8", "diagnostic", dict(history="H0c", f=0.3, shared_age=True, cluster_mean=10.0)),
    ("D9", "diagnostic", dict(history="H0c", f=0.3, cluster_mean=10.0)),
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


def stage1(successes: int, n: int = N1) -> str:
    """'pass' if the lower limit exceeds the floor, 'fail' if the upper limit is below it, else 'borderline'."""
    if lower_limit(successes, n) > FLOOR:
        return "pass"
    return "fail" if upper_limit(successes, n) < FLOOR else "borderline"


def stage2(successes: int) -> str:
    """The pooled 2,000 of a borderline cell passes at STAGE2_PASS successes: the threshold that holds the
    overall chance of passing a cell at the floor to 0.05 once the interim look is allowed for."""
    return "pass" if successes >= STAGE2_PASS else "fail"


def pass_probability(coverage: float, n1: int = N1, n2: int = N2) -> float:
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
        **{k: cell[k] for k in ("cluster_mean", "class_trend", "misassign", "older_report", "confine", "truth_scenario", "shared_age") if k in cell},
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
        out[f"fstar_{cls}"], out[f"state_{cls}"], out[f"ok_fstar_{cls}"], out[f"spread_fstar_{cls}"] = b.value, b.state, b.converged, b.spread
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
            out[f"fstar459_{cls}"], out[f"state459_{cls}"], out[f"ok459_{cls}"], out[f"spread459_{cls}"] = b.value, b.state, b.converged, b.spread
        else:
            out[f"fstar459_{cls}"], out[f"state459_{cls}"], out[f"ok459_{cls}"], out[f"spread459_{cls}"] = math.nan, "", True, 0.0
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


def shift_to_target(margins: list[float], target: float = CALIBRATION_TARGET) -> float:
    """The smallest shift of the critical value, not below 0, at which at least the target share of the margins
    (statistic minus critical value; -inf for a replicate that makes no claim) are covered."""
    if not margins:
        return math.nan
    return max(0.0, float(np.sort(margins)[math.ceil(target * len(margins)) - 1]))


def coverage(rows: list[dict], covers) -> float:
    """Unconditional coverage over every replicate: no first appearance makes no claim and covers; an error
    does not."""
    return mean((not r["error"]) and (r["no_tau"] or bool(covers(r))) for r in rows)


def margins(rows: list[dict], margin, ok) -> list[float]:
    """Statistic minus critical value per replicate, for shift_to_target: -inf where no claim is made, +inf for
    an error or a failed output (no shift covers them)."""
    return [math.inf if r["error"] else -math.inf if r["no_tau"] else math.inf if not ok(r) else margin(r) for r in rows]


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
    """(summary column, shift column, class) for every acceptance quantity of a cell."""
    truth, design, spec = cell_objects(cell)
    out = [(f"fcover_{c}", f"delta_f_{c}", c) for c in evaluated_classes(truth, spec) if c in truth.members]
    for cls, fs in origin_readouts(truth, design, spec).items():
        out += [(f"ocover_{cls}_{f:g}", f"delta_ocover_{cls}_{f:g}", cls) for f in fs]
    return out if cell["kind"] == "acceptance" else []


def grid_quantities() -> set[tuple[str, str]]:
    return {(c["name"], col) for c in CELLS for col, _, _ in acceptance_quantities(c)}


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
        bound_ok = lambda r: r[f"ok_fstar_{cls}"]
        for label, key, target in (("", f"lr_{cls}", "abar_rel"), ("_nominal", f"lr_nominal_{cls}", "abar_nominal_rel")):
            if label and not any(r.get(key) is not None for r in ok):
                continue
            test_ok = lambda r: r[f"ok_lr{label}_{cls}"]
            delivered_ok = lambda r: test_ok(r) and bound_ok(r)
            margin = lambda r: -math.inf if r.get(key) is None else r[key] - r["crit_t0"]
            if cls in truth.members:
                out[f"fcover{label}_{cls}"] = coverage(rows, lambda r: margin(r) <= 0 and delivered_ok(r))
                out[f"fcover{label}_test_{cls}"] = coverage(rows, lambda r: margin(r) <= 0 and test_ok(r))
                out[f"fcover{label}_nontrivial_{cls}"] = mean(margin(r) <= 0 and delivered_ok(r) for r in nt)
                out[f"delta{label}_f_{cls}"] = shift_to_target(margins(rows, margin, delivered_ok))
                out[f"failed{label}_f_{cls}"] = sum(not delivered_ok(r) for r in ok)
                out[f"mismatch{label}_f_{cls}"] = sum(
                    (margin(r) <= 0) != (r[f"fstar_{cls}"] >= r[target]) and abs(r[f"fstar_{cls}"] - r[target]) > ROOT_TOL * (1 + r[target])
                    for r in nt if delivered_ok(r) and r.get(key) is not None and np.isfinite(r[target])
                    and r[f"state_{cls}"] in ("finite", "ceiling-limited"))
        out[f"member_{cls}"] = cls in truth.members
        out[f"outside_{cls}"] = mean(r["abar_rel"] > (spec.h1_ceiling if cls == "H1" else 1.0) + 1e-9 for r in nt)
        good, good_nt = [r for r in ok if bound_ok(r)], [r for r in nt if bound_ok(r)]
        at459 = [r for r in ok if r[f"state459_{cls}"]]
        good459 = [r for r in at459 if r[f"ok459_{cls}"]]
        out[f"failed_fstar_{cls}"] = len(ok) - len(good)
        out[f"flagged_fstar_{cls}"] = mean(not bound_ok(r) or r[f"spread_fstar_{cls}"] > ev.SPREAD_FLAG for r in ok)
        out[f"failed459_{cls}"] = len(at459) - len(good459)
        out[f"flagged459_{cls}"] = mean(not r[f"ok459_{cls}"] or r[f"spread459_{cls}"] > ev.SPREAD_FLAG for r in at459)
        for state in ev.STATES:
            out[f"state_{cls}_{state}"] = mean(r[f"state_{cls}"] == state for r in good)
            out[f"state_nontrivial_{cls}_{state}"] = mean(r[f"state_{cls}"] == state for r in good_nt)
            out[f"state459_{cls}_{state}"] = mean(r[f"state459_{cls}"] == state for r in good459)
        out[f"fstar_median_{cls}"] = median(r[f"fstar_{cls}"] for r in good_nt if r[f"state_{cls}"] == "finite")
        out[f"fstar459_median_{cls}"] = median(r[f"fstar459_{cls}"] for r in good459 if r[f"state459_{cls}"] == "finite")
    for state in ev.STATES:
        out[f"state_H1-no-ceiling_{state}"] = mean(r["state_H1-no-ceiling"] == state for r in ok)
    for cls, fs in origin_readouts(truth, design, spec).items():
        for f in fs:
            key = f"{cls}_{f:g}"
            margin = lambda r: r[f"lr0_{key}"] - r["crit_t0"]
            test_ok = lambda r: r[f"ok_lr0_{key}"]
            delivered_ok = lambda r: test_ok(r) and r[f"ok_set_{key}"]
            out[f"ocover_{key}"] = coverage(rows, lambda r: margin(r) <= 0 and delivered_ok(r) and r[f"cover_set_{key}"])
            out[f"ocover_set_{key}"] = coverage(rows, lambda r: r[f"ok_set_{key}"] and r[f"cover_set_{key}"])
            out[f"ocover_test_{key}"] = coverage(rows, lambda r: margin(r) <= 0 and test_ok(r))
            out[f"delta_ocover_{key}"] = shift_to_target(margins(rows, margin, delivered_ok))
            out[f"failed_ocover_{key}"] = sum(not delivered_ok(r) for r in ok)
            out[f"mismatch_ocover_{key}"] = sum(margin(r) <= 0 and delivered_ok(r) and not r[f"cover_set_{key}"] for r in ok)
    for cls in ORIGIN_CLASSES:
        app = [r for r in ok if not math.isnan(r[f"fmin_applicable_{cls}"])]
        pick = lambda r, what: r[f"{what}_{cls}_{r[f'fmin_applicable_{cls}']:g}"]
        exact = lambda r: pick(r, "ok_lr0") and pick(r, "lr0") <= r["crit_t0"]
        out[f"n_applicable_{cls}"] = len(app)
        out[f"cover_set_applicable_{cls}"] = mean(pick(r, "ok_set") and pick(r, "cover_set") for r in app)
        out[f"cover_exact_applicable_{cls}"] = mean(exact(r) for r in app)
        out[f"cover_exact_applicable_nontrivial_{cls}"] = mean(exact(r) for r in app if not r["trivial"])
        for f in READOUTS:
            key = f"{cls}_{f:g}"
            good = [r for r in ok if r[f"ok_set_{key}"]]
            out[f"failed_set_{key}"] = len(ok) - len(good)
            out[f"unbounded_{key}"] = mean(r[f"unbounded_{key}"] for r in good)
            out[f"connected_{key}"] = mean(r[f"connected_{key}"] for r in good)
            out[f"endpoint_median_{key}"] = median(r[f"endpoint_{key}"] for r in good)
            out[f"excluded_{key}"] = mean(r[f"excluded_{key}"] for r in good)
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


# --- the calibration receipt and the acceptance verdicts -----------------------------------------


def protocol() -> dict:
    """What a binding calibration must have been: replicates 0..N1-1 on the calibration seed, at the target."""
    return dict(root_seed=ROOT_SEEDS["calibrate"], start=0, reps=N1, target=CALIBRATION_TARGET)


def calibrated_shift(summary: list[dict], cells: list[dict]) -> tuple[float, list[dict]]:
    """delta: the largest delta_* over every acceptance quantity of every acceptance cell, with the list."""
    by_name = {s["name"]: s for s in summary}
    parts = [dict(cell=c["name"], quantity=col, delta=by_name[c["name"]][d]) for c in cells for col, d, _ in acceptance_quantities(c)]
    return max((p["delta"] for p in parts), default=0.0), parts


def check_receipt(rec: dict) -> float:
    """The receipt's delta, once it is shown to apply: the same code and inputs, the declared protocol, exactly
    the acceptance quantities of the whole grid, and a finite non-negative delta that is the largest of them."""
    problems = []
    if rec.get("sha256") != code_hashes():
        problems.append("the code or inputs differ from the calibration")
    problems += [f"{k} is {rec.get(k)!r}, not {v!r}" for k, v in protocol().items() if rec.get(k) != v]
    parts = rec.get("parts", [])
    keys = [(p["cell"], p["quantity"]) for p in parts]
    if len(keys) != len(set(keys)) or set(keys) != grid_quantities():
        problems.append("it does not cover exactly the acceptance quantities of the grid")
    delta = rec.get("delta")
    if not (isinstance(delta, (int, float)) and math.isfinite(delta) and delta >= 0):
        problems.append(f"delta {delta!r} is not finite and non-negative")
    elif parts and delta != max(p["delta"] for p in parts):
        problems.append("delta is not the largest of its parts")
    if problems:
        raise SystemExit("calibration receipt refused: " + "; ".join(problems))
    return float(delta)


def stage1_verdicts(cells: list[dict], summary: list[dict]) -> list[dict]:
    out = []
    for c, s in zip(cells, summary):
        for col, _, _ in acceptance_quantities(c):
            k = round(s[col] * s["n_rep"])
            v = stage1(k, N1)
            out.append(dict(cell=c["name"], quantity=col, k1=k, stage1=v, k2=None, pooled=None, final="pending" if v == "borderline" else v))
    return out


def stage2_cells(verdicts: list[dict]) -> list[str]:
    return list(dict.fromkeys(v["cell"] for v in verdicts if v["stage1"] == "borderline"))


def pooled_verdicts(verdicts: list[dict], summary: list[dict]) -> list[dict]:
    """Stage 2: each borderline quantity pools its N1 + N2 replicates; the others keep their stage-1 verdict."""
    by_name = {s["name"]: s for s in summary}
    out = []
    for v in verdicts:
        v = dict(v)
        if v["stage1"] == "borderline":
            s = by_name[v["cell"]]
            k2 = round(s[v["quantity"]] * s["n_rep"])
            v.update(k2=k2, pooled=v["k1"] + k2, final=stage2(v["k1"] + k2))
        out.append(v)
    return out


def grid_result(verdicts: list[dict]) -> str:
    finals = [v["final"] for v in verdicts]
    if {(v["cell"], v["quantity"]) for v in verdicts} != grid_quantities():
        return "incomplete"
    return "rejected" if "fail" in finals else "stage 2 needed" if "pending" in finals else "accepted"


def check_stage1(first: dict, receipt_sha: str) -> None:
    """Stage 2 continues only a complete stage 1 run on the same receipt and code."""
    problems = []
    if first.get("stage") != 1:
        problems.append("it is not a stage-1 verdict file")
    if first.get("receipt_sha256") != receipt_sha:
        problems.append("it used another receipt")
    if first.get("sha256") != code_hashes():
        problems.append("the code or inputs have changed since")
    if (first.get("root_seed"), first.get("start"), first.get("reps")) != (ROOT_SEEDS["accept"], 0, N1):
        problems.append("it did not run replicates 0..N1-1 on the acceptance seed")
    if first.get("result") == "incomplete":
        problems.append("it does not cover every acceptance quantity")
    if problems:
        raise SystemExit("stage 1 refused: " + "; ".join(problems))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", choices=tuple(ROOT_SEEDS), default="dev")
    ap.add_argument("--receipt", type=Path, help="the calibration receipt (accept phase)")
    ap.add_argument("--stage1", type=Path, help="stage 2 of acceptance: the stage-1 verdict file to complete")
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--start", type=int, default=0, help="index of the first replicate")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--cells", nargs="*", default=None)
    ap.add_argument("--tag", default="dev")
    args = ap.parse_args()
    root = ROOT_SEEDS[args.phase]
    cells = [c for c in CELLS if args.cells is None or c["name"] in args.cells]
    start, reps, shift, receipt_sha, first = args.start, args.reps, 0.0, None, None
    if args.phase == "accept":
        shift, receipt_sha = check_receipt(json.loads(args.receipt.read_text())), sha256(args.receipt)
        if args.stage1:
            first = json.loads(args.stage1.read_text())
            check_stage1(first, receipt_sha)
            names = stage2_cells(first["quantities"])
            cells, start, reps = [c for c in CELLS if c["name"] in names], N1, N2
    elif args.stage1:
        raise SystemExit("--stage1 belongs to the accept phase")
    jobs = [(c, j, root, shift) for c in cells for j in range(start, start + reps)]
    t0 = time.time()
    rows = []
    if jobs:
        with Pool(args.workers) as pool:
            rows = pool.map(replicate, jobs, chunksize=1)
    elapsed = time.time() - t0
    OUT.mkdir(exist_ok=True)
    summary = [summarise(c, [r for r in rows if r["cell"] == c["name"]]) for c in cells]
    if rows:
        write_csv(OUT / f"validation_{args.tag}.csv", summary)
        write_csv(OUT / f"validation_{args.tag}_reps.csv", rows)
    meta = dict(
        phase=args.phase, root_seed=root, replicate_seed="SeedSequence(root_seed, spawn_key=(cell id, replicate)); child 0 simulates",
        crit_shift=shift, receipt=str(args.receipt) if args.receipt else None, receipt_sha256=receipt_sha,
        stage1=str(args.stage1) if first else None, reps=reps, start=start, step_ma=STEP, readouts=READOUTS, m2_max=M2_MAX,
        spec=asdict(ev.Spec(crit_shift=shift)), calibration_target=CALIBRATION_TARGET, n1=N1, n2=N2, stage2_pass=STAGE2_PASS,
        spread_flag=ev.SPREAD_FLAG, repair_iter=ev.REPAIR_ITER,
        cells=[{k: (str(v) if isinstance(v, float) and math.isinf(v) else v) for k, v in c.items()} for c in cells],
        design=asdict(us.Design()), elapsed_seconds=elapsed, workers=args.workers,
        python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__, sha256=code_hashes(),
    )
    (OUT / f"validation_{args.tag}.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    if args.phase == "calibrate":
        delta, parts = calibrated_shift(summary, cells)
        rec = protocol() | dict(start=start, reps=reps, root_seed=root, delta=delta, calibration=f"validation_{args.tag}",
                                cells=[c["name"] for c in cells], parts=parts, sha256=code_hashes())
        (OUT / f"receipt_{args.tag}.json").write_text(json.dumps(rec, indent=2) + "\n")
        print(f"delta = {delta:.4g} -> {OUT / f'receipt_{args.tag}.json'}")
    verdicts = None
    if first is not None:
        verdicts = pooled_verdicts(first["quantities"], summary)
    elif args.phase == "accept" and start == 0 and reps == N1:
        verdicts = stage1_verdicts(cells, summary)
    if verdicts is not None:
        result = grid_result(verdicts)
        (OUT / f"verdicts_{args.tag}.json").write_text(json.dumps(dict(
            stage=2 if first else 1, result=result, receipt=str(args.receipt), receipt_sha256=receipt_sha,
            stage1=str(args.stage1) if first else None, root_seed=root, start=start, reps=reps, sha256=code_hashes(),
            quantities=verdicts), indent=2) + "\n")
        print(f"grid {result} -> {OUT / f'verdicts_{args.tag}.json'}")
    print(f"{len(jobs)} replicates in {elapsed:.0f} s")


if __name__ == "__main__":
    main()
