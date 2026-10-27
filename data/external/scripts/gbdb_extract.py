"""Extract window plant records and sampling-effort tables from the GBDB snapshot (Xu 2020, Zenodo 4245604).

Usage (on deep-server, after gbdb_xlsx2csv.py has written RAW_DIR/csv/):
  ssh deep-server python3 -I - RAW_DIR OUT_DIR PBDB_OCC_CSV TIMESCALE_CSV < gbdb_extract.py
  RAW_DIR        /data/codex/silurian_plants/raw/gbdb/<UTC stamp>
  OUT_DIR        where the tables are written (copy them to data/external/gbdb/ afterwards)
  PBDB_OCC_CSV   data/eprp/record/pbdb_plant_occurrences.csv (genus lookup for the plant filter)
  TIMESCALE_CSV  data/timescale.csv (age-basis comparison only; no age is changed)

Everything is standard library. Source values are copied unchanged; derived columns are prefixed derived_ and
columns joined from the fossils table are prefixed j_fossils_. GBDB ages are never converted or repaired.
"""
import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

csv.field_size_limit(10**9)
RAW, OUT, PBDB_OCC, TIMESCALE = (Path(a) for a in sys.argv[1:5])
OUT.mkdir(parents=True, exist_ok=True)

WIN_OLD, WIN_YOUNG = 485.0, 383.0          # window: early_age > 383 and late_age < 485 (PBDB rule, strict)
FF_OLD, FF_YOUNG = 383.0, 358.86            # Frasnian + Famennian extension for anchor genera (ICS v2024/12 bounds)
FAMENNIAN_BASE_GBDB = 372.2                  # Frasnian top on GBDB's own scale, used only for a plausibility flag

# ----------------------------------------------------------------------------------------------------------
# Loading
# ----------------------------------------------------------------------------------------------------------


def load(name):
    with open(RAW / "csv" / name, newline="", encoding="utf-8") as fh:
        r = csv.reader(fh)
        header = next(r)
        return header, [row for row in r]


SH, S = load("GBDB_all_sections__Sheet1.csv")
FH, F = load("GBDB_fossils__T_Fossil.csv")
assert all(len(r) == len(SH) for r in S) and all(len(r) == len(FH) for r in F)


def unique_names(header):
    seen, out = collections.Counter(), []
    for h in header:
        out.append(h if seen[h] == 0 else f"{h}.{seen[h]}")
        seen[h] += 1
    return out


SN = unique_names(SH)       # the second 'unit_lithology1A' becomes 'unit_lithology1A.1'
FN = list(FH)
IX = {n: i for i, n in enumerate(SN)}
FX = {n: i for i, n in enumerate(FN)}
N_SEC_COLS = {"section": range(0, 11), "formation": range(11, 15), "age": range(15, 24), "unit": range(24, 55),
              "collection": range(55, 60), "taxon": range(60, 65), "reference": range(65, 72)}


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def norm(s):
    return re.sub(r"[\s ]+", " ", s).strip().lower()


# ----------------------------------------------------------------------------------------------------------
# Names: genus token, binomial parsing
# ----------------------------------------------------------------------------------------------------------
DROP_TOKENS = {"cf.", "cf", "aff.", "aff", "?", "n.", "gen.", "nov.", "sp.", "spp.", "n.sp.", "indet.", "ex", "gr.", "sensu",
               "sp", "spp", "gr", "ssp.", "var."}


def tokens(s):
    s = re.sub(r"\(.*?\)", " ", s)
    s = s.replace("?", " ")
    return [t for t in re.split(r"\s+", s.strip()) if t and t.lower() not in DROP_TOKENS]


def genus_token(g):
    t = tokens(g)
    if not t:
        return ""
    return re.sub(r"[^A-Za-z]", "", t[0])


def epithet_token(sp):
    t = tokens(sp)
    return re.sub(r"[^a-z]", "", t[0].lower()) if t else ""


# ----------------------------------------------------------------------------------------------------------
# Plant filter (matches data/eprp/scripts/record_pbdb.py in intent; GBDB has no taxonomy tree, so GBDB's
# FossilGroup field and name rules stand in for PBDB's lineage)
# ----------------------------------------------------------------------------------------------------------
EMBRYO_GROUP = {
    "Lycopodiophyta": "lycophytes_incl_zosterophylls", "Psilotophyta": "psilophytes_incl_trimerophytes",
    "Equisetophyta": "ferns_cladoxylopsids_sphenophytes", "Filicophyta": "ferns_cladoxylopsids_sphenophytes",
    "Bryophyta": "bryophytes", "Marchantiophyta": "bryophytes", "Anthocerotophyta": "bryophytes",
    "Cycadophyta": "seed_plants", "Coniferophyta": "seed_plants", "Ginkgophyta": "seed_plants",
    "Gnetophyta": "seed_plants", "Magnoliophyta": "seed_plants"}
SPORE_GROUP = {"Sporites": ("dispersed_spores", "dispersed_spore"), "Pollenites": ("dispersed_pollen", "dispersed_pollen")}
FLAG_GROUP = {"Chlorophyta": "green_algae", "Charophyta": "streptophyta_not_embryophyta", "Rhodophyta": "red_algae",
              "Phaeophyta": "algae_unspecified", "Acritarchs": "acritarchs_prasinophytes"}
SEED_LABEL_GROUPS = {"Cycadophyta", "Coniferophyta", "Ginkgophyta", "Gnetophyta", "Magnoliophyta", "Pollenites"}
FLAGGED_SUBSETS = {"green_algae", "streptophyta_not_embryophyta", "red_algae", "algae_unspecified",
                   "acritarchs_prasinophytes", "fungi"}

SPORE_SUFFIX = re.compile(r"(spor(a|ites|is)|triletes|tetras|raletes)$", re.I)
NEMATOPHYTE_NAMES = {"prototaxites", "nematothallus", "nematoplexus", "nematophyton", "nematasketum", "pachytheca", "parka",
                     "protaxites", "pathytheca", "nemadophyton"}
# curated lists copied from data/eprp/scripts/record_pbdb.py (reviewed there 2026-10-26)
CURATED_PLANT = {g.lower() for g in [
    "Aberlemnia", "Anaeurophyton", "Bojophyton", "Eorhynia", "Euomphalopteris", "Hunanodendrum", "Lycopodolica",
    "Minarodendron", "Nemadophyton", "Nematasketum", "Phacelophyton", "Protaxites", "Pathytheca", "Pseudlepidodendron",
    "Enigmophytospora", "Conchulophyton", "Huia", "Palaeogeminella", "Proteolobus", "Nodospora", "Sawdonia",
    "Salopella", "Pachytheca", "Retustoriletes", "Nikitinspoirites", "Camptozonotriltes"]}
EXTRA_SPORE = {g.lower() for g in [
    "Raistrickia", "Trileites", "Cirratriradites", "Chauvinia", "Hispanaediscus", "Laevolancis", "Artemopyra",
    "Cymbohilates", "Lagenicula", "Honseleria", "Dyadospora", "Pseudodyadospora", "Cheilotetras", "Emphanisporites",
    "Cristatisporites", "Cystosporites", "Ancyrospora", "Samarasporites"]}
CURATED_ALGAL = {g.lower() for g in ["Paleooedogonium", "Paleoclosterium", "Paleodidymoprium", "Alga", "Algae", "Pheoclosterium"]}
CURATED_FUNGAL = {g.lower() for g in ["Winfrenatia", "Tortotubus", "Ornatifilum", "Palaeomyces", "Palaeoglomus", "Paleoglomus",
                                       "Glomites", "Archaeosporites", "Palaeoendogone", "Rugososporomyces"]}
# GBDB-specific additions from a review of excluded names with a blank or unknown group in the window (2026-10-27);
# plant genera or higher plant names whose group is missing. Calcimicrobes (Ortonella, Garwoodia, Rothpletzella,
# Sphaerocodium, Nuia, Microcodium) stay out, as cyanobacteria do in the PBDB filter.
CURATED_PLANT |= {g.lower() for g in ["Prolepidodendron", "Psilophylites", "Eocladoxylon", "Cycas", "Bennettites", "Artemisia",
                                      "Cyperaceae", "Lygodium", "Desmiophyllum"]}
# project card genera and anchors (taxa/*.md at 2026-10-27; includes cards not yet in taxa/README.md)
CARDS = {
    "aberlemnia-caledonica": dict(genera=["Aberlemnia"], species=[("aberlemnia", "caledonica")], alt=[("cooksonia", "caledonica")]),
    "aglaophyton-majus": dict(genera=["Aglaophyton"], species=[("aglaophyton", "majus"), ("aglaophyton", "major")], alt=[("rhynia", "major"), ("rhynia", "majus")]),
    "ambitisporites": dict(genera=["Ambitisporites"], alt=[("ambitiporites", "*")]),
    "asteroxylon-mackiei": dict(genera=["Asteroxylon"], species=[("asteroxylon", "mackiei")], alt=[("asteroxylon", "mackei")]),
    "baragwanathia-longifolia": dict(genera=["Baragwanathia"], species=[("baragwanathia", "longifolia")], alt=[("baragwanthia", "longifolia")]),
    "baragwanathia-brevifolioides": dict(genera=["Baragwanathia"], species=[("baragwanathia", "brevifolioides")]),
    "cooksonia": dict(genera=["Cooksonia"]),
    "dawsonites": dict(genera=["Dawsonites"]),
    "drepanophycus-spinaeformis": dict(genera=["Drepanophycus"], species=[("drepanophycus", "spinaeformis")]),
    "early-glomeromycotan-fungi": dict(genera=["Palaeoglomus", "Paleoglomus", "Glomites", "Archaeosporites", "Palaeoendogone", "Rugososporomyces"], alt=[("palaeomyces", "*")]),
    "eophyllophyton-bellum": dict(genera=["Eophyllophyton"], species=[("eophyllophyton", "bellum")]),
    "eophytes": dict(genera=["Partitatheca", "Culullitheca", "Fusiformitheca", "Grisellatheca", "Ficoiditheca", "Lenticulatheca"]),
    "franhueberia-gerriennei": dict(genera=["Franhueberia"], species=[("franhueberia", "gerriennei")]),
    "hedeia": dict(genera=["Hedeia"]),
    "horneophyton-lignieri": dict(genera=["Horneophyton"], species=[("horneophyton", "lignieri"), ("hornea", "lignieri")], alt=[("hornea", "*")]),
    "metzgeriothallus-sharonae": dict(genera=["Metzgeriothallus"]),
    "nematothallus": dict(genera=["Nematothallus"], alt=[("nematoplexus", "*"), ("nematasketum", "*")]),
    "nothia-aphylla": dict(genera=["Nothia"]),
    "ordovician-cryptospores": dict(genera=["Tetrahedraletes", "Cryptospora", "Dyadospora", "Pseudodyadospora", "Hispanaediscus", "Laevolancis", "Rimosotetras", "Segestrespora", "Artemopyra", "Cheilotetras", "Velatitetras", "Cymbohilates", "Abditodyadus", "Tetraplanarisporites"], alt=[("tetrahadraletes", "*")]),
    "partitatheca": dict(genera=["Partitatheca"], alt=[("cymbohilates", "*")]),
    "pertica": dict(genera=["Pertica"]),
    "pluricaulis-biformis": dict(genera=["Pluricaulis"]),
    "prototaxites": dict(genera=["Prototaxites"], alt=[("protaxites", "*")]),
    "psilophyton": dict(genera=["Psilophyton"]),
    "renalia-hueberi": dict(genera=["Renalia"], species=[("renalia", "hueberi")]),
    "rhynia-gwynne-vaughanii": dict(genera=["Rhynia"], species=[("rhynia", "gwynnevaughanii"), ("rhynia", "gwynnevaughani")], alt=[("rhynia", "major")]),
    "rhynie-chert-gametophytes": dict(genera=["Lyonophyton", "Langiophyton", "Kidstonophyton", "Remyophyton"]),
    "riccardiothallus-devonicus": dict(genera=["Riccardiothallus"]),
    "salopella": dict(genera=["Salopella"]),
    "sawdonia-ornata": dict(genera=["Sawdonia"], species=[("sawdonia", "ornata")]),
    "tortotubus-protuberans": dict(genera=["Tortotubus"], species=[("tortotubus", "protuberans")], alt=[("ornatifilum", "lornensis")]),
    "winfrenatia-reticulata": dict(genera=["Winfrenatia"], species=[("winfrenatia", "reticulata")]),
    "yarravia": dict(genera=["Yarravia"]),
    "zosterophyllum": dict(genera=["Zosterophyllum"]),
}
ANCHORS = ["Archaeopteris", "Callixylon", "Eospermatopteris", "Wattieza", "Elkinsia", "Leclercqia"]
TARGETS = {slug: {"kind": "card", **d} for slug, d in CARDS.items()}
for a in ANCHORS:
    TARGETS["anchor:" + a.lower()] = {"kind": "anchor", "genera": [a]}
GENUS2TARGETS = collections.defaultdict(set)
ALT2TARGETS = collections.defaultdict(set)
for slug, d in TARGETS.items():
    for g in d["genera"]:
        GENUS2TARGETS[g.lower()].add(slug)
    for g, e in d.get("alt", []):
        ALT2TARGETS[g].add(slug)
ANCHOR_GENERA = {a.lower() for a in ANCHORS}
CARD_GENERA = {g.lower() for d in CARDS.values() for g in d["genera"]}
CURATED_PLANT |= CARD_GENERA - CURATED_FUNGAL - {"palaeomyces"}   # card genera count as plant evidence in unlabelled groups

# PBDB genus lookup from the project's PBDB window extract (record/pbdb_plant_occurrences.csv)
_c = collections.defaultdict(collections.Counter)
_m = collections.defaultdict(collections.Counter)
with open(PBDB_OCC, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        g = r["d_genus"].strip().lower()
        if g:
            _c[g][r["d_subset"]] += 1
            if r["d_in_core"] == "yes":
                _m[g][r["d_major_group"]] += 1
PBDB_SUBSET = {g: c.most_common(1)[0][0] for g, c in _c.items()}
PBDB_MAJOR = {g: c.most_common(1)[0][0].removeprefix("pbdb_") for g, c in _m.items()}
PBDB_CORE_SUBSETS = {"embryophyta_pbdb_tree", "plantae_unplaced_pbdb_tree", "plant_unlinked_organ", "plant_unlinked_name"}


# dominant GBDB group of each genus over rows that carry a group: lets blank-group rows inherit it
_gm = collections.defaultdict(collections.Counter)
for _r in S:
    if _r[IX["genusname"]] and _r[IX["FossilGroup"]] not in ("", "unknown"):
        _gm[genus_token(_r[IX["genusname"]]).lower()][_r[IX["FossilGroup"]]] += 1
GMODE = {}
for _g, _c2 in _gm.items():
    _dg, _n = _c2.most_common(1)[0]
    GMODE[_g] = (_dg, _n / sum(_c2.values()), sum(_c2.values()))


def classify(group, gtok, ttype):
    """(subset, in_core, basis, major_group, record_type, group_conflict, reason) or None if excluded"""
    g = gtok.lower()
    if g in NEMATOPHYTE_NAMES:
        return ("nematophyte_name", "yes", "name_curated_nematophyte", "nematophytes_and_thalloid_problematica",
                "plant_organ_or_megafossil" if not SPORE_SUFFIX.search(g) else "unspecified",
                "no" if group in ("", "unknown") else "yes", f"nematophyte or thalloid problematicum by name; GBDB group '{group}'")
    if g in CURATED_FUNGAL:
        return ("fungi", "no", "name_curated_fungal", "fungi", "unspecified", "yes" if group not in ("", "unknown") else "no",
                f"curated fungal genus; GBDB group '{group}'")
    pb = PBDB_SUBSET.get(g)
    if group in EMBRYO_GROUP:
        major = PBDB_MAJOR.get(g, EMBRYO_GROUP[group])
        return ("embryophyta_gbdb_group", "yes", f"gbdb_group:{group}", major, "plant_organ_or_megafossil", "no",
                f"GBDB group {group}")
    if group in SPORE_GROUP:
        major, rtype = SPORE_GROUP[group]
        return ("dispersed_spore_pollen_gbdb_group", "yes", f"gbdb_group:{group}", major, rtype, "no", f"GBDB group {group}")
    if group in FLAG_GROUP:
        if pb in PBDB_CORE_SUBSETS:
            return ("plant_pbdb_genus_lookup", "yes", "pbdb_genus_lookup", PBDB_MAJOR.get(g, "plantae_other_or_indet"),
                    "unspecified", "yes", f"genus is core in PBDB filter ({pb}); GBDB group {group} is algal or acritarch")
        if pb in FLAGGED_SUBSETS and pb != FLAG_GROUP[group]:
            return (pb, "no", "pbdb_genus_lookup", pb, "unspecified", "yes",
                    f"genus is {pb} in PBDB filter; GBDB group {group} would give {FLAG_GROUP[group]}")
        return (FLAG_GROUP[group], "no", f"gbdb_group:{group}", FLAG_GROUP[group], "unspecified", "no", f"GBDB group {group}")
    # group is not a plant group: animals, unknown, blank, trace fossils, chitinozoa, dinoflagellates, cyanobacteria
    if pb:
        if pb in PBDB_CORE_SUBSETS:
            return ("plant_pbdb_genus_lookup", "yes", "pbdb_genus_lookup", PBDB_MAJOR.get(g, "plantae_other_or_indet"),
                    "dispersed_spore" if SPORE_SUFFIX.search(g) or g in EXTRA_SPORE else "unspecified",
                    "no" if group in ("", "unknown") else "yes", f"genus is core in PBDB filter ({pb}); GBDB group '{group}'")
        return (pb, "no", "pbdb_genus_lookup", pb, "unspecified", "no" if group in ("", "unknown") else "yes",
                f"genus is {pb} in PBDB filter; GBDB group '{group}'")
    if group in ("", "unknown"):
        dg, dshare, dn = GMODE.get(g, ("", 0, 0))
        if dshare >= 0.8 and (dg in EMBRYO_GROUP or dg in SPORE_GROUP or dg in FLAG_GROUP):
            sub, core, basis, major, rtype, _, _r = classify(dg, gtok, ttype)
            return (sub, core, f"inferred_group_from_genus:{dg}", major, rtype, "no",
                    f"GBDB group '{group}' (blank or unknown); genus is recorded under {dg} in {dshare:.0%} of {dn} labelled GBDB rows")
        if g in CURATED_ALGAL:
            return ("algae_unspecified", "no", "name_curated_algal", "algae_unspecified", "unspecified", "no", "curated algal name")
        if g in CURATED_PLANT:
            return ("plant_unlinked_name", "yes", "name_curated", "plantae_other_or_indet", "unspecified", "no", "curated plant genus (PBDB list plus project card genera)")
        if g in EXTRA_SPORE or SPORE_SUFFIX.search(g):
            return ("plant_unlinked_name", "yes", "name_spore_form_genus", "dispersed_spores", "dispersed_spore", "no",
                    "spore form-genus ending or listed spore genus; no GBDB group")
    elif g in CURATED_PLANT and ttype not in ("family", "order", "class", "phylum-division", "superfamily", "subfamily"):
        return ("plant_unlinked_name", "yes", "name_curated", "plantae_other_or_indet", "unspecified", "yes",
                f"curated plant genus under GBDB group '{group}'")
    return None


_CACHE = {}


def classify_cached(group, gtok, ttype):
    k = (group, gtok.lower(), ttype)
    if k not in _CACHE:
        _CACHE[k] = classify(group, gtok, ttype)
    return _CACHE[k]


# Effort groups for the all-sections table (everything that is not a plant by the filter)
EFFORT = {
    "graptolites": {"Graptolithina (Hemichordata)", "Enteropneusta (Hemichordata)"},
    "conodonts": {"Conodonta"},
    "brachiopods": {"Brachiopoda"},
    "trilobites": {"Trilobitomorpha (Arthropoda)"},
    "molluscs": {"Bivalvia (Mollusca)", "Cephalopoda (Mollusca)", "Gastropoda (Mollusca)", "Hyolitha (Mollusca)", "Tentaculita (Mollusca)",
                 "Monoplacophora (Mollusca)", "Polyplacophora (Mollusca)", "Scaphopoda (Mollusca)", "Rostroconchia (Mollusca)",
                 "Aplacophora (Mollusca)"},
    "corals_sponges_stromatoporoids": {"Anthozoa (Cnidaria)", "Hydrozoa (Cnidaria)", "Cubozoa (Cnidaria)", "Scyphozoa (Cnidaria)",
                                       "Staurozoa (Cnidaria)", "Porifera", "Stromatoporoids", "Archaeocyatha"},
    "other_invertebrates": {"Bryozoa/Ectoprocta", "Crustacea (Arthropoda)", "Annelida", "Chelicerata (Arthropoda)", "Hexapoda (Arthropoda)",
                            "Myriapoda (Arthropoda)", "Crinozoa (Echinodermata)", "Echinozoa (Echinodermata)", "Blastozoa (Echinodermata)",
                            "Asterozoa (Echinodermata)", "Acanthocephala", "Rotifera", "Chaetognatha", "Ctenophora", "Cycliophora",
                            "Gastrotrichia", "Placozoa", "small shelly fossil", "Cephalochordata (Chordata)", "Urochordata (Chordata)"},
    "vertebrates": {"Agnatha (Vertebrata)", "Placodermi (Vertebrata)", "Acanthodii (Vertebrata)", "Chondrichthyes (Vertebrata)",
                    "Osteichthyes (Vertebrata)", "Amphibia (Vertebrata)", "Reptilia (Vertebrata)", "Aves (Vertebrata)", "Mammalia (Vertebrata)"},
    "microfossils_other": {"Foraminifera", "Radiolaria", "Coccoliths", "Ciliophora", "Sarcomastigophora", "Apicomplexa", "Amoebozoa",
                           "Mycetozoa", "Bacillariophyta/Diatoms", "Chrysophyta", "Xanthophyceae", "Euglenophyta", "Cryptophyta", "Microspora"},
    "chitinozoa_dinoflagellates": {"Chitinozoa", "Dinoflagellata"},
    "trace_fossils": {"Trace fossils"},
    "cyanobacteria_stromatolites": {"Cyanophyta/Stromatolites", "Prochlorophyta"},
}
EFFORT_OF = {g: k for k, v in EFFORT.items() for g in v}
EFFORT_KEYS = list(EFFORT) + ["plants_core", "plants_flagged", "unknown_or_unlabelled"]

# Region: province-based, approximate (inference). South China block = Yangtze + Cathaysia.
SOUTH_CHINA = {"yunnan", "guizhou", "sichuan", "chongqing", "hubei", "hunan", "jiangxi", "zhejiang", "anhui", "jiangsu", "shanghai",
               "fujian", "guangdong", "guangxi", "hainan"}


def region(country, province):
    if country == "China":
        p = re.sub(r"[^a-z]", "", province.lower())
        return "China: South China (province-based)" if p in SOUTH_CHINA else "China: other blocks (province-based)"
    return country or "(none)"


PERIOD_HINTS = [("Cambrian", r"cambrian|寒武"), ("Ordovician", r"ordovician|奥陶"), ("Silurian", r"silurian|志留"),
                ("Devonian", r"devonian|泥盆"), ("Carboniferous", r"carboniferous|石炭"), ("Permian", r"permian|二叠"),
                ("Triassic", r"triassic|三叠"), ("Jurassic", r"jurassic|侏罗"), ("Cretaceous", r"cretaceous|白垩"),
                ("Cenozoic", r"tertiary|cenozoic|paleogene|neogene|quaternary|第三|新生|古近|新近|第四|miocene|eocene|oligocene|pliocene|pleistocene")]
PERIOD_RE = [(n, re.compile(p, re.I)) for n, p in PERIOD_HINTS]


def period_hints(*texts):
    t = " ".join(texts)
    return ";".join(n for n, rx in PERIOD_RE if rx.search(t))


def coords(lat_s, lon_s, latdir, londir):
    lat, lon = fnum(lat_s), fnum(lon_s)
    if lat is None or lon is None:
        return "", "", "missing"
    flags = []
    if abs(lat) > 90 or abs(lon) > 180:
        flags.append("out_of_range")
    if lat == 0 and lon == 0:
        flags.append("zero_zero")
    if (latdir == "South" and lat > 0) or (latdir == "North" and lat < 0):
        flags.append("lat_direction_conflict")
    if (londir == "West" and lon > 0) or (londir == "East" and lon < 0):
        flags.append("lon_direction_conflict")
    ok = "out_of_range" not in flags and "zero_zero" not in flags
    return (lat if ok else ""), (lon if ok else ""), ";".join(flags)


# ----------------------------------------------------------------------------------------------------------
# Pass 1: per-row derivations on the sections table
# ----------------------------------------------------------------------------------------------------------
I = IX
c_gen, c_sp, c_suf, c_grp, c_tt = I["genusname"], I["speciesname"], I["speciesname_suffix"], I["FossilGroup"], I["TaxonType"]
c_ea, c_la = I["early_age"], I["late_age"]

seen_digest = {}
dup_of = [0] * len(S)             # xlsx row (1-based, header = row 1) of the first identical row, 0 if first/unique
for n, row in enumerate(S):
    d = hashlib.md5("\x1f".join(row).encode("utf-8")).digest()
    first = seen_digest.setdefault(d, n + 2)
    dup_of[n] = 0 if first == n + 2 else first

rowinfo = [None] * len(S)           # per taxon row: (cls, gtok, ea, la)
for n, row in enumerate(S):
    ea, la = fnum(row[c_ea]), fnum(row[c_la])
    gtok = genus_token(row[c_gen]) if row[c_gen] else ""
    cls = classify_cached(row[c_grp], gtok, row[c_tt]) if gtok else None
    rowinfo[n] = (cls, gtok, ea, la)


# genus-level age profile across all aged rows (used only to flag doubtful window records; nothing is repaired)
gprof = collections.defaultdict(lambda: [0, 0, 0, 0])     # n_aged, n_younger_than_window, n_in_window, n_older
for n, row in enumerate(S):
    cls, gtok, ea, la = rowinfo[n]
    if not gtok or ea is None or dup_of[n]:
        continue
    p = gprof[gtok.lower()]
    p[0] += 1
    if ea <= WIN_YOUNG:
        p[1] += 1
    elif la >= WIN_OLD:
        p[3] += 1
    else:
        p[2] += 1


# formation entries holding seed-plant or pollen labelled records that GBDB dates entirely before the Famennian
BAD_FORMS = set()
for n, row in enumerate(S):
    cls, gtok, ea, la = rowinfo[n]
    if cls and row[c_grp] in SEED_LABEL_GROUPS and cls[3] in ("seed_plants", "dispersed_pollen") and la is not None and la > FAMENNIAN_BASE_GBDB \
            and gtok.lower() not in PBDB_SUBSET:
        BAD_FORMS.add(row[I["fromation_id"]])


def window_status(ea, la, anchor):
    if ea is None or la is None:
        return "no_age", ""
    if ea > WIN_YOUNG and la < WIN_OLD:
        return "window", "window"
    if anchor and ea > FF_YOUNG and la < FF_OLD:
        return "anchor_ff", "anchor_ff"
    return "outside", ""


# fossils-table index for the join (plant-relevant rows get matched by section, collection, formation, genus, epithet)
fidx = collections.defaultdict(list)
for r in F:
    g = genus_token(r[FX["fossil species"]])
    k = (norm(r[FX["SectionName"]]), norm(r[FX["Collection"]]), norm(r[FX["Formation"]]), g.lower(),
         epithet_token(" ".join(tokens(r[FX["fossil species"]])[1:2])))
    fidx[k].append(r)
fossil_matched = set()


def fossils_join(row, gtok):
    k = (norm(row[I["SectionName"]]), norm(row[I["CollectionNo"]]), norm(row[I["Formation_name"]]), gtok.lower(), epithet_token(row[c_sp]))
    hits = fidx.get(k, [])
    for h in hits:
        fossil_matched.add(h[0])
    return hits


# ----------------------------------------------------------------------------------------------------------
# Output 1: window plant fossils (+ anchors in FF) and no-age candidates
# ----------------------------------------------------------------------------------------------------------
rec_cols = [SN[i] for r in ("section", "formation", "age") for i in N_SEC_COLS[r]] + \
           ["unit_id", "unit_no"] + [SN[i] for r in ("collection", "taxon", "reference") for i in N_SEC_COLS[r]]
rec_idx = [IX[c] for c in rec_cols]
DER = ["derived_sections_xlsx_row", "derived_exact_duplicate_of_row", "derived_taxon_as_recorded", "derived_genus", "derived_subset",
       "derived_in_core", "derived_basis", "derived_major_group", "derived_record_type", "derived_group_conflict", "derived_reason",
       "derived_flag", "derived_window_basis", "derived_span_myr", "derived_overlap_with_window_myr", "derived_fully_inside_window",
       "derived_lat", "derived_lon", "derived_coord_flag", "derived_region", "derived_card_or_anchor", "derived_ref_period_hints",
       "derived_genus_in_pbdb_window_extract", "derived_genus_n_aged_rows_gbdb", "derived_genus_share_aged_rows_younger_than_window"]
JOIN = ["j_fossils_ids", "j_fossils_n_matches", "j_fossils_species_string", "j_fossils_depth", "j_fossils_ref_authors", "j_fossils_enterer"]


def row_derived(n, row, info, window_basis):
    cls, gtok, ea, la = info
    subset, core, basis, major, rtype, conflict, reason = cls
    taxon = " ".join(t for t in (row[c_gen], row[c_sp], row[c_suf]) if t)
    span = (ea - la) if ea is not None and la is not None else ""
    ov = max(0.0, min(ea, WIN_OLD) - max(la, WIN_YOUNG)) if ea is not None else ""
    inside = ("yes" if (ea <= WIN_OLD and la >= WIN_YOUNG) else "no") if ea is not None else ""
    flag = ""
    flags = []
    if row[c_grp] in SEED_LABEL_GROUPS and major in ("seed_plants", "dispersed_pollen") and la is not None and la > FAMENNIAN_BASE_GBDB \
            and gtok.lower() not in PBDB_SUBSET:
        flags.append("seed_plant_or_pollen_group_label_but_GBDB_age_entirely_older_than_Famennian")
    dg, dshare, dn = GMODE.get(gtok.lower(), ("", 0, 0))
    if dn >= 3 and dshare >= 0.8 and not (dg in EMBRYO_GROUP or dg in SPORE_GROUP or dg in FLAG_GROUP):
        flags.append("genus_mostly_recorded_under_a_non_plant_GBDB_group")
    gp = gprof.get(gtok.lower(), [0, 0, 0, 0])
    in_pbdb = gtok.lower() in PBDB_SUBSET
    share = (gp[1] / gp[0]) if gp[0] else ""
    if gp[0] >= 5 and share != "" and share >= 0.8 and rtype not in ("dispersed_spore", "dispersed_pollen"):
        flags.append("genus_mostly_dated_younger_than_window_elsewhere_in_GBDB")
    if row[I["fromation_id"]] in BAD_FORMS and "seed_plant_or_pollen_group_label_but_GBDB_age_entirely_older_than_Famennian" not in flags:
        flags.append("formation_entry_also_holds_seed_plant_or_pollen_labelled_records_dated_older_than_Famennian")
    flag = ";".join(flags)
    lat, lon, cflag = coords(row[I["LatitudeDecimal"]], row[I["LongitudeDecimal"]], row[I["LatitudeDirection"]], row[I["LongitudeDirection"]])
    targets = set(GENUS2TARGETS.get(gtok.lower(), ()))
    ep = epithet_token(row[c_sp])
    for g, e in ((gtok.lower(), ep),):
        for slug in ALT2TARGETS.get(g, ()):
            alts = TARGETS[slug].get("alt", [])
            if any(a == g and (b == "*" or b == e) for a, b in alts):
                targets.add(slug + "(alt)")
    return [n + 2, dup_of[n] or "", taxon, gtok, subset, core, basis, major, rtype, conflict, reason, flag, window_basis,
            f"{span:.2f}" if span != "" else "", f"{ov:.2f}" if ov != "" else "", inside, lat, lon, cflag,
            region(row[I["Country"]], row[I["Province"]]), ";".join(sorted(targets)),
            period_hints(row[I["ref_Title"]], row[I["ref_JournalOrBookTitle"]]),
            "yes" if in_pbdb else "no", gp[0], f"{share:.3f}" if share != "" else ""]


def join_cols(hits):
    if not hits:
        return ["", 0, "", "", "", ""]
    ids = ";".join(h[0] for h in hits)
    return [ids, len(hits), " | ".join(sorted({h[FX["fossil species"]] for h in hits})), " | ".join(sorted({h[FX["Depth"]] for h in hits})),
            " | ".join(sorted({h[FX["RefAuthorInfo"]] for h in hits})), " | ".join(sorted({h[FX["Enterer"]] for h in hits}))]


win_rows = []                         # indices of retained window/anchor plant rows
noage_rows = []                       # indices of age-less plant rows kept as candidates
plant_all_rows = collections.Counter()
for n, row in enumerate(S):
    cls, gtok, ea, la = rowinfo[n]
    if cls is None:
        continue
    anchor = gtok.lower() in ANCHOR_GENERA
    st, wb = window_status(ea, la, anchor)
    plant_all_rows[(cls[0], st)] += 1
    if st in ("window", "anchor_ff"):
        win_rows.append((n, wb))
    elif st == "no_age":
        hints = period_hints(row[I["ref_Title"]], row[I["ref_JournalOrBookTitle"]])
        why = []
        if gtok.lower() in CARD_GENERA | ANCHOR_GENERA | NEMATOPHYTE_NAMES:
            why.append("card_anchor_or_nematophyte_genus")
        if (cls[1] == "yes" or cls[0] == "fungi") and any(h in hints.split(";") for h in ("Ordovician", "Silurian", "Devonian")):
            why.append("core_plant_and_reference_title_names_Ordovician_Silurian_or_Devonian")
        if why:
            noage_rows.append((n, ";".join(why)))

win_der = {n: row_derived(n, S[n], rowinfo[n], wb) for n, wb in win_rows}


with open(OUT / "gbdb_plant_fossils.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(rec_cols + DER + JOIN)
    for n, wb in win_rows:
        row = S[n]
        info = rowinfo[n]
        hits = fossils_join(row, info[1])
        w.writerow([row[i] for i in rec_idx] + win_der[n] + join_cols(hits))

with open(OUT / "gbdb_plant_no_age_candidates.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(rec_cols + DER + ["derived_candidate_reason"] + JOIN)
    for n, why in noage_rows:
        row = S[n]
        info = rowinfo[n]
        hits = fossils_join(row, info[1])
        w.writerow([row[i] for i in rec_idx] + row_derived(n, row, info, "no_age") + [why] + join_cols(hits))

# plant-classified fossils-table rows with no sections-table counterpart (no age is available for them)
skeys = {(norm(r[I["SectionName"]]), norm(r[I["CollectionNo"]]), norm(r[I["Formation_name"]]), genus_token(r[c_gen]).lower(), epithet_token(r[c_sp]))
         for r in S if r[c_gen]}
fonly = []
for r in F:
    gtok = genus_token(r[FX["fossil species"]])
    if not gtok:
        continue
    cls = classify_cached(r[FX["FossilGroup"]], gtok, "")
    if cls is None:
        continue
    k = (norm(r[FX["SectionName"]]), norm(r[FX["Collection"]]), norm(r[FX["Formation"]]), gtok.lower(),
         epithet_token(" ".join(tokens(r[FX["fossil species"]])[1:2])))
    if k not in skeys:
        fonly.append((r, gtok, cls))
with open(OUT / "gbdb_plant_fossils_table_only.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(FN + ["derived_genus", "derived_subset", "derived_in_core", "derived_basis", "derived_major_group", "derived_group_conflict",
                     "derived_note"])
    for r, gtok, cls in fonly:
        w.writerow(r + [gtok, cls[0], cls[1], cls[2], cls[3], cls[5], "no counterpart in the sections table; the fossils table carries no age"])

# ----------------------------------------------------------------------------------------------------------
# Output 2: plant sections (all units of every section holding a retained plant record)
# ----------------------------------------------------------------------------------------------------------
plant_secs = {S[n][0] for n, _ in win_rows}
unit_cols = [SN[i] for i in range(0, 55)]
unit_stats = collections.OrderedDict()
unit_first = {}
refs_by_unit = collections.defaultdict(set)
core_win = collections.Counter()
flag_win = collections.Counter()
for n, row in enumerate(S):
    if row[0] in plant_secs:
        k = (row[0], row[I["fromation_id"]], row[I["unit_id"]])
        if k not in unit_first:
            unit_first[k] = n
        refs_by_unit[k].add(row[I["ReferenceID"]])
unit_variants = collections.defaultdict(set)
for n, row in enumerate(S):
    if row[0] in plant_secs:
        k = (row[0], row[I["fromation_id"]], row[I["unit_id"]])
        unit_variants[k].add(tuple(row[i] for i in range(0, 55)))
for n, _ in win_rows:
    row = S[n]
    k = (row[0], row[I["fromation_id"]], row[I["unit_id"]])
    (core_win if rowinfo[n][0][1] == "yes" else flag_win)[k] += (0 if dup_of[n] else 1)
n_variants = sum(1 for v in unit_variants.values() if len(v) > 1)
with open(OUT / "gbdb_plant_sections.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(unit_cols + ["derived_lat", "derived_lon", "derived_coord_flag", "derived_region", "derived_unit_age_status",
                            "derived_unit_overlaps_window", "derived_n_core_plant_records_window_or_anchor",
                            "derived_n_flagged_records_window_or_anchor", "derived_n_taxon_rows_in_unit", "derived_reference_ids"])
    unit_rows = collections.Counter(k for k in ((r[0], r[I["fromation_id"]], r[I["unit_id"]]) for r in S if r[0] in plant_secs))
    for k, n in sorted(unit_first.items(), key=lambda kv: (int(kv[0][0]), kv[1])):
        row = S[n]
        ea, la = fnum(row[c_ea]), fnum(row[c_la])
        lat, lon, cflag = coords(row[I["LatitudeDecimal"]], row[I["LongitudeDecimal"]], row[I["LatitudeDirection"]], row[I["LongitudeDirection"]])
        status = "numeric" if ea is not None and la is not None else "no_age"
        overlaps = ("yes" if ea > WIN_YOUNG and la < WIN_OLD else "no") if status == "numeric" else ""
        w.writerow([row[i] for i in range(0, 55)] + [lat, lon, cflag, region(row[I["Country"]], row[I["Province"]]), status, overlaps,
                                                      core_win[k], flag_win[k], unit_rows[k], ";".join(sorted(refs_by_unit[k]))])

# ----------------------------------------------------------------------------------------------------------
# Output 3: all sections with any window-age unit (sampling effort)
# ----------------------------------------------------------------------------------------------------------
sec = collections.OrderedDict()
for n, row in enumerate(S):
    ea, la = rowinfo[n][2], rowinfo[n][3]
    sid = row[0]
    s = sec.get(sid)
    if s is None:
        s = sec[sid] = {"units": set(), "units_win": set(), "forms": set(), "forms_win": set(), "formnames_win": set(), "refs_win": set(),
                        "ea": [], "la": [], "labels": collections.Counter(), "colls": set(), "n_rows_all": 0, "n_rows_win": 0,
                        "eff": collections.Counter(), "first": n, "units_noage": set(), "n_taxon_all": 0, "plant_win_units": set()}
    uk = (row[I["fromation_id"]], row[I["unit_id"]])
    s["units"].add(uk)
    s["n_rows_all"] += 1
    if ea is None or la is None:
        s["units_noage"].add(uk)
    taxon = bool(row[c_gen]) and not dup_of[n]
    if taxon:
        s["n_taxon_all"] += 1
    if ea is not None and la is not None and ea > WIN_YOUNG and la < WIN_OLD:
        s["units_win"].add(uk)
        s["forms_win"].add(row[I["fromation_id"]])
        s["formnames_win"].add(row[I["Formation_name"]])
        s["ea"].append(ea)
        s["la"].append(la)
        s["n_rows_win"] += 1
        lab = " / ".join(x for x in (row[I["early_interval"]], row[I["intage_max"]], row[I["intage_min"]], row[I["epoch_max"]], row[I["epoch_min"]],
                                     row[I["period_max"]], row[I["emlperiod_max"]]) if x)
        s["labels"][(lab, row[c_ea], row[c_la])] += 1
        s["refs_win"].add(row[I["ReferenceID"]])
        if taxon:
            cls = rowinfo[n][0]
            if cls:
                key = "plants_core" if cls[1] == "yes" else "plants_flagged"
                s["plant_win_units"].add(uk)
            else:
                key = EFFORT_OF.get(row[c_grp], "unknown_or_unlabelled" if row[c_grp] in ("", "unknown") else "other_invertebrates")
            s["eff"][key] += 1
            if row[I["CollectionNo"]]:
                s["colls"].add(row[I["CollectionNo"]])
sec_cols_src = ["sectionID", "SectionName", "Country", "Province", "County", "Village", "Locality", "LatitudeDecimal", "LatitudeDirection",
                "LongitudeDecimal", "LongitudeDirection"]
with open(OUT / "gbdb_window_sections_all.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(sec_cols_src + ["derived_lat", "derived_lon", "derived_coord_flag", "derived_region", "derived_n_units_total",
                               "derived_n_units_window", "derived_n_units_no_age", "derived_n_formations_window", "derived_formation_names_window",
                               "derived_oldest_early_age_window_units", "derived_youngest_late_age_window_units",
                               "derived_age_labels_window_units", "derived_reference_ids_window_units", "derived_n_collections_window_units",
                               "derived_n_taxon_rows_window_units"] + ["derived_n_" + k for k in EFFORT_KEYS] +
              ["derived_n_taxon_rows_all_units", "derived_n_window_units_with_plant_records"])
    n_out = 0
    for sid, s in sec.items():
        if not s["units_win"]:
            continue
        row = S[s["first"]]
        lat, lon, cflag = coords(row[I["LatitudeDecimal"]], row[I["LongitudeDecimal"]], row[I["LatitudeDirection"]], row[I["LongitudeDirection"]])
        labels = "; ".join(f"{lab} [{a}-{b}] x{n}" for (lab, a, b), n in s["labels"].most_common(6))
        w.writerow([row[IX[c]] for c in sec_cols_src] + [lat, lon, cflag, region(row[I["Country"]], row[I["Province"]]), len(s["units"]),
                                                          len(s["units_win"]), len(s["units_noage"]), len(s["forms_win"]),
                                                          "; ".join(sorted(s["formnames_win"])), f"{max(s['ea']):g}", f"{min(s['la']):g}", labels,
                                                          ";".join(sorted(s["refs_win"], key=lambda x: int(x))), len(s["colls"]),
                                                          sum(s["eff"].values())] + [s["eff"][k] for k in EFFORT_KEYS] +
                  [s["n_taxon_all"], len(s["plant_win_units"])])
        n_out += 1

# ----------------------------------------------------------------------------------------------------------
# Output 4: plant filter audit (window + anchor rows), plus excluded names from plant-adjacent groups
# ----------------------------------------------------------------------------------------------------------
aud = collections.OrderedDict()
allc = collections.Counter()
for n, row in enumerate(S):
    gtok = rowinfo[n][1]
    if gtok:
        allc[(row[c_grp], gtok.lower(), "all")] += 1
        if rowinfo[n][2] is None:
            allc[(row[c_grp], gtok.lower(), "noage")] += 1
ADJ = {"", "unknown", "Trace fossils", "Cyanophyta/Stromatolites", "Dinoflagellata", "Chitinozoa"}
ret = {n for n, _ in win_rows}
for n, row in enumerate(S):
    cls, gtok, ea, la = rowinfo[n]
    if not gtok or dup_of[n]:
        continue
    st, _ = window_status(ea, la, gtok.lower() in ANCHOR_GENERA)
    if st not in ("window", "anchor_ff"):
        continue
    if cls is None and row[c_grp] not in ADJ:
        continue
    key = (row[c_gen].strip(), row[c_grp], cls[0] if cls else "(excluded)", cls[2] if cls else "excluded")
    a = aud.setdefault(key, {"cls": cls, "gtok": gtok, "n_win": 0, "n_ff": 0, "secs": set(), "colls": set(), "ea": [], "la": []})
    a["n_win" if st == "window" else "n_ff"] += 1
    a["secs"].add(row[0])
    a["colls"].add((row[0], row[I["CollectionNo"]]))
    a["ea"].append(ea)
    a["la"].append(la)
with open(OUT / "gbdb_plant_filter_names.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["decision", "derived_subset", "derived_basis", "gbdb_fossil_group", "genus_as_recorded", "derived_genus", "derived_major_group",
                "derived_group_conflict", "n_window_records", "n_anchor_ff_records", "n_sections", "n_collections", "oldest_early_age",
                "youngest_late_age", "n_records_all_ages_this_genus_and_group", "n_records_no_age_this_genus_and_group", "reason"])
    for (g_rec, grp, subset, basis), a in sorted(aud.items(), key=lambda kv: (kv[1]["cls"] is None, kv[0][2], kv[0][1], kv[0][0].lower())):
        cls = a["cls"]
        dec = "excluded" if cls is None else ("included_core" if cls[1] == "yes" else "included_flagged")
        reason = cls[6] if cls else f"no plant evidence: GBDB group '{grp}' is not a plant group and the name is not on the PBDB or curated lists"
        w.writerow([dec, subset if cls else "", basis if cls else "", grp, g_rec, a["gtok"], cls[3] if cls else "", cls[5] if cls else "",
                    a["n_win"], a["n_ff"], len(a["secs"]), len(a["colls"]), f"{max(a['ea']):g}", f"{min(a['la']):g}",
                    allc[(grp, a["gtok"].lower(), "all")], allc[(grp, a["gtok"].lower(), "noage")], reason])

# ----------------------------------------------------------------------------------------------------------
# Output 5: card taxa and anchors, genus-level summary and names as recorded
# ----------------------------------------------------------------------------------------------------------
tstat = {t: {"all": 0, "dup": 0, "win": 0, "ff": 0, "noage": 0, "outside": 0, "secs": set(), "secs_win": set(), "ea": [], "la": [], "sc": 0, "sc_n": 0,
             "countries": collections.Counter(), "spec": 0, "hints": collections.Counter(), "noage_secs": set()} for t in TARGETS}
nm = collections.OrderedDict()
for n, row in enumerate(S):
    cls, gtok, ea, la = rowinfo[n]
    if not gtok:
        continue
    gl = gtok.lower()
    ep = epithet_token(row[c_sp])
    hit = set(GENUS2TARGETS.get(gl, ()))
    for slug in ALT2TARGETS.get(gl, ()):
        if any(a == gl and (b == "*" or b == ep) for a, b in TARGETS[slug].get("alt", [])):
            hit.add(slug + "|alt")
    if not hit:
        continue
    st, _ = window_status(ea, la, gl in ANCHOR_GENERA)
    reg = region(row[I["Country"]], row[I["Province"]])
    for h in hit:
        slug, _, alt = h.partition("|")
        t = tstat[slug]
        if alt:
            key = (slug, "alt", " ".join(x for x in (row[c_gen], row[c_sp], row[c_suf]) if x), row[c_grp], row[c_ea], row[c_la], reg, row[I["Country"]], row[I["Province"]])
        else:
            key = (slug, "strict", " ".join(x for x in (row[c_gen], row[c_sp], row[c_suf]) if x), row[c_grp], row[c_ea], row[c_la], reg, row[I["Country"]], row[I["Province"]])
        e = nm.setdefault(key, {"n": 0, "secs": set(), "status": st, "labels": collections.Counter(), "cls": cls[0] if cls else "(not plant by filter)",
                                "dups": 0, "forms": set()})
        e["n"] += 1
        e["dups"] += 1 if dup_of[n] else 0
        e["secs"].add(row[0])
        e["forms"].add(row[I["Formation_name"]])
        e["labels"][row[I["early_interval"]] or row[I["intage_max"]] or row[I["epoch_max"]] or row[I["period_max"]]] += 1
        if alt:
            continue
        if dup_of[n]:
            t["dup"] += 1
            continue
        t["all"] += 1
        t["secs"].add(row[0])
        t["countries"][row[I["Country"]]] += 1
        if reg.startswith("China: South"):
            t["sc"] += 1
        if reg.startswith("China"):
            t["sc_n"] += 1
        t[{"window": "win", "anchor_ff": "ff", "no_age": "noage", "outside": "outside"}[st]] += 1
        if st == "no_age":
            t["noage_secs"].add(row[0])
            for h2 in period_hints(row[I["ref_Title"]], row[I["ref_JournalOrBookTitle"]]).split(";"):
                if h2:
                    t["hints"][h2] += 1
        if st in ("window", "anchor_ff"):
            t["secs_win"].add(row[0])
        if ea is not None:
            t["ea"].append(ea)
            t["la"].append(la)
        sp = TARGETS[slug].get("species", [])
        if any(a == gl and b == ep for a, b in sp):
            t["spec"] += 1
with open(OUT / "gbdb_card_anchor_summary.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["target", "kind", "genera_matched", "n_records_all_ages_excl_exact_duplicates", "n_exact_duplicate_rows", "n_sections",
                "n_records_window", "n_records_anchor_ff", "n_records_outside_window", "n_records_no_age", "n_sections_with_window_or_ff_records",
                "n_sections_with_no_age_records", "n_records_species_level_match", "oldest_early_age_aged_records", "youngest_late_age_aged_records",
                "n_records_in_China", "n_records_South_China_province_based", "countries", "no_age_records_reference_period_hints"])
    for slug, d in TARGETS.items():
        t = tstat[slug]
        w.writerow([slug, d["kind"], "; ".join(d["genera"]), t["all"], t["dup"], len(t["secs"]), t["win"], t["ff"], t["outside"], t["noage"],
                    len(t["secs_win"]), len(t["noage_secs"]), t["spec"] if d.get("species") else "",
                    f"{max(t['ea']):g}" if t["ea"] else "", f"{min(t['la']):g}" if t["la"] else "", t["sc_n"], t["sc"],
                    "; ".join(f"{c or '(none)'} {n}" for c, n in t["countries"].most_common()),
                    "; ".join(f"{h} {n}" for h, n in t["hints"].most_common())])
with open(OUT / "gbdb_card_anchor_names.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["target", "match", "name_as_recorded", "gbdb_fossil_group", "early_age", "late_age", "age_status", "derived_region", "country", "province",
                "formations", "age_labels", "plant_filter_subset", "n_rows", "n_exact_duplicate_rows", "n_sections"])
    for (slug, match, name, grp, ea, la, reg, ctry, prov), e in sorted(nm.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2].lower(), kv[0][4], kv[0][8])):
        w.writerow([slug, match, name, grp, ea, la, e["status"], reg, ctry, prov, "; ".join(sorted(e["forms"]))[:200],
                    "; ".join(f"{k or '(none)'} x{v}" for k, v in e["labels"].most_common(3)), e["cls"], e["n"], e["dups"], len(e["secs"])])

# ----------------------------------------------------------------------------------------------------------
# Output 6: age basis (which numbers GBDB attaches to which names) and field dictionary
# ----------------------------------------------------------------------------------------------------------
ts = []
with open(TIMESCALE, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        ts.append((r["stage"], float(r["base_ma"])))
ts.sort(key=lambda x: -x[1])
proj = {}
for i, (st, base) in enumerate(ts):
    proj[st.lower()] = (base, ts[i + 1][1] if i + 1 < len(ts) else "")   # top of a stage = base of the next younger one
LAB = ["early_interval", "intage_max", "intage_min", "epoch_max", "epoch_min", "period_max", "emlperiod_max"]
pairs = {l: collections.defaultdict(collections.Counter) for l in LAB}
only_one_label = collections.Counter()
for n, row in enumerate(S):
    if row[c_ea] == "":
        continue
    filled = [l for l in LAB if row[I[l]]]
    only_one_label[tuple(filled)] += 1
    for l in filled:
        pairs[l][row[I[l]]][(row[c_ea], row[c_la])] += 1
with open(OUT / "gbdb_age_basis.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["label_field", "label", "n_rows_with_numeric_age", "n_distinct_age_pairs", "modal_early_age", "modal_late_age", "modal_pair_n_rows",
                "other_pairs_top3", "matches_project_stage_name", "project_stage_base_ma", "project_stage_top_ma",
                "modal_early_age_minus_project_base", "modal_late_age_minus_project_top"])
    for l in LAB:
        for lab, c in sorted(pairs[l].items(), key=lambda kv: -sum(kv[1].values())):
            (ea, la), n_ = c.most_common(1)[0]
            p = proj.get(lab.lower())
            dE = f"{float(ea) - p[0]:.2f}" if p and fnum(ea) is not None else ""
            dL = f"{float(la) - p[1]:.2f}" if p and p[1] != "" and fnum(la) is not None else ""
            w.writerow([l, lab, sum(c.values()), len(c), ea, la, n_, "; ".join(f"{a}-{b} x{k}" for (a, b), k in c.most_common(4)[1:]),
                        "yes" if p else "", p[0] if p else "", p[1] if p else "", dE, dL])
with open(OUT / "gbdb_label_field_patterns.tsv", "w") as fo:
    fo.write("filled_label_fields\tn_rows_with_numeric_age\n")
    for k, n_ in only_one_label.most_common():
        fo.write(f"{'+'.join(k)}\t{n_}\n")

with open(OUT / "gbdb_fields.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["table", "workbook_sheet", "column_no", "column_as_in_file", "column_as_used_here", "role", "n_nonblank", "n_distinct", "example_values"])
    roles = {}
    for r, rng in N_SEC_COLS.items():
        for i in rng:
            roles[i] = {"section": "section location", "formation": "formation", "age": "age of the formation (stage names and numeric Ma)",
                        "unit": "stratigraphic unit (lithology, thickness, contact, environment)", "collection": "collection within the unit",
                        "taxon": "taxon of the collection", "reference": "source reference"}[r]
    for i, h in enumerate(SH):
        vals = collections.Counter(r[i] for r in S if r[i] != "")
        w.writerow(["sections", "GBDB_all sections.xlsx / Sheet1", i + 1, h, SN[i], roles[i], sum(vals.values()), len(vals),
                    " | ".join(v[:40] for v, _ in vals.most_common(4))])
    frole = {"ID": "fossil record id", "fossil species": "taxon name as entered, with qualifiers", "FossilGroup": "major group", "SectionName": "section name",
             "Collection": "collection within section", "Country": "location", "Province": "location", "County": "location", "Village": "location",
             "LongitudeDecimal": "coordinate", "LatitudeDecimal": "coordinate", "Formation": "formation name", "Lithology": "lithology",
             "Depth": "depth or position value (not documented; large values in coal sections)", "RefAuthorInfo": "reference authors",
             "RefPublicationYear": "reference year", "RefTitle": "reference title", "RefJournalOrBookTitle": "reference journal or book",
             "Enterer": "GBDB data enterer"}
    for i, h in enumerate(FH):
        vals = collections.Counter(r[i] for r in F if r[i] != "")
        w.writerow(["fossils", "GBDB_fossils.xlsx / T_Fossil", i + 1, h, h, frole.get(h, ""), sum(vals.values()), len(vals),
                    " | ".join(v[:40] for v in [x for x, _ in vals.most_common(4)])])

# ----------------------------------------------------------------------------------------------------------
# Statistics for the README
# ----------------------------------------------------------------------------------------------------------
stats = {
    "sections_rows": len(S), "fossils_rows": len(F), "sections_exact_duplicate_rows": sum(1 for d in dup_of if d),
    "sections_taxon_rows": sum(1 for r in S if r[c_gen]), "sections_taxon_rows_nodup": sum(1 for n, r in enumerate(S) if r[c_gen] and not dup_of[n]),
    "n_sections": len(sec), "n_sections_with_any_numeric_age": sum(1 for s in sec.values() if len(s["units_noage"]) < len(s["units"])),
    "n_window_sections": sum(1 for s in sec.values() if s["units_win"]),
    "n_window_sections_with_plants": sum(1 for s in sec.values() if s["plant_win_units"]),
    "win_plant_rows": len(win_rows), "win_plant_rows_nodup": sum(1 for n, _ in win_rows if not dup_of[n]),
    "win_plant_sections": len(plant_secs), "noage_candidate_rows": len(noage_rows), "fossils_table_only_plant_rows": len(fonly),
    "units_with_variant_unit_fields": n_variants,
    "fossil_rows_matched_to_retained_plant_rows": len({i for n, _ in win_rows for i in join_cols(fossils_join(S[n], rowinfo[n][1]))[0].split(";") if i}),
    "plant_rows_by_subset_and_age_status": {f"{a}|{b}": c for (a, b), c in sorted(plant_all_rows.items())},
}
json.dump(stats, open(OUT / "gbdb_extract_stats.json", "w"), indent=1)
print(json.dumps(stats, indent=1))
