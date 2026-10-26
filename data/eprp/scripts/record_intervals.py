"""record_intervals.py: PBDB and Macrostrat interval definitions overlapping 485-383 Ma, mapped to the
project's stages (data/timescale.csv, ICS v2024/12) and compared with them.

Run on deep-server AFTER record_pbdb.py (it reads that script's plant occurrence file for interval usage):
    ssh deep-server python3 - < record_intervals.py
Reads EPRP's timescale mirror read-only; writes intervals_window.csv and ics2024_chart_values_window.csv to OUT.
The ICS v2024/12 chart values (printed ages and uncertainties, read from the chart PDFs by EPRP) go to the second
file, which belongs in data/eprp/local/record/ because EPRP lists the chart PDFs as licence-unclear.
"""
import csv
import collections
import json
import sys

csv.field_size_limit(1 << 30)
OUT = "/data/codex/silurian_plants-eprp/record/out/"
TS = "/data/paleodata/timescale/"
PBDB_INTERVALS = "/data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url/intervals.csv"
MACROSTRAT_INTERVALS = TS + "macrostrat/raw/2026-10-23T0844Z_url/intervals_all.json"
MACROSTRAT_INTERVALS_UNITS_SNAPSHOT = "/data/paleodata/macrostrat/raw/2026-10-25T0011Z_url/defs__intervals.json"
ICS_PBDB = TS + "derived/2026-10-23T0844Z/ics2024_pbdb_bases.tsv"
ICS_VERSIONS = TS + "derived/2026-10-23T0844Z/isc_boundaries_by_version.tsv"
WIN_TOP, WIN_BASE = 383.0, 485.0
TOL = 0.5


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# data/timescale.csv of the consuming project (sha256 baf5a4071bd1b47010c3a5f1ffe7b3aebb1fe773497724968a7fcd5858d4c35f),
# copied here so the script is self-contained: stage, base_ma (youngest first, as in the file)
PROJECT = [("Givetian", 387.95), ("Eifelian", 393.47), ("Emsian", 410.62), ("Pragian", 413.02), ("Lochkovian", 419.62),
           ("Pridoli", 422.7), ("Ludfordian", 425.0), ("Gorstian", 426.7), ("Homerian", 430.6), ("Sheinwoodian", 432.9),
           ("Telychian", 438.6), ("Aeronian", 440.5), ("Rhuddanian", 443.1), ("Hirnantian", 445.2), ("Katian", 452.8),
           ("Sandbian", 458.2), ("Darriwilian", 469.4), ("Dapingian", 471.3), ("Floian", 477.1), ("Tremadocian", 486.85)]
FRASNIAN_BASE = 382.31   # ICS v2024/12 printed value (Frasnian base) from ics2024_pbdb_bases.tsv; not in the project table
BASE = dict(PROJECT)
ORDER_YOUNG_TO_OLD = [s for s, _ in PROJECT]
TOP = {}
for i, s in enumerate(ORDER_YOUNG_TO_OLD):
    TOP[s] = BASE[ORDER_YOUNG_TO_OLD[i - 1]] if i > 0 else FRASNIAN_BASE
# epoch/period names that are unions of project stages: (oldest stage, youngest stage); top compared only if the
# unit's top coincides with the youngest stage's top
UNIONS = {
    "Early Devonian": ("Lochkovian", "Emsian"), "Lower Devonian": ("Lochkovian", "Emsian"),
    "Middle Devonian": ("Eifelian", "Givetian"),
    "Devonian": ("Lochkovian", None),
    "Silurian": ("Rhuddanian", "Pridoli"), "Llandovery": ("Rhuddanian", "Telychian"),
    "Wenlock": ("Sheinwoodian", "Homerian"), "Ludlow": ("Gorstian", "Ludfordian"),
    "Ordovician": ("Tremadocian", "Hirnantian"), "Early Ordovician": ("Tremadocian", "Floian"),
    "Middle Ordovician": ("Dapingian", "Darriwilian"), "Late Ordovician": ("Sandbian", "Hirnantian"),
}

# PBDB interval re-datings in the window, from EPRP's scans (resources/sources/pbdb-chronosphere/profile/
# redating_2024_2026.tsv, sha256 9fa99b67a2e1e797247d7df12bda7dec102bcdd6947df36fb7ff0b99cad5b300, EPRP commit ac42dfb).
# Value: modal base age (max_ma) of single-interval occurrence rows named so, in PBDB downloads before and after the
# step; step A = between the downloads of 2024-03-31 and 2024-04-01, step B = between 2025-03-31 and 2025-04-10.
# Only names that overlap the window are listed; keyed by interval name (not scale-specific).
REDATING = {}


_RAW = {
    "Aeronian": [("B", 440.8, 440.5, 167)], "Arenig": [("A", 478.6, 477.7, 1526), ("B", 477.7, 477.1, 1526)],
    "Ashbyan": [("A", 460.9, 457.0, 50), ("B", 457.0, 457.3, 50)], "Ashgill": [("A", 449.5, 449.6, 118), ("B", 449.6, 449.5, 222)],
    "Blackriveran": [("A", 460.9, 457.0, 237), ("B", 457.0, 457.3, 262)], "Bohdalec": [("A", 457.5, 458.0, 88), ("B", 458.0, 459.3, 87)],
    "Canadian": [("B", 485.4, 486.85, 61)], "Caradoc": [("A", 460.9, 458.4, 539), ("B", 458.4, 458.2, 537)],
    "Chatfieldian": [("A", 460.9, 453.7, 134), ("B", 453.7, 453.8, 134)], "Chazyan": [("A", 468.1, 470.0, 355), ("B", 470.0, 471.3, 355)],
    "Clinton": [("A", 439.0, 440.7, 153), ("B", 440.7, 440.1, 153)], "Costonian": [("A", 460.9, 458.4, 20), ("B", 458.4, 458.2, 20)],
    "Cressagian": [("A", 485.4, 485.0, 61), ("B", 485.0, 486.4, 61)], "Darriwilian": [("B", 467.3, 469.4, 45)],
    "Dawan": [("A", 478.6, 477.9, 252), ("B", 477.9, 478.8, 252)], "Demingian": [("B", 485.4, 486.85, 33)],
    "Dobrotivian": [("B", 459.7, 461.0, 91)], "Early Devonian": [("B", 419.2, 419.62, 104)],
    "Early Emsian": [("A", 409.1, 407.6, 271), ("B", 407.6, 410.62, 298)], "Early Givetian": [("A", 388.1, 387.7, 186), ("B", 387.7, 387.95, 186)],
    "Early Llandeilo": [("A", 466.0, 461.3, 268), ("B", 461.3, 461.1, 268)], "Early Llanvirn": [("A", 466.0, 468.4, 150), ("B", 468.4, 468.0, 150)],
    "Early Ordovician": [("B", 485.4, 486.85, 50)], "Eastonian": [("A", 456.1, 452.0, 422), ("B", 452.0, 452.3, 422)],
    "Edenian": [("A", 460.9, 451.1, 413), ("B", 451.1, 451.0, 413)], "Eifelian": [("B", 393.3, 393.47, 1299)],
    "Emsian": [("B", 407.6, 410.62, 307)], "Gasconadian": [("B", 485.4, 486.85, 40)], "Givetian": [("B", 387.7, 387.95, 831)],
    "Gorstian": [("B", 427.4, 426.7, 112)], "Harju": [("A", 452.0, 450.6, 94), ("B", 450.6, 450.5, 94)],
    "Helderbergian": [("B", 419.2, 419.62, 27)], "Homerian": [("B", 430.5, 430.6, 47)],
    "Idavere": [("A", 460.9, 457.5, 33), ("B", 457.5, 458.0, 33)], "Katian": [("B", 453.0, 452.8, 24)],
    "Klabava": [("A", 478.6, 477.7, 50), ("B", 477.7, 477.1, 50)], "Kosovian": [("A", 445.6, 445.2, 41)],
    "Lancefieldian": [("A", 485.4, 482.8, 33), ("B", 482.8, 484.3, 33)], "Lasnamagi": [("A", 463.5, 460.4, 58), ("B", 460.4, 461.4, 58)],
    "Late Emsian": [("A", 402.5, 398.3, 342), ("B", 398.3, 399.5, 342)], "Late Llandeilo": [("A", 460.9, 461.3, 62), ("B", 461.3, 461.1, 62)],
    "Late Llanvirn": [("A", 463.5, 461.3, 207), ("B", 461.3, 461.1, 207)], "Late Ordovician": [("B", 458.4, 458.2, 152)],
    "Llandeilo": [("A", 466.0, 461.3, 158), ("B", 461.3, 461.1, 158)], "Llandovery": [("A", 443.4, 443.8, 1475), ("B", 443.8, 443.1, 1474)],
    "Llanvirn": [("A", 466.0, 468.4, 140), ("B", 468.4, 468.0, 140)], "Lochkovian": [("B", 419.2, 419.62, 736)],
    "Longvillian": [("A", 457.5, 457.4, 108), ("B", 457.4, 457.2, 108)], "Ludfordian": [("B", 425.6, 425.0, 394)],
    "Ludlow": [("B", 427.4, 426.7, 369)], "Maysvillian": [("A", 452.0, 450.4, 525), ("B", 450.4, 450.2, 561)],
    "Middle Devonian": [("B", 393.3, 393.47, 130)], "Middle Givetian": [("A", 388.1, 385.9, 57)],
    "Middle Ordovician": [("B", 470.0, 471.3, 307)], "Migneintian": [("A", 485.4, 480.8, 38), ("B", 480.8, 481.1, 38)],
    "Niagaran": [("A", 443.4, 440.1, 30), ("B", 440.1, 439.4, 30)], "Ningkuo": [("A", 478.6, 477.9, 142), ("B", 477.9, 478.8, 142)],
    "Ordovician": [("B", 485.4, 486.85, 67)], "Porkuni": [("A", 445.6, 445.2, 33)], "Pragian": [("B", 410.8, 413.02, 561)],
    "Pridoli": [("B", 423.0, 422.7, 235)], "Pusgillian": [("A", 449.5, 449.6, 111), ("B", 449.6, 449.5, 111)],
    "Rangerian": [("A", 471.8, 470.0, 51), ("B", 470.0, 471.3, 51)], "Rawtheyan": [("A", 455.8, 448.9, 328), ("B", 448.9, 448.8, 328)],
    "Rhuddanian": [("A", 443.4, 443.8, 740), ("B", 443.8, 443.1, 740)], "Richmondian": [("A", 449.5, 449.8, 517), ("B", 449.8, 449.6, 682)],
    "Rocklandian": [("A", 460.9, 457.0, 124), ("B", 457.0, 457.3, 124)], "Sandbian": [("B", 458.4, 458.2, 54)],
    "Sarka": [("B", 467.3, 469.4, 117)], "Sheinwoodian": [("B", 433.4, 432.9, 274)],
    "Shermanian": [("A", 460.9, 457.0, 355), ("B", 457.0, 457.3, 355)], "Silurian": [("A", 443.4, 443.8, 351), ("B", 443.8, 443.1, 351)],
    "Soudleyan": [("A", 457.5, 458.4, 115), ("B", 458.4, 458.2, 115)], "Stairsian": [("A", 485.4, 482.0, 32), ("B", 482.0, 483.4, 32)],
    "Telychian": [("B", 438.5, 438.6, 152)], "Tremadoc": [("A", 485.4, 485.0, 804), ("B", 485.0, 486.4, 804)],
    "Trentonian": [("A", 460.9, 457.0, 70), ("B", 457.0, 457.3, 70)], "Tulean": [("A", 485.4, 480.3, 47), ("B", 480.3, 481.7, 47)],
    "Turinian": [("A", 460.9, 457.0, 36), ("B", 457.0, 457.3, 36)], "Varangu": [("A", 485.4, 482.2, 22), ("B", 482.2, 483.8, 22)],
    "Vinice": [("A", 457.5, 458.0, 31), ("B", 458.0, 459.3, 31)], "Wenlock": [("B", 433.4, 432.9, 828)],
    "Whiterockian": [("A", 471.8, 470.0, 51), ("B", 470.0, 471.3, 51)], "Woolstonian": [("A", 455.8, 457.4, 42), ("B", 457.4, 457.2, 42)],
    "Wufeng": [("B", 449.5, 449.4, 95)], "Zlichovian": [("A", 409.1, 407.6, 27)],
}
STEP_LABEL = {"A": "2024-03-31/04-01", "B": "2025-03-31/04-10"}
for _n, _l in _RAW.items():
    for _s, _o, _nw, _r in _l:
        REDATING.setdefault(_n, {})[_s] = (_o, _nw, _r)


def redating_text(name):
    d = REDATING.get(name)
    if not d:
        return ""
    return "; ".join(f"{STEP_LABEL[s]}: {o}->{n} ({r} rows)" for s, (o, n, r) in sorted(d.items()))


# ------------------------------------------------------------------------------------------------
def overlap(a_top, a_base, b_top, b_base):
    return min(a_base, b_base) - max(a_top, b_top)


def f(x):
    return None if x in ("", None) else float(x)


def stage_map(top, base):
    """project stages overlapping [top, base], best overlap, contained flag"""
    ov = []
    for s in ORDER_YOUNG_TO_OLD:
        o = overlap(top, base, TOP[s], BASE[s])
        if o > 1e-9:
            ov.append((s, o))
    best = max(ov, key=lambda t: t[1]) if ov else None
    contained = len(ov) == 1 and top >= TOP[ov[0][0]] - 1e-9 and base <= BASE[ov[0][0]] + 1e-9
    return ov, best, contained


# ICS chart values for each boundary (older releases from the RDF series): label -> {"2013": ..., "2020": ...}
ICS_OLD = {}
with open(ICS_VERSIONS, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        for lab in r["labels"].split(" | "):
            ICS_OLD.setdefault(lab.strip(), []).append((r["2013_ma"], r["2020_ma"]))
ICS_PBDB_ROWS = {}
with open(ICS_PBDB, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        ICS_PBDB_ROWS[(r["pbdb_interval"], r["pbdb_type"])] = r


def old_chart(name):
    vs = []
    for v in (name, name.replace("Early", "Lower"), name.replace("Late", "Upper")):
        vs.append("Base of " + v)
    hits = []
    for v in vs:
        hits += ICS_OLD.get(v, [])
    hits = list(dict.fromkeys(hits))
    if len(hits) == 1:
        return hits[0]
    return ("", "")


# plant-occurrence usage of interval names (as entered)
use_early, use_late = collections.Counter(), collections.Counter()
with open(OUT + "pbdb_plant_occurrences.csv", newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        use_early[r["early_interval"]] += 1
        if r["late_interval"]:
            use_late[r["late_interval"]] += 1

HEAD = ["source", "source_scale", "interval_id", "interval_name", "abbrev", "interval_type", "parent_id",
        "top_ma", "base_ma", "source_reference_no",
        "ics_v2013_01_gts2012_base_ma", "ics_v2020_01_base_ma",
        "pbdb_redating_steps_base_age",
        "d_is_international_scale", "d_project_stage_exact", "d_project_stages_overlapped", "d_project_stage_best",
        "d_best_overlap_fraction_of_interval", "d_contained_in_one_project_stage",
        "d_base_diff_vs_project_myr", "d_top_diff_vs_project_myr", "d_flag_gt_0p5_myr_vs_project",
        "d_base_diff_vs_ics_v2013_01_myr", "d_flag_gt_0p5_myr_vs_ics_v2013_01",
        "d_base_diff_vs_best_stage_myr", "d_n_plant_filter_occ_early_interval", "d_n_plant_filter_occ_late_interval",
        "d_name_shared_by_n_window_intervals"]
rows = []

# ---- PBDB
pbdb_rows = []
with open(PBDB_INTERVALS, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        t, b = f(r["t_age"]), f(r["b_age"])
        if t is None or b is None:
            continue
        if b > WIN_TOP and t < WIN_BASE:
            pbdb_rows.append(r)
# ---- Macrostrat
with open(MACROSTRAT_INTERVALS, encoding="utf-8") as fh:
    ms = json.load(fh)["success"]["data"]
ms_rows = [r for r in ms if r["b_age"] is not None and r["t_age"] is not None
           and float(r["b_age"]) > WIN_TOP and float(r["t_age"]) < WIN_BASE]
log("pbdb intervals in window", len(pbdb_rows), "macrostrat", len(ms_rows))
INTL_MS = {1, 2, 3, 11, 13, 14, 20}
name_count = collections.Counter([r["interval_name"] for r in pbdb_rows] + [r["name"] for r in ms_rows])


def build(source, scale, iid, name, abbrev, itype, parent, t, b, ref, intl):
    key = (name, itype)
    v13, v20 = old_chart(name) if intl else ("", "")
    ov, best, contained = stage_map(t, b)
    exact = name if name in BASE else ""
    base_diff = top_diff = None
    comp = ""
    if exact:
        base_diff, top_diff = b - BASE[exact], t - TOP[exact]
    elif name in UNIONS and intl:
        old_s, young_s = UNIONS[name]
        base_diff = b - BASE[old_s]
        top_diff = (t - TOP[young_s]) if young_s else None
    flag = ""
    if intl and (base_diff is not None or top_diff is not None):
        flag = "yes" if any(d is not None and abs(d) > TOL for d in (base_diff, top_diff)) else "no"
    d13 = ""
    f13 = ""
    if intl and v13 not in ("", None):
        d13 = b - float(v13)
        f13 = "yes" if abs(d13) > TOL else "no"
    bs = ""
    if best:
        bs = b - BASE[best[0]]
    return [source, scale, iid, name, abbrev, itype, parent, t, b, ref,
            v13, v20,
            redating_text(name) if source == "pbdb" else "",
            "yes" if intl else "no", exact, ";".join(s for s, _ in ov), best[0] if best else "",
            f"{best[1] / (b - t):.3f}" if best else "", "yes" if contained else "no",
            "" if base_diff is None else f"{base_diff:.4g}", "" if top_diff is None else f"{top_diff:.4g}", flag,
            "" if d13 == "" else f"{d13:.4g}", f13, "" if bs == "" else f"{bs:.4g}",
            use_early[name] if source == "pbdb" else "", use_late[name] if source == "pbdb" else "", name_count[name]]


for r in pbdb_rows:
    rows.append(build("pbdb", "pbdb scale " + r["scale_no"], r["interval_no"], r["interval_name"], r["abbrev"], r["type"],
                      r["parent_no"], f(r["t_age"]), f(r["b_age"]), r["reference_no"], r["scale_no"] == "1"))
for r in ms_rows:
    tsids = {x["timescale_id"] for x in r["timescales"] if x["timescale_id"] is not None}
    rows.append(build("macrostrat", "; ".join(f'{x["timescale_id"]} {x["name"]}' for x in r["timescales"] if x["timescale_id"] is not None) or "(no timescale listed)",
                      r["int_id"], r["name"], r["abbrev"] or "", r["int_type"], "", float(r["t_age"]), float(r["b_age"]), "",
                      bool(tsids & INTL_MS)))
rows.sort(key=lambda x: (x[0], -float(x[8]), float(x[7]), x[3]))
with open(OUT + "intervals_window.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(HEAD)
    w.writerows(rows)

with open(OUT + "ics2024_chart_values_window.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["pbdb_interval", "pbdb_type", "pbdb_base_ma", "ics_2024_12_printed", "uncertainty_ma", "approximate",
                "integer_token"])
    for r in pbdb_rows:
        if r["scale_no"] == "1":
            ics = ICS_PBDB_ROWS.get((r["interval_name"], r["type"]))
            if ics:
                w.writerow([ics["pbdb_interval"], ics["pbdb_type"], ics["pbdb_base_ma"], ics["ics_2024_12_printed"],
                            ics["uncertainty_ma"], ics["approximate"], ics["integer_token"]])

# ---- diagnostics
IX = {k: i for i, k in enumerate(HEAD)}
log("rows", len(rows), collections.Counter(r[0] for r in rows))
flag = [r for r in rows if r[IX["d_flag_gt_0p5_myr_vs_project"]] == "yes"]
log("international rows compared with project table:", sum(1 for r in rows if r[IX["d_flag_gt_0p5_myr_vs_project"]] != ""),
    "flagged >0.5 Myr:", len(flag))
for r in flag:
    log("  FLAG", r[0], r[IX["interval_name"]], r[IX["top_ma"]], r[IX["base_ma"]], r[IX["d_base_diff_vs_project_myr"]], r[IX["d_top_diff_vs_project_myr"]])
f13 = [r for r in rows if r[IX["d_flag_gt_0p5_myr_vs_ics_v2013_01"]] == "yes"]
log("rows differing >0.5 Myr from ICS v2013/01 (GTS2012):", [(r[0], r[IX["interval_name"]], r[IX["base_ma"]], r[IX["ics_v2013_01_gts2012_base_ma"]]) for r in f13])
# PBDB vs Macrostrat international intervals, same names
pb = {r["interval_name"]: (f(r["t_age"]), f(r["b_age"])) for r in pbdb_rows if r["scale_no"] == "1"}
dif = []
for r in ms_rows:
    if r["name"] in pb and {x["timescale_id"] for x in r["timescales"]} & INTL_MS:
        if abs(float(r["b_age"]) - pb[r["name"]][1]) > 1e-6 or abs(float(r["t_age"]) - pb[r["name"]][0]) > 1e-6:
            dif.append((r["name"], pb[r["name"]], r["t_age"], r["b_age"]))
log("PBDB scale 1 vs Macrostrat international: differing names", dif)
# Macrostrat intervals: timescale mirror (2026-10-23) vs units snapshot (2026-10-25)
with open(MACROSTRAT_INTERVALS_UNITS_SNAPSHOT, encoding="utf-8") as fh:
    ms2 = {r["int_id"]: r for r in json.load(fh)["success"]["data"]}
nd = 0
for r in ms_rows:
    o = ms2.get(r["int_id"])
    if o is None or o["t_age"] != r["t_age"] or o["b_age"] != r["b_age"] or o["name"] != r["name"]:
        nd += 1
log("macrostrat window intervals differing between the 10-23 timescale copy and the 10-25 units snapshot:", nd)
# project stages not matched by name in PBDB scale 1
log("project stages missing from PBDB scale 1 names:", [s for s in BASE if s not in pb])
# PBDB intervals used by plant-filter occurrences but absent from window intervals table
names_win = {r["interval_name"] for r in pbdb_rows}
miss = [(n, c) for n, c in use_early.items() if n not in names_win]
log("plant-filter early_interval names not among window PBDB intervals:", miss[:20], len(miss))
