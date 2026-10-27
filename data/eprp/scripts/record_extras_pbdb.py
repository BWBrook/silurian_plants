"""record_extras_pbdb.py (tranche 2): PBDB specimens, measurements, plant taxa, opinions, references, and Frasnian-Famennian
anchor occurrences, from the same snapshot as record_pbdb.py (tranche 1).

Run on deep-server (stdlib only):
    scp data/eprp/record/pbdb_plant_occurrences.csv deep-server:<IN_DIR>/
    ssh deep-server python3 - < record_extras_pbdb.py
Reads the PBDB global snapshot read-only and tranche 1's pbdb_plant_occurrences.csv (checked against its manifest sha256);
writes to OUT under /data/codex/silurian_plants/raw/pbdb-extras/<UTC stamp>/. Copy the tables into data/eprp/record/
(or data/eprp/local/record/ when over 20 MB) afterwards.

The taxonomy, filter and derived-column code in the block between the two COPIED markers is copied unchanged from
record_pbdb.py lines 39-236 (tranche 1), so the plant filter is identical; nothing in record_pbdb.py is edited.

Outputs:
  pbdb_plant_specimens.csv       specimens.csv rows linked to a tranche-1 or anchor occurrence, or whose taxon lies in the plant
                                 subsets (any age); all 46 original columns + d_*
  pbdb_plant_measurements.csv    measurements__c*.csv rows with the same rule; all 127 original columns (second 'cc' = cc.1) + d_*
  pbdb_plant_taxa.csv            taxa.csv rows in the plant subsets or the anchors; all original columns + d_*
  pbdb_plant_opinions.csv        opinions.csv rows whose orig_no is one of those taxa; all original columns + d_*
  pbdb_extras_references.csv     references cited by the rows above and by the anchor occurrences
  pbdb_anchor_occurrences_frasnian_famennian.csv  anchor-genus occurrences outside the window that overlap the Frasnian-Famennian
  pbdb_extras_inputs_sha256.tsv  sha256 of every mirror file read, checked against the snapshot MANIFEST.json
  summary.txt                    counts logged during the run
"""
import csv
import collections
import datetime
import glob
import hashlib
import json
import os
import re
import statistics
import sys

csv.field_size_limit(1 << 30)

SNAP = "/data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url/"
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%MZ")
BASE = "/data/codex/silurian_plants/raw/pbdb-extras/"
IN_DIR = BASE + "input/"
OUT = BASE + STAMP + "/"
T1_OCC = IN_DIR + "pbdb_plant_occurrences.csv"
T1_OCC_SHA256 = "bc617e869f133ede3461eac25ef54fd9cb9efe5a2be3f137ae1b8a7f8537ef01"   # data/eprp/record/MANIFEST.tsv
T1_REF = IN_DIR + "pbdb_plant_references.csv"
T1_REF_SHA256 = "60a183a8781afec69300f6d7277a2c7955a23ee87b48a439b24407bff61a5a82"
WIN_TOP = 383.0    # Ma, younger edge of the tranche-1 window
WIN_BASE = 485.0   # Ma, older edge
FF_TOP = 358.86    # Ma, base of the Tournaisian in data/timescale.csv (sha256 396bde65..., 2026-10-27): top of the Famennian
FF_BASE = 382.31   # Ma, base of the Frasnian in data/timescale.csv
ANCHORS = ["Archaeopteris", "Callixylon", "Eospermatopteris", "Wattieza", "Elkinsia", "Leclercqia"]
ANCHOR_L = {a.lower() for a in ANCHORS}

os.makedirs(OUT, exist_ok=True)
LOGF = open(OUT + "summary.txt", "w")


def log(*a):
    print(*a, file=sys.stderr, flush=True)
    print(*a, file=LOGF, flush=True)


def sha256_of(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


assert sha256_of(T1_OCC) == T1_OCC_SHA256, "tranche-1 occurrence file differs from its manifest sha256"
assert sha256_of(T1_REF) == T1_REF_SHA256, "tranche-1 reference file differs from its manifest sha256"

# ---- COPIED START: record_pbdb.py lines 39-236, unchanged ----
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

# ---- COPIED END ----


# ---------------------------------------------------------------------------------------------
# Tranche-1 occurrence set
# ---------------------------------------------------------------------------------------------
T1 = {}          # occurrence_no -> dict of d_ flags
T1_ACC = collections.Counter()      # accepted_no (an orig_no) -> n tranche-1 occurrences
T1_IDN = collections.Counter()      # identified_no (a taxon_no, the identified spelling) -> n
with open(T1_OCC, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        T1[r["occurrence_no"]] = {k: r[k] for k in ("d_subset", "d_in_core", "d_major_group", "d_genus")}
        T1_ACC[r["accepted_no"]] += 1
        T1_IDN[r["identified_no"]] += 1
T1_REFS = set()
with open(T1_REF, newline="", encoding="utf-8") as f:
    T1_REFS = {r["reference_no"] for r in csv.DictReader(f)}
log("tranche-1 occurrences", len(T1), "tranche-1 references", len(T1_REFS))

PLANT_ROOT_IDS = {"Plantae": ID["Plantae"], "Embryophyta": ID["Embryophyta"], "Streptophyta": ID["Streptophyta"],
                  "Charophyta": ID["Charophyta"]}
EXCLUDE_FROM_TAXA_SUBSET = [ID[k] for k in ("Chlorophyta", "Rhodophyta", "Biliphyta", "Algae", "Fungi", "Acritarcha",
                                              "Archaeplastida")]


def lineage_names(o):
    return " > ".join(T[x]["name"] for x in reversed(ancestors(o))) if o else ""


def taxon_node(accepted_no, taxon_no, orig_no):
    """orig_no used for the lineage, following tranche 1: the accepted name's orig_no, else the row's own"""
    for a in (accepted_no, taxon_no, orig_no):
        if a and a in T:
            return a
        if a and a in TNO2ORIG:
            return TNO2ORIG[a]
    return ""


def taxon_subset(o):
    """the plant subsets of tranche 1's ordered rules that are kept for the taxa table (1, 3, 6), else ''"""
    if not o:
        return ""
    S = set(ancestors(o))
    if ID["Embryophyta"] in S:
        return "embryophyta_pbdb_tree"
    if ID["Chlorophyta"] in S:
        return ""
    if ID["Streptophyta"] in S or ID["Charophyta"] in S:
        return "streptophyta_not_embryophyta"
    if ID["Rhodophyta"] in S or ID["Biliphyta"] in S or ID["Algae"] in S:
        return ""
    if ID["Plantae"] in S:
        return "plantae_unplaced_pbdb_tree"
    return ""


def dedup_header(h):
    seen = collections.Counter()
    out = []
    for k in h:
        seen[k] += 1
        out.append(k if seen[k] == 1 else f"{k}.{seen[k] - 1}")
    return out


# ---------------------------------------------------------------------------------------------
# Taxa
# ---------------------------------------------------------------------------------------------
TAXA_OUT = []
TAXA_SUBSET_BY_ORIG = {}        # orig_no -> d_taxon_subset or anchor tag
ANCHOR_NODES = {o for o, t in T.items() if t["name"].lower() in ANCHOR_L}
log("anchor genus nodes", {T[o]["name"]: o for o in ANCHOR_NODES})
with open(SNAP + "taxa.csv", newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    THEAD = next(rd)
    TH = dedup_header(THEAD)
    TI = {k: i for i, k in enumerate(TH)}
    dup_diff = 0
    for row in rd:
        o = taxon_node(row[TI["accepted_no"]], row[TI["taxon_no"]], row[TI["orig_no"]])
        sub = taxon_subset(o)
        first = re.sub(r"[^a-z]", "", (row[TI["taxon_name"]].split(" ")[0] if row[TI["taxon_name"]] else "").lower())
        S = set(ancestors(o)) if o else set()
        is_anchor = bool(S & ANCHOR_NODES) or first in ANCHOR_L or re.sub(r"[^a-z]", "", row[TI["genus"]].lower()) in ANCHOR_L
        if not sub and not is_anchor:
            continue
        if not sub:
            sub = "anchor_outside_plant_tree"
        for k in ("firstapp_max_ma", "firstapp_min_ma", "lastapp_max_ma", "lastapp_min_ma", "early_interval", "late_interval"):
            if row[TI[k]] != row[TI[k + ".1"]]:
                dup_diff += 1
        fmx, lmn = row[TI["firstapp_max_ma"]], row[TI["lastapp_min_ma"]]
        try:
            ov = "yes" if (float(fmx) > WIN_TOP and float(lmn) < WIN_BASE) else "no"
        except ValueError:
            ov = ""
        tn = row[TI["taxon_no"]]
        TAXA_OUT.append(row + [sub, "yes" if is_anchor else "no", ov, T1_ACC.get(row[TI["orig_no"]], 0), T1_IDN.get(tn, 0), lineage_names(o)])
        TAXA_SUBSET_BY_ORIG.setdefault(row[TI["orig_no"]], sub)
DER_TAXA = ["d_taxon_subset", "d_is_anchor", "d_range_overlaps_window", "d_n_tranche1_occurrences_accepted",
            "d_n_tranche1_occurrences_identified", "d_pbdb_lineage"]
TAXA_OUT.sort(key=lambda r: int(r[TI["taxon_no"]]))
with open(OUT + "pbdb_plant_taxa.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(TH + DER_TAXA)
    w.writerows(TAXA_OUT)
log("taxa rows", len(TAXA_OUT), "by subset", dict(collections.Counter(r[len(TH)] for r in TAXA_OUT)))
log("taxa duplicate-header cells that differ between the two copies", dup_diff)
PLANT_ORIG = set(TAXA_SUBSET_BY_ORIG)
PLANT_TAXON_NO = {r[TI["taxon_no"]] for r in TAXA_OUT}
log("distinct orig_no in plant taxa", len(PLANT_ORIG))

# ---------------------------------------------------------------------------------------------
# Anchor occurrences outside the window
# ---------------------------------------------------------------------------------------------
ANCHOR_OUT = []
anchor_rows_all = collections.Counter()     # name-matched anchor rows by fate, whole snapshot
anchor_inside_window_in_t1 = 0
HEAD = None
IX = None
for fpath in sorted(glob.glob(SNAP + "occurrences__p*.csv")):
    with open(fpath, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        h = next(rd)
        if HEAD is None:
            HEAD = h
            IX = {k: i for i, k in enumerate(h)}
        assert h == HEAD, fpath
        for row in rd:
            toks = set()
            for col in ("identified_name", "accepted_name", "primary_name", "genus"):
                toks |= {re.sub(r"[^a-z]", "", t.lower()) for t in row[IX[col]].replace("?", " ").split()}
            gset = toks & ANCHOR_L
            if not gset:
                continue
            try:
                mx, mn = float(row[IX["max_ma"]]), float(row[IX["min_ma"]])
            except ValueError:
                anchor_rows_all["no_age"] += 1
                continue
            in_win = mx > WIN_TOP and mn < WIN_BASE
            if in_win:
                anchor_rows_all["in_window"] += 1
                if row[IX["occurrence_no"]] in T1:
                    anchor_inside_window_in_t1 += 1
                continue
            res = classify(row, IX)
            if res is None:
                anchor_rows_all["outside_window_fails_plant_filter"] += 1
                continue
            ov_ff = min(mx, FF_BASE) - max(mn, FF_TOP)
            if ov_ff <= 0:
                anchor_rows_all["outside_window_no_overlap_with_FF"] += 1
                continue
            anchor_rows_all["outside_window_overlaps_FF"] += 1
            subset, basis, lineage = res
            rtype = record_type(row, IX)
            mg = major_group(subset, rtype, row, IX, lineage)
            ANCHOR_OUT.append(row + [subset, "yes" if subset in CORE else "no", basis, mg, rtype, derive_genus(row, IX),
                                     f"{mx - mn:.4g}", f"{ov_ff:.4g}", "yes" if (mx <= FF_BASE and mn >= FF_TOP) else "no",
                                     ";".join(sorted(g.capitalize() for g in gset)), lineage])
DER_ANCHOR = ["d_subset", "d_in_core", "d_basis", "d_major_group", "d_record_type", "d_genus", "d_span_myr",
              "d_overlap_with_frasnian_famennian_myr", "d_fully_inside_frasnian_famennian", "d_anchor_genus",
              "d_pbdb_lineage"]
ANCHOR_OUT.sort(key=lambda r: int(r[IX["occurrence_no"]]))
with open(OUT + "pbdb_anchor_occurrences_frasnian_famennian.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(HEAD + DER_ANCHOR)
    w.writerows(ANCHOR_OUT)
AIX = {k: i for i, k in enumerate(HEAD + DER_ANCHOR)}
ANCHOR_OCC = {r[IX["occurrence_no"]] for r in ANCHOR_OUT}
log("anchor name-matched rows by fate", dict(anchor_rows_all), "in-window anchor rows that are in tranche 1:", anchor_inside_window_in_t1)
log("anchor occurrences written", len(ANCHOR_OUT), "by genus", dict(collections.Counter(r[AIX["d_anchor_genus"]] for r in ANCHOR_OUT)))
log("anchor by subset", dict(collections.Counter(r[AIX["d_subset"]] for r in ANCHOR_OUT)))

# ---------------------------------------------------------------------------------------------
# Specimens and measurements
# ---------------------------------------------------------------------------------------------
def set_label(occ_no, accepted_no, identified_no):
    """which rule keeps a specimen or measurement row (first applicable), '' if none"""
    if occ_no in T1:
        return "tranche1_occurrence"
    if occ_no in ANCHOR_OCC:
        return "anchor_occurrence"
    for a in (accepted_no, identified_no):
        if a and a != "0":
            o = a if a in T else TNO2ORIG.get(a, "")
            if o and (o in PLANT_ORIG or taxon_subset(o)):
                return "plant_taxon_any_age"
    return ""


def occ_flags(occ_no):
    if occ_no in T1:
        return [T1[occ_no]["d_subset"], T1[occ_no]["d_in_core"], T1[occ_no]["d_major_group"], T1[occ_no]["d_genus"]]
    return ["", "", "", ""]


SPEC_OUT = []
n_spec = 0
with open(SNAP + "specimens.csv", newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    SHEAD = next(rd)
    SI = {k: i for i, k in enumerate(SHEAD)}
    for row in rd:
        n_spec += 1
        lab = set_label(row[SI["occurrence_no"]], row[SI["accepted_no"]], row[SI["identified_no"]])
        if not lab:
            continue
        SPEC_OUT.append(row + [lab] + occ_flags(row[SI["occurrence_no"]]))
DER_SPM = ["d_set", "d_subset", "d_in_core", "d_major_group", "d_genus"]
SPEC_OUT.sort(key=lambda r: int(r[SI["specimen_no"]]))
with open(OUT + "pbdb_plant_specimens.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(SHEAD + DER_SPM)
    w.writerows(SPEC_OUT)
log("specimens read", n_spec, "kept", len(SPEC_OUT), dict(collections.Counter(r[len(SHEAD)] for r in SPEC_OUT)))

MEAS_OUT = []
n_meas = 0
MHEAD = None
for fpath in sorted(glob.glob(SNAP + "measurements__c*.csv")):
    with open(fpath, newline="", encoding="utf-8") as fh:
        rd = csv.reader(fh)
        h = next(rd)
        if MHEAD is None:
            MHEAD = h
            MH = dedup_header(h)
            MI = {k: i for i, k in enumerate(MH)}
        assert h == MHEAD, fpath
        for row in rd:
            n_meas += 1
            lab = set_label(row[MI["occurrence_no"]], row[MI["accepted_no"]], row[MI["identified_no"]])
            if not lab:
                continue
            MEAS_OUT.append(row + [lab] + occ_flags(row[MI["occurrence_no"]]))
MEAS_OUT.sort(key=lambda r: int(r[MI["measurement_no"]]))
with open(OUT + "pbdb_plant_measurements.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(MH + DER_SPM)
    w.writerows(MEAS_OUT)
log("measurements read", n_meas, "kept", len(MEAS_OUT), dict(collections.Counter(r[len(MH)] for r in MEAS_OUT)))

# ---------------------------------------------------------------------------------------------
# Opinions
# ---------------------------------------------------------------------------------------------
OPN_OUT = []
n_opn = 0
with open(SNAP + "opinions.csv", newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    OHEAD = next(rd)
    assert len(set(OHEAD)) == len(OHEAD)
    OI = {k: i for i, k in enumerate(OHEAD)}
    for row in rd:
        n_opn += 1
        o = row[OI["orig_no"]]
        if o in PLANT_ORIG:
            OPN_OUT.append(row + [TAXA_SUBSET_BY_ORIG[o]])
OPN_OUT.sort(key=lambda r: int(r[OI["opinion_no"]]))
with open(OUT + "pbdb_plant_opinions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(OHEAD + ["d_taxon_subset"])
    w.writerows(OPN_OUT)
log("opinions read", n_opn, "kept", len(OPN_OUT), "by subset", dict(collections.Counter(r[-1] for r in OPN_OUT)))
log("opinion types", dict(collections.Counter(r[OI["opinion_type"]] for r in OPN_OUT)))

# ---------------------------------------------------------------------------------------------
# References cited by the new rows
# ---------------------------------------------------------------------------------------------
cited = collections.defaultdict(collections.Counter)
for r in TAXA_OUT:
    if r[TI["reference_no"]]:
        cited[r[TI["reference_no"]]]["taxa"] += 1
for r in OPN_OUT:
    if r[OI["reference_no"]]:
        cited[r[OI["reference_no"]]]["opinions"] += 1
for r in SPEC_OUT:
    if r[SI["reference_no"]]:
        cited[r[SI["reference_no"]]]["specimens"] += 1
for r in MEAS_OUT:
    if r[MI["reference_no"]]:
        cited[r[MI["reference_no"]]]["measurements"] += 1
for r in ANCHOR_OUT:
    if r[IX["reference_no"]]:
        cited[r[IX["reference_no"]]]["anchor_occurrences"] += 1
SRC_ORDER = ["taxa", "opinions", "specimens", "measurements", "anchor_occurrences"]
with open(SNAP + "references.csv", newline="", encoding="utf-8") as fh:
    rd = csv.reader(fh)
    RHEAD = next(rd)
    RI = {k: i for i, k in enumerate(RHEAD)}
    ref_rows = {row[0]: row for row in rd if row[0] in cited}
missing = sorted(set(cited) - set(ref_rows), key=int)
with open(OUT + "pbdb_extras_references.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(RHEAD + ["d_cited_by"] + ["d_n_" + s for s in SRC_ORDER] + ["d_in_tranche1_references"])
    for rn in sorted(ref_rows, key=int):
        c = cited[rn]
        w.writerow(ref_rows[rn] + [";".join(s for s in SRC_ORDER if c[s])] + [c[s] for s in SRC_ORDER]
                   + ["yes" if rn in T1_REFS else "no"])
log("references cited", len(cited), "found", len(ref_rows), "missing", missing, "also in tranche-1 references",
    sum(1 for r in ref_rows if r in T1_REFS))

# ---------------------------------------------------------------------------------------------
# Input checksums against the snapshot manifest
# ---------------------------------------------------------------------------------------------
man = {x["key"]: x["sha256"] for x in json.load(open(SNAP + "MANIFEST.json"))["files"]}
inputs = ([SNAP + n for n in ["specimens.csv", "taxa.csv", "opinions.csv", "references.csv", "datainfo.json"]]
          + sorted(glob.glob(SNAP + "measurements__c*.csv")) + sorted(glob.glob(SNAP + "occurrences__p*.csv")))
with open(OUT + "pbdb_extras_inputs_sha256.tsv", "w", encoding="utf-8") as fh:
    fh.write("source\trole\tpath\tbytes\tsha256\tmirror_manifest_sha256\tmatches_manifest\n")
    for p in inputs:
        s = sha256_of(p)
        e = man.get(os.path.basename(p), "")
        fh.write(f"pbdb\tread\t{p}\t{os.path.getsize(p)}\t{s}\t{e}\t{'yes' if e == s else 'NO'}\n")
    for p, e in ((T1_OCC, T1_OCC_SHA256), (T1_REF, T1_REF_SHA256)):
        s = sha256_of(p)
        fh.write(f"tranche 1 (data/eprp/record)\tread\t{p}\t{os.path.getsize(p)}\t{s}\t{e}\t{'yes' if e == s else 'NO'}\n")
log("output dir", OUT)
