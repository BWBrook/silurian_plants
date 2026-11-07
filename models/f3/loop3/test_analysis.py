import itertools

import numpy as np
import pandas as pd

import analysis
from endpoint import PiecewiseRecovery, known_cutoff_bound
from histories import load_histories, YOUNG


def test_conservative_envelope_dominates_all_age_range_corners():
    recovery = PiecewiseRecovery(np.array([0., 2., 5., 10., 1000.]), np.array([2., 1., .5, .1]))
    r = pd.DataFrame({"min_ma": [1., 3., 6.], "max_ma": [4., 4., 9.]})
    bound, possible, certain, oldest = analysis.envelope(r, recovery, 2.)
    assert (possible, certain, oldest) == (3, 2, 9.)
    for ages in itertools.product(*zip(r.min_ma, r.max_ma)):
        used = np.array(ages)[np.array(ages) >= 2.]
        result = known_cutoff_bound(used, recovery, 2.)
        assert result.bound_ma <= bound.bound_ma


def test_partial_window_units_cannot_increase_guaranteed_count():
    recovery = PiecewiseRecovery(np.array([0., 1000.]), np.ones(1))
    r = pd.DataFrame({"min_ma": [1., 3.], "max_ma": [8., 5.]})
    _, possible, certain, oldest = analysis.envelope(r, recovery, 2.)
    assert (possible, certain, oldest) == (2, 1, 8.)


def test_missing_country_does_not_drop_known_collection():
    h = pd.read_csv(analysis.ROOT / "data/macro/horizons_reviewed.csv")
    r = analysis.select_records(h, "B0")
    assert r.member_ids.str.contains("pbdb:27182", regex=False).any()
    assert not r.unit_id.isna().any()


def test_excluded_name_cannot_reenter_through_crown_flag():
    r = pd.read_csv(analysis.ROOT / "data/macro/accepted_occurrence_links.csv")
    assert not r.occurrence_no.isin([209041, 1573884, 1573887, 1573888]).any()
    assert r.collection_no.eq(22860).any()
    assert not (r.b2 & ~r.b1).any()
    assert not (r.b1 & ~r.b0).any()


def test_named_localities_are_not_deleted_by_country_genus_match():
    h = pd.read_csv(analysis.ROOT / "data/macro/horizons_reviewed.csv").set_index("horizon_id")
    for collection in [10679, 10706, 14043, 14045, 14131, 52698]:
        assert h.loc[f"pbdb:{collection}", "eligible_primary"]
    assert not h.loc["pbdb:53659", "eligible_primary"]


def test_proxy_density_integrates_to_collection_equivalents():
    e = pd.read_csv(analysis.ROOT / "data/macro/effort_reviewed.csv")
    e = e[e.region == "global"]
    for key, column in [("pbdb_all", "all_collection_equivalents"),
                        ("pbdb_plant_excluded", "plant_excluded_equivalents")]:
        history = load_histories()[key]
        assert np.isclose(history.exposure_cap, e[column].sum(), rtol=1e-12)


def test_simulation_counts_match_reported_primary_envelope():
    import simulation
    h = pd.read_csv(analysis.ROOT / "data/macro/horizons_reviewed.csv")
    counts = simulation.observed_counts()
    for category, n in counts.items():
        r = analysis.select_records(h, category)
        assert n == int((r.min_ma >= YOUNG).sum())


def test_canonical_b0_and_former_inventory_reproduce_expected_envelopes():
    h = pd.read_csv(analysis.ROOT / "data/macro/horizons_reviewed.csv")
    flat = load_histories()["flat"]
    canonical = analysis.select_records(h, "B0")
    former = analysis.select_records(h, "B0", exclude_members={"tail:S-w22-K12"})
    canonical_fit, _, canonical_n, canonical_oldest = analysis.envelope(canonical, flat, YOUNG)
    former_fit, _, former_n, former_oldest = analysis.envelope(former, flat, YOUNG)
    assert (canonical_n, canonical_oldest) == (76, 452.8)
    assert np.isclose(canonical_fit.bound_ma, 455.18534542)
    assert (former_n, former_oldest) == (75, 432.9)
    assert np.isclose(former_fit.bound_ma, 434.50683364)


def test_cross_channel_body_admission_and_geography_are_bound_to_sources():
    h = pd.read_csv(analysis.ROOT / "data/macro/horizons_reviewed.csv")
    oman = h[h.horizon_id.eq("tail:S-w22-K12")]
    assert set(oman.reading) == {"main", "inclusive"}
    assert oman.b0.all() and not oman.b1.any() and not oman.b2.any()
    assert set(oman.source_channel) == {"spore"}
    assert not h.horizon_id.eq("tail:S-w22-Dr4").any()
    xiemisitai = h[h.horizon_id.eq("pbdb:278439")].iloc[0]
    assert xiemisitai.region == "Kazakhstania"
    assert "West Junggar" in xiemisitai.region_basis


def test_e4_only_tail_records_do_not_enter_b1():
    h = pd.read_csv(analysis.ROOT / "data/macro/horizons_reviewed.csv")
    indexed = h.set_index(["horizon_id", "reading"])
    for horizon, reading in [
        ("tail:M-bohemica", "main"),
        ("tail:M-capel-horeb-ludlow", "main"),
        ("tail:M-capel-horeb-ludlow", "inclusive"),
        ("tail:M-lang-tracheid-axis", "main"),
        ("tail:M-lang-tracheid-axis", "inclusive"),
    ]:
        row = indexed.loc[(horizon, reading)]
        assert row.b0 and not row.b1 and not row.b2
    assert indexed.loc[("tail:M-bohemica", "inclusive"), "b2"]


def test_age_allocation_rng_is_keyed_to_the_analysis_cell():
    first = analysis.case_rng("main", "B2", "Emsian", "independent_uniform").uniform(size=8)
    repeated = analysis.case_rng("main", "B2", "Emsian", "independent_uniform").uniform(size=8)
    other = analysis.case_rng("main", "B1", "Emsian", "independent_uniform").uniform(size=8)
    assert np.array_equal(first, repeated)
    assert not np.array_equal(first, other)
