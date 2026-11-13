# Stage 2 numeric claim binding

7 November 2026. Codex implementation for R9.

`tools/claims.py` now recognises the optional `manuscript/value-bindings.csv`
sidecar. A claim present in that sidecar is strict: every numeric citation
span in the checked renderings must carry exactly one unique `.V###` class.
The binding resolves its own evidence path, JSON equality selector and source
field, then checks the displayed value with the existing precision and
rounding rule. A value elsewhere in the claim cannot satisfy that binding.
Missing, non-unique or empty selectors, wrong claim IDs, source-field drift,
and display values that do not match their selected source row are errors.
Claims without sidecar rows, including superseded legacy citations, retain the
existing checker behaviour.

The initial strict set is C27. All 19 numeric C27 spans in `brief.md`,
`main.md` and `for-agents.md` have unique bindings to the B2 primary Emsian
rows in `models/f3/loop3/out/reviewed_bounds.csv`; the supplement has no
numeric C27 span. The sidecar distinguishes constant, PBDB-density,
plant-excluded, 25 Myr decline and domain-limit fields rather than pooling
the C27 values.

Verification:

- `uv run --with pytest pytest -q tools/test_claims.py`: 8 passed.
- `python3 tools/claims.py check manuscript/claims.csv manuscript/text/main.md manuscript/text/supplement.md manuscript/text/brief.md manuscript/text/for-agents.md`: 0 errors, 0 warnings.

C40, C45 and C47 are deliberately not strict in this tranche. Their source
records need agreed row or arithmetic selectors before adding `.V###` classes;
the legacy pooled checks remain active for them.

## Parent integration

The final strict set also includes C40 (V020–V034) and C48–C52 (V035–V052), bound to
canonical rows for body endpoints, frontier cases, interval witnesses, boundary scenarios,
dependence conventions and signed influence. Remaining legacy claims are explicitly left for
Claude's ledger/prose integration. The parent fixed ASCII-minus parsing when adding signed
influence values; that regression is now covered. The earlier paragraph describing C40 as
unbound records the initial tranche and is superseded by this integration note.
