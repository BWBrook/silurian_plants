# Loop 3 review A: positive-record endpoint inference

Codex (OpenAI; independent methods specialist), 1 November 2026. Scope: `docs/plan-loop3.md`,
`docs/loop3-pilot.md`, `models/f3/loop3/macro.py`, the existing estimator, ramp and recovery code,
and the pilot horizon/output tables. I read the held primary texts of Marshall (1990, 1997) and
Strauss & Sadler (1989), re-derived the endpoint statistics, and ran numerical probes against the
pilot data. This review does not audit fossil identities or source ages.

## Verdict

The positive-record analysis is scientifically worthwhile, but the pilot numerical limits should
not enter the paper. Two implementation choices materially create them: collection totals per
stage are multiplied by lineage-time integrated over the stage, counting stage duration twice;
and medians of confidence bounds from uniformly imputed ages are described as 95% limits although
that pooling has no nominal coverage. The profiled logistic result is additionally dominated by
the allowed capacity/rate grid. These are repairable without returning to the complete-empty-rock
requirement.

Sprint B should use a new, small endpoint procedure and freeze the pilot as provenance. For each
recovery history fixed independently of the focal occurrence ages, transform calendar age to
cumulative recovery exposure and invert the exact maximum order statistic. A fixed younger cutoff
uses all n observations and is both simpler and more efficient than estimating both range ends.
Flat time and PBDB collection **density per Myr** are defensible conditional cases. Declining-past
histories and explicit recoverability delays are useful sensitivity cases. They remain assumptions,
not estimated preservation histories. Matched simulations should report both correct-history
coverage and failure under mismatch, clustering and delayed recoverability.

## Target and scope

The statistical endpoint is the start of the process that could generate the selected body-fossil
category under a stated recovery history. It is not automatically the lineage origin or crown node.
For B2, a crown-member fossil supplies a minimum for crown Tracheophyta, but extending its recovery
process backward constrains the crown origin only if crown members were recoverable according to
that history from the node onward. B1 constrains a polysporangiophyte body process; it is not a
direct crown-member record. B0 is a negative control against the older spore minimum, not a second
estimate of that minimum.

The occurrence unit must be an independent horizon. PBDB collection numbers, localities and beds
need not be independent horizons. Marshall (1990, printed pp. 3–4) explicitly warns that recording
the same fossil bed repeatedly in a composite section artificially narrows the interval. The final
analysis therefore needs horizon, locality and region-stage collapsed runs. The last two are
dependence sensitivities, not alternative taxonomic readings.

## Decisive defects in the pilot

### 1. Stage duration is counted twice

`tools/occurrences.py` apportions each PBDB collection across stages by its fraction of age overlap.
The resulting body effort is a collection-equivalent **total per stage**. `macro.effort_series()`
passes that total to `ramp.py`, whose expected count is recovery effort multiplied by the integral
of abundance over the stage in lineage-Myr. Thus a stage of duration d receives approximately
`collections × d`, rather than `collections`, exposure. For this use, the multiplier must be the
collection total divided by stage duration.

The distortion is large. The Emsian total is 154.92 collections across 17.15 Myr, or 9.03 per Myr;
the Pragian total is 74.61 across 2.40 Myr, or 31.09 per Myr. The pilot model treats 154.92 and
74.61 as per-Myr intensities and then integrates through those durations.

I refitted the 40 pilot age draws after only this unit correction. Median older profile limits (Ma)
changed as follows:

| Category | Pilot constant | Per-Myr constant | Pilot logistic | Per-Myr logistic |
|---|---:|---:|---:|---:|
| B0 | 434.54 | 431.96 | 452.57 | 436.78 |
| B1 | 434.69 | 432.04 | 454.06 | 438.73 |
| B2 | 427.73 | 425.60 | 437.97 | 427.94 |

These are diagnostic refits, not replacement results. They show that the paper-level conclusion
cannot be based on the pilot outputs.

### 2. The logistic history is not identified by this record

The pilot profiles over five capacities and a broad rate grid. With stage-total effort, the B0 and
B1 optima select the smallest capacity (K=10); B2 selects K=10 and the maximum rate (3.0). After
the duration correction, all three select the largest capacity (K=1000). Moving the effort units
therefore flips the selected capacity from one grid edge to the other. The B1 limit being older
than B0 is not itself a coding error: B1 is nested within B0 but the six additional, mostly younger
B0 horizons alter a separately profiled recovery shape, so no monotonicity theorem applies. The
anomaly is evidence of shape sensitivity, and the boundary selections show that the fitted shape
should not be a headline estimator.

The birth-death fit reinforces this diagnosis. Under stage-total effort its net-growth estimate is
the zero boundary and reproduces the constant fit; with per-Myr effort it moves to about 0.05–0.07
per Myr and closely follows the K=1000 logistic result. The data do not separate biological growth,
preservability and sampling effort.

### 3. Age imputation does not propagate age uncertainty into a 95% bound

For every draw, `macro.py` samples an exact age uniformly within each reported range. Uniformity
inside a stage is an unsupported geological prior. It then reports the median of 200 classical or
40 profile limits. A median of conditional 95% limits is not a 95% confidence limit for an
interval-censored record. The 5–95% spread in the output is a distribution of imputations, not
frequentist coverage or a probability interval for origin.

Three PBDB ranges cross the 393.47 Ma analysis edge. On 10,000 repetitions, the ramp input silently
uses a median of 105 rather than the stated 107 B0 horizons, 99 rather than 101 B1 horizons, and 82
rather than 84 B2 horizons because `stage_counts()` drops draws outside its edges. The table still
reports the undepleted totals. More basically, the B2 median classical limit (about 425.6 Ma) is
younger than the 426.7 Ma oldest possible age carried by its input, which is inappropriate as the
single reported older limit when that age uncertainty is unresolved.

For the known-cutoff endpoint statistic below, a conservative age envelope is simple: use the
maximum oldest age among units that could lie above the cutoff and n-min equal to the number whose
youngest admissible age is at least the cutoff. A partial-window unit can affect the maximum age but
does not increase n-min. Because the bound increases with the oldest age and decreases with n, this
envelopes every allocation allowed by the age ranges. Report the midpoint or random-within-stage
analysis only as a sensitivity. A full interval-censored likelihood is possible, but unnecessary
for the principal conditional comparison.

### 4. Effort is conditional and partly endogenous

Land plus marginal PBDB collections are a useful rock/collecting proxy, but the response's plant
collections are among those collections. The proxy also rises in the Devonian partly because the
plant record is rich there. Using it makes the calculation an absence argument through an aggregate
proxy, as the pilot notes. It should be called a conditional recovery history, not measured search
effort for plants. A non-plant-collection subtraction is informative as a sensitivity but is also
selected by the absence of a plant record; it does not make the design independent. Macrostrat
non-marine units offer a genuinely different proxy if their age and geographic support can be
matched.

PBDB effort is held only through the Darriwilian boundary in this layer. A transformed bound that
needs more cumulative exposure than the declared history contains must be reported as not bounded
within that declared domain. It says nothing about whether total lifetime exposure is finite.
Extrapolating the last density to 515.5 Ma is a separate assumed history, not an automatic software
fallback.

## Exact fixed-history endpoint method

Let c be a fixed younger cutoff and w(a)>0 a recovery density fixed without using the focal fossil
ages. Define cumulative exposure

\[
U(a)=\int_c^a w(s)\,ds.
\]

Conditional on n independent horizons and an origination/recoverability endpoint T, the transformed
ages are iid Uniform(0,U(T)). If M is the largest transformed observed age, then

\[
P\{M/U(T)\le x\mid n\}=x^n.
\]

Inverting the lower alpha tail gives the exact one-sided bound

\[
U(T_{1-\alpha})=M\alpha^{-1/n}.
\]

This conditions on n and assumes the category remains recoverable from T through c. It does not
require the absolute occurrence rate. If only the observed younger endpoint is usable, the primary
texts give the less efficient one-endpoint range formula

\[
U(T_{1-\alpha})=U(A_{young})+
 [U(A_{old})-U(A_{young})]\alpha^{-1/(n-1)}.
\]

For constant w this is exactly the Strauss-Sadler/Marshall expression. Marshall (1997, printed
pp. 166–169) generalises it by equating recovery-potential area in the extension to a multiple of
the observed-range area, requires the observed horizons to be consistent with the proposed
recovery curve, and says the curve must be determined independently of the observed finds. These
conditions rule out treating a step anchored at the observed oldest fossil as a nominal 95% bound.
Such a step can remain a clearly labelled sensitivity.

I implemented these results in `models/f3/loop3/endpoint.py`. Its piecewise-constant recovery
density is transformed and inverted analytically within bins. It distinguishes `bounded`,
`at_boundary`, `beyond_domain` and `undefined`; exceeding the declared exposure domain returns no
numerical bound, while equality is reported at the boundary. Nine
focused tests cover the two source formulas, vectorised transform/inversion, scale invariance,
finite-domain behaviour, input failures and 50,000-replicate coverage under both flat and nonuniform
declared recovery. All pass. The empirical coverages are constrained to 0.95 ± 0.004.

## Recovery histories and delay support

The final runner should predeclare a small set, all in per-Myr units:

1. flat calendar-time recovery;
2. global PBDB land+marginal collection density by stage (stage total divided by duration);
3. PBDB density multiplied by a fixed decline into the past, with timescales such as 25 and 10 Myr;
4. where a history ends before its calculated endpoint, `beyond_domain`, reported as “not bounded
   within the declared domain”, rather than as an infinite-origin result;
5. lineage-to-recoverable-form delays of 0, 5, 10 and 20 Myr, applied as biological support
   scenarios after estimating the recoverable-process endpoint; a fixed lag also shifts the
   lineage-age domain older by that lag.

The decline timescales and delay values are sensitivity axes, not fitted parameters. A delay moves
the lineage origin older than the estimated start of recoverability. The B0 spore comparison can
show that zero delay or a shared body-recovery history fails for a lineage known to exist earlier;
it cannot estimate a transferable tracheophyte delay. It is therefore a negative-control check on
assumptions, not calibration data for B2.

## Matched validation required for the paper

The exact conditional-n simulation is cheap on the Mac mini: draw n uniform cumulative exposures,
invert through each fixed history and check the bound. It should be supplemented by simulations of
the complete reporting procedure:

- correctly specified flat and each fixed nonuniform history at the observed B0/B1/B2 n;
- true decline faster and slower than declared;
- stage censoring followed by the exact conservative age-envelope rule;
- duplicated horizons and clustered locality/region-stage occurrences, comparing every collapse
  level;
- delays between lineage origin and recoverability, reporting coverage for the recoverable endpoint
  and failure for the lineage origin until the delay is added;
- finite history support, where `beyond_domain` is a valid outcome rather than a failure.

Coverage must describe the entire predeclared procedure, including age handling and unit collapse.
Report claim frequency and coverage among claims when a procedure can be undefined or beyond its
declared domain.
Do not reuse Loop 1's recovery grid as validation: it simulates a different estimator and inherits
the stage-total/per-Myr mismatch.

The implemented validation uses the reviewed locality × age-range proxy counts (B0=75, B1=70,
B2=48), 3,000 replicates per cell and 144 cells. Across the 54 exact-age, correctly specified
history cells, coverage including beyond-domain no-claims was 0.941–0.958; 51 of 54 Wilson
intervals contained 0.95, as expected with many simultaneous Monte Carlo checks. The conservative
stage-age envelope covered 0.947–1.000. These are method checks conditional on n, not calibration of
the empirical fossil record.

The stress tests show why the limits must retain their qualifiers. Treating pairs or quartets of
duplicate horizons as independent reduced coverage to 0.775–0.783 and 0.522–0.534 respectively.
Fitting flat recovery when true recovery declined with a 10 Myr timescale gave only 0.034–0.241
coverage, worsening for older origins. The reverse mismatch made no bounded claims in these cells,
rather than providing evidence for an old origin. A 10 or 20 Myr recoverability delay gave zero
coverage for lineage origin when ignored and 0.947–0.957 when the known delay was added.

Finite-domain selection also matters. In matched declining-history cells at 458.2 Ma, as few as
4.5% of simulations gave a bound inside the domain; conditional coverage among those bounded
claims was as low as 0.015 even while unconditional coverage remained near 0.95. The output
therefore reports claim frequency and conditional-on-bounded coverage beside unconditional
coverage. `models/f3/loop3/out/simulation_results.csv` and `simulation_receipt.json` bind the full
results and inputs.

## Recommendation

Adopt Loop 3 with the endpoint method above. Preserve `macro.py`, its outputs and `ramp.py` as the
pilot and audit trail. The final paper can report substantive conditional estimates even when broad
or beyond the declared domain, provided every result names the recovery history, age envelope,
unit collapse and node/recoverability interpretation. Do not describe a clock interval as excluded
merely because it is older than a bound under a history already rejected by the B0 negative control.
Instead report
which histories make each clock age compatible and what lineage-to-body delay each requires.

The separate source-identity review is material and its adjudications must remain bound to these
results. Further independent statistical review would be useful after paper integration, because
the decisive risk has moved from the endpoint algebra to unit construction, age-envelope use,
recovery-history adequacy and the wording of clock compatibility.

## Scoped review: retrospective stage-suppression grid

I independently reviewed `suppression_sensitivity.py`, its three focused tests, the 144-row output
and its receipt after the main analysis exposed strong lack of fit in the globally declining
histories. The grid is complete and non-selective within its declared retrospective family: two
readings × three categories × two baselines × three stage breaks × four multipliers, with 144
unique cells. A multiplier of one reproduces each baseline at every break. All 26 focused Loop 3
methods tests pass.

The pivotal B2 flat-history values rederive directly. With c=393.47 Ma, oldest possible age
M=426.7 Ma and n=48, multiplying recovery older than M by 0.1 gives

\[
M + (M-c)\{0.05^{-1/48}-1\}/0.1 = 448.1000595\ \text{Ma}.
\]

The 0.01 case requires more exposure than the history contains and is correctly reported
`beyond_domain`. A 432.9 Ma break is a genuine null control for this B2 result: the flat and PBDB
bounds are reached before the break, so all four multipliers leave them unchanged. The output also
correctly preserves the baseline shape statistic whenever the modified segment lies wholly older
than the admissible B2 ages.

This grid changes the interpretation, not the endpoint algebra. The global 10 Myr decline changes
recovery throughout the observed B2 range and has severe conditional-maximum lack of fit under
both declared age-allocation schemes. In contrast, suppression beginning at or older than the
oldest possible B2 record is not identified by the B2 positive record. An unchanged shape statistic
does not support that older tail; it demonstrates that the record cannot test it. Histories whose
break intersects fossil-age support are partly testable, but the grid's midpoint KS p value remains
a nominal diagnostic. It must not be used alone to rank histories because the full shape analysis
shows material age-allocation dependence.

The stage breaks and multipliers were defined after seeing the pilot, and the 426.7 Ma break is
effectively anchored to the oldest possible B2 age. The resulting numbers are therefore
retrospective compatibility sensitivities, not nominal, simultaneous or selection-adjusted 95%
limits. The complete grid may be reported in the supplement, while the paper should state the
scientific result in the main text: recovery shape within the observed range is falsifiable, but
pre-first-occurrence recovery can remain unidentified. No member of the grid validates a molecular
clock posterior, and no favourable member should be selected as the preferred history.

The final field name `modified_segment_overlaps_age_support` states its actual rule: at least one
unit's admissible age interval extends beyond the break (`max_ma > break_ma`), not that an exact
fossil age was observed there. The final receipt binds the exact functional data, timescale, code,
output and `data/macro/build_receipt.json`, making the source-transformation provenance chain
explicit. These final changes do not alter the numerical verdict.

## Scoped review: design and results claim alignment

I checked `loop3-design.md` and `loop3-results.md` against the current reviewed bounds, age and unit
sensitivities, shape diagnostics, delay table, simulation grid, spore first-appearance table and
published clock intervals carried in the primer. The primary counts and bounds, unit and geographic
contrasts, 458.2 Ma strict certain cryptospore minimum, Hooper and Harris intervals, 431.2 Ma soft
maximum, delay values and simulation ranges all reproduce. The documents correctly distinguish the
primary fixed-history conditional 95% bounds from the retrospective suppression calculations, and
they do not convert either into validation of a clock posterior.

Three wording constraints remain material for paper integration. First, a fixed biological delay
does not move the recoverability-process bound; it maps that bound to a lineage bound and shifts the
lineage-age domain by the same amount. Thus 428.84 Ma remains the flat B2 recoverability bound, while
448.84 Ma is the lineage bound under an assumed 20 Myr delay. Second, the retrospective 448.10 Ma
calculation is not an admission or exclusion threshold: it is where the 0.05 endpoint calculation
lands under one post-pilot fixed scenario. Third, the 10 Myr decline is not the only B2 history with
poor within-record adequacy. Under independent age allocations, the nominal p-value 5–95% ranges
are 6.96×10^-5–0.0161 for the 25 Myr decline and 1.85×10^-4–0.0158 for plant-excluded PBDB, versus
0.0144–0.265 for PBDB-all and 0.0731–0.765 for flat recovery. These are not combined tests or a basis
for selecting a best history, but the bounded 431.63 Ma decline-25 result should not be presented as
equally adequate by omission.

The display distinction is adequate only if captions carry the same status. The first four plotted
rows are fixed-history conditional envelope results; daggered suppression points are retrospective
endpoint-rule sensitivities without nominal or selection-adjusted 95% coverage. A break at 432.9 Ma
is a null control because the B2 target exposure is reached at 428.84 Ma without entering the
older-than-432.9 segment. This direction should be stated in age language rather than the ambiguous
word “before”.
