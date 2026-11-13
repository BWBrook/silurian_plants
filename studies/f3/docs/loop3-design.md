# Loop 3 sprint B: declared positive-record analysis

Codex, 1 November 2026, adopting Barry's Loop 3 brief and revising Claude's pilot after independent
source and methods reviews. This specification describes the implemented analysis, including the
source corrections made during review. It is not a preregistration before seeing the pilot.

## Biological target and observation unit

The target is the older endpoint of the process generating the selected positive body records.
Categories retain B0 (accepted embryophyte bodies), B1 (polysporangiophyte bodies) and B2 (crown
tracheophyte members). Source readings are main and inclusive. A category's recoverability
endpoint constrains lineage origin only under the stated biological mapping and recovery history.
An origin can precede recognisable/preservable bodies.

The inventory retains source observation and PBDB collection IDs. The primary counting unit is a
locality–age proxy: PBDB formation plus coordinates rounded to 0.1 degree and identical numerical
age support; curated named sites plus identical age support. This is a conservative aggregation,
not a claim that the proxy is a source-verified bed. Missing geographical keys retain the collection
ID rather than silently dropping or merging records. For a collapsed unit, the oldest-member age
has support from the maximum of member lower ages to the maximum of member upper ages.

Only explicit collection/occurrence identifiers justify replacing a PBDB record with its curated
interpretation. Country, taxon and overlapping ages do not establish material identity. Regional
checklists and unresolved duplicates are withheld from the primary unit count and retained in a
separate sensitivity. Source decisions and the limits of the stratified audit are recorded in
`studies/f3/data/macro/source_adjudications.csv`; this is not certification of all 241 name assignments.
Names classified as implausible in the interval cannot enter through a yes in a B1/B2 column.

PBDB ranges wider than 20 Myr remain in the inventory and enter a wide-age sensitivity when their
whole upper age lies within the inference domain. A wholly younger curated record is excluded;
records straddling a younger cutoff can set the oldest possible age but not the guaranteed count.
The source ages are retained, not silently replaced by their in-window part.

The pilot's 241-name roster covers records overlapping 445.2–393.47 Ma. To audit the older part
of the inference domain, retain a separate screen of all 556 older-only non-spore PBDB rows
(69 names). Source review resolves the seven plausible/unplaced candidates, representing 17
occurrences, as non-embryophytes or the already-rejected *Boiophyton*. Other rows retain their
database algal/acritarch categories with source-audit status explicit. This inventory establishes
what was screened; it is neither a global completeness proof nor a searched-rock denominator.

## Fixed-history endpoint calculation

For a fixed younger cutoff c, cumulative recovery is U(a)=integral from c to a of w(s) ds.
Conditional on n independent units drawn with density proportional to the declared w on [c,T],
the exact one-sided 95% older bound satisfies U(T_upper)=U(A_oldest) × 0.05^(-1/n).
The absolute recovery rate cancels. `endpoint.py` also implements the classical observed-range
formula with n−1, used as a midpoint-age comparison to the pilot; it is not the primary result.
Derivations and primary-source reading are in the methods audit.

The primary age treatment uses the greatest possible oldest age and the smallest number of units
guaranteed older than c. Monotonicity makes this an envelope of the exact-age bounds when all source
age intervals contain their actual ages. This geological support condition is separate from
statistical coverage. No probability distribution is assigned to the source age ranges.

Cutoffs are the ends of the Emsian (393.47), Pragian (410.62), Lochkovian (413.02) and Pridoli
(419.62 Ma), from the project timescale. The inference domain ends at 469.4 Ma, where the held PBDB
effort history ends. A bound beyond available cumulative exposure is reported as **not bounded
within the declared domain**, not as an infinite-age inference. No proxy is extrapolated to the
Cambrian. A boundary equality is reported separately.

Six fixed recovery histories are evaluated without fitting them to the focal fossils:

1. Constant recovery in calendar time.
2. PBDB all-taxa land+marginal collection density per Myr, apportioned by source age overlap.
3. The same proxy after removing collection IDs in the held plant-filtered PBDB extract.
4. Recovery declining into the past on a 25 Myr exponential timescale.
5. Recovery declining into the past on a 10 Myr exponential timescale.
6. Plant-excluded PBDB density multiplied by the 10 Myr decline.

The exponential histories are declared piecewise constant at 0.05 Myr resolution, retaining every
stage boundary. Their normalisation is immaterial. Plant-exclusion is a response-related filter,
not verified independent or non-plant-only effort. The proxy cannot establish actual fossil-search
opportunities. Conditional-on-maximum KS diagnostics check within-range shape at midpoint and
imputed ages; nominal exact-age p values and their imputation spread do not constitute a combined
test for interval-dated records, model selection or empirical calibration.

**Retrospective extrapolation grid.** After seeing that steep smooth declines fit the observed
age distribution poorly, evaluate every combination of flat/PBDB-all baseline, stage breaks
419.62/426.7/432.9 Ma and older-recovery multipliers 1/0.5/0.1/0.01, for all three categories and
both readings (144 cells). Do not select a member to match a clock. The 426.7 Ma break coincides
with the oldest possible main B2 record, so this is explicitly a retrospective sensitivity:
the 0.05 endpoint rule does not supply nominal, simultaneous or selection-adjusted confidence
for the reported grid. Each row states whether the changed segment overlaps fossil age support.
The grid separates recovery shapes that the observed sequence can test from extrapolation into
an interval lacking accepted body occurrences; an inherited shape statistic cannot validate that
unobserved extrapolation. A 432.9 Ma break is a null control when the bound lies younger than it.

## Sensitivity and simulation

- Recount as individual collections/observations, whole localities, and region–stage cells.
  The last is assigned by midpoint stage and is a deliberately coarse dependence diagnostic.
- Restore wide-age and unresolved-material records separately; omit low-confidence names and a
  weak botanical-source collection; compare the curated tail alone; collapse the named uncertain
  Kosov/Podolia links. These variants test density and identity choices, not new preferred readings.
- Leave each represented palaeogeographic unit out in turn. Regions follow the existing approximate
  country/state assignment for PBDB and curated source assignments for the tail. Recompute the
  PBDB exposure after the same omission. Do not interpret this as a reconstructed palaeogeography.
- Allocate ages 256 times independently and by a shared quantile across all ranges (root seed
  20261102). Their quantiles are descriptive sensitivity summaries, never confidence bounds.
- Apply explicit lineage-to-recoverability delays of 0, 5, 10 and 20 Myr. These are assumptions,
  not estimates from the B0–spore discrepancy; shifting the endpoint also shifts its domain.
- Simulate 3,000 replicates per cell (root seed 20261101) at the reviewed primary counts and
  recoverability endpoints 432, 445 and 458.2 Ma. Check each correctly specified history with exact
  and stage-censored dates; mismatch constant and steeply declining histories; repeat underlying
  units two or four times; and impose 10/20 Myr delays with and without the correct adjustment.
  Report unconditional coverage including no-bound outcomes, bounded-claim frequency, coverage
  among bounded claims and Monte Carlo Wilson intervals. These verify the declared procedures
  and expose their failure modes; they do not qualify the actual fossil record.

All source, code and output bindings are recorded separately for assembly, estimation, simulation
and figures. The Loop 1/F3 engine, qualification receipts, R pilot and Loop 2 package are frozen.
No new R, remote compute, external correspondence or public release is part of sprint B.
