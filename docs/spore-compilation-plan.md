# Dispersed-spore compilation plan

Scoping study, 2026-10-27, drafted by a Claude Sonnet 5.5 subagent (`claude-sonnet-5-5`); not yet reviewed. It serves the spore channel of F3 and the spore similarity matrices of F4 (`docs/framings.md`) and answers the project-side task in `docs/sources.md`. Facts about Palynodata and the Global Acritarch Database (GAD) come from the EPRP session's check and are not re-verified here beyond the Crossref DOIs. All other facts come from sources opened for this study; where only an abstract or a press summary was read, the table says so.

**Proposed structure.** Four layers, each a separate source tag in the final tables:

1. Palynodata (EPRP extraction, literature to 2006) as the base occurrence layer.
2. The Wellman et al. lists as the curated Ordovician–Silurian layer, plus two Devonian and Ordovician tables from the same group.
3. The post-2006 literature as the gap, filled by the method GAD used.
4. Marine palynological documents (acritarch, chitinozoan) as a sampling-effort layer that records where spores were looked for and not found.

## 1. Existing compilations

| Source | Coverage and level | Tabulated? | Access and licence |
|---|---|---|---|
| Palynodata (White 2008) | EPRP: 14,114 spore and pollen rows from 985 documents, 485–383 Ma; 738 Ordovician-labelled spore rows from 135 documents; per-document mentions, region text, no coordinates, 2006-era ages | Yes, rows | Open Government Licence – Canada; the Crossref abstract confirms the last literature entered was 2006 |
| Wellman, Steemans & Vecoli 2013, Appendix 2 (supplement) | Tremadoc–Pridoli, species lists by region and series: about 150 region-by-series lines, 120 references, of which 8 date from 2007 or later (my count from the PDF text). Compiled by Steemans around 2011 on GTS2004 series names (Llanvirn, Caradoc, Ashgill). 787 species–series–region data points were analysed (Silurian only) | Text in a PDF; needs parsing | Supplement PDF on figshare (geolsoc.figshare.com, article 3453524), CC BY 4.0. The chapter says the full database "is available from the authors" |
| Steemans's Liège database | The full database behind the chapter, updated with unpublished data (Bek et al. 2024: "database stored in the University of Liege") | Unknown | Request only |
| Wellman, Cascales-Miñana & Servais 2022, Table 1 | 48 Ordovician assemblages, Dapingian–Hirnantian, with palaeocontinent, palaeoenvironment, age-dating basis (conodont, chitinozoan, graptolite, invertebrate, palynology, lithostratigraphy) and references; no taxa. Flags disputed entries in footnotes | Table in PDF | CC BY (Crossref). The paper states no dataset was generated |
| Wellman, Steemans & Lopes 2023, Table 7 and Appendix 1 | 33 regions with Emsian spore assemblages, with spore zone and key references; Appendix 1 holds Emsian taxon lists by region and local zone | Table 7 in PDF; Appendix 1 online | CC BY (Crossref); "data on request" |
| Ball 2022 (Sheffield PhD) | Anglo-Welsh Basin, Ludlow to mid-Lochkovian: 183 species in 42 genera, per-sample counts to 250 spores | Yes: Appendix 3 workbook (counts, ornament groups) | White Rose eTheses, open; CC BY-NC-ND 4.0, so treat derived tables as local |
| Pšenička et al. 2021 | Silurian globally; Table 1 is a graphic of spore-type frequency | No | CC BY; data on request |
| Bek et al. 2024; Bek et al. 2026 | Pridoli by climate belt (Table 2 counts, Table 3 autochthonous taxa); 2026 paper on Ordovician–Silurian cryptospore and trilete diversity against climate (abstract only read) | Summary tables only | 2024 CC BY; 2026 hybrid open access, CC BY-NC |
| Cascales-Miñana 2016 | Ordovician–Mississippian spore and megafossil diversity curves (abstract only) | Data source not verified | Paywalled; ORBi copy restricted |
| Steemans, Wellman & Gerrienne 2010 | Ordovician–Lochkovian palaeogeographic synthesis with maps (abstract only) | Not verified | Closed |
| Wang et al. 2026 | Global cryptospore review: 36 genera, 102 species s.l.; Chao2, GAM, NMDS (from the NIGPAS news item, not the paper) | Unknown | Paywalled |

**Best seeds.** Palynodata for breadth, the three open Wellman tables for curated assemblage-level metadata, and Ball 2022 for Anglo-Welsh sample counts. The largest single gain would be the Liège database, which would bring the curated list to about 2020. It needs a request to Steemans and Wellman, which is an external message and so Barry's call.

**Not occurrence datasets, but needed.** Zonation and correlation sources give the zone-to-stage links the age crosswalk needs: Richardson & McGregor 1986 (Old Red Sandstone continent), Streel et al. 1987 (Ardenne–Rhenish), Breuer & Steemans 2013 (north-western Gondwana), Richardson & Ioannides 1973 (Libya) and Edwards & Richardson 2004 (Anglo-Welsh). Strother and colleagues (Strother 2000; Strother et al. 2015; Strother & Foster 2021) supply the exclusion and dispute rules, not tables. Capel et al. 2022 and 2023 cover macrofossils only. Hooper et al. 2026 hold character scores and calibration tables on data.bris (linked from the paper's data statement), not occurrences.

## 2. The primary-literature universe

**Method.** Three independent lenses, none complete.

1. An OpenAlex title-and-abstract search (27 October 2026) for cryptospore, miospore, trilete spore, dispersed spore, spore assemblage or spore zone together with Ordovician to Early Devonian stage terms returned 493 works: 28, 38, 63 and 84 for 1950–79, 1980s, 1990s and 2000–06, and 280 for 2007–2026. Abstracts are sparse before 1990, so the early counts are floors; Palynodata covers that period.
2. Of the 280, 274 titles are unique and 192 name spores or palynology. Dropping ultrastructure, in situ, review, Cambrian, Carboniferous and Mesozoic papers leaves 130 occurrence-type titles: 71 Ordovician–Silurian, 49 Devonian, 10 undated in the title. They fall 21, 43, 33, 26 and 7 in 2007–09, 2010–14, 2015–19, 2020–24 and 2025–26.
3. Recall check: of 22 post-2006 papers cited in Wellman et al. 2022 Table 1 that I checked by eye against the list, 17 were among the 130 (about 75%; a small test set).

Dividing by recall and adding a judgemental allowance for papers whose titles omit spore terms gives **about 200 post-2006 spore-bearing papers (plausible range 150–260)**. The curated lists confirm the gap: Wellman et al. 2013 cite almost nothing after 2009, and about 24 of 55 distinct author-year citations in the 2022 Ordovician table post-date 2006 (my count).

| Region | Ordovician assemblages, Wellman et al. 2022 (n = 48) | Appendix 2 lines, Wellman et al. 2013 (about 150) | Post-2006 titles found (n = 130) | Central estimate, post-2006 papers |
|---|---|---|---|---|
| Laurentia (incl. Scotland, Svalbard) | 7 | 17 | 12 | 20 |
| Avalonia, Baltica, peri-Gondwanan Europe | 15 | 63 | 27 | 40 |
| North Africa | 6 | 19 | 10 | 15–25 |
| Arabia, Iran, Turkey | 9 | 15 | 29 | 45 |
| South America | 5 | 16 | 29 | 45 |
| South Africa, Australia, other Gondwana | 3 | 2 | 1 | 5–10 |
| South China, Tarim, E Asia, Siberia, Kazakhstania | 3 | 8 | 12 | 25–35 |
| Unassigned in title | | | 10 | about 15 |

South China, North Africa (petroleum reports) and Siberia (Russian-language journals) are the likeliest undercounts. Argentina, Brazil and Uruguay are well indexed.

**Marine palynological documents.** OpenAlex finds 704 works up to 2006 and 711 from 2007 that mention acritarchs, chitinozoans or phytoplankton with the same stage terms (overlap with the spore set not measured). GAD already supplies the acritarch layer, with ICS v2024/12 ages and palaeocoordinates (Shu et al. 2025: 415 references added for 2008–2023 to Palynodata's 7,369). Chitinozoan documents after 2006 would be tagged at document level only. For scale: GAD needed 415 new references across all time; our gap is about half that, but each paper needs assemblage-level, spore-type extraction.

## 3. Record schema

Four tables in `data/spores/` (CSV, loaded to DuckDB), plus crosswalks. Every row carries `source_tag` (palynodata, wellman2013, wellman2022, wellman2023, ball2022, gap) so layers can be dropped or compared.

**`documents`**: `doc_id`, DOI, citation, language, access status and licence, `palynodata_doc_id`, `extractor`, `extraction_date`.

**`assemblages`** (one per sample horizon, section interval or formation composite; `assemblage_scope` says which, and a Palynodata-only record is a pseudo-assemblage of document × region text × age):
- *Place:* locality, country, formation, section or core with depth, latitude and longitude with source and uncertainty, `palaeogeo_unit_reported` and `palaeogeo_unit` (harmonised: Wellman's units plus Siberia, Kazakhstania, Armorican Terrane Assemblage), palaeocoordinates with plate model and version.
- *Age, never overwritten:* `age_as_reported` verbatim, `timescale_as_reported` (for example GTS2004 series, GTS2012, regional spore zone), `age_basis` (conodont, chitinozoan, graptolite, invertebrate, acritarch, spore zone, radiometric, lithostratigraphic), basis taxon or zone, `age_circular` (true when the spores date the rock), `stage_min` and `stage_max` on ICS v2024/12 names, `crosswalk_rule_id`, radiometric ages as measured with method and error.
- *Setting:* lithology as reported and class; facies as reported; `setting_class` (marine shelf, marine offshore, marginal marine, non-marine, unknown) and a marine/non-marine flag.
- *Quality:* `n_samples`, `n_spores_counted`, count method, spore yield, thermal maturity, `reworking_status` (none, discussed, claimed, demonstrated), `contamination_note`, `status` (accepted, disputed, excluded) with reason.
- *Source:* page, table or figure; extractor confidence.

**`occurrences`**:
- *Name:* `taxon_as_reported` verbatim with qualifiers (cf., aff., sp.), author and year if given, `genus_reported`, `genus_harmonised` with `harmonisation_rule`.
- *Spore type:* `spore_class` (cryptospore, trilete, monolete, other miospore, spore-like questionable), `unit` (monad, dyad, tetrad, polyad), `attachment` (fused, unfused), `envelope` (none, laevigate, ornamented), `hilate` flag, `trilete_mark` (functional, questionable, absent), `ornament` (laevigate, ornamented). The characters follow the cryptospore taxonomy Wellman et al. 2022 list (units, attachment, envelope, ornament); the Steemans & Wellman 2018 key (text not read) is the first reference for the lookup.
- *Abundance:* value and unit (count, %, presence only), `illustrated`, `in_situ`, taxon-level reworking flag.
- *Source:* page, table or figure.

**`effort`**: one row per marine palynological document (or GAD reference) with locality, age fields as above and `spores_reported` yes/no, so spore-free assemblages count as zero observations.

**Crosswalks** (all versioned): regional series and zone names to ICS v2024/12 stage ranges (Llanvirn, Caradoc, Ashgill and spore zones straddle stage boundaries, so map to a range and cite the correlation source); palaeogeographic units; genus to spore type. Radiometric ages are kept as measured and re-assigned to stages on `data/timescale.csv`; Ma values are never converted between timescales.

## 4. Extraction plan

Effort figures are my estimates in agent-time, not measurements.

| Phase | Work | Output | Effort |
|---|---|---|---|
| 0 | Schema, three crosswalks, spore-type lookup seeded from Steemans & Wellman 2018 | Empty tables, rules | 2–3 days |
| 1 | Palynodata at document level (EPRP extract); digitise Wellman 2013 Appendix 2, Wellman 2022 Table 1, Wellman 2023 Table 7 and Ball 2022 Appendix 3; merge and de-duplicate by locality and age | **MVD-A**, Darriwilian–Emsian, all open | about 1 week |
| 2 | Harvest 2007–2026 literature from OpenAlex and Crossref; triage about 250 spore candidates; load GAD as the effort layer | Gap list with access status | 2–3 days |
| 3 | Assemblage- and occurrence-level extraction of gap papers, Ordovician–Silurian first (about 70–90), then Lochkovian–Emsian (about 60–100). About 20–40 agent-minutes per paper including table checks | **MVD-B**, then full | 70–130 agent-hours; 1.5–3 weeks with 5–8 parallel agents |
| 4 | Independent second-agent re-extraction of 10%; compare with the curated lists; Barry reviews exceptions | Error rates | 2–3 days; a few hours of Barry's time |

**Minimum viable dataset.** Presence and first appearance by stage × palaeogeographic unit for six spore classes (cryptospore monad incl. hilate and enveloped, dyad, tetrad, trilete laevigate, trilete ornamented, other), Dapingian or Darriwilian to Emsian (16 stages with the disputed Dapingian), with age basis and setting class per record. MVD-A reaches this from Palynodata plus the three open tables, without re-reading papers, at document-level resolution. MVD-B adds the 2007–2026 first appearances and the spore-free effort rows, which first-appearance estimators need.

**Open sources alone suffice for MVD-A.** The Liège database, paywalled primary papers (Elsevier journals mainly; open-access share not measured) and the data behind Cascales-Miñana 2016 and Wang et al. 2026 need a request or institutional access.

## 5. Risks

- **Taxonomic inconsistency.** Wellman et al. 2013 write that synonymy "is probably rife" and note that palynology schools use different taxonomies by region, so apparent provincialism can be a naming artefact. Their own labels disagree: the text calls North African localities "southwestern Gondwana", the appendix uses that label for Saudi Arabia. Harmonise to genus and morphological class, keep names as reported, and never map to plant groups at extraction.
- **False trilete and hilate marks.** Spores torn from cryptospore tetrads and dyads can bear a false mark (Wellman et al. 2022), so Ordovician trilete records need `trilete_mark` status and an illustration flag. Hooper et al. 2026 rest their embryophyte-crown maximum on Swedish Sandbian spores but did not use them as a minimum, because the mark might be a compression artefact.
- **Age uncertainty.** Regional series and zones straddle stages; Early Devonian bases differ by up to 3 Myr between GTS2012 and ICS v2024/12 (`docs/primer.md` §1). Many Ordovician ages rest on palynology itself, which is circular for first-appearance tests, hence `age_circular`.
- **Contamination, reworking and definitions.** some Hirnantian glacial-deposit cryptospores are reworked (`taxa/ordovician-cryptospores.md`); Wellman et al. 2022 flag the Argentine Dapingian record as questioned by Strother et al. 2015; the Tremadocian–Arenig "spore-like" forms are variously read as algal or acritarch (Strother & Foster 2021; Navidi-Izad et al. 2022). Carry `status` and `reworking_status`, and run F3 with and without disputed records.
- **Hooper et al. 2026.** If trilete spores mark the crown embryophyte and cryptospores are stem-group, the two channels no longer mean "vascular" and "bryophyte". The schema therefore stores morphology, not affinity, so either reading can be applied downstream, and the first-appearance records that Hooper et al. use as calibrations (Qusaiba-1 *Ambitisporites avitus*, Dalby Limestone) get explicit flags.
- **Double counting.** One assemblage is often re-reported (Qusaiba-1 appears in several papers); de-duplicate on locality, interval and age before computing first appearances.
- **Licences and access.** Ball 2022 is NoDerivatives; Palynodata is OGL; the Elsevier supplements are "on request". Record the licence per row source.

## References

- Ball AC (2022). The late Silurian – Early Devonian adaptive radiation of vascular land plants: palynological evidence from the Anglo-Welsh Basin, U.K. PhD thesis, University of Sheffield (no DOI).
- Bek J, Steemans P, Frýda J, Žárský V (2024). Silurian Climatic Zonation of Cryptospore, Trilete Spore and Plant Megafossils, with Emphasis on the Přídolí Epoch. Life 14: 258. https://doi.org/10.3390/life14020258
- Bek J, Strossová Z, Frojdová J, Frýda J (2026). Did the first plants prefer the same temperatures as modern plants? Evidence from Ordovician and Silurian cryptospores and trilete spores. Palaeoworld 35: 201138. https://doi.org/10.1016/j.palwor.2026.201138
- Breuer P, Steemans P (2013). Devonian spore assemblages from northwestern Gondwana: taxonomy and biostratigraphy. Special Papers in Palaeontology 89: 1–163 (no DOI).
- Capel E, Cleal CJ, Xue J, Monnet C, Servais T, Cascales-Miñana B (2022). The Silurian–Devonian terrestrial revolution: Diversity patterns and sampling bias of the vascular plant macrofossil record. Earth-Science Reviews 231: 104085. https://doi.org/10.1016/j.earscirev.2022.104085
- Capel E, Cleal CJ, Servais T, Cascales-Miñana B (2023). New insights into Silurian–Devonian palaeophytogeography. Palaeogeography, Palaeoclimatology, Palaeoecology 613: 111393. https://doi.org/10.1016/j.palaeo.2023.111393
- Cascales-Miñana B (2016). Apparent changes in the Ordovician–Mississippian plant diversity. Review of Palaeobotany and Palynology 227: 19–27. https://doi.org/10.1016/j.revpalbo.2015.10.005
- Edwards D, Richardson JB (2004). Silurian and Lower Devonian plant assemblages from the Anglo-Welsh Basin: a palaeobotanical and palynological synthesis. Geological Journal 39: 375–402. https://doi.org/10.1002/gj.997
- Hooper J, Worth AM, Wellman CH, Clark JW, Donoghue PCJ (2026). Reconstructing spore evolution recalibrates the timescale of land plant diversification. Nature Plants. https://doi.org/10.1038/s41477-026-02432-3
- Navidi-Izad N, Benachour H, Kroeck D, Steemans P, Servais T (2022). Virgatasporites and Attritasporites: the oldest land plant derived spores, cryptospores or acritarchs? Botany Letters 169: 495–509. https://doi.org/10.1080/23818107.2022.2113560
- Pšenička J, Bek J, Frýda J, Žárský V, Uhlířová M, Štorch P (2021). Dynamics of Silurian Plants as Response to Climate Changes. Life 11: 906. https://doi.org/10.3390/life11090906
- Richardson JB, Ioannides NS (1973). Silurian Palynomorphs from the Tanezzuft and Acacus Formations, Tripolitania, North Africa. Micropaleontology 19: 257–307. https://doi.org/10.2307/1484881
- Richardson JB, McGregor DC (1986). Silurian and Devonian spore zones of the Old Red Sandstone Continent and adjacent regions. Geological Survey of Canada Bulletin 364. https://doi.org/10.4095/120614
- Shu X, Song H, Lei Y, Chu D, Dal Corso J, et al. (2025). Global Acritarch Database (> 110 000 occurrences). Earth System Science Data 17: 3567–3582. https://doi.org/10.5194/essd-17-3567-2025
- Steemans P, Wellman C (2018). A key for the identification of cryptospores. Palynology 42: 492–503. https://doi.org/10.1080/01916122.2017.1411844
- Steemans P, Wellman CH, Gerrienne P (2010). Palaeogeographic and palaeoclimatic considerations based on Ordovician to Lochkovian vegetation. Geological Society, London, Special Publications 339: 49–58. https://doi.org/10.1144/sp339.5
- Streel M, Higgs K, Loboziak S, Riegel W, Steemans P (1987). Spore stratigraphy and correlation with faunas and floras in the type marine Devonian of the Ardenne-Rhenish regions. Review of Palaeobotany and Palynology 50: 211–229. https://doi.org/10.1016/0034-6667(87)90001-7
- Strother PK (2000). Cryptospores: the origin and early evolution of the terrestrial flora. The Paleontological Society Papers 6: 3–20. https://doi.org/10.1017/s1089332600000681
- Strother PK, Foster C (2021). A fossil record of land plant origins from charophyte algae. Science 373: 792–796. https://doi.org/10.1126/science.abj2927
- Strother PK, Traverse A, Vecoli M (2015). Cryptospores from the Hanadir Shale Member of the Qasim Formation, Ordovician (Darriwilian) of Saudi Arabia: taxonomy and systematics. Review of Palaeobotany and Palynology 212: 97–110. https://doi.org/10.1016/j.revpalbo.2014.08.018
- Wang K, Xu H-H, Liu B, Wang Y (2026). Dynamic evolution of cryptospores: The origin and rise of the land flora. Earth-Science Reviews 277: 105476. https://doi.org/10.1016/j.earscirev.2026.105476
- Wellman CH, Cascales-Miñana B, Servais T (2022). Terrestrialization in the Ordovician. Geological Society, London, Special Publications 532: 171–190. https://doi.org/10.1144/sp532-2022-92
- Wellman CH, Steemans P, Lopes G (2023). Dispersed spore assemblages from the Lower Devonian Rañeces - La Vid groups of Northern Spain: Palaeogeographical implications. Review of Palaeobotany and Palynology 310: 104825. https://doi.org/10.1016/j.revpalbo.2022.104825
- Wellman CH, Steemans P, Vecoli M (2013). Chapter 29 Palaeophytogeography of Ordovician–Silurian land plants. Geological Society, London, Memoirs 38: 461–476. https://doi.org/10.1144/m38.29
- White JM, Palynodata Inc. (2008). Palynodata Datafile: 2006 version. Geological Survey of Canada Open File 5793. https://doi.org/10.4095/225704
