"""rockrecord_build.py: build the Silurian-Devonian British rock-record tables from the DiGMapGB-625 polygons and the BGS Lexicon.

Run on deep-server after rockrecord_bgs_polygons.py and rockrecord_lexicon.py (stdlib only):
    ssh deep-server python3 - < rockrecord_build.py
Reads <raw stamp>/derived/{bedrock_polygons.csv, lexicon_entries.csv, lexicon_divisions.csv, sd_lex_codes.txt}; writes to
<raw stamp>/derived/out/ :
  bgs_units_silurian_devonian.csv       one row per LEX code (tracked)
  bgs_outcrop_area_by_age.csv           outcrop area by BGS period, series and stage (tracked)
  bgs_polygon_age_scale_observed.csv    BGS age terms in the polygon attributes with their year values (tracked; evidence for the scale)
  bgs_geochronology_divisions_used.csv  BGS Geochronology Division values the Lexicon uses (tracked)
  bgs_lexicon_entries_sd.csv            full Lexicon entries including prose fields (local only)
  bgs_polygons_silurian_devonian.csv    polygon-level attribute table with derived columns, no geometry (local only)

Ages are BGS's own and are never converted: polygon years (2008 edition scale) and Lexicon Ma (BGS Geochronology, current) are kept in
separate columns, and everything computed is prefixed derived_.
"""
import collections
import csv
import glob
import os
import re
import shutil
import sys

csv.field_size_limit(1 << 30)
RAW = os.path.dirname(sorted(glob.glob("/data/codex/silurian_plants/raw/bgs/*/bgs_geology_625k_shapefile.zip"))[-1]) + "/"
DER = RAW + "derived/"
OUT = DER + "out/"
os.makedirs(OUT, exist_ok=True)
SD_TOP_Y, SD_BASE_Y = 354_000_000, 443_000_000
# Base ages (Ma) of the project's stages, data/timescale.csv (ICS v2024/12), as read on 2026-10-27 (file sha256 396bde65de806aba...):
PROJ = {"Tournaisian": 358.86, "Famennian": 372.15, "Frasnian": 382.31, "Givetian": 387.95, "Eifelian": 393.47, "Emsian": 410.62,
        "Pragian": 413.02, "Lochkovian": 419.62, "Pridoli": 422.7, "Ludfordian": 425.0, "Gorstian": 426.7, "Homerian": 430.6,
        "Sheinwoodian": 432.9, "Telychian": 438.6, "Aeronian": 440.5, "Rhuddanian": 443.1, "Hirnantian": 445.2, "Tremadocian": 486.85}
# BGS term -> (project stage whose base is the term's base, project stage whose base is the term's top)
TERM_TO_PROJ = {"SILURIAN": ("Rhuddanian", "Lochkovian"), "DEVONIAN": ("Lochkovian", "Tournaisian"),
                "LLANDOVERY": ("Rhuddanian", "Sheinwoodian"), "WENLOCK": ("Sheinwoodian", "Gorstian"), "LUDLOW": ("Gorstian", "Pridoli"),
                "PRIDOLI": ("Pridoli", "Lochkovian"), "EARLY DEVONIAN": ("Lochkovian", "Eifelian"), "MID DEVONIAN": ("Eifelian", "Frasnian"),
                "LATE DEVONIAN": ("Frasnian", "Tournaisian"), "RHUDDANIAN": ("Rhuddanian", "Aeronian"), "TELYCHIAN": ("Telychian", "Sheinwoodian"),
                "LOCHKOVIAN": ("Lochkovian", "Pragian"), "PRAGHIAN": ("Pragian", "Emsian"), "EMSIAN": ("Emsian", "Eifelian"),
                "FAMENNIAN": ("Famennian", "Tournaisian")}
LABEL_TO_PROJ = {"Silurian Period": "Rhuddanian", "Llandovery Epoch": "Rhuddanian", "Rhuddanian Age": "Rhuddanian", "Aeronian Age": "Aeronian",
                 "Telychian Age": "Telychian", "Wenlock Epoch": "Sheinwoodian", "Sheinwoodian Age": "Sheinwoodian", "Homerian Age": "Homerian",
                 "Ludlow Epoch": "Gorstian", "Gorstian Age": "Gorstian", "Ludfordian Age": "Ludfordian", "Pridoli Epoch": "Pridoli",
                 "Devonian Period": "Lochkovian", "Early Devonian Epoch": "Lochkovian", "Lochkovian Age": "Lochkovian", "Pragian Age": "Pragian",
                 "Emsian Age": "Emsian", "Mid Devonian Epoch": "Eifelian", "Eifelian Age": "Eifelian", "Givetian Age": "Givetian",
                 "Late Devonian Epoch": "Frasnian", "Frasnian Age": "Frasnian", "Famennian Age": "Famennian",
                 "Carboniferous Period": "Tournaisian", "Ordovician Period": "Tremadocian"}
NI_LON, NI_LAT_MAX, NI_LAT_MIN = -5.43, 55.30, 53.9   # centroid rule for Northern Ireland (inference): west of 5.43 W, between 53.9 and 55.3 N


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def rd(p):
    return list(csv.DictReader(open(p, newline="", encoding="utf-8")))


poly = rd(DER + "bedrock_polygons.csv")
lex = {r["code"]: r for r in rd(DER + "lexicon_entries.csv")}
div = {r["code"]: r for r in rd(DER + "lexicon_divisions.csv")}


def is_sd(r):
    a, b = r["MAX_TIME_Y"], r["MIN_TIME_Y"]
    return bool(a) and bool(b) and int(a) > SD_TOP_Y and int(b) < SD_BASE_Y


# ---- BGS's own scale, read from the polygon terms ----
base_of, top_of = collections.defaultdict(set), collections.defaultdict(set)
count_of = collections.Counter()
for r in poly:
    if r["MAX_TIME_Y"]:
        base_of[r["MAX_TIME_D"]].add(int(r["MAX_TIME_Y"]))
        count_of[("max", r["MAX_TIME_D"])] += 1
    if r["MIN_TIME_Y"]:
        top_of[r["MIN_TIME_D"]].add(int(r["MIN_TIME_Y"]))
        count_of[("min", r["MIN_TIME_D"])] += 1
for t in set(base_of) | set(top_of):
    assert len(base_of[t]) <= 1 and len(top_of[t]) <= 1 or t in ("",), ("term with several year values", t, base_of[t], top_of[t])

SERIES = ["LLANDOVERY", "WENLOCK", "LUDLOW", "PRIDOLI", "EARLY DEVONIAN", "MID DEVONIAN", "LATE DEVONIAN"]
PERIODS = ["SILURIAN", "DEVONIAN"]
STAGES = ["RHUDDANIAN", "TELYCHIAN", "LOCHKOVIAN", "PRAGHIAN", "EMSIAN", "FAMENNIAN"]
SERIES_PERIOD = {"LLANDOVERY": "SILURIAN", "WENLOCK": "SILURIAN", "LUDLOW": "SILURIAN", "PRIDOLI": "SILURIAN",
                 "EARLY DEVONIAN": "DEVONIAN", "MID DEVONIAN": "DEVONIAN", "LATE DEVONIAN": "DEVONIAN"}
STAGE_SERIES = {"RHUDDANIAN": "LLANDOVERY", "TELYCHIAN": "LLANDOVERY", "LOCHKOVIAN": "EARLY DEVONIAN", "PRAGHIAN": "EARLY DEVONIAN",
                "EMSIAN": "EARLY DEVONIAN", "FAMENNIAN": "LATE DEVONIAN"}
BINS = {}      # term -> (base_y, top_y), None where BGS gives only one side
for t in PERIODS + SERIES + STAGES:
    b = next(iter(base_of[t])) if base_of.get(t) else None
    tp = next(iter(top_of[t])) if top_of.get(t) else None
    BINS[t] = (b, tp)
log("BGS term bounds read from polygon fields (base_y, top_y):", BINS)
with open(OUT + "bgs_polygon_age_scale_observed.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["bgs_term", "bgs_rank_label", "base_year_as_MAX_TIME_Y", "n_polygons_as_max", "top_year_as_MIN_TIME_Y", "n_polygons_as_min",
                "derived_project_base_ma", "derived_base_diff_bgs_minus_project_ma", "derived_project_top_ma", "derived_top_diff_bgs_minus_project_ma"])
    for t in PERIODS + SERIES + STAGES:
        lab = "period" if t in PERIODS else ("series_epoch" if t in SERIES else "stage_age")
        b, tp = BINS[t]
        pb, pt = TERM_TO_PROJ[t]
        row = [t, lab, "" if b is None else b, count_of[("max", t)], "" if tp is None else tp, count_of[("min", t)],
               PROJ[pb], "" if b is None else f"{b / 1e6 - PROJ[pb]:.2f}", PROJ[pt], "" if tp is None else f"{tp / 1e6 - PROJ[pt]:.2f}"]
        w.writerow(row)

# ---- rock group, region, ORS ----
METAMORPHIC = {"HBSCH", "SCHM", "GPSP", "PEL"}
EXTRUSIVE = {"LATM", "LATF", "MFLAVA", "MFTUF", "PYRR"}
INTRUSIVE = {"FELSR", "MFIR", "UMFT", "SYR"}
SEDIMENTARY = {"SCSM", "MDCB", "COSD", "LMCM", "SCON", "SMSC", "WACKE", "MDSS", "CSSM", "BRCMBR", "SCGS"}


def rock_group(rcs):
    if rcs in METAMORPHIC:
        return "metamorphic"
    if rcs in EXTRUSIVE:
        return "igneous_extrusive"
    if rcs in INTRUSIVE:
        return "igneous_intrusive"
    if rcs in SEDIMENTARY:
        return "sedimentary"
    raise ValueError("unmapped RCS " + rcs)


def lex_ancestors(code):
    out, seen, x = [], set(), code
    while x in lex and x not in seen:
        seen.add(x)
        b = [y for y in lex[x].get("broader", "").split(";") if y]
        if not b:
            break
        out.append(b[0])
        x = b[0]
    return out


ORS_LEX = {c for c in lex if c == "ORS" or "ORS" in lex_ancestors(c)}


def ors_evidence(r):
    ev = []
    if "OLD RED SANDSTONE" in r["LEX_D"]:
        ev.append("625k_name")
    if r["SUPGP_EQ"] == "ORS":
        ev.append("625k_supergroup_ORS")
    if "OLD RED SANDSTONE" in r["PREV_NAME"]:
        ev.append("625k_previous_name")
    if r["LEX"] in ORS_LEX:
        ev.append("lexicon_ORS_or_descendant")
    return ";".join(ev)


ENV = [
    ("non-marine", r"\bnon-?marine\b|\bterrestrial\b|\bcontinental\b"),
    ("fluvial_alluvial", r"\bfluvial\b|\balluvial\b|\briver\b|\bstream\b|\bbraided\b|\bmeander|\bfloodplain\b|\bred beds\b"),
    ("lacustrine", r"\blacustrine\b|\blake\b|\blakes\b"),
    ("aeolian", r"\baeolian\b|\beolian\b|\bdune"),
    ("coastal_deltaic_estuarine_tidal", r"\bdelta|\bestuar|\bcoastal\b|\btidal\b|\bbeach\b|\bshoreface\b|\bintertidal\b|\blagoon"),
    ("shallow_marine_shelf", r"\bshallow[- ]marine\b|\bshelf\b|\bnearshore\b|\breef|\bplatform\b|\bshoal"),
    ("deep_marine_basinal", r"\bdeep[- ]water\b|\bdeep[- ]marine\b|\bturbidit|\bbathyal\b|\bbasinal\b|\bhemipelagic\b|\bpelagic\b|\bflysch\b|\bbouma\b|\bsubmarine fan\b|\bslope\b"),
    ("marine_unspecified", r"(?<!non-)(?<!non )\bmarine\b"),
    ("volcanic", r"\bvolcan|\blava\b|\bignimbrite|\brhyolit|\bbasalt|\bandesit|\btuff|\bpyroclast"),
    ("intrusive", r"\bgranit|\bgranodiorit|\btonalit|\bintrusi|\bpluton|\bdolerite\b|\bgabbro|\bdiorite\b|\bsyenit"),
    ("calcrete_palaeosol", r"\bcalcrete\b|\bpalaeosol|\bcornstone\b"),
]
ENV = [(k, re.compile(v, re.I)) for k, v in ENV]


def env_keywords(text):
    return ";".join(k for k, rx in ENV if rx.search(text))


# ---- polygon level ----
SD = [r for r in poly if is_sd(r)]
rows_out = []
for r in SD:
    mx, mn = int(r["MAX_TIME_Y"]), int(r["MIN_TIME_Y"])
    lon, lat = float(r["centroid_lon"]), float(r["centroid_lat"])
    region = "northern_ireland" if (lon < NI_LON and NI_LAT_MIN < lat < NI_LAT_MAX) else "great_britain_and_isle_of_man"
    shares = {}
    for t in SERIES + PERIODS:
        b, tp = BINS[t]
        ov = max(0, min(mx, b) - max(mn, tp))
        span = mx - mn
        shares[t] = (ov / span) if span > 0 else (1.0 if (mx <= b and mn >= tp and mx > tp) else 0.0)
        shares[t + "|excl"] = 1 if (mx <= b and mn >= tp) else 0
    rows_out.append(dict(r, region=region, rock_group=rock_group(r["RCS"]), ors=ors_evidence(r), shares=shares,
                         area_km2=float(r["area_m2"]) / 1e6, mx=mx, mn=mn))
log("S-D polygons", len(rows_out), "NI", sum(1 for r in rows_out if r["region"] == "northern_ireland"))

# ---- outcrop area table ----
REGIONS = ["all_uk", "great_britain_and_isle_of_man", "northern_ireland"]
GROUPS = ["all", "sedimentary", "igneous_extrusive", "igneous_intrusive", "metamorphic"]
SUBSETS = ["all", "ors_flagged"]


def selected(r, region, group, subset):
    return ((region == "all_uk" or r["region"] == region) and (group == "all" or r["rock_group"] == group)
            and (subset == "all" or r["ors"]))


area_rows = []
hdr = ["level", "bgs_term", "bgs_base_year", "bgs_top_year", "region", "rock_group", "subset", "n_polygons_overlap",
       "area_km2_overlap_any", "n_polygons_exclusive", "area_km2_exclusive", "area_km2_apportioned_by_bgs_years",
       "n_polygons_labelled_at_stage", "area_km2_labelled_at_stage", "area_km2_labelled_both_ends_same_stage"]
for level, terms in (("period", PERIODS), ("series", SERIES), ("stage", STAGES)):
    for t in terms:
        b, tp = BINS[t]
        for region in REGIONS:
            for group in GROUPS:
                for subset in SUBSETS:
                    P = [r for r in rows_out if selected(r, region, group, subset)]
                    if level in ("period", "series"):
                        ov = [r for r in P if r["shares"][t] > 0]
                        ex = [r for r in P if r["shares"][t + "|excl"]]
                        if not ov:
                            continue
                        area_rows.append([level, t, b, tp, region, group, subset, len(ov), f"{sum(r['area_km2'] for r in ov):.3f}",
                                          len(ex), f"{sum(r['area_km2'] for r in ex):.3f}",
                                          f"{sum(r['area_km2'] * r['shares'][t] for r in P):.3f}", "", "", ""])
                    else:
                        lab = [r for r in P if r["MAX_TIME_D"] == t or r["MIN_TIME_D"] == t]
                        both = [r for r in P if r["MAX_TIME_D"] == t and r["MIN_TIME_D"] == t]
                        if not lab:
                            continue
                        area_rows.append([level, t, "" if b is None else b, "" if tp is None else tp, region, group, subset, "", "",
                                          "", "", "", len(lab), f"{sum(r['area_km2'] for r in lab):.3f}",
                                          f"{sum(r['area_km2'] for r in both):.3f}"])
with open(OUT + "bgs_outcrop_area_by_age.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(hdr)
    w.writerows(area_rows)
log("outcrop area rows", len(area_rows))

# ---- units table ----
by_lex = collections.defaultdict(list)
for r in rows_out:
    by_lex[r["LEX"]].append(r)


def uniq(rs, k, sep=";"):
    return sep.join(sorted({x[k] for x in rs if x[k]}))


UCOLS = ["lex_code", "digmap625_lex_name", "derived_row_role", "digmap625_n_polygons_sd", "derived_area_km2_sd_polygons",
         "derived_area_km2_great_britain_and_isle_of_man", "derived_area_km2_northern_ireland",
         "derived_area_km2_by_rock_group", "digmap625_rank", "digmap625_rock_class_codes", "digmap625_rock_class_descriptions",
         "digmap625_hierarchy_eq", "digmap625_previous_names", "digmap625_map_codes", "digmap625_age_onegl",
         "digmap625_max_time_d", "digmap625_min_time_d", "digmap625_max_time_y", "digmap625_min_time_y",
         "digmap625_max_period", "digmap625_min_period", "digmap625_max_epoch", "digmap625_min_epoch", "digmap625_max_age",
         "digmap625_min_age", "derived_ors", "derived_ors_evidence",
         "lexicon_found", "lexicon_label", "lexicon_status", "lexicon_rank", "lexicon_parent_codes", "lexicon_web_parent_unit",
         "lexicon_oldest_age_division", "lexicon_oldest_age_ma", "lexicon_youngest_age_division", "lexicon_youngest_age_ma",
         "lexicon_age_range_text", "lexicon_definition", "lexicon_lithology_classes", "lexicon_references_count",
         "lexicon_references", "lexicon_source_info_ids", "derived_lexicon_obsolete", "derived_environment_keywords",
         "derived_oldest_age_lexicon_minus_polygon_ma", "derived_youngest_age_lexicon_minus_polygon_ma"]
units = []
codes = sorted(by_lex)
extra = sorted(c for c in lex if c not in by_lex and (c in ORS_LEX or c in {a for k in by_lex for a in lex_ancestors(k)}))
for c in codes + extra:
    rs = by_lex.get(c, [])
    L = lex.get(c, {})
    role = ("in_sd_polygons" if rs else ("ors_lexicon_descendant_not_in_sd_polygons" if c in ORS_LEX else "ancestor_of_sd_code"))
    area = sum(r["area_km2"] for r in rs)
    gb = sum(r["area_km2"] for r in rs if r["region"] == "great_britain_and_isle_of_man")
    ni = area - gb
    rg = collections.defaultdict(float)
    for r in rs:
        rg[r["rock_group"]] += r["area_km2"]
    hier = sorted({"/".join(r[k] for k in ("BED_EQ", "MB_EQ", "FM_EQ", "SUBGP_EQ", "GP_EQ", "SUPGP_EQ")) for r in rs})
    text = " ".join([L.get("lithology_description", ""), L.get("definition", ""), L.get("web_lithological_description", "")])
    omx = min([r["mx"] for r in rs], default=None)
    pmx = max([r["mx"] for r in rs], default=None)
    pmn = min([r["mn"] for r in rs], default=None)
    lo = L.get("oldest_ma", "")
    ly = L.get("youngest_ma", "")
    diff_o = f"{float(lo) - pmx / 1e6:.2f}" if (lo and pmx is not None and ";" not in lo) else ""
    diff_y = f"{float(ly) - pmn / 1e6:.2f}" if (ly and pmn is not None and ";" not in ly) else ""
    obs = "yes" if (L.get("status") == "deprecated" or "[Obsolete" in L.get("pref_label", "")) else ("no" if L else "")
    units.append(dict(
        lex_code=c, digmap625_lex_name=uniq(rs, "LEX_D") if rs else "", derived_row_role=role,
        digmap625_n_polygons_sd=len(rs) if rs else "", derived_area_km2_sd_polygons=f"{area:.3f}" if rs else "",
        derived_area_km2_great_britain_and_isle_of_man=f"{gb:.3f}" if rs else "",
        derived_area_km2_northern_ireland=f"{ni:.3f}" if rs else "",
        derived_area_km2_by_rock_group=";".join(f"{k}={v:.1f}" for k, v in sorted(rg.items())) if rs else "",
        digmap625_rank=uniq(rs, "RANK"), digmap625_rock_class_codes=uniq(rs, "RCS"), digmap625_rock_class_descriptions=uniq(rs, "RCS_D", " | "),
        digmap625_hierarchy_eq=" | ".join(hier) if rs else "", digmap625_previous_names=uniq(rs, "PREV_NAME", " | "),
        digmap625_map_codes=uniq(rs, "MAP_CODE"), digmap625_age_onegl=uniq(rs, "AGE_ONEGL"),
        digmap625_max_time_d=uniq(rs, "MAX_TIME_D"), digmap625_min_time_d=uniq(rs, "MIN_TIME_D"),
        digmap625_max_time_y=";".join(str(x) for x in sorted({r["mx"] for r in rs})),
        digmap625_min_time_y=";".join(str(x) for x in sorted({r["mn"] for r in rs})),
        digmap625_max_period=uniq(rs, "MAX_PERIOD"), digmap625_min_period=uniq(rs, "MIN_PERIOD"),
        digmap625_max_epoch=uniq(rs, "MAX_EPOCH"), digmap625_min_epoch=uniq(rs, "MIN_EPOCH"),
        digmap625_max_age=uniq(rs, "MAX_AGE"), digmap625_min_age=uniq(rs, "MIN_AGE"),
        derived_ors="yes" if (c in ORS_LEX or any(r["ors"] for r in rs)) else "no",
        derived_ors_evidence=";".join(sorted({e for r in rs for e in r["ors"].split(";") if e} | ({"lexicon_ORS_or_descendant"} if c in ORS_LEX else set()))),
        lexicon_found="yes" if L.get("in_lod") == "yes" else "no", lexicon_label=L.get("pref_label", ""), lexicon_status=L.get("status", ""),
        lexicon_rank=L.get("rank", ""), lexicon_parent_codes=L.get("broader", ""), lexicon_web_parent_unit=L.get("web_parent_unit", ""),
        lexicon_oldest_age_division=L.get("oldest_div", ""), lexicon_oldest_age_ma=lo, lexicon_youngest_age_division=L.get("youngest_div", ""),
        lexicon_youngest_age_ma=ly, lexicon_age_range_text=L.get("web_age_range", ""), lexicon_definition=L.get("definition", ""),
        lexicon_lithology_classes=L.get("lithology_classes", ""), lexicon_references_count=L.get("web_n_references", ""),
        lexicon_references=L.get("web_references", ""), lexicon_source_info_ids=L.get("source_info_ids", ""),
        derived_lexicon_obsolete=obs, derived_environment_keywords=env_keywords(text) if L else "",
        derived_oldest_age_lexicon_minus_polygon_ma=diff_o, derived_youngest_age_lexicon_minus_polygon_ma=diff_y))
with open(OUT + "bgs_units_silurian_devonian.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, UCOLS, lineterminator="\n")
    w.writeheader()
    w.writerows(units)
log("units", len(units), dict(collections.Counter(u["derived_row_role"] for u in units)))

# ---- divisions used ----
used = set()
for c, L in lex.items():
    for k in ("oldest_div", "youngest_div", "predominant_div", "broader_predominant_div"):
        for x in L.get(k, "").split(";"):
            if x:
                used.add(x)
with open(OUT + "bgs_geochronology_divisions_used.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["division_code", "label", "rank", "max_age_ma", "min_age_ma", "broader", "used_by_lexicon_entries_fetched",
                "derived_project_stage_with_same_base", "derived_project_base_ma", "derived_max_age_diff_bgs_minus_project_ma"])
    for d in sorted(div):
        r = div[d]
        ps = LABEL_TO_PROJ.get(r.get("pref_label", ""), "")
        mx = r.get("max_age_ma", "")
        w.writerow([d, r.get("pref_label", ""), r.get("rank", ""), mx, r.get("min_age_ma", ""),
                    r.get("broader", ""), "yes" if d in used else "no (ancestor)", ps, PROJ.get(ps, ""),
                    f"{float(mx) - PROJ[ps]:.2f}" if (ps and mx) else ""])

# ---- local tables ----
shutil.copy(DER + "lexicon_entries.csv", OUT + "bgs_lexicon_entries_sd.csv")
PCOLS = list(SD[0].keys())
with open(OUT + "bgs_polygons_silurian_devonian.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    extra_cols = ["derived_region", "derived_rock_group", "derived_ors_evidence", "derived_area_km2"] + ["derived_share_" + t.lower().replace(" ", "_") for t in SERIES + PERIODS]
    w.writerow(PCOLS + extra_cols)
    for r in rows_out:
        w.writerow([r[k] for k in PCOLS] + [r["region"], r["rock_group"], r["ors"], f"{r['area_km2']:.6f}"] +
                   [f"{r['shares'][t]:.4f}" for t in SERIES + PERIODS])
log("done", OUT)
