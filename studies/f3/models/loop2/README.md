# Loop 2 sprint 1 reproduction

Result and scientific limits: `../../docs/loop2-sprint1-results.md`.
The design was declared in `robustness_design.json` before the numerical grid.
These files implement sensitivities and method validation, not a new qualified primary design.

From the repository root:

```sh
python3 studies/f3/tools/loop2_observations.py check
uv run --with numpy --with scipy --with pytest python -m pytest studies/f3/models/loop2/test_count_share.py studies/f3/models/loop2/test_contamination.py -q
uv run studies/f3/models/loop2/count_share_validation.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run studies/f3/models/loop2/engine_sensitivity.py --workers 4
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run studies/f3/models/loop2/contamination.py --full --workers 4
uv run studies/f3/models/loop2/figures.py
```

Reruns overwrite only Loop 2 outputs. Receipts record runtime versions; times and PDF metadata can
change on rerun. Scientific CSVs and source bindings are the evidence, not receipt timestamps.
At most four local workers are permitted; the completed grids take seconds on mini.

A runnable **hypothetical protocol example**, not fossil data:

```sh
uv run --with numpy --with scipy python - <<'PY'
import sys
sys.path.insert(0, 'studies/f3/models/loop2')
from count_share import common_effort_bound, zero_target_stratified_bound
print(common_effort_bound(0, 10, effort_ratio=1.0))
print(zero_target_stratified_bound([10], [1.0]))
print(common_effort_bound(0, 10, effort_ratio=None))
PY
```

The first two yield rate-ratio upper limit 0.3492828477 under known equal effective effort;
the last yields an infinite ratio bound because unknown effort has no positive lower limit.
The module never treats a total palynomorph count or a percentage as a trilete/control tally.

Outputs:

- `out/count_share_validation.*`: exact conditional-method checks and explicit misspecification examples.
- `out/engine_sensitivity.*`: 36 frozen-engine diagnostic cases and baseline cross-checks.
- `out/engine_sensitivity_reference_inventory.csv`: unmatched core/cutting reference inventory.
- `out/contamination_grid.csv`: 5,760 joint comparisons with separate model-conflict status.
- `out/contamination_break_even.csv`: 384 root/no-root entries for the kappa=0 surface.
- `out/contamination_manifest.json`: bound source and output hashes.
- `out/engine_influence.*`, `out/joint_window_sensitivity.*`: PNG/PDF figures, bound by `out/figures.json`.
- `claims.csv`: claim-to-evidence status ledger.

The contamination model's constant indigenous intensity differs from the frozen flexible H0
exposure-weighted mean. No-transfer roots are likelihood-comparison contours, not confidence
regions. Shared chronology scenarios are fixed ordered stress cases, not estimated geological
probabilities. A model-conflict row cannot be read as an old-origin compatibility result.
