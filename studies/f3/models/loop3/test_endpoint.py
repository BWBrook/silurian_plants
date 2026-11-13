import numpy as np
import pytest

from endpoint import PiecewiseRecovery, known_cutoff_bound, known_cutoff_summary, observed_range_bound


def flat(oldest=100.0):
    return PiecewiseRecovery(np.array([0.0, oldest]), np.array([1.0]))


def test_piecewise_exposure_and_inverse_are_vectorised():
    recovery = PiecewiseRecovery(np.array([0.0, 2.0, 5.0]), np.array([2.0, 0.5]))
    ages = np.array([0.0, 1.0, 2.0, 4.0, 5.0])
    exposure = np.array([0.0, 2.0, 4.0, 5.0, 5.5])
    assert np.allclose(recovery.exposure(ages), exposure)
    assert np.allclose(recovery.age_at(exposure), ages)


def test_known_cutoff_matches_uniform_order_statistic_formula():
    ages = np.array([10.0, 20.0, 30.0])
    got = known_cutoff_bound(ages, flat(), cutoff_ma=0.0)
    expected = 30.0 * 0.05 ** (-1.0 / 3.0)
    assert got.status == "bounded"
    assert got.bound_ma == pytest.approx(expected)
    summary = known_cutoff_summary(3, 30.0, flat(), cutoff_ma=0.0)
    assert summary == got


def test_observed_range_matches_marshall_formula():
    ages = np.array([10.0, 20.0, 30.0, 40.0])
    got = observed_range_bound(ages, flat())
    extension = (0.05 ** (-1.0 / 3.0) - 1.0) * 30.0
    assert got.bound_ma == pytest.approx(40.0 + extension)


def test_density_scale_does_not_change_age_bound():
    ages = np.array([10.0, 20.0, 30.0])
    one = known_cutoff_bound(ages, PiecewiseRecovery(np.array([0.0, 100.0]), np.array([1.0])), 0.0)
    seven = known_cutoff_bound(ages, PiecewiseRecovery(np.array([0.0, 100.0]), np.array([7.0])), 0.0)
    assert one.bound_ma == pytest.approx(seven.bound_ma)


def test_target_beyond_finite_recovery_domain_is_not_called_an_infinite_bound():
    got = known_cutoff_bound(np.array([8.0, 9.0]), flat(10.0), cutoff_ma=0.0)
    assert got.status == "beyond_domain"
    assert np.isnan(got.bound_ma)
    assert got.target_exposure > got.exposure_cap
    assert got.domain_max_ma == 10.0


def test_target_at_domain_boundary_is_distinguished_from_interior_bound():
    alpha = 0.05
    oldest = 10.0 * alpha ** 0.5
    got = known_cutoff_bound(np.array([oldest, oldest]), flat(10.0), cutoff_ma=0.0)
    assert got.status == "at_boundary"
    assert got.bound_ma == 10.0


def test_known_cutoff_coverage_under_declared_recovery():
    rng = np.random.default_rng(20261101)
    n, reps, truth = 8, 50_000, 80.0
    ages = rng.uniform(0.0, truth, size=(reps, n))
    bounds = ages.max(axis=1) * 0.05 ** (-1.0 / n)
    coverage = np.mean(bounds >= truth)
    assert coverage == pytest.approx(0.95, abs=0.004)


def test_known_cutoff_coverage_under_nonuniform_declared_recovery():
    rng = np.random.default_rng(20261102)
    recovery = PiecewiseRecovery(np.array([0.0, 20.0, 50.0, 100.0]), np.array([3.0, 0.2, 2.0]))
    n, reps, truth = 6, 50_000, 80.0
    truth_exposure = recovery.exposure(truth)
    oldest_exposure = rng.uniform(0.0, truth_exposure, size=(reps, n)).max(axis=1)
    targets = oldest_exposure * 0.05 ** (-1.0 / n)
    coverage = np.mean(targets >= truth_exposure)
    assert coverage == pytest.approx(0.95, abs=0.004)


def test_undefined_and_invalid_inputs_are_explicit():
    recovery = flat()
    assert known_cutoff_bound(np.array([]), recovery, 0.0).status == "undefined"
    assert observed_range_bound(np.array([5.0]), recovery).status == "undefined"
    assert observed_range_bound(np.array([5.0, 5.0]), recovery).status == "undefined"
    with pytest.raises(ValueError, match="strictly positive"):
        PiecewiseRecovery(np.array([0.0, 1.0]), np.array([0.0]))
    with pytest.raises(ValueError, match="cutoff"):
        known_cutoff_bound(np.array([4.0]), recovery, 5.0)
    with pytest.raises(ValueError, match="non-negative integer"):
        known_cutoff_summary(-1, 5.0, recovery, 0.0)
    with pytest.raises(ValueError, match="confidence"):
        observed_range_bound(np.array([4.0, 5.0]), recovery, 1.0)
