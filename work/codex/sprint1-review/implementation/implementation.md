# Qualification integrity implementation handoff

31 October 2026. Owned files: `models/f3/qualify.py`, `m2.py`, new
`qualification_contract.py`, `designs/m2.toml`, and new
`test_qualification_contract.py`. No commits, source-table edits, estimator edits,
frozen-output rewrites or full qualification ensembles were made by this delegate.
Exact final file hashes are in `code_hashes.json` alongside this note.

## Implemented

- Receipts bind the active declaration, every directly consumed source CSV, the
  source-file hash register and reporting rule, timescale, all eight statistical
  dependency modules, generated units/exclusions, specification, class scope,
  complete declared quantity grid and phase protocol. Original PDFs remain the
  parent's independently checked provenance inputs; compute binds their register.
- Python major/minor and exact NumPy/SciPy versions are binding. Full Python and
  platform versions are recorded. Deterministic inputs match exactly. Recomputed
  reference rates and boundary-f values have explicit 1e-8 absolute/relative
  tolerance; acceptance and stage 2 then use the calibration's exact saved rates
  and resolved truths, including in spawned workers.
- Every consumed attempt is retained, including rejected screens and failures.
  Screen metadata must agree with its decision. Pre-screen errors prevent binding
  completion; unconverged screens raise instead of masquerading as S1 exclusions.
  Post-screen failures remain failures for every required quantity. Explicit
  no-first-appearance abstentions receive all mandatory scores.
- Quantity schemas are derived before draws. Missing, extra or malformed scores,
  invalid Boolean fields, duplicate/missing/reordered attempts, early stopping,
  forged summaries, missing grid cells, stale dependencies and incompatible seeds,
  targets, caps or shifts are refused. Calibration, acceptance and stage-2 pooling
  are independently reconstructed from the saved replicate rows.
- Receipt payload and replicate bytes have hashes; stage dependencies bind exact
  receipt files. Artifacts are immutable. Old receipts are historical and cannot
  be silently resealed or attached as current qualification.
- Empirical results recompute the current screen, validate the whole qualification
  chain and record the bound receipt hash. Nonprimary variants are explicitly
  unqualified sensitivities. QB main/zero is an inadmissible coding diagnostic.
  QB H0c remains an unqualified class diagnostic; H0m/H0/H1 retain their declared
  qualification scope. A sensitivity may still run when its primary fails the
  screen and no primary receipt exists.
- Boundary ages/classes and origin grid spacing come from the declaration.
  The estimator is unchanged. The agreed review amendment adds B3 at the central
  H0(459.1) boundary and B4's nonmonotone pre-459.1 window history; Q8's unchanged
  later intensity is explicit. B4 is scored only in H0/H1. The final grid is
  12 acceptance plus three diagnostic cells.
- Binding roots are fresh: calibration 20261111, acceptance 20261112 and stage 2
  20261113. Development retains 20261100. Target/cap remain 1,000/20,000, with the
  original 0.955 calibration, 0.95 nominal and 0.93 acceptance-floor contract.

## Verification

Pinned local runtime: Python 3.12.15, NumPy 2.3.4, SciPy 1.16.3.

```sh
PYTHONDONTWRITEBYTECODE=1 /private/tmp/sp-f3-pinned/bin/python -m pytest -q -p no:cacheprovider models/f3/test_qualification_contract.py models/f3/test_designs.py
```

**58 tests passed in 9.51 s.** The tests include a full 1,000 + 1,000 stage-2
pass/fail boundary lifecycle using explicitly synthetic artifact fixtures. They
test integrity and protocol handling; they are not statistical qualification.

The final actual QB development CLI smoke ran all 15 cells: **45 passing
replicates from 70 consumed attempts, zero pre-screen or post-screen errors**.
Its artifact directory is `/private/tmp/sp-sprint1-contract-final-dev-b4/`; its
log is `/private/tmp/sp-sprint1-contract-final-dev-b4.log`. Summary and artifact
hashes are in `dev_summary.json`. This three-pass-per-cell smoke is nonbinding.
Independent review and the parent-owned cross-machine binding check are separate.

## Regeneration path

Use the pinned runtime and a fresh qualification directory. Each phase validates
its predecessor before drawing anything; existing artifacts cause refusal.

```sh
python models/f3/qualify.py --design LY-MZ-CU --rho 1 --phase calibrate --workers 8 --out-dir NEW_QUAL_DIRECTORY
python models/f3/qualify.py --design LY-MZ-CU --rho 1 --phase accept --workers 8 --out-dir NEW_QUAL_DIRECTORY
```

Run `--phase stage2` only for a complete stage 1 with borderline quantities.
Calibration includes diagnostics; acceptance includes the 12 acceptance cells;
stage 2 runs only cells with borderline quantities and pools only those quantities.
`--target` and `--no-diagnostics` are development-only options.

After accepted current evidence exists:

```sh
python models/f3/m2.py results 8 --qual-dir NEW_QUAL_DIRECTORY --out-dir NEW_EMPIRICAL_DIRECTORY
```

No historical receipt is a prerequisite or a valid substitute for this rerun.
The new grid, fresh seeds, class scope and changed protocol artifacts require new
calibration/acceptance evidence. Numerical empirical read-outs should be compared
with the retained baseline; Monte Carlo counts should not be expected to match
because the phase seeds and grid changed.
