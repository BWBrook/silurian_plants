# Public reproduction repairs

Codex, 8 November 2026. This note records the bounded repairs requested in F9 and F12 of the second
GPT-6 Pro review. It does not rerun the full Loop 3 analyses or change any scientific output.

## F9: input prerequisite and comparison policy

`check-public` now depends on `fetch-pbdb`, so the archived CC0 PBDB snapshot is restored and checked
before tests that read `data/occurrences/raw/`. Existing matching bytes are accepted; a different local
file is refused. The target still never substitutes a live PBDB query.

Reproduction retains byte identity for all selected outputs except
`models/f3/loop3/out/stage2_murzuq/dependence_sensitivity.csv`, whose optimiser output can differ only
in last-place floating-point arithmetic. For that one CSV, the comparator requires the same header,
row order/count, identity columns (`grouping`, `frailty_shape`, `separate_well_rates`, `n_reference`,
`n_older`, `scope`, `excluded_well`) and all non-numeric fields. Other numeric fields must be within
absolute tolerance `1e-9`. The receipt records both exact reference and candidate SHA-256 hashes and
the comparison policy, so numerical tolerance is not confused with byte identity. A schema, key,
categorical or materially different numerical value fails.

The focused tests cover round-off acceptance, key changes, large numerical drift, non-numeric drift,
source prerequisite ordering and source-manifest verification. Full `reproduce-derived` and
`rebuild-source` runs remain parent-level checks after the B1 restoration lands.

## F12: public source route

`check-sources` continues to skip cleanly when the private source is absent, while reporting the
expected SHA-256, byte count and public route from the tracked source manifest so an outsider can act
on the result. When the locally held, git-ignored related 2013 thesis is present, it verifies both the
SHA-256 and byte count against `library/closed.tsv`, runs the existing observation check, and reports the institutional route
`https://etheses.whiterose.ac.uk/id/eprint/4475/`. The receipt states that this is the related 2013
thesis, not the exact 2011 conference abstract, and does not redistribute the copyrighted PDF.

## Verification

`uv run --with pytest --with numpy --with pandas --with scipy --with matplotlib python -m pytest
tools/test_reproduction.py -q` passes all six focused tests. Python compilation, Makefile dry-run and
`git diff --check` pass. The full public test target and both reproduction targets await integration
with the restored B1 outputs.
