"""record_extras_manifest.py (tranche 2): append the tranche-2 files to data/eprp/record/MANIFEST.tsv.

Run from data/eprp/scripts/ (stdlib only):  python3 record_extras_manifest.py
Computes rows and sha256 of each delivered file and appends one line per file that is not yet listed; existing lines are not touched.
"""
import csv
import hashlib
import os

csv.field_size_limit(1 << 30)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")                    # data/eprp/
MAN = os.path.join(ROOT, "record", "MANIFEST.tsv")
PBDB_SRC = "PBDB global snapshot (EPRP source `pbdb`); tranche-1 occurrence and reference tables"
PBDB_VER = "2026-10-23T0329Z_url"
PBDB_LIC = "CC0 (PBDB API datainfo data_license)"
ASUD_LIC = ("CC BY 4.0 (WFS AccessConstraints '(c) Commonwealth of Australia (Geoscience Australia) 2020 ... Creative Commons Attribution 4.0 "
            "International Licence'; GA eCat a05f7892-8ca9-7506-e044-00144fdd4fa6: CC-BY 4.0, (c) Commonwealth of Australia (Geoscience Australia) "
            "and Geological Society of Australia (Australian Stratigraphy Commission) 2026)")
PB = "scripts/record_extras_pbdb.py"
ITEMS = [
    ("local/record/pbdb_plant_taxa.csv",
     "PBDB taxa.csv rows (any age) in the Embryophyta tree, Plantae-unplaced and Streptophyta-not-Embryophyta groups of the tranche-1 filter, plus the six anchor genera (72 original columns, second copies suffixed .1, + 6 derived d_*)",
     PBDB_SRC, PBDB_VER, PBDB_LIC, PB),
    ("local/record/pbdb_plant_opinions.csv",
     "All PBDB opinions (opinions.csv) whose orig_no is a taxon in pbdb_plant_taxa.csv (29 original columns + d_taxon_subset)",
     PBDB_SRC, PBDB_VER, PBDB_LIC, PB),
    ("record/pbdb_plant_taxa_window.csv",
     "Window subset: taxa with d_range_overlaps_window = yes; rows and columns unchanged from the whole-tree table",
     PBDB_SRC, PBDB_VER, PBDB_LIC, "scripts/record_extras_window_subsets.py"),
    ("record/pbdb_plant_opinions_window.csv",
     "Window subset: opinions whose orig_no is a window taxon; rows and columns unchanged from the whole-tree table",
     PBDB_SRC, PBDB_VER, PBDB_LIC, "scripts/record_extras_window_subsets.py"),
    ("record/pbdb_plant_specimens.csv",
     "PBDB specimens (specimens.csv) linked to a tranche-1 or anchor occurrence, or whose taxon is in the plant subsets at any age (46 original columns + 5 derived d_*); none links to a tranche-1 or anchor occurrence",
     PBDB_SRC, PBDB_VER, PBDB_LIC, PB),
    ("record/pbdb_plant_measurements.csv",
     "PBDB measurements (measurements__c000-c162) with the same selection as pbdb_plant_specimens.csv (127 original columns, second cc suffixed .1, + 5 derived d_*); none links to a tranche-1 or anchor occurrence",
     PBDB_SRC, PBDB_VER, PBDB_LIC, PB),
    ("record/pbdb_extras_references.csv",
     "PBDB references cited by the tranche-2 taxa, opinions, specimens, measurements and anchor occurrences (34 original columns + 7 derived d_*; d_in_tranche1_references flags the 14 also in pbdb_plant_references.csv)",
     PBDB_SRC, PBDB_VER, PBDB_LIC, PB),
    ("record/pbdb_anchor_occurrences_frasnian_famennian.csv",
     "PBDB occurrences of Archaeopteris, Callixylon, Eospermatopteris, Wattieza, Elkinsia and Leclercqia outside the 485-383 Ma window that pass the tranche-1 plant filter and overlap the Frasnian-Famennian (95 original columns + 11 derived d_*)",
     PBDB_SRC, PBDB_VER, PBDB_LIC, PB),
    ("record/pbdb_extras_inputs_sha256.tsv",
     "sha256 of every mirror file read by record_extras_pbdb.py (183 files) and of the two tranche-1 tables it reads, checked against the snapshot MANIFEST.json and the tranche-1 manifest",
     "EPRP mirror manifests on deep-server", "see file", "n/a (file names and checksums)", PB),
    ("record/asud_silurian_devonian_units.csv",
     "Australian Silurian-Devonian stratigraphic units from the ASUD WFS layer StratigraphicUnit (34 original columns + 19 derived_*): numeric-age overlap with 443.1-358.86 Ma or a Silurian/Devonian term in the text age; Victorian flag, parent chain, environment keywords from the description, and links to tranche-1 PBDB plant collections by formation name",
     "Geoscience Australia, Australian Stratigraphic Units Database WFS (EPRP source `asud`); tranche-1 PBDB collection and occurrence tables",
     "2026-10-22T0604Z_wfs", ASUD_LIC, "scripts/record_extras_asud.py"),
    ("record/asud_provenance.tsv",
     "Provenance of the ASUD run: eCat record and WFS capabilities fetched 2026-10-27 (URL, timestamp, licence, sha256) and the mirror file used",
     "Geoscience Australia eCat; ASUD WFS GetCapabilities", "fetched 2026-10-27", "CC BY 4.0 (see asud_silurian_devonian_units.csv row)", "scripts/record_extras_asud.py"),
]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


def nrows(p):
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.reader(f, delimiter="\t" if p.endswith(".tsv") else ",")
        next(rd)
        return sum(1 for _ in rd)


listed = {l.split("\t")[0] for l in open(MAN, encoding="utf-8").read().splitlines()[1:]}
txt = open(MAN, encoding="utf-8").read()
if not txt.endswith("\n"):
    txt += "\n"
add = 0
for path, desc, src, ver, lic, script in ITEMS:
    if path in listed:
        continue
    full = os.path.join(ROOT, path)
    txt += "\t".join([path, desc, src, ver, lic, script, str(nrows(full)), sha(full), "2026-10-27"]) + "\n"
    add += 1
open(MAN, "w", encoding="utf-8").write(txt)
print("appended", add)
