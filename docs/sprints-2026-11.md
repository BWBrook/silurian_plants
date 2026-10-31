# Two sprints towards Loop 1's empirical answers

**Revision v2**, Codex, 31 October 2026, responding to Claude Opus 5.5's draft
and Board 2678. Codex agrees the sequential pairing with the revisions below;
Claude's acceptance is recorded when it starts sprint 1 against this version.
Barry's instruction (chat, 2026-10-31): "you and Codex agree on two sprints that
would substantively advance the work, after which you will counter-review each
other's work, in a follow-up handshake."

Execution order: Claude drafts; Codex revises; Claude executes sprint 1; Codex
executes sprint 2; Claude reviews/fixes sprint 2; Codex reviews/fixes sprint 1;
then both reconcile. Each execution includes its own independent check. The
later counter-reviews remain separate from those checks.

## Outcome and division of work

Sprint 1 delivers an executable, qualified M2 analysis on admissible real designs,
plus explicit diagnoses for designs that cannot support it. Sprint 2 uses that
pipeline for a bounded M1 source programme and an M3 evidence/identifiability
assessment. It also produces the combined draft results and value-of-information
memo, ready for counter-review. A numerical exclusion is not a completion criterion.

The engine has synthetic validation evidence; this does not qualify a new age,
contamination, dependence or observation model. The seven existing candidate
frames and the Libya mapping are available; none is yet an analysis-ready binary
frame. The design declarations and simulator must make that transition explicit.

Sequential dependency is useful for the numerical pipeline. Source assessment,
reporting maps and the M3 evidence assessment remain modular: sprint 2 can complete
these even if sprint 1 finds no qualified design. It must not inherit an unsupported
pipeline assumption merely to produce a number.

## Shared execution and scientific rules

- **Authority.** Complete the owned sprint autonomously: source work, adjudication,
  code, analyses, checks, commits and pushes. Cross-ownership edits are allowed
  during sequential execution and logged for review. Preserve raw source reports
  and frozen inputs; corrections create traceable revisions. No simultaneous edits
  to shared files. External contact, publication and spending beyond authorised
  resources remain Barry's decisions. The consult triggers in `plan-f3.md` are
  flags, not general stop gates; continue unaffected work and declared alternatives.
- **Design freeze.** Commit each complete roster of candidate designs and readings
  before its first numerical screen. Record units, reference and first-appearance
  rules, classes/transport, age model, dependence, contamination, eligibility,
  binary conversion, targets, nuisance scenarios and the exact screening rule.
  These are prospective analysis declarations after source inspection, not claims
  of outcome-blind preregistration. Record which outcomes were already known.
- **Selection.** Report every declared design, reading and sensitivity, including
  inadmissible or unqualified ones; do not retain only the favourable variants.
  Map designs to the seven existing source frames. Sprint 2 may add frames through
  its predeclared source-search roster and admission rule, with a dated extension
  to `f3-shape.md`'s roster. Source inventories and analytical combinations are
  different objects. Qualify the actual reporting/selection procedure; overlapping
  samples and data-dependent variant choices need their joint procedure represented.
- **Contract.** Keep 0.955 empirical calibration, 0.95 nominal coverage and the
  independently assessed 0.93 floor distinct. Preserve the existing two-stage
  acceptance rule; stage 2 is the prescribed follow-up, not an automatic replacement
  for stage 1. For each required cell/batch, target 1,000 passing replicates, with a
  total cap of 20,000 attempts. Calibration and acceptance use separate seeds;
  stage 2 adds its independent batch and follows the declared pooled decision rule.
  Log all attempts, passes, failures and exclusions. Simulate the same first-
  appearance, reference, eligibility, screening and fitting procedure used on data.
  Numerical failures after passing stay in the acceptance denominator as failures;
  they are not replaced with successful draws.
  The cap is administrative: hitting it means qualification incomplete under this
  budget, not biological non-identifiability. Amendments are committed with reasons,
  and affected downstream evidence is invalidated and rerun; no post-result tuning
  with the same acceptance seeds.
- **Resources.** Moderate work runs on mini; heavy qualification on Nectar under
  its current control-plane instructions, after a target smoke/timing run. Use
  c3.3xlarge for the heavy tranche, BLAS one thread under pools, and restore
  c3.large after collecting verified outputs. Record the estimated workload before
  launching the full grid. Outside replies and new purchases are not dependencies.
- **Evidence.** Each handoff includes declarations, code/input hashes, environment,
  seeds, attempt/pass ledger, immutable calibration and acceptance receipts,
  source-to-outcome links and rerun commands. A fresh bounded reviewer independently
  checks central scientific and integrity claims. Routine computational legwork may
  use Codex delegates; the later Claude/Codex counter-review supplies the cross-system
  challenge. Report findings to Barry and the Board at handoff; flag a material
  mid-sprint change when needed, without imposing a handoff after every small step.

## Sprint 1 — Claude: M2 and the reusable real-design pipeline

**Completion:** every declared M2 design has a source-admission decision and a
numerical qualification/result status where applicable; at least one complete
real-design path through the adapter and pipeline is exercised. Deliver the M2
result note, reusable interface and a known-answer handoff example. A demonstrated
source or identifiability limit is acceptable; an unresolved software defect is
reported as incomplete software, not relabelled a scientific result.

### 1. Close admission and freeze designs

H2 is ready for this bounded admission step, not for immediate binary fitting.
Use the completed thesis mapping; no new source-acquisition campaign is required.
Establish event-wide reporting and productivity eligibility consistently in older
and reference material. Keep unresolved identities and unknown reports outside
binary conversion, with their exclusions and effects visible.

Declare the following comparison roster, allowing explicit non-admission:

- **H2 within well.** Eight younger cuttings and 17 Hawaz entries are mapped.
  There is no younger core reference within H2. A separate free core rate is
  therefore unsupported: show the supported cutting-class comparison and a
  separately labelled core/cutting transport scenario if scientifically justified.
  Freeze the minimum-reference support rule before screening.
  Do not silently calibrate cores with the cutting rate. The two unspecified
  appendix types require an explicit material-type reading or exclusion.
- **Libya core-only across wells.** Preserve the 7287-ft prose/chart conflict as
  distinct report interpretations. A chart blank does not negate a specific prose
  specimen by default. Compare support with that specimen accepted versus treated
  as unresolved; admit a zero only if the reporting rule independently warrants it.
  State cross-well/facies transport and reference support in each case.
- **D1 and I3.** Assess without prejudging failure. Preserve missing productivity
  links, the I3 Cr3 conflicts and possibly caved Ash Shabiyat recoveries. A scientific
  exclusion is distinct from an incomplete source mapping.
- **Qusaiba plus Borenshult.** Declare a cross-region/core reference-transport
  scenario, including the support for its rate ratio or sensitivity range. Apply
  the same target identification and reporting definition on both sides.
- **Borenshult alone.** Carry the prior scoped screen result as historical evidence.
  Recompute only if the chosen design or current pipeline changes its assumptions.

Record all seven source frames' disposition, including those not admitted to these
M2 comparisons. No eligible frame is forced to supply a numerical result.

### 2. Implement only the extensions these designs require

The engine already has class rates and cluster structure. Inspect and reuse that
support; extend the adapter, joint-age integration and simulator where required.

- A single well does not estimate a population distribution of well effects.
  Declare externally supported dependence parameters or a transparent sensitivity
  grid; do not fit an unconstrained cluster variance from one well.
- Caving can move younger material into a deeper cutting. A potentially caved
  positive cannot securely fix the indigenous first appearance at the cutting's
  depositional age. Use an explicit uncertain-origin/contamination observation
  model with justified sensitivity values, or a clearly conditional no-caving
  scenario plus an unresolved/excluded-observation alternative. Excluding a
  detection alone must not leave an artificial negative behind. Do not estimate
  a caving fraction from these ambiguous positives without identifying information.
- Shared formation/boundary uncertainty differs from identical sample ages.
  Use an ordered within-section model conditional on shared boundaries, retaining
  stage/zone conflicts. Coarse alternative allocations can bracket missing geology;
  an arbitrary uniform allocation is a stated scenario, not recovered chronology.
  Matching formation names across wells do not establish synchronous boundaries.
- Keep source tables separate from generated binary inputs. Every generated row
  traces to a source report, material key, named reading and versioned rule.

Test material failure modes and limiting cases, including unsupported class rates,
contamination, chronology and selection. Re-scoring old saved rows checks the
checker; targeted reruns are also required when estimator/simulator behaviour
changes. Old synthetic receipts do not certify new observation-model features.

### 3. Screen, qualify and report

Screen under each declared structure using the engine where the homogeneous
shortcut is inapplicable. Define the screen independently of the newly tuned
critical-value shift, or otherwise predeclare a non-circular selection/calibration
procedure. Freeze the simulator and nuisance grid before calibration; qualify the
same returned bounds/sets and conditional selection used empirically.

For qualified designs, report f*(T), origin sets at f in {1, 0.1, 0.01}, and the
459.1 Ma comparison under each named history class/reading. Keep the three layers:
encounter intensity, conditional biological translation, and fossil-to-node
implication. Retention scenarios remain alongside the result, not multiplied into
it. Distinguish finite, ceiling-limited, unbounded and zero-exposure states from
source inadmissibility, numerical failure and qualification-budget exhaustion.

Deliver `docs/audits/` result/audit records and update Q1/Q2/Q5. Pivotal-record
claims identify whether a reading changes admission, reference support or a
qualified verdict. The pipeline handoff must specify its input schema, unsupported
cases, validated settings, receipts and smoke-run example, so sprint 2 can start
without another design negotiation. No new ASR or clock reanalysis is required.

## Sprint 2 — Codex: bounded M1 analysis and M3 evidence limits

**Completion:** a reconciled M1 frame-admission ledger and, wherever support permits,
a qualified 515.5 Ma/E2 analysis; an M3/431.2 Ma/E3 denominator assessment; and a
combined draft result/limit and value-of-information memo. Do not promise that
complete pre-Darriwilian frames exist before inspecting their primary reporting.

### 1. Freeze and execute a bounded source roster

Use held material first. Register the exact publications, supplements and source
identifiers before detailed extraction, ranked by recoverable complete inventory,
event reporting and older/reference support, not by target detections. Cover:

- the held Cambrian studies (Strother 2016; Wang et al. 2022), checking their actual
  specimen/sample grain and whether E2 applies under the declared readings;
- the Argentine Dapingian studies (Rubinstein et al. 2010, 2011), with the
  identification dispute and duplicate material preserved;
- the existing Saudi, Paraguay and Samphire candidate sources and their known
  completeness/access limitations.

The full Palynodata release is a literature/search and coverage inventory, not a
complete processed-sample inventory or a source of E2 zeros. Use it to locate and
contextualise the roster. Add a source only through a logged completeness/support
criterion; do not undertake an unbounded Cambrian literature census. For each
roster item, finish with a mapped admissible frame or a precise missing-field/source
limit. Do not hold the sprint open for unavailable primary texts or expert replies.

E1 reporting/productivity rules do not automatically certify E2: audit the target
category, preparation and non-target eligibility for embryophytic cryptospores.
Retain geographic, stratigraphic and temporal gaps; distinguish constraints on
intensity in sampled intervals from statements about continuous absence since
515.5 Ma.

### 2. Apply the pipeline where supported

Freeze the complete M1 design/reading roster, then screen and qualify under the
sprint-1 interface and contract. Check the handoff example and the source-to-input
mapping before large runs. Local adapter or implementation repairs are authorised;
log them and invalidate/requalify affected results. A changed estimand, observation
model or acceptance rule requires a declared scientific amendment, not silent reuse
of a prior receipt. If no design is admissible, deliver the evidence-supported
limit and conditional sampling scenarios rather than manufacturing a denominator.

### 3. M3: audit denominators before a numerical screen

PBDB/GBDB collections and the held literature identify candidate deposits and
specimens. Omission of plant records from a database collection is not a searched
negative. Seek a declared section/bed/material inventory with positive and negative
reporting and compatible reference opportunities. Re-examinations and publication
counts are not new trials. Screen with the engine only after these requirements
are met; otherwise document the precise missing denominator. Do not transfer
palynological rates or productivity eligibility to compression fossils. Select
preservation-relevant facies independently of E3 detection and audit megafossil
search/reporting scope. Any proposed number of additional
collections is conditional on explicit detection, facies, age and dependence
scenarios, not an empirically estimated requirement without rate support.

### 4. Assemble the draft synthesis

Combine M2, M1 and M3 results and limits, preserving their different targets and
qualification status. Rank further evidence by the specific uncertainty or verdict
it could resolve; use conditional sensitivity calculations where support permits.
Update Q1/Q2/Q5 and AI roles. A clear negative answer about available information
counts as progress; numerical failure or unfinished source work stays labelled as
such. No public release occurs in these sprints.

## Counter-review and reconciliation

Claude reviews/fixes sprint 2, then Codex reviews/fixes sprint 1, with cross-ownership
changes checked first. Each independently reconstructs at least one decisive
source-to-outcome mapping and reruns one empirical result and its binding
qualification where such a result exists. If none exists, reproduce the decisive
non-admission/non-identifiability evidence instead. Review central contamination,
class-transport, age and selection assumptions, not just test counts.

Corrections carry input/code/result hashes and a ledger of downstream invalidation.
A sprint-1 repair that affects sprint-2 results triggers the corresponding reruns
and review before reconciliation. Do not retain an earlier conclusion merely
because it passed the earlier review.

The reconciliation delivers Loop 1's close memo: what holds across declared
readings, what depends on them, what cannot be identified, material unresolved
implementation limitations, the ranked evidence that would change the answer,
and a structural-review entry. Record adopted decisions separately from reviewer
proposals. Bring material disagreements to Barry with both positions; proceed
within the agreed scientific envelope without routine approval requests.
