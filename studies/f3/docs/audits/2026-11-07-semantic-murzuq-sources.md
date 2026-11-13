# Semantic review: Murzuq, M1/M2 and source-facing claims

**Reviewed:** commit `87ad964`, against `manuscript/estimands.md`, 7 November 2026
**Scope:** article abstract, §§2, 3.1, 3.2, 4, 5 and Table 4; brief; Supplement S2.5 and S6; agent guide; implementation semantics in `models/f3/loop3/murzuq_stage2.py`. No numerical analysis or literature search was repeated.

## Decision

The manuscript is **not yet a semantic pass**, but closure needs wording changes only. The source and numerical account is otherwise coherent. The abstract misidentifies 459.1 Ma as the Sandbian base rather than that base plus its quoted uncertainty. One repeated, material error describes the primary Murzuq calculation as assuming marginally independent cuttings; the model instead makes cuttings conditionally independent given a shared well frailty. A related error describes inverse-block-size composite weighting as though each block were one binary observation and sometimes calls its unqualified 0.39–0.42 contour a limit. One sentence also makes the M2 crown-to-encounter implication without stating the necessary persistence and catchment conditions.

No result, claim value, source admission or model needs to change. The minimal replacements below would close this review.

## Material findings and minimal replacements

### 1. Abstract misstates the source of 459.1 Ma

**Severity: major (headline calibration meaning).** `manuscript/text/main.md:14–16` says:

> The 459.1 Ma value is the base of the Sandbian stage, which the oldest possible and the oldest definite Swedish trilete spores give alike.

The GTS2012 Sandbian base is 458.4 Ma; the calibration value is that base plus its quoted 0.7 Myr uncertainty. The definite and possible triletes give the same value because both are Sandbian and the calibration applies the same stage-base-plus-uncertainty rule.

**Minimal replacement:**

> “The 459.1 Ma value is the GTS2012 Sandbian base plus its quoted uncertainty, which the oldest possible and the oldest definite Swedish trilete spores give alike.”

### 2. Abstract conflates conditional with marginal independence and promotes an unqualified contour to a limit

**Severity: major (headline estimand).** `manuscript/text/main.md:17–20` says:

> If cuttings are independent and delivery was equal, it limits sustained, delivered trilete encounter in that basin, mostly through later-Ordovician samples, to about a tenth of the Llandovery level; treating cuttings from one well and formation as a block loosens the limit to about 0.4.

The primary model integrates a shared Gamma(2,2) well frailty; its observation assumption is conditional independence given that frailty (`murzuq_stage2.py:57–78`). The 0.4 result uses inverse block-size weights (`murzuq_stage2.py:44–54`), not one binary outcome per block, and uses the uncalibrated `-2 log(0.05)` comparison convention. It is an unqualified composite-likelihood sensitivity, not a loosened qualified limit.

**Minimal replacement:**

> Conditional on a shared well effect, equal delivery and independent cutting outcomes given that effect, the qualified comparison limits sustained, delivered trilete encounter in that basin, mostly through later-Ordovician samples, to about a tenth of the Llandovery level. An unqualified inverse-block-size composite-likelihood sensitivity gives a contour of about 0.4.

### 3. The same dependence error recurs in the main result, Table 4, conclusion, brief and agent guide

**Severity: major as a repeated cross-product error; each occurrence is a small wording repair.**

- `manuscript/text/main.md:230–236` correctly identifies the 0.393 and 0.419 results as retrospective composite-likelihood sensitivities, but ends: “a tenth rests on treating cuttings from one well and formation as independent observations”. Replace that clause with:

  > “a tenth rests on conditional independence of cutting outcomes given the shared well frailty; inverse-block-size weighting by well–formation or well–stage support gives unqualified comparison contours near four tenths.”

  For complete terminological consistency, change “moves the constant-history limit” at line 232 to “moves the constant-history comparison contour”, and “the older record counts as about six blocks” at lines 233–234 to “the older record has total likelihood weight of about six”.

- `manuscript/text/main.md:414` says the conclusion rests on “independence of cuttings within a well” and fails if cuttings “behave as one observation (limit about 0.4)”. Replace the relevant cells with:

  > Rests on: “conditional independence of cutting outcomes given the shared well frailty”
  > Fails if: “substantial residual within-block dependence remains after the well frailty; inverse-block-size composite weighting gives an unqualified contour near 0.4”

  The sensitivity does not fit full block dependence and does not collapse each block to a binary observation, so “fails if” should remain explicitly diagnostic rather than claim that a dependence model was estimated.

- `manuscript/text/main.md:448–451` ends the M2 conclusion with “whose strength depends on treating cuttings as independent.” Replace with:

  > “whose strength depends on conditional independence of cutting outcomes after the shared well effect.”

- `manuscript/text/brief.md:32` ends “they assume each sample is independent”. Replace with the plain-language:

  > “they allow samples from the same well to share a well effect, but assume that the samples are otherwise independent.”

- `manuscript/text/for-agents.md:171–172` says “Only with independent cuttings”. Replace with:

  > “Only with cuttings conditionally independent given the shared well frailty; inverse-block-size composite weighting gives an unqualified contour near four tenths (C51).”

### 4. Supplement S2.5 overstates what the block sensitivity represents

**Severity: moderate.** S2.5 gives the correct Gamma frailty, inverse weights and unqualified status, but three phrases undo that precision:

- `manuscript/text/supplement.md:147–150`: replace “depends on independence among cuttings” with “depends on residual conditional independence among cuttings after the shared well frailty”.
- `manuscript/text/supplement.md:154`: replace “Independent cuttings, shared well frailty (as qualified)” with “Conditionally independent cuttings given shared well frailty (as qualified)”.
- `manuscript/text/supplement.md:162–164`: replace the two sentences with:

  > “Inverse block-size weights give each block unit total likelihood weight, yielding effective weights of about seven reference and six older blocks. This is a composite likelihood, not a binary observation per block, an estimated correlation or a fitted full-block-dependence model. Across the qualified conditional-independence result and this unqualified weighting sensitivity, the comparison contour moves from about a tenth to about four tenths of reference intensity.”

This preserves the useful scale comparison without interpreting the weighting device as a generative dependence model or calibrated bound.

### 5. One M2 trait-to-node implication omits its conditions

**Severity: moderate.** `manuscript/text/main.md:184–187` says that because Hooper et al.'s reconstruction makes a proximal trilete aperture modal at the embryophyte crown, “a crown older than 459.1 Ma would imply undetected trilete producers.” The inference additionally needs retention of the trait, recognisable production and presence within the Murzuq catchment; the manuscript correctly states these conditions later in Table 4 and S6.

**Minimal replacement:**

> “Under that crown-state reconstruction, and conditional on persistence, recognisable trilete production and producer presence in the basin catchment, a crown older than 459.1 Ma would imply undetected trilete encounter.”

“Encounter” is preferable to “producers” because Murzuq constrains delivered and recovered encounter, not producer abundance separately.

## Checks that pass

- **M1 fairness:** the abstract, §3.1, Supplement S4 and agent guide all state both components of the published M1 rationale: affinity below the oldest possible total-group records and the qualitative preservation-control argument. They correctly limit the criticism to the absence of an enumerated, comparably searched frame and do not call M1 simply untestable or based only on affinity.
- **M2 time geometry:** §3.2 Table 2 states sustained intensity from 459.1 Ma to the Llandovery reference; Supplement S2.2 identifies the reference boundary as 443.1 Ma. The brief states that the 28 zeros are older than about 443 Ma, and the article, supplement and agent guide all distinguish the 10 broadly dated Darriwilian cuttings in two wells that may extend before 459.1 Ma from the 18 Katian/Hirnantian zeros wholly younger than it.
- **M2 calibration outside the abstract:** §3.2, Supplement S2.4 and the agent guide correctly identify 459.1 Ma as 458.4 + 0.7 Ma under the GTS2012 stage-base-plus-uncertainty rule, and explain why the possible and definite Sandbian occurrences yield the same value.
- **What Murzuq constrains:** outside the phrases identified above, the products consistently restrict the result to local, sustained, delivered/recovered encounter and the product `rho f`; they do not infer producer abundance separately or a dated global absence. The equal-delivery producer-intensity statements are explicitly conditional.
- **0.39–0.42 status:** the detailed main result, claims ledger, Supplement S2.5 and Stage 2 agent-guide results correctly label the values retrospective, unqualified composite-likelihood sensitivities. The remaining misuse is confined to the abstract/Table 4/S2.5 “limit” or “one observation” language listed above.
- **Trait persistence:** Table 4, its following paragraph, Supplement S6 and `estimands.md` correctly state that 0.977 is conditional on coding, model, tree and chronology, is not observed survival or the fraction of extinct local producers making recognisable spores, and is not multiplied into coverage. M1 cryptospore persistence is explicitly unassessed.

## Remaining uncertainty and next decision

This review tests agreement of prose with the declared estimands and implementation; it does not independently validate the frozen numerical outputs, source transcriptions or the chosen frailty/block conventions. After the five groups of wording repairs above, a targeted semantic diff is sufficient; no rerun or broader prose revision is warranted.
