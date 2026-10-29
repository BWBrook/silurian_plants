"""record_fr2.py: plant, algal and fungal families of Benton's Fossil Record 2 (FR2), flagged for the
485-383 Ma window.

Run on nectar:  ssh nectar python3 - < record_fr2.py
Reads EPRP's derived FR2 tables (classic-compendia/fr2/derived), which EPRP built from Bristol's chapter
workbooks. FR2 has no stated licence, so the output belongs in data/eprp/local/record/ (gitignored).
Writes fr2_plant_families.csv to OUT.
"""
import csv
import glob
import sys

OUT = "/data/codex/silurian_plants/eprp/record/out/"
D = glob.glob("/data/codex/artifacts/eprp-paleodata-backup/latest/classic-compendia/fr2/derived/*/")[0]
KINGDOMS = {"Plantae": "land_plants_fr2_kingdom_Plantae", "Algae": "algae_fr2_kingdom_Algae_flagged",
            "Fungi": "fungi_fr2_kingdom_Fungi_flagged"}
# FR2 divisions whose names correspond to ICS stages overlapping 485-383 Ma (stage names are the stable
# correlation; FR2's own ages are Harland et al. 1990 and sit 3-25 Myr away from ICS v2024/12)
WINDOW_BY_NAME = ["Tremadoc", "Arenig", "Llanvirn", "Llandeilo", "Caradoc", "Ashgill", "Llandovery", "Wenlock", "Ludlow",
                  "Pridoli", "Lochkovian", "Pragian", "Emsian", "Eifelian", "Givetian"]
WIN_TOP, WIN_BASE = 383.0, 485.0

divs = list(csv.DictReader(open(D + "fr2_divisions.csv", newline="")))
names = [r["division"] for r in divs]
IDX = {n: i for i, n in enumerate(names)}
BASEMA = {r["division"]: float(r["base_ma"]) if r["base_ma"] else None for r in divs}
TOPMA = {r["division"]: float(r["top_ma"]) if r["top_ma"] else None for r in divs}
WIN_IDX = {IDX[n] for n in WINDOW_BY_NAME}
HARLAND_WIN = {n for n in names if BASEMA[n] is not None and BASEMA[n] > WIN_TOP and TOPMA[n] < WIN_BASE}

rows = list(csv.DictReader(open(D + "fr2_families.csv", newline="")))
fields = list(rows[0].keys())
DER = ["d_group", "d_max_range_overlaps_window_by_division_name", "d_min_range_overlaps_window_by_division_name",
       "d_max_range_overlaps_window_by_harland_ages", "d_max_first_division_in_window_by_name",
       "d_max_first_harland_base_ma", "d_max_last_harland_top_ma", "d_n_window_divisions_in_max_range"]


def span(a, b):
    if a in IDX and b in IDX and IDX[a] <= IDX[b]:
        return range(IDX[a], IDX[b] + 1)
    return None


out = []
for r in rows:
    if r["kingdom"] not in KINGDOMS:
        continue
    ms = span(r["max_first"], r["max_last"])
    ns = span(r["min_first"], r["min_last"])
    ov_max = "" if ms is None else ("yes" if WIN_IDX & set(ms) else "no")
    ov_min = "" if ns is None else ("yes" if WIN_IDX & set(ns) else "no")
    hl = ""
    if ms is not None:
        hl = "yes" if any(names[i] in HARLAND_WIN for i in ms) else "no"
    first_in = "" if r["max_first"] not in IDX else ("yes" if IDX[r["max_first"]] in WIN_IDX else "no")
    b = BASEMA.get(r["max_first"])
    t = TOPMA.get(r["max_last"])
    out.append([r[k] for k in fields] + [KINGDOMS[r["kingdom"]], ov_max, ov_min, hl, first_in,
                                         "" if b is None else b, "" if t is None else t,
                                         "" if ms is None else len(WIN_IDX & set(ms))])
with open(OUT + "fr2_plant_families.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(fields + DER)
    w.writerows(out)
print("rows", len(out), file=sys.stderr)
print("overlapping window by name (max range):", sum(1 for o in out if o[len(fields) + 1] == "yes"), file=sys.stderr)
print("by group:", {k: sum(1 for o in out if o[len(fields)] == v) for k, v in KINGDOMS.items()}, file=sys.stderr)
print("Harland ages window divisions:", sorted(HARLAND_WIN, key=lambda n: IDX[n]), file=sys.stderr)
