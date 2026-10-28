# The shape of F3 (v3)

**Status: proposal, v3, 2026-10-28.** Drafted by Claude Opus 5.5. Codex agrees the scientific direction in principle (Correspondence `silurian-plants`, discussion 99, message 2484). Two refinements in this version are new and await Codex's reply; they are marked. Nothing here has been applied to real data. Adoption is Barry's decision.

**Revision history.**
- **v1** (`f01d4bd`) followed Barry's adoption of the second amendment (chat, 2026-10-28: "Yes, agreed, adopt it. Then let's re-assess the full shape of F3 given this constraint").
- **v2** (`eebb5e9`) incorporated the first Codex review (`docs/audits/2026-10-28-f3-reshape-codex-review.md`, F3-R1–R6).
- **v3** incorporates the second (`docs/audits/2026-10-28-f3-reshape-v2-codex-review.md`, V2-R1–R5, and the draft unit interface in message 2483), with Claude's reply in discussion 99.

## What the recovery study established, and what it did not

The pilot (`models/f3/README.md`, step 3; `models/f3/out/recovery_grid.csv`) leaves four facts.

1. **The older side of an origination interval is the usable part, and it is broad.** For the capacity-profiled logistic fit at mid preservation, Darriwilian–Sandbian window:
   - **coverage** 0.93–0.98 under logistic growth, 0.88 and 0.56 under the two birth–death settings;
   - **median interval widths** of 24–45 Myr.
2. **An old origination is never excluded outright.** Under exponential growth, preservation and origination trade off exactly. Only empty, sampled older units bound an origination, and only under a named history.
3. **About 30 body-fossil records did not pass** under any ramp tested; that is not a universal threshold.
4. **The pilot has not validated the procedure proposed here:**
   - its origin search stops at 515.5 Ma;
   - it never used the Cambrian effort;
   - it tuned preservation to target record counts;
   - its birth–death likelihood uses the expected trajectory, while the simulator draws stochastic paths.

## The question

**Under which explicit sampling and biological assumptions are older origins incompatible with the fossil absences behind the land-plant clock maxima, and where does the record not constrain them?**

Every maximum F3 tests is a fossil-absence argument. It assumes a lineage would have been preserved and sampled soon after it arose (primer §5.3, assumption 2). That assumption can be measured, though only through the empty, sampled units older than a first appearance. Testing the maxima, which are inputs, rather than the clock posteriors avoids reusing in the test the fossils that shaped the result. Re-examining a calibration's fossils is still an audit, not independent validation: reused and new evidence are kept apart. A maximum the absence record fails to support is not thereby wrong.

| Maximum | Used by | Fossil basis | Event | Mapping from fossil character to node (named, not assumed) |
|---|---|---|---|---|
| M1: 515.5 Ma, crown Embryophyta | Morris et al. (2018); Su et al. (2021), strategy 1 | Cambrian cryptospore-like palynomorphs | E2 | crown origin implies cryptospore production by then; an old crown need not entail equally old production of the accepted cryptospore categories |
| M2: 459.1 Ma, soft, crown Embryophyta | Hooper et al. (2026) | the oldest possible trilete spores (Dalby) | E1 | Hooper et al.'s ancestral-state reading: the crown ancestor made trilete monads, so trilete production is as old as the crown |
| M3: 431.2 Ma, soft, crown Tracheophyta | Hooper et al. (2026) | *Cooksonia* cf. *pertoni*, Homerian, as a total-group record | E3 | polysporangiophyte bodies are total-group, not crown, tracheophytes; *Cooksonia* is a morphotype (`taxa/cooksonia.md`) |

**Tail specifications are unresolved.** Hooper et al.'s Methods describe 2.5% tails. Their deposited MCMCtree input uses 1% tails for every calibration, and gives 421 Ma, not 420.7, for the tracheophyte minimum. Matching the deposited outputs to the published dates would be a consistency check, not decisive provenance (Q9, below).

## What F3 reports

Three layers, each with its assumptions stated.

### 1. Data layer: compatibility with the absences

**The detection model.**
- **Detection probability.** A unit *i* older than the first appearance has a latent age *t*, and detects the event with probability *p_i*(*t*) = 1 − exp(−*r*_c *a*(*t*)).
- **Reference rate.** *r*_c is the reference encounter rate for the unit's eligibility class *c*. It is estimated, with its uncertainty, from the complete eligible reference frame after the first appearance: detections and eligible non-detections.
- **Intensity.** *a*(*t*) is relative encounter intensity, 1 at the reference.

**The target.** With known ages, the zero-count likelihood constrains the reference-rate-weighted mean intensity, ā_r = Σ *r*_c *a*(*t_i*) / Σ *r*_c, across the eligible units between a candidate origin *T* and the first appearance. With latent ages, the target is the ratio of integrated weighted intensity to integrated reference exposure over that interval. The likelihood integrates over the joint latent structure (unit ages, shared stage boundaries, clusters), not over separately marginalised units.

**History classes are declared before analysis, and each gets its own result:**
- **H0 (primary; new in v3, awaiting Codex): no pre-appearance intensity above the reference**, *a*(*t*) ≤ 1. This is the biological assumption that a lineage was not more readily encountered before its first recorded appearance than after it. It includes every monotone rise, logistic and birth–death expected paths among them. It is what makes a finite bound possible: Codex's counterexamples (V2-R1) show that unrestricted pulses, or a cluster with a real chance of no detection opportunity, leave no finite bound at all. Under H0 the ceiling is the reference itself, not an arbitrary choice.
- **H0m:** the monotone non-decreasing subset of H0, used for confidence sets on the origin.
- **H1, sensitivity:** bounded pulses above the reference, with the ceiling and pulse duration stated.

**Each result is reported in one of four states:**
- **finite data bound:** below the class ceiling;
- **ceiling-limited:** the data do not exclude the ceiling;
- **unbounded:** no finite bound in that class;
- **zero eligible exposure.**

Results from different history classes are not merged into one headline.

**Inference is by test inversion.** For a fixed, predeclared history class, inverting level-0.05 tests of candidate origins gives a 95% confidence set for the origin. Its older endpoint is reported when the set is connected; otherwise the set is reported as found. The summary read-outs, where *f\**_H(*T*) reaches 1, 0.1 and 0.01 of the reference, each carry marginal coverage only. Any claim about the whole curve at once needs separate calibration. Reference-rate uncertainty and the dependence of the reference window on the observed first appearance are part of the test.

### 2. Biological translation

This layer is labelled and rests on a named detection assumption. Under proportional and comparable detection (D1), relative encounter intensity reads as relative abundance of the producers in the sampled catchments. Production, transport, preservation, preparation and reporting all sit between the two. The source audit says which of them the data constrain.

### 3. Node implication

This layer is labelled and rests on a named mapping (the table above).

**Verdicts** (V2-R4):
- **incompatible with the specified encounter histories;**
- **compatible with them;**
- **uninformative under the stated model.**

A further statement that the record *supports a maximum* is made only beside an independently justified restriction on how rare, geographically confined or delayed the lineage could have been, and that restriction is stated with it. Whether a required rare phase is biologically plausible is answered from independent biology (primer §6), not read off the record. The surface or confidence set is reported before any label at M1, M2 or M3. The maximum is a comparison point, not necessarily the boundary the data identify.

**Not produced:** a probability that a node is older than its maximum. That needs a joint model with priors on node age, on the character-to-node link and on nuisance parameters, declared and validated separately, possibly under Q9.

## Sampling units

**Interface.** The draft is in discussion 99, message 2483; Codex owns it. Two tables:
- **`units.csv`:** one row per unique material/locality/horizon block, with clusters, age model and evidence.
- **`outcomes.csv`:** one row per unit × event × reading, with outcome, eligibility and evidence.

**Rules:**
- **Frame inclusion is auditable** and independent of the target result. Exclusions and unresolved candidates are recorded.
- **Outcomes are specific to the event and the reading.** "Contains spores" is not an outcome, and extra event or reading rows never multiply units.
- **Outcomes distinguish:**
  - `detected`;
  - `explicit_non_detection`;
  - `not_reported`;
  - `unresolved`.

  Converting them to a binary reported-encounter outcome follows a named reporting rule.
- **Age uncertainty is kept separate from genuinely different sampled horizons.**
- **The first-appearance rule, reference window and eligible older units are not attributes of the evidence.** They belong to a named analysis specification (Claude, `models/f3/`).

**Eligibility.**
- **Scope comes from stated aims, methods and reporting coverage**, never from whether the target was found.
- **Unknown eligibility stays unknown.**
- **Reference rates are estimated per class** from that class's detections and eligible non-detections. The transport assumption from the reference interval to older intervals is stated, and the reference composition is standardised or stratified. Pooling across classes that lack reference support needs its own stated assumption.
- **A paper on other palynomorphs** "may contribute a class-calibrated trial where reference support and the reporting audit justify it; otherwise eligibility and detection remain unresolved" (V2-R2). The direction of its difference from a spore-focused class is estimated, not assumed.
- **Expectation bias and old terminology** ("leiospheres", "alete spores"; Strother & Foster 2021, supplement) remain stated sensitivity bounds.

**One sampling frame.** Reference rates and older negatives come from the same source population: Palynodata to 2006 at first. Post-2006 records inform adjudication. They enter the frame only if their denominators are rebuilt too.

**Positive controls** show preservation opportunity, not equal detection:
- Darriwilian cryptospores for E1;
- Cambrian charophyte-grade palynomorphs for E2.

## Validation before any real-data result

The complete procedure is simulated on the real design:
- the selection of the first appearance, the reference set and the older units (no conditioning on replicates that happen to be empty);
- finite reference data;
- latent ages with shared boundaries;
- clustering and overdispersion;
- eligibility-class mixtures, including misassignment;
- reporting and facies differences;
- regional confinement;
- histories in H0, H0m and H1.

The origin domain extends past the oldest unit, and a profile that reaches the edge is reported as unbounded. The quantity validated is the reported one: the confidence set or endpoint for the origin, and the marginal read-outs.

**Acceptance per correctly specified cell** (fixed before the run; the rule itself is new in v3 and awaits Codex):
- **Nominal and floor.** Nominal coverage is 95%. The floor is 0.93, a chosen scientific tolerance and not a Monte Carlo allowance.
- **Stage 1.** Run 1,000 replicates. The cell passes if the one-sided 95% exact lower limit of coverage exceeds 0.93 (at least 944 successes), and fails if the one-sided 95% upper limit is below 0.93 (at most 915).
- **Stage 2.** A borderline cell gets one preplanned further batch of 1,000. The pooled 2,000 must show at least 1,880 successes.

**Operating characteristics:**

| True coverage | P(pass) |
|---|---|
| 0.95 | 0.983 |
| 0.94 | 0.57 |
| 0.93 | 0.07 |
| 0.92 | 0.002 |

The one-stage rule alone passes a perfectly calibrated cell only 83% of the time, so a grid of many cells would fail good procedures by chance. No batches beyond the preplanned one. The number of cells, and the expected count of chance failures among them, are stated with the grid.

**A failing cell, or a plausible mis-specified scenario that reverses a conclusion, changes the report.** The conclusion is qualified by that assumption, the model is expanded, or the sensitivity is reported as unresolved. It is not confined to a robustness table.

## Where the evidence stands (2026-10-28, before any estimator)

The counts below are Palynodata documents counted in every stage they overlap; the unit table replaces them.

- **M2 (E1, triletes).**
  - **First appearance:** certain Katian, possible Sandbian (Borenshult and Dalby, contested).
  - **Documents below it:** Darriwilian 572, Dapingian 500, Floian 405, Tremadocian 418, then about 175–185 per Middle and Late Cambrian stage.
  - **Earlier reports:** every pre-Katian trilete report checked so far, the Cambrian ones included, is rejected or doubtful (`data/spores/crosswalks/doc_vetting.csv`).
  - **Positive control:** Darriwilian cryptospores.

  The most informative test.
- **M1 (E2, cryptospores).**
  - **First appearance:** certain Darriwilian (Hanadir, checked in full text); possible Dapingian (Saudi Dp1). The Argentine record is disputed at specimen level (`docs/rejected-records.md`, entry 16).
  - **Cambrian forms:** the cryptospore-like forms (Laurentia; Kaili Formation, South China) are a positive control under the main reading and the event itself under the inclusive one.
  - **Likely result:** "uninformative before about 506 Ma", with the deciding evidence named, unless the broad-age Early Cambrian units carry weight once restored.
- **M3 (E3, plant bodies).**
  - **Oldest record:** under the main reading, *C. barrandei* (mid-Sheinwoodian, about 432 Ma; Libertín et al. 2018) predates Hooper et al.'s Homerian basis. It is not, by its age alone, a contradiction, since stem lineages can predate a crown, but it bears on the fossil basis of the 431.2 Ma maximum.
  - **Pivotal alternative:** Zbrza (Hirnantian).
  - **Effort:** PBDB collection totals are coverage covariates, not a denominator of opportunities.
  - **Test:** statistical only if a bounded inventory of comparable positive and eligible-negative beds can be assembled. Otherwise, uninformative from the assembled data.

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

Whether an absence argument is defensible and how much a maximum moves a clock posterior are different questions. The effective prior includes every calibration and their joint ordering.
- **First step (Codex):** trace the deposited outputs to their calibration trees and control settings through headers, logs or run records. Identify the focal nodes from the labelled topology, and reproduce the reported summaries with declared units, chains, burn-in and interval definitions.
  - **If the files cannot link settings to outputs**, the discrepancy stays unresolved and the 1% and 2.5% specifications are analysed as alternatives.
  - **Matching rounded ages** is a consistency check, not proof of which run produced the paper (V2-R5).
- **Later:** a controlled recalibration varying maxima and tails, holding everything else fixed.
- **Combined analyses:** any eventual one must not count the same fossils in both a calibration prior and a fossil likelihood.

## What this gives up and what it gains

- **Given up:** origination windows and point estimates; probability verdicts on maxima; E4, E6 and E7 as statistical results in this deliverable.
- **Gained:**
  - a question the record can answer, with its conditionality stated in named assumptions;
  - conditional exclusions where the data justify them;
  - a direct bearing on the calibrations that separate the young and old timescales;
  - a procedure that transfers to any fossil-absence maximum.

  The contribution is not the zero-count algebra, which is standard. It is the adjudicated evidence, the eligible units, the explicit mappings and the propagation of uncertainty.

## Division of work and sequence

Agreed in discussion 99 (messages 2474, 2477 and 2484).

1. **Codex:**
   - the unit interface (`data/units/`) and a source-audited M2 pilot that deliberately includes detections, defensible negatives, unknowns, duplicates and broad-age cases;
   - the Q9 provenance check.
2. **Claude:**
   - the analysis specification and estimator against the agreed interface;
   - the extended origin domain;
   - the validation study (`models/f3/`);
   - occurrence adjudication, including *C. barrandei*;
   - named reading definitions for the outcome table.
3. **Both:** settle the validation grid and acceptance rule before running, and review each other's outputs.
4. **Apply:** M2, then M1; M3 only as far as its sampling supports.
5. **Close Loop 1:** value of information and the loop-close entries, as in `docs/plan-f3.md`.

## Open between Claude and Codex

These are new in v3, posted in discussion 99:
- **H0** as the primary history class, with the reference as its ceiling;
- **the two-stage acceptance rule;**
- **Claude's comments on the interface:**
  - recorded palynomorph types as preservation evidence;
  - Palynodata age names and crosswalk grade as age evidence;
  - E1 and E2 outcomes filled on the same pilot units;
  - a `readings.csv` in `data/occurrences/` defining the named readings.

Codex agrees the rest. Anything unresolved goes to Barry with both positions stated.
