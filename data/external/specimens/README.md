# specimens/: museum fossil-specimen records for the 485–383 Ma window

GBIF, iDigBio and the EPRP Australian mirror, searched for early-land-plant material. Extracted 2026-10-27
by a Claude Sonnet 5.5 subagent (`claude-sonnet-5-5`) for the silurian_plants project. EPRP was used read-only
(commit `ac42dfb`); nothing was written to EPRP or to `/data/paleodata`. Scripts are `../scripts/specimens_*`
(stdlib Python). The heavy queries ran on `deep-server`; the raw JSON pages stay there (not reachable from the Macs; a rebuild re-harvests on `nectar`).

## 1. What is here

All paths are under `data/external/`. Row counts are data rows. `local/` is git-ignored.

| Path | Rows | MB | Contents |
|---|---:|---:|---|
| `local/specimens/idigbio_specimens.csv` | 19,843 | 20.2 | Full iDigBio window table; rows of the NHMUK and NRM-PZ recordsets state no licence and iDigBio records their rights as 'Unknown License, assume Public Domain', so rights are unclear for the table as a whole. Git-ignored |
| `local/specimens/specimens_merged_all.csv` | 44,873 | 48.7 | Merged table including iDigBio rows with no stated licence. Git-ignored |
| `specimens/ala_specimens.csv` | 274 | 0.3 | Window specimens from the EPRP mirror of GBIF Australia and Papua New Guinea records (the ALA route); a subset of GBIF's records |
| `specimens/build_stats.json` |  | 0.0 | Counts written by the build script: records retrieved, dropped by reason, subsets, window statuses, dedupe groups and rule counts |
| `specimens/card_taxa_specimens_by_institution.csv` | 907 | 0.0 | Long form of the card summary: scope name x source x institutionCode x rows |
| `specimens/card_taxa_specimens_summary.csv` | 131 | 0.1 | Per card taxon, anchor genus, nematophyte and charophyte name: specimens by source and institution, ages as given, names as recorded |
| `specimens/dedupe_by_institution.csv` | 51 | 0.0 | Physical specimens per institutionCode by the source set that holds them (GBIF, ALA mirror, iDigBio); shows where sources hold unlinked records |
| `specimens/gbif_backbone_placement.csv` | 117 | 0.0 | Where each searched genus sits in the GBIF backbone (all homonyms), with fossil-specimen counts per backbone taxon |
| `specimens/gbif_datasets.csv` | 64 | 0.0 | GBIF datasets of the retained records: datasetKey, title, DOI, licence, publisher and record counts, for citation |
| `specimens/gbif_specimens.csv` | 24,756 | 26.4 | GBIF fossil specimens in the 485-383 Ma window (plus Frasnian-Famennian anchor genera), core and flagged subsets, one row per GBIF occurrence |
| `specimens/idigbio_recordsets.csv` | 28 | 0.0 | iDigBio recordsets behind the retained rows with the data rights each states and the share of rows with a record-level licence |
| `specimens/idigbio_specimens_open_licence.csv` | 14,387 | 15.3 | iDigBio window specimens whose own record or whose recordset states CC0, CC BY or CC BY-NC (derived_licence_effective_source says which); the full iDigBio table is in local/specimens/ |
| `specimens/specimen_filter_names.csv` | 2,392 | 0.4 | Filter audit: each distinct name among window candidates, by source, with count, classification (core, flagged, excluded) and reason |
| `specimens/specimens_merged.csv` | 39,417 | 43.5 | GBIF, ALA-mirror and open-licence iDigBio rows in one table; every source row kept, duplicates linked by derived_dedupe_key and derived_duplicate_of |
| `specimens/harvest_provenance/*.tsv` | 10 files | 10.0 | Per-harvest `provenance.tsv` (every raw page with URL, query, time, record count, sha256) and `queries.tsv` (every query with its count and how many records were new) |
| `specimens/README.md`, `specimens/MANIFEST.tsv` | | | This file; the manifest (path, description, source, version, licence, script, rows, sha256, extracted) |
| `scripts/specimens_scope.py`, `specimens_scope_names.csv`, `specimens_harvest.py`, `specimens_build.py`, `specimens_manifest.py` | | | Scripts (stdlib Python) and the searched-names table |

Source columns keep the source's own values. Every column the scripts compute starts with `derived_`; no source
age, name or licence was converted or repaired. Collector and determiner names (`recordedBy`, `identifiedBy`) are
not carried over, as in EPRP's convention for the Australian mirror. Media: URLs only, no image downloaded.

## 2. Scope

- **Window.** 485–383 Ma, applied to the age fields as recorded (§4). Frasnian–Famennian (382.31–358.86 Ma)
  records are kept for the anchor genera only: *Archaeopteris*, *Callixylon*, *Eospermatopteris*, *Wattieza*,
  *Elkinsia* and, added by the project on 2026-10-27, *Leclercqia*.
- **Taxa.** Land plants (Embryophyta, including dispersed-spore form genera), fossil charophytes, *Prototaxites* and
  the nematophytes (*Nematothallus*, *Nematophyton*, *Pachytheca*, *Nematasketum*, *Nematoplexus*, *Parka* and
  the other names the cards give), and every card taxon, anchor genus and tranche-2 name by name. The full list of
  searched names, with the reason each is on it, is `../scripts/specimens_scope_names.csv`, built from `taxa/*.md`
  by `specimens_scope.py` (it reads the cards at run time; names from `docs/decisions.md` for cards not yet written
  are tagged `planned_card`): 147 name rows from 59 cards, the anchors, nematophytes, charophytes and planned cards, of which 134 are searchable names (98 genera and 36 binomials, 92 distinct genera) and the rest group, site or higher-rank cards that are not searched by name. The harvest ran from an earlier version of this file, written before the project's later cards (117 rows); the current file adds only group and site cards and the genera *Anthoceros* and *Phlegmariurus*, which a supplementary run covered (`20261027T012054Z`, `20261027T012105Z`).
  Search-aid names (charophyte genera, *Nematophycus*, *P. southworthii*) come from the analyst's general knowledge,
  not from a source read in this task, and are marked as such in the reason column.
- **Core, flagged, excluded** (the EPRP PBDB filter's idea, `data/eprp/record/README.md` §2; classification is by the
  record's own lineage plus names, in `derived_class` and `derived_subset`; every distinct name is in
  `specimen_filter_names.csv` with its count, class and reason):
  - *core*: embryophyte lineage, dispersed spore form genera, nematophytes and thalloid problematica named in scope,
    scope-named fungi and lichens (*Winfrenatia*, *Palaeoglomus* ...), fossil charophytes.
  - *flagged* (kept, and reported as subsets): green algae other than charophytes (mostly receptaculitids and
    dasyclads), red algae, algae without a group, acritarchs and prasinophytes, fungi not named in scope, plant-like
    problematica and trace fossils filed under plants (*Buthotrephis*, *Protosalvinia* ...), Plantae-only
    determinations, kingdom *incertae sedis*, and embryophyte lineages that cannot be right for the age (seed-plant
    or flowering-plant lineages on records older than 340 Ma; vascular lineages on records entirely older than
    433 Ma), and scope names whose backbone lineage is animal or protist (homonyms).
  - *excluded* (counted in the build statistics and listed in the name audit, not in the tables): animals,
    foraminifera and other protists, cyanobacteria and calcimicrobes, ichnofossils, nameless or unidentified lots,
    and animal genera that the source files under a plant or fungal homonym (*Orthoceras*, *Tetradium*, *Vertebrata*...).
  Charophytes are core here because the brief puts them in scope; EPRP's PBDB filter flags them. Plantae-only
  determinations are flagged here; EPRP's filter treats PBDB's equivalent as core.

## 3. Sources, queries and versions

### GBIF (live search, 2026-10-27)

`https://api.gbif.org/v1/occurrence/search`, `basisOfRecord=FOSSIL_SPECIMEN`, no authentication (the asynchronous
download API needs an account and was not used), user agent `silurian-plants-specimen-harvest/1.0` (no contact
details). 300 records a page; any query above 9,000 hits was split by `datasetKey` because pages beyond an offset
of about 10,000 are slow (observed: 36 s a page at offset 15,000). Raw pages: `deep-server:/data/codex/silurian_plants/raw/gbif/<stamp>/`
with `provenance.tsv` (URL, query, UTC time, record count, sha256 for every page) and `queries.tsv`; copies are in
`harvest_provenance/`.

Query groups, in the order they ran:
1. Plantae (`taxonKey=6`) with `earliestPeriodOrLowestSystem` and with `latestPeriodOrHighestSystem` in Ordovician,
   Silurian or Devonian. GBIF counted 4,871, 1,660 and 15,844 for the earliest field; the retrieved records match
   those counts exactly. The same two queries for Fungi, Chromista, Protozoa, Bacteria, Archaea and kingdom
   *incertae sedis* (kingdom keys 5, 4, 7, 3, 2, 0).
2. The epoch and stage fields (earliest and latest) for 12 epoch names and 31 stage names across the window, for
   each of those kingdoms. GBIF's period filter also matches records that give only a stage or epoch, so almost every
   such query was already covered: before paging a query I counted its records not already inside the period
   queries; only queries with new records were fetched. 633 queries of this kind were planned (168 epoch, 434 stage, 31 free-text); 603 were skipped as already covered and 30 were fetched, which could add at most 5,228 records (5,167 from the free-text queries, many of them not stratigraphic: *Ludlow* is a town).
3. Free-text `q` for 31 period, epoch and stage names (Devonian, Lochkovian, Downtonian ...) on Plantae, to reach
   records with no period field. Same novelty test.
4. Every searched genus by `q` (any kingdom, any age) and by backbone `taxonKey` for each non-animal usage of
   the name in the legacy backbone (so homonyms such as *Cooksonia* Druce, a moth, are not taken). No name had more
   than 6,000 hits, so none was capped.
5. `/occurrence/{key}/verbatim` for the 16,507 candidate records that GBIF could match only approximately
   (`TAXON_MATCH_HIGHERRANK`, `_FUZZY` or `_NONE`). GBIF's search results do not carry the verbatim name, so
   `taxon_recorded` comes from the verbatim record where fetched (`taxon_recorded_basis = gbif_verbatim_record`) and
   otherwise is GBIF's interpreted name, which for an exact match is the recorded name.
6. `/dataset/{key}` and `/organization/{key}` for the datasets of retained rows (`gbif_datasets.csv`).

Result: 34,133 unique records retrieved (31,330 in kingdom Plantae), 810 MB of search pages,
about 30 (structured pass 23, names pass 7) minutes of paging. In the GBIF backbone (legacy backbone, `gbif_backbone_placement.csv`),
*Prototaxites*, *Nematothallus*, *Nematophyton*, *Nematophycus*, *Nematasketum* and *Cosmochlaina* sit in kingdom Fungi, family
Nematothallaceae; *Pachytheca* (Hooker), *Parka*, *Nematoplexus*, *Tortotubus* and *Ambitisporites* are Plantae with no phylum;
*Winfrenatia* is Fungi. A Plantae-only query therefore misses the nematophytes; the name queries and the Fungi
kingdom queries catch them.

### iDigBio (live search, 2026-10-27)

`https://search.idigbio.org/v2/search/records/`, `rq` JSON, `basisofrecord: fossilspecimen`, 1,000 records a page
sorted by uuid, 0.3 s between pages. The index was last modified 2026-04-23. Groups: (1) `kingdom: plantae` with a
record-wide full-text term for 31 period, epoch and stage names plus 8 regional names (Niagaran, Cincinnatian,
Helderbergian ...); iDigBio's period fields are free text ("Devonian (late Emsian)", "Lower Devonian",
"dévonien"), so a full-text term was the practical route; (2) the other kingdom labels (fungi, protozoa, chromista,
*incertae sedis*, taxon-indet., microfossils/palynology ...) and records with no kingdom but a name, for Devonian,
Silurian and Ordovician; (3) every searched genus by `scientificname` (no name had more than 6,000 hits).
37,870 unique records, 353 MB. iDigBio's own copy of each name is lower-case and re-matched to the GBIF
backbone; `taxon_recorded` is the provider's `dwc:scientificName`, `taxon_interpreted` iDigBio's `scientificName`, `taxon_accepted` its
`canonicalname`. Media UUIDs are in the records; the media records were fetched one by one for the URLs
(`/view/mediarecords/{uuid}`, `accessuri`). `idigbio_recordsets.csv` lists the recordsets and the rights each states.

### ALA and GBIF Australia (EPRP mirror, read-only)

`deep-server:/data/paleodata/gbif-ala-fossils/gbif/raw/2026-10-22T1013Z_url/`, backed up at
`nectar:/data/codex/artifacts/eprp-paleodata-backup/latest/gbif-ala-fossils/gbif/raw/2026-10-22T1013Z_url/` (catalogue entry
`eprp/resources/sources/gbif-ala-fossils/README.md`): GBIF `FOSSIL_SPECIMEN` records for country AU and PG, harvested
2026-10-22, Neptune excluded, 42,782 records. These are GBIF records, so ALA's own copies add none (the catalogue entry
says ALA re-serves GBIF's NHM, UCMP, MCZ and ANWC records); ALA's live API was not queried. The same window and
classification filters give `ala_specimens.csv`. 273 of the 274 ALA rows have a live GBIF row (matched by `gbifID`).
**Museums Victoria is not in the mirror** (no dataset of that publisher) and has no `FOSSIL_SPECIMEN` record in live GBIF either (observed:
`institutionCode=NMV` has 1,075,894 records, none of them fossil specimens; `q=Baragwanathia` returns 70 fossil
specimens, from NRM 30, NHMUK 16, KU 6, NSM 4, UOMNH 3, MfN 2, UCMP 2, UF 2 and a few others, and 18 PBDB material citations).
The Victorian material (*Baragwanathia*, *Hedeia*, *Yarravia*, Yea Formation, Jordan River Beds) is held abroad.
Of the mirror's 42,782 records, 274 are kept (262 in the window, 12 undated name matches); 27,598 are dated outside the window, 12,762 have no age field and match no scope name, and 2,060 are excluded by taxon (mostly animals). The kept rows come from NHMUK 122, FMNH 55, NRM 42, UOMNH 33, KU 6, NSM 4, UF 3, UMMP 3, MfN 2 and one each from CMC, UCMP, UiO and MNHN, and 101 are from Victoria: *Baragwanathia longifolia* 54, *Hedeia* 17, *Zosterophyllum* 8, *Yarravia* 3, from the Jordan River Beds (9 rows), Yea Formation (5) and Wilson Creek Shale (3) and, for 83 rows, no formation. Australian plant records that give a formation but no age (for example Oregon's *Baragwanathia* from the Yea Formation) are kept only when a scope name matches; the 12,762 undated records that match no scope name are counted in the build statistics only.

## 4. Age logic (`derived_age_*`, `derived_window_status`)

GBIF's age fields are mostly names from its geological-time vocabulary (`LowerDevonian`, `Emsian`); iDigBio's are the
provider's free text. Both give ICS names as entered, never numbers. `derived_age_max_ma` and `derived_age_min_ma` are
the bases and tops of the named intervals in `data/timescale.csv` (ICS v2024/12; tops are the next younger stage's
base; a few non-window names use approximate ICS values, flagged in the script):
- the narrowest interval among the stage, epoch and period fields gives each bound; a coarser latest field never
  widens a finer earliest one; free text is parsed for period, epoch, stage and a few regional names (Gedinnian,
  Siegenian, Niagaran, Cincinnatian ... mapped to ICS intervals by the analyst, flagged
  `regional_term_mapped_by_analyst`);
- `in_window`: the age range overlaps 485–383 Ma (PBDB's rule); `derived_fully_inside_window` says whether it lies
  wholly inside and `derived_age_span_myr` gives the width (a record of "Devonian" alone spans 60.8 Myr);
- `anchor_late_devonian`: an anchor genus whose range overlaps 383–358.86 Ma;
- records with no age field are kept only if a card taxon, anchor, nematophyte or charophyte name matches
  (`undated_scope_name`; `coarse_age_scope_name` for Paleozoic-only), not for extant or planned cards;
  stratigraphic text fields (formation, group, member, bed, lithostratigraphic terms) are read for window names
  (`derived_age_basis = text:stratigraphic_fields`);
- records dated wholly outside the window are dropped.

## 5. Result

Records retrieved: 34,133 GBIF (unique `gbifID`), 37,870 iDigBio (unique uuid), 42,782 read from the ALA mirror. Rows kept:

| | GBIF | iDigBio | ALA mirror |
|---|---:|---:|---:|
| rows kept | 24,756 | 19,843 | 274 |
| core | 13,431 | 10,453 | 194 |
| flagged | 11,325 | 9,390 | 80 |
| dropped: outside window | 5,169 | 5,154 | 27,598 |
| dropped: undated | 1,688 | 658 | 12,762 |
| dropped: coarse age only | 8 | 0 | 88 |
| dropped: taxon excluded (in window by age) | 2,512 | 12,215 | 2,060 |

Window status of the kept rows:

| `derived_window_status` | GBIF | iDigBio | ALA mirror |
|---|---:|---:|---:|
| `in_window` | 20,533 | 16,283 | 262 |
| `anchor_late_devonian` | 1,642 | 1,108 | 0 |
| `undated_scope_name` | 2,525 | 2,452 | 12 |
| `coarse_age_scope_name` | 56 | 0 | 0 |

Subsets of the kept rows (class core or flagged; the excluded names are in the audit):

| `derived_subset` | Class | GBIF rows | iDigBio rows | ALA-mirror rows |
|---|---|---:|---:|---:|
| `embryophyta` | core | 11,539 | 8,200 | 187 |
| `nematophytes_and_thalloid_problematica` | core | 1,173 | 1,515 | 7 |
| `plant_spore_form_genus` | core | 271 | 304 | 0 |
| `scope_named_taxon` | core | 226 | 213 | 0 |
| `charophytes` | core | 167 | 173 | 0 |
| `scope_named_fungi_or_lichens` | core | 55 | 48 | 0 |
| `green_algae` | flagged | 5,378 | 4,543 | 59 |
| `plantae_unplaced_indeterminate` | flagged | 3,713 | 3,428 | 15 |
| `problematica_ichnofossils_or_algae` | flagged | 738 | 450 | 4 |
| `plantae_unplaced_named` | flagged | 459 | 266 | 0 |
| `acritarchs_prasinophytes` | flagged | 382 | 211 | 0 |
| `fungi_other` | flagged | 178 | 221 | 0 |
| `embryophyta_lineage_implausible_for_age` | flagged | 282 | 94 | 1 |
| `incertae_sedis_kingdom` | flagged | 93 | 43 | 1 |
| `algae_unspecified` | flagged | 44 | 75 | 0 |
| `scope_name_filed_under_animalia` | flagged | 9 | 34 | 0 |
| `red_algae` | flagged | 31 | 9 | 0 |
| `scope_name_filed_under_protists` | flagged | 18 | 16 | 0 |

Excluded by taxon, GBIF (in window by age): 1,167 animal_name_filed_under_plant_or_fungus_lineage, 534 protozoa_chromista, 471 animal, 206 bacteria_cyanobacteria, 134 no_lineage_no_plant_evidence.
Excluded by taxon, iDigBio (in window by age): 8,986 no_lineage_no_plant_evidence, 1,581 animal, 553 ichnofossil, 487 other_lineage, 168 animal_name_filed_under_plant_or_fungus_lineage, 166 animal_or_trace_fossil_name, 161 bacteria_cyanobacteria, 113 protozoa_chromista.

Institutions holding most kept rows, GBIF: (none) 182, AMNH 53, CM 18, CMC 381, Department of Geology, TalTech 29, FMNH 4,141, KU 4,059, MNHN 122, MPM 40, MfN 128, Milwaukee Public Museum (MPM) 50, NHMUK 5,356. iDigBio: (none) 21, AMNH 53, CM 20, CMC 248, FMNH 4,134, KU 3,795, MCZ 1, MNHN 41, MUGM 11, NCSM 4, NHMUK 5,100, NMMNHS 17. ALA mirror: CMC 1, FMNH 55, KU 6, MNHN 1, MfN 2, NHMUK 122, NRM 42, NSM 4, UCMP 1, UF 3, UMMP 3, UOMNH 33.

## 6. Deduplication

Matching rules, applied across all kept rows with union-find (a row can be linked by more than one rule):

1. `gbifID`: the ALA-mirror rows are GBIF records, so a mirror row and a live GBIF row with the same `gbifID` are the same record.
2. `occurrenceID` (trimmed, lower-case, at least 8 characters) equal across sources.
3. Normalised `institutionCode` + `catalogNumber` (alphanumerics only, lower-case) equal; within one source this also links several rows with one catalogue number (for example successive determinations of one RBINS specimen).
4. GBIF datasets that are iDigBio-sourced: none found. Observed: none of the 64 GBIF datasets behind the kept rows has an iDigBio endpoint (all are institutional IPT or BioCASE feeds), so this rule matched nothing; specimens that both sources hold are linked by rules 2 and 3. `gbif_datasets.csv` carries `idigbio_sourced` and `n_gbif_rows_also_in_idigbio` for each dataset.

Result (observed): **26,102 physical specimens** for 44,873 rows in `specimens_merged_all.csv` (39,417 in the open `specimens_merged.csv`). By the sources that hold each specimen: 17,828 gbif+idigbio, 6,570 gbif, 1,430 idigbio, 146 gbif+ala_mirror+idigbio, 127 gbif+ala_mirror, 32 (rows sharing a catalogue key inside one source: idigbio), 1 ala_mirror.

Cross-source specimens by the rules that link them: 17,628 inst_catalog+occurrenceID, 271 gbifID+inst_catalog+occurrenceID, 200 occurrenceID, 2 gbifID+inst_catalog. By the strongest rule (order `gbifID`, `occurrenceID`, `inst_catalog`): 17,828 occurrenceID, 273 gbifID.

Rows sharing a catalogue key inside one source (not cross-source): 32 idigbio|inst_catalog.

Both rows are kept for every duplicate: `derived_dedupe_key` is shared, `derived_duplicate_of` on the non-primary rows names the primary (`source:record_id`; primary order GBIF, ALA mirror, iDigBio), `derived_dedupe_rule` lists the rules that linked the group, and `derived_in_gbif`, `derived_in_ala_mirror`, `derived_in_idigbio` and `derived_n_rows_for_specimen` are repeated on each row. The per-source tables keep every raw row once.

Institutions in both live sources where many specimens are linked in neither direction are the likely residual duplicates (`dedupe_by_institution.csv`; top institutions below, counts of physical specimens by the sources that hold them):

| institutionCode | specimens | ala | gbif | gbif_and_ala | gbif_and_ala_and_idigbio | gbif_and_idigbio | idigbio |
|---|---:|---:|---:|---:|---:|---:|---:|
| NHMUK | 5,391 | 0 | 227 | 64 | 58 | 5,007 | 35 |
| KU | 5,054 | 0 | 1,259 | 0 | 6 | 2,794 | 995 |
| FMNH | 4,142 | 0 | 8 | 0 | 55 | 4,078 | 1 |
| NRM | 2,685 | 0 | 2,287 | 42 | 0 | 356 | 0 |
| UCMP | 2,323 | 0 | 139 | 0 | 1 | 2,159 | 24 |
| YPM | 1,643 | 0 | 344 | 0 | 0 | 1,133 | 166 |
| RBINS-Scientific Heritage | 1,445 | 0 | 0 | 0 | 0 | 1,350 | 95 |
| UiO | 1,048 | 1 | 1,047 | 0 | 0 | 0 | 0 |
| CMC | 387 | 0 | 139 | 0 | 1 | 241 | 6 |
| UOMNH | 347 | 0 | 48 | 11 | 22 | 257 | 9 |
| USNM | 244 | 0 | 1 | 0 | 0 | 240 | 3 |
| (none) | 187 | 0 | 166 | 0 | 0 | 16 | 5 |

## 7. Licences

Per-record licence is kept in `license`, `rightsHolder` and `accessRights`, classed in `derived_licence_class` (CC0, CC-BY, CC-BY-NC, other, none). For iDigBio rows with no record licence, `derived_licence_class_recordset` classes the rights the row's recordset states. `derived_licence_effective` is the record's class where it is open, else the recordset's, and `derived_licence_effective_source` says which; `derived_nc_flag` marks CC BY-NC rows on that basis.

| Rows by effective licence | CC0 | CC-BY | CC-BY-NC | unclear |
|---|---:|---:|---:|---:|
| GBIF | 11,875 | 10,720 | 2,161 | 0 |
| ALA mirror | 210 | 57 | 7 | 0 |
| iDigBio | 6,103 | 6,037 | 2,247 | 5,456 |

- **GBIF and the ALA mirror**: every row is CC0, CC BY or CC BY-NC, so both tables are in `specimens/`, NC rows flagged. Dataset licences, DOIs and record counts for citation are in `gbif_datasets.csv`. No GBIF derived dataset was registered (outward-facing).
- **iDigBio**: 5,456 of the 19,843 kept rows (the NHMUK recordset 5,100 and the NRM palaeozoology recordset 356) state no licence, and iDigBio records those two recordsets' rights as 'Unknown License, assume Public Domain', which is its default, not a licence. A further 3,192 rows have no record licence but sit in recordsets that state CC0, CC BY or CC BY-NC (UCMP, USNM, Condon, CMC, UF ...); 11,195 rows carry an open licence themselves (FMNH, KU, RBINS, YPM ...). Most NHMUK specimens are also in GBIF with an explicit CC0 or CC BY record licence, so the clear rights attach to the GBIF row. Rights are therefore unclear for the table as a whole, so the full table is `local/specimens/idigbio_specimens.csv` (git-ignored), and `idigbio_specimens_open_licence.csv` holds the rows whose record or recordset states CC0, CC BY or CC BY-NC.
- **Merged table**: `specimens_merged.csv` holds the open-licence rows of all sources; `local/specimens/specimens_merged_all.csv` adds the iDigBio rows with unclear rights. Group columns (`derived_n_rows_for_specimen`, `derived_in_*`) count all rows, but every `derived_duplicate_of` in the open file points at a row that is in it (checked).
- CC BY and CC BY-NC require attribution; cite GBIF.org with the query and date and the dataset DOIs of the rows used (`gbif_datasets.csv`), and the iDigBio provider (`idigbio_recordsets.csv`, `rightsHolder`).

## 8. Card taxa and anchors

**Card taxa (species and genus cards, with name variants below them)**

| Name | GBIF rows | iDigBio rows | ALA rows | Physical specimens | In window | Undated name matches | Institutions (specimens) |
|---|---:|---:|---:|---:|---:|---:|---|
| Aberlemnia caledonica | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Aglaophyton majus | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Ambitisporites | 30 | 22 | 0 | 30 | 30 | 0 | NHMUK:22; NRM:5; UiO:3 |
| Anthoceros | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Archaeopteris | 883 | 436 | 2 | 886 | 270 | 246 | NRM:284; NHMUK:127; YPM:122; KU:95; UiO:92 |
| Asteroxylon mackiei | 90 | 65 | 0 | 90 | 81 | 9 | NHMUK:26; KU:25; NRM:13; UCMP:12; (none):5 |
| Baragwanathia brevifolioides | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Baragwanathia longifolia | 61 | 23 | 57 | 61 | 53 | 8 | NRM:30; NHMUK:16; NSM:3; UOMNH:3; MfN:2 |
| Chara | 8 | 8 | 0 | 8 | 8 | 0 | NHMUK:4; CMC:2; (none):1; YPM:1 |
| Coleochaete | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Cooksonia | 183 | 166 | 0 | 184 | 172 | 12 | YPM:84; NHMUK:79; MfN:8; (none):3; NRM:3 |
| Dawsonites | 166 | 107 | 0 | 166 | 66 | 100 | RBINS-Scientific Heritage:51; (none):35; NHMUK:34; NRM:20; UiO:10 |
| Drepanophycus spinaeformis | 421 | 340 | 2 | 421 | 92 | 329 | RBINS-Scientific Heritage:278; NHMUK:44; NRM:32; (none):19; SMF:14 |
| Eophyllophyton bellum | 1 | 0 | 0 | 1 | 1 | 0 | NRM:1 |
| Franhueberia gerriennei | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Hedeia | 20 | 10 | 17 | 20 | 20 | 0 | NRM:10; NHMUK:6; UOMNH:3; KU:1 |
| Horneophyton lignieri | 45 | 18 | 0 | 45 | 37 | 8 | NRM:19; NHMUK:13; CMN:4; (none):4; UCMP:4 |
| Leclercqia | 42 | 40 | 0 | 42 | 39 | 3 | UCMP:15; USNM:15; YPM:9; KU:1; SSSM:1 |
| Marchantia polymorpha | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Metzgeriothallus sharonae | 662 | 662 | 0 | 662 | 662 | 0 | UCMP:662 |
| Nematothallus | 119 | 118 | 0 | 119 | 119 | 0 | NHMUK:103; UOMNH:14; NRM:1; YPM:1 |
| Nothia aphylla | 3 | 0 | 0 | 3 | 3 | 0 | NRM:3 |
| Palaeostigma | 3 | 2 | 0 | 3 | 3 | 0 | CMC:2; UOMNH:1 |
| Parka decipiens | 204 | 176 | 1 | 204 | 201 | 3 | NHMUK:162; NRM:25; YPM:6; FMNH:4; UOMNH:3 |
| Partitatheca | 2 | 1 | 0 | 2 | 2 | 0 | NHMUK:2 |
| Pertica | 78 | 44 | 0 | 79 | 55 | 24 | YPM:43; UF:11; NRM:9; KU:4; USNM:4 |
| Phlegmariurus squarrosus | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Pluricaulis biformis (manuscript name) | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Prototaxites | 210 | 431 | 4 | 513 | 159 | 354 | RBINS-Scientific Heritage:301; NHMUK:96; Department of Geology, TalTech:28; NRM:25; UOMNH:15 |
| Psilophyton | 2004 | 1492 | 0 | 1986 | 1002 | 984 | RBINS-Scientific Heritage:651; NHMUK:373; NRM:304; KU:175; YPM:133 |
| Psilotum nudum | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Renalia hueberi | 46 | 35 | 0 | 46 | 42 | 4 | YPM:17; UCMP:11; NHMUK:7; KU:5; UF:3 |
| Rhynia gwynne-vaughanii | 71 | 57 | 0 | 71 | 70 | 1 | UCMP:36; NRM:13; KU:12; NHMUK:8; FMNH:1 |
| Riccardiothallus devonicus | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Salopella | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Sawdonia ornata | 105 | 69 | 0 | 116 | 110 | 6 | NRM:41; YPM:25; KU:16; UF:7; NHMUK:6 |
| Tmesipteris | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Tortotubus protuberans | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Ulothrix | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Ulva | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Wattieza | 31 | 25 | 0 | 31 | 12 | 4 | UOMNH:20; NRM:6; UCMP:5 |
| Winfrenatia reticulata | 45 | 45 | 0 | 45 | 45 | 0 | KU:45 |
| Yarravia | 4 | 3 | 3 | 4 | 3 | 1 | NHMUK:3; KU:1 |
| Zosterophyllum | 292 | 207 | 8 | 291 | 222 | 69 | NHMUK:158; NRM:28; MfN:20; RBINS-Scientific Heritage:15; (none):14 |

**Members of assemblage and morphogroup cards**

| Name | GBIF rows | iDigBio rows | ALA rows | Physical specimens | In window | Undated name matches | Institutions (specimens) |
|---|---:|---:|---:|---:|---:|---:|---|
| Palaeoglomus | 9 | 2 | 0 | 9 | 9 | 0 | UOMNH:7; UCMP:2 |
| Paleoglomus | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Glomites | 1 | 1 | 0 | 1 | 1 | 0 | KU:1 |
| Archaeosporites | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Palaeoendogone | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Rugososporomyces | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Tetrahedraletes | 25 | 25 | 0 | 27 | 27 | 0 | NHMUK:25; NRM:2 |
| Cryptospora | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Dyadospora | 33 | 26 | 0 | 33 | 33 | 0 | NHMUK:26; NRM:7 |
| Pseudodyadospora | 16 | 14 | 0 | 16 | 16 | 0 | NHMUK:14; NRM:2 |
| Hispanaediscus | 20 | 16 | 0 | 20 | 20 | 0 | NHMUK:16; NRM:2; UOMNH:2 |
| Laevolancis | 27 | 26 | 0 | 28 | 28 | 0 | NHMUK:26; NRM:2 |
| Rimosotetras | 8 | 8 | 0 | 8 | 8 | 0 | NHMUK:8 |
| Segestrespora | 21 | 21 | 0 | 21 | 21 | 0 | NHMUK:21 |
| Artemopyra | 15 | 13 | 0 | 15 | 15 | 0 | NHMUK:13; NRM:2 |
| Cheilotetras | 8 | 7 | 0 | 8 | 8 | 0 | NHMUK:7; NRM:1 |
| Velatitetras | 13 | 13 | 0 | 13 | 13 | 0 | NHMUK:13 |
| Cymbohilates | 23 | 17 | 0 | 23 | 23 | 0 | NHMUK:17; NRM:6 |
| Abditodyadus | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Tetraplanarisporites | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Lyonophyton | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Langiophyton | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Kidstonophyton | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Remyophyton | 0 | 0 | 0 | 0 | 0 | 0 |  |

**Anchor genera (Frasnian-Famennian records counted separately)**

| Name | GBIF rows | iDigBio rows | ALA rows | Physical specimens | In window | Undated name matches | Institutions (specimens) |
|---|---:|---:|---:|---:|---:|---:|---|
| Archaeopteris | 883 | 436 | 2 | 886 | 270 + 370 late Dev. | 246 | NRM:284; NHMUK:127; YPM:122; KU:95; UiO:92 |
| Callixylon | 265 | 205 | 1 | 268 | 175 + 50 late Dev. | 43 | KU:91; NHMUK:60; NRM:38; YPM:22; SMF:12 |
| Eospermatopteris | 20 | 20 | 0 | 20 | 18 + 0 late Dev. | 2 | YPM:15; NHMUK:3; CMC:1; USNM:1 |
| Wattieza | 31 | 25 | 0 | 31 | 12 + 15 late Dev. | 4 | UOMNH:20; NRM:6; UCMP:5 |
| Elkinsia | 1212 | 846 | 0 | 2054 | 3 + 2051 late Dev. | 0 | KU:2050; UOMNH:2; FMNH:1; USNM:1 |
| Leclercqia | 42 | 40 | 0 | 42 | 39 + 0 late Dev. | 3 | UCMP:15; USNM:15; YPM:9; KU:1; SSSM:1 |

**Nematophytes and thalloid problematica**

| Name | GBIF rows | iDigBio rows | ALA rows | Physical specimens | In window | Undated name matches | Institutions (specimens) |
|---|---:|---:|---:|---:|---:|---:|---|
| Prototaxites | 210 | 431 | 4 | 513 | 159 | 354 | RBINS-Scientific Heritage:301; NHMUK:96; Department of Geology, TalTech:28; NRM:25; UOMNH:15 |
| Nematothallus | 119 | 118 | 0 | 119 | 119 | 0 | NHMUK:103; UOMNH:14; NRM:1; YPM:1 |
| Nematophyton | 101 | 69 | 0 | 101 | 95 | 6 | NHMUK:70; NRM:20; KU:3; OMNH:2; CMC:1 |
| Pachytheca | 524 | 970 | 0 | 638 | 188 | 450 | RBINS-Scientific Heritage:424; NHMUK:185; KU:13; SMF:3; USNM:3 |
| Nematasketum | 5 | 10 | 0 | 10 | 10 | 0 | NHMUK:10 |
| Nematoplexus | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Nematophycus | 3 | 4 | 0 | 4 | 4 | 0 | NHMUK:4 |
| Parka | 243 | 216 | 3 | 243 | 240 | 3 | NHMUK:195; NRM:25; UOMNH:9; YPM:6; FMNH:4 |
| Cosmochlaina | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Prototaxites taiti | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Prototaxites loganii | 14 | 1 | 0 | 14 | 10 | 4 | NRM:9; OMNH:2; CMN:1; SMF:1; UOMNH:1 |
| Prototaxites southworthii | 4 | 4 | 0 | 5 | 4 | 1 | KU:3; NHMUK:1; USNM:1 |
| Nematothallus williamii | 0 | 0 | 0 | 0 | 0 | 0 |  |

**Charophyte search names**

| Name | GBIF rows | iDigBio rows | ALA rows | Physical specimens | In window | Undated name matches | Institutions (specimens) |
|---|---:|---:|---:|---:|---:|---:|---|
| Palaeonitella | 6 | 4 | 0 | 6 | 6 | 0 | KU:3; NHMUK:2; UOMNH:1 |
| Moellerina | 41 | 41 | 0 | 41 | 2 | 39 | AMNH:38; FMNH:1; UOMNH:1; USNM:1 |
| Sycidium | 22 | 16 | 0 | 22 | 6 | 16 | AMNH:15; NRM:5; MfN:1; NHMUK:1 |
| Trochiliscus | 23 | 18 | 0 | 23 | 18 | 5 | NHMUK:10; NRM:5; USNM:4; UCMP:3; UF:1 |
| Eochara | 0 | 1 | 0 | 1 | 0 | 1 | OMNH:1 |
| Octochara | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Praechara | 10 | 10 | 0 | 10 | 0 | 10 | USNM:10 |
| Chovanella | 0 | 12 | 0 | 12 | 0 | 12 | OMNH:12 |
| Mesochara | 4 | 0 | 0 | 4 | 0 | 4 | USNM:4 |

**Name variants and synonyms named by the cards or EPRP (counted separately, never merged)**

| Name | GBIF rows | iDigBio rows | ALA rows | Physical specimens | In window | Undated name matches | Institutions (specimens) |
|---|---:|---:|---:|---:|---:|---:|---|
| Aglaophyton major | 91 | 64 | 0 | 92 | 76 | 16 | UCMP:32; NHMUK:18; NRM:18; YPM:6; CMN:4 |
| Rhynia major | 30 | 22 | 0 | 31 | 22 | 9 | NHMUK:18; CMN:4; (none):4; FMNH:3; MfN:1 |
| Baragwanathia brevifolia | 0 | 0 | 0 | 0 | 0 | 0 |  |
| Hornea lignieri | 17 | 13 | 0 | 17 | 13 | 4 | NHMUK:13; (none):4 |
| Rhynia gwynnevaughani | 106 | 34 | 0 | 106 | 105 | 1 | UCMP:40; NHMUK:34; NRM:13; KU:12; UOMNH:4 |

Zero rows means that no kept record carries the name in the genus field, the accepted or interpreted name, or the recorded name (genus level for genus cards; species level needs the epithet). Card genera are reported by their species cards' genus rows (`card_genus` role) in `card_taxa_specimens_summary.csv`, with the columns `n_rows_matched_by_recorded_name_only` and `n_rows_matched_by_interpreted_or_accepted_name_only` that show where a source's backbone changed the name; `near_name_candidates_not_merged` lists near-spellings (for example *Baragwanthia*, *Swadonia*) that were not counted.

## 9. Caveats and limits

- **Nameless and unmatched records are not in the tables.** GBIF holds 57,296 window-period fossil-specimen records that it could not match to any name (`issue=TAXON_MATCH_NONE`; earliest period Ordovician 20,808, Silurian 12,086, Devonian 24,402; observed 2026-10-27). Their search results carry no `scientificName`, so they cannot be reached by name or by taxon key. Most are lots with no name at all (the NMNH Paleobiology dataset alone has 26,874; KUBI Paleobotany 3,925 Devonian). A verbatim sample of 12 records from each of six of the largest datasets found names in 14 of 72: *Nikitinisporites canadensis* at KUBI, and 'Gen. indet.' and *Linopteris* sp. at the Sam Noble Museum. A small share of plant records is therefore missing from the GBIF side; the iDigBio side holds the *Nikitinisporites* records under a palynology kingdom label, which is how they reached `idigbio_specimens.csv`. iDigBio has about 38,400 further window-period records with neither kingdom nor name (by full-text term: 16,044 Ordovician, 5,782 Silurian, 16,594 Devonian; USNM, KU, MCZ, YPM).
- **Age resolution varies.** 5,213 GBIF rows (21 per cent) and 2,449 iDigBio rows (12 per cent) have a derived age span over 60 Myr, mostly the period 'Devonian' alone. Use `derived_age_span_myr` and `derived_fully_inside_window` before binning. 'In window' means the recorded range overlaps 485–383 Ma, not that it lies inside it. Rows with no derived age are the undated name matches.
- **Records are not linked where the sources use different identifiers.** The clearest case is KUBI Paleobotany: its GBIF dataset and its iDigBio recordset give the same lots different UUIDs and often no catalogue number (KUBI's 2,050 *Elkinsia* specimens are 1,208 GBIF rows and 842 iDigBio rows that share no identifier), so 1,259 KU specimens are GBIF-only and 995 iDigBio-only in `dedupe_by_institution.csv`, and many are probably the same lots counted twice. UCMP (139 GBIF-only), YPM (344 and 166) and NRM (2,287 GBIF-only, since NRM publishes only to GBIF) show the same pattern at smaller scale. No fuzzy rule was applied: lots from one locality are indistinguishable by the fields both sources share.
- **Names.** GBIF's search results omit the recorded name, so the verbatim record was fetched for every retained row that GBIF matched only approximately. For 14,950 rows with a verbatim record, the recorded genus differs from GBIF's interpreted genus in 1,130: GBIF fell back to a family (417), phylum (256), kingdom (210) or class (122), or changed the spelling (*Swadonia ornata* for *Sawdonia ornata*, *Psylophyton* for *Psilophyton*) . `taxon_recorded_basis` says where each `taxon_recorded` comes from; 1,804 rows (1,771 of them NRM) have a verbatim genus but no scientific name, so the recorded name is the genus and epithet fields and the empty higher ranks are filled from the verbatim record (`taxon_issue_flags` lists VERBATIM_* fields used). Misspellings in the sources are kept as recorded (*Baragwanthia*, *Chauleria*, *Mosellophtyon*) and listed as near names in the card summary, not merged.
- **Classification rests on lineage and name, not on examination of specimens.** The curated name lists in `specimens_build.py` (animal genera filed under plant homonyms, problematica, calcimicrobes, acritarch stems, spore form endings) are the analyst's judgement and are visible in `specimen_filter_names.csv`. Backbone homonyms matter: *Orthoceras annulata* (a cephalopod) sits under Tracheophyta, *Tetradium* (a coral) under Rutaceae, *Vertebrata* (the vertebrates) under red algae, *Dictyonema* (a graptolite) under Basidiomycota. Receptaculitids (*Receptaculites*, *Calathium*, *Ischadites*, *Pasceolus*) are green algae to FMNH and GBIF and sponges or animals to other providers' lineages, so the same genus can be flagged in one source and excluded in the other.
- **Ordovician 'Plantae'.** GBIF's 4,871 Ordovician Plantae records (the earliest-period field) give 4,859 kept rows: 4,492 green algae (receptaculitids and dasyclads; FMNH alone holds 3,723), 155 problematica and trace fossils, 65 acritarchs, 31 seed-plant or vascular lineages that cannot be right for the age (*Orthoceras*, *Tetradium*, *Lloydia* ...), 58 Plantae-only determinations, 39 cryptospore genera named by the cards, 8 other spore genera, 11 other algae. None of these 4,871 has an unflagged embryophyte lineage; the plant evidence is the 47 dispersed spores. A further 55 kept GBIF rows from the University of Oregon museum (UOMNH: 'Bryophyta', *Thallites*, *Naiadita*, *Akdalophyton*, *Hispanaediscus* and others) carry a bryophyte lineage and an Ordovician-only age taken from their latest-age fields; they are core by lineage, and their identity and dating need checking.
- **Snapshot.** GBIF and iDigBio are live; the counts are those of 2026-10-27. The mirror is 2026-10-22. One mirror row (UiO A35187, *Pycnoidocyathus*, an archaeocyathan, flagged `incertae_sedis_kingdom`) has no live GBIF row in the harvest; its record may have changed since.
- **Undated name matches.** `undated_scope_name` rows (2,525 GBIF, 2,452 iDigBio, 12 ALA mirror) are all records of a card, anchor, nematophyte or charophyte genus with no usable age field, at any age; many are *Prototaxites*, *Pachytheca*, *Psilophyton* and *Drepanophycus* from RBINS and NHMUK. They are candidates, not window records.
- **Free text.** 882 GBIF rows reached the table only through free-text `q` queries and are in the window through a stratigraphic text field; iDigBio's full-text terms also match place names (*Ludlow*, Shropshire and elsewhere), which the age logic discards.
- **Access limits.** GBIF's asynchronous download API needs an account, so paged search was used (offset limit 100,000; pages beyond an offset of about 10,000 are slow; search results omit verbatim names, hence 16,507 verbatim lookups). GBIF citation therefore rests on dataset DOIs, not a download DOI. iDigBio's `search/media` endpoint rejected record-UUID queries, so media records were fetched one at a time; its `rq` has no negation, so full-text terms returned overlapping sets. ALA's live API was not queried (brief: mirror only).
- **Size and time.** GBIF: 810 MB of search pages (688 MB structured pass in 23 min with 3 workers; 122 MB names pass in 7 min with 2), plus 79 MB of verbatim records (22,369 requests for 16,507 distinct records, because a second worker pool ran the list in reverse to save time and the two overlapped) and 1.4 MB of dataset records. iDigBio: 353 MB of pages in 7 min and 86 MB of media records (15,046). Together about 1.3 GB, over the 1 GB guideline for the two pulls combined and under it for each; the verbatim and media lookups took 36 minutes. Raw pages stay on deep-server.

## 10. Not done

- No GBIF download or derived dataset (needs an account; outward-facing).
- No live ALA query, no media download, no georeferencing, no re-identification, and no synonym merging: spelling variants and synonyms are separate name rows and near-spellings are listed, not counted.
- No record outside `FOSSIL_SPECIMEN` basis (PBDB's GBIF dataset is `MATERIAL_CITATION`, so it does not duplicate these rows; 18 PBDB citations of *Baragwanathia* are not specimens). `PRESERVED_SPECIMEN` fossils were not searched.
- No Frasnian–Famennian records for non-anchor genera; no cross-match to PBDB occurrences or to the project's cards beyond names.
- No collector or determiner names in the tables (they remain in the raw pages on deep-server).
- No age was converted to numbers except in the `derived_` columns, and no source value was corrected.
- Not run: a second independent check of the classification lists by another agent.

## 11. Reproduce

```bash
# 1. names (local): reads taxa/*.md
python3 data/external/scripts/specimens_scope.py > data/external/scripts/specimens_scope_names.csv
# 2. harvest (on nectar; scp the two files or ssh nectar python3 - ARGS < script)
python3 specimens_harvest.py gbif   /data/codex/silurian_plants/raw specimens_scope_names.csv --workers 3
python3 specimens_harvest.py idigbio /data/codex/silurian_plants/raw specimens_scope_names.csv
python3 specimens_harvest.py gbif-datasets <gbif harvest dir>
python3 specimens_harvest.py idigbio-recordsets <idigbio harvest dir>
# 3. which rows need a verbatim record or media record, then fetch them
python3 specimens_build.py --gbif <dirs> --idigbio <dirs> --ala <mirror dir> --scope specimens_scope_names.csv \
    --timescale data/timescale.csv --out build --emit-lists lists
python3 specimens_harvest.py gbif-verbatim <gbif dir> lists_gbif_verbatim_keys.txt --workers 10
python3 specimens_harvest.py idigbio-media <idigbio dir> lists_idigbio_media_uuids.txt --workers 8
# 4. build the tables, then the manifest
python3 specimens_build.py --gbif <dirs> --idigbio <dirs> --ala <mirror dir> --scope specimens_scope_names.csv \
    --timescale data/timescale.csv --out build
python3 specimens_manifest.py data/external <gbif stamps> <idigbio stamp>
```

The GBIF run used `--workers 3` for the main structured pass (`20261027T005837Z`, stopped by hand after its
structured queries finished because the name queries were already running in a second process, `--only names`,
`20261027T011309Z`; a third small run, `20261027T012054Z`, added the genera of cards written during the work:
*Anthoceros* and *Phlegmariurus*).
