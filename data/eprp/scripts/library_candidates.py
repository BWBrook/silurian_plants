#!/usr/bin/env python3
"""Stage 2 of the silurian_plants library extraction: gather candidates by several routes.

Routes (recorded per work in `routes`):
  title      title matches a plant-specific, interval-plus-context or methods pattern
  abstract   title, OpenAlex abstract, keywords or concepts match the same patterns
  fts        a library.py search query (queries in library_queries.py) matched the work
  topic      EPRP canon topic id or OpenAlex topic relevant to the project
  author     an author on the watch list, with some plant, interval or earth-system context
  venue      a palaeobotany or botany venue, with some plant, interval or earth-system context
  text       the open full text has a high density of early-plant terms (open texts only)
  methods-text  title or EPRP canon topic matches the F3 methods vocabulary (ranges, birth-death, dating, record quality)
  question   the work carries an EPRP question tag for range estimation, fossil-record quality, rates or dating (Q-005, Q-006, Q-017, Q-019, Q-041, Q-042, B-007)

Read-only on the store. stdlib only. Needs features.jsonl from library_features.py.

    python3 library_candidates.py --features features.jsonl --store /data/codex/artifacts/eprp-paleodata-backup/latest/library \
        --out candidates.tsv --fts-out fts_hits.tsv
"""
import argparse
import collections
import csv
import json
import multiprocessing
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import library_queries  # noqa: E402

I = re.I

# plant-specific terms: any hit marks a work as a candidate (group name -> pattern)
STRONG = {
    "taxa": r"cooksonia|baragwanathia|aglaophyton|asteroxylon|psilophyton|prototaxites|nematothall|nematophyt|\brhynia|"
            r"horneophyton|zosterophyll|sawdonia|drepanophycus|renalia|\bpertica|eophyllophyton|aberlemnia|partitatheca|"
            r"tortotubus|winfrenatia|gosslingia|trimerophyton|hostinella|\bhedeia|yarravia|salopella|tarrantia|uskiella|"
            r"archaeopteris|wattieza|cladoxyl|pseudosporochnus|eospermatopteris|leclercqia|haskinsia|adoketophyton|bathurstia|"
            r"protolepidodendron|sporogonites|tortilicaulis|steganotheca|sciadophyton|lyonophyton|kidstonophyton|spongiophyton|"
            r"protosalvinia|orestovia|taeniocrada|sennicaulis|stockmansella|teruelia|eorhynia|\bpsilophyt|sphenothallus|"
            r"rhynie|windyfield|aneurophyt|protopteridium|\bforesta\b|thursophyton|nothia\b|\bhicklingia|\bzosterophyl",
    "groups": r"rhyniophyt|trimerophyt|euphyllophyt|polysporangiophyt|tracheophyt|eutracheophyt|protracheophyt|"
              r"progymnosperm|\beophyte|lycophyt|lycopsid|lycopod|\bbryophyt|liverwort|hornwort|marchantio|hepatic|"
              r"streptophyt|zygnemat|zygnematophyc|charophyt|coleochaet|embryophyt|cladoxylopsid",
    "spores": r"cryptospor|trilete|\bdyads?\b|permanent tetrad|miospore|ambitisporites|tetrahedraletes|dyadospora|"
              r"laevolancis|spore wall|sporopollenin|megaspore|heterospor|sporomorph|\bspores?\b|palynolog",
    "origin": r"land plants?\b|early plants|terrestriali[sz]ation|vascular plants?\b|origin of plants|plant terrestrial|"
              r"alternation of generations|sporophyte|gametophyte|plant evolution|palaeobotan|paleobotan|"
              r"phytogeograph|palaeophytogeograph|paleophytogeograph|evolutionary floras?|early vascular|earliest vascular",
    "traits": r"\bstomat|\bcuticle|tracheid|\bxylem|lignin|telome|\brhizoid|apical meristem|\bmegaphyll|\bmicrophyll|"
              r"vascular tissue|water[- ]conduct|plant height|plant branching|plant architecture",
    "fungi-animals": r"mycorrhiz|arbuscul|glomeromycot|mucoromycot|\bfungi\b|\bfungal|\blichen|terrestrial arthropod|myriapod|"
                     r"pneumodesmus|euthycarcinoid|trigonotarbid|rhyniognatha|hexapod|herbivor|invasion of the land|"
                     r"terrestrial(?:i[sz]ation| invasion| ecosystem)|\barachnid|scorpion",
}
INTERVAL = (r"ordovician|silurian|devonian|palaeozoic|paleozoic|llandover|wenlock|ludlow|pridol|lochkov|pragian|emsian|"
            r"eifelian|givetian|frasnian|famennian|katian|sandbian|darriwilian|hirnantian|rhuddanian|aeronian|telychian|"
            r"sheinwoodian|homerian|gorstian|ludfordian|cambrian|mid-paleozoic|mid-palaeozoic")
PLANT_CTX = (r"\bplants?\b|flora|vegetation|forest|\bferns?\b|\bmoss|spore|sporang|palynolog|stomat|cuticle|tracheid|xylem|"
             r"\broots?\b|\bleaf|\bleaves|lignin|mycorrhiz|fung|lichen|\balgae|\balgal|herbivor|arthropod|myriapod|"
             r"weathering|paleosol|palaeosol|charcoal|wildfire|terrestrial|\bsoils?\b")
ESYS = (r"weathering|atmospheric (?:co2|oxygen|o2)|carbon cycle|carbon dioxide|\bpco2|geocarb|copse|anoxi|paleosol|palaeosol|"
        r"\bsoils?\b|\brivers?\b|fluvial|alluvial|charcoal|wildfire|fusain|phosph|eutroph|biogeochemic|oxygenation|"
        r"carbon burial|silicate")
METHODS_PAT = (r"stratigraphic range|range extension|range end|confidence interval|signor|fossili[sz]ed birth|birth[- ]death|"
               r"pyrate|deepdive|preservation rate|sampling rate|first appearance|last appearance|origination time|"
               r"time of origin|tip[- ]dating|total[- ]evidence|fossil calibration|calibrat|node dating|molecular clock|"
               r"divergence time|sampling bias|completeness|taphonom|range[- ]through|three[- ]timer|stratigraphic uncertainty|"
               r"extinction (?:date|time)|sighting|preservation|origination and extinction|time[- ]averaging|ghost lineage|"
               r"pull of the recent|rock record")
METHODS_CTX = r"fossil|stratigraph|palaeo|paleo|extinction|origination|diversif|lineage|clade"

WATCH_AUTHORS = {
    "Edwards": r"^(?:d(?:ianne|\.)?\s*(?:\w\.\s*)?)edwards$|dianne edwards|^d\.? ?edwards$",
    "Wellman": r"wellman", "Kenrick": r"kenrick", "Crane": r"^(?:peter r\.? )?crane$|peter.* crane",
    "Gensel": r"gensel", "Hetherington": r"hetherington", "Strother": r"strother",
    "Morris, J.L.": r"jennifer l\.? morris|^j\.? ?l\.? morris$|jennifer morris", "Berner": r"robert a\.? berner|^r\.? ?a\.? berner$",
    "Lenton": r"lenton", "Boyce": r"boyce", "Taylor, T.N.": r"thomas n\.? taylor|^t\.? ?n\.? taylor$",
    "Kerp": r"hans kerp|^h\.? kerp$", "Remy": r"winfried remy|^w\.? remy$", "Steemans": r"steemans",
    "Gerrienne": r"gerrienne", "Cascales-Minana": r"cascales", "Capel": r"capel", "Raymond": r"annie raymond|^a\.? raymond$",
    "Niklas": r"niklas", "Beerling": r"beerling", "Algeo": r"algeo", "Scheckler": r"scheckler", "Labandeira": r"labandeira",
    "Shear": r"william a\.? shear|^w\.? a\.? shear$", "Garwood": r"garwood", "Strullu-Derrien": r"strullu", "Hueber": r"hueber",
    "Banks": r"harlan p\.? banks|^h\.? p\.? banks$", "Doran": r"doran", "Hao": r"shougang hao|hao shougang|^s\.? hao$",
    "Xue": r"jinzhuang xue|xue jinzhuang", "Tomescu": r"tomescu", "Stein": r"william e\.? stein|^w\.? e\.? stein$",
    "Rothwell": r"rothwell", "Donoghue": r"donoghue", "Puttick": r"puttick", "Harrison": r"c\.? jill harrison|^c\.? j\.? harrison$",
    "Dahl": r"tais w\.? dahl|^t\.? w\.? dahl$", "Arens": r"arens", "Cleal": r"cleal", "Retallack": r"retallack",
    "Glasspool": r"glasspool", "Gibling": r"gibling", "Davies": r"neil s\.? davies|^n\.? s\.? davies$", "Gray": r"jane gray|^j\.? gray$",
    "Boucot": r"boucot", "Servais": r"servais", "Vecoli": r"vecoli", "Rubinstein": r"rubinstein", "Beck": r"john m\.? beck|^j\.? m\.? beck$",
    "Richardson": r"john b\.? richardson|^j\.? b\.? richardson$", "Libertin": r"libert", "Bek": r"jir.* bek|^j\.? bek$",
    "Meyer-Berthaud": r"meyer-berthaud", "Decombeix": r"decombeix", "Prestianni": r"prestianni", "Mosbrugger": r"mosbrugger",
    "Roth-Nebelsick": r"roth-nebelsick", "Haig": r"david haig|^d\.? haig$", "Bower": r"bower", "McElwain": r"mcelwain",
    "Royer": r"dana l\.? royer|^d\.? l\.? royer$", "Bradshaw": r"corey j\.? a\.? bradshaw|^c\.? j\.? a\.? bradshaw$|bradshaw",
    "Silvestro": r"silvestro", "Marshall": r"charles r\.? marshall|^c\.? r\.? marshall$", "Alroy": r"alroy",
    "Foote": r"michael foote|^m\.? foote$", "Wagner": r"peter j\.? wagner|^p\.? j\.? wagner$", "Heath": r"tracy a\.? heath",
    "Stadler": r"tanja stadler", "Gavryushkina": r"gavryushkina", "Solow": r"solow", "Liow": r"liow", "Starrfelt": r"starrfelt",
    "Morris, P.": r"^(?:peter )?morris$", "Gonez": r"gonez", "Berry": r"christopher m\.? berry|^c\.? m\.? berry$", "Kustatscher": r"kustatscher",
    "Falcon-Lang": r"falcon-lang", "Mills": r"benjamin j\.? w\.? mills|^b\.? j\.? w\.? mills$", "Dunn": r"jason p\.? dunn",
}
RELEVANT_TOPICS = {
    "ecology/plants", "taphonomy/ranges", "rates/fossil-estimation", "phylo/dating", "taphonomy/completeness",
    "diversity/sampling", "climate/oxygen-carbon", "ecology/foodwebs", "biogeography/provinces", "rates/birth-death",
}
RELEVANT_OA_TOPICS = {
    "plant diversity and evolution", "fern and epiphyte biology", "fossil insects in amber", "plant ecophysiology and growth",
    "mycorrhizal fungi and plant interactions", "lichen and bryophyte ecology", "algal ecology and management",
}
# only plant-themed venues fire the venue route on their own (with a context hit); general geology venues do not
VENUE_STRICT = (r"palaeobotan|paleobotan|palynolog|botan|plant|annals of botany|new phytologist|phytotaxa|palaeobotanist|"
                r"acta palaeobot|fossil record|alcheringa")

TEXT_STRONG = re.compile(
    "|".join(STRONG[k] for k in ("taxa", "groups")) + r"|cryptospor|trilete|embryophyt|land plants|early land plant",
    I)


def compile_all():
    c = {k: re.compile(v, I) for k, v in STRONG.items()}
    return (c, re.compile(INTERVAL, I), re.compile(PLANT_CTX, I), re.compile(ESYS, I), re.compile(METHODS_PAT, I),
            re.compile(METHODS_CTX, I))


def run_fts(store, queries, limit, hits):
    lib = os.path.join(store, "_tools", "library.py")
    for sset, group, q in queries:
        p = subprocess.run([sys.executable, lib, "search", "--tsv", "--limit", str(limit), "--store", store, q],
                           capture_output=True, text=True)
        if p.returncode != 0:
            print("FTS error", q, p.stderr[:200], file=sys.stderr)
            continue
        rows = list(csv.DictReader(p.stdout.splitlines(), delimiter="\t"))
        for rank, r in enumerate(rows, 1):
            hits[r["openalex_id"]].append((sset, group, q, r["matched"], rank))
        print(f"{len(rows):4d}  {sset}/{group}  {q}", file=sys.stderr)


QUESTION_TAGS = {"Q-005", "Q-006", "Q-017", "Q-019", "Q-041", "Q-042", "B-007"}

G = {}


def process(w):
    """Evaluate one work against the routes; return a row or None."""
    groups, interval, plant_ctx, esys, methods_pat, methods_ctx = G["rx"]
    watch, venue_strict, fts, store = G["watch"], G["venue"], G["fts"], G["store"]
    wid = w["openalex_id"]
    head = " ".join([w["title"], w["abstract"], " ".join(w["keywords"]), " ".join(w["concepts"])])
    tit = w["title"]
    routes = []
    sg = {}
    for g, rx in groups.items():
        m = sorted({x.lower() for x in rx.findall(head)})
        if m:
            sg[g] = m
    spec_spore = re.search(
        r"cryptospor|trilete|dyad|permanent tetrad|miospore|sporopollenin|megaspore|heterospor|spore wall", head, I)
    per = sorted({x.lower() for x in interval.findall(head)})
    es = bool(esys.search(head))
    ctx = bool(plant_ctx.search(head))
    mt = bool(methods_pat.search(head)) and bool(methods_ctx.search(head))
    if any(g in sg for g in ("taxa", "groups", "origin", "traits")) or spec_spore or (per and (ctx or es or sg)):
        routes.append("abstract")
    if tit and (re.search(STRONG["taxa"] + "|" + STRONG["groups"], tit, I) or re.search(
            r"cryptospor|trilete|embryophyt|land plants?|vascular plant|terrestriali[sz]ation", tit, I)
            or (interval.search(tit) and (plant_ctx.search(tit) or esys.search(tit)))):
        routes.append("title")
    mtit = bool(methods_pat.search(w["title"]) and methods_ctx.search(head))
    if mt and (w["topic"] in RELEVANT_TOPICS or mtit):
        routes.append("methods-text")
    fh = fts.get(wid, [])
    if fh:
        routes.append("fts")
    tops = {t.lower() for t in w["topics"]}
    if w["topic"] in RELEVANT_TOPICS or (w["oa_topic"] or "").lower() in RELEVANT_OA_TOPICS or tops & RELEVANT_OA_TOPICS:
        routes.append("topic")
    if QUESTION_TAGS & set(re.split(r"[;, ]+", w["questions"] or "")):
        routes.append("question")
    ah = sorted({k for k, rx in watch.items() for au in w["authors"] if rx.search(au)})
    if ah and (ctx or es or per or sg or venue_strict.search(w["venue"] or "")):
        routes.append("author")
    if venue_strict.search(w["venue"] or "") and (sg or per or es):
        routes.append("venue")
    td = tt = 0
    ttop = ""
    if w["has_text_file"]:
        try:
            with open(os.path.join(store, "text", wid + ".txt"), encoding="utf-8", errors="replace") as tf:
                txt = tf.read()
            cnt = collections.Counter(x.lower() for x in TEXT_STRONG.findall(txt))
            td, tt = len(cnt), sum(cnt.values())
            ttop = ",".join(f"{k}:{v}" for k, v in cnt.most_common(4))
        except OSError:
            pass
        if td >= 3 and tt >= 12:
            routes.append("text")
    if not routes or routes == ["topic"]:
        return None
    fqs = [f"{q}[{m}]" for (_, _, q, m, _) in fh]
    fa_p = len({h[2] for h in fh if h[0] == "plants" and "abstract" in h[3]})
    fa_m = len({h[2] for h in fh if h[0] == "methods" and "abstract" in h[3]})
    return [wid, w["doi"], w["year"], w["first_author"], w["title"], w["venue"], w["type"], w["cited_by"],
            w["oa_status"], w["fulltext"], w["tiers"], w["questions"], w["topic"], w["oa_topic"],
            int(w["has_text_file"]), len(w["abstract"]), ",".join(sg), "|".join(sorted({t for v in sg.values() for t in v})),
            ",".join(per), int(es), int(mt), ";".join(routes), len(fh), fa_p, fa_m, ",".join(sorted({h[0] for h in fh})),
            " ; ".join(fqs), ",".join(ah), td, tt, ttop]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True)
    ap.add_argument("--store", default="/data/codex/artifacts/eprp-paleodata-backup/latest/library")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fts-out", required=True)
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    fts = collections.defaultdict(list)
    run_fts(a.store, library_queries.all_queries(), a.limit, fts)
    with open(a.fts_out, "w", encoding="utf-8") as fh:
        fh.write("openalex_id\tset\tgroup\tquery\tmatched\trank\n")
        for w, hs in fts.items():
            for h in hs:
                fh.write("\t".join([w, *map(str, h)]) + "\n")

    G["rx"] = compile_all()
    G["watch"] = {k: re.compile(v, I) for k, v in WATCH_AUTHORS.items()}
    G["venue"] = re.compile(VENUE_STRICT, I)
    G["fts"] = fts
    G["store"] = a.store
    works = [json.loads(line) for line in open(a.features, encoding="utf-8")]
    cols = ["openalex_id", "doi", "year", "first_author", "title", "venue", "type", "cited_by", "oa_status", "fulltext",
            "tiers", "questions", "topic", "oa_topic", "has_text_file", "n_abs", "strong_groups", "strong_terms",
            "periods", "esys", "methods", "routes", "fts_n", "fts_plants_abs", "fts_methods_abs", "fts_sets",
            "fts_queries", "author_hits", "text_distinct", "text_total", "text_top"]
    n_out = 0
    with multiprocessing.get_context("fork").Pool(a.workers) as pool, open(a.out, "w", newline="", encoding="utf-8") as out:
        wr = csv.writer(out, delimiter="\t", lineterminator="\n")
        wr.writerow(cols)
        for row in pool.imap(process, works, chunksize=100):
            if row:
                wr.writerow(row)
                n_out += 1
    print(f"candidates: {n_out}", file=sys.stderr)


if __name__ == "__main__":
    main()
