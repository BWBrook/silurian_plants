#!/usr/bin/env python3
"""Build the specimen tables from the raw GBIF, iDigBio and ALA-mirror pages (stdlib only).

Reads: a GBIF harvest dir and an iDigBio harvest dir written by specimens_harvest.py (with their datasets/, verbatim/,
recordsets/ and media/ subdirectories when fetched), the EPRP gbif-ala-fossils mirror (read-only), specimens_scope_names.csv
and data/timescale.csv.  Writes under OUT/specimens (open-licence tables, specimen_filter_names.csv, card summaries,
gbif_datasets.csv, gbif_backbone_placement.csv, idigbio_recordsets.csv), OUT/local_specimens (tables whose records carry no
or unclear licences) and OUT/build_stats.json.  Source values are never converted or repaired; every computed column is
prefixed derived_.

usage: python3 specimens_build.py --gbif DIR --idigbio DIR --ala DIR --scope CSV --timescale CSV --out DIR
       python3 specimens_build.py ... --emit-lists PREFIX   (write PREFIX_gbif_verbatim_keys.txt and PREFIX_idigbio_media_uuids.txt, then stop)
"""
import csv
import difflib
import glob
import json
import os
import re
import sys
import collections

WIN_OLD, WIN_YOUNG = 485.0, 383.0          # window, Ma (brief)
FF_YOUNG = 358.86                          # Famennian top, for anchor genera
csv.field_size_limit(10 ** 9)

# ------------------------------------------------------------------ time scale

STAGES = []   # (name, base, top)


def load_timescale(path):
    rows = list(csv.DictReader(open(path)))
    rows = [(r["stage"], float(r["base_ma"]), r["series"], r["period"]) for r in rows]
    rows.sort(key=lambda x: -x[1])
    for i, (name, base, series, period) in enumerate(rows):
        top = rows[i + 1][1] if i + 1 < len(rows) else None
        STAGES.append((name, base, top, series, period))


INTERVALS = {}      # lower-case name -> (base, top, level, note)
COARSE = {"paleozoic": (538.8, 251.9), "phanerozoic": (538.8, 0.0), "palaeozoic": (538.8, 251.9)}


def build_intervals():
    st = {s[0].lower(): s for s in STAGES}
    for name, base, top, series, period in STAGES:
        if top is not None and name != "Tournaisian":
            INTERVALS[name.lower()] = (base, top, "stage", "")

    def span(a, b):
        return (st[a][1], st[b][2])
    ser = {"lower ordovician": span("tremadocian", "floian"), "middle ordovician": span("dapingian", "darriwilian"),
           "upper ordovician": span("sandbian", "hirnantian"), "llandovery": span("rhuddanian", "telychian"),
           "wenlock": span("sheinwoodian", "homerian"), "ludlow": span("gorstian", "ludfordian"),
           "lower devonian": span("lochkovian", "emsian"), "middle devonian": span("eifelian", "givetian"),
           "upper devonian": span("frasnian", "famennian")}
    for k, (b, t) in ser.items():
        INTERVALS[k] = (b, t, "series", "")
    INTERVALS["pridoli"] = (st["pridoli"][1], st["pridoli"][2], "series", "")
    INTERVALS["ordovician"] = (st["tremadocian"][1], st["hirnantian"][2], "period", "")
    INTERVALS["silurian"] = (st["rhuddanian"][1], st["pridoli"][2], "period", "")
    INTERVALS["devonian"] = (st["lochkovian"][1], st["famennian"][2], "period", "")
    INTERVALS["cambrian"] = (538.8, st["tremadocian"][1], "period", "ICS v2024/12 value not in project table")
    INTERVALS["furongian"] = (497.0, st["tremadocian"][1], "series", "ICS value not in project table")
    INTERVALS["carboniferous"] = (st["famennian"][2], 298.9, "period", "ICS value not in project table")
    INTERVALS["mississippian"] = (st["famennian"][2], 323.2, "series", "ICS value not in project table")
    INTERVALS["pennsylvanian"] = (323.2, 298.9, "series", "ICS value not in project table")
    INTERVALS["permian"] = (298.9, 251.9, "period", "ICS value not in project table")
    # outside the window: only used to recognise that a record is dated and not in the window
    for k, (b, t) in {"triassic": (251.9, 201.4), "jurassic": (201.4, 145.0), "cretaceous": (145.0, 66.0),
                      "paleogene": (66.0, 23.03), "paleocene": (66.0, 56.0), "eocene": (56.0, 33.9),
                      "oligocene": (33.9, 23.03), "neogene": (23.03, 2.58), "miocene": (23.03, 5.33),
                      "pliocene": (5.33, 2.58), "tertiary": (66.0, 2.58), "quaternary": (2.58, 0.0),
                      "pleistocene": (2.58, 0.0117), "holocene": (0.0117, 0.0), "recent": (0.0117, 0.0),
                      "cenozoic": (66.0, 0.0), "mesozoic": (251.9, 66.0), "precambrian": (4600.0, 538.8),
                      "proterozoic": (2500.0, 538.8), "neoproterozoic": (1000.0, 538.8), "ediacaran": (635.0, 538.8)}.items():
        INTERVALS[k] = (b, t, "period", "approximate; only used to recognise a non-window age")


# regional or traditional terms mapped to the nearest ICS interval by the analyst; flagged in derived_age_basis
ALIAS = {"gedinnian": ("lochkovian",), "siegenian": ("pragian",), "downtonian": ("pridoli", "lochkovian"),
         "dittonian": ("lochkovian", "pragian"), "ludlovian": ("ludlow",), "wenlockian": ("wenlock",),
         "llandoverian": ("llandovery",), "niagaran": ("llandovery", "wenlock"), "alexandrian": ("llandovery",),
         "cincinnatian": ("upper ordovician",), "cayugan": ("ludlow", "pridoli"), "helderbergian": ("lochkovian",),
         "oriskanian": ("lower devonian",), "ulsterian": ("lower devonian",), "erian": ("middle devonian",)}
OTHER_PERIOD_WORDS = {"néogène": "neogene", "paléogène": "paleogene", "crétacé": "cretaceous", "jurassique": "jurassic",
                      "trias": "triassic", "permien": "permian", "quaternaire": "quaternary", "pléistocène": "pleistocene",
                      "éocène": "eocene", "oligocène": "oligocene", "miocène": "miocene", "pliocène": "pliocene",
                      "paléocène": "paleocene", "cambrien": "cambrian", "tertiaire": "tertiary", "pennsylvanien": "pennsylvanian",
                      "mississippien": "mississippian"}
PERIOD_WORDS = {"furongian": "cambrian", "miaolingian": "cambrian", "terreneuvian": "cambrian", "ordovician": "ordovician", "ordovicien": "ordovician", "silurian": "silurian", "silurien": "silurian",
                "devonian": "devonian", "devonien": "devonian", "dévonien": "devonian", "cambrian": "cambrian",
                "carboniferous": "carboniferous", "carbonifère": "carboniferous", "permian": "permian",
                "mississippian": "mississippian", "pennsylvanian": "pennsylvanian"}
MOD_LOWER = {"early", "lower", "lowermost"}
MOD_MID = {"middle"}
MOD_UP = {"late", "upper", "uppermost"}
SIL_SERIES = {"lower": ("llandovery",), "early": ("llandovery",), "lowermost": ("llandovery",), "middle": ("wenlock",),
              "upper": ("ludlow", "pridoli"), "late": ("ludlow", "pridoli"), "uppermost": ("pridoli",)}


def split_camel(s):
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s)


_PA = {}


def parse_age(text):
    k = text if isinstance(text, str) else str(text)
    if k not in _PA:
        _PA[k] = _parse_age(text)
    return _PA[k]


def _parse_age(text):
    """Parse a free-text or vocabulary age string into the finest named intervals.
    Returns (base, top, level, basis) or None.  basis is 'ics' or 'alias' (regional term mapped by the analyst)."""
    if not text:
        return None
    s = split_camel(str(text)).lower()
    s = re.sub(r"[\?\(\)\[\],;:/&|]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        return None
    found = []      # (base, top, level, basis)
    alias_used = False

    def take(pattern, fn):
        nonlocal s
        for m in list(re.finditer(pattern, s)):
            r = fn(m)
            if r:
                found.append(r)
        s = re.sub(pattern, " ", s)

    take(r"\b(%s)\b" % "|".join(k for k in INTERVALS if INTERVALS[k][2] == "stage" or k == "pridoli"),
         lambda m: INTERVALS[m.group(1)])
    take(r"\b(%s)\b" % "|".join(ALIAS), lambda m: ("alias", m.group(1)))
    # series phrases
    def ser(m):
        mod, per = m.group(1), m.group(2)
        per = PERIOD_WORDS.get(per, per)
        if per == "silurian":
            return ("multi", SIL_SERIES[mod])
        key = ("lower " if mod in MOD_LOWER else "middle " if mod in MOD_MID else "upper ") + per
        return INTERVALS.get(key)
    take(r"\b(early|lower|lowermost|middle|late|upper|uppermost)\s+(ordovician|silurian|devonian|ordovicien|silurien|devonien|dévonien)\b", ser)
    take(r"\b(llandovery|wenlock|ludlow)\b", lambda m: INTERVALS[m.group(1)])
    take(r"\b(furongian|miaolingian|terreneuvian|ordovician|silurian|devonian|ordovicien|silurien|devonien|dévonien|cambrian|carboniferous|carbonifère|permian|mississippian|pennsylvanian)\b",
         lambda m: INTERVALS[PERIOD_WORDS[m.group(1)]])
    take(r"\b(%s)\b" % "|".join(sorted(OTHER_PERIOD_WORDS, key=len, reverse=True)), lambda m: INTERVALS[OTHER_PERIOD_WORDS[m.group(1)]])
    take(r"\b(triassic|jurassic|cretaceous|paleogene|paleocene|eocene|oligocene|neogene|miocene|pliocene|tertiary|quaternary|pleistocene|holocene|recent|cenozoic|mesozoic|precambrian|proterozoic|neoproterozoic|ediacaran)\b",
         lambda m: INTERVALS[m.group(1)])
    ivs = []
    for f in found:
        if f[0] == "alias":
            alias_used = True
            for nm in ALIAS[f[1]]:
                ivs.append(INTERVALS[nm])
        elif f[0] == "multi":
            for nm in f[1]:
                ivs.append(INTERVALS[nm])
        else:
            ivs.append(f)
    if not ivs:
        c = [COARSE[w] for w in COARSE if w in text.lower()]
        if c:
            return (c[0][0], c[0][1], "coarse", "ics")
        return None
    # drop an interval that contains another found interval (keeps the finest)
    keep = []
    for i, a in enumerate(ivs):
        contains_other = any(j != i and a[0] >= b[0] and a[1] <= b[1] and (a[0], a[1]) != (b[0], b[1]) for j, b in enumerate(ivs))
        if not contains_other:
            keep.append(a)
    base = max(a[0] for a in keep)
    top = min(a[1] for a in keep)
    order = {"stage": 0, "series": 1, "period": 2}
    level = min((a[2] for a in keep), key=lambda x: order.get(x, 3))
    return (base, top, level, "alias" if alias_used else "ics")


LEVEL_ORDER = (("stage", "AgeOrLowestStage", "AgeOrHighestStage"), ("epoch", "EpochOrLowestSeries", "EpochOrHighestSeries"),
               ("period", "PeriodOrLowestSystem", "PeriodOrHighestSystem"))
TEXT_AGE_FIELDS = ("lithostratigraphicTerms", "formation", "group", "member", "bed", "lowestBiostratigraphicZone",
                   "highestBiostratigraphicZone", "geologicalContextID")


def derive_age(row, anchor):
    """Window logic on the age fields as recorded.  Returns dict of derived_* columns."""
    ear, lat = {}, {}
    for lvl, e, l in LEVEL_ORDER:
        ear[lvl] = parse_age(row.get("earliest" + e))
        lat[lvl] = parse_age(row.get("latest" + l))
    ear["era"] = parse_age(row.get("earliestEraOrLowestErathem"))
    lat["era"] = parse_age(row.get("latestEraOrHighestErathem"))
    def narrowest(d):
        c = [(l, d[l]) for l in ("stage", "epoch", "period") if d[l] and d[l][2] != "coarse"]
        if not c:
            return None, ""
        l, v = min(c, key=lambda x: x[1][0] - x[1][1])
        return v, l
    efine, elvl = narrowest(ear)
    lfine, llvl = narrowest(lat)
    notes = []
    out = {"derived_age_max_ma": "", "derived_age_min_ma": "", "derived_age_span_myr": "", "derived_age_basis": "",
           "derived_age_note": "", "derived_fully_inside_window": "", "derived_window_status": ""}
    basis = ""
    for tag, d in (("earliest", ear), ("latest", lat)):
        lv = sorted((d[l] for l in ("stage", "epoch", "period") if d[l] and d[l][2] != "coarse"), key=lambda v: v[0] - v[1])
        for fi in range(len(lv)):
            for co in range(fi + 1, len(lv)):
                if lv[fi][0] > lv[co][0] + 0.5 or lv[fi][1] < lv[co][1] - 0.5:
                    notes.append("%s stage, epoch and period fields disagree" % tag)
    notes = sorted(set(notes))
    if efine and lfine:
        e_in_l = efine[0] <= lfine[0] + 1e-9 and efine[1] >= lfine[1] - 1e-9
        l_in_e = lfine[0] <= efine[0] + 1e-9 and lfine[1] >= efine[1] - 1e-9
        if e_in_l and not l_in_e:
            lfine = efine
            llvl = elvl
            notes.append("latest field coarser than earliest; finest field used for both bounds")
        elif l_in_e and not e_in_l:
            efine = lfine
            elvl = llvl
            notes.append("earliest field coarser than latest; finest field used for both bounds")
    if efine or lfine:
        mx = efine[0] if efine else lfine[0]
        mn = lfine[1] if lfine else efine[1]
        if efine and lfine and efine[0] < lfine[1] - 1e-9:
            notes.append("earliest and latest fields are in reverse order")
            mx, mn = max(efine[0], lfine[0]), min(efine[1], lfine[1])
        basis = "fields:" + ("earliest_%s" % elvl if efine else "") + ("+" if efine and lfine else "") + ("latest_%s" % llvl if lfine else "")
        if (efine and efine[3] == "alias") or (lfine and lfine[3] == "alias"):
            basis += ";regional_term_mapped_by_analyst"
        out["derived_age_max_ma"] = "%.2f" % mx
        out["derived_age_min_ma"] = "%.2f" % mn
        out["derived_age_span_myr"] = "%.2f" % (mx - mn)
        overlap = mx > WIN_YOUNG and mn < WIN_OLD
        inside = mx <= WIN_OLD and mn >= WIN_YOUNG
        out["derived_fully_inside_window"] = "yes" if inside else "no"
        if overlap:
            out["derived_window_status"] = "in_window"
            if mx - mn > 60:
                notes.append("age range wider than 60 Myr")
        elif anchor and mx > FF_YOUNG and mn < WIN_YOUNG:
            out["derived_window_status"] = "anchor_late_devonian"
        else:
            out["derived_window_status"] = "outside_window"
    else:
        coarse = any(x and x[2] == "coarse" for x in list(ear.values()) + list(lat.values()))
        txt = " ; ".join(str(row.get(f) or "") for f in TEXT_AGE_FIELDS)
        tp = parse_age(txt) if txt.strip(" ;") else None
        if tp and tp[2] != "coarse":
            mx, mn = tp[0], tp[1]
            basis = "text:stratigraphic_fields"
            out["derived_age_max_ma"] = "%.2f" % mx
            out["derived_age_min_ma"] = "%.2f" % mn
            out["derived_age_span_myr"] = "%.2f" % (mx - mn)
            out["derived_fully_inside_window"] = "yes" if (mx <= WIN_OLD and mn >= WIN_YOUNG) else "no"
            if mx > WIN_YOUNG and mn < WIN_OLD:
                out["derived_window_status"] = "in_window"
            elif anchor and mx > FF_YOUNG and mn < WIN_YOUNG:
                out["derived_window_status"] = "anchor_late_devonian"
            else:
                out["derived_window_status"] = "outside_window"
        elif coarse:
            basis = "coarse_only"
            out["derived_window_status"] = "coarse_age_only"
        else:
            basis = "none"
            out["derived_window_status"] = "undated"
    out["derived_age_basis"] = basis
    out["derived_age_note"] = "; ".join(notes)
    return out


# ------------------------------------------------------------------ licences

def licence_class(lic):
    s = (lic or "").strip().lower()
    if not s:
        return "none"
    if "publicdomain/zero" in s or s in ("cc0", "cc0 1.0", "cc-0") or "cc0" in s:
        return "CC0"
    if re.search(r"by-nc-nd|by-nc-sa|nc-nd|nc-sa", s):
        return "other"
    if re.search(r"by-nc|attribution-noncommercial|noncommercial|by_nc|cc\d? ?by ?-?nc", s):
        return "CC-BY-NC"
    if re.search(r"by-sa|by-nd|sharealike|noderiv", s):
        return "other"
    if re.search(r"/by/|creative commons attribution|attribution 4|cc\d? ?by(?![a-z-])|by 4\.0|by 3\.0|by 2\.0", s):
        return "CC-BY"
    return "other"


# ------------------------------------------------------------------ scope names

class Scope:
    def __init__(self, path):
        self.rows = list(csv.DictReader(open(path, encoding="utf-8")))
        self.genera = collections.defaultdict(list)       # genus lower -> rows
        self.binom = collections.defaultdict(list)        # (genus, epithet) lower -> rows
        for r in self.rows:
            if r["role"] == "card_assemblage" or r["name_rank"] == "higher":
                continue
            g = r["genus"].lower()
            self.genera[g].append(r)
            if r["epithet"]:
                self.binom[(g, r["epithet"].lower().replace("-", ""))].append(r)
        self.anchor_genera = {r["genus"].lower() for r in self.rows if r["role"] == "anchor"}
        self.nema_genera = {r["genus"].lower() for r in self.rows if r["role"] == "nematophyte"}
        self.glomero = {r["genus"].lower() for r in self.rows if r["card_slug"] == "early-glomeromycotan-fungi"}
        self.fungal_cards = {"tortotubus", "winfrenatia"} | self.glomero
        self.char_names = {r["genus"].lower() for r in self.rows if r["role"] == "charophyte"}
        self.genus_list = sorted(self.genera)
        self.undated_ok = {r["genus"].lower() for r in self.rows if r["genus"] and r["name_rank"] != "higher"
                           and r["role"] in ("card", "card_genus", "card_member", "card_variant", "anchor", "nematophyte", "charophyte")
                           and r["kind"] not in ("extant", "planned")}

    def match(self, genus, epithet):
        """Return list of (scope row, level) for exact genus (and species epithet) matches."""
        g = (genus or "").lower()
        e = (epithet or "").lower().replace("-", "")
        out = []
        if g in self.genera:
            for r in self.genera[g]:
                if r["epithet"]:
                    if e and e == r["epithet"].lower().replace("-", ""):
                        out.append((r, "species"))
                else:
                    out.append((r, "genus"))
        return out

    def near(self, genus):
        g = (genus or "").lower()
        if len(g) < 6 or g in self.genera:
            return ""
        m = difflib.get_close_matches(g, self.genus_list, n=1, cutoff=0.86)
        return m[0] if m else ""


# ------------------------------------------------------------------ taxonomic classification

EMBRYO_PHYLA = {"tracheophyta", "bryophyta", "marchantiophyta", "anthocerotophyta", "rhyniophyta", "lycopodiophyta",
                "lycophyta", "pteridophyta", "equisetophyta", "sphenophyta", "magnoliophyta", "angiospermae", "pinophyta",
                "coniferophyta", "cycadophyta", "ginkgophyta", "gnetophyta", "psilophyta", "psilophytophyta",
                "zosterophyllophyta", "trimerophytophyta", "progymnospermophyta", "polypodiophyta", "spermatophyta",
                "pteridospermophyta", "cycadeoidophyta", "embryophyta", "gymnospermae", "filicophyta", "lepidodendrophyta",
                "cladoxylopsida", "hepaticophyta", "bryophyta s.l.", "musci", "hepaticae", "pteridospermatophyta",
                "lyginopteridophyta", "lycopsida", "pteridosperms"}
EMBRYO_CLASSES = {"lycopodiopsida", "equisetopsida", "polypodiopsida", "pinopsida", "magnoliopsida", "liliopsida",
                  "bryopsida", "jungermanniopsida", "marchantiopsida", "cycadopsida", "ginkgoopsida", "gnetopsida",
                  "isoetopsida", "marattiopsida", "psilotopsida", "sphagnopsida", "andreaeopsida", "anthocerotopsida",
                  "progymnospermopsida", "cladoxylopsida", "zosterophyllopsida", "trimerophytopsida", "lycopsida",
                  "sphenopsida", "filicopsida", "pteridopsida", "hepaticopsida", "pteridospermopsida", "rhyniopsida",
                  "cooksoniopsida", "zosterophyllopsida"}
EMBRYO_PHYLA |= {"langiophytophyta", "rhyniophytina", "tracheophytes", "progymnospermae", "pteridophylla", "psilophytopsida"}
FUNGAL_PHYLA = {"ascomycota", "basidiomycota", "glomeromycota", "chytridiomycota", "blastocladiomycota", "zygomycota", "mucoromycota",
                "neocallimastigomycota", "microsporidia", "cryptomycota", "olpidiomycota", "entomophthoromycota"}
CHARO_TERMS = {"charophyta", "charophyceae", "charales", "characeae", "zygnematophyceae", "coleochaetophyceae",
               "klebsormidiophyceae", "streptophyta", "sycidiales", "moellerinales", "trochiliscales", "chovanellales",
               "charophytes", "charophycae", "chlorokybophyceae", "mesostigmatophyceae", "sycidiaceae", "porocharaceae",
               "moellerinaceae", "trochiliscaceae", "palaeocharaceae"}
GREEN_TERMS = {"chlorophyta", "chlorophyceae", "ulvophyceae", "dasycladales", "bryopsidales", "prasinophyceae",
               "trebouxiophyceae", "cladophorales", "receptaculitales", "receptaculitaceae", "dasycladaceae",
               "dasycladophyceae", "siphonocladales", "codiaceae", "chlorophycophyta", "chaetophorales", "ulotrichales",
               "bryopsidophyceae", "ulvales", "caulerpales", "cyclocrinitaceae", "cyclocrinitales", "pyramidophyceae",
               "phycomelaina", "microspora", "halimedaceae", "udoteaceae", "acetabulariaceae", "triploporellaceae",
               "seletonellaceae", "diploporaceae", "gyroporellaceae", "vermiporellaceae", "palaeoporellaceae",
               "anthracoporellaceae", "mizziaceae", "chlorophyll"}
RED_TERMS = {"rhodophyta", "florideophyceae", "bangiophyceae", "corallinales", "solenoporaceae", "solenoporales",
             "peyssonneliales", "gymnocodiaceae", "rhodophycophyta", "corallinophycidae", "gelidiales", "gigartinales",
             "hildenbrandiales", "sporolithales", "ungdarellaceae", "rhodophycea", "archaeolithophyllaceae", "bangiales",
             "nemaliales", "lithothamniaceae", "sphaerocodiaceae", "ortonella"}
ALGAE_TERMS = {"algae", "phycophyta", "chromophyta", "phaeophyta", "phaeophyceae", "xanthophyceae", "cyanophyta",
               "algae incertae sedis", "algae, calcareous", "calcareous algae", "problematica algae", "bacillariophyta"}
CYANO_TERMS = {"cyanobacteria", "cyanophyceae", "cyanophyta", "nostocales", "oscillatoriales", "girvanellaceae"}
ANIMAL_PHYLA = {"arthropoda", "mollusca", "brachiopoda", "echinodermata", "cnidaria", "porifera", "bryozoa", "annelida",
                "chordata", "hemichordata", "chaetognatha", "nematoda", "platyhelminthes", "foraminifera", "radiolaria",
                "tentaculita", "conodonta", "graptolithina", "ctenophora", "sipuncula", "onychophora", "tardigrada",
                "cryptozoa", "ichnotaxon", "vetulicolia", "hyolitha", "stromatoporoidea", "archaeocyatha", "chitinozoa"}
ACRITARCH_PATTERN = re.compile("(" + "|".join(sorted(set(['acritarch', 'sphaeridi', 'sphaerid', 'baltisphaer', 'veryhachium', 'micrhystridium', 'leiosphaeri', 'cymatiosphaera', 'dictyotidium', 'multiplicisphaeridium', 'ammonidium', 'estiastra', 'gorgonisphaer', 'polygonium', 'tasmanites', 'pterospermella', 'navifusa', 'lophosphaeridium', 'cymatiogalea', 'stelliferidium', 'comasphaeridium', 'diexallophasis', 'visbysphaera', 'oppilatala', 'solisphaeridium', 'domasia', 'dilatisphaera', 'cymbosphaeridium', 'duvernaysphaera', 'evittia', 'exochoderma', 'hoegklintia', 'ordovicidium', 'eupoikilofusa', 'muraticavea', 'ooidium', 'pheoclosterium', 'quadrisporites', 'salopidium', 'synsphaeridium', 'tylotopalla', 'tornacia', 'umbellasphaeridium', 'vulcanisphaera', 'buedingiisphaer', 'lunulidia', 'neoveryhachium', 'ozotobrachion', 'vogtlandia', 'cheleutochroa', 'dateriocradus', 'chuaria', 'palaeohystrichophora', 'dorsennidium', 'eisenackidium', 'helosphaeridium', 'cristallinium', 'goniosphaeridium', 'polyedryxium', 'stellinium', 'daillydium', 'petaloferidium', 'pachysphaeridium', 'pterocephalidium', 'hapsidopalla', 'pirea', 'onondagaella', 'uncinisphaera', 'arbusculidium', 'hemiruptia', 'rhopaliophora', 'orthosphaeridium', 'actinotodissus', 'saharidia', 'florisphaeridium', 'villosacapsula', 'lophodiacrodium', 'coryphidium', 'acanthodiacrodium', 'athabascaella', 'archaeoperisaccus', 'frankea', 'retisphaeridium', 'aremoricanium', 'dactylofusa', 'leiofusa', 'eomarginata', 'campanasphaera', 'maranhites', 'pterospermopsis', 'dasydiacrodium', 'dicrodiacrodium', 'peteinosphaeridium', 'polyancistrodorus', 'elektoriskos']))) + ")", re.I)
SPORE_PATTERN = re.compile(r"(sporites|sporis|spora\b|spora |triletes|tetras\b|raletes|hilates|dyadus|dyadospora|sporites\b|pollenites)", re.I)
SPORE_GENERA = {"raistrickia", "hispanaediscus", "laevolancis", "retusotriletes", "retustoriletes", "camptozonotriltes",
                "dibolisporites", "emphanisporites", "apiculiretusispora", "ambitisporites", "dictyotriletes", "streelispora",
                "cymbohilates", "cheilotetras", "velatitetras", "rimosotetras", "segestrespora", "artemopyra",
                "abditodyadus", "tetrahedraletes", "cryptospora", "dyadospora", "pseudodyadospora", "tetraplanarisporites",
                "gneudnaspora", "chelinospora", "synorisporites", "lophozonotriletes", "grandispora", "verrucosisporites",
                "acinosporites", "aneurospora", "samarisporites", "geminospora", "retispora", "cyclogranisporites",
                "leiotriletes", "punctatisporites", "granulatisporites", "calamospora", "knoxisporites", "densosporites",
                "lycospora", "rhabdosporites", "archaeozonotriletes", "ancyrospora", "hystricosporites", "cirratriradites",
                "contagisporites", "auroraspora", "rugospora", "tholisporites", "aberrantis", "crassigalea", "qualisaspora",
                "attritasporites", "coronaspora", "pseudoreticulatispora", "pyramidaspora", "navifusa", "leiosphaeridia"}
# Genus names that review of this harvest showed to be animals filed under plant or fungal homonyms (curated by the analyst)
CURATED_ANIMAL = {
    "tetradium", "lichenaria", "amphipora", "stromatopora", "labechia", "thamnopora", "favosites", "halysites",
    "heliolites", "syringopora", "cladopora", "alveolites", "aulopora", "sarcinula", "paleofavosites", "palaeofavosites",
    "streptelasma", "calapoecia", "cyathophyllum", "clathrodictyon", "actinostroma", "parallelopora", "palaeocoryne",
    "orthoceras", "stricklandia", "dictyonema", "gyroceras", "vertebrata", "ptychophyllum", "pholidophyllum", "cairocaris",
    "inocaulis", "monograptus",
    "arthropoda", "spinicaudata", "platyhelminthes", "phyllopoda", "eurypterida", "crustacea", "trilobita", "ostracoda",
    "brachiopoda", "gastropoda", "bivalvia", "cephalopoda", "bryozoa", "echinodermata", "crinoidea", "anthozoa",
}
# graptolite-like names that GBIF places among the dasyclad green algae: left to the lineage rule, so they stay flagged
GRAPTUS_EXEMPT = {"medusaegraptus", "medusagraptus", "diplospirograptus"}
CALCIMICROBES = {"girvanella", "hedstroemia", "ortonella", "renalcis", "epiphyton", "bevocastria", "nubecularia",
                 "sphaerocodium", "rothpletzella"}
PROBLEMATICA = {"buthotrephis", "bythotrephis", "taonurus", "fucoides", "chondrites", "zoophycos", "palaeophycus",
                "psammosiphon", "sphaerococcites", "fucoidea", "fucoidia", "phycodes", "phytopsis", "conostichus", "lockeia",
                "arthrophycus", "arthraria", "dactylophycus", "discophycus", "chloephycus", "licrophycus", "cryptozoon",
                "cryptozoön", "planolites", "skolithos", "thalassinoides", "rusophycus", "cruziana", "teichichnus", "monocraterion",
                "bifungites", "arenicolites", "thalassocystis", "spongiophyton", "protosalvinia", "foerstia"}
LATE_PLANT_CLASSES = {"magnoliopsida", "liliopsida", "pinopsida", "cycadopsida", "ginkgoopsida", "gnetopsida", "dicotyledones",
                      "monocotyledones", "magnoliophyta", "pinophyta", "coniferophyta", "cycadophyta", "ginkgophyta",
                      "gnetophyta", "angiospermae", "gymnospermae"}
CURATED_ANIMAL_RE = re.compile(r"(ichnofossil|ichnotaxon|trace fossil|burrow|trackway|coprolite|conodont|graptolit|"
                               r"foraminifer|radiolari|chitinozo|ostracod|trilobit|brachiopod|bryozo|crinoid|coral|"
                               r"stromatopor|sponge)", re.I)


def lc(s):
    return (s or "").strip().lower()


IGNORE_TOK = {"cf.", "cf", "aff.", "aff", "sp.", "sp", "spp.", "indet.", "gen.", "nov.", "?"}


def name_tokens(nm):
    return [t for t in re.sub(r"[?\(\)\"]", " ", nm or "").split() if t.lower() not in IGNORE_TOK]


def genus_epithet(nm):
    t = name_tokens(nm)
    g = re.sub(r"[^A-Za-z\-]", "", t[0]).lower() if t else ""
    e = t[1].lower().replace("-", "") if len(t) > 1 and re.match(r"^[a-z][a-z\-]{2,}$", t[1]) else ""
    return g, e


def row_names(row):
    """genus and epithet from each name field of the row: via -> (genus, epithet), equal pairs kept once."""
    out, seen = {}, set()
    cand = [("genus_field", (re.sub(r"[^A-Za-z\-]", "", row.get("genus") or "").lower(), (row.get("specificEpithet") or "").lower().replace("-", ""))),
            ("accepted", genus_epithet(row.get("taxon_accepted"))), ("interpreted", genus_epithet(row.get("taxon_interpreted"))),
            ("recorded", genus_epithet(row.get("taxon_recorded")))]
    for via, ge in cand:
        if ge[0] and len(ge[0]) >= 3 and ge not in seen:
            seen.add(ge)
            out[via] = ge
    return out


def classify(row, scope):
    """Return (class, subset, basis, reason) following the EPRP PBDB filter's logic where it applies."""
    kingdom, phylum, klass, order, family, genus = (lc(row.get(k)) for k in
                                                   ("kingdom", "phylum", "class", "order", "family", "genus"))
    hc = lc(row.get("higherClassification"))
    names = " ".join(lc(row.get(k)) for k in ("taxon_recorded", "taxon_interpreted", "taxon_accepted"))
    names_by_via = row.get("_names") or row_names(row)
    gens = {g for g, e in names_by_via.values()}
    gen = next((g for g, e in names_by_via.values()), "")
    lineage = {kingdom, phylum, klass, order, family} | set(hc.replace(",", " ").split())
    lineage.discard("")
    scope_named = any(g in scope.genera for g in gens)

    def has(terms):
        return bool(lineage & terms) or any(t in names.split() for t in terms)

    # scope-named taxa first (name evidence, whatever the backbone says)
    if gens & scope.nema_genera:
        return ("core", "nematophytes_and_thalloid_problematica", "name:scope_nematophyte",
                "named nematophyte or thalloid problematicum (backbone kingdom %s)" % (kingdom or "none"))
    if gens & scope.fungal_cards:
        return ("core", "scope_named_fungi_or_lichens", "name:card_taxon", "card taxon in a fungal or lichen group")
    if gens & scope.char_names or has(CHARO_TERMS):
        return ("core", "charophytes", "lineage:charophyte" if has(CHARO_TERMS) else "name:scope_charophyte",
                "fossil charophyte; in scope per brief (EPRP's PBDB filter flags streptophyte non-embryophytes)")
    if (gens & CURATED_ANIMAL or any(g.endswith("graptus") and g not in GRAPTUS_EXEMPT for g in gens)) and not scope_named:
        return ("excluded", "animal_name_filed_under_plant_or_fungus_lineage", "name:curated_animal",
                "recorded or interpreted genus is an animal (coral, cephalopod, brachiopod, graptolite, arthropod) that the source files under a plant, fungal or Plantae-only determination")
    if gens & CALCIMICROBES and not scope_named:
        return ("excluded", "bacteria_cyanobacteria", "name:curated_calcimicrobe", "calcimicrobe (cyanobacterial), as EPRP excludes")
    if kingdom == "fungi" or phylum in FUNGAL_PHYLA or klass.endswith("mycetes"):
        return ("flagged", "fungi_other", "lineage:Fungi", "fungus not named in scope")
    if kingdom == "animalia" or phylum in ANIMAL_PHYLA:
        if scope_named:
            return ("flagged", "scope_name_filed_under_animalia", "name:scope_genus_under_animalia",
                    "genus on the scope list but this record's backbone lineage is animal; check homonym")
        return ("excluded", "animal", "lineage:%s" % (phylum or kingdom), "animal lineage")
    if kingdom in ("bacteria", "archaea") or has(CYANO_TERMS):
        if scope_named:
            return ("flagged", "scope_name_filed_under_bacteria", "name:scope_genus", "scope genus under bacteria")
        return ("excluded", "bacteria_cyanobacteria", "lineage:%s" % (phylum or kingdom), "bacterial lineage (calcimicrobes, as EPRP excludes)")
    if gens & PROBLEMATICA and kingdom not in ("ichnofossil",):
        return ("flagged", "problematica_ichnofossils_or_algae", "name:curated_problematica",
                "name on the curated list of plant-like problematica, algae and trace fossils; backbone lineage %s" % (phylum or kingdom or "none"))
    if kingdom == "ichnofossil" or phylum == "ichnotaxon":
        return ("excluded", "ichnofossil", "lineage:ichnofossil", "trace fossil; EPRP's PBDB filter excludes ichnofossils")
    if has(RED_TERMS):
        return ("flagged", "red_algae", "lineage:red algae", "red algae or calcareous red algae (borderline group)")
    if has(GREEN_TERMS):
        return ("flagged", "green_algae", "lineage:green algae", "green algae other than charophytes (borderline group)")
    if has(ALGAE_TERMS):
        return ("flagged", "algae_unspecified", "lineage:algae", "algae, group not given (borderline group)")
    if any(ACRITARCH_PATTERN.search(g) for g in gens) or "acritarcha" in lineage or "incertae sedis acritarcha" in hc:
        return ("flagged", "acritarchs_prasinophytes", "name_or_lineage:acritarch", "acritarch or prasinophyte (borderline group)")
    if kingdom in ("protozoa", "chromista", "protista") or has({"chitinozoa", "radiolaria", "foraminifera"}):
        if scope_named:
            return ("flagged", "scope_name_filed_under_protists", "name:scope_genus", "scope genus under protozoa or chromista")
        return ("excluded", "protozoa_chromista", "lineage:%s" % (phylum or kingdom), "protist lineage, not plant-like")
    # embryophytes
    if phylum in EMBRYO_PHYLA or klass in EMBRYO_CLASSES or order in EMBRYO_CLASSES or has({"embryophyta", "bryophyta", "tracheophyta"}):
        amin = row.get("derived_age_min_ma")
        amin = float(amin) if amin not in (None, "") else None
        spore = any(SPORE_PATTERN.search(g) or g in SPORE_GENERA for g in gens)
        if amin is not None and not scope_named and not spore:
            if (klass in LATE_PLANT_CLASSES or phylum in LATE_PLANT_CLASSES or order in LATE_PLANT_CLASSES) and amin > 340:
                return ("flagged", "embryophyta_lineage_implausible_for_age", "lineage:%s+age" % (klass or phylum),
                        "seed-plant or flowering-plant lineage on a record whose whole age range is older than 340 Ma; likely a homonym or misfiled name")
            if phylum in ("tracheophyta",) and amin > 433.4:
                return ("flagged", "embryophyta_lineage_implausible_for_age", "lineage:Tracheophyta+age",
                        "vascular-plant lineage on a record whose whole age range is older than the oldest vascular macrofossils (about 433 Ma)")
        return ("core", "embryophyta", "lineage:%s" % (phylum or klass or "embryophyta"), "embryophyte lineage")
    if CURATED_ANIMAL_RE.search(names):
        if scope_named:
            return ("flagged", "scope_name_filed_under_animalia", "name:scope_genus", "scope genus with animal-like name tokens; check")
        return ("excluded", "animal_or_trace_fossil_name", "name:curated_animal", "name or tokens indicate an animal, microfossil or trace fossil filed under a plant lineage")
    if scope_named:
        return ("core", "scope_named_taxon", "name:scope", "genus on the scope list (cards, anchors); lineage gives no further placement")
    if any(SPORE_PATTERN.search(g) or g in SPORE_GENERA for g in gens):
        return ("core", "plant_spore_form_genus", "name:spore_form_genus", "spore form genus by name ending or curated list")
    if kingdom == "plantae" or "plantae" in lineage:
        nm0 = lc(row.get("taxon_accepted") or row.get("taxon_interpreted") or row.get("taxon_recorded"))
        first = nm0.split(" ")[0] if nm0 else ""
        if not nm0 or first in ("plantae", "plant", "plants") or re.search(r"(aceae|ales|ophyta|opsida|phyceae|ineae|idae)$", first):
            return ("flagged", "plantae_unplaced_indeterminate", "lineage:Plantae only, name at family rank or above",
                    "kingdom Plantae and a determination at family rank or above (mostly 'Plantae'); identity unchecked")
        return ("flagged", "plantae_unplaced_named", "lineage:Plantae only, genus or species named",
                "kingdom Plantae with a genus or species name but no phylum or class; plant, alga, acritarch or problematicum unchecked")
    if kingdom == "incertae sedis":
        return ("flagged", "incertae_sedis_kingdom", "lineage:kingdom incertae sedis",
                "source places the name in no kingdom (incertae sedis); plant, alga, trace fossil or animal unchecked")
    if not kingdom and not phylum:
        return ("excluded", "no_lineage_no_plant_evidence", "none", "no kingdom or phylum and no plant evidence in the name")
    return ("excluded", "other_lineage", "lineage:%s" % (kingdom or phylum), "lineage not plant-like")


# ------------------------------------------------------------------ record mappers

COMMON = ["source", "record_id", "gbifID", "occurrenceID", "institutionCode", "collectionCode", "catalogNumber",
          "otherCatalogNumbers", "datasetKey", "datasetName", "publishingOrgKey", "basisOfRecord", "license",
          "rightsHolder", "accessRights", "taxon_recorded", "taxon_recorded_basis", "taxon_interpreted", "taxon_accepted",
          "taxonRank", "taxonomicStatus", "kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet",
          "higherClassification", "typeStatus", "country", "countryCode", "stateProvince", "county", "locality",
          "verbatimLocality", "decimalLatitude", "decimalLongitude", "coordinateUncertaintyInMeters", "eventDate", "year",
          "individualCount", "preparations", "occurrenceRemarks", "references",
          "earliestEonOrLowestEonothem", "latestEonOrHighestEonothem", "earliestEraOrLowestErathem",
          "latestEraOrHighestErathem", "earliestPeriodOrLowestSystem", "latestPeriodOrHighestSystem",
          "earliestEpochOrLowestSeries", "latestEpochOrHighestSeries", "earliestAgeOrLowestStage",
          "latestAgeOrHighestStage", "lowestBiostratigraphicZone", "highestBiostratigraphicZone",
          "lithostratigraphicTerms", "group", "formation", "member", "bed", "geologicalContextID", "media_urls", "n_media",
          "taxon_issue_flags"]
DERIVED = ["derived_licence_class", "derived_licence_class_recordset", "derived_licence_effective", "derived_licence_effective_source", "derived_nc_flag", "derived_class", "derived_subset", "derived_class_basis",
           "derived_class_reason", "derived_window_status", "derived_age_max_ma", "derived_age_min_ma",
           "derived_age_span_myr", "derived_fully_inside_window", "derived_age_basis", "derived_age_note",
           "derived_scope_match", "derived_scope_match_level", "derived_near_scope_name", "derived_found_by",
           "derived_gbif_dataset_idigbio_sourced", "derived_dedupe_key"]


def s(v):
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return " | ".join(str(x) for x in v)
    return str(v).replace("\r", " ").replace("\n", " ")


def gbif_row(r, source, verbatim):
    g = r.get
    row = {c: "" for c in COMMON}
    row.update(source=source, record_id=s(g("key")), gbifID=s(g("gbifID") or g("key")), occurrenceID=s(g("occurrenceID")),
               institutionCode=s(g("institutionCode")), collectionCode=s(g("collectionCode")),
               catalogNumber=s(g("catalogNumber")), otherCatalogNumbers=s(g("otherCatalogNumbers")),
               datasetKey=s(g("datasetKey")), datasetName=s(g("datasetName")), publishingOrgKey=s(g("publishingOrgKey")),
               basisOfRecord=s(g("basisOfRecord")), license=s(g("license")), rightsHolder=s(g("rightsHolder")),
               accessRights=s(g("accessRights")), taxon_interpreted=s(g("scientificName")),
               taxon_accepted=s(g("acceptedScientificName")), taxonRank=s(g("taxonRank")),
               taxonomicStatus=s(g("taxonomicStatus")), kingdom=s(g("kingdom")), phylum=s(g("phylum")),
               **{"class": s(g("class"))}, order=s(g("order")), family=s(g("family")), genus=s(g("genus")),
               specificEpithet=s(g("specificEpithet")), higherClassification=s(g("higherClassification")),
               typeStatus=s(g("typeStatus")), country=s(g("country")), countryCode=s(g("countryCode")),
               stateProvince=s(g("stateProvince")), county=s(g("county")), locality=s(g("locality")),
               verbatimLocality=s(g("verbatimLocality")), decimalLatitude=s(g("decimalLatitude")),
               decimalLongitude=s(g("decimalLongitude")), coordinateUncertaintyInMeters=s(g("coordinateUncertaintyInMeters")),
               eventDate=s(g("eventDate")), year=s(g("year")), individualCount=s(g("individualCount")),
               preparations=s(g("preparations")), occurrenceRemarks=s(g("occurrenceRemarks")),
               references=s(g("references")))
    for k in ("earliestEonOrLowestEonothem", "latestEonOrHighestEonothem", "earliestEraOrLowestErathem",
              "latestEraOrHighestErathem", "earliestPeriodOrLowestSystem", "latestPeriodOrHighestSystem",
              "earliestEpochOrLowestSeries", "latestEpochOrHighestSeries", "earliestAgeOrLowestStage",
              "latestAgeOrHighestStage", "lowestBiostratigraphicZone", "highestBiostratigraphicZone",
              "lithostratigraphicTerms", "group", "formation", "member", "bed", "geologicalContextID"):
        row[k] = s(g(k))
    urls = [m.get("identifier") for m in (g("media") or []) if m.get("identifier")]
    row["media_urls"] = " | ".join(urls)
    row["n_media"] = str(len(urls))
    row["taxon_issue_flags"] = " ".join(i for i in (g("issues") or []) if i.startswith("TAXON_") or i in
                                       ("SCIENTIFIC_NAME_ASSIGNED", "TAXON_MATCH_FUZZY"))
    vb = verbatim.get(row["gbifID"])
    if vb is not None and vb["name"]:
        row["taxon_recorded"] = s(vb["name"])
        row["taxon_recorded_basis"] = "gbif_verbatim_record"
    elif vb is not None and vb["genus"]:
        row["taxon_recorded"] = s((vb["genus"] + " " + vb["epithet"]).strip())
        row["taxon_recorded_basis"] = "gbif_verbatim_record_genus_and_epithet_fields"
        for k, v in vb["higher"].items():
            if v and not row[k]:
                row[k] = s(v)
                row["taxon_issue_flags"] = (row["taxon_issue_flags"] + " VERBATIM_" + k.upper() + "_USED").strip()
        if not row["genus"]:
            row["genus"] = s(vb["genus"])
            row["taxon_issue_flags"] = (row["taxon_issue_flags"] + " VERBATIM_GENUS_USED").strip()
    elif vb is not None:
        row["taxon_recorded"] = ""
        row["taxon_recorded_basis"] = "gbif_verbatim_record_without_taxon_name"
    elif g("verbatimIdentification"):
        row["taxon_recorded"] = s(g("verbatimIdentification"))
        row["taxon_recorded_basis"] = "gbif_verbatimIdentification"
    else:
        row["taxon_recorded"] = s(g("scientificName"))
        row["taxon_recorded_basis"] = "gbif_interpreted_name_not_verbatim" + (
            "_match_issue" if "TAXON_MATCH" in row["taxon_issue_flags"] and "EXACT" not in row["taxon_issue_flags"] else "")
    return row


def idig_row(it):
    d, ix = it["data"], it.get("indexTerms", {})
    idata = ix.get("indexData", {})
    g = d.get
    row = {c: "" for c in COMMON}
    org = ""
    row.update(source="idigbio", record_id=it["uuid"], occurrenceID=s(g("dwc:occurrenceID") or g("id")),
               institutionCode=s(g("dwc:institutionCode")), collectionCode=s(g("dwc:collectionCode")),
               catalogNumber=s(g("dwc:catalogNumber")), otherCatalogNumbers=s(g("dwc:otherCatalogNumbers")),
               datasetKey=s(ix.get("recordset")), datasetName=s(g("dwc:datasetName")), publishingOrgKey="",
               basisOfRecord=s(g("dwc:basisOfRecord")), license=s(g("dcterms:license")),
               rightsHolder=s(g("dcterms:rightsHolder")), accessRights=s(g("dcterms:accessRights")),
               taxon_recorded=s(g("dwc:scientificName")) + (" " + s(g("dwc:scientificNameAuthorship")) if g("dwc:scientificNameAuthorship") and s(g("dwc:scientificNameAuthorship")) not in s(g("dwc:scientificName")) else ""),
               taxon_recorded_basis="idigbio_provider_dwc:scientificName",
               taxon_interpreted=s(idata.get("dwc:scientificName")),
               taxon_accepted=s(ix.get("canonicalname")).capitalize() if ix.get("canonicalname") else "",
               taxonRank=s(idata.get("dwc:taxonRank") or g("dwc:taxonRank")),
               taxonomicStatus=s(idata.get("dwc:taxonomicstatus") or ix.get("taxonomicstatus")),
               kingdom=s(g("dwc:kingdom") or idata.get("dwc:kingdom")), phylum=s(g("dwc:phylum") or idata.get("dwc:phylum")),
               **{"class": s(g("dwc:class") or idata.get("dwc:class"))}, order=s(g("dwc:order") or idata.get("dwc:order")),
               family=s(g("dwc:family") or idata.get("dwc:family")), genus=s(g("dwc:genus") or idata.get("dwc:genus")),
               specificEpithet=s(g("dwc:specificEpithet") or idata.get("dwc:specificEpithet")),
               higherClassification=s(g("dwc:higherClassification")), typeStatus=s(g("dwc:typeStatus")),
               country=s(g("dwc:country")), countryCode=s(ix.get("countrycode")), stateProvince=s(g("dwc:stateProvince")),
               county=s(g("dwc:county")), locality=s(g("dwc:locality")), verbatimLocality=s(g("dwc:verbatimLocality")),
               decimalLatitude=s(g("dwc:decimalLatitude")), decimalLongitude=s(g("dwc:decimalLongitude")),
               coordinateUncertaintyInMeters=s(g("dwc:coordinateUncertaintyInMeters")),
               eventDate=s(g("dwc:eventDate")), year=s(g("dwc:year")), individualCount=s(g("dwc:individualCount")),
               preparations=s(g("dwc:preparations")), occurrenceRemarks=s(g("dwc:occurrenceRemarks")),
               references=s(g("dcterms:references")))
    for k in ("earliestEonOrLowestEonothem", "latestEonOrHighestEonothem", "earliestEraOrLowestErathem",
              "latestEraOrHighestErathem", "earliestPeriodOrLowestSystem", "latestPeriodOrHighestSystem",
              "earliestEpochOrLowestSeries", "latestEpochOrHighestSeries", "earliestAgeOrLowestStage",
              "latestAgeOrHighestStage", "lowestBiostratigraphicZone", "highestBiostratigraphicZone",
              "lithostratigraphicTerms", "group", "formation", "member", "bed", "geologicalContextID"):
        row[k] = s(g("dwc:" + k))
    row["media_urls"] = ""        # filled from mediarecords where fetched
    row["n_media"] = str(len(ix.get("mediarecords") or []))
    row["_media_uuids"] = list(ix.get("mediarecords") or [])
    fl = ix.get("flags") or []
    row["taxon_issue_flags"] = " ".join(f for f in fl if "taxon" in f)
    return row


# ------------------------------------------------------------------ main pipeline

def read_pages(dirpath, pattern="*.json"):
    for fp in sorted(glob.glob(os.path.join(dirpath, pattern))):
        try:
            yield fp, json.load(open(fp))
        except json.JSONDecodeError:
            print("WARNING unreadable page skipped:", fp, file=sys.stderr)


def qgroup_map(dirpath):
    m = {}
    qf = os.path.join(dirpath, "queries.tsv")
    if os.path.exists(qf):
        for line in open(qf, encoding="utf-8").read().splitlines()[1:]:
            p = line.split("\t")
            m[p[0]] = p[1]
    return m


def found_by(fp, qmap):
    base = os.path.basename(fp)
    qid = base.rsplit("__", 1)[0]
    # partitioned pages carry a _dsXXXXXXXX suffix
    qid = re.sub(r"_ds[0-9a-f]{8}$", "", qid)
    grp = qmap.get(qid, "")
    if grp in ("period", "epoch", "stage", "text"):
        return grp
    return "name" if qid.startswith("name_") else grp


def dedupe_norm(x):
    return re.sub(r"[^a-z0-9]", "", (x or "").lower())


OPEN = {"CC0", "CC-BY", "CC-BY-NC"}
WINDOW_CANDIDATE = {"in_window", "anchor_late_devonian"}


def run(args):
    out = args["out"]
    sp_dir, lo_dir = os.path.join(out, "specimens"), os.path.join(out, "local_specimens")
    os.makedirs(sp_dir, exist_ok=True)
    os.makedirs(lo_dir, exist_ok=True)
    load_timescale(args["timescale"])
    build_intervals()
    scope = Scope(args["scope"])
    stats = collections.OrderedDict()

    verbatim, datasets, orgs, media, recordsets = {}, {}, {}, {}, {}
    gdirs = [d for d in (args.get("gbif") or "").split(",") if d]
    for gd in gdirs:
        for fp in glob.glob(os.path.join(gd, "verbatim", "*.json")):
            d = json.load(open(fp))
            key = os.path.basename(fp).split("__")[0].replace("verbatim_", "")
            T = "http://rs.tdwg.org/dwc/terms/"
            verbatim[key] = {"name": d.get(T + "scientificName") or d.get(T + "verbatimIdentification") or "",
                             "genus": d.get(T + "genus") or "", "epithet": d.get(T + "specificEpithet") or "",
                             "higher": {k: d.get(T + k) or "" for k in ("kingdom", "phylum", "class", "order", "family")}}
        for fp in glob.glob(os.path.join(gd, "datasets", "dataset_*.json")):
            d = json.load(open(fp))
            datasets[d["key"]] = d
        for fp in glob.glob(os.path.join(gd, "datasets", "organization_*.json")):
            d = json.load(open(fp))
            orgs[d["key"]] = d
    idirs = [d for d in (args.get("idigbio") or "").split(",") if d]
    for idr in idirs:
        for fp in glob.glob(os.path.join(idr, "media", "*.json")):
            d = json.load(open(fp))
            media[d["uuid"]] = (d.get("indexTerms", {}).get("accessuri") or d.get("data", {}).get("dcterms:identifier") or "")
        for fp in glob.glob(os.path.join(idr, "recordsets", "*.json")):
            d = json.load(open(fp))
            recordsets[d["uuid"]] = d

    def idig_sourced(ds_key):
        d = datasets.get(ds_key)
        if not d:
            return ""
        o = orgs.get(d.get("publishingOrganizationKey", ""), {})
        blob = " ".join([o.get("title", ""), d.get("title", ""), " ".join(e.get("url", "") for e in d.get("endpoints", []))])
        return "yes" if re.search(r"idigbio", blob, re.I) else "no"

    gbif_raw, ala_raw, idig_raw = {}, {}, {}
    for gd in gdirs:
        qmap = qgroup_map(gd)
        for fp, d in read_pages(gd, "*.json"):
            fb = found_by(fp, qmap)
            for r in d.get("results", []):
                k = str(r["key"])
                if k in gbif_raw:
                    gbif_raw[k][1].add(fb)
                else:
                    gbif_raw[k] = (r, {fb})
    if args.get("ala"):
        for fp, d in read_pages(args["ala"], "[AP][UG]__*__p*__*.json"):
            for r in d.get("results", []):
                ala_raw[str(r["key"])] = (r, {"ala_mirror"})
    for idr in idirs:
        qmap = qgroup_map(idr)
        for fp, d in read_pages(idr, "*.json"):
            fb = found_by(fp, qmap)
            for it in d.get("items", []):
                u = it["uuid"]
                if u in idig_raw:
                    idig_raw[u][1].add(fb)
                else:
                    idig_raw[u] = (it, {fb})
    stats["gbif_unique_records_retrieved"] = len(gbif_raw)
    stats["ala_mirror_unique_records_read"] = len(ala_raw)
    stats["idigbio_unique_records_retrieved"] = len(idig_raw)

    tables = {"gbif": [], "idigbio": [], "ala": []}
    audit = collections.defaultdict(collections.Counter)
    audit_meta = {}
    drop_counts = {k: collections.Counter() for k in tables}
    need_verbatim, need_media = set(), set()
    near_names = collections.defaultdict(collections.Counter)
    near_cache = {}

    def process(rows_in, source, tab):
        for key, (raw, fb) in rows_in.items():
            row = gbif_row(raw, source, verbatim) if source in ("gbif", "ala_mirror") else idig_row(raw)
            row["derived_found_by"] = ",".join(sorted(fb))
            row["derived_licence_class"] = licence_class(row["license"])
            rights = recordsets.get(row["datasetKey"], {}).get("data", {}).get("data_rights", "") if source == "idigbio" else ""
            row["derived_licence_class_recordset"] = licence_class(rights) if rights else ""
            if row["derived_licence_class"] in OPEN:
                row["derived_licence_effective"], row["derived_licence_effective_source"] = row["derived_licence_class"], "record"
            elif row["derived_licence_class_recordset"] in OPEN:
                row["derived_licence_effective"], row["derived_licence_effective_source"] = row["derived_licence_class_recordset"], "recordset"
            else:
                row["derived_licence_effective"], row["derived_licence_effective_source"] = row["derived_licence_class"], ""
            row["derived_nc_flag"] = "yes" if row["derived_licence_effective"] == "CC-BY-NC" else "no"
            row["derived_gbif_dataset_idigbio_sourced"] = idig_sourced(row["datasetKey"]) if source != "idigbio" else ""
            row["_names"] = row_names(row)
            gens = {g for g, e in row["_names"].values()}
            anchor = bool(gens & scope.anchor_genera)
            row.update(derive_age(row, anchor))
            cl, sub, basis, reason = classify(row, scope)
            row["derived_class"], row["derived_subset"], row["derived_class_basis"], row["derived_class_reason"] = cl, sub, basis, reason
            hits = []
            for via, (g, e) in row["_names"].items():
                for r, lv in scope.match(g, e):
                    hits.append((r, lv, via))
            row["derived_scope_match"] = "; ".join(sorted({"%s:%s[%s]" % (r["role"], r["card_slug"] or r["name"], via) for r, _, via in hits}))
            row["derived_scope_match_level"] = "; ".join(sorted({lv for _, lv, _ in hits}))
            nearest = ""
            for g in sorted(gens):
                if g not in near_cache:
                    near_cache[g] = scope.near(g)
                if near_cache[g]:
                    nearest = near_cache[g]
                    break
            near = nearest
            row["derived_near_scope_name"] = near
            ws = row["derived_window_status"]
            undated_named = any(g in scope.undated_ok for g in gens) or (near and near in scope.undated_ok)
            keep = ws in WINDOW_CANDIDATE
            if not keep and ws in ("undated", "coarse_age_only") and undated_named:
                keep = True
                row["derived_window_status"] = "undated_scope_name" if ws == "undated" else "coarse_age_scope_name"
            nm = (row["taxon_accepted"] or row["taxon_interpreted"] or row["taxon_recorded"]).strip() or "(no name)"
            if keep:
                audit[(source, nm)][row["derived_window_status"]] += 1
                m = audit_meta.setdefault((source, nm), {k: collections.Counter() for k in ("class", "subset", "reason", "kingdom", "phylum", "basis")})
                m["class"][cl] += 1
                m["subset"][sub] += 1
                m["reason"][reason] += 1
                m["basis"][basis] += 1
                m["kingdom"][row["kingdom"] or "(none)"] += 1
                m["phylum"][row["phylum"] or "(none)"] += 1
            if not keep:
                drop_counts[tab][ws] += 1
                continue
            if cl == "excluded":
                drop_counts[tab]["taxon_excluded:" + sub] += 1
                continue
            tables[tab].append(row)
            if near and not any(g in scope.genera for g in gens):
                near_names[near][nm] += 1
            if source != "idigbio" and "TAXON_MATCH" in row["taxon_issue_flags"] and row["taxon_recorded_basis"].startswith("gbif_interpreted"):
                need_verbatim.add(row["gbifID"])
            if source == "idigbio":
                need_media.update(row.get("_media_uuids", []))

    process(gbif_raw, "gbif", "gbif")
    process(ala_raw, "ala_mirror", "ala")
    process(idig_raw, "idigbio", "idigbio")

    if args.get("emit_lists"):
        pre = args["emit_lists"]
        open(pre + "_gbif_verbatim_keys.txt", "w").write("\n".join(sorted(need_verbatim)) + "\n")
        open(pre + "_idigbio_media_uuids.txt", "w").write("\n".join(sorted(need_media)) + "\n")
        print("verbatim keys: %d; iDigBio media uuids: %d" % (len(need_verbatim), len(need_media)))
        return

    for row in tables["idigbio"]:
        us = row.pop("_media_uuids", [])
        urls = [media[u] for u in us if media.get(u)]
        row["media_urls"] = " | ".join(urls) if urls else (" | ".join("https://search.idigbio.org/v2/view/mediarecords/" + u for u in us))

    # ---- dedupe
    def keys_for(row):
        k = []
        inst, cat = dedupe_norm(row["institutionCode"]), dedupe_norm(row["catalogNumber"])
        if inst and cat:
            k.append(("inst_catalog", inst + "|" + cat))
        oid = row["occurrenceID"].strip().lower()
        if oid and len(oid) >= 8:
            k.append(("occurrenceID", oid))
        return k
    allrows = tables["gbif"] + tables["ala"] + tables["idigbio"]
    for r in allrows:
        ks = keys_for(r)
        r["derived_dedupe_key"] = ks[0][1] if ks else r["source"] + ":" + r["record_id"]
    parent = list(range(len(allrows)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    index = collections.defaultdict(list)
    for i, r in enumerate(allrows):
        if r["source"] in ("gbif", "ala_mirror"):
            index[("gbifID", r["gbifID"])].append(i)
        for rule, k in keys_for(r):
            index[(rule, k)].append(i)
    fired = collections.defaultdict(set)
    within = collections.Counter()
    for (rule, k), idxs in index.items():
        if len(idxs) < 2:
            continue
        cross = len({allrows[i]["source"] for i in idxs}) > 1
        if not cross:
            within[(allrows[idxs[0]]["source"], rule)] += 1
            if rule != "inst_catalog":
                continue
        for j in idxs[1:]:
            a, b = find(idxs[0]), find(j)
            if a != b:
                parent[b] = a
        for i in idxs:
            fired[i].add(rule if cross else "inst_catalog_within_source")
    groups = collections.defaultdict(list)
    for i in range(len(allrows)):
        groups[find(i)].append(i)
    prec = {"gbif": 0, "ala_mirror": 1, "idigbio": 2}
    merged = []
    comp, ruleset, first_rule = collections.Counter(), collections.Counter(), collections.Counter()
    for idxs in groups.values():
        idxs.sort(key=lambda i: (prec[allrows[i]["source"]], allrows[i]["record_id"]))
        srcs = sorted({allrows[i]["source"] for i in idxs}, key=lambda x: prec[x])
        primary = allrows[idxs[0]]
        comp["+".join(srcs)] += 1
        rs = set().union(*[fired.get(i, set()) for i in idxs])
        if len(idxs) > 1 and len(srcs) > 1:
            ruleset["+".join(sorted(rs))] += 1
            first_rule[next(r for r in ("gbifID", "occurrenceID", "inst_catalog") if r in rs)] += 1
        elif len(idxs) > 1:
            comp["(rows sharing a catalogue key inside one source: %s)" % srcs[0]] += 1
        for pos, i in enumerate(idxs):
            r = dict(allrows[i])
            r["derived_dedupe_key"] = primary["derived_dedupe_key"]
            r["derived_duplicate_of"] = "" if pos == 0 else "%s:%s" % (primary["source"], primary["record_id"])
            r["derived_dedupe_rule"] = "+".join(sorted(rs)) if len(idxs) > 1 else ""
            r["derived_in_gbif"] = "yes" if "gbif" in srcs else "no"
            r["derived_in_ala_mirror"] = "yes" if "ala_mirror" in srcs else "no"
            r["derived_in_idigbio"] = "yes" if "idigbio" in srcs else "no"
            r["derived_n_rows_for_specimen"] = str(len(idxs))
            merged.append(r)
    merged.sort(key=lambda r: (r["derived_dedupe_key"], prec[r["source"]], r["record_id"]))
    stats["dedupe_physical_specimens"] = len(groups)
    stats["dedupe_key_collisions_not_cross_source"] = {"%s|%s" % k: v for k, v in within.items()}
    stats["dedupe_group_composition_by_source_set"] = dict(comp)
    stats["dedupe_cross_source_groups_by_rule_set"] = dict(ruleset)
    stats["dedupe_cross_source_groups_by_strongest_rule"] = dict(first_rule)
    coll = {}
    for tab in ("gbif", "idigbio"):
        c = collections.Counter(r["derived_dedupe_key"] for r in tables[tab] if "|" in r["derived_dedupe_key"])
        coll[tab] = {"keys_shared_by_several_rows_in_one_source": sum(1 for v in c.values() if v > 1),
                     "rows_in_those_keys": sum(v for v in c.values() if v > 1)}
    stats["within_source_catalogue_key_collisions"] = coll
    idsrc = [r for r in tables["gbif"] if r["derived_gbif_dataset_idigbio_sourced"] == "yes"]
    in_idig = {r["derived_dedupe_key"] for r in tables["idigbio"]}
    stats["gbif_rows_from_idigbio_sourced_datasets"] = {"rows": len(idsrc), "matched_to_an_idigbio_row": sum(1 for r in idsrc if r["derived_dedupe_key"] in in_idig)}

    # ---- write
    def write(path, rows, cols):
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore", lineterminator="\n")
            w.writeheader()
            for r in rows:
                w.writerow(r)
    cols = COMMON + DERIVED
    mcols = cols + ["derived_duplicate_of", "derived_dedupe_rule", "derived_in_gbif", "derived_in_ala_mirror", "derived_in_idigbio",
                    "derived_n_rows_for_specimen"]
    isopen = lambda r: r["derived_licence_effective"] in OPEN
    for tab, name in (("gbif", "gbif_specimens.csv"), ("ala", "ala_specimens.csv")):
        write(os.path.join(sp_dir, name), [r for r in tables[tab] if isopen(r)], cols)
        rest = [r for r in tables[tab] if not isopen(r)]
        if rest:
            write(os.path.join(lo_dir, name.replace(".csv", "_licence_unclear.csv")), rest, cols)
        stats["rows_%s_not_open_licence" % tab] = len(rest)
    write(os.path.join(lo_dir, "idigbio_specimens.csv"), tables["idigbio"], cols)
    write(os.path.join(sp_dir, "idigbio_specimens_open_licence.csv"), [r for r in tables["idigbio"] if isopen(r)], cols)
    write(os.path.join(sp_dir, "specimens_merged.csv"), [r for r in merged if isopen(r)], mcols)
    write(os.path.join(lo_dir, "specimens_merged_all.csv"), merged, mcols)

    # ---- dedupe diagnostic by institution (shows where the sources hold records that no key links)
    inst = collections.defaultdict(collections.Counter)
    for r in merged:
        if r["derived_duplicate_of"] == "":
            k = ("gbif" if r["derived_in_gbif"] == "yes" else "") + ("+ala" if r["derived_in_ala_mirror"] == "yes" else "") + ("+idigbio" if r["derived_in_idigbio"] == "yes" else "")
            inst[r["institutionCode"] or "(none)"][k.strip("+") if k else "other"] += 1
    keys = sorted({k for c in inst.values() for k in c})
    drows2 = []
    for i, c in inst.items():
        row = {"institutionCode": i, "n_physical_specimens": sum(c.values())}
        for k in keys:
            row["n_specimens_in_" + k.replace("+", "_and_")] = c.get(k, 0)
        drows2.append(row)
    drows2.sort(key=lambda r: -r["n_physical_specimens"])
    write(os.path.join(sp_dir, "dedupe_by_institution.csv"), drows2, ["institutionCode", "n_physical_specimens"] + ["n_specimens_in_" + k.replace("+", "_and_") for k in keys])

    # ---- filter-name audit
    arows = []
    for (src, nm), c in audit.items():
        m = audit_meta[(src, nm)]
        arows.append({"source": src, "name": nm, "n_records_in_window_candidates": sum(c.values()),
                      "classification": m["class"].most_common(1)[0][0],
                      "classification_mix": "; ".join("%s:%d" % kv for kv in m["class"].most_common()) if len(m["class"]) > 1 else "",
                      "subset": m["subset"].most_common(1)[0][0],
                      "reason": m["reason"].most_common(1)[0][0],
                      "basis": m["basis"].most_common(1)[0][0],
                      "kingdom": "; ".join("%s:%d" % kv for kv in m["kingdom"].most_common(3)),
                      "phylum": "; ".join("%s:%d" % kv for kv in m["phylum"].most_common(3)),
                      "window_status_counts": "; ".join("%s:%d" % kv for kv in sorted(c.items()))})
    arows.sort(key=lambda r: (r["source"], -r["n_records_in_window_candidates"], r["name"]))
    write(os.path.join(sp_dir, "specimen_filter_names.csv"), arows, list(arows[0].keys()))

    # ---- GBIF datasets
    dup_ds = collections.Counter(r["datasetKey"] for r in merged if r["source"] == "gbif" and r["derived_in_idigbio"] == "yes")
    dsrows = collections.Counter()
    for tab in ("gbif", "ala"):
        for r in tables[tab]:
            dsrows[(tab, r["datasetKey"])] += 1
    drows = []
    for k in sorted({k for (_, k) in dsrows}):
        d = datasets.get(k, {})
        o = orgs.get(d.get("publishingOrganizationKey", ""), {})
        drows.append({"datasetKey": k, "title": d.get("title", ""), "doi": d.get("doi", ""), "dataset_licence": d.get("license", ""),
                      "publishingOrganization": o.get("title", ""), "publishingCountry": d.get("publishingCountry", ""),
                      "installationKey": d.get("installationKey", ""), "endpoint_urls": " | ".join(e.get("url", "") for e in d.get("endpoints", []) if e.get("url")),
                      "idigbio_sourced": idig_sourced(k), "n_records_gbif_specimens": dsrows.get(("gbif", k), 0),
                      "n_gbif_rows_also_in_idigbio": dup_ds.get(k, 0),
                      "n_records_ala_mirror_specimens": dsrows.get(("ala", k), 0)})
    drows.sort(key=lambda r: (-r["n_records_gbif_specimens"], -r["n_records_ala_mirror_specimens"]))
    write(os.path.join(sp_dir, "gbif_datasets.csv"), drows, list(drows[0].keys()) if drows else ["datasetKey"])

    # ---- iDigBio recordsets
    rrows = []
    cnt = collections.Counter((r["datasetKey"], r["derived_licence_effective"]) for r in tables["idigbio"])
    for u in sorted({k for (k, _) in cnt}):
        d = recordsets.get(u, {}).get("data", {})
        rrows.append({"recordset_uuid": u, "collection_name": d.get("collection_name", ""), "institution_web_address": d.get("institution_web_address", ""),
                      "recordset_data_rights": d.get("data_rights", ""),
                      "n_rows": sum(v for (k, _), v in cnt.items() if k == u),
                      "n_rows_open_licence_record_or_recordset": sum(v for (k, lc_), v in cnt.items() if k == u and lc_ in OPEN),
                      "n_rows_licence_unclear": sum(v for (k, lc_), v in cnt.items() if k == u and lc_ not in OPEN)})
    rrows.sort(key=lambda r: -r["n_rows"])
    if rrows:
        write(os.path.join(sp_dir, "idigbio_recordsets.csv"), rrows, list(rrows[0].keys()))

    # ---- GBIF backbone placement of the scope names
    bpath = next((os.path.join(gd, "name_matches.tsv") for gd in gdirs if os.path.exists(os.path.join(gd, "name_matches.tsv"))), "")
    if bpath:
        qcount = {}
        for gd in gdirs:
            for line in open(os.path.join(gd, "queries.tsv"), encoding="utf-8").read().splitlines()[1:]:
                p = line.split("\t")
                mm = re.match(r"name_(.+)_taxonKey(\d+)$", p[0])
                if mm:
                    qcount[(mm.group(1), mm.group(2))] = p[3]
        brows = []
        for line in open(bpath, encoding="utf-8").read().splitlines()[1:]:
            p = line.split("\t")
            brows.append({"query_name": p[0], "backbone_usageKey": p[1], "scientificName": p[2], "rank": p[3], "taxonomicStatus": p[4],
                          "kingdom": p[5], "phylum": p[6], "class": p[7], "order": p[8], "family": p[9], "acceptedKey": p[10],
                          "n_fossil_specimen_records_taxonKey": qcount.get((p[0], p[1]), "")})
        write(os.path.join(sp_dir, "gbif_backbone_placement.csv"), brows, list(brows[0].keys()))

    # ---- card taxa summary
    by_gen = collections.defaultdict(list)
    for r in merged:
        for g in {g for g, _ in r["_names"].values()}:
            by_gen[g].append(r)
    srows, irows = [], []
    top = lambda c, n=8: "; ".join("%s:%d" % kv for kv in c.most_common(n))
    for sr in scope.rows:
        if sr["role"] == "card_assemblage" or sr["name_rank"] == "higher":
            continue
        g, e = sr["genus"].lower(), sr["epithet"].lower().replace("-", "")
        sel, via_of = [], {}
        for r in by_gen.get(g, []):
            vias = set()
            for via, (gg, ee) in r["_names"].items():
                if gg == g and (not e or ee == e):
                    vias.add("recorded" if via == "recorded" else "interpreted_or_accepted")
            if vias:
                sel.append(r)
                via_of[id(r)] = vias
        prim, seen_keys = [], set()
        for r in sel:
            if r["derived_dedupe_key"] not in seen_keys:
                seen_keys.add(r["derived_dedupe_key"])
                prim.append(r)
        bysrc = collections.Counter(r["source"] for r in sel)
        ws = collections.Counter(r["derived_window_status"] for r in prim)
        first = lambda r: "; ".join(x for x in (r["earliestPeriodOrLowestSystem"], r["earliestEpochOrLowestSeries"], r["earliestAgeOrLowestStage"]) if x) or "(none)"
        last = lambda r: "; ".join(x for x in (r["latestPeriodOrHighestSystem"], r["latestEpochOrHighestSeries"], r["latestAgeOrHighestStage"]) if x) or "(none)"
        nearc = near_names.get(g, {})
        srows.append({"scope_name": sr["name"], "role": sr["role"], "card_slug": sr["card_slug"], "synonym_of": sr["synonym_of"],
                      "match_level": "species" if e else "genus", "n_rows_gbif": bysrc.get("gbif", 0),
                      "n_rows_ala_mirror": bysrc.get("ala_mirror", 0), "n_rows_idigbio": bysrc.get("idigbio", 0),
                      "n_physical_specimens": len(prim),
                      "n_rows_matched_by_recorded_name_only": sum(1 for r in sel if via_of[id(r)] == {"recorded"}),
                      "n_rows_matched_by_interpreted_or_accepted_name_only": sum(1 for r in sel if via_of[id(r)] == {"interpreted_or_accepted"}),
                      "n_in_window": ws.get("in_window", 0),
                      "n_anchor_late_devonian": ws.get("anchor_late_devonian", 0),
                      "n_undated_or_coarse_age": ws.get("undated_scope_name", 0) + ws.get("coarse_age_scope_name", 0),
                      "n_core": sum(1 for r in prim if r["derived_class"] == "core"), "n_flagged": sum(1 for r in prim if r["derived_class"] == "flagged"),
                      "n_nc_licence": sum(1 for r in prim if r["derived_nc_flag"] == "yes"),
                      "institutions_physical_specimens": top(collections.Counter(r["institutionCode"] or "(none)" for r in prim), 12),
                      "countries": top(collections.Counter(r["country"] or "(none)" for r in prim), 6),
                      "earliest_age_fields_as_given": top(collections.Counter(first(r) for r in prim)),
                      "latest_age_fields_as_given": top(collections.Counter(last(r) for r in prim)),
                      "formations_as_given": top(collections.Counter((r["formation"] or r["lithostratigraphicTerms"] or "(none)") for r in prim), 6),
                      "names_as_recorded": top(collections.Counter(r["taxon_recorded"] for r in prim), 8),
                      "derived_subsets": top(collections.Counter(r["derived_subset"] for r in prim), 4),
                      "near_name_candidates_not_merged": top(nearc, 6) if nearc else ""})
        for src in ("gbif", "ala_mirror", "idigbio"):
            for k, v in collections.Counter(r["institutionCode"] or "(none)" for r in sel if r["source"] == src).most_common():
                irows.append({"scope_name": sr["name"], "role": sr["role"], "card_slug": sr["card_slug"], "source": src,
                              "institutionCode": k, "n_rows": v})
    write(os.path.join(sp_dir, "card_taxa_specimens_summary.csv"), srows, list(srows[0].keys()))
    write(os.path.join(sp_dir, "card_taxa_specimens_by_institution.csv"), irows, ["scope_name", "role", "card_slug", "source", "institutionCode", "n_rows"])

    for tab, rows in tables.items():
        stats["rows_" + tab] = len(rows)
        stats["class_" + tab] = dict(collections.Counter(r["derived_class"] for r in rows))
        stats["subset_" + tab] = dict(collections.Counter(r["derived_subset"] for r in rows))
        stats["window_status_" + tab] = dict(collections.Counter(r["derived_window_status"] for r in rows))
        stats["licence_class_" + tab] = dict(collections.Counter(r["derived_licence_class"] for r in rows))
        stats["licence_effective_" + tab] = dict(collections.Counter("%s (%s)" % (r["derived_licence_effective"], r["derived_licence_effective_source"] or "unclear") for r in rows))
        stats["dropped_" + tab] = dict(drop_counts[tab])
        stats["institutions_" + tab] = dict(collections.Counter(r["institutionCode"] for r in rows).most_common(25))
    stats["rows_merged_all"] = len(merged)
    stats["rows_merged_open_licence"] = sum(1 for r in merged if isopen(r))
    json.dump(stats, open(os.path.join(out, "build_stats.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(stats, indent=1, sort_keys=True))


if __name__ == "__main__":
    a = sys.argv[1:]
    args = {}
    i = 0
    while i < len(a):
        args[a[i].lstrip("-").replace("-", "_")] = a[i + 1]
        i += 2
    run(args)
