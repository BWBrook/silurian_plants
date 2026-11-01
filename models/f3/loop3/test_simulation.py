import numpy as np
import pytest

import histories
import simulation


def test_observed_locality_age_counts_are_nested():
    counts = simulation.observed_counts()
    assert counts["B0"] >= counts["B1"] >= counts["B2"] > 0


def test_wilson_interval_contains_observed_fraction():
    low, high = simulation.wilson(95, 100)
    assert low < 0.95 < high
    assert np.isnan(simulation.wilson(0, 0)[0])


def test_matched_flat_known_cutoff_has_nominal_coverage():
    row = simulation.simulate_cell("B2", 30, "flat", "flat", 445.0, 445.0, "exact", "test",
                                   n_reps=30_000, seed=1)
    assert abs(row["coverage_including_no_claim"] - 0.95) < 0.006


def test_stage_envelope_is_never_younger_than_exact_bound():
    recovery = histories.load_histories()["flat"]
    ages = simulation.sample_ages(recovery, 445.0, 30, 1_000, np.random.default_rng(2))
    exact = simulation.evaluate_draws(ages, recovery, 445.0, "exact", 30)
    censored = simulation.evaluate_draws(ages, recovery, 445.0, "stage_envelope", 30)
    assert censored["median_reported_bound_ma"] >= exact["median_reported_bound_ma"]
    assert censored["coverage_including_no_claim"] >= exact["coverage_including_no_claim"]


def test_counting_four_duplicates_as_independent_causes_severe_undercoverage():
    row = simulation.simulate_cell("B2", 40, "flat", "flat", 445.0, 445.0, "exact", "test",
                                   n_reps=30_000, seed=3, duplicate_factor=4)
    assert row["coverage_including_no_claim"] < 0.65


def test_known_delay_adjustment_restores_recovery_endpoint_coverage_for_lineage():
    raw = simulation.simulate_cell("B2", 30, "flat", "flat", 432.0, 452.0, "exact", "test",
                                   n_reps=30_000, seed=4)
    adjusted = simulation.simulate_cell("B2", 30, "flat", "flat", 432.0, 452.0, "exact", "test",
                                        n_reps=30_000, seed=4, delay_adjustment_ma=20.0)
    assert raw["coverage_including_no_claim"] < 0.1
    assert abs(adjusted["coverage_including_no_claim"] - 0.95) < 0.006


def test_fixed_delay_shifts_bound_and_domain_without_changing_bounded_status():
    recovery = histories.load_histories()["flat"]
    n = 30
    exposure_factor = (1 - simulation.CONFIDENCE) ** (-1 / n)
    oldest = histories.YOUNG + (460.0 - histories.YOUNG) / exposure_factor
    ages = np.full((1, n), oldest)

    result = simulation.evaluate_draws(
        ages,
        recovery,
        target_truth_ma=480.0,
        age_mode="exact",
        n_reported=n,
        delay_adjustment_ma=20.0,
    )

    assert result["n_bounded"] == 1
    assert result["claim_frequency"] == 1.0
    assert result["median_reported_bound_ma"] == pytest.approx(480.0)
    assert result["recoverability_domain_max_ma"] == pytest.approx(469.4)
    assert result["reported_target_domain_max_ma"] == pytest.approx(489.4)
