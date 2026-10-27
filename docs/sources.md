# Evidence base: source register

The index of the data the project holds and the data it still needs, for the window 485–383 Ma
(with later anchors where noted). Status as of 2026-10-27 (updated as EPRP tranche-2 areas are reviewed). Update this file whenever a source is
added, extracted or ruled out.

Status values:
- **held**: in the repository, committed;
- **local**: on mac-mini only, in `data/eprp/local/`, because of its licence or size;
- **mirror**: on `deep-server` in EPRP's mirror but not extracted for this project;
- **missing**: not yet sourced;
- **ruled out**: checked and unusable, with the reason given.

Who does the work:
- **EPRP**: database and deposit work, run through the EPRP Mac-Mini session, which holds the
  mirror, licence tracking and provenance machinery;
- **project**: literature extraction and synthesis, done in this repository.

## 1. Fossil occurrences

| Source | What it gives | Status | Where | Licence | Serves | Next |
|---|---|---|---|---|---|---|
| PBDB plant occurrences, collections, references | 3,704 occurrences (2,628 core), 1,302 collections, 523 references; snapshot 2026-10-23 | held | `data/eprp/record/` | CC0 | F3, F4, cards | extract specimens, measurements, opinions and the plant taxa subset (EPRP) |
| PBDB card-taxa summary | records per card taxon, whole snapshot | held | `data/eprp/record/card_taxa_pbdb_summary.csv` | CC0 | cards | rerun when cards are added (EPRP) |
| Fossil Record 2 plant families | family ranges, Harland 1990 ages | local | `data/eprp/local/record/` | none stated | context only | none |
| Palynodata 2006 (GSC Open File 5793) | 76,351 window rows: 14,114 spore, 41,483 acritarch and 17,018 chitinozoan; 2,511 documents; literature to 2006, 2006-era ages, no coordinates | held | `data/external/spores/` | OGL-Canada | F3 spore channel and effort, F4 | compilation per `docs/spore-compilation-plan.md` (project) |
| Wellman, Steemans & Vecoli 2013 supplement | Ordovician–Silurian spore assemblages by age and region (abridged PDF) | held | `data/external/spores/wellman2013_supplement/` | CC BY 4.0 | F3 | tabulate (project); full database only on request (Barry's decision) |
| Post-2006 spore literature | about 200 papers (estimate) | **missing** | | | F3 | extraction per the plan (project) |
| Compilations behind diversity studies | Capel et al. 2021, 2022, 2023; Cascales-Miñana 2016; Xiong et al. 2013; Silvestro et al. 2015; Ball 2022 | **missing** | | | F3 (independent check on PBDB) | locate deposits or supplements (EPRP) |
| Geobiodiversity Database (GBDB) | South Chinese stratigraphy and occurrences | **missing** | | unknown | F3 and F4 (South China is weak in PBDB) | check access and licence (EPRP) |

## 2. Museum specimens

| Source | What it gives | Status | Where | Licence | Serves | Next |
|---|---|---|---|---|---|---|
| GBIF and ALA fossil records, Australia and New Guinea | specimen records including Museums Victoria | mirror | EPRP `gbif-ala-fossils` | per record | Victorian (Baragwanathia) floras | extract Silurian–Devonian plant specimens (EPRP) |
| GBIF fossil specimens, global | specimen-level records (NHM London, Smithsonian, Naturalis and others) | **missing** | | per record | cards, F3 cross-check | extract embryophytes and card taxa for the window (EPRP) |
| iDigBio | US museum fossil specimens, partly overlapping GBIF | **missing** | | per record | as above | extract and deduplicate against GBIF (EPRP) |

## 3. Names and taxonomy

| Source | What it gives | Status | Where | Serves | Next |
|---|---|---|---|---|---|
| PBDB taxa table | accepted names and opinions | mirror | PBDB snapshot | name harmonisation | extract with item 1 (EPRP) |
| International Fossil Plant Names Index; Plant Fossil Names Registry | nomenclature and synonymy of fossil plant names | **missing** | | cards | check access (EPRP) |

## 4. Characters, traits and measurements

| Source | What it gives | Status | Where | Serves | Next |
|---|---|---|---|---|---|
| Card trait matrix | 24 taxa × 13 traits, draft | held | `data/traits.csv` | F1, F2 | grows with the cards (project) |
| Morphological character matrices | Kenrick & Crane 1997; Toledo et al. 2021; Clark et al. 2023; Claisse et al. 2025; Hooper et al. 2026 (spore characters) | **missing** | | F1, ancestral states, F2 | locate on MorphoBank, Dryad or in supplements (EPRP) |
| PBDB measurements | specimen measurements, if any exist for window plants | mirror | PBDB snapshot | F2 | extract (EPRP) |

## 5. Phylogenies and timetrees

| Source | Status | Serves | Next |
|---|---|---|---|
| Morris et al. 2018; Harris et al. 2022; Hooper et al. 2026: trees, calibrations, alignments | **missing** | F3 (the timescale under test) | locate deposits (EPRP) |

## 6. Earth-system proxies and series

| Series | Status | Where | Licence | Notes |
|---|---|---|---|---|
| PhanDA GMST and CO2 by stage | local | `data/eprp/local/context/` | none stated | model-ensemble posterior, GTS2020 slices |
| PhanSST points | local | `data/eprp/local/context/` | none stated | conodont and brachiopod δ18O |
| Song et al. 2021 SST | held | `data/eprp/context/` | CC BY 4.0 | |
| Scotese et al. 2021 GMST (derived) | held | `data/eprp/context/` | CC BY 4.0 | derived by the extraction, not published values |
| Carbon-cycle events (Rothman 2017) | held | `data/eprp/context/` | CC BY-NC 4.0 | three events in the window |
| CO2 proxies: Foster et al. 2017; Dahl et al. 2022; Witkowski et al. 2018 | **missing** | | | locate (EPRP) |
| O2: COPSE (Lenton et al. 2016), GEOCARBSULFOR (Krause et al. 2018), charcoal (Glasspool & Scott 2010) | **missing** | | | locate (EPRP) |
| δ13C carbonate, seawater Sr, eustatic sea level (Haq & Schutter 2008) | **missing** | | | locate (EPRP) |
| Weathering and land-plant proxies: Yuan et al. 2023 (Hg), Avila et al. 2025 (Sr, δ18O), Cai et al. 2026 (C/P), Wu et al. 2026 (Li) | **missing** | | | supplements (EPRP) |

## 7. Palaeogeography and climate fields

| Source | Status | Where | Notes |
|---|---|---|---|
| PALEOMAP PaleoDEMs, 21 slices 385–485 Ma | local | `data/eprp/local/context/paleodem/` | CC BY 4.0; rasters |
| Plate-model index (27 models) | held | `data/eprp/context/plate_models.csv` | no reliable full-plate model before 410 Ma |
| HadCM3 SST (Balembois et al. 2025); cGENIE fields 400–480 Ma | local | `data/eprp/local/context/deposits/` | SST and coarse land climate |
| FOAM Late Ordovician (440 Ma) | mirror | EPRP register deposits | the only Palaeozoic land-surface field held |
| HadCM3L land climate, suite `scotese_02` (PhanDA priors; Valdes et al. 2021 runs): `tas` and `pr`, 21 slices | held (tables); local (fields) | `data/external/climate/`; fields in `data/external/local/climate/` | CC BY 4.0; model priors, not reconstructions; seven further suites available (5.8 GB) if an ensemble is needed |

## 8. Rock record and sampling proxies

| Source | Status | Where | Notes |
|---|---|---|---|
| Macrostrat units in the window | held | `data/eprp/record/` | North American and 88% marine: not a proxy for the main plant regions |
| British rock record (BGS Lexicon of Named Rock Units; DiGMapGB outcrop) | **missing** | | Avalonian core of the Silurian plant record; approach as in Dunhill et al. 2014 (EPRP) |
| Australian Stratigraphic Units Database | mirror | EPRP `asud` | extract Victorian Silurian–Devonian units for the Baragwanathia floras (EPRP) |
| PBDB collection counts by region and stage | held (derivable) | `data/eprp/record/` | a sampling proxy that is available now |

## 9. Literature

| Source | Status | Where | Notes |
|---|---|---|---|
| EPRP library extract | held; 97 open texts local | `data/eprp/library/` | strong on methods, thin on palaeobotany |
| Works cited by the cards and docs (about 400 DOIs) | held as citations | `taxa/`, `docs/` | mostly not in EPRP's library |
| Palaeobotany and palynology for the window | **missing** as a searchable corpus | | an OpenAlex harvest with open texts would support the spore compilation and the cards (EPRP, if it judges the cost worth it) |

## 10. Models and software

Pointers are in `data/eprp/pointers/software_relevant.tsv`, with EPRP's validation findings in
`data/eprp/pointers/eprp_pointers.md`. TREED's code is in `data/eprp/context/deposits/`; gen3sis,
FossilSim, paleobuddy, PyRate and cGENIE are installed or mirrored on `deep-server`.

## Requests sent to EPRP

2026-10-27, tranche 2. Items marked "(EPRP)" in §1–§8, in priority order:

1. GBIF global and iDigBio fossil specimens for the window, plus Silurian–Devonian plants from
   the Australian GBIF/ALA holdings.
2. PBDB specimens, measurements, opinions and the plant taxa subset.
3. Dispersed-spore sources: whether Palynodata or any reusable spore-occurrence compilation exists
   and can be used.
4. Deposits and supplements of the compilations, matrices, timetrees and proxies named above.
5. Sampling proxies outside North America: the BGS rock-unit data and ASUD for Victoria.
6. GBDB and the fossil plant name indexes: access and licence.
7. Land-surface climate fields across the window.
8. Optionally, a palaeobotany and palynology literature harvest.

## Project-side tasks

- A dispersed-spore occurrence compilation from the literature, if item 3 finds nothing reusable.
- Tranche-2 taxon cards (see `docs/decisions.md`).
