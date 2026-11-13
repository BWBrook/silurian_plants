# Review C closure check

Codex (OpenAI GPT-6), 7 November 2026. Reviewed Claude's response in Board discussion 106,
message 2905, and repository `1067c88` (adjudication `8cb6a0f`, Oman analysis `df805b2`).
The older commit identifiers in the handoff predate the authorised privacy-history rewrite.
Claude retains manuscript, figure and scientific claim integration; this tranche supplies
review and a mechanical repair of the claim evidence references.

## Interpretation still requiring a final edit

The revised numerical comparison is explicitly conditional in section 3.3, and the earlier
claims of an observed biological lag have been withdrawn there. A few summary statements
still turn bounds into event dates or a spore minimum into an origin date:

- Main section 4.1 says the recoverable record “begins about 20 Myr after” certain spores.
- Table 3 calls “Land-plant bodies became recoverable about 20 Myr after certain spores” a
  conclusion, even though the inventory omits fragments admitted by the declared category.
- The conclusion says “20 Myr after the lineage or almost at once”. The spore benchmark is
  a minimum, not a lineage origin, and the Oman endpoint bound does not establish simultaneity.
- Brief finding 4 says the method puts bodies “21–24 million years later” and that the gap
  “almost vanishes”. Name the comparison of conditional bounds rather than a measured interval.

Use one consistent statement, adapted to each audience:

> Including the accepted Katian sporangial fragments moves the conditional older bounds from
> 434.5–437.2 Ma to 455.2–456.6 Ma under constant and effort-tracking histories, and to 465.2 Ma
> under decline25. Their separation from the 458.2 Ma spore minimum is not an estimate of the
> time between lineage origin and body recoverability; the fitted recovery histories also
> describe the augmented sequence poorly.

For the brief: “Adding one accepted set of capsule fragments moves the calculated oldest
limit back by about 20 million years. These calculations depend on assumptions about
preservation and cannot date the delay between plant origins and their fossilised bodies.”

Main section 4.1 also calls the Sheinwoodian *Cooksonia* the “oldest unequivocal body fossil”
immediately after accepting older Oman sporangial bodies. Qualify this as an axial or branched
sporophyte record, consistently with the source and category. The accompanying universal
statement that recoverable bodies need lignified tissue is inappropriate for B0, which includes
non-vascular sporangial fragments; describe traits as affecting recovery rather than requirements
for every land-plant body.

These are completion of C1's interpretation repair, not a request for a new model or a
redefinition of B0 after observing the results.

## Provenance repair performed

All 44 claim rows still used pre-rewrite commit identifiers. Those objects remained available
locally, masking the failure a fresh clone would encounter. For each distinct stamp, the parent
matched its commit timestamp and subject to exactly one commit in the rewritten reachable
history, then required identical Git objects for every listed evidence path at the old and new
commits. Only the commit column changed; claim values, limits and statuses did not.

C42 and C43 additionally had genuine evidence-drift warnings: their source audit had gained the
accepted R5 correction distinguishing a stage-base maximum from a separately justified crown
minimum. The parent checked that appended diff against review C/R5 and confirmed the readings
table was unchanged, then stamped both to `8cb6a0f`. This changes neither their source reading
nor their values. No older public history was restored.

A fresh `git clone --no-local` of reachable history, with the repaired ledger copied in, passed
the claims check. The local final ledger has 44 claims cited, zero errors and zero warnings.
No scientific values or support statuses were promoted in this mechanical repair.

## Independent scientific checks and disposition

The companion methods audit (`2026-11-07-review-c-closure-methods.md`) reproduces the
C24/C28/C31/C33/C40/C41 calculations. C40 gives 455.19/456.62/456.09/465.21 Ma for
constant/PBDB/plant-excluded/decline25 in the main reading with Oman; this is not a new
biological lag estimate. There is no numerical blocker to accepting those calculations.
Before final integration:

- C40 and the main prose must identify 452.8 Ma as the **oldest possible** age of the added
  Katian unit, whose stage enclosure is 452.8–445.2 Ma, rather than a point-dated fossil.
- C31/C41 intervals are 5th–95th percentiles across 256 allocations, not full ranges or
  confidence intervals. Table S7 labels this correctly; use the same qualification in the
  ledger and main prose.
- The KS diagnostics use asymptotic p values conditional on treating allocated ages as exact.
  “Exact-age” must not be read as an exact finite-sample test. No combined interval-age test
  or model selection is established.
- The Oman script's frozen comparison is 48 output cells (two readings, four cutoffs, six
  histories), not 48 fossil records. It checks bounds with `np.allclose` default tolerances;
  describe this accurately, rather than claiming an exact whole-output identity check.

The separate membership audit (`2026-11-07-b0-membership-review.md`) checks all 111 E2
observations and the relevant candidate sources. Only S-w22-K12 passes the declared B0
within those checked records. Its count is one locality–age unit, not 12 fragments or three
unmapped samples. The older Hawaz sheets and questioned sporangial contents behind S-w22-Dr4
lack secure land-plant tissue identity and are excluded explicitly; a database sporangial
record also fails the pre-Silurian age requirement. This is a bounded inventory/source check,
not proof of an exhaustive global absence. The primary Oman paper's Caradoc and the later
review's Katian assignment remain distinct.

## Verification and handoff

- `make -C manuscript check` passed lint and citation audits for all profiles. Its initial
  C42/C43 drift warnings were resolved after the specific addendum check described above.
- Final `tools/claims.py check`: 44 claims cited, zero errors, zero warnings.
- Existing Loop 3 tests: 26 passed; `tools/units.py check` passed.
- The methods delegate independently reconstructed endpoints and seeded diagnostics in memory
  from the held inputs. Endpoint differences were at most 4.2e-9 Ma; C41 p-value differences
  were at most 3.4e-13. All 24 checked receipt bindings matched; frozen outputs were not rewritten.
- Parent verified all 44 ledger rows differ only in the commit field, all stamps are reachable,
  and refreshed the candidate manifest after the metadata changes. Manuscript text/PDFs, figures,
  model code, observations and frozen numerical outputs were not edited.

**Verdict:** numerical and present-inventory membership checks pass; a bounded final wording
and metadata integration is still required before Loop 3 closes. Claude can use these audits
as the independent check for the six provisional claims, while retaining their conditional
scope and correcting the age/percentile wording. No additional modelling, data acquisition or
broad review cycle is required by these findings. Final rendering and claim promotion remain
with Claude under the agreed ownership; release remains Barry's decision.
