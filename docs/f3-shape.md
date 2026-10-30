# The shape of F3 (v3)

**Status: adopted, v3, 2026-10-28** (Barry, chat: "Yes, adopt v3"). Drafted by Claude Opus 5.5; Codex agreed the scientific direction (Correspondence `silurian-plants`, discussion 99, message 2484). Codex has since agreed H0's reference ceiling and unconditional coverage as the acceptance target (message 2496). Its implementation review (2026-10-29) led to the repairs under "Repairs after Codex's implementation review", which Codex then checked and accepted (R1). Its second review led to the changes under "Second review", which govern the estimator and await Codex's check. If Codex objects, the disagreement goes back to Barry stated both ways. This document governs F3's statistical contribution (`docs/plan-f3.md`, third amendment). Nothing here has yet been applied to real data.

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
- **H0 (primary; new in v3, agreed by Codex): no pre-appearance intensity above the reference**, *a*(*t*) ≤ 1. This is the biological assumption that a lineage was not more readily encountered before its first recorded appearance than after it. It includes every monotone rise, logistic and birth–death expected paths among them. It is what makes a finite bound possible: Codex's counterexamples (V2-R1) show that unrestricted pulses, or a cluster with a real chance of no detection opportunity, leave no finite bound at all. Under H0 the ceiling is the reference itself, not an arbitrary choice.
- **H0m:** the monotone non-decreasing subset of H0, used for confidence sets on the origin.
- **H1, sensitivity:** any path up to a stated ceiling above the reference, so pulses of any duration up to it. The pulse duration was dropped on 2026-10-29: the bound does not use it (see the refinements below).
- **H0c,** the constant path, is the narrowest class. How each class is computed, exactly or as a conservative bound, is set out under "Repairs".

**Each result is reported in one of four states:**
- **finite data bound:** below the class ceiling;
- **ceiling-limited:** the data do not exclude the ceiling;
- **unbounded:** no finite bound in that class;
- **zero eligible exposure.**

Results from different history classes are not merged into one headline.

**Inference is by test inversion.** For a fixed, predeclared history class, inverting level-0.05 tests of candidate origins gives a 95% confidence set for the origin. Its older endpoint is reported when the set is connected; otherwise the set is reported as found. The summary read-outs, where *f\**_H(*T*) reaches 1, 0.1 and 0.01 of the reference, each carry marginal coverage only. Any claim about the whole curve at once needs separate calibration. Reference-rate uncertainty and the dependence of the reference window on the observed first appearance are part of the test. The critical value is a declared rule: the value matched to the one-sided Poisson limit for the number of older detections (5.99 when there are none, not χ²₁'s 3.84), plus a shift calibrated by simulation at the real design (repair 4).

### 2. Biological translation

This layer is labelled and rests on a named detection assumption. Under proportional and comparable detection (D1), relative encounter intensity reads as relative abundance of the producers in the sampled catchments. Production, transport, preservation, preparation and reporting all sit between the two. The source audit says which of them the data constrain.

### 3. Node implication

This layer is labelled and rests on a named mapping (the table above). The evidence for each mapping is assessed by the trait pilot (`pilot-traits.md`; framing decided by Barry, 2026-10-29).

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
- latent ages within fixed chart boundaries, with boundaries that differ from the chart as a diagnostic;
- clustering and overdispersion;
- eligibility-class mixtures, including misassignment;
- reporting and facies differences;
- regional confinement;
- histories in H0, H0m and H1.

The origin domain extends past the oldest unit, and a profile that reaches the edge is reported as unbounded. The quantity validated is the reported one: the confidence set or endpoint for the origin, and the marginal read-outs.

**Acceptance per correctly specified cell** (fixed before the run; stage 2 corrected after Codex's review, I3):
- **Nominal and floor.** Nominal coverage is 95%. The floor is 0.93, a chosen scientific tolerance and not a Monte Carlo allowance.
- **Stage 1.** Run 1,000 replicates. The cell passes if the one-sided 95% exact lower limit of coverage exceeds 0.93 (at least 944 successes), and fails if the one-sided 95% upper limit is below 0.93 (at most 915).
- **Stage 2.** A borderline cell gets one preplanned further batch of 1,000. The pooled 2,000 must show at least 1,886 successes. That threshold holds the chance of certifying a procedure at the floor to 5% over both stages. The first version reapplied a fixed-sample limit (1,880) after the interim look, which certified it 6.9% of the time.

**Operating characteristics** (exact binomial sums):

| True coverage | P(pass) |
|---|---|
| 0.95 | 0.950 |
| 0.94 | 0.427 |
| 0.93 | 0.048 |
| 0.92 | 0.002 |

The one-stage rule alone passes a perfectly calibrated cell only 83% of the time, so a grid of many cells would fail good procedures by chance. No batches beyond the preplanned one. The number of cells, and the expected count of chance failures among them, are stated with the grid.

**A failing cell, or a plausible mis-specified scenario that reverses a conclusion, changes the report.** The conclusion is qualified by that assumption, the model is expanded, or the sensitivity is reported as unresolved. It is not confined to a robustness table.

## Refinements from the estimator build (2026-10-29, Claude)

The estimator, simulator and smoke-scale harness are in `models/f3/` (`envelope.py`, `units_sim.py`, `validate.py`). They were built by a Claude Sonnet 5.5 subagent to the construction above and reviewed by Claude Opus 5.5. The as-built smoke run is preserved at `c7729ad`. It and the review changed six points. Codex's implementation review then overturned three of them: the exactness of the critical value (item 1), the shared alternative's cover for the logistic class (item 2), and the equal-duty H0 (item 6). The next section replaces them. Items 3–5 stand.

1. **Critical value.** Both *f\** and the origin sets are one-sided upper limits on the older units' exposure, and F3's older units mostly have no detections. In that regime the statistic is −2 log P0, so χ²₁ at 3.84 rejects whenever P0 < 0.147. A one-sided level-0.05 test needs P0 < 0.05, a critical value of 5.99.
   - **As-built smoke run (χ²₁):** *f\** coverage over non-trivial replicates was 0.87–0.95 in the cells below the ceiling.
   - **Count-matched value:** 0.94–0.99.
   - **Smoke re-run with all the refinements:** coverage over all replicates is 0.93–0.99, against 0.91–0.95 under χ²₁ (`models/f3/README.md`, "Smoke results").
   - **The rule now:** the critical value reproduces the exact one-sided Poisson (Garwood) limit for the number *n* of older detections in (τ, *T*]. It is 5.99 at *n* = 0 and falls towards the one-sided χ² value of 2.71.
2. **One alternative for the bounded classes.** H0c, H0, logistic and H1 are tested against the best constant history on [0, ceiling]. That history belongs to each of those classes, so the test stays conservative where the H0 bound is not attained. H0m's members are explicit, and it uses its own exact supremum. With no older detection, nothing changes.
3. **H1 is a ceiling class.** The convex-order bound holds for every path up to the ceiling, so a pulse-duration limit adds nothing to it. H1 is now "any path up to *C* times the reference".
4. **The scale is the reference window's own intensity.** *a* = 1 means the window's intensity, wherever the observed first appearance puts the window. If the first appearance falls inside a rise, the window is itself low. In the smoke cells with a(t) = 0.3 before τ0, the realised window averaged 0.56–0.72 of the established intensity. *f\** is then relative to that lower level, which a reader of "*f\** = 0.5" must be told. The biological layer states this. The validation scores the truth on the same scale.
5. **τ is the base (older boundary) of the oldest stage holding a certain detection.** That stage opens the reference window, so older units are those with any part of their range older than it. The draft specification had called this the stage's "top"; the name is now fixed.
6. **Limits stated, not fixed:**
   - **H0 is bounded over equal-duty paths only.** A path that concentrates its duty where unit rates are higher fits slightly better when class mix differs between stages. For a 10-fold class contrast in separate stages the gap is at most 0.06 in log P0, about 3% in *f\**.
   - **With no older detection, H0m origin sets end the longest declared delay beyond H0c's.** H0m adds to the origin only through that declared bound; its value is in *f\**.

**What is validated.** Coverage is over all replicates, as above. A replicate whose true origin lies at or below the estimated τ makes no claim and counts as covered. Coverage over the non-trivial replicates is reported beside it, because it is lower: in the stationary as-built cell it was 0.84 under the count-matched value. It is a relevant-subset diagnostic, not the acceptance quantity.

## Repairs after Codex's implementation review (2026-10-29; Claude, awaiting Codex's check)

Codex reviewed the estimator at `b2c6443` (`docs/audits/2026-10-29-f3-implementation-review.md`, I1–I4). Claude Opus 5.5 reproduced its counterexamples and its sequential calculation, and accepts its findings. The repairs restore the classes this document declares, and govern the estimator from this date.

1. **Fixed stage boundaries (I4).** The printed "±" values are not standard deviations (primer §1), so independent normal draws, sorted, are not a geological age model. The primary analysis fixes the ICS v2024/12 bases. Boundary uncertainty enters as two coherent scenarios: every base moved by its printed value towards older, or towards younger, ages, with blank values held at the chart age. Joint posterior draws, where they exist, would replace both. Latent ages within a unit's stage range are still integrated exactly.

2. **The history classes are what they say (I1).** With fixed boundaries, every unit's age density is uniform within each piece of (τ, *T*] cut by the stage bases. A path therefore enters every unit's likelihood only through its piece means *x_p*: exactly for a constant path, and through two per-unit bounds otherwise.
   - **Non-detection:** for *a* ∈ [*L_p*, *U_p*] with mean *x_p*, E e^(−*ru a*) is at most the chord between *L_p* and *U_p* (convexity).
   - **Detection:** E[1 − e^(−*ru a*)] ≤ 1 − e^(−*ru x_p*) (Jensen).

   Multiplied within a cluster given *u* and integrated over *u*, the bounds cover the likelihood of every path with those means. Each class is then an optimisation over *x*:
   - **H0c:** constant *x*, with the exact likelihood.
   - **H0:** any *x* ∈ [0, 1]^P. It is exact when no older unit detects, because a path at 0 or 1 within each piece attains every unit's bound at once. It replaces the equal-duty surrogate.
   - **H0m:** *x* monotone non-decreasing towards τ, ≤ 1. It is a conservative bound, because a monotone path can be two-valued within only one piece. It replaces the delayed-step grid.
   - **H1:** any *x* ∈ [0, *C*]^P.
   - **Logistic is withdrawn as a confidence class.** Its paths lie in H0m, and without a constant submodel the shared alternative did not nest it. Logistic histories stay in the validation as truths.

   The target is linear in *x*: ā_r = Σ *c_p x_p*, where *c_p* is piece *p*'s share of the older units' reference exposure. Since the second review its weights are the rates being fitted, not the reference-window estimates (below, item 1). *f\** is the largest *f* for which the class supremum over ā_r ≥ *f* is not rejected. The alternative is the best constant history on [0, class ceiling]: one alternative for H0c, H0m and H0, whose statistics therefore nest, *f\**(H0c) ≤ *f\**(H0m) ≤ *f\**(H0). Each fit is multi-started, including from an allocation that hides intensity in the sparsest pieces, and reports its convergence. A fit whose starts disagree by more than 0.05 in log-likelihood is flagged.

3. **Origin read-outs.** "*a* ≥ *f*_min on (τ, *T*]" holds pointwise:
   - **H0c:** constant at or above *f*_min.
   - **H0:** any path in [*f*_min, 1]. It equals H0c when no older unit detects.
   - **H0m:** monotone, and at or above *f*_min from at most *D* = 10 Myr after the origin. *D* was the longest delay on the old grid and is now continuous.

   The reported set includes its younger part: every origin between the top of the first-appearance stage and τ belongs to it by construction (I3).

4. **The critical value is a declared rule, calibrated by simulation (I2).** The count-matched value is exact only for fixed rates and independent Poisson counts. Profiled reference rates, a selected window and clusters break that.
   - **Codex's counterexamples reproduce.** Its exact Bernoulli enumerations reject at 0.098 for 10 reference units and 50 older ones at *p* = 0.84. For 10 and 200 at *p* = 0.04, given a reference detection, they reject at 0.089.
   - **They need thin reference windows.** At sizes near F3's design (30, 60 or 200 reference units, *p* 0.04–0.12, given a reference detection), the same enumeration gives 0.019–0.031 (Claude, 2026-10-29).
   - **The rule now.** The critical value is the count-matched value plus a shift δ ≥ 0. δ is set by simulation at the real design as the smallest value giving coverage of at least 0.95 in every correctly specified calibration cell. The calibration replicates are separate from the acceptance run. Until then, δ = 0.

5. **Stage 2 needs 1,886 of 2,000 (I3);** see the operating characteristics above.

6. **The binding validation runs on the real design (I3).** It simulates outcomes on the real unit table, with its ranges, classes, clusters and frame, once that table exists. Each replicate selects its own first appearance. Until then, a development grid on the synthetic Palynodata design looks for failure modes and binds nothing. Both grids add cells the smoke grid lacked:
   - **Least-favourable members:** paths that put their intensity in the sparsest stages, for H0 and H1.
   - **Confounding:** class composition that changes with age.
   - **Off-grid H0m members:** an off-grid step, a linear rise and a logistic rise.
   - **Diagnostics:** eligibility misassignment, lower reporting in older units, regional confinement, a wrong cluster shape, and boundaries that differ from the chart.

   **The development grid has run** (2026-10-29, 21 cells × 1,000 replicates; `models/f3/README.md`). Every correctly specified cell would pass stage 1 at δ = 0, with coverage 0.946–0.995. The diagnostics stay at or above 0.945 against the effective target. Read against the nominal path, regional confinement falls to 0.907–0.936, so the biological translation (§2) must state that *f\** bounds reported, range-averaged intensity.

7. **Reporting.** Unconditional coverage is the acceptance quantity, and Codex agrees. Coverage over the truth-defined subset, where the true origin is older than τ̂, remains a diagnostic of non-uniformity. Any observable reporting rule, such as finite against unbounded or a minimum older exposure, is declared before calibration and calibrated with the procedure.

## Second review: target, numerical status and the calibration contract (2026-10-29; Claude; checked by Codex)

Codex checked the repairs (`docs/audits/2026-10-29-f3-repairs-and-frame-review.md`, R1–R4; Correspondence 2541). It accepted the chord and Jensen construction within its model, the fixed boundaries and their scenarios, the withdrawal of logistic as a class and stage 2 at 1,886. It asked for three changes before any binding calibration. Claude Opus 5.5 accepts all three and has made them in `models/f3/`.

1. **The constraint targets the true-rate quantity (R2).** The weights *c_p* were fixed at the rates fitted to the reference window alone, while validation scored against the generating rates. In Codex's A12 example the two weightings give 0.212 and 0.173. The constraint ā ≥ *f* now uses *c*(*r*) at the rates being profiled, so the supremum is over the target as defined in §1, not over a plug-in. *c* depends on *r* only through the class mix of the older exposure: with one class carrying the exposure, or one piece, it is fixed. Otherwise the constraint is bilinear in (*r*, *x*). A differential-evolution search agrees with the optimiser on a two-class design to 2 × 10⁻³ in log-likelihood (`test_envelope.py`).

2. **One normalisation (R2).** "*a* = 1 in the reference window" is now realised in the same way on both sides of the ratio. The reference mean is integrated over the reference units' age ranges, weighted by the true rates, as the older target already was. Validation had divided by the path at the hidden realised ages. Hidden ages are part of the random data, not of the parameter, so the integrated form is the target. The realised form is kept as a diagnostic.

3. **A numerical status belongs to the result it describes (R3).**
   - A fit returns its highest feasible candidate with that run's own status. Candidates within 10⁻⁶ in log-likelihood count as equal, and a converged one is preferred.
   - A selected run that did not converge is restarted once from where it stopped. If it still fails, the fit has failed.
   - A statistic fails when its alternative or its null fails. Origin sets carry the status of every grid point.
   - In validation, a failed decisive statistic does not cover at any shift. An unresolved optimisation can therefore never produce a finite exclusion that counts as success.
   - **Two causes of false failure were found and removed.** First, SLSQP reports failure (mode 8) for a run that sits inside the 10⁻⁶ constraint tolerance and gains 10⁻⁸ in log-likelihood; the tie rule handles it. Second, at the class ceiling (*f* = *C*, which happens when the reference window lies wholly inside the reduced-intensity period) the feasible set is the single point *x* ≡ *C*. There the null is the constant history *C*, whose bound likelihood is exact.

4. **The calibration and acceptance contract (R4).** These terms are fixed before the binding run:
   - **Inputs.** The real unit table, the analysis specification, the code and the timescale are hashed into a receipt. The nuisance grid is the declared cell list, rebuilt on the real design.
   - **Seeds.** Calibration and acceptance draw from disjoint seed streams: root seeds 20261101 and 20261102, with acceptance stage 1 on replicates 0–999 and stage 2 on 1,000–1,999.
   - **One shift.** δ is a tuning proposal: the smallest shift, not below 0, at which the stored truth-point margins of every acceptance quantity of every acceptance cell reach 0.955 in the calibration batch. The outputs were computed at shift 0 and a wider critical value changes grid sets and numerical searches, so delivered coverage at δ is what the independent acceptance run establishes (target agreed by Claude and Codex, Correspondence 2553 and 2557; nominal coverage stays 0.95). The acceptance quantities are *f\** coverage under each class that contains the truth, plus each fixed origin read-out (below). δ is written to the receipt before acceptance starts. The acceptance run refuses a receipt whose code or inputs differ, whose protocol (calibration seed, replicates 0–999, target) differs, which does not cover exactly the grid's acceptance quantities, or whose δ is not finite and non-negative.
   - **Scoring.** Each replicate is scored against the true-rate, range-integrated target (items 1–2).
   - **Fixed read-outs.** An origin read-out is accepted against only in cells whose truth satisfies its hypothesis for every possible τ: the truth is in the class and *a* ≥ *f*_min on (τ₀, *t*₀ − *D*]. Those cells give it the full 1,000 replicates. A read-out chosen from the simulated truth remains a diagnostic, reported with its denominator.
   - **Replicates without a result.** A replicate with no first appearance makes no claim, so it covers, and its frequency is reported. An error, or a failed delivered output, does not cover.
   - **What is validated is the delivered output.** A replicate covers when the reported bound or set was computed successfully and contains the truth: for *f\**, the bound and the statistic at the truth both converged and the statistic is within the critical value; for an origin read-out, the set and the statistic at *t*₀ both converged and the grid set contains *t*₀. Coverage of the truth-point test alone is a diagnostic (third review, below).
   - **What the shift guarantees.** δ tunes the procedure on 1,000 calibration replicates. At 0.95 that empirical quantile reaches the population's 95th percentile with probability of only about 0.46; at the agreed 0.955 about 0.74 (Codex). A maximum over a finite grid is not least-favourable over every nuisance value. The certificate is the independent acceptance run against the 0.93 floor. The claim made is acceptance at that floor, not population coverage of 0.95.
   - **Implementation.** `validate.py` runs the phases `dev`, `calibrate` and `accept`; acceptance stage 2 completes a verified stage-1 verdict file (third review).

5. **Shared ages within a section (R1).** The likelihood treats unit ages as independent given their ranges, and the envelope argument is proved for that case. Samples from one section or borehole are ordered by depth, so their ages are not independent. Three diagnostic cells test it (`models/f3/README.md`): in D7 and D8 every unit of a cluster takes the same relative position in its own range, so a whole section is early or late together, with mean cluster size 3 and 10; D9 is D8's independent-age control. Coverage holds: shared ages cost nothing measurable at size 3 and about 0.01 at size 10 (0.969 against 0.979 under H0c), and stay at or above 0.969 in every class. The limitation is therefore declared rather than the likelihood extended. Codex agreed, with a condition (Correspondence 2557): D7–D9 test one construction, not every geological dependence, and the 0.01 is neither a universal bound nor evidence that dependence is negligible. Before application, the binding grid freezes the real frame's cluster sizes and plausible coeval, depth-ordered and shared-boundary scenarios. If the intended claim does not survive them, the claim is narrowed or the likelihood extended; a failed case is not relabelled as a diagnostic while an unconditional claim is kept.

6. **Dress rehearsal on the synthetic design.** Calibration, receipt and stage-1 acceptance were run on the development design (`models/f3/README.md`, "Second-review rehearsal"); stage 2 was not needed and was not yet executable. It binds nothing; the binding run waits for the real frame.
   - **Calibration** gave δ = 0: all 117 acceptance quantities reached 0.95 unshifted (lowest A15 under H0c, 952 of 1,000).
   - **Independent acceptance** at that δ passed all 117 at stage 1 (lowest A15 under H0c, 946; the pass line is 944).
   - **Numerics.** One fit failed in 63,000 replicates, and it counted as a miss. Every calibration miss was re-solved from about 65 further starts, and none became a cover, so the misses are sampling, not missed optima.
   - **The repair barely moves the statistic.** Re-running the development seeds with the repaired code leaves *f\** under H0c unchanged and coverage within 0.002 everywhere. The development grid's δ = 0.11 against 0 here is batch variation at a cell near 0.95: A15 under H0c covers 0.948 over three batches.
   - **The acceptance rule's operating characteristic matters at that level.** A cell at 0.948 fails acceptance with probability 0.105, one at 0.955 with 0.004. Hence the proposal below to calibrate to 0.955.

## Third review: the executable contract (2026-10-29; Codex found, Claude repaired)

Codex accepted R2 and the core R3 repairs, reproduced all 117 rehearsal quantities from the stored replicates, and found four places where the code fell short of the contract above (Correspondence 2557; `docs/audits/2026-10-29-f3-response-and-ghelli-frame.md`). Claude Opus 5.5 repaired all four in `models/f3/validate.py` (`models/f3/README.md`, "Third-review repairs"):

1. **Stage 2 runs.** It refuses a stage-1 verdict file that is not complete, or was made on another receipt, code or seed; reruns only the cells with a borderline quantity on replicates 1,000–1,999; pools each borderline quantity's 2,000 and applies 1,886. The grid is accepted when every acceptance quantity passes.
2. **The receipt's scope is checked**, as in item 4 above.
3. **Delivered coverage is the acceptance quantity**, as in item 4. Before, a replicate whose bound failed could count as covering because the statistic at the truth converged.
4. **Summaries carry status.** *f\** at 459.1 keeps its status and spread; medians, states and set shapes count converged outputs, with failures counted beside them.

Re-summarised under the new rules, the stored calibration, acceptance and paired development runs are unchanged, and the delivered bound and the truth-point test never disagree. Only shared-age D9 under H1 moves, from 0.996 to 0.995. Pooled over the three stored batches, A15 under H0c is the one quantity below 0.955 (0.948, δ = 0.33). Single batches give δ = 0.14, 0.22 and 0.38, so the binding δ is one draw from that spread, and one long-gap cell sets the width of every bound.

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

Codex agreed H0, the reference ceiling and unconditional coverage (message 2496), accepted the repairs (R1, message 2541), accepted R2 and the core R3 repairs (message 2557), agreed the 0.955 calibration target (message 2557) and integrated the productivity condition into the reporting rule (`data/units/reporting-rule.md`, message 2558). Codex accepted the third-review repairs and the replicate re-scoring (messages 2628, 2629); its strict-parsing correction is made (`models/f3/README.md`, "Sixth review").

**A design screen gates qualification (Claude, 2026-10-31; `docs/audits/2026-10-31-borenshult-reading-and-screen.md`).** Before a binding grid is built on a real frame, the frame must pass `models/f3/screen.py` under at least one declared reading. The screen bounds the zero-count statistic by 2 m r f, which nothing in the real test can raise; the reading set is fixed from the sources, not from the screen. Borenshult, the core behind M2's own fossil, fails under both readings: under main it has no in-frame E1 reference, and under inclusive its three Darriwilian samples give at most 3.2 against 5.99. Its absence premise therefore cannot be tested on its own core, whatever the age model.

Open, posted in discussion 99:
- **the shared-age scenarios for the binding grid** (item 5): built on the first frame that passes the screen, with Borenshult's ordered depths, shared boundaries and common ash correlation (Codex, `data/units/borenshult_ages.csv`) as the template;
- **the frame tranche** (Codex): a frame with in-frame E1 detections after the first appearance under main (Katian or later) and tens of eligible, productive older units, or a declared transport assumption between a reference core and older cores; a complete original sample log, or another source with documented complete sample and event reporting. Hanadir's 1996 chart gives 14 depths but does not certify a complete processed inventory; Pelmis (Ghavidel-Syooki 2017) gives 27 productive sample codes, with its 140-sample collection and the MG-130 discrepancy still to reconcile.

Anything unresolved goes to Barry with both positions stated.
