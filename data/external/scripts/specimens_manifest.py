#!/usr/bin/env python3
"""Write data/external/specimens/MANIFEST.tsv for the specimen tables (stdlib only).

usage: python3 specimens_manifest.py EXTERNAL_DIR GBIF_STAMPS IDIGBIO_STAMP
  EXTERNAL_DIR   the project's data/external
  GBIF_STAMPS    comma-separated UTC stamps of the GBIF harvest directories
  IDIGBIO_STAMP  UTC stamp of the iDigBio harvest directory
Paths in the manifest are relative to EXTERNAL_DIR.  Row counts are data rows (header excluded).
"""
import csv
import hashlib
import os
import sys

ext = sys.argv[1]
gb = sys.argv[2]
ig = sys.argv[3]
EXTRACTED = "2026-10-27"
csv.field_size_limit(10 ** 9)

GBIF_SRC = "GBIF occurrence search API (api.gbif.org/v1), basisOfRecord=FOSSIL_SPECIMEN"
GBIF_VER = "live search %s; raw pages on deep-server:/data/codex/silurian_plants/raw/gbif/<stamp>/" % gb
IDIG_SRC = "iDigBio search API (search.idigbio.org/v2), basisofrecord=fossilspecimen"
IDIG_VER = "live search %s (index lastModified 2026-04-23); raw pages on deep-server:/data/codex/silurian_plants/raw/idigbio/%s/" % (ig, ig)
ALA_SRC = "EPRP gbif-ala-fossils mirror (GBIF records for AU and PG, Neptune excluded), deep-server:/data/paleodata/gbif-ala-fossils"
ALA_VER = "mirror harvest 2026-10-22T1013Z_url; EPRP commit ac42dfb"
OPEN = "per record: CC0, CC BY or CC BY-NC (NC rows flagged derived_nc_flag)"
META = {
    "specimens/gbif_specimens.csv": ("GBIF fossil specimens in the 485-383 Ma window (plus Frasnian-Famennian anchor genera), core and flagged subsets, one row per GBIF occurrence", GBIF_SRC, GBIF_VER, OPEN, "scripts/specimens_harvest.py; scripts/specimens_build.py"),
    "specimens/ala_specimens.csv": ("Window specimens from the EPRP mirror of GBIF Australia and Papua New Guinea records (the ALA route); a subset of GBIF's records", ALA_SRC, ALA_VER, OPEN, "scripts/specimens_build.py"),
    "specimens/idigbio_specimens_open_licence.csv": ("iDigBio window specimens whose own record or whose recordset states CC0, CC BY or CC BY-NC (derived_licence_effective_source says which); the full iDigBio table is in local/specimens/", IDIG_SRC, IDIG_VER, OPEN, "scripts/specimens_harvest.py; scripts/specimens_build.py"),
    "specimens/specimens_merged.csv": ("GBIF, ALA-mirror and open-licence iDigBio rows in one table; every source row kept, duplicates linked by derived_dedupe_key and derived_duplicate_of", GBIF_SRC + "; " + IDIG_SRC + "; " + ALA_SRC, GBIF_VER + "; " + IDIG_VER + "; " + ALA_VER, OPEN, "scripts/specimens_build.py"),
    "specimens/specimen_filter_names.csv": ("Filter audit: each distinct name among window candidates, by source, with count, classification (core, flagged, excluded) and reason", "derived from the tables above", "as the tables above", "derived; no source licence applies to the classification", "scripts/specimens_build.py"),
    "specimens/card_taxa_specimens_summary.csv": ("Per card taxon, anchor genus, nematophyte and charophyte name: specimens by source and institution, ages as given, names as recorded", "derived from the tables above", "as the tables above", "derived counts", "scripts/specimens_build.py"),
    "specimens/card_taxa_specimens_by_institution.csv": ("Long form of the card summary: scope name x source x institutionCode x rows", "derived from the tables above", "as the tables above", "derived counts", "scripts/specimens_build.py"),
    "specimens/gbif_datasets.csv": ("GBIF datasets of the retained records: datasetKey, title, DOI, licence, publisher and record counts, for citation", "GBIF dataset and organization API (api.gbif.org/v1)", GBIF_VER, "dataset licences as stated per dataset", "scripts/specimens_harvest.py gbif-datasets; scripts/specimens_build.py"),
    "specimens/gbif_backbone_placement.csv": ("Where each searched genus sits in the GBIF backbone (all homonyms), with fossil-specimen counts per backbone taxon", "GBIF species API, legacy backbone d7dddbf4-2cf0-4f39-9b2a-bb099caae36c", GBIF_VER, "GBIF Backbone Taxonomy CC BY 4.0", "scripts/specimens_harvest.py; scripts/specimens_build.py"),
    "specimens/idigbio_recordsets.csv": ("iDigBio recordsets behind the retained rows with the data rights each states and the share of rows with a record-level licence", "iDigBio search API view/recordsets", IDIG_VER, "metadata", "scripts/specimens_harvest.py idigbio-recordsets; scripts/specimens_build.py"),
    "specimens/dedupe_by_institution.csv": ("Physical specimens per institutionCode by the source set that holds them (GBIF, ALA mirror, iDigBio); shows where sources hold unlinked records", "derived from the tables above", "as the tables above", "derived counts", "scripts/specimens_build.py"),
    "local/specimens/idigbio_specimens.csv": ("Full iDigBio window table; rows of the NHMUK and NRM-PZ recordsets state no licence and iDigBio records their rights as 'Unknown License, assume Public Domain', so rights are unclear for the table as a whole. Git-ignored", IDIG_SRC, IDIG_VER, "unclear for rows without a record licence; see derived_licence_class", "scripts/specimens_harvest.py; scripts/specimens_build.py"),
    "local/specimens/specimens_merged_all.csv": ("Merged table including iDigBio rows with no stated licence. Git-ignored", GBIF_SRC + "; " + IDIG_SRC + "; " + ALA_SRC, GBIF_VER + "; " + IDIG_VER + "; " + ALA_VER, "unclear for rows without a record licence", "scripts/specimens_build.py"),
}


import glob
for p in sorted(glob.glob(os.path.join(ext, "specimens", "harvest_provenance", "*.tsv"))):
    rel = os.path.relpath(p, ext)
    kind = "provenance.tsv: one row per raw JSON page (URL, query, timestamp, offset, record count, bytes, sha256)" if p.endswith("_provenance.tsv") else "queries.tsv: one row per query (id, group, parameters, count reported, records fetched, new unique records, note, seconds)"
    src = GBIF_SRC if "/gbif_" in p else IDIG_SRC
    META[rel] = ("Harvest " + kind, src, "harvest dir " + os.path.basename(p).split("_")[1] + " on deep-server:/data/codex/silurian_plants/raw", "metadata", "scripts/specimens_harvest.py")
META["specimens/build_stats.json"] = ("Counts written by the build script: records retrieved, dropped by reason, subsets, window statuses, dedupe groups and rule counts", "derived from the tables above", "as the tables above", "derived counts", "scripts/specimens_build.py")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def nrows(p):
    if p.endswith(".json"):
        return ""
    with open(p, newline="", encoding="utf-8") as f:
        if p.endswith(".tsv"):
            return sum(1 for _ in f) - 1
        return sum(1 for _ in csv.reader(f)) - 1


out = os.path.join(ext, "specimens", "MANIFEST.tsv")
with open(out, "w", encoding="utf-8", newline="") as f:
    f.write("path\tdescription\tsource\tsource_version\tlicence\tscript\trows\tsha256\textracted\n")
    for rel in sorted(META):
        p = os.path.join(ext, rel)
        if not os.path.exists(p):
            print("missing", rel, file=sys.stderr)
            continue
        d, src, ver, lic, scr = META[rel]
        f.write("\t".join([rel, d, src, ver, lic, scr, str(nrows(p)), sha(p), EXTRACTED]) + "\n")
print("wrote", out)
