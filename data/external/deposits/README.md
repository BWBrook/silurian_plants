# Published datasets, supplements and code deposits

Located and mirrored on 2026-10-27 for the evidence base (`docs/sources.md`, rows marked "(EPRP)"). One row per work, with
status, sizes and paths, is in `deposit_index.csv`; every mirrored file is in `MANIFEST.tsv` with its sha256. Raw copies,
with the mirroring tool's provenance (URL, retrieval time, provider checksum), are on `deep-server` under
`/data/codex/silurian_plants/raw/deposits/<id>/<UTC stamp>/`.

## Result

25 target works (the 24 with DOIs in the brief, whose Hooper entry appears in two lists, plus Ball's thesis, which has none),
2 rows for the coordinator's addition (Shu et al. 2025 data and code, both mirrored), and 12 related deposits found on the
way. Status of the 25 targets (a 'mirrored' work may keep its files over 20 MB in `local/`):

| Status | Works |
|---|---|
| mirrored (14) | Xiong 2013, Silvestro 2015, Clark 2023, Claisse 2025, Hooper 2026, Morris 2018, Harris 2022, Foster 2017, Dahl 2022 (ERDA archive missing), Witkowski 2018, Yuan 2023, Avila 2025, Cai 2026, Wu 2026 |
| local-only (6) | Capel 2021, Capel 2022, Cascales-Minana 2016, Ball 2022, Krause 2018, Glasspool & Scott 2010 |
| access-limited (4) | Capel 2023, Toledo 2021, Lenton 2016, Haq & Schutter 2008 |
| not-found (1) | Kenrick & Crane 1997 |

Related deposits: mirrored (6) COPSE (Mills), Cai COPSE, Grossman & Joachimski, DM-SED, van der Meer, Capel 2025; local-only (4)
COPSE reloaded (Daines), Veizer 1999, Prokoph 2008, Veizer & Prokoph 2015; on-request (1) the McArthur Sr look-up table;
link-only (1) Franziskakis et al. 2025 (1.30 GB, over the size limit).

Most valuable items:
- **Character matrices**: Clark et al. 2023 (548 characters, 410 extant and fossil species, with time-calibrated trees); Hooper et al. 2026 (27 spore characters, 50 taxa, calibrations in Supplementary Table 4); Claisse et al. 2025 (44 zosterophyll-centred taxa, 42 characters).
- **Diversity compilations as tables**: Capel 2021 and 2022 genus lists (stage-level ranges, localities, references), Capel 2025 species matrix, Cascales-Minana 2016 genus list, Silvestro 2015's raw PBDB download, Ball 2022 spore counts.
- **Timetree inputs**: Morris 2018 alignments and the PNAS SI Appendix (calibrations); Harris 2022 alignments, trees, MCMCTree posteriors and dated trees.
- **Proxies**: Foster 2017 CO2 compilation and LOESS fit; Witkowski 2018, Dahl 2022 CO2 data; Cai 2026 geochemistry compilation (21,697 rows); Yuan 2023 Hg isotopes; Avila 2025 Sr; Wu 2026 Li; GEOCARBSULFOR and COPSE code; the Veizer, Prokoph, Grossman & Joachimski and DM-SED isotope compilations.
- **Acritarchs**: Global Acritarch Database (115,860 rows; project's method template for building on Palynodata) and its code.

## Method

1. DOIs from `docs/primer.md`, `docs/precedents.md` and `docs/framings.md`; Toledo 2021 and Claisse 2025 were not in them and were identified by Crossref author and title search (see the Toledo caveat in the index). Every DOI was checked against Crossref (`crossref_check.tsv`).
2. EPRP's mirror was checked first: `deep-server:/data/paleodata/register-deposits/` (94 directories) and its `snapshots.tsv` hold none of these works (the one Foster entry is Foster et al. 2023, an unrelated paper).
3. Data availability: publisher landing pages where they allowed plain requests (Nature, PLOS, Copernicus, White Rose, ORBi, data.bris); otherwise Europe PMC full text and its `supplementaryFiles` endpoint (open-access articles in PMC), DataCite and the Dryad, Zenodo and Figshare search APIs (query by DOI and title), the MorphoBank public service (all 2,178 published projects), TreeBASE PhyloWS, GitHub, and Elsevier's public supplement CDN (file names `mmc<N>` guessed from the PII and checked by HEAD request).
4. Mirroring with EPRP's `data_mirror.py` (copied unchanged to `scripts/deposits_data_mirror.py`; Zenodo, Figshare and GitHub files verified against provider checksums; plain URLs checked by Content-Length and hashed) and EPRP's `other_repos.py` (Mendeley, checked against the provider's sha256). No credentials, accounts or API keys were used. Dryad was not needed (no target is on Dryad). A plain user agent without contact details was used throughout.
5. Mac copies by `scripts/deposits_build.py` (re-hashes every file after copying); index by `scripts/deposits_index.py`.

## Licence and placement decisions

Rule from the brief: tracked in `deposits/<id>/` when the licence allows redistribution and the file is under 20 MB; otherwise `local/deposits/<id>/` (git-ignored).

- **Tracked, CC BY / CC0-class / Apache**: Foster, Dahl (data tables), Hooper ESM, Claisse, Silvestro, Xiong, Avila, Cai, Wu, Capel 2025, Grossman & Joachimski, van der Meer, COPSE (Mills, Apache-2.0), Cai COPSE, Shu data (reference list) and code, Krause Zenodo and ESM, Morris README, Harris (files under 20 MB).
- **Tracked and flagged as NC**: Witkowski 2018 and Yuan 2023 (CC BY-NC 4.0); Clark 2023 and Hooper 2026 data (data.bris "Non-Commercial Government Licence for public sector information", treated like CC BY-NC: a judgement, as the NCGL is not on the brief's list). `MANIFEST.tsv` descriptions carry "[NC licence: tracked and flagged]".
- **Local by size although CC BY**: the Shu CSV (54 MB), DM-SED (39 MB), the Morris alignment zip (38 MB), Hooper's divergence-time zip (65 MB), Dahl 2022's Supplementary Information PDF (43 MB), Harris's large tarballs and posteriors (481 MB in all).
- **Local by licence**: Elsevier supplements (Capel 2021 and 2022, Cascales-Minana 2016, Prokoph 2008, Veizer & Prokoph 2015; Capel 2022 is CC BY-NC-ND), Ball 2022 (CC BY-NC-ND), the Morris PNAS SI Appendix (CC BY-NC-ND), Glasspool & Scott ESM (Nature copyright), Veizer 1999 (none stated), GitHub code with no licence (Krause, Daines COPSE, Harris ALE_methods), the Capel thesis (none stated).
- Tracked total is 145 MB (Harris 47 MB, Cai COPSE 17 MB, Hooper ESM 14 MB are the largest); local is about 1.0 GB. Decide whether Harris's 47 MB belongs in git.

## Timescale bases (each series keeps its own; nothing was converted or repaired)

| Series | Basis | Evidence |
|---|---|---|
| Foster 2017 CO2 | GTS2012 | stated in the notes sheet and the paper |
| Dahl 2022 CO2 | GTS2012 implied by 'Age(2012)' columns; one flora dated on GTS2020 | column header; paper text |
| Witkowski 2018 | not stated (Ma column) | searched |
| Capel 2021 | ICS chart 2019 | postprint text |
| Capel 2022 | ICS v2020/03 | thesis chapter that reprints it (the journal text was not read) |
| Cascales-Minana 2016 | GTS 2015 | range-chart header |
| Xiong 2013 | ICS chart 2013-01 | paper text |
| Claisse 2025 | ICS chart (Cohen et al. 2013) | paper text |
| Avila 2025 Sr | GTS 2020 | column header |
| Grossman & Joachimski 2022 | GTS2020 | paper text |
| Shu 2025 | literature ages kept as published; gaps filled from ICS Dec 2024 (v2024/12, the project's own basis) | paper text |
| Veizer 1999 | Harland et al. 1990 | the Ottawa page |
| Prokoph 2008, Veizer & Prokoph 2015 | GTS2004 (and GTS2012 columns in the 2015 tables); the 2008 database sheet gives only 'Age (Ma)' | column headers |
| Morris 2018 calibrations | ICS v2016/10 | SI Appendix |
| Harris 2022, Clark 2023, Hooper 2026 | not stated in the text or README searched | searched |
| Silvestro 2015 | PBDB interval ages as of about 2014 (inferred) | not stated |
| Glasspool & Scott 2010 | 10 Myr bins; version not stated | searched |
| Cai 2026, Yuan 2023, Wu 2026, Ball 2022, DM-SED, COPSE, GEOCARBSULFOR | not determined or not stated | |

## Access limits Barry could resolve

- **Wiley** (403 to automated access): Toledo et al. 2021 supporting information (matrix); Capel et al. 2023 data statement and supplement; Wu et al. 2026 data statement (the data were found on Mendeley). Library access or a browser download; or ask Tomescu (Toledo) and Capel.
- **Science and PNAS** (403): Haq & Schutter 2008 online material; Lenton et al. 2016 SI Appendix. Library access. (PNAS SI of Morris 2018 and Science Advances SI of Yuan and Witkowski came through Europe PMC.)
- **HAL** (proof-of-work page) holds author versions of Capel 2021, 2022 and 2023; the Capel thesis at Lille, mirrored, covers the same chapters.
- **University of Copenhagen ERDA** (`erda.ku.dk`) timed out from this Mac and from `deep-server`, and refused a WebFetch, on 2026-10-27: Dahl et al. 2022's model archive (doi 10.17894/ucph.214a6434-b7eb-4e62-aaac-afefc1247da4) was not retrieved. Retry later.
- **On request**: the McArthur et al. LOWESS Sr look-up table (j.mcarthur@ucl.ac.uk per the UCL abstract); Capel et al. 2022 raw diversity and sampling data (per the thesis text).
- **Not digital**: the Kenrick & Crane 1997 character matrix is printed in the book (library copy).
- **Size**: Franziskakis et al. 2025 sea-level and palaeogeography maps (Zenodo 15396265, 1.30 GB) is over the limit and needs authorisation.
- **Unpublished**: MorphoBank P4938 (Claisse 2025) is reported 'not found or not published'; the matrix is in the paper's Supplementary Data.

## Surprises and caveats

Observed:
- GEOCARBSULFOR code and data are public on the author's GitHub (and a later version on Zenodo), although the paper says 'upon request'.
- Veizer's isotope-database page (Ottawa) returns 404; the files came from the Internet Archive capture of 2024-07-19 (an archive copy of the author's files, no licence stated).
- Capel et al. 2021, 2022 and Cascales-Minana 2016 deposited no repository dataset; their tables are Elsevier supplements.
- Hooper et al. 2026's data.bris record (published 2026-10-07) predates the paper (2026-10-22).
- Two Mendeley datasets of the same title (Wu): published 2025-12-12 and 2026-07-08; the Cai 2026 Figshare record is duplicated (29848700 and 31080109, identical files).
- Avila et al. 2025's Table S1 holds Sr only; its conodont d18O is from the Grossman & Joachimski compilation, mirrored separately.

Data availability statements: read for Xiong, Silvestro, Ball (record), Clark, Claisse, Hooper, Morris, Harris, Foster, Dahl, Witkowski, Krause, Yuan, Cai and Shu; Capel 2021 (postprint) and Capel 2022 (thesis chapter that reprints it) only second-hand. Not read, because the publisher page was blocked, closed or unfetched: Capel 2022 (journal), Capel 2023, Cascales-Minana 2016, Toledo 2021, Lenton 2016 (the accepted manuscript has none), Glasspool & Scott 2010, Haq & Schutter 2008, Avila 2025 (supplements found through Figshare) and Wu 2026.

Inferred, not verified:
- The Wu 2026 datasets belong to the JGR paper (title, topic and site match; the paper's data statement was not readable) and which of the two it cites is unknown.
- Toledo et al. 2021 is the paper meant by the brief (the only Crossref match for the author, year and topic).
- COPSE in `copse-mills` and `copse-reloaded-daines` is the lineage of the Lenton 2016 model, not the 2016 release.
- Contents were checked by sheet headers and row counts only; no table was validated against its paper. Several are PDF tables (Xiong 2013, Glasspool & Scott 2010, the Capel thesis, Ball's thesis) and need extraction before use.
- One or two papers (Capel 2022's journal text, Capel 2023, Hooper's ref. 14) were not read directly; see the index notes.

## Not done

- ERDA archive (Dahl 2022) not retrieved; Toledo, Haq & Schutter, Lenton SI, Capel 2023 supplements not obtained.
- Not mirrored: Franziskakis et al. 2025 (1.3 GB); `dschrempf/mcmc-date` (GPL-3.0 dating program, 84 MB, not a data deposit); Royer's GEOCARBSULF code (Figshare 902207) and Tostevin & Mills's COPSE parameter files (Figshare 12258185), which are leads for the O2 models; the Elsevier author postprints at ORBi and HAL; the StabisoDB site; PyRate input files for Silvestro 2015.
- The Yuan 2023 R code (.rar) was not opened; Hooper's 65 MB MCMCTree zip was not unpacked.
- No table was extracted from PDFs; no data were converted, repaired or merged; no EPRP or other project files were touched; no git commands were run.

## Files

- `deposit_index.csv`, `MANIFEST.tsv`, `crossref_check.tsv`, this README.
- `<id>/` tracked deposit folders (each with `PROVENANCE.json`); `../local/deposits/<id>/` for files not tracked.
- Scripts in `../scripts/`: `deposits_crossref_check.py`, `deposits_data_mirror.py` (EPRP copy), `deposits_other_repos.py` (EPRP copy), `deposits_mirror_run.sh` (run on deep-server, one item per deposit), `deposits_catalogue.py`, `deposits_build.py`, `deposits_index.py`.
- Reproduce: `bash deposits_mirror_run.sh <item> ...` on deep-server (needs the two EPRP copies beside it), then `uv run --with openpyxl --with xlrd python3 deposits_build.py`, then `python3 -I deposits_index.py`.
