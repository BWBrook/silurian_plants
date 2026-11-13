import numpy as np

from endpoint import known_cutoff_summary
from histories import load_histories, YOUNG
from suppression_sensitivity import step_history


def test_suppression_beyond_oldest_support_leaves_record_distribution_unchanged():
    base = load_histories()["flat"]
    step = step_history(base, 426.7, .1)
    observed = np.array([395., 410., 419., 425., 426.7])
    assert np.allclose(base.exposure(observed), step.exposure(observed))
    assert step.exposure(445.) < base.exposure(445.)


def test_factor_one_matches_baseline_and_late_break_is_a_null_control():
    base = load_histories()["pbdb_all"]
    fit = known_cutoff_summary(48, 426.7, base, YOUNG)
    for multiplier in [1., .1, .01]:
        recovery = step_history(base, 432.9, multiplier)
        other = known_cutoff_summary(48, 426.7, recovery, YOUNG)
        assert np.isclose(fit.bound_ma, other.bound_ma)


def test_past_suppression_has_independent_analytic_answer():
    base = load_histories()["flat"]
    rec = step_history(base, 426.7, .1)
    result = known_cutoff_summary(48, 426.7, rec, YOUNG)
    expected = 426.7 + (426.7 - YOUNG) * (.05 ** (-1 / 48) - 1) / .1
    assert np.isclose(result.bound_ma, expected)
    assert known_cutoff_summary(48, 426.7, step_history(base, 426.7, .01), YOUNG).status == "beyond_domain"
