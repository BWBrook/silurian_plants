import pandas as pd
import pytest

import build_reviewed


def inputs():
    root = build_reviewed.ROOT
    observations = pd.read_csv(root / "data/occurrences/observations.csv")
    assignments = pd.read_csv(root / "data/occurrences/reading_assignments.csv")
    scale = pd.read_csv(root / "data/timescale.csv")
    membership = pd.read_csv(root / "data/macro/body_membership.csv", keep_default_na=False)
    return observations, assignments, scale, membership


def test_cross_channel_membership_is_explicit_nested_and_timescale_derived():
    observations, assignments, scale, membership = inputs()
    rows = build_reviewed.body_membership_rows(observations, assignments, scale, membership)
    assert set(rows.horizon_id) == {"tail:S-w22-K12"}
    assert set(rows.reading) == {"main", "inclusive"}
    assert set(rows.source_channel) == {"spore"}
    assert rows.b0.all() and not rows.b1.any() and not rows.b2.any()
    assert rows.eligible_primary.all()
    katian = scale.set_index("stage").loc["Katian", "base_ma"]
    hirnantian = scale.set_index("stage").loc["Hirnantian", "base_ma"]
    assert (rows.max_ma == katian).all()
    assert (rows.min_ma == hirnantian).all()


def test_accepted_membership_requires_both_declared_readings():
    observations, assignments, scale, membership = inputs()
    membership.loc[membership.obs_id == "S-w22-K12", "readings"] = "main"
    with pytest.raises(ValueError, match="requires main and inclusive"):
        build_reviewed.body_membership_rows(observations, assignments, scale, membership)


def test_source_channel_mismatch_is_an_admission_error():
    observations, assignments, scale, membership = inputs()
    membership.loc[membership.obs_id == "S-w22-K12", "source_channel"] = "mesofossil"
    with pytest.raises(ValueError, match="source-channel mismatch"):
        build_reviewed.body_membership_rows(observations, assignments, scale, membership)


def test_category_nesting_is_enforced_before_admission():
    observations, assignments, scale, membership = inputs()
    k12 = membership.obs_id == "S-w22-K12"
    membership.loc[k12, ["b0", "b1", "b2"]] = ["no", "yes", "yes"]
    with pytest.raises(ValueError, match="body-category nesting"):
        build_reviewed.body_membership_rows(observations, assignments, scale, membership)
