"""Checks of the real-design extensions: rate multipliers, numerical age ranges, the oldest-possible first
appearance, the window read-out and the M2 adapter.

    uv run --with pytest --with numpy --with scipy pytest models/f3/test_designs.py -p no:cacheprovider
"""

import math

import numpy as np
import pytest

import designs as dz
import envelope as ev
import screen

AGE = ev.AgeModel.load()
TS = AGE.timescale
S = TS.index
SPEC = ev.Spec(cluster_shape_k=math.inf, min_units_per_class=1, fa_rule="oldest-possible")
FAR = 559.0


def units(k, n, old_stage, m, mult=1.0, lo=math.nan, hi=math.nan, ref_young="Telychian", ref_old="Rhuddanian"):
    """k detections in n reference units (range ref_young..ref_old) and m empty older units in old_stage."""
    young = np.r_[np.full(n, S(ref_young)), np.full(m, S(old_stage))]
    old = np.r_[np.full(n, S(ref_old)), np.full(m, S(old_stage))]
    d = np.r_[np.ones(k), np.zeros(n - k), np.zeros(m)].astype(int)
    mu = np.r_[np.ones(n), np.broadcast_to(mult, m)]
    return ev.Units(young, old, np.zeros(n + m, int), np.zeros(n + m, int), d, mu,
                    np.r_[np.full(n, math.nan), np.full(m, lo)], np.r_[np.full(n, math.nan), np.full(m, hi)])


def test_oldest_possible_rule_sets_tau_at_the_oldest_stage_a_detection_can_occupy():
    u = units(7, 8, "Darriwilian", 5)
    assert ev.Problem(u, SPEC, AGE).tau == pytest.approx(AGE.base[S("Rhuddanian")])
    with pytest.raises(ev.NoFirstAppearance):
        ev.Problem(u, ev.Spec(cluster_shape_k=math.inf, min_units_per_class=1), AGE)


@pytest.mark.parametrize("rho,f", [(0.5, 0.8), (0.25, 1.0), (0.1, 1.0)])
def test_a_uniform_multiplier_rescales_the_constant_history(rho, f):
    """With empty older units, the constant path f at rate multiplier rho is the path rho f at 1."""
    a = ev.Problem(units(7, 8, "Darriwilian", 6, rho), SPEC, AGE).lr("H0c", FAR, f).value
    b = ev.Problem(units(7, 8, "Darriwilian", 6), SPEC, AGE).lr("H0c", FAR, rho * f).value
    assert a == pytest.approx(b, rel=1e-6, abs=1e-8)


def test_multipliers_enter_the_homogeneous_profile_as_effective_older_units():
    mult = np.array([1.0, 0.5, 0.25, 0.25, 2.0])
    pr = ev.Problem(units(13, 16, "Hirnantian", 5, mult), SPEC, AGE)
    for f in (0.2, 0.6, 1.0):
        assert pr.lr("H0c", FAR, f).value == pytest.approx(screen.profile_lr(13, 16, mult.sum(), f), rel=1e-5)


def test_a_numerical_range_equal_to_the_stage_range_changes_nothing():
    lo, hi = AGE.base[S("Darriwilian") - 1], AGE.base[S("Darriwilian")]
    a = ev.Problem(units(7, 8, "Darriwilian", 6), SPEC, AGE)
    b = ev.Problem(units(7, 8, "Darriwilian", 6, lo=lo, hi=hi), SPEC, AGE)
    for T in (459.1, 465.0, FAR):
        assert a.fstar("H0", T).value == pytest.approx(b.fstar("H0", T).value, rel=1e-9)


def test_units_placed_before_459_1_carry_no_exposure_younger_than_it():
    pr = ev.Problem(units(7, 8, "Darriwilian", 6, lo=459.1, hi=AGE.base[S("Darriwilian")]), SPEC, AGE)
    assert pr.fstar("H0", 459.1).state == "zero-exposure"
    assert pr.exposure(464.25) == pytest.approx(0.5 * pr.exposure(FAR), rel=1e-9)
    with pytest.raises(ValueError):
        ev.Problem(units(7, 8, "Darriwilian", 6, lo=455.0, hi=465.0), SPEC, AGE)


def test_window_read_out_equals_the_origin_test_when_no_unit_lies_after_its_start():
    pr = ev.Problem(units(7, 8, "Darriwilian", 6, lo=459.1, hi=AGE.base[S("Darriwilian")]), SPEC, AGE)
    for f in (1.0, 0.1):
        for T in (462.0, 468.0, FAR):
            w, o = pr.origin_stat("H0", T, f, start=459.1), pr.origin_stat("H0", T, f)
            assert w.value == pytest.approx(o.value, rel=1e-6, abs=1e-8)
    assert pr.origin_stat("H0", 459.0, 1.0, start=459.1).value == 0.0
    with pytest.raises(ValueError):
        pr.origin_stat("H0c", 462.0, 1.0, start=459.1)


def test_window_read_out_ignores_empty_units_after_its_start():
    """Older units only in the Hirnantian, after 459.1: the window null can put a = 0 there, so it cannot
    reject, while the origin test, which needs a >= f over them too, can."""
    pr = ev.Problem(units(13, 16, "Hirnantian", 10), SPEC, AGE)
    assert pr.origin_stat("H0", 470.0, 1.0, start=459.1).value == pytest.approx(0.0, abs=1e-6)
    assert pr.origin_stat("H0", 470.0, 1.0).value > ev.count_crit(0)


def test_adapter_traces_every_generated_row_to_a_source_report():
    decl = dz.declarations()
    h2 = next(d for d in decl["design"] if d["id"] == "LY-H2-CU")
    b = dz.build(h2, dict(material_type="chart-code", allocation="stage", cluster_k=math.inf))
    ref = [r for r in b.rows if not r.transported]
    old = [r for r in b.rows if r.transported]
    assert (len(ref), sum(r.d for r in ref), len(old), sum(r.d for r in old)) == (8, 7, 9, 0)
    assert all(r.rule == dz.RULES["libya"] and r.evidence for r in b.rows)
    assert {r.formation for r in old} == {"Bir Tlacsin", "Hawaz"}
    b2 = dz.build(h2, dict(material_type="appendix-only", allocation="stage", cluster_k=math.inf))
    assert {u for u, _ in b2.excluded} >= {"H2-NC186:4950", "H2-NC186:4990"}
    u, classes = b.units(0.25)
    assert classes == ["Cutting"] and np.allclose(u.mult[u.young > S("Rhuddanian")], 0.25)
