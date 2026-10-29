# Dispersed spores and other palynomorphs: Palynodata window extract

Extracted 2026-10-27 by Claude Opus 5.5 (Anthropic) on mac-mini for the project's dispersed-spore
gap (framing F3's spore channel, F4). This is an as-is extract: no ages converted, no names
harmonised, no duplicates merged. Building a compilation from it is project work.

## Sources

- **Palynodata Datafile: 2006 version** (Palynodata Inc. & J.M. White 2008, Geological Survey of
  Canada Open File 5793, doi 10.4095/225704). **Licence: Open Government Licence – Canada**, free
  to copy, modify and redistribute with attribution. That is what the current official record
  states (NRCan Open S&T Repository, handle 1845/177682, `rights.license`, checked 2026-10-27), and
  Crossref's licence metadata for the DOI points to the same licence. It supersedes the
  `licence.txt` bundled in the 2008 release (kept in `palynodata_release/` as part of the release),
  which is the restrictive NRCan end-user agreement of the time: internal use on a single
  computer, no redistribution. Do not treat that bundled agreement as binding on this extract.
  Release zip sha256 `5460e39d…70db1a`; raw copy at
  `deep-server:/data/codex/silurian_plants/raw/palynodata/2026-10-27T0038Z/` (not reachable from the Macs), local copy in
  `local/spores/of_5793.zip`, which is what the script reads. The data sit in an Access (JET3) database, `paly.mdb` (sha256
  `eb1fa8c3…cde85c1`), inside the release's `apps/Paly.CAB`; `mdb-export` reads it.
- **Wellman, Steemans & Vecoli 2013**, *Palaeophytogeography of Ordovician–Silurian land plants*,
  Geological Society Memoir 38, ch. 29 (doi 10.1144/M38.29). Supplement (Figshare
  doi 10.6084/m9.figshare.3453524, CC BY 4.0): `wellman2013_supplement/18680.pdf`, 40 pages. It
  lists Ordovician–Silurian dispersed-spore assemblages by age and region with species and
  references, compiled by P. Steemans, omitting assemblages judged poorly dated, poorly preserved
  or doubtfully identified. Tremadoc–Arenig entries are spore-like palynomorphs of questionable
  affinity. Left as the PDF; tabulating it belongs to the compilation.

## What Palynodata is

An index of palynomorph taxa reported in 22,152 documents of the palynological literature, built
from 1974 by an industry and academic consortium and released by Canada in 2008. The last
literature entered dates from 2006. Each `TAXON` row is one taxon in one document, with a region
as text, the oldest and youngest age names assigned, and numeric start and end ages from
Palynodata's own age table. It has no coordinates.

## Files

| File | Rows | Contents |
| --- | ---: | --- |
| `palynodata_taxon_window.csv` | 109,687 | Every `TAXON` row in the window, all microfossil types, all original columns, plus `derived_` columns |
| `palynodata_documents_window.csv` | 3,540 | `NewEng` citations for every document with a window row (title, authors, year, journal, pages, global age, lithology, location), plus window row counts by type and `derived_window_has_spores` |
| `palynodata_lithostr_window.csv` | 4,015 | Formations named by those documents (`LITHOSTR`) |
| `palynodata_theagetable.csv`, `palynodata_agetable.csv`, `palynodata_age_change.csv` | 2,132; 2,117; 2,113 | Palynodata's age-name tables, needed to read its ages |
| `palynodata_taxloc.csv` | 1,056 | Location names |
| `palynodata_codes.csv` | 36 | Code meanings for `TMIC`, `TIDR`, `TNEW`, `TNEWC`, `TEME` and `TSYN`, from the release's `DESCRIPT.HTM` |
| `palynodata_release/` | 9 files | Release readme, licence, citation, metadata and field descriptions |

**Window rule.** A row is in the window if its numeric range (`agestart`, `ageend`) overlaps
383–600 Ma on Palynodata's own timescale (109,659 rows), or if it has no numeric age and its age
names match a window term (28 rows; `derived_window_basis` says which). Rows with broad ages such as
"Paleozoic" are included; `derived_span_myr` and `derived_fully_inside_window` let them be filtered.

**Window widened 2026-10-28** (Claude Opus 5.5) from 383–485 Ma to 383–600 Ma, for the
pre-Ordovician control on spore first appearances (`docs/plan-f3.md`, second amendment).
Palynodata's table places the Tremadoc at about 505–490 Ma and the Cambrian at about 570–505 Ma, so
the old 485 Ma edge dropped every Tremadoc-only document as well as the Cambrian. The widening kept
every earlier row and added 33,336 rows from 1,338 documents (157 of them with spore rows).

**Counts in the window (2026-10-27 extract, 383–485 Ma).** By `TMIC`: acritarchs 41,483;
chitinozoans 17,018; spores or pollen 14,114; scolecodonts 2,581; algae 361; dinoflagellates 325;
other 194; fungal spores 113; unknown affinity 88; plants 69; others 5. Of the 2,511 documents, 985
report spores and 1,526 report only other palynomorphs. Ordovician-labelled spore rows: 738 from 135
documents, mostly Ashgill and Caradoc. **After the widening:** acritarchs 69,483; chitinozoans
17,254; spores or pollen 14,629; algae 3,565; scolecodonts 2,621; other 781; fungal spores 484;
dinoflagellates 409; unknown affinity 376; plants 69; others 16. Of 3,540 documents, 1,117 have
spore rows.

## Read before use

- **Rows are mentions, not samples.** One assemblage can recur across papers; a taxon can appear
  in a synonymy list (`TSYN` set: 1,241 window spore rows) or be described as new (`TNEW` = X: 663)
  rather than reported from a fresh sample. Reworked or caved identifications are flagged in
  `TIDR` (15 window spore rows reworked).
- **Spores absent is not proven absent.** A document that lists only acritarchs or chitinozoans is
  evidence of sampling effort, but marine studies may not have counted or reported land-derived
  spores, and Palynodata indexes what a document names.
- **Ages are Palynodata's.** Age names predate current ICS usage (Gedinnian, Siegenian, Ludlovian,
  Gothlandian, Downtonian), and numeric ages come from its own 2006-era table, not from
  `../../timescale.csv`. Nothing has been converted.
- **Locations are text**, at region or country level ("Canada(NWT,Franklin)"); `TLOC` and the
  document's `GlobalLocation` are the only geography.
- **Coverage stops in 2006.** Later key records (for example Rubinstein et al. 2010, Middle
  Ordovician) are absent. The Global Acritarch Database (Shu et al. 2025, ESSD 17:3567) extended
  Palynodata's acritarchs with 2008–2023 literature and ICS v2024/12 ages; its data and code are in
  `../deposits/` as a method template.
- `TAGE` and `GenAge` are empty in the source; `TOLD`, `THYP`, `TYOU` and `TSUB` have no documented
  purpose.

## Reproduce

From `data/external/`: `python3 scripts/spores_palynodata.py`. It checks both checksums, unpacks
`paly.mdb` with `bsdtar`, exports tables with `mdb-export` (Homebrew `mdbtools`) and fetches the
Wellman et al. supplement from Figshare. Working files go to `local/spores/work/`.

## Verification

200 randomly sampled window rows were found verbatim in an independent `mdb-export` of `TAXON`.
Every window document has a `NewEng` citation.
