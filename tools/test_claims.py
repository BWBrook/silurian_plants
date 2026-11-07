import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import claims


FIELDS = claims.BINDING_FIELDS


def _fixture(tmp_path, *, selector=None, display="428.8", claim="C27", doc_claim="C27",
             evidence_value="428.84000595", extra_rows=()):
    evidence = tmp_path / "evidence.csv"
    with evidence.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "history", "older_bound_ma"])
        writer.writeheader()
        writer.writerow({"category": "B2", "history": "flat", "older_bound_ma": evidence_value})
        for row in extra_rows:
            writer.writerow(row)
    doc = tmp_path / "doc.md"
    doc.write_text(f"value [{display}]{{.{doc_claim} .V001}}\n")
    sidecar = tmp_path / "value-bindings.csv"
    with sidecar.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerow({
            "binding_id": "V001",
            "claim_id": claim,
            "evidence": "evidence.csv",
            "selector": json.dumps(selector if selector is not None else {"category": "B2", "history": "flat"}, separators=(",", ":")),
            "value_column": "older_bound_ma",
            "estimand": "test value",
            "display_values": json.dumps([display]),
        })
    return sidecar, doc


def _run(tmp_path, **kwargs):
    old_root = claims.ROOT
    claims.ROOT = tmp_path
    try:
        sidecar, doc = _fixture(tmp_path, **kwargs)
        errors = []
        claims.check_bindings(sidecar, {"C27": {}, "C40": {}}, [doc], errors)
        return errors
    finally:
        claims.ROOT = old_root


def test_correct_rounding_binds_to_the_selected_field(tmp_path):
    assert _run(tmp_path) == []


def test_swapping_flat_value_for_pbdb_value_fails(tmp_path):
    errors = _run(tmp_path, display="428.9")
    assert any("does not match source" in error for error in errors)


def test_missing_selector_fails_as_non_unique(tmp_path):
    errors = _run(tmp_path, selector={})
    assert any("at least one equality field" in error for error in errors)


def test_no_row_selector_fails(tmp_path):
    errors = _run(tmp_path, selector={"category": "B2", "history": "decline25"})
    assert any("matched 0 rows" in error for error in errors)


def test_duplicate_row_selector_fails(tmp_path):
    errors = _run(tmp_path, extra_rows=({"category": "B2", "history": "flat", "older_bound_ma": "428.84000595"},))
    assert any("matched 2 rows" in error for error in errors)


def test_wrong_claim_binding_fails(tmp_path):
    errors = _run(tmp_path, claim="C40")
    assert any("binds C40, not C27" in error for error in errors)


def test_upstream_evidence_drift_fails(tmp_path):
    errors = _run(tmp_path, evidence_value="428.95000000")
    assert any("does not match source" in error for error in errors)


def test_legacy_superseded_citation_remains_valid(tmp_path):
    doc = tmp_path / "legacy.md"
    doc.write_text("old [452.6]{.C35 .superseded}\n")
    cited = set()
    claims.check_doc(doc, {"C35": {"status": "superseded", "value": "452.6"}}, cited, [])
    assert cited == {"C35"}


def test_signed_influence_values_keep_minus_in_ledger_and_prose():
    assert claims.numbers("-1.669552")[0][1] == claims.numbers("−1.669552")[0][1] < 0
