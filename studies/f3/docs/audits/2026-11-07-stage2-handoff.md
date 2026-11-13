# GPT-6 Pro stage 2: results and handoff

Codex (gpt-6.1-sol), 7 November 2026. Implements the stage-2/3 analysis and reproduction
tranche handed over in Board discussion 140, message 2921, from stage-1 base `2c293fa`.
`manuscript/estimands.md` was agreed before code changes. No new measurements or author
requests were assumed. Claude retains full new-result narrative integration and semantic review.

## What is complete

- Canonical body rebuild, executable category membership, Oman exclusion comparison, region fix.
- Retrospective B2 age–intensity frontier across unit rules and fixed diagnostic delays.
- Murzuq time-by-well panel, separately fitted well rates, block and well-drop sensitivities.
- Interval-feasibility witnesses and negative certificates, including cutoff-straddling units.
- Shared-boundary scenarios and targeted influential-record checks.
- Public immutable raw PBDB archive/fetch, pinned reproduction environment, separate public/raw/private
  checks, case-specific claim bindings and declared dependency-closure manifests.
- Independent source check of C45–C47; they are supported. New C48–C52 remain provisional for Claude's
  integration. Numeric changes to earlier results were propagated to the ledger, quotations,
  generated tables and data-driven figures; the new analyses are introduced in the agent guide.

## Scientific results to integrate

| Item | Result | Interpretation |
|---|---|---|
| Canonical B0 | 78 possible / 76 guaranteed main units; constant bound 455.185345 Ma | K12 is one B0 unit, with Katian ages derived from the timescale. The former 77/75 inventory remains `without_oman_fragments` in the same pipeline. |
| Newly exposed B1 leak | Main B1 72/70 → 69/67; constant 434.624082 → 434.703019 Ma | E4-only tracheid records had incorrectly implied E3 branching. B1 now requires E3 or nested E5. B2 locality-age primary bounds remain unchanged. |
| Geography / C30 | West Junggar replaces Tarim for Xiemisitai in fossils and effort; B2 region-stage 20 → 19 units, 432.069514 → 432.375017 Ma | This changes a dependence sensitivity. The curated-unit constant bound remains 434.05 Ma. |
| Frontier / C48 | Main primary zero-delay earlier/later intensity contours: 0.476 at 431.2 Ma, 0.124 at 444 Ma, 0.105 at 447 Ma, 0.0846 at 452 Ma | Retrospective compatibility contours, not fitted recording rates or a joint confidence region. Corrected region-stage and curated sets require much less suppression. |
| Murzuq / C45, C51 | 10 Darriwilian cuttings in two wells have possible pre-459.1 support; 18 older zeros are wholly younger. Constant contour 0.09103, separate wells 0.09951; inverse block weighting 0.3930 / 0.4189 | Local sustained encounter; the block calculations are unqualified composite sensitivities. Full intervals, rather than point ages, are plotted. |
| Intervals / C49 | All 50 possible B2 units permit decline25: conditional-age asymptotic p 0.07661, finite-sample p 0.06713. The combined plant-excluded decline10 history also has a witness. | These counterexamples defeat a blanket claim over all recorded age supports. Optimised p values are not calibrated after searching ages. |
| Negative interval certificates | No support-consistent B2 inclusion subset attains nominal 5% non-rejection for pure decline10; no B0 subset does for any of the six histories | Scope is the encoded independent age-support rectangles and conditional-age diagnostic, not rejection of a biological history. Guaranteed-only B2 decline25 fails; the combined guaranteed case depends on asymptotic versus finite-sample convention. |
| Timescale / C50 | Constant primary B2 427.31–430.42 Ma over five deterministic shared-boundary scenarios; largest shift 1.58 Myr | Constant and PBDB histories remain younger under fixed, fractional-mapping and source-rule comparisons. Decline25 crosses. These are not geological probability intervals. |
| Influence / C52 | Removing main Yea units shifts constant B2 −1.67 Myr; removing Bathurst units +0.26 Myr; removing C. barrandei shifts B1 −2.38 Myr | Same-unit leave-group-out diagnostics; opposite effects occur under other readings/histories. No fossil is reidentified by a leave-out. |

The age–delay frontier reports `candidate_not_older_than_envelope_anchor` outside its chosen
parameterisation; that status does not exclude a true fossil age younger than its permitted upper
edge. The timescale output retains fixed published 431.2 Ma, an explicitly conditional fractional
mapping and the source-rule comparison (shifted current Homerian base + its quoted 1.3 Myr,
baseline 431.9 Ma) separately. None is silently substituted as a new calibration.

## Verification and reproduction

- Final claims check: 52 claims cited, zero errors and zero warnings; five new analyses are provisional.
- `make check-public`: 60 tests pass. Public tests require no copyrighted PDF or private delegate output.
- `make reproduce-derived`: 65 selected result CSVs regenerate byte for byte in a temporary copy
  containing tracked files only. Raw-collection timescale recalculation is explicitly skipped there.
- `make rebuild-source`: restores the exact public PBDB bytes and reproduces 76 selected build/result
  CSVs, including the shared-timescale analysis. It never replaces the snapshot with a live query.
- `make check-sources`: the held thesis extraction check passes locally. A missing copyrighted thesis
  produces an explicit `SKIPPED`, verified by regression test; this is not a full literature audit.
- The 144-cell Loop 3 simulation was rerun at canonical counts B0=76, B1=67, B2=48. Loop 1/2 qualification
  and the R pilot were not rerun or requalified.
- The interval implementation passed an independent mathematical audit: event-cell completeness,
  rank ordering/ties, all four cutoff inclusion masks, direct positive witnesses and negative bounds.
  Independent brute permutations agreed on 720 fixed-discrepancy decisions and 120 optimum brackets.
- The Murzuq calculation and panel, and the reproduction/manifest implementation, received separate
  bounded checks. The audit files below preserve scope and limits.
- The initial legacy claim checker now has a case-binding layer: 52 `.V###` bindings cover C27, C40
  and the new C48–C52 spans. A C27 flat-to-PBDB value swap fails; rounding, missing/non-unique selectors,
  wrong claim identity, changed source values and signed influence values have regression coverage.
- `makedoc.lock.json` pins the exact build-tool source; `tools/reproduce.py` pins the numerical package
  versions used for the public result reproduction. TeX/Pandoc remain system dependencies. The three
  PDFs were refreshed; the brief remains two A4 pages. Changed table and panel layout was inspected.

The frozen raw input is DOI <https://doi.org/10.5281/zenodo.24028289>, CC0, 27,830 collections.
Anonymous download restores the exact 12,983,563 bytes, raw SHA-256
`e0d1f772c1617c218948d1d2605661e93edcfe75e0fe8ce92afee91d3350a8b8`.
This routine input deposit is not a release of the paper. The retired additive Oman outputs/receipt
remain archival evidence at `df805b2`; current products use the canonical/exclusion pipeline.

## Remaining integration, within the agreed split

Claude should integrate C48–C52 into the article, supplement and brief where useful, apply the precise
interval-feasibility wording, and perform the semantic review against `estimands.md`. The source-rule
comparison and new B1 admission correction need an explicit account. Remaining legacy claims can be
migrated to value bindings during that ledger/prose pass; they retain pooled checking until migrated.
Do not describe the binding tool as an automatic guarantee of scientific meaning or exhaustive
runtime dependencies. The manifest traverses declared ledger/receipt/local-import dependencies and
labels private, bulk and historical inputs; its scope is inspectable.

Material residual uncertainty concerns geological ordering and dependence among recorded supports,
source-timescale identity, locality/formation ascertainment, heterogeneous B0 recording channels and
fossil-to-node mapping. The feasible age vectors are mathematical witnesses, not inferred dates.
The exhaustive search is a double-precision certificate to recorded tolerances, not exact arithmetic.
No new modelling or outside measurements are required by these implementation checks.

Companion records: `2026-11-07-stage2-inventory-frontier.md`,
`2026-11-07-stage2-interval-timescale.md`, `2026-11-07-stage2-interval-review.md`,
`2026-11-07-stage2-source-checks.md`, `2026-11-07-stage2-murzuq-review.md`,
`2026-11-07-stage2-claim-binding.md`, `2026-11-07-stage2-reproduction-review.md`,
and the two `2026-11-07-reproduction-*.json` receipts.
