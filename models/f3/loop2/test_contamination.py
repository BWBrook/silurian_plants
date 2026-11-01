"""Regression tests for the unqualified Murzuq contamination diagnostic."""

import math
from pathlib import Path

import numpy as np
import pytest

import contamination as ct


def test_frozen_frame_reconstructs_primary_counts_and_all_older_zeros():
    for allocation in ("stage", "pre459"):
        frame = ct.build_frame(allocation)
        assert frame.tau == pytest.approx(443.1)
        assert (frame.n_reference, frame.d_reference, frame.n_older) == (59, 51, 28)
        assert len(frame.wells) == 5


@pytest.mark.parametrize("allocation", ["stage", "pre459"])
def test_g1_b0_matches_frozen_envelope_h0c_and_window_lrs(allocation):
    rho, f = 0.5, 0.1
    frame = ct.build_frame(allocation)
    problem = ct.envelope_problem(allocation, rho)
    cases = [
        ("independent-uniform", "tau", 459.1, "H0c"),
        ("independent-uniform", 459.1, 462.6, "H0"),
    ]
    for chronology, start, end, cls in cases:
        q = ct.target_weights(frame, chronology, start, end)
        null = ct.profile(rho * f, 0.0, q, frame)
        alt = ct.profile(0.0, 0.0, q, frame)
        got = max(0.0, 2.0 * (alt.log_likelihood - null.log_likelihood))
        expected = problem.origin_stat(cls, end, f, None if start == "tau" else float(start)).value
        assert got == pytest.approx(expected, abs=5e-7)


def test_point_age_likelihood_matches_gamma_laplace_identity():
    well = ct.Well("W", 1, 4, ("o1", "o2"), (1.0, 2.0), (460.0, 461.0), (460.0, 461.0))
    frame = ct.Frame("test", 443.1, (well,), 96, 2.0)
    q = (np.ones(2),)
    r, a, b, k = 0.7, 0.2, 0.3, 2.0
    # One reference detection: (1-exp(-ru)); three reference zeros and
    # two point-age older zeros: exp[-ru*2(a+b)].
    c = 3.0 + 2.0 * (a + b)
    probability = (k / (k + r * c)) ** k - (k / (k + r * (c + 1.0))) ** k
    assert ct.loglik(r, a, b, q, frame) == pytest.approx(math.log(probability), abs=3e-7)


def test_parameterisation_uses_a_and_b_not_only_their_sum_except_when_all_q_one():
    well = ct.Well("W", 1, 3, ("o1",), (1.0,), (459.0,), (469.0,))
    frame = ct.Frame("test", 443.1, (well,), 192, 2.0)
    all_one = (np.ones(1),)
    partial = (np.array([0.4]),)
    assert ct.loglik(0.6, 0.2, 0.3, all_one, frame) == pytest.approx(
        ct.loglik(0.6, 0.4, 0.1, all_one, frame), abs=1e-12
    )
    assert ct.loglik(0.6, 0.2, 0.3, partial, frame) != pytest.approx(
        ct.loglik(0.6, 0.4, 0.1, partial, frame), abs=1e-5
    )
    a1, b1 = ct.transformed_parameters(0.5, 0.4, 0.25, 0.2)
    a2, b2 = ct.transformed_parameters(0.2, 1.0, 0.0, 0.2)
    assert (a1, b1) == pytest.approx((0.04, 0.15))
    assert (a2, b2) == pytest.approx((0.04, 0.0))


def test_shared_quantile_is_deterministic_and_checks_age_depth_order():
    frame = ct.build_frame("stage")
    q = ct.target_weights(frame, "shared-quantile-0.5", 459.1, 467.1)
    assert all(set(x).issubset({0.0, 1.0}) for x in q)
    bad = ct.Frame(
        "bad", 443.1,
        (ct.Well("W", 1, 2, ("o1", "o2"), (1.0, 2.0), (460.0, 450.0), (470.0, 460.0)),),
        96, 2.0,
    )
    with pytest.raises(ValueError, match="age-depth order"):
        ct.target_weights(bad, "shared-quantile-0.5", 459.1, 469.4)


def test_high_contamination_baseline_is_flagged_as_model_conflict():
    frame = ct.build_frame("stage")
    q = ct.target_weights(frame, "independent-uniform", "tau", 459.1)
    ref = ct.profile_reference(frame, q)
    f0 = ct.profile(0.0, 0.9, q, frame)
    result = ct._comparison(frame, q, 0.0, 0.9, ref, f0, f0, 0.05)
    assert result["model_conflict"]
    assert result["comparison_status"] == "model-conflict"


def test_break_even_checks_monotonicity_and_retains_no_root_cases():
    frame = ct.build_frame("stage")
    q = ct.target_weights(frame, "independent-uniform", 459.1, 462.6)
    f0 = ct.profile(0.0, 0.0, q, frame)
    got = ct._break_even(frame, q, f0, 0.05)
    assert got["monotone"]
    assert got["root_status"] in {"finite", "no-root-through-a1"}
    if got["root_status"] == "finite":
        candidate = ct.profile(got["effective_a_critical"], 0.0, q, frame)
        lr = 2 * (f0.log_likelihood - candidate.log_likelihood)
        assert lr == pytest.approx(-2 * math.log(0.05), abs=2e-6)


def test_break_even_output_declares_kappa_zero_scope():
    _, rows = ct._evaluate_group(("stage", "independent-uniform", "origin459.1"))
    assert rows
    assert all(r["break_even_scope"] == "no-older-contamination" for r in rows)
    assert all(r["kappa"] == 0 and r["b_kappa_1_minus_g"] == 0 for r in rows)


def test_declared_factorial_has_5760_rows_and_manifest_scope_is_local():
    assert len(ct.declared_rows()) == 5760
    source = Path(ct.__file__).read_text()
    assert "count_share.py" not in source
    assert "engine_sensitivity" not in source


def test_f3_design_override_cannot_redirect_the_frozen_source(monkeypatch, tmp_path):
    monkeypatch.setattr(ct.designs, "DESIGNS", tmp_path / "other.toml")
    with pytest.raises(RuntimeError, match="frozen declaration"):
        ct.build_frame("stage")


@pytest.mark.parametrize(
    "call",
    [
        lambda f, q: ct.loglik(0.0, 0.1, 0.1, q, f),
        lambda f, q: ct.loglik(9.0, 0.1, 0.1, q, f),
        lambda f, q: ct.loglik(0.5, -0.1, 0.1, q, f),
        lambda f, q: ct.loglik(0.5, 0.1, math.nan, q, f),
        lambda f, q: ct.profile(0.1, -0.1, q, f),
        lambda f, q: ct.loglik(0.5, 0.1, 0.1, (np.array([1.2]),), f),
        lambda f, q: ct.transformed_parameters(0.0, 0.5, 0.1, 0.2),
        lambda f, q: ct.transformed_parameters(1.0, 0.0, 0.1, 0.2),
    ],
)
def test_invalid_inputs_fail(call):
    frame = ct.Frame("test", 443.1, (ct.Well("W", 1, 2, ("o",), (1.0,), (460.0,), (461.0,)),), 96, 2.0)
    q = (np.array([0.5]),)
    with pytest.raises((TypeError, ValueError)):
        call(frame, q)
