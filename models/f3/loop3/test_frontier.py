import numpy as np
import pandas as pd

import analysis
import frontier
from histories import YOUNG


def test_review_frontier_closed_form_is_reproduced():
    result = frontier.contour(426.7, 48, 431.2, 0)
    assert np.isclose(result["extra_earlier_exposure_required"], 2.140005948579742)
    assert np.isclose(result["earlier_to_later_intensity"], 0.47555687746216485)
    assert np.isclose(result["contour_cdf_at_oldest"], 0.05)


def test_delay_candidate_not_older_than_envelope_anchor_is_flagged():
    result = frontier.contour(426.7, 48, 431.2, 5)
    assert result["status"] == "candidate_not_older_than_envelope_anchor"
    assert np.isnan(result["earlier_to_later_intensity"])


def test_frontier_output_has_fixed_candidates_delays_and_units():
    table = pd.read_csv(frontier.OUT / "frontier.csv")
    assert set(table.unit_treatment) == set(frontier.UNIT_TREATMENTS)
    assert set(table.candidate_lineage_ma) == set(frontier.CANDIDATES)
    assert set(table.assumed_diagnostic_delay_myr) == set(frontier.DELAYS)
    assert set(table.cutoff_ma) == {YOUNG}
    assert len(table) == 2 * len(frontier.UNIT_TREATMENTS) * len(frontier.CANDIDATES) * len(frontier.DELAYS)


def test_region_stage_change_does_not_change_primary_b2_membership():
    h = pd.read_csv(analysis.ROOT / "data/macro/horizons_reviewed.csv")
    primary = analysis.select_records(h, "B2", units="locality_age")
    region_stage = analysis.select_records(h, "B2", units="region_stage")
    assert len(primary) == 50
    assert int((primary.min_ma >= YOUNG).sum()) == 48
    assert int((region_stage.min_ma >= YOUNG).sum()) == 19
    assert len(region_stage) < len(primary)
