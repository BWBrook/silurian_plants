# Historical 5fcee58 numerical evidence audit

All 28 saved numerical ledgers independently reconstruct correctly. This package
is historical: the production loader rejected a one-ULP difference in a
recomputed screen critical value on the Mac. The integrity-only portability
repair and its new binding rerun must complete before current qualification is
attached. This independent checker used an absolute 1e-12 numerical comparison
for that recomputation, while preserving the exact stored LR-versus-critical
selection decision.

The check imported no F3 simulator, estimator, validation or contract code. It
read the frozen declarations and Git blobs at `5fcee58`, independently derived
the applicable quantity rosters, integrated the declared paths, reconstructed
every cell summary, recomputed calibration order statistics and binomial
acceptance decisions, and checked receipt/ledger hashes and dependencies.

Verified totals:

- 14 calibration and 14 stage-1 acceptance receipts; no stage 2 required.
- 378 cells: 210 calibration cells including diagnostics, 168 acceptance cells.
- 3,501 cell–quantity summaries: 1,998 calibration and 1,503 acceptance.
- 378,000 passing records from 482,605 consumed attempts.
- Zero pre-screen or post-screen errors; every calibration shift is zero.
- All 1,503 stage-1 quantity verdicts pass the adopted 0.93 coverage-floor rule.
- Exact path integration checked all 378,000 stored reference and mean-intensity
  targets. Maximum absolute discrepancies were 5.16e-12 for a_ref and 9.77e-12
  for abar_rel.

The worst observed acceptance false-claim frequency is 38/1,000, in H2 at rho=0.5,
cell Q4, for six H0/H0c/H0m mean or origin quantities. That cell has 683
non-abstaining analyses. This is a finite-grid empirical result, not a bound on
the true error probability of every possible history or simultaneous curve.

## New boundary cells

For B3, the H0 mean-intensity quantity at 459.1 Ma:

| MZ rho | Misses / screen passes | Non-abstaining analyses |
|---|---:|---:|
| 1 | 0 / 1,000 | 703 |
| 0.5 | 2 / 1,000 | 827 |
| 0.25 | 4 / 1,000 | 843 |
| 0.1 | 12 / 1,000 | 839 |

Across all designs, B3's worst observed H0 frequency is 32/1,000 at H2/rho=0.5
(682 non-abstaining analyses).

For B4, the pre-459.1 window at f=1 through 462.6 Ma:

| MZ rho | Misses / screen passes | Non-abstaining analyses |
|---|---:|---:|
| 1 | 20 / 1,000 | 60 |
| 0.5 | 7 / 1,000 | 107 |
| 0.25 | 0 / 1,000 | 247 |
| 0.1 | 0 / 1,000 | 466 |

The worst B4 window frequency is the MZ/rho=1 result, 20/1,000. Its 20 misses
among 60 non-abstaining analyses underscore the distinction between the declared
screen-conditioned false-claim rate and coverage conditional on an informative
claim. The stored claims fields count the former procedure's non-abstaining
analyses; they do not necessarily count finite exclusions for each quantity.

## Checker validation and files

The separate checker also reproduced the development smoke, accepted a
synthetic stage-2 pool of 1,886/2,000, rejected 1,885/2,000, and rejected a
re-sealed ledger whose pass flag contradicted its screen statistic. Those
fixtures are marked SYNTHETIC and are not simulation evidence.

- `audit_saved_ledgers.py`: exact checker snapshot used for this audit.
- `audit.json`: complete reconstructed receipt-level report.
- `quantities.csv`: all 3,501 quantity summaries, counts and verdicts.
- The parent directory holds checker exercises and their results.

No ensemble or numerical fit was rerun by this auditor. Source-to-adapter
correctness and the primary MZ likelihood calculation were separate checks;
this audit reconstructs saved evidence and target definitions.
