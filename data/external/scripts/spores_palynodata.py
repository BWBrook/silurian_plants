"""Extract the 485–383 Ma window from Palynodata (2006 version) as-is, with documents and formations.

Usage (from data/external/): python3 scripts/spores_palynodata.py
Needs `unzip`, `bsdtar` (macOS built-in) and `mdb-export` (Homebrew mdbtools). Input is the release
zip at local/spores/of_5793.zip, a copy of deep-server:/data/codex/silurian_plants/raw/palynodata/
2026-10-27T0038Z/of_5793.zip (GSC Open File 5793, doi 10.4095/225704, Open Government Licence –
Canada). Source values are copied unchanged; added columns are prefixed derived_.

Window rows: TAXON rows whose numeric age range (agestart, ageend) overlaps 383–485 Ma, plus rows
with no numeric age whose age names match a window term. All microfossil types are kept.
"""

import csv
import hashlib
import re
import shutil
import subprocess
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ZIP = Path("local/spores/of_5793.zip")
ZIP_SHA = "5460e39df359db91ae16e8bff7d156f9f190901af9505d838b26dee8cc70db1a"
MDB_SHA = "eb1fa8c3b2f8a1e06a31e2194846ae541ac5240338b4194f63b00823ccde85c1"
WORK = Path("local/spores/work")
OUT = Path("spores")
OLD, YOUNG = 485.0, 383.0
WELLMAN_URL = "https://ndownloader.figshare.com/files/5423108"

WINDOW_TERMS = re.compile(
    r"ordovic|tremado|arenig|llanvirn|llandeilo|caradoc|ashgill|hirnant|katian|sandbian|darriwil|"
    r"dapingian|floian|whiterock|silurian|gothland|llandover|wenlock|ludlo|pridol|downton|devonian|"
    r"gedinn|lochkov|siegen|prag|emsian|eifel|givet|dittonian|breconian",
    re.IGNORECASE,
)

CODES = [
    ("TMIC", "A", "Acritarchs"), ("TMIC", "B", "Calcareous Dinoflagellates"),
    ("TMIC", "C", "(Unregistered Type) (nanno)"), ("TMIC", "D", "Dinoflagellates"),
    ("TMIC", "E", "Algae"), ("TMIC", "F", "Fungal Spores"), ("TMIC", "K", "Scolecodonts"),
    ("TMIC", "L", "Plants"), ("TMIC", "M", "Microfossils of unknown affinity"), ("TMIC", "O", "Other"),
    ("TMIC", "P", "(Unregistered Type) (foram)"), ("TMIC", "R", "Modern Dinoflagellates"),
    ("TMIC", "S", "Spores or Pollen"), ("TMIC", "T", "Silicious Microfossils"), ("TMIC", "Z", "Chitinozoans"),
    ("TIDR", "A", "cf./aff. and reworked taxa"), ("TIDR", "B", "cf./aff. and caved taxa"),
    ("TIDR", "C", "caved taxa"), ("TIDR", "I", "(error?)"), ("TIDR", "M", "(error?)"),
    ("TIDR", "R", "reworked taxa"), ("TIDR", "S", "(error?)"), ("TIDR", "X", "cf./aff. with genus or species"),
    ("TNEW", "I", "Informal Taxon"), ("TNEW", "S", "(error?)"), ("TNEW", "U", "Unpublished Taxon"),
    ("TNEW", "X", "New Taxon"), ("TNEWC", "X", "New Combination"), ("TEME", "X", "Emendation"),
    ("TSYN", "C", "Comment on Status"), ("TSYN", "I", "(error?)"), ("TSYN", "J", "Junior Synonym"),
    ("TSYN", "L", "(error?)"), ("TSYN", "N", "Nomen nudum"), ("TSYN", "S", "Senior Synonym"),
    ("TSYN", "X", "Synonym List"),
]
RELEASE_DOCS = ["readme.txt", "licence.txt", "citation.txt", "metadata.txt", "abstract.txt",
                "doc/HTML/DESCRIPT.HTM", "doc/HTML/LICENCE.HTM", "doc/HTML/CPYRIGHT.HTM", "doc/HTML/PALINTRO.HTM"]


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def export(table):
    out = WORK / f"{table}.csv"
    with out.open("w") as f:
        subprocess.run(["mdb-export", str(WORK / "paly.mdb"), table], stdout=f, check=True)
    with out.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows):>7} rows -> {path}")


def docnum(v):
    v = (v or "").strip()
    return str(int(v)) if v.isdigit() else v


assert sha256(ZIP) == ZIP_SHA, "release zip differs from the mirrored copy"
WORK.mkdir(parents=True, exist_ok=True)
subprocess.run(["unzip", "-q", "-o", str(ZIP), "apps/Paly.CAB", *RELEASE_DOCS, "-d", str(WORK)], check=True)
subprocess.run(["bsdtar", "-xf", str(WORK / "apps/Paly.CAB"), "-C", str(WORK), "paly.mdb"], check=True)
assert sha256(WORK / "paly.mdb") == MDB_SHA, "paly.mdb differs from the inspected copy"
OUT.mkdir(exist_ok=True)

taxon = export("TAXON")
fields = list(taxon[0])
keep, by_doc = [], defaultdict(Counter)
for r in taxon:
    try:
        a, b = float(r["agestart"]), float(r["ageend"])
        old, young = max(a, b), min(a, b)
        hit, basis = old > YOUNG and young < OLD, "numeric_overlap"
    except ValueError:
        old = young = None
        hit, basis = bool(WINDOW_TERMS.search(" ".join([r["oldage"], r["youngage"], r["tage"]]))), "age_name_only"
    if not hit:
        continue
    r = dict(r)
    r["derived_window_basis"] = basis
    r["derived_old_ma"] = "" if old is None else f"{old:g}"
    r["derived_young_ma"] = "" if young is None else f"{young:g}"
    r["derived_span_myr"] = "" if old is None else f"{old - young:g}"
    r["derived_fully_inside_window"] = "" if old is None else str(old <= OLD and young >= YOUNG)
    r["derived_docnum"] = docnum(r["TDOC"])
    keep.append(r)
    by_doc[r["derived_docnum"]][r["TMIC"]] += 1
derived = ["derived_window_basis", "derived_old_ma", "derived_young_ma", "derived_span_myr",
           "derived_fully_inside_window", "derived_docnum"]
write(OUT / "palynodata_taxon_window.csv", keep, fields + derived)

docs = [dict(r) for r in export("NewEng") if docnum(r["AUTHDOCNUM"]) in by_doc]
types = sorted({t for c in by_doc.values() for t in c})
for r in docs:
    c = by_doc[docnum(r["AUTHDOCNUM"])]
    for t in types:
        r[f"derived_window_rows_{t or 'blank'}"] = c.get(t, 0)
    r["derived_window_has_spores"] = c.get("S", 0) > 0
doc_fields = list(docs[0]) if docs else []
write(OUT / "palynodata_documents_window.csv", docs, doc_fields)
missing = set(by_doc) - {docnum(r["AUTHDOCNUM"]) for r in docs}
print(f"window documents without a NewEng citation: {len(missing)}")

lith = [r for r in export("LITHOSTR") if docnum(r["AUTHDOCNUM"]) in by_doc]
write(OUT / "palynodata_lithostr_window.csv", lith, ["AUTHDOCNUM", "AUTHSEQNUM", "LITHOSTGR"])

for table, name in [("THEAGETABLE", "palynodata_theagetable.csv"), ("agetable", "palynodata_agetable.csv"),
                    ("AGE_CHANGE", "palynodata_age_change.csv"), ("TAXLOC", "palynodata_taxloc.csv")]:
    rows = export(table)
    write(OUT / name, rows, list(rows[0]))
write(OUT / "palynodata_codes.csv", [dict(zip(("field", "code", "meaning"), c)) for c in CODES],
      ["field", "code", "meaning"])

rel = OUT / "palynodata_release"
for d in RELEASE_DOCS:
    (rel / d).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(WORK / d, rel / d)

wel = OUT / "wellman2013_supplement"
wel.mkdir(exist_ok=True)
req = urllib.request.Request(WELLMAN_URL, headers={"User-Agent": "silurian_plants-data/1.0"})
with urllib.request.urlopen(req, timeout=60) as r:
    (wel / "18680.pdf").write_bytes(r.read())
print("Wellman et al. 2013 supplement sha256", sha256(wel / "18680.pdf"))

n = Counter(r["TMIC"] for r in keep)
print("window rows by TMIC:", dict(n.most_common()))
print("window documents:", len(by_doc), "with spores:", sum(1 for c in by_doc.values() if c.get("S")))
