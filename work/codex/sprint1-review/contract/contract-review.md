# Independent qualification-contract review

Disposition: the final implementation is cleared for the planned binding rerun.
This review is not a binding coverage result. No repository file was edited by
this auditor and no ensemble was run.

## Defect found and repaired

The first implementation allowed an exception before the screen to disappear
from the acceptance population. A synthetic ledger containing one simulator
failure followed by 1,000 successful screen-passing records produced
`complete=true`, `result=pass`, and `errors_before_screen=1`.
`prescreen-original.json` preserves that counterexample.

The final implementation makes such a cell incomplete and prevents a calibration
from completing when any recorded pre-screen error occurs. Numerical screen
nonconvergence raises a failure; it is not an ordinary S1 rejection. Normal
attempts now preserve screen status, convergence, statistic, critical value and
older-detection count, and the verifier checks the pass flag against the
statistic. A legitimate no-first-appearance exclusion remains distinct.

## Final adversarial checks

`probe_contract.py` uses clearly named AUDIT-TOY artifacts; these are fabricated
contract fixtures, not simulation evidence. The final pinned-runtime run proves:

- A pre-screen exception followed by the required number of passing attempts
  yields `complete=false`, `result=incomplete`.
- `passed=True` with a statistic below the critical value is rejected.
- An unconverged frame-potential statistic raises an error.
- A stage-2 artifact without stage-1 evidence is rejected by the direct loader;
  the high-level attachment remains only `calibrated only` and cannot attach a
  pass.
- Rewriting an existing calibration artifact is refused, and its hash remains
  unchanged.
- A 1e-10 perturbation to a derived reference rate passes the declared numerical
  tolerance; a 1e-5 perturbation is refused.

Code inspection additionally confirmed a predeclared nonempty quantity roster,
strict Boolean and sequential-attempt parsing, reconstruction of summaries and
verdicts from the ledger, exact calibration/acceptance dependencies, stage-2
pooling limited to borderline quantities, source/generated-unit/statistical-code
binding, and distinct labels for sensitivities and QB's unqualified H0c output.
The implementation agent owns the larger mutation and lifecycle test suite.

The runtime contract pins Python major.minor and exact NumPy/SciPy versions;
platform and Python patch remain informational. Derived reference rates and
boundary truths can differ within 1e-8 absolute/relative tolerance when checking
the same source design across hosts. Acceptance and stage 2 then use the exact
calibrated rates and resolved truths, and their binding hashes must equal the
calibration's. Raw input/code/generated-unit bindings remain exact.

## Final actual development smoke

Command from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 /private/tmp/sp-f3-pinned/bin/python models/f3/qualify.py --design LY-H2-CU --rho 1 --phase dev --target 5 --workers 2 --out-dir /private/tmp/sp-sprint1-contract-review/h2-final-dev
```

The final 15-cell grid (12 acceptance cells including B3/B4, three diagnostics)
completed with 75 passing records from 76 consumed attempts, with zero errors
before or after the screen. Reading the saved CSV and reconstructing its
assessment reproduced every saved summary field. The runtime was Python 3.12.15,
NumPy 2.3.4 and SciPy 1.16.3 on macOS arm64.

Binding SHA-256:
`0e62a107f18976a0c7e25a3ec96f3687f9a783341d15f8195b5c4cff68077dd6`

Receipt payload SHA-256:
`932417eff0c7a6354b9b4e945bbfa909c25c2ff7c7fba53b540731309e0a1eef`

Reviewed statistical sources at that smoke:

- `m2.py`: `48da9074700e4a17e5555c2849de43a780ad3e44423d5ecfe8a96ed95ac313e1`
- `qualify.py`: `279989c16864571a550cedcaf8e1a6de56358d67370674324aa0b6d0b291ab6b`
- `qualification_contract.py`: `48eef04162897b321390ca3f745c6766dd830f25d15c29712e35cc770a548b79`
- Active declaration: `d27bd4277d9910a9396f688d0b893b06f5feeea007523134a8e49b09bb5421bd`

The parent separately reported successful final cross-host binding checks for
LY-MZ and QB under the pinned runtime. The binding ensemble and empirical
attachment remain the next gate.

## Scientific scope retained

The final declared additions address two material gaps identified in review:
B3 tests the H0-compatible boundary at 459.1 Ma, and B4 tests reference-level
pre-459.1 encounter through 462.6 Ma with zero encounter between tau0 and
459.1. B4 belongs to H0/H1, not H0m. Fresh binding seeds avoid reusing the
earlier acceptance draws inspected during review.

All coverage language remains conditional on the declared finite grid and
potential screen. The stored `claims_*` fields count non-abstaining analyses
under the implemented rule (tau<t0 and positive total older exposure); they do
not necessarily count informative finite exclusions for each output. I3's
unbounded windows illustrate the distinction. No further grid extension is
recommended for this tranche.

## Artifacts

- `probe_contract.py`, `probe-results-final.json`: focused final adversarial probes.
- `repro_prescreen.py`, `prescreen-original.json`: original failing counterexample.
- `h2-final-dev.log` and `h2-final-dev/`: actual pinned development smoke.
- `toy-artifacts-final/`: synthetic AUDIT-TOY fixtures only; never empirical evidence.
