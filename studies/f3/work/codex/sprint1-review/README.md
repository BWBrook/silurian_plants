# Sprint-1 counter-review evidence

The integrated scientific account is
`docs/audits/2026-10-31-sprint1-codex-review.md`.

- `check_historical.py`, `historical_*`: immutable Git-object reconstruction at
  `f08afb4`, independently checking the original 28 receipts and their tables.
- `source/`: independent primary-source/chart and design reconstruction at the
  original handoff. The explicitly named baseline adapter/declaration are audit
  inputs, not alternate production implementations. Copyrighted PDFs stay in
  the ignored library and are identified by hashes.
- `methods/`: independent Murzuq likelihood calculation and original-grid
  membership/reference checks. `check_reference.py` concerns the original
  `f08afb4` code and saved acceptance tables; run it against that revision when
  reproducing `reference-results.json`. The report distinguishes denominator
  changes from changes to a vacuous interval condition.
- `contract/`: independent adversarial review. The `AUDIT-TOY` fixtures and
  pre-screen counterexample are fabricated contract tests, not simulations.
- `implementation/`: implementation handoff and development smoke evidence.
- `crosshost/`: Mac/Nectar comparison of the frozen binding with matching
  Python major.minor and exact NumPy/SciPy versions.
- `tests.log`: full 228-test F3 run before the frozen rerun.
- `run_qualification.py`: committed at `5fcee58` before the fresh 14-combination
  recalibration/acceptance run; refuses an existing output directory.
- `evidence-check/`: independent saved-ledger reconstruction without F3 imports,
  including the historical 5fcee58 package and final binding evidence.
- `check_current.py`: product-loader validation on the Mac plus comparison of
  all empirical rows against `f08afb4`. Use the pinned rerun runtime and pass
  the completed run directory and a receipt output path.

Current binding qualification artifacts live in `models/f3/out/qual/`; the
original files remain recoverable from Git. Historical audit findings describe
the inspected state and do not certify later code or results. No R or ASR
analysis was changed by this tranche.

The portability repair is frozen at `31fab51`. Its 239-test full-suite log is
`tests-final.log`; the immutable historical-loader regression is under
`crosshost/historical-loader-check.json`.
