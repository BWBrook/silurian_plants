"""Checks of the F3 compatibility estimator (envelope.py), its simulator and the acceptance rule.

    uv run --with pytest --with numpy --with scipy python -m pytest -q studies/f3/models

Ages are Ma, decreasing towards the present. Stage boundaries are fixed, so toy data sets have exact
ranges and a closed form, an enumeration or an independent quadrature is the reference; coverage tests use
fixed seeds.
"""

import functools
import gzip
import itertools
import math

import numpy as np
import pytest
from scipy import integrate, optimize, stats

import envelope as ev
import sim
import units_sim as us
import validate as val

AGE = ev.AgeModel.load()
TS = AGE.timescale
I = TS.index
SPEC_TOML = sim.ROOT / "studies" / "f3" / "models" / "specs" / "m2-draft.toml"


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


def problem(rows, k=math.inf, **spec):
    kw = dict(cluster_shape_k=k, min_units_per_class=2) | spec
    return ev.Problem(toy_units(rows), ev.Spec(**kw), AGE)


# --- ages ------------------------------------------------------------------------------------------


def test_age_scenarios_are_ordered_use_the_printed_uncertainty_and_leave_blank_stages_fixed():
    chart, older, younger = (ev.AgeModel.load(scenario=s) for s in ev.SCENARIOS)
    assert np.all(older.base >= chart.base) and np.all(chart.base >= younger.base)
    for m in (chart, older, younger):
        assert np.all(np.diff(m.base) > 0)
    i = I("Darriwilian")
    assert older.base[i] - chart.base[i] == pytest.approx(AGE.unc[i]) and chart.base[i] - younger.base[i] == pytest.approx(AGE.unc[i])
    assert np.all(chart.base == TS.base)
    paibian = I("Paibian")
    assert AGE.unc[paibian] == 0 and older.base[paibian] == younger.base[paibian] == chart.base[paibian]
    assert np.isnan(chart.top[0]) and np.all(chart.top[1:] == chart.base[:-1])


def test_age_model_rejects_crossing_bases_and_unknown_scenarios():
    unc = np.zeros(len(TS.names))
    unc[I("Emsian")] = 100.0
    with pytest.raises(ValueError):
        ev.AgeModel(TS, unc, "older")
    with pytest.raises(ValueError):
        ev.AgeModel(TS, AGE.unc, "oldest")


def test_older_scenario_moves_tau_and_the_unit_ranges():
    rows = strong_reference() + older_rows(5)
    chart = problem(rows)
    older = ev.Problem(toy_units(rows), ev.Spec(cluster_shape_k=math.inf, min_units_per_class=2, age_scenario="older"), ev.AgeModel.load(scenario="older"))
    assert older.tau == pytest.approx(chart.tau + AGE.unc[I("Katian")]) and np.all(older.hi > chart.hi)
    with pytest.raises(ValueError):
        ev.Problem(toy_units(rows), ev.Spec(), ev.AgeModel.load(scenario="older"))


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


def oracle_ell(pr, win, theta, x, L, U, bound):
    """The log-likelihood from explicit per-unit formulas and scipy quadrature over the cluster effect."""
    r = np.exp(theta)
    k = pr.spec.cluster_shape_k
    chi = lambda ru, p: (
        ((U[p] - x[p]) * math.exp(-ru * L[p]) + (x[p] - L[p]) * math.exp(-ru * U[p])) / (U[p] - L[p]) if bound and U[p] > L[p] else math.exp(-ru * (L[p] if bound else x[p]))
    )

    def phi(unit, u):
        if unit[0] == "ref":
            _, c, d = unit
            e = math.exp(-r[c] * u)
            return 1 - e if d else e
        _, i = unit
        ru = r[pr.oc[i]] * u
        w, qref = win.W[i], pr.Qref[i]
        if pr.od[i]:
            return qref * (1 - math.exp(-ru)) + sum(w[p] * (1 - math.exp(-ru * x[p])) for p in range(len(w)))
        return qref * math.exp(-ru) + (1 - qref - w.sum()) + sum(w[p] * chi(ru, p) for p in range(len(w)))

    clusters: dict = {}
    for j in range(pr.n_ref):
        clusters.setdefault(pr.rcl[j], []).append(("ref", pr.rc[j], pr.rd[j]))
    for i in range(pr.n_old):
        clusters.setdefault(pr.ocl[i], []).append(("old", i))
    total = 0.0
    for units in clusters.values():
        if math.isinf(k):
            total += math.log(np.prod([phi(un, 1.0) for un in units]))
        else:
            f = lambda u: stats.gamma.pdf(u, k, scale=1 / k) * np.prod([phi(un, u) for un in units])
            total += math.log(integrate.quad(f, 0, np.inf, epsabs=0, epsrel=1e-11, limit=200)[0])
    return total


def toy_with_clusters(older_hit=1):
    """Reference units in clusters of three; older units share clusters 0 to 2 with them, so those
    clusters span the first appearance."""
    rows = reference_rows(6, detections=(("Katian", 2), ("Rhuddanian", 1)), stages=("Katian", "Hirnantian", "Rhuddanian"))
    rows = [(y, o, c, i // 3, d) for i, (y, o, c, _, d) in enumerate(rows)]
    old = [("Sandbian", "Sandbian", 0, 0, 0), ("Sandbian", "Sandbian", 0, 0, 0), ("Sandbian", "Sandbian", 0, 1, 0)]
    old += [("Darriwilian", "Darriwilian", 0, 2, 0), ("Katian", "Darriwilian", 0, 2, older_hit), ("Sandbian", "Darriwilian", 0, 1, 0)]
    old += [("Sandbian", "Floian", 0, 1, 0), ("Hirnantian", "Dapingian", 0, 0, older_hit)]
    return rows + old


@pytest.mark.parametrize("k", [math.inf, 2.0, 0.8])
@pytest.mark.parametrize("bound", [False, True])
def test_engine_matches_independent_quadrature_with_detected_and_straddling_units(k, bound):
    pr = problem(toy_with_clusters(), k=k, nodes=64)
    win = pr.window(pr.edges(474.0))
    assert win.has_det and win.P >= 3 and np.any((pr.Qref > 0) & (pr.Qref < 1))
    rng = np.random.default_rng(4)
    L = rng.uniform(0, 0.3, win.P)
    U = L + rng.uniform(0.4, 1.5, win.P)
    x = rng.uniform(L, U)
    theta = np.log(np.array([0.3]))
    got = pr._eval(win, theta, x, L, U, bound, grad=False)
    assert got == pytest.approx(oracle_ell(pr, win, theta, x, L, U, bound), abs=2e-5)


@pytest.mark.parametrize("k", [math.inf, 2.0])
def test_engine_matches_enumeration_for_the_exact_and_the_undetected_bound_likelihoods(k):
    rows = toy_with_clusters(older_hit=0)
    pr = problem(rows, k=k)
    win = pr.window(pr.edges(474.0))
    rng = np.random.default_rng(6)
    L, U = rng.uniform(0, 0.3, win.P), rng.uniform(0.5, 1.5, win.P)
    x = rng.uniform(L, U)
    r = np.array([0.3])
    for bound in (False, True):
        clusters: dict = {}
        for j in range(pr.n_ref):
            clusters.setdefault(pr.rcl[j], []).append((None, pr.rd[j], pr.rc[j]))
        for i in range(pr.n_old):
            clusters.setdefault(pr.ocl[i], []).append((i, pr.od[i], pr.oc[i]))
        total = 0.0
        for members in clusters.values():
            vals, probs, rr, d = [], [], [], []
            for i, di, ci in members:
                if i is None:
                    vals.append([1.0]), probs.append([1.0])
                else:
                    w = win.W[i]
                    rest = 1 - pr.Qref[i] - w.sum()
                    if bound:
                        s = (x - L) / (U - L)
                        vals.append([1.0, 0.0, *L, *U]), probs.append([pr.Qref[i], rest, *(w * (1 - s)), *(w * s)])
                    else:
                        vals.append([1.0, 0.0, *x]), probs.append([pr.Qref[i], rest, *w])
                rr.append(r[ci]), d.append(di)
            n_atoms = max(len(v) for v in vals)
            vals = np.array([v + [0.0] * (n_atoms - len(v)) for v in vals])
            probs = np.array([p + [0.0] * (n_atoms - len(p)) for p in probs])
            total += math.log(outcome_prob(np.array(rr), vals, probs, d, k))
        assert pr._eval(win, np.log(r), x, L, U, bound, grad=False) == pytest.approx(total, abs=2e-5)


@pytest.mark.parametrize("k", [math.inf, 2.0])
@pytest.mark.parametrize("bound", [False, True])
def test_analytic_gradients_match_finite_differences(k, bound):
    pr = problem(toy_with_clusters(), k=k)
    win = pr.window(pr.edges(474.0))
    rng = np.random.default_rng(7)
    L = np.zeros(win.P)
    U = np.full(win.P, 3.0)
    for _ in range(3):
        theta = np.log(pr.r_ref) + rng.normal(0, 0.3, 1)
        x = rng.uniform(0.1, 2.5, win.P)
        value, grad = pr._eval(win, theta, x, L, U, bound)
        z = np.concatenate([theta, x])
        step = 1e-6
        num = np.array([
            (pr._eval(win, (z + step * e)[:1], (z + step * e)[1:], L, U, bound, False) - pr._eval(win, (z - step * e)[:1], (z - step * e)[1:], L, U, bound, False)) / (2 * step)
            for e in np.eye(len(z))
        ])
        assert np.allclose(grad, num, rtol=1e-5, atol=1e-6)


def random_design(rng, k, detected=True):
    rows = reference_rows(15, detections=(("Katian", 1), ("Hirnantian", 3), ("Rhuddanian", 2)), stages=REF_STAGES[:4])
    rows += [("Sandbian", "Floian", 0, 500, 0), ("Sandbian", "Floian", 0, 501, int(detected))]
    stages = ["Sandbian", "Darriwilian", "Dapingian", "Floian"]
    for j in range(rng.integers(6, 14)):
        a, b = sorted(rng.integers(0, 4, 2))
        if a == b and detected:
            b = min(b + 1, 3) if a < 3 else a
            a = a if a != b else 2
        rows.append((stages[a], stages[b], 0, int(rng.integers(0, 8)) + 700, int(detected and rng.random() < 0.3)))
    return problem(rows, k=k)


def fine_window(pr, win, m):
    edges = np.concatenate([np.linspace(lo, hi, m, endpoint=False) for lo, hi in zip(win.edges[:-1], win.edges[1:])] + [[win.edges[-1]]])
    return pr.window(tuple(edges))


@pytest.mark.parametrize("k", [math.inf, 2.0])
def test_chord_and_jensen_bounds_dominate_the_exact_likelihood_of_every_fine_path(k):
    rng = np.random.default_rng(8)
    for _ in range(25):
        pr = random_design(rng, k)
        win = pr.window(pr.edges(475.0))
        assert win.P == len(win.edges) - 1 and win.has_det
        L = rng.uniform(0, 0.3, win.P)
        U = L + rng.uniform(0.2, 1.5, win.P)
        m = 4
        v = rng.uniform(L[:, None], U[:, None], (win.P, m))
        theta = np.log(pr.r_ref) + rng.normal(0, 0.3, 1)
        exact = pr._eval(fine_window(pr, win, m), theta, v.ravel(), None, None, False, False)
        assert exact <= pr._eval(win, theta, v.mean(axis=1), L, U, True, False) + 1e-9


@pytest.mark.parametrize("k", [math.inf, 2.0])
def test_the_bound_is_attained_by_a_path_at_L_or_U_when_no_older_unit_detects(k):
    rng = np.random.default_rng(9)
    for _ in range(15):
        pr = random_design(rng, k, detected=False)
        win = pr.window(pr.edges(475.0))
        L = rng.uniform(0, 0.3, win.P)
        U = L + rng.uniform(0.2, 1.5, win.P)
        m = 5
        up = rng.integers(0, m + 1, win.P)
        v = np.where(np.arange(m)[None, :] < up[:, None], U[:, None], L[:, None])
        theta = np.log(pr.r_ref) + rng.normal(0, 0.3, 1)
        exact = pr._eval(fine_window(pr, win, m), theta, v.ravel(), None, None, False, False)
        assert exact == pytest.approx(pr._eval(win, theta, v.mean(axis=1), L, U, True, False), abs=1e-9)


def brute_sup(pr, win, L, U, mono, f, levels=9, rounds=3):
    """The supremum over x by grid search with the target met exactly on the last piece, refined around the
    best point and polished by a numerical-gradient SLSQP started there; the reference rate is profiled by
    an independent scalar search at each grid point."""
    P, c = win.P, win.coef(np.zeros(pr.n_cls))

    def value(x):
        res = optimize.minimize_scalar(lambda th: -pr._eval(win, np.array([th]), x, L, U, True, False), bounds=ev.LOG_R_BOUNDS, method="bounded", options={"xatol": 1e-10})
        return -res.fun, res.x

    centre, half = (L + U) / 2, (U - L) / 2
    best, bx, bth = -math.inf, None, None
    for _ in range(rounds):
        axes = [np.unique(np.clip(np.linspace(centre[p] - half[p], centre[p] + half[p], levels), L[p], U[p])) for p in range(P)]
        for head in itertools.product(*axes[:-1]):
            need = (f - c[:-1] @ np.array(head)) / c[-1]
            for last in [max(L[-1], need), *axes[-1]]:
                x = np.array([*head, min(last, U[-1])])
                if c @ x < f - 1e-12 or (mono and np.any(np.diff(x) > 1e-12)):
                    continue
                v, th = value(x)
                if v > best:
                    best, bx, bth = v, x, th
        centre, half = bx, half / 3
    rows, lb = ([np.r_[0.0, c]] if f > 0 else []), ([f] if f > 0 else [])
    if mono:
        rows += [np.r_[0.0, np.eye(P)[p] - np.eye(P)[p + 1]] for p in range(P - 1)]
        lb += [0.0] * (P - 1)
    res = optimize.minimize(
        lambda z: -pr._eval(win, z[:1], z[1:], L, U, True, False), np.r_[bth, bx], method="SLSQP",
        bounds=optimize.Bounds(np.r_[ev.LOG_R_BOUNDS[0], L], np.r_[ev.LOG_R_BOUNDS[1], U]),
        constraints=[optimize.LinearConstraint(np.array(rows), np.array(lb), np.inf)] if rows else [], options={"ftol": 1e-13, "maxiter": 500},
    )
    z = np.clip(res.x, np.r_[ev.LOG_R_BOUNDS[0], L], np.r_[ev.LOG_R_BOUNDS[1], U])
    polished = pr._eval(win, z[:1], z[1:], L, U, True, False)
    feasible = (not rows) or float((np.array(lb) - np.array(rows) @ z).max()) <= 1e-7
    return max(best, polished) if feasible else best


@pytest.mark.parametrize("detected", [False, True])
@pytest.mark.parametrize("cls, mono, C", [("H0", False, 1.0), ("H0m", True, 1.0)])
def test_optimiser_matches_a_brute_force_search_on_a_tiny_design(cls, mono, C, detected):
    rows = reference_rows(20, detections=tuple((st, 3) for st in REF_STAGES)) + older_rows(8, "Sandbian", "Darriwilian") + older_rows(6, "Sandbian", "Sandbian", 0, 2000)
    rows += older_rows(5, "Darriwilian", "Floian", 0, 3000) + older_rows(1, "Darriwilian", "Floian", int(detected), 4000)
    pr = problem(rows)
    win = pr.window(pr.edges(470.0))
    assert win.P == 3 and win.has_det == detected
    L, U = np.zeros(win.P), np.full(win.P, C)
    for f in (0.0, 0.35, 0.8):
        fit = pr.bound_sup(win, L, U, mono, f)
        brute = brute_sup(pr, win, L, U, mono, f)
        assert fit.converged and fit.spread < ev.SPREAD_FLAG
        assert fit.value >= brute - 1e-7
        assert fit.value == pytest.approx(brute, abs=2e-4)
        assert win.coef(fit.theta) @ fit.x >= f - 1e-6 and (not mono or np.all(np.diff(fit.x) <= 1e-7))


@pytest.mark.parametrize("mono", [False, True])
def test_vertex_start_is_feasible_and_puts_the_target_on_one_piece_or_a_step(mono):
    pr = problem(strong_reference() + older_rows(30) + older_rows(20, "Dapingian", "Floian", 0, 2000), k=2.0)
    win = pr.window(pr.edges(476.0))
    L, U = np.zeros(win.P), np.full(win.P, 3.0)
    x = pr._vertex_start(win, L, U, mono, 0.6)
    assert x is not None and win.coef(pr._th) @ x >= 0.6 - 1e-9 and np.all(x >= L) and np.all(x <= U + 1e-12)
    floor = ev.FLOOR * 3.0
    assert (np.all(np.diff(x) <= 1e-12) if mono else np.sum(x > floor + 1e-9) == 1)
    assert pr._vertex_start(win, L, U, mono, 3.0 + 1e-6) is None


def test_lr_is_non_decreasing_in_f_and_zero_up_to_the_best_constant():
    pr = problem(strong_reference() + older_rows(40) + older_rows(30, "Dapingian", "Floian", 0, 2000) + older_rows(2, "Sandbian", "Floian", 1, 5000), k=2.0)
    T = 476.0
    fs = np.linspace(0.0, 1.0, 11)
    for cls in ("H0c", "H0m", "H0"):
        lr = np.array([pr.lr(cls, T, f).value for f in fs])
        assert np.all(np.diff(lr) >= -1e-6) and lr[0] == 0.0
    assert pr.lr("H0", T, 1.0 + 1e-3).value == math.inf
    at_ceiling = [pr.lr(cls, T, 1.0 + 4.5e-13) for cls in ("H0c", "H0m", "H0")]
    assert all(st.converged for st in at_ceiling) and at_ceiling[1].value == at_ceiling[2].value == pytest.approx(at_ceiling[0].value)
    assert pr.lr("H1", T, 3.0).value == pytest.approx(2 * (pr.const_max(T, 0.0, 3.0)[0] - pr.ell_const(T, 3.0)))


def test_best_constant_search_agrees_with_a_scan_when_an_older_unit_is_detected():
    rows = strong_reference() + older_rows(40) + older_rows(1, d=1, cluster0=2000)
    pr = problem(rows, k=2.0)
    T = 475.0
    best_scan = max(pr.ell_const(T, f) for f in np.linspace(0, 1, 101))
    hat, x_hat, ok, _ = pr.const_max(T)
    assert ok
    assert hat >= best_scan - 1e-3 and hat <= best_scan + 0.05
    assert 0.0 < x_hat < 1.0


def two_class_problem(detected):
    """Two classes with different reference rates whose older units sit in different stages, so the target
    coefficients move with the rates."""
    rows = strong_reference() + [(st, st, 1, 500 + 20 * i + j, int(j < 1)) for i, st in enumerate(REF_STAGES) for j in range(20)]
    rows += older_rows(10, "Sandbian", "Sandbian") + [("Darriwilian", "Darriwilian", 1, 2000 + j, 0) for j in range(12)]
    rows += [("Dapingian", "Dapingian", 1, 3000 + j, 0) for j in range(4)] + older_rows(6, "Darriwilian", "Dapingian", 0, 4000)
    rows += [("Sandbian", "Darriwilian", 1, 5000, int(detected))]
    return problem(rows)


def test_target_coefficients_follow_the_rates_and_their_gradient_is_exact():
    pr = two_class_problem(False)
    win = pr.window(pr.edges(470.0))
    assert pr.n_cls == 2 and win.P == 3 and not win.rate_free
    x = np.array([0.9, 0.4, 0.1])
    for theta in (np.log(pr.r_ref), np.array([-3.0, -1.0]), np.array([-1.0, -4.0])):
        assert win.coef(theta).sum() == pytest.approx(1.0)
        abar, g = win.target(theta, x)
        assert abar == pytest.approx(win.coef(theta) @ x)
        z, h = np.r_[theta, x], 1e-6
        num = [(win.target((z + h * e)[:2], (z + h * e)[2:])[0] - win.target((z - h * e)[:2], (z - h * e)[2:])[0]) / (2 * h) for e in np.eye(5)]
        assert np.allclose(g, num, atol=1e-7)
    assert not np.allclose(win.coef(np.array([-3.0, -1.0])), win.coef(np.array([-1.0, -4.0])))
    assert win.target_floor(np.array([0.2, 0.0, 0.0])) == pytest.approx(min(win.coef(np.array([-30.0, 0.0])) @ [0.2, 0, 0], win.coef(np.array([0.0, -30.0])) @ [0.2, 0, 0]), abs=1e-9)
    one = problem(strong_reference() + older_rows(30) + older_rows(20, "Dapingian", "Floian", 0, 2000)).window(pr.edges(476.0))
    assert one.rate_free


@pytest.mark.parametrize("detected", [False, True])
@pytest.mark.parametrize("mono", [False, True])
def test_two_class_supremum_constrains_the_target_at_its_own_rates_and_matches_a_global_search(mono, detected):
    pr = two_class_problem(detected)
    win = pr.window(pr.edges(470.0))
    L, U = np.zeros(win.P), np.ones(win.P)
    th0 = np.log(pr.r_ref)
    bounds = [(t - 2.5, t + 2.5) for t in th0] + [(0.0, 1.0)] * win.P
    for f in (0.35, 0.8):
        fit = pr.bound_sup(win, L, U, mono, f)
        assert fit.converged
        assert win.coef(fit.theta) @ fit.x >= f - 1e-6 and (not mono or np.all(np.diff(fit.x) <= 1e-7))
        cons = [optimize.NonlinearConstraint(lambda z: win.target(z[:2], z[2:])[0], f, np.inf)]
        if mono:
            cons.append(optimize.LinearConstraint(np.c_[np.zeros((win.P - 1, 2)), np.eye(win.P)[:-1] - np.eye(win.P)[1:]], 0.0, np.inf))
        de = optimize.differential_evolution(lambda z: -pr._eval(win, z[:2], z[2:], L, U, True, False), bounds, constraints=cons,
                                             seed=1, tol=1e-10, maxiter=400, polish=True)
        assert np.all(np.abs(fit.theta - th0) < 2.5)
        assert fit.value >= -de.fun - 1e-6
        assert fit.value == pytest.approx(-de.fun, abs=2e-3)


def test_select_keeps_the_highest_candidate_with_its_own_status():
    z = np.zeros(2)
    best, spread = ev.select([(-5.0, z, True), (-3.0, z + 1, False), (-4.0, z, True)])
    assert best[0] == -3.0 and best[2] is False and spread == 2.0
    best, _ = ev.select([(-3.0, z, True), (-3.0 + 1e-8, z + 1, False)])
    assert best[2] is True and best[0] == -3.0


def test_a_statistic_fails_when_its_alternative_or_its_null_fails(monkeypatch):
    pr = problem(strong_reference() + older_rows(40) + older_rows(1, d=1, cluster0=2000), k=2.0)
    T = 475.0
    assert all(pr.lr(cls, T, 0.5).converged for cls in ("H0c", "H0m", "H0"))
    good = pr.const_max(T, 0.0, 1.0)
    monkeypatch.setattr(pr, "bound_sup", lambda *a, **k: ev.Fit(good[0] - 1.0, None, None, False, 0.0))
    assert not pr.lr("H0", T, 0.5).converged and not pr.origin_stat("H0", T, 0.1).converged
    monkeypatch.undo()
    monkeypatch.setattr(pr, "const_max", lambda T, lo=0.0, hi=1.0: (good[0], good[1], False, 0.0))
    for cls in ("H0c", "H0m", "H0"):
        assert not pr.lr(cls, T, 0.5).converged and not pr.origin_stat(cls, T, 0.1).converged
    assert not pr.fstar("H0c", T).converged
    assert not pr.origin_set("H0c", 0.1, np.array([pr.tau, T])).ok[1]


# --- first appearance and the reference window -----------------------------------------------------


def test_tau_is_the_older_boundary_of_the_oldest_stage_with_a_certain_detection():
    rows = reference_rows(12, detections=(("Katian", 1), ("Rhuddanian", 2)), stages=("Sandbian", "Katian", "Hirnantian", "Rhuddanian", "Aeronian", "Telychian"))
    rows = [(y, o, c, k, 1 if (y == "Sandbian" and k == 0) else d) for y, o, c, k, d in rows]
    rows += [("Sandbian", "Darriwilian", 0, 900, 1)]  # a broad-range detection is not certain
    rows += [("Katian", "Katian", 1, 901 + j, int(j < 1)) for j in range(3)]  # class 1 has too few reference units
    pr = problem(rows, min_units_per_class=10, reference_stages=5)
    assert pr.s_star == I("Sandbian") and pr.tau == TS.base[I("Sandbian")] == 458.2
    assert pr.n_ref == 12 * 5
    assert pr.n_dropped_outside == 12
    assert pr.n_dropped_uncalibrated == 3
    assert list(pr.calibrated) == [0]
    assert pr.n_old == 1 and pr.od.tolist() == [1]  # the broad unit has a part older than tau


def test_broad_detection_alone_gives_no_first_appearance():
    rows = reference_rows(12, detections=()) + [("Sandbian", "Darriwilian", 0, 900, 1)]
    with pytest.raises(ev.NoFirstAppearance):
        problem(rows)


def test_pieces_follow_the_stage_bases_and_the_lag_and_drop_empty_ones():
    pr = problem(strong_reference() + older_rows(5, "Sandbian", "Darriwilian"))
    assert pr.edges(500.0) == (452.8, 458.2, 469.4, 471.3, 477.1, 486.85, 491.0, 494.2, 497.0, 500.0)
    assert pr.edges(500.0, lag=10.0) == (452.8, 458.2, 469.4, 471.3, 477.1, 486.85, 490.0, 491.0, 494.2, 497.0, 500.0)
    assert pr.edges(470.0, lag=20.0) == (452.8, 458.2, 469.4, 470.0)
    assert pr.edges(452.0) == (452.8,)
    win = pr.window(pr.edges(500.0))
    assert win.P == 2 and np.allclose(win.piece_hi, [458.2, 469.4])
    assert np.allclose(win.W.sum(axis=1), 1.0) and win.coef(np.zeros(pr.n_cls)).sum() == pytest.approx(1.0)
    assert np.allclose(win.W[0], [(458.2 - 452.8) / (469.4 - 452.8), (469.4 - 458.2) / (469.4 - 452.8)])


# --- calibration ----------------------------------------------------------------------------------


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
        lr = 2 * (pr.const_max(T)[0] - pr.ell_const(T, f_true))
        cover += lr <= stats.chi2.ppf(0.95, 1)
    assert cover / reps == pytest.approx(0.95, abs=0.03)


# --- the four states -------------------------------------------------------------------------------


def test_finite_state_matches_the_zero_count_bound():
    pr = problem(strong_reference() + older_rows(100))
    b = pr.fstar("H0c", 475.0)
    assert b.state == "finite" and b.ceiling == 1.0

    def ell(r, f):  # reference binomial (15 detections of 100) and 100 older non-detections, k = inf
        return 15 * math.log(-math.expm1(-r)) - 85 * r - 100 * r * f

    r_hat = optimize.minimize_scalar(lambda r: -ell(r, 0.0), bounds=(1e-4, 3), method="bounded", options={"xatol": 1e-10}).x
    prof = lambda f: -optimize.minimize_scalar(lambda r: -ell(r, f), bounds=(1e-4, 3), method="bounded", options={"xatol": 1e-10}).fun
    assert pr.crit(475.0) == pytest.approx(-2 * math.log(0.05))  # no older detection: P0 >= alpha
    want = optimize.brentq(lambda f: 2 * (ell(r_hat, 0.0) - prof(f)) - pr.crit(475.0), 0.0, 1.0)
    assert b.value == pytest.approx(want, rel=2e-3)
    assert pr.fstar("H0", 475.0).value >= b.value - 1e-6
    assert pr.fstar("H1", 475.0).value >= pr.fstar("H0", 475.0).value - 1e-6
    assert pr.fstar("H0m", 475.0).value >= b.value - 1e-3


def test_classes_nest_with_and_without_older_detections_on_a_toy_table():
    base = strong_reference() + older_rows(60) + older_rows(30, "Dapingian", "Floian", 0, 3000)
    for rows in (base, base + older_rows(2, d=1, cluster0=5000)):
        pr = problem(rows, k=2.0)
        T = 476.0
        c, m, h0 = (pr.fstar(cls, T) for cls in ("H0c", "H0m", "H0"))
        assert c.state == "finite" and c.value <= m.value + 2e-3 and m.value <= h0.value + 2e-3
        assert h0.value > c.value + 1e-3
        assert pr.fstar("H1", T).value >= h0.value - 2e-3
        assert all(b.converged and b.spread < ev.SPREAD_FLAG for b in (c, m, h0))
    assert pr.n_older_detections(T) == 2 and pr.crit(T) == pytest.approx(ev.count_crit(2))


def test_classes_nest_on_simulated_tables():
    checked = 0
    for seed, (history, t0) in enumerate([("H0c", 476.0), ("step", 476.0), ("H0c", 500.0), ("hide", 476.0)]):
        for rep in range(3):
            truth = us.Truth(history=history, f=0.3, t0=t0, delay=4.3)
            s = us.simulate(truth, us.Design(), np.random.SeedSequence(100 * seed + rep))
            try:
                pr = ev.Problem(s.units, ev.Spec(), AGE)
            except ev.NoFirstAppearance:
                continue
            for T in (t0, 459.1):
                if pr.exposure(T) <= 0:
                    continue
                c, m, h0 = (pr.fstar(cls, T).value for cls in ("H0c", "H0m", "H0"))
                assert c <= m + 2e-3 and m <= h0 + 2e-3
                checked += 1
    assert checked >= 8


def test_ceiling_limited_state_when_the_data_cannot_reject_the_ceiling():
    pr = problem(reference_rows() + older_rows(3))
    b = pr.fstar("H0c", 475.0)
    assert (b.state, b.value) == ("ceiling-limited", 1.0)


def test_zero_exposure_state():
    pr = problem(reference_rows() + older_rows(50, young="Floian", old="Floian"))
    for cls in ("H0c", "H0m", "H0", "H1", "H1-no-ceiling"):
        assert pr.fstar(cls, 460.0).state == "zero-exposure"
    assert pr.fstar("H0c", 480.0).state != "zero-exposure"
    with pytest.raises(ValueError):
        pr.fstar("logistic", 480.0)


def test_codex_counterexample_one_unit_with_a_short_high_intensity_pulse():
    """One eligible unit whose age falls in the window with probability eps = 0.1. Under H0 the data cannot
    reject the ceiling; for every finite ceiling C the ceiling is not rejected either, so f* = C grows without
    bound, and with no ceiling the result is unbounded."""
    top, base = TS.top[I("Sandbian")], TS.base[I("Sandbian")]
    T = float(top + 0.1 * (base - top))
    rows = strong_reference() + older_rows(1, young="Sandbian", old="Sandbian")
    pr = problem(rows)
    assert pr._qmid(T)[0] == pytest.approx(0.1)
    assert (pr.fstar("H0", T).state, pr.fstar("H0", T).value) == ("ceiling-limited", 1.0)
    for C in (3.0, 10.0, 1000.0):
        b = problem(rows, h1_ceiling=C).fstar("H1", T)
        assert (b.state, b.value) == ("ceiling-limited", C)
    free = pr.fstar("H1-no-ceiling", T)
    assert (free.state, free.value) == ("unbounded", math.inf)
    full = problem(strong_reference() + older_rows(40)).fstar("H1", 470.0)
    assert full.state == "finite" and full.value < 3.0


# --- origins ---------------------------------------------------------------------------------------


def test_origin_set_reports_bounded_unbounded_and_disconnected_sets():
    pr = problem(strong_reference() + older_rows(60, young="Dapingian", old="Dapingian") + older_rows(60, young="Floian", old="Floian", cluster0=3000))
    grid = pr.grid(2.0)
    assert grid[0] == pr.tau and grid[-1] == pr.spec.domain_ma[1]
    assert grid[-2] <= pr.T_flat + 2.0 + pr.spec.h0m_lag_ma + 1e-9
    strict = pr.origin_set("H0c", 1.0, grid)
    assert not strict.unbounded and strict.connected and strict.runs[0][0] == pr.tau
    assert 460.0 <= strict.older_endpoint <= 475.0
    assert strict.contains(strict.T[0]) and not strict.contains(500.0)
    loose = pr.origin_set("H0c", 0.01, grid)
    assert loose.unbounded and loose.runs[-1][1] == pr.spec.domain_ma[1]
    delayed = pr.origin_set("H0m", 1.0, grid)
    assert strict.older_endpoint <= delayed.older_endpoint <= strict.older_endpoint + pr.spec.h0m_lag_ma + 2.0
    with pytest.raises(ValueError):
        pr.origin_set("H1", 1.0, grid)
    synthetic = ev.OriginSet("H0c", 1.0, 3.84, np.array([450.0, 452.0, 454.0, 456.0, 458.0]), np.array([0, 1, 9, 2, 8.0]), 560.0, 445.0, np.ones(5, bool))
    assert synthetic.runs == [(450.0, 454.0), (456.0, 458.0)] and not synthetic.connected and not synthetic.unbounded
    assert synthetic.complete_runs == [(445.0, 454.0), (456.0, 458.0)]


def test_complete_runs_start_at_the_top_of_the_first_appearance_stage():
    pr = problem(strong_reference() + older_rows(60, young="Dapingian", old="Dapingian"))
    o = pr.origin_set("H0c", 1.0, pr.grid(2.0))
    assert pr.s_star == I("Katian") and pr.age.base[pr.s_star - 1] == 445.2
    assert o.runs[0][0] == pr.tau == 452.8 and o.complete_runs[0] == (445.2, o.runs[0][1])
    assert o.contains(450.0) is True and o.contains(445.2) is True


def test_with_no_older_detection_the_H0_origin_set_equals_H0c_and_H0m_is_the_delayed_step():
    pr = problem(strong_reference() + older_rows(40) + older_rows(30, "Dapingian", "Floian", 0, 3000) + older_rows(20, "Floian", "Floian", 0, 4000), k=2.0)
    grid = pr.grid(4.0)
    D = pr.spec.h0m_lag_ma
    for f_min in pr.spec.readouts:
        h0c, h0 = pr.origin_set("H0c", f_min, grid), pr.origin_set("H0", f_min, grid)
        assert np.allclose(h0c.lr, h0.lr, atol=1e-6) and np.array_equal(h0c.keep, h0.keep)
        for T in (466.0, 474.0, 480.0):
            win = pr.window(pr.edges(T, D))
            x = np.where(win.piece_hi <= T - D + 1e-9, f_min, 0.0)
            step = pr._profile(win, x, x, x, False)[0]
            assert pr.lr_origin("H0m", T, f_min) == pytest.approx(max(0.0, 2 * (pr.const_max(T)[0] - step)), abs=1e-6)


def test_H0m_origin_statistic_never_exceeds_H0cs_and_H0_with_detections_stays_bounded_by_it():
    pr = problem(strong_reference() + older_rows(40) + older_rows(30, "Dapingian", "Floian", 0, 3000) + older_rows(2, "Sandbian", "Floian", 1, 5000), k=2.0)
    for T in (466.0, 476.0, 490.0):
        for f_min in (1.0, 0.1):
            h0c, h0, h0m = (pr.lr_origin(cls, T, f_min) for cls in ("H0c", "H0", "H0m"))
            assert h0 <= h0c + 1e-6 and h0m <= h0 + 2e-3 or h0m <= h0c + 1e-6


def test_an_older_detection_wholly_older_than_t_makes_t_inadmissible():
    rows = strong_reference() + older_rows(20, young="Floian", old="Floian") + [("Dapingian", "Floian", 0, 5000, 1)]
    pr = problem(rows)
    assert pr.window(pr.edges_const(460.0)).impossible and not pr.window(pr.edges_const(475.0)).impossible
    assert pr.lr_origin("H0c", 460.0, 1.0) == math.inf
    assert np.isfinite(pr.lr_origin("H0c", 475.0, 1.0))
    assert pr.lr_origin("H0", 460.0, 1.0) == math.inf and pr.lr_origin("H0m", 460.0, 1.0) == math.inf


# --- the critical value and the specification ------------------------------------------------------


def test_count_critical_value_runs_from_the_rule_of_three_to_about_chi_square_one_sided():
    assert ev.count_crit(0) == pytest.approx(-2 * math.log(0.05), abs=1e-9)
    assert ev.count_crit(1) == pytest.approx(4.37, abs=0.02)
    assert 2.7 < ev.count_crit(500) < ev.count_crit(50) < 3.1
    assert ev.count_crit(0) > ev.count_crit(1) > ev.count_crit(5) > ev.count_crit(50)


def test_crit_shift_moves_the_critical_value():
    rows = strong_reference() + older_rows(20) + older_rows(2, d=1, cluster0=5000)
    assert problem(rows, crit_shift=0.7).crit(475.0) == pytest.approx(ev.count_crit(2) + 0.7)


def test_draft_specification_sets_every_inference_field():
    spec = ev.Spec.from_toml(SPEC_TOML)
    assert spec == ev.Spec()  # the draft declares the defaults; a frozen spec need not
    assert spec.classes == ("H0c", "H0m", "H0", "H1") and spec.h0m_lag_ma == 10.0 and spec.crit_shift == 0.0 and spec.age_scenario == "chart"


# --- the acceptance rule ---------------------------------------------------------------------------


def test_stage_one_thresholds_and_exact_limits():
    assert val.lower_limit(944, 1000) == pytest.approx(0.93053, abs=2e-5)
    assert val.stage1(944) == "pass" and val.stage1(943) == "borderline"
    assert val.stage1(915) == "fail" and val.stage1(916) == "borderline"
    assert val.upper_limit(915, 1000) < 0.93 <= val.upper_limit(916, 1000)


def test_stage_two_pooled_threshold():
    assert val.STAGE2_PASS == 1886
    assert val.stage2(1886) == "pass" and val.stage2(1885) == "fail"


@pytest.mark.parametrize("coverage, expected", [(0.95, 0.95039), (0.94, 0.42713), (0.93, 0.04837), (0.92, 0.00212)])
def test_acceptance_operating_characteristics(coverage, expected):
    assert val.pass_probability(coverage) == pytest.approx(expected, abs=6e-6)


def test_one_stage_rule_alone_would_fail_good_cells():
    assert stats.binom.sf(943, 1000, 0.95) == pytest.approx(0.83, abs=0.01)


def test_calibration_shift_is_the_smallest_nonnegative_shift_reaching_the_target():
    margins = [-math.inf] * 50 + list(np.linspace(-1.0, 1.0, 50))
    assert val.CALIBRATION_TARGET == 0.955
    assert val.shift_to_target(margins) == pytest.approx(np.sort(margins)[95])
    assert val.shift_to_target(margins, 0.95) == pytest.approx(np.sort(margins)[94])
    assert val.shift_to_target([-1.0] * 100) == 0.0 and val.shift_to_target([math.inf] * 10) == math.inf


# --- the simulator and the real selection ----------------------------------------------------------


def test_simulated_design_follows_the_effort_and_tau_comes_from_the_record():
    s = us.simulate(us.Truth(history="H0c", f=0.3), us.Design(scale=0.05), 5)
    effort = us.spore_effort()
    assert abs(len(s.units) - sum(round(0.05 * n) for st, n in effort.items() if round(0.05 * n) > 0)) == 0
    assert np.all(s.units.young <= s.units.old)
    broad = (s.units.old > s.units.young).mean()
    assert 0.05 < broad < 0.25
    pr = ev.Problem(s.units, ev.Spec(nodes=8), AGE)
    certain = (s.units.d == 1) & (s.units.young == s.units.old)
    assert pr.s_star == s.units.old[certain].max() and pr.tau == TS.base[pr.s_star]


def test_true_paths_and_members():
    t = np.array([440.0, 455.0, 465.0, 470.0, 475.0, 480.0])
    d = us.Design()
    assert us.Truth(history="H0c", f=0.3, t0=476.0).path(d)(t).tolist() == [1.0, 0.3, 0.3, 0.3, 0.3, 0.0]
    assert us.Truth(history="step", f=0.3, t0=476.0, delay=4.3).path(d)(t).tolist() == [1.0, 0.3, 0.3, 0.3, 0.0, 0.0]
    ramp = us.Truth(history="ramp", t0=476.0, tau0=452.8).path(d)(np.array([452.8 + 1e-9, 464.4, 476.0]))
    assert ramp == pytest.approx([1.0, 0.5, 0.0], abs=1e-6)
    lg = us.Truth(history="logistic", g=0.3, h=7.7, t0=476.0, tau0=452.8).path(d)(np.array([452.8 + 1e-9, 476.0]))
    assert lg[0] == pytest.approx(1.0, abs=1e-6) and 0 < lg[1] < 0.2
    members = {h: us.Truth(history=h).members for h in us.HISTORIES}
    assert members["H0c"] == ("H0c", "H0m", "H0", "H1") and members["hide"] == ("H0", "H1") and members["hide_h1"] == ("H1",)
    assert all(m == ("H0m", "H0", "H1") for h, m in members.items() if h in ("step", "ramp", "logistic"))


@pytest.mark.parametrize("history, height", [("hide", 1.0), ("hide_h1", 3.0)])
def test_hide_path_lights_the_stages_with_fewest_units_per_myr_until_the_average_is_f(history, height):
    truth = us.Truth(history=history, f=0.3, t0=476.0, tau0=452.8)
    design = us.Design()
    path = truth.path(design)
    t = np.linspace(452.8, 476.0, 232001)[1:]
    a = path(t)
    assert set(np.unique(a)) <= {0.0, height} and a.mean() == pytest.approx(0.3, abs=2e-4)
    lit = np.array(truth.lit(design, AGE))
    assert lit[0, 1] == pytest.approx(469.4)  # Darriwilian has the fewest units per Myr and is filled from its older end
    assert path(np.array([440.0, 477.0])).tolist() == [1.0, 0.0]
    assert all(lo >= 452.8 and hi <= 476.0 for lo, hi in lit)


def test_design_options_confound_class_with_age_and_mislabel_reports_and_confine():
    base = us.simulate(us.Truth(f=0.5), us.Design(scale=0.2), 3)
    trend = us.simulate(us.Truth(f=0.5), us.Design(scale=0.2, class_trend=0.8), 3)
    older = trend.t_true > 470
    assert (trend.cls_true[older] == 0).mean() > 0.7 > 0.5 > (trend.cls_true[~older] == 0).mean()
    assert abs((base.cls_true == 0).mean() - 0.6) < 0.06
    mis = us.simulate(us.Truth(f=0.5), us.Design(scale=0.2, misassign=0.3), 3)
    assert 0.2 < (mis.units.cls != mis.cls_true).mean() < 0.4
    rep = us.simulate(us.Truth(f=0.5, t0=500.0), us.Design(scale=0.2, older_report=0.5), 3)
    mid = (rep.t_true > 452.8) & (rep.t_true <= 500.0)
    assert np.allclose(rep.a_unit[mid], 0.25) and np.allclose(rep.a_unit[rep.t_true <= 452.8], 1.0) and np.all(rep.a_unit[rep.t_true > 500.0] == 0.0)
    conf = us.simulate(us.Truth(f=0.5, t0=500.0), us.Design(scale=0.2, confine=0.5), 3)
    older_units = (conf.t_true > 452.8) & (conf.t_true <= 500.0)
    in_b = conf.a_unit[older_units] == 0
    assert 0.3 < in_b.mean() < 0.7 and np.all(np.isin(conf.a_unit[older_units], [0.0, 0.5]))
    clusters = conf.units.cluster[older_units]
    assert all(len(set(in_b[clusters == c])) == 1 for c in np.unique(clusters))



def test_shared_age_puts_each_cluster_at_one_position_in_its_ranges_and_keeps_the_marginal():
    base = AGE.base
    s = us.simulate(us.Truth(f=0.5), us.Design(scale=0.2, shared_age=True), 3)
    u = s.units
    pos = (s.t_true - base[u.young - 1]) / (base[u.old] - base[u.young - 1])
    assert np.all((pos >= 0) & (pos <= 1))
    assert all(np.ptp(pos[u.cluster == c]) < 1e-9 for c in np.unique(u.cluster))
    first = np.unique(u.cluster, return_index=True)[1]
    assert abs(pos[first].mean() - 0.5) < 0.05 and abs((pos[first] < 0.25).mean() - 0.25) < 0.06
    big = us.simulate(us.Truth(f=0.5), us.Design(scale=0.2, cluster_mean=10.0), 3)
    assert 8 < len(big.units.cluster) / len(np.unique(big.units.cluster)) < 12
    shared = next(c for c in val.CELLS if c["name"] == "D8")
    assert val.cell_objects(shared)[1] == us.Design(k=2.0, scale=0.05, cluster_mean=10.0, shared_age=True)

def test_truth_scenario_moves_the_true_ages():
    for scenario in ("older", "younger"):
        design = us.Design(truth_scenario=scenario)
        s = us.simulate(us.Truth(), design, 4)
        base = ev.AgeModel.load(scenario=scenario).base
        assert np.all(s.t_true >= base[s.units.young - 1]) and np.all(s.t_true <= base[s.units.old])


def test_true_target_for_a_known_path():
    truth = us.Truth(history="H0c", f=0.4, t0=476.0)
    s = us.simulate(truth, us.Design(), 6)
    pr = ev.Problem(s.units, ev.Spec(nodes=8), AGE)
    assert pr.tau >= truth.tau0, "seed chosen so that tau lies at or older than the point where a leaves 1"
    path = truth.path()
    assert pr.abar_truth(path, 476.0, s.r[pr.calibrated]) == pytest.approx(0.4, abs=5e-3)
    assert us.min_intensity(path, pr.tau, 476.0) == 0.4 and us.min_intensity(path, 500.0, 476.0) == 1.0
    eff = us.effective_path(path, truth, us.Design(older_report=0.5, confine=0.2))
    assert eff(np.array([440.0, 460.0])).tolist() == pytest.approx([1.0, 0.4 * 0.5 * 0.8])


def test_harness_replicate_records_coverage_statistics_informativeness_and_states():
    cell = next(c for c in val.CELLS if c["name"] == "A4")
    row = val.replicate((cell, 0, val.ROOT_SEEDS["dev"], 0.0))
    assert row["error"] == "" and row["no_tau"] is False
    for key in ("tau", "trivial", "cover_set_H0c_1", "cover_set_H0m_0.1", "cover_set_H0_0.01", "lr0_H0c_0.01", "endpoint_H0c_1", "state_H0", "fstar_H0c", "lr_H0c", "state459_H0",
                "fstar459_H0m", "crit_t0", "a_ref", "a_ref_realised", "abar_rel", "state_H1-no-ceiling", "n_fits", "n_flagged", "n_failed", "seconds", "fmin_applicable_H0m",
                "ok_lr_H0", "ok_fstar_H0m", "ok_lr0_H0_0.1", "ok_set_H0c_1", "spread_fstar_H0c", "ok459_H0m", "spread459_H1"):
        assert key in row
    assert row["state_H0"] in ev.STATES and row["state_H1-no-ceiling"] in ev.STATES
    summary = val.summarise(cell, [row])
    assert summary["n_valid"] == 1 and "cover_set_applicable_H0c" in summary and "fcover_H0c" in summary and "delta_f_H0" in summary
    assert "ocover_H0c_0.1" in summary and "ocover_H0c_1" not in summary and "delta_ocover_H0m_0.01" in summary and "failed_f_H0" in summary
    assert {"fcover_test_H0c", "mismatch_f_H0c", "ocover_set_H0c_0.1", "ocover_test_H0c_0.1", "mismatch_ocover_H0c_0.1", "failed459_H0"} <= set(summary)
    assert "fcover_chi2_H0c" not in summary and not any("chi2" in k or "logistic" in k for k in row)


def test_reference_normalisation_integrates_the_path_over_each_unit_range():
    lo, hi = np.array([440.0, 445.0]), np.array([444.0, 455.0])
    assert val.range_mean(lambda t: np.full_like(t, 0.7), lo, hi) == pytest.approx([0.7, 0.7])
    assert val.range_mean(lambda t: t - 440.0, lo, hi) == pytest.approx([2.0, 10.0], abs=1e-6)
    step = lambda t: np.where(t > 450.0, 0.2, 1.0)
    assert val.range_mean(step, lo, hi)[1] == pytest.approx(0.6, abs=1e-3)


def test_coverage_counts_no_claim_as_covered_and_errors_and_failed_statistics_as_not():
    rows = [dict(error="", no_tau=False, lr=1.0, ok=True), dict(error="", no_tau=False, lr=9.0, ok=True),
            dict(error="", no_tau=False, lr=1.0, ok=False), dict(error="", no_tau=True), dict(error="boom", no_tau=False)]
    covers = lambda r: r["lr"] <= 3.0 and r["ok"]
    assert val.coverage(rows, covers) == pytest.approx(2 / 5)
    m = val.margins(rows, lambda r: r["lr"] - 3.0, lambda r: r["ok"])
    assert m == [-2.0, 6.0, math.inf, -math.inf, math.inf]


def test_delivered_coverage_needs_the_reported_bound_and_set_to_have_succeeded():
    cell = next(c for c in val.CELLS if c["name"] == "A4")
    row = val.replicate((cell, 0, val.ROOT_SEEDS["dev"], 0.0))
    good = dict(row, trivial=False, lr_H0c=0.0, ok_lr_H0c=True, ok_fstar_H0c=True, state_H0c="finite", fstar_H0c=0.5, abar_rel=0.3,
                **{"lr0_H0c_0.1": 0.0, "ok_lr0_H0c_0.1": True, "ok_set_H0c_0.1": True, "cover_set_H0c_0.1": True})
    bound_failed = dict(good, ok_fstar_H0c=False)
    set_failed = dict(good, **{"ok_set_H0c_0.1": False})
    grid_misses = dict(good, **{"cover_set_H0c_0.1": False})
    s = val.summarise(cell, [good, bound_failed, set_failed, grid_misses])
    assert s["fcover_test_H0c"] == 1.0 and s["fcover_H0c"] == 0.75 and s["failed_f_H0c"] == 1 and s["failed_fstar_H0c"] == 1
    assert s["delta_f_H0c"] == math.inf  # one failed bound in four: no shift reaches the target
    assert s["ocover_test_H0c_0.1"] == 1.0 and s["ocover_H0c_0.1"] == 0.5 and s["ocover_set_H0c_0.1"] == 0.5
    assert s["failed_ocover_H0c_0.1"] == 1 and s["mismatch_ocover_H0c_0.1"] == 1 and s["mismatch_f_H0c"] == 0
    assert s["delta_ocover_H0c_0.1"] == math.inf  # a failed set and a grid set that omits t0: neither can be shifted into coverage
    omitted = val.summarise(cell, [dict(good, fstar_H0c=0.2)])  # the test covers, the delivered bound does not
    assert omitted["mismatch_f_H0c"] == 1 and omitted["fcover_test_H0c"] == 1.0 and omitted["fcover_H0c"] == 0.0 and omitted["delta_f_H0c"] == math.inf
    assert val.summarise(cell, [dict(good, fstar_H0c=0.2995)])["fcover_H0c"] == 1.0  # within the root tolerance


def _receipt(**changes) -> dict:
    parts = [dict(cell=c, quantity=q, delta=0.1) for c, q in sorted(val.grid_quantities())]
    return val.protocol() | dict(delta=0.1, parts=parts, sha256=val.code_hashes()) | changes


def test_acceptance_refuses_a_receipt_outside_its_calibrated_scope():
    assert val.check_receipt(_receipt()) == 0.1
    parts = _receipt()["parts"]
    for bad in (dict(reps=5), dict(start=1000), dict(root_seed=val.ROOT_SEEDS["dev"]), dict(target=0.95), dict(sha256={}),
                dict(delta=math.nan), dict(delta=-0.1), dict(delta=math.inf), dict(delta=0.05), dict(parts=parts[:-1]), dict(parts=parts + parts[:1]),
                dict(parts=parts[:-1] + [dict(parts[-1], delta=math.nan)]), dict(parts=parts[:-1] + [dict(parts[-1], delta=-0.2)])):
        with pytest.raises(SystemExit):
            val.check_receipt(_receipt(**bad))


def test_stage_one_verdicts_count_each_acceptance_quantity():
    a6 = next(c for c in val.CELLS if c["name"] == "A6")
    s = {"name": "A6", "n_rep": 1000, "fcover_H0m": 0.944, "fcover_H0": 0.943, "fcover_H1": 0.915, "ocover_H0m_0.1": 0.95, "ocover_H0m_0.01": 0.916}
    v = val.stage1_verdicts([a6], [s])
    assert [x["k1"] for x in v] == [944, 943, 915, 950, 916]
    assert [x["stage1"] for x in v] == ["pass", "borderline", "fail", "pass", "borderline"]
    assert [x["final"] for x in v] == ["pass", "pending", "fail", "pass", "pending"] and val.stage2_cells(v) == ["A6"]


def test_stage_two_reruns_only_borderline_cells_and_pools_their_counts():
    quantities = sorted(val.grid_quantities())
    verdicts = [dict(cell=c, quantity=q, k1=1000, stage1="pass", k2=None, pooled=None, final="pass") for c, q in quantities]
    assert val.grid_result(verdicts) == "accepted" and val.stage2_cells(verdicts) == []
    (c1, q1), (c2, q2) = quantities[0], quantities[-1]
    verdicts[0].update(k1=940, stage1="borderline", final="pending")
    verdicts[-1].update(k1=930, stage1="borderline", final="pending")
    assert val.grid_result(verdicts) == "stage 2 needed" and val.stage2_cells(verdicts) == [c1, c2]
    pooled = val.pooled_verdicts(verdicts, [{"name": c1, "n_rep": 1000, q1: 0.946}, {"name": c2, "n_rep": 1000, q2: 0.955}])
    assert (pooled[0]["k2"], pooled[0]["pooled"], pooled[0]["final"]) == (946, 1886, "pass")
    assert (pooled[-1]["k2"], pooled[-1]["pooled"], pooled[-1]["final"]) == (955, 1885, "fail")
    assert pooled[1:-1] == verdicts[1:-1] and val.grid_result(pooled) == "rejected" and val.grid_result(pooled[:-1]) == "incomplete"


@functools.lru_cache(maxsize=1)
def _a4_replicates(n: int = 3) -> tuple:
    a4 = next(c for c in val.CELLS if c["name"] == "A4")
    return tuple(val.replicate((a4, j, val.ROOT_SEEDS["accept"], 0.0)) for j in range(n))


def _write_stage1(tmp_path, rows: list[dict], summary: list[dict]) -> dict:
    val.write_csv(tmp_path / "validation_acc1.csv", summary)
    val.write_csv(tmp_path / "validation_acc1_reps.csv", rows, exact=True)
    return val.evidence("acc1")


def _stage1(tmp_path, monkeypatch):
    """A real stage 1 on a one-cell grid (A4) with N1 = 3: replicate rows, their summary and the verdict file."""
    a4 = next(c for c in val.CELLS if c["name"] == "A4")
    monkeypatch.setattr(val, "OUT", tmp_path)
    monkeypatch.setattr(val, "CELLS", [a4])
    monkeypatch.setattr(val, "N1", 3)
    rows = [dict(r) for r in _a4_replicates()]
    summary = [val.summarise(a4, rows)]
    verdicts = val.stage1_verdicts([a4], summary)
    return dict(stage=1, receipt_sha256="r", sha256=val.code_hashes(), root_seed=val.ROOT_SEEDS["accept"], start=0, reps=3,
                result=val.grid_result(verdicts), evidence=_write_stage1(tmp_path, rows, summary), quantities=verdicts)


def test_replicate_tables_round_trip_exactly_for_rescoring(tmp_path):
    rows = [dict(r) for r in _a4_replicates()]
    val.write_csv(tmp_path / "reps.csv", rows, exact=True)
    back = val.read_reps(tmp_path / "reps.csv")
    a4 = next(c for c in val.CELLS if c["name"] == "A4")
    assert val.summarise(a4, back) == pytest.approx(val.summarise(a4, rows), nan_ok=True)


def test_stage_two_refuses_a_stage_one_from_another_receipt_code_seed_or_scope(tmp_path, monkeypatch):
    first = _stage1(tmp_path, monkeypatch)
    val.check_stage1(first, "r", tmp_path)
    for change in (dict(receipt_sha256="x"), dict(sha256={}), dict(start=1000), dict(reps=5), dict(root_seed=val.ROOT_SEEDS["calibrate"]),
                   dict(result="rejected"), dict(stage=2), dict(evidence={})):
        with pytest.raises(SystemExit):
            val.check_stage1(first | change, "r", tmp_path)


def test_stage_two_derives_verdicts_from_counts_and_counts_from_the_stage_one_evidence(tmp_path, monkeypatch):
    first = _stage1(tmp_path, monkeypatch)
    q = first["quantities"]
    relabel = lambda v, k: dict(v, k1=k, stage1=val.stage1(k, 3), final=val.stage1(k, 3) if val.stage1(k, 3) != "borderline" else "pending")
    k = q[1]["k1"]
    for quantities in (
        q[:1] + [dict(q[1], k1=k - 1)] + q[2:],  # a count changed, its labels kept
        q[:1] + [relabel(q[1], k - 1)] + q[2:],  # a consistent relabel that its summary and replicates contradict
        q[:1] + [dict(q[1], k1=float(k))] + q[2:], q[:1] + [dict(q[1], k1=4)] + q[2:],  # not an integer count in range
        q[:-1], q + q[-1:],  # a quantity missing or repeated
        q[:1] + [dict(q[1], k2=3, pooled=k + 3)] + q[2:],  # stage-2 fields already filled
    ):
        with pytest.raises(SystemExit):
            val.check_stage1(first | dict(quantities=quantities, result=val.grid_result(quantities)), "r", tmp_path)
    (tmp_path / "validation_acc1.csv").write_text((tmp_path / "validation_acc1.csv").read_text() + "\n")
    with pytest.raises(SystemExit):
        val.check_stage1(first, "r", tmp_path)  # the summary no longer matches its hash


def test_stage_two_rescores_the_stage_one_replicates(tmp_path, monkeypatch):
    first = _stage1(tmp_path, monkeypatch)
    a4 = val.CELLS[0]
    rows = [dict(r) for r in _a4_replicates()]
    summary = val.summarise(a4, rows)
    for bad_rows, bad_summary in (
        (rows[:-1], summary),  # a replicate missing
        (rows + rows[-1:], summary),  # a replicate repeated
        ([dict(rows[0], error="boom")] + rows[1:], summary),  # a failed replicate behind an all-success summary
        (rows, dict(summary, n_rep=6)),  # a summary over the wrong number of replicates
    ):
        evidence = _write_stage1(tmp_path, bad_rows, [bad_summary])
        with pytest.raises(SystemExit):
            val.check_stage1(first | dict(evidence=evidence), "r", tmp_path)


def test_stage_two_refuses_malformed_replicate_ids_and_flags(tmp_path, monkeypatch):
    first = _stage1(tmp_path, monkeypatch)
    rows = [dict(r) for r in _a4_replicates()]
    summary = val.summarise(val.CELLS[0], rows)
    assert {"fcover_H0c"} <= {v["quantity"] for v in first["quantities"]}
    for bad_rows in (
        [dict(r, rep=r["rep"] + 0.25) for r in rows],  # fractional ids that int() would truncate to 0, 1, 2
        [dict(rows[0], rep=False), dict(rows[1], rep=True)] + rows[2:],  # Boolean ids
        [dict(rows[0], ok_fstar_H0c="")] + rows[1:],  # a scored flag missing
        [dict(rows[0], ok_lr_H0c="false")] + rows[1:],  # a scored flag in a non-Boolean encoding
    ):
        evidence = _write_stage1(tmp_path, bad_rows, [summary])
        with pytest.raises(SystemExit, match="malformed"):
            val.check_stage1(first | dict(evidence=evidence), "r", tmp_path)


def test_stage_two_refuses_bound_states_outside_the_engine_invariants(tmp_path, monkeypatch):
    """Codex's case (review 2026-10-31): a bound pushed below the truth is refused as finite, and must not pass by
    renaming its state."""
    first = _stage1(tmp_path, monkeypatch)
    rows = [dict(r) for r in _a4_replicates()]
    summary = val.summarise(val.CELLS[0], rows)
    j = next(i for i, r in enumerate(rows) if not r["no_tau"] and not r["trivial"] and r["abar_rel"] > 0)
    below = [dict(r) for r in rows]
    below[j]["fstar_H0c"] = 0.0
    for bad_rows, match in (
        (below, "refused"),  # a well-formed but uncovering bound: the old summary no longer matches
        ([dict(r, state_H0c="bogus") if i == j else r for i, r in enumerate(below)], "malformed"),
        ([dict(r, state_H0c="ceiling-limited") if i == j else r for i, r in enumerate(below)], "malformed"),
        ([dict(r, state_H0c="zero-exposure") if i == j else r for i, r in enumerate(below)], "malformed"),
        ([dict(r, state459_H0c="bogus") if i == j else r for i, r in enumerate(rows)], "malformed"),
        ([dict(r, **{"state_H1-no-ceiling": "finite"}) if i == j else r for i, r in enumerate(rows)], "malformed"),
        # Codex's second case: zero exposure with no value, yet a finite truth and truth-point statistic retained
        ([dict(r, state_H0c="zero-exposure", fstar_H0c=math.nan) if i == j else r for i, r in enumerate(rows)], "malformed"),
    ):
        evidence = _write_stage1(tmp_path, bad_rows, [summary])
        with pytest.raises(SystemExit, match=match):
            val.check_stage1(first | dict(evidence=evidence), "r", tmp_path)


def test_stage_one_evidence_may_be_read_through_its_compressed_copy(tmp_path, monkeypatch):
    first = _stage1(tmp_path, monkeypatch)
    reps = tmp_path / "validation_acc1_reps.csv"
    (tmp_path / "validation_acc1_reps.csv.gz").write_bytes(gzip.compress(reps.read_bytes()))
    reps.unlink()
    val.check_stage1(first, "r", tmp_path)


def test_origin_readouts_are_acceptance_quantities_only_where_the_truth_satisfies_them_for_every_tau():
    got = {c["name"]: val.origin_readouts(*val.cell_objects(c)) for c in val.CELLS if c["name"] in ("A1", "A2", "A6", "A7", "A9", "A10")}
    assert got["A1"] == {"H0c": [1.0, 0.1, 0.01], "H0m": [1.0, 0.1, 0.01], "H0": [1.0, 0.1, 0.01]}
    assert got["A2"] == {"H0c": [0.1, 0.01], "H0m": [0.1, 0.01], "H0": [0.1, 0.01]}
    assert got["A6"] == {"H0c": [], "H0m": [0.1, 0.01], "H0": []}
    assert got["A7"] == {"H0c": [], "H0m": [0.1, 0.01], "H0": []}
    assert got["A9"] == {"H0c": [], "H0m": [], "H0": []} and got["A10"] == got["A9"]
    d2 = next(c for c in val.CELLS if c["name"] == "D2")
    assert val.acceptance_quantities(d2) == []
    a6 = [q[0] for q in val.acceptance_quantities(next(c for c in val.CELLS if c["name"] == "A6"))]
    assert a6 == ["fcover_H0m", "fcover_H0", "fcover_H1", "ocover_H0m_0.1", "ocover_H0m_0.01"]


def test_calibrated_shift_is_the_largest_shift_over_the_acceptance_quantities():
    cells = [c for c in val.CELLS if c["name"] in ("A6", "D2")]
    summary = [{"name": "A6", "delta_f_H0m": 0.0, "delta_f_H0": 0.2, "delta_f_H1": 0.1, "delta_ocover_H0m_0.1": 0.4, "delta_ocover_H0m_0.01": 0.0},
               {"name": "D2", "delta_f_H0c": 9.0}]
    delta, parts = val.calibrated_shift(summary, cells)
    assert delta == 0.4 and len(parts) == 5


def test_harness_cells_cover_the_declared_scenarios():
    names = [c["name"] for c in val.CELLS]
    assert names == [f"A{i}" for i in range(1, 16)] + [f"D{i}" for i in range(1, 10)]
    assert all(c["kind"] == ("acceptance" if c["name"][0] == "A" else "diagnostic") for c in val.CELLS)
    for c in val.CELLS:
        truth, design, spec = val.cell_objects(c)
        assert spec.age_scenario == "chart" and truth.t0 > truth.tau0
    d4 = next(c for c in val.CELLS if c["name"] == "D4")
    assert d4["k"] == 0.8 and val.cell_objects(d4)[2].cluster_shape_k == 2.0
    assert next(c for c in val.CELLS if c["name"] == "A5")["nodes"] == 64
