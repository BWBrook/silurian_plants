# Sprint 2 pipeline reuse gate

Read-only check by Codex against repository HEAD `63ca45e` in
`/Users/bwbrook/papers/silurian_plants`. This is the bounded reuse gate, not the
scheduled full scientific counter-review of M2. The check edited no repository files or frozen
outputs; its scratch evidence is now integrated under data/units/sprint2/pipeline/.

## Checks completed

- Read `models/f3/README.md` Step 5, `designs.py`, `m2.py`, `qualify.py`,
  `designs/m2.toml`, and `docs/audits/2026-10-31-m2-real-designs.md`.
- Eleven tests in `models/f3/test_designs.py` passed in 1.09 s.
- The development qualifier for LY-H2-CU, rho=1, target=40, root seed 20261100,
  four workers completed all thirteen cells in 7.3 s: 520 passing replicates
  from 561 attempts, with zero errors among passing rows. B1 had one
  nontrivial H0/H0c claim, neither missed; B2 had zero such claims.
- All 28 JSON qualification receipts under `models/f3/out/qual/` matched their
  five currently recorded code hashes. Those hashes cover envelope.py,
  designs.py, m2.py, qualify.py, and designs/m2.toml only.
- For LY-H2-CU/rho1, the saved calibration table had 13,000 passing rows and
  the acceptance table 10,000. For every cell, row counts, distinct ordered
  replicate IDs, last-index-plus-one attempt counts, and all stored coverage
  counts matched the corresponding receipt. Calibration is marked complete,
  target 1,000; acceptance is marked pass, target 1,000. No ensemble was rerun.

Interpreter:
`/Users/bwbrook/.cache/uv/archive-v0/vsTkiUdBbIXXYrS1/bin/python`.

Test command, from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/bwbrook/.cache/uv/archive-v0/vsTkiUdBbIXXYrS1/bin/python -m pytest -q -p no:cacheprovider models/f3/test_designs.py
```

Development command:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 /Users/bwbrook/.cache/uv/archive-v0/vsTkiUdBbIXXYrS1/bin/python /tmp/sp-sprint2-pipeline/run_dev.py --design LY-H2-CU --rho 1 --phase dev --target 40 --workers 4
```

The wrapper sets `qualify.OUT` to scratch because the CLI has no output-directory
argument. Scratch evidence:

- `/private/tmp/sp-sprint2-pipeline/run_dev.py`
- `/private/tmp/sp-sprint2-pipeline/dev.log`
- `/private/tmp/sp-sprint2-pipeline/dev/LY-H2-CU_rho1_dev.json`
- `/private/tmp/sp-sprint2-pipeline/dev/LY-H2-CU_rho1_dev_reps.csv.gz`

Checked saved receipts and replicate tables:

- `models/f3/out/qual/LY-H2-CU_rho1_calibrate.json`
- `models/f3/out/qual/LY-H2-CU_rho1_calibrate_reps.csv.gz`
- `models/f3/out/qual/LY-H2-CU_rho1_accept.json`
- `models/f3/out/qual/LY-H2-CU_rho1_accept_reps.csv.gz`

## Gate outcome and necessary repair

The computational smoke passes; source assembly and exploratory E2 screening can
reuse the machinery after an event-specific adapter exists. A binding E2
certificate needs active-input and receipt binding first:

1. `qualify.py:325-328` always hashes designs/m2.toml, even if F3_DESIGNS selects
   M1. The active declaration, source data, timescale, and validate.py (which
   supplies calibration/acceptance rules) are not all bound.
2. `qualify.py:353-361` checks only that limited code dictionary. It does not
   enforce matching design/protocol/grid, declared replicate count, calibration
   completeness, or a finite non-negative shift. The target override is not
   restricted to development. Stage 2 lacks the older harness's
   replicate-to-summary evidence checks.
3. `m2.py:96-109` reads shifts and verdicts without integrity checks before
   attaching them to empirical outputs.

Bind the active declaration, generated units and underlying inputs, all
statistical dependencies, expected quantities and protocol; refuse incomplete or
inconsistent evidence before attaching "qualified". These gaps do not show that
the sampled existing M2 receipts are wrong.

## Precise acceptance interpretation

The amended screen evaluates frame potential by setting the predeclared
transported-unit outcomes to zero; full analysis uses the actual outcomes. Its
qualified error quantity is

`P(a delivered claim excludes truth | the potential screen passes)`.

Abstentions are counted as non-errors. This is not coverage conditional on
receiving an informative claim. Calibration targets 0.955, nominal coverage is
0.95, and independent acceptance assesses the 0.93 floor on the specified finite
grid. The audit's "certified <=0.05" wording is stronger than that acceptance
contract establishes. Claim and miss counts must accompany the result.

## E2 reuse limits

- Freeze transported membership from source/design information, never observed
  event presence. Potential screening suppresses those outcomes only for the
  screen; empirical analysis retains them.
- E2 needs its own source builder, readings, reference support, reporting and
  eligibility rules, ages and qualification grid. Changing the event label alone
  does not change the E1 source builders.
- Qualification boundary resolution still hard-codes 469.4 Ma in
  `qualify.py:296-302`; M1 cannot inherit the M2 cells unchanged.
- Transport ratios are fixed scenarios. The implementation does not estimate
  between-section variance from a single section or model contaminating
  positives. The oldest-possible first-appearance rule is not a full
  contamination model.
- The estimator assumes independent ages; the simulator orders ages only within
  its declared groups. This does not qualify arbitrary shared-boundary or
  chronological dependencies.
- Only primary variants have their own qualification. Other variants inherit
  the primary shift and remain sensitivity calculations.

No claim here certifies all M2 science or all future E2 designs.

## Sprint-2 disposition

No M1 numerical design was admitted after the source assessment. Consequently no
binding E2 reuse, model edit or qualification rerun was needed in this sprint.
The receipt/protocol repairs and scientific interpretation remain explicitly open
for the scheduled sprint-1 counter-review; the smoke is not binding qualification.
The retained development receipt/replicates and runner are in
`data/units/sprint2/pipeline/`. The runner redirects new runs to local scratch.
