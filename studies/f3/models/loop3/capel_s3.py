# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "openpyxl", "scipy"]
# ///
"""S3: crown vascular-plant records from Capel, Monnet and Cascales-Minana (2025) Table S1, under the
rules frozen in studies/f3/docs/audits/2026-11-21-inventory-symmetry-s3-rules.md (Task 1B).

Writes the row-level mapping (crown assignment, ages, locality key, region), the age and region maps, and
the row-level check of the cases disputed in review (S3-A10 to S3-A16). It computes no share: S3 counts
wait for the second agent's sign-off.

    uv run studies/f3/models/loop3/capel_s3.py
"""

import hashlib
import re
import unicodedata
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

from histories import DOMAIN, stage_bounds

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "out"
XLSX = ROOT / "data/external/local/deposits/capel2025-global-plant-diversity/Table_S1_revised_Hist_Biol.xlsx"
SHA256 = "d310a56da8139373a02015b2963da0d6b28a122884e1a82a031a4e21f18f1471"
YOUNG, LOCHKOVIAN_BASE = 393.47, 419.62

B2_GROUPS = {"Lycopsida", "Zosterophyllopsida", "Barinophytopsida", "Basal euphyllophytes", "Euphyllophyta inc. sed.",
             "Cladoxylopsida", "Filicopsida", "Sphenopsida", "Progymnospermopsida", "Stenokoleales", "Spermatophyta"}
NOT_B2 = {"Rhyniophytoids", "Eophyta", "Paratracheophyta", "Horneophytopsida", "Protracheophyta"}
UNRESOLVED = {"Basal eutracheophytes", "Incertae sedis"}
SERIES = {"ludlow": ("gorstian", "ludfordian"), "early devonian": ("lochkovian", "emsian"),
          "middle devonian": ("eifelian", "givetian"), "late devonian": ("frasnian", "famennian")}
ALIASES = {"campbellton fm, altholville, new brunswick, canada": "campbellton fm, atholville, new brunswick, canada"}
SPELLING = {"gordstian": "gorstian", "fammenian": "famennian"}
FIRST_ROW, LAST_ROW = 4, 1200
# S3-A11: Yea-area rows mapped to F3's documented horizons (data/occurrences/observations.csv). Each takes the
# F3 main-reading envelope of its horizon (interpretations.csv); literal Capel ages stay in literal_*.
YEA_HORIZON = {
    124: ("M-yea-unspecified", "gorstian", "emsian",
          "Upper Yea Fm., Yea; Garratt & Rickards 1984 is F3's source for the unspecified Yea Baragwanathia"),
    734: ("M-ghin-ghin", "gorstian", "emsian", "Parazosterophyllum timsiae and McSweeney et al. 2020 listed at Loc. 1"),
    1199: ("M-ghin-ghin", "gorstian", "emsian", "Ghin Ghin Road, bed not stated; F3 attaches McSweeney et al. 2022 "
           "to Loc. 1; the alternative, B2 (Pridoli-Emsian), would add one unit to Yea-inclusive locality counts"),
    904: ("ghin-ghin-road-unidentified", "gorstian", "emsian", "Ghin Ghin Road, bed not stated (Loc. 1 or B2); not crown"),
    906: ("M-limestone-road", "gorstian", "emsian", "Loc. 4, Limestone Road; not crown"),
    1146: ("M-limestone-road", "gorstian", "emsian", "Loc. 4, Limestone Road; not crown"),
}
# S3-A12: rows whose material F3 reads specifically, overriding the genus rule in the F3-aligned reading.
MATERIAL = {6: ("not_B2", "Aberlemnia cf. caledonica, Negra Muerta: F3's Negra Muerta cf. caledonica "
                "(tail:M-bolivia-caledonica) is B1 in main, B2 in inclusive; specimen identity open")}
QUALIFIERS = r"^(mid- to late |early to mid-|early |middle |mid- |mid |late )\s*"
REGION = {
    "USA": "Laurentia", "New York": "Laurentia", "Canada": "Laurentia", "North Greenland": "Laurentia",
    "Norway": "Baltica", "Western Norway": "Baltica", "Scotland": "Laurentia", "England": "Avalonia",
    "Ireland": "Avalonia", "Belgium": "Avalonia", "France": "peri-Gondwana-Europe", "Spain": "peri-Gondwana-Europe",
    "Czech Republic": "peri-Gondwana-Europe", "Germany": "multiple", "Poland": "multiple", "Russia": "multiple",
    "Russian Federation": "multiple", "Ukraine": "Baltica", "Kazakhstan": "Kazakhstania",
    "Central Kazakhstan": "Kazakhstania", "Southern Kazakhstan": "Kazakhstania", "Vietnam": "South-China",
    "Australia": "Gondwana-Australia-Antarctica", "Victoria": "Gondwana-Australia-Antarctica",
    "Antarctica": "Gondwana-Australia-Antarctica", "West Antarctica": "Gondwana-Australia-Antarctica",
    "Morocco": "Gondwana-North-Africa-Arabia", "Niger": "Gondwana-North-Africa-Arabia",
    "Chad": "Gondwana-North-Africa-Arabia", "Northeast Chad": "Gondwana-North-Africa-Arabia",
    "Egypt": "Gondwana-North-Africa-Arabia", "Argentina": "Gondwana-South-America", "Bolivia": "Gondwana-South-America",
    "Brasil": "Gondwana-South-America", "Brazil": "Gondwana-South-America", "Colombia": "Gondwana-South-America",
    "Chile": "Gondwana-South-America", "Venezuela": "Gondwana-South-America", "South Africa": "Gondwana-other",
    "India": "Gondwana-other", "Falkland Islands": "Gondwana-other", "": "unknown",
}
NORTH_CHINA = {"Inner Mongolia", "Hebei", "Shanxi", "Shandong", "Liaoning", "Ningxia", "Henan", "Beijing", "Tianjin", "Jilin"}
SOUTH_CHINA = {"Yunnan", "Guizhou", "Sichuan", "Chongqing", "Hunan", "Hubei", "Guangxi", "Jiangxi", "Zhejiang", "Anhui",
               "Jiangsu", "Guangdong", "Fujian"}


def stages():
    t = pd.read_csv(ROOT / "data/timescale.csv")
    t = t.sort_values("base_ma").reset_index(drop=True)
    t["top_ma"] = t.base_ma.shift(1)
    return {s.lower(): (b, top) for s, b, top in zip(t.stage, t.base_ma, t.top_ma)}


def age(text, st):
    """(max_ma, min_ma, status) for one Temporal distribution string."""
    s = re.sub(r"\s+", " ", str(text) if isinstance(text, str) else "").strip().rstrip("*").strip()
    if not s:
        return np.nan, np.nan, "unmapped"
    s = s.lower()
    if s in SERIES:
        old, young = SERIES[s]
    elif "post-" in s:
        return np.nan, np.nan, "outside_window"
    else:
        parts = [re.sub(QUALIFIERS, "", p.strip()) for p in re.split(r"(?<!mid)-(?! to)", s)]
        parts = [SPELLING.get(p, p) for p in parts]
        if len(parts) == 1:
            old = young = parts[0]
        elif len(parts) == 2:
            old, young = parts
        else:
            raise ValueError(f"unparsed age string: {text!r}")
        old, young = SERIES.get(old, (old, old))[0], SERIES.get(young, (young, young))[1]
    if old not in st or young not in st:
        raise ValueError(f"unmapped stage in {text!r}: {old}, {young}")
    hi, lo = st[old][0], st[young][1]
    if lo is None or np.isnan(lo):
        lo = st[young][0]
    status = "in_window" if hi > YOUNG else "outside_window"
    return hi, lo, status


def locality_key(text):
    s = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode().casefold()
    s = re.sub(r"\bformation\b", "fm", s)
    s = re.sub(r"[^a-z0-9, ]", " ", s)
    return re.sub(r"\s+", " ", s).replace(" ,", ",").strip()


def region(text):
    s = str(text) if isinstance(text, str) else ""
    last = s.split(",")[-1].strip()
    if last == "UK":
        if "Scotland" in s:
            return "Laurentia"
        if re.search(r"England|Wales|Shropshire|Hereford|Worcestershire|Gloucestershire|Devon|Cornwall|Somerset", s):
            return "Avalonia"
        return "multiple"
    if last in ("Norway", "Western Norway") and re.search(r"Spitsbergen|Svalbard", s):
        return "Laurentia"
    if last == "China":
        if "Xinjiang" in s:
            return "Kazakhstania" if re.search(r"Junggar|Hoboksar|Xiemisitai|Wutubulake", s) else "Tarim"
        if any(p in s for p in NORTH_CHINA):
            return "North-China"
        if any(p in s for p in SOUTH_CHINA):
            return "South-China"
        return "multiple"
    if last not in REGION:
        raise ValueError(f"unmapped country field {last!r} in {s!r}")
    return REGION[last]


def genus(name):
    s = re.sub(r"^(cf\.|aff\.|\?|\")\s*", "", str(name).strip())
    s = re.sub(r"^(cf\.|aff\.|\?|\")\s*", "", s)
    return s.split()[0].strip('?"<>') if s.split() else ""


def midpoint_stage(mid):
    """Stage base (Ma) of the stage holding each midpoint: stage_bounds inside the F3 domain, the full ICS
    table below 393.47 Ma (S3-A14)."""
    mid = np.minimum(DOMAIN, np.asarray(mid, dtype=float))
    out = np.empty(len(mid))
    inside = mid >= YOUNG
    if inside.any():
        out[inside] = stage_bounds(mid[inside])[1]
    t = pd.read_csv(ROOT / "data/timescale.csv").sort_values("base_ma")
    bases = t.base_ma.values
    for i in np.flatnonzero(~inside):
        out[i] = bases[np.searchsorted(bases, mid[i], side="left")]
    return out


def crown_lookup():
    nc = pd.read_csv(ROOT / "studies/f3/data/macro/name_classifications.csv")
    nc["genus"] = nc.name.map(lambda n: genus(str(n).strip("<>\"")))
    return nc.groupby("genus").crown_tracheophyte.agg(lambda v: set(v))


def parse():
    assert hashlib.sha256(XLSX.read_bytes()).hexdigest() == SHA256
    ws = openpyxl.load_workbook(XLSX).worksheets[0]
    grid = {(r, c): ws.cell(r, c).value for r in range(FIRST_ROW, LAST_ROW + 1) for c in range(1, 6)}
    for m in ws.merged_cells.ranges:
        if m.min_col == m.max_col == 5 and m.min_row >= FIRST_ROW and m.max_row <= LAST_ROW:
            for r in range(m.min_row + 1, m.max_row + 1):
                grid[r, 5] = grid[m.min_row, 5]
    foot = ws.cell(LAST_ROW + 1, 1).value
    assert str(foot).startswith('*"Post-Tournaisian"') and all(ws.cell(LAST_ROW + 1, c).value is None for c in range(2, 6))
    d = pd.DataFrame([[grid[r, c] for c in range(1, 6)] for r in range(FIRST_ROW, LAST_ROW + 1)],
                     columns=["species", "group", "time", "locality", "reference"])
    d["capel_row"] = range(FIRST_ROW, LAST_ROW + 1)
    d = d.set_index(d.capel_row.values)
    assert d.time.notna().all() and d.locality.notna().all()
    d["continuation"] = d.species.isna()
    d["species"], d["group"] = d.species.ffill(), d.group.ffill()
    rows_per_species = d.groupby(d.continuation.eq(False).cumsum()).size().value_counts().to_dict()
    st = stages()
    ages = [age(t, st) for t in d.time]
    d["max_ma"], d["min_ma"], d["age_status"] = zip(*ages)
    crown = crown_lookup()
    d["genus"] = d.species.map(genus)
    f3 = d.genus.map(lambda g: crown.get(g, set()))
    d["f3_crown"] = f3.map(lambda v: next(iter(v)) if len(v) == 1 else ("mixed" if v else "absent"))
    d["capel_class"] = d.group.map(lambda g: "B2" if g in B2_GROUPS else ("not_B2" if g in NOT_B2 else
                                                                          ("unresolved" if g in UNRESOLVED else "unknown")))
    assert not d.capel_class.eq("unknown").any(), d.loc[d.capel_class.eq("unknown"), "group"].unique()
    d["b2_rule"] = np.where(d.f3_crown.isin(["yes", "no"]), "f3_genus", "capel_group")
    d["b2"] = np.where(d.f3_crown.eq("yes"), "B2", np.where(d.f3_crown.eq("no"), "not_B2", d.capel_class))
    d["b2_genus_rule"] = d.b2
    d["material_note"] = ""
    for row, (cls, note) in MATERIAL.items():
        d.loc[row, ["b2", "b2_rule", "material_note"]] = cls, "f3_material", note
    d["conflict"] = d.f3_crown.isin(["yes", "no"]) & d.capel_class.isin(["B2", "not_B2"]) & (
        d.f3_crown.eq("yes") != d.capel_class.eq("B2"))
    d["locality_key"] = d.locality.map(locality_key).replace(ALIASES)
    d["region"] = d.locality.map(region)
    loc = d.locality.fillna("")
    flagged = loc.str.contains(r"\bYea\b|Ghin Ghin|Limestone Road") & ~loc.str.contains("Norton Gully")
    assert set(d.index[flagged]) == set(YEA_HORIZON), sorted(set(d.index[flagged]) ^ set(YEA_HORIZON))
    d["literal_max_ma"], d["literal_min_ma"] = d.max_ma, d.min_ma
    d["yea"], d["yea_horizon"], d["yea_note"] = False, "", ""
    for row, (hz, old, young, note) in YEA_HORIZON.items():
        d.loc[row, ["yea", "yea_horizon", "yea_note", "max_ma", "min_ma", "locality_key"]] = (
            True, hz, note, st[old][0], st[young][1], "yea:" + hz)
    d["yea"] = d.yea.astype(bool)
    return d, rows_per_species


VARIANTS = ("main", "f3_strict", "permissive", "capel_groups", "yea_literal")


def units(d, variant="main", counting="locality_age", exclude_rows=()):
    """S3 units. main: F3 genus rule with F3 material readings (S3-A12); permissive: genus rule only;
    f3_strict: main without rows whose F3 genus reading is uncertain or mixed (S3-A12); capel_groups: Capel's
    groups alone (S3-A7); yea_literal: main with Capel's literal Yea ages and keys. exclude_rows drops Capel
    rows before aggregation (Task 6). Same aggregation as select_records."""
    col = {"main": "b2", "f3_strict": "b2", "yea_literal": "b2", "permissive": "b2_genus_rule",
           "capel_groups": "capel_class"}[variant]
    keep = d[col].eq("B2") & ~d.capel_row.isin(exclude_rows)
    if variant == "f3_strict":
        keep &= ~d.f3_crown.isin(["uncertain", "mixed"])
    r = d[keep].copy()
    if variant == "yea_literal":
        r["max_ma"], r["min_ma"] = r.literal_max_ma, r.literal_min_ma
        r.loc[r.yea, "locality_key"] = r.locality[r.yea].map(locality_key)
    r = r[r.max_ma > YOUNG]
    if counting == "locality_age":
        r["unit_id"] = r.locality_key + "|" + r.min_ma.astype(str) + "|" + r.max_ma.astype(str)
    elif counting == "region_stage":
        old = midpoint_stage((r.min_ma.values + r.max_ma.values) / 2)
        r["unit_id"] = r.region + "|midpoint-stage:" + pd.Series(old, index=r.index).astype(str)
    return r.groupby("unit_id", as_index=False).agg(
        min_ma=("min_ma", "max"), max_ma=("max_ma", "max"), region=("region", "first"),
        member_ids=("capel_row", lambda x: ";".join(map(str, sorted(x)))), n_members=("capel_row", "size"))


DISPUTED = (6, 8, 124, 128, 297, 477, 530, 734, 904, 906, 1130, 1146, 1191, 1199, 47, 158, 556)


def main():
    d, per_species = parse()
    print("rows per species:", per_species)
    assert per_species == {1: 809, 2: 194} and len(d) == 1197, per_species
    for v in VARIANTS:
        for c in ("locality_age", "region_stage"):
            units(d, v, c)
    cols = ["capel_row", "continuation", "species", "genus", "group", "time", "max_ma", "min_ma", "literal_max_ma",
            "literal_min_ma", "age_status", "f3_crown", "capel_class", "b2_rule", "b2_genus_rule", "b2", "conflict",
            "material_note", "locality", "locality_key", "region", "yea", "yea_horizon", "yea_note", "reference"]
    d[cols].to_csv(OUT / "capel_s3_rows.csv", index=False, lineterminator="\n")
    chk = d.loc[list(DISPUTED), cols].copy()
    chk["midpoint_stage_base_ma"] = midpoint_stage(((chk.min_ma + chk.max_ma) / 2).values)
    chk["window_status"] = np.where(chk.max_ma <= YOUNG, "outside",
                                    np.where(chk.min_ma >= YOUNG, "guaranteed", "possible_only"))
    chk["counted_in"] = [";".join(v for v in VARIANTS if not units(d.loc[[i]], v).empty) for i in chk.index]
    chk.to_csv(OUT / "capel_s3_disputed_rows.csv", index=False, lineterminator="\n")
    timemap = d.groupby(d.time.str.strip()).agg(max_ma=("literal_max_ma", "first"), min_ma=("literal_min_ma", "first"),
                                                 status=("age_status", "first"), rows=("capel_row", "size"))
    timemap.to_csv(OUT / "capel_s3_age_map.csv", lineterminator="\n")
    country = d.assign(field=d.locality.str.split(",").str[-1].str.strip()).groupby(["field", "region"]).size()
    country.rename("rows").to_csv(OUT / "capel_s3_region_map.csv", lineterminator="\n")
    print(d.b2.value_counts().to_string())
    print("f3_crown:", d.f3_crown.value_counts().to_dict(), "| conflicts:", int(d.conflict.sum()),
          "| age status:", d.age_status.value_counts().to_dict(), "| Yea rows:", int(d.yea.sum()))


if __name__ == "__main__":
    main()
