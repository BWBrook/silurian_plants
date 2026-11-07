# Stage 2 body inventory, B2 frontier and influential-record check

Codex (OpenAI), 7 November 2026. This audit implements R2, the assigned part of R3, the
Xiemisitai correction in R6 and the targeted influential-record check. It does not alter the
manuscript, claims ledger, Loop 1/2 qualification or simulation qualification.

## Decisive findings

1. **The canonical B0 inventory now matches its declared category.** `S-w22-K12` enters as one
   Ghaba-1 locality-age unit in each of the separate main and inclusive inventories. It is B0 only:
   the source supports spore-filled fragments with covering interpreted as sporangial wall, not an
   axis, branching sporophyte or crown-tracheophyte character. The numerical Katian interval,
   452.8--445.2 Ma, is derived at rebuild time from `data/timescale.csv`. `S-w22-Dr4` remains an
   explicit identity rejection in `data/macro/body_membership.csv`; its cuticle-like sheets and
   monad cluster do not demonstrate accepted land-plant tissue.
2. **The former E3--E5-tail B0 inventory remains reproducible as an exclusion sensitivity.** Under
   constant intensity, the main canonical inventory has 76 guaranteed units, oldest possible age
   452.8 Ma and conditional bound 455.185345 Ma. Excluding K12 reconstructs 75 units, 432.9 Ma and
   434.506834 Ma. The 20.68 Myr movement is oldest-member sensitivity, not a biological delay.
3. **An executable category check exposed and repaired a pre-existing B1 leak.** The builder had set
   B1 true for every E3, E4 or E5 tail record, although B1 is defined by E3 and nested E5; E4-only
   tracheid evidence is synthesis evidence, not evidence of a branching polysporangiophyte. The repair
   removes `M-bohemica`, `M-capel-horeb-ludlow` and `M-lang-tracheid-axis` from main B1, while
   inclusive `M-bohemica` remains through its E5 reading. Main B1 changes from 72/70 possible/guaranteed
   units to 69/67 and its constant bound from 434.624082 to 434.703019 Ma; inclusive changes from
   76/74 to 74/72 and from 447.337146 to 447.397755 Ma. This is a category repair, not Monte Carlo drift.
   All 48 B2 locality-age primary bounds remain exactly unchanged. The Xiemisitai geography correction
   changes B2 region-stage collapse from 20 to 19 units and its constant bound from 432.069514 to
   432.375017 Ma.
4. **The B2 frontier exposes strong unit dependence.** With zero assumed diagnostic delay, the
   primary 48-unit contour requires earlier/later intensity 0.476 at 431.2 Ma, 0.124 at 444 Ma and
   0.0846 at 452 Ma. The corrected 19-unit region-stage contours are 1.261, 0.328 and 0.224; the
   15-unit curated-tail contours are 1.632, 0.425 and 0.290. Values above one are increases, not
   reductions. These are retrospective flat-plus-step compatibility contours, not fitted recording
   rates, likelihood support or a joint confidence region.
5. **Influential-record effects differ by endpoint and recovery history.** Under constant intensity,
   removing three Yea/Baragwanathia locality-age units moves the B2 bound 1.67 Myr younger; removing
   five represented Bathurst/Zosterophyllum units leaves the oldest age unchanged and moves the bound
   0.26 Myr older. Removing *Cooksonia barrandei* moves B1 2.38 Myr younger, but changes canonical B0
   by only 0.03 Myr because Oman controls its oldest age. Across all six histories, signs can change
   where the loss of count competes with the loss of the oldest record; no leave-out result is a
   reidentification or preferred fossil reading.

### Exact integration values

| Inventory/reading | Possible/guaranteed | Oldest possible (Ma) | Flat | PBDB all | PBDB plant-excluded | Decline25 |
|---|---:|---:|---:|---:|---:|---:|
| B0 canonical, main | 78/76 | 452.8 | 455.185345 | 456.622183 | 456.089449 | 465.209081 |
| B0 without Oman, main | 77/75 | 432.9 | 434.506834 | 436.375532 | 435.732079 | 437.156146 |
| B0 canonical, inclusive | 82/80 | 452.8 | 455.063832 | 456.427474 | 455.921879 | 464.403648 |
| B0 without Oman, inclusive | 81/79 | 445.2 | 447.199304 | 448.269647 | 447.845653 | 452.978598 |
| B1 corrected, main | 69/67 | 432.9 | 434.703019 | 436.799875 | 436.077860 | 437.729166 |
| B1 corrected, inclusive | 74/72 | 445.2 | 447.397755 | 448.574340 | 448.108261 | 453.901128 |

The two decline10 histories remain beyond the 469.4 Ma domain for these conservative envelopes.
For B2, collection, wide-age, corrected region-stage and curated-tail constant bounds are respectively
428.001084, 428.092041, 432.375017 and 434.045668 Ma; the leave-one-region range remains
427.221481--430.452452 Ma. The keyed independent-uniform B2 flat shape diagnostic is now
0.055890--0.714743 (5th--95th percentile nominal *p*), replacing 0.073080--0.764863 from the former
single shared random stream. Its midpoint value (0.008481) and shared-quantile range
(3.124e-9--0.016468) are unchanged. This is a documented new Monte Carlo sample, not a data change.

## Evidence, model and assumptions

The scientific target is the one-sided older endpoint for the onset of a recoverable fossil
category under a fixed recording history, a fixed younger cutoff and independent locality-age
units. It is not a lineage origin. The observation process combines biological output and range,
diagnosability, delivery and preservation, and collection and reporting. The frontier varies their
unidentified product; it cannot identify any component separately.

The inventory rebuild now takes `data/macro/name_classifications.csv` as a committed adjudicated
input. It no longer reconstructs that table from ignored `work/codex/loop3/out_*.json` files.
`data/macro/body_membership.csv` is the explicit interface for material whose observation channel
does not itself imply body membership. The builder checks observation identity, source channel,
main-plus-inclusive age assignments, category nesting and disposition before admitting a row. It
also rejects unadjudicated E3--E5 events from non-body channels.

Age-allocation simulations use a SHA-256-derived random stream keyed by reading, category, cutoff and
allocation rule. Adding or reordering an unrelated inventory cell therefore cannot change B1/B2 draws.
The Oman-excluded B0 variant has its own key. This replaces the former single sequential stream; its
changed Monte Carlo quantiles are a deliberate reproducibility repair, not hidden backwards-compatibility
logic.

PBDB collection 278439 is Xiemisitai Bed 16, near Hoboksar. Liu et al. (2024), DOI
`10.1016/j.palaeo.2023.111903`, place the Xiemisitai Formation and plant locality in Hoboksar County,
West Junggar. The rebuild therefore groups it with the project's other West Junggar material under
`Kazakhstania`, not `Tarim`, and records that basis in the generated row. This changes a
region-stage dependence treatment, not the occurrence age or locality-age primary inventory. The
same collection is present in the raw all-taxa effort frame; the rebuild applies the identical
override there so leave-region-out fossil membership and exposure proxies remain aligned.

For a unit treatment with fixed cutoff `c`, oldest permitted fossil age `A`, guaranteed count `n`
and lower-tail probability `alpha=0.05`, the step contour uses

`extra exposure = (A-c) * (alpha^(-1/n) - 1)`

and, for a candidate lineage age `T` with assumed diagnostic delay `d`,

`earlier/later intensity = extra exposure / ((T-d)-A)`.

The break at `A` is data-selected and retrospective. If `T-d <= A`, the script reports
`candidate_not_older_than_envelope_anchor` rather than inventing a rate. This is outside the chosen
conservative-envelope contour parameterisation; it does not biologically exclude the combination,
because the fossil's true age may be younger within its support. Delays of 0, 5, 10 and 20 Myr are
assumptions, not estimated biological durations.

## Verification

- `uv run --script models/f3/loop3/build_reviewed.py` rebuilt 289 horizon-reading rows and a receipt
  binding the committed classification and body-membership inputs. K12 appears exactly twice, once
  per declared inventory, and never in B1/B2; Dr4 appears only in the adjudication table.
- `uv run --script models/f3/loop3/analysis.py` rebuilt the canonical reviewed outputs. The primary
  B0 result is Oman-inclusive; `variant=without_oman_fragments` preserves the exclusion comparison.
- The reviewer closed form is reproduced independently in a unit test: for `A=426.7`, `n=48`,
  `c=393.47` and candidate 431.2 Ma, extra exposure is 2.140005949 and the intensity multiplier is
  0.475556877; substituting it gives a conditional maximum CDF of 0.05.
- `frontier.csv` contains 168 cells: two readings, three unit treatments, seven candidate ages and
  four assumed delays. `influential_taxa.csv` contains 48 same-unit, same-cutoff comparisons.
- The full 47-test Loop 3 suite passes. Targeted coverage includes malformed source-channel admission,
  missing readings, category nesting, E4-only B1 exclusion, Katian age derivation, K12/Dr4 membership,
  Xiemisitai geography, old/new B0 reconstruction, per-cell random streams, the analytic frontier and
  its out-of-parameterisation delay status.

## Residual risks and recommendation

K12 broadens B0 across an acid-macerated palynological recovery channel. Treating its twelve
fragments as one unit avoids specimen pseudoreplication, but the recovery process remains unlike many
macrofossil collections. The Katian assignment comes from the later synthesis, whereas the 2003
primary report used broader Caradoc terminology. Neither issue justifies selective exclusion; both
remain conditions on the B0 interpretation.

The locality-age inventory still contains incompletely verified PBDB horizons and residual
within-region dependence. Region-stage and curated treatments are coarse sensitivities, not estimates
of an effective sample size. Diagnostic delay and early recording intensity are structurally traded
off in the frontier; the present positive-record data do not identify them jointly. The targeted
leave-outs expose leverage but do not propagate taxonomic model uncertainty across all 241 classified
names.

**Recommendation:** use the canonical B0 result with the former inventory immediately beside it;
present the B2 frontier as compatibility contours across unit and assumed-delay treatments; and retain
the influential-record table as a leverage diagnostic. Independent scientific review would still
materially improve confidence in the interpretation of the heterogeneous B0 recovery channel and the
mapping from fossil characters to B2, but it is unlikely to change the implemented arithmetic or the
K12/Dr4 membership decision without new source evidence.
