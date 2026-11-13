# Published Borenshult alternatives and homogeneous screen

This additive review preserves the original sampling-unit tables, frozen M2
declaration, qualification inputs and results. It implements the published reading
in `studies/f3/docs/audits/2026-11-04-borenshult-figure3-reading.md`, independently checked
against the held published Figure 3 and Figure 4. It neither replaces the global `main`/`inclusive`/`outlier` readings
nor changes the occurrence or spore compilation.

`readings.csv` defines three non-nested E1 alternatives. `outcomes.csv` contains each
of the 34 inventoried samples once per alternative, retaining literal outcome
states, figure-specific reports, source locators and the conflict at 41.1 m:

- `figure3-definite`: detected at 43.1, 41.9, 41.1, 40.35, 40.2 and 33.05 m.
- `figure4-definite`: detected at the same depths except 41.1 m, where Figure 4
  lists no trilete taxon and the literal outcome remains `not_reported`.
- `concordant-definite`: a reviewer-proposed reading, not adopted globally, with
  the five depths at which the figures agree counted as detected. The conflicting
  41.1 m report remains `unresolved` and is excluded from both binary conversions.
- All three keep possible-only 48.2 and 34 m `unresolved`. All other
  `explicit_non_detection` and `not_reported` outcomes retain the frozen table's
  reporting basis. No unpublished correspondence is an input.

Figure 3 positions are schematic and mapped to the published sampled depths;
40.35 m uses an offset symbol and leader line. These are sample identities,
not new measurements or exact numerical ages inferred from plot coordinates.

These alternatives are not nested in the old occurrence-reading vocabulary, so
they have their own validator rather than extending every global unit/event row.
The validator checks exact material coverage, published mapping, source links and
the unresolved/figure-conflict distinctions.

## Screen contract

`screen_spec.json` declares the design and binds the existing qualification files.
`studies/f3/models/borenshult_review.py` calls the unchanged pure functions in `screen.py`.
It uses independent, homogeneous units, one comparable class and fixed reference
membership. The reference boundary is the deepest detected sample, 43.1 m in all
alternatives; the screen treats every eligible older zero trial as fully exposed.

Four inventory samples lie below that boundary: 48.2, 59.1, 67.6 and 71.1 m.
Only the latter three provide older zero trials. The unresolved 48.2 m sample is
excluded, not converted to a negative. Thirty samples lie at or above the boundary;
excluding unresolved 34 m leaves 29 reference trials in the literal-figure
complete conversions. The concordant reading also excludes 41.1 m, leaving 28.

- **Complete reported-category:** `detected` gives one; `explicit_non_detection`
  and `not_reported` give zero, conditionally on the documented comprehensive
  category reporting. Unresolved outcomes are excluded on both sides.
- **Explicit-only optimistic diagnostic:** reference trials include only
  detections and explicit non-detections. Older trials retain the complete
  conversion. This asymmetric diagnostic follows the historical screen and does
  not constitute an adopted primary observation model.

The Figure 3 reference is 6/29 or 6/16; the Figure 4 reference is 5/29 or 5/15;
the reviewer-proposed concordant reference is 5/28 or 5/15.
At 41.1 m the Figure 4 `not_reported` state becomes zero only in the complete
conversion; the explicit-only diagnostic omits it. The concordant reading
excludes it as unresolved rather than treating the disagreement as a negative.

The target is intensity `f=1`, the critical value is 5.991464547107979, and the
ceilings are H0=1 and H1=3. Both known-rate and profiled constant-path statistics
are reported at the target and each ceiling. A finite constant-path threshold is
not the full H1 class bound. No reading/conversion excludes `f=1` in this design.
The Figure 3 explicit-only H1 constant threshold is about 2.7655; its full class
bound has not been calculated here.

**Chronological and inferential limits:** this is an all-exposure resource screen.
It does not assign numerical ages to samples, test the fixed 459.1 Ma maximum,
propagate geological uncertainty, or deliver a new qualification or released
confidence bound. The existing engine chooses a stage-base reference boundary;
changing the detected depths alone would not make it use the 43.1 m horizon's
numerical age. Clustering, heterogeneous classes and cross-region transport are
outside this homogeneous calculation.

## Reproduction

From the repository root, the first run writes the new output directory:

```bash
uv run studies/f3/models/borenshult_review.py
uv run --with numpy --with scipy --with pytest pytest -q studies/f3/models/test_borenshult_review.py studies/f3/models/test_screen.py
```

The runner refuses an existing output directory. Replay with a fresh path:

```bash
uv run studies/f3/models/borenshult_review.py --out-dir /tmp/borenshult-review-replay
```

The evidence table has 102 rows (34 samples × three readings); the screen has
12 rows (three readings × two conversions × two ceilings).
Outputs under `studies/f3/models/out/borenshult_review/` are `screen.csv`, exact
`membership.json`, and `receipt.json`. The receipt hashes source evidence,
sidecars, specification, runner, shared screen code and outputs; it also records
unchanged hashes for every file bound by the existing QB-CO qualification.
It contains no private correspondence or copyrighted source text. The held
2019 and 2023 published PDFs are required for the source-hash checks. Tests cover unresolved
exclusion, the 41.1 m conflict, incomplete/duplicate inventories, inadmissible
recoding, receipt hashes and overwrite refusal.
