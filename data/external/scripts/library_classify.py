"""Classify the silurian_plants literature store and build the project's library tables (no network).

Usage (on deep-server, from _tools/, after `library.py resolve` and `library.py index --out STORE/_index`):
  python3 library_classify.py [--store DIR] [--out DIR]

Reads STORE/openalex/*.json, STORE/_index/works.tsv (library.py's merged one-row-per-work index), the seed
tiers in _tools/seeds/ and library_screen_decisions.tsv (the manual title-and-abstract screen). Writes to
--out (default STORE/_build/): works.tsv, cited_dois_resolution.tsv, screen.tsv, abstracts.tsv,
closed_candidates.csv, counts.tsv and stats.json.

Subsets
  priority_spores  rule-passing, screened-in dispersed-spore occurrence papers, 2007-2026 (see RULES)
  cards            works resolved from DOIs cited in taxa/*.md and docs/*.md (tier cited)
  window_other     works of tier window that are not priority_spores (may overlap cards)
  window-marine    works of tier window-marine (acritarch, chitinozoan, phytoplankton; sampling effort)
Access classes (from OpenAlex's own fields; Unpaywall is not used)
  oa_pdf           an open-access location (best_oa_location or any is_oa location) gives a pdf_url
  oa_status_only   OpenAlex says open access (is_oa or oa_status other than closed) but gives no pdf_url
  closed           otherwise
"""

import argparse
import csv
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import library as L  # noqa: E402

csv.field_size_limit(sys.maxsize)

REGIONS = {
    "1": "Laurentia (incl. Scotland, Svalbard)",
    "2": "Avalonia, Baltica, peri-Gondwanan Europe",
    "3": "North Africa",
    "4": "Arabia, Iran, Turkey",
    "5": "South America",
    "6": "South Africa, Australia, other Gondwana",
    "7": "South China, Tarim, E Asia, Siberia, Kazakhstania",
    "8": "Unassigned",
}
REGION_KEYWORDS = {
    "1": r"canad|arctic|nunavut|ellesmere|greenland|svalbard|spitsbergen|scotland|scottish|laurentia|united states|appalachian|\bohio\b|pennsylvania|new york|michigan|anticosti|qu[eé]bec|gasp[eé]|ontario|alaska|texas|north america|utah|tennessee|virginia|maine\b|new brunswick|midland valley",
    "2": r"england|english|\bwales\b|welsh|britain|british|belgi|ardenne|german|rhenish|poland|polish|baltic|baltica|estonia|latvia|lithuania|sweden|swedish|gotland|norway|finland|bohemia|czech|barrandian|prague|spain|spanish|iberia|portugal|france|french|armorica|ukrain|podoli|moesia|austria|ital|ireland|avalonia|newfoundland|netherlands|holy cross",
    "3": r"liby|algeria|morocc|tunisia|egypt|sahara|ghadam|murzuq|tidikelt|north africa|chad\b",
    "4": r"saudi|arabia|\biran|turk[ei]|jordan|oman\b|iraq|syria|qusaiba|alborz|zagros|kerman|anatolia|taurides",
    "5": r"argentin|bolivia|brazil|paran[aá]|amazon|peru\b|colombia|uruguay|paraguay|chile|venezuela|precordillera|south america|andean|tarija",
    "6": r"south africa|australia|tasmania|new zealand|antarctica|\bindia|himalaya|spiti|ethiopia|falkland|gondwana",
    "7": r"china|chinese|yunnan|guizhou|sichuan|xinjiang|tarim|siberia|kazakhstan|japan|korea|junggar|kunlun|vietnam|kuznetsk|tungus|qujing|zhejiang",
}
KEYWORD_RX = {k: re.compile(v, re.I) for k, v in REGION_KEYWORDS.items()}

SPORE_RX = re.compile(r"spore|trilete|monolete|sporomorph|miospore", re.I)
PALYNO_RX = re.compile(r"palynolog|palynomorph|palynoflor|palynostrat|palynozon|palynofac", re.I)
STAGE_TERMS = ("ordovician silurian devonian siluro tremado floian arenig dapingian darriwilian llanvirn llandeil sandbian "
               "katian caradoc ashgill hirnantian llandover rhuddanian aeronian telychian wenlock sheinwoodian homerian "
               "ludlow gorstian ludfordian pridol přídolí lochkovian gedinn pragian siegen emsian downtonian gothlandian "
               "dittonian").split()
STAGE_RX = re.compile("|".join(STAGE_TERMS), re.I)

OSD = re.compile(r"ordovician|silurian|devonian|siluro|ordovic|tremado|arenig|llanvirn|caradoc|ashgill|llandover|wenlock|"
                 r"ludlow|pridol|přídolí|lochkov|gedinn|pragian|siegen|emsian|dapingian|darriwilian|sandbian|katian|hirnantian", re.I)
OUTSIDE_PERIOD = re.compile(
    r"cambrian|carboniferous|mississippian|pennsylvanian|permian|triassic|jurassic|cretaceous|paleogene|palaeogene|neogene|"
    r"tertiary|quaternary|holocene|pleistocene|mesozoic|cenozoic|proterozoic|ediacaran|cryogenian|pliocene|miocene|eocene|"
    r"oligocene|paleocene|palaeocene|stephanian|westphalian|namurian|visean|tournaisian|lias|bajocian|albian|barremian|"
    r"aptian|cenomanian|turonian|campanian|maastrichtian|ladinian|carnian|norian|anisian|rhaetian|anthropocene|late glacial|permo", re.I)
LATE_DEV = re.compile(r"middle devonian|late devonian|upper devonian|mid-devonian|frasnian|famennian|givetian|eifelian|"
                      r"middle[- ]late devonian|devonian[- ]carboniferous|devonian[/-]mississippian|dev\.?-carb", re.I)
EARLY = re.compile(r"lower devonian|early devonian|emsian|lochkovian|pragian|siegenian|gedinnian|silur|ordovic|pridol|přídolí|"
                   r"siluro|early[- ]middle devonian|lower[- ]middle devonian|early to middle devonian", re.I)

CHRONO = [("Dapingian", r"dapingian"), ("Darriwilian", r"darriwilian|llanvirn"), ("Sandbian", r"sandbian"),
          ("Katian", r"katian|caradoc"), ("Hirnantian", r"hirnantian|ashgill"), ("Llandovery", r"llandover|rhuddanian|aeronian|telychian"),
          ("Wenlock", r"wenlock|sheinwoodian|homerian"), ("Ludlow", r"ludlow|gorstian|ludfordian"),
          ("Pridoli", r"pridol|přídolí"), ("Lochkovian", r"lochkov|gedinn"), ("Pragian", r"pragian|siegen"), ("Emsian", r"emsian")]
CHRONO_PERIOD = [("Ordovician", r"ordovic"), ("Silurian", r"silur"), ("Devonian", r"devonian")]


def auto_class(title, typ):
    t = title or ""
    if typ in ("review", "reference-entry"):
        return "review", "type review or reference entry"
    if re.search(r"\breview\b|overview|retrospective|history of|state[- ]of[- ]the[- ]art|perspective", t, re.I):
        return "review", "title: review or overview"
    if re.search(r"ultrastructur|wall structure|\bTEM\b|transmission electron|\bSEM\b|nanostructur|chemical composition|\bFTIR\b|"
                 r"raman|sporopollenin|wall (layer|morpholog)|spore wall|exine", t, re.I):
        return "ultrastructure", "title: ultrastructure or wall chemistry"
    if re.search(r"in situ|sporangi|fructification|spore-bearing|mesofossil|reproductive|fertile|strobil|cone\b", t, re.I) \
            and not re.search(r"dispersed|assemblage|miospore|palynolog|biostratig", t, re.I):
        return "in_situ", "title: in situ spores or sporangia"
    if OUTSIDE_PERIOD.search(t) and not OSD.search(t):
        return "outside_period", "title: Cambrian, Carboniferous, Mesozoic or younger, no Ordovician-Devonian term"
    if LATE_DEV.search(t) and not EARLY.search(t):
        return "outside_epoch", "title: Middle or Late Devonian only (younger than Emsian)"
    return "", ""


def candidate_rule(title, abstract):
    txt = f"{title} {abstract}"
    stage = STAGE_RX.search(txt)
    if SPORE_RX.search(txt) and stage:
        return "R1"
    if PALYNO_RX.search(txt) and stage:
        return "R2"
    if SPORE_RX.search(title) and not stage:
        return "R3"
    return ""


RULE_TEXT = [
    ("R1", "Spore terms (spore, cryptospore, miospore, trilete, monolete, sporomorph) in title or abstract AND a window term "
           "(Ordovician, Silurian, Devonian or any Dapingian-Emsian stage or old name such as Llanvirn, Caradoc, Ashgill, "
           "Llandoverian, Ludlovian, Gedinnian, Siegenian) in title or abstract; publication year 2007-2026; type not "
           "dataset, paratext, erratum, retraction, editorial, letter, peer-review, grant, standard or supplementary."),
    ("R2", "Palynology terms (palynolog*, palynomorph*, palynoflor*, palynostrat*, palynozon*, palynofac*) AND a window term, "
           "but no spore term; same year and type limits. Added because OpenAlex lacks many abstracts, so titles such as "
           "'Palynology of the Lower Devonian ...' would otherwise be lost. Included only if the title or abstract points to "
           "land-derived palynomorphs or generic palynology of in-window strata and no abstract names only acritarchs or "
           "chitinozoans (basis palynology_title_only, confidence low)."),
    ("R3", "A spore term in the title but no window term in title or abstract (mostly works without an abstract); same limits. "
           "Screened by reading."),
    ("auto", "Automatic exclusions from the title, applied before the manual screen: review (type review or title review, "
             "overview, history of, perspective), ultrastructure, in_situ (sporangia, in situ spores), outside_period "
             "(Cambrian, Carboniferous, Mesozoic or younger with no Ordovician-Devonian term), outside_epoch (Middle or Late "
             "Devonian only). A manual decision overrides an automatic class."),
    ("manual", "Every remaining candidate was read by title (and abstract where unclear). include: reports dispersed-spore or "
               "cryptospore assemblages of Dapingian-Emsian age from rock samples. include_borderline: probable but "
               "unconfirmed (no abstract, mixed marine and terrestrial palynomorphs, or the assemblage is part of a wider "
               "study). exclude: ultrastructure, in situ spores only, reviews and syntheses (kept as cross-check sources), "
               "Cambrian, Tremadocian-Floian, Carboniferous, Mesozoic, Middle-Late Devonian only, marine palynomorph-only, "
               "methods, catalogues, geochemistry. Default for an unreviewed candidate is exclude."),
    ("region", "Region is the plan's table (docs/spore-compilation-plan.md section 2): assigned by reading the title and "
               "abstract; region_secondary names a second region where the paper spans two. Country keywords are used only "
               "as a check. Tibet, Himalaya, Ethiopia and the Falklands count as other Gondwana; Maine and the Gaspe-New "
               "Brunswick belt as Laurentia; Ireland, Newfoundland and the Moesian terrane as Avalonia, Baltica, "
               "peri-Gondwanan Europe; global compilations are Unassigned."),
]


def abstract_of(rec):
    return re.sub(r"\s+", " ", L.abstract_text(rec)).strip()


def oa_fields(rec):
    oa = rec.get("open_access") or {}
    status = oa.get("oa_status") or ""
    best = rec.get("best_oa_location") or {}
    pdf = bool(best.get("pdf_url")) or any(loc.get("is_oa") and loc.get("pdf_url") for loc in rec.get("locations") or [])
    is_oa = bool(oa.get("is_oa")) or status not in ("", "closed")
    return status, pdf, ("oa_pdf" if pdf else "oa_status_only" if is_oa else "closed")


def publisher_of(rec):
    src = (rec.get("primary_location") or {}).get("source") or {}
    return src.get("host_organization_name") or src.get("display_name") or ""


def ages_of(title, abstract):
    txt = f"{title} {abstract}"
    hits = [i for i, (_, rx) in enumerate(CHRONO) if re.search(rx, txt, re.I)]
    if hits:
        lo, hi = CHRONO[min(hits)][0], CHRONO[max(hits)][0]
        return lo if lo == hi else f"{lo}-{hi}"
    per = [n for n, rx in CHRONO_PERIOD if re.search(rx, txt, re.I)]
    return "-".join(per[:1] + per[-1:]) if len(set(per)) > 1 else (per[0] if per else "Ordovician-Devonian")


def region_check(title, abstract):
    scores = {k: 3 * len(rx.findall(title)) + len(rx.findall(abstract)) for k, rx in KEYWORD_RX.items()}
    scores = {k: v for k, v in scores.items() if v}
    return max(scores, key=scores.get) if scores else ""


def card_label(path):
    p = Path(path)
    return p.stem if p.parts[0] == "taxa" else path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", type=Path, default=Path("/data/codex/silurian_plants/library"))
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    store, out = a.store, a.out or a.store / "_build"
    out.mkdir(parents=True, exist_ok=True)

    recs = L.load_records(store)
    aliases = L.load_aliases(store)
    seeds = L.load_seeds()
    index_rows = L.read_tsv(store / "_index" / "works.tsv")
    decisions = {r["openalex_id"]: r for r in L.read_tsv(HERE / "library_screen_decisions.tsv")}

    canon_of = {}
    for r in index_rows:
        canon_of[r["openalex_id"]] = r["openalex_id"]
        for m in filter(None, r["merged"].split(";")):
            canon_of[m] = r["openalex_id"]
    subset_seed_tiers = {"priority_spores", "cards"}  # phase 2 fetch seeds, not classification tiers
    tiers_of = {r["openalex_id"]: set(r["tiers"].split(";")) - subset_seed_tiers for r in index_rows}

    cited_files = defaultdict(set)
    cited_doi_rows = []
    for r in seeds["cited"]:
        wid = L.seed_wid(r, aliases)
        cw = canon_of.get(wid, wid) if wid in recs else None
        files = set(filter(None, (r.get("files") or "").split(";")))
        cited_doi_rows.append((r["doi"], files, wid if wid in recs else None, cw))
        if cw:
            cited_files[cw] |= files

    # ---- screen
    screen_rows = [{"kind": "rule", "rule": k, "reason": v} for k, v in RULE_TEXT]
    screened = {}
    rule_counts = Counter()
    for wid, rec in sorted(recs.items(), key=lambda kv: ((kv[1].get("publication_year") or 0), kv[0])):
        year = rec.get("publication_year") or 0
        if not (2007 <= year <= 2026) or rec.get("type") in L.SKIP_TYPES:
            continue
        title = re.sub(r"\s+", " ", rec.get("title") or "").strip()
        ab = abstract_of(rec)
        rule = candidate_rule(title, ab)
        d = decisions.get(wid)
        if not rule and not d:
            continue
        auto, auto_reason = auto_class(title, rec.get("type"))
        if d:
            decision, basis, reason = d["decision"], d["basis"], d["reason"]
            region, region2 = d["region"], d["region_secondary"]
        elif auto:
            decision, basis, reason, region, region2 = "exclude", "", auto_reason, "", ""
        else:
            decision, basis, region, region2 = "exclude", "", "", ""
            reason = ("palynology-only candidate not judged to report spores" if rule == "R2"
                      else "spore-term-in-title candidate without window term; not a window occurrence paper" if rule == "R3"
                      else "not a dispersed-spore occurrence paper (title and abstract screen)")
        if decision.startswith("include") and not region:
            region = region_check(title, ab) or "8"
        rule_counts[rule or "decision_only"] += 1
        screened[wid] = {"decision": decision, "region": region, "region2": region2}
        screen_rows.append({
            "kind": "screen", "openalex_id": wid, "canonical_id": canon_of.get(wid, wid), "doi": L.norm_doi(rec.get("doi")),
            "year": year, "type": rec.get("type"), "title": title, "rule": rule or "decision_only", "auto_class": auto,
            "decision": decision, "basis": basis or ("spore_terms" if rule == "R1" else ""), "reason": reason,
            "region": REGIONS.get(region, ""), "region_secondary": REGIONS.get(region2, ""),
            "region_keyword_check": REGIONS.get(region_check(title, ab), "") if decision.startswith("include") else ""})
    L.write_tsv(out / "screen.tsv", screen_rows, ["kind", "openalex_id", "canonical_id", "doi", "year", "type", "title", "rule",
                                                   "auto_class", "decision", "basis", "reason", "region", "region_secondary",
                                                   "region_keyword_check"])

    priority = {}
    for wid, s in screened.items():
        if s["decision"].startswith("include"):
            cw = canon_of.get(wid, wid)
            cur = priority.get(cw)
            if cur is None or (cur["decision"] != "include" and s["decision"] == "include"):
                priority[cw] = dict(s, via=wid)

    # ---- works
    manifest = L.load_manifest(store)
    held_ids = {w for w, m in manifest.items() if m["status"] in L.OPEN_HELD and (store / (m.get("path") or f"pdf/{w}.pdf")).exists()}
    works, abstracts, closed = [], [], []
    for r in index_rows:
        wid = r["openalex_id"]
        rec = recs[wid]
        tiers = tiers_of[wid]
        subsets = []
        if wid in priority:
            subsets.append("priority_spores")
        if "cited" in tiers:
            subsets.append("cards")
        if "window" in tiers and wid not in priority:
            subsets.append("window_other")
        if "window-marine" in tiers:
            subsets.append("window-marine")
        status, pdf, access = oa_fields(rec)
        region = REGIONS.get(priority[wid]["region"], "") if wid in priority else ""
        title = re.sub(r"\s+", " ", rec.get("title") or "").strip()
        row = {"openalex_id": wid, "doi": L.norm_doi(rec.get("doi")), "year": rec.get("publication_year") or "",
               "first_author": L.first_author(rec), "title": title, "venue": L.venue(rec), "type": rec.get("type") or "",
               "language": rec.get("language") or "", "oa_status": status, "has_oa_pdf_url": "yes" if pdf else "no",
               "tiers": ";".join(sorted(tiers)), "subsets": ";".join(subsets), "region": region,
               "in_project": "yes" if "cited" in tiers else "no", "access": access,
               "fetch_candidates": len(L.candidates(rec)), "skipped_type": rec.get("type") in L.SKIP_TYPES}
        works.append(row)
        abstracts.append({"openalex_id": wid, "abstract": abstract_of(rec)})
        if access == "closed" and ("priority_spores" in subsets or "cards" in subsets):
            reasons = []
            if "priority_spores" in subsets:
                reasons.append(f"{ages_of(title, abstract_of(rec))} spore assemblage, {region}")
            if "cards" in subsets:
                labels = sorted(card_label(f) for f in cited_files[wid])
                reasons.append("cited by " + ("card " if all(not x.startswith("docs/") for x in labels) else "")
                               + ", ".join(labels[:6]) + (f" (+{len(labels) - 6} more)" if len(labels) > 6 else ""))
            closed.append({"doi": row["doi"], "title": title, "first_author": row["first_author"], "year": row["year"],
                           "venue": row["venue"], "publisher": publisher_of(rec), "subset": ";".join(
                               s for s in subsets if s in ("priority_spores", "cards")), "region": region,
                           "priority_reason": "; ".join(reasons), "open_copy_held": "yes" if wid in held_ids else "no"})
    fields = ["openalex_id", "doi", "year", "first_author", "title", "venue", "type", "language", "oa_status", "has_oa_pdf_url",
              "tiers", "subsets", "region", "in_project", "access"]
    L.write_tsv(out / "works.tsv", works, fields)
    L.write_tsv(out / "abstracts.tsv", abstracts, ["openalex_id", "abstract"])
    closed.sort(key=lambda r: (r["subset"], str(r["year"]), r["first_author"]))
    with open(out / "closed_candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, ["doi", "title", "first_author", "year", "venue", "publisher", "subset", "region", "priority_reason", "open_copy_held"],
                           lineterminator="\n")
        w.writeheader()
        w.writerows(closed)

    # ---- cited DOI resolution
    by_work = defaultdict(list)
    for doi, files, wid, cw in cited_doi_rows:
        if cw:
            by_work[cw].append(doi)
    dead = {r["key"]: r for r in L.read_tsv(store / "unresolved-keys.tsv")} if (store / "unresolved-keys.tsv").exists() else {}
    res_rows = []
    for doi, files, wid, cw in cited_doi_rows:
        if not wid:
            d = dead.get(f"doi:{doi}")
            res_rows.append({"doi": doi, "source_files": ";".join(sorted(files)), "openalex_id": "unresolved",
                             "reason": f"OpenAlex has no work; registry {d['status'] if d else 'not recorded'}"})
            continue
        rec = recs[wid]
        notes = []
        rdoi = L.norm_doi(rec.get("doi"))
        if rdoi and rdoi != doi:
            notes.append(f"OpenAlex DOI differs: {rdoi}")
        if not rdoi:
            notes.append("OpenAlex record has no DOI")
        if rec.get("type") in L.SKIP_TYPES:
            notes.append(f"record type {rec.get('type')}")
        if cw != wid:
            notes.append(f"merged into {cw} by library.py index")
        others = [x for x in by_work[cw] if x != doi]
        if others:
            notes.append("same work as " + ", ".join(others))
        res_rows.append({"doi": doi, "source_files": ";".join(sorted(files)), "openalex_id": cw, "reason": "; ".join(notes)})
    L.write_tsv(out / "cited_dois_resolution.tsv", sorted(res_rows, key=lambda r: r["doi"]),
                ["doi", "source_files", "openalex_id", "reason"])

    # ---- counts for the gate
    sizes = []
    eprp = Path("/data/paleodata/library/manifest.tsv")
    if eprp.exists():
        sizes = [int(r["bytes"]) for r in L.read_tsv(eprp) if r.get("status") == "ok" and (r.get("bytes") or "").isdigit()]
    mb = 2.0
    mean_mb = round(statistics.mean(sizes) / 1e6, 2) if sizes else mb
    subset_names = ["priority_spores", "cards", "window_other", "window-marine"]
    precedence = {n: i for i, n in enumerate(subset_names)}
    counts, stats = [], {}

    def tally(label, rows):
        n = len(rows)
        fetchable = [r for r in rows if not r["skipped_type"]]
        c = Counter(r["access"] for r in rows)
        counts.append({"subset": label, "works": n, "skipped_type": n - len(fetchable), "oa_pdf_url": c["oa_pdf"],
                       "oa_status_only": c["oa_status_only"], "closed": c["closed"],
                       "with_fetch_candidate": sum(1 for r in fetchable if r["fetch_candidates"]),
                       "est_pdfs_pdf_url": sum(1 for r in fetchable if r["access"] == "oa_pdf"),
                       "est_mb_pdf_url": round(sum(1 for r in fetchable if r["access"] == "oa_pdf") * mb),
                       "est_mb_all_candidates": round(sum(1 for r in fetchable if r["fetch_candidates"]) * mb),
                       "est_mb_pdf_url_at_eprp_mean": round(sum(1 for r in fetchable if r["access"] == "oa_pdf") * mean_mb),
                       "est_mb_all_candidates_at_eprp_mean": round(sum(1 for r in fetchable if r["fetch_candidates"]) * mean_mb)})

    for name in subset_names:
        tally(name, [r for r in works if name in r["subsets"].split(";")])
    tally("union (each work once)", [r for r in works if r["subsets"]])
    partition = defaultdict(list)
    for r in works:
        s = [x for x in r["subsets"].split(";") if x]
        if s:
            partition[min(s, key=precedence.get)].append(r)
    for name in subset_names:
        tally(f"exclusive: {name}", partition[name])
    cols = ["subset", "works", "skipped_type", "oa_pdf_url", "oa_status_only", "closed", "with_fetch_candidate",
            "est_pdfs_pdf_url", "est_mb_pdf_url", "est_mb_all_candidates", "est_mb_pdf_url_at_eprp_mean",
            "est_mb_all_candidates_at_eprp_mean"]
    L.write_tsv(out / "counts.tsv", counts, cols)

    # ---- priority_spores stats against the plan
    inc = [(cw, p) for cw, p in priority.items()]
    clear = [cw for cw, p in inc if p["decision"] == "include"]
    reg = Counter(REGIONS[p["region"]] for _, p in inc)
    reg_clear = Counter(REGIONS[p["region"]] for cw, p in inc if p["decision"] == "include")
    title_of = {r["openalex_id"]: r["title"] for r in works}
    year_bins = Counter()
    split = Counter()
    for cw, p in inc:
        y = int(next(r["year"] for r in works if r["openalex_id"] == cw))
        year_bins["2007-09" if y <= 2009 else "2010-14" if y <= 2014 else "2015-19" if y <= 2019 else "2020-24" if y <= 2024 else "2025-26"] += 1
        t = title_of[cw]
        title_named = bool(SPORE_RX.search(t) or PALYNO_RX.search(t))
        split["title_names_spores_or_palynology"] += title_named
        os_ = re.search(r"ordovic|silur|pridol|přídolí|katian|hirnant|llando|wenlock|ludlow", t, re.I)
        dev = re.search(r"devon|lochkov|pragian|emsian|gedinn", t, re.I)
        split["title_O-S" if os_ and not dev else "title_Devonian" if dev and not os_ else "title_both" if os_ and dev else "title_undated"] += 1
    stats.update({
        "priority_total": len(inc), "priority_clear": len(clear), "priority_borderline": len(inc) - len(clear),
        "priority_by_region_all": dict(reg), "priority_by_region_clear": dict(reg_clear),
        "priority_year_bins": dict(year_bins), "priority_title_split": dict(split),
        "candidates_by_rule": dict(rule_counts),
        "decisions": dict(Counter(s["decision"] for s in screened.values())),
        "records": len(recs), "works": len(works), "cited_dois": len(cited_doi_rows),
        "cited_resolved": sum(1 for r in res_rows if r["openalex_id"] != "unresolved"),
        "cited_distinct_works": len({r["openalex_id"] for r in res_rows if r["openalex_id"] != "unresolved"}),
        "eprp_pdf_median_mb": round(statistics.median(sizes) / 1e6, 2) if sizes else None,
        "eprp_pdf_mean_mb": round(statistics.mean(sizes) / 1e6, 2) if sizes else None, "eprp_pdf_n": len(sizes),
        "closed_candidates": len(closed),
        "region_keyword_disagreements": sum(1 for r in screen_rows if r.get("kind") == "screen" and r["decision"].startswith("include")
                                            and r["region_keyword_check"] and r["region"] != r["region_keyword_check"]),
        "unknown_decision_ids": [w for w in decisions if w not in recs],
        "included_not_rule_candidates": [w for w, d in decisions.items() if d["decision"].startswith("include") and w in recs
                                         and not candidate_rule(recs[w].get("title") or "", abstract_of(recs[w]))],
    })
    (out / "stats.json").write_text(json.dumps(stats, indent=1, ensure_ascii=False))
    print(json.dumps(stats, indent=1, ensure_ascii=False))
    for c in counts:
        print(c)


if __name__ == "__main__":
    main()
