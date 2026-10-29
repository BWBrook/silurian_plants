"""record_inputs.py: sha256 of every EPRP mirror file the record_* scripts read, checked against the mirror's own
manifest where one exists.

Run on nectar:  ssh nectar python3 - < record_inputs.py
Writes inputs_sha256.tsv to OUT. Files marked 'upstream, not read' are the source workbooks of EPRP's derived FR2
tables, listed for provenance only.
"""
import glob
import hashlib
import json
import os
import sys

OUT = "/data/codex/silurian_plants/eprp/record/out/"
PBDB = "/data/codex/artifacts/eprp-paleodata-backup/latest/pbdb/global/raw/2026-10-23T0329Z_url/"
MAC = "/data/codex/artifacts/eprp-paleodata-backup/latest/macrostrat/raw/2026-10-25T0011Z_url/"
TSM = "/data/codex/artifacts/eprp-paleodata-backup/latest/timescale/macrostrat/raw/2026-10-23T0844Z_url/"
FR2D = glob.glob("/data/codex/artifacts/eprp-paleodata-backup/latest/classic-compendia/fr2/derived/*/")[0]
FR2B = glob.glob("/data/codex/artifacts/eprp-paleodata-backup/latest/classic-compendia/fr2/bristol/raw/*/")[0]
TSD = "/data/codex/artifacts/eprp-paleodata-backup/latest/timescale/derived/2026-10-23T0844Z/"

items = []   # (source, role, path, manifest_dir)
for f in sorted(glob.glob(PBDB + "occurrences__p*.csv")) + sorted(glob.glob(PBDB + "collections__p*.csv")):
    items.append(("pbdb", "read", f, PBDB))
for n in ["references.csv", "taxa.csv", "intervals.csv", "datainfo.json"]:
    items.append(("pbdb", "read", PBDB + n, PBDB))
for f in sorted(glob.glob(MAC + "units__p*.csv")) + sorted(glob.glob(MAC + "columns__p*.geojson")):
    p = os.path.basename(f)[-7:-4] if f.endswith(".csv") else os.path.basename(f)[-11:-8]
    if p.endswith("14") or p.endswith("13"):
        continue
    items.append(("macrostrat", "read", f, MAC))
items.append(("macrostrat", "read (interval comparison)", MAC + "defs__intervals.json", MAC))
items.append(("timescale", "read", TSM + "intervals_all.json", TSM))
for n in ["ics2024_pbdb_bases.tsv", "isc_boundaries_by_version.tsv"]:
    items.append(("timescale", "read (EPRP derived; no manifest)", TSD + n, None))
for n in ["fr2_families.csv", "fr2_divisions.csv"]:
    items.append(("classic-compendia fr2", "read (EPRP derived; no manifest)", FR2D + n, None))
for n in ["2-Fungi.xlsx", "3-Algae.xlsx", "42-Bryophyta.xlsx", "43-Pteridophyta.xlsx", "44-Gymnospermophyta.xlsx",
          "45-Magnoliophyta.xlsx"]:
    items.append(("classic-compendia fr2", "upstream, not read", FR2B + n, FR2B))

man = {}


def manifest(d):
    if d not in man:
        man[d] = {x["key"]: x["sha256"] for x in json.load(open(d + "MANIFEST.json"))["files"]}
    return man[d]


with open(OUT + "inputs_sha256.tsv", "w", encoding="utf-8") as fh:
    fh.write("source\trole\tmirror_path\tbytes\tsha256\tmirror_manifest_sha256\tmatches_manifest\n")
    for src, role, path, md in items:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        exp = manifest(md).get(os.path.basename(path), "") if md else ""
        ok = "" if not md else ("yes" if exp == h.hexdigest() else "NO")
        fh.write(f"{src}\t{role}\t{path}\t{os.path.getsize(path)}\t{h.hexdigest()}\t{exp}\t{ok}\n")
        print(path, ok, file=sys.stderr, flush=True)
