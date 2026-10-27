# Literature library: seeds, metadata, classification, counts and open texts (phases 1 and 2)

Built 2026-10-27 by Claude Sonnet 5.5 (`claude-sonnet-5-5`, Anthropic), as a subagent, on mac-mini and deep-server.
**Phase 1** (seed lists, OpenAlex metadata, abstracts, classification and counts) is described first; **Phase 2** (open texts for
`priority_spores` and `cards`, the Codex verification checks and the `open_unread` fetch) is the last section before the licence.
Phase 2 was approved by the project and relayed by the coordinating agent; only `priority_spores` and `cards` were fetched, and
`window_other` and `window-marine` remain metadata-only. The `priority_spores` screen is my reading, since re-screened independently by Codex (Phase 2).

## Files

| File | Contents |
| --- | --- |
| `works.tsv` | One row per work (6,312): `openalex_id doi year first_author title venue type language oa_status has_oa_pdf_url tiers subsets region in_project access`. `access` is `oa_pdf`, `oa_status_only` or `closed` (definitions below). Duplicate OpenAlex records of one work are merged by `library.py index`. |
| `cited_dois_resolution.tsv` | The 624 DOIs cited in `taxa/*.md` and `docs/*.md`, their source files, the OpenAlex id they resolve to, and notes. |
| `queries.tsv` | Every OpenAlex query run, verbatim, with date, hit count (and counts by period), credits and role (`seed` or `probe`). |
| `screen.tsv` | The classification rules (`kind=rule`) and every screened candidate for `priority_spores` (`kind=screen`) with rule, automatic class, decision, basis, reason and region. |
| `closed_candidates.csv` | Register of closed-access works in `priority_spores` and `cards` (396; column `open_copy_held` marks the 5 for which phase 2 found an open copy), for Barry to obtain through institutional login. |
| `counts.tsv` | The gate counts below, machine-readable. |
| `credits.tsv` | OpenAlex credit log (795 credits in all). |
| `seeds/*.tsv` | The seed tiers as deployed in the store's `_tools/seeds/`: `cited`, `window`, `window-marine` (phase 1); `priority_spores`, `cards`, `open_unread` (phase 2). |
| `fetch_results.tsv` | Phase 2: one row per work the fetch attempted (794): outcome, route, URL, size, sha256, quarantine flag. |
| `cited_identity_check.tsv` | Phase 2: Codex check that each of the 623 cited works is the work the project cites (all `same_work`). |
| `screen_codex_check.tsv` | Phase 2: every disagreement between Codex's independent re-screen and `screen.tsv` (as it stood before the changes), with my adjudication. |
| `open_unread_results.tsv` | Phase 2: the project's 41 open-but-unread works (45 rows): fetched, blocked, not found or failed, with route, URL, sha256 and identity verdict. |
| `codex_audit.md` | Phase 2: record of the Codex runs (models, chunks, coverage, cost, results). |
| `../local/library/abstracts.tsv` | Abstracts rebuilt from OpenAlex's inverted indexes (git-ignored: publisher text, local only). |
| `../local/library/pdf/`, `text/` | Phase 2: 206 open PDFs and their extracted text, `<W>.pdf` and `<W>.txt` (git-ignored; private research copies). |
| `../local/library/codex/` | Phase 2: Codex job inputs, schemas and outputs (git-ignored). |

Scripts (`data/external/scripts/`): `library_eprp_library.py` (EPRP's `library.py`, unedited copy, sha256 `93b10132...ccbd1003`), `library_run.py`,
`library_cited_seed.py`, `library_window.py`, `library_classify.py`, and `library_screen_decisions.tsv` (the manual screen decisions,
the input to `library_classify.py`). Phase 2 added `library_subset_seeds.py`, `library_fetch_report.py`, `library_text_export.py`,
`library_codex.py`, `library_codex_export.py`, `library_codex_screen_report.py`, `library_screen_codex_adjudication.tsv` and
`library_open_unread.py`.

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
  - **Manual screen** of the rest by reading titles and, where unclear, abstracts: `include` (124 in R1), `include_borderline` (16), `exclude` (207). Reviews and global compilations such as the Bek et al. and Pšenička et al. papers are set aside as cross-check sources, not counted. Tremadocian-Floian assemblages are outside the window. Marine-only (acritarch, chitinozoan) palynology is excluded. R2 and R3 papers are included only when the title points to generic or land-derived palynology of in-window strata and the abstract, if any, does not name marine groups only (basis `palynology_title_only`, confidence low; 44 papers).
  - **182 works** (185 records, 3 merged duplicates): 154 `include`, 28 `include_borderline`. (The phase 1 figures were 183, 160 and 23; the Codex check in Phase 2 removed three works, added two and re-graded three.)
- **`cards`**: the 623 resolved `cited` works.
- **`window_other`**: `window` works that are not `priority_spores` (4,764; may overlap `cards`).
- **`window-marine`**: tier `window-marine` works (1,469).

Region (priority_spores only) follows the plan's table, assigned by reading title and abstract; `screen.tsv` shows a keyword check beside each assignment
(5 of the 186 records screened in phase 1 disagreed: four with generic "Gondwana" wording and one multi-region paper). Multi-region papers have a primary region and `region_secondary`.

### Comparison with `docs/spore-compilation-plan.md` section 2

| Region | Plan: titles found (n = 130) | Plan: central estimate | Here: all (182) | Here: `include` only (154) |
| --- | ---: | --- | ---: | ---: |
| Laurentia (incl. Scotland, Svalbard) | 12 | 20 | 18 | 14 |
| Avalonia, Baltica, peri-Gondwanan Europe | 27 | 40 | 45 | 37 |
| North Africa | 10 | 15-25 | 15 | 14 |
| Arabia, Iran, Turkey | 29 | 45 | 42 | 39 |
| South America | 29 | 45 | 38 | 29 |
| South Africa, Australia, other Gondwana | 1 | 5-10 | 5 | 3 |
| South China, Tarim, E Asia, Siberia, Kazakhstania | 12 | 25-35 | 19 | 18 |
| Unassigned | 10 | about 15 | 0 | 0 |
| **Total** | **130** | **about 200 (150-260)** | **182** | **154** |

By year (2007-09, 2010-14, 2015-19, 2020-24, 2025-26): here 33, 56, 53, 28, 12; plan 21, 43, 33, 26, 7. Titles here name Ordovician-Silurian (85), Devonian (68), both (11) or neither (18); the plan's titles were 71, 49 and 10 undated.

Where it differs, and why (the reasons are inferred from the rules, not tested):

- The R1 rule alone gives 140 included records (124 + 16 borderline), close to the plan's 130. R2 and R3 add 45 more (43 and 2), giving 185 records and 182 works after three duplicate records are merged.
- The count lies inside the plan's 150-260 range but below its 200 central estimate, so the plan's allowance for papers with spore-free titles was probably generous, or OpenAlex's coverage is the limit (see caveats).
- Unassigned is 0 because regions come from abstracts as well as titles, and global compilations are set aside.
- Europe is above the plan's central estimate (45 against 40) and South China and E Asia below its range (19 against 25-35). The plan expected a South China undercount (Chinese-language journals); the OpenAlex hits are mostly English-language records.
- The plan appears to have kept Devonian titles of any epoch (49). Here 60 works with spore or palynology in the title are excluded as Middle or Late Devonian only (some of them not occurrence papers), which lowers the Devonian count.

## Cited DOIs (`cited_dois_resolution.tsv`)

All 624 resolved (none `unresolved`), to 623 works. Ten rows carry notes: seven DOIs for which OpenAlex holds the work under a different DOI (earlier or later forms of the same article, one of them a JSTOR
alias), a pair of DOIs for one work, a `letter` record (10.1144/jgs2012-089) and a `paratext` record (10.3133/b1300), the last two of which `library.py fetch` would skip. Resolution is to the record OpenAlex returns for the DOI; the Codex check
in Phase 2 found all 623 to be the work the project cites.

## Counts for the gate

Access classes, from OpenAlex's fields as of 2026-10-27:

- **has OA PDF URL**: `best_oa_location.pdf_url`, or any location with `is_oa` and a `pdf_url`.
- **OA by status only**: `is_oa` or an `oa_status` other than `closed`, but no `pdf_url` (a landing page or repository record).
- **Closed**: neither.

| Subset | Works | OA PDF URL | OA status only | Closed | Est. PDFs (PDF URL) | Est. size at 2 MB | Works `library.py` would try* | Est. size at 2 MB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `priority_spores` | 182 | 52 | 40 | 90 | 52 | 104 MB | 87 | 174 MB |
| `cards` | 623 | 219 | 94 | 310 | 218 | 436 MB | 290 | 580 MB |
| `window_other` | 4,764 | 905 | 703 | 3,156 | 877 | 1.75 GB | 1,289 | 2.58 GB |
| `window-marine` | 1,469 | 285 | 168 | 1,016 | 279 | 558 MB | 403 | 806 MB |
| Union (each work once) | 6,312 | 1,291 | 904 | 4,117 | 1,260 | 2.5 GB | 1,826 | 3.65 GB |
| Exclusive partition, by precedence in the order above | 182 / 612 / 4,475 / 1,043 | 52 / 213 / 832 / 194 | 40 / 93 / 659 / 112 | 90 / 306 / 2,984 / 737 | 52 / 212 / 804 / 192 | 104 / 424 / 1,608 / 384 MB | 87 / 283 / 1,186 / 270 | 174 / 566 / 2,372 / 540 MB |

\* Works with at least one candidate source in `library.py`'s own logic (open-access locations, landing pages, PubMed Central), excluding the
133 records of types `fetch` skips (dataset, paratext, erratum and similar; 2 in `cards`, 123 in `window_other`, 15 in `window-marine`).
The estimates exclude them too.

**Size.** OpenAlex gives no file sizes, so the table uses the brief's 2 MB per PDF. The 2,976 PDFs already in EPRP's store have a median of 1.89 MB but a
mean of 4.36 MB, so a total at that mean would be about 2.2 times larger (for example 227 MB for `priority_spores` by PDF URL, 5.5 GB for the union). Phase 2 confirmed it: the 202 copies held in the two fetched subsets average 4.2 MB. `counts.tsv` has both.
Every figure is a ceiling on what is open, not a forecast of what `fetch` will retrieve: publishers often refuse scripted PDF requests even for open works (see EPRP's README).

Closed-access share: 49% of `priority_spores`, 50% of `cards`, 66% of `window_other`, 69% of `window-marine`.
`closed_candidates.csv` lists the 396 closed works in `priority_spores` and `cards` (priority and cited-by-card reasons, publisher from OpenAlex's host organisation; 5 of them now have an open copy, marked in `open_copy_held`). Two cited works predate 1931; `library.py`'s Internet Archive route would
try them. No non-open route was tried for any closed work.

## How `fetch` behaves (read from `library.py` before phase 2; confirmed by the run)

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
- Tiers are seed files. There are no per-work or per-subset switches, so phase 2 needs `priority_spores.tsv` and `cards.tsv` seed files (openalex ids from `works.tsv`) in `_tools/seeds/`, then `library_run.py fetch --tier priority_spores cards` (done in phase 2).
- The Semantic Scholar and CORE routes send only a DOI (and the CORE key). The tool's user agent carries no email.
- Phase 2 also needs `pdftotext` and `pdfinfo` (present on deep-server).

## OpenAlex credits

**795 credits** (about 0.08 USD of the key's 10,000-credit daily budget; 9,205 remained at the end), all through `library.py` functions on deep-server:
cited-tier resolution 13 (13 batches of 50 DOIs; single-work lookups for alias DOIs cost 0), scratch probes while reconstructing queries b and c 180,
the 15 logged probes 150, paging of the four seed queries 440, a first header probe 11, and one DOI lookup in phase 2 (the Zenodo DOI, 1). A search query costs 10 credits per page whatever the page size; page size 200 keeps that to 25 pages for query `a`. `credits.tsv` has the log.

## Caveats

- **Classification is one agent's reading, with one independent check.** The `priority_spores` screen used titles and OpenAlex abstracts, not the papers; Codex re-screened it blind in Phase 2. 28 works are borderline and 44 are title-based. Reviews and compilations (21) were set aside rather than counted; an extraction plan may want them as cross-checks.
- **OpenAlex coverage.** Many palaeopalynology records have no abstract (22 works with a spore term in the title had no abstract and no window term in the title), and regional, conference and Russian, Chinese and Persian-language records are thin. The count is a floor for what the literature holds.
- **Window tiers are noisy.** Query `a` includes unrelated works through `flora` and period names (for example a philosophy preprint in `window_other`). `window_other` is a harvest, not a curated list; 123 of its records are datasets and other types `fetch` skips.
- **Query `a` returned 4,842 rows for 4,835 hits** (cursor pages repeat a few works), keeping 4,832 distinct works; three hits were not returned, probably index changes during paging.
- **OA fields lag.** `closed` in OpenAlex can hide a green copy found later; `oa_status_only` works may not yield a PDF.
- **Reconstructed queries.** Queries b and c reproduce the plan's counts to within 4 percent but not exactly (the plan's term lists are not recorded).
- **Dates.** Query dates are UTC; the first calls ran on 2026-10-27 about 03:40 UTC.
- **`docs/closed-literature.csv`** appeared untracked in the repository during this work. It is not mine; in phase 2 I read it (not modified) for citation lines of works without DOIs.

## Phase 2: open texts, Codex checks and `open_unread` (2026-10-27)

Approved by the project and relayed by the coordinating agent: fetch open copies for `priority_spores` and `cards`, defer
`window_other` and `window-marine`; the 41 `open_unread` works were added on the same basis. Observed results are stated as
counts from the store's own records; reasons marked "inferred" are not tested.

### Fetch

- Seed tiers `priority_spores` (182 works) and `cards` (623) were written from `works.tsv` by `library_subset_seeds.py` (copies in `seeds/`).
- Every fetch ran as `library_run.py fetch --store ... --tier priority_spores cards --workers 8`. Its first log line confirms
  `publisher TDM routes active: none`. The first pass ran 04:09-05:10 UTC; a second pass with the same command retried transient failures and found
  nothing new. 794 works were tried (796 selected; two are record types `fetch` skips).
- **No TDM copy was taken.** `tdm/` never held a file, and nothing from `tdm/` or `quarantine/` was copied to the Mac. (`textindex` created an
  empty `tdm/search-tdm.sqlite` holding no texts; I deleted it.) No key was read or printed.

| Subset | Works tried | Held (open copy kept) | Quarantined | Withdrawn after the identity check | Failed | No copy found | Size held |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `priority_spores` | 182 | 38 (37 with a text layer, 1 scan) | 1 | 3 | 53 | 87 | 132 MB |
| `cards` | 623 | 169 (164 + 5 scans) | 5 | 4 | 158 | 287 | 750 MB |
| Union | 794 | 202 | 5 | 7 | 209 | 371 | 848 MB |

(The two subsets share 10 works. Held counts are after the 7 withdrawals.)

- **Routes of the 202 held copies:** OpenAlex open-access locations 116, PubMed Central open-access bucket 69, Semantic Scholar links 13, CORE repository links 4, Internet Archive 0.
- **Why 209 works failed** (a work can show several reasons): HTTP 403 from the publisher 115, link was not a PDF 57, landing page with no PDF link 46, not in the PMC open-access subset 42,
  network error or timeout 30, HTTP 404 7, HTTP 429 3, HTTP 500 2. 371 works have no copy at any open source `library.py` looks at.
- **Against the gate counts:** phase 1 counted 52 and 218 works with an OA PDF URL in `priority_spores` and `cards`; 38 and 169 are held. The 202 copies average 4.2 MB, about twice the brief's 2 MB.
- **Held copies on the Mac:** `local/library/pdf/<W>.pdf` and `text/<W>.txt`, 206 each (855 MB and 14 MB), git-ignored. They are the 202 above plus
  two works re-screened out of `priority_spores` after they were fetched (W2075902280, W7135205057) and two `open_unread` works with no OpenAlex record (Chaloner et al. 1978, Kidston & Lang 1921 Part IV, stored under pseudo ids XU010 and XU101).
  Nine held files are scans without a text layer (inferred from `no_text`: they need OCR for full text; I OCR'd only their first two pages for the identity check).
- `library.py textindex` built `search.sqlite` (titles, abstracts and the held open texts) on deep-server.

### Quarantine review (Codex gpt-6.1-terra)

Six PDFs for five works failed `library.py`'s title check. For each, Codex saw the expected metadata and the first three pages' text. Verdicts: 5 `same_work`
(four are the supplementary material of the expected work, one is the main text: W2312953052, Treatise Part B Protista 1 ch. 1) and 1 `unreadable` (W4401715016, a Wiley PDF whose extracted text is download footers only).
`library.py` has no release command, so none was released: the five `same_work` files stay in `quarantine/` and are listed here. The supplements are not the works the project cites, so only W2312953052 is a candidate for release by hand.
The excerpt text was removed from the Mac after the review.

### Identity check of accepted texts (Codex gpt-6.1-terra)

213 accepted copies (first two pages of text, or OCR for scans) against the expected title, authors, year and venue: **204 match, 7 mismatch, 2 unclear**; coverage 213 of 213.
The 7 mismatches were withdrawn with `library.py withdraw` (reasons are in `manifest.tsv`): three supplementary-material PDFs (W1990866222, Gerrienne et al. 2011; W2008436885, a Rhynie chert U-Pb age paper; W3211791534, "Recalibrating the Devonian time scale"),
a conference abstract volume containing the expected abstract among others (W2230006337), a different conference abstract (W2254873166), a whole journal issue's front matter (W4405796352) and a newsletter issue (W7155675004).
The 2 unclear copies were kept: W2594148471 (a preprint with a different title) and W4406765794 (OCR text only an OCR notice).

### Cited-DOI intended-work check (Codex gpt-6.1-terra)

All 623 cited works were compared with the project's own citation lines (the line or lines in `taxa/` and `docs/` where each DOI appears): **623 `same_work`, no `different_work`, no `unclear`**
(`cited_identity_check.tsv`). A script check agrees: the OpenAlex title shares at least 60% of its words with a project line for 622 works (the 623rd, a Spanish title at 57%, is the right work),
and no project year differs from OpenAlex's by more than one. There are no mismatches to list.

### Screen spot-check (Codex gpt-6.1-sol)

Codex re-screened, blind to my decisions and from title and abstract under the same rules, all 183 `priority_spores` works of phase 1 and a random 200 of the 606 excluded candidates (seed 20261027); coverage 383 of 383 in four chunks.

| | Works | Same include/exclude call | Same three-way grade |
| --- | ---: | ---: | ---: |
| `priority_spores` | 183 | 176 (96.2%) | 98 (53.6%) |
| Excluded sample | 200 | 183 (91.5%) | 183 (91.5%) |
| Both | 383 | 359 (93.7%) | 281 (73.4%) |

Region agreed for 175 of 176 works both screens included. Codex graded 73 of my `include` as `include_borderline` (it cannot confirm assemblage age from the abstract) and 5 the reverse. There were 24 include/exclude disagreements (7 among `priority_spores`, 17 in the sample), listed with 78 grade-only differences in `screen_codex_check.tsv`.
I adjudicated each of the 24 (one-line reasons in that file):

- Codex was right for three `priority_spores` works, which were removed: W2075902280 (spores come only from the Middle Devonian assemblage), W4298208550 (a synthesis of existing Zenta Range palynomorph knowledge) and W7135205057 (assemblage dated Eifelian-Givetian).
- Three were re-graded `include` to `include_borderline` and stay in: W1479948401, W1762144596, W3171257164. One borderline was kept (W1485211926).
- Of the 17 excluded works Codex would include, two were added as `include_borderline`: W2776142699 (Rhynie chert dispersed spores; the title-only rule R3 missed it) and W2033254699 (Chigua Formation, a late Emsian-early Eifelian assemblage). The other 15 stay excluded (palynofacies, stratigraphy, Late Devonian or macrofossil papers).
- **`priority_spores` is now 182 works** (154 `include`, 28 `include_borderline`); the regional table and counts above are the updated figures. `library_screen_decisions.tsv`, `screen.tsv`, `works.tsv`, `counts.tsv`, `closed_candidates.csv` and the seeds were regenerated. W2776142699 was already held; W2033254699 has no open copy.
- The sample estimates the miss rate among excluded candidates at about 8.5% by Codex's reading (17 of 200), 1% (2 of 200) after adjudication; that applies to the 606 candidates only, not to works the rules never found.

### `open_unread` (the project's 41 open-but-unread works)

The input `~/papers/silurian_plants/library/open_unread.tsv` was read, not edited. Rows map to 45 works (row 5 holds four Kidston & Lang parts; Part IV also has a Zenodo copy). 34 map to OpenAlex records (all already in `cards`); the seed tier `open_unread` holds them plus the Zenodo DOI (`works.tsv` shows it in `tiers`).
Each work went through the library's open routes first and then, if still not held, through its stated URL with `library.py`'s own download, title check and manifest code (`library_open_unread.py`); fetched files then went through the Codex identity check.
Results (`open_unread_results.tsv`): **15 fetched** (all 15 identity `match`), **23 blocked**, **7 failed**.

- **Blocked** (a bot challenge or HTTP 403, recorded with host and status and not worked around; Barry downloads these by hand): Biodiversity Heritage Library, 9 works (public `itempdf` links answer 403 with a Cloudflare "Just a moment" page, once per item, no key, no registration);
  Wiley 5 (`nph.` and `bsapubs.onlinelibrary.wiley.com`), Royal Society archive 3, and one each for CSIRO (connectsci.au), Taylor & Francis, NRC Research Press, Durham repository, Cardiff ORCA (all HTTP 403) and the NRM DIVA repository (a bot challenge page).
- **Failed** (7): four Elsevier DOI links whose landing page offers no PDF link (Gess & Berry 2024, Stein et al. 2020, Bek et al. 2026, Edwards et al. 2001), one Newcastle repository landing page with no PDF link (Abbott et al. 1998), Gerrienne et al. 2011 (held, then withdrawn: the ORBi file is the supplement)
  and Wellman, Steemans & Vecoli 2013 (the figshare file is the chapter's supplementary material, quarantined; the chapter text was not obtained).
- **Fetched by the stated URL** rather than OpenAlex locations: Kidston & Lang 1921 Part IV (Zenodo record 2503478, through its public API) and Chaloner, Hill & Rogerson 1978 (the PalAss archive PDF, a scan with no text layer; no OpenAlex record exists). Thirteen more came from OpenAlex locations or PMC (twelve in the main fetch, one PMC copy).
- Supplements named in the input (Prats 2024 SI, Stein 2020 SI) were not separately fetched.

### Codex jobs

Every job was read-only with a schema and a stated item count; coverage was checked by script after each (`library_codex.py check`). Details and cost lines are in `codex_audit.md`.

| Job | Model | Run via | Chunks | Items returned | Time | Codex tokens |
| --- | --- | --- | ---: | ---: | --- | --- |
| `cited` identity | gpt-6.1-terra | raw `codex exec` | 6 | 623 of 623 | 44-47 s | 333,925 |
| `screen` re-check | gpt-6.1-sol | raw `codex exec` | 4 | 383 of 383 | 132-192 s | 310,569 |
| `quarantine` | gpt-6.1-terra | `codex-delegate` | 1 | 6 of 6 | 18 s | 82,524 in (36,480 cached), 451 out |
| `identity` | gpt-6.1-terra | `codex-delegate` | 2 | 213 of 213 | 47-56 s | 732,231 in (590,848 cached), 8,047 out |


## Licence

OpenAlex metadata (ids, DOIs, titles, years, venues, access fields, counts) is CC0. The classification, screen decisions and region assignments are the
project's own work. Abstracts are publisher text and stay in `local/library/abstracts.tsv`.

## Reproduce

From `data/external/`: `python3 scripts/library_cited_seed.py` writes `library/seeds/cited.tsv`. On deep-server, from `/data/codex/silurian_plants/library/_tools/`
(helper scripts and seeds copied there):
`python3 library_run.py resolve --store ..`, `python3 library_window.py probes`, `python3 library_window.py seed`, `python3 library_window.py finalize`,
`python3 library_run.py resolve --store ..`, `python3 library_run.py index --store .. --out ../_index`, `python3 library_classify.py`.
Phase 2: `python3 library_subset_seeds.py`, `python3 library_run.py fetch --store .. --tier priority_spores cards --workers 8`, `python3 library_text_export.py`,
then on the Mac `python3 scripts/library_codex.py prep-<job>` and `run <job>` for each Codex job, `library_run.py withdraw` for mismatches,
`python3 library_open_unread.py seeds`/`direct`/`report`, `python3 library_fetch_report.py` and `python3 library_run.py textindex --store ..`.
Rerunning `seed` costs about 440 credits and returns whatever OpenAlex holds on that day.
