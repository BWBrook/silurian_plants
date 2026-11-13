# Independent saved-ledger checker

`audit_saved_ledgers.py` imports only the Python standard library and SciPy.
It never imports the F3 simulator, estimator, validation or qualification
assessment. It reads the requested frozen Git revision and reconstructs:

- Source/code hashes, primary variant, specification, timescale, runtime and
  phase protocol.
- The final 15 truth cells and their required quantity rosters.
- Sequential consumed attempts, screen selection flags, abstentions and errors.
- Reference intensity and exposure-weighted targets by exact integration of
  each declared path, compared with the saved numerical targets.
- All coverage, non-abstention and miss counts; 0.955 calibration order
  statistics; exact-binomial stage-1 verdicts; and the 1,886/2,000 stage-2 rule.
- Receipt payloads, compressed ledger hashes, exact calibrated truths and
  dependency hashes.

The final script independently brackets the screen critical value with eight
successive representable floating-point values on either side. It keeps the
stored LR-versus-stored-critical selection comparison exact. This implements
the narrowly reviewed cross-host portability allowance for the frozen
oldest-possible screen, whose older-detection count is zero.

Run against a completed binding package, substituting its frozen code revision:

```sh
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 /private/tmp/sp-f3-pinned/bin/python /private/tmp/sp-sprint1-new-evidence-review/audit_saved_ledgers.py /path/to/qual --revision FROZEN_REVISION --expect-all --output /private/tmp/sp-sprint1-new-evidence-review/current-audit.json
```

The JSON report has a companion `current-audit-quantities.csv` containing every
cell–quantity result. `--expect-all` requires all 14 selected design/rho pairs
and a completed final acceptance verdict. A fail verdict is reported as a
scientific failure, not confused with malformed evidence. Development records
can be checked separately using `--include-dev`; they never count towards
binding completion.

`exercise_checker.py` creates explicitly SYNTHETIC fixtures to exercise the
stage-2 threshold (1,886 passes; 1,885 fails) and rejection of a re-sealed screen
contradiction. These are not simulation evidence.

`historical-5fcee58/` preserves the first completed 28-ledger audit and its exact
checker snapshot. That numerical reconstruction passed, but the old production
loader's exact floating-point equality failed across hosts. The package is
historical pending the new frozen-code rerun. No source repository files or
simulation outputs were changed by this auditor.
