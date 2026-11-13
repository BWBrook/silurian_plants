#!/usr/bin/env python3
"""Build and verify the Loop 2 Murzuq observation-basis audit.

This audit adds observation-protocol metadata to the existing 164-row appendix
inventory. It does not digitise palynofacies percentages, recode E1 outcomes, or
modify any source table. The generated rows deliberately retain unknown count
fields: the thesis uses different preparations for aggregate palynofacies and
taxon-specific biostratigraphic searching.

Usage from the repository root::

    python studies/f3/tools/loop2_observations.py build
    python studies/f3/tools/loop2_observations.py check
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "studies" / "f3" / "data" / "units" / "loop2" / "observation"
APPENDIX = ROOT / "studies" / "f3" / "data" / "units" / "libya_appendix1.csv"
CHART = ROOT / "studies" / "f3" / "data" / "units" / "libya_chart_reports.csv"
PROSE = ROOT / "studies" / "f3" / "data" / "units" / "libya_prose_support.csv"
GATE = ROOT / "studies" / "f3" / "docs" / "audits" / "2026-11-01-loop2-count-gate.md"
THESIS = ROOT / "library" / "closed" / "abuhmida2013-thesis-related_macbook20261030.pdf"
SCRIPT = Path(__file__).resolve()

THESIS_SHA256 = "c0e3bf798fb3c27db0bf9cbb155396be5b4b8e003ee2228defb615a65abf3211"
EXPECTED_APPENDIX_ROWS = 164
EXPECTED_CHART_ROWS = 158
EXPECTED_EXACT_MATCHES = 153
EXPECTED_UNMATCHED_APPENDIX = 11
EXPECTED_UNMATCHED_CHART = 5

PANEL_LOCATORS = {
    "A28i-NC186": "Abuhmida 2013 enclosure 4 palynofacies panel, PDF p.631 (printed p.615); locator only",
    "B2-NC186": "Abuhmida 2013 enclosure 4 palynofacies panel, PDF p.633 (printed p.617); locator only",
    "D1-200": "Abuhmida 2013 enclosure 4 palynofacies panel, PDF p.635 (printed p.619); locator only",
    "E1-NC174": "Abuhmida 2013 enclosure 4 palynofacies panel, PDF p.637 (printed p.621); locator only",
    "H2-NC186": "Abuhmida 2013 enclosure 4 palynofacies panel, PDF p.639 (printed p.623); locator only",
    "I3-NC186": "Abuhmida 2013 enclosure 4 palynofacies panel, PDF p.641 (printed p.625); locator only",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def key(well: str, depth: str) -> tuple[str, Decimal]:
    try:
        value = Decimal(depth.strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError(f"invalid depth {depth!r} for {well!r}") from exc
    if not value.is_finite():
        raise ValueError(f"non-finite depth {depth!r} for {well!r}")
    return well.strip(), value.normalize()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"no rows in {path}")
    return rows


def keyed(rows: Iterable[dict[str, str]], label: str) -> dict[tuple[str, Decimal], dict[str, str]]:
    out: dict[tuple[str, Decimal], dict[str, str]] = {}
    for row in rows:
        k = key(row["well"], row["depth_ft"])
        if k in out:
            raise ValueError(f"duplicate {label} key {k}")
        out[k] = row
    return out


def literal_status(value: str) -> str:
    """Keep source values as strings; blank remains blank rather than becoming a boolean."""
    return value


def expected_rows() -> tuple[list[dict[str, str]], list[dict[str, str]], dict[str, int]]:
    appendix_rows = read_rows(APPENDIX)
    chart_rows = read_rows(CHART)
    prose_rows = read_rows(PROSE)
    appendix = keyed(appendix_rows, "appendix")
    chart = keyed(chart_rows, "chart")
    prose = keyed(prose_rows, "prose")

    if len(appendix_rows) != EXPECTED_APPENDIX_ROWS:
        raise ValueError(f"expected {EXPECTED_APPENDIX_ROWS} appendix rows, found {len(appendix_rows)}")
    if len(chart_rows) != EXPECTED_CHART_ROWS:
        raise ValueError(f"expected {EXPECTED_CHART_ROWS} chart rows, found {len(chart_rows)}")
    if len(prose_rows) != EXPECTED_APPENDIX_ROWS:
        raise ValueError(f"expected {EXPECTED_APPENDIX_ROWS} prose rows, found {len(prose_rows)}")

    matches = sorted(set(appendix) & set(chart))
    if len(matches) != EXPECTED_EXACT_MATCHES:
        raise ValueError(f"expected {EXPECTED_EXACT_MATCHES} exact chart matches, found {len(matches)}")

    rows: list[dict[str, str]] = []
    for a in appendix_rows:
        k = key(a["well"], a["depth_ft"])
        c = chart.get(k)
        p = prose.get(k)
        if p is None:
            raise ValueError(f"appendix row has no prose row: {k}")
        matched = c is not None
        row: dict[str, str] = {
            "unit_id": f"{a['well']}:{a['depth_ft']}",
            "well": a["well"],
            "depth_ft": a["depth_ft"],
            "appendix_type": a["type"],
            "appendix_formation": a["formation"],
            "appendix_core_number": a["core_number"],
            "appendix_type_cell": a["type_cell"],
            "appendix_note": a["note"],
            "appendix_source_id": a["source_id"],
            "appendix_source_locator": a["source_locator"],
            "chart_join_status": "exact_decimal_depth_match" if matched else "no_exact_chart_row",
            "chart_type_code": c["type_code"] if c else "",
            "chart_e1_report_literal": c["ambitisporites_dilutus_report"] if c else "",
            "chart_target_symbols_literal": c["target_symbols"] if c else "",
            "chart_marine_symbols_literal": c["marine_symbols"] if c else "",
            "chart_other_green_symbols_literal": c["other_green_symbols"] if c else "",
            "chart_total_symbols_literal": c["total_symbols"] if c else "",
            "chart_panels_agree_literal": c["panels_agree"] if c else "",
            "chart_source_locator": c["source_locator"] if c else "",
            "chart_exact_appendix_match_literal": c["exact_appendix_match"] if c else "",
            "prose_exact_chart_label_literal": p["exact_chart_label_present"],
            "prose_e1_status_literal": literal_status(p["e1_prose_status"]),
            "prose_productivity_status_literal": literal_status(p["productivity_prose_status"]),
            "prose_barren_scope_literal": literal_status(p["barren_report_scope"]),
            "prose_e1_assemblage_context_literal": literal_status(p["e1_assemblage_context"]),
            "prose_adopted_binary_e1_literal": literal_status(p["adopted_binary_e1"]),
            "prose_chart_comparison_literal": literal_status(p["chart_comparison"]),
            "panel_locator": PANEL_LOCATORS.get(a["well"], "no mapped enclosure-4 panel locator"),
            "palynofacies_link_status": "locator_only_not_row_audited",
            "palynofacies_preparation": "kerogen; separate palynofacies preparation",
            "palynofacies_denominator": "200",
            "palynofacies_denominator_unit": "organic_particles",
            "cryptospore_percent_status": "not_established_in_this_audit",
            "cryptospore_percent": "",
            "cryptospore_category_scope": "aggregate palynofacies cryptospore group; includes stated incertae sedis",
            "e1_count_status": "unavailable",
            "e1_observation_basis": "oxidised-residue first-slide count plus additional-slide rare-form scan",
            "e1_search_denominator": "unknown",
            "additional_slide_search": "yes_in_protocol_unknown_per_unit",
            "e1_count_literal": "",
            "cryptospore_count_literal": "",
            "paired_total_literal": "",
            "observation_basis_compatibility": "incompatible_for_trilete_share_likelihood",
            "mismatch_reason": (
                "exact appendix/chart row absent; no per-sample count pairing"
                if not matched
                else "chart occurrence symbols and aggregate palynofacies fraction use different effort/protocols"
            ),
        }
        rows.append(row)

    unmatched_chart = [chart[k] for k in sorted(set(chart) - set(appendix))]
    unmatched = [
        {
            "well": r["well"],
            "depth_ft": r["depth_ft"],
            "type_code": r["type_code"],
            "source_locator": r["source_locator"],
            "exact_appendix_match_literal": r["exact_appendix_match"],
            "status": "chart_row_without_appendix_key",
        }
        for r in unmatched_chart
    ]
    counts = {
        "appendix_rows": len(appendix_rows),
        "chart_rows": len(chart_rows),
        "prose_rows": len(prose_rows),
        "exact_appendix_chart_matches": len(matches),
        "unmatched_appendix_rows": len(appendix) - len(matches),
        "unmatched_chart_rows": len(unmatched),
        "rows_written": len(rows),
    }
    if counts["unmatched_appendix_rows"] != EXPECTED_UNMATCHED_APPENDIX:
        raise ValueError(counts)
    if counts["unmatched_chart_rows"] != EXPECTED_UNMATCHED_CHART:
        raise ValueError(counts)
    return rows, unmatched, counts


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    fields = list(rows[0])
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build() -> None:
    rows, unmatched, counts = expected_rows()
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUT / "observation_basis.csv", rows)
    write_csv(OUT / "unmatched_chart_rows.csv", unmatched)
    summary = {
        "schema": "loop2-murzuq-observation-basis-v1",
        "status": "observation_audit_only_no_outcome_recode",
        "counts": counts,
        "source_hashes": {str(p.relative_to(ROOT)): sha256(p) for p in (APPENDIX, CHART, PROSE, GATE, THESIS)},
        "thesis_sha256_expected_from_count_gate": THESIS_SHA256,
        "script_sha256": sha256(SCRIPT),
        "panel_locators": PANEL_LOCATORS,
        "count_semantics": {
            "palynofacies_denominator": "nominal 200 organic particles; actual per-row count not recovered",
            "e1_search": "all palynomorphs on first biostratigraphic slide plus additional-slide rare-form scan",
            "share_model": "not admitted from this audit; paired counts/search effort unavailable",
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    readme = """# Loop 2 Murzuq observation-basis audit

`observation_basis.csv` has one row per literal row in `studies/f3/data/units/libya_appendix1.csv` (164 rows).
The audit joins `libya_chart_reports.csv` and `libya_prose_support.csv` by exact well plus Decimal
depth. It preserves source strings and current source E1 statuses; it does not derive or recode an
outcome. Five chart rows have no appendix key and are retained in `unmatched_chart_rows.csv`.

The thesis's nominal 200-organic-particle palynofacies denominator is recorded as protocol metadata.
No per-row count, cryptospore percentage or trilete count is copied: the palynofacies preparation
and aggregate cryptospore group are distinct from the oxidised-residue biostratigraphic slide and
additional rare-form scan used for E1. Thus no paired count-share likelihood is admitted here.
Panel page references are locators only and were not used to digitise values.

Run `python studies/f3/tools/loop2_observations.py build` to regenerate outputs, or `python studies/f3/tools/loop2_observations.py check`
to verify the deterministic reconstruction, counts, source hashes and generated output hashes without
writing files.
"""
    (OUT / "README.md").write_text(readme)
    receipt = {
        "schema": "loop2-murzuq-observation-receipt-v1",
        "status": "observation_audit_only_no_outcome_recode",
        "source_hashes": summary["source_hashes"],
        "script_sha256": summary["script_sha256"],
        "outputs": {
            name: sha256(OUT / name)
            for name in ("observation_basis.csv", "unmatched_chart_rows.csv", "summary.json", "README.md")
        },
        "counts": counts,
    }
    (OUT / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps(counts, sort_keys=True))


def check() -> None:
    rows, unmatched, counts = expected_rows()
    needed = [OUT / n for n in ("observation_basis.csv", "unmatched_chart_rows.csv", "summary.json", "README.md", "receipt.json")]
    missing = [str(p) for p in needed if not p.exists()]
    if missing:
        raise SystemExit(f"missing generated outputs; run build first: {missing}")
    with (OUT / "observation_basis.csv").open(newline="") as f:
        got_rows = list(csv.DictReader(f))
    with (OUT / "unmatched_chart_rows.csv").open(newline="") as f:
        got_unmatched = list(csv.DictReader(f))
    # Compare canonical serialized rows, including field order as represented by DictReader.
    if got_rows != rows:
        raise SystemExit("observation_basis.csv differs from deterministic reconstruction")
    if got_unmatched != unmatched:
        raise SystemExit("unmatched_chart_rows.csv differs from deterministic reconstruction")
    receipt = json.loads((OUT / "receipt.json").read_text())
    if receipt["counts"] != counts:
        raise SystemExit("receipt counts differ")
    for rel, expected in receipt["source_hashes"].items():
        if sha256(ROOT / rel) != expected:
            raise SystemExit(f"source hash mismatch: {rel}")
    if sha256(SCRIPT) != receipt["script_sha256"]:
        raise SystemExit("script hash mismatch; rebuild outputs")
    for name, expected in receipt["outputs"].items():
        if sha256(OUT / name) != expected:
            raise SystemExit(f"generated output hash mismatch: {name}")
    if receipt["source_hashes"][str(THESIS.relative_to(ROOT))] != THESIS_SHA256:
        raise SystemExit("held thesis hash differs from count-gate receipt")
    print(json.dumps({"status": "pass", **counts}, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "check"))
    args = parser.parse_args(argv)
    try:
        (build if args.command == "build" else check)()
    except (OSError, ValueError, KeyError, csv.Error) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
