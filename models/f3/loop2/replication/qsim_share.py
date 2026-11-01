"""QSIM-801 within-sample trilete-share bound from Vecoli et al. (2017).

Observation contract (sprint 2, Claude):
- one examination per sample (Vecoli et al.'s 20 Liège preparations) produced both the
  cryptospore occurrence marks of their Table 1 and the study-wide statement that no trilete
  spore was observed (printed p.330);
- every mark is at least one examined cryptospore dispersal unit, so the marks lower-bound the
  examined land-spore units; Le Hérissé et al.'s counts are not used;
- h is the probability that a trilete unit present in the examined material is recovered and
  recorded, relative to a cryptospore unit (recognition and preparation parity at h = 1).

Estimand: a persistent floor theta on the trilete:cryptospore unit ratio, i.e. theta_i >= theta in
every positive sample.  Conditional on each sample's land-spore total N_i, zero triletes has
probability prod (1 + h theta_i)^(-N_i) <= (1 + h theta)^(-M) with M = sum of marks <= sum N_i,
so rejecting theta when (1 + h theta)^(-M) <= alpha is a valid level-alpha test of the floor.
It is not a bound on a mean ratio: heterogeneity raises the all-zero probability.
Within-sample clustering is carried as a design effect that divides M.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "models" / "f3" / "loop2"))
from count_share import zero_target_stratified_bound  # noqa: E402

TABLE = ROOT / "data" / "units" / "loop2" / "replication" / "qsim801_vecoli2017_table1.csv"
SOURCE = ROOT / "library" / "closed" / "vecoli2017.pdf"
OUT = Path(__file__).resolve().parent / "out"
ALPHA = 0.05
EFFORTS = (1.0, 0.5, 0.25, 0.1)
DESIGN_EFFECTS = (1, 2, 4)
SCENARIO_RATIOS = (0.01, 0.03, 0.1, 0.3, 1.0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load() -> list[dict]:
    with TABLE.open() as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["cryptospore_marks"] = int(r["cryptospore_marks"])
        assert int(r["trilete_reported"]) == 0
        assert r["cryptospore_marks"] == (len(r["taxa"].split("; ")) if r["taxa"] else 0)
    return rows


def theta_upper(marks: int, h: float, design_effect: float = 1.0) -> float:
    m_eff = marks / design_effect
    return (ALPHA ** (-1.0 / m_eff) - 1.0) / h


def bounds(rows: list[dict]) -> list[dict]:
    counts = [r["cryptospore_marks"] for r in rows if r["cryptospore_marks"] > 0]
    m = sum(counts)
    out = []
    for h in EFFORTS:
        module = zero_target_stratified_bound(counts, [h] * len(counts), ALPHA)["theta_upper"]
        for de in DESIGN_EFFECTS:
            t = theta_upper(m, h, de)
            if de == 1:
                assert math.isclose(t, module, rel_tol=1e-7), (t, module)
            out.append({"effort_ratio_h": h, "design_effect": de, "marks_M": m,
                        "positive_samples": len(counts), "theta_upper": round(t, 5),
                        "recovered_share_upper": round(h * t / (1 + h * t), 5)})
    return out


def scenarios(m: int) -> list[dict]:
    return [{"persistent_ratio": th, "effort_ratio_h": h,
             "p_zero_triletes_given_at_least_M": round((1 + h * th) ** (-m), 6)}
            for th in SCENARIO_RATIOS for h in EFFORTS]


def known_answer(rows: list[dict], reps: int = 20000, seed: int = 20261101) -> list[dict]:
    """False-rejection rate of the persistent-floor test when the true floor holds.

    Regime "boundary": small samples and a large, even species pool, so marks nearly equal the
    examined count (the least favourable case for the marks lower bound) and all-zero outcomes
    are common near the declared bound.  Regime "turnover": Vecoli-like richness, where marks
    fall far below the examined count.
    """
    rng = np.random.default_rng(seed)
    n_pos = sum(1 for r in rows if r["cryptospore_marks"] > 0)
    regimes = {"boundary": (2.0, 10.0, 400, 50.0), "turnover": (5.0, 300.0, 22, 0.3)}
    out = []
    for regime, (lo, hi, pool, conc) in regimes.items():
        for floor in (0.01, 0.03, 0.05):
            for hetero in (False, True):
                false_reject = 0
                marks_sum = 0
                for _ in range(reps):
                    marks, zero = 0, True
                    for _ in range(n_pos):
                        lam = float(rng.uniform(lo, hi))
                        seen = rng.multinomial(int(rng.poisson(lam)), rng.dirichlet(np.full(pool, conc)))
                        marks += int((seen > 0).sum())
                        th = floor * (1.0 + rng.exponential(2.0)) if hetero else floor
                        if rng.poisson(lam * th) > 0:
                            zero = False
                    marks_sum += marks
                    if zero and (1 + floor) ** (-marks) <= ALPHA:
                        false_reject += 1
                out.append({"regime": regime, "true_floor": floor, "heterogeneous_above_floor": hetero,
                            "replicates": reps, "false_rejection_rate": round(false_reject / reps, 4),
                            "mean_marks": round(marks_sum / reps, 1)})
    return out


def write(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    rows = load()
    OUT.mkdir(exist_ok=True)
    b = bounds(rows)
    m = b[0]["marks_M"]
    s = scenarios(m)
    k = known_answer(rows)
    write(OUT / "qsim_share_bounds.csv", b)
    write(OUT / "qsim_share_scenarios.csv", s)
    write(OUT / "qsim_share_known_answer.csv", k)
    receipt = {
        "analysis": "QSIM-801 persistent-floor trilete:cryptospore bound (Loop 2 sprint 2)",
        "alpha": ALPHA,
        "marks_M": m,
        "inputs": {str(TABLE.relative_to(ROOT)): sha256(TABLE),
                   "library/closed/vecoli2017.pdf": sha256(SOURCE) if SOURCE.exists() else "not-held-here"},
        "code": {str(Path(__file__).relative_to(ROOT)): sha256(Path(__file__)),
                 "models/f3/loop2/count_share.py": sha256(ROOT / "models/f3/loop2/count_share.py")},
        "max_false_rejection": max(r["false_rejection_rate"] for r in k),
        "status": "unqualified empirical bound under declared parity; known-answer check of the marks lower bound",
    }
    (OUT / "qsim_share_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"M": m, "h1": b[0], "max_false_rejection": receipt["max_false_rejection"]}, indent=1))


if __name__ == "__main__":
    main()
