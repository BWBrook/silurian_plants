# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "openpyxl", "scipy"]
# ///
"""S3: crown vascular-plant records from Capel, Monnet and Cascales-Minana (2025) Table S1, under the
rules frozen in studies/f3/docs/audits/2026-11-21-inventory-symmetry-s3-rules.md (Task 1B).

Writes the row-level mapping (crown assignment, ages, locality key, region) and the S0-S3 crosswalk of
units reaching above 419.62 Ma. It computes no share: S3 counts wait for the second agent's sign-off.

    uv run studies/f3/models/loop3/capel_s3.py
"""

import difflib
import hashlib
import re
import unicodedata
from pathlib import Path

import numpy as np
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


def crown_lookup():
    nc = pd.read_csv(ROOT / "studies/f3/data/macro/name_classifications.csv")
    nc["genus"] = nc.name.map(lambda n: genus(str(n).strip("<>\"")))
    return nc.groupby("genus").crown_tracheophyte.agg(lambda v: set(v))


def parse():
    assert hashlib.sha256(XLSX.read_bytes()).hexdigest() == SHA256
    raw = pd.read_excel(XLSX, header=None)
    d = raw.iloc[3:].copy()
    d.columns = ["species", "group", "time", "locality", "reference"]
    d["capel_row"] = d.index + 1
    d["continuation"] = d.species.isna()
    d["species"], d["group"] = d.species.ffill(), d.group.ffill()
    rows_per_species = d.groupby(d.continuation.eq(False).cumsum()).size().value_counts().to_dict()
    st = stages()
    ages = [age(t, st) for t in d.time]
    d["max_ma"], d["min_ma"], d["age_status"] = zip(*ages)
    crown = crown_lookup()
    d["genus"] = d.species.map(genus)
    f3 = d.genus.map(lambda g: crown.get(g, set()))
    d["f3_crown"] = f3.map(lambda v: "yes" if v == {"yes"} else ("no" if v == {"no"} else ("mixed" if v else "absent")))
    d["capel_class"] = d.group.map(lambda g: "B2" if g in B2_GROUPS else ("not_B2" if g in NOT_B2 else
                                                                          ("unresolved" if g in UNRESOLVED else "unknown")))
    assert not d.capel_class.eq("unknown").any(), d.loc[d.capel_class.eq("unknown"), "group"].unique()
    d["b2_rule"] = np.where(d.f3_crown.isin(["yes", "no"]), "f3_genus", "capel_group")
    d["b2"] = np.where(d.f3_crown.eq("yes"), "B2", np.where(d.f3_crown.eq("no"), "not_B2", d.capel_class))
    d["conflict"] = d.f3_crown.isin(["yes", "no"]) & d.capel_class.isin(["B2", "not_B2"]) & (
        d.f3_crown.eq("yes") != d.capel_class.eq("B2"))
    d["locality_key"] = d.locality.map(locality_key).replace(ALIASES)
    d["region"] = d.locality.map(region)
    loc = d.locality.fillna("")
    d["yea"] = loc.str.contains(r"\bYea\b") & loc.str.contains("Victoria|Australia") & ~loc.str.contains("Norton Gully")
    d["literal_max_ma"], d["literal_min_ma"] = d.max_ma, d.min_ma
    d.loc[d.yea, "max_ma"], d.loc[d.yea, "min_ma"] = 426.7, YOUNG
    return d, rows_per_species


def fuzzy_groups(keys_by_region):
    """Single-linkage merge of keys with difflib ratio >= 0.92 within one region, over sorted keys."""
    merged = {}
    for reg, keys in keys_by_region.items():
        keys = sorted(set(keys))
        parent = {k: k for k in keys}

        def find(k):
            while parent[k] != k:
                k = parent[k]
            return k
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                if difflib.SequenceMatcher(None, a, b).ratio() >= 0.92:
                    parent[find(b)] = find(a)
        merged.update({k: find(k) for k in keys})
    return merged


def units(d, variant="main", counting="locality_age"):
    """S3 units for variant main, plus_unresolved, yea_literal or fuzzy; same aggregation as select_records."""
    r = d[d.b2.isin(["B2", "unresolved"] if variant == "plus_unresolved" else ["B2"])].copy()
    if variant == "yea_literal":
        r["max_ma"], r["min_ma"] = r.literal_max_ma, r.literal_min_ma
    r = r[r.max_ma > YOUNG]
    key = r.locality_key
    if variant == "fuzzy":
        m = fuzzy_groups(r.groupby("region").locality_key.apply(list).to_dict())
        key = key.map(m)
    if counting == "locality_age":
        r["unit_id"] = key + "|" + r.min_ma.astype(str) + "|" + r.max_ma.astype(str)
    elif counting == "region_stage":
        _, old = stage_bounds(np.minimum(DOMAIN, (r.min_ma.values + r.max_ma.values) / 2))
        r["unit_id"] = r.region + "|midpoint-stage:" + pd.Series(old, index=r.index).astype(str)
    return r.groupby("unit_id", as_index=False).agg(
        min_ma=("min_ma", "max"), max_ma=("max_ma", "max"), region=("region", "first"),
        member_ids=("capel_row", lambda x: ";".join(map(str, sorted(x)))), n_members=("capel_row", "size"))


def main():
    d, per_species = parse()
    print("rows per species:", per_species)
    assert per_species == {1: 810, 2: 194}, per_species
    cols = ["capel_row", "continuation", "species", "genus", "group", "time", "max_ma", "min_ma", "literal_max_ma",
            "literal_min_ma", "age_status", "f3_crown", "capel_class", "b2_rule", "b2", "conflict", "locality",
            "locality_key", "region", "yea", "reference"]
    d[cols].to_csv(OUT / "capel_s3_rows.csv", index=False, lineterminator="\n")
    timemap = d.groupby(d.time.fillna("").str.strip()).agg(max_ma=("literal_max_ma", "first"), min_ma=("literal_min_ma", "first"),
                                                            status=("age_status", "first"), rows=("capel_row", "size"))
    timemap.to_csv(OUT / "capel_s3_age_map.csv", lineterminator="\n")
    country = d.assign(field=d.locality.fillna("").str.split(",").str[-1].str.strip()).groupby(["field", "region"]).size()
    country.rename("rows").to_csv(OUT / "capel_s3_region_map.csv", lineterminator="\n")
    win = d[d.b2.isin(["B2", "unresolved"]) & (d.max_ma > YOUNG)]
    m = fuzzy_groups(win.groupby("region").locality_key.apply(list).to_dict())
    pairs = sorted({(k, v) for k, v in m.items() if k != v})
    pd.DataFrame(pairs, columns=["key", "merged_into"]).to_csv(OUT / "capel_s3_fuzzy_merges.csv", index=False,
                                                               lineterminator="\n")
    print(d.b2.value_counts().to_string())
    print("conflicts:", int(d.conflict.sum()), "| age status:", d.age_status.value_counts().to_dict(),
          "| fuzzy merges in window:", len(pairs), "| Yea rows:", int(d.yea.sum()))


if __name__ == "__main__":
    main()
