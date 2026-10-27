"""Independent checks of the GBDB extraction against the converted source CSVs.

Usage (on deep-server): ssh deep-server python3 -I - RAW_DIR OUT_DIR < gbdb_verify.py
Checks, each printed as PASS or FAIL with counts:
  1. every row of gbdb_plant_fossils.csv and gbdb_plant_no_age_candidates.csv equals its source row in all original columns
  2. the set of window sections recomputed from the source (any row with early_age > 383 and late_age < 485) equals gbdb_window_sections_all.csv
  3. per-section window taxon-row counts (excluding exact duplicate rows) equal the sum of the effort-group columns
  4. every window row in a GBDB plant group appears in gbdb_plant_fossils.csv (no plant-group row lost), and the window plant rows
     in the output all sit inside the window or are anchor Frasnian-Famennian rows
  5. gbdb_plant_sections.csv holds every unit of every plant section exactly once and its unit fields equal the source
"""
import collections
import csv
import sys
from pathlib import Path

csv.field_size_limit(10**9)
RAW, OUT = Path(sys.argv[1]), Path(sys.argv[2])


def load(p):
    with open(p, newline="", encoding="utf-8") as fh:
        r = csv.reader(fh)
        h = next(r)
        return h, [row for row in r]


SH, S = load(RAW / "csv" / "GBDB_all_sections__Sheet1.csv")
seen = collections.Counter(SH)
names, cnt = [], collections.Counter()
for h in SH:
    names.append(h if cnt[h] == 0 else f"{h}.{cnt[h]}")
    cnt[h] += 1
IX = {n: i for i, n in enumerate(names)}
ok_all = True


def report(name, ok, detail=""):
    global ok_all
    ok_all &= ok
    print(("PASS " if ok else "FAIL ") + name + (" " + detail if detail else ""))


def f(v):
    try:
        return float(v)
    except ValueError:
        return None


# 1. source equality
for fn in ("gbdb_plant_fossils.csv", "gbdb_plant_no_age_candidates.csv"):
    h, rows = load(OUT / fn)
    orig = [c for c in h if not c.startswith("derived_") and not c.startswith("j_fossils_")]
    cols = [IX[c] for c in orig]
    bad = 0
    xr = h.index("derived_sections_xlsx_row")
    for r in rows:
        src = S[int(r[xr]) - 2]
        if any(r[h.index(c)] != src[IX[c]] for c in orig):
            bad += 1
    report(f"1 source equality {fn}", bad == 0, f"rows={len(rows)} mismatches={bad} original_columns={len(orig)}")

# 2. window sections recomputed
win = set()
for r in S:
    ea, la = f(r[IX["early_age"]]), f(r[IX["late_age"]])
    if ea is not None and la is not None and ea > 383 and la < 485:
        win.add(r[0])
h, rows = load(OUT / "gbdb_window_sections_all.csv")
outset = {r[0] for r in rows}
report("2 window section set", win == outset, f"recomputed={len(win)} output={len(outset)} only_recomputed={len(win - outset)} only_output={len(outset - win)}")

# 3. per-section taxon-row counts
import hashlib
first = {}
dup = [False] * len(S)
for n, r in enumerate(S):
    d = hashlib.md5("\x1f".join(r).encode("utf-8")).digest()
    if d in first:
        dup[n] = True
    else:
        first[d] = n
cnts = collections.Counter()
for n, r in enumerate(S):
    ea, la = f(r[IX["early_age"]]), f(r[IX["late_age"]])
    if ea is not None and la is not None and ea > 383 and la < 485 and r[IX["genusname"]] and not dup[n]:
        cnts[r[0]] += 1
eff = [i for i, c in enumerate(h) if c.startswith("derived_n_") and c not in (
    "derived_n_units_total", "derived_n_units_window", "derived_n_units_no_age", "derived_n_formations_window", "derived_n_collections_window_units",
    "derived_n_taxon_rows_window_units", "derived_n_taxon_rows_all_units", "derived_n_window_units_with_plant_records")]
tw = h.index("derived_n_taxon_rows_window_units")
bad = sum(1 for r in rows if cnts[r[0]] != int(r[tw]) or cnts[r[0]] != sum(int(r[i]) for i in eff))
report("3 per-section taxon-row counts", bad == 0, f"sections={len(rows)} mismatches={bad} total_taxon_rows={sum(cnts.values())}")

# 4. no plant-group row lost
PG = {"Lycopodiophyta", "Psilotophyta", "Equisetophyta", "Filicophyta", "Bryophyta", "Marchantiophyta", "Anthocerotophyta", "Cycadophyta",
      "Coniferophyta", "Ginkgophyta", "Gnetophyta", "Magnoliophyta", "Sporites", "Pollenites", "Chlorophyta", "Charophyta", "Rhodophyta",
      "Phaeophyta", "Acritarchs"}
h4, rows4 = load(OUT / "gbdb_plant_fossils.csv")
got = {int(r[h4.index("derived_sections_xlsx_row")]) for r in rows4}
missing = []
for n, r in enumerate(S):
    ea, la = f(r[IX["early_age"]]), f(r[IX["late_age"]])
    if r[IX["FossilGroup"]] in PG and r[IX["genusname"]] and ea is not None and ea > 383 and la < 485 and (n + 2) not in got:
        missing.append(n + 2)
report("4 window plant-group rows all present", not missing, f"plant-group window rows absent from output={len(missing)}")
outside = 0
for r in rows4:
    ea, la = f(r[h4.index("early_age")]), f(r[h4.index("late_age")])
    wb = r[h4.index("derived_window_basis")]
    if wb == "window" and not (ea > 383 and la < 485):
        outside += 1
    if wb == "anchor_ff" and not (ea > 358.86 and la < 383):
        outside += 1
report("4 output rows inside window or anchor Frasnian-Famennian", outside == 0, f"outside={outside}")

# 5. plant sections
h5, rows5 = load(OUT / "gbdb_plant_sections.csv")
psecs = {r[h4.index("sectionID")] for r in rows4}
units = {}
for r in S:
    if r[0] in psecs:
        units.setdefault((r[0], r[IX["fromation_id"]], r[IX["unit_id"]]), r)
ids = [(r[h5.index("sectionID")], r[h5.index("fromation_id")], r[h5.index("unit_id")]) for r in rows5]
bad = 0
for r, k in zip(rows5, ids):
    src = units.get(k)
    if src is None or any(r[h5.index(c)] != src[IX[c]] for c in names[:55]):
        bad += 1
report("5 plant sections: units complete, unique, equal to source", len(ids) == len(set(ids)) and set(ids) == set(units) and bad == 0,
       f"units_output={len(ids)} units_source={len(units)} mismatches={bad}")
print("ALL PASS" if ok_all else "SOME CHECKS FAILED")
