# gbdb/: Geobiodiversity Database (GBDB) window plant records and sampling effort

Extracted 2026-10-27 by a Claude Sonnet 5.5 subagent (`claude-sonnet-5-5`) from the Zenodo snapshot of the
GBDB (Xu 2020), read-only on the source. The window is **485–383 Ma** (Tremadocian to Givetian), plus
Frasnian–Famennian records of six anchor genera (*Archaeopteris*, *Callixylon*, *Eospermatopteris*,
*Wattieza*, *Elkinsia*, *Leclercqia*). Scripts: `../scripts/gbdb_*`. Extraction ran on `deep-server` (not reachable from the Macs; a rebuild re-pulls on `nectar`, §11); the
raw copy is `deep-server:/data/codex/silurian_plants/raw/gbdb/20261027T004503Z/` (zip, workbooks, CSV
conversions). All files here are under 20 MB and CC BY 4.0, so none is in `../local/gbdb/` (unused).
Treat everything as input, not verified fact.

Original columns are the source's own, unchanged (checked, `gbdb_verify.py`: every output row equals its
source row in all 43 original columns). `derived_*` columns are computed here; `j_fossils_*` are joined
from the other workbook. **No GBDB age was converted or repaired.**

## 1. Source

- **Xu, H.-H. (2020).** *Data of fossils and sections of the Geobiodiversity Database (GBDB).* Zenodo,
  version "5-Nov-2020", doi 10.5281/zenodo.4245604 (concept 10.5281/zenodo.4245603). Licence CC BY 4.0.
  One file, `GBDB fossils and sections.zip`, 174,469,214 bytes, md5 `d8ab936d…` (matches Zenodo),
  sha256 `9bbd8aa0…4021ca38`. Downloaded 2026-10-27T00:45Z with a plain user agent; a second download
  (01:38Z, `gbdb_fetch.py`) gave workbooks with identical sha256. `provenance.tsv` has the URLs,
  checksums and member hashes.
- **Versions (observed).** The versions endpoint lists only this record. The related record
  doi 10.5281/zenodo.3667645 (version "31Dec2019", `GBDB_all sections.xlsx`) is its earlier version, and
  that file has the **same md5** as the sections workbook in this zip: the sections table is the
  31 December 2019 state; only the fossils workbook (modified 2020-11-05) is newer. A later Zenodo item,
  10.5281/zenodo.21765787 (2026-08-03), holds Mesozoic–Cenozoic brachiopod, bivalve and echinoderm
  occurrences from the GBDB and is outside this task. Nothing newer for the Palaeozoic was found.
- The live site (geobiodiversity.com) was not accessed; no account was created. The snapshot is nearly
  six years old; the live database may hold later ages and records.

## 2. Files

| File | Rows | Contents |
| --- | ---: | --- |
| `gbdb_plant_fossils.csv` | 3,099 | Window plant records (core and flagged) plus the 2 anchor Frasnian–Famennian rows. One row per sections-table taxon row; 43 original columns, 22 `derived_*`, 6 `j_fossils_*` |
| `gbdb_plant_sections.csv` | 2,389 | Every stratigraphic unit (section × formation entry × unit) of the 146 sections holding those records: all 55 section, formation, age and unit columns, plus `derived_*` counts |
| `gbdb_plant_filter_names.csv` | 650 | Audit of the filter: each distinct genus name as recorded, by GBDB group, with decision, basis, counts and reason; includes excluded names from plant-adjacent groups |
| `gbdb_window_sections_all.csv` | 3,217 | Every section with at least one window-age unit: location, units, ages, references, and counts of taxon rows by major group (window units only) |
| `gbdb_card_anchor_summary.csv` | 40 | One row per card taxon (34) and anchor genus (6): records by age status, sections, China and South China counts, countries |
| `gbdb_card_anchor_names.csv` | 109 | The same by name as recorded, GBDB group, numeric age, region, formations |
| `gbdb_plant_no_age_candidates.csv` | 2,129 | Plant records with **no GBDB age** that may belong to the window (§6) |
| `gbdb_plant_fossils_table_only.csv` | 340 | Plant-classified rows of the fossils workbook with no counterpart in the sections workbook (no age available) |
| `gbdb_age_basis.csv` | 305 | For each age label (six label columns), the numeric `early_age`/`late_age` pairs GBDB attaches, with the project's ICS v2024/12 stage ages and differences |
| `gbdb_label_field_patterns.tsv` | | Which age label columns co-occur on rows with a numeric age |
| `gbdb_fields.csv` | 91 | Field dictionary of both workbooks: column, role, non-blank count, distinct count, examples |
| `gbdb_xlsx_inventory.tsv` | 5 | Workbook sheets, rows and widths |
| `gbdb_pbdb_overlap_references.csv`, `_sections.csv`, `_records.csv`, `_pbdb_collections_china.csv`, `_pbdb_occurrences_china_core.csv`, `_summary.json` | | PBDB overlap tables (§8) |
| `gbdb_extract_stats.json` | | Counts printed by the extraction |
| `provenance.tsv` | | Source URL, licence, checksums, timestamp |
| `MANIFEST.tsv` | | Delivered files with source, licence, script, rows, sha256 |

## 3. Structure of the snapshot (observed)

Two Excel workbooks, no shared key.

**`GBDB_fossils.xlsx`, sheet `T_Fossil`** (three further sheets are empty): 422,948 rows × 19 columns,
`ID` 1–422,948 (unique), `fossil species` (name as entered, with qualifiers), `FossilGroup`, `SectionName`,
`Collection`, `Country`, `Province`, `County`, `Village`, `LongitudeDecimal`, `LatitudeDecimal`,
`Formation`, `Lithology`, `Depth` (unexplained large numbers in coal sections), reference authors, year,
title, journal, `Enterer`. It has **no section ID, no age and no taxonomy** beyond `FossilGroup`
(86 groups; 6,682 rows blank). 1,710 rows are identical apart from `ID`.

**`GBDB_all sections.xlsx`, sheet `Sheet1`**: 764,544 rows × 72 columns. It is a **denormalised join**:
one row per section × formation entry × unit × collection × taxon × reference (a unit with no
collection has one row, with blank taxon fields). Column groups: section (`sectionID`, name, country,
province, county, village, locality, decimal latitude and longitude with direction); formation
(`fromation_id` [sic], `group_`, `Formation_name`, `bed`); age (`early_interval`, `intage_min`,
`intage_max`, `epoch_max`, `epoch_min`, `period_max`, `emlperiod_max`, `early_age`, `late_age`); unit
(`unit_id`, `unit_no`, colours, lithologies A–D, thickness, `ContactBase`, `Facies`, `Environment`,
`Details`); collection (`CollectionNo`, depth bounds, precision); taxon (`FossilGroup`, `TaxonType`,
`genusname`, `speciesname`, `speciesname_suffix`); reference (`ReferenceID` and author, title, year,
journal). The header repeats `unit_lithology1A` (second copy suffixed `.1` here, following the PBDB
extract; likely lithology 2A, inferred) and `ref_Title`/`ref_title` (identical in every row).

| Count | Value |
| --- | ---: |
| sections (`sectionID`; 151 without coordinates) | 26,423 |
| formation entries (`fromation_id`; per section, not global) | 57,879 |
| units (`unit_id`) | 238,122 |
| (section, collection) pairs | 122,118 |
| references (`ReferenceID`) | 5,340 |
| country labels (China 71% of rows; 16,994 rows "PleaseSelect") | 85 |
| taxon rows (`genusname` filled) | 573,982 (569,860 after dropping exact duplicate rows) |
| exact duplicate rows, all 72 columns | 8,907 |
| distinct genus names as recorded | 21,125 |

**Keys.** Within the sections workbook: `sectionID` → `fromation_id` → `unit_id` → (`CollectionNo`, taxon),
with `ReferenceID` on each row. Age fields are constant within a formation entry (checked for all 57,879) and unit fields within a
(section, formation entry, unit) (checked for the 2,389 units of the plant sections). `SectionName` is not
unique (19,779 names; 3,392 have more than one `sectionID`) and `CollectionNo` is free text, unique only
within a section. **Between workbooks** the only link is by
name: (`SectionName`, `Collection`, `Formation`, `FossilGroup`) matches 419,915 of 422,948 fossils rows
(99.3%) to a sections taxon row; adding the parsed genus and species epithet matches 376,157 (88.9%)
(qualifiers such as "cf." and "?" are entered differently). The sections workbook holds more taxon rows
(573,982) than the fossils workbook (422,948), so the fossils workbook is not a subset or superset. This
extract therefore takes **records from the sections workbook** (the only one with ages) and joins
fossils-workbook fields on (section name, collection, formation, genus, epithet): 1,192 fossils `ID`s
attach to retained rows (`j_fossils_ids`; 322 of 410 core rows have one, 1,112 of all 3,099).

**Coordinates.** Decimal degrees, already signed (West and South negative: 0 sections where the sign
contradicts the direction field). 151 sections have none; 22 sit at (0, 0); 4 are out of range (latitude up
to 514, longitude up to 827). The fossils workbook has 292 rows out of range. `derived_lat`/`derived_lon`
repeat the value when it is in range and not (0, 0); `derived_coord_flag` says why not. All retained plant
records have valid coordinates.

## 4. Age basis (observed unless marked)

- Ages are **numeric Ma on the formation entry**: `early_age` (older bound) and `late_age` (younger bound),
  233 distinct pairs, never inverted. The scale is not named. They come with up to seven label columns
  (stage in `early_interval`, `intage_max` or `intage_min`; series in `epoch_max` or `epoch_min`; system in
  `period_max`; early/middle/late in `emlperiod_max`), 116 `early_interval` and 75 `intage_max` values
  among them (`gbdb_label_field_patterns.tsv`).
- **Only 305,119 rows (39.9%) carry any age; 43% of taxon rows (247,655).** Where a row has one label
  column filled, the pair is that stage's bounds.
- **The stage values are GTS2012-era (ICS v2013/01) values, not ICS v2024/12** (`gbdb_age_basis.csv`):
  the modal GBDB base age equals the ICS v2013/01 base recorded in
  `../../eprp/record/intervals_window.csv` for all 18 stages that table covers (Tremadocian 485.4 to
  Eifelian 393.3). For the project's stages the modal GBDB pair minus the project's base: Tremadocian −1.45 Myr, Floian
  +0.6, Dapingian −1.3, Darriwilian −2.1, Sandbian +0.2, Katian +0.2, Hirnantian 0, Rhuddanian +0.3,
  Telychian −0.1, Sheinwoodian +0.5, Pridoli +0.3, Lochkovian −0.42, **Pragian −2.22, Emsian −3.02**,
  Eifelian −0.17, Givetian −0.25, Frasnian +0.39, Famennian +0.05. The Pragian, Emsian and Darriwilian
  gaps match the PBDB re-dating note in `../../eprp/record/README.md` §4. Examples: Pragian 410.8–407.6,
  Emsian 407.6–393.3, Lochkovian 419.2–410.8, Pridoli 423–419.2, Givetian 387.7–382.7, Famennian
  372.2–358.9.
- The **Ordovician series are the British ones** on an older chart, each with variants: Arenig 478.6–466
  and 478.6–468.1, Llanvirn 466–460.9, Caradoc 460.9–449.5 and its subdivisions, Ashgill 449.5–443.7. Some pairs are **regional intervals**
  (409.1–402.5, 402.5–391.9, 379.5–376.1, 376.1–370.6, 364.7–360.7). The number is whatever the formation
  entry carries, so a label and its numbers can differ (for example `intage_max` Emsian is paired with
  409.1–402.5, 402.5–391.9 and 407.6–393.3).
- **Window rule (PBDB's):** `early_age > 383` and `late_age < 485`, strict, on GBDB's own numbers. 115,149
  rows, 22,000 (section, formation entry, unit) units and 3,217 sections qualify. Cambrian units (`late_age` 485.4) fall just outside; the
  Tremadocian (485.4–477.7) is inside; Frasnian units (`early_age` 382.7) are outside, as with ICS v2024/12
  (382.31). Anchor extension: `early_age > 358.86` and `late_age < 383`, anchor genera only. Mixing these
  ages with PBDB's or the project's needs the vintage difference above in mind, up to 3 Myr in the Early
  Devonian.
- `derived_span_myr`, `derived_overlap_with_window_myr` and `derived_fully_inside_window` mark wide spans
  (core rows: 347 fully inside, 63 not; 318 span ≤ 10 Myr, 92 span 10–50, none wider).

## 5. Plant filter

GBDB has no taxonomy tree, so `FossilGroup` and names stand in for PBDB's lineage. Subsets, subset names
and core/flagged status follow `../../eprp/record/README.md` §2 where they exist; the order applied
(`gbdb_extract.py`, `classify`):

1. **Nematophyte names** (*Prototaxites*, *Nematothallus*, *Nematoplexus*, *Nematophyton*, *Nematasketum*,
   *Pachytheca*, *Parka* and misspellings), any group: `nematophyte_name`, core.
2. **Curated fungal genera** (PBDB's ten): `fungi`, flagged. None occurs in the window.
3. **GBDB plant groups.** Embryophyte groups (Lycopodiophyta, Psilotophyta, Equisetophyta, Filicophyta,
   Bryophyta, Marchantiophyta, Anthocerotophyta, Cycadophyta, Coniferophyta, Ginkgophyta, Gnetophyta,
   Magnoliophyta): `embryophyta_gbdb_group`, core. Sporites, Pollenites: `dispersed_spore_pollen_gbdb_group`,
   core. Chlorophyta: `green_algae`; Charophyta: `streptophyta_not_embryophyta`; Rhodophyta: `red_algae`;
   Phaeophyta: `algae_unspecified`; Acritarchs: `acritarchs_prasinophytes` (all flagged). A genus that is
   core in the PBDB window extract overrides an algal or acritarch group (for example *Taeniocrada*,
   *Dyadospora*, filed by GBDB under Acritarchs); a genus flagged differently in PBDB takes PBDB's subset
   (*Leiosphaeridia* becomes `green_algae`, as in PBDB).
4. **Any other group** (animals, `unknown`, blank, Trace fossils, Chitinozoa, Dinoflagellata,
   Cyanophyta/Stromatolites): a genus in the PBDB window plant genus list takes PBDB's subset
   (`plant_pbdb_genus_lookup`; 414 genera from `pbdb_plant_occurrences.csv`); a blank or `unknown` group
   inherits the plant group the genus has in ≥ 80% of its labelled rows elsewhere in GBDB
   (`inferred_group_from_genus:…`); then PBDB's curated plant, algal and spore-form rules (spore-form
   endings, `name_spore_form_genus`). The curated plant list adds the project's card genera and nine
   names from a review of excluded blank-group window names (*Cycas*, *Bennettites*, *Artemisia*, …).
5. Excluded, as in PBDB: Chitinozoa, Dinoflagellata, Cyanophyta/Stromatolites (calcimicrobes such as
   *Girvanella*, *Ortonella*), Trace fossils (*Chondrites*, *Buthotrephis*), Foraminifera, all animals.

`derived_major_group` uses PBDB's labels (without the `pbdb_` prefix): the PBDB genus's major group where
the genus is in the PBDB extract, else the GBDB group (`seed_plants` = Cycadophyta, Coniferophyta,
Ginkgophyta, Gnetophyta, Magnoliophyta). `derived_record_type` is `dispersed_spore`, `dispersed_pollen`,
`plant_organ_or_megafossil` or `unspecified`. `derived_group_conflict` = yes where the GBDB group disagrees
with the name-based result (260 rows, 29 of them core).

**Doubt flags** (`derived_flag`; informative only, nothing is dropped or repaired). 131 of the 410 core
rows carry one:
- `seed_plant_or_pollen_group_label_but_GBDB_age_entirely_older_than_Famennian`: a seed-plant or pollen
  group label (angiosperms, conifers, cycads, ginkgos) on a unit GBDB dates before the Famennian, for a
  genus absent from the PBDB window extract.
- `formation_entry_also_holds_seed_plant_or_pollen_labelled_records_dated_older_than_Famennian`: same
  formation entry as such a record.
- `genus_mostly_dated_younger_than_window_elsewhere_in_GBDB`: ≥ 80% of the genus's aged GBDB rows (≥ 5)
  are younger than the window (not applied to dispersed spores, whose long-ranging genera would trip it).
- `genus_mostly_recorded_under_a_non_plant_GBDB_group`: ≥ 80% of ≥ 3 labelled rows sit in an animal group
  (for example *Crotalocephalus*, a trilobite genus, under Lycopodiophyta).
Not caught by any flag: 10 rows from Dongdacun (Xizang, formation entry "Zhongyan", dated 478.6–466 Ma)
that are Carboniferous-type spores (*Lycospora*, *Crassispora*, …); inspection, not a rule, marks them as
mis-aged.

## 6. Results

**Window plant records: 3,099 rows (3,087 after dropping 12 exact duplicates), 146 sections**,
by `derived_subset`:

| Subset | Rows |
| --- | ---: |
| core: `embryophyta_gbdb_group` | 182 |
| core: `dispersed_spore_pollen_gbdb_group` | 168 |
| core: `plant_pbdb_genus_lookup` | 39 (2 are *Callixylon*, anchor Famennian) |
| core: `plant_unlinked_name` | 17 |
| core: `nematophyte_name` (*Prototaxites* 3, *Pachytheca* 1) | 4 |
| **core total** | **410** (131 genera; 64 sections; no exact duplicates) |
| flagged: `acritarchs_prasinophytes` | 2,379 |
| flagged: `green_algae` | 228 |
| flagged: `streptophyta_not_embryophyta` (charophytes) | 58 |
| flagged: `red_algae` (*Protosphaeridium*, *Solenopora*, *Tetradium*) | 20 |
| flagged: `algae_unspecified` | 4 |
| flagged: `fungi` | 0 |

Core rows by `derived_major_group`: dispersed spores 181, lycophytes including zosterophylls 68, seed
plants 51, ferns and sphenophytes 49, other or indeterminate Plantae 27, psilophytes 18, progymnosperms 9,
nematophytes 4, other tracheophytes 3.
**279 core rows carry no doubt flag** (36 sections, 65 genera): 169 dispersed spores; 67 lycophytes
including zosterophylls (*Zosterophyllum* 29, *Protolepidodendron* 10, *Lepidodendropsis* 10, *Knorria* 9);
18 psilophytes in PBDB's sense (*Taeniocrada* 7, *Dawsonites* 3, *Drepanophycus* 2, *Psilophytites* 2,
*Cooksonia* 1, *Hostinella* 1); 9 progymnosperms (*Barrandeina* 5, *Protopteridium* 4); and 16 others
(*Salopella* 4, *Sciadophyton* 3, *Callixylon* 2, which PBDB files under seed plants, *Psilophylites* 2).
(*Prototaxites* is flagged only because GBDB files it under Cyanophyta.) By GBDB age: 68 Wenlock spores
(Fentou Fm, Jiangsu, 433.4–427.4), 40 Pridoli (423–419.2; Xinjiang 20, Yunnan 13, Gansu 6, Sichuan 1),
31 Lochkovian, 26 Pragian (Posongchong Fm, 410.8–407.6), 31 Emsian–Eifelian (Danlin Fm, 409.1–391.9, and
407.6–393.3), 58 Givetian (Haikou Fm and others, 387.7–382.7), 7 Telychian, 5 Hirnantian, 1 Katian,
2 Famennian, and the 10 anomalous rows (below).

**Window sections.** 3,217 of 26,423 sections have a window-age unit (22,000 units; 14,849 further units of
these sections have no age). 2,959 are in China. 1,126 of them (35%) have no taxon row in a window
unit. Counts of taxon rows in window units: graptolites 34,851, conodonts 20,229, brachiopods 14,275,
trilobites 12,779, molluscs 6,997, corals, sponges and stromatoporoids 4,905, plants (core) 408, plants
(flagged) 2,677, chitinozoans and dinoflagellates 2,614, other invertebrates 1,216, unlabelled 737,
vertebrates 264, other microfossils 251, trace fossils 105, cyanobacteria 61. Only 145 sections hold any
plant record (63 core). `gbdb_window_sections_all.csv` gives these per section, with the formation names,
age labels, reference IDs and collection counts.

**Records with no age (the main limit).** Of 68,235 core plant rows in the whole table, **74% (50,694) have
no GBDB age**, 25% are dated outside the window and 0.6% (410) fall inside it; of the 17,864 flagged rows,
67% have no age. Age-less formation entries cannot be placed from GBDB alone, and several are not Early
Palaeozoic (the *Drepanophycus spinaeformis* rows at Huazi, Liaoning, are from a paper on the Early
Carboniferous flora, 1994). `gbdb_plant_no_age_candidates.csv` lists the core rows (and fungi) without
an age that **may** belong to the window, by two inferences: the genus is a card, anchor or nematophyte
genus (234 rows), or the reference title names the Ordovician, Silurian or Devonian in English or Chinese
(`derived_ref_period_hints`; 1,967 rows; 72 meet both). By region: South China provinces 1,041, other
China 366, UK 636, unassigned country 85. It is a triage list, not window membership: 181 sections,
1,457 dispersed-spore rows. Ages of the same formation name elsewhere in GBDB were not used.

## 7. Card taxa and anchors

34 cards (`taxa/*.md` as of 2026-10-27, ten of them not yet in `taxa/README.md`) and 6 anchor genera,
matched on the genus token of `genusname`, with the cards' alternative names reported separately (full
table: `gbdb_card_anchor_summary.csv`, names as recorded: `gbdb_card_anchor_names.csv`). **Records are
sections-table taxon rows without exact duplicates.**

| Target | All ages | Window | Anchor FF | No age | Sections | China (South China) | GBDB ages |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| *Zosterophyllum* | 87 | 29 | | 56 | 36 | 87 (82) | 423–419.2, 410.8–407.6, 409.1–391.9; 2 rows 125–113 |
| *Drepanophycus* (*D. spinaeformis* 40) | 55 | 2 | | 53 | 25 | 55 (48) | 409.1–391.9 |
| *Psilophyton* | 25 | 0 | | 25 | 13 | 25 (23) | none aged |
| *Ambitisporites* (+1 typo) | 41 | 7 | | 34 | 19 | 17 (8); 24 UK | 423–419.2, 419.2–410.8 |
| Ordovician cryptospore genera | 21 | 4 | | 17 | 5 | 20 (14) | 445.2–433.4 |
| *Dawsonites* | 8 | 3 | | 5 | 6 | 8 (8) | 410.8–407.6, 387.7–382.7 |
| *Salopella* | 4 | 4 | | 0 | 4 | 4 (0) | 423–419.2 |
| *Prototaxites* | 4 | 3 | | 1 | 2 | 3 (0); 1 UK | 460.9–449.5 (Lianglitag Fm, Xinjiang; group Cyanophyta) |
| *Cooksonia* | 3 | 1 | | 2 | 3 | 3 (3) | 387.7–382.7 |
| *Rhynia* (2 under group Acritarchs) | 2 | 0 | | 2 | 1 | 2 (2) | none aged |
| *Asteroxylon* | 1 | 0 | | 1 | 1 | 1 (1) | none aged |
| *Archaeopteris* (anchor) | 20 | 0 | 0 | 20 | 12 | 20 (18) | none aged (filed under Cycadophyta) |
| *Callixylon* (anchor) | 2 | | 2 | 0 | 1 | 2 (0) | 372.2–358.9 (Hongguleleng Fm, Xinjiang) |

**Absent from the snapshot** (no genus match, typos checked): *Aberlemnia*, *Aglaophyton*,
*Baragwanathia* (both cards), *Eophyllophyton*, *Franhueberia*, *Hedeia*, *Horneophyton*, *Metzgeriothallus*,
*Nematothallus*, *Nothia*, *Partitatheca* and the other eophyte genera, *Pertica*, *Pluricaulis*, *Renalia*,
the Rhynie gametophyte genera, *Riccardiothallus*, *Sawdonia*, *Tortotubus*, *Winfrenatia*, *Yarravia*, the
glomeromycotan genera, and the anchors *Eospermatopteris*, *Wattieza*, *Elkinsia* and *Leclercqia*. So
**11 of 34 cards and 2 of 6 anchors occur at all; only *Zosterophyllum* (29), *Ambitisporites* (7),
*Salopella* (4), the cryptospore genera (4), *Dawsonites* (3), *Prototaxites* (3), *Drepanophycus* (2) and
*Cooksonia* (1) have dated window records, and *Eophyllophyton*, a Posongchong plant, is not in the
snapshot** (observed; that the snapshot is built from regional stratigraphic lists rather than the
palaeobotanical literature is an inference).

**South China.** "South China" is province-based and approximate (inference): Yunnan, Guizhou, Sichuan,
Chongqing, Hubei, Hunan, Jiangxi, Zhejiang, Anhui, Jiangsu, Shanghai, Fujian, Guangdong, Guangxi, Hainan
(`derived_region`); western Yunnan and western Sichuan are not South China block. Observed: **409 of 410
core window records are in China**, 245 (60%) in the South China provinces; of the 279 unflagged, 232
(83%); of the 3,217 window sections, 2,959 are in China and 1,989 (62%) in the South China provinces; the
core records in China outside South China (164) are mostly doubt-flagged Qinghai, Gansu and Xizang entries
(117 of 164). Carded genera: 82 of 87 *Zosterophyllum* and 48 of 55 *Drepanophycus* records are South
China. Outside China, the 3,099 rows include Russia 435 (Ordovician acritarchs and algae), Iran 190,
Canada 19, Jordan 15, UK 11 and Estonia 1.

## 8. Overlap with PBDB (`gbdb_pbdb_overlap_*`; nothing deleted or merged)

Method (`gbdb_pbdb_overlap.py`): references matched by first-author surname, year and title word overlap;
sections matched to PBDB plant collections by distance (haversine) and formation-name tokens; core GBDB
records labelled A (same reference and genus), B (same formation name and genus, China, any distance), C
(genus within 25 km), D (25–100 km). PBDB data: `pbdb_plant_occurrences.csv`, `_collections.csv`,
`_references.csv`.

- **References (observed).** 88 GBDB references cite the window plant records (44 the core ones); 31 of the
  88 have a first author in Chinese characters and cannot be compared with PBDB's Latin names (17 of the
  core 44). One matches by author, year and title (Cai, Dou & Edwards 1993, *Geological Magazine*, PBDB
  reference 4053), and another coincides on surname and year only. The large share of GBDB records cite
  regional compilations ("Stratigraphic Tables of Qinghai", "Regional Geology of Xizang") that PBDB does not.
- **Same reference, different records.** Cai et al. 1993 is cited by 7 GBDB window records at Wutubulak
  (*Psilophytites*, *Ambitisporites*, *Salopella*, *Hostinella*, algae) and by PBDB collections whose core
  occurrences are *Zosterophyllum*, *Eocooksonia* and others: no genus is shared. PBDB places its
  Wutubulake collection 217 km from GBDB's section (PBDB coordinates are estimated from maps), so
  distance alone misses this pair.
- **Sections.** Of the 146 GBDB plant sections: 1 shares a PBDB reference; 20 have a PBDB plant collection
  within 50 km whose formation name overlaps (11 with a shared core genus); 12 more lie within 10 km of
  one; 18 within 50 km; **95 (65%) have no PBDB plant collection within 50 km**.
- **Records (estimate).** Of 410 core window records, **45 (11%) have any PBDB counterpart** (B 41, C 3,
  D 1, A none) and 365 do not; of the 279 unflagged, 36 (13%) do. 41 of 45 rest on genus plus formation
  name, not on a shared reference or collection, so true duplicates are probably fewer (inference). They
  are *Zosterophyllum* (Posongchong, Wutubulake), *Lepidodendropsis* (Haikou) and *Hunanodendrum*. The
  flagged algae and acritarch rows were not compared.
- **From the PBDB side.** PBDB's China core occurrences number 68 in 52 collections (67 carry a genus name): 7 have a
  window-aged GBDB counterpart and 3 an age-less one (15% together); 57 do not. 46 of the 52 collections have a GBDB
  window section within 50 km, 31 with a matching formation name, 26 with a GBDB plant section.
- **Genera.** GBDB's 131 core window genera include 49 of PBDB's 317; in China 11 of PBDB's 40 core
  genera are in GBDB's window plants.
- **Reading.** The two databases are largely independent for China. GBDB adds 410 core window rows
  (279 unflagged) against PBDB's 68 for China, mostly Silurian–Devonian spores and zosterophylls in
  South China, but with weaker ages and identifications. Do not de-duplicate wholesale; use the tables for
  candidate pairs. Records with non-Latin references and pairs more than 50 km apart under different
  names are under-counted (inference).

## 9. Read before use

- **Dating is the weak point.** Ages are per formation entry, GTS2012-era, missing for most rows, and in
  places implausible: floras (*Neocalamites*, *Danaeopsis*, *Podozamites*, *Betula*,
  *Quercus*: genera that GBDB dates after the Devonian in most of its other rows, or that carry
  angiosperm, conifer, cycad or ginkgo labels) sit under Ordovician and Silurian formation entries
  ("Zhongyan", "Xiayan" in Qinghai and Gansu; "Bulong" in Xizang) that cite regional geology compilations. Filter on `derived_flag` blank
  first. The cause is unknown; name collisions between formations are one possibility (inference).
- **Rows are list entries, not specimens.** A row is a taxon listed for a collection in a unit in a
  reference; regional compilations list a formation's fossils without a collection. 12 of the 3,099 rows
  repeat another row exactly (`derived_exact_duplicate_of_row`); none is a core row.
- **GBDB groups are loose.** *Archaeopteris* is filed under Cycadophyta, *Taeniocrada* and *Rhynia*
  under Acritarchs, *Prototaxites* under Cyanophyta, *Pachytheca* under Anthozoa, *Hunanodendrum* under
  Graptolithina and a trilobite genus under Lycopodiophyta. The name rules above repair the *filter*,
  not the source.
- **Unvalidated names.** No taxonomy, synonymy or opinion data are in the snapshot (the Zenodo
  description mentions them). Misspellings are common (*Retusortriletes*, *Ambitiporites*,
  *Tetrahadraletes*) and are kept as recorded; only the card and anchor tables search known variants.
- **Spore records.** Chinese records are mainly from lists attached to sections, often at genus level
  (`TaxonType` genus, 168 of the 410 core rows).
- **Chinese-language fields.** Reference titles, authors and `Details` are partly in Chinese;
  `derived_ref_period_hints` reads English and Chinese period words only.
- **South China** is a province test, not a block assignment.
- **Provinces** carry variant spellings ("Inner Mongolia", "Neimenggu"); `Country` has "PleaseSelect".

## 10. Not done

No age conversion or repair; no use of the live site; no palaeocoordinates; no formation-name age lookup
for age-less rows; no review of the 2,689 flagged rows beyond the name audit; no review of rows outside the
window; no comparison of algae and acritarchs with PBDB; no reconciliation of GBDB's period labels with
the project's stages beyond `gbdb_age_basis.csv`; no row-level table of all window taxa (the effort table
has counts only); no check against the original GBDB publications.

## 11. Reproduce

```bash
cd data/external/scripts
ssh nectar python3 -I - /data/codex/silurian_plants/raw/gbdb < gbdb_fetch.py   # Zenodo API, md5 check, unzip, provenance.json
R=/data/codex/silurian_plants/raw/gbdb/<UTC stamp>          # the folder it created
ssh nectar python3 -I - $R < gbdb_xlsx2csv.py               # streams both workbooks to $R/csv/ (about 3 min)
scp ../../eprp/record/pbdb_plant_occurrences.csv ../../timescale.csv nectar:$R/aux/
ssh nectar python3 -I - $R $R/out $R/aux/pbdb_plant_occurrences.csv $R/aux/timescale.csv < gbdb_extract.py
ssh nectar python3 -I - $R $R/out < gbdb_verify.py          # independent checks, expects ALL PASS
rsync -a nectar:$R/out/ ../gbdb/                            # also copy $R/csv/xlsx_inventory.tsv as gbdb_xlsx_inventory.tsv
                                                            # (provenance.tsv was written by hand from the fields of $R/provenance.json)
                                                            # then, from the project root:
python3 data/external/scripts/gbdb_pbdb_overlap.py
cd data/external && python3 scripts/gbdb_manifest.py
```
