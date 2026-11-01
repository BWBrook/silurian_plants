import math

import pytest

import qsim_share as qs


def test_source_table_reconstructs_99_marks_in_17_positive_rows():
    rows = qs.load()
    marks = [row["cryptospore_marks"] for row in rows]
    assert len(rows) == 20
    assert sum(value > 0 for value in marks) == 17
    assert sum(marks) == 99


def test_analytic_D1_root_is_exact_and_matches_declared_value():
    limit = qs.theta_upper(99, 1.0)
    assert math.isclose(limit, 0.03072240652208702, rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(qs.zero_probability(99, limit, 1.0), qs.ALPHA,
                        rel_tol=0.0, abs_tol=2e-16)


def test_persistent_floor_is_not_a_mean_or_an_every_sample_ceiling():
    ratios = [0.0, 1.0]
    assert qs.persistent_floor(ratios) == 0.0
    assert sum(ratios) / len(ratios) == 0.5
    assert not all(ratio <= 0.03072240652208702 for ratio in ratios)


def test_D4_h_point_one_does_not_reject_theta_one():
    probability = qs.zero_probability(99, theta=1.0, h=0.1, effective_m_divisor=4.0)
    assert math.isclose(probability, 0.09452159518084427, rel_tol=0.0, abs_tol=1e-15)
    assert probability > qs.ALPHA
    assert qs.theta_upper(99, h=0.1, effective_m_divisor=4.0) > 1.0


@pytest.mark.parametrize(
    ("args", "error"),
    [
        ((0, 1.0), ValueError),
        ((99, 0.0), ValueError),
        ((99, 1.0, 0.5), ValueError),
        ((99, 1.0, 1.0, 1.0), ValueError),
        ((99.5, 1.0), TypeError),
    ],
)
def test_theta_upper_rejects_impossible_inputs(args, error):
    with pytest.raises(error):
        qs.theta_upper(*args)


@pytest.mark.parametrize("ratios", [[], [-0.1, 0.2], [math.inf], [math.nan]])
def test_persistent_floor_rejects_impossible_inputs(ratios):
    with pytest.raises(ValueError):
        qs.persistent_floor(ratios)


def test_output_rows_separate_bound_from_heuristic_sensitivities():
    rows = qs.bounds(qs.load())
    assert "recovered_share_upper" not in rows[0]
    assert rows[0]["status"] == "model-conditional-independent-unit-calculation"
    assert all(
        row["status"] == "heuristic-effective-M-exponent-sensitivity-not-confidence-bound"
        for row in rows if row["effective_M_divisor"] > 1.0
    )
    assert all("not-pooled-share" in row["estimand"] for row in rows)
