import copy
import json

import pytest

import borenshult_review as review


@pytest.fixture
def data():
    return (review.read_csv(review.DATA / "outcomes.csv"), review.read_csv(review.DATA / "readings.csv"),
            json.loads((review.DATA / "screen_spec.json").read_text()))


def test_possible_samples_never_become_older_or_reference_zeros(data):
    rows, readings, spec = data
    review.validate(rows, readings, spec)
    results, membership = review.calculate(rows)
    for m in membership:
        assert m["onset_depth_m"] == 43.1
        assert set(m["older_inventory_ids"]) == {"BOR-71.1", "BOR-67.6", "BOR-59.1", "BOR-48.2"}
        assert set(m["older_trial_ids"]) == {"BOR-71.1", "BOR-67.6", "BOR-59.1"}
        assert m["unresolved_older_ids"] == ["BOR-48.2"]
        assert m["unresolved_reference_ids"] == (["BOR-41.1", "BOR-34"]
                                                 if m["reading"] == "concordant-definite" else ["BOR-34"])
        assert not review.POSSIBLE.intersection(m["reference_trial_ids"] + m["older_trial_ids"])
        if m["reading"] == "concordant-definite":
            assert "BOR-41.1" not in m["reference_trial_ids"]
    assert {(r["reading"], r["reference_conversion"], r["k"], r["n_ref"]) for r in results} == {
        ("figure3-definite", "complete reported-category", 6, 29),
        ("figure3-definite", "explicit-only (optimistic diagnostic)", 6, 16),
        ("figure4-definite", "complete reported-category", 5, 29),
        ("figure4-definite", "explicit-only (optimistic diagnostic)", 5, 15),
        ("concordant-definite", "complete reported-category", 5, 28),
        ("concordant-definite", "explicit-only (optimistic diagnostic)", 5, 15)}
    assert all(not r["excludes_target"] for r in results)


def test_figure_conflict_is_retained_in_all_alternatives(data):
    rows, readings, spec = data
    conflict = {r["reading_id"]: r for r in rows if r["unit_id"] == "BOR-41.1"}
    assert conflict["figure3-definite"]["outcome"] == "detected"
    assert conflict["figure4-definite"]["outcome"] == "not_reported"
    assert conflict["concordant-definite"]["outcome"] == "unresolved"
    assert all(r["conflict"] == review.CONFLICT for r in conflict.values())
    damaged = copy.deepcopy(rows)
    next(r for r in damaged if r["unit_id"] == "BOR-41.1")["conflict"] = ""
    with pytest.raises(ValueError, match="figure conflict"):
        review.validate(damaged, readings, spec)


@pytest.mark.parametrize("damage", ["missing", "duplicate", "unresolved-to-zero", "conflict-to-zero"])
def test_rejects_incomplete_duplicate_or_recoded_evidence(data, damage):
    rows, readings, spec = data
    if damage == "missing":
        rows.pop()
    elif damage == "duplicate":
        rows.append(rows[0].copy())
    elif damage == "unresolved-to-zero":
        next(r for r in rows if r["unit_id"] == "BOR-48.2")["outcome"] = "not_reported"
    else:
        next(r for r in rows if r["unit_id"] == "BOR-41.1" and r["reading_id"] == "concordant-definite")["outcome"] = "not_reported"
    with pytest.raises(ValueError):
        review.validate(rows, readings, spec)


def test_receipt_binds_exact_membership_outputs_and_preserved_inputs(tmp_path):
    out = tmp_path / "review"
    review.run(out=out)
    receipt = json.loads((out / "receipt.json").read_text())
    assert receipt["membership"] == json.loads((out / "membership.json").read_text())
    assert receipt["preserved_qualification_files_unchanged"]
    assert receipt["fixed_age_test"] is False
    assert receipt["qualification"] == "not performed"
    for name, digest in receipt["output_sha256"].items():
        assert review.sha256(out / name) == digest
    with pytest.raises(ValueError, match="already exists"):
        review.run(out=out)
