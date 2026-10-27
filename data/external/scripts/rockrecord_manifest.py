"""rockrecord_manifest.py: write data/external/rock-record/MANIFEST.tsv for the British rock-record tables.

Run from data/external/scripts/ (stdlib only):  python3 rockrecord_manifest.py
Paths in the manifest are relative to data/external/. Rows are records (CSV/TSV) or features (GeoPackage layer).
"""
import csv
import hashlib
import os
import sqlite3

csv.field_size_limit(1 << 30)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "rock-record", "MANIFEST.tsv")
SRC = "BGS Geology 625k DiGMapGB-625 bedrock polygons V5.17 (2008 edition), Shapefile and GeoPackage downloads"
VER = "BGS download pages dated 06/10/2025 (Shapefile) and 05/12/2024 (GeoPackage), fetched 2026-10-27T0039Z"
OGL = ("Open Government Licence (BGS licence page links v3; DOI landing page links v2); acknowledgement 'Contains British Geological Survey "
       "materials (c) UKRI [year]' (BGS page) or 'Contains NERC materials (c)NERC [year]' (NERC record); shapefile metadata: 'Copyright NERC 2008'")
LEXV = "BGS Lexicon of Named Rock Units (linked data and web pages), fetched 2026-10-27"
LEXLIC = "no licence statement found (BGS: free access, 'as seen'; UKRI copyright); reuse terms unconfirmed, attribution given"
ITEMS = [
    ("rock-record/bgs_units_silurian_devonian.csv",
     "One row per BGS LEX code: the 36 codes of the 2,634 Silurian-Devonian polygons, the 21 Old Red Sandstone Supergroup descendants in the Lexicon without such polygons, and 2 ancestors; polygon area (UK, GB, NI, by rock group), BGS polygon age terms and years, Lexicon status, rank, parent, ages (Ma), lithology classes, definition sentence, reference list; derived_ ORS flags and environment keywords",
     SRC + "; BGS Lexicon", VER + "; " + LEXV, "polygon fields: " + OGL + "; Lexicon fields: " + LEXLIC, "scripts/rockrecord_build.py"),
    ("rock-record/bgs_outcrop_area_by_age.csv",
     "Outcrop area (km2) of the Silurian-Devonian polygons by BGS period, series and stage, by region (UK, GB+IoM, NI), rock group and ORS flag: overlap, exclusive and year-apportioned areas on BGS's own polygon years",
     SRC, VER, OGL, "scripts/rockrecord_build.py"),
    ("rock-record/bgs_polygon_age_scale_observed.csv",
     "BGS age terms found in the polygon attributes with the year values they carry as MAX_TIME_Y (base) and MIN_TIME_Y (top), and their offset from the project's data/timescale.csv",
     SRC, VER, OGL, "scripts/rockrecord_build.py"),
    ("rock-record/bgs_geochronology_divisions_used.csv",
     "BGS Geochronology Division records (Ma) used by the Lexicon entries fetched, with offsets from the project's data/timescale.csv where a stage base matches",
     "BGS Geochronology dataset linked data (data.bgs.ac.uk)", "fetched 2026-10-27", LEXLIC, "scripts/rockrecord_lexicon.py; scripts/rockrecord_build.py"),
    ("rock-record/bgs_provenance_digmapgb625.tsv",
     "Provenance of the DiGMapGB-625 pull: URL, UTC timestamp, licence, bytes, sha256 of the two zips, the dataset pages, the NERC record and the DiGMapGB-50 page (not downloaded)",
     "BGS", "fetched 2026-10-27T0039Z", "n/a (file names and checksums)", "scripts/rockrecord_fetch.py"),
    ("rock-record/bgs_provenance_lexicon.tsv",
     "Provenance of the Lexicon pulls: URL, UTC timestamp, licence note, bytes, sha256 of each linked-data record, web page and Geochronology Division",
     "BGS", "fetched 2026-10-27", "n/a (file names and checksums)", "scripts/rockrecord_lexicon.py"),
    ("local/rock-record/bgs_625k_bedrock_silurian_devonian.gpkg",
     "Vector: the 2,634 DiGMapGB-625 bedrock polygons that overlap Silurian-Devonian on BGS's own years, all source attributes, EPSG:27700 (LOCAL ONLY: vector)",
     SRC, VER, OGL, "scripts/rockrecord_bgs_polygons.py"),
    ("local/rock-record/bgs_polygons_silurian_devonian.csv",
     "Attribute table of those 2,634 polygons (no geometry): all source attributes, area_m2, centroid, derived_ region, rock group, ORS evidence, area and series/period shares (LOCAL ONLY with the vector)",
     SRC, VER, OGL, "scripts/rockrecord_build.py"),
    ("local/rock-record/bgs_625k_bedrock_all_polygons_attributes.csv",
     "Attribute table of all 11,244 DiGMapGB-625 bedrock polygons (no geometry): all source attributes, area_m2 (planar EPSG:27700), centroid lon/lat (LOCAL ONLY; for totals and checks)",
     SRC, VER, OGL, "scripts/rockrecord_bgs_polygons.py"),
    ("local/rock-record/bgs_lexicon_entries_sd.csv",
     "Full Lexicon entries (60) for the codes in bgs_units_silurian_devonian.csv, including the prose fields: lithology description, boundary definitions, thickness, distribution, previous names (LOCAL ONLY: reuse terms unconfirmed)",
     "BGS Lexicon of Named Rock Units (linked data and web pages)", LEXV, LEXLIC, "scripts/rockrecord_lexicon.py"),
]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


def nrows(p):
    if p.endswith(".gpkg"):
        con = sqlite3.connect("file:" + p + "?mode=ro", uri=True)
        n = con.execute("SELECT COUNT(*) FROM bgs_625k_bedrock_silurian_devonian").fetchone()[0]
        con.close()
        return n
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.reader(f, delimiter="\t" if p.endswith(".tsv") else ",")
        next(rd)
        return sum(1 for _ in rd)


with open(OUT, "w", encoding="utf-8") as f:
    f.write("path\tdescription\tsource\tsource_version\tlicence\tscript\trows\tsha256\textracted\n")
    for path, desc, src, ver, lic, script in ITEMS:
        full = os.path.join(ROOT, path)
        f.write("\t".join([path, desc, src, ver, lic, script, str(nrows(full)), sha(full), "2026-10-27"]) + "\n")
print("wrote", OUT)
