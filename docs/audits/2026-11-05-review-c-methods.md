# Review C: statistical claims and Borenshult calibration logic

Codex specialist delegate (configured GPT-5.6-sol/high), 5 November 2026. Read-only audit of manuscript C at
`9f694aa`, checked against the frozen Loop 2/3 tables. I did not rerun qualification,
change frozen files, or use private correspondence or `library/closed/`. For Borenshult I
inspected the public open-access Rubinstein & Vajda (2019) PDF and the public Hooper et al.
(2026) supplementary PDF.

## Required repairs

### R1. C24 overstates the identified product

`manuscript/text/main.md:145-146`, `for-agents.md:47-49`, and `claims.csv:25` say that
`rho*f` stays near 0.09 across the delivery scenarios. That is true only for the
constant-intensity H0c row:

| rho | H0c limit | rho x H0c | exposure-weighted H0 limit | rho x H0 |
|---:|---:|---:|---:|---:|
| 1 | 0.0910 | 0.0910 | 0.1835 | 0.1835 |
| 0.5 | 0.1821 | 0.0911 | 0.2576 | 0.1288 |
| 0.25 | 0.3641 | 0.0910 | 0.4211 | 0.1053 |
| 0.1 | 0.9103 | 0.0910 | 0.9207 | 0.0921 |

These are direct calculations from primary rows 56-59 of
`models/f3/out/m2_results.csv`. The exposure-weighted product spans 0.092-0.184, a
twofold range. Repair C24 by restricting `rho*f approximately 0.09` to H0c. Describe the H0
row separately and retain the broader identification claim that delivery and production are
not separately identified.

### R2. C28 is a conditional separation, not an observed body lag, and B0 omits Oman

The arithmetic is correct: `458.2 - {437.16, 436.38, 435.73, 434.51}` gives
21.04-23.69 Myr. The interpretation is not. C28 compares a strict cryptospore minimum
with one-sided 95% older bounds on a model-defined B0 recoverability endpoint. It does not
observe either lineage origin or the endpoint. Under each fixed recovery history it supplies
a conditional lower bound on their separation, not a measured 21-24 Myr lag.

More importantly, the advertised B0 target is “any embryophyte body” (`docs/plan-loop3.md:80-88`),
but the selected B0 inventory omits the Katian Oman material. The public primary report calls
these “spore-containing plant fragments”, identifies sporangia, and treats them as direct
evidence of bona fide land plants. The repository independently records spore masses with
sporangial covering (`data/occurrences/observations.csv:199`; `interpretations.csv:305`) but
keeps them in E2 and explicitly does not pass them to the body analysis. Exclusion from E3/E4
is correct because no branched axes or tracheids occur; exclusion from B0 is not justified by
the current B0 definition. Including a Katian body occurrence would invalidate the statement
that the oldest B0 body is Sheinwoodian and materially shorten the claimed separation.

Until B0 is redefined and defended or the Oman fragments enter a sensitivity analysis, C28
supports only the arithmetic separation between the selected B0 endpoint and 458.2 Ma. Remove
“demonstrably”, “observed feature”, “we know”, and “the record shows” from
`main.md:20-21,182-189,246-249,274-275,305-306`, `brief.md:34`, and
`for-agents.md:54-56`. The claims-ledger row should name the selected-body definition and
state that the quantity is a conditional lower separation bound, not a body-lag observation.

### R3. Shape diagnostics do not robustly validate constant recovery

`main.md:213-217` and C31 report only independent-uniform age allocations: constant
recovery has nominal p 5th-95th percentiles of 0.073-0.765 while decline10 has about
2e-11 to 8e-7 over the same percentiles. The frozen
`shape_diagnostics.csv` also contains results that reverse the reassuring part of this contrast:

- midpoint ages: constant p = 0.00848 and PBDB-all p = 0.00918;
- shared-quantile allocations: constant p 5th-95th percentiles = 3.1e-9 to 0.0165 and
  PBDB-all p 5th-95th percentiles = 2.7e-5 to 0.0577;
- decline10 is poor under every treatment checked.

Thus the robust discrimination is against decline10, not in favour of constant recovery. The
manuscript may retain C31 as explicitly limited to independent-uniform draws, but it must report
that constant recovery also fails at midpoint and under shared-quantile allocation. This matters
because no probability law was assigned to ages within source ranges; independent-uniform draws
cannot silently become the preferred adequacy test. Table S7 should expose midpoint p and the
shared-quantile results already frozen, or the text should state them directly.

### R4. C32 and C33 are illustrative mappings, not empirically required magnitudes

The reported arithmetic checks:

- flat recovery x0.1 before 426.7 Ma maps B2 from 428.8400 to 448.1001 Ma;
- 447 - 428.84 = 18.16 Myr and 20 Myr maps 428.84 to 448.84 Ma;
- 444-452 Ma corresponds to differences of about 15.2-23.2 Myr.

But `main.md:218-226,256-260` and `brief.md:33,38` risk making “tenfold” and
“15-23 Myr” sound like requirements estimated by the fossils. C32 is a post hoc grid member
whose break is anchored to the oldest possible record; it is neither a fitted suppression nor a
threshold. C33 adds an assumed delay to a one-sided endpoint bound. The differences are minimum
delays needed to reach the named clock ages at that 95% boundary under flat recovery, not delay
estimates. Use “one illustrative sufficient scenario” for tenfold suppression and “at least about
15-23 Myr at the endpoint bound” for the delay arithmetic. Do not say either magnitude is required
without profiling a declared recovery/delay model.

### R5. The Borenshult addendum conflates three mappings

The Figure 3 reading itself is sound. Visual inspection of the public PDF confirms separate
definite/possible symbols, a possible occurrence near 48.2 m, definite occurrences beginning near
43.1 m, and that both lie in the Sandbian below the Kinnekulle K-bentonite. Hooper Supplementary
Table 4 explicitly derives 459.1 Ma as the GTS2012 Sandbian base 458.4 Ma plus 0.7 Myr. Therefore,
if Hooper's stage-base rule is retained, swapping the named 48.2 m occurrence for a definite 43.1 m
occurrence does not change the published 459.1 Ma maximum (458.9 Ma on the repository timescale).

The final paragraph of `docs/audits/2026-11-04-borenshult-figure3-reading.md:119-125`
goes too far in saying that the reading moves “the minimum, not the maximum”. Figure confidence,
stage-base dating and fossil-to-node mapping are separate:

1. Under Hooper's ancestral-character/stem-evolution mapping, a trilete first appearance is used as
   a maximum on crown Embryophyta; the stage-base value is unchanged.
2. A Borenshult trilete supplies a minimum on crown Embryophyta only under an additional mapping that
   makes its producer a crown member or a descendant total group. A trilete mark alone does not do
   that under Hooper's own maximum argument.
3. If that alternative minimum mapping is adopted, the overlying 454.41 +/- 0.17 Ma bentonite gives
   a conservative minimum of about 454.24 Ma by Hooper's “young uncertainty edge” convention, not an
   unqualified 454.4 Ma node minimum.

Repair the addendum to call the minimum consequence a conditional alternative calibration, not a
consequence of accepting the Figure 3 symbols alone.

## Verified claims

- C25/C26: 77/72/50 possible and 75/70/48 Emsian-guaranteed B0/B1/B2 units; 16 B2 units
  with older-than-Pridoli support span eight recorded regions.
- C27/C39: the main B2 and B1 endpoint values in the ledger and Tables 2/S3 match
  `reviewed_bounds.csv` at the stated precision.
- C29/C30: the inclusive constant B0 value 447.20 Ma and the B2 unit/geographic
  sensitivities match the frozen table.
- C34: across 54 matched exact-age cells, unconditional coverage is 0.941-0.9583;
  duplicate-pair and duplicate-quartet coverage is 0.775-0.783 and 0.522-0.534; fitting flat
  recovery to true decline10 gives 0.034-0.241. Unadjusted 10/20 Myr lineage delays give zero
  lineage-age coverage; correct adjustment restores about 0.947-0.957. These are procedure checks,
  not qualification of the fossil record.

## Optional precision improvements

- Replace “48 dated crown-member localities” (`main.md:17`) and “77 localities”
  (`brief.md:27`) with locality-age proxy units. The brief also mixes 77 possible B0 with 48
  guaranteed B2; use either possible counts (77/50) or guaranteed counts (75/48) consistently.
- In `main.md:173`, replace “n independent units after a younger cutoff c” with “n units older
  than the younger cutoff c (c < a <= T)”; “after” is ambiguous on a Ma scale.
- “Robust to most data choices” (`main.md:207`) is too broad for a conditional sensitivity set:
  region-stage collapse moves B2 to 432.07 Ma and the curated tail to 434.05 Ma, while unmodelled
  residual dependence can be worse. State the observed range of declared sensitivities instead.

## Recommendation and residual risk

R1-R5 are required before scientific sign-off. The frozen arithmetic is mostly accurate; the
material defects arise when conditional endpoint calculations are promoted to observed biological
lags or preferred recovery histories. The Oman/B0 boundary is the only issue that may require a new
declared sensitivity rather than prose repair. The highest-value next work is source-only:
adjudicate the Oman body definition and the Borenshult fossil-to-node mapping against the published
record already accessible to the project. Neither adjudication would change the statistical
dispositions above.

Public sources used: Rubinstein & Vajda (2019),
<https://www.diva-portal.org/smash/get/diva2%3A1372936/FULLTEXT01.pdf>; Hooper et al. (2026)
Supplementary Table 4,
<https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41477-026-02432-3/MediaObjects/41477_2026_2432_MOESM1_ESM.pdf>;
Wellman, Osterloff & Mohiuddin (2003), <https://eprints.whiterose.ac.uk/106/>.
