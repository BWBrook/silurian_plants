"""Checks of the ramp-aware estimators, the realistic inputs and the recovery-study machinery.

    uv run --with pytest --with numpy --with scipy pytest studies/f3/models

Ages are Ma, decreasing towards the present. Datasets built from expected counts (psi * E * integral
of N, not integers) carry no sampling noise, so the likelihood must peak at the truth. Coverage tests
use fixed seeds.
"""

import csv

import numpy as np
import pytest
from scipy import integrate, optimize

import inputs
import ramp
import recovery
import report
import sim

TS = sim.Timescale.load()
SERIES = inputs.effort_series()
EDGES = SERIES.edges
FIRST = TS.index("Emsian")
EFFORT = np.array([SERIES.spores / SERIES.spores.mean(), SERIES.bodies / SERIES.bodies.mean()])
LOGISTIC = ramp.RampModel(EDGES, ramp.Logistic(100.0))
BIRTH_DEATH = ramp.RampModel(EDGES, ramp.ExpectedBirthDeath())
LOGISTIC_TRUTH = {"rate": 0.3, "k": 100.0}


def expected_counts(model, t0, params, totals):
    mass = model.stage_mass(t0, params)
    psi = np.array([total / (EFFORT[c] @ mass) for c, total in enumerate(totals)])
    return psi[:, None] * EFFORT * mass


def sampled_counts(growth, t0, psi, seed=0):
    channels = {
        "a": sim.Channel(psi[0], dict(zip(SERIES.stages, EFFORT[0].tolist()))),
        "b": sim.Channel(psi[1], dict(zip(SERIES.stages, EFFORT[1].tolist()))),
    }
    run = sim.simulate(growth, t0, channels, float(EDGES[0]), TS, seed)
    return np.array([np.bincount(run.records[c].stage - FIRST, minlength=len(SERIES.stages)) for c in ("a", "b")])


def exponential_abundance(t0, g, window_end, step=0.005):
    s = np.arange(0.0, t0 - window_end + step, step)
    s[-1] = t0 - window_end
    return sim.Abundance((t0 - s)[::-1], np.exp(g * (s[:-1] + s[1:]) / 2)[::-1])


# --- stage integrals -------------------------------------------------------------------------


def stage_overlap(t0, j):
    """The part of stage j (index into the window, youngest first) younger than t0, as s = t0 - t."""
    top, base = EDGES[j], EDGES[j + 1]
    return (0.0, 0.0) if t0 <= top else (t0 - min(base, t0), t0 - top)


@pytest.mark.parametrize("t0", [431.5, 437.0, 462.0])
def test_logistic_stage_mass_matches_quadrature(t0):
    r, k = 0.3, 100.0
    mass = LOGISTIC.stage_mass(t0, {"rate": r, "k": k})
    for j in range(len(SERIES.stages)):
        lo, hi = stage_overlap(t0, j)
        expected = integrate.quad(lambda s: k / (1 + (k - 1) * np.exp(-r * s)), lo, hi)[0] if hi > lo else 0.0
        assert mass[j] == pytest.approx(expected, rel=1e-9, abs=1e-12)


@pytest.mark.parametrize("g", [0.0, 0.03, 0.1, 0.4])
def test_birth_death_stage_mass_matches_quadrature(g):
    t0 = 437.0
    mass = BIRTH_DEATH.stage_mass(t0, {"rate": g})
    for j in range(len(SERIES.stages)):
        lo, hi = stage_overlap(t0, j)
        expected = integrate.quad(lambda s: np.exp(g * s), lo, hi)[0] if hi > lo else 0.0
        assert mass[j] == pytest.approx(expected, rel=1e-9, abs=1e-12)


def test_stage_mass_matches_the_simulators_abundance():
    t0 = 437.0
    ab = sim.simulate_abundance(sim.Logistic(0.3, 100.0), t0, float(EDGES[0]), 0)
    simulated = sim.stage_exposure(ab, TS)[FIRST : FIRST + len(SERIES.stages)]
    assert LOGISTIC.stage_mass(t0, LOGISTIC_TRUTH) == pytest.approx(simulated, rel=2e-3, abs=1e-9)
    ab = exponential_abundance(t0, 0.1, float(EDGES[0]))
    simulated = sim.stage_exposure(ab, TS)[FIRST : FIRST + len(SERIES.stages)]
    assert BIRTH_DEATH.stage_mass(t0, {"rate": 0.1}) == pytest.approx(simulated, rel=1e-3, abs=1e-9)


def test_no_abundance_before_origination_and_the_origination_stage_is_truncated():
    t0 = 435.0  # inside the Telychian, [432.9, 438.6)
    mass = BIRTH_DEATH.stage_mass(t0, {"rate": 0.0})
    names = SERIES.stages
    assert np.all(mass[names.index("Aeronian") :] == 0.0)
    assert mass[names.index("Telychian")] == pytest.approx(t0 - 432.9)
    assert mass[names.index("Sheinwoodian")] == pytest.approx(432.9 - 430.6)


def test_edges_must_ascend_with_age():
    with pytest.raises(ValueError):
        ramp.RampModel(EDGES[::-1], ramp.ExpectedBirthDeath())


def test_bad_inputs_are_rejected():
    n, e = np.ones((1, 15)), np.ones((1, 15))
    for bad_n, bad_e in [(-n, e), (n, -e), (np.zeros((1, 15)), e), (n[:, :14], e[:, :14]), (n, e[:, :14])]:
        with pytest.raises(ValueError):
            ramp.fit(BIRTH_DEATH, bad_n, bad_e)
    no_effort = e.copy()
    no_effort[0, 3] = 0.0
    with pytest.raises(ValueError):
        ramp.fit(BIRTH_DEATH, n, no_effort)


# --- recovery of known parameters -------------------------------------------------------------


def test_expected_counts_peak_at_the_truth():
    for model, t0, params in [(LOGISTIC, 437.0, LOGISTIC_TRUTH), (BIRTH_DEATH, 437.0, {"rate": 0.1}), (LOGISTIC, 460.0, {"rate": 0.15, "k": 100.0})]:
        n = expected_counts(model, t0, params, (500, 200))
        f = ramp.fit(model, n, EFFORT)
        assert f.t0 == pytest.approx(t0, abs=1e-3)
        assert f.params["rate"] == pytest.approx(params["rate"], rel=1e-3)
        assert f.lo <= t0 <= f.hi


def test_large_sample_logistic_recovers_origination_rate_and_psi():
    t0, psi = 437.0, np.array([40.0, 8.0])
    n = sampled_counts(sim.Logistic(0.3, 100.0), t0, psi, seed=1)
    assert n.sum() > 100_000
    f = ramp.fit(LOGISTIC, n, EFFORT)
    assert f.t0 == pytest.approx(t0, abs=0.1)
    assert f.params["rate"] == pytest.approx(0.3, rel=0.02)
    assert f.psi == pytest.approx(psi, rel=0.02)
    assert f.lo <= t0 <= f.hi and f.hi - f.lo < 1.0 and f.bounded


def test_large_sample_birth_death_recovers_origination_and_net_rate():
    t0, psi = 437.0, np.array([40.0, 8.0])
    ab = exponential_abundance(t0, 0.1, float(EDGES[0]))
    channels = {c: sim.Channel(p, dict(zip(SERIES.stages, EFFORT[i].tolist()))) for i, (c, p) in enumerate(zip("ab", psi))}
    records = sim.simulate_records(ab, channels, TS, 2)
    n = np.array([np.bincount(records[c].stage - FIRST, minlength=len(SERIES.stages)) for c in "ab"])
    f = ramp.fit(BIRTH_DEATH, n, EFFORT)
    assert f.t0 == pytest.approx(t0, abs=0.1)
    assert f.params["rate"] == pytest.approx(0.1, rel=0.03)
    assert f.psi == pytest.approx(psi, rel=0.03)
    assert f.lo <= t0 <= f.hi


def test_constant_abundance_gives_zero_net_rate():
    n = sampled_counts(sim.Constant(50), 437.0, np.array([0.08, 0.02]), seed=3)
    f = ramp.fit(BIRTH_DEATH, n, EFFORT)
    assert f.params["rate"] < 0.01
    assert f.lo <= 437.0 <= f.hi


# --- two channels ------------------------------------------------------------------------------


def test_joint_fit_reduces_to_one_channel_when_the_second_has_no_effort():
    n = expected_counts(LOGISTIC, 437.0, LOGISTIC_TRUTH, (120, 40))
    noisy = np.round(n)
    for model, data in [(LOGISTIC, noisy), (BIRTH_DEATH, noisy)]:
        one = ramp.fit(model, data[:1], EFFORT[:1])
        joint = ramp.fit(model, np.vstack([data[:1], np.zeros(15)]), np.vstack([EFFORT[:1], np.zeros(15)]))
        assert (joint.t0, joint.lo, joint.hi, joint.bounded) == (one.t0, one.lo, one.hi, one.bounded)
        assert joint.loglik == pytest.approx(one.loglik)
        assert joint.psi[0] == pytest.approx(one.psi[0])
        assert np.array_equal(joint.profile, one.profile)


def test_joint_surface_is_the_sum_of_the_channel_surfaces():
    n = np.round(expected_counts(LOGISTIC, 437.0, LOGISTIC_TRUTH, (120, 40)))
    both, first, second = (LOGISTIC.surface(n, EFFORT), LOGISTIC.surface(n[:1], EFFORT[:1]), LOGISTIC.surface(n[1:], EFFORT[1:]))
    finite = np.isfinite(both)
    assert finite.any() and np.allclose(both[finite], (first + second)[finite])
    assert np.array_equal(finite, np.isfinite(first) & np.isfinite(second))


def test_joint_fit_bounds_the_origination_when_neither_channel_does():
    n = expected_counts(LOGISTIC, 460.0, LOGISTIC_TRUTH, (15, 15))
    spores, bodies, joint = (ramp.fit(LOGISTIC, n[idx], EFFORT[idx]) for idx in ([0], [1], [0, 1]))
    assert not spores.bounded and not bodies.bounded
    assert joint.bounded and joint.lo <= 460.0 <= joint.hi < ramp.T0_MAX
    assert joint.loglik - joint.profile[-1] > ramp.PROFILE_LEVEL


def test_a_channel_with_one_flat_profile_leaves_the_other_to_decide():
    n = expected_counts(BIRTH_DEATH, 437.0, {"rate": 0.1}, (300, 3))
    spores, bodies, joint = (ramp.fit(BIRTH_DEATH, n[idx], EFFORT[idx]) for idx in ([0], [1], [0, 1]))
    assert spores.bounded and not bodies.bounded
    assert joint.lo == pytest.approx(spores.lo, abs=0.5) and joint.hi == pytest.approx(spores.hi, abs=0.5)


# --- age convention and profile ----------------------------------------------------------------


def test_origination_is_never_younger_than_the_oldest_stage_with_records():
    n = np.zeros((1, 15))
    n[0, SERIES.stages.index("Pridoli")] = 4
    n[0, SERIES.stages.index("Lochkovian")] = 10
    n[0, SERIES.stages.index("Emsian")] = 25
    f = ramp.fit(BIRTH_DEATH, n, EFFORT[:1])
    assert f.t0 > 419.62 and f.lo >= 419.62  # the top of the Pridoli
    older = np.roll(n, 1, axis=1)  # every record one stage older
    g = ramp.fit(BIRTH_DEATH, older, EFFORT[:1])
    assert g.t0 > f.t0 and g.lo > f.lo
    assert np.all(np.diff(f.t0_grid) > 0) and f.lo <= f.t0 <= f.hi


def test_records_in_the_youngest_stage_alone_put_origination_in_the_window():
    n = np.zeros((1, 15))
    n[0, 0] = 30
    f = ramp.fit(BIRTH_DEATH, n, EFFORT[:1])
    assert f.t0 > EDGES[0] and f.lo >= EDGES[0]


def test_profile_is_unbounded_for_a_birth_death_ramp_with_few_records_and_bounded_for_a_dense_constant_record():
    sparse = expected_counts(BIRTH_DEATH, 435.0, {"rate": 0.1}, (20, 3))
    f = ramp.fit(BIRTH_DEATH, sparse[:1], EFFORT[:1])
    assert not f.bounded and f.hi == ramp.T0_MAX and f.lo == pytest.approx(432.9)
    n = expected_counts(BIRTH_DEATH, 437.0, {"rate": 0.0}, (400, 100))
    g = ramp.fit(BIRTH_DEATH, n[:1], EFFORT[:1])
    assert g.bounded and g.hi < 440.0


def test_profile_interval_covers_at_its_nominal_rate_under_its_own_model():
    n_reps, covered = 300, 0
    window = (430.6, 438.6)
    for i in range(n_reps):
        seed = sim.child_seed(20261030, i)
        t0 = float(np.random.default_rng(sim.child_seed(seed, 1)).uniform(*window))
        ab = sim.simulate_abundance(sim.Logistic(0.3, 100.0), t0, float(EDGES[0]), 0)
        mass = sim.stage_exposure(ab, TS)[FIRST : FIRST + 15]
        psi = [250 / (EFFORT[0] @ mass), 80 / (EFFORT[1] @ mass)]
        n = sampled_counts(sim.Logistic(0.3, 100.0), t0, np.array(psi), seed=sim.child_seed(seed, 2))
        f = ramp.fit(LOGISTIC, n, EFFORT)
        covered += f.lo <= t0 <= f.hi
    assert 0.91 <= covered / n_reps <= 0.99


@pytest.mark.parametrize(
    "model, growth, psi, extra",
    [
        (LOGISTIC, sim.Logistic(0.3, 100.0), (0.03, 0.01), {"k": 100.0}),
        (BIRTH_DEATH, sim.BirthDeath(0.25, 0.15), (0.1, 0.02), {}),
    ],
)
def test_grid_profile_agrees_with_nested_optimisation(model, growth, psi, extra):
    n = sampled_counts(growth, 436.0, np.array(psi), seed=5)
    f = ramp.fit(model, n, EFFORT)
    profile = ramp._profile(model.surface(n, EFFORT))
    inside = np.flatnonzero(profile >= f.loglik - ramp.PROFILE_LEVEL)
    assert len(inside) >= 4
    for i in inside[:: len(inside) // 4]:

        def negative(log_rate):
            mass = model.stage_mass(model.t0_grid[i], {"rate": np.exp(log_rate), **extra})
            return -float(ramp._loglik(mass, ramp._log_mass(mass), n, EFFORT))

        starts = np.arange(np.log(0.003), np.log(3.0), 0.5)
        nested = -min(optimize.minimize_scalar(negative, bounds=(a, a + 0.5), method="bounded").fun for a in starts)
        assert profile[i] == pytest.approx(nested, abs=0.02)


def dense_interval(families, n, effort, around, half=6.0):
    """The profile interval from a T0 grid of 0.05 Myr and 600 rates per family: a reference for the default grids."""
    t0 = np.arange(around - half, around + half, 0.05)
    profiles = []
    for family in families:
        positive = family.default_rates[family.default_rates > 0]
        rates = np.geomspace(positive[0], positive[-1], 600)
        if family.default_rates[0] == 0:
            rates = np.concatenate([[0.0], rates])
        profiles.append(ramp._profile(ramp.RampModel(EDGES, family, t0, rates).surface(n, effort)))
    edge = EDGES[np.flatnonzero((n > 0).any(axis=0)).max()]
    profile = np.max(profiles, axis=0)
    return ramp._interval(t0, profile, profile.max(), edge)


@pytest.mark.parametrize(
    "fitted, truth, t0, params, totals",
    [
        ([ramp.ExpectedBirthDeath()], ramp.ExpectedBirthDeath(), 450.0, {"rate": 0.001}, (1000, 300)),
        ([ramp.ExpectedBirthDeath()], ramp.ExpectedBirthDeath(), 436.0, {"rate": 0.0}, (30000, 9000)),
        ([ramp.Logistic(300.0), ramp.Logistic(1000.0)], ramp.Logistic(1000.0), 436.0, {"rate": 1.0, "k": 1000.0}, (20000, 6000)),
        ([ramp.Logistic(100.0)], ramp.Logistic(100.0), 436.0, {"rate": 0.6, "k": 100.0}, (20000, 6000)),
    ],
)
def test_interval_agrees_with_a_dense_reference_and_contains_the_maximum(fitted, truth, t0, params, totals):
    n = np.round(expected_counts(ramp.RampModel(EDGES, truth), t0, params, totals))
    f = ramp.fit([ramp.RampModel(EDGES, family) for family in fitted], n, EFFORT)
    lo, hi, bounded = dense_interval(fitted, n, EFFORT, f.t0)
    assert bounded and f.bounded
    assert f.lo <= f.t0 <= f.hi
    assert f.lo == pytest.approx(lo, abs=0.15) and f.hi == pytest.approx(hi, abs=0.15)


def test_profiling_the_capacity_never_lowers_the_profile():
    n = np.round(expected_counts(LOGISTIC, 437.0, LOGISTIC_TRUTH, (120, 40)))
    fixed = ramp.fit(LOGISTIC, n, EFFORT)
    free = ramp.fit([ramp.RampModel(EDGES, ramp.Logistic(k)) for k in (30.0, 100.0, 300.0)], n, EFFORT)
    assert np.all(free.profile >= fixed.profile - 1e-12)
    assert free.loglik >= fixed.loglik - 1e-9
    assert free.hi >= fixed.hi - 1e-9 and free.lo <= fixed.lo + 1e-9


def test_polish_improves_on_the_grid_and_leaves_the_interval_sane():
    n = np.round(expected_counts(LOGISTIC, 437.2, {"rate": 0.27, "k": 100.0}, (200, 60)))
    coarse, polished = ramp.fit(LOGISTIC, n, EFFORT, polish=False), ramp.fit(LOGISTIC, n, EFFORT)
    assert polished.loglik >= coarse.loglik
    assert abs(polished.t0 - coarse.t0) <= ramp.T0_STEP
    assert polished.lo <= polished.t0 <= polished.hi


# --- inputs -------------------------------------------------------------------------------------


def test_effort_series_has_the_window_stages_and_fixed_boundaries():
    assert SERIES.stages[0] == "Emsian" and SERIES.stages[-1] == "Darriwilian" and len(SERIES.stages) == 15
    assert SERIES.edges[0] == pytest.approx(393.47) and SERIES.edges[-1] == pytest.approx(469.4)
    assert np.all(np.diff(SERIES.edges) > 0)
    assert np.array_equal(SERIES.base, TS.base[FIRST : FIRST + 15])
    assert np.all(SERIES.spores > 0) and np.all(SERIES.bodies > 0)


def test_effort_series_sums_the_table_over_units():
    rows = list(csv.DictReader(open(inputs.EFFORT_CSV)))
    for stage in ("Darriwilian", "Telychian", "Lochkovian"):
        i = SERIES.stages.index(stage)
        spores = sum(float(r["n_docs"]) for r in rows if r["channel"] == "spore" and r["stage"] == stage)
        bodies = sum(float(r["land"]) + float(r["marginal"]) for r in rows if r["channel"] == "body" and r["stage"] == stage)
        assert SERIES.spores[i] == pytest.approx(spores) and SERIES.bodies[i] == pytest.approx(bodies)
    assert SERIES.bodies[SERIES.stages.index("Lochkovian")] > 2 * SERIES.bodies[SERIES.stages.index("Pridoli")]


def test_effort_series_csv_round_trips(tmp_path):
    inputs.write_csv(SERIES, tmp_path / "effort_series.csv")
    rows = list(csv.DictReader(open(tmp_path / "effort_series.csv")))
    assert [r["stage"] for r in rows] == list(SERIES.stages)
    assert [float(r["spore_effort"]) for r in rows] == pytest.approx(SERIES.spores.tolist())
    assert [float(r["body_effort"]) for r in rows] == pytest.approx(SERIES.bodies.tolist(), abs=0.006)
    assert [float(r["base_ma"]) for r in rows] == pytest.approx(SERIES.base.tolist())


def test_a_missing_stage_in_the_effort_table_is_an_error(tmp_path):
    rows = [r for r in csv.DictReader(open(inputs.EFFORT_CSV)) if r["stage"] != "Pragian"]
    path = tmp_path / "effort.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match="Pragian"):
        inputs.effort_series(path)


# --- recovery machinery -------------------------------------------------------------------------


def test_origination_windows_span_the_named_stages():
    assert recovery.window_bounds(TS, "darriwilian-sandbian") == pytest.approx((452.8, 469.4))
    assert recovery.window_bounds(TS, "telychian-sheinwoodian") == pytest.approx((430.6, 438.6))


def test_a_replicate_is_reproducible_and_depends_on_its_index():
    ctx = recovery.context()
    a, b, c = (recovery.replicate(ctx, "telychian-sheinwoodian", "logistic_r0.3", rep) for rep in (4, 4, 5))
    assert a[0] == b[0] and a[1] == b[1]
    assert a[0] != c[0]
    assert set(a[1]) == {(e, l, cs, k) for e in recovery.EFFORTS for l in recovery.LEVELS for cs in recovery.CHANNEL_SETS for k in recovery.ESTIMATORS}


def test_preservation_levels_fix_the_expected_record_count():
    ctx = recovery.context()
    ab = sim.simulate_abundance(sim.BirthDeath(0.25, 0.15), 437.0, ctx.window_end, 9)
    mass = sim.stage_exposure(ab, TS)[ctx.first : ctx.last + 1]
    for effort in recovery.EFFORTS:
        e = ctx.effort[effort]
        psi = recovery.psi_for_targets(e, mass, recovery.LEVELS["mid"])
        assert psi * (e @ mass.T) == pytest.approx(recovery.LEVELS["mid"])


def test_verdict_applies_the_plan_criteria_strictly():
    assert recovery.verdict("classical", 0.90, 1.99, 0.0) == (True, True, True)
    assert recovery.verdict("classical", 0.899, 0.0, 0.0)[0] is False
    assert recovery.verdict("classical", 0.95, 2.0, 0.0)[0] is False
    assert recovery.verdict("ramp_bd", 0.95, 0.5, 0.11) == (True, False, False)
    assert recovery.verdict("ramp_bd", 0.95, 0.5, 0.10) == (True, True, True)
    assert recovery.verdict("ramp_logistic_kfree", 0.95, 0.5, 0.5) == (True, False, False)
    assert recovery.verdict("griwm", 0.95, -1.9, 0.0)[2] is True


def test_griwm_interval_is_calibrated_on_the_reference_errors():
    rng = np.random.default_rng(0)
    t0 = rng.uniform(430.0, 440.0, 4000)
    res = np.column_stack([t0 + rng.normal(1.0, 1.5, 4000), np.zeros(4000), np.zeros(4000), np.zeros(4000)])
    reference = rng.normal(1.0, 1.5, 4000)
    own = recovery.summarise(t0, res, "griwm", reference)
    assert 0.93 < own["coverage_calibrated"] < 0.97 and own["median_bias_ma"] == pytest.approx(1.0, abs=0.15)
    assert own["median_width_ma"] == pytest.approx(2 * 1.96 * 1.5, rel=0.1)
    shifted = recovery.summarise(t0, res, "griwm", reference + 5.0)
    assert shifted["coverage_calibrated"] < 0.5 and shifted["passes"] is False


def test_unbounded_profiles_cover_but_are_not_identified():
    t0 = np.full(100, 435.0)
    res = np.column_stack([np.full(100, 433.0), np.full(100, 432.9), np.full(100, ramp.T0_MAX), np.ones(100)])
    out = recovery.summarise(t0, res, "ramp_bd", None)
    assert out["coverage_interval"] == 1.0 and out["frac_unbounded"] == 1.0
    assert out["identified"] is False and out["usable"] is False


def test_recovery_run_returns_a_complete_small_grid():
    windows = {"telychian-sheinwoodian": recovery.WINDOWS["telychian-sheinwoodian"]}
    growth = {"constant": recovery.GROWTH["constant"], "logistic_r0.3": recovery.GROWTH["logistic_r0.3"]}
    rows = recovery.run(n_reps=8, workers=2, windows=windows, growth=growth)
    assert len(rows) == 2 * len(recovery.EFFORTS) * len(recovery.LEVELS) * len(recovery.CHANNEL_SETS) * len(recovery.ESTIMATORS)
    assert set(rows[0]) <= set(recovery.COLUMNS)
    for r in rows:
        assert r["n_reps"] == 8 and 0.0 <= r["frac_undefined"] <= 1.0
        for key in ("coverage_interval", "coverage_upper", "coverage_calibrated"):
            assert 0.0 <= r.get(key, 0.5) <= 1.0


def grid_row(estimator, growth, **values):
    row = dict.fromkeys(recovery.COLUMNS, "")
    row.update(window="w", growth=growth, effort="real", level="mid", channels="joint", estimator=estimator, passes="False", usable="False")
    row.update({k: str(v) for k, v in values.items()})
    return row


def test_report_counts_passes_and_takes_the_coverage_each_estimator_is_judged_on():
    rows = [
        grid_row("classical", "constant", coverage_upper=0.97, coverage_interval=0.2, median_bias_ma=1.0, median_width_ma=4, frac_unbounded=0, passes="True", usable="True"),
        grid_row("classical", "constant", coverage_upper=0.5, coverage_interval=0.1, median_bias_ma=-6.0, median_width_ma=2, frac_unbounded=0),
        grid_row("griwm", "constant", coverage_calibrated=0.93, median_bias_ma=0.5, median_width_ma=9, frac_unbounded=0, passes="True", usable="True"),
        grid_row("ramp_bd", "constant", coverage_interval=0.91, coverage_upper=0.95, median_bias_ma=0.2, median_width_ma=60, frac_unbounded=0.7, passes="True"),
    ]
    summary = {(r["estimator"], r["growth"]): r for r in report.summarise(rows)}
    classical = summary[("classical", "constant")]
    assert (classical["n_scenarios"], classical["n_pass"], classical["n_usable"]) == (2, 1, 1)
    assert classical["min_coverage"] == 0.5 and classical["median_coverage"] == pytest.approx(0.735)
    assert (classical["min_bias_ma"], classical["max_bias_ma"]) == (-6.0, 1.0)
    assert summary[("griwm", "constant")]["min_coverage"] == 0.93
    ramp_bd = summary[("ramp_bd", "constant")]
    assert (ramp_bd["n_pass"], ramp_bd["n_usable"], ramp_bd["mean_frac_unbounded"]) == (1, 0, 0.7)
