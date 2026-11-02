# Third-party material and its licences

The project's own code is under the [MIT Licence](LICENSE) and its own text, figures and derived
tables under [CC BY-SA 4.0](LICENSE-CONTENT). That covers material authored for this project only.
Everything below keeps the licence of its source. Where a table or folder mixes sources, the
licence stated per record or per row in that folder's `MANIFEST.tsv` and README governs, and the
`CC BY-SA` of this repository adds no rights to it and removes none. Items marked **NC** allow
non-commercial use only; do not reuse them commercially.

This repository does not contain third-party datasets, supplements or code deposits, or journal
articles, theses or their supplements. Deposits are fetched by script (below) into git-ignored
folders on the user's own machine.

## Fetched, not redistributed

| What | Source | Licence | How to obtain |
|---|---|---|---|
| 27 published data, supplement and code deposits (Harris 2022, Cai 2026, Hooper 2026, Silvestro 2015, Dahl 2022, Grossman 2022, van der Meer 2025, Claisse 2025, Xiong 2013, Avila 2025, Shu 2025, Krause 2018, Foster 2017, Capel 2025, Morris 2018, Wu 2026 and others, listed in `data/external/deposits/deposit_index.csv`) | Figshare, Zenodo, Europe PMC, Springer Nature, PLOS, data.bris, Mendeley Data, GitHub | CC BY 4.0 for most; Apache-2.0 for COPSE (Mills) and Krause's Zenodo code; **NC** for Witkowski 2018 and Yuan 2023 (CC BY-NC 4.0) and for the two data.bris deposits (Clark 2023, Hooper 2026), which carry the UK Non-Commercial Government Licence; each row's licence is in `data/external/deposits/MANIFEST.tsv` | `python3 data/external/scripts/deposits_fetch.py` writes them to `data/external/local/deposits/`, checking every file against the sha256 in the manifest |
| 11 Earth-system and modelling deposits (Alroy, Crampton, Franeck, Freitas, Holland, Malanoski, Stigall on Dryad; Balembois, Cooper, Rogger 2024 and 2026 on Figshare and Zenodo) | Dryad, Figshare, Zenodo | CC0 (Dryad), CC BY 4.0 (others; TREED ships its own `LICENSE.txt`) | DOIs, versions and sha256 are in `data/eprp/context/MANIFEST.tsv`; Dryad downloads need a free API account |
| Palynodata Datafile (Palynodata Inc. and White 2008, GSC Open File 5793, doi 10.4095/225704) and the window tables extracted from it | NRCan Open S&T Repository | Open Government Licence - Canada per the current record; the 2008 release bundles an older restrictive end-user agreement. Kept out of this repository to avoid redistributing under that conflict | Put the release zip at `data/external/local/spores/of_5793.zip` and run `data/external/scripts/spores_palynodata.py`; see `data/external/spores/README.md` |
| Wellman, Steemans and Vecoli 2013 supplement (`18680.pdf`) | Figshare doi 10.6084/m9.figshare.3453524 | CC BY 4.0 | download from the DOI to `data/external/spores/wellman2013_supplement/` |
| Journal articles, theses and publisher supplements read under library access | publishers, repositories | their own terms; never committed | listed (bibliographic data only) in `library/closed.tsv` and `docs/closed-literature.csv` |

## Tracked in this repository

| Path | What | Source | Licence |
|---|---|---|---|
| `data/external/specimens/` | GBIF, Atlas of Living Australia mirror and iDigBio specimen records for the study window (`gbif_specimens.csv`, `idigbio_specimens_open_licence.csv`, `specimens_merged.csv` and summaries) | GBIF, ALA and iDigBio data publishers; datasets, DOIs and licences in `gbif_datasets.csv` and `idigbio_recordsets.csv` | Per record: CC0, CC BY or **CC BY-NC**. Of 39,417 merged rows, 4,415 (11%) have an NC effective licence; rows are flagged in `derived_licence_class` and `derived_licence_effective`. Rows with unclear rights are not included. Cite the dataset publishers listed in the dataset tables |
| `data/external/specimens/` (GBIF Backbone placement) | taxon placement of names | GBIF Backbone Taxonomy | CC BY 4.0 |
| `data/eprp/record/` | PBDB occurrence, collection, reference, measurement and opinion tables for the window | Paleobiology Database | CC0 |
| `data/eprp/record/` | Macrostrat unit tables | Macrostrat | CC BY 4.0 |
| `data/eprp/record/` | Australian Stratigraphic Units Database table | Geoscience Australia | CC BY 4.0 |
| `data/eprp/context/` | extracted climate, plate-model and event tables (`rothman2017_events_window.csv`, `scotese2021_gmst_derived_window.csv`, `song2021_*`, `paleodem_slices.csv`, `plate_models.csv`) | Rothman 2017, Scotese 2021, Song 2021, PALEOMAP | Licence per row of `data/eprp/context/MANIFEST.tsv`; the Rothman 2017 table is **NC** |
| `data/external/gbdb/` | Geobiodiversity Database tables for China and overlap checks against PBDB | GBDB (Fan et al. 2020, doi 10.5281/zenodo.4245604) | CC BY 4.0 |
| `data/external/rock-record/` | British Geological Survey unit and polygon-derived tables | BGS DigMapGB-625 and Lexicon | Open Government Licence (v3 per the BGS page); contains BGS materials (c) UKRI. `bgs_geochronology_divisions_used.csv` and `bgs_units_silurian_devonian.csv` carry Lexicon fields with no licence statement found: free access, UKRI copyright, reuse terms unconfirmed, attribution given |
| `data/external/climate/` | HadCM3L land summaries and slices for 485-383 Ma | PhanDA priors (Judd et al. 2024; Valdes et al. 2021) | CC BY 4.0 for the derived numbers. The BRIDGE mask and snow fields have no stated licence and are not redistributed |
| `data/external/library/`, `data/eprp/library/` | bibliographic metadata, screening tables | OpenAlex, Crossref | CC0 |
| `data/spores/`, `data/units/`, `data/occurrences/`, `data/macro/` | spore, occurrence and unit tables compiled for this project from the sources above | project work built on third-party records | CC BY-SA 4.0 for the compilation and annotations; the underlying source records keep the terms above |
| `portal/assets/*.webp` | eight reading-room images | Wikimedia Commons; creator, licence and changes per image in `portal/images.json` | see the image table below |
| `models/griwm_r/` | GRIWM extinction-model R code | adapted from CRIWM by Fred Saltre | MIT (`models/griwm_r/LICENSE`) |

### Portal images

Each image is resized and converted to WebP. Attribution and the change note are in
`portal/images.json`.

| File | Subject | Creator | Licence |
|---|---|---|---|
| `cooksonia.webp` | Cooksonia pertoni, USNM 298794 | Jonathan Chen | CC BY-SA 4.0 |
| `cooksonia-reconstruction.webp` | Cooksonia museum reconstruction | Matteo De Stefano / MUSE | CC BY-SA 3.0 |
| `rhynia.webp` | Rhynia in Rhynie chert | Peter coxhead | CC BY-SA 3.0 |
| `asteroxylon.webp` | Asteroxylon mackiei reconstruction (Hetherington et al. 2021) | Matt Humpage | CC BY 4.0 |
| `prototaxites.webp` | Prototaxites taitii in Rhynie chert | Parasitaxus | CC BY 4.0 |
| `marchantia.webp` | Marchantia polymorpha | Krzysztof Ziarnek, Kenraiz | CC BY-SA 4.0 |
| `phlegmariurus.webp` | Phlegmariurus squarrosus | Krzysztof Ziarnek, Kenraiz | CC BY-SA 4.0 |
| `psilotum.webp` | Psilotum nudum | Forest and Kim Starr | CC BY 3.0 |

## Not in this repository

Material with no licence or a restrictive one stays in git-ignored `local/` folders on the
owner's machines and is not published: Capel 2021 and 2022, Cascales-Minana 2016, Prokoph 2008,
Veizer and Prokoph 2015, theses, publisher supplements, FR2, ICS chart values, BRIDGE masks, BGS
Lexicon prose, PhanDA and PhanSST fields without a stated licence, and Green 2022.
