"""Regression tests for the protocol-limited count-share method."""

import math

import numpy as np
import pytest
from scipy.stats import beta

from count_share import common_effort_bound, zero_target_stratified_bound


def test_zero_target_common_effort_matches_clopper_pearson_and_transform():
    got = common_effort_bound(0, 20, 2.0, alpha=0.05)
    q = float(beta.ppf(0.95, 1, 20))
    assert got.share_upper == pytest.approx(q)
    assert got.rate_ratio_upper == pytest.approx(q / (1 - q) / 2.0)
    assert got.biological_share_upper == pytest.approx(got.rate_ratio_upper / (1 + got.rate_ratio_upper))


def test_common_effort_monotonic_counts_and_effort():
    low = common_effort_bound(0, 30, 1.0)
    high = common_effort_bound(0, 60, 1.0)
    more_effort = common_effort_bound(0, 30, 2.0)
    assert high.rate_ratio_upper < low.rate_ratio_upper
    assert more_effort.rate_ratio_upper < low.rate_ratio_upper


def test_common_effort_nonzero_target_is_exact_cp_upper():
    got = common_effort_bound(3, 7, 1.5, alpha=0.1)
    q = float(beta.ppf(0.9, 4, 7))
    assert got.share_upper == pytest.approx(q)
    assert got.rate_ratio_upper == pytest.approx(q / (1 - q) / 1.5)


def test_common_effort_analytic_one_one_cp_upper():
    got = common_effort_bound(1, 1, 1.0, alpha=0.05)
    assert got.share_upper == pytest.approx(math.sqrt(1 - 0.05))


def test_zero_stratified_one_control_matches_expm1_formula():
    got = zero_target_stratified_bound([1], [1.0], alpha=0.05)
    assert got["theta_upper"] == pytest.approx(math.expm1(-math.log(0.05)))


@pytest.mark.parametrize("effort", [1e14, 1e16])
def test_zero_stratified_large_effort_uses_scaled_root(effort):
    got = zero_target_stratified_bound([1], [effort], alpha=0.05)
    expected = math.expm1(-math.log(0.05)) / effort
    assert got["theta_upper"] == pytest.approx(expected, rel=1e-12, abs=0.0)


def test_zero_stratified_finite_effort_range_is_guarded():
    got = zero_target_stratified_bound([1], [1e308], alpha=0.05)
    expected = math.expm1(-math.log(0.05)) / 1e308
    assert got["theta_upper"] == pytest.approx(expected, rel=1e-12, abs=0.0)
    unrepresentable = zero_target_stratified_bound([1], [5e-324], alpha=0.05)
    assert math.isinf(unrepresentable["theta_upper"])
    assert unrepresentable["status"] == "numerically-unbounded"


def test_zero_stratified_root_and_residual():
    got = zero_target_stratified_bound([10, 20], [0.5, 2.0], alpha=0.05)
    theta = got["theta_upper"]
    residual = 10 * math.log1p(0.5 * theta) + 20 * math.log1p(2.0 * theta) + math.log(0.05)
    assert got["status"] == "finite"
    assert residual == pytest.approx(0.0, abs=1e-11)


def test_zero_stratified_monotonic_information():
    one = zero_target_stratified_bound([10], [1.0])
    two = zero_target_stratified_bound([10, 10], [1.0, 1.0])
    assert two["theta_upper"] < one["theta_upper"]


def test_zero_effort_is_vacuous_and_empty_counts_are_vacuous():
    assert common_effort_bound(0, 30, 0.0).status == "unidentified-known-zero-effort"
    assert common_effort_bound(0, 30, None).status == "unidentified-unknown-effort-includes-zero"
    assert common_effort_bound(0, 0, 1.0).status == "unidentified-no-counts"
    with pytest.raises(ValueError, match="impossible"):
        common_effort_bound(1, 30, 0.0)
    got = zero_target_stratified_bound([10, 20], [0.0, 0.0])
    assert math.isinf(got["theta_upper"])
    assert got["biological_share_upper"] == 1.0
    assert zero_target_stratified_bound([], [])["status"] == "unidentified-no-known-positive-effort"


def test_zero_stratified_unknown_effort_stratum_contributes_no_information():
    known = zero_target_stratified_bound([10], [1.0])
    mixed = zero_target_stratified_bound([10, 20], [1.0, None])
    assert mixed["theta_upper"] == pytest.approx(known["theta_upper"])


@pytest.mark.parametrize("args", [
    (True, 2, 1.0), (1.5, 2, 1.0), (-1, 2, 1.0), (0, -2, 1.0), (0, 2, math.nan),
])
def test_common_invalid_counts_or_parameters(args):
    with pytest.raises((TypeError, ValueError)):
        common_effort_bound(*args)


def test_zero_invalid_inputs_and_mismatched_lengths():
    with pytest.raises((TypeError, ValueError)):
        zero_target_stratified_bound([1.2], [1.0])
    with pytest.raises((TypeError, ValueError)):
        zero_target_stratified_bound([1], [math.nan])
    with pytest.raises(ValueError):
        zero_target_stratified_bound([1], [1.0, 2.0])
