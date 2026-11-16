# C61 reconciliation accepted

Codex, 16 November 2026. Acceptance review of `7ab70c5`, evidence `ed73e1a`,
against `2026-11-16-c61-review.md` and the current interpretation specification.
**C61 is supported after one equal-valued binding correction.** No numerical
result, inventory membership or biological interpretation changes in this turn.

| Previous finding | Acceptance evidence | Disposition |
|---|---|---|
| Endpoint read as a required clock maximum; B1 conflated with Hooper's fossil category | The new C61 estimand, Results (i), Discussion, Conclusion and S5.11 restrict the comparison to this endpoint method. Hooper's Irish *Cooksonia* is described as total-group Tracheophyta; B1 is broader. The text explicitly leaves a B1 start at 431.2 Ma open. | Accepted |
| 434.6 Ma claimed at every count | All four counting rules are now reported: 434.09–437.19 Ma, including the 101-collection result. The range reaches the Abstract, Results, Table 2 caption, Discussion and Conclusion. | Accepted |
| Selected gaps presented as historical lower bounds | The text defines conditional, post hoc two-rate benchmarks on average finding; the main Conditions list and five new S19 rows retain the model and selection assumptions. S18 headings identify factors. The shape tests address a different question. | Accepted |
| Two cutoff-membership states omitted | The script enumerates all four subsets and writes 120 case rows. A separate rank-interval scheduling implementation checks each verdict and brackets each saved p value at its displayed precision. All current verdicts are preserved. | Accepted |
| Missing-record account leaves the *Capesporangites* age open and implies an exhaustive extra-unit count | The main text, S5.11 and closed-literature register give the published Pridoli stage, distinguish a missing taxon from the existing Kosov unit, and retain unread bed/provenance details. Ludford Lane's abstract establishes bodies without a branching account; one-to-four additions is a sensitivity to named leads. | Accepted |

## Numerical and binding checks

The bounded independent acceptance check is
`2026-11-16-c61-reconciliation-numerics.md`. It reconstructs all 20 counting-rule
endpoints, checks all 120 inclusion-state shape rows and their aggregate
verdicts, and verifies that the production script regenerates `groups.csv`,
`groups_shape.csv` and `groups_inside.csv` byte-for-byte in a temporary output
directory. The earlier independent group, gap and primary-source checks remain
the supporting evidence; unchanged analyses were not repeated wholesale.

All 75 C61 bindings were traced to their cases, including equal-valued cells.
One remaining mismatch was found in Table S18: the Oman gap's 75 **other** finds
used V271, the count of the separate inventory **without** Oman. It now uses
the existing V261, selecting `groups_inside.csv`, B0/main/with Oman, `n_other`.
Table S17's B0-without-Oman count retains V271. The printed value stays 75.
This is a binding repair, not a new or changed result.

Visual inspection also found the full code path in the S18 caption running
beyond the page. It is shortened to `out/groups_inside.csv`, relative to the
analysis directory named at the start of S5.11. No source or claim changes.

The complete scientific reconciliation is accepted; `estimands.md`'s C61 entry
is agreed. The study decision log and questions register record the acceptance.
Q1 and Q2 keep their statuses. Younger E3 screening and the detailed
*Capesporangites* bed remain explicit limitations; this acceptance does not
certify an exhaustive fossil inventory or identify actual finding histories.

Final verification:

- `make -C studies/f3/manuscript check` passed: 59 supported claims, two
  superseded, none provisional; zero errors and warnings; all profile reference
  audits passed. The final source change also passes the claims check.
- `make -C studies/f3/manuscript supplement` passed. The repaired S18 caption
  and S19 conditions were visually inspected. The article has 20 PDF pages;
  the supplement has 39, as the checked-in `7ab70c5` supplement already did.
- `python3 studies/f3/manuscript/package.py` refreshed the package and
  dependency manifests: 444 candidate files, no private source files included.

Companion-product revisions and broader prose trimming remain outside this
bounded reconciliation.
