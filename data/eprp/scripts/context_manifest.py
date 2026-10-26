#!/usr/bin/env python3
"""Build context/MANIFEST.tsv and context/sources_used.tsv for the delivered context files.

Run locally (stdlib only) after the three remote scripts have been run and their output rsynced into
data/eprp/context/ and data/eprp/local/context/ :
    python3 data/eprp/scripts/context_manifest.py
Reads EPRP's register-deposits snapshots.tsv from the read-only checkout for deposit licences and versions.
"""
import csv, hashlib, os, re, sys
from collections import defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # data/eprp
SNAP = os.path.expanduser("~/git/eprp/resources/sources/register-deposits/snapshots.tsv")
EXTRACTED = "2026-10-26"
HEADER = ["path", "description", "source", "source_version", "licence", "script", "rows", "sha256", "extracted"]

snap = {}
with open(SNAP, encoding="utf-8", newline="") as f:
    for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
        snap[r["deposit"]] = r

CL, PG, DP = "scripts/context_climate.py", "scripts/context_palaeogeography.py", "scripts/context_deposits.py"
CCBY = "CC BY 4.0"
NOLIC = "none stated in the source repository; held privately under Barry's 23 October 2026 mirroring decision; not for redistribution"

# (path regex, description, source, version, licence, script)
REG = [
    (r"^context/README\.md$", "What each file is, filters, versions, hashes, timescale bases, counts, gaps and caveats", "this extraction", "", "project documentation", "hand-written"),
    (r"^context/song2021_O5_window\.csv$", "Song et al. 2021 Database S1, sheet O5 (clumped-isotope temperatures, Hirnantian and late Katian), all 21 rows; header kept verbatim; derived_* columns added", "Song et al. 2021, Nat. Commun., Database S1.xlsx", "Zenodo 10.5281/zenodo.5027293", CCBY, CL),
    (r"^context/song2021_S1-S3_window\.csv$", "Song et al. 2021 Database S1, sheet S1-S3 (Silurian conodont apatite d18O and SST estimates), rows with Age (Ma) in 383-485; header kept verbatim; derived_* columns added", "Song et al. 2021, Nat. Commun., Database S1.xlsx", "Zenodo 10.5281/zenodo.5027293", CCBY, CL),
    (r"^context/song2021_D1-D3_window\.csv$", "Song et al. 2021 Database S1, sheet D1-D3 (Devonian and Silurian conodont apatite d18O and SST estimates), rows with Age (Ma) in 383-485; header kept verbatim; derived_* columns added", "Song et al. 2021, Nat. Commun., Database S1.xlsx", "Zenodo 10.5281/zenodo.5027293", CCBY, CL),
    (r"^context/scotese2021_gmst_derived_window\.csv$", "Global, tropical and polar mean surface temperature DERIVED here (cos-latitude weighted) from the Scotese et al. 2021 1-degree maps for slices labelled 385-480 Ma; not published values", "Scotese et al. 2021, gmst_scotese02a_v21321_csv-list.zip", "Zenodo 8238875 (scotese02a_v21321, C1)", CCBY, CL),
    (r"^context/rothman2017_events_window\.csv$", "Rothman 2017 Table 1 carbon-isotope events with Date in 383-485 Ma (End-Ordovician, Mulde, Lau); NC", "Rothman 2017, Sci. Adv. 3: e1700906, via EPRP derived/2026-10-23/rothman2017_events.tsv (cross-checked against the PMC5606709 XML Table 1)", "2026-10-23T0915Z_url; EPRP derived 2026-10-23", "CC BY-NC 4.0 (NC: non-commercial use only)", CL),
    (r"^context/timescale_basis\.csv$", "Per delivered series: the timescale basis, the evidence for it, and Devonian notes", "this extraction; sources as named per row", "", "project documentation", CL),
    (r"^context/timescale_stage_bounds\.csv$", "Stage bases on ICS v2024/12 (project timescale.csv), GTS2012 (Green et al. 2022 Table S1) and the GTS2020 chart values quoted in docs/primer.md s1.2", "data/timescale.csv; Green et al. 2022 boundaries; docs/primer.md", "", "factual boundary ages; mixed sources", CL),
    (r"^context/plate_models\.csv$", "The 26 GPlates Plate Model Manager models plus Wright et al. 2013: reference, time coverage, 485-383 Ma coverage, licence, deep-server path, EPRP notes, script-derived pole statistics for the window", "EPRP palaeogeography entry: GPlates index models.json, gplates-models-licences.tsv, palaeogeography_profile.tsv; mirror zips", "index snapshot 2026-10-24T0301Z_url", "metadata; per-model licences listed in the file", PG),
    (r"^context/paleodem_slices\.csv$", "The 21 PALEOMAP PaleoDEM slices at plate-model ages 385-485 Ma: map id, stratigraphic description, ICS v2024/12 stage checks, file names and sha256 of the copies in local/context/paleodem/", "Scotese & Wright 2018 PaleoDEM report Table 1 and zips", "Zenodo 10.5281/zenodo.5460860", CCBY, PG),
    (r"^context/register_deposits_relevant\.csv$", "31 register deposits judged relevant to the framings (relevance and framing columns are inference), with citation, DOI, licence, size, path, contents and where copies sit", "EPRP register-deposits entry (snapshots.tsv, README) and the mirror", "EPRP checkout ac42dfb", "metadata; deposit licences listed per row", DP),
    (r"^context/register_deposits_screened\.csv$", "All 93 register deposits with the screening verdict and reason (inference)", "EPRP register-deposits entry (snapshots.tsv, README) and the mirror", "EPRP checkout ac42dfb", "metadata; deposit licences listed per row", DP),
    (r"^context/sources_used\.tsv$", "Every mirror file read, with deep-server path, computed sha256 and the sha256 in the mirror's MANIFEST.json", "EPRP mirror on deep-server", "", "metadata", "scripts/context_manifest.py (merges the three scripts' lists)"),
    (r"^local/context/phanda_gmst_co2_window\.csv$", "PhanDA GMST and CO2 percentiles (5, 16, 50, 84, 95) for the 18 stage slices overlapping 485-383 Ma; original 16 columns", "PhanDA repository, 5_Outputs/PhanDA_GMSTandCO2_percentiles.csv (Judd et al. 2024)", "git 9f06c0d976 (2026-03-09)", NOLIC, CL),
    (r"^local/context/phanda_ltg_window\.csv$", "PhanDA latitudinal surface-air-temperature gradient percentiles for the same 18 slices (73 latitudes each); original columns plus slice and slice ages joined", "PhanDA repository, 5_Outputs/PhanDA_LTG_percentiles/PhanDA_SATgradient_percentiles_bystage", "git 9f06c0d976 (2026-03-09)", NOLIC, CL),
    (r"^local/context/phansst_window\.csv$", "PhanSST proxy points with Age (GTS2020) in 383-485 Ma: all 55 original columns; two derived_* columns added", "PhanSST_v001.csv (Judd et al. 2022)", "git 32cc98ed53 (2023-03-09)", NOLIC, CL),
    (r"^local/context/green2022_boundaries_window\.csv$", "Green et al. 2022 stage-boundary table rows with age (+/- 1 sigma) overlapping 485-383 Ma; original columns plus derived_* ICS crosswalk", "Green et al. 2022 repository data/boundaries.tsv", "git e3038b5c02 (2023-03-21)", "repository: none stated; article CC BY-NC-ND 4.0 (no derivatives); held privately", CL),
    (r"^local/context/green2022_lips_window\.csv$", "Green et al. 2022 LIP table rows overlapping 485-383 Ma (Suordakh only)", "Green et al. 2022 repository data/LIPs Including Oceanic.tsv", "git e3038b5c02 (2023-03-21)", "repository: none stated; article CC BY-NC-ND 4.0 (no derivatives); held privately", CL),
    (r"^local/context/green2022_impacts_window\.csv$", "Green et al. 2022 impact table rows with age (+/- 1 sigma) overlapping 485-383 Ma (4 craters)", "Green et al. 2022 repository data/impacts.tsv", "git e3038b5c02 (2023-03-21)", "repository: none stated; article CC BY-NC-ND 4.0 (no derivatives); held privately", CL),
    (r"^local/context/timescale_stage_bounds_phanda_phansst\.csv$", "PhanDA slice bounds and the observed age range of PhanSST points under each stage label, Tremadocian-Givetian", "PhanDA and PhanSST repositories", "PhanDA 9f06c0d976; PhanSST 32cc98ed53", NOLIC, CL),
    (r"^local/context/paleodem/csv_1deg/?$", "PALEOMAP PaleoDEM 1-degree lon-lat-elevation CSV, 21 slices at plate-model ages 385-485 Ma (raster as table)", "Scotese & Wright 2018, PaleoDEMS_long_lat_elev_csv_v2.zip", "Zenodo 10.5281/zenodo.5460860", CCBY, PG),
    (r"^local/context/paleodem/nc_1deg/?$", "PALEOMAP PaleoDEM 1-degree netCDF, 21 slices at plate-model ages 385-485 Ma", "Scotese & Wright 2018, Maps_1-88_1degX1deg_PaleoDEMS_nc.zip", "Zenodo 10.5281/zenodo.5460860", CCBY, PG),
    (r"^local/context/paleodem/nc_6min/?$", "PALEOMAP PaleoDEM 6-arcminute netCDF, 21 slices at plate-model ages 385-485 Ma", "Scotese & Wright 2018, Maps_1-88_6minX6min_PaleoDEMS_nc.zip", "Zenodo 10.5281/zenodo.5460860", CCBY, PG),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def nrows(path):
    if not path.endswith((".csv", ".tsv")):
        return ""
    delim = "\t" if path.endswith(".tsv") else ","
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        return str(sum(1 for _ in csv.reader(f, delimiter=delim, quoting=csv.QUOTE_NONE if delim == "\t" else csv.QUOTE_MINIMAL)) - 1)


def folder_sha(files):
    h = hashlib.sha256()
    for rel, p in sorted(files):
        h.update(f"{sha256(p)}  {rel}\n".encode())
    return h.hexdigest()


def meta(path):
    for pat, *rest in REG:
        if re.match(pat, path):
            return rest
    return None


rows = []
# 0. merge sources_used_*.tsv
parts = {"climate": "context_climate.py", "palaeogeography": "context_palaeogeography.py", "deposits": "context_deposits.py"}
merged = []
for part in parts:
    p = f"{ROOT}/context/sources_used_{part}.tsv"
    with open(p, encoding="utf-8", newline="") as f:
        r = csv.reader(f, delimiter="\t")
        h = next(r)
        for x in r:
            merged.append([part] + x)
# column layouts differ per part; normalise to one header
with open(f"{ROOT}/context/sources_used.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["part", "source", "version", "file", "deep_server_path", "bytes", "sha256_computed", "sha256_in_mirror_manifest", "check"])
    for m in merged:
        part, rest = m[0], m[1:]
        if part == "climate":      # route, version, file, path, bytes, sha, msha, check
            w.writerow([part] + rest)
        elif part == "palaeogeography":  # mirror_dir, file, path, bytes, sha, msha, check
            w.writerow([part, rest[0], "", rest[1], rest[2], rest[3], rest[4], rest[5], rest[6]])
        else:                       # deposit, version_dir, file, path, bytes, sha, msha, check
            w.writerow([part] + rest)

# 1. context/ files
for dp, dn, fn in os.walk(f"{ROOT}/context"):
    for n in sorted(fn):
        p = os.path.join(dp, n)
        rel = os.path.relpath(p, ROOT)
        if rel == "context/MANIFEST.tsv" or n == ".DS_Store" or n.startswith("sources_used_"):
            continue
        if rel.startswith("context/deposits/"):
            dep = rel.split("/")[2]
            r = snap[dep]
            lic = r["licence"]
            desc = f"Copy of {n} from the {dep} deposit"
            src = f"{dep} ({r['doi_or_record']})"
            rows.append([rel, desc, src, r["version_dir"], lic, DP, nrows(p), sha256(p), EXTRACTED])
            continue
        m = meta(rel)
        if m is None:
            sys.exit(f"no manifest metadata for {rel}")
        rows.append([rel, m[0], m[1], m[2], m[3], m[4], nrows(p), sha256(p), EXTRACTED])

# 2. local/context files: raster folders and many-file groups as one row
loc_root = f"{ROOT}/local/context"
for dp, dn, fn in sorted(os.walk(loc_root)):
    fn = [n for n in fn if n != ".DS_Store" and n != ".gitignore"]
    if not fn:
        continue
    rel_dir = os.path.relpath(dp, ROOT)
    if rel_dir.startswith("local/context/paleodem/"):
        files = [(n, os.path.join(dp, n)) for n in fn]
        m = meta(rel_dir)
        rows.append([rel_dir + "/", f"{m[0]} ({len(files)} files)", m[1], m[2], m[3], m[4], "", folder_sha(files), EXTRACTED])
        continue
    if rel_dir.startswith("local/context/deposits/"):
        dep = rel_dir.split("/")[3]
        r = snap[dep]
        byext = defaultdict(list)
        for n in fn:
            byext[os.path.splitext(n)[1]].append(n)
        for ext, names in byext.items():
            if len(names) >= 10:
                files = [(n, os.path.join(dp, n)) for n in names]
                rows.append([rel_dir + "/", f"{len(files)} {ext} files copied from the {dep} deposit (window slices, 383-485 Ma); gridded data", f"{dep} ({r['doi_or_record']})",
                             r["version_dir"], r["licence"] + " (redistributable; kept under local/ because rasters)", DP, "", folder_sha(files), EXTRACTED])
            else:
                for n in names:
                    p = os.path.join(dp, n)
                    note = "" if re.search(r"cc0|cc-by-4|cc by 4|apache|mit", r["licence"], re.I) else " (licence unclear: kept under local/)"
                    rows.append([os.path.relpath(p, ROOT), f"Copy of {n} from the {dep} deposit", f"{dep} ({r['doi_or_record']})",
                                 r["version_dir"], r["licence"] + note, DP, nrows(p), sha256(p), EXTRACTED])
        continue
    for n in sorted(fn):
        p = os.path.join(dp, n)
        rel = os.path.relpath(p, ROOT)
        m = meta(rel)
        if m is None:
            sys.exit(f"no manifest metadata for {rel}")
        rows.append([rel, m[0], m[1], m[2], m[3], m[4], nrows(p), sha256(p), EXTRACTED])

rows.sort(key=lambda r: (r[0].startswith("local/"), r[0]))
with open(f"{ROOT}/context/MANIFEST.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(HEADER)
    w.writerows(rows)
for part in parts:
    os.remove(f"{ROOT}/context/sources_used_{part}.tsv")
print("MANIFEST.tsv:", len(rows), "rows;", sum(1 for r in rows if r[0].startswith("local/")), "under local/;",
      "sources_used.tsv:", len(merged), "rows")
