# Material extracted from EPRP

This folder holds references, data and pointers drawn from EPRP (Barry's Extinction and
Paleontology Research Programme, private repository `BWBrook/eprp`) for this project's use. EPRP
is a source, not a collaborator: nothing here was written back to it, and its development
happens elsewhere. Extracted by Claude Opus 5.5 (Anthropic) on mac-mini, 2026-10-26, with three
Claude Sonnet 5.5 subagents for the library, record and context areas. Files here are uncommitted
until Barry or the project session decides otherwise.

## Provenance

- EPRP repository state: commit `ac42dfb` of `/Users/bwbrook/git/eprp` (read-only checkout,
  updated only by fast-forward).
- Bulk data: EPRP's mirror on `deep-server:/data/paleodata/<id>/`, filtered there. Each area's
  README names the snapshot versions and input checksums.
- `MANIFEST.tsv` lists every delivered file with its source, source version, licence, generating
  script, row count, SHA-256 and extraction date. It is rebuilt and checked against the files on
  disk by `python3 scripts/build_manifest.py` (run from this folder).
- Scripts in `scripts/` reproduce each extraction from the same EPRP state and snapshots.

## Layout

| Folder | Contents |
| --- | --- |
| `library/` | References from EPRP's literature library, screened for relevance; `references.tsv` is the main table |
| `record/` | Fossil-record data: PBDB plant occurrences, collections and references; card-taxa summary; intervals mapped to the project's timescale; Macrostrat rock record |
| `context/` | Earth-system context: climate and carbon series, palaeogeography, relevant deposits held by EPRP |
| `pointers/` | What EPRP offers beyond data: adjacent register questions, community question lists, software with EPRP's validation findings |
| `scripts/` | Extraction scripts, `area_*.py`, and `build_manifest.py` |
| `local/` | Gitignored. Material whose licence forbids redistribution or states none, publisher full texts held for local reading, and large rasters |

## What the first pass found

- **References** (`library/`): 426 works kept from 7,959 candidates. 281 are on plants and their
  setting, led by weathering and CO2, arthropods and herbivory, and plant diversity; 145 are
  methods, mainly range estimation, fossilised birth–death, rock-record bias and molecular
  dating. 367 are not yet cited by the project. All 418 DOIs resolve in Crossref with matching
  title and year; 8 older works have none. 97 open full texts are in `local/library/text/`.
- **Occurrences** (`record/`): 3,704 PBDB occurrences overlapping 485–383 Ma. 2,628 are core
  land-plant records in 611 collections; 1,076 are flagged algae, acritarchs and fungi. The
  file comes with 523 source references. The snapshot (2026-10-23) uses the same stage ages as
  `../timescale.csv`.
- **Rock record** (`record/`): 5,932 Macrostrat units, 94% North American and 88% marine. It is
  a regional sampling proxy, not a global one.
- **Context** (`context/`, `local/context/`):
  - temperature and CO2 series: PhanDA, PhanSST, Song 2021, a GMST derived from Scotese 2021;
  - carbon-cycle events and large igneous provinces;
  - 21 PALEOMAP elevation maps for the window;
  - an index of 27 plate models;
  - 31 relevant deposits from EPRP's collection, among them TREED's code.
- **Pointers** (`pointers/`): one adjacent register question (Q-018, plant mass extinction);
  community questions on terrestrialisation; and EPRP's validation findings for the
  range-estimation and preservation tools that F3 would use.

Findings that bear on the framings:

- **PBDB alone cannot calibrate F3.** Core occurrences thin out sharply before the Emsian (259
  across all earlier stages, against 966 in the Givetian alone). There are none in the
  Tremadocian to Dapingian, and only one Ordovician spore record. A dispersed-spore compilation
  from the literature would be needed.
- **Temperature and CO2 series are on GTS2020 or GTS2012, not ICS v2024/12.** Devonian
  boundaries differ by up to 3 Myr. Nothing has been converted; `context/README.md` tabulates
  the offsets.
- **EPRP holds no CO2 or O2 proxy compilation.** PhanDA's CO2 is a data-assimilation output,
  not an independent proxy series.
- **The library is thin on core palaeobotany.** It has few spore, Rhynie Chert and early-taxon
  works, and lacks several standard reviews the project already cites. It is strong on methods
  and Earth-system links.

## Using it

- Read an area's README before using its files: each states filters, caveats and what was not done.
- These are inputs, not verified facts for the cards. The project's conventions still apply:
  DOIs must be checked against Crossref before use (the DOIs in `library/` come from OpenAlex via
  EPRP), and ages come from `../timescale.csv`. Where a source uses a different timescale, the
  area README says so and nothing has been silently converted.
- Do not hand-edit extracted tables; change the script and rerun it.
- `local/` must stay out of git: the repository has a GitHub remote.
