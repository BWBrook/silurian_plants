import numpy as np
import pandas as pd

from interval_feasibility import (
    OPT_TOL,
    ROOT,
    _matching_at_discrepancy,
    analysis_sets,
    witness_allocation,
)
from histories import load_histories


def test_event_enumeration_has_known_unconstrained_infimum():
    lower = np.zeros(5)
    upper = np.ones(5)
    theoretical = 1 / (2 * 4)
    assert _matching_at_discrepancy(lower, upper, theoretical + 1e-10)[0] is not None
    assert _matching_at_discrepancy(lower, upper, theoretical - 1e-6)[0] is None


def test_reproduces_reviewers_decisive_b2_witnesses():
    records = pd.read_csv(ROOT / "studies/f3/data/macro/horizons_reviewed.csv")
    sets, _, _, _ = analysis_sets(records)
    histories = load_histories()
    expected = {
        "decline25": (0.18244723543219032, 0.07660948249764679),
        "pbdb_excluded_decline10": (0.18664876704527533, 0.0658096266107708),
    }
    for history, (expected_d, expected_p) in expected.items():
        allocation, summary, _, _ = witness_allocation(sets["B2_possible"], histories[history])
        assert allocation.within_recorded_support.all()
        assert abs(summary["global_D_upper"] - summary["global_D_lower"]) <= OPT_TOL
        assert np.isclose(summary["witness_D"], expected_d, atol=2e-8, rtol=0)
        assert np.isclose(summary["witness_asymptotic_p"], expected_p, atol=2e-8, rtol=0)


def test_guaranteed_and_canonical_membership_are_explicit():
    records = pd.read_csv(ROOT / "studies/f3/data/macro/horizons_reviewed.csv")
    sets, metadata, membership, source = analysis_sets(records)
    assert len(sets["B2_possible"]) == 50
    assert len(sets["B2_guaranteed"]) == 48
    assert sorted(len(value) for key, value in sets.items() if key.startswith("B2")) == [48, 49, 49, 50]
    assert sorted(len(value) for key, value in sets.items() if key.startswith("B0")) == [76, 77, 77, 78]
    assert len(sets["B0_canonical"]) == 78
    assert sets["B0_canonical"].member_ids.str.contains("S-w22-K12", regex=False).any()
    assert source == "canonical_horizons_reviewed"
    assert len(membership) == 16
    assert all(value["n_partial_units"] == 2 for value in metadata.values())


def test_nonmaximum_edge_is_capped_at_profiled_maximum():
    lower = np.array([0.99, 0.98, 0.0])
    upper = np.ones(3)
    result, _ = _matching_at_discrepancy(lower, upper, 0.75)
    assert result is not None
    maximum, matching = result
    assert maximum >= lower.max()
    for index, slot in enumerate(matching):
        if slot != len(lower) - 1:
            assert lower[index] / maximum <= 1 + 1e-12
