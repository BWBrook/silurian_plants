# Independent final evidence audit: 31fab51

**Pass.** All 28 final receipts independently reconstruct correctly against the
frozen code and declaration at `31fab51`. All 14 primary design/rho acceptance
chains pass at stage 1; every calibration shift is zero. No stage 2 was needed.

The checker imports no F3 code. It independently verifies frozen inputs and
protocols, quantity rosters, screen flags, all consumed attempts, exact path
targets, coverage counts, calibration order statistics, binomial acceptance
verdicts, hashes and dependency chains. The eight-ULP screen-critical allowance
is checked by stepping through adjacent representable floating-point values;
the recorded LR-versus-recorded-critical decision remains exact.

## Verified counts

- 14 calibration and 14 acceptance receipts, covering 378 cells.
- 378,000 passing records from 482,605 consumed attempts.
- 3,501 cell–quantity summaries, including 1,503 acceptance verdicts.
- Zero pre-screen or post-screen errors.
- All 378,000 stored reference and mean-intensity targets checked by exact
  integration. Maximum absolute differences: 5.16e-12 for a_ref and 9.77e-12
  for abar_rel.

The worst observed acceptance miss frequency is **38/1,000**, at H2/rho=0.5 in
Q4 for the H0/H0c/H0m mean and f=1 origin quantities (683 non-abstaining analyses).
This is the result on the declared finite grid and acceptance rule; it does not
establish simultaneous coverage or coverage conditional on an informative claim.

## Boundary checks

| MZ rho | B3 H0 misses / 1,000 | B3 non-abstaining | B4 window f=1 misses / 1,000 | B4 non-abstaining |
|---|---:|---:|---:|---:|
| 1 | 0 | 703 | 20 | 60 |
| 0.5 | 2 | 827 | 7 | 107 |
| 0.25 | 4 | 843 | 0 | 247 |
| 0.1 | 12 | 839 | 0 | 466 |

Across all designs, the worst B3 H0 frequency is 32/1,000 at H2/rho=0.5. The worst
B4 window frequency is 20/1,000 at MZ/rho=1. The stored claim counts are
non-abstaining analyses under the implemented rule, not necessarily finite
exclusions for every quantity.

## Exact same-seed comparison

Every one of the 28 compressed ledgers is **byte-for-byte identical** to the
historical `5fcee58` run. All statistical summaries and all statistical binding
values (including the resolved truths and rates) are exact matches. The only
changed file binding is `models/f3/qualification_contract.py`, which contains
the reviewed portability guard. Receipt envelopes and hashes bind the new code;
the statistical results did not change.

## Files and reproduction

- `audit_saved_ledgers.py`: exact independent checker snapshot.
- `audit.json`: full receipt-level audit and reconstructed verdicts.
- `audit-quantities.csv`: all 3,501 quantity results.
- `summary.json`: counts, worst acceptance quantities and MZ boundary results.
- `compare_runs.py`, `exact-comparison.json`: exact historical/final comparison.

```sh
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 /private/tmp/sp-f3-pinned/bin/python /private/tmp/sp-sprint1-new-evidence-review/final-31fab51/audit_saved_ledgers.py /private/tmp/sp-sprint1-rerun-final/qual --revision 31fab51 --expect-all --output /private/tmp/sp-sprint1-new-evidence-review/final-31fab51/audit.json
```

This auditor ran no simulations or numerical fits and made no repository edits.
The parent's separate current-source product-loader check remains distinct from
this independent saved-evidence reconstruction.
