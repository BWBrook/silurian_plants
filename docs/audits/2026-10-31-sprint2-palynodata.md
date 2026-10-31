# Sprint 2 Palynodata coverage and regeneration check

31 October 2026. Independent review against source-roster commit
`d17d033cc2bb7f083a61e31228d30919f2406beb`. The reviewer made no repository or model edits; the parent integrated derived tables and this report.

## Result

All eight held Palynodata derivatives reproduce byte-for-byte. The complete release ZIP and
extracted MDB match the extractor's pinned SHA-256 values; `hashes.csv` records the complete
hashes. The independent extraction uses `mdbtools v1.0.1`. Seven derivatives were rebuilt from
fresh database exports; the eighth, the code-description table, reuses the current extractor's
`CODES` definitions, so this is not an independent semantic audit of those definitions.

The full database has 1,142,020 `TAXON` rows and 22,152 `NewEng` citations; 22,065 citation IDs
have taxon rows. The held 383–600 Ma legacy-age window has 109,687 rows from 3,540 documents.
The release's numeric citation years range from 1838 to 2007: “2006 version” should not be
interpreted as a perfectly enforced publication-year cutoff.

## Bounded roster census

Each of these six citation identities matched the expected publication year and normalised
title in the full database. Counts are taxon mentions, not occurrences or independent samples.

| Roster source | Palynodata ID | All taxon rows | Window rows | Full rows coded S |
| --- | --- | ---: | ---: | ---: |
| Balme 1961, Samphire | 03280 | 44 | 1 | 39 |
| Strother et al. 1996, Hanadir | 18701 | 13 | 13 | 4 |
| Steemans & Pereira 2002, Paraguay | 21733 | 21 | 21 | 19 |
| Grahn et al. 2000, Paraguay companion | 20806 | 58 | 39 | 0 |
| Edwards & Feehan 1980, Irish Cooksonia | 09667 | 1 | 1 | 1 |
| Edwards, Feehan & Smith 1983, companion | 16937 | 11 | 11 | 7 |

`S` means **Spores or Pollen**, not verified embryophyte spores. Full row details, the original
age assignments and type counts are retained in the four `roster_*` CSVs. The 1980 paper's
title says Late Wenlock, whereas its indexed row says Early Ludlovian; retain this as an
index/source discrepancy requiring reconciliation, not a revised age. The 1983 record says
Late Wenlockian. Legacy numerical ages were not converted to ICS ages.

The ten selected later roster papers have no normalised exact-title match in the full citation
table (`roster_post2006_unmatched.csv`). This is an exact-title census, not a fuzzy-title search
or proof that their material was never mentioned by an earlier source. New studies and
supplements must not inherit coverage from older papers on the same material.

## Cambrian and Tremadocian coverage

Selection uses original named age endpoints, including spelled-out Early/Middle/Late and
abbreviated E./M./L. prefixes. Numerical legacy ages do not decide geological membership.
The initial scratch classifier omitted the spelled-out prefixes; that defect was corrected
and the complete census rerun before this report. Use only the current outputs and receipt
(script SHA-256 `5e1d503df48fe1f1df6eecb47c2d8dbe0d90176b1321bd39a4558c459662fd64`).

| Full-release named-endpoint selection | All rows | Documents | S rows | Documents with S |
| --- | ---: | ---: | ---: | ---: |
| Any Cambrian endpoint, including listed regional names | 17,502 | 776 | 288 | 98 |
| Any Tremadocian endpoint | 6,937 | 312 | 52 | 14 |
| Either group, deduplicated union | 23,718 | 956 | 340 | 111 |
| Only populated endpoints Cambrian | 13,015 | 603 | 193 | 71 |
| Only populated endpoints Tremadocian | 4,378 | 240 | 26 | 10 |

Groups overlap and document counts are not additive. The held numeric window retains all
340 selected S rows but omits two other Cambrian-labelled rows. The label ledger explicitly
excludes Precambrian/Eocambrian and the unresolved spelling `Middle Cambria` (two rows);
this bounded label census is not a taxonomic or chronological harmonisation. Broad ranges
with one qualifying endpoint must not be presented as narrowly dated Cambrian assemblages.

## Integration and reproduction

The existing `data/external/spores/MANIFEST.tsv` has blank `rows` and `sha256` fields and its
taxon description still says 485–383 Ma. The verified derivative corresponds to the widened
383–600 Ma rule documented in the README. These were manifest metadata defects, not changed derivative contents. The parent filled the eight verified row counts/hashes and corrected the window description during integration, retaining extraction-date provenance.

The census supports literature discovery and traceable source coverage. It supplies no
sample identifiers, complete sampling denominator, justified negative observations, material
deduplication or admitted M1 design. No scientific admission or model decision follows from
these counts. Existing receipt fixes remain for the scheduled sprint-1 counter-review.

Reproduce locally, without network access or changes to held inputs:

```sh
UV_CACHE_DIR=/private/tmp/sp-sprint2-palynodata/uv-cache uv run --no-project data/units/sprint2/palynodata/census.py --repo /Users/bwbrook/papers/silurian_plants --out /private/tmp/sp-sprint2-palynodata > /private/tmp/sp-sprint2-palynodata/run.log
```

The script checks pinned ZIP/MDB hashes, verifies its inputs remained unchanged during the
run, asserts the six citation identities and ten later exact-title nonmatches, and writes
`receipt.json`, `hashes.csv`, the census tables and regenerated derivatives. The receipt records
the executed script hash and all eight derivative comparisons; `run.log` preserves its summary.
