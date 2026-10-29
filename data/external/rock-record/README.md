# rock-record/: British Silurian–Devonian rock record (BGS)

Bedrock area by age for Great Britain and Northern Ireland, from the open BGS DiGMapGB-625 polygons, with the BGS Lexicon
of Named Rock Units entries for their units. It is a sampling proxy for the Avalonian core of the Silurian–Devonian plant
record, in the spirit of Dunhill et al. (2014, *Nature Communications* 5:4818, doi:10.1038/ncomms5818; DOI checked against
Crossref). Extracted 2026-10-27 by a Claude Sonnet 5.5 subagent (`claude-sonnet-5-5`), read-only, from open web services; the
raw pulls are on `deep-server` in `/data/codex/silurian_plants/raw/bgs/2026-10-27T0128Z/` (200 MB; not reachable from the Macs, so a rebuild re-pulls on `nectar`). Scripts:
`../scripts/rockrecord_*.py`. Paths below are relative to `data/external/`.

**What Dunhill et al. used, and what this is not.** Their Methods (as shown on PubMed Central; the Supplementary Methods
were not read) measure outcrop area from BGS digital bedrock geology named "DiGMapGB-50" (1:50 000), assess sampling proxies at
epoch level, and treat marine and terrestrial outcrop separately. DiGMapGB-50 is not openly licensed (§6), so this
extraction uses DiGMapGB-625, which BGS says was made by generalising 1:50 000 data (the 2007 fifth-edition bedrock map).
Areas will differ from a 1:50 000 calculation (inference: generalisation merges small units; not tested). No marine/terrestrial
split is provided (§5).

## 1. Files

| File | Rows | Contents |
| --- | ---: | --- |
| `rock-record/bgs_units_silurian_devonian.csv` | 59 | One row per BGS LEX code: the 36 codes of the Silurian–Devonian polygons, the 21 Old Red Sandstone (ORS) Supergroup descendants in the Lexicon that have no such polygons, and 2 ancestors. Area, BGS polygon age terms and years, Lexicon status, rank, parent, ages (Ma), lithology classes, definition sentence and reference list, `derived_` ORS flags and environment keywords |
| `rock-record/bgs_outcrop_area_by_age.csv` | 222 | Bedrock area (km²) by BGS period, series and stage, by region, rock group and ORS flag (§3) |
| `rock-record/bgs_polygon_age_scale_observed.csv` | 15 | BGS age terms in the polygon attributes with the year values they carry, and their offsets from `data/timescale.csv` (§2) |
| `rock-record/bgs_geochronology_divisions_used.csv` | 42 | BGS Geochronology Division records (Ma) behind the Lexicon ages, with offsets from `data/timescale.csv` |
| `rock-record/bgs_provenance_digmapgb625.tsv`, `rock-record/bgs_provenance_lexicon.tsv` | 8, 236 | URL, UTC timestamp, licence, bytes and sha256 of every page, record and zip pulled |
| `rock-record/MANIFEST.tsv` | | Delivered files with source, version, licence, script, rows, sha256 |
| `local/rock-record/bgs_625k_bedrock_silurian_devonian.gpkg` | 2,634 | **Local only (vector).** The Silurian–Devonian polygons with all source attributes, EPSG:27700 |
| `local/rock-record/bgs_polygons_silurian_devonian.csv` | 2,634 | **Local only.** Their attribute table without geometry, plus area, centroid and `derived_` region, rock group, ORS evidence and age-bin shares |
| `local/rock-record/bgs_625k_bedrock_all_polygons_attributes.csv` | 11,244 | **Local only.** Attributes, area and centroid of every bedrock polygon (totals and checks) |
| `local/rock-record/bgs_lexicon_entries_sd.csv` | 60 | **Local only.** Full Lexicon entries including the prose fields (§6) |

Column prefixes in the units table: `digmap625_` from the polygon attributes (aggregated over the unit's polygons), `lexicon_`
from the Lexicon, `derived_` computed here. No source age is converted or repaired.

## 2. Sources, versions, licences and time scales

**DiGMapGB-625 (BGS Geology 625k), bedrock polygons.** Product version 5.17, released 11 February 2008 (`VERSION`, `RELEASED`), nominal
scale 1:625 000, 11,244 polygons covering UK onshore bedrock "at surface/rock head" (shapefile metadata): bedrock beneath superficial
deposits is shown, so the area is bedrock area at rockhead, not strictly outcrop. Downloaded from the BGS dataset page
(`https://www.bgs.ac.uk/datasets/bgs-geology-625k-digmapgb/`): the Shapefile zip (page dated 06/10/2025; page size 16.49 MB, file 16.0 MB) and the GeoPackage zip
(page dated 05/12/2024; page size 15.91 MB, file 16.7 MB, so the page figure is stale or rounded differently). They hold the same polygons: 11,244 each, and per-unit area sums agree to 1 m² (checked). Total area
244,870.9 km² (planar, EPSG:27700; the shapefile `.prj` carries no EPSG code, so 27700 was assigned). The bedrock theme only: dykes (3,263
polygons), superficial deposits and faults were not used.

**Licence (decision).** BGS states open availability "under the Open Government Licence" with acknowledgement. Its licence page links
OGL v3 and asks for "Contains British Geological Survey materials © UKRI [year]"; the NERC catalogue record asks for "Contains NERC
materials ©NERC [year]"; the shapefile metadata says "Copyright NERC 2008". The DOI landing page (10.5285/d9c6923b-a339-48f7-b1cf-5c9bbb664ef5)
links OGL v2. I treat the polygon-derived tables as OGL with acknowledgement and tracked them. The acknowledgement year is not fixed by BGS.

**BGS Lexicon of Named Rock Units.** Per-code linked-data records (`https://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/<code>.json`) and web
pages (`https://webapps.bgs.ac.uk/lexicon/lexicon.cfm?pub=<code>`), no login; 60 entries (the 36 polygon codes, `ORS` and its 30 child
units, and ancestors), plus the linked-data labels of the rank and lithology codes they use (65 lithology classes). The Lexicon offers no bulk download on the pages read, and its `SourceInfo` and `TypeLocality` records do not
dereference (404), so `lexicon_source_info_ids` are bare ids and the usable source text is the entry's reference list from the web page.
**No licence statement was found** on the Lexicon pages, the linked-data scheme (title "BGS Lexicon of Named Rock Units [Linked Open Data]") or
BGS's Lexicon page, which says only that access is free and "as seen". Decision: the tracked units table keeps structured fields, BGS's
one-sentence `definition` and the bibliographic references (facts and citations); the prose fields (lithology description, boundary
definitions, thickness, distribution, previous names) are in `local/rock-record/bgs_lexicon_entries_sd.csv`. If BGS or Barry confirms
OGL for the Lexicon, that file can move to the tracked area.

**Time scales (three, all BGS's or ours; none converted).**
1. *Polygon age fields* (`MAX_TIME_D`/`MIN_TIME_D` terms, `MAX_TIME_Y`/`MIN_TIME_Y` years, 2008 edition). The files and metadata I read document
   no scale. From the data (`bgs_polygon_age_scale_observed.csv`, each term has one value, asserted): Silurian 443–417 Ma, Devonian
   417–354 Ma; Llandovery 443–428, Wenlock 428–423, Ludlow 423–419, Pridoli 419–417, Early Devonian 417–391, Mid Devonian 391–370, Late Devonian
   370–354; Lochkovian 417–412, Emsian 400–391, Famennian 364–354 (the Rhuddanian base, Telychian top and Pragian top are the only values given
   for those stages). Against `data/timescale.csv` (ICS v2024/12, sha256 `396bde65de806aba…`) the term bases differ by −0.1 Myr (Silurian,
   Llandovery) to −4.9 (Wenlock), −3.7 (Ludlow, Pridoli), −2.6 (Early Devonian), −2.5 (Mid Devonian) and −12.3 (Late Devonian; the BGS Late Devonian
   begins at 370 Ma, the project's Frasnian at 382.31 Ma).
2. *Lexicon ages* (`lexicon_oldest_age_ma`, `lexicon_youngest_age_ma`): the BGS Geochronology dataset, which BGS describes as "based on The Geologic
   Time Scale 2012 … with additions"; the division definitions cite GTS2020. Silurian values equal ICS v2024/12 bases (offset 0.00; the Ordovician Period base is 486.9 against 486.85);
   Devonian values differ: Lochkovian and Pragian −0.62, Emsian −0.12, Eifelian +0.83, Givetian −2.65, Frasnian −3.41, Famennian −1.05, top of the
   Devonian 359.3 against 358.86 (`bgs_geochronology_divisions_used.csv`). BGS's Devonian values match neither GTS2012 nor ICS v2024/12 exactly; I did not
   identify their source.
3. *Project* `data/timescale.csv`, used here only to report offsets.

The two BGS scales disagree for the same unit: Lexicon oldest age minus polygon `MAX_TIME_Y` has median +3.3 Myr (range −8.1 to +10.5; the
undifferentiated Pridoli unit `PRID` has a Lexicon range, 422.7–419.0, entirely older than its polygon range, 419–417). For area by age, the
polygon fields are used, because they are attached to each polygon; the Lexicon ages are carried as unit attributes.

## 3. Selection, derived fields and the area table

**Silurian–Devonian polygons:** `MAX_TIME_Y > 354 000 000` and `MIN_TIME_Y < 443 000 000` on BGS's own polygon years, so any polygon whose age range overlaps
BGS's Silurian–Devonian: **2,634 polygons, 48,575.0 km²** (19.8% of the 244,870.9 km² total), 36 LEX codes. Many span the boundaries
(unnamed igneous intrusions "Ordovician to Silurian", "Late Silurian to Early Devonian"). By derived rock group: sedimentary 38,508 km², extrusive
igneous 2,412, intrusive igneous 7,549, metamorphic 106 (`derived_rock_group` from the polygon rock-class code `RCS`; the 24 codes present are mapped
explicitly in `rockrecord_build.py`; `PYRR` pyroclastic rock inside "intrusion" units is counted extrusive).

**Region (`derived_region`, an inference):** Northern Ireland if the polygon centroid lies west of 5.43° W and between 53.9° and 55.3° N, else Great Britain and the Isle of
Man. The rule puts 731 polygons totalling 14,164 km² of all bedrock in Northern Ireland (not checked against an official area; a first version of the rule
without the 53.9° N limit swept in Cornwall and Scilly, which lie west of 5.43° W). Silurian–Devonian area: Great Britain and Isle of Man 45,035 km², Northern Ireland 3,540 km².

**Old Red Sandstone (`derived_ors`, `derived_ors_evidence`):** a unit is flagged if its polygon name contains "OLD RED SANDSTONE" (`625k_name`), `SUPGP_EQ` is `ORS`
(`625k_supergroup_ORS`), its previous name contains it (`625k_previous_name`), or the Lexicon puts it under the Old Red Sandstone Supergroup (`lexicon_ORS_or_descendant`; 30 child
units, 9 of which have Silurian–Devonian polygons). **14 codes, 11,351 km²** (23% of the Silurian–Devonian area): `ATGK` Arbuthnott–Garvock, `CSSL` Cross Slieve, `DRCR`
Dunnottar–Crawton, `FIN` Fintona, `LNK` Lanark, `LORS` Lower ORS, `MOR` Middle ORS, `ORS` Supergroup, `REST` Reston, `SAG` Stratheden, `SEG` Strathmore, `SHAN` Shanmullagh,
`SHG` Stonehaven, `UORS` Upper ORS. `LORS` and `UORS` are obsolete in the current Lexicon ("Obsolete: use DAUG", "use ORSU"; `derived_lexicon_obsolete`).
Not flagged: the undifferentiated Lower, Middle and Upper Devonian units `LDEV`, `MDEV`, `UDEV` (3,710, 1,466 and 2,245 km²). 2,708 km² of `LDEV` has polygon centroids north of 51.4° N
(Wales and the Welsh Borders rather than Devon and Cornwall), where Lower Devonian rocks may be largely Lower Old Red Sandstone facies; that is an inference from location, since BGS labels
the unit Lower Devonian, undifferentiated, and the Lexicon entry carries no lithology or reference.

**Environment (`derived_environment_keywords`):** the Lexicon has no environment field (observed in the 60 records). Keywords (fluvial, volcanic, marine, …) are matched
in the Lexicon definition and lithology text; 16 of the 36 polygon units get any. Treat as weak.

**Area table, `bgs_outcrop_area_by_age.csv`.** Long format: `level` (period, series, stage), BGS term, its base and top year, `region` (`all_uk`,
`great_britain_and_isle_of_man`, `northern_ireland`), `rock_group` (`all`, `sedimentary`, `igneous_extrusive`, `igneous_intrusive`, `metamorphic`) and `subset` (`all`, `ors_flagged`).
Period and series rows give three areas: *overlap_any* (polygons whose range overlaps the term; double-counts), *exclusive* (polygons whose whole range lies within the term) and
*apportioned_by_bgs_years* (each polygon's area × the fraction of its BGS year range inside the term; my choice of rule, not BGS's or Dunhill et al.'s; parts of a polygon outside
Silurian–Devonian are not counted, so apportioned series areas sum to 46,778 km² of the 48,575). Stage rows give only the area of polygons labelled with that stage at either end
(`MAX_AGE`/`MIN_AGE` or the time terms) and where both ends name the same stage, because BGS gives a stage label for few polygons and only one boundary year for several stages.

United Kingdom, all regions, area in km² (period or series; BGS years in Ma):

| BGS term | Years (base–top) | Exclusive, sedimentary | Apportioned, all rocks | Apportioned, sedimentary | Apportioned, ORS-flagged |
| --- | --- | ---: | ---: | ---: | ---: |
| Silurian | 443–417 | 19,120 | 21,878 | 19,500 | 362 |
| Llandovery | 443–428 | 7,999 | 11,992 | 11,208 | 163 |
| Wenlock | 428–423 | 2,351 | 3,681 | 3,420 | 67 |
| Ludlow | 423–419 | 1,866 | 3,001 | 2,112 | 90 |
| Pridoli | 419–417 | 2,641 | 3,204 | 2,760 | 41 |
| Devonian | 417–354 | 18,001 | 24,900 | 18,588 | 10,989 |
| Early Devonian | 417–391 | 7,844 | 13,563 | 8,365 | 4,617 |
| Mid Devonian | 391–370 | 5,216 | 6,054 | 5,421 | 3,923 |
| Late Devonian | 370–354 | 4,562 | 5,284 | 4,802 | 2,449 |

## 4. What the series says (observed; reading in italics is inference)

- Exclusively dated sedimentary bedrock is largest in the Llandovery (8.0 thousand km²) and Early Devonian (7.8), smallest in the Ludlow (1.9) and Wenlock (2.4); the apportioned
  series changes shape because most polygons span several epochs. *Epoch-level area is therefore a coarse and rule-dependent sampling proxy.*
- The ORS-flagged units hold about 10,990 of the 18,590 km² of apportioned Devonian sedimentary bedrock, and 53% (4,134 of 7,844 km²), 72% (3,750 of 5,216; one unit, `MOR`) and 51% (2,317 of 4,562) of
  the exclusively Early, Mid and Late Devonian sedimentary area.
- 21 of the 30 Lexicon ORS child units occur nowhere in the 625k bedrock layer (observed), among them the Rhynie Group (`RHN`) and the Daugleddau Group (`DAUG`, the current name for `LORS`);
  *their ground is carried under `ORS`, `LORS` and neighbouring codes, so unit-level area for them needs the 1:50 000 data.*

## 5. Caveats

- **Edition and nomenclature.** The polygons are the 2008 edition (V5.17); several LEX codes have since been revised (two are now obsolete in the Lexicon). Polygon ages are on an
  undocumented 2008 scale that differs from the Lexicon's and from ICS v2024/12 (§2). Any stage-level use needs an explicit apportionment rule and a choice of scale; none is applied here
  (no conversion to ICS stages).
- **Bedrock at rockhead, onshore only.** No offshore rock, no thickness or volume, and sampled by 1:625 000 generalisation: small units are absorbed.
- **Region and rock group are derived** (rules in §3); ORS flags rest on names and Lexicon hierarchy; `LDEV` is not flagged.
- **No marine/terrestrial split**, which Dunhill et al. used.
- **Lexicon references are entry-level**, not age-specific: 17 of the 36 polygon units list any reference, 19 have none recorded (the undifferentiated and unnamed units). A reference such as
  Richardson et al. (1984, miospores) in the `ATGK` list suggests how an age was set; the Lexicon does not say so (inference).
- **Lexicon entries are a moving target** ("a dynamic database", "subject to revision without notice"); this is the state on 2026-10-27.

## 6. Access limits and decisions

- **DiGMapGB-50 (1:50 000) not pulled.** BGS lists it "Open / Premium": free only to view as a WMS layer or in GeoIndex; data licensed at £0.23 per km² for commercial use, with user, licence and
  preparation fees (BGS page, `bgs-geology-50k_dataset_page.html` in the raw folder). No view-service scraping was attempted.
- **DiGMapGB-250** (bedrock only, 1:250 000) was not evaluated.
- **Lexicon licence** unconfirmed (§2); prose kept local.
- No credentials were used or created. BGS's download links are tokenised public GET links.

## 7. Not done

- No conversion of BGS ages to ICS stages and no ICS-stage area series.
- No marine/terrestrial or facies assignment beyond keywords; no superficial, dyke or fault themes.
- No comparison of 625k areas with 1:50 000 areas, and no reproduction of Dunhill et al.'s numbers.
- No Lexicon entries beyond the 60 listed; no `SourceInfo` texts (not dereferenceable).
- No check of the NI total against an official figure.

## 8. Reproduce

From `data/external/scripts/`, with the GDAL command-line tools on `nectar`:

```sh
for s in rockrecord_fetch rockrecord_bgs_polygons rockrecord_lexicon rockrecord_build; do
  ssh nectar python3 - < $s.py
done
R=/data/codex/silurian_plants/raw/bgs/<stamp>
rsync -a nectar:$R/derived/out/ out/             # copy the four tracked tables and two local tables
rsync -a nectar:$R/derived/bgs_625k_bedrock_silurian_devonian.gpkg ../local/rock-record/
python3 rockrecord_manifest.py
```

A rerun gave identical zip checksums and byte-identical area, scale, divisions and polygon tables. Citation: British Geological Survey, BGS Geology 625k (DiGMapGB-625), version 5.17 (2008), and
BGS Lexicon of Named Rock Units, retrieved 2026-10-27, Open Government Licence where stated; acknowledge as BGS requires.
