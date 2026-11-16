# C61 reconciliation: numeric and binding acceptance

Codex, 16 November 2026. Reviewed `7ab70c525871d582341b6028af4d9eb6d8424c87`,
with analysis changes at `ed73e1a`. Bounded follow-up to
`2026-11-16-c61-group-review.md` (committed at `13229b1`). No production,
ledger or manuscript edits were made by this review.

## Verdict

**Numeric, reproduction and case-binding acceptance pass.** The initial
case-binding finding below was repaired by the parent; see the final addendum.

At the initial review, supplement Table S18's Oman “Other units” cell was
`[75]{.C61 .V271}`. V271 selects `groups.csv`, B0 **without Oman**,
`n_guaranteed`. The cell describes `groups_inside.csv`, B0 **with Oman**,
`n_other`; its correct existing binding is **V261**. Both currently equal 75,
so the arithmetic checker passes, but the case-specific evidence link is wrong.
Keep V271 for the B0-without-Oman count in Tables 2 and S17.

## Analysis and independent verification

- `groups.py::shape` now sorts the two cutoff straddlers, enumerates masks
  `00`, `01`, `10`, `11` using `range(2 ** len(partial))`, and searches each
  selected inventory. Thus the two missing single-straddler states are
  genuinely computed, not copied from endpoint states. `groups_shape.csv`
  contains exactly 5 groups × 6 histories × 4 states = **120 distinct rows**.
- Used the saved audit's independent exposure integration and rank-interval
  scheduling verifier, without importing the production selector, recovery,
  optimiser or matching implementation. For **every one of the 120 rows**,
  independently verified the selected count, finite-KS threshold decision and
  optimal p within its three-significant-digit rounding interval. Constructed
  passing witnesses were checked against all supports and their KS statistics
  were calculated directly. SciPy's KS distribution remains a shared
  probability-distribution dependency, as disclosed in the original audit.
- Checked every `groups.csv` maximum p and number of passing states directly
  against the corresponding four `groups_shape.csv` rows. All agree. The new
  B1-main plant-excluded PBDB maximum p of **0.266** comes from a single-straddler
  state; the all-possible p of 0.260 is no longer incorrectly treated as the
  overall maximum. Pass/fail conclusions are unchanged from the independent
  four-state review.
- Reconstructed all four counting rules directly from the horizon CSV, using
  the timescale CSV for midpoint-stage grouping. All **20** group × counting
  rule counts and endpoints agree with the new output. Shape searches remain
  locality–age searches; the four counting rules are endpoint sensitivities.

| Group | Collection endpoint | Locality endpoint | Locality–age endpoint | Region–stage endpoint (Ma) |
|---|---:|---:|---:|---:|
| B0 +Oman | 454.453227 | 455.2511 | 455.185345 | 458.819619 |
| B0 −Oman | 434.009030 | 434.5518 | 434.506834 | 437.040691 |
| B1 main | 434.087039 | 434.703019 | 434.649615 | 437.190979 |
| B1 inclusive | 446.697153 | 447.4294 | 447.367027 | 450.276714 |
| B2 main | 428.001084 | 428.8870 | 428.840006 | 432.375017 |

The B1-main extrema are correctly **434.1–437.2 Ma** when rounded to one
decimal place, with 101 collections and 29 region–stage units. The former
“434.6 Ma or older at every count” numerical problem is repaired.

## Strict bindings

Independently resolved all **75** new C61 binding rows, V246–V320. Every JSON
selector matches exactly one evidence row, every selected value agrees with
its display rounding, and all **102** nonempty C61 cited spans in
`manuscript/text/main.md` and `manuscript/text/supplement.md` use exactly one
permitted binding. There are no orphan binding IDs. The brief and agent guide
were not reconciled by this check; companion-product updates remain deferred.
Then checked cited case meaning against selector meaning; this catches the
Oman/V271 mismatch above, which these numeric checks cannot detect.

Equal numbers in different groups are otherwise separated correctly: for
example B1-main 432.9 Ma uses V248, while B0-without-Oman 432.9 Ma uses V273;
Oman's 12.30 Myr shortest gap uses V310, while Zbrza's 12.30 Myr longest gap
uses V316. The B1 p bindings select the explicit guaranteed state `00`,
matching the corresponding prose/table qualification.

## Production reproduction

Imported `groups`, redirected `OUT` to a temporary directory, copied only its
required `reviewed_bounds.csv` comparison input there, and ran `groups.main()`.
Compared each emitted CSV's bytes against its saved counterpart; all three
were identical. The temporary directory was removed automatically. Saved
project evidence was not overwritten.

| Output | SHA-256 |
|---|---|
| groups.csv | `1e9851cd035177f001618f5633474622a6dc1826293f38953ae38923d3711076` |
| groups_shape.csv | `ac8f49f5b6ba00a80f73a4fe471c1f49efe12c78eb0b1798f510e9fd197e8077` |
| groups_inside.csv | `1d2c0afc4150558d5fec97dad6f98ed94eccb4791e3e7bfc7bceead5bfbc27b4` |

No unrelated analysis or new regression tests were run. Source membership,
biological interpretation and final ledger acceptance remain with the parent
reviewer and the separate source/inside-measure checks.

## Final targeted acceptance

Confirmed the parent's exact correction: Table S18's Oman “Other units” 75
now uses **V261** (B0 with Oman, `n_other`); Table S17's B0-without-Oman 75
retains **V271** (`n_guaranteed`). The corresponding main-text gap count and
Table 2's without-Oman count also retain their correct V261/V271 distinction.
No number changed and no numeric search was rerun. The sole case-binding
finding is resolved; this bounded numeric/binding review is accepted.
