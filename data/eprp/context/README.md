# Earth-system context for 485–383 Ma, extracted from EPRP's data mirror

Extracted 2026-10-26 by Claude Sonnet 5.5 (Claude Code subagent) for `silurian_plants`. Source: EPRP checkout `/Users/bwbrook/git/eprp` at commit `ac42dfbb4361d45e689d09c1324fd2495fb20f95` (read-only; nothing was written, staged or branched there) and the mirror on `deep-server:/data/paleodata/` (read-only). Window: anything overlapping 485–383 Ma, inclusive. Ages are Ma, left exactly as the sources give them; the project's timescale (`data/timescale.csv`, ICS v2024/12) is used only for flags and crosswalks, never to change a value. Observation, inference and not-done are kept apart below: "observed" means seen in a file or script output this session, "inferred" means my reading.

Reproduce with `ssh -o BatchMode=yes deep-server python3 - < data/eprp/scripts/context_climate.py` (likewise `context_palaeogeography.py`, `context_deposits.py`), rsync `/data/codex/silurian_plants-eprp/context/{context,local/context}/` back, then `python3 data/eprp/scripts/context_manifest.py`. Two of the scripts (`context_palaeogeography.py`, `context_deposits.py`) read inputs copied from the EPRP checkout into `/data/codex/silurian_plants-eprp/context/inputs/` (named in each script's header; sha256 values in §4). Every mirror file read is listed with its computed sha256 and the sha256 in the mirror's `MANIFEST.json` in `sources_used.tsv` (239 files, no mismatches; the EPRP-derived Rothman table has no mirror manifest).

## 1. Licence decisions

The brief's rule: no licence stated or no derivatives → `local/context/` (gitignored); NC → `context/` but flagged. `data/eprp/.gitignore` (`local/`, written by another agent; verified with `git check-ignore`) ignores everything under `local/`.

| Where | What | Why |
|---|---|---|
| `context/` | Song et al. 2021 (CC BY 4.0), Scotese et al. 2021 derived GMST (CC BY 4.0 maps), PaleoDEM slice index (CC BY 4.0), metadata tables, small CC0/CC BY/MIT deposit files | licence allows redistribution |
| `context/` flagged **NC** | `rothman2017_events_window.csv` | Rothman 2017 is CC BY-NC 4.0 |
| `local/context/` | PhanDA, PhanSST (GitHub head), Green et al. 2022 tables | the three GitHub repositories state no licence; the Green article is CC BY-NC-ND (no derivatives). Held privately under Barry's 23 October 2026 mirroring approval (EPRP climate-forcing entry; the reuse questions are EPRP CONTACTS C29, C30) |
| `local/context/` | PaleoDEM rasters (CC BY 4.0; 557 MB; with the deposit grids `local/context/` is 604 MB) | rasters, as instructed |
| `local/context/` | Balembois et al. SST and cGENIE grids (CC BY 4.0), Malanoski et al. coastline GeoTIFFs (CC0): redistributable but gridded; Currano et al. zip: licence "other-open", unclear | rasters; unclear licence |

Consequence for use: the PhanDA GMST/CO2 series and the PhanSST points, the two most useful temperature sources, exist only in `local/context/` on this machine. If they are needed in a committed table, the licence questions (EPRP CONTACTS C29, C30) have to be answered first.

## 2. Files

Paths are relative to `data/eprp/`. `MANIFEST.tsv` has one row per delivered file (raster folders, and the 34 Balembois grids, as one row each with a combined hash); row counts below are data rows.

### Climate and carbon

| File | Rows | Content and filter |
|---|---:|---|
| `local/context/phanda_gmst_co2_window.csv` | 18 | PhanDA GMST and CO2 percentiles (5, 16, 50, 84, 95) for every stage slice with UpperAge < 485 and LowerAge > 383; the 16 original columns, unchanged |
| `local/context/phanda_ltg_window.csv` | 1,314 | PhanDA latitudinal surface-air-temperature gradient percentiles, the same 18 slices × 73 latitudes; original 6 columns plus `derived_slice_*` (stage and slice ages joined from the file above). Units are not documented by PhanDA (values read as °C; inferred) |
| `local/context/phansst_window.csv` | 4,974 | PhanSST points with `Age` 383–485 (nominal age; no age uncertainty exists): all 55 original columns, plus `derived_ics2024_stage_of_age` and `derived_stage_label_differs` (§5) |
| `context/scotese2021_gmst_derived_window.csv` | 17 | **Derived here**, not published values: area-weighted (cos latitude) global, 30°S–30°N and poleward-of-60° mean surface temperature of each Scotese et al. 1° map labelled 385–480 Ma. The mirror holds maps, not a GMST table |
| `context/song2021_O5_window.csv`, `song2021_S1-S3_window.csv`, `song2021_D1-D3_window.csv` | 21, 160, 325 | Song et al. 2021 Database S1, the three sheets with ages in the window (all other sheets are 374.4 Ma or younger). Original header strings kept verbatim (including trailing spaces and Excel float artefacts such as `2.5000000000000001E-2` = quantile 0.025; the group label `SST (℃)` in row 1 of S1-S3 and D1-D3 marks the quantile columns as sea-surface temperature in °C); cell values copied as stored. Added: `derived_xlsx_row`, `derived_ics2024_stage_of_age`, `derived_stage_label_differs` |
| `context/rothman2017_events_window.csv` | 3 | Rothman 2017 Table 1 events dated 383–485 Ma: End-Ordovician 445.80, Silurian Mulde 428.20, Silurian Lau 423.50. **NC.** Taken from EPRP's `derived/2026-10-23/rothman2017_events.tsv` and checked here against Table 1 in the article XML: 31 of 31 rows agree |
| `local/context/green2022_boundaries_window.csv` | 21 | Green et al. 2022 stage boundaries (rows 71–91, 382.7–485.4 Ma) with age ± 1σ overlapping the window; original columns plus the ICS v2024/12 base of the stage above the boundary and the shift |
| `local/context/green2022_lips_window.csv` | 1 | Large igneous provinces: only Suordakh (Siberia, 450 ± 12 to 444 ± 11 Ma; volume NaN, eruption rate `#VALUE!` in the source) |
| `local/context/green2022_impacts_window.csv` | 4 | Impact craters with age ± 1σ overlapping the window: Carswell 481.5 ± 0.4 (39 km), Lawn Hill 476 ± 8 (18 km), Nicholson Lake 387 ± 5 (12.5 km), Siljan 380.9 ± 4.6 (52 km; in only through its 1σ) |

Selection for Green's three tables: nominal overlap, else overlap after widening by 1σ; the column `derived_window_basis` says which. Nothing else in those tables overlaps: Kalkarindji ends at 498.3 Ma, Kola–Dnieper starts at 378.64 Ma and Viluy at 376.7 Ma (observed, the nearest LIPs on either side). Rothman's table has no other event in the window (Cambrian Spice at 497.0 and Frasnian–Famennian at 372.2 Ma fall outside); Ireviken is not in it.

### Palaeogeography

| File | Rows | Content |
|---|---:|---|
| `context/paleodem_slices.csv` | 21 | The 21 PALEOMAP PaleoDEM maps with plate-model age 385–485 Ma (Maps 67.5–82.5): description and ages from Table 1 of the PaleoDEM report, ICS v2024/12 stage checks, the three file names with bytes and sha256, and the matching Balembois HadCM3 SST file |
| `local/context/paleodem/csv_1deg/` | 21 files | lon, lat, elevation (m) CSV, 1° |
| `local/context/paleodem/nc_1deg/` | 21 files | netCDF, 1° (1.1 MB) |
| `local/context/paleodem/nc_6min/` | 21 files | netCDF, 6 arcmin (521 MB) |
| `context/plate_models.csv` | 27 | the 26 GPlates index models plus Wright et al. 2013 (not in the index): reference, index range, coverage of 485–383 Ma, licence, deep-server path, EPRP notes, PBDB use, and script-derived pole counts in the window |

### Register deposits

| File | Rows | Content |
|---|---:|---|
| `context/register_deposits_relevant.csv` | 31 | deposits judged relevant, with framings, relevance rating and one-line note (both inference) |
| `context/register_deposits_screened.csv` | 93 | every deposit with its verdict and reason |
| `context/deposits/<id>/` | 30 files | small files of 11 deposits whose licence allows redistribution (CC0, CC BY 4.0; TREED also Apache 2.0) |
| `local/context/deposits/<id>/` | 56 files | Balembois HadCM3 SST for the 21 window slices and 13 cGENIE climate files (400–480 Ma), Malanoski et al. isolated-coastline GeoTIFFs for the 21 window maps, the Currano et al. herbivory zip (unclear licence) |

### Timescale and bookkeeping

`context/timescale_basis.csv` (6 rows: each series' own timescale basis, evidence, Devonian note), `context/timescale_stage_bounds.csv` (20 stages on ICS v2024/12, GTS2012 and the GTS2020 chart), `local/context/timescale_stage_bounds_phanda_phansst.csv` (PhanDA slice bounds and the age range of PhanSST points under each stage label), `context/sources_used.tsv`, `context/MANIFEST.tsv`, this file.

## 3. Coverage of the window

| Series | Coverage 485–383 Ma | Quality in the window |
|---|---|---|
| PhanDA GMST, CO2, gradient | all 18 stage slices, Tremadocian to Givetian | stage-wide only; wide intervals; CO2 5–95% spans a factor of 2.4 to 12.5 within a slice |
| PhanSST | 4,974 points, 383.3–482.0 Ma, 163 sites, 49 lead-author–year sources; conodont phosphate δ18O 2,498, brachiopod calcite δ18O 2,476, no TEX86, UK'37 or Mg/Ca | uneven: Katian 1,008, Aeronian 30, Rhuddanian 27, Givetian 76 (source stage labels); 93% have ages from relative information (AgeFlag 1: 3,228; 2: 1,397; 0, a numeric age: 349); diagenesis flag good 4,000, questionable 905, blank 69 |
| Scotese et al. 2021 | 17 temperature maps (385–450, then 460, 470, 480 Ma); none at 455, 465, 475, 485 | maps adjusted to δ18O and lithological climate indicators; no CO2 table |
| Song et al. 2021 | O5: 21 clumped-isotope rows, 443.5–446.0 Ma (Hirnantian, late Katian); S1-S3: 160 rows 421.0–443.8 Ma; D1-D3: 325 rows 383.0–424.3 Ma | sample-level SST estimates with quantiles; nothing older than 446.0 Ma |
| Rothman 2017 | 3 events | coarse |
| Green et al. 2022 | 21 boundaries, 1 LIP, 4 impacts | no LIP volume or eruption rate for Suordakh |
| PaleoDEM | 21 slices at 5 Myr (Givetian to Cambro-Ordovician boundary) | one map per slice, no uncertainty |
| Plate models | 8 of the 26 index models span the window (index range), plus Wright et al. 2013; 5 more span 410–383 Ma only (§6) | |

Carried over from the EPRP catalogue entries (climate-forcing, palaeogeography, register-deposits): PhanDA assimilates each slice separately, so there is no joint temporal posterior; six PhanDA slices merge two stages, two of them in the window (Pragian/Lochkovian, Aeronian/Rhuddanian); PhanDA and PhanSST ages are GTS2020 (§5); the PhanSST GitHub head holds 568 more rows than the DOI release v0.0.1-beta (observed in the window: 4,974 against 4,945); Green's σ column records rounding, not measurement uncertainty, for the 18 youngest boundaries (none in the window); Green's S2 LIP names differ from the repository's for two LIPs (neither in the window); the PhanDA HadCM3L priors (11.4 GB) are indexed only and were not touched.

PhanDA GMST and CO2 in the window (percentiles 50 and 5–95; slice bounds as in the file, GTS2020):

| Slice (Ma) | GMST, °C | CO2, ppm |
|---|---|---|
| Givetian (378.9–385.3) | 25.7 (21.5–30.0) | 1004 (667–1575) |
| Eifelian (385.3–394.3) | 22.5 (18.8–26.9) | 708 (353–1329) |
| Emsian (394.3–410.5) | 25.3 (21.8–29.1) | 2035 (1228–3434) |
| Pragian/Lochkovian (410.5–419.0) | 28.8 (23.4–33.2) | 2018 (606–3888) |
| Pridoli (419.0–422.73) | 33.2 (25.5–38.6) | 1282 (430–4031) |
| Ludfordian (422.73–425.01) | 34.0 (28.2–38.2) | 1245 (398–4506) |
| Gorstian (425.01–426.74) | 25.6 (18.8–32.9) | 1187 (369–4613) |
| Homerian (426.74–430.62) | 21.0 (15.0–26.7) | 524 (288–903) |
| Sheinwoodian (430.62–432.93) | 19.9 (13.6–25.9) | 505 (279–912) |
| Telychian (432.93–438.59) | 24.4 (17.7–30.8) | 631 (370–1062) |
| Aeronian/Rhuddanian (438.59–443.07) | 19.5 (13.0–24.4) | 620 (349–1069) |
| Hirnantian (443.07–445.21) | 20.8 (14.8–27.2) | 624 (345–1156) |
| Katian (445.21–452.75) | 27.8 (23.0–32.8) | 483 (341–690) |
| Sandbian (452.75–458.18) | 27.3 (22.4–32.9) | 482 (329–685) |
| Darriwilian (458.18–469.42) | 31.0 (24.6–35.9) | 2553 (1242–4313) |
| Dapingian (469.42–471.26) | 30.9 (23.3–35.9) | 3243 (2287–4674) |
| Floian (471.26–477.08) | 31.5 (23.3–39.3) | 3326 (2330–4785) |
| Tremadocian (477.08–486.85) | 32.1 (22.6–36.9) | 3261 (2286–4665) |

Observed disagreement between the two GMST series: PhanDA's medians are 3–16 °C warmer than the Scotese-derived means in every Silurian and Hirnantian slice, pairing each stage with the nearest map label (my pairing): Pridoli 33.2 against 19.0 at the 420 Ma map, Ludfordian 34.0 against 17.7 at 425 Ma, Hirnantian 20.8 against 8.1 at 445 Ma, Sheinwoodian 19.9 against 16.6 at 430 Ma. Scotese-derived values (slice label; global, 30°S–30°N, poleward of 60°): 385: 21.7, 27.0, 6.9; 390: 19.5, 24.8, 4.8; 395: 18.0, 23.3, 3.3; 400: 17.3, 23.8, −1.9; 405: 20.5, 27.0, 1.3; 410: 18.3, 26.8, −8.1; 415: 20.7, 28.2, −0.9; 420: 19.0, 26.9, −3.9; 425: 17.7, 25.6, −5.2; 430: 16.6, 23.2, −2.3; 435: 18.5, 25.5, −1.7; 440: 15.7, 23.6, −7.3; 445: 8.1, 21.4, −28.5; 450: 14.0, 22.6, −11.6; 460: 17.1, 24.6, −4.5; 470: 18.5, 24.7, 1.0; 480: 20.2, 25.9, 4.1. An independent DuckDB check of the 410 Ma map reproduced the weighted mean (18.3097 against 18.3097). The primer's 18.7 °C for the Early–Middle Devonian cool interval (Scotese et al. 2021) is close to the 390–400 Ma derived values (19.5, 18.0, 17.3); the derived numbers are my computation from the maps, not the article's curve, and I did not check them against it.

Observed quirks, none repaired: (1) in every Scotese list file the first two cells of the 90°N row read 50 and −55 in all 17 slices (in the 450 Ma file the other cells of that row are constant at −16.75, the only slice I checked); the row has zero weight in the means and is excluded from `min_cell_c_excl_lat90_row`/`max_cell_c_excl_lat90_row`; longitude 180 duplicates −180 and is skipped (`n_cells_skipped` 181). (2) Green's `impacts.tsv` holds U+FFFD where a degree sign was lost, and its LIP tables hold `#VALUE!` and `NaN`; rows with missing trailing fields were padded with empty strings to the header width (structure only). (3) The Song O5 sheet carries original and updated ages and stages (`Age-updated`, `Stage-updated`): five rows labelled late Katian at 445.7–446.0 Ma are re-assigned to the Hirnantian at about 442.9–443.0 Ma; the filter uses the original `Age, Ma`. (4) Song's Devonian ages are interpolated (decimals such as 392.1731).

## 4. Versions and hashes

All mirror files verified: computed sha256 equals the mirror manifest's. Full list: `sources_used.tsv`.

| Source | Mirror version | File | sha256 |
|---|---|---|---|
| PhanDA | git 9f06c0d976 (2026-03-09) | `5_Outputs/PhanDA_GMSTandCO2_percentiles.csv` | `22cad7964bac3b679ad83bf8a9c83eb66e995898a01eb9e93142087b2d4f6e1f` |
| PhanDA | same | 18 `PhanDA_LTG_*.csv` (list in `sources_used.tsv`) | per file |
| PhanSST | git 32cc98ed53 (2023-03-09) | `PhanSST_v001.csv` | `c46913f8501d6f8f95d5e27884c4f4055d68accc08d0cd3a060a93a50e33833b` |
| PhanSST (count comparison only) | Zenodo v0.0.1-beta 7275402 | `PhanSST-v0.0.1-beta.zip` | `abedad63039d70bcaccdf99cdcb559101477b80c477c3bc53526d45aeec39182` |
| Song et al. 2021 | Zenodo 5027293 | `Database S1.xlsx` | `19e2590fa5a40d10535c2a5f0ebe211141e78427e8734786e4f4cc9a7b2a2473` |
| Scotese et al. 2021 | Zenodo 8238875 (scotese02a_v21321, C1) | `gmst_scotese02a_v21321_csv-list.zip` | `b27286b06cf8ae679a1dae862267cf4ced3d074a7977a5a0d6772af8d7913298` |
| Rothman 2017 | plain-URL snapshot 2026-10-23T0915Z | `PMC5606709_fullText.xml` | `a97bea4a2d4fbf8c706500b39055fc38c5a5861b7149d74b16a15aad598efad8` |
| Rothman 2017 (EPRP parse) | `derived/2026-10-23` | `rothman2017_events.tsv` | `7cdce2455c871cac9d9a6643e296d222bb9d84b65f7fcf27dbb2f001b0b382e8` |
| Green et al. 2022 | git e3038b5c02 (2023-03-21) | `data/boundaries.tsv` | `f97fa431f9bc074c4a6d1e770618ba160b630cf88c757677f6a22e710edc3825` |
| | | `data/LIPs Including Oceanic.tsv` | `3568d85a66accee51f2221dab543d24cf3e82076baf72e639113d290c45910b7` |
| | | `data/impacts.tsv` | `c4f9caccbbcd9ac43d64e0df267b4d5756dbc57293bd5165a644fba0e3eff2ac` |
| GPlates index | snapshot 2026-10-24T0301Z | `models.json` | `1c489b8443946c61f486405294cf6b60c986690da81096b3876c38eb84e2826a` |
| PaleoDEM | Zenodo 5460860 | `PaleoDEMS_long_lat_elev_csv_v2.zip` | `db43e6261411ff468c9030ca240778a73f224bf34bf8186c735477e41454c873` |
| | | `Scotese_Wright_2018_Maps_1-88_1degX1deg_PaleoDEMS_nc.zip` | `7014767a168c28d3762f55117ebafcd0f6b6b90029a495e2d14fd23f94abc16d` |
| | | `Scotese_Wright_2018_Maps_1-88_6minX6min_PaleoDEMS_nc.zip` | `ab360184d8260a815ef5ed6b8b4e0abdbf99ef5ee8aa87dfd070af323ceb42da` |
| | | `Scotese_Wright2018_PALEOMAP_PaleoDEMs.pdf` | `8a5fca14f9860d148427a56cec241b4fc5b4108ff91bb867e8b68bde1392edac` |
| Wright et al. 2013 | snapshot 2026-10-24T0320Z (a 0303Z snapshot also exists) | `bg-10-1529-2013-supplement.zip` | `effa5e4b2598219eb4e6c8e4e95a8d0126e1da8a7635be4eba2ac0258192f550` |
| EPRP checkout files | ac42dfb | `resources/sources/palaeogeography/gplates-models-licences.tsv` | `41c1898ab38be0f89b06bee2ea37d7e5b46d00a05ef695696899b82c34fc1be7` |
| | | `…/palaeogeography/profile/palaeogeography_profile.tsv` | `bae0c9120e4800eee09d14470bfcb4f902146cdba615ffd8d68756caaf212034` |
| | | `…/register-deposits/snapshots.tsv` | `11169283a0bdd1201eceb9c30a6445aa1a77f9e887d444bd7bd39cefedc630d4` |

Register deposits: the version of each deposit is its `version_dir` in `snapshots.tsv` (newest mirrored version), given per file in `MANIFEST.tsv`.

## 5. Timescale bases

Nothing was converted. `timescale_basis.csv` gives each series' basis and the evidence. In short: PhanDA and PhanSST are on GTS2020 (PhanSST's ReadMe says so; PhanDA's Ordovician–Silurian slice bounds equal ICS v2024/12 to rounding; its Eifelian, Emsian and Lochkovian bases equal the GTS2020 chart values quoted in `docs/primer.md` §1.2, and its Eifelian/Givetian bound, 385.3, is not in the primer's table); Green et al. boundaries are GTS2012; Rothman cites GTS2012 for its biostratigraphically dated events but gives the K–Pg at 65.50 Ma (older value, outside the window); Song's Devonian sheets give no scale (the Carboniferous–Permian sheets say "Age (Ma)-2012"; GTS2012 inferred, the article was not read); the Scotese maps and PaleoDEMs are labelled by PALEOMAP plate-model age and the PaleoDEM report's stage ages are "from Ogg, Ogg & Gradstein (2012)" (observed, GTS2012 midpoints: the Pragian 409.2, Givetian 385.2 and Eifelian 390.5 Ma entries equal the midpoints of the GTS2012 stages, my arithmetic).

| Stage | ICS 2024/12 base | GTS2012 base | GTS2020 chart base (primer) | PhanDA slice (upper–lower) | PhanSST ages under the stage label (whole file) |
|---|---|---|---|---|---|
| Givetian | 387.95 | 387.7 | – | Givetian (378.9–385.3) | 378.9–387.0 (n=331) |
| Eifelian | 393.47 | 393.3 | 394.3 | Eifelian (385.3–394.3) | 385.7–395.1 (n=366) |
| Emsian | 410.62 | 407.6 | 410.5 | Emsian (394.3–410.5) | 394.3–407.8 (n=265) |
| Pragian | 413.02 | 410.8 | 412.4 | Pragian/Lochkovian (410.5–419.0) | 408.6–412.4 (n=92) |
| Lochkovian | 419.62 | 419.2 | 419.0 | Pragian/Lochkovian (410.5–419.0) | 412.4–419.0 (n=148) |
| Pridoli | 422.7 | 423.0 | – | Pridoli (419.0–422.73) | 419.0–422.7 (n=92) |
| Ludfordian | 425.0 | 425.6 | – | Ludfordian (422.73–425.01) | 422.7–424.9 (n=441) |
| Gorstian | 426.7 | 427.4 | – | Gorstian (425.01–426.74) | 424.4–426.6 (n=77) |
| Homerian | 430.6 | 430.5 | – | Homerian (426.74–430.62) | 426.8–430.9 (n=271) |
| Sheinwoodian | 432.9 | 433.4 | – | Sheinwoodian (430.62–432.93) | 429.1–434.2 (n=261) |
| Telychian | 438.6 | 438.5 | – | Telychian (432.93–438.59) | 432.9–438.6 (n=155) |
| Aeronian | 440.5 | 440.8 | – | Aeronian/Rhuddanian (438.59–443.07) | 438.9–440.2 (n=30) |
| Rhuddanian | 443.1 | 443.8 | – | Aeronian/Rhuddanian (438.59–443.07) | 440.0–443.5 (n=27) |
| Hirnantian | 445.2 | 445.2 | – | Hirnantian (443.07–445.21) | 443.2–446.0 (n=123) |
| Katian | 452.8 | 453.0 | – | Katian (445.21–452.75) | 445.2–452.8 (n=1008) |
| Sandbian | 458.2 | 458.4 | – | Sandbian (452.75–458.18) | 452.3–460.8 (n=404) |
| Darriwilian | 469.4 | 467.3 | – | Darriwilian (458.18–469.42) | 458.4–469.8 (n=526) |
| Dapingian | 471.3 | 470.0 | – | Dapingian (469.42–471.26) | 468.0–471.0 (n=272) |
| Floian | 477.1 | 477.7 | – | Floian (471.26–477.08) | 471.3–476.6 (n=177) |
| Tremadocian | 486.85 | 485.4 | – | Tremadocian (477.08–486.85) | 478.4–486.6 (n=173) |

Where the Devonian mismatch matters (observed):

- PhanDA's Eifelian/Givetian bound is 385.3 Ma against ICS v2024/12's 387.95 (2.65 Myr). The Eifelian slice therefore also holds ages that ICS v2024/12 calls Givetian. The Emsian base differs by 0.1 Myr, the Lochkovian base by 0.6, the Eifelian base by 0.8.
- PhanSST: 294 of the 4,974 window points have a stage label that differs from the ICS v2024/12 stage of their `Age`; 162 of those are Devonian by age. The biggest groups: 106 labelled Eifelian with ages below 387.95 (ICS: Givetian), 28 labelled Pragian and 12 Eifelian with ages in the Emsian (ICS), 9 Lochkovian in the Pragian, 7 Pridoli in the Lochkovian. In the Silurian the largest groups are 32 points labelled Sheinwoodian that are Homerian by age, 19 Sheinwoodian that are Telychian, and 31 Gorstian that are Ludfordian. The stage label and the age are both the source's; use either deliberately.
- Song D1-D3: the label disagrees with the ICS v2024/12 stage of the age for 66 of 325 rows (Pragian→Emsian 38, Lochkovian→Pragian 19, Pridoli→Ludfordian 4, Pridoli→Lochkovian 3, Emsian→Eifelian 2); the flag normalises spelling and series names.
- Green boundaries on GTS2012: the Emsian base is 3.02 Myr older and the Pragian base 2.22 Myr older on ICS v2024/12 (the largest Devonian shifts); Ordovician: Darriwilian base +2.1, Dapingian +1.3, Tremadocian +1.45 Myr.
- PaleoDEM Map 71 is labelled Pragian (409.2 Ma) with plate-model age 410, which is Emsian on ICS v2024/12 (410.62 Ma base); the other 20 labels are consistent with their stage at the description age.
- Three label systems coexist for the same 21 maps: PaleoDEM files and the Scotese temperature maps use the plate-model age (385, 390, … 485; the Scotese file labels are inferred to be the same); the Balembois HadCM3 SST files use the description age rounded (385, 391, 395, 400, 405, 409, 415, 421, 425, 430, 436, 441, 445, 449, 456, 460, 465, 470, 475, 482, 485). `paleodem_slices.csv` gives the match.

## 6. Palaeogeography

**PaleoDEM.** 21 slices, one per row of `paleodem_slices.csv`; the 485 Ma map is the Cambro-Ordovician boundary (485.4 Ma, GTS2012), 385 the Givetian. The 380 Ma map (early Frasnian) and 490 Ma map (Jiangshanian) fall outside. The report states: use the "plate tectonic model age" with the PALEOMAP Global Plate Model v2d3 in GPlates. Elevation and bathymetry are model reconstructions (Scotese), not data.

**Plate models, 26 in the index (+ Wright 2013).** Full coverage of 485–383 Ma by the index range: `cao2024`, `muller2025` (0–1,800 Ma), `merdith2021`, `muller2022` (0–1,000 Ma; palaeomagnetic against mantle frame, diverging through the Palaeozoic), `paleomap` (0–750), `scotese_and_wright2018`, `torsvikcocks2017`, `golonka` (0–540), and Wright et al. 2013 (rotation file to 850 Ma). 410–383 Ma only: `matthews2016_mantle_ref`, `matthews2016_pmag_ref`, `young2018`, `zahirovic2022` (0–410), `domeier2014` (250–410). None of the other 13 reaches the window. Six models state no licence in the index (`torsvikcocks2017`, `matthews2016_pmag_ref`, `domeier2014`, `muller2008`, `golonka`, `rodinia`); `golonka` and `torsvikcocks2017` are among the full-coverage ones, so their use needs a licence check. The files are not copied; `plate_models.csv` gives `/data/paleodata/palaeogeography/gplates-models/raw/2026-10-24T0301Z_url/<model>__*.zip`.

Observed: the rotation files of `paleomap` and `scotese_and_wright2018` are byte-identical (header "PALEOMAP Plate Model m15g60_v2d3"), and so is the one in Malanoski et al. 2026; `golonka`'s rotation file has the same name, maximum pole age (850 Ma) and window pole counts as Wright et al. 2013's but a different size (70,859 against 86,561 bytes). Rotation files carry poles beyond their index ranges for all 26 models (five run to 3,000 Ma, which EPRP calls placeholders), so "poles exist" does not mean coverage; the script-derived columns count poles and moving plates with a non-zero rotation in the window. Observed: `muller2025` has 835 poles in the window for 161 plates, `merdith2021` 472 for 148, `paleomap`/`scotese_and_wright2018` only 29 for 10 plates, `golonka`/Wright 102 for 42.

**PBDB.** Per EPRP, PBDB's default `gplates` palaeocoordinates come from Wright et al. 2013, `scotese` from PALEOMAP and `seton` from Seton et al. 2012. Plate IDs match on 99.5–100% of collections; palaeolatitudes match within 1° for 98–99.7% of collections under 100 Ma but for only 75–92% (Wright) from 100 Ma, probably through later rotation-file versions in PBDB (EPRP, unresolved). So for the window the mirrored Wright file is only an approximation of PBDB's own coordinates. Alternatives covering the Palaeozoic are present (above); EPRP has no test of any of them against PBDB for the window or against each other. The project's primer states that no reliable global full-plate model exists before 410 Ma; EPRP does not address this.

## 7. Register deposits

93 deposits screened; 31 relevant (3 high, 9 moderate, 19 low); 62 not (marine animal or vertebrate dynamics outside the window, Ediacaran, Mesozoic–Cenozoic, modern). The relevance, framing and note columns are my inference from EPRP's entry and the deposits' READMEs.

Most useful for the project:

1. `rogger2026-treed-vegetation-model` (Rogger et al. 2026, GMD, doi:10.5194/gmd-19-4931-2026): TREED, a trait- and optimality-based vegetation model with lagged evolution and dispersal on a global climate grid (Julia). Code, README, LICENSE and `Project.toml` are in `context/deposits/`; the three case-study zips (1.4 GB) are not. Not in the project's primer or precedents.
2. `rogger2024-lip-climate-sensitivity` (Rogger et al. 2024, Science, doi:10.1126/science.adn3450): eco-evolutionary vegetation coupled to a geologic carbon-cycle model and a PlaSim climate lookup, with LIP degassing on Permian–Triassic, Triassic–Jurassic, Paleocene–Eocene and present-day geographies; dispersal and niche-adaptation rates are the biological parameters. The closest existing structure for F5 and F6. 2.8 GB; README copied.
3. `pohl2024-late-ordovician-foam` (Zenodo 10610771; FOAM set-up of Ontiveros et al. 2023): atmosphere, ocean and coupled netCDF for 440 Ma at "840ppm" per the file names (173 MB; path only). The only Palaeozoic land-surface climate field in the register.
4. `balembois2025-marine-biodiversity-drivers` (Balembois et al. 2025, Nat. Commun., doi:10.1038/s41467-025-63428-9): HadCM3BL monthly SST on 109 PALEOMAP slices (21 in the window, in `local/context/deposits/`) and cGENIE climate fields with surface air temperature, humidity and precipitation at 36 × 36 for 400–480 Ma (13 files copied). Marine paper, usable as boundary conditions.
5. `malanoski2026-paleogeography-extinction-risk`: coastline isolation and distance-to-track metrics on the same PALEOMAP maps (GeoTIFFs for the 21 window maps copied; stage table `massext_tab.csv` copied).
6. Observation-model material for F3: `holland2016-stratigraphy-mass-extinction` (forward stratigraphic model), `alroy2026-coverage-rarefaction`, `cooper2024-deepdive` (code copied), `stigall2026-ordovician-species` (in-window phylodynamic example), `franeck2018-ordovician-radiation`, `crampton2026-extinction-spectrum` (graptoloid rates through the Hirnantian and the Silurian events).
7. `freitas2026-patch-biogeography-simulations` for F4.

Caveats from the catalogue: `benson2025-marine-latitudinal-diversity`, its companion `close2025-marine-latitudinal-diversity-code`, `kocsis2018-biogeographic-imprint`, `smith2023-biodeeptime` and `malanoski2026` hold or derive from PBDB records that PBDB now withholds (EPRP's flag; Barry's 24 October decision keeps them in the mirror). The TREED record states CC BY 4.0 on Zenodo and Apache 2.0 in its LICENSE.txt; both allow redistribution. `cao2022-reverse-weathering-esm` is Springer Nature TDM licence, held privately, and was not copied; it is end-Permian and outside the window. Indexed-only records (not on disk): `rogger2025-petm-vegetation` (15.6 GB), `shum2026-dark-land-refugia` (106 GB, not relevant), and four others. `liu2026-phanerozoic-productivity-oxygen` holds ocean model grids and PhanSST values and no variable named for atmospheric O2 or CO2 (variable names read with scipy and h5py in scratch).

## 8. Gaps: series the project cites that EPRP does not hold

Searched: the EPRP source READMEs, `resources/sources/index.tsv` and `resources/capability-inventory.md` for COPSE, GEOCARB, Royer, Foster, phytane, stomatal, paleosol and pCO2; no hit. Not held (observed absence):

- CO2: the Foster et al. (2017) compilation (1,241 estimates; starts at 420 Ma), Franks et al. (2014) leaf gas-exchange estimates, Witkowski et al. (2018) phytane δ13C CO2 for the Late Ordovician and Devonian, Nardin et al. (2011) GEOCLIM output, Lenton et al. (2016) COPSE output. The only CO2 series EPRP holds is PhanDA's, which I infer is a model-ensemble posterior rather than an independent proxy; its 5–95% range spans a factor of 2.4 to 12.5 within a slice and reaches 3,300 ppm (median) in the Floian against 480–630 ppm for Sandbian–Hirnantian. The Scotese PDF discusses a revised CO2 curve in a figure only (no table); the Balembois cGENIE files contain no CO2 variable (the CO2 prescribed is not recoverable from them); the Pohl FOAM file names carry 840 ppm.
- O2: Krause et al. (2018) GEOCARBSULFOR, Lenton et al. (2016) COPSE O2, charcoal and fire-window constraints (Glasspool et al. 2004; Scott & Glasspool 2006), Mo isotope (Dahl et al. 2010) and I/Ca (Lu et al. 2018) records. Nothing in EPRP.
- Related series the primer cites: Grossman & Joachimski (2022) δ18O compilation (22,332 carbonate and 4,615 phosphate analyses; PhanSST's conodont and brachiopod points are a different compilation), eustatic sea level (Haq & Schutter 2008), Sr and carbon-isotope seawater curves (only Rothman's three events). Present, by contrast: Finnegan et al. (2011) clumped isotopes and Trotter et al. (2016) and Joachimski et al. (2009) conodont data, as sample rows in Song's O5, S1-S3 and D1-D3 sheets.

## 9. Not done

- No age conversions, no harmonised temperature table across sources, no GMST or CO2 interpolation to the project's stages.
- Articles were not read: Song's timescale basis, the Scotese temperature-map stage names, Rothman's date sources and Green's definitions rest on the catalogue entries, the mirror files and the PaleoDEM report only. The PhanSST reference list (xlsx) was not extracted; each row carries `LeadAuthor`, `Year`, `PublicationDOI`, `DataDOI`.
- The PhanDA ensemble `.mat`, the `GMST_*.mat` prior files and the HadCM3L priors were not read.
- Plate-model files were not copied or reconstructed (no pygplates run); pole counts are plain text counts and do not test validity. EPRP's PBDB comparisons were not repeated.
- The PaleoAtlas zips (`PALEOMAP_PaleoAtlases.zip`, `Scotese_PaleoAtlas_v3.zip`) were not opened.
- Deposit screening used EPRP's descriptions, deposit READMEs and file lists; the contents of most deposits were not opened (exceptions: the Liu and Balembois grids' variable names, the Malanoski rotation file, the Stigall and Rogger READMEs). cGENIE variables were listed but not interpreted.
- Rogger et al.'s climate inputs (Zenodo doi:10.5281/zenodo.17777278) are not in the mirror.
