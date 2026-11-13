"""Model-conditional QSIM-801 persistent-floor calculation.

Vecoli et al. (2017) report 99 cryptospore taxon-by-sample presence marks in
17 of 20 samples and no observed trilete spores. A mark proves that at least
one cryptospore specimen was observed, but the source does not document the
search effort, stopping rule, recognition protocol, or independence needed to
treat every mark as a target-detectable independent trial.

The D=1 calculation is therefore conditional on a co-ascertainment model: each
mark lower-bounds an independently target-classifiable unit, target detection
remains active with relative effort h, and theta is a floor holding in every
informative sample. It is a limit on the minimum sample ratio, not a pooled
share and not an empirical qualification of the fossil frame. Divisors D=2
and D=4 are heuristic effective-M exponent sensitivities, not validated
clustering adjustments or confidence bounds.
"""

# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "numpy>=2.0",
#   "scipy>=1.14",
# ]
# ///

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
import time
from pathlib import Path
from typing import Sequence

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "studies" / "f3" / "models" / "loop2"))
from count_share import zero_target_stratified_bound  # noqa: E402

TABLE = ROOT / "studies" / "f3" / "data" / "units" / "loop2" / "replication" / "qsim801_vecoli2017_table1.csv"
SOURCE = ROOT / "library" / "closed" / "vecoli2017.pdf"
SCRIPT = Path(__file__).resolve()
COUNT_SHARE = ROOT / "studies" / "f3" / "models" / "loop2" / "count_share.py"
OUT = SCRIPT.parent / "out"
ALPHA = 0.05
EFFORTS = (1.0, 0.5, 0.25, 0.1)
EFFECTIVE_M_DIVISORS = (1.0, 2.0, 4.0)
SCENARIO_RATIOS = (0.01, 0.03, 0.1, 0.3, 1.0)
SIMULATION_REPS = 20_000
SIMULATION_SEED = 20_261_101
TOY_STRATA = 17
TOY_FLOORS = (0.01, 0.03, 0.05)
TOY_REGIMES = {
    "boundary": {
        "lambda_low": 2.0,
        "lambda_high": 10.0,
        "taxon_pool": 400,
        "dirichlet_concentration": 50.0,
    },
    "turnover": {
        "lambda_low": 5.0,
        "lambda_high": 300.0,
        "taxon_pool": 22,
        "dirichlet_concentration": 0.3,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _integer_marks(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError("marks must be a positive integer")
    value = int(value)
    if value <= 0:
        raise ValueError("marks must be a positive integer")
    return value


def _positive_finite(value: float, name: str, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise TypeError(f"{name} must be a finite number greater than {minimum}")
    value = float(value)
    if not math.isfinite(value) or value <= minimum:
        raise ValueError(f"{name} must be a finite number greater than {minimum}")
    return value


def _alpha(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise TypeError("alpha must be a finite number in (0, 1)")
    value = float(value)
    if not math.isfinite(value) or not 0.0 < value < 1.0:
        raise ValueError("alpha must be a finite number in (0, 1)")
    return value


def persistent_floor(sample_ratios: Sequence[float]) -> float:
    """Return the minimum sample ratio, deliberately not a mean."""
    if not sample_ratios:
        raise ValueError("sample_ratios must be non-empty")
    ratios = []
    for i, value in enumerate(sample_ratios):
        if isinstance(value, bool) or not isinstance(value, (int, float, np.integer, np.floating)):
            raise TypeError(f"sample_ratios[{i}] must be finite and non-negative")
        value = float(value)
        if not math.isfinite(value) or value < 0.0:
            raise ValueError(f"sample_ratios[{i}] must be finite and non-negative")
        ratios.append(value)
    return min(ratios)


def theta_upper(marks: int, h: float, effective_m_divisor: float = 1.0,
                alpha: float = ALPHA) -> float:
    """Invert the all-zero exponent calculation.

    Only ``effective_m_divisor=1`` is the analytic model-conditional bound.
    Larger divisors are explicitly heuristic effective-M sensitivities.
    """
    marks = _integer_marks(marks)
    h = _positive_finite(h, "h")
    divisor = _positive_finite(effective_m_divisor, "effective_m_divisor")
    if divisor < 1.0:
        raise ValueError("effective_m_divisor must be at least 1")
    alpha = _alpha(alpha)
    effective_m = marks / divisor
    return math.expm1(-math.log(alpha) / effective_m) / h


def zero_probability(marks: int, theta: float, h: float,
                     effective_m_divisor: float = 1.0) -> float:
    """Return the declared all-zero exponent probability or sensitivity."""
    marks = _integer_marks(marks)
    h = _positive_finite(h, "h")
    divisor = _positive_finite(effective_m_divisor, "effective_m_divisor")
    if divisor < 1.0:
        raise ValueError("effective_m_divisor must be at least 1")
    if isinstance(theta, bool) or not isinstance(theta, (int, float, np.integer, np.floating)):
        raise TypeError("theta must be finite and non-negative")
    theta = float(theta)
    if not math.isfinite(theta) or theta < 0.0:
        raise ValueError("theta must be finite and non-negative")
    return math.exp(-(marks / divisor) * math.log1p(h * theta))


def load() -> list[dict]:
    with TABLE.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != 20:
        raise ValueError(f"expected 20 QSIM-801 rows, found {len(rows)}")
    depths = set()
    for i, row in enumerate(rows, start=2):
        try:
            marks = int(row["cryptospore_marks"])
            triletes = int(row["trilete_reported"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid count field at CSV line {i}") from exc
        if marks < 0:
            raise ValueError(f"negative cryptospore marks at CSV line {i}")
        if triletes != 0:
            raise ValueError(f"non-zero trilete report at CSV line {i}")
        taxa_count = len(row["taxa"].split("; ")) if row["taxa"] else 0
        if marks != taxa_count:
            raise ValueError(f"mark/taxon mismatch at CSV line {i}: {marks} != {taxa_count}")
        if row["depth_ft"] in depths:
            raise ValueError(f"duplicate depth at CSV line {i}: {row['depth_ft']}")
        depths.add(row["depth_ft"])
        row["cryptospore_marks"] = marks
        row["trilete_reported"] = triletes
    return rows


def bounds(rows: list[dict]) -> list[dict]:
    counts = [row["cryptospore_marks"] for row in rows if row["cryptospore_marks"] > 0]
    marks = sum(counts)
    out = []
    for h in EFFORTS:
        module = zero_target_stratified_bound(counts, [h] * len(counts), ALPHA)["theta_upper"]
        for divisor in EFFECTIVE_M_DIVISORS:
            theta = theta_upper(marks, h, divisor)
            if divisor == 1.0 and not math.isclose(theta, module, rel_tol=1e-12):
                raise RuntimeError(f"analytic/module disagreement: {theta} != {module}")
            status = (
                "model-conditional-independent-unit-calculation"
                if divisor == 1.0
                else "heuristic-effective-M-exponent-sensitivity-not-confidence-bound"
            )
            out.append({
                "effort_ratio_h": h,
                "effective_M_divisor": divisor,
                "marks_M": marks,
                "effective_M": round(marks / divisor, 5),
                "positive_samples": len(counts),
                "theta_upper": round(theta, 5),
                "persistent_floor_share_limit": round(theta / (1.0 + theta), 5),
                "estimand": "minimum-sample-ratio-persistent-floor-not-pooled-share",
                "status": status,
            })
    return out


def scenarios(marks: int) -> list[dict]:
    return [{
        "persistent_ratio": theta,
        "effort_ratio_h": h,
        "p_zero_triletes_given_at_least_M": round(zero_probability(marks, theta, h), 6),
        "status": "model-conditional-independent-unit-probability",
    } for theta in SCENARIO_RATIOS for h in EFFORTS]


def known_answer(reps: int = SIMULATION_REPS, seed: int = SIMULATION_SEED) -> list[dict]:
    """Toy method stress, not qualification of the QSIM-801 observation frame.

    Seventeen strata retain the original stress design because they match the
    number of positive table rows. They are not treated as a random sample or
    as evidence that the microscopy observation contract holds.
    """
    reps = _integer_marks(reps)
    rng = np.random.default_rng(seed)
    out = []
    for regime, parameters in TOY_REGIMES.items():
        low = parameters["lambda_low"]
        high = parameters["lambda_high"]
        pool = parameters["taxon_pool"]
        concentration = parameters["dirichlet_concentration"]
        for floor in TOY_FLOORS:
            for heterogeneous in (False, True):
                false_reject = 0
                marks_sum = 0
                for _ in range(reps):
                    marks = 0
                    zero = True
                    for _ in range(TOY_STRATA):
                        lam = float(rng.uniform(low, high))
                        seen = rng.multinomial(
                            int(rng.poisson(lam)),
                            rng.dirichlet(np.full(pool, concentration)),
                        )
                        marks += int((seen > 0).sum())
                        theta = floor * (1.0 + rng.exponential(2.0)) if heterogeneous else floor
                        if rng.poisson(lam * theta) > 0:
                            zero = False
                    marks_sum += marks
                    if zero and marks > 0 and zero_probability(marks, floor, 1.0) <= ALPHA:
                        false_reject += 1
                out.append({
                    "regime": regime,
                    "true_floor": floor,
                    "heterogeneous_above_floor": heterogeneous,
                    "toy_strata": TOY_STRATA,
                    "replicates": reps,
                    "seed": seed,
                    "false_rejection_rate": round(false_reject / reps, 4),
                    "mean_marks": round(marks_sum / reps, 1),
                    "status": "toy-method-stress-not-real-frame-qualification",
                })
    return out


def write(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    started = time.perf_counter()
    tracked = (TABLE, SOURCE, SCRIPT, COUNT_SHARE)
    missing = [str(path) for path in tracked if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing bound source/code files: {missing}")
    pre_hashes = {str(path.relative_to(ROOT)): sha256(path) for path in tracked}

    rows = load()
    OUT.mkdir(exist_ok=True)
    bound_rows = bounds(rows)
    marks = bound_rows[0]["marks_M"]
    scenario_rows = scenarios(marks)
    simulation_rows = known_answer()
    output_paths = {
        "bounds": OUT / "qsim_share_bounds.csv",
        "scenarios": OUT / "qsim_share_scenarios.csv",
        "toy_method_stress": OUT / "qsim_share_known_answer.csv",
    }
    write(output_paths["bounds"], bound_rows)
    write(output_paths["scenarios"], scenario_rows)
    write(output_paths["toy_method_stress"], simulation_rows)

    post_hashes = {str(path.relative_to(ROOT)): sha256(path) for path in tracked}
    if pre_hashes != post_hashes:
        raise RuntimeError("source or code drifted during the QSIM-801 run")
    runtime_seconds = time.perf_counter() - started
    receipt = {
        "analysis": "QSIM-801 persistent-floor model calculation (Loop 2 close repair)",
        "status": "model-conditional-method-calculation-not-real-frame-qualification",
        "estimand": "minimum-sample-ratio-persistent-floor-not-pooled-share",
        "alpha": ALPHA,
        "marks_M": marks,
        "positive_samples": sum(row["cryptospore_marks"] > 0 for row in rows),
        "assumptions": {
            "D1": "co-ascertained independent target-classifiable units with fixed positive h",
            "D2_D4": "heuristic effective-M exponent sensitivities; not clustering confidence bounds",
        },
        "simulation": {
            "scope": "toy-method-stress-not-real-frame-qualification",
            "seed": SIMULATION_SEED,
            "replicates_per_cell": SIMULATION_REPS,
            "strata": TOY_STRATA,
            "floors": list(TOY_FLOORS),
            "regimes": TOY_REGIMES,
            "maximum_observed_false_rejection_rate": max(
                row["false_rejection_rate"] for row in simulation_rows
            ),
        },
        "runtime": {
            "seconds": round(runtime_seconds, 6),
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "pre_run_hashes": pre_hashes,
        "post_run_hashes": post_hashes,
        "input_drift": False,
        "output_hashes": {
            str(path.relative_to(ROOT)): sha256(path) for path in output_paths.values()
        },
    }
    receipt_path = OUT / "qsim_share_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "M": marks,
        "D1_h1": bound_rows[0],
        "toy_max_false_rejection": receipt["simulation"]["maximum_observed_false_rejection_rate"],
        "runtime_seconds": receipt["runtime"]["seconds"],
        "receipt": str(receipt_path.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
