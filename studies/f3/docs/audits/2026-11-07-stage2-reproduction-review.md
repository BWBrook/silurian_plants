# Stage 2 reproduction and package-closure review

7 November 2026. Codex, bounded read-only audit. The working graph was still
mutable, so this review did not run the slow derived or source rebuild.

## What is sound

`tools/reproduce.py` builds its temporary tree from `git ls-files`, so a public
derived run cannot accidentally read an ignored private source or a local
untracked working file. Source mode restores the declared PBDB archive into
that temporary tree before running `build_reviewed.py`; it does not issue a
live PBDB query. `fetch_pbdb_snapshot.py` verifies the compressed payload hash,
decompressed raw hash and byte count, refuses a different existing target, and
writes through a `.part` file before replacement. The archive is labelled CC0
and its URL, DOI, query, retrieval date and both hashes are in
`data/external/pbdb-snapshot.json`.

The source-only check is honest: when the copyrighted Abuhmida thesis is not
present, `make check-sources` prints `status: SKIPPED` with the missing path;
it does not report a false pass or copy the PDF into the candidate. The
package data manifest labels `library/closed/` and the third-party local
deposit as excluded private inputs, and labels the PBDB CSV as a public
immutable bulk archive excluded from Git.

`manuscript/Makefile` checks the exact makedoc commit and a clean makedoc
working tree before linting. The current lock commit and live checkout both
equal `b613e715a86f81623953403f84353314405057db`. The lock intentionally does
not pin TeX or Pandoc, and the README says so.

The temporary-fixture regression tests pass:

```
uv run --no-project --with pytest pytest -q tools/test_reproduction.py
2 passed
```

The three reproduction scripts compile successfully. The slow derived/source
runs remain for the parent after the inventory tranche is committed.

## Current R8 disposition

The former additive `oman_sensitivity.py` route is now deliberately retired.
Canonical and explicit-exclusion B0 values are read from the reviewed
inventory outputs by the figure/table path, while the historical Oman receipt
is retained as archived provenance at commit `df805b2`. `package.py` now marks
`models/f3/loop3/out/oman_receipt.json` as archived provenance with a commit
locator rather than requiring the deleted historical script. A direct closure
probe now succeeds and returns that archived edge.

Receipt-local paths are now resolved against the receipt directory (or its
parent when needed) and fail explicitly when unresolved or ambiguous. This
removes the previous silent omission of local receipt edges. The working graph
is still mutable, so the package manifests and generated receipts must be
regenerated once the parent commits the final canonical outputs; the current
working-tree hashes are not yet a release receipt.

## Closure limits to retain

The closure is useful but not a complete static dependency proof. Runtime
assets named only inside arbitrary Python or Markdown are not discovered; the
package's explicit seeds and receipts cover the present Loop 3 graph but do
not remove that limitation. Archived receipts are provenance records, not
current executable dependencies, and are labelled with their historical
commit rather than silently treated as present files.

The public rebuild intentionally copies only tracked files. Until the new
inventory inputs and methods are committed, an invocation from this dirty
working tree will omit untracked additions such as
`data/macro/body_membership.csv`; the parent should commit the coherent graph
before treating the derived/source results as public-build evidence. The
reproducer compares the selected Loop 3 CSV outputs, not every generated
receipt, figure or manifest; that scope is stated in its JSON receipt and
must not be inflated to full-tree identity.

## Verdict

Archive integrity, private-source exclusion, honest source skipping, the
makedoc revision gate and the repaired receipt-local closure are sound. Final
derived/source runs and a post-commit package regeneration remain outstanding;
those are release checks, not a remaining Oman dependency defect. No
scientific status or output was changed in this audit.
