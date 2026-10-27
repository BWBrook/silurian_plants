# Literature library: seeds, metadata, classification and counts (phase 1)

Built 2026-10-27 by Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic), as a subagent, on mac-mini and deep-server.
This is **phase 1 only**: seed lists, OpenAlex metadata, abstracts, classification and counts. **No PDF or
full text has been downloaded. Phase 2 (texts) awaits Barry's approval of the counts below.** The classification
(especially the `priority_spores` screen) is one agent's reading and has had no independent check.

## Files

| File | Contents |
| --- | --- |
| `works.tsv` | One row per work (6,312): `openalex_id doi year first_author title venue type language oa_status has_oa_pdf_url tiers subsets region in_project access`. `access` is `oa_pdf`, `oa_status_only` or `closed` (definitions below). Duplicate OpenAlex records of one work are merged by `library.py index`. |
| `cited_dois_resolution.tsv` | The 624 DOIs cited in `taxa/*.md` and `docs/*.md`, their source files, the OpenAlex id they resolve to, and notes. |
| `queries.tsv` | Every OpenAlex query run, verbatim, with date, hit count (and counts by period), credits and role (`seed` or `probe`). |
| `screen.tsv` | The classification rules (`kind=rule`) and every screened candidate for `priority_spores` (`kind=screen`) with rule, automatic class, decision, basis, reason and region. |
| `closed_candidates.csv` | Register of closed-access works in `priority_spores` and `cards` (395), for Barry to obtain through institutional login. |
| `counts.tsv` | The gate counts below, machine-readable. |
| `credits.tsv` | OpenAlex credit log. |
| `seeds/cited.tsv`, `seeds/window.tsv`, `seeds/window-marine.tsv` | The three seed tiers, as deployed in the store's `_tools/seeds/`. |
| `../local/library/abstracts.tsv` | Abstracts rebuilt from OpenAlex's inverted indexes (git-ignored: publisher text, local only). |

Scripts (`data/external/scripts/`): `library_eprp_library.py` (EPRP's `library.py`, unedited copy, sha256 `93b10132...ccbd1003`), `library_run.py`,
`library_cited_seed.py`, `library_window.py`, `library_classify.py`, and `library_screen_decisions.tsv` (the manual screen decisions,
the input to `library_classify.py`).

## Store and tool

`deep-server:/data/codex/silurian_plants/library/` holds the store: `openalex/<W>.json` (6,369 full OpenAlex records,
abstract inverted indexes and reference lists included), `aliases.tsv`, `credits.tsv`, `queries.tsv`, `_index/` (`library.py index` output) and
`_build/` (this folder's tables). `_tools/` holds an unedited copy of EPRP's `library.py` (identical sha256), `seeds/` and my helper
scripts. EPRP's own store (`/data/paleodata/library`) was never written to; its `manifest.tsv` was read, not written, for PDF sizes.
Every OpenAlex call went through `library.py`'s `openalex_url` and `get_json` on deep-server, using the key already configured there
(never read, printed or moved). No email or contact identifier was sent, and Unpaywall was not called. Open-access information
comes from OpenAlex's own `open_access`, `best_oa_location` and `locations` fields.

## Method

1. **Tier `cited`.** `library_cited_seed.py` applies the project's own `DOI_RE` and `clean_doi` (copied from `tools/cards.py`
   and checked against that file on each run) to every line of `taxa/*.md` and `docs/*.md`: 68 files, **624 distinct DOIs** (the brief
   expected about 450; `docs/precedents.md` alone has 142 and `docs/primer.md` 90). `docs/audits/` is outside the brief and adds one further DOI
   (`tools/cards.py dois` skips it too). `library.py resolve` resolved all 624 to 623 OpenAlex works (two DOIs are aliases of one work).
2. **Tier `window`** is the union of queries `a`, `b` and `d`; **tier `window-marine`** is query `c`. All use OpenAlex
   `title_and_abstract.search`, paged with `per-page` 200 and a cursor, saving full records to the store (so `library.py resolve`
   afterwards found nothing left to fetch). The exact strings are in `queries.tsv`.

   | id | Query (abbreviated; verbatim in `queries.tsv`) | Hits 2026-10-27 |
   | --- | --- | ---: |
   | a | (Silurian OR Devonian OR Ordovician) AND (spore, spores, cryptospore, palynology, palynomorph, land plant(s), embryophyte, tracheophyte, flora, rhyniophyte, zosterophyll, lycopsid, Prototaxites, nematophyte, Rhynie chert, terrestrialization) | 4,835 (the brief's count reproduced exactly; 4,832 distinct works returned) |
   | b | reconstruction of the plan's section 2 query: six spore terms (cryptospore, miospore, trilete, dispersed spore, spore assemblage(s), spore zone, palynozone) AND (Ordovician, Silurian, Early or Lower Devonian, or any Tremadoc-Emsian stage or old name) | 492 (plan: 493; 2007-2026: 287 against 280) |
   | d | extension: spore and plant terms (as a, plus miospore, trilete, palynozone, terrestrialisation, minus flora) AND stage names or old names, no period name needed | 1,517 |
   | c | (acritarch OR chitinozoan OR phytoplankton) AND the same stage terms as b | 1,477 (744 up to 2006, 733 from 2007; plan: 704 and 711) |

   Probes `p1`-`p15` in `queries.tsv` are the variants tried to reconstruct b and c (hit counts only). Query b is the variant
   closest to the plan's 493 works and its period split (31, 31, 59, 84, 287 against the plan's 28, 38, 63, 84, 280); the plan's exact term lists are not recorded, so neither
   reconstruction is exact. The tiers hold 4,945 `window`, 1,469 `window-marine` and 623 `cited` works after merging duplicate records;
   426 works are in both window tiers, 299 in `cited` and `window`.
3. **Index.** `library.py index` merged duplicate records (6,369 records, 6,312 works) and wrote `_index/works.tsv`;
   `library_classify.py` builds this folder's `works.tsv` from it.

## Classification

Subsets (a work can be in several; `subsets` lists all that apply):

- **`priority_spores`**: dispersed-spore and cryptospore occurrence papers published 2007-2026 that report Dapingian-Emsian assemblages. Rules R1-R3 and the manual screen are in `screen.tsv`; summary:
  - **R1** (511 candidates): spore term AND window term (any period, stage or old name) in title or abstract.
  - **R2** (254): palynology term, no spore term, AND window term. **R3** (27): spore term in the title, no window term, mostly works without an abstract. R2 and R3 exist because OpenAlex lacks abstracts for many palaeopalynology papers.
  - **Automatic exclusions** from the title: review (17 in R1), ultrastructure (19), in situ spores or sporangia (20), outside period (Cambrian, Carboniferous, Mesozoic; 25), outside epoch (Middle or Late Devonian only; 84).
  - **Manual screen** of the rest by reading titles and, where unclear, abstracts: `include` (128 in R1), `include_borderline` (13), `exclude` (205). Reviews and global compilations such as the Bek et al. and Pšenička et al. papers are set aside as cross-check sources, not counted. Tremadocian-Floian assemblages are outside the window. Marine-only (acritarch, chitinozoan) palynology is excluded. R2 and R3 papers are included only when the title points to generic or land-derived palynology of in-window strata and the abstract, if any, does not name marine groups only (basis `palynology_title_only`, confidence low; 44 papers).
  - **183 works** (186 records, 3 merged duplicates): 160 `include`, 23 `include_borderline`.
- **`cards`**: the 623 resolved `cited` works.
- **`window_other`**: `window` works that are not `priority_spores` (4,762; may overlap `cards`).
- **`window-marine`**: tier `window-marine` works (1,469).

Region (priority_spores only) follows the plan's table, assigned by reading title and abstract; `screen.tsv` shows a keyword check beside each assignment
(5 of 186 records disagree: four with generic "Gondwana" wording and one multi-region paper). Multi-region papers have a primary region and `region_secondary`.

### Comparison with `docs/spore-compilation-plan.md` section 2

| Region | Plan: titles found (n = 130) | Plan: central estimate | Here: all (183) | Here: `include` only (160) |
| --- | ---: | --- | ---: | ---: |
| Laurentia (incl. Scotland, Svalbard) | 12 | 20 | 17 | 14 |
| Avalonia, Baltica, peri-Gondwanan Europe | 27 | 40 | 45 | 37 |
| North Africa | 10 | 15-25 | 15 | 14 |
| Arabia, Iran, Turkey | 29 | 45 | 42 | 40 |
| South America | 29 | 45 | 40 | 34 |
| South Africa, Australia, other Gondwana | 1 | 5-10 | 5 | 3 |
| South China, Tarim, E Asia, Siberia, Kazakhstania | 12 | 25-35 | 19 | 18 |
| Unassigned | 10 | about 15 | 0 | 0 |
| **Total** | **130** | **about 200 (150-260)** | **183** | **160** |

By year (2007-09, 2010-14, 2015-19, 2020-24, 2025-26): here 32, 57, 53, 28, 13; plan 21, 43, 33, 26, 7. Titles here name Ordovician-Silurian (85), Devonian (68), both (11) or neither (19); the plan's titles were 71, 49 and 10 undated.

Where it differs, and why (the reasons are inferred from the rules, not tested):

- The R1 rule alone gives 141 included records (128 + 13 borderline), close to the plan's 130. R2 and R3 add 45 more (44 and 1), giving 186 records and 183 works after three duplicate records are merged.
- The count lies inside the plan's 150-260 range but below its 200 central estimate, so the plan's allowance for papers with spore-free titles was probably generous, or OpenAlex's coverage is the limit (see caveats).
- Unassigned is 0 because regions come from abstracts as well as titles, and global compilations are set aside.
- Europe is above the plan's central estimate (45 against 40) and South China and E Asia below its range (19 against 25-35). The plan expected a South China undercount (Chinese-language journals); the OpenAlex hits are mostly English-language records.
- The plan appears to have kept Devonian titles of any epoch (49). Here 60 works with spore or palynology in the title are excluded as Middle or Late Devonian only (some of them not occurrence papers), which lowers the Devonian count.

## Cited DOIs (`cited_dois_resolution.tsv`)

All 624 resolved (none `unresolved`), to 623 works. Ten rows carry notes: seven DOIs for which OpenAlex holds the work under a different DOI (earlier or later forms of the same article, one of them a JSTOR
alias), a pair of DOIs for one work, a `letter` record (10.1144/jgs2012-089) and a `paratext` record (10.3133/b1300), the last two of which `library.py fetch` would skip. Resolution is to the record OpenAlex returns for the DOI; it was not
checked that each record is the work the project means (Crossref title checks are `tools/cards.py dois`).

## Counts for the gate

Access classes, from OpenAlex's fields as of 2026-10-27:

- **has OA PDF URL**: `best_oa_location.pdf_url`, or any location with `is_oa` and a `pdf_url`.
- **OA by status only**: `is_oa` or an `oa_status` other than `closed`, but no `pdf_url` (a landing page or repository record).
- **Closed**: neither.

| Subset | Works | OA PDF URL | OA status only | Closed | Est. PDFs (PDF URL) | Est. size at 2 MB | Works `library.py` would try* | Est. size at 2 MB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `priority_spores` | 183 | 53 | 41 | 89 | 53 | 106 MB | 88 | 176 MB |
| `cards` | 623 | 219 | 94 | 310 | 218 | 436 MB | 290 | 580 MB |
| `window_other` | 4,762 | 903 | 702 | 3,157 | 875 | 1.75 GB | 1,287 | 2.57 GB |
| `window-marine` | 1,469 | 285 | 168 | 1,016 | 279 | 558 MB | 403 | 806 MB |
| Union (each work once) | 6,312 | 1,291 | 904 | 4,117 | 1,260 | 2.5 GB | 1,826 | 3.65 GB |
| Exclusive partition, by precedence in the order above | 183 / 613 / 4,473 / 1,043 | 53 / 214 / 830 / 194 | 41 / 93 / 658 / 112 | 89 / 306 / 2,985 / 737 | 53 / 213 / 802 / 192 | 106 / 426 / 1,604 / 384 MB | 88 / 284 / 1,184 / 270 | 176 / 568 / 2,368 / 540 MB |

\* Works with at least one candidate source in `library.py`'s own logic (open-access locations, landing pages, PubMed Central), excluding the
133 records of types `fetch` skips (dataset, paratext, erratum and similar; 2 in `cards`, 123 in `window_other`, 15 in `window-marine`).
The estimates exclude them too.

**Size.** OpenAlex gives no file sizes, so the table uses the brief's 2 MB per PDF. The 2,976 PDFs already in EPRP's store have a median of 1.89 MB but a
mean of 4.36 MB, so a total at that mean would be about 2.2 times larger (for example 231 MB for `priority_spores` by PDF URL, 5.5 GB for the union). `counts.tsv` has both.
Every figure is a ceiling on what is open, not a forecast of what `fetch` will retrieve: publishers often refuse scripted PDF requests even for open works (see EPRP's README).

Closed-access share: 49% of `priority_spores`, 50% of `cards`, 66% of `window_other`, 69% of `window-marine`.
`closed_candidates.csv` lists the 395 closed works in `priority_spores` and `cards` (priority and cited-by-card reasons, publisher from OpenAlex's host organisation). Two cited works predate 1931; `library.py`'s Internet Archive route would
try them. No non-open route was tried for any closed work.

## How `fetch` would behave (read from `library.py`; not run)

For each work, in tier order and then by W id, `fetch` tries:

1. **OpenAlex locations** flagged open access: ordered by version (published, accepted, submitted), then direct `pdf_url`s before landing pages, then repositories before publishers; a landing page without a `pdf_url` is searched for `citation_pdf_url` or a same-host file link. A PubMed Central location or `ids.pmcid` goes to the PMC open-access bucket.
2. **Lookup routes**, in this order: CORE (its key is installed on deep-server; paced at one request per 6.5 s), Semantic Scholar (DOI lookup, no key), and for works published in 1930 or earlier the Internet Archive's unrestricted scans.
3. **Publisher TDM**, only for Wiley and only after every open route has finished without a transient failure. `TDM_ROUTES` holds a single entry (Wiley, DOI prefixes 10.1111, 10.1002, 10.1029, 10.1046, 10.1034, 10.1890). Elsevier has no route in the code.

**TDM would be used automatically on deep-server.** The Wiley token file exists there (checked for existence only), so a plain `library.py fetch` would
request TDM copies, stored under `tdm/wiley/`, for Wiley-prefix DOIs with no open copy. In these subsets 477 works have Wiley-prefix DOIs (6 in `priority_spores`, 121 in `cards`, 358 in `window_other`, 72 in `window-marine`; 338 of the 477 have no OA PDF URL).

To exclude TDM without editing `library.py`: run every `fetch` through `library_run.py`, which empties `library.TDM_ROUTES` before the command runs (checked: it prints `{}` after import).
Do not copy `tdm/` off deep-server; after a run, `ls /data/codex/silurian_plants/library/tdm` should not exist. Changing `HOME` to hide the token would also hide the CORE key, so it is the worse option.

Other facts for phase 2:

- `fetch` with no `--tier` takes every seed tier that does not start with `field-`, so it would also fetch `window-marine`. Name tiers with `--tier`.
- Tiers are seed files. There are no per-work or per-subset switches, so phase 2 needs `priority_spores.tsv` and `cards.tsv` seed files (openalex ids from `works.tsv`) in `_tools/seeds/`, then `library_run.py fetch --tier priority_spores cards`.
- The Semantic Scholar and CORE routes send only a DOI (and the CORE key). The tool's user agent carries no email.
- Phase 2 also needs `pdftotext` and `pdfinfo` (present on deep-server).

## OpenAlex credits

**794 credits** (about 0.08 USD of the key's 10,000-credit daily budget; 9,206 remained at the end), all through `library.py` functions on deep-server:
cited-tier resolution 13 (13 batches of 50 DOIs; single-work lookups for alias DOIs cost 0), scratch probes while reconstructing queries b and c 180,
the 15 logged probes 150, paging of the four seed queries 440, and a first header probe 11. A search query costs 10 credits per page whatever the page size; page size 200 keeps that to 25 pages for query `a`. `credits.tsv` has the log.

## Caveats

- **Classification is a single-agent reading.** The `priority_spores` screen used titles and OpenAlex abstracts, not the papers. 23 works are borderline and 44 are title-based. Reviews and compilations (21) were set aside rather than counted; an extraction plan may want them as cross-checks.
- **OpenAlex coverage.** Many palaeopalynology records have no abstract (22 works with a spore term in the title had no abstract and no window term in the title), and regional, conference and Russian, Chinese and Persian-language records are thin. The count is a floor for what the literature holds.
- **Window tiers are noisy.** Query `a` includes unrelated works through `flora` and period names (for example a philosophy preprint in `window_other`). `window_other` is a harvest, not a curated list; 123 of its records are datasets and other types `fetch` skips.
- **Query `a` returned 4,842 rows for 4,835 hits** (cursor pages repeat a few works), keeping 4,832 distinct works; three hits were not returned, probably index changes during paging.
- **OA fields lag.** `closed` in OpenAlex can hide a green copy found later; `oa_status_only` works may not yield a PDF.
- **Reconstructed queries.** Queries b and c reproduce the plan's counts to within 4 percent but not exactly (the plan's term lists are not recorded).
- **Dates.** Query dates are UTC; the first calls ran on 2026-10-27 about 03:40 UTC.
- **`docs/closed-literature.csv`** appeared untracked in the repository during this work. It is not mine and was not read or touched.

## Licence

OpenAlex metadata (ids, DOIs, titles, years, venues, access fields, counts) is CC0. The classification, screen decisions and region assignments are the
project's own work. Abstracts are publisher text and stay in `local/library/abstracts.tsv`.

## Reproduce

From `data/external/`: `python3 scripts/library_cited_seed.py` writes `library/seeds/cited.tsv`. On deep-server, from `/data/codex/silurian_plants/library/_tools/`
(helper scripts and seeds copied there):
`python3 library_run.py resolve --store ..`, `python3 library_window.py probes`, `python3 library_window.py seed`, `python3 library_window.py finalize`,
`python3 library_run.py resolve --store ..`, `python3 library_run.py index --store .. --out ../_index`, `python3 library_classify.py`.
Rerunning `seed` costs about 440 credits and returns whatever OpenAlex holds on that day.
