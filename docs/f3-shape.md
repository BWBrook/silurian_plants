# The shape of F3 (v2)

**Status: proposal, v2, 2026-10-28.** Drafted by Claude Opus 5.5; awaiting Codex's critique (Correspondence `silurian-plants`, discussion 99), then Barry's decision. Nothing here has been applied to real data.

**Revision history.**
- v1 (`f01d4bd`) followed Barry's adoption of the second amendment (chat, 2026-10-28: "Yes, agreed, adopt it. Then let's re-assess the full shape of F3 given this constraint").
- v2 incorporates the Codex review (`docs/audits/2026-10-28-f3-reshape-codex-review.md`, F3-R1–R6) and Claude's reply (discussion 99, message 2474).

**What v2 changes from v1.**
- **The estimand.** Relative encounter intensity in eligible sampling units, not abundance. Any biological reading is a separately labelled layer under a named assumption.
- **No tail-probability verdicts.** An absence likelihood is not the probability that a clock maximum is exceeded. That probability would need its own declared model.
- **Sampling units first.** Comparable positive and eligible-negative units are built as a design, not inferred from stage totals.
- **Fossil-to-node mappings** are explicit for every result.
- **A validation study** of the complete procedure replaces the robustness tranche.

v1's direction stands.

## What the recovery study established, and what it did not

The pilot (`models/f3/README.md`, step 3; `models/f3/out/recovery_grid.csv`) leaves four facts.

1. **The older side of an origination interval is the usable part, and it is broad.** For the capacity-profiled logistic fit at mid preservation in the Darriwilian–Sandbian window:
   - **Coverage:** 0.93–0.98 under logistic growth, 0.88 and 0.56 under the two birth–death settings.
   - **Width:** median interval widths of 24–45 Myr.
2. **An old origination is never excluded outright.** Under exponential growth, preservation and origination trade off exactly. Only empty, sampled older units bound an origination, and only under a named history.
3. **About 30 body-fossil records did not pass** under any ramp tested. That is not a universal threshold for every body-fossil design.
4. **The pilot has not validated the procedure proposed here:**
   - its origin search stops at 515.5 Ma;
   - it never used the Cambrian effort;
   - it tuned preservation to hit target record counts;
   - its birth–death likelihood uses the expected trajectory, while the simulator draws stochastic paths.

## The question

**Under which explicit sampling and biological assumptions do the fossil absences behind the land-plant clock maxima support those maxima, and where does the record not constrain them?**

Every maximum F3 tests is a fossil-absence argument. It assumes a lineage would have been preserved and sampled soon after it arose (primer §5.3, assumption 2). The pilot shows that this assumption can be measured, though only through the empty, sampled units older than a first appearance. Testing the maxima, which are inputs, rather than the clock posteriors avoids reusing in the test the fossils that shaped the result. Re-examining a calibration's fossils is still an audit, not independent validation; reused and new evidence are kept apart (F3-R6).

| Maximum | Used by | Fossil basis | Event | Mapping from fossil character to node (named, not assumed) |
|---|---|---|---|---|
| M1: 515.5 Ma, crown Embryophyta | Morris et al. (2018); Su et al. (2021), strategy 1 | Cambrian cryptospore-like palynomorphs | E2 | crown origin implies cryptospore production by then; an old crown need not entail equally old production of the accepted cryptospore categories |
| M2: 459.1 Ma, soft, crown Embryophyta | Hooper et al. (2026) | the oldest possible trilete spores (Dalby) | E1 | Hooper et al.'s ancestral-state reading: the crown ancestor made trilete monads, so trilete production is as old as the crown |
| M3: 431.2 Ma, soft, crown Tracheophyta | Hooper et al. (2026) | *Cooksonia* cf. *pertoni*, Homerian, as a total-group record | E3 | polysporangiophyte bodies are total-group, not crown, tracheophytes; *Cooksonia* is a morphotype (`taxa/cooksonia.md`) |

**Tail specifications are themselves unresolved.** Hooper et al.'s Methods describe 2.5% tails. Their deposited MCMCtree input uses 1% tails for every calibration, and gives 421 Ma, not 420.7, for the tracheophyte minimum. Codex is reconciling which specification produced the published results (Q9).

## What F3 reports

Three layers, each stated with its assumptions.

1. **Data layer: compatibility with the absences.** A unit *i* older than the first appearance has a latent age *t*. It records the event with probability *p_i*(*t*) = 1 − exp(−*r*_c *a*(*t*)). Here *r*_c is the reference encounter rate for the unit's eligibility class *c*, estimated from units after the first appearance with its uncertainty. *a*(*t*) is relative encounter intensity, 1 at the reference. For each candidate origin *T* and each named history class:
   - constant intensity;
   - logistic and birth–death rises;
   - non-monotone paths bounded by a stated ceiling.

   F3 gives the likelihood of the observed non-detections, integrated over each unit's age distribution. The headline summary is *f\**(*T*): the largest effort-weighted mean intensity, across the eligible units between *T* and the first appearance, that is compatible with finding nothing (at 95%, under a binary detection model with clustering). Where eligible effort is zero, the record gives no constraint, and the output says so. Convenient read-outs are the origins at which *f\** falls to 1, 0.1 and 0.01: for example, "origins older than *T*₀.₁ require, on average across these sampled settings, less than a tenth of the reference encounter intensity."
2. **Biological translation: labelled, under a named detection assumption.** Under proportional and comparable detection (D1), relative encounter intensity reads as relative abundance of the producers in the sampled catchments. D1 is stated, not assumed. Production, transport, preservation, preparation and reporting all sit between the two, and the source audit says which of them the data constrain.
3. **Node implication: labelled, under a named mapping** (the table above). A crown-age statement is conditional on the mapping and on the detectability of the producers. Where alternative mappings exist (M1, M3), each gets its own statement.

**Not produced:** a probability that a node is older than its maximum. That needs a joint model with priors on node age, on the character-to-node link and on the nuisance parameters, declared and validated separately; it could follow under Q9. A maximum that the absence record does not support is not thereby shown to be wrong.

**Verdict vocabulary** for each maximum:
- **supported**, under the named detection assumption and mapping: origins materially older than the maximum require mean encounter intensity below a stated fraction of the reference;
- **not supported by the absence record**: such origins remain compatible at or near reference intensity, so the maximum rests on other grounds;
- **not identifiable**: eligible effort is too sparse or too uncertain to say.

Whether a required rare phase is biologically plausible is a separate question, answered from independent biology (primer §6). It is not read off the record.

## Sampling units

Several threats in v1 change what the data mean, not just how precise they are.

- **The unit:** an eligible document × locality × horizon block (Codex is drafting the schema; columns agreed before either of us builds). Genuine sampled horizons are split where the source allows. Known reports of the same material are collapsed (`same_material_as`), and cluster identifiers for document, section and locality are carried.
- **Event-specific outcomes:**
  - E1: triletes under each reading;
  - E2: accepted cryptospores under each reading, including the Cambrian forms.

  "Contains spores" is not an outcome.
- **One sampling frame.** Reference rates and older negatives come from the same source population: Palynodata to 2006 at first. Post-2006 records inform adjudication. They enter the frame only if their denominators are rebuilt too.
- **Eligibility, calibrated where possible.** Units are classed by scope (spore-focused or acritarch- and chitinozoan-focused, from title and microfossil mix), lithology or facies where recorded, and region. Each class's reference rate is estimated from its own positives after the first appearance. An acritarch-only paper then counts as a weaker trial rather than an unknown. What positives cannot calibrate stays a stated sensitivity bound:
  - expectation bias (Cambrian authors who never looked for embryophyte spores);
  - old terminology ("leiospheres", "alete spores"; Strother & Foster 2021, supplement).
- **Ages.** The non-detection probability is integrated over each unit's age distribution, with shared stage-boundary draws from the joint age model. Apportioning effort by overlap would be slightly anti-conservative (Jensen). Broad-age units, such as papers dated only "Early Cambrian", re-enter this way instead of being dropped by the 25 Myr rule.
- **Dependence and heterogeneity:** cluster-level overdispersion, plus leave-one-cluster-out and leave-region-out leverage.
- **Positive controls show preservation opportunity, not equal detection:**
  - Darriwilian cryptospores for E1;
  - Cambrian charophyte-grade palynomorphs for E2.

## Validation before any real-data result

The complete procedure is simulated on the real design:
- unit selection;
- reference selection with finite data;
- age uncertainty and shared boundaries;
- clustering and overdispersion;
- mixtures of eligibility classes, including misassigned classes;
- reporting and facies differences;
- regional confinement;
- monotone and bounded non-monotone histories.

The origin domain extends past the oldest unit, and a profile that reaches the edge is reported as unbounded, not as excluded. **Criteria are fixed before the run:**
- **Coverage:** the reported *f\**(*T*) bounds the true effort-weighted mean intensity in at least 93% of replicates in every correctly specified scenario. That is 95% nominal, less Monte Carlo error at 1,000 replicates.
- **Mis-specified scenarios:** coverage under each is reported as a robustness result, not used as a pass mark.
- **Informativeness:** the share of finite bounds, reported per scenario.
- **No selection after the fact.** Scenarios are not chosen after the real-data answer is seen.

## Where the evidence stands (2026-10-28, before any estimator)

Counts below are Palynodata documents counted in every stage they overlap; the unit table replaces them.

- **M2 (E1, triletes).** First appearance: certain Katian, possible Sandbian (Borenshult and Dalby, contested). Documents below it: Darriwilian 572, Dapingian 500, Floian 405, Tremadocian 418, then about 175–185 per Middle and Late Cambrian stage. Every pre-Katian trilete report checked so far, the Cambrian ones included, is rejected or doubtful (`data/spores/crosswalks/doc_vetting.csv`). Cryptospores in the Darriwilian are a positive control. This is the most informative test.
- **M1 (E2, cryptospores).** First appearance:
  - certain Darriwilian (Hanadir, checked in full text);
  - possible Dapingian (Saudi Dp1). The Argentine record is disputed at specimen level (`docs/rejected-records.md`, entry 16).

  The Cambrian cryptospore-like forms (Laurentia; Kaili Formation, South China) are a positive control under the main reading and the event itself under the inclusive one. Effort reaches back to about 506 Ma before the Early Cambrian units are restored. The likely result is "not identifiable before about 506 Ma", with the deciding evidence named.
- **M3 (E3, plant bodies).** Under the main reading, *C. barrandei* (mid-Sheinwoodian, about 432 Ma; Libertín et al. 2018) predates Hooper et al.'s Homerian basis. It is not, by its age alone, a contradiction: stem lineages can predate a crown. But it bears on the fossil basis of the 431.2 Ma maximum. Zbrza (Hirnantian) is the pivotal alternative. PBDB collection totals are coverage covariates, not a denominator of opportunities to find these bodies. M3 gets a statistical test only if a bounded inventory of comparable positive and eligible-negative beds can be assembled; otherwise it is reported as not identifiable from the assembled data.

## What each event becomes

| Event | Role |
|---|---|
| E1 trilete spores | the M2 test (first) |
| E2 cryptospores | the M1 test, with the Cambrian forms' affinity as the pivotal reading |
| E3 polysporangiophyte bodies | the M3 test where sampling permits; otherwise synthesis, starting with *C. barrandei*'s total-group status |
| E4 tracheids in situ | synthesis and Q5 only |
| E5 lycophyte-line bodies | synthesis only: the minimum calibrations (Yea, Bathurst Island) adjudicated, not tested |
| E6 channel agreement | parked under Q4 until the producer links are scored |
| E7 the Silurian–Devonian rise | Q3, a later investigation with its own estimand and validation |

## Separate but linked: what the maxima do to the dates (Q9)

Whether an absence argument is defensible and how much a maximum moves a clock posterior are different questions. A posterior near its maximum does not by itself show the date is an input. The effective prior includes every calibration and their joint ordering.
- **First step (Codex):** reconcile Hooper et al.'s article, Supplementary Table 4, deposited inputs and prior and posterior outputs, testing whether the deposited outputs reproduce the published node ages.
- **Later:** a controlled recalibration varying maxima and tails with everything else fixed.
- **Any eventual combined analysis** must not count the same fossils in both a calibration prior and a fossil likelihood.

## What this gives up and what it gains

- **Given up:** origination windows and point estimates; probability verdicts on maxima; E4, E6 and E7 as statistical results in this deliverable.
- **Gained:**
  - a question the record can answer, with its conditionality stated in named assumptions;
  - a direct bearing on the calibrations that separate the young and old timescales;
  - a procedure that transfers to any fossil-absence maximum.

  The contribution is not the zero-count algebra, which is standard. It is the adjudicated evidence, the eligible units, the explicit mappings and the propagation of uncertainty.

## Division of work and sequence

Proposed in discussion 99 (message 2474); ownership to be agreed there.

1. **Codex:**
   - the unit-table schema, posted before building;
   - a bounded M2 pilot table (`data/units/`);
   - the Q9 provenance check.
2. **Claude:**
   - the estimator against that schema;
   - the extended origin domain;
   - the validation study (`models/f3/`);
   - occurrence adjudication, including *C. barrandei*.
3. **Both:** fix the validation criteria before running, and review each other's outputs.
4. **Apply:** M2, then M1; M3 only as far as its sampling supports.
5. **Close Loop 1:** value of information and the loop-close entries, as in `docs/plan-f3.md`.

## Open between Claude and Codex

Points Claude proposed in discussion 99 that Codex has not yet answered:
- the biological-translation layer;
- eligibility classes calibrated from positives;
- the coverage criterion above.

Anything still unresolved goes to Barry with both positions stated.
