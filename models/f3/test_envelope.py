"""Checks of the F3 compatibility estimator (envelope.py), its simulator and the acceptance rule.

    uv run --with pytest --with numpy --with scipy python -m pytest -q models/f3

Ages are Ma, decreasing towards the present. Toy data sets use zero boundary uncertainty where a
closed form or an enumeration is the reference; coverage tests use fixed seeds.
"""

import itertools
import math

import numpy as np
import pytest
from scipy import stats

import envelope as ev
import sim
import units_sim as us
import validate as val

AGE = ev.AgeModel.load()
TS = AGE.timescale
EXACT = ev.AgeModel(TS, np.zeros(len(TS.names)))
I = TS.index


def toy_units(rows):
    """rows: (young stage, old stage, class, cluster, outcome)."""
    y, o, c, k, d = zip(*rows)
    return ev.Units(np.array([I(s) for s in y]), np.array([I(s) for s in o]), np.array(c), np.array(k), np.array(d))


def reference_rows(n_per_stage=20, detections=(("Katian", 1),), stages=("Katian", "Hirnantian", "Rhuddanian", "Aeronian", "Telychian"), cluster0=0):
    rows, cl = [], cluster0
    first = dict(detections)
    for st in stages:
        for j in range(n_per_stage):
            rows.append((st, st, 0, cl, int(j < first.get(st, 0))))
            cl += 1
    return rows


REF_STAGES = ("Katian", "Hirnantian", "Rhuddanian", "Aeronian", "Telychian")


def strong_reference():
    """100 reference units, 15 detections (reference rate about 0.16)."""
    return reference_rows(20, detections=tuple((st, 3) for st in REF_STAGES))


def older_rows(n, young="Sandbian", old="Darriwilian", d=0, cluster0=1000):
    return [(young, old, 0, cluster0 + j, d) for j in range(n)]


def problem(rows, age=EXACT, k=math.inf, seed=0, **spec):
    kw = dict(age_draws=2, cluster_shape_k=k, min_units_per_class=2) | spec
    return ev.Problem(toy_units(rows), ev.Spec(**kw), age, seed)


# --- ages ------------------------------------------------------------------------------------------


def test_boundary_draws_are_ordered_use_the_stated_sd_and_leave_blank_stages_fixed():
    b = AGE.draw_boundaries(np.random.default_rng(0), 4000)
    assert np.all(np.diff(b, axis=1) >= 0)
    sd = b.std(axis=0)
    i = I("Darriwilian")
    assert sd[i] == pytest.approx(AGE.unc[i], rel=0.1)
    cambrian = I("Paibian")
    assert AGE.unc[cambrian] == 0 and np.all(b[:, cambrian] == AGE.base[cambrian])


def test_all_units_share_each_boundary_draw():
    pr = problem(reference_rows() + older_rows(3), age=AGE, age_draws=5)
    assert pr.lo.shape == (5, 3)
    assert np.all(pr.lo == pr.lo[:, :1]) and np.all(pr.hi == pr.hi[:, :1])
    assert len(np.unique(pr.lo[:, 0])) == 5


# --- the cluster integral --------------------------------------------------------------------------


@pytest.mark.parametrize("k", [1.0, 2.0, 5.0])
def test_gamma_nodes_reproduce_the_closed_form_and_monte_carlo(k):
    u, logw = ev.gamma_nodes(k, 48)
    w = np.exp(logw)
    assert w.sum() == pytest.approx(1.0, abs=1e-7) and (w * u).sum() == pytest.approx(1.0, abs=1e-6)
    draws = np.random.default_rng(1).gamma(k, 1 / k, 2_000_000)
    for lam in (0.1, 1.0, 5.0, 20.0):
        exact = (1 + lam / k) ** -k
        assert (w * np.exp(-lam * u)).sum() == pytest.approx(exact, rel=1e-4)
        mc = np.exp(-lam * draws)
        assert abs(mc.mean() - exact) < 4 * mc.std() / math.sqrt(len(draws))


def p0_enum(r, vals, probs, k):
    """No-detection probability by explicit enumeration of the units' intensity atoms."""
    total = 0.0
    for combo in itertools.product(range(probs.shape[1]), repeat=len(r)):
        p = np.prod([probs[i, j] for i, j in enumerate(combo)])
        lam = sum(r[i] * vals[i, j] for i, j in enumerate(combo))
        total += p * (math.exp(-lam) if math.isinf(k) else (1 + lam / k) ** -k)
    return total


def outcome_prob(r, vals, probs, d, k):
    """P(the units with d = 1 detect and the rest do not), by inclusion-exclusion over the detections."""
    det = [i for i in range(len(r)) if d[i]]
    non = [i for i in range(len(r)) if not d[i]]
    total = 0.0
    for m in range(len(det) + 1):
        for s in itertools.combinations(det, m):
            idx = non + list(s)
            total += (-1) ** m * p0_enum(r[idx], vals[idx], probs[idx], k)
    return total


@pytest.mark.parametrize("k", [math.inf, 2.0, 0.8])
def test_quadrature_matches_enumeration(k):
    rng = np.random.default_rng(2)
    r = rng.uniform(0.05, 1.5, 4)
    vals = rng.uniform(0, 1, (4, 3))
    probs = rng.dirichlet(np.ones(3), 4)
    assert ev.no_detection_probability(r, vals, probs, k) == pytest.approx(p0_enum(r, vals, probs, k), rel=1e-5)


@pytest.mark.parametrize("k", [math.inf, 2.0, 0.8])
def test_convex_order_bound_dominates_every_path_and_is_tight_for_bang_bang(k):
    rng = np.random.default_rng(3)
    for _ in range(60):
        n = int(rng.integers(1, 6))
        r = rng.uniform(0.05, 2.0, n)
        vals = rng.uniform(0, 1, (n, 4))
        probs = rng.dirichlet(np.ones(4), n)
        m = (vals * probs).sum(axis=1)
        assert ev.p0_bound(r, m, k) >= ev.no_detection_probability(r, vals, probs, k) - 1e-9
        m01 = rng.uniform(0, 1, n)
        bang = np.stack([np.zeros(n), np.ones(n)], axis=1)
        exact = ev.no_detection_probability(r, bang, np.stack([1 - m01, m01], axis=1), k)
        assert ev.p0_bound(r, m01, k) == pytest.approx(exact, rel=1e-12)
    # and the gap is real: a constant path at the mean is strictly less likely to produce no detection
    assert ev.p0_bound(np.array([1.0, 1.0]), np.array([0.5, 0.5]), math.inf) > math.exp(-1.0) + 0.02


def exact_q(young, old, tau, T):
    lo, hi = TS.top[I(young)], TS.base[I(old)]
    qref = np.clip((min(hi, tau) - lo) / (hi - lo), 0, 1)
    qmid = np.clip((min(hi, T) - max(lo, tau)) / (hi - lo), 0, 1)
    return qref, qmid


def engine_vs_oracle(kind, k, x, C, rows, T, r):
    pr = problem(rows, k=k)
    w = pr.window(T)
    got = pr._ell_member(w, r, kind, x, C)
    units = toy_units(rows)
    keep = (units.old <= pr.s_star) & (units.young > pr.s_star - 5) | (units.old > pr.s_star)
    clusters = {}
    for i in np.flatnonzero(keep):
        clusters.setdefault(units.cluster[i], []).append(i)
    total = 0.0
    for members in clusters.values():
        vals, probs, rr, d = [], [], [], []
        for i in members:
            qref, qmid = exact_q(TS.names[units.young[i]], TS.names[units.old[i]], pr.tau_nom, T) if units.old[i] > pr.s_star else (1.0, 0.0)
            rest = 1 - qref - qmid
            if kind == "const":
                vals.append([1.0, x, 0.0]), probs.append([qref, qmid, rest])
            else:
                vals.append([1.0, 0.0, C]), probs.append([qref, rest + qmid * (1 - x / C), qmid * x / C])
            rr.append(r[units.cls[i]]), d.append(units.d[i])
        total += math.log(outcome_prob(np.array(rr), np.array(vals), np.array(probs), d, k))
    return got, total


def toy_with_clusters(older_hit=1):
    """Reference units in clusters of three; older units share clusters 0 to 2 with them, so those
    clusters span the first appearance."""
    rows = reference_rows(6, detections=(("Katian", 2), ("Rhuddanian", 1)), stages=("Katian", "Hirnantian", "Rhuddanian"))
    rows = [(y, o, c, i // 3, d) for i, (y, o, c, _, d) in enumerate(rows)]
    old = [("Sandbian", "Sandbian", 0, 0, 0), ("Sandbian", "Sandbian", 0, 0, 0), ("Sandbian", "Sandbian", 0, 1, 0)]
    old += [("Darriwilian", "Darriwilian", 0, 2, 0), ("Katian", "Darriwilian", 0, 2, older_hit), ("Sandbian", "Darriwilian", 0, 1, 0)]
    return rows + old


@pytest.mark.parametrize("k", [math.inf, 2.0])
def test_engine_likelihood_matches_enumeration_for_constant_histories(k):
    got, want = engine_vs_oracle("const", k, 0.4, 1.0, toy_with_clusters(), 460.0, np.array([0.3]))
    assert got == pytest.approx(want, abs=2e-5)


@pytest.mark.parametrize("k", [math.inf, 2.0])
@pytest.mark.parametrize("C", [1.0, 3.0])
def test_engine_likelihood_matches_enumeration_for_the_bound(k, C):
    got, want = engine_vs_oracle("bound", k, 0.4 * C, C, toy_with_clusters(older_hit=0), 460.0, np.array([0.3]))
    assert got == pytest.approx(want, abs=2e-5)


def test_bound_at_ceiling_equals_constant_history_and_exceeds_it_below():
    pr = problem(reference_rows() + older_rows(30), k=2.0)
    T = 475.0
    assert pr.ell_p("bound", T, 1.0, 1.0) == pytest.approx(pr.ell_p("const", T, 1.0), abs=1e-6)
    pr2 = problem(reference_rows() + older_rows(30, young="Sandbian", old="Sandbian"), k=2.0)
    for x in (0.2, 0.6):
        assert pr2.ell_p("bound", 456.0, x, 1.0) >= pr2.ell_p("const", 456.0, x) - 1e-9


# --- first appearance and the reference window -----------------------------------------------------


def test_tau_is_the_older_boundary_of_the_oldest_stage_with_a_certain_detection():
    rows = reference_rows(12, detections=(("Katian", 1), ("Rhuddanian", 2)), stages=("Sandbian", "Katian", "Hirnantian", "Rhuddanian", "Aeronian", "Telychian"))
    rows = [(y, o, c, k, 1 if (y == "Sandbian" and k == 0) else d) for y, o, c, k, d in rows]
    rows += [("Sandbian", "Darriwilian", 0, 900, 1)]  # a broad-range detection is not certain
    rows += [("Katian", "Katian", 1, 901 + j, int(j < 1)) for j in range(3)]  # class 1 has too few reference units
    pr = problem(rows, min_units_per_class=10, reference_stages=5)
    assert pr.s_star == I("Sandbian") and pr.tau_nom == TS.base[I("Sandbian")] == 458.2
    # reference window: Sandbian and the four younger stages; Telychian is outside it
    assert pr.n_ref == 12 * 5
    assert pr.n_dropped_outside == 12
    assert pr.n_dropped_uncalibrated == 3
    assert list(pr.calibrated) == [0]
    assert pr.n_old == 1 and pr.od.tolist() == [1]  # the broad unit has a part older than tau


def test_broad_detection_alone_gives_no_first_appearance():
    rows = reference_rows(12, detections=()) + [("Sandbian", "Darriwilian", 0, 900, 1)]
    with pytest.raises(ev.NoFirstAppearance):
        problem(rows)


# --- the chi-square calibration --------------------------------------------------------------------


def test_profile_lr_is_calibrated_in_a_regular_case():
    """Reference rate profiled jointly with the older intensity f; the LR at the true f is chi-square 1."""
    p_ref, f_true, T = 0.2, 0.5, 475.0
    r = -math.log1p(-p_ref)
    p_old = -math.expm1(-r * f_true)
    rng = np.random.default_rng(11)
    stages = {"Katian": 30, "Hirnantian": 30, "Rhuddanian": 20, "Aeronian": 20}
    cover, reps = 0, 500
    for _ in range(reps):
        rows, cl = [], 0
        for st, n in stages.items():
            for _ in range(n):
                rows.append((st, st, 0, cl, int(rng.random() < p_ref)))
                cl += 1
        rows += [("Sandbian", "Darriwilian", 0, 1000 + j, int(rng.random() < p_old)) for j in range(120)]
        pr = problem(rows)
        lr = 2 * (pr.hat("const", T)[0] - pr.ell_p("const", T, f_true))
        cover += lr <= stats.chi2.ppf(0.95, 1)
    assert cover / reps == pytest.approx(0.95, abs=0.03)


def test_boundary_shortcut_agrees_with_a_scan_when_an_older_unit_is_detected():
    rows = strong_reference() + older_rows(40) + older_rows(1, d=1, cluster0=2000)
    pr = problem(rows, k=2.0)
    T = 475.0
    best_scan = max(pr.ell_p("const", T, f) for f in np.linspace(0, 1, 101))
    hat, x_hat = pr.hat("const", T)
    assert hat >= best_scan - 1e-3 and hat <= best_scan + 0.05
    assert 0.0 < x_hat < 1.0


# --- the four states -------------------------------------------------------------------------------


def test_finite_state_matches_the_zero_count_bound():
    from scipy import optimize

    pr = problem(strong_reference() + older_rows(100))
    b = pr.fstar("H0c", 475.0)
    assert b.state == "finite" and b.ceiling == 1.0

    def ell(r, f):  # reference binomial (15 detections of 100) and 100 older non-detections, k = inf
        return 15 * math.log(-math.expm1(-r)) - 85 * r - 100 * r * f

    r_hat = optimize.minimize_scalar(lambda r: -ell(r, 0.0), bounds=(1e-4, 3), method="bounded", options={"xatol": 1e-10}).x
    prof = lambda f: -optimize.minimize_scalar(lambda r: -ell(r, f), bounds=(1e-4, 3), method="bounded", options={"xatol": 1e-10}).fun
    want = optimize.brentq(lambda f: 2 * (ell(r_hat, 0.0) - prof(f)) - pr.spec.crit, 0.0, 1.0)
    assert b.value == pytest.approx(want, rel=2e-3)
    assert pr.fstar("H0", 475.0).value >= b.value - 1e-6
    assert pr.fstar("H1", 475.0).value >= pr.fstar("H0", 475.0).value - 1e-6
    assert pr.fstar("H0m", 475.0).value >= b.value - 1e-3


def test_logistic_class_reports_the_largest_unrejected_expected_path():
    pr = problem(strong_reference() + older_rows(100), k=2.0)
    b = pr.fstar("logistic", 475.0)
    assert b.state == "finite" and 0.0 < b.value < b.ceiling and b.ceiling == pytest.approx(1.0, abs=0.01)
    assert b.value <= pr.fstar("H0", 475.0).value + 1e-6  # every logistic path is in H0


def test_ceiling_limited_state_when_the_data_cannot_reject_the_ceiling():
    pr = problem(reference_rows() + older_rows(3))
    b = pr.fstar("H0c", 475.0)
    assert (b.state, b.value) == ("ceiling-limited", 1.0)


def test_zero_exposure_state():
    pr = problem(reference_rows() + older_rows(50, young="Floian", old="Floian"))
    for cls in ("H0c", "H0m", "H0", "H1", "logistic"):
        assert pr.fstar(cls, 460.0).state == "zero-exposure"
    assert pr.fstar("H1-no-ceiling", 460.0).state == "zero-exposure"
    assert pr.fstar("H0c", 480.0).state != "zero-exposure"


def test_codex_counterexample_one_unit_with_a_short_high_intensity_pulse():
    """One eligible unit whose age falls in the window with probability eps = 0.1. Under H0 the data cannot
    reject the ceiling; for every finite ceiling C the ceiling is not rejected either, so f* = C grows without
    bound, and with no ceiling the result is unbounded."""
    top, base = TS.top[I("Sandbian")], TS.base[I("Sandbian")]
    T = float(top + 0.1 * (base - top))
    rows = strong_reference() + older_rows(1, young="Sandbian", old="Sandbian")
    pr = problem(rows)
    assert pr.window(T).qmean[0] == pytest.approx(0.1)
    assert (pr.fstar("H0", T).state, pr.fstar("H0", T).value) == ("ceiling-limited", 1.0)
    for C in (3.0, 10.0, 1000.0):
        b = ev.Problem(toy_units(rows), ev.Spec(age_draws=2, cluster_shape_k=math.inf, min_units_per_class=2, h1_ceiling=C), EXACT).fstar("H1", T)
        assert (b.state, b.value) == ("ceiling-limited", C)
    free = pr.fstar("H1-no-ceiling", T)
    assert (free.state, free.value) == ("unbounded", math.inf)
    # with 40 units certain to be in the window the ceiling is rejected and f* is finite
    full = problem(strong_reference() + older_rows(40)).fstar("H1", 470.0)
    assert full.state == "finite" and full.value < 3.0


def test_origin_set_reports_bounded_unbounded_and_disconnected_sets():
    pr = problem(strong_reference() + older_rows(60, young="Dapingian", old="Dapingian") + older_rows(60, young="Floian", old="Floian", cluster0=3000))
    grid = pr.grid(2.0)
    assert grid[0] == pr.tau_nom and grid[-1] == pr.spec.domain_ma[1]
    tab = pr.origin_tables(grid)
    strict = pr.origin_set(tab, "H0c", 1.0)
    assert not strict.unbounded and strict.connected and strict.runs[0][0] == pr.tau_nom
    assert 460.0 <= strict.older_endpoint <= 475.0
    assert strict.contains(strict.T[0]) and not strict.contains(500.0)
    loose = pr.origin_set(tab, "H0c", 0.01)
    assert loose.unbounded and loose.runs[-1][1] == pr.spec.domain_ma[1]
    delayed = pr.origin_set(tab, "H0m", 1.0)
    assert strict.older_endpoint <= delayed.older_endpoint <= strict.older_endpoint + max(pr.spec.delays_ma) + 2.0
    synthetic = ev.OriginSet("H0c", 1.0, 3.84, np.array([450.0, 452.0, 454.0, 456.0, 458.0]), np.array([0, 1, 9, 2, 8.0]), 560.0)
    assert synthetic.runs == [(450.0, 454.0), (456.0, 458.0)] and not synthetic.connected and not synthetic.unbounded


def test_an_older_detection_wholly_older_than_t_makes_t_inadmissible():
    rows = strong_reference() + older_rows(20, young="Floian", old="Floian") + [("Dapingian", "Floian", 0, 5000, 1)]
    pr = problem(rows)
    assert pr.window(460.0).impossible and not pr.window(475.0).impossible
    assert pr.lr_origin("H0c", 460.0, 1.0) == math.inf
    assert np.isfinite(pr.lr_origin("H0c", 475.0, 1.0))


# --- the acceptance rule ---------------------------------------------------------------------------


def test_stage_one_thresholds_and_exact_limits():
    assert val.lower_limit(944, 1000) == pytest.approx(0.93053, abs=2e-5)
    assert val.stage1(944) == "pass" and val.stage1(943) == "borderline"
    assert val.stage1(915) == "fail" and val.stage1(916) == "borderline"
    assert val.upper_limit(915, 1000) < 0.93 <= val.upper_limit(916, 1000)


def test_stage_two_pooled_threshold():
    assert val.stage2(1880) == "pass" and val.stage2(1879) == "fail"


@pytest.mark.parametrize("coverage, expected, tol", [(0.95, 0.983, 0.0015), (0.94, 0.57, 0.01), (0.93, 0.069, 0.003), (0.92, 0.002, 0.001)])
def test_acceptance_operating_characteristics(coverage, expected, tol):
    assert val.pass_probability(coverage) == pytest.approx(expected, abs=tol)


def test_one_stage_rule_alone_would_fail_good_cells():
    assert stats.binom.sf(943, 1000, 0.95) == pytest.approx(0.83, abs=0.01)


# --- the simulator and the real selection ----------------------------------------------------------


def test_simulated_design_follows_the_effort_and_tau_comes_from_the_record():
    s = us.simulate(us.Truth(history="H0c", f=0.3), us.Design(scale=0.05), AGE, 5)
    effort = us.spore_effort()
    assert abs(len(s.units) - sum(round(0.05 * n) for st, n in effort.items() if round(0.05 * n) > 0)) == 0
    assert np.all(s.units.young <= s.units.old)
    broad = (s.units.old > s.units.young).mean()
    assert 0.05 < broad < 0.25
    pr = ev.Problem(s.units, ev.Spec(age_draws=3, nodes=8), AGE, 5)
    certain = (s.units.d == 1) & (s.units.young == s.units.old)
    assert pr.s_star == s.units.old[certain].max() and pr.tau_nom == TS.base[pr.s_star]


def test_true_path_and_target():
    t = np.array([440.0, 455.0, 470.0, 480.0])
    assert us.Truth(history="H0c", f=0.3, t0=476.0).path(t).tolist() == [1.0, 0.3, 0.3, 0.0]
    assert us.Truth(history="H0m", f=0.3, t0=476.0, delay=8.0).path(t).tolist() == [1.0, 0.3, 0.0, 0.0]
    s = us.simulate(us.Truth(history="H0c", f=0.4, t0=476.0), us.Design(), AGE, 6)
    pr = ev.Problem(s.units, ev.Spec(age_draws=20, nodes=8), AGE, 6)
    truth = us.Truth(history="H0c", f=0.4, t0=476.0)
    assert pr.tau_nom >= truth.tau0, "seed chosen so that tau lies at or older than the point where a leaves 1"
    assert pr.abar_truth(truth.path, 476.0, s.r[pr.calibrated]) == pytest.approx(0.4, abs=5e-3)
    comb = us.Truth(history="H0", f=0.3, t0=476.0)
    assert pr.abar_truth(comb.path, 476.0, s.r[pr.calibrated]) == pytest.approx(0.3, abs=0.03)  # partial teeth in short ranges


def test_harness_replicate_records_coverage_informativeness_and_states():
    cell = next(c for c in val.CELLS if c["name"] == "H0c_f0.3_kinf")
    row = val.replicate((cell, 0))
    assert row["error"] == "" and row["no_tau"] is False
    for key in ("tau", "trivial", "cover_set_H0c_1", "cover_set_H0m_0.1", "lr0_H0c_0.01", "endpoint_H0c_1", "state_H0", "fcover_H0c", "fcover2_H0c", "crit_alt", "a_ref", "abar_rel", "state_H1-no-ceiling"):
        assert key in row
    assert row["state_H0"] in ev.STATES and row["state_H1-no-ceiling"] in ev.STATES
    summary = val.summarise(cell, [row])
    assert summary["n_valid"] == 1 and "cover_set_applicable_H0c" in summary


def test_exact_count_critical_value_runs_from_the_rule_of_three_to_about_chi_square_one_sided():
    assert ev.exact_count_crit(0) == pytest.approx(-2 * math.log(0.05), abs=1e-9)
    assert ev.exact_count_crit(1) == pytest.approx(4.37, abs=0.02)
    assert 2.7 < ev.exact_count_crit(500) < ev.exact_count_crit(50) < 3.1
    assert ev.exact_count_crit(0) > ev.exact_count_crit(1) > ev.exact_count_crit(5) > ev.exact_count_crit(50)
