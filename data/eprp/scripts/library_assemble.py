#!/usr/bin/env python3
"""Stage 3 of the silurian_plants library extraction: apply the screen and write the deliverables.

Inputs
  --works        EPRP resources/library/works.tsv (commit ac42dfb)
  --candidates   candidates.tsv from library_candidates.py
  --fts          fts_hits.tsv from library_candidates.py
  --decisions    library_decisions.tsv: the manual screen (keep or drop, with set, theme and note)
  --project      the silurian_plants checkout, for the in_project cross-check
Outputs (in --out): references.tsv, screened_out.tsv, README.md, MANIFEST.tsv, and the list of open texts to copy.

Candidates without a manual decision were screened by title in a first pass and dropped; their reason is
inferred from the evidence by rule (column decided_by = rule). Manual decisions carry their own note
(decided_by = manual). stdlib only; runs locally.
"""
import argparse
import collections
import csv
import datetime
import glob
import hashlib
import os
import re
import subprocess
import sys

THEME_REMAP = {}

LATER = re.compile(
    r"carbonifer|mississippian|pennsylvanian|permian|triassic|jurassic|cretaceous|paleogene|palaeogene|paleocene|"
    r"eocene|oligocene|miocene|pliocene|neogene|pleistocene|holocene|quaternary|cenozoic|mesozoic|tertiary|"
    r"stephanian|westphalian|visean|namurian|tournaisian|permo|k-t\b|k-pg|end-permian|end-triassic|p-tr", re.I)
PLANTISH = re.compile(
    r"plant|flora|vegetation|forest|spore|pollen|palynolog|fern|moss|lycop|lycophyt|bryophyt|liverwort|hornwort|"
    r"charophyt|algae|alga\b|fung|lichen|herbivor|mycorrh|paleobotan|palaeobotan|stomat|cuticle|xylem|tracheid",
    re.I)
MARINE = re.compile(
    r"trilobit|brachiopod|conodont|graptolit|coral|crinoid|bryozo|sponge|ostracod|cephalopod|gastropod|bivalve|"
    r"echinoid|echinoderm|foraminifer|stromatopor|nautiloid|ammonoid|fish|vertebrate|arthropod|chitinozoa|acritarch|"
    r"radiolari|tabulate|rugose|asteroid|ophiuroid|mollus|reef|plankton|marine|burgess|chengjiang|cambrian|ordovician|"
    r"silurian|devonian|paleozoic|palaeozoic", re.I)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"]+")


def clean_doi(raw):
    doi = raw.rstrip(".,;:'")
    for opener, closer in ("()", "[]", "<>"):
        while doi.endswith(closer) and doi.count(closer) > doi.count(opener):
            doi = doi[:-1].rstrip(".,;:'")
    return doi.lower()


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def project_text(project):
    paths = sorted(glob.glob(os.path.join(project, "docs", "**", "*.md"), recursive=True)
                   + glob.glob(os.path.join(project, "taxa", "*.md")))
    dois, blob = set(), []
    for p in paths:
        txt = open(p, encoding="utf-8").read()
        for m in DOI_RE.findall(txt):
            dois.add(clean_doi(m))
        blob.append(norm(txt))
    return dois, " ".join(blob), len(paths)


def infer_reason(c, fts_parts):
    routes = c["routes"].split(";")
    title = c["title"]
    terms = c["strong_terms"]
    per = c["periods"]
    has_plant = bool(PLANTISH.search(title + " " + terms))
    if not c["title"].strip():
        return "front matter or untitled record; no substantive content"
    if LATER.search(title) and not re.search(r"ordovician|silurian|devonian", title, re.I):
        return "later-interval palaeobotany or palaeontology (Carboniferous or younger); outside scope"
    if "methods-text" in routes or "question" in routes or "fts" in routes and c["fts_methods_abs"] != "0":
        if not has_plant and not per:
            return "methods vocabulary or EPRP question tag only; not one of the core works for F3"
    if routes == ["fts"] and not any("abstract" in p for p in fts_parts):
        return "matched only in open or TDM full text, with no title or abstract evidence; passing mention"
    if MARINE.search(title) and not re.search(r"plant|flora|spore|palynolog|vegetat|terrestr|land|soil|weather|lichen|fung|alga", title, re.I):
        return "marine invertebrate or vertebrate palaeontology; false keyword hit"
    if has_plant and not per:
        return "plant, fungal or palynological work outside the Ordovician–Devonian scope, or modern ecology"
    if per and not has_plant:
        return "Ordovician–Devonian marine or other non-plant work; false keyword hit"
    return "no substantive early land-plant, methods or earth-system content on title and abstract screen"


THEME_NOTES = {
    "plants": [
        ("early-vascular", "Rhyniophytoids, polysporangiophytes and Silurian–Devonian floras and sites (Cooksonia, Pinnatiramosus, Trout Valley, Campbellton)"),
        ("spores", "Cryptospores, trilete spores and Ordovician–Devonian palynology"),
        ("origins", "Embryophyte origins, terrestrialisation, streptophyte algae and reviews of early land plants"),
        ("rhynie-chert", "Rhynie and Windyfield chert plants and their preservation"),
        ("nematophytes", "Prototaxites, Nematothallus, banded tubes, Spongiophyton and Protosalvinia"),
        ("lycophytes", "Zosterophylls, Baragwanathia-type lycopsids and Devonian arborescent lycopsids"),
        ("euphyllophytes", "Trimerophytes, cladoxylopsids and early euphyllophytes with secondary growth"),
        ("bryophytes", "Bryophyte and liverwort fossils and fossil-calibrated bryophyte dating"),
        ("life-cycle", "Heterospory, seed origin and plant reproductive palaeobiology"),
        ("anatomy-physiology", "Stomata, tracheids, roots, leaves and hydraulics of early plants"),
        ("plant-modelling", "Simulation and process models of early plants, vegetation and their feedbacks"),
        ("fungi-lichens", "Early fungi, mycorrhiza and lichen-like organisms"),
        ("early-terrestrial-biota", "Pre-vascular and microbial terrestrial communities, including contested Cambrian palaeosol fossils"),
        ("arthropods-herbivory", "Early terrestrial arthropods, herbivory and plant–animal interactions"),
        ("plant-diversity", "Diversity curves, evolutionary floras, extinction and sampling bias in the plant record"),
        ("phytogeography", "Floral provinces and plant dispersal, Silurian–Devonian"),
        ("weathering-co2", "Weathering, CO2, O2 and carbon-cycle models, proxies and plant effects"),
        ("soils-rivers-fire", "Palaeosols, rivers, charcoal and early wildfire"),
        ("devonian-anoxia", "Devonian anoxia and its proposed plant–weathering link (mostly context; no plant claim in many abstracts)"),
        ("palaeogeography-climate", "Ordovician–Devonian palaeogeography, temperature records and the time scale"),
        ("molecular-clock", "Molecular clocks for land plants"),
    ],
    "methods": [
        ("range-estimation", "Confidence intervals and Bayesian estimators for range ends, Signor–Lipps, sighting records, origination-age estimators"),
        ("fossil-birth-death", "FBD, PyRate and DeepDive-type models; preservation-aware rate estimation; fossil-sampling simulators"),
        ("tip-dating", "Tip-dating and total-evidence dating with FBD priors"),
        ("molecular-dating", "Fossil calibration, maximum ages and clock-versus-fossil discrepancy"),
        ("rock-record-bias", "Rock-record and completeness bias, stratigraphic palaeobiology, time resolution"),
        ("plant-preservation", "Plant taphonomy and preservation bias in the plant record"),
        ("record-comparison", "Microfossil versus macrofossil and organ-level plant records"),
        ("diversity-sampling", "Sampling-standardised diversity and rate estimators"),
    ],
}


def write_readme(path, a, stats, cands, works, kept, dropped, pdois):
    ft = collections.Counter(w["fulltext"] for w in works.values())
    routes = collections.Counter()
    for c in cands.values():
        for r in c["routes"].split(";"):
            routes[r] += 1
    nread = sum(1 for r in dropped if r["screen"] == "title read")
    themes = collections.Counter((r["set"], r["theme"]) for r in kept)
    core = sum(1 for r in kept if r["screen_note"].startswith("CORE"))
    newc = collections.Counter((r["set"]) for r in kept if r["in_project"] == "no")
    tdm_kept = [r for r in kept if r["fulltext"] == "tdm"]
    lines = []
    w = lines.append
    w("# Literature library: references for silurian_plants")
    w("")
    w("References drawn from EPRP's literature library for a project on early land-plant evolution (Late Ordovician to Early")
    w("Devonian), screened for relevance, with a cross-check against what the project already cites. Extracted 2026-10-26 by a")
    w("Claude Sonnet 5.5 subagent (Anthropic) under Claude Opus 5.5 orchestration; the screen decisions are the subagent's")
    w("and have not been reviewed by Barry or a second agent.")
    w("")
    w("Files:")
    w("")
    w("- `references.tsv`: one row per kept work (%d), sorted by set, theme, year." % len(kept))
    w("- `screened_out.tsv`: every candidate that was dropped (%d), with a one-phrase reason, how it was decided (`manual` or `rule`)" % len(dropped))
    w("  and whether its title was read (`screen`). Together with `references.tsv` it covers every candidate and every work added by hand (`found_by` starts `manual`).")
    w("- `MANIFEST.tsv`: delivered files with hashes. Scripts are in `../scripts/library_*`; open full texts (%d) are in" % stats["texts"])
    w("  `../local/library/text/` (gitignored). `../local/library/work/` (gitignored) holds `candidates.tsv` and `fts_hits.tsv`, the")
    w("  evidence behind every candidate, plus the run's counts.")
    w("")
    w("## Source and store state")
    w("")
    w("- EPRP checkout `/Users/bwbrook/git/eprp` at commit `%s` (read-only). Its `resources/library/works.tsv` holds %s works." % (a.eprp_commit, format(len(works), ",")))
    w("- Store: `deep-server:/data/paleodata/library/` as of 2026-10-25 (the index files are dated 25 October 2026; `search.sqlite`")
    w("  built 2026-10-25 20:11). 29,372 OpenAlex records, 2,989 open text files, `tdm/` copies not read. Full-text status in `works.tsv`:")
    w("  " + ", ".join("%s %d" % (k, v) for k, v in ft.most_common()) + ".")
    w("- Nothing was written to EPRP or to `/data/paleodata`. Remote scratch was `/data/codex/silurian_plants-eprp/library/`.")
    w("")
    w("## Routes and queries")
    w("")
    w("Candidates came from several routes, recorded per work in the `found_by` column of both tables (routes first, then up to six")
    w("search queries with the part that matched: `abstract` is title plus OpenAlex abstract, `fulltext` an open text, `tdm` a")
    w("publisher copy that matched but was never read):")
    w("")
    w("| Route | What it does | Candidates |")
    w("| --- | --- | ---: |")
    desc = {
        "abstract": "title, OpenAlex abstract, keywords or concepts match plant-specific terms (taxa, groups, spore terms, origin terms, traits, fungi and animals) or an Ordovician–Devonian term with plant or earth-system context",
        "title": "the title alone matches those patterns",
        "fts": "any of the %d `library.py search` queries in `library_queries.py` matched (taxa, spores, origins, traits, fungi and animals, earth system, diversity, methods)" % 369,
        "topic": "EPRP canon topic id or OpenAlex topic relevant to the project (never a candidate on its own)",
        "author": "an author on a watch list (Edwards, Wellman, Kenrick, Crane, Gensel, Strother, Berner, Lenton, Boyce, Marshall, Alroy, Silvestro and others) with plant, interval or earth-system context",
        "venue": "a palaeobotany or botany venue with plant, interval or earth-system context",
        "text": "the open full text mentions at least three distinct early-plant terms, twelve times or more",
        "methods-text": "title or canon topic matches the F3 methods vocabulary (ranges, birth–death, dating, preservation, record quality)",
        "question": "EPRP question tag for range estimation, fossil-record quality, rates or dating (Q-005, Q-006, Q-017, Q-019, Q-041, Q-042, B-007)",
    }
    for r in ("abstract", "title", "fts", "topic", "author", "venue", "text", "methods-text", "question"):
        w("| %s | %s | %d |" % (r, desc[r], routes.get(r, 0)))
    w("")
    w("A work can arrive by several routes. Seventeen queries with OR were first written without parentheses (FTS5 gives OR lower")
    w("precedence than AND); they were parenthesised before the final run. Porter stemming still turns `terrestrialization` into")
    w("`terrestri*`, so full-text-only hits are noisy and the screen absorbs them. A final sweep of all %s works for methods terms in" % format(len(works), ","))
    w("titles and abstracts (Brownian bridge, FBD, PyRate, DeepDive, tip-dating, calibration, sighting records and similar) found eight")
    w("further works, added by hand.")
    w("")
    w("## Screen")
    w("")
    w("- %d candidates in all. Titles were read for %d of the dropped candidates and all kept ones; the remainder were dropped by rule" % (stats["candidates"], nread + stats["kept"]))
    w("  from title and evidence flags and are marked `rule only` in `screened_out.tsv`. About 120 borderline works also had their")
    w("  abstracts read. The rule-assigned reasons (`decided_by` = `rule`) describe why a title-level screen drops such a work; they")
    w("  are not a reading of its abstract.")
    w("- Kept: real relevance to early land plants and their world (taxa, spores, origins, anatomy, fungi, arthropods, floras,")
    w("  provinces, weathering, CO2, O2, soils, rivers, fire, Devonian anoxia), or, for the `methods` set, the works a modeller of")
    w("  framing F3 would use: range-end and origination estimators, FBD and PyRate-type models, tip-dating and calibration, rock-record")
    w("  and completeness bias, plant taphonomy. `CORE:` in `screen_note` marks the first reads in the methods set and the key")
    w("  plant-record works (%d)." % core)
    w("- Dropped: Quaternary and Cenozoic palynology, Carboniferous or later palaeobotany, modern plant ecology and genomics,")
    w("  marine invertebrate and vertebrate palaeontology that only matched a keyword (for example `Sphenothallus`, which is a marine")
    w("  tube-dwelling animal), journal covers and peer-review stubs, and general quantitative palaeobiology that is not needed for F3.")
    w("- Beyond-window works are kept when they bear on plant evolution (Middle and Late Devonian plants, Late Devonian anoxia, seed")
    w("  and heterospory origins) and say so in `screen_note`. Carboniferous and later work is kept only if it is a general model,")
    w("  diversity compilation, clock method or record-bias study.")
    w("- Works the project already cites that EPRP holds were kept even when marginal (Palaeozoic temperature and sea-level records,")
    w("  Late Ordovician extinction reviews), and say so.")
    w("- `theme` is the subagent's inference. Decisions are in `../scripts/library_decisions.tsv` (keeps and the %d manual drops)." % stats["dropped_manual"])
    w("")
    w("## Counts")
    w("")
    w("| | |")
    w("| --- | ---: |")
    w("| Candidates | %d |" % stats["candidates"])
    w("| Kept | %d |" % stats["kept"])
    w("| Kept, `plants` set | %d |" % stats["by_set"].get("plants", 0))
    w("| Kept, `methods` set | %d |" % stats["by_set"].get("methods", 0))
    w("| Dropped | %d (%d manual, %d by rule) |" % (stats["dropped"], stats["dropped_manual"], stats["dropped"] - stats["dropped_manual"]))
    w("| Kept with an open full text copied to `local/library/text/` | %d |" % stats["texts"])
    w("| Kept with an open scan that has no usable text layer (not copied; OCR needed) | %d |" % sum(1 for r in kept if "without a usable text layer" in r["screen_note"]))
    w("| Kept with a publisher TDM copy only (not copied) | %d |" % stats["tdm_only"])
    w("| Kept with no full text in EPRP | %d |" % stats["none"])
    w("| Kept and already in the project (DOI, or title) | %d |" % stats["in_project"])
    w("| Kept and new to the project | %d (plants %d, methods %d) |" % (stats["new"], newc.get("plants", 0), newc.get("methods", 0)))
    w("| DOIs found in the project's `docs/` and `taxa/` | %d |" % stats["project_dois"])
    w("")
    w("By theme (`set / theme`):")
    w("")
    w("| Set | Theme | Works | What it holds |")
    w("| --- | --- | ---: | --- |")
    for sset in ("plants", "methods"):
        for th, d in THEME_NOTES[sset]:
            w("| %s | `%s` | %d | %s |" % (sset, th, themes.get((sset, th), 0), d))
    missing = [k for k in themes if k[1] not in [t for s_, lst in THEME_NOTES.items() for t, _ in lst]]
    if missing:
        raise SystemExit("themes without notes: %s" % missing)
    w("")
    if tdm_kept:
        w("Kept works whose only full text in EPRP is a publisher TDM copy (nothing was read or copied; local reading of these is for local mining only, under EPRP's TDM rules):")
        w("")
        for r in tdm_kept:
            w("- %s %s: %s" % (r["first_author"], r["year"], r["title"][:110]))
        w("")
    w("## Columns of `references.tsv`")
    w("")
    w("`openalex_id`, `doi` (OpenAlex's), `year`, `first_author`, `title`, `venue`, `type`, `cited_by` (OpenAlex count at EPRP's harvest),")
    w("`oa_status`, `fulltext` (`open`: EPRP holds an open copy; `tdm`: publisher copy only; `none`), `local_text` (relative to")
    w("`data/eprp/`, empty if not copied), `set` (`plants` or `methods`), `theme`, `found_by`, `eprp_tiers`, `eprp_questions`,")
    w("`in_project` (DOI found in the project's docs and cards, or the title found there when the DOI is missing; the latter is")
    w("noted), `screen_note`.")
    w("")
    w("## Limits and visible gaps")
    w("")
    w("- EPRP's library is built around quantitative palaeobiology and a few core journals, so palaeobotany is thin. Only 59 of the")
    w("  project's %d DOIs are held, and works the project's primer and framings cite most are absent: for example the Morris et al." % stats["project_dois"])
    w("  2018 timescale of early land plants, Puttick et al. 2018 on land-plant interrelationships, Kenrick et al. 2012 on")
    w("  terrestrialisation, Berner 1997 and Beerling and Berner 2005 on plants and weathering, Davies and Gibling 2010 on")
    w("  Cambrian–Devonian alluvial systems, Steemans et al. 2009, Wellman et al. 2003, Rubinstein et al. 2010 and Hooper et al. 2026.")
    w("  A search of all %s works by title, and by first author and year, found none of them (the library's Puttick 2018 and Davies" % format(len(works), ","))
    w("  2010 records are different papers).")
    w("- Palaeobotany journals are covered only where cited or citing: *Review of Palaeobotany and Palynology* 7 works, *Palynology* 2,")
    w("  *International Journal of Plant Sciences* 2, *Botanical Journal of the Linnean Society* 7, *Annals of Botany* 14, *American")
    w("  Journal of Botany* 16, *New Phytologist* 32, against *Lethaia* 2,843 and *Palaeontology* 2,041. OpenAlex lacks *Palaeontology*")
    w("  before 2000 and the Journal of Paleontology run has 4,445 works without DOIs; EPRP's own README records both.")
    w("- Only a handful of works hold early-plant taxa: `Cooksonia` has one work in the titles, `Rhynie` six, `cryptospore` two,")
    w("  `Prototaxites` none. Most Silurian–Devonian plant knowledge sits outside the library. The `methods` side is much better covered.")
    w("- The first-pass `fts` route reaches full texts and TDM indexes, but TDM texts were not read, so a TDM-only work with no")
    w("  informative title or abstract could not be screened; such works are in `screened_out.tsv` as passing mentions.")
    w("- Some OpenAlex records are duplicates or stubs: two records for Over et al. 2008/2009, two Kidwell and Flessa records, three")
    w("  Womack et al. 2020 records (one kept), Marshall's peer-review stubs and journal covers. One abstract does not match its title")
    w("  (Wang et al. 2022 on confidence intervals for the duration of a mass extinction). Duplicates kept are flagged in `screen_note`.")
    w("- `cited_by`, `oa_status` and `year` are OpenAlex values at EPRP's harvest. `eprp_questions` carries only EPRP's cited-tier tags.")
    w("- Screening was by one agent. Dropped works with `screen` = `rule only` were not individually read; a random sample of 100 of")
    w("  them (seed 7), checked afterwards against titles and abstracts, contained none that is relevant.")
    w("")
    w("## DOIs")
    w("")
    w("The DOIs are OpenAlex's, via EPRP, and some are SICI-form identifiers for older *Paleobiology*, *Palaios* and *Geology* works. They")
    w("must be verified against Crossref (`uv run tools/cards.py dois` in the project) before use in cards. Never cite from this table")
    w("without checking the paper.")
    w("")
    w("## Reproduce")
    w("")
    w("From `data/eprp/scripts/`: `bash library_run.sh` copies `works.tsv` to nectar, runs `library_features.py` and")
    w("`library_candidates.py` there (under ten minutes with 16 workers), pulls `candidates.tsv` and `fts_hits.tsv` into")
    w("`../local/library/work/`, copies the open texts of kept works, and runs `library_assemble.py` and `library_manifest.py`.")
    w("The screen itself is `library_decisions.tsv` plus the rules in `library_assemble.py`; `library_screen_read.txt` lists the")
    w("candidates whose titles were read. A rerun against the same store state gives the same candidate set and the same tables.")
    w("`candidates.tsv` and `fts_hits.tsv` were reproduced byte for byte on 2026-10-29 by running the first two stages on `nectar`")
    w("against its backup of EPRP's mirror.")
    w("")
    open(path, "w", encoding="utf-8").write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--works", required=True)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--fts", required=True)
    ap.add_argument("--decisions", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--work", default="", help="directory for intermediate files (texts_to_copy.txt, stats.json); default --out")
    ap.add_argument("--read", default="", help="library_screen_read.txt: candidates whose titles were read in the screen")
    ap.add_argument("--texts-dir", default="", help="local directory holding the copied open texts; local_text is set only for files present there")
    ap.add_argument("--eprp-commit", default="ac42dfb")
    a = ap.parse_args()

    works = {r["openalex_id"]: r for r in csv.DictReader(open(a.works, encoding="utf-8"), delimiter="\t")}
    cands = {r["openalex_id"]: r for r in csv.DictReader(open(a.candidates, encoding="utf-8"), delimiter="\t")}
    fts = collections.defaultdict(list)
    for r in csv.DictReader(open(a.fts, encoding="utf-8"), delimiter="\t"):
        fts[r["openalex_id"]].append(r)
    dec = {}
    for r in csv.DictReader(open(a.decisions, encoding="utf-8"), delimiter="\t"):
        dec[r["openalex_id"]] = r
    pdois, pblob, npaths = project_text(a.project)
    read = set(open(a.read).read().split()) if a.read else set()

    def found_by(w, nq=6):
        c = cands.get(w)
        hits = fts.get(w, [])
        parts = []
        if c:
            parts.append(c["routes"].replace(";", "+"))
            if c["author_hits"]:
                parts.append("author:" + c["author_hits"])
        else:
            n0 = dec.get(w, {}).get("note", "")
            parts.append("manual: not a candidate by any route; added from the project cross-check" if n0.startswith("cited by project")
                         else "manual: not a candidate by any route; added from the methods-term sweep of titles and abstracts")
        qs = []
        for h in hits:
            tag = h["matched"].replace(";", "/")
            qs.append(f"{h['query']}[{tag}]")
        qs = sorted(set(qs), key=lambda q: (("abstract" not in q), q))
        if qs:
            parts.append("fts: " + " | ".join(qs[:nq]) + (f" (+{len(qs) - nq} more)" if len(qs) > nq else ""))
        return "; ".join(parts)

    def ft_class(status):
        return {"ok": "open", "no_text": "open", "tdm_ok": "tdm", "tdm_no_text": "tdm"}.get(status, "none")

    kept, dropped = [], []
    for w, c in cands.items():
        d = dec.get(w)
        if d and d["decision"] == "keep":
            continue
        reason = d["note"] if d and d["decision"] == "drop" and d["note"] else None
        by = "manual" if reason else "rule"
        if not reason:
            reason = infer_reason(c, [h["matched"] for h in fts.get(w, [])])
        wk = works[w]
        dropped.append({"openalex_id": w, "doi": wk["doi"], "year": wk["year"], "first_author": wk["first_author"],
                        "title": wk["title"], "venue": wk["venue"], "found_by": found_by(w, 3), "reason": reason,
                        "decided_by": by, "screen": "title read" if (w in read or by == "manual") else "rule only"})
    for w, d in dec.items():
        if d["decision"] != "keep":
            if w not in cands:
                wk = works[w]
                dropped.append({"openalex_id": w, "doi": wk["doi"], "year": wk["year"], "first_author": wk["first_author"],
                                "title": wk["title"], "venue": wk["venue"], "found_by": found_by(w, 3), "reason": d["note"],
                                "decided_by": "manual", "screen": "title read"})
            continue
        wk = works[w]
        status = wk["fulltext"]
        text_src = os.path.join(a.texts_dir, w + ".txt") if a.texts_dir else ""
        usable = False
        if ft_class(status) == "open" and (not a.texts_dir or os.path.exists(text_src)):
            usable = not a.texts_dir or len(open(text_src, encoding="utf-8", errors="replace").read().strip()) >= 200
            if a.texts_dir and not usable:
                os.remove(text_src)
        has_text = ft_class(status) == "open" and usable
        doi = wk["doi"].lower()
        by_doi = doi in pdois
        by_title = (not by_doi) and len(norm(wk["title"])) > 25 and norm(wk["title"])[:80] in pblob
        note = d["note"]
        if ft_class(status) == "open" and not has_text:
            note = (note + "; " if note else "") + "EPRP holds an open scan without a usable text layer (OCR needed)"
        if by_title:
            note = (note + "; " if note else "") + "in project by title only (DOI absent from docs and cards)"
        theme = THEME_REMAP.get(d["theme"], d["theme"])
        kept.append({
            "openalex_id": w, "doi": wk["doi"], "year": wk["year"], "first_author": wk["first_author"],
            "title": wk["title"], "venue": wk["venue"], "type": wk["type"], "cited_by": wk["cited_by"],
            "oa_status": wk["oa_status"], "fulltext": ft_class(status),
            "local_text": f"local/library/text/{w}.txt" if has_text else "", "set": d["set"], "theme": theme,
            "found_by": found_by(w), "eprp_tiers": wk["tiers"], "eprp_questions": wk["questions"],
            "in_project": "yes" if (by_doi or by_title) else "no", "screen_note": note})
    kept.sort(key=lambda r: (r["set"], r["theme"], int(r["year"] or 0), r["first_author"], r["title"]))
    dropped.sort(key=lambda r: (r["decided_by"], r["reason"], int(r["year"] or 0), r["first_author"]))

    os.makedirs(a.out, exist_ok=True)
    work = a.work or a.out
    os.makedirs(work, exist_ok=True)
    kcols = ["openalex_id", "doi", "year", "first_author", "title", "venue", "type", "cited_by", "oa_status", "fulltext",
             "local_text", "set", "theme", "found_by", "eprp_tiers", "eprp_questions", "in_project", "screen_note"]
    with open(os.path.join(a.out, "references.tsv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=kcols, delimiter="\t", lineterminator="\n")
        wr.writeheader()
        wr.writerows(kept)
    dcols = ["openalex_id", "doi", "year", "first_author", "title", "venue", "found_by", "reason", "decided_by", "screen"]
    with open(os.path.join(a.out, "screened_out.tsv"), "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=dcols, delimiter="\t", lineterminator="\n")
        wr.writeheader()
        wr.writerows(dropped)
    with open(os.path.join(work, "texts_to_copy.txt"), "w") as fh:
        for r in kept:
            if r["local_text"]:
                fh.write(r["openalex_id"] + ".txt\n")

    stats = {
        "candidates": len(cands), "kept": len(kept), "dropped": len(dropped),
        "dropped_manual": sum(1 for r in dropped if r["decided_by"] == "manual"),
        "by_set": collections.Counter(r["set"] for r in kept),
        "by_theme": collections.Counter((r["set"], r["theme"]) for r in kept),
        "texts": sum(1 for r in kept if r["local_text"]),
        "tdm_only": sum(1 for r in kept if r["fulltext"] == "tdm"),
        "none": sum(1 for r in kept if r["fulltext"] == "none"),
        "in_project": sum(1 for r in kept if r["in_project"] == "yes"),
        "project_dois": len(pdois), "project_files": npaths,
        "new": sum(1 for r in kept if r["in_project"] == "no"),
    }
    write_readme(os.path.join(a.out, "README.md"), a, stats, cands, works, kept, dropped, pdois)
    print(stats)
    import json
    with open(os.path.join(work, "stats.json"), "w") as fh:
        json.dump({k: (dict(v) if isinstance(v, collections.Counter) and not any(isinstance(x, tuple) for x in v) else
                       ({f"{x[0]}/{x[1]}": n for x, n in v.items()} if isinstance(v, collections.Counter) else v))
                   for k, v in stats.items()}, fh, indent=1)


if __name__ == "__main__":
    main()
