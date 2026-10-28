# Plan: first deliverable (F3 and the dataset)

Adopted 2026-10-28 (Barry, chat: "Yes, adopt it", accepting Claude's recommendation of the curated, provenance-tracked dataset plus the F3 observation model as the first deliverable). This plan was drafted by Claude Opus 5.5. It is for Barry to object to by exception: the stages below proceed without further approval except at the consult triggers.

## Endpoint

**Question.** Given how the record was preserved and sampled, when did the main early land-plant lineages arise, as judged separately from the spore and megafossil records? And are those windows consistent with the competing molecular-clock scenarios (§5.3 of the primer)?

**Why it matters.**
- **The clocks.** The three scenarios disagree by up to 65 Myr on the age of crown embryophytes (515–450 Ma), and Hooper et al.'s 2026 recalibration rests on reading a first appearance as a maximum age.
- **The method.** No study yet puts simulation-validated intervals on early land-plant first appearances (`docs/framings.md`, F3).
- **Reuse.** The observation model it needs is the one every later framing needs.

**What it delivers.**
1. **Dataset v1.** A versioned, provenance-tracked occurrence dataset for the Darriwilian–Emsian, with two channels (dispersed spores; megafossils and mesofossils), a sampling-effort layer and a record of rejected and disputed records. Every record traces to a source document and is either verified against it or flagged.
2. **Recovery study.** A simulation that shows which origination estimators recover known truth on records with this window's gaps and effort history, and with what bias and coverage.
3. **Origination windows.** For the target events below, from each channel, with uncertainty, and a verdict on consistency with each clock scenario.
4. **Papers.** A paper describing the data, a paper on the analysis, and the human–AI correspondence record. Their release is Barry's decision.

**The point at which to stop and report.** All three analytical deliverables exist and have been checked, and a short memo states what the record does and does not support. Earlier stops are listed under the consult triggers.

## Target events

These were chosen because each matches a clock calibration or a contested claim, and each has a fossil channel that can speak to it.

| Event | Channel | Bears on |
|---|---|---|
| E1 First trilete spores (total-group embryophytes on Hooper et al.'s reading) | dispersed spores | Hooper et al.'s soft maximum of 459.1 Ma on crown embryophytes |
| E2 First cryptospores accepted as embryophytic | dispersed spores | Morris et al.'s (2018) maximum of 515.5 Ma; the stasis of Ordovician cryptospores |
| E3 First polysporangiophyte megafossils (*Cooksonia* and relatives) | megafossils | Hooper et al.'s maximum of 431.2 Ma on crown tracheophytes |
| E4 First tracheids in situ | megafossils and mesofossils | the late Ludlow record (`taxa/cooksonia.md`) |
| E5 First lycophyte-line (zosterophyll) megafossils | megafossils | the minimum for crown tracheophytes |
| E6 Agreement between the channels | both | do the spore types of known producers appear in step with those producers' bodies? |
| E7 The Silurian–Devonian rise | both | how much of the apparent radiation tracks sampling effort? |

**Circularity rule.** Fossils that a clock study uses as minimum calibrations cannot test that study. E1–E5 therefore test the maxima, and the agreement between the two channels, not the minima. Each analysis lists which records are calibrations in which study.

**What logic allows.** A sampling-corrected window for when a character first arose bounds the corresponding crown from above only under the stated preservation model. That conditionality goes into every verdict.

## Stages

Each stage ends in something that can be inspected. The stages are a route, not approval gates.

**Stage 0. Data freeze v0.**
- **Spores.** Finish MVD-B on the open texts, and fold in Barry's downloads from the closed list as they arrive.
- **Megafossils.** Build the megafossil channel from PBDB, GBDB, the cards and the literature.
- **Reconcile.** Bring names, ages (stage first, per primer §1.2) and attributions into line.
- **Effort.** Build the effort layer: documents per stage and region for spores; collections and sections for megafossils.

Output: `data/occurrences/` v0, with a README and a validation report. Sol extracts and audits under the existing per-record verification rule.

**Stage 1. Sketch.**
- **Simulator.** The smallest virtual palaeontology: lineages under birth–death; one trait (the spore type); constant preservation per channel; sampled first appearances.
- **Estimators.** Marshall (1990) intervals, and the Gaussian-resampled, inverse-weighted estimator of Bradshaw et al. (2012) run in reverse for first appearances.
- **Stopping point.** It runs end to end on known truths.

**Stage 2. Ground: the recovery study.**
- **Realistic histories.** Replace constant preservation with the real effort history from Stage 0, and with preservation that depends on facies and gaps.
- **What is measured.** The bias, interval coverage and identifiability of each estimator. Of particular interest is whether an old origin with poor preservation can be told apart from a young origin with good preservation.
- **Acceptance criteria, fixed before running.** An estimator is used on real data only if, across the plausible scenarios, nominal 95% intervals cover the true origination time at least 90% of the time and its median bias is under 2 Myr.
- **Separating the two.** The acceptance criteria concern the estimators. They are not predictions about the timescale.

**Stage 3. Apply.** Run the validated estimators on the real channels for E1–E7. State each verdict as conditional on its preservation model.

**Stage 4. Enrich, one mechanism at a time, only where Stage 3 shows a discrepancy.** Candidates:
- regional structure by palaeocontinent;
- spore transport into marine settings;
- reworking and caving;
- the uncertainty in linking spores to the plants that produced them.

**Stage 5. Synthesise.** A memo, then drafts of the two papers. Barry reviews before anything is released.

## Tools and compute

- **Code.**
  - Python with `uv`, as in the existing tooling.
  - The simulator and the two classical estimators are implemented here and tested against known truths.
  - PyRate, `tbea` and StratPal serve as cross-checks only, at pinned versions. EPRP found pitfalls in each that bite on a record dominated by gaps (`data/eprp/pointers/eprp_pointers.md`): Marshall's method in `tbea` returning no upper bound; StratPal mapping wrongly above hiatuses; PyRate undercovering at low preservation.
- **Compute.**
  - Pilots run on mac-mini.
  - Recovery ensembles run on `deep-server` under `/data/codex/`, after a smoke test there.
- **Seeds and hashes.** Each run records its seeds and the data-freeze hash.

## Authority and limits

- **Proceeds without asking** (reversible): extraction, data cleaning, code, simulations, commits and pushes, and compute on `deep-server`.
- **Stays with Barry:**
  - any contact outside the collaboration, including the Wellman, Steemans and Vecoli database request;
  - any public release of data or preprints;
  - spending beyond the mesh.
- **Out of scope for this deliverable:**
  - F1/F2 mechanistic simulation;
  - phylogenetic reanalysis;
  - the carbon cycle;
  - anything later than the Emsian, except anchors.

## Consult triggers

1. **The recovery study (Stage 2) shows the record cannot tell the clock scenarios apart.** Report before Stage 3, with what would make them separable, such as more data or a narrower question.
2. **Results contradict a published calibration by more than the stated uncertainty.** Report before writing it up.
3. **A record or source would change a verdict but can be reached only through contact or purchase.**
4. **The spore–producer links prove too weak for E6.** The question then needs narrowing, and that is a scientific choice.
