# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Write climate/MANIFEST.tsv: one row per file or folder this task produced, with row counts and sha256.

Header: path description source source_version licence script rows sha256 extracted
Paths are relative to data/external/. Folder rows carry a file count and no sha256 (the per-file hashes are
in climate/hadcm3l_slices.csv and in the folder's SHA256SUMS).

Usage: uv run climate_manifest.py
"""
import csv
import hashlib
from pathlib import Path

EXT = Path(__file__).resolve().parent.parent
EXTRACTED = "2026-10-27"
ZENODO = "PhanDA HadCM3L priors, Zenodo 8237751 (Judd et al. 2024; simulations of Valdes et al. 2021), suite scotese_02"
ZVER = "Zenodo version 1 (2023-08-11); scotese_02_tas.zip md5 5dc5fb031d6840b22c29a52158991f73, scotese_02_pr.zip md5 8c15488f422669aeba0a1a09e8a4b783"
CCBY = "CC BY 4.0"
DERIVED = "CC BY 4.0 (derived from CC BY 4.0 data; cite Judd et al. 2024 and Valdes et al. 2021)"
BRIDGE = "none stated by the BRIDGE site; not redistributed"
NA = ""

ROWS = [
    ("climate/README.md", "Source, citation, experiment choice, slices, age basis, method, caveats, what was not done", "this task", "2026-10-27", NA, "hand-written", None),
    ("climate/hadcm3l_slices.csv", "One row per file: slice, mean block, variable, ages and their basis, units, grid, temporal resolution, size, sha256 (210 rows)", ZENODO, ZVER, CCBY, "scripts/climate_hadcm3l_tables.py", "csv"),
    ("climate/hadcm3l_land_summary.csv", "Land-area-weighted mean annual tas and pr per slice, land area, GMST and ice-free variants; derived_ columns", ZENODO + "; land mask and heavy-snow flag from BRIDGE annual climatologies", ZVER, "Derived numbers: CC BY 4.0 (cite Judd et al. 2024 and Valdes et al. 2021); the BRIDGE mask and snow fields have no stated licence", "scripts/climate_hadcm3l_tables.py", "csv"),
    ("climate/hadcm3l_qc.csv", "Per-slice checks: tas and pr duplicate variables, mask complementarity, agreement of M1-M5 with the BRIDGE climatology", ZENODO + "; BRIDGE annual climatologies", ZVER, DERIVED, "scripts/climate_hadcm3l_tables.py", "csv"),
    ("climate/hadcm3l_experiment_info.csv", "ExperimentInfo.xlsx in long form: 8 suites x 109 slices with experiment age, plate age, PUMA run id and CO2", "ExperimentInfo.xlsx in Zenodo 8237751", "Zenodo version 1; xlsx md5 0c61461d58ce3614a604d8dbe3636ad8", CCBY, "scripts/climate_hadcm3l_info.py", "csv"),
    ("local/climate/hadcm3l_phanda_stage_slice_map.csv", "PhanDA stage to the two HadCM3L slices of its prior ensemble, decoded from ExpNo.mat (GTS2020 stage labels)", "PhanDA repository 3_GlobalFiles/PriorInfo/ExpNo.mat (EJJudd/PhanDA)", "git 9f06c0d976 (2026-03-09)", "none stated in the source repository", "scripts/climate_hadcm3l_info.py", "csv"),
    ("climate/other_sources.csv", "Survey of other land-climate sources for 485-383 Ma: coverage, variables, resolution, licence, size, URL, access route", "Zenodo, figshare, Crossref and DataCite APIs, BRIDGE and GFZ pages, EPRP registers", "queried 2026-10-27", CCBY, "hand-written", "csv"),
    ("climate/doi_check.tsv", "Every DOI cited in README.md and other_sources.csv, checked against Crossref or DataCite", "Crossref and DataCite APIs", "queried 2026-10-27", "n/a", "scripts/climate_doi_check.py", "tsv"),
    ("climate/hadcm3l_raw_provenance.tsv", "Provenance of the raw files on deep-server: URL, UTC time, bytes, md5, sha256 (copy of PROVENANCE.tsv)", "deep-server:/data/codex/silurian_plants/raw/hadcm3l/PROVENANCE.tsv", "2026-10-27", NA, "scripts/climate_fetch_hadcm3l.sh; scripts/climate_fetch_bristol_pdclann.sh", "tsv"),
    ("local/climate/hadcm3l/ExperimentInfo.xlsx", "ExperimentInfo.xlsx, byte-identical", "Zenodo 8237751", "Zenodo version 1; md5 0c61461d58ce3614a604d8dbe3636ad8", CCBY, "scripts/climate_fetch_hadcm3l.sh", None),
    ("local/climate/hadcm3l/PROVENANCE.tsv", "Download provenance for the Zenodo files: URL, timestamp, md5 and sha256", "Zenodo 8237751", "Zenodo version 1", CCBY, "scripts/climate_fetch_hadcm3l.sh", None),
    ("local/climate/hadcm3l/scotese_02/", "Slices 12-32 (485.4-385.2 Ma), tas and pr, M1-M5, byte-identical to the zip members, with SHA256SUMS (git-ignored)", ZENODO, ZVER, CCBY, "scripts/climate_extract_hadcm3l.sh", "dir:*.nc"),
    ("local/climate/hadcm3l/bristol_pdclann/", "BRIDGE annual-mean climatology files <run>a.pdclann.nc for the 21 window runs, used for the land-sea mask and checks (git-ignored)", "paleo.bristol.ac.uk BRIDGE pages (Valdes et al. 2021)", "fetched 2026-10-27", BRIDGE, "scripts/climate_fetch_bristol_pdclann.sh", "dir:*.nc"),
]
for s in sorted((EXT / "scripts").glob("climate_*")):
    ROWS.append((f"scripts/{s.name}", "Reproducing script for the climate folder", "this task", "2026-10-27", NA, "-", None))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def n_records(path, kind):
    with open(path, newline="") as fh:
        rows = list(csv.reader(fh, delimiter="," if kind == "csv" else "\t"))
    return len(rows) - 1


def main():
    out = EXT / "climate/MANIFEST.tsv"
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["path", "description", "source", "source_version", "licence", "script", "rows", "sha256", "extracted"])
        for path, desc, src, ver, lic, script, kind in ROWS:
            p = EXT / path
            if kind and kind.startswith("dir:"):
                n = len(list(p.glob(kind[4:])))
                w.writerow([path, desc, src, ver, lic, script, f"{n} files", "", EXTRACTED])
            else:
                rows = n_records(p, kind) if kind in ("csv", "tsv") else ""
                w.writerow([path, desc, src, ver, lic, script, rows, sha(p), EXTRACTED])
    print("wrote", out)


if __name__ == "__main__":
    main()
