# Plan: first deliverable (synthesis and F3)

Adopted 2026-10-28 (Barry, chat: "Yes, adopt it"). Revised the same day after discussion (Barry: "Yes, revise it"). Drafted by Claude Opus 5.5. The programme principles behind it are in `docs/charter.md` ("Purpose"); the questions it serves are in `docs/questions.md` (Q1–Q4). Barry objects by exception: work proceeds without further approval except at the consult triggers.

## Two contributions, two standards

**A. Synthesis.** An occurrence dataset that traces every record to its source and keeps disagreement in usable form. It covers dispersed spores, megafossils and mesofossils, Darriwilian to Emsian.

- Every adjudication is inspectable: who made it, on what evidence, and what the alternatives were.
- The effect of each contested reading on the pattern is measured (the pivotal-records analysis below).
- Another researcher can follow the route from specimen and publication to any conclusion.

**B. Statistics (F3).** When did the main early land-plant lineages arise, judged from each record channel with sampling corrected for? And are those windows consistent with the competing clock scenarios (primer §5.3)?

- Estimators are used only after they have passed the recovery study.
- Every verdict is conditional on a named preservation model and a named reading of the data.
- A demonstrated limit counts as a result: what the record cannot tell apart, together with the observation that would resolve it.

Testing old narratives is a third contribution, and a programme-level one (Q5 in `docs/questions.md`). This deliverable feeds it whenever an adjudication finds that a widely repeated claim was never re-checked against its source. The Lochkovian "first tracheids" corrected on 2026-10-28 is the model case.

## Data model: observations, interpretations, readings

- **Observation.** What one source reports, recorded as stated:
  - the taxon as reported;
  - the specimen or assemblage;
  - the locality and horizon;
  - any measurement;
  - where in the source it appears (page, figure or table);
  - the source itself;
  - whether it has been checked against the source text.
- **Interpretation.** One or more for each observation, each with its source and its author (a paper, or the adjudicator: Claude, Codex or Barry):
  - identity, with revision history;
  - affinity, meaning spore class or producer group;
  - age: the stage assignment and its basis, kept apart from any numerical evidence (primer §1.2);
  - status: accepted, disputed or rejected.
- **Reading.** A named set of choices, one interpretation per contested observation. Each analysis declares its main reading before it runs; the other readings are sensitivity analyses. This guards against results that change with whichever reading is chosen.

`data/spores/` already does this crudely, with a strict and an inclusive set. Loop 1 generalises it, and builds the megafossil channel the same way. Card front matter stays the modelling summary; the occurrence data carry the alternatives.

## Target events

| Event | Channel | Bears on |
|---|---|---|
| E1 First trilete spores (total-group embryophytes on Hooper et al.'s reading) | dispersed spores | Hooper et al.'s soft maximum of 459.1 Ma on crown embryophytes |
| E2 First cryptospores accepted as embryophytic | dispersed spores | Morris et al.'s (2018) maximum of 515.5 Ma; the Ordovician cryptospore stasis |
| E3 First polysporangiophyte megafossils (*Cooksonia* and relatives) | megafossils | Hooper et al.'s maximum of 431.2 Ma on crown tracheophytes |
| E4 First tracheids in situ | megafossils and mesofossils | the late Ludlow record (`taxa/cooksonia.md`) |
| E5 First lycophyte-line (zosterophyll) megafossils | megafossils | the minimum for crown tracheophytes |
| E6 Agreement between the channels | both | do the spore types of known producers appear in step with those producers' bodies? Only where the producer link holds |
| E7 The Silurian–Devonian rise | both | how much of the apparent radiation tracks sampling effort? |

**Circularity rule.** Fossils that a clock study uses as minimum calibrations cannot test that study. E1–E5 test its maxima, and the agreement between channels; never its minima.

**What logic allows.** A sampling-corrected window for a character's first appearance bounds the corresponding crown from above only under the stated preservation model.

## Loop 1: narrow and fast

1. **The tail and its disputes.** For E1–E5, assemble every record older than the oldest undisputed record of the event, plus one stage beyond it. Give each its interpretations and alternative readings. Add the effort layer:
   - spores: documents per stage and palaeogeographic unit (Palynodata and the post-2006 extraction);
   - megafossils: collections and sections (PBDB and GBDB).

   The contested records already known include the Dalby "trilete" spores, the Swedish Sandbian spores, the Argentine Dapingian cryptospores, Zbrza, the Ordos preprint, the age of the Yea *Baragwanathia* beds and the attribution of the Ludlow tracheid axes (`docs/rejected-records.md`; cards).
2. **Sketch.** The smallest virtual palaeontology: lineages under birth–death, one trait (spore type), constant preservation in each channel, and sampled first appearances. The estimators are Marshall (1990) intervals and the Gaussian-resampled, inverse-weighted estimator of Bradshaw et al. (2012), run in reverse for first appearances. Both are checked against known truths.
3. **Recovery study.**
   - **Conditions.** The real effort history, with preservation that depends on facies and gaps.
   - **Measures.** Bias, coverage and identifiability. In particular: can an old origin with poor preservation be told apart from a young origin with good preservation?
   - **Acceptance, fixed before running.** An estimator is used on real data only if its nominal 95% intervals cover the true origination time at least 90% of the time across the plausible scenarios, with median bias under 2 Myr.
   - **Not a prediction.** These criteria are about the estimators, not about which timescale is right.
   **Amendment after the sketch** (2026-10-28, Claude Opus 5.5; recorded before any real data were analysed). The sketch (`models/f3/README.md`) found:
   - **Classical intervals.** Marshall (1990) and Strauss & Sadler (1989) give the same one-endpoint bound. It covers the true origination 94–95% of the time under its own assumptions. When abundance ramps up after origination (logistic or birth–death growth), coverage falls to 4–81% and the median bias runs from 2 to 27 Myr too young. The bias is of the same order as the disagreement between the clock scenarios.
   - **GRIWM.** Its point estimate lies older than the truth in only 64–81% of replicates, even under uniform sampling. Its interval reflects dating error only.
   - **A fault in the authors' code.** The arrival option of the published GRIWM code (`signor_lipps = "arr"`, `Rextinct/R/griwm.R`) returns an estimate slightly younger than the oldest record. The sketch therefore uses the extinction algorithm on a mirrored age axis. Reporting the fault to the authors is Barry's decision.

   The step changes as follows. The original criteria stand for interval estimators.
   - **New estimators.** The recovery study adds estimators that model the abundance ramp and preservation: likelihood or Bayesian fits of an occurrence process with growing intensity, and birth–death with preservation, cross-checked against PyRate. A clade that starts rare is the expected case for early land plants.
   - **Point estimators.** GRIWM and the Strauss & Sadler point are judged on median bias under 2 Myr and on an interval calibrated by simulation.
   - **One classical estimator.** Only one classical bound is carried.
   - **Boundary ages.** These are drawn from the joint age model, not fixed.
   - **The deciding question.** Whether the ramp itself can be estimated from two channels plus effort is the identifiability question, and so the first thing the recovery study answers.
   **Second amendment, adopted after the recovery study** (2026-10-28, drafted by Claude Opus 5.5; adopted by Barry, chat, 2026-10-28: "Yes, agreed, adopt it"; recorded before any real data were analysed). The recovery study (`models/f3/README.md`, step 3) found the following:
   - **No estimator meets the original criteria** across the plausible scenarios. The classical bound and GRIWM fail every ramp.
   - **The capacity-profiled logistic fit covers but sits young.** Its 95% interval covers the true origination in 119 of 120 logistic scenarios, but its maximum lies 0.2–7.5 Myr young of the truth. Its older limit covers 93–98% of the time under logistic growth and 81–88% under birth–death growth.
   - **Exponential growth leaves an exact trade-off** between preservation and origination. Only empty but well-sampled older stages bound the origination. With the data starting at the Darriwilian, older originations cannot be identified at all.
   - **Record counts.** About 100 spore records bound origination to within a few Myr under a logistic ramp. About 30 body-fossil records do not.

   Changes:
   1. **Older limit.** Judge and report the **older limit of the interval**, the quantity a test of a clock maximum needs. An estimator passes a scenario if that limit covers the true origination at least 90% of the time. Point estimates are not reported as findings, and the bias criterion applies only where one is.
   2. **Informativeness.** An interval counts only if its profile is bounded within the search range in at least 90% of replicates. Otherwise the result for that scenario is "not identifiable", stated with the evidence that would resolve it. This closes the loophole by which an unbounded interval "covers" trivially.
   3. **Estimators.** The primary estimator is the logistic fit with capacity profiled (`ramp_logistic_kfree`), stated as conditional: "if abundance rose logistically …". The fixed-capacity logistic and birth–death fits are sensitivity checks. The classical bound and GRIWM are reported only as the naive view.
   4. **Extend the spore effort and tail back through the Cambrian.** The window edge makes old originations unidentifiable, and the test of the 515–493 Ma scenarios depends on documented palynological sampling without spores before the Darriwilian. The Tremadocian–Dapingian effort is added (2026-10-28). The Cambrian needs the full Palynodata release (`data/external/local/spores/of_5793.zip`).
   5. **Robustness next.** Before any real-data verdict, test the primary fit against effort series that are wrong by plausible amounts.
   6. **Body-fossil events (E3–E5).** These have too few records for any estimator to pass under a ramp. Report their intervals with that caveat, and rest their verdicts mainly on the pivotal records.

   These changes narrow the claim from "origination windows" to "sampling-based older limits on origination, conditional on the shape of the rise", the quantity the clock-maximum tests require. The original criteria are kept above for the record.
   **Shape of F3 after the second amendment** (proposed 2026-10-28, awaiting Barry): `docs/f3-shape.md` proposes testing the fossil-absence maxima behind the clock results with an abundance envelope over the empty, sampled stages, and moving E4–E7 out of the statistical contribution. If adopted, it replaces the event table's statistical roles and steps 4–5 below.
4. **Apply and find the pivotal records.** Run the accepted estimators on each event under its main reading. Then repeat across the readings of the contested tail. A record is **pivotal** if its reading flips a verdict (for example, compatibility with a clock maximum) or moves the estimated window by more than 1 Myr. The output is a short list of the adjudications that decide each answer, with what each reading implies.
5. **Value of information.** Rank the evidence that could still be obtained by how much it would narrow an answer, rerunning with each item resolved each way. Candidates:
   - a closed paper;
   - a re-dated section;
   - a specialist adjudication;
   - a dataset obtainable only through contact.

   The ranking updates `docs/questions.md`, the closed-literature list and the leads register.
6. **Close the loop.**
   - A memo: what holds under every reading, what depends on which records, what the record cannot tell apart, and the observation that would settle it.
   - A structural-review entry in `docs/decisions.md` (below).

## Later loops

Each later loop broadens the evidence where the value-of-information ranking points, not towards completeness for its own sake. The full dataset (v1) builds up across loops. Mechanisms are added one at a time, and only where results disagree with the data:

- regional structure by palaeocontinent;
- spore transport into marine settings;
- reworking and caving;
- uncertainty in which plants produced which spores.

The pivotal records are where specialist palaeobotanical judgement matters most, and where outside input would count for most.

**Experts are never a blocker** (Barry, 2026-10-28). Specialists may be unreachable, inactive or unresponsive. Where contact is worth trying, flag it with the question to ask; whether to send it is Barry's decision. The work always proceeds on the published record and the databases, carrying the contested readings as alternatives. A reply, if one comes, updates a reading; waiting for one never holds up a stage.

## Outputs

- **Dataset release** with a descriptor, and an analysis paper. Release is Barry's decision.
- **The human–AI correspondence record.**
- **The two kinds of novelty, kept apart.** The enabling novelty (scale and verification, evidenced by the audit records) is reported apart from the scientific findings.

## Tools and compute

- **Code.**
  - Python with `uv`.
  - The simulator and the two classical estimators are written here and tested against known truths.
  - PyRate, `tbea` and StratPal are used only as cross-checks, at pinned versions. EPRP found faults in each that bite on a gap-dominated record (`data/eprp/pointers/eprp_pointers.md`).
- **Compute.**
  - Pilots run on mac-mini.
  - Recovery ensembles run locally (10 cores) or on `nectar-vm` at `c3.large` (8 vCPU) under `/data/codex/silurian_plants/`, after a smoke test. `deep-server` has been unreachable since 2026-10-28.
  - Each run records its seeds and the data hash.

## Authority and limits

- **Proceeds without asking** (reversible): extraction, adjudication, code, simulations, commits and pushes, and compute on the mesh hosts Barry has made available (`nectar-vm`; `deep-server` when reachable).
- **Stays with Barry:**
  - any contact outside the collaboration, including the Wellman, Steemans and Vecoli database request and any approach to specialists over the pivotal records;
  - public release;
  - spending beyond the mesh.
- **Out of scope for this deliverable:** F1/F2 simulation, phylogenetic reanalysis, the carbon cycle, and post-Emsian records other than anchors.

## Consult triggers

1. **A result contradicts a published calibration by more than the stated uncertainty.** Report before writing it up.
2. **A pivotal record turns on specialist judgement this team cannot make with confidence.** Flag whom to ask and what to ask, then continue with both readings carried forward.
3. **Evidence with high value of information can only be had by contact or purchase.** Flag it, and continue without it.
4. **The producer links prove too weak for E6, so the question has to be narrowed.**

None of these triggers pauses the work; each is a flag for Barry. If the record cannot tell the clock scenarios apart, that is not a trigger either. It is a result, reported at the loop's close together with the observation that would resolve it.

## Structural review at each loop's close

A short entry in `docs/decisions.md`:

- Does the repository's structure serve the next investigation as well as this one?
- Which assumptions did the work expose?
- Did any evidence change a question in `docs/questions.md`?
