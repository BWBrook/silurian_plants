"""record_pbdb.py: PBDB plant occurrences in the 485-383 Ma window, their collections and references,
the card-taxa summary and counts by interval.

Run on deep-server (stdlib only):  ssh deep-server python3 - < record_pbdb.py
Reads the PBDB global snapshot read-only; writes to OUT (scratch on deep-server). Copy the results
into data/eprp/record/ afterwards. Run record_pbdb.py before record_intervals.py.

Outputs (OUT):
  pbdb_plant_occurrences.csv     all 95 original occurrence columns + d_* derived columns
  pbdb_plant_collections.csv     all 143 original collection columns (second copies of duplicated
                                 headers get a ".1" suffix) + d_* derived columns
  pbdb_plant_references.csv      all 34 original reference columns + d_* derived columns
  pbdb_plant_filter_names.csv    one row per distinct name x subset x basis in the occurrence file
  card_taxa_pbdb_summary.csv     one row per card taxon, whole snapshot (all ages)
  pbdb_plant_counts_by_interval.csv  raw counts by interval, binning rule and major group
"""
import csv
import collections
import glob
import os
import re
import statistics
import sys

csv.field_size_limit(1 << 30)

SNAP = "/data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url/"
OUT = "/data/codex/silurian_plants-eprp/record/out/"
WIN_TOP = 383.0    # Ma, younger edge of the extraction window
WIN_BASE = 485.0   # Ma, older edge

os.makedirs(OUT, exist_ok=True)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------------------------
# PBDB taxonomy (taxa.csv): parent chains in orig_no space
# ---------------------------------------------------------------------------------------------
T = {}                      # orig_no -> dict(name, parent, acc, diff, n)
TNO2ORIG = {}               # taxon_no -> orig_no
with open(SNAP + "taxa.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        o = r["orig_no"]
        TNO2ORIG.setdefault(r["taxon_no"], o)
        if o not in T or r["taxon_no"] == o:
            T[o] = dict(name=r["taxon_name"], parent=r["parent_no"], acc=r["accepted_no"],
                        diff=r["difference"], n=int(r["n_occs"] or 0))
log("taxa", len(T))


def idof(name):
    c = [o for o, t in T.items() if t["name"] == name and t["acc"] == o and not t["diff"]]
    if len(c) != 1:
        c.sort(key=lambda o: -T[o]["n"])
        log("WARN name", name, "candidates", [(o, T[o]["n"], T[T[o]["parent"]]["name"] if T[o]["parent"] in T else "") for o in c])
    return c[0]


ID = {n: idof(n) for n in ["Plantae", "Embryophyta", "Chlorophyta", "Streptophyta", "Charophyta", "Rhodophyta",
                           "Biliphyta", "Algae", "Fungi", "Acritarcha", "Archaeplastida", "Opisthokonta",
                           "Eucarya", "Protozoa", "Chromista", "Chromalveolata", "Rhizopodea", "Chitinozoa",
                           "Bacteria", "Cyanobacteria", "Ichnofossils"]}
log(ID)
_ANC = {}


def ancestors(o):
    """list of orig_no from o to the root, cycle-safe, memoised"""
    if o in _ANC:
        return _ANC[o]
    chain, seen, x = [], set(), o
    while x and x in T and x not in seen:
        seen.add(x)
        chain.append(x)
        x = T[x]["parent"]
    _ANC[o] = chain
    return chain


NON_PLANT_ROOTS = {k: ID[k] for k in ["Opisthokonta", "Eucarya", "Protozoa", "Chromista", "Chromalveolata",
                                      "Rhizopodea", "Chitinozoa", "Bacteria", "Cyanobacteria", "Ichnofossils"]}

# ---------------------------------------------------------------------------------------------
# Name rules for occurrences with no usable position in PBDB's plant tree
# ---------------------------------------------------------------------------------------------
SPORE_SUFFIX = re.compile(r"(spor(a|ites|is)|triletes|tetras|raletes)$", re.I)
EXTRA_SPORE_GENERA = {g.lower() for g in [
    "Raistrickia", "Trileites", "Cirratriradites", "Chauvinia", "Hispanaediscus", "Laevolancis", "Artemopyra",
    "Cymbohilates", "Lagenicula", "Honseleria", "Dyadospora", "Pseudodyadospora", "Cheilotetras", "Emphanisporites",
    "Cristatisporites", "Cystosporites", "Ancyrospora", "Samarasporites"]}
# plant-like genera with neither a PBDB link nor a specific plant_organ nor a spore-form suffix, taken from
# a review of the unlinked names in the window (2026-10-26); each is a megafossil or problematic plant name
CURATED_PLANT_GENERA = {g.lower() for g in [
    "Aberlemnia", "Anaeurophyton", "Bojophyton", "Eorhynia", "Euomphalopteris", "Hunanodendrum", "Lycopodolica",
    "Minarodendron", "Nemadophyton", "Nematasketum", "Phacelophyton", "Protaxites", "Pathytheca", "Pseudlepidodendron",
    "Enigmophytospora", "Conchulophyton", "Huia", "Palaeogeminella", "Proteolobus", "Nodospora", "Sawdonia",
    "Salopella", "Pachytheca", "Retustoriletes", "Nikitinspoirites", "Camptozonotriltes"]}
CURATED_ALGAL_GENERA = {g.lower() for g in ["Paleooedogonium", "Paleoclosterium", "Paleodidymoprium", "Alga", "Algae"]}
CURATED_FUNGAL_GENERA = {g.lower() for g in ["Winfrenatia", "Tortotubus", "Ornatifilum", "Palaeomyces", "Palaeoglomus",
                                              "Paleoglomus", "Glomites", "Archaeosporites", "Palaeoendogone",
                                              "Rugososporomyces"]}
HIGHER_NAME = re.compile(r"(idae|inae|aceae|ales|phyta|phytina|opsida|oidea|ida)$", re.I)
NOT_GENUS = {"plantae", "algae", "alga", "spores", "lycopsids", "psilophyte", "morphotype", "trimerophyte",
             "incertae", "axes", "acritarch", "dasycladae", "fungi"}

PLANT_MACRO_ORGANS = {"axis", "leaf", "root", "cuticle", "wood", "flower", "seed/fruit", "seed repro",
                      "non-seed repro", "multi organs", "plant debris", "fertile axis", "sterile axis"}

CORE = {"embryophyta_pbdb_tree", "plantae_unplaced_pbdb_tree", "plant_unlinked_organ", "plant_unlinked_name"}
FLAGGED_ORDER = ["green_algae", "streptophyta_not_embryophyta", "red_algae", "algae_unspecified",
                 "acritarchs_prasinophytes", "fungi"]


def clean_genus_token(s):
    s = s.strip().strip('"').strip("<>").strip()
    s = re.sub(r"^\?\s*", "", s)
    return s


EXCL = collections.Counter()


def classify(row, ix):
    """returns (subset, basis, lineage_names) or None to exclude"""
    acc, ide = row[ix["accepted_no"]], row[ix["identified_no"]]
    o = ""
    if acc and acc in T:
        o = acc
    elif acc and acc in TNO2ORIG:
        o = TNO2ORIG[acc]
    elif ide and ide != "0":
        o = TNO2ORIG.get(ide, ide if ide in T else "")
    S = set(ancestors(o)) if o else set()
    lineage = " > ".join(T[x]["name"] for x in reversed(ancestors(o))) if o else ""
    if o:
        if ID["Embryophyta"] in S:
            return "embryophyta_pbdb_tree", "pbdb_tree:Embryophyta", lineage
        if ID["Chlorophyta"] in S:
            return "green_algae", "pbdb_tree:Chlorophyta", lineage
        if ID["Streptophyta"] in S or ID["Charophyta"] in S:
            return "streptophyta_not_embryophyta", "pbdb_tree:Streptophyta", lineage
        if ID["Rhodophyta"] in S or ID["Biliphyta"] in S:
            return "red_algae", "pbdb_tree:Rhodophyta", lineage
        if ID["Algae"] in S:
            return "algae_unspecified", "pbdb_tree:Algae", lineage
        if ID["Plantae"] in S:
            return "plantae_unplaced_pbdb_tree", "pbdb_tree:Plantae", lineage
        if ID["Fungi"] in S:
            return "fungi", "pbdb_tree:Fungi", lineage
        if ID["Acritarcha"] in S or ID["Archaeplastida"] in S:
            return "acritarchs_prasinophytes", "pbdb_tree:Acritarcha/Archaeplastida", lineage
        for k, v in NON_PLANT_ROOTS.items():
            if v in S:
                EXCL["tree:" + k] += 1
                return None
    organs = {t.strip() for t in row[ix["plant_organ"]].split(",") if t.strip()}
    specific = organs - {"unassigned", "marine palyn"}
    g = clean_genus_token(row[ix["primary_name"]] or row[ix["identified_name"]].split(" ")[0]).lower()
    g = re.sub(r"[^a-z]", "", g)
    if g in CURATED_FUNGAL_GENERA:
        return "fungi", "name_curated", lineage
    if specific:
        return "plant_unlinked_organ", "plant_organ:" + ",".join(sorted(specific)), lineage
    if "marine palyn" in organs:
        return "acritarchs_prasinophytes", "plant_organ:marine palyn", lineage
    if g in CURATED_ALGAL_GENERA:
        return "algae_unspecified", "name_curated", lineage
    if g in CURATED_PLANT_GENERA:
        return "plant_unlinked_name", "name_curated", lineage
    if g in EXTRA_SPORE_GENERA or SPORE_SUFFIX.search(g):
        return "plant_unlinked_name", "name_spore_form_genus", lineage
    EXCL["no_plant_evidence:" + ("tree_orphan" if o else "unlinked")] += 1
    return None


def record_type(row, ix):
    organs = {t.strip() for t in row[ix["plant_organ"]].split(",") if t.strip()}
    g = re.sub(r"[^a-z]", "", clean_genus_token(row[ix["primary_name"]]).lower())
    if organs & {"microspore", "megaspore"}:
        return "dispersed_spore"
    if (organs - {"unassigned"}) & PLANT_MACRO_ORGANS:
        return "plant_organ_or_megafossil"
    if g in EXTRA_SPORE_GENERA or SPORE_SUFFIX.search(g):
        return "dispersed_spore"
    return "unspecified"


NEMATOPHYTE_NAMES = {"prototaxites", "nematothallus", "nematoplexus", "nematophyton", "nematasketum", "pachytheca",
                     "parka", "protaxites", "pathytheca", "nemadophyton"}
GROUP_BY_ANCESTOR = [
    ("pbdb_lycophytes_incl_zosterophylls", {"Lycopodophyta", "Lycopsida", "Lycophyta", "Lycopodiophyta", "Lycopodiopsida",
                                       "Zosterophyllopsida", "Zosterophyllophyta", "Lycophytina", "Protolepidodendraceae"}),
    ("pbdb_psilophytes_incl_trimerophytes", {"Psilophytophyta", "Psilophytopsida", "Rhyniopsida", "Psilophytales"}),
    ("pbdb_progymnosperms", {"Progymnospermophyta", "Progymnospermopsida", "Aneurophytophyta", "Aneurophytopsida",
                        "Archaeopteridopsida"}),
    ("pbdb_ferns_cladoxylopsids_sphenophytes", {"Cladoxylopsida", "Polypodiopsida", "Pteridopsida", "Pteridophyta",
                                           "Sphenophyta", "Sphenopsida", "Equisetopsida", "Equisetophyta"}),
    ("pbdb_seed_plants", {"Pteridospermophyta", "Lyginopteridopsida", "Cycadophyta", "Cycadopsida", "Coniferophyta",
                     "Pinopsida", "Gymnospermae", "Spermatophyta"}),
    ("pbdb_bryophytes", {"Bryophyta", "Marchantiophyta", "Hepaticae"}),
]


def major_group(subset, rtype, row, ix, lineage):
    if subset not in CORE:
        return subset
    if rtype == "dispersed_spore":
        return "dispersed_spores"
    names = set(lineage.split(" > ")) if lineage else set()
    g = re.sub(r"[^a-z]", "", clean_genus_token(row[ix["primary_name"]]).lower())
    if g in NEMATOPHYTE_NAMES or names & {n.capitalize() for n in NEMATOPHYTE_NAMES}:
        return "nematophytes_and_thalloid_problematica"
    for label, s in GROUP_BY_ANCESTOR:
        if names & s:
            return label
    ph = row[ix["phylum"]]
    for label, s in GROUP_BY_ANCESTOR:
        if ph in s:
            return label
    if names & {"Tracheophyta"} or ph == "Tracheophyta":
        return "pbdb_tracheophyta_other_or_indet"
    return "plantae_other_or_indet"


def derive_genus(row, ix):
    g = row[ix["genus"]]
    if g:
        return g
    pn = clean_genus_token(row[ix["primary_name"]])
    if re.fullmatch(r"[A-Z][a-z]+", pn) and not HIGHER_NAME.search(pn) and pn.lower() not in NOT_GENUS:
        return pn
    return ""


# ---------------------------------------------------------------------------------------------
# Card taxa (taxa/*.md of the consuming project); strict match rules plus alternative names
# searched but not merged
# ---------------------------------------------------------------------------------------------
CARDS = [
    # slug, rank, strict genera, strict species pairs, alt pairs (searched, reported separately)
    dict(slug="aberlemnia-caledonica", genera=["Aberlemnia"], species=[("Aberlemnia", "caledonica")],
         alt=[("Cooksonia", "caledonica")]),
    dict(slug="aglaophyton-majus", genera=["Aglaophyton"], species=[("Aglaophyton", "majus"), ("Aglaophyton", "major")],
         alt=[("Rhynia", "major"), ("Rhynia", "majus")]),
    dict(slug="ambitisporites", genera=["Ambitisporites"], species=[], alt=[]),
    dict(slug="asteroxylon-mackiei", genera=["Asteroxylon"], species=[("Asteroxylon", "mackiei")],
         alt=[("Asteroxylon", "mackei"), ("Asteroxylon", "mackiel")]),
    dict(slug="baragwanathia-longifolia", genera=["Baragwanathia"], species=[("Baragwanathia", "longifolia")],
         alt=[("Baragwanthia", "longifolia"), ("Baragwanthia", "longifolia")]),
    dict(slug="cooksonia", genera=["Cooksonia"], species=[], alt=[]),
    dict(slug="drepanophycus-spinaeformis", genera=["Drepanophycus"], species=[("Drepanophycus", "spinaeformis")], alt=[]),
    dict(slug="early-glomeromycotan-fungi",
         genera=["Palaeoglomus", "Paleoglomus", "Glomites", "Archaeosporites", "Palaeoendogone", "Rugososporomyces"],
         species=[], alt=[("Palaeomyces", "*")]),
    dict(slug="eophyllophyton-bellum", genera=["Eophyllophyton"], species=[("Eophyllophyton", "bellum")], alt=[]),
    dict(slug="horneophyton-lignieri", genera=["Horneophyton"], species=[("Horneophyton", "lignieri"), ("Hornea", "lignieri")],
         alt=[]),
    dict(slug="nematothallus", genera=["Nematothallus"], species=[], alt=[("Nematoplexus", "*"), ("Nematasketum", "*")]),
    dict(slug="ordovician-cryptospores",
         genera=["Tetrahedraletes", "Cryptospora", "Dyadospora", "Pseudodyadospora", "Hispanaediscus", "Laevolancis",
                 "Rimosotetras", "Segestrespora", "Artemopyra", "Cheilotetras", "Velatitetras", "Cymbohilates",
                 "Abditodyadus", "Tetraplanarisporites"],
         species=[], alt=[]),
    dict(slug="partitatheca", genera=["Partitatheca"], species=[], alt=[("Cymbohilates", "*")]),
    dict(slug="pertica", genera=["Pertica"], species=[], alt=[]),
    dict(slug="prototaxites", genera=["Prototaxites"], species=[], alt=[("Protaxites", "*")]),
    dict(slug="psilophyton", genera=["Psilophyton"], species=[], alt=[]),
    dict(slug="renalia-hueberi", genera=["Renalia"], species=[("Renalia", "hueberi")], alt=[]),
    dict(slug="rhynia-gwynne-vaughanii", genera=["Rhynia"], species=[("Rhynia", "gwynnevaughanii"), ("Rhynia", "gwynnevaughani")],
         alt=[("Rhynia", "major")]),
    dict(slug="rhynie-chert-gametophytes", genera=["Lyonophyton", "Langiophyton", "Kidstonophyton", "Remyophyton"],
         species=[], alt=[]),
    dict(slug="riccardiothallus-devonicus", genera=["Riccardiothallus"], species=[("Riccardiothallus", "devonicus")], alt=[]),
    dict(slug="sawdonia-ornata", genera=["Sawdonia"], species=[("Sawdonia", "ornata")], alt=[]),
    dict(slug="tortotubus-protuberans", genera=["Tortotubus"], species=[("Tortotubus", "protuberans")],
         alt=[("Ornatifilum", "lornensis")]),
    dict(slug="winfrenatia-reticulata", genera=["Winfrenatia"], species=[("Winfrenatia", "reticulata")], alt=[]),
    dict(slug="zosterophyllum", genera=["Zosterophyllum"], species=[], alt=[]),
]
CARD_RANK_ASSEMBLAGE = {"early-glomeromycotan-fungi", "ordovician-cryptospores", "rhynie-chert-gametophytes"}
GENUS_CARD = {"ambitisporites", "cooksonia", "nematothallus", "partitatheca", "pertica", "prototaxites", "psilophyton",
              "zosterophyllum"}
GENUS2CARDS = collections.defaultdict(set)
ALT2CARDS = collections.defaultdict(set)
for c in CARDS:
    for g in c["genera"]:
        GENUS2CARDS[g.lower()].add(c["slug"])
    for g, e in c["alt"]:
        ALT2CARDS[g.lower()].add(c["slug"])
    c["spec_set"] = {(g.lower(), e) for g, e in c["species"]}
    c["alt_set"] = {(g.lower(), e) for g, e in c["alt"]}

DROP_TOKENS = {"cf.", "aff.", "?", "n.", "gen.", "nov.", "sp.", "spp.", "n.sp.", "n.", "indet.", "ex", "gr.", "sensu"}


def parse_binomial(s):
    """first genus-like token and second epithet-like token of a name string, lower-cased"""
    toks = [t for t in re.split(r"\s+", s.replace("(", " ").replace(")", " ").strip()) if t]
    toks = [t for t in toks if t.lower() not in DROP_TOKENS]
    if not toks:
        return None
    g = re.sub(r"[^a-z]", "", toks[0].lower())
    e = ""
    if len(toks) > 1:
        e = re.sub(r"[^a-z]", "", toks[1].lower())
    return g, e


def row_pairs(row, ix):
    pairs = set()
    for col in ("identified_name", "accepted_name"):
        s = row[ix[col]]
        if s:
            p = parse_binomial(s)
            if p:
                pairs.add(p)
    pn = clean_genus_token(row[ix["primary_name"]])
    if pn:
        g = re.sub(r"[^a-z]", "", pn.lower())
        e = re.sub(r"[^a-z]", "", row[ix["species_name"]].lower())
        pairs.add((g, e))
    gcol = re.sub(r"[^a-z]", "", row[ix["genus"]].lower())
    if gcol:
        pairs.add((gcol, ""))
    return pairs


# ---------------------------------------------------------------------------------------------
# Pass over all occurrences
# ---------------------------------------------------------------------------------------------
occ_files = sorted(glob.glob(SNAP + "occurrences__p*.csv"))
HEAD = None
IX = None
coll_total = collections.Counter()     # public occurrences per collection, all taxa
n_total = 0
n_noage = 0
n_window_all = 0
plant_rows = []                         # (row, subset, basis, lineage)
card_hits = collections.defaultdict(list)   # slug -> list of dict
card_alt_hits = collections.defaultdict(collections.Counter)
newline_cells_occ = 0

for fpath in occ_files:
    with open(fpath, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        h = next(rd)
        if HEAD is None:
            HEAD = h
            IX = {k: i for i, k in enumerate(h)}
            assert len(set(h)) == len(h), "duplicate occurrence headers"
        assert h == HEAD, fpath
        for row in rd:
            n_total += 1
            coll_total[row[IX["collection_no"]]] += 1
            # card matching, whole snapshot
            pn = clean_genus_token(row[IX["primary_name"]]).lower()
            pn = re.sub(r"[^a-z]", "", pn)
            acc_first = re.sub(r"[^a-z]", "", (row[IX["accepted_name"]].split(" ")[0] if row[IX["accepted_name"]] else "").lower())
            idn_first = (parse_binomial(row[IX["identified_name"]]) or ("", ""))[0]
            gcol = re.sub(r"[^a-z]", "", row[IX["genus"]].lower())
            gset = {pn, acc_first, idn_first, gcol}
            hit_cards = set()
            for g in gset:
                if g in GENUS2CARDS:
                    hit_cards |= GENUS2CARDS[g]
                if g in ALT2CARDS:
                    hit_cards |= ALT2CARDS[g]
            if hit_cards:
                pairs = row_pairs(row, IX)
                for c in CARDS:
                    if c["slug"] not in hit_cards:
                        continue
                    gen_hit = any(g.lower() in {p[0] for p in pairs} for g in c["genera"])
                    spec_hit = bool(pairs & c["spec_set"])
                    alt_hit = False
                    for (g, e) in c["alt_set"]:
                        if any(p[0] == g and (e == "*" or p[1] == e) for p in pairs):
                            alt_hit = True
                            altname = row[IX["identified_name"]] or row[IX["accepted_name"]]
                    if alt_hit and not spec_hit:
                        card_alt_hits[c["slug"]][altname] += 1
                    if gen_hit or spec_hit:
                        card_hits[c["slug"]].append(dict(
                            occ=row[IX["occurrence_no"]], coll=row[IX["collection_no"]], spec=spec_hit,
                            idn=row[IX["identified_name"]], acn=row[IX["accepted_name"]],
                            ei=row[IX["early_interval"]], li=row[IX["late_interval"]],
                            mx=row[IX["max_ma"]], mn=row[IX["min_ma"]], cc=row[IX["cc"]],
                            pl1=row[IX["paleolat"]], pl2=row[IX["paleolat2"]], pl3=row[IX["paleolat3"]],
                            tm=row[IX["time_major"]], ref=row[IX["reference_no"]]))
            # window and plant filter
            try:
                mx = float(row[IX["max_ma"]])
                mn = float(row[IX["min_ma"]])
            except ValueError:
                n_noage += 1
                continue
            if not (mx > WIN_TOP and mn < WIN_BASE):
                continue
            n_window_all += 1
            res = classify(row, IX)
            if res is None:
                continue
            plant_rows.append((row,) + res)
log("excluded window rows by reason", dict(EXCL))
log("occurrences", n_total, "no-age", n_noage, "window all taxa", n_window_all, "plant-filtered", len(plant_rows))

# ---------------------------------------------------------------------------------------------
# Build occurrence output
# ---------------------------------------------------------------------------------------------
DER_OCC = ["d_subset", "d_in_core", "d_basis", "d_major_group", "d_record_type", "d_genus", "d_span_myr",
           "d_overlap_with_window_myr", "d_fully_inside_window", "d_pbdb_lineage"]
plant_rows.sort(key=lambda t: int(t[0][IX["occurrence_no"]]))
occ_out = []
for row, subset, basis, lineage in plant_rows:
    mx, mn = float(row[IX["max_ma"]]), float(row[IX["min_ma"]])
    rtype = record_type(row, IX)
    mg = major_group(subset, rtype, row, IX, lineage)
    span = mx - mn
    ov = min(mx, WIN_BASE) - max(mn, WIN_TOP)
    occ_out.append(row + [subset, "yes" if subset in CORE else "no", basis, mg, rtype, derive_genus(row, IX),
                          f"{span:.4g}", f"{ov:.4g}", "yes" if (mx <= WIN_BASE and mn >= WIN_TOP) else "no", lineage])
with open(OUT + "pbdb_plant_occurrences.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(HEAD + DER_OCC)
    w.writerows(occ_out)
OIX = {k: i for i, k in enumerate(HEAD + DER_OCC)}
log("wrote occurrences", len(occ_out))
newline_occ = sum(1 for r in occ_out for c in r if "\n" in c or "\r" in c)
log("cells with line breaks in occurrence output", newline_occ)

# filter-names audit
names_ct = collections.defaultdict(lambda: [0, set(), ""])
for r in occ_out:
    nm = r[OIX["accepted_name"]] or r[OIX["identified_name"]]
    k = (r[OIX["d_subset"]], r[OIX["d_basis"]][:80], nm)
    names_ct[k][0] += 1
    names_ct[k][1].add(r[OIX["collection_no"]])
with open(OUT + "pbdb_plant_filter_names.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["d_subset", "d_basis", "name_accepted_else_identified", "n_occurrences", "n_collections"])
    for k, v in sorted(names_ct.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
        w.writerow([k[0], k[1], k[2], v[0], len(v[1])])

# ---------------------------------------------------------------------------------------------
# Collections: needed = plant occurrences' collections + card hit collections (for modern coords)
# ---------------------------------------------------------------------------------------------
need = {r[IX["collection_no"]] for r in occ_out}
need_card = {h["coll"] for hs in card_hits.values() for h in hs}
coll_rows = {}
coll_latlng = {}
CHEAD = None
for fpath in sorted(glob.glob(SNAP + "collections__p*.csv")):
    with open(fpath, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        h = next(rd)
        if CHEAD is None:
            CHEAD = h
        assert h == CHEAD
        ci = {}
        for i, k in enumerate(h):
            ci.setdefault(k, i)
        for row in rd:
            cn = row[ci["collection_no"]]
            if cn in need:
                coll_rows[cn] = row
            if cn in need_card:
                coll_latlng[cn] = (row[ci["lng"]], row[ci["lat"]])
CI = {}
for i, k in enumerate(CHEAD):
    CI.setdefault(k, i)
seen = collections.Counter()
CHEAD_OUT = []
for k in CHEAD:
    seen[k] += 1
    CHEAD_OUT.append(k if seen[k] == 1 else f"{k}.{seen[k] - 1}")
plant_ct = collections.Counter(r[OIX["collection_no"]] for r in occ_out)
core_ct = collections.Counter(r[OIX["collection_no"]] for r in occ_out if r[OIX["d_in_core"]] == "yes")
DER_COLL = ["d_n_plant_filter_occurrences", "d_n_core_occurrences", "d_n_public_occurrences_all_taxa"]
with open(OUT + "pbdb_plant_collections.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(CHEAD_OUT + DER_COLL)
    missing = sorted(need - set(coll_rows), key=int)
    log("collections needed", len(need), "found", len(coll_rows), "missing", len(missing))
    for cn in sorted(coll_rows, key=int):
        w.writerow(coll_rows[cn] + [plant_ct[cn], core_ct[cn], coll_total[cn]])
log("wrote collections", len(coll_rows))

# ---------------------------------------------------------------------------------------------
# References
# ---------------------------------------------------------------------------------------------
occ_refs = collections.Counter(r[OIX["reference_no"]] for r in occ_out)
coll_refs = collections.Counter()
for cn, row in coll_rows.items():
    coll_refs[row[CI["reference_no"]]] += 1
need_ref = set(occ_refs) | set(coll_refs)
with open(SNAP + "references.csv", newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    RHEAD = next(rd)
    RIX = {k: i for i, k in enumerate(RHEAD)}
    ref_rows = {row[0]: row for row in rd if row[0] in need_ref}
DER_REF = ["d_n_plant_filter_occurrences_citing", "d_n_plant_collections_citing_as_primary", "d_cited_by"]
with open(OUT + "pbdb_plant_references.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(RHEAD + DER_REF)
    for rn in sorted(ref_rows, key=int):
        by = "occurrences and collections" if occ_refs[rn] and coll_refs[rn] else ("occurrences" if occ_refs[rn] else "collections")
        w.writerow(ref_rows[rn] + [occ_refs[rn], coll_refs[rn], by])
log("references needed", len(need_ref), "found", len(ref_rows), "missing", sorted(need_ref - set(ref_rows)))

# ---------------------------------------------------------------------------------------------
# Counts by interval
# ---------------------------------------------------------------------------------------------
ints = {}
with open(SNAP + "intervals.csv", newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        if r["scale_no"] == "1":
            ints[r["interval_name"]] = (float(r["t_age"]), float(r["b_age"]))
cells = collections.defaultdict(lambda: [0, set(), set()])
for r in occ_out:
    for rule, col in (("time_major", "time_major"), ("time_contain", "time_contain"), ("as_entered", None)):
        if col is None:
            iv = r[OIX["early_interval"]] + (" to " + r[OIX["late_interval"]] if r[OIX["late_interval"]] else "")
        else:
            iv = r[OIX[col]]
            iv = iv if iv not in ("", "-") else "(none: age range not within one stage)" if rule == "time_contain" else "(none)"
        for mgk in (r[OIX["d_major_group"]], "ALL_CORE" if r[OIX["d_in_core"]] == "yes" else None, "ALL_INCLUDING_FLAGGED"):
            if mgk is None:
                continue
            c = cells[(rule, iv, mgk)]
            c[0] += 1
            c[1].add(r[OIX["collection_no"]])
            if r[OIX["d_genus"]]:
                c[2].add(r[OIX["d_genus"]])
with open(OUT + "pbdb_plant_counts_by_interval.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["binning_rule", "interval", "interval_base_ma", "interval_top_ma", "interval_overlaps_window",
                "major_group", "group_in_core", "n_occurrences", "n_collections", "n_genera"])

    def sk(k):
        rule, iv, mg = k
        b = ints[iv][1] if iv in ints else -1
        return (rule, -b, iv, 0 if mg.startswith("ALL") else 1, mg)
    for k in sorted(cells, key=sk):
        rule, iv, mg = k
        c = cells[k]
        t, b = ints.get(iv, (None, None))
        ov = "" if t is None else ("yes" if (b > WIN_TOP and t < WIN_BASE) else "no")
        if mg == "ALL_CORE":
            core = "yes"
        elif mg == "ALL_INCLUDING_FLAGGED":
            core = "mixed"
        else:
            core = "yes" if mg not in FLAGGED_ORDER else "no"
        w.writerow([rule, iv, "" if b is None else b, "" if t is None else t, ov, mg, core, c[0], len(c[1]), len(c[2])])
log("wrote counts", len(cells))

# ---------------------------------------------------------------------------------------------
# Card summary
# ---------------------------------------------------------------------------------------------
# card front matter is supplied inline (copied from taxa/*.md on 2026-10-26) so the script is self-contained
CARD_FM = {
    "aberlemnia-caledonica": ("Aberlemnia caledonica", "species", "Pridoli", "Lochkovian"),
    "aglaophyton-majus": ("Aglaophyton majus", "species", "Pragian", "Emsian"),
    "ambitisporites": ("Ambitisporites", "genus", "Katian", "Lochkovian"),
    "asteroxylon-mackiei": ("Asteroxylon mackiei", "species", "Pragian", "Emsian"),
    "baragwanathia-longifolia": ("Baragwanathia longifolia", "species", "Lochkovian", "Pragian"),
    "cooksonia": ("Cooksonia", "genus", "Sheinwoodian", "Lochkovian"),
    "drepanophycus-spinaeformis": ("Drepanophycus spinaeformis", "species", "Pragian", "Givetian"),
    "early-glomeromycotan-fungi": ("Early arbuscular mycorrhizal (glomeromycotan) fungi", "assemblage", "Darriwilian", "Emsian"),
    "eophyllophyton-bellum": ("Eophyllophyton bellum", "species", "Pragian", "Pragian"),
    "horneophyton-lignieri": ("Horneophyton lignieri", "species", "Pragian", "Emsian"),
    "nematothallus": ("Nematothallus", "genus", "Ludfordian", "Lochkovian"),
    "ordovician-cryptospores": ("Ordovician cryptospore assemblages", "assemblage", "Darriwilian", "Hirnantian"),
    "partitatheca": ("Partitatheca", "genus", "Lochkovian", "Lochkovian"),
    "pertica": ("Pertica", "genus", "Emsian", "Eifelian"),
    "prototaxites": ("Prototaxites", "genus", "Pridoli", "Givetian"),
    "psilophyton": ("Psilophyton", "genus", "Pragian", "Eifelian"),
    "renalia-hueberi": ("Renalia hueberi", "species", "Emsian", "Emsian"),
    "rhynia-gwynne-vaughanii": ("Rhynia gwynne-vaughanii", "species", "Pragian", "Emsian"),
    "rhynie-chert-gametophytes": ("Rhynie Chert gametophytes", "morphogroup", "Pragian", "Emsian"),
    "riccardiothallus-devonicus": ("Riccardiothallus devonicus", "species", "Pragian", "Pragian"),
    "sawdonia-ornata": ("Sawdonia ornata", "species", "Emsian", "Emsian"),
    "tortotubus-protuberans": ("Tortotubus protuberans", "species", "Rhuddanian", "Emsian"),
    "winfrenatia-reticulata": ("Winfrenatia reticulata", "species", "Pragian", "Pragian"),
    "zosterophyllum": ("Zosterophyllum", "genus", "Ludfordian", "Emsian"),
}
CARD_NOTES = {
    "aberlemnia-caledonica": "Species not in PBDB under this name; the only genus-level hit is 'Aberlemnia sp.'. The original combination appears once as 'Cooksonia cf. caledonica' (listed in alt_names_found, not counted).",
    "aglaophyton-majus": "Genus Aglaophyton absent from PBDB. The species occurs once under its original combination 'Rhynia major' (alt_names_found, not counted; PBDB accepted name is Rhynia).",
    "ambitisporites": "Dispersed spore form genus. PBDB holds 9 records (A. avitus, dilutus, tripapillatus, sp.); the oldest is Wenlock (max 432.9 Ma), so none of the Ordovician (Katian to Hirnantian) records on the card is in PBDB.",
    "asteroxylon-mackiei": "Strict species count is zero: PBDB holds the epithet misspelt 'mackei' once (alt_names_found) plus other species (A. elberfeldense, A. setchelli, now Stenokoleos) and cf. Asteroxylon sp.; genus-level counts include these.",
    "baragwanathia-longifolia": "Genus has two spellings in PBDB: 'Baragwanathia' and 'Baragwanthia'. Strict species count merges the epithet longifolia under the correct genus spelling only; the misspelt genus is in alt_names_found.",
    "cooksonia": "Genus-level hits include '? Cooksonia', 'cf. Cooksonia' and species such as C. hemisphaerica, C. pertoni, C. cambrensis, C. downtonensis, C. synorispora; no C. barrandei. Names such as Contignisporites cooksoniae and Isabelidinium cooksoniae are excluded (epithet only).",
    "drepanophycus-spinaeformis": "Genus-level count includes other species (D. gaspianus, D. colophyllus, D. spinosus, D. qujingensis and others); the species-level count covers D. spinaeformis and cf. spinaeformis only.",
    "early-glomeromycotan-fungi": "None of the card's fungal genera (Palaeoglomus, Glomites, Archaeosporites, Palaeoendogone, Rugososporomyces) is in PBDB under the searched names. Five Palaeomyces/Palaeomycites records (Rhynie-type fungal names not on the card) are listed in alt_names_found, not counted.",
    "eophyllophyton-bellum": "Present once.",
    "horneophyton-lignieri": "The single record is identified as 'Hornea lignieri' (the older genus name); PBDB's accepted name is Horneophyton lignieri, so it is counted at species level. The genus name Hornea is not searched as a genus because it is also used for unrelated, younger taxa in PBDB; genus-level count is Horneophyton (by accepted or classification genus) only.",
    "nematothallus": "Genus-level hits are Nematothallus pseudovasculosa and Nematothallus; other nematophyte genera (Nematoplexus, Nematasketum) are in alt_names_found, not counted.",
    "ordovician-cryptospores": "Assemblage card; the genus list is this script's list of standard cryptospore genera, not a card field. PBDB holds 15 records in 3 collections, Hirnantian (max 445.2 Ma) to Wenlock, none Darriwilian to Katian: PBDB does not cover the Ordovician cryptospore record the card rests on.",
    "partitatheca": "Genus absent from PBDB.",
    "pertica": "Genus-level hits are Pertica dalhousii and Pertica varia; the strings 'perticaense' (Chieseiceras), 'pertica' (Streblotrypa, Undularia) are different taxa and excluded.",
    "prototaxites": "Genus-level count; PBDB lists Prototaxites under Plantae (not fungi). 'Protaxites' (one misspelt record) is in alt_names_found.",
    "psilophyton": "Genus-level count includes many species, among them P. princeps, P. dawsonii and 'Psilophyton robustius' (accepted as Trimerophyton robustius). Many species names are Late Devonian or younger records outside the window.",
    "renalia-hueberi": "Species present once; Renalia dorfii is a second species at genus level.",
    "rhynia-gwynne-vaughanii": "PBDB spells the epithet 'gwynnevaughanii' (no hyphen) and holds one record, accepted as Rhynia; 'Rhynia major' (= Aglaophyton) is in alt_names_found.",
    "rhynie-chert-gametophytes": "Morphogroup card; the genus list is the four genera named on the card (Lyonophyton, Langiophyton, Kidstonophyton, Remyophyton). PBDB has single records for the first three and none for Remyophyton; names are not in PBDB's taxonomy (no accepted name).",
    "riccardiothallus-devonicus": "Absent from PBDB.",
    "sawdonia-ornata": "Not in PBDB's taxonomy (accepted_name blank): identified names only, 'Sawdonia ornata' and 'cf. Sawdonia ornata'. Other Sawdonia species at genus level.",
    "tortotubus-protuberans": "Absent from PBDB (the taxon name exists in the taxa table with no occurrences).",
    "winfrenatia-reticulata": "Only 'Winfrenatia sp. n. gen.' (genus-level, one record), not the species.",
    "zosterophyllum": "Genus-level count includes '?', 'cf.' and 'sp.' records; one 'Zosterophyllum sinense' is accepted as Plantae.",
}


def f_or_none(x):
    try:
        return float(x)
    except ValueError:
        return None


def age_block(hs):
    """oldest/youngest occurrence (by max_ma / min_ma) and median age span of a list of hits"""
    ages = [(f_or_none(h["mx"]), f_or_none(h["mn"]), h) for h in hs
            if f_or_none(h["mx"]) is not None and f_or_none(h["mn"]) is not None]
    if not ages:
        return ages, None, None, ""
    old = sorted(ages, key=lambda t: (-t[0], t[0] - t[1], int(t[2]["occ"])))[0]
    yng = sorted(ages, key=lambda t: (t[1], t[0] - t[1], int(t[2]["occ"])))[0]
    return ages, old, yng, f"{statistics.median([a - b for a, b, _ in ages]):.4g}"


occ_ids = {r[OIX["occurrence_no"]] for r in occ_out}
with open(OUT + "card_taxa_pbdb_summary.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["card_slug", "card_name", "card_rank", "card_range_first_stage", "card_range_last_stage",
                "match_rule", "n_occurrences_card_level", "n_collections_card_level", "n_occurrences_genus_level",
                "n_occurrences_in_window_485_383_card_level",
                "oldest_max_ma", "oldest_min_ma", "oldest_early_interval", "oldest_late_interval", "oldest_time_major",
                "oldest_occurrence_no", "youngest_min_ma", "youngest_max_ma", "youngest_early_interval",
                "youngest_late_interval", "youngest_time_major", "youngest_occurrence_no", "median_age_span_myr",
                "genus_level_oldest_max_ma", "genus_level_oldest_early_interval", "genus_level_youngest_min_ma",
                "genus_level_youngest_late_or_early_interval",
                "countries_cc_count", "n_with_palaeocoords_gplates", "n_with_palaeocoords_scotese",
                "n_with_palaeocoords_seton", "n_with_modern_coords", "n_references", "matched_names",
                "alt_names_searched", "alt_names_found_not_counted", "name_notes"])
    window_miss = 0
    for c in CARDS:
        slug = c["slug"]
        nm, rank, f1, l1 = CARD_FM[slug]
        hits = card_hits.get(slug, [])
        genus_card = slug in GENUS_CARD or slug in CARD_RANK_ASSEMBLAGE
        counted = hits if genus_card else [h for h in hits if h["spec"]]
        if slug in CARD_RANK_ASSEMBLAGE:
            rule = "genus in: " + ", ".join(c["genera"])
        elif genus_card:
            rule = "genus = " + c["genera"][0] + " (identified, accepted, primary-name or classification genus; cf. and ? ignored)"
        else:
            rule = "genus + epithet in: " + ", ".join(sorted(f"{g} {e}" for g, e in c["species"])) + " (cf. and ? ignored; epithet punctuation ignored)"
        ages, old, yng, med = age_block(counted)
        n_win = sum(1 for mx, mn, h in ages if mx > WIN_TOP and mn < WIN_BASE)
        row = [slug, nm, rank, f1, l1, rule, len(counted), len({h["coll"] for h in counted}), len(hits), n_win]
        if old:
            row += [old[0], old[1], old[2]["ei"], old[2]["li"], old[2]["tm"], old[2]["occ"],
                    yng[1], yng[0], yng[2]["ei"], yng[2]["li"], yng[2]["tm"], yng[2]["occ"], med]
        else:
            row += [""] * 13
        gages, gold, gyng, _ = age_block(hits)
        if gold:
            row += [gold[0], gold[2]["ei"], gyng[1], gyng[2]["li"] or gyng[2]["ei"]]
        else:
            row += [""] * 4
        ccs = collections.Counter((h["cc"] or "(blank)") for h in counted)
        row.append("; ".join(f"{k}:{v}" for k, v in ccs.most_common()))
        row += [sum(1 for h in counted if h["pl1"]), sum(1 for h in counted if h["pl2"]), sum(1 for h in counted if h["pl3"])]
        row.append(sum(1 for h in counted if coll_latlng.get(h["coll"], ("", ""))[0] != "" and coll_latlng.get(h["coll"], ("", ""))[1] != ""))
        row.append(len({h["ref"] for h in counted}))
        nmc = collections.Counter(h["acn"] or h["idn"] for h in counted)
        row.append("; ".join(f"{k} ({v})" for k, v in nmc.most_common(12)))
        row.append("; ".join(f"{g} {e}" for g, e in c["alt"]))
        alts = card_alt_hits.get(slug, collections.Counter())
        row.append("; ".join(f"{k} ({v})" for k, v in alts.most_common()))
        row.append(CARD_NOTES[slug])
        w.writerow(row)
        # QA: every in-window match (genus level) must be in the plant-filter output
        for mx, mn, h in gages:
            if mx > WIN_TOP and mn < WIN_BASE and h["occ"] not in occ_ids:
                window_miss += 1
                log("QA: card hit in window but not in plant filter:", slug, h["occ"], h["idn"], h["acn"])
log("card QA misses", window_miss)

# ---------------------------------------------------------------------------------------------
# Diagnostics to stderr
# ---------------------------------------------------------------------------------------------
sc = collections.Counter((r[OIX["d_subset"]], r[OIX["d_basis"]].split(":")[0]) for r in occ_out)
for k, v in sorted(sc.items()):
    log("subset", k, v)
log("major groups", collections.Counter(r[OIX["d_major_group"]] for r in occ_out).most_common())
log("record types", collections.Counter(r[OIX["d_record_type"]] for r in occ_out).most_common())
log("fully inside window", collections.Counter(r[OIX["d_fully_inside_window"]] for r in occ_out))
