"""Checks of the F3 sketch against known truths.

    uv run --with pytest --with numpy --with scipy pytest models/f3

Ages are Ma, decreasing towards the present. Coverage tests use fixed seeds.
"""

import numpy as np
import pytest
from scipy import stats

import estimators as est
import run_sketch
import sim

TS = sim.Timescale.load()
END = float(TS.base[TS.index("Eifelian")])  # end of the Emsian
T0 = 437.0  # Telychian


def records(growth, psi=0.02, seed=0, effort=None, t0=T0):
    run = sim.simulate(growth, t0, {"x": sim.Channel(psi, effort)}, END, TS, seed)
    return run.records["x"]


def binomial_ci_contains(successes: int, n: int, p: float, level: float = 0.9999) -> bool:
    return stats.binomtest(successes, n, p).pvalue > 1 - level


# --- simulator -------------------------------------------------------------------------------


def test_records_lie_in_window_and_in_their_stage():
    rec = records(sim.BirthDeath(0.25, 0.15), psi=0.05, seed=3)
    assert len(rec.age) > 10
    assert np.all((rec.age >= END) & (rec.age <= T0))
    assert np.all((rec.young <= rec.age) & (rec.age < rec.old))
    assert np.all(np.diff(rec.age) <= 0)  # oldest first
    assert np.array_equal(rec.old, TS.base[TS.stage_of(rec.age)])


def test_same_seed_reproduces_and_other_seeds_differ():
    a, b, c = (records(sim.BirthDeath(0.25, 0.15), 0.05, seed=s) for s in (7, 7, 8))
    assert np.array_equal(a.age, b.age)
    assert not np.array_equal(a.age, c.age)


def test_abundance_path_does_not_depend_on_psi_or_channels():
    growth = sim.BirthDeath(0.25, 0.15)
    one = sim.simulate(growth, T0, {"a": sim.Channel(0.01)}, END, TS, seed=11).abundance
    two = sim.simulate(growth, T0, {"a": sim.Channel(0.5), "b": sim.Channel(0.1)}, END, TS, seed=11).abundance
    assert np.array_equal(one.edges, two.edges) and np.array_equal(one.values, two.values)


def test_zero_effort_in_a_stage_removes_its_records():
    growth = sim.Constant(50)
    rec = records(growth, psi=0.05, seed=1, effort={"Pridoli": 0.0})
    assert not np.any(rec.stage == TS.index("Pridoli"))
    assert np.any(rec.stage == TS.index("Ludfordian")) and np.any(rec.stage == TS.index("Lochkovian"))


def test_negative_effort_is_rejected():
    with pytest.raises(ValueError):
        records(sim.Constant(50), effort={"Pridoli": -1.0})


def total_records(growth, psi, effort=None, n_reps=300):
    return sum(len(records(growth, psi, seed=s, effort=effort).age) for s in range(n_reps))


def test_count_follows_psi_times_abundance_times_effort():
    n_reps, psi, k = 300, 0.01, 50
    expected = n_reps * psi * k * (T0 - END)
    observed = total_records(sim.Constant(k), psi, n_reps=n_reps)
    assert abs(observed - expected) < 4 * np.sqrt(expected)
    doubled = total_records(sim.Constant(k), psi, effort={name: 2.0 for name in TS.names}, n_reps=n_reps)
    assert abs(doubled - 2 * expected) < 4 * np.sqrt(2 * expected)


def test_effort_acts_per_stage():
    n_reps, psi, k = 300, 0.02, 50
    half = {"Lochkovian": 0.5}
    lochkovian = TS.index("Lochkovian")
    width = TS.base[lochkovian] - TS.top[lochkovian]
    count = sum(np.sum(records(sim.Constant(k), psi, seed=s, effort=half).stage == lochkovian) for s in range(n_reps))
    expected = n_reps * psi * k * 0.5 * width
    assert abs(count - expected) < 4 * np.sqrt(expected)


def test_logistic_starts_at_one_and_rises_to_capacity():
    ab = sim.simulate_abundance(sim.Logistic(r=0.35, k=100), T0, END, seed=0)
    assert ab.edges[0] == END and ab.edges[-1] == T0
    assert ab.at(T0 - 1e-6) == pytest.approx(1.0, abs=0.01)
    assert np.all(np.diff(ab.values) <= 0)  # ages ascend, so N falls towards the origin
    assert ab.at(END + 1e-6) == pytest.approx(100.0, rel=0.01)
    assert ab.at(T0 + 1.0) == 0.0


def test_birth_death_starts_with_one_lineage_and_survives():
    ab = sim.simulate_abundance(sim.BirthDeath(0.25, 0.15), T0, END, seed=5)
    assert ab.values[-1] == 1.0 and ab.values.min() >= 1.0
    assert ab.edges[0] == END and ab.edges[-1] == T0
    assert np.all(ab.values == np.round(ab.values))


def test_birth_death_grows_at_the_net_rate():
    s_max, lam, mu = T0 - END, 0.25, 0.15
    ends = np.array([sim.simulate_abundance(sim.BirthDeath(lam, mu), T0, END, seed=s).values[0] for s in range(200)])
    # conditioned on survival N grows as W e^{(lam-mu)s}; the median log growth rate is close to lam - mu
    rate = np.log(np.median(ends)) / s_max
    assert rate == pytest.approx(lam - mu, abs=0.03)


# --- estimators on tiny cases ----------------------------------------------------------------


def test_marshall_hand_cases():
    # C = 0.5, H = 2: alpha = 1/(0.5) - 1 = 1; C = 15/16, H = 5: alpha = 16^(1/4) - 1 = 1
    assert est.marshall_1990(np.array([10.0, 6.0]), conf=0.5).hi == pytest.approx(14.0)
    assert est.marshall_1990(np.array([10.0, 9.0, 8.0, 7.0, 6.0]), conf=0.9375).hi == pytest.approx(14.0)
    # C = 0.75, H = 3: alpha = 0.25^(-1/2) - 1 = 1
    iv = est.marshall_1990(np.array([10.0, 8.0, 6.0]), conf=0.75)
    assert (iv.lo, iv.point, iv.hi) == pytest.approx((10.0, 10.0, 14.0))


def test_strauss_sadler_hand_cases():
    ages = np.array([10.0, 8.0, 6.0])
    iv = est.strauss_sadler_1989(ages, conf=0.75)
    assert iv.hi == pytest.approx(14.0)
    assert iv.point == pytest.approx(10.0 + 4.0 * (np.sqrt(2.0) - 1.0))  # alpha at C = 0.5, H = 3
    assert iv.lo == 10.0
    assert est.strauss_sadler_1989(ages).hi == est.marshall_1990(ages).hi


def test_classical_bounds_extend_towards_older_ages():
    ages = np.array([405.0, 401.0, 400.0, 396.0, 395.0])
    for estimator in (est.marshall_1990, est.strauss_sadler_1989):
        iv = estimator(ages)
        assert iv.lo == 405.0  # the first appearance is the oldest record
        assert iv.hi > 405.0 and iv.point >= 405.0
        assert np.isfinite(iv.hi)
        shuffled = estimator(ages[[3, 0, 4, 2, 1]])
        assert tuple(shuffled) == tuple(iv)
        older = estimator(np.append(ages, 420.0))
        assert older.lo == 420.0 and older.hi > 420.0
        younger = estimator(np.append(ages, 390.0))
        assert younger.lo == 405.0 and younger.hi > iv.hi  # a younger record lengthens the range only


@pytest.mark.parametrize("n", [2, 3, 5, 10, 40])
def test_classical_upper_bound_exists_for_few_records(n):
    ages = np.linspace(420.0, 400.0, n)
    assert np.isfinite(est.marshall_1990(ages).hi)
    assert est.marshall_1990(ages).hi > 420.0


def test_too_few_records_give_nan():
    for estimator in (est.marshall_1990, est.strauss_sadler_1989, est.weighted_mcinerny):
        assert np.isnan(estimator(np.array([400.0])).point)
    assert est.oldest(np.array([400.0])).point == 400.0
    assert np.isnan(est.oldest(np.array([])).point)


def test_weighted_mcinerny_hand_case():
    # series of 2: span 1, (1+1)*1/2 = 1 beyond 10, weight 1; series of 3: span 4, 5/3 beyond, weight 1/4
    value = est.weighted_mcinerny(np.array([10.0, 9.0, 6.0]), alpha=np.exp(-1.0), unit=1.0).point
    assert value == pytest.approx((1.0 * 11.0 + 0.25 * (10.0 + 5.0 / 3.0)) / 1.25)


@pytest.mark.parametrize(
    "ages, alpha, reference",
    [
        ([100, 90, 60], np.exp(-1.0), 107.133333333),
        ([945, 908, 898, 770, 687, 661, 629, 573, 384, 372, 266, 206, 202, 177, 62], 0.05, 1035.69435349),
        ([945, 908, 898, 770, 687, 661, 629, 573, 384, 372, 266, 206, 202, 177, 62], 0.5, 965.984697455),
        ([10, 10, 8], np.exp(-1.0), 11.0),
    ],
)
def test_weighted_mcinerny_matches_the_authors_code_on_a_mirrored_axis(ages, alpha, reference):
    # Reference: the inner loop of griwm.R in cjabradshaw/CRIWM (8eb6f51), run in R with signor_lipps = "ext"
    # on negated ages and negated back; integer ages and unit = 1 year as in that code.
    value = est.weighted_mcinerny(np.array(ages, dtype=float), alpha=alpha, unit=1.0).point
    assert value == pytest.approx(reference, rel=1e-10)


def test_weighted_mcinerny_lies_older_than_the_oldest_record_and_ignores_order():
    rng = np.random.default_rng(0)
    ages = rng.uniform(400.0, 430.0, size=20)
    value = est.weighted_mcinerny(ages).point
    assert value > ages.max()
    assert est.weighted_mcinerny(rng.permutation(ages)).point == pytest.approx(value)


def test_griwm_with_exact_dates_is_the_point_estimate_and_resamples_otherwise():
    ages = np.array([430.0, 428.0, 425.0, 420.0, 415.0, 411.0])
    exact = est.griwm(ages, 0.0, np.random.default_rng(1), n_resample=50)
    assert exact.lo == exact.point == exact.hi == pytest.approx(est.weighted_mcinerny(ages).point)
    noisy = est.griwm(ages, 1.0, np.random.default_rng(1), n_resample=2000)
    assert noisy.lo < noisy.point < noisy.hi
    again = est.griwm(ages, 1.0, np.random.default_rng(1), n_resample=2000)
    assert tuple(noisy) == tuple(again)


# --- stage resampling ------------------------------------------------------------------------


def test_stage_resampling_draws_each_record_within_its_stage():
    young, old = np.array([410.62, 413.02, 419.62]), np.array([413.02, 419.62, 422.7])
    seen = []

    def spy(ages):
        seen.append(ages.copy())
        return est.oldest(ages)

    est.stage_resampled(spy, young, old, np.random.default_rng(0), n_draws=1000)
    draws = seen[0]
    assert draws.shape == (1000, 3)
    assert np.all(draws >= young) and np.all(draws < old)
    assert np.all(draws.mean(axis=0) == pytest.approx((young + old) / 2, abs=0.2))


def test_stage_resampling_pools_draws():
    young, old = np.array([410.62, 413.02, 419.62]), np.array([413.02, 419.62, 422.7])
    iv = est.stage_resampled(est.marshall_1990, young, old, np.random.default_rng(2), n_draws=2000)
    assert 419.62 <= iv.lo <= iv.point <= iv.hi
    assert iv.hi > old[-1] - 0.5
    again = est.stage_resampled(est.marshall_1990, young, old, np.random.default_rng(2), n_draws=2000)
    assert tuple(iv) == tuple(again)


def test_stage_resampling_of_one_record_is_undefined():
    assert np.isnan(est.stage_resampled(est.marshall_1990, np.array([410.0]), np.array([413.0]), np.random.default_rng(0)).hi)


# --- known truths ----------------------------------------------------------------------------


def constant_world_outcomes(n_reps=2000, psi=0.02):
    hi, point = [], []
    for i in range(n_reps):
        rec = records(sim.Constant(50), psi, seed=sim.child_seed(20261028, i))
        marshall, strauss = est.marshall_1990(rec.age), est.strauss_sadler_1989(rec.age)
        assert marshall.hi == strauss.hi
        hi.append(marshall.hi >= T0)
        point.append(strauss.point >= T0)
    return np.array(hi), np.array(point)


def test_classical_interval_covers_at_its_nominal_rate_under_its_own_assumptions():
    # constant N, constant effort: horizons are uniform over the true range, Marshall's assumption
    covered, point_above = constant_world_outcomes()
    assert binomial_ci_contains(int(covered.sum()), len(covered), 0.95)
    assert abs(covered.mean() - 0.95) < 0.02
    # the Strauss-Sadler point estimate is the median: the truth is older than it half the time
    assert binomial_ci_contains(int(point_above.sum()), len(point_above), 0.5)


def test_ramp_degradation_is_reported_not_asserted():
    """Coverage and bias of every estimator under the two ramps. Printed with pytest -s; only
    checked to be finite so that the numbers are recorded, not made to pass."""
    rows = run_sketch.run_grid(
        n_reps=150,
        psis=(0.02,),
        growths={"logistic": run_sketch.GROWTH["logistic"], "birthdeath": run_sketch.GROWTH["birthdeath"]},
    )
    print()
    for r in rows:
        if r["channel"] == "spores" and r["dating"] == "exact":
            print(
                f"{r['growth']:>10} {r['estimator']:<20} n={r['median_records']:>5.0f} "
                f"coverage_upper={r['coverage_upper']:.2f} median_bias={r['median_bias_ma']:+.1f} Myr"
            )
    assert all(0.0 <= r["coverage_upper"] <= 1.0 and np.isfinite(r["median_bias_ma"]) for r in rows if "coverage_upper" in r)
