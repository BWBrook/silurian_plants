# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas"]
# ///
"""Matched validation and stress tests for the Loop 3 fixed-history endpoint procedure."""

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

import histories

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
HORIZONS = ROOT / "studies/f3/data/macro/horizons_reviewed.csv"
EFFORT = ROOT / "studies/f3/data/macro/effort_reviewed.csv"
SEED = 20261101
N_REPS = 3_000
CONFIDENCE = 0.95
TRUTHS = (432.0, 445.0, 458.2)
CATEGORIES = ("B0", "B1", "B2")
HISTORY_NAMES = (
    "flat", "decline25", "decline10", "pbdb_all", "pbdb_plant_excluded",
    "pbdb_excluded_decline10",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def observed_counts(path: Path = HORIZONS) -> dict[str, int]:
    h = pd.read_csv(path)
    h = h[h.reading.isin(["all", "main"]) & h.eligible_primary & (h.min_ma >= histories.YOUNG)]
    units = h.groupby(["locality", "min_ma", "max_ma"], dropna=False)[["b0", "b1", "b2"]].any()
    return {name.upper(): int(units[name].sum()) for name in ("b0", "b1", "b2")}


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return float("nan"), float("nan")
    p = successes / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    half = z * np.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return float(centre - half), float(centre + half)


def sample_ages(recovery, truth_ma: float, n_independent: int, n_reps: int, rng) -> np.ndarray:
    low = recovery.exposure(histories.YOUNG)
    high = recovery.exposure(truth_ma)
    exposure = rng.uniform(low, high, size=(n_reps, n_independent))
    return recovery.age_at(exposure)


def endpoint_arrays(n_reported: int, oldest_ma: np.ndarray, recovery, confidence: float = CONFIDENCE):
    alpha = 1 - confidence
    cutoff_exposure = recovery.exposure(histories.YOUNG)
    target = cutoff_exposure + (recovery.exposure(oldest_ma) - cutoff_exposure) * alpha ** (-1 / n_reported)
    tolerance = 64 * np.finfo(float).eps * max(1.0, recovery.exposure_cap)
    bounded = target < recovery.exposure_cap - tolerance
    at_boundary = np.abs(target - recovery.exposure_cap) <= tolerance
    beyond = target > recovery.exposure_cap + tolerance
    bound = np.full(len(oldest_ma), np.nan)
    bound[bounded] = recovery.age_at(target[bounded])
    bound[at_boundary] = recovery.edges_ma[-1]
    return bound, bounded, at_boundary, beyond


def evaluate_draws(
    ages: np.ndarray,
    fitted_recovery,
    target_truth_ma: float,
    age_mode: str,
    n_reported: int,
    delay_adjustment_ma: float = 0.0,
) -> dict:
    if age_mode == "exact":
        oldest = ages.max(axis=1)
        n_for_bound = n_reported
    elif age_mode == "stage_envelope":
        young, old = histories.stage_bounds(ages)
        oldest = old.max(axis=1)
        n_for_bound = int(np.min((young >= histories.YOUNG).sum(axis=1)))
    else:
        raise ValueError(f"unknown age mode: {age_mode}")
    bound, bounded, at_boundary, beyond = endpoint_arrays(n_for_bound, oldest, fitted_recovery)
    if delay_adjustment_ma:
        bound = np.where(bounded | at_boundary, bound + delay_adjustment_ma, np.nan)
    recoverability_domain_max = float(fitted_recovery.edges_ma[-1])
    reported_target_domain_max = recoverability_domain_max + delay_adjustment_ma
    covered = (~bounded) | (bound >= target_truth_ma)
    bounded_covered = bounded & (bound >= target_truth_ma)
    n_covered = int(covered.sum())
    n_bounded = int(bounded.sum())
    all_ci = wilson(n_covered, len(bound))
    bounded_ci = wilson(int(bounded_covered.sum()), n_bounded)
    finite = bound[np.isfinite(bound)]
    return {
        "n_for_bound": n_for_bound,
        "recoverability_domain_max_ma": recoverability_domain_max,
        "reported_target_domain_max_ma": reported_target_domain_max,
        "n_bounded": n_bounded,
        "n_at_boundary": int(at_boundary.sum()),
        "n_beyond_domain": int(beyond.sum()),
        "claim_frequency": n_bounded / len(bound),
        "beyond_domain_frequency": float(beyond.mean()),
        "coverage_including_no_claim": n_covered / len(bound),
        "coverage_wilson_low": all_ci[0],
        "coverage_wilson_high": all_ci[1],
        "coverage_conditional_bounded": int(bounded_covered.sum()) / n_bounded if n_bounded else float("nan"),
        "bounded_coverage_wilson_low": bounded_ci[0],
        "bounded_coverage_wilson_high": bounded_ci[1],
        "median_reported_bound_ma": float(np.median(finite)) if len(finite) else float("nan"),
        "bound_q05_ma": float(np.quantile(finite, 0.05)) if len(finite) else float("nan"),
        "bound_q95_ma": float(np.quantile(finite, 0.95)) if len(finite) else float("nan"),
    }


def simulate_cell(
    category: str,
    n_reported: int,
    true_history: str,
    fitted_history: str,
    recovery_truth_ma: float,
    target_truth_ma: float,
    age_mode: str,
    scenario: str,
    n_reps: int,
    seed: int,
    duplicate_factor: int = 1,
    delay_adjustment_ma: float = 0.0,
) -> dict:
    declared = histories.load_histories()
    n_independent = int(np.ceil(n_reported / duplicate_factor))
    rng = np.random.default_rng(seed)
    independent = sample_ages(declared[true_history], recovery_truth_ma, n_independent, n_reps, rng)
    ages = np.repeat(independent, duplicate_factor, axis=1)[:, :n_reported]
    result = evaluate_draws(ages, declared[fitted_history], target_truth_ma, age_mode, n_reported,
                            delay_adjustment_ma)
    return {
        "scenario": scenario,
        "category": category,
        "true_history": true_history,
        "fitted_history": fitted_history,
        "age_mode": age_mode,
        "duplicate_factor": duplicate_factor,
        "delay_adjustment_ma": delay_adjustment_ma,
        "recovery_truth_ma": recovery_truth_ma,
        "target_truth_ma": target_truth_ma,
        "n_reported": n_reported,
        "n_independent": n_independent,
        "n_reps": n_reps,
        **result,
    }


def run(n_reps: int = N_REPS) -> list[dict]:
    counts = observed_counts()
    specs = []
    for category in CATEGORIES:
        for history in HISTORY_NAMES:
            for truth in TRUTHS:
                for age_mode in ("exact", "stage_envelope"):
                    specs.append((category, counts[category], history, history, truth, truth, age_mode,
                                  "matched", 1, 0.0))
        for true_history, fitted_history in (("flat", "decline10"), ("decline10", "flat")):
            for truth in TRUTHS:
                specs.append((category, counts[category], true_history, fitted_history, truth, truth, "exact",
                              "history_mismatch", 1, 0.0))
        for duplicate_factor in (2, 4):
            specs.append((category, counts[category], "flat", "flat", 445.0, 445.0, "exact",
                          "duplicated_horizons", duplicate_factor, 0.0))
        for lineage_truth in (442.0, 452.0):
            delay = lineage_truth - 432.0
            specs.append((category, counts[category], "flat", "flat", 432.0, lineage_truth, "exact",
                          "recoverability_delay_unadjusted", 1, 0.0))
            specs.append((category, counts[category], "flat", "flat", 432.0, lineage_truth, "exact",
                          "recoverability_delay_adjusted", 1, delay))
    rows = []
    for i, spec in enumerate(specs):
        seed = int(np.random.SeedSequence(SEED, spawn_key=(i,)).generate_state(1)[0])
        rows.append(simulate_cell(*spec[:8], n_reps=n_reps, seed=seed,
                                  duplicate_factor=spec[8], delay_adjustment_ma=spec[9]))
    return rows


def input_hashes():
    paths = [
        ROOT / "data/timescale.csv",
        ROOT / "studies/f3/data/macro/build_receipt.json",
        HORIZONS,
        EFFORT,
        HERE / "endpoint.py",
        HERE / "histories.py",
        Path(__file__).resolve(),
    ]
    return {str(path.relative_to(ROOT)): sha256(path) for path in paths}


def write(rows: list[dict], inputs: dict[str, str]):
    OUT.mkdir(exist_ok=True)
    csv_path = OUT / "simulation_results.csv"
    fields = list(rows[0])
    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: round(value, 6) if isinstance(value, float) else value for key, value in row.items()})
    receipt = {
        "root_seed": SEED,
        "n_reps_per_cell": N_REPS,
        "confidence": CONFIDENCE,
        "conditioning": "fixed n; no empirical calibration claim",
        "delay_adjustment": (
            "a fixed lag shifts both a finite recoverability bound and its reported target domain; "
            "endpoint status and claim frequency remain those of the recoverability calculation"
        ),
        "truth_ages_ma": TRUTHS,
        "history_names": HISTORY_NAMES,
        "observed_locality_age_counts": observed_counts(),
        "inputs": inputs,
        "outputs": {str(csv_path.relative_to(ROOT)): sha256(csv_path)},
        "cells": len(rows),
        "numpy": np.__version__,
        "pandas": pd.__version__,
    }
    receipt_path = OUT / "simulation_receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
    return csv_path, receipt_path


def main():
    before = input_hashes()
    rows = run()
    if input_hashes() != before:
        raise RuntimeError("simulation input changed during the run")
    paths = write(rows, before)
    print(json.dumps({"rows": len(rows), "counts": observed_counts(), "outputs": [str(p) for p in paths]}))


if __name__ == "__main__":
    main()
