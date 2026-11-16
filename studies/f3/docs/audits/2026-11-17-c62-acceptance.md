# C62 reconciliation accepted

Codex, 17 November 2026. Acceptance review of `220887a`, analysis `8af9f56`,
against the review at `39305fd`. **C62 is supported.** The three scientific
repairs hold. The acceptance adds case-specific count metadata and corrects
bindings; it changes no scientific value or inventory membership.

## Scientific reconciliation

| Review finding | Accepted repair |
|---|---|
| The main record was described as empty only after silently excluding Oman | The main calculation now retains Oman: one early body unit among 76, with 75 later units. The no-Oman zero-count inventory is explicitly a sensitivity. |
| The conditional requirement was called a historical requirement already met | The realised-precedent assertion is withdrawn. The Discussion, C62 estimand and ledger describe a model-conditional comparison to the vascular requirement, with post-selection status in Conditions and S19. |
| Oman was used to distinguish finding from recognisability too broadly | The text says that some bodies were recognisable in the Katian and this weakens a universal first-recognisability date of 432.9 Ma. Changes in recognisable body forms can contribute to lower mean finding; they are not presented as a sufficient shared-onset delay. The ash age is nominal with its quoted uncertainty, and continuity of producers, body forms and features remains open. |

The original source/meaning reviewer independently accepts these repairs in
`estimands.md`, Discussion, Conditions/S19 and the ledger. No new source reading
was needed; the Borenshult and Oman primary-source checks remain as recorded
in `2026-11-16-c62-source-meaning-review.md`. The parent agrees the revised C62
estimand. The comparison concerns broad land-plant bodies and does not
demonstrate a historical rate reduction or its transfer to crown vascular plants.

One ambiguity remained in the reconciliation: C62 still offered later
recognisability as a separate sufficient alternative, inviting the shared-delay
reading used for the vascular examples. Such an onset must still admit the early
Oman body. The final accepted wording instead says that changes in which body
forms were recognisable could contribute to lower average finding. This
clarification reaches the estimand first, then the ledger, Discussion, S5.11,
S19 and questions register. The independent source/meaning reviewer checked
the final wording and accepts it. No number or model calculation changes.

## Independent counts and arithmetic

The parent reconstructed B0 main units directly from `horizons_reviewed.csv`
with the standard-library CSV reader, grouping by locality and age group or
region and midpoint stage from `data/timescale.csv`. This used no production
selection function. Guaranteed units were divided at 432.9 Ma and the nominal
454.41 Ma spore anchor. Oman is the sole early unit in both counting treatments.

| Treatment | Total units | Early units | Later units | Factor |
|---|---:|---:|---:|---:|
| With Oman, locality–age | 76 | 1 | 75 | 8.411773508072 |
| Without Oman, locality–age | 75 | 0 | 75 | 13.386575599019 |
| With Oman, region–stage | 31 | 1 | 30 | 3.240458877031 |
| Without Oman, region–stage | 30 | 0 | 30 | 5.194785624434 |

All four factors were independently obtained by directly summing the binomial
polynomial and inverting its 0.05 tail by bisection. No production root-finder
or closed-form routine was used. With `G = 21.51`, `L = 39.43` Myr and
`p = rho*G/(rho*G+L)`, the one-positive tail is
`(1-p)^n + n*p*(1-p)^(n-1)`. This verifies the new main-case factors and the
unchanged zero-count sensitivities at the saved precision. The sampling model
conditions on the total count in these fixed windows; it is distinct from
C61's exact-oldest-conditioned Oman gap. Its post-selection qualification is
preserved.

## Binding completion

The Discussion's main-case 75 later finds still used V322, the total of the
no-Oman sensitivity. This equals 75 numerically, but obscures the case. Evidence
commit `ce6eb02` adds `n_later` to the two spore-anchored rows, using the already
computed later-unit selection. All previous output cells are unchanged.

The main passage now uses V336, selecting the with-Oman spore case's explicit
`n_later`. V322 remains the no-Oman sensitivity's total. V321, V325 and V327
also now select the accepted main case for its shared span and later-window
parameters. All 15 C62 binding rows and all 15 numeric spans were checked
against their intended cases and rounding. Existing C61 selectors remain
unique and preserve their original values.

Production reproduction in a temporary output directory is byte-identical for
`groups.csv`, `groups_shape.csv` and `groups_inside.csv`. The first two tables
remain byte-identical to `220887a`; all pre-existing cells of the five-row
inside table remain equal. Only the later-count metadata column is added.
C61 is restamped after this verification and stays supported.

## Disposition

The acceptance is recorded in the study decision log and questions register;
Q1 and Q2 keep their statuses. The manuscript checks, rendered comparison and
package manifests accompany the acceptance commit. Companion products,
broader prose work and existing untracked drafts are outside this review.

Final checks: `make -C studies/f3/manuscript check` passes with 60 supported
claims, two superseded and none provisional, zero errors and warnings, and
all profile citation audits passing. The main and supplement builds pass;
the comparison passages were inspected at article page 10 and supplement
page 22. The PDFs remain 20 and 39 pages. Package generation records 444
candidate files and no private sources; their sizes and SHA-256 hashes were
verified after generation.
