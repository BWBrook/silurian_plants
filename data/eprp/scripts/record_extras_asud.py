"""record_extras_asud.py (tranche 2): Australian Silurian-Devonian stratigraphic units from the ASUD WFS snapshot in EPRP's mirror.

Run on deep-server (stdlib only):
    scp data/eprp/record/pbdb_plant_occurrences.csv data/eprp/record/pbdb_plant_collections.csv deep-server:<IN_DIR>/
    ssh deep-server python3 - < record_extras_asud.py
Reads /data/paleodata/asud/raw/2026-10-22T0604Z_wfs/StratigraphicUnit.csv read-only (sha256 checked against the mirror MANIFEST.json),
tranche 1's plant occurrence and collection tables, and fetches the Geoscience Australia eCat record and the WFS capabilities for the
licence statement. Writes to /data/codex/silurian_plants/raw/pbdb-extras/asud/<UTC stamp>/ : asud_silurian_devonian_units.csv,
PROVENANCE.tsv (URL, timestamp, licence, sha256) and the two catalogue files. Copy the table to data/eprp/record/ afterwards.

All 34 source columns are kept unchanged and in source order; derived columns are prefixed derived_ (no source age is converted or repaired).
"""
import csv
import collections
import datetime
import hashlib
import json
import os
import re
import sys
import urllib.request

csv.field_size_limit(1 << 30)

ASUD = "/data/paleodata/asud/raw/2026-10-22T0604Z_wfs/"
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%MZ")
BASE = "/data/codex/silurian_plants/raw/pbdb-extras/"
IN_DIR = BASE + "input/"
OUT = BASE + "asud/" + STAMP + "/"
UA = "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"
SD_TOP, SD_BASE = 358.86, 443.1      # Ma: base of the Tournaisian and of the Rhuddanian in data/timescale.csv (ICS v2024/12)
WIN_TOP, WIN_BASE = 383.0, 485.0     # Ma: tranche-1 window
os.makedirs(OUT, exist_ok=True)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 22), b""):
            h.update(c)
    return h.hexdigest()


# ---- provenance: catalogue evidence and the mirror file ----
prov = []


def fetch(name, url, note):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    with open(OUT + name, "wb") as f:
        f.write(data)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    prov.append([name, url, ts, "CC BY 4.0 (see note)", str(len(data)), sha256_bytes(data), note])
    return data


ecat = fetch("ecat_a05f7892-8ca9-7506-e044-00144fdd4fa6.xml",
             "https://ecat.ga.gov.au/geonetwork/srv/api/records/a05f7892-8ca9-7506-e044-00144fdd4fa6/formatters/xml",
             "Geoscience Australia eCat record for the Australian Stratigraphic Units Database: licence 'Creative Commons Attribution 4.0 International Licence, CC-BY 4.0', (c) Commonwealth of Australia (Geoscience Australia) and Geological Society of Australia (Australian Stratigraphy Commission) 2026")
caps = fetch("wfs_capabilities.xml",
             "https://services.ga.gov.au/gis/stratunits/ows?service=WFS&version=2.0.0&request=GetCapabilities",
             "WFS GetCapabilities: AccessConstraints '(c) Commonwealth of Australia (Geoscience Australia) 2020. This product is released under the Creative Commons Attribution 4.0 International Licence'")
man = {x["key"]: x for x in json.load(open(ASUD + "MANIFEST.json"))["files"]}
src_sha = sha256_file(ASUD + "StratigraphicUnit.csv")
assert src_sha == man["StratigraphicUnit.csv"]["sha256"], "mirror file differs from its manifest"
prov.append(["StratigraphicUnit.csv", man["StratigraphicUnit.csv"]["url"], "2026-10-22T06:04:38Z (EPRP mirror retrieval)",
             "CC BY 4.0 (WFS AccessConstraints; eCat record)", str(os.path.getsize(ASUD + "StratigraphicUnit.csv")), src_sha,
             "EPRP mirror deep-server:" + ASUD + "StratigraphicUnit.csv, numberMatched 18357; sha256 equals the mirror manifest"])
with open(OUT + "PROVENANCE.tsv", "w") as f:
    f.write("file\turl\tretrieved_utc\tlicence\tbytes\tsha256\tnote\n")
    for r in prov:
        f.write("\t".join(r) + "\n")

# ---- tranche-1 PBDB plant context, for the name link ----
STATE_CODE = {"Victoria": "VIC", "New South Wales": "NSW", "Queensland": "QLD", "Western Australia": "WA",
              "South Australia": "SA", "Tasmania": "TAS", "Northern Territory": "NT",
              "Australian Capital Territory": "ACT"}
COLL = {}
with open(IN_DIR + "pbdb_plant_collections.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["cc"] == "AU":
            COLL[r["collection_no"]] = r
GEN = collections.defaultdict(set)
BARAG = set()
with open(IN_DIR + "pbdb_plant_occurrences.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        c = r["collection_no"]
        if c in COLL and r["d_in_core"] == "yes":
            GEN[c].add(r["d_genus"] or r["identified_name"])
        if c in COLL and re.search(r"baragwan", r["identified_name"] + r["accepted_name"], re.I):
            BARAG.add(c)
log("tranche-1 Australian collections", len(COLL), "with a Baragwanathia occurrence", len(BARAG))

RANK_WORDS = r"\b(formation|group|member|subgroup|supergroup|beds?|suite|fm|gp|mbr)\b"
LITH_WORDS = (r"\b(shale|siltstone|sandstone|mudstone|limestone|conglomerate|quartzite|greywacke|slate|marl|chert|"
              r"volcanics?|tuff|basalt|rhyolite|dolomite|granite|porphyry|schist|gneiss|coal|measures|metasediments?)\b")


def stem(s, lith):
    s = s.lower()
    s = re.sub(RANK_WORDS, " ", s)
    if lith:
        s = re.sub(LITH_WORDS, " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def name_parts(name):
    return [p.strip() for p in re.split(r"[;,]|\band\b", name) if p.strip()]


def stems_of(name):
    out = set()
    for p in name_parts(name):
        out.add(stem(p, False))
        out.add(stem(p, True))
    out.discard("")
    return out


COLL_FIELD_STEMS = {}
COLL_TEXT = {}
for cn, c in COLL.items():
    s = set()
    for k in ("formation", "formation.1", "geological_group", "member"):
        if c[k]:
            s.add(stem(c[k], False))
            s.add(stem(c[k], True))
    s.discard("")
    COLL_FIELD_STEMS[cn] = s
    COLL_TEXT[cn] = " ".join(c[k] for k in ("stratcomments", "collection_name", "geology_comments", "lithdescript")).lower()

# ---- ASUD ----
SD_TERMS = ["silurian", "devonian", "llandovery", "wenlock", "ludlow", "pridoli", "rhuddanian", "aeronian", "telychian",
            "sheinwoodian", "homerian", "gorstian", "ludfordian", "lochkovian", "pragian", "emsian", "eifelian", "givetian",
            "frasnian", "famennian"]
SD_RE = re.compile(r"\b(" + "|".join(SD_TERMS) + r")\b", re.I)
ENV = [
    ("non-marine", r"\bnon-?marine\b|\bterrestrial\b|\bcontinental\b"),
    ("fluvial_alluvial", r"\bfluvial\b|\balluvial\b|\briver\b|\bstream\b|\bbraided\b|\bmeander|\bfloodplain\b"),
    ("lacustrine", r"\blacustrine\b|\blake\b|\blakes\b"),
    ("aeolian", r"\baeolian\b|\beolian\b|\bdune"),
    ("glacial", r"\bglacial\b|\bglacigenic\b|\btillite\b|\bdiamictite\b"),
    ("coastal_deltaic_estuarine", r"\bdelta|\bestuar|\bcoastal\b|\btidal\b|\bbeach\b|\bshoreface\b|\bintertidal\b|\blagoon"),
    ("shallow_marine_shelf", r"\bshallow[- ]marine\b|\bshelf\b|\bnearshore\b|\breef|\bplatform\b|\bshoal"),
    ("deep_marine_basinal", r"\bdeep[- ]water\b|\bdeep[- ]marine\b|\bturbidit|\bbathyal\b|\bbasinal\b|\bhemipelagic\b|\bpelagic\b|\bflysch\b|\bbouma\b|\bsubmarine fan\b|\bslope\b"),
    ("marine_unspecified", r"(?<!non-)(?<!non )\bmarine\b"),
    ("volcanic", r"\bvolcan|\blava\b|\bignimbrite|\brhyolit|\bbasalt|\bandesit|\btuff|\bpyroclast"),
    ("intrusive", r"\bgranit|\bgranodiorit|\btonalit|\bintrusi|\bpluton|\bdolerite\b|\bgabbro|\bdiorite\b|\bsyenit"),
]
ENV = [(k, re.compile(v, re.I)) for k, v in ENV]
PLANT_RE = re.compile(r"\b(plants?|flora|macroflora|microflora|spores?|miospores?|lycopod\w*|psilophyt\w*|zosterophyll\w*|baragwan\w*|cooksonia|"
                      r"plant fossils?)\b", re.I)
LEVELS = ["BED", "MEMBER", "FORMATION", "SUBGROUP", "GROUPNAME", "SUPERGROUP"]
OWN_LEVEL = {"Bed": "BED", "Member, phase": "MEMBER", "Formation, beds": "FORMATION", "Subgroup": "SUBGROUP",
             "Group, Suite": "GROUPNAME", "Supergroup": "SUPERGROUP"}
LEVEL_RANK = {"BED": "bed", "MEMBER": "member", "FORMATION": "formation", "SUBGROUP": "subgroup", "GROUPNAME": "group",
              "SUPERGROUP": "supergroup"}


def num(x):
    try:
        return float(x)
    except ValueError:
        return None


DER = ["derived_in_victoria", "derived_state_list", "derived_age_older_ma", "derived_age_younger_ma", "derived_age_flag",
       "derived_overlaps_silurian_devonian", "derived_overlaps_project_window", "derived_sd_text_terms", "derived_sd_basis",
       "derived_composite_name", "derived_parent_unit", "derived_parent_rank", "derived_parent_chain",
       "derived_environment_keywords", "derived_description_plant_terms", "derived_pbdb_plant_collections_by_name_field",
       "derived_pbdb_plant_collections_by_text_mention", "derived_pbdb_core_genera_in_matched_collections",
       "derived_pbdb_baragwanathia_collection_nos"]
out_rows = []
n_all = 0
with open(ASUD + "StratigraphicUnit.csv", newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    HEAD = next(rd)
    IX = {k: i for i, k in enumerate(HEAD)}
    for row in rd:
        n_all += 1
        state = row[IX["STATE"]]
        states = [s.strip() for s in state.split(",") if s.strip()]
        a, b = num(row[IX["NUMERICOLDERAGE"]]), num(row[IX["NUMERICYOUNGERAGE"]])
        flag, hi, lo = "", None, None
        if a is None or b is None:
            flag = "missing"
        else:
            hi, lo = max(a, b), min(a, b)
            if a < b:
                flag = "inverted"
            if a in (4031.0, 4567.0):
                flag = "placeholder_eon_base"
            elif a == 0 and b == 0:
                flag = "zero_zero"
        ov_sd = ov_win = ""
        if hi is not None:
            ov_sd = "yes" if (hi > SD_TOP and lo < SD_BASE and flag not in ("placeholder_eon_base", "zero_zero")) else "no"
            ov_win = "yes" if (hi > WIN_TOP and lo < WIN_BASE and flag not in ("placeholder_eon_base", "zero_zero")) else "no"
        terms = sorted({m.lower() for m in SD_RE.findall(row[IX["GEOLOGICHISTORY"]])})
        if ov_sd == "yes" and terms:
            basis = "numeric_and_text"
        elif ov_sd == "yes":
            basis = "numeric_only"
        elif terms and hi is None:
            basis = "text_only_no_numeric"
        elif terms:
            basis = "text_only_numeric_disjoint"
        else:
            continue
        name = row[IX["NAME"]]
        composite = "yes" if len(name_parts(name)) > 1 else "no"
        own = OWN_LEVEL.get(row[IX["RANK"]], "")
        parent, prank = "", ""
        if own:
            for lv in LEVELS[LEVELS.index(own) + 1:]:
                v = row[IX[lv]]
                if v and v != name:
                    parent, prank = v, LEVEL_RANK[lv]
                    break
        chain = " > ".join(row[IX[lv]] for lv in reversed(LEVELS) if row[IX[lv]])
        text = row[IX["DESCRIPTION"]] + " " + row[IX["LITHOLOGY"]]
        env = ";".join(k for k, rx in ENV if rx.search(text))
        ust = stems_of(name)
        by_field, by_text = [], []
        for cn, c in COLL.items():
            if STATE_CODE.get(c["state"], "?") not in states:
                continue
            if ust & COLL_FIELD_STEMS[cn]:
                by_field.append(cn)
            elif any(len(p) >= 8 and len(stem(p, True)) >= 4 and re.search(r"\b" + re.escape(p.lower()) + r"\b", COLL_TEXT[cn])
                     for p in name_parts(name)):
                by_text.append(cn)
        matched = by_field + by_text
        genera = ";".join(sorted({g for cn in matched for g in GEN[cn] if g}))
        barag = ";".join(cn for cn in matched if cn in BARAG)
        out_rows.append(row + ["yes" if "VIC" in states else "no", ";".join(states),
                               "" if hi is None else f"{hi:g}", "" if lo is None else f"{lo:g}", flag, ov_sd, ov_win,
                               ";".join(terms), basis, composite, parent, prank, chain, env,
                               ";".join(sorted({m.lower() for m in PLANT_RE.findall(row[IX["DESCRIPTION"]])})),
                               ";".join(by_field), ";".join(by_text), genera, barag])
out_rows.sort(key=lambda r: int(r[IX["STRATNO"]]))
with open(OUT + "asud_silurian_devonian_units.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(HEAD + DER)
    w.writerows(out_rows)
DX = {k: i for i, k in enumerate(HEAD + DER)}
log("ASUD rows", n_all, "selected", len(out_rows))
log("basis", dict(collections.Counter(r[DX["derived_sd_basis"]] for r in out_rows)))
log("victoria", sum(1 for r in out_rows if r[DX["derived_in_victoria"]] == "yes"),
    "victoria only", sum(1 for r in out_rows if r[DX["STATE"]] == "VIC"))
log("age flags", dict(collections.Counter(r[DX["derived_age_flag"]] for r in out_rows)))
log("rows with a PBDB plant collection link", sum(1 for r in out_rows if r[DX["derived_pbdb_plant_collections_by_name_field"]] or r[DX["derived_pbdb_plant_collections_by_text_mention"]]))
for r in out_rows:
    if r[DX["derived_pbdb_baragwanathia_collection_nos"]]:
        log("BARAG", r[DX["STRATNO"]], r[DX["NAME"]], r[DX["STATE"]], r[DX["GEOLOGICHISTORY"]], r[DX["derived_pbdb_baragwanathia_collection_nos"]])
log("output dir", OUT)
