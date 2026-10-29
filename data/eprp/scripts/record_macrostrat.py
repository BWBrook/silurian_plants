"""record_macrostrat.py: Macrostrat units overlapping 485-383 Ma, with environment class, column
metadata, and counts and column area by stage.

Run on nectar:  ssh nectar python3 - < record_macrostrat.py
Reads the Macrostrat snapshot read-only; writes macrostrat_units_window.csv and
macrostrat_summary_by_stage.csv to OUT.

Coverage: Macrostrat's land columns are mostly North American; see the README. Project 14 ("core columns")
composites the other projects and is excluded; project 13 is empty.
"""
import csv
import collections
import glob
import json
import re
import sys

csv.field_size_limit(1 << 30)
SNAP = "/data/codex/artifacts/eprp-paleodata-backup/latest/macrostrat/raw/2026-10-25T0011Z_url/"
OUT = "/data/codex/silurian_plants/eprp/record/out/"
WIN_TOP, WIN_BASE = 383.0, 485.0
EXCLUDE_PROJECTS = {"14", "13"}

# data/timescale.csv of the consuming project (sha256 baf5a4071bd1b47010c3a5f1ffe7b3aebb1fe773497724968a7fcd5858d4c35f);
# Givetian top uses the ICS v2024/12 Frasnian base 382.31 (not in the project table)
PROJECT = [("Givetian", 387.95), ("Eifelian", 393.47), ("Emsian", 410.62), ("Pragian", 413.02), ("Lochkovian", 419.62),
           ("Pridoli", 422.7), ("Ludfordian", 425.0), ("Gorstian", 426.7), ("Homerian", 430.6), ("Sheinwoodian", 432.9),
           ("Telychian", 438.6), ("Aeronian", 440.5), ("Rhuddanian", 443.1), ("Hirnantian", 445.2), ("Katian", 452.8),
           ("Sandbian", 458.2), ("Darriwilian", 469.4), ("Dapingian", 471.3), ("Floian", 477.1), ("Tremadocian", 486.85)]
BASE = dict(PROJECT)
STAGES = [s for s, _ in PROJECT]
TOP = {s: (BASE[STAGES[i - 1]] if i else 382.31) for i, s in enumerate(STAGES)}
MID = {s: (TOP[s] + BASE[s]) / 2 for s in STAGES}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ---- column metadata
COLS = {}
PROJECT_NAME = {}
for fpath in sorted(glob.glob(SNAP + "columns__p*.geojson")):
    pid = re.search(r"p(\d+)", fpath).group(1)
    if pid in EXCLUDE_PROJECTS:
        continue
    with open(fpath, encoding="utf-8") as fh:
        feats = json.load(fh)["success"]["data"]["features"]
    for ft in feats:
        p = ft["properties"]
        COLS[(pid, str(p["col_id"]))] = p
        PROJECT_NAME[pid] = p.get("project_name", "")
log("columns", len(COLS), PROJECT_NAME)

# ---- units
HEAD = None
win_units = []
n_units_all = 0
for fpath in sorted(glob.glob(SNAP + "units__p*.csv")):
    pid = re.search(r"p(\d+)", fpath).group(1)
    if pid in EXCLUDE_PROJECTS:
        continue
    with open(fpath, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        try:
            h = next(rd)
        except StopIteration:
            continue
        if HEAD is None:
            HEAD = h
        assert h == HEAD, fpath
        ix = {k: i for i, k in enumerate(h)}
        for row in rd:
            n_units_all += 1
            try:
                t, b = float(row[ix["t_age"]]), float(row[ix["b_age"]])
            except ValueError:
                continue
            if b > WIN_TOP and t < WIN_BASE:
                win_units.append((pid, row))
IX = {k: i for i, k in enumerate(HEAD)}
log("units read", n_units_all, "in window", len(win_units))


def env_info(s):
    """classes of the '|'-separated environment entries 'name type class [~ proportion]'"""
    entries = [e.strip() for e in s.split("|") if e.strip()]
    marine, nonmarine, nm_names = False, False, []
    for e in entries:
        e = re.sub(r"\s*~\s*[0-9.eE+-]+$", "", e).strip()
        if e.endswith("non-marine"):
            nonmarine = True
            nm_names.append(e[: -len("non-marine")].strip() or "non-marine")
        elif e.endswith("marine"):
            marine = True
    if marine and nonmarine:
        cls = "both"
    elif marine:
        cls = "marine"
    elif nonmarine:
        cls = "non-marine"
    else:
        cls = "unknown"
    return cls, nm_names


DER = ["d_span_myr", "d_env_class", "d_nonmarine_flag", "d_nonmarine_environments", "d_project_stages_overlapped",
       "d_n_project_stages_overlapped"]
JOIN = ["j_project_name", "j_col_name", "j_col_group", "j_col_type", "j_status_code", "j_col_area_km2"]
rows_out = []
unit_info = []   # (pid, col_id, status, area, t, b, cls)
for pid, row in sorted(win_units, key=lambda x: (x[0], int(x[1][IX["col_id"]]), int(x[1][IX["unit_id"]]))):
    t, b = float(row[IX["t_age"]]), float(row[IX["b_age"]])
    cls, nm = env_info(row[IX["environ"]])
    cp = COLS.get((pid, row[IX["col_id"]]), {})
    ov = [s for s in STAGES if min(b, BASE[s]) - max(t, TOP[s]) > 1e-9]
    rows_out.append(row + [cp.get("project_name", ""), cp.get("col_name", ""), cp.get("col_group", ""), cp.get("col_type", ""),
                           cp.get("status_code", ""), cp.get("col_area", "")]
                    + [f"{b - t:.4g}", cls, "yes" if cls in ("non-marine", "both") else "no", "; ".join(nm),
                       ";".join(ov), len(ov)])
    unit_info.append((pid, row[IX["col_id"]], cp.get("status_code", ""), float(row[IX["col_area"]] or 0), t, b, cls))
with open(OUT + "macrostrat_units_window.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(HEAD + JOIN + DER)
    w.writerows(rows_out)
log("units written", len(rows_out))

# ---- summary by stage
labels_of = {"marine": ["marine_only", "ANY_marine"], "non-marine": ["nonmarine_only", "ANY_nonmarine"],
             "both": ["both_marine_and_nonmarine", "ANY_marine", "ANY_nonmarine"], "unknown": ["unknown"]}
LABEL_ORDER = ["ALL", "marine_only", "nonmarine_only", "both_marine_and_nonmarine", "unknown", "ANY_marine", "ANY_nonmarine"]
cell = collections.defaultdict(lambda: dict(n_ov=0, n_ov_act=0, n_mid_act=0, cols_ov=set(), cols_mid=set(), area={}))
for pid, col, status, area, t, b, cls in unit_info:
    for s in STAGES:
        ov = min(b, BASE[s]) - max(t, TOP[s])
        if ov <= 1e-9:
            continue
        mid = t <= MID[s] <= b
        for lab in ["ALL"] + labels_of[cls]:
            c = cell[(pid, s, lab)]
            c["n_ov"] += 1
            if status == "active":
                c["n_ov_act"] += 1
                c["cols_ov"].add(col)
                c["area"][col] = area
                if mid:
                    c["n_mid_act"] += 1
                    c["cols_mid"].add(col)
with open(OUT + "macrostrat_summary_by_stage.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["project_id", "project_name", "stage", "stage_base_ma", "stage_top_ma", "unit_env_class",
                "n_units_overlapping_stage_all_columns", "n_units_overlapping_stage_active_columns",
                "n_units_spanning_stage_midpoint_active_columns", "n_active_columns_overlapping_stage",
                "n_active_columns_spanning_stage_midpoint", "area_km2_active_columns_overlapping_stage",
                "area_km2_active_columns_spanning_stage_midpoint", "note"])
    for pid in sorted({k[0] for k in cell}, key=int):
        for s in STAGES:
            for lab in LABEL_ORDER:
                c = cell.get((pid, s, lab))
                if c is None:
                    continue
                a_ov = sum(c["area"][k] for k in c["cols_ov"])
                a_mid = sum(c["area"][k] for k in c["cols_mid"])
                note = ""
                if lab.startswith("ANY_"):
                    note = "units with at least one marine (or non-marine) entry; overlaps marine_only/both or nonmarine_only/both"
                if pid == "10":
                    note = (note + "; " if note else "") + "North American Ediacaran project: columns lie inside project 1's; do not add areas"
                w.writerow([str(int(pid)), PROJECT_NAME.get(pid, ""), s, BASE[s], TOP[s], lab, c["n_ov"], c["n_ov_act"], c["n_mid_act"],
                            len(c["cols_ov"]), len(c["cols_mid"]), f"{a_ov:.1f}", f"{a_mid:.1f}", note])

# ---- diagnostics
byproj = collections.Counter(pid for pid, *_ in unit_info)
log("units by project", dict(byproj))
log("columns with window units by project",
    {pid: len({(p, c) for p, c, *_ in unit_info if p == pid}) for pid in byproj})
log("unit env classes", collections.Counter(c for *_, c in unit_info))
log("column status of window units", collections.Counter(s for _, _, s, *_ in unit_info))
act_area = {}
for pid, col, status, area, *_ in unit_info:
    if status == "active":
        act_area.setdefault(pid, {})[col] = area
log("active column area with a window unit, km2", {pid: round(sum(v.values())) for pid, v in act_area.items()})
