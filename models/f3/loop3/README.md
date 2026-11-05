# Reviewed positive-record endpoint analysis

`macro.py`, `pilot_figure.py` and `out/pilot_*` are preserved pilot provenance. Use the reviewed
pipeline below for the current scientific results. It is separate from the frozen F3 engine and
qualification system; no qualification status is inherited.

From the repository root:

```sh
uv run models/f3/loop3/build_reviewed.py
uv run models/f3/loop3/analysis.py
uv run models/f3/loop3/simulation.py
uv run models/f3/loop3/suppression_sensitivity.py
uv run models/f3/loop3/oman_sensitivity.py
uv run models/f3/loop3/figures_reviewed.py
uv run --with numpy --with pandas --with scipy --with pytest python -m pytest models/f3/loop3/test_endpoint.py models/f3/loop3/test_simulation.py models/f3/loop3/test_analysis.py models/f3/loop3/test_suppression.py -q
```

The workload is moderate and runs locally. `endpoint.py` implements exact fixed-history
order-statistic bounds; `histories.py` declares the recovery densities and domain. `analysis.py`
forms source/unit/age/geographic sensitivities and shape diagnostics. `simulation.py` tests the
declared procedure and specified failures, not empirical calibration. `suppression_sensitivity.py`
is a complete retrospective extrapolation grid, not a selected confidence result.

The main outputs in `out/` are:

- `reviewed_bounds.csv`: conservative age envelopes by category, reading, recovery history,
  cutoff, unit and source/geographic scenario.
- `primary_unit_membership.csv`: exact source membership of each primary locality–age unit.
- `age_sensitivity.csv` and `classical_comparison.csv`: descriptive age-allocation and classical
  midpoint-age comparisons. Their summary quantiles are not confidence bounds.
- `shape_diagnostics.csv`: conditional-on-maximum KS statistics; nominal exact-age p values and
  sensitivity to age allocation, not a combined test for censored ages or a model-selection rule.
- `delay_sensitivity.csv`: explicitly assumed shifts from recoverability to lineage origin.
- `simulation_results.csv`: coverage, Monte Carlo intervals, claim frequencies and coverage among
  bounded claims for every declared simulation cell.
- `suppression_sensitivity.csv`: all combinations of baseline, stage break and earlier-recovery
  multiplier, with age-support overlap and scope explicit.
- `oman_sensitivity.csv`, `oman_shape.csv`: B0 with the Katian Oman sporangial fragments (S-w22-K12),
  which the declared B0 (macro- and mesofossils) admits but the frozen E3–E5 tail omits; review C,
  2026-11-05. The script checks that it reproduces the frozen B0 rows before writing.
- `fig_macro_recovery.*`, `fig_macro_sensitivity.*`, `fig_macro_suppression.*`: PNG/PDF figures.

Each producing stage writes its own receipt. `beyond_domain` means no bound within 393.47–469.4 Ma,
not proof of an infinitely old origin. A fixed delay shifts the lineage domain as well as its
bound. These results concern a recoverable category under the declared history; crown implications
are a separate biological argument. See `docs/loop3-design.md`, `docs/loop3-results.md` and the
three Loop 3 audits for the scientific interpretation, evidence limits and handoff to Claude.
