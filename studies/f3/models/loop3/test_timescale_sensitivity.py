import numpy as np
import pandas as pd

from timescale_sensitivity import (
    BASE_YOUNG,
    BOUNDARY_TOL,
    boundary_scenarios,
    boundary_table,
    effort_for_scenario,
    histories_for_scenario,
    map_candidate_431_2,
    map_support,
    source_rule_candidate,
    ROOT,
)
from histories import load_histories


def test_shared_boundary_scenarios_are_ordered_and_within_quoted_uncertainty():
    scale = boundary_table()
    scenarios = boundary_scenarios(scale)
    for name, scenario in scenarios.items():
        assert np.all(np.diff(scenario.scenario_base_ma) > 0)
        assert (scenario.shift_ma.abs() <= scale.base_unc_ma + 1e-12).all()
        if name == "all_younger":
            assert np.allclose(scenario.shift_ma, -scale.base_unc_ma)
        if name == "all_older":
            assert np.allclose(scenario.shift_ma, scale.base_unc_ma)
    assert scenarios["alternating_a"].basis_amplitude.iloc[0] < 1
    assert scenarios["alternating_b"].basis_amplitude.iloc[0] < 1


def test_pbdb_support_moves_only_when_both_endpoints_map_exactly():
    scale = boundary_table()
    older = boundary_scenarios(scale)["all_older"]
    minimum, maximum, basis = map_support(419.62, 422.7, "pbdb", scale, older)
    assert basis == "shared_pbdb_exact_boundary_support"
    assert minimum > 419.62 and maximum > 422.7
    minimum, maximum, basis = map_support(393.47, 399.5, "pbdb", scale, older)
    assert (minimum, maximum) == (393.47, 399.5)
    assert basis == "fixed_pbdb_numerical_support_not_exactly_mapped"
    minimum, maximum, basis = map_support(445.2, 452.8, "tail", scale, older)
    assert basis == "shared_curated_stage_boundaries"
    assert minimum > 445.2 and maximum > 452.8


def test_baseline_effort_is_exact_reconstruction_and_candidate_mapping_is_identity():
    scale = boundary_table()
    baseline = boundary_scenarios(scale)["baseline"]
    raw = pd.read_csv(ROOT / "data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv", low_memory=False)
    plant_ids = set(pd.read_csv(ROOT / "data/eprp/record/pbdb_plant_collections.csv", usecols=["collection_no"]).collection_no)
    reconstructed = effort_for_scenario(raw, plant_ids, scale, baseline)
    stored = pd.read_csv(ROOT / "data/macro/effort_reviewed.csv")
    stored = stored[stored.region.eq("global")].sort_values("young_ma").reset_index(drop=True)
    for column in ["all_collection_equivalents", "plant_excluded_equivalents", "all_density_per_myr",
                   "plant_excluded_density_per_myr"]:
        assert np.allclose(reconstructed[column], stored[column], rtol=0, atol=2e-10)
    reconstructed_histories = histories_for_scenario(reconstructed, baseline)
    stored_histories = load_histories()
    ages = np.linspace(393.47, 469.4, 101)
    for name in stored_histories:
        assert np.allclose(reconstructed_histories[name].exposure(ages), stored_histories[name].exposure(ages),
                           rtol=0, atol=2e-10)
    candidate, young, old, fraction = map_candidate_431_2(scale, baseline)
    assert np.isclose(candidate, 431.2, atol=BOUNDARY_TOL)
    assert (young, old) == ("Homerian", "Sheinwoodian")
    assert 0 < fraction < 1
    assert np.isclose(baseline.scenario_base_ma.iloc[0], BASE_YOUNG)
    rule_candidate, shifted_base, offset = source_rule_candidate(scale, baseline)
    assert np.isclose(shifted_base, 430.6)
    assert np.isclose(offset, 1.3)
    assert np.isclose(rule_candidate, 431.9)
