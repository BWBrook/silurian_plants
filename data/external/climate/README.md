# Land-surface climate: PhanDA HadCM3L priors, suite scotese_02, 485–383 Ma

Extracted 2026-10-27. Monthly-climatology 2 m air temperature (`tas`) and precipitation (`pr`) from 21 HadCM3L time slices, with a land summary per slice and a survey of other land-climate sources. These are **model priors, not reconstructions** (see Caveats). They serve framing F1 (moisture) and F4 (spore biogeography) in `docs/sources.md` §7, which listed this item as missing.

"Observed" below means read in the files, records or pages during this task. "Inferred" is my reading of those observations.

## 1. Source and citation

- **Data.** PhanDA HadCM3L Model Priors, Zenodo record 8237751 (version 1, published 2023-08-11), concept DOI 10.5281/zenodo.8237750, CC BY 4.0. Record DOI: 10.5281/zenodo.8237751. Eight suites of 109 time slices; each variable is a zip of 545 netCDF files (109 slices × five 20-yr means).
- **Simulations.** Run by the Bristol BRIDGE group; the suites `scotese_spinupa` and `scotese_02` were first published as the 109-slice Phanerozoic sequences of Valdes et al. (2021). The model is HadCM3L (HadCM3BL-M2.1aD, 3.75° × 2.5°); geography is Scotese's PALEOMAP maps (Scotese & Wright 2018).
- **Which paper to cite for which.** Cite Judd et al. (2024) and the Zenodo record for the files; cite Valdes et al. (2021) for the model, boundary conditions and the `scotese_02` and `scotese_spinupa` sequences.

References (DOIs checked against Crossref or DataCite on 2026-10-27 by `scripts/climate_doi_check.py`; results in `doi_check.tsv`):

- Judd, E. J., Tierney, J. E., Lunt, D. J., Montañez, I. P., Huber, B. T., Wing, S. L. & Valdes, P. J. (2024) A 485-million-year history of Earth's surface temperature. Science 385: eadk3705. doi:10.1126/science.adk3705
- Judd, E. J. et al. (2023) PhanDA HadCM3L Model Priors (Zenodo, version 1). doi:10.5281/zenodo.8237751
- Valdes, P. J., Scotese, C. R. & Lunt, D. J. (2021) Deep ocean temperatures through time. Climate of the Past 17: 1483–1506. doi:10.5194/cp-17-1483-2021
- Scotese, C. R. & Wright, N. (2018) PALEOMAP Paleodigital Elevation Models (PaleoDEMs) for the Phanerozoic (Zenodo). doi:10.5281/zenodo.5460860
- Scotese, C. R., Song, H., Mills, B. J. W. & van der Meer, D. G. (2021) Phanerozoic paleotemperatures: the earth's changing climate during the last 540 million years. Earth-Science Reviews 215: 103503. doi:10.1016/j.earscirev.2021.103503
- Foster, G. L., Royer, D. L. & Lunt, D. J. (2017) Future climate forcing potentially without precedent in the last 420 million years. Nature Communications 8: 14845. doi:10.1038/ncomms14845
- Rae, J. W. B. et al. (2021) Atmospheric CO2 over the past 66 million years from marine archives. Annual Review of Earth and Planetary Sciences 49: 609–641. doi:10.1146/annurev-earth-082420-063026

## 2. Experiments, and the baseline chosen

`ExperimentInfo.xlsx` (md5 verified) and the Zenodo description give the eight suites. Window CO2 is from `hadcm3l_experiment_info.csv` (observed). The "Update A/B" model changes are not described in the record or in any source I could read (the accepted manuscript of Judd et al. returned HTTP 403 to a plain user agent); only the labels are known.

| Suite | CO2 | Model configuration | CO2 in the window (ppm) | Role (observed from the record and the BRIDGE pages) |
|---|---|---|---|---|
| `scotese_solara` | 1 × pre-industrial | Original | 276 | fixed-CO2 sensitivity |
| `scotese_2co2a` | 2 × pre-industrial | Original | 560 | fixed-CO2 sensitivity |
| `scotese_4co2a` | 4 × pre-industrial | Original | 1,120 | fixed-CO2 sensitivity |
| `scotese_spinupa` | smoothed Foster et al. (2017) | Original | 1,079–1,904 | last 500 years of a 5,500-year spin-up (BRIDGE page) |
| **`scotese_02`** | Foster et al. (2017) | Original | **1,093–2,513** | Valdes et al. (2021) headline sequence |
| `scotese_06` | as `scotese_02` | Update A | 1,093–2,513 (identical) | newer configuration |
| `scotese_07` | Foster plus Rae et al. (2021) | Update B | as `scotese_02` except 410 Ma (2,162 against 2,102) | newer configuration |
| `scotese_08` | tuned to match the GMST of Scotese et al. (2021) | Update B | 369–3,114 | CO2 as a free parameter |

**Choice: `scotese_02`.** Reasons:

1. It is a standard, published HadCM3L run: the sequence documented in Valdes et al. (2021), with the original model configuration, proxy-based CO2 and PALEOMAP geography, and the BRIDGE pages describe it as the Foster-CO2 sequence.
2. The three fixed-CO2 suites hold CO2 at 276, 560 and 1,120 ppm, so only the last lies inside the 1,000–3,000 ppm sensitivity range for the Silurian–Early Devonian (`docs/primer.md` §3.2) and none varies through the window; they isolate geography and solar forcing. `scotese_08` takes CO2 from a temperature target (369 ppm at 445 Ma against 1,708 ppm), not a CO2 proxy. `scotese_spinupa` is a smoothed-CO2 variant of the same configuration.
3. `scotese_06` and `scotese_07` have the same window CO2 but newer model configurations whose changes I could not document. They are the natural sensitivity test of model version, 814 MB each for `tas` and `pr`; not pulled.
4. Its CO2 in the slices inside the window (455.7–395 Ma) is about 1,300–2,100 ppm (1,093–2,513 ppm across all slices extracted), inside the primer's 1,000–3,000 ppm sensitivity range, which is a judgement, not a proxy result.

This is a judgement, not a measurement. Foster et al. (2017) reach back only to 420 Ma; per the text of Valdes et al. (2021) as I read it, the paper proposes two extensions of the curve to 540 Ma, so the Ordovician and most of the Silurian part of the window rests on an extension. I did not check which extension `scotese_02` uses.

## 3. What was obtained

On `deep-server:/data/codex/silurian_plants/raw/hadcm3l/` (provenance in `PROVENANCE.tsv` there, copied to `hadcm3l_raw_provenance.tsv` here):

| File | Bytes | md5 (matches the Zenodo record) | Fetched (UTC) |
|---|---|---|---|
| `ExperimentInfo.xlsx` | 25,443 | `0c61461d58ce3614a604d8dbe3636ad8` | 2026-10-27T00:44:33Z |
| `scotese_02_tas.zip` | 304,593,710 | `5dc5fb031d6840b22c29a52158991f73` | 2026-10-27T00:49:01Z |
| `scotese_02_pr.zip` | 515,100,776 | `8c15488f422669aeba0a1a09e8a4b783` | 2026-10-27T00:56:46Z |

Both zips pass `unzip -t`. Each holds 545 netCDF files; the `pr` zip also holds one stray macOS resource-fork file, `__MACOSX/._scotese_02_104_26Ma_502pCO2_M4_pr.nc` (slice 104, outside the window, not extracted).

**Extracted slices.** Experiment numbers 12–32: 21 slices × 5 means (M1–M5) × 2 variables = 210 files, 232,177,638 bytes (tas 109.8 MB, pr 122.4 MB), copied byte-identical to `local/climate/hadcm3l/scotese_02/` (git-ignored; `SHA256SUMS` verified after the copy). File names: `scotese_02_<NNN>_<age>Ma_<CO2>pCO2_M<k>_<var>.nc`. No file needed subsetting or regridding.

**Window rule.** The window is 485–383 Ma. Slice 12 (plate age 485, experiment age 485.4) is the oldest slice inside it; slice 32 (385, 385.2) is the youngest, and slice 33 (380) falls outside. Slice 11 (490) is outside. The 21 plate ages match the 21 PaleoDEM slices of `data/eprp/context/paleodem_slices.csv` one-to-one (observed).

**Also pulled (outside the pre-approved two zips).** The 21 BRIDGE annual-mean climatology files `<run>a.pdclann.nc` (1.29 MB each, 27 MB) from paleo.bristol.ac.uk, for the land–sea mask and an independent check; they are in `local/climate/hadcm3l/bristol_pdclann/`. The BRIDGE site states no licence (§7).

### Slices

Stage columns compare each age with `data/timescale.csv` (ICS v2024/12) without converting it; "differs" means the two ages fall in different stages.

| No. | Plate age (Ma) | Experiment age (Ma) | CO2 (ppm) | BRIDGE run | ICS v2024/12 stage at plate age | at experiment age | PaleoDEM map |
|---|---|---|---|---|---|---|---|
| 12 | 485 | 485.4 | 2,513 | teXPt | Tremadocian | Tremadocian | 82.5 |
| 13 | 480 | 481.6 | 2,438 | teXPs | Tremadocian | Tremadocian | 82 |
| 14 | 475 | 475 | 2,308 | teXPr | Floian | Floian | 81.5 |
| 15 | 470 | 470 | 2,210 | teXPq | Dapingian | Dapingian | 81 |
| 16 | 465 | 465 | 2,111 | teXPp | Darriwilian | Darriwilian | 80.5 |
| 17 | 460 | 460 | 2,013 | teXPo | Darriwilian | Darriwilian | 80 |
| 18 | 455 | 455.7 | 1,929 | teXPn | Sandbian | Sandbian | 79 |
| 19 | 450 | 449.1 | 1,799 | teXPm | Katian | Katian | 78 |
| 20 | 445 | 444.5 | 1,708 | teXPl | Hirnantian | Hirnantian | 77 |
| 21 | 440 | 441.2 | 1,643 | teXPk | Aeronian | Rhuddanian (differs) | 76 |
| 22 | 435 | 436 | 1,576 | teXPj | Telychian | Telychian | 75.5 |
| 23 | 430 | 430.4 | 1,531 | teXPi | Homerian | Homerian | 75 |
| 24 | 425 | 425.2 | 1,490 | teXPh | Ludfordian | Gorstian (differs) | 74 |
| 25 | 420 | 421.1 | 1,457 | teXPg | Pridoli | Pridoli | 73 |
| 26 | 415 | 415 | 1,579 | teXPf | Lochkovian | Lochkovian | 72 |
| 27 | 410 | 410 | 2,102 | teXPe | Emsian | Emsian | 71 |
| 28 | 405 | 405 | 1,689 | teXPd | Emsian | Emsian | 70.5 |
| 29 | 400 | 400 | 1,731 | teXPc | Emsian | Emsian | 70 |
| 30 | 395 | 395 | 1,297 | teXPb | Emsian | Emsian | 69 |
| 31 | 390 | 390.5 | 1,093 | teXPa | Eifelian | Eifelian | 68 |
| 32 | 385 | 385.2 | 1,377 | teXpz | Givetian | Givetian | 67.5 |

## 4. Age basis

- **Two ages per slice** (observed in `ExperimentInfo.xlsx`). *Plate Age* is the PALEOMAP map age, in 5-Myr steps. *Experiment Age* is the label the simulation carries (the BRIDGE "Age of Simulation"; file names round it). In `hadcm3l_slices.csv`, `nominal_age_ma` is the Plate Age and `experiment_age_ma` the Experiment Age.
- **Timescale of the Experiment Age: not stated.** I checked the arithmetic against the GTS2012 stage bases in `data/eprp/context/timescale_stage_bounds.csv`. Twelve ages (slices 13 and 18–26, 31, 32) equal a stage midpoint, or for slices 21, 23 and 24 a stage-pair midpoint, on that scale to within 0.06 Myr (e.g. 449.1 = midpoint of Katian, 453.0–445.2; 444.5 = Hirnantian with a Rhuddanian base of 443.8; 441.2 = Rhuddanian plus Aeronian). The other nine equal 5-Myr map ages (475, 470, 465, 460, 410, 405, 400, 395) or the Cambrian–Ordovician boundary (485.4). Inferred: the Experiment Age is a GTS2012-era stage midpoint where the slice stands for a stage, and the map age otherwise.
- **Mismatches to carry.** (a) The project's stages are ICS v2024/12, which shifted Early Devonian bases by up to 3 Myr; the stage column above is a comparison, not a conversion. (b) Slice 27 has Experiment Age 410 in `ExperimentInfo.xlsx` and in the file name, but the BRIDGE list says 409 Ma and the PaleoDEM description age is 409.2 (Pragian on GTS2012); on ICS v2024/12 both 409.2 and 410 are Emsian. (c) Slices 21 and 24 change stage between plate age and experiment age. (d) PhanDA itself is on GTS2020 and picks two slices per stage (`hadcm3l_phanda_stage_slice_map.csv`, decoded from `3_GlobalFiles/PriorInfo/ExpNo.mat` in the PhanDA repository, commit 9f06c0d976, no licence stated); PhanDA's stage bounds differ from `data/timescale.csv` in the Devonian.
- Use the plate age when joining to the PaleoDEMs and to the Balembois fields of `data/eprp/` and the experiment age when joining to proxy or stage data on a GTS2012-era scale.

## 5. File contents

Observed from the files (`hadcm3l_slices.csv` has one row per file):

- **Format.** NetCDF4 classic; written by CDO and NCO in 2020 from the BRIDGE monthly series.
- **`tas` files.** Contain `temp_mm_1_5m` (original, float32, K, dimensions month × 1 × lat × lon, lat 90 to −90, lon 0 to 356.25) and `tas` (float64, no units attribute, dimensions month × 1 × lon × lat, lon −180 to 176.25). The two hold identical values: I checked every file (maximum absolute difference 0.0 K after transposing and rolling the longitude by 48 columns; `hadcm3l_qc.csv`). `tas` is the PhanDA copy. Units are K.
- **`pr` files.** Contain `precip_mm_srf` (original, float32; the `units` attribute says "kg m-2", the `long_name` says kg m-2 s-1), `pr` (float64, the PhanDA copy, same layout as `tas`), and two PhanDA anomaly fields (`pr_anomaly`, `prln_anomaly`, 96 × 73). `pr` equals `precip_mm_srf` × 31,536,000 exactly in every file, so **`pr` is in mm per year, as an annual rate (365 × 86,400 s) applied to each monthly mean**, not mm per month.
- **Grid.** 96 longitudes × 73 latitudes (3.75° × 2.5°), poles included. No land–sea mask, orography, vegetation or soil field is in either file type.
- **Time.** 12 values: a monthly climatology of one 20-yr block, on the model's 360-day calendar (`days since 1850-12-00`, so all months have equal length). The file history shows the five blocks M1–M5 are months 1–240, 241–480, 481–720, 721–960 and 961–1200 of the last 100 model years. All five come from one continuous run, so they sample decadal variability, not independent ensemble members.
- **Labelling.** Slices are labelled by experiment number, age and CO2 in the file name; there are no stage labels (stages enter only through the PhanDA map).

## 6. Land summary and method

`hadcm3l_land_summary.csv`, one row per slice. Derived columns carry the prefix `derived_`.

1. **Land mask.** Cells where the BRIDGE soil-moisture field (`sm_mm_soil`, annual-mean climatology of the same run) is defined. Its footprint is the complement of the sea-evaporation field (`evapsea_mm_srf`) in 20 slices; slice 14 has one cell (35° N, 180° E) in neither field, treated as sea (`hadcm3l_qc.csv`). The mask is a model land–sea mask (not PaleoDEM elevation regridded).
2. **Area weights.** Per cell, sin(north edge) − sin(south edge) × 3.75° in radians × R², R = 6,371 km, with half-height polar cells; the weights sum to 4πR².
3. **Annual means.** Mean of the 12 months for each block, then the mean of M1–M5; `_min_over_M` and `_max_over_M` give the range of the five block means.
4. **Land means.** Area-weighted over land cells: `derived_land_tas_c` (°C) and `derived_land_pr_mm_yr` (mm/yr, as supplied in `pr`). `derived_gmst_c` is the area-weighted mean 1.5 m air temperature over the whole globe, not a blended sea-surface and air product.
5. **Heavy-snow land cells (heuristic).** Land cells whose BRIDGE annual-mean lying-snow mass exceeds 5,000 kg m-2. In the 21 slices that field is bimodal: below 500 kg m-2 in 98% of land cells, at least 10,000 in ice-sheet cells (768 cells hold exactly 50,000), and 67 of about 30,000 land-cell values fall between 500 and 10,000. I read these cells as permanent land ice or snow; Valdes et al. (2021) prescribe land ice from the Scotese reconstructions. The `derived_icefree_` columns exclude them. This identification is inferred from the field's distribution, not from an ice mask.

Headline results (all derived; area-weighted):

| No. | Plate age (Ma) | Land area (10^6 km2) | Heavy-snow land cells | Land tas (°C) | Ice-free land tas (°C) | Land pr (mm/yr) | Ice-free land pr (mm/yr) | GMST (°C) |
|---|---|---|---|---|---|---|---|---|
| 12 | 485 | 83.64 | 0 | 19.17 | 19.17 | 865 | 865 | 20.9 |
| 13 | 480 | 83.54 | 0 | 19.04 | 19.04 | 876 | 876 | 21.01 |
| 14 | 475 | 82.75 | 0 | 21.19 | 21.19 | 938 | 938 | 21.57 |
| 15 | 470 | 83.55 | 0 | 20.58 | 20.58 | 944 | 944 | 20.92 |
| 16 | 465 | 85.8 | 0 | 21.15 | 21.15 | 939 | 939 | 20.83 |
| 17 | 460 | 85.81 | 0 | 21.44 | 21.44 | 931 | 931 | 20.86 |
| 18 | 455 | 87.09 | 0 | 21.4 | 21.4 | 929 | 929 | 20.87 |
| 19 | 450 | 87.72 | 961 | 5.08 | 23.14 | 834 | 1026 | 17.32 |
| 20 | 445 | 89.73 | 976 | 5.55 | 23.33 | 848 | 1048 | 17.17 |
| 21 | 440 | 93.78 | 480 | 16.59 | 19.05 | 868 | 898 | 18.8 |
| 22 | 435 | 87.71 | 512 | 14.28 | 16.97 | 874 | 909 | 18.69 |
| 23 | 430 | 73.4 | 422 | 17.14 | 19.28 | 984 | 1016 | 19.67 |
| 24 | 425 | 76.13 | 0 | 18.9 | 18.9 | 1064 | 1064 | 20.48 |
| 25 | 420 | 77.92 | 0 | 17.58 | 17.58 | 1093 | 1093 | 20.25 |
| 26 | 415 | 79.28 | 0 | 18.14 | 18.14 | 1065 | 1065 | 21.19 |
| 27 | 410 | 81.22 | 779 | 10.12 | 18.72 | 889 | 1019 | 20.04 |
| 28 | 405 | 81.63 | 308 | 14.41 | 15.38 | 964 | 980 | 20.92 |
| 29 | 400 | 81.2 | 354 | 14.15 | 15.49 | 938 | 960 | 21.06 |
| 30 | 395 | 83.88 | 0 | 15.77 | 15.77 | 998 | 998 | 21.01 |
| 31 | 390 | 83.32 | 0 | 14.54 | 14.54 | 988 | 988 | 20.75 |
| 32 | 385 | 79.76 | 0 | 14.4 | 14.4 | 953 | 953 | 20.33 |

Observations:

- Land covers 14.4–18.4% of the surface (73–94 × 10^6 km²). GMST is 17.2–21.6 °C.
- Land mean tas runs 5.1–21.4 °C including heavy-snow cells and 14.4–23.3 °C excluding them. The low values at 450, 445 and 410 Ma come from large ice-covered areas (30 × 10^6 km² at 450 and 445 Ma, 15.5 × 10^6 km² at 410 Ma). Use the ice-free columns for plant habitat.
- Land precipitation is 834–1,093 mm/yr (865–1,093 ice-free): highest at 425–415 Ma, lowest ice-free at 485–480 Ma and lowest overall at 450 Ma, where ice covers most land cells. Global land means hide the regional structure that F1 and F4 need; the grids carry it.
- Variability between the five blocks is small: up to 0.66 K in land tas and 53 mm/yr in land pr per slice.
- **Prior against posterior.** Against the PhanDA posterior GMST (a private local copy, `data/eprp/local/context/phanda_gmst_co2_window.csv`, via the stage–slice map), the `scotese_02` GMST is cooler in 16 of 17 comparable stages (the Givetian slices lie outside the window). The prior range is 18.0–21.3 °C; the posterior medians span 19.5–34.0 °C, with a median difference of +6.4 °C, 10–11 °C from the Tremadocian to the Darriwilian and 13–14 °C at the Pridoli and Ludfordian. (The posterior values are not redistributed here.)

**Checks (`hadcm3l_qc.csv`).** The mean of M1–M5 differs from the BRIDGE 100-yr climatology by at most 0.055 K in tas and 41 mm/yr in pr, except slice 19 where the two agree to 0.0002 K; I infer the BRIDGE annual file for the other slices was averaged over a different 100-year window from the final 100 years used in the Zenodo files (months 22789–23988 of the series); I did not establish the BRIDGE window. For teXPk the CO2 on its BRIDGE page (1,643.28 ppm) equals the `ExperimentInfo.xlsx` value.

## 7. Other land-climate sources

Full table: `other_sources.csv` (24 rows: coverage, variables, resolution, licence, size, URL, access route). Nothing over 1 GB was pulled, and apart from the 27 MB of BRIDGE masks and one 8 MB probe of a Pohl file (not kept) nothing beyond the two zips.

- **The other seven experiments** are all in the same record: 1,418–1,435 MB each for the four variables, 814–823 MB for `tas` plus `pr` (11.4 GB in all).
- **BRIDGE pages (Valdes et al. 2021).** `https://www.paleo.bristol.ac.uk/ummodel/scripts/papers/Valdes_et_al_2021.html` links `scotese_02` and `scotese_spinupa`. Land fields can be downloaded by plain HTTP without a login: per run, an annual-mean file of more than 40 variables including soil moisture, evaporation components, runoff, relative humidity, soil temperature and snow, plus monthly climatologies and full monthly series (observed for one run: 518 MB for precipitation, 346 MB for temperature). **Terms: none stated** on the pages; the usage PDF says runs are "potentially made public", warns that descriptions are brief, and asks users to contact BRIDGE to check a run before use; the paper is CC BY 4.0 and the derived Zenodo files are CC BY 4.0. Directory listings are forbidden (HTTP 403).
- **Gridded PhanDA posterior fields.** None found on Zenodo or in the repository; the published posterior products are GMST and CO2 percentiles, the GMST ensemble and latitudinal gradients per stage (EPRP holds them).
- **FOAM, CESM and others with public land fields.**
  - Pohl et al. (2022), FOAM, Zenodo 6620748, CC BY 4.0, 711 MB: monthly precipitation, evaporation, runoff, P − E, top-soil temperature, topography and Köppen–Geiger classes at 480, 460, 440, 420 and 400 Ma; per-slice netCDF 8.3 MB. This is the most direct complement to HadCM3L for F1 and a different model family. Related FOAM sets: Zenodo 5780097 (4.9 GB, fixed boundary conditions) and 7220854 (1.4 GB, slab model with Foster CO2).
  - Li et al. (2022), CESM1.2.2, figshare, CC BY 4.0, 754 MB: ten slices (480–390 Ma at 10-Myr steps) at 0.9° × 1.25°, with land fraction and surface geopotential; CO2 tuned to the GMST of Scotese et al. (2021). Doi: 10.1038/s41597-022-01490-4.
  - Brugger et al. (2019), CLIMBER3alpha, GFZ, CC BY 4.0, Devonian only, coarse (22.5° × 7.5° atmosphere). Doi: 10.1029/2019PA003562.
  - Held by EPRP, not duplicated: FOAM at 440 Ma (Pohl 2024 deposit, Zenodo 10610771) and Balembois et al. (2025) sea-surface temperature fields (figshare 27201498; no land fields).
  - Not located or unverified: a CESM–ISSM Late Ordovician run (Sun et al. 2026 preprint), CESM–BIOME4 vegetation (EGU 2023 abstract), and HadCM3L with slice-specific plant functional types (EGU 2025 abstract). No Zenodo or Bristol record of Palaeozoic HadCM3L runs with early-plant vegetation was found.

## 8. Caveats

1. **Priors, not reconstructions.** No proxy constrains these runs; the PhanDA posterior moves the same ensemble toward δ18O-based sea-surface temperatures and is substantially warmer (§6). Treat absolute land temperatures as one model's response to a prescribed CO2 curve and geography.
2. **Vegetation and soil.** The files carry no vegetation. Valdes et al. (2021), as I read the text, use a uniform medium-loam soil, and the paper does not clearly say whether the dynamic vegetation component was active; a 2025 conference abstract says the runs use modern plant functional types. There is no early-land-plant representation, which matters for albedo, evapotranspiration and runoff in F1. A 2025 conference abstract on HadCM3L Phanerozoic runs says this is a limitation being addressed (secondary; not verified).
3. **Land ice.** Prescribed from Scotese reconstructions. Eight slices contain heavy-snow cells (450, 445, 440, 435, 430, 410, 405 and 400 Ma); land means must be read with the ice-free columns.
4. **Resolution.** 3.75° × 2.5° gives about 1,360–1,650 land cells per slice. Orography is smoothed; this is not a regional-scale source.
5. **Dating.** Slices are 5-Myr maps carrying stage-midpoint labels; the Early Devonian maps are labelled on a scale that differs from ICS v2024/12 by up to 3 Myr (§4).
6. **Missing land-moisture fields in the Zenodo zips.** `tas` and `pr` alone give no P − E, soil moisture or runoff; those are in the BRIDGE annual and monthly files and in Pohl et al. (2022).
7. **The BRIDGE mask and snow fields have no stated licence.** Only derived numbers (the land and ice-free summaries) are committed; the files stay in `local/`.
8. **Spin-up.** teXPk ran 2,000 model years with 1,900 of spin-up (BRIDGE page); the other slices were not checked. The ocean may not be fully equilibrated.

## 9. Not done

- No other experiment was downloaded, and the `so` and `tos` variables were not pulled.
- No regional or latitude-band summaries, and no stage-level aggregation (the PhanDA stage map is given as a separate table).
- No comparison with Pohl et al. (2022) or Li et al. (2022) fields; no pull of any other source.
- The Update A and Update B changes were not read (the Judd et al. manuscript PDF is behind HTTP 403 for a plain user agent; I did not work around it).
- BRIDGE terms were not queried with the group; no contact was made.
- No orography or land-sea mask file was searched for in the BRIDGE ancillary folders.

## 10. Reproducing

All commands run from `data/external/scripts/`; Python scripts carry inline `uv` metadata.

```bash
ssh deep-server 'bash -s' < climate_fetch_hadcm3l.sh          # xlsx and the two zips, md5 checked, provenance logged
ssh deep-server 'bash -s' < climate_extract_hadcm3l.sh        # slices 12-32, SHA256SUMS
rsync -a deep-server:/data/codex/silurian_plants/raw/hadcm3l/extracted/scotese_02/ ../local/climate/hadcm3l/scotese_02/
uv run climate_hadcm3l_info.py EXPERIMENTINFO.xlsx EXPNO.mat ../climate   # experiment info; the PhanDA stage-slice map goes to ../local/climate/ (source states no licence)
CODES=$(awk -F, '$1=="scotese_02" && $2>=12 && $2<=32 {print $5}' ../climate/hadcm3l_experiment_info.csv | tr '\n' ' ')
ssh deep-server "bash -s -- $CODES" < climate_fetch_bristol_pdclann.sh
uv run climate_hadcm3l_tables.py scotese_02                  # slices, land summary, QC
cp ../local/climate/hadcm3l/PROVENANCE.tsv ../climate/hadcm3l_raw_provenance.tsv   # after rsync of PROVENANCE.tsv from deep-server
uv run climate_doi_check.py
uv run climate_manifest.py
```

`EXPNO.mat` is `3_GlobalFiles/PriorInfo/ExpNo.mat` in the PhanDA mirror (`deep-server:/data/paleodata/climate-forcing/phanda/raw/2026-03-09_9f06c0d976/`); `other_sources.csv` was written by hand from the Zenodo, figshare, Crossref and DataCite APIs and the pages linked in it.

## 11. Access limits

- Zenodo: open; about 0.25 MB/s per connection from `deep-server`, so the downloads used four range requests per file.
- BRIDGE site: open, no login; directory listings 403; no licence statement.
- The accepted manuscript of Judd et al. (research-information.bris.ac.uk) returned HTTP 403 to a plain user agent.
- The Nature Scientific Data article page for Li et al. (2022) redirects to a cookie handshake; I read the open-access full text through Europe PMC instead.
- No credentials, accounts or tokens were used.
