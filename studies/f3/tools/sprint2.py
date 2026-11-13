#!/usr/bin/env python3
"""Reproduce sprint-2 source extraction and conditional sampling arithmetic."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "studies/f3/data/units/sprint2"


def write_csv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def qusaiba():
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "page.html"
        subprocess.run([
            "pdftotext", "-f", "6", "-l", "6", "-bbox",
            str(ROOT / "library/closed/wellman2015_firststudy.pdf"), str(path),
        ], check=True)
        words = [(float(w.attrib["xMin"]), float(w.attrib["yMin"]), w.text)
                 for w in ET.parse(path).iter() if w.tag.endswith("word")]
    columns = sorted((x, text) for x, y, text in words if 95 < y < 96)
    assert len(columns) == 37
    taxon_rows = {}
    for x, y, text in words:
        if x < 130 and 195 < y < 368 and text != "X":
            taxon_rows.setdefault(round(y, 1), []).append((x, text))
    taxa = {y: " ".join(t for _, t in sorted(parts))
            for y, parts in taxon_rows.items()}
    assert len(taxa) == 21
    records = list(csv.DictReader((ROOT / "studies/f3/data/units/qusaiba_inventory.csv").open()))
    records = sorted((r for r in records if r["wellman_table2_member"] == "yes"),
                     key=lambda r: int(r["wellman_table2_order_top_to_base"]))
    assert len(records) == 37
    depths = sorted((x, text) for x, y, text in words
                    if 135 < y < 150 and re.fullmatch(r"\??\d+(?:\.\d+)?m", text))
    assert len(depths) == 37
    assert [int(r["wellman_table2_order_top_to_base"]) for r in records] == list(range(1, 38))
    assert all(abs(core[0] - depth[0]) < 0.01 for core, depth in zip(columns, depths))
    assert [(core[1], depth[1]) for core, depth in zip(columns, depths)] == [
        (r["wellman_core"], r["wellman_literal_depth_label"]) for r in records
    ]
    marks = [[] for _ in columns]
    for x, y, text in words:
        if text != "X" or not 194 < y < 368:
            continue
        column = min(range(37), key=lambda i: abs(x - columns[i][0]))
        assert abs(x - columns[column][0]) < 4
        taxon_y = min(taxa, key=lambda ty: abs(ty - y))
        assert abs(taxon_y - y) < 1.2
        marks[column].append(taxa[taxon_y])
    rows = []
    for i, (record, reported) in enumerate(zip(records, marks)):
        assert reported
        rows.append(dict(
            record_id=record["record_id"],
            table_column=i + 1,
            literal_depth_label=record["wellman_literal_depth_label"],
            reported_core=columns[i][1],
            cryptospore_dyad_tetrad_report="present",
            reported_taxa=";".join(reported),
            productivity="marine palynomorphs in all37; methods p112 and results p122",
            source_id="wellman2015",
            source_locator="Table2 printed116/PDF6; dyad/tetrad rows only",
            analytical_status="reference-candidate-only; no older interval in this source",
        ))
    write_csv(OUT / "qusaiba_e2_reports.csv", rows)
    print(f"Qusaiba: {len(rows)} columns with reported cryptospore dyads/tetrads")


def scenarios():
    rows = []
    for reference_probability in (0.1, 0.5, 0.9):
        for transport in (1.0, 0.5, 0.1):
            for intensity in (1.0, 0.1, 0.01):
                rate = -math.log1p(-reference_probability) * transport * intensity
                n = math.ceil(-math.log(0.05) / rate)
                assert math.exp(-n * rate) <= 0.05
                assert n == 1 or math.exp(-(n - 1) * rate) > 0.05
                rows.append(dict(
                    assumed_reference_detection=reference_probability,
                    assumed_transport_ratio=transport,
                    assumed_relative_intensity=intensity,
                    older_detection=-math.expm1(-rate),
                    independent_empty_blocks_for_probability_at_most_0_05=n,
                    probability_all_empty=math.exp(-n * rate),
                    status="hypothetical-known-rate-scenario; not empirical qualification",
                ))
    write_csv(OUT / "conditional_sampling.csv", rows)
    print(f"Sampling scenarios: {len(rows)} exact homogeneous Poisson calculations")


def evidence_check():
    source_rows = list(csv.DictReader((OUT / "source_files.csv").open()))
    for row in source_rows:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"], row["path"]
    admission = list(csv.DictReader((OUT / "m1_admission.csv").open()))
    groups = {r["source_group"] for r in admission}
    assert len(groups) == 7 and len(admission) == 21
    assert {(r["source_group"], r["reading_id"]) for r in admission} == {
        (g, r) for g in groups for r in ("main", "inclusive", "outlier")
    }
    source_ids = {r["source_id"] for r in source_rows}
    for row in admission:
        assert set(row["source_ids"].split(";")) <= source_ids
        assert row["decision"] == "not-admitted-as-M1-older-reference-design"
        assert (ROOT / row["audit"]).is_file()
        assert (OUT / row["evidence_table"]).is_file()
    for name, count in [("samphire1961_inventory.csv", 6), ("qusaiba_e2_reports.csv", 37),
                        ("conditional_sampling.csv", 27)]:
        assert len(list(csv.DictReader((OUT / name).open()))) == count, name
    print(f"Verified {len(source_rows)} source hashes and all {len(admission)} admission entries")


def receipt():
    evidence_check()
    paths = list(OUT.rglob("*")) + list((ROOT / "studies/f3/docs/audits").glob("2026-10-31-sprint2-*.md"))
    paths += [Path(__file__), ROOT / "studies/f3/docs/sprint2-source-roster.md",
              ROOT / "studies/f3/docs/sprint2-results-and-value-of-information.md",
              ROOT / "studies/f3/docs/sprints-2026-11.md", ROOT / "data/timescale.csv",
              ROOT / "data/external/spores/MANIFEST.tsv"]
    for name in ("units", "outcomes", "frames", "frame_samples", "sources", "source_files", "candidates"):
        paths.append(ROOT / f"studies/f3/data/units/{name}.csv")
    for name in ("m2_units", "m2_screen", "m2_results"):
        paths.append(ROOT / f"studies/f3/models/out/{name}.csv")
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted(set(paths)) if p.is_file() and p != OUT / "receipt.json"
              and "__pycache__" not in p.parts}
    record = dict(
        source_roster_commit="d17d033cc2bb7f083a61e31228d30919f2406beb",
        sprint1_handoff_commit="63ca45e",
        scope="Source-admission evidence and conditional planning, not binding M1/M3 qualification",
        sources=list(csv.DictReader((OUT / "source_files.csv").open())),
        files=hashes,
    )
    (OUT / "receipt.json").write_text(json.dumps(record, indent=2) + "\n")
    print(f"Receipt binds {len(hashes)} evidence, input and code files")


def check():
    evidence_check()
    record = json.loads((OUT / "receipt.json").read_text())
    for path, expected in record["files"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected, path
    print(f"Receipt: all {len(record['files'])} file hashes match")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["qusaiba", "scenarios", "all", "receipt", "check"])
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.command in ("qusaiba", "all"):
        qusaiba()
    if args.command in ("scenarios", "all"):
        scenarios()
    if args.command == "receipt":
        receipt()
    if args.command == "check":
        check()
