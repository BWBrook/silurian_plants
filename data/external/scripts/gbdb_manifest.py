"""Write gbdb/MANIFEST.tsv from the files on disk (rows and sha256 recomputed).

Usage: python3 scripts/gbdb_manifest.py   (run from data/external/)
Lists every delivered file in gbdb/ and the gbdb_* scripts. rows = parsed records minus header for .csv/.tsv.
"""
import csv
import hashlib
from pathlib import Path

SRC = "GBDB snapshot, Xu 2020, Zenodo doi 10.5281/zenodo.4245604"
VER = "5-Nov-2020 (zip sha256 9bbd8aa0...4021ca38; sections workbook = 31Dec2019 state)"
LIC = "CC BY 4.0"
PBDB = "; PBDB window plant extract (data/eprp/record, CC0)"
EXTRACTED = "2026-10-27"
F = [
    ("gbdb_plant_fossils.csv", "Window plant records (core plus flagged subsets, 485-383 Ma on GBDB's own ages) and anchor Frasnian-Famennian rows; sections-table taxon rows, 43 original columns + derived_ + j_fossils_", "gbdb_extract.py", SRC),
    ("gbdb_plant_sections.csv", "All units of the sections holding those records: 55 section, formation, age and unit columns + derived_", "gbdb_extract.py", SRC),
    ("gbdb_plant_filter_names.csv", "Audit of the plant filter: each distinct genus name as recorded by GBDB group, with decision, basis, counts, reason; includes excluded names from plant-adjacent groups", "gbdb_extract.py", SRC + PBDB),
    ("gbdb_window_sections_all.csv", "Every section with any window-age unit: location, units, ages, references and taxon-row counts by major group (sampling effort)", "gbdb_extract.py", SRC),
    ("gbdb_card_anchor_summary.csv", "Card taxa (34) and anchor genera (6): records by age status, sections, China and South China counts", "gbdb_extract.py", SRC),
    ("gbdb_card_anchor_names.csv", "Card and anchor matches by name as recorded, group, numeric age, region and formation", "gbdb_extract.py", SRC),
    ("gbdb_plant_no_age_candidates.csv", "Plant records with no GBDB age that may belong to the window (card, anchor or nematophyte genus, or reference title naming Ordovician, Silurian or Devonian); triage list, not window membership", "gbdb_extract.py", SRC),
    ("gbdb_plant_fossils_table_only.csv", "Plant-classified fossils-workbook rows with no counterpart in the sections workbook (no age available)", "gbdb_extract.py", SRC),
    ("gbdb_age_basis.csv", "Numeric age pairs GBDB attaches to each age label, with the project's ICS v2024/12 stage ages and differences", "gbdb_extract.py", SRC + "; data/timescale.csv"),
    ("gbdb_label_field_patterns.tsv", "Which age label columns co-occur on rows with a numeric age", "gbdb_extract.py", SRC),
    ("gbdb_fields.csv", "Field dictionary of both workbooks: role, non-blank and distinct counts, examples", "gbdb_extract.py", SRC),
    ("gbdb_xlsx_inventory.tsv", "Sheets, non-empty rows and widths of the two workbooks", "gbdb_xlsx2csv.py", SRC),
    ("gbdb_extract_stats.json", "Counts printed by the extraction", "gbdb_extract.py", SRC),
    ("gbdb_pbdb_overlap_references.csv", "GBDB references of window and no-age plant records matched to PBDB plant references (author, year, title overlap)", "gbdb_pbdb_overlap.py", SRC + PBDB),
    ("gbdb_pbdb_overlap_sections.csv", "GBDB plant sections against PBDB plant collections: distance, formation-name overlap, shared genera, overlap class", "gbdb_pbdb_overlap.py", SRC + PBDB),
    ("gbdb_pbdb_overlap_records.csv", "GBDB core window records with PBDB counterpart level (A same reference and genus ... D genus within 100 km)", "gbdb_pbdb_overlap.py", SRC + PBDB),
    ("gbdb_pbdb_overlap_pbdb_collections_china.csv", "PBDB plant collections in China against GBDB window sections", "gbdb_pbdb_overlap.py", SRC + PBDB),
    ("gbdb_pbdb_overlap_pbdb_occurrences_china_core.csv", "PBDB core plant occurrences in China with GBDB counterpart level", "gbdb_pbdb_overlap.py", SRC + PBDB),
    ("gbdb_pbdb_overlap_summary.json", "Overlap counts", "gbdb_pbdb_overlap.py", SRC + PBDB),
    ("provenance.tsv", "Source URL, licence, download time, checksums of the zip, workbooks and CSV conversions", "", "Zenodo API record 4245604"),
]
S = ["gbdb_fetch.py", "gbdb_xlsx2csv.py", "gbdb_extract.py", "gbdb_verify.py", "gbdb_pbdb_overlap.py", "gbdb_manifest.py"]
FIELDS = ["path", "description", "source", "source_version", "licence", "script", "rows", "sha256", "extracted"]


def entry(path, desc, script, src, ver, lic):
    p = Path(path)
    rows = ""
    if p.suffix in {".csv", ".tsv"}:
        with p.open(newline="", encoding="utf-8") as fh:
            rows = str(sum(1 for _ in csv.reader(fh, delimiter="\t" if p.suffix == ".tsv" else ",")) - 1)
    return {"path": path, "description": desc, "source": src, "source_version": ver, "licence": lic,
            "script": f"scripts/{script}" if script else "", "rows": rows, "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "extracted": EXTRACTED}


rows = [entry(f"gbdb/{n}", d, s, src, VER, LIC) for n, d, s, src in F]
rows += [entry(f"scripts/{n}", "Reproducing script (standard library only)", "", "project", "", "project") for n in S]
for r in rows:
    if r["path"].startswith("scripts/"):
        r["script"] = ""
with open("gbdb/MANIFEST.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "entries -> gbdb/MANIFEST.tsv")
