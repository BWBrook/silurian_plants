# Literature library: references for silurian_plants

References drawn from EPRP's literature library for a project on early land-plant evolution (Late Ordovician to Early
Devonian), screened for relevance, with a cross-check against what the project already cites. Extracted 2026-10-26 by a
Claude Sonnet 5.5 subagent (Anthropic) under Claude Opus 5.5 orchestration; the screen decisions are the subagent's
and have not been reviewed by Barry or a second agent.

Files:

- `references.tsv`: one row per kept work (426), sorted by set, theme, year.
- `screened_out.tsv`: every candidate that was dropped (7540), with a one-phrase reason, how it was decided (`manual` or `rule`)
  and whether its title was read (`screen`). Together with `references.tsv` it covers every candidate and every work added by hand (`found_by` starts `manual`).
- `MANIFEST.tsv`: delivered files with hashes. Scripts are in `../scripts/library_*`; open full texts (97) are in
  `../local/library/text/` (gitignored). `../local/library/work/` (gitignored) holds `candidates.tsv` and `fts_hits.tsv`, the
  evidence behind every candidate, plus the run's counts.

## Source and store state

- EPRP checkout `/Users/bwbrook/git/eprp` at commit `ac42dfb` (read-only). Its `resources/library/works.tsv` holds 28,850 works.
- Store: `deep-server:/data/paleodata/library/` as of 2026-10-25 (the index files are dated 25 October 2026; `search.sqlite`
  built 2026-10-25 20:11). 29,372 OpenAlex records, 2,989 open text files, `tdm/` copies not read. Full-text status in `works.tsv`:
  not_tried 12428, no_copy 9728, ok 2972, failed 1679, skipped_type 1246, tdm_ok 781, no_text 15, withdrawn 1.
- Nothing was written to EPRP or to `/data/paleodata`. Remote scratch was `/data/codex/silurian_plants-eprp/library/`.

## Routes and queries

Candidates came from several routes, recorded per work in the `found_by` column of both tables (routes first, then up to six
search queries with the part that matched: `abstract` is title plus OpenAlex abstract, `fulltext` an open text, `tdm` a
publisher copy that matched but was never read):

| Route | What it does | Candidates |
| --- | --- | ---: |
| abstract | title, OpenAlex abstract, keywords or concepts match plant-specific terms (taxa, groups, spore terms, origin terms, traits, fungi and animals) or an Ordovician–Devonian term with plant or earth-system context | 2604 |
| title | the title alone matches those patterns | 472 |
| fts | any of the 369 `library.py search` queries in `library_queries.py` matched (taxa, spores, origins, traits, fungi and animals, earth system, diversity, methods) | 5317 |
| topic | EPRP canon topic id or OpenAlex topic relevant to the project (never a candidate on its own) | 1727 |
| author | an author on a watch list (Edwards, Wellman, Kenrick, Crane, Gensel, Strother, Berner, Lenton, Boyce, Marshall, Alroy, Silvestro and others) with plant, interval or earth-system context | 773 |
| venue | a palaeobotany or botany venue with plant, interval or earth-system context | 67 |
| text | the open full text mentions at least three distinct early-plant terms, twelve times or more | 43 |
| methods-text | title or canon topic matches the F3 methods vocabulary (ranges, birth–death, dating, preservation, record quality) | 1090 |
| question | EPRP question tag for range estimation, fossil-record quality, rates or dating (Q-005, Q-006, Q-017, Q-019, Q-041, Q-042, B-007) | 96 |

A work can arrive by several routes. Seventeen queries with OR were first written without parentheses (FTS5 gives OR lower
precedence than AND); they were parenthesised before the final run. Porter stemming still turns `terrestrialization` into
`terrestri*`, so full-text-only hits are noisy and the screen absorbs them. A final sweep of all 28,850 works for methods terms in
titles and abstracts (Brownian bridge, FBD, PyRate, DeepDive, tip-dating, calibration, sighting records and similar) found eight
further works, added by hand.

## Screen

- 7959 candidates in all. Titles were read for 3714 of the dropped candidates and all kept ones; the remainder were dropped by rule
  from title and evidence flags and are marked `rule only` in `screened_out.tsv`. About 120 borderline works also had their
  abstracts read. The rule-assigned reasons (`decided_by` = `rule`) describe why a title-level screen drops such a work; they
  are not a reading of its abstract.
- Kept: real relevance to early land plants and their world (taxa, spores, origins, anatomy, fungi, arthropods, floras,
  provinces, weathering, CO2, O2, soils, rivers, fire, Devonian anoxia), or, for the `methods` set, the works a modeller of
  framing F3 would use: range-end and origination estimators, FBD and PyRate-type models, tip-dating and calibration, rock-record
  and completeness bias, plant taphonomy. `CORE:` in `screen_note` marks the first reads in the methods set and the key
  plant-record works (51).
- Dropped: Quaternary and Cenozoic palynology, Carboniferous or later palaeobotany, modern plant ecology and genomics,
  marine invertebrate and vertebrate palaeontology that only matched a keyword (for example `Sphenothallus`, which is a marine
  tube-dwelling animal), journal covers and peer-review stubs, and general quantitative palaeobiology that is not needed for F3.
- Beyond-window works are kept when they bear on plant evolution (Middle and Late Devonian plants, Late Devonian anoxia, seed
  and heterospory origins) and say so in `screen_note`. Carboniferous and later work is kept only if it is a general model,
  diversity compilation, clock method or record-bias study.
- Works the project already cites that EPRP holds were kept even when marginal (Palaeozoic temperature and sea-level records,
  Late Ordovician extinction reviews), and say so.
- `theme` is the subagent's inference. Decisions are in `../scripts/library_decisions.tsv` (keeps and the 156 manual drops).

## Counts

| | |
| --- | ---: |
| Candidates | 7959 |
| Kept | 426 |
| Kept, `plants` set | 281 |
| Kept, `methods` set | 145 |
| Dropped | 7540 (156 manual, 7384 by rule) |
| Kept with an open full text copied to `local/library/text/` | 97 |
| Kept with an open scan that has no usable text layer (not copied; OCR needed) | 5 |
| Kept with a publisher TDM copy only (not copied) | 19 |
| Kept with no full text in EPRP | 305 |
| Kept and already in the project (DOI, or title) | 59 |
| Kept and new to the project | 367 (plants 226, methods 141) |
| DOIs found in the project's `docs/` and `taxa/` | 393 |

By theme (`set / theme`):

| Set | Theme | Works | What it holds |
| --- | --- | ---: | --- |
| plants | `early-vascular` | 22 | Rhyniophytoids, polysporangiophytes and Silurian–Devonian floras and sites (Cooksonia, Pinnatiramosus, Trout Valley, Campbellton) |
| plants | `spores` | 13 | Cryptospores, trilete spores and Ordovician–Devonian palynology |
| plants | `origins` | 14 | Embryophyte origins, terrestrialisation, streptophyte algae and reviews of early land plants |
| plants | `rhynie-chert` | 6 | Rhynie and Windyfield chert plants and their preservation |
| plants | `nematophytes` | 9 | Prototaxites, Nematothallus, banded tubes, Spongiophyton and Protosalvinia |
| plants | `lycophytes` | 5 | Zosterophylls, Baragwanathia-type lycopsids and Devonian arborescent lycopsids |
| plants | `euphyllophytes` | 2 | Trimerophytes, cladoxylopsids and early euphyllophytes with secondary growth |
| plants | `bryophytes` | 3 | Bryophyte and liverwort fossils and fossil-calibrated bryophyte dating |
| plants | `life-cycle` | 3 | Heterospory, seed origin and plant reproductive palaeobiology |
| plants | `anatomy-physiology` | 9 | Stomata, tracheids, roots, leaves and hydraulics of early plants |
| plants | `plant-modelling` | 14 | Simulation and process models of early plants, vegetation and their feedbacks |
| plants | `fungi-lichens` | 4 | Early fungi, mycorrhiza and lichen-like organisms |
| plants | `early-terrestrial-biota` | 7 | Pre-vascular and microbial terrestrial communities, including contested Cambrian palaeosol fossils |
| plants | `arthropods-herbivory` | 33 | Early terrestrial arthropods, herbivory and plant–animal interactions |
| plants | `plant-diversity` | 27 | Diversity curves, evolutionary floras, extinction and sampling bias in the plant record |
| plants | `phytogeography` | 4 | Floral provinces and plant dispersal, Silurian–Devonian |
| plants | `weathering-co2` | 58 | Weathering, CO2, O2 and carbon-cycle models, proxies and plant effects |
| plants | `soils-rivers-fire` | 10 | Palaeosols, rivers, charcoal and early wildfire |
| plants | `devonian-anoxia` | 24 | Devonian anoxia and its proposed plant–weathering link (mostly context; no plant claim in many abstracts) |
| plants | `palaeogeography-climate` | 13 | Ordovician–Devonian palaeogeography, temperature records and the time scale |
| plants | `molecular-clock` | 1 | Molecular clocks for land plants |
| methods | `range-estimation` | 31 | Confidence intervals and Bayesian estimators for range ends, Signor–Lipps, sighting records, origination-age estimators |
| methods | `fossil-birth-death` | 30 | FBD, PyRate and DeepDive-type models; preservation-aware rate estimation; fossil-sampling simulators |
| methods | `tip-dating` | 18 | Tip-dating and total-evidence dating with FBD priors |
| methods | `molecular-dating` | 24 | Fossil calibration, maximum ages and clock-versus-fossil discrepancy |
| methods | `rock-record-bias` | 29 | Rock-record and completeness bias, stratigraphic palaeobiology, time resolution |
| methods | `plant-preservation` | 6 | Plant taphonomy and preservation bias in the plant record |
| methods | `record-comparison` | 2 | Microfossil versus macrofossil and organ-level plant records |
| methods | `diversity-sampling` | 5 | Sampling-standardised diversity and rate estimators |

Kept works whose only full text in EPRP is a publisher TDM copy (nothing was read or copied; local reading of these is for local mining only, under EPRP's TDM rules):

- Close et al. 2018: How should we estimate diversity in the fossil record? Testing richness estimators using sampling‐standardised
- Wagner & Marcot 2013: Modelling distributions of fossil sampling rates over time, space and taxa: assessment and implications for ma
- Silvestro et al. 2014: PyRate: a new program to estimate speciation and extinction rates from incomplete fossil data
- Barido‐Sottani et al. 2019: FossilSim : An r package for simulating fossil occurrence data under mechanistic models of preservation and re
- Petrucci et al. 2022: paleobuddy: An R package for flexible simulations of diversification and fossil sampling
- Cooper et al. 2025: DeepDiveR—A software for deep learning estimation of palaeodiversity from fossil occurrences
- Magallón et al. 2015: A metacalibrated time‐tree documents the early rise of flowering plant phylogenetic diversity
- Claramunt 2022: CladeDate : Calibration information generator for divergence time estimation
- Solow & Roberts 2003: A NONPARAMETRIC TEST FOR EXTINCTION BASED ON A SIGHTING RECORD
- Bapst 2012: paleotree: an R package for paleontological and phylogenetic analyses of evolution
- Bapst 2013: A stochastic rate‐calibrated method for time‐scaling phylogenies of fossil taxa
- Koch et al. 2023: Inaccurate fossil placement does not compromise tip‐dated divergence times
- Coiro 2024: Embracing uncertainty: The way forward in plant fossil phylogenetics
- Labandeira 2007: The origin of herbivory on land: Initial patterns of plant tissue consumption by arthropods
- Labandeira et al. 2013: Middle D evonian liverwort herbivory and antiherbivore defence
- Shen et al. 2024: Ancient large‐scale gene duplications and diversification in bryophytes illuminate the plant terrestrializatio
- Cascales‐Miñana & Cleal 2013: The plant fossil record reflects just two great extinction events
- Driese et al. 2021: Soils, Chemical Weathering, and Climate Change in Earth History
- Boyce et al. 2022: What we talk about when we talk about the long‐term carbon cycle

## Columns of `references.tsv`

`openalex_id`, `doi` (OpenAlex's), `year`, `first_author`, `title`, `venue`, `type`, `cited_by` (OpenAlex count at EPRP's harvest),
`oa_status`, `fulltext` (`open`: EPRP holds an open copy; `tdm`: publisher copy only; `none`), `local_text` (relative to
`data/eprp/`, empty if not copied), `set` (`plants` or `methods`), `theme`, `found_by`, `eprp_tiers`, `eprp_questions`,
`in_project` (DOI found in the project's docs and cards, or the title found there when the DOI is missing; the latter is
noted), `screen_note`.

## Limits and visible gaps

- EPRP's library is built around quantitative palaeobiology and a few core journals, so palaeobotany is thin. Only 59 of the
  project's 393 DOIs are held, and works the project's primer and framings cite most are absent: for example the Morris et al.
  2018 timescale of early land plants, Puttick et al. 2018 on land-plant interrelationships, Kenrick et al. 2012 on
  terrestrialisation, Berner 1997 and Beerling and Berner 2005 on plants and weathering, Davies and Gibling 2010 on
  Cambrian–Devonian alluvial systems, Steemans et al. 2009, Wellman et al. 2003, Rubinstein et al. 2010 and Hooper et al. 2026.
  A search of all 28,850 works by title, and by first author and year, found none of them (the library's Puttick 2018 and Davies
  2010 records are different papers).
- Palaeobotany journals are covered only where cited or citing: *Review of Palaeobotany and Palynology* 7 works, *Palynology* 2,
  *International Journal of Plant Sciences* 2, *Botanical Journal of the Linnean Society* 7, *Annals of Botany* 14, *American
  Journal of Botany* 16, *New Phytologist* 32, against *Lethaia* 2,843 and *Palaeontology* 2,041. OpenAlex lacks *Palaeontology*
  before 2000 and the Journal of Paleontology run has 4,445 works without DOIs; EPRP's own README records both.
- Only a handful of works hold early-plant taxa: `Cooksonia` has one work in the titles, `Rhynie` six, `cryptospore` two,
  `Prototaxites` none. Most Silurian–Devonian plant knowledge sits outside the library. The `methods` side is much better covered.
- The first-pass `fts` route reaches full texts and TDM indexes, but TDM texts were not read, so a TDM-only work with no
  informative title or abstract could not be screened; such works are in `screened_out.tsv` as passing mentions.
- Some OpenAlex records are duplicates or stubs: two records for Over et al. 2008/2009, two Kidwell and Flessa records, three
  Womack et al. 2020 records (one kept), Marshall's peer-review stubs and journal covers. One abstract does not match its title
  (Wang et al. 2022 on confidence intervals for the duration of a mass extinction). Duplicates kept are flagged in `screen_note`.
- `cited_by`, `oa_status` and `year` are OpenAlex values at EPRP's harvest. `eprp_questions` carries only EPRP's cited-tier tags.
- Screening was by one agent. Dropped works with `screen` = `rule only` were not individually read; a random sample of 100 of
  them (seed 7), checked afterwards against titles and abstracts, contained none that is relevant.

## DOIs

The DOIs are OpenAlex's, via EPRP, and some are SICI-form identifiers for older *Paleobiology*, *Palaios* and *Geology* works. They
must be verified against Crossref (`uv run tools/cards.py dois` in the project) before use in cards. Never cite from this table
without checking the paper.

## Reproduce

From `data/eprp/scripts/`: `bash library_run.sh` copies `works.tsv` to deep-server, runs `library_features.py` and
`library_candidates.py` there (under ten minutes with 16 workers), pulls `candidates.tsv` and `fts_hits.tsv` into
`../local/library/work/`, copies the open texts of kept works, and runs `library_assemble.py` and `library_manifest.py`.
The screen itself is `library_decisions.tsv` plus the rules in `library_assemble.py`; `library_screen_read.txt` lists the
candidates whose titles were read. A rerun against the same store state gives the same candidate set and the same tables.

## Crossref check (added at integration, 2026-10-27)

`crossref_check.tsv` checks every DOI in `references.tsv` against Crossref
(`scripts/library_crossref.py`). All 418 DOIs resolve; every one matches the OpenAlex title
(similarity at least 0.85, or containment) and year (within one year, print against online). The
8 remaining works have no DOI (1936–1993 items such as early Devonian floras and *The Fossil
Record 2*). The project's rule still applies: confirm a DOI with `tools/cards.py dois` once it
is cited in a card or doc.
