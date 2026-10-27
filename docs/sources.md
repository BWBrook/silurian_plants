# Evidence base: source register

The index of the data the project holds and the data it still needs, for the window 485–383 Ma,
with Frasnian–Famennian anchors where noted. Status as of 2026-10-27, after EPRP tranche 2. Update
this file whenever a source is added, extracted or ruled out.

Status values:
- **held**: in the repository, committed;
- **local**: on mac-mini only, under a `local/` folder, because of licence or size;
- **limited**: access blocked or on request;
- **missing**: not yet sourced;
- **ruled out**: checked and unusable, with the reason given.

Provenance: `data/eprp/` holds material from Barry's EPRP mirror; `data/external/` holds material
acquired from outside EPRP. Both came from the EPRP Mac-Mini session. Each area README gives
filters, licences and caveats; read it before use. Raw pulls are on `deep-server` under
`/data/codex/silurian_plants/raw/` (4.9 GB). The `local/` folders hold 2.5 GB on mac-mini.

## 1. Fossil occurrences

| Source | What it gives | Status | Where | Licence |
|---|---|---|---|---|
| PBDB plant occurrences, collections, references | 3,704 occurrences (2,628 core), 1,302 collections; snapshot 2026-10-23 | held | `data/eprp/record/` | CC0 |
| PBDB anchors, Frasnian–Famennian | 163 occurrences (*Archaeopteris*, *Callixylon*, *Eospermatopteris*, *Elkinsia*) | held | `data/eprp/record/` | CC0 |
| PBDB taxa and opinions | window subsets (413 taxa, 653 opinions) tracked; whole plant tree local | held / local | `data/eprp/record/`, `data/eprp/local/record/` | CC0 |
| PBDB specimens and measurements | none links to a window plant occurrence: plant sizes must come from the literature | held (as a negative result) | `data/eprp/record/` | CC0 |
| Palynodata 2006 | 76,351 window rows (14,114 spore, 41,483 acritarch, 17,018 chitinozoan) from 2,511 documents; literature to 2006, 2006-era ages, no coordinates | held | `data/external/spores/` | OGL-Canada |
| Wellman, Steemans & Vecoli 2013 supplement | Ordovician–Silurian spore assemblages (abridged PDF) | held | `data/external/spores/` | CC BY 4.0; full database on request (Barry's decision) |
| Project spore dataset (MVD-A) | occurrences, vetted first appearances and stage presence from Palynodata plus Wellman 2013 | held | `data/spores/` | derived; see its README |
| Post-2006 spore literature | 182 priority papers; 33 open full texts extracted (370 assemblages, 97% of records verified in text; two texts fetched into `library/open/`); the rest closed | partly held | `data/spores/sources/mvdb_*.csv` | the remainder waits on Barry's downloads (`docs/closed-literature.csv`, priority 1) |
| GBDB (Zenodo 2020) | 410 core window plant records (131 genera, mostly China), 3,217 window sections; GTS2012 ages | held | `data/external/gbdb/` | CC BY 4.0 |
| Diversity compilations | Xiong 2013, Silvestro 2015, Capel 2025 mirrored; Capel 2021, 2022, Cascales-Miñana 2016, Ball 2022 local; Capel 2023 limited | mixed | `data/external/deposits/` | per deposit |
| Fossil Record 2 plant families | Harland 1990 ages | local | `data/eprp/local/record/` | none stated |

## 2. Museum specimens

| Source | What it gives | Status | Where | Licence |
|---|---|---|---|---|
| GBIF, iDigBio, ALA (merged) | 39,417 open-licence rows, 26,102 physical specimens, duplicates linked; full iDigBio table local | held | `data/external/specimens/` | per record; open subset tracked |

GBIF files *Prototaxites* and the nematophytes under Fungi. Most Ordovician "Plantae" are
receptaculitid green algae, and these are flagged. There are no Museums Victoria *Baragwanathia*
among GBIF fossil specimens.

## 3. Names and taxonomy

| Source | Status | Notes |
|---|---|---|
| PBDB taxa and opinions | held | see §1 |
| International Fossil Plant Names Index; Plant Fossil Names Registry | ruled out for bulk use | no export, API or licence: manual lookups only |

## 4. Characters, traits and measurements

| Source | Status | Where |
|---|---|---|
| Card trait matrix (59 taxa) | held, draft | `data/traits.csv` |
| Clark et al. 2023 (548 × 410), Claisse et al. 2025, Hooper et al. 2026 spore matrix | held | `data/external/deposits/` |
| Kenrick & Crane 1997 matrix | ruled out | print only |
| Toledo et al. 2021 | limited | Wiley blocks the supplement |

## 5. Phylogenies and timetrees

| Source | Status | Where |
|---|---|---|
| Hooper et al. 2026 (MCMCTree files, calibrations); Morris et al. 2018 (alignments, calibrations); Harris et al. 2022 | held | `data/external/deposits/` |

## 6. Earth-system proxies and series

| Series | Status | Where |
|---|---|---|
| PhanDA GMST and CO2; PhanSST | local | `data/eprp/local/context/` |
| Song et al. 2021 SST; Scotese 2021 GMST (derived); Rothman 2017 events | held | `data/eprp/context/` |
| CO2: Foster et al. 2017, Dahl et al. 2022, Witkowski et al. 2018 | held | `data/external/deposits/` |
| Carbon cycle: Cai et al. 2026 data and COPSE code; COPSE (Mills) | held | `data/external/deposits/` |
| COPSE (Daines); Krause et al. 2018; Glasspool & Scott 2010 | local | `data/external/local/deposits/` |
| Lenton et al. 2016 | limited | PNAS supplement blocked |
| δ13C, Sr, δ18O: Grossman & Joachimski 2022, DM-SED 2025 held; Veizer 1999, Veizer & Prokoph 2015, Prokoph 2008 local | mixed | `data/external/deposits/` |
| Seawater Sr look-up (McArthur LOWESS) | limited | on request from the authors |
| Sea level: van der Meer 2025 held; Haq & Schutter 2008 limited; Franziskakis 2025 maps link only (1.3 GB) | mixed | `data/external/deposits/` |
| Weathering and land-plant proxies: Yuan 2023, Avila 2025, Wu 2026 | held | `data/external/deposits/` |

## 7. Palaeogeography and climate fields

| Source | Status | Where |
|---|---|---|
| PALEOMAP PaleoDEMs, 21 slices | local | `data/eprp/local/context/paleodem/` |
| Plate-model index (27 models) | held | `data/eprp/context/plate_models.csv` |
| HadCM3 SST (Balembois et al. 2025); cGENIE 400–480 Ma | local | `data/eprp/local/context/deposits/` |
| HadCM3L land climate, suite `scotese_02`, `tas` and `pr`, 21 slices | held (tables), local (fields) | `data/external/climate/` |
| Seven further HadCM3L suites (5.8 GB) | on hold | only if an ensemble is needed |

## 8. Rock record and sampling proxies

| Source | Status | Where | Notes |
|---|---|---|---|
| Macrostrat units | held | `data/eprp/record/` | North American, 88% marine |
| BGS DiGMapGB-625 | held | `data/external/rock-record/` | 2,634 Silurian–Devonian polygons, 48,575 km²; 2008 BGS age scale; no marine/terrestrial split |
| BGS Lexicon prose | local | `data/external/local/rock-record/` | no licence stated |
| ASUD | held | `data/eprp/record/` | 3,753 Australian Silurian–Devonian units, CC BY 4.0 |
| Palynological sampling effort | held | `data/external/spores/`, GAD in `data/external/deposits/` | documents reporting marine palynomorphs without spores |

## 9. Literature

| Source | Status | Notes |
|---|---|---|
| EPRP library extract (426 works; 97 open texts local) | held | strong on methods, thin on palaeobotany |
| Palaeobotany and palynology harvest, plus the project's cited DOIs (EPRP item 8) | phase 1 held; phase 2 (open texts) running | `data/external/library/`; closed works in `docs/closed-literature.csv` |

## 10. Models and software

Pointers: `data/eprp/pointers/`. TREED code: `data/eprp/context/deposits/`. COPSE variants and the
GAD code: `data/external/deposits/`. gen3sis, FossilSim, paleobuddy, PyRate and cGENIE are on
`deep-server`. SCI-FI (SCION with FLORA; Gurung et al. 2024) runs headless in MATLAB on mac-mini (smoke test 2026-10-27; outputs in `deep-server:/data/codex/silurian_plants/runs/scifi-smoke-2026-10-27/`). The Codex CLI (0.164) runs non-interactively here with schema-constrained output,
which makes it a candidate for bulk extraction (2026-10-27 smoke test).

## Open items for Barry

1. Whether to ask Wellman, Steemans and Vecoli for their full assemblage database (an external
   contact).
2. Five Elsevier supplements (Capel 2021, 2022; Cascales-Miñana 2016; Prokoph 2008; Veizer &
   Prokoph 2015) were fetched from Elsevier's public supplement server with file names inferred
   from the article ID, because the article pages block automated requests. They are held
   locally only. Keep them, or delete them and re-download through a browser.
3. Supplements behind Wiley, Science and PNAS walls (Toledo 2021, Capel 2023, Haq & Schutter 2008,
   Lenton 2016): a browser or library download would resolve these.
4. The go-ahead for EPRP item 8 and for the spore compilation (possibly on Codex).
