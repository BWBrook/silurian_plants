# record/: fossil-record data from EPRP

PBDB plant occurrences, collections and references, a summary for the project's 24 card taxa, counts
by interval, PBDB and Macrostrat interval definitions mapped to the project's timescale, Macrostrat
rock-record units, and Fossil Record 2 plant families. Window: anything overlapping **485–383 Ma**
(Ordovician to Middle Devonian, a margin either side of the project interval, 470–393 Ma).
Extracted 2026-10-26 by a Claude Sonnet 5.5 subagent (`claude-sonnet-5-5`) from EPRP commit `ac42dfb`,
read-only. Scripts: `../scripts/record_*.py`. Extraction ran on `deep-server`; nothing was written to
EPRP or `/data/paleodata`.

Ages are Ma on the sources' own scales. PBDB, Macrostrat and the project's `../../timescale.csv` all
use ICS v2024/12 (checked: no international interval differs by more than 0.5 Myr, see §4). FR2 uses
Harland et al. (1990) ages, which sit far from ICS v2024/12 (for example the Tremadoc base at 510 Ma against 486.85 Ma,
and the Lochkovian base at 408.4 Ma against 419.62 Ma; §6).

## 1. Files

`d_*` columns are derived by the scripts; `j_*` columns are joined from another source file; all other
columns are the source's own, unchanged (checked: every output row equals its snapshot row in all
original columns). Where a source had two columns of the same name (PBDB collections: 17 columns), the
second copy is suffixed `.1`; the copies are identical in all 278,593 rows.

| File | Rows | Contents |
| --- | ---: | --- |
| `pbdb_plant_occurrences.csv` | 3,704 | PBDB occurrences in the window that pass the plant filter (§2), 95 original columns + 10 `d_*`. Core and flagged subsets in one file, told apart by `d_subset` / `d_in_core` |
| `pbdb_plant_collections.csv` | 1,302 | The collections of those occurrences, 143 original columns + 3 `d_*` |
| `pbdb_plant_references.csv` | 523 | The references cited by those occurrences (`reference_no`) or as the primary reference of those collections, 34 original columns + 3 `d_*`. `formatted` is PBDB's formatted citation; `doi` is PBDB's, not verified against Crossref |
| `pbdb_plant_filter_names.csv` | 683 | Audit of the filter: each distinct accepted-else-identified name by subset and basis, with occurrence and collection counts |
| `card_taxa_pbdb_summary.csv` | 24 | One row per card taxon, from the whole snapshot (all ages) |
| `pbdb_plant_counts_by_interval.csv` | 1,031 | Raw counts of occurrences, collections and genera by interval, binning rule and major group (§3) |
| `intervals_window.csv` | 442 | PBDB (267) and Macrostrat (175) interval definitions overlapping the window, mapped to the project's stages and compared with them (§4) |
| `macrostrat_units_window.csv` | 5,932 | Macrostrat units overlapping the window: 43 original columns + 6 `j_*` + 6 `d_*` (§5). The file has 5,974 physical lines: 42 `notes` cells hold CRLF line breaks, kept as in the source, so count records with a CSV parser, not `wc -l` |
| `macrostrat_summary_by_stage.csv` | 456 | Unit counts and active-column area by project, project stage and marine/non-marine class (§5) |
| `inputs_sha256.tsv` | 57 | sha256 of the 51 mirror files the scripts read and 6 upstream FR2 workbooks (provenance only), checked against the mirrors' own manifests |
| `MANIFEST.tsv` | | Delivered files with source, version, licence, script, rows, sha256 |
| `../local/record/fr2_plant_families.csv` | 554 | Plant, algal and fungal families of Fossil Record 2 (§6). **Gitignored: FR2 has no stated licence** |
| `../local/record/ics2024_chart_values_window.csv` | 33 | ICS v2024/12 chart values (printed age with ±) for the window's PBDB international intervals. **Gitignored: EPRP lists the chart PDFs as licence-unclear** |

## 2. PBDB plant filter (exact)

**Window.** A row is in the window if `max_ma > 383` and `min_ma < 485` (strict; all 1,782,649 rows have
numeric ages). 227,465 occurrences, all taxa. `d_span_myr` is `max_ma − min_ma`;
`d_overlap_with_window_myr` is the overlap with 383–485; `d_fully_inside_window` is yes/no. Wide spans
are kept: 1,336 of the 3,704 rows (1,272 of 2,628 core) are not fully inside the window, a few with
spans of 100 Myr or more (for example Heidiphyllum, "Paleozoic" to Triassic, 538.8–201.4 Ma). Filter on
`d_span_myr` for analyses.

**Taxonomic filter.** Each window row is placed by the first rule that applies. Lineages come from the
snapshot's `taxa.csv`, following `parent_no` from the occurrence's `accepted_no` (an `orig_no`), or
from `identified_no` when there is no accepted name. Node ids are PBDB `orig_no` values.

| Order | Condition | `d_subset` | Core? |
| ---: | --- | --- | --- |
| 1 | lineage contains Embryophyta (250231) | `embryophyta_pbdb_tree` | yes |
| 2 | Chlorophyta (54811) | `green_algae` | flagged |
| 3 | Streptophyta (518962) or Charophyta (55110) | `streptophyta_not_embryophyta` (charophytes, *Spongiophyton*, ...) | flagged |
| 4 | Rhodophyta (54808) or Biliphyta (114015) | `red_algae` | flagged |
| 5 | Algae (167464) | `algae_unspecified` | flagged |
| 6 | Plantae (54311) and none of the above | `plantae_unplaced_pbdb_tree`: PBDB keeps these under Plantae but outside Embryophyta (*Prototaxites*, *Nematothallus*, Lycopodophyta genera, spore form genera under Plantae, "Plantae" indet.) | yes |
| 7 | Fungi (151419) | `fungi` | flagged |
| 8 | Acritarcha (141161) or Archaeplastida (212479) | `acritarchs_prasinophytes` | flagged |
| 9 | Opisthokonta, Eucarya, Protozoa, Chromista, Chromalveolata, Rhizopodea, Chitinozoa, Bacteria, Cyanobacteria or Ichnofossils | excluded | |
| 10 | no lineage ("taxon not entered", `identified_no` 0) or a lineage with none of the nodes above ("orphan", e.g. *Dibolisporites*): evidence rules below | | |

Rules for order 10, in this order: (a) genus (`primary_name`) in a short curated fungal list (including
*Winfrenatia*, *Tortotubus*, *Palaeoglomus*) → `fungi`, basis `name_curated`; (b) `plant_organ` has any
token other than `unassigned` or `marine palyn` → `plant_unlinked_organ` (core); (c) `plant_organ` is
`marine palyn` → `acritarchs_prasinophytes`; (d) genus in a curated algal list (*Paleooedogonium*,
*Paleoclosterium*, *Paleodidymoprium*, "Alga(e)") → `algae_unspecified`; (e) genus in a curated plant list
→ `plant_unlinked_name`, basis `name_curated`; (f) genus ends in `-spora`, `-sporites`, `-sporis`,
`-triletes`, `-tetras` or `-raletes`, or is on a short list of spore genera without such an ending
(*Raistrickia*, *Hispanaediscus*, *Laevolancis*, ...) → `plant_unlinked_name`, basis
`name_spore_form_genus`; (g) otherwise excluded. `plant_organ = unassigned` is not evidence: PBDB sets it
on crinoids, graptolites, arthropods and other animals. The curated lists (26 plant, 5 algal and 10 fungal
names, from a review of the window's unlinked names on 2026-10-26) are in `record_pbdb.py`; they include typo variants
(*Protaxites*, *Retustoriletes*, *Camptozonotriltes*). `d_basis` records the rule (`pbdb_tree:<node>`,
`plant_organ:<tokens>`, `name_curated`, `name_spore_form_genus`).

Result (occurrences / collections / `d_genus` values):

| `d_subset` | Occ. | Coll. | Genera |
| --- | ---: | ---: | ---: |
| `embryophyta_pbdb_tree` (core) | 1,423 | 440 | 110 |
| `plantae_unplaced_pbdb_tree` (core) | 546 | 260 | 80 |
| `plant_unlinked_organ` (core) | 313 | 126 | 95 |
| `plant_unlinked_name` (core) | 346 | 88 | 63 |
| **core total** | **2,628** | **611** | **317** |
| `green_algae` (flagged) | 376 | 322 | 37 |
| `red_algae` (flagged; mostly *Tetradium*, *Solenopora*) | 393 | 299 | 14 |
| `acritarchs_prasinophytes` (flagged) | 200 | 59 | 33 |
| `algae_unspecified` (flagged) | 76 | 76 | 6 |
| `streptophyta_not_embryophyta` (flagged) | 25 | 24 | 5 |
| `fungi` (flagged; *Palaeomyces*, "Fungi", *Winfrenatia*) | 6 | 2 | 2 |
| **flagged total** | **1,076** | | |

Excluded window rows, by reason: Opisthokonta (the animal lineage) 214,808;
unlinked with no plant evidence 6,609; orphan lineage with no plant evidence 481; Protozoa 834 (chitinozoan and radiolarian
genera, from the names); Ichnofossils 438 (including plant-like traces such as *Buthotrephis*,
*Chondrites*, *Zoophycos*); Bacteria (including Cyanobacteria) 322; Chromista 133; Chitinozoa 106; Chromalveolata
30. These are lookalike groups left out on purpose.

Limits of the filter (inference unless stated):
- Acritarchs are incomplete: only the Acritarcha and Archaeplastida lineages are flagged. PBDB places
  some acritarch genera under Chromalveolata (30 window rows, for example *Multiplicisphaeridium*) and
  Protozoa, and some are unlinked (*Camosphaeridium*, *Cymatisphaera*); none of these is in the file.
  PBDB classes *Leiosphaeridia* (15 rows), usually treated as an acritarch, under green algae.
- Plant-like names with no PBDB link, no specific `plant_organ` and no spore-form ending are missed
  unless on the curated list. The audit file lists what was included, not what was dropped.
- Groups follow PBDB's current classification, not the project cards. `d_major_group` for core rows is,
  in order: `dispersed_spores` (`d_record_type` = `dispersed_spore`: `plant_organ` has microspore or
  megaspore, or the genus is spore-form); `nematophytes_and_thalloid_problematica` (*Prototaxites*,
  *Nematothallus*, *Nematoplexus*, *Nematophyton*, *Nematasketum*, *Pachytheca*, *Parka* and misspellings);
  then by PBDB lineage or `phylum`: `pbdb_lycophytes_incl_zosterophylls`,
  `pbdb_psilophytes_incl_trimerophytes` (PBDB's Psilophytophyta: includes *Psilophyton*, *Cooksonia*,
  *Drepanophycus*, *Taeniocrada*, which the cards place elsewhere), `pbdb_progymnosperms`,
  `pbdb_ferns_cladoxylopsids_sphenophytes`, `pbdb_seed_plants`, `pbdb_bryophytes`,
  `pbdb_tracheophyta_other_or_indet`, `plantae_other_or_indet`. Flagged rows take their subset name.
  `d_record_type` is `dispersed_spore`, `plant_organ_or_megafossil` or `unspecified`.
- `d_genus` is PBDB's `genus` field, else `primary_name` if it looks like a genus (one capitalised word,
  not a higher-rank ending or a stop-list term such as "Plantae"). 587 core rows have none.
- `d_pbdb_lineage` gives the PBDB lineage used (blank for unlinked rows).

## 3. Counts by interval

`pbdb_plant_counts_by_interval.csv`: raw counts, no richness estimation. Three binning rules:
`time_major` (PBDB's own column, its default `timerule=major`: the international stage holding the
larger part of the occurrence's age range), `time_contain` (the stage that wholly contains it; "(none:
age range not within one stage)" otherwise) and `as_entered` (`early_interval`, or "early to late" when
both are given; 159 distinct labels, mostly regional). Per interval and rule there is one row per
`major_group`, plus `ALL_CORE` and `ALL_INCLUDING_FLAGGED`. `n_genera` counts distinct `d_genus`.
`interval_base_ma` and `interval_top_ma` come from PBDB scale 1 where the label is an international
interval.

**PBDB's bins put Pridoli occurrences in "Ludfordian"** (observed: 76 of the 78 rows with
`early_interval` Pridoli, 422.7–419.62 Ma, have `time_major` and `time_contain` = Ludfordian, whose own
interval is 425.0–422.7 Ma). Use `as_entered` to separate them.

Core occurrences by `time_major` stage (collections and genera in the file):

| Stage | Core occ. | Coll. | Genera | of which dispersed spores |
| --- | ---: | ---: | ---: | ---: |
| Tremadocian, Floian, Dapingian | 0 | 0 | 0 | 0 |
| Darriwilian | 4 | 4 | 3 | 0 |
| Sandbian | 11 | 10 | 5 | 0 |
| Katian | 2 | 2 | 1 | 0 |
| Hirnantian | 1 | 1 | 1 | 1 |
| Rhuddanian | 3 | 2 | 2 | 2 |
| Aeronian | 0 | 0 | 0 | 0 |
| Telychian | 2 | 2 | 1 | 0 |
| Sheinwoodian | 2 | 2 | 1 | 0 |
| Homerian | 36 | 13 | 16 | 19 |
| Gorstian | 3 | 3 | 1 | 0 |
| Ludfordian (incl. Pridoli) | 83 | 37 | 26 | 11 |
| Lochkovian | 58 | 23 | 22 | 13 |
| Pragian | 54 | 14 | 36 | 11 |
| Emsian | 592 | 128 | 105 | 107 |
| Eifelian | 238 | 35 | 42 | 187 |
| Givetian | 966 | 198 | 150 | 328 |
| Frasnian or Famennian (range reaches into the window) | 293 | | | |
| no single stage (`time_major` "-") | 280 | 118 | 79 | 24 |

The record is thin and lopsided: three Ordovician stages with no core record at all, and Givetian
records outnumber every stage before the Emsian combined. The Ordovician core rows are mostly
problematic taxa that PBDB files under Plantae (*Proaulopora*, *Phacelophyton*, *Bojophyton*,
*Bythotrephis*, *Alectorurus*, from Liu et al. 2021 and older work; identity not checked here). The
only Ordovician spore is *Tetrahedraletes* cf. *medinensis*, Hirnantian, South Africa (Gray et al. 1986).
One reference supplies a large share: Stein (2002, reference 6895, SUNY-Binghamton collection)
accounts for 598 core rows (466 are informal "Euphyllophytina" morphotypes from 95 Early to Middle
Devonian collections in the USA and Canada); Richardson (1964) 345 rows and Balme (1988) 237.

## 4. Intervals and timescale

`intervals_window.csv`: every interval whose age range overlaps the window (`top_ma < 485`, `base_ma >
383`): PBDB's table (2026-10-23 snapshot, 19 scales, `source_scale` = "pbdb scale N"; PBDB's interval table
carries no scale names) and Macrostrat's definitions (`intervals?all`, timescale mirror of 2026-10-23;
`source_scale` lists Macrostrat's timescales). The Macrostrat intervals of the 2026-10-25 units snapshot
are identical for all 175 window intervals (checked).

Mapping to the project's table (`data/timescale.csv`, sha256 `baf5a407...`; the Givetian top uses the
ICS v2024/12 Frasnian base, 382.31 Ma, which the project table lacks):
- `d_project_stage_exact`: name match. `d_base_diff_vs_project_myr` and `d_top_diff_vs_project_myr` are
  differences in age (interval minus project). For epochs and periods that are unions of project stages
  (Early Devonian, Silurian, ...) the base is compared with the oldest component stage.
  `d_flag_gt_0p5_myr_vs_project` flags a difference above 0.5 Myr; it is filled only for international
  intervals with a like-for-like comparison (62 rows).
- `d_project_stages_overlapped`, `d_project_stage_best`, `d_best_overlap_fraction_of_interval`,
  `d_contained_in_one_project_stage`, `d_base_diff_vs_best_stage_myr`: age-overlap mapping for every
  interval, including regional ones. This is not a like-for-like comparison and is not flagged: for
  example PBDB's British Tremadoc (base 486.4 Ma) lies 0.45 Myr from the Tremadocian base.
- `ics_v2013_01_gts2012_base_ma` and `ics_v2020_01_base_ma`: base ages of the same boundary on the older
  ICS charts (CGI-IUGS RDF series), where the label matches a single boundary. `d_base_diff_vs_ics_v2013_01_myr`
  and its flag compare PBDB/Macrostrat with GTS2012.
- `pbdb_redating_steps_base_age`: EPRP's recorded re-datings (below), by interval name.
- `d_n_plant_filter_occ_early_interval`, `d_n_plant_filter_occ_late_interval`: how many occurrences in
  `pbdb_plant_occurrences.csv` use the name (by name, so identical on rows sharing a name across scales;
  `d_name_shared_by_n_window_intervals`).

**Result (observed).** PBDB's international intervals (scale 1) and Macrostrat's agree with each other
and with the project's table in all 62 compared rows: **0 differences above 0.5 Myr**, including all
Devonian boundaries (Lochkovian 419.62, Pragian 413.02, Emsian 410.62, Eifelian 393.47, Givetian 387.95
Ma). The discrepancy is with older vintages, and it is large in the Devonian: against ICS v2013/01
(GTS2012, which most pre-2024 literature uses) the Pragian base is 2.22 Myr older now, the Emsian 3.02,
the Darriwilian 2.1, the Dapingian 1.3, the Tremadocian 1.45, the Floian −0.6 and the Gorstian −0.7;
the Lochkovian (+0.42) and Eifelian (+0.17) are within 0.5.

**EPRP's known PBDB re-dating issue** (`resources/sources/pbdb-chronosphere/README.md`; data in
`profile/redating_2024_2026.tsv`, sha256 `9fa99b67...`). PBDB moved its interval ages onto ICS-chart
values in three main steps between downloads (2024-03-31/04-01: 460 intervals changed; 2025-03-31/04-10:
317; 2026-08-02/09: 17) and two small ones (2024-02-14/15: one interval; 2025-09-08/18: ten North
American land-mammal ages). The first two touch the window. The second moved the
Devonian onto the Harrigan et al. (2022) ages used by ICS v2024/12: Pragian 410.8 → 413.02 (561 rows),
Emsian 407.6 → 410.62, Lochkovian 419.2 → 419.62, Eifelian 393.3 → 393.47, Givetian 387.7 → 387.95,
Frasnian 382.7 → 382.31, Pridoli 423.0 → 422.7, Ludfordian 425.6 → 425.0, Gorstian 427.4 → 426.7,
Sheinwoodian 433.4 → 432.9, Darriwilian 467.3 → 469.4, Tremadoc 485.0 → 486.4 (after 485.4 → 485.0 in the
first). The Llandovery and Rhuddanian went 443.4 → 443.8 → 443.1. So any PBDB download or extract made
before about 10 April 2025 carries GTS2012-era Devonian and Silurian ages, and a download made between
the steps carries a mixture; an analysis that mixes vintages would shift per-stage counts and rates by
up to 3 Myr. The snapshot used here (2026-10-23) postdates every step. EPRP's third main step (August 2026) moved
three boundaries (Olenekian, Anisian, Wuchiapingian) off the ICS chart; none lies in the window. A
re-dating changes an occurrence's `max_ma` / `min_ma` because PBDB stores ages by interval.

## 5. Macrostrat rock record

`macrostrat_units_window.csv`: units with `t_age < 485` and `b_age > 383`, from the snapshot of
2026-10-25 (API v2.5.0), all projects except 14 ("core columns", which composites the others) and 13
(empty). 5,932 of 133,418 units. Original columns include age (`t_age`, `b_age`, interval names and
positions), `lith`, `environ`, thickness, column id and area, PBDB link counts, centroid and
palaeo-coordinates. `j_*` are joined from the column files: `j_project_name`, `j_col_name`, `j_col_group`,
`j_col_type`, `j_status_code`, `j_col_area_km2`. `d_env_class` is derived from `environ` (the class,
marine or non-marine, of each entry): `marine`, `non-marine`, `both`, or `unknown` (no environment); 
`d_nonmarine_flag` is yes for non-marine or both; `d_nonmarine_environments` lists the non-marine
entries. Macrostrat's "non-marine" includes fluvial, alluvial, eolian, glacial and generic non-marine
entries; I did not separate strictly terrestrial settings further. `d_project_stages_overlapped`
lists the project stages the unit overlaps.

| `d_env_class` | Units |
| --- | ---: |
| marine | 5,234 (4,202 of them "inferred marine") |
| both | 65 |
| non-marine | 84 |
| unknown | 549 |

`macrostrat_summary_by_stage.csv`: one row per project, project stage (the 20 stages of the project
table, Givetian top 382.31 Ma) and unit class: `ALL`, `marine_only`, `nonmarine_only`,
`both_marine_and_nonmarine`, `unknown`, and `ANY_marine` / `ANY_nonmarine` (units with at least one such
entry, so these overlap the exclusive classes). Columns give unit counts (any overlap with the stage; and
for active columns, with the stage's midpoint within the unit's age range) and the summed area of
distinct **active** columns that have such a unit (`area_km2_active_columns_*`, from `col_area`).
Obsolete columns overlap active ones and are not summed; no window unit lies in an obsolete column
(19 are in "in process" columns, which are also excluded from the area). Check: the North American
`ALL`, `ANY_marine` and `ANY_nonmarine` midpoint areas reproduce EPRP's own stage-area series
(`resources/sources/macrostrat/profile/macrostrat_stage_area.tsv`) to within rounding for the six
stages compared (Givetian 6,914,176 / 5,594,313 / 460,304 km² for any / marine / non-marine, 268
columns).

**Geographic coverage (observed).** The 5,932 window units are 5,580 in project 1 (North America;
628 columns), 183 in project 10 (the North American Ediacaran project, whose columns lie inside
North America's: do not add the two), 147 in South America (34 columns), 20 in the Caribbean and 2 in
Indonesia. Macrostrat has no window units from Europe, Asia, Africa, Australia (one placeholder column,
no ages) or New Zealand. **This is a North American rock record**, not a global one: active-column area
with a window unit is about 15.75 million km² in North America, 3.60 million in South America, 0.72
million in the Caribbean. Environment is overwhelmingly marine (88% of units; 549 units, 9%, have none),
and most of that is Macrostrat's "inferred marine" class (4,202 units). Unit ages are interval-derived (the EPRP entry finds 21%
of North American unit boundaries on a stage boundary, against 0.1% by chance). Median unit age span
is 3.7 Myr.

## 6. Fossil Record 2

`../local/record/fr2_plant_families.csv`: all 554 FR2 rows of kingdom Plantae (389; chapters 42–45, which
are Bryophyta, Pteridophyta, Gymnospermophyta, Magnoliophyta), Algae (139, flagged: includes acritarchs,
dinoflagellates, diatoms, charophytes) and Fungi (26, flagged), from EPRP's derived table
(`fr2/derived/2026-10-23T0505Z_url/fr2_families.csv`, itself from the Bristol chapter workbooks, sha256 in
`inputs_sha256.tsv`). All 13 original columns are kept, including the maximum and minimum range
(`max_first` ... `min_last`, FR2 division names) and `extant`. FR2 rows are families or family-surrogates
("Unnamed", orders, genera such as *Cooksonia*).

Window flags (`d_*`): FR2's division names are on Harland et al. (1990) ages, which are not ICS v2024/12.
The primary flag is therefore by **division name**: `d_max_range_overlaps_window_by_division_name`
(and `..._min_range_...`) is yes if the range includes any division correlated with a stage that
overlaps 485–383 Ma (Tremadoc, Arenig, Llanvirn, Llandeilo, Caradoc, Ashgill, Llandovery, Wenlock,
Ludlow, Pridoli, Lochkovian, Pragian, Emsian, Eifelian, Givetian). `d_max_range_overlaps_window_by_harland_ages`
uses FR2's own division ages instead (the Tremadoc, at 510–493 Ma in Harland's scale, drops out, for
example). `d_max_first_division_in_window_by_name` flags families that first appear in the window;
`d_max_first_harland_base_ma` and `d_max_last_harland_top_ma` give the division ages. 108 rows have no
usable range (blank flags).

Result: 45 families overlap the window by name (14 Plantae, 26 Algae, 5 Fungi), 35 of them first appearing
in it, and 41 overlap on Harland ages. The 14 land-plant families are all in Pteridophyta (Cooksonia
from the Wenlock; Rhyniaceae, Zosterophyllaceae, Horneophytaceae, Trimerophytaceae, Barinophytaceae,
Drepanophycaceae, Protolepidodendraceae, Cladoxylaceae, Ibykaceae, Rhacophytaceae, Aneurophytaceae,
Archaeopteridaceae and Lycopodiaceae, from the Ludlow to the Givetian); FR2's bryophyte orders start in
the Frasnian or later.

## 7. Card taxa in PBDB

`card_taxa_pbdb_summary.csv` (whole snapshot; card names, ranks and stage ranges are copied from the 24
`taxa/*.md` cards as they stood on 2026-10-26). Matching is strict and by name, with `cf.`, `aff.` and `?`
ignored and epithet punctuation ignored. For a species card the rule is genus + epithet in the identified
name, the accepted name, or `primary_name` + `species_name`; for a genus card, genus in any of those or in
the `genus` classification field; the three assemblage cards use a genus list (the cryptospore genus list is
mine, not a card field). `n_occurrences_card_level` is the strict count; `n_occurrences_genus_level` counts
the whole genus. Synonyms, older combinations and misspellings are searched separately
(`alt_names_searched`) and listed in `alt_names_found_not_counted`; they are not merged into any count.
Each row has the oldest and youngest occurrence (`max_ma` / `min_ma`, `early_interval`, `late_interval`,
PBDB's `time_major`, occurrence number), the median age span, countries (`cc`:count), counts with
palaeocoordinates under each plate model (GPlates, Scotese, Seton; Seton gives none in this age range),
modern coordinates and references, and `name_notes`. The oldest occurrence is the largest `max_ma`
(ties: shortest span); the youngest is the smallest `min_ma`.

| Card | Card-level n | Genus-level n | Oldest max_ma (interval) | Youngest min_ma (interval) |
| --- | ---: | ---: | --- | --- |
| aberlemnia-caledonica | 0 | 1 | genus: 422.7 (Pridoli) | genus: 419.62 (Pridoli) |
| aglaophyton-majus | 0 | 0 | | |
| ambitisporites | 9 | 9 | 432.9 (Wenlock) | 358.86 (Late Devonian) |
| asteroxylon-mackiei | 0 | 5 | genus: 413.02 (Pragian) | genus: 358.86 (Famennian) |
| baragwanathia-longifolia | 3 | 4 | 426.7 (Ludlow) | 382.31 (Middle Devonian) |
| cooksonia | 33 | 33 | 443.1 (Silurian) | 382.31 (Givetian) |
| drepanophycus-spinaeformis | 45 | 103 | 419.62 (Early Devonian) | 372.15 (Frasnian) |
| early-glomeromycotan-fungi | 0 | 0 | | |
| eophyllophyton-bellum | 1 | 1 | 413.02 (Pragian) | 410.62 (Pragian) |
| horneophyton-lignieri | 1 | 1 | 413.02 (Pragian) | 410.62 (Pragian) |
| nematothallus | 2 | 2 | 422.7 (Pridoli) | 413.02 (Lochkovian) |
| ordovician-cryptospores | 14 | 14 | 445.2 (Hirnantian) | 426.7 (Wenlock) |
| partitatheca | 0 | 0 | | |
| pertica | 3 | 3 | 419.62 (Devonian) | 387.95 (Eifelian) |
| prototaxites | 35 | 35 | 443.1 (Silurian) | 358.86 (Late Famennian) |
| psilophyton | 89 | 89 | 419.62 (Early Devonian) | 316.9 (Westphalian A) |
| renalia-hueberi | 1 | 2 | 410.62 (Early Emsian) | 399.5 (Early Emsian) |
| rhynia-gwynne-vaughanii | 1 | 2 | 413.02 (Pragian) | 410.62 (Pragian) |
| rhynie-chert-gametophytes | 3 | 3 | 413.02 (Pragian) | 410.62 (Pragian) |
| riccardiothallus-devonicus | 0 | 0 | | |
| sawdonia-ornata | 16 | 21 | 419.62 (Early Devonian) | 379.0 (Early Frasnian) |
| tortotubus-protuberans | 0 | 0 | | |
| winfrenatia-reticulata | 0 | 1 | genus: 413.02 (Pragian) | genus: 410.62 (Pragian) |
| zosterophyllum | 33 | 33 | 443.1 (Silurian) | 358.86 (Late Devonian) |

Reading it (observed from the file; the reasons are inferences):
- **Reasonable coverage** (more than ten records): *Cooksonia*, *Prototaxites*, *Psilophyton*,
  *Zosterophyllum*, *Drepanophycus spinaeformis*, *Sawdonia ornata*, though most of these are
  genus-level, wide-interval records (median span of *Drepanophycus* 26 Myr, *Psilophyton* 26 Myr).
- **Single records**: *Eophyllophyton bellum*, *Horneophyton lignieri*, *Renalia hueberi*, *Rhynia*
  *gwynne-vaughanii*, and one each of three Rhynie gametophyte genera (*Lyonophyton*, *Langiophyton*,
  *Kidstonophyton*).
- **Absent or only under another name**: *Aglaophyton* (only as "*Rhynia major*", one record), *Aberlemnia
  caledonica* (one genus-level "*Aberlemnia* sp."; the original combination "*Cooksonia* cf.
  *caledonica*" once), *Asteroxylon mackiei* (misspelt "*mackei*" once; five records of the genus),
  *Winfrenatia* (one genus-level record), *Partitatheca*, *Riccardiothallus*, *Tortotubus* (the name is in
  PBDB's taxonomy with no occurrences), *Remyophyton*, and all the glomeromycotan fungus genera on
  the fungal card (five *Palaeomyces*/*Palaeomycites* records exist but are not on the card).
- **Ordovician cryptospores and the earliest trilete spores are not in PBDB in any useful number**: 14
  cryptospore-genus records in 3 collections, Hirnantian to Wenlock, none Darriwilian to Katian; *Ambitisporites*
  has 9 records, the oldest Wenlock, not the Katian record on the card.
- **Name problems**: PBDB lists *Sawdonia* and many other Rhynie-era names without a taxonomy entry
  (no accepted name); *Baragwanathia* is also spelt "*Baragwanthia*"; the epithet of *Rhynia
  gwynne-vaughanii* has no hyphen; *Horneophyton lignieri* is entered as "*Hornea lignieri*" (PBDB's
  accepted name is *Horneophyton lignieri*), and *Hornea* is a homonym of unrelated, younger taxa, so it
  is not searched as a genus; "*Psilophyton robustius*" is accepted as *Trimerophyton robustius*.
- PBDB assigns age to the interval named by the contributor, so *Baragwanathia* "Ludlow" (426.7–422.7 Ma) and
  the other early records are only as good as the collection's stratigraphic assignment, which PBDB
  does not re-evaluate.

## 8. Inputs, versions and checksums

All paths on `deep-server`, read-only. `inputs_sha256.tsv` has the sha256 of 57 files: the 51 read and 6
FR2 source workbooks listed for provenance only. All 53 that have a mirror `MANIFEST.json` entry match it (PBDB
23, Macrostrat 23, timescale 1, FR2 workbooks 6); the 4 EPRP-derived tables (2 timescale, 2 FR2) have none.
Key files:

| Source | Version | File | sha256 |
| --- | --- | --- | --- |
| PBDB global snapshot | 2026-10-23T0329Z_url (pulled 2026-10-23 03:29–04:03 UTC; `datainfo` access time 03:29:58 GMT; 1,782,649 public occurrences) | `/data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url/` `occurrences__p01..p12` (15 files), `collections__p01..p04` | in `inputs_sha256.tsv` |
| | | `references.csv` | `e5f8977ad2b24fb620115e6b81cba6714a90f77ddee730a919edb4b19bb98cdc` |
| | | `taxa.csv` | `aeb225a5088d93144cf36ccc92fb07b932b92f6d85a31d7a4d2fee1c69fdd945` |
| | | `intervals.csv` (identical to `pbdb/intervals/raw/2026-10-22T0611Z_url/intervals.csv`) | `de1bb12d95699078cbc8e0572dea74ed4935aa1e32051a58d0b62cab7b1d88b8` |
| | | `datainfo.json` (licence statement) | `d971fb760b380434cb32845380d9bd9854d7af4581c859c7a2021ad18fad8286` |
| Macrostrat API v2.5.0 | 2026-10-25T0011Z_url | `/data/paleodata/macrostrat/raw/2026-10-25T0011Z_url/` `units__p*.csv`, `columns__p*.geojson` (projects other than 13, 14) | in `inputs_sha256.tsv` |
| Macrostrat intervals | 2026-10-23T0844Z_url (timescale mirror) | `/data/paleodata/timescale/macrostrat/raw/2026-10-23T0844Z_url/intervals_all.json` | `53d4962b0231a023ce5d81ef3641ff76b583f40dfed302fd80c239ec2e8b6033` |
| ICS tables derived by EPRP | 2026-10-23T0844Z | `/data/paleodata/timescale/derived/2026-10-23T0844Z/ics2024_pbdb_bases.tsv` | `52f75428ed9f8d4f0b17f87c6aec94462e9e29bfdd67d71348b6110eb2532eb2` |
| | | `isc_boundaries_by_version.tsv` | `263692cf8c951f9465e26946f2e782624afea5c0236e28c3c3a47a376a18da4f` |
| FR2, EPRP derived | 2026-10-23T0505Z_url | `/data/paleodata/classic-compendia/fr2/derived/2026-10-23T0505Z_url/fr2_families.csv` | `0fe00658c2e7fbcb38e62ced545b6834da3feed1e2dd88d7fdcce4f3cd4c75ca` |
| | | `fr2_divisions.csv` | `9efa7bbe00837beced4e2cdb538bc120f134284d63d17b5adec08e843371a4b7` |

Embedded in scripts (not read from the mirror): the project's `data/timescale.csv` (sha256 `baf5a4071bd1b47010c3a5f1ffe7b3aebb1fe773497724968a7fcd5858d4c35f`)
and the window's re-dating events from EPRP's `profile/redating_2024_2026.tsv` (sha256 `9fa99b67a2e1e797247d7df12bda7dec102bcdd6947df36fb7ff0b99cad5b300`).
The cryptospore, fungal and spore-form name lists in `record_pbdb.py` are mine.

Licences: PBDB CC0 per the API's `datainfo` (`data_license`), recorded with this snapshot; Macrostrat CC
BY 4.0 (API metadata); CGI-IUGS RDF series CC0; ICS chart PDFs print a copyright line and no licence
(EPRP tier `unclear`); FR2 none stated. Cite PBDB with the data-service query URL and retrieval date
(2026-10-23), and the primary references in `pbdb_plant_references.csv`; cite Macrostrat as Peters et al.
(2018) and the API with its access date.

## 9. Caveats from the EPRP catalogue entries that bear on this use

- **Withheld PBDB records.** PBDB's collection-joined queries also return access-restricted occurrences
  (225,363 globally). EPRP's snapshot was built from record-level queries and contains public occurrences
  only (checked by EPRP against `occs/single`), and so do these files. Collection `n_occs` normally counts
  withheld records too; for these 1,302 collections it equals the public count (observed), so none of
  them has withheld records. `d_n_public_occurrences_all_taxa` gives the public count over all taxa.
- **No versions in PBDB.** The live database changes; this snapshot is the fixed copy. Interval re-dating
  (§4) means an extract's ages depend on its date.
- **Licence change.** PBDB's licence was CC BY 4.0 until 2025-02-20 and is CC0 in the API since; the
  Navigator page and GBIF still say CC BY 4.0. The snapshot's `datainfo` states CC0.
- **2025 IODP import.** 306,489 PBDB occurrences created on 2025-09-21 are marine microfossils, mostly
  Pleistocene to Miocene (EPRP entry); none is among the window's 227,465 rows (checked by creation stamp).
- **Coordinates and age.** `protected` is FED or NPS on 177 occurrence rows (74 collections): PBDB flags
  collections on US federal or National Park land; whether coordinates are then generalised is not
  documented in the catalogue (inference: treat them as possibly imprecise). Palaeocoordinates are
  model-dependent; EPRP's check on its Australian region found GPlates and Scotese palaeolatitudes differ by a
  median 12–16° for Silurian to Carboniferous collections (not rechecked for this file). 2,625 of 2,628 core rows have GPlates palaeocoordinates,
  2,613 Scotese, none Seton.
- **Coverage follows projects.** One contributor's entry of one reference (Stein 2002) is 16% of the
  filtered rows; core rows come mostly from the USA (539), UK (526), Canada (381), Australia (259) and
  Belgium (219).
- **Macrostrat.** See §5: North American, interval-derived ages, PBDB link counts include withheld
  records (not used here).
- **FR2** is frozen (1993), on Harland et al. (1990) ages, and has no stated licence.

## 10. Not done

- No richness or range estimation, no standardisation, no cleaning of PBDB identifications beyond the
  rules above; raw values are unchanged.
- The identity of the Ordovician "plant" records (§3) was not checked against the literature.
- No taxonomic harmonisation to the project's cards beyond the name matching in §7.
- PBDB specimens, measurements, opinions and the full taxa table were not extracted; Macrostrat
  measurements, `fossils` links, sections and age models were not used (the unit file's
  `pbdb_collections` / `pbdb_occurrences` counts are kept as given). Sepkoski's animal compendium is not
  relevant here.
- No match between Macrostrat units and the PBDB collections in the plant file was attempted.
- Acritarchs, red algae and animal-lookalike groups were not completed or refined (§2).

## 11. Reproduce

From `data/eprp/scripts/` (each script is stdlib Python and self-contained):

```sh
for s in record_pbdb record_intervals record_fr2 record_macrostrat record_inputs; do
  ssh deep-server python3 - < $s.py
done
rsync -a deep-server:/data/codex/silurian_plants-eprp/record/out/ out/
```

`record_pbdb.py` must run before `record_intervals.py` (it reads the plant occurrence file for interval
usage). A second run on 2026-10-26 gave byte-identical outputs. Copy `fr2_plant_families.csv` and
`ics2024_chart_values_window.csv` to `data/eprp/local/record/` and the rest to `data/eprp/record/`.
