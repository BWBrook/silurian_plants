# Loop 3 review A and sprint B: what positive body records can establish

Codex, 1 November 2026. Reviewed Claude's Loop 2 endorsement and Loop 3 proposal/pilot (Board
2802 and 2809; `ddb7552`, `b2d57e1`), adopted the revised design under Barry's authority, and
implemented the macrofossil tranche. **Review A and sprint B are complete; Loop 3 is not closed.**
Claude owns the substantial main-text/supplement reconstruction next, followed by Codex's review.
No new measurements, outside assistance or correspondence are assumed.

## The scientific result

Positive occurrences support a substantive conditional analysis. They do not require the
searched-empty-rock denominator used by the previous absence-rate analysis. The necessary
assumption is instead how the recoverable-record process behaved before and during the observed
sequence. The assembled record can challenge some histories within its observed range, but it
cannot identify recovery in an earlier interval with no accepted body occurrence.

This distinction is sharper than saying that a sufficiently flexible model gives a wide interval.
A steep exponential decline into the past removes the older bound, but it also fits the observed
age sequence poorly. An abrupt suppression entirely before the oldest admissible crown-member
record changes the extrapolation without changing the conditional distribution of the recorded
finds. The latter is an identified limit of the evidence, not support for a particular suppression.

The body analysis therefore adds quantitative conditions on early vascular-plant histories. It
does not independently validate the young clock, refute the older clocks, or turn a recoverability
endpoint into a crown date. The biological mapping and fixed-delay scenarios are explicit.

## Corrected record and primary estimates

The main reading contains 77 B0, 72 B1 and 50 B2 possible locality–age units; respectively 75, 70
and 48 are guaranteed older than the 393.47 Ma cutoff. Units with ranges crossing the cutoff are
not silently counted as certain. B0 comprises accepted embryophyte bodies, B1 polysporangiophyte
bodies and B2 crown-tracheophyte members. These are source-linked proxies for independent horizons,
not a fully verified bed inventory. `primary_unit_membership.csv` gives every constituent record.

Conservative age-envelope older bounds (Ma), conditional on each fixed history and independent
units, using the exact one-sided 95% endpoint rule:

| Recovery history | B0 | B1 | B2 |
|---|---:|---:|---:|
| Constant | 434.51 | 434.62 | 428.84 |
| PBDB land+marginal collection density per Myr | 436.38 | 436.63 | 428.88 |
| PBDB density with plant-filter matches removed | 435.73 | 435.94 | 428.45 |
| Decline into the past, 25 Myr timescale | 437.16 | 437.50 | 431.63 |
| Decline into the past, 10 Myr timescale | Beyond domain | Beyond domain | Beyond domain |
| Plant-excluded PBDB × 10 Myr decline | Beyond domain | Beyond domain | Beyond domain |

“Beyond domain” means no older bound through 469.4 Ma, the limit of the declared recovery history.
It is not an infinite-age estimate. The age-envelope guarantee assumes that the reported age
supports contain the actual fossil ages; it does not make geological assignments certain.
Uniform and shared-quantile age allocations are reported separately as sensitivities.

The accepted strict cryptospore minimum is 458.2 Ma in the existing first-appearance table. The
434–437 Ma B0 limits are much younger. This is a check against treating the body-recovery endpoint
as the origin of the broader embryophyte lineage under those histories. It is not a known true
origination date, an empirical coverage experiment, or a measured lag to apply to B2.

## What changes the result

**Sampling units and density.** For B2 under constant recovery, counting collections separately
gives 428.00 Ma; locality–age proxies give 428.84; whole-locality collapse 428.89; region–stage
collapse 432.07; and the curated tail alone 434.05. The last two reflect strongly reduced
effective density, not newly discovered earlier fossils. Restoring wide-age records gives 428.09;
restoring uncertain material rows gives 428.60. These are declared sensitivity contrasts, not
alternative empirically calibrated sampling designs.

**Geography.** Leaving each represented region out gives B2 constant-history limits of
427.22–430.45 Ma. The youngest is without the Australian–Antarctic records; the oldest is without
Laurentia. The corresponding PBDB histories are recalculated with the same region removed.
Regional assignments remain approximate where they derive from modern country/state.

**Within-record recovery shape.** Conditional-on-maximum KS diagnostics expose lack of fit for
some declared histories. For B2, the independent-uniform age allocations give nominal p-value
5–95% ranges of about 0.073–0.765 for constant recovery, but about 2×10^-11–8×10^-7 for a
10 Myr smooth decline. These are sensitivity summaries of exact-age diagnostics, not combined
tests for interval-dated fossils. The 25 Myr decline and plant-excluded PBDB history also show
poor adequacy under these allocations: their respective nominal p-value ranges are
6.96×10^-5–0.0161 and 1.85×10^-4–0.0158, compared with 0.0144–0.265 for PBDB-all.
These diagnostics do not select a best model, establish independent PBDB effort or correct an
endpoint for model selection. Neither the bounded 25 Myr decline nor the unbounded steeper
decline should be presented as equally supported by the observed sequence.

**Recovery outside observed support.** The complete retrospective stage-break grid uses flat and
PBDB baselines, breaks at 419.62/426.7/432.9 Ma, and older multipliers 1/0.5/0.1/0.01, for both
readings and all categories. For main B2, reducing flat recovery to 0.1 before 426.7 Ma moves the
endpoint-rule result from **428.84 to 448.10 Ma**; 0.01 gives no bound within 469.4 Ma. No main
B2 record has age support older than 426.7 Ma, so these changes leave the within-record shape
statistic unchanged. The 432.9 Ma break has no effect because the bound lies younger than it.

The 426.7 Ma break is effectively anchored to the reviewed oldest possible B2 record. The grid is
therefore a retrospective sensitivity, not nominal, simultaneous or selection-adjusted 95%
inference. The 448.10 Ma value is where the endpoint rule lands under that retrospective scenario,
not an admission or exclusion threshold for the Harris 447–452 Ma interval. No fitted recovery multiplier or preferred
clock follows. This grid makes the pre-first-occurrence recovery assumption quantitatively usable.

**Biological delay.** Fixed delays of 0/5/10/20 Myr map the recoverability bound to a lineage bound
and shift the lineage-age domain by the same amount. A delay is an assumed mapping, not inferred
from this record or transferred from spores. For example, a 20 Myr delay maps the unchanged
428.84 Ma constant-history B2 recoverability bound to a 448.84 Ma lineage bound. The data do not
identify that delay or equate body morphology with the crown divergence.

## Why the pilot numbers were replaced

The independent source and methods audits found material defects, now repaired:

- The pilot passed stage collection totals to a likelihood expecting per-Myr density, multiplying
  by stage duration twice. A diagnostic unit correction alone moved its B0 logistic limit from
  452.57 to 436.78 Ma and B2 from 437.97 to 427.94; the selected capacity flipped between grid
  boundaries. Those refits diagnose the problem and are not the replacement inference.
- Medians of imputed-age confidence limits were presented as 95% limits. The new primary uses a
  conservative age envelope; imputation quantiles are labelled as sensitivities.
- Country, genus and age overlap falsely replaced distinct PBDB localities. Only explicit
  identifiers now justify replacement. The original 21 replacements included seven explicit
  links; the revised parser finds 11 eligible collection replacements across the expanded source
  crosswalk. These are different scopes, not contradictory counts.
- Collection numbers were treated as independent beds. Repeated locality–age groups are now
  collapsed, with alternative units retained; uncertain regional lists no longer add primary units.
- Names classified as implausible in the window could still enter B1/B2 through an OR condition.
  The accepted-category gate now applies to every category. An out-of-window curated row and
  partially in-window ages are handled explicitly. A missing-country key no longer drops a unit.
- The source identifiers called `wang2026` in two namespaces refer to different papers. A new
  identity crosswalk distinguishes them without silently changing frozen provenance tables.

The older-only PBDB screen contains 556 non-spore rows and 69 names. Source review of the seven
plausible/unplaced names (17 occurrences) found cyanobacteria, algae/trace fossils and the rejected
*Boiophyton*, not an additional embryophyte body. Other older names retain explicit database-level
screen status. These exclusions are not fossil non-detections and the inventory is not a search
denominator. The exact historical *Alectorurus venosus* specimen remains unreassessed, without
positive embryophyte evidence in the routes examined.

## Verification and limitations

All 26 focused endpoint, simulation, source/unit and suppression regression tests pass. The exact
endpoint formula reproduces the primary-source classical formula under constant recovery and
known analytical exposure transforms. A separate methods reviewer checked the conservative age
envelope, final unit selection and the suppression grid, including its null control and direct
448.1000595 Ma calculation. Source review is stratified and explicit about records still known
only through database fields or abstracts; it does not certify every younger occurrence.

There are 144 matched/stress simulation cells, each with 3,000 replicates at the reviewed record
counts. Correctly specified exact-age coverage ranges approximately 0.941–0.958; stage envelopes
are conservative. Treating duplicated pairs/quartets as independent gives coverage about
0.78/0.53. Fitting constant recovery to a true 10 Myr decline gives 0.034–0.241. Ignored 10/20 Myr
lineage-to-body delays can give zero lineage coverage; adding the known simulated delay restores
nominal behaviour. Claim frequency and coverage among bounded claims are reported separately:
95% unconditional coverage does not imply 95% coverage after selecting the bounded outcomes.
These are checks of explicit procedures and failures, not empirical qualification of the fossils.

Assembly, analysis, simulation, retrospective grid and figures have separate input/output hash
receipts. The final verification receipt records their current bindings and confirms that the
pre-existing F3 studies/f3/models/qualification data, occurrence inputs and R pilot remain unchanged.
No R or remote computation was needed. Public release and external correspondence remain Barry's.

The required repository-wide DOI checker queried 736 distinct DOIs and flagged 26 references,
all in four unchanged historical action/request documents. Those pre-existing citation/parser
flags are outside this tranche and were not silently repaired. New older-candidate DOI identities
were checked separately against Crossref in the source audit. No card or card-generated table
was edited.

## Handoff for the reconstructed paper

Claude should now write the main text around the biological problem: why clocks disagree, what
different fossil channels can establish, and why recognisable bodies can lag lineage origin.
The main results are the qualified regional spore comparison, the body-record conditional
estimates, and the separation of testable within-record recovery from unobserved earlier recovery.
The biological pilot links specimens and traits to node claims; it is not an automatic numerical
correction to these bounds.

Move estimator derivations, F3 qualification machinery, source adjudications, age/unit/geographic
grids, QSIM and execution history to the supplement and repository. Remove internal codes from the
main narrative. Do not carry forward the pilot's 452.6/454.1/438.0 logistic figures, the statement
that bodies “favour the young clock”, a measured 15–25 Myr preservation lag, or outside-author
requests as future work.

Figure files are `studies/f3/models/loop3/out/fig_macro_recovery.pdf`, `fig_macro_sensitivity.pdf` and
`fig_macro_suppression.pdf`, with PNG previews. The main figure's first four rows are conditional
envelope results; its purple triangles are explicitly retrospective suppression sensitivities.
The green bands are the Hooper/Harris published crown-age intervals reproduced in the source
primer, not independent validation targets; the dashed 431.2 Ma line is the proposed soft maximum.
The other figures and complete tables are available for the supplement. Captions should state
that geological support, unit independence and recovery history remain assumptions.
