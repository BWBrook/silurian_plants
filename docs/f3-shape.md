# The shape of F3 after the recovery study

Proposal by Claude Opus 5.5, 2026-10-28, at Barry's request after he adopted the second amendment (chat, 2026-10-28: "Yes, agreed, adopt it. Then let's re-assess the full shape of F3 given this constraint"). **Status: proposed, awaiting Barry's decision.** Nothing here has yet been applied to real data. It changes the statistical question of `docs/plan-f3.md`, not the synthesis.

## The constraint

The recovery study (`models/f3/README.md`, step 3) and the second amendment leave three facts.

1. **Only the older side of an origination interval is defensible**, and only conditionally. If abundance rose logistically, the capacity-profiled fit's older limit covers the true origination 93–98% of the time; under birth–death growth, 81–88%. Point estimates sit up to 7.5 Myr young and are not findings.
2. **An old origination is never excluded outright.** Under exponential growth, preservation and origination trade off exactly. Only stages that were well sampled and yielded nothing bound an origination, and the binding is always "unless the lineage stayed rare enough".
3. **About 30 body-fossil records cannot carry an estimator-based verdict** under the ramps tested. About 100 spore records give bounded but broad older limits (median widths of 24–45 Myr at mid preservation in the Darriwilian–Sandbian window), given effort back through the empty stages.

## What follows

Three consequences shape the question.

- **Compatibility can be robust; incompatibility cannot.** A slower rise only makes early absence easier to explain. So an origination that the record allows at constant abundance is allowed under every ramp, while an older one is excluded only under a named ramp. The record can therefore say two different kinds of thing about a scenario: "allowed whatever the rise" or "requires a cryptic phase of this depth and length".
- **The natural target is a fossil-absence argument, and the clock maxima are fossil-absence arguments.** Every maximum F3 was to test rests on the assumption that a lineage would have been preserved and sampled soon after it arose (primer §5.3, assumption 2). That is exactly the quantity the recovery study shows we can measure: what an absence in sampled stages licenses. The posteriors of Hooper et al. (2026) sit against their maxima: crown embryophytes 457–450 Ma under a 459.1 Ma soft maximum, crown tracheophytes 432–428 Ma under 431.2 Ma (primer §5.3; `taxa/baragwanathia-brevifolioides.md`). Whether those maxima are justified by sampling decides whether the young timescale is a finding or an input.
- **Testing the maxima avoids the circularity that testing the posteriors would carry.** A posterior already contains the fossils that set its bounds. The maximum is an input with a stated tail probability (Hooper et al.: 2.5% of being exceeded), and a tail probability can be checked against sampling.

## Proposed question

**Do the fossil absences that set the land-plant clock maxima survive correction for sampling?** For each maximum: is it justified at its stated tail probability, overconfident by a measurable amount, or not identifiable from the record, with the observation that would decide it.

| Maximum | Used by | Bounding fossil (the oldest record that is not absent) | Channel | Event |
|---|---|---|---|---|
| M1: 515.5 Ma on crown Embryophyta | Morris et al. (2018); Su et al. (2021), strategy 1 | Cambrian cryptospore-like palynomorphs | spores | E2 |
| M2: 459.1 Ma, soft, on crown Embryophyta | Hooper et al. (2026) | the oldest possible trilete spores, Dalby Limestone, Sweden | spores | E1 |
| M3: 431.2 Ma, soft, on crown Tracheophyta | Hooper et al. (2026) | *Cooksonia* cf. *pertoni*, Homerian, in Hooper et al.; *C. barrandei*, mid-Sheinwoodian, c. 432 Ma, in our main reading | megafossils | E3 |

For each maximum the deliverable has four parts:

1. **The bounding record and the contested tail beneath it, adjudicated** (contribution A, with every alternative reading kept).
2. **The abundance envelope** (method below): for every older stage, the highest abundance, relative to a named reference level, that is compatible with finding nothing, given the documented effort.
3. **The cryptic phase each scenario requires.** For an origination at time *T*, the greatest mean relative abundance *f\**(*T*) the lineage could have held from *T* to its first appearance. "A crown-embryophyte origination at 515 Ma requires embryophyte spores to have stayed below *x*% of their Katian frequency per document for 50 Myr" is the form of the answer.
4. **The older limit under named rise models**, logistic (primary, as amended) and birth–death, and the probability they place beyond the maximum, compared with its stated tail.

Minima are not tested (circularity rule). They enter as adjudications: the Bathurst Island *Zosterophyllum*, the Yea *Baragwanathia* beds, and *Cooksonia* cf. *pertoni*.

## The abundance envelope

Each document (spores) or collection (bodies) in stage *s* detects the spore type or body type with rate *r*·*a*ₛ, where *a*ₛ is the lineage's mean abundance in that stage relative to a reference stage, and *r* is the per-document detection rate observed in the reference stage. With effort *E*ₛ, finding nothing in every stage before the first appearance has probability exp(−*r* Σ *E*ₛ *a*ₛ). At 95%, Σ *E*ₛ *a*ₛ ≤ 3.0/*r*. Every origination is compatible with the record if abundance stayed beneath that envelope; the logistic and birth–death fits are two trajectories tested against it.

The envelope is the non-parametric form of the identifiability result: it uses exactly the empty, sampled stages that the study showed are the only source of information. Its assumptions are few and explicit: Poisson detection, a detection rate per unit abundance that does not change between the reference stage and the empty stages, and correct effort. Each can fail, and each failure is tested before any verdict (next section). Two choices are fixed before it touches real data: the reference stage (the first stage after the first appearance with at least a set number of documents, with the uncertainty of *r* carried through), and the stage-exposure rule for an origination inside a stage.

## Threats, each tested on simulated data before any verdict

1. **Mismeasured effort** (the amendment's item 5): effort wrong by a constant factor, and by stage-specific factors.
2. **Reporting bias.** Palynodata indexes what a paper names, and a paper on acritarchs may not report spores. Calibrate the propensity to report spores where they are known to be present (Katian to Wenlock), by document type, and test a lower propensity in the Cambrian and Early Ordovician, where authors may not have looked for land-plant spores. Terminology compounds this: older work would have called spore-like remains of this age "leiospheres" or "alete spores" (Strother & Foster 2021, supplementary text), so a search on spore names alone can miss them. Missing effort makes the envelope looser, which is conservative; effort that could not have detected spores makes it tighter, which is not.
3. **Facies.** Land-derived spores thin offshore. Repeat with effort restricted to nearshore and marginal lithologies.
4. **Regional confinement.** A lineage confined to one palaeocontinent is not tested by sampling elsewhere. Compute the envelope for each palaeogeographic unit and for the unit of first appearance alone.
5. **Affinity.** What counts as an embryophyte spore decides where E2's first appearance sits (entry 10 of `docs/rejected-records.md`). The Cambrian charophyte-grade palynomorphs also act as a positive control: their recovery shows that the preparations would have kept sporopollenin-walled spores.
6. **Dating of the effort.** Palynodata's age names, crosswalked with a confidence grade (`data/spores/crosswalks/age_names.csv`); repeat with high-confidence documents only. The effort table counts a document in every stage its range overlaps, so a "Middle Cambrian" paper counts four times; the envelope needs each document apportioned across its range (a document is one trial whose detection rate is the mean abundance over its range). Documents dated only "Early Cambrian" (32 Myr) are dropped by the 25 Myr rule and should be brought back the same way.

## What each event becomes

| Event | Before | Proposed |
|---|---|---|
| E1 trilete spores | origination window; tests M2 | the M2 test (primary result) |
| E2 cryptospores | origination window; tests Morris et al.'s maximum | the M1 test, with the affinity of the Cambrian forms as the pivotal reading |
| E3 polysporangiophyte bodies | origination window; tests M3 | the M3 test; the envelope may show the body record cannot justify M3, which is itself the result |
| E4 tracheids in situ | origination window | synthesis only: an adjudicated tail and a Q5 case. Tracheid preservation needs rare mesofossil facies, whose effort cannot yet be measured |
| E5 lycophyte-line bodies | minimum for crown tracheophytes | synthesis only: the minimum calibrations adjudicated (Yea, Bathurst Island) |
| E6 channel agreement | statistical event | parked under Q4 until the producer links are scored (consult trigger 4) |
| E7 the Silurian–Devonian rise | statistical event | moved to Q3, in a later loop with its own estimand and recovery test |

## What this gives up and what it gains

- **Given up:** origination windows and point estimates; E4, E6 and E7 as statistical results in this deliverable.
- **Gained:**
  - a question the record can answer, with the answer's conditionality in its units (a depth and length of cryptic phase), not hidden in a model choice;
  - a direct bearing on why the clock results disagree: the young timescale (Hooper et al.) and the old (Morris et al.; Harris et al.) use the same kind of molecular data under different calibrations, the maxima prominent among them (Q9 asks how much of the 55 Myr shift each choice explains);
  - no circularity, because inputs are tested, not outputs;
  - a method that applies to any fossil-absence maximum in any clade, which suits the programme's purpose as a demonstration (charter, "Purpose").

It remains F3: whether the record, read through a preservation model, supports the competing timescales. The test now targets where the timescales get their bounds.

## Where the evidence stands (2026-10-28, before any estimator)

- **M2 (E1, trilete spores).** First appearance: certain Katian, possible Sandbian (Borenshult and Dalby, contested). Below it, palynological documents per stage: Darriwilian 572, Dapingian 500, Floian 405, Tremadocian 418, then about 175–185 per Middle and Late Cambrian stage (Palynodata to 2006; counted in every stage a document overlaps). Cryptospores are present from the Darriwilian, so the preparations were recovering sporopollenin-walled spores in those stages: a positive control. Every pre-Katian trilete report checked so far is rejected or doubtful, the Cambrian ones included (`data/spores/crosswalks/doc_vetting.csv`). This looks like the most informative test.
- **M1 (E2, cryptospores).** First appearance: certain Darriwilian (Hanadir, now checked in full text), possible Dapingian (Saudi Dp1; the Argentine record is disputed at specimen level, rejected-records entry 16). The Cambrian cryptospore-like palynomorphs (Laurentia; Kaili Formation, South China) are a positive control under the main reading and the event itself under the inclusive one. Effort reaches back to about 506 Ma. Testing a 515.5 Ma origination needs the Early Cambrian papers, which the dating rule now drops; apportioning their effort (threat 6) would bring them back.
- **M3 (E3, polysporangiophyte bodies).** First appearance under the main reading: *C. barrandei*, mid-Sheinwoodian, about 432 Ma (Libertín et al. 2018), which lies slightly older than the 431.2 Ma maximum that Hooper et al. set from the Homerian *C.* cf. *pertoni*. Zbrza (Hirnantian) is the pivotal alternative, and the Bolivian *Cooksonia* now counts. Body effort before the Sheinwoodian is 18–70 land and marginal PBDB collections per stage. Whether that can justify any maximum is what the envelope will show.

## Sequence

1. Re-adjudicate the pivotal records against the papers Barry obtained. Done 2026-10-28 (`docs/decisions.md`).
2. Extend the effort layer through the Cambrian. Done 2026-10-28, apart from apportioning documents across their age ranges.
3. The robustness tranche: threats 1–6 on simulated records with the real effort history.
4. Apply, in the order M2, M1, M3.
5. Value of information and the loop's close, as in `docs/plan-f3.md`.
