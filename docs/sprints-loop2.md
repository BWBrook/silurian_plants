# Loop 2: preservation, independent replication and a complete research package

**Proposal v1 — Codex, 1 November 2026, for Claude's critique and revision.** The first paired
sprint is closed in `loop1-close.md`. Barry requested more ambitious plans and reversed the roles:
"You propose the next two sprint plans (try to be even more ambitious than last time with these),
and Claude critiques and updates them. Then you implement sprint 1, after which Claude critiques
and does sprint 2, and then you critique. Reverse order!"
This is a prospective plan after inspecting the sources and Loop 1 results, not outcome-blind
preregistration. Claude's revised, agreed version precedes implementation. No Loop 2 analysis
has started under this proposal.

## Scientific endpoint

Loop 1 established an executable M2 result from one study and precisely why M1/M3 currently lack
admissible absence designs. This pair should deliver a complete, privately reviewable first-study
package that answers a stronger question: **which constraints on early land-plant producers survive
changes in preservation assumptions, independent source material and fossil-to-node readings?**

Two substantive advances are required: an explicit account of how transport and preservation can
change the quantitative answer, and an independent attempt to reproduce or contradict it outside
the Murzuq study. The result may be a robust conditional exclusion, a demonstrable confounding
limit, or disagreement between sources. Neither a narrower age bound nor admission of a second
frame is a success criterion. A limit must identify the missing observation and show what it
would change; repeating that the record is incomplete is insufficient.

The programme remains F3 plus the bounded trait-to-node pilot (`innovation-scope.md`,
`pilot-traits.md`). A new joint clock/phylogeny model or F1/F2 evolutionary simulation is outside
this pair. A manuscript is an internal research artefact; release or submission remains Barry's
decision.

## Sequence and ownership

| Stage | Owner | Delivery |
|---|---|---|
| Plan | Codex proposes; Claude critiques and updates | Agreed v2, explicit changes and reasons on the Board |
| Sprint 1 | Codex implements, with bounded independent source and methods checks | Observation-data audit, identifiability and robustness analyses, qualified results where warranted, executable handoff |
| Review 1 | Claude critiques and resolves sprint-1 issues before relying on its outputs | Source reconstruction, numerical check and qualification review; retained disagreements made explicit |
| Sprint 2 | Claude implements, with independent checks | External-frame replication attempt, M1/M3 evidence advance, trait-to-node synthesis, full private paper/data package |
| Review 2 and close | Codex critiques; collaborators reconcile | Corrected package, claim-by-claim status, Loop 2 close and next highest-value evidence |

No concurrent editing of shared files. Sprint 1 owns new `data/units/loop2/observation/`,
`models/f3/loop2/` and its audit/results notes. Sprint 2 owns new
`data/units/loop2/replication/`, `data/units/loop2/m1-m3/`, and `manuscript/`.
These are proposed output locations, not a new framework: reuse existing extractors, schemas,
estimation and qualification modules where their contracts fit. Shared-source, card, pilot and
programme edits are sequential and recorded. Split delegate ownership by file and bounded outcome;
use an independent specialist on central scientific claims rather than duplicating all work.

## Sprint 1 — Codex: determine what the observation process permits

### 1. Reconstruct the information actually available

Audit all 164 Abuhmida appendix entries and their chart/prose matches, preserving original material
identities and exclusions. For each, recover the most informative defensible E1, cryptospore and
non-target observation, with page/figure/cell locators and independently checked decisive values.
Do not copy interval summaries into sample rows. Distinguish:

- exact counts, count intervals, percentages with known totals, digitised fractions and presence marks;
- the 200-organic-particle palynofacies count from the separate palynomorph first-slide count and
  additional slide search; identify which observations include the extra search;
- separate trilete/cryptospore tallies from the pooled "cryptospore/spore" category;
- observed absence, unknown reporting, barren preparation, preservation and caved/reworked material;
- cryptospore morphology from producer affinity, using the adopted E2 addendum when E2 is claimed.

The transport-control category need not equal embryophytic E2, but any broader category must be
defined independently, keep its taxon composition and never be relabelled as E2. Retain uncertainty
in numerator, denominator and shared material identity. Complete a source-locked feasibility
matrix before selecting the observation model.

### 2. Derive and test the estimand before fitting it

Keep the frozen Loop 1 encounter results as the benchmark. Specify the mapping from producer output
through transport, preservation, preparation and counting to the reported observation. Separate
what the data identify from what is supplied by a scenario or biological assumption.

**Preferred extension, conditional on usable counts:** a joint trilete/cryptospore observation
model for output relative to cryptospore producers, normalised to the reference interval. As a
candidate starting point, conditioning two Poisson counts on their total can remove a genuinely
shared exposure factor. Derive the actual likelihood for the recovered protocol before adopting
it: shared effort, additional slide searches, overdispersion and differential recovery may defeat
that cancellation. Cryptospore counts are stochastic observations, not error-free exposures.
Zeros, pooled taxa, all-positive binary references and changing control composition require
explicit treatment. An estimated relative output is not an absolute production or crown-age
estimate, and does not measure the old transport ratio ρ.

**If separate counts are absent:** retain the binary encounter model and build a substantive
partial-identification analysis. Show which combinations of producer output and differential
delivery are observationally equivalent, and calculate the delivery/contamination/age assumptions
at which each central conclusion changes. Interval compositions or colour marks may constrain a
scenario only through their actual observation model; they never become invented counts or known
exposures. A further presence/absence control model is worthwhile only if its identifying
restrictions and recoverable gain can be demonstrated.

This branch must add something beyond Loop 1's four-ρ table: derive explicit observational-equivalence
classes and a joint delivery–contamination–chronology identified region or break-even surface, with
the new observation or design change that would resolve each material ambiguity. Distinguish a
model-identified region from a sampling-uncertainty interval and from a grid of sensitivity results.

Choose at most one new observation-model family for binding qualification in this sprint. The
alternative is a rigorous non-identifiability result plus the benchmark's robustness analysis,
not a succession of weakly identified model variants. A small known-answer study must demonstrate
identification and numerical recovery before the full real-design qualification.

### 3. Produce a quantitative robustness analysis

For the pooled Murzuq design and its component wells, compare the following against the frozen
baseline, recording both movement of bounds and whether any informative result remains:

| Assumption | Required challenge | Scientific output |
|---|---|---|
| Delivery and recovery | Existing ρ scenarios, and differential E1/control recovery if a control model is used | Thresholds at which the reference-level M2 exclusion or a relative-output conclusion changes |
| Caving/reworking | A directional contamination mechanism or defensible bounded contamination calculation, including its effect on reference positives and the recovered first appearance | Distinguish indigenous encounter from transported contaminants; a smaller ρ is not a contamination model |
| Geological ages | Coherent, ordered/shared chronology alternatives respecting source correlations, plus the current Hawaz allocations | How chronology changes endpoints and sampled support; no uniform-age assumption presented as measured age uncertainty |
| Between-well structure | Existing frailty assumptions and leave-one-well-out influence | Whether a well or pooling assumption drives the result; overlapping wells are not independent replications |

First identify the influential assumptions using labelled development diagnostics and analytic
counterexamples. Then freeze a manageable joint challenge grid containing combinations that can
plausibly defeat the intended claim; one-at-a-time checks do not establish joint robustness.
Preserve unsupported ranges as scenario ranges rather than assigning evidential probabilities.
Do not fit an unconstrained collection of transport, contamination and production parameters to
the same target data and call the result identified.

The minimum quantitative deliverables are the 459.1 Ma intensity comparison, the reference-level
window comparison, the low-encounter alternatives already used in Loop 1, and the conditions under
which each answer reverses. For a relative-output model, declare corresponding new quantities and
show explicitly why their scales differ. Do not subtract bounds for different estimands as an
"improvement". Qualification applies to released quantities and scenarios, not to every exploratory
surface. Curves or several designs are not simultaneous confidence statements without a separately
declared joint procedure.

Each quantitative robustness claim enters a ledger as **frozen qualified result**, **newly qualified
result**, **unqualified sensitivity**, or **identification limit**, with its supporting evidence.
"Survives" always names the tested assumption envelope. Chronology changes, contamination models
and omitted-well analyses cannot inherit the baseline certificate or become unqualified headline
robustness claims simply because their point results agree.

### 4. Qualify, report and hand over a complete result

Preserve the nominal 0.95, empirical calibration 0.955 and independently assessed 0.93 floor, and
the adopted two-stage rule. For every new released primary design/observation model, simulate its
actual eligibility, reference definition, first appearance, potential screen and estimation path.
Report attempts, pass rate, abstentions, non-abstaining coverage and numerical failures. New data
types and contamination/chronology models require their own simulations and receipts; old
qualification never transfers merely because the optimizer is unchanged.

Declare estimands, nuisance/history grid, quantity list, calibration/acceptance roots and stopping
rule before the binding run. Any calibration changed after seeing acceptance uses fresh acceptance
evidence. Rarely passing or numerically incomplete runs remain incomplete. Use adversarial boundary
and non-identifiable cases, not only histories that naturally deliver trivial sets. Selected-result
coverage remains deferred; retain the Loop 1 reporting discipline and both B4 denominators. Do not
start a separate conditional-inference project merely to improve the label.

**Sprint-1 acceptance:** the full declared material audit is accounted for; the model choice follows
the source feasibility result; at least the benchmark has a quantitative robustness/identifiability
analysis; each released extension passes its own contract or is explicitly withheld; and an
independent check reconstructs a decisive source mapping and one numerical result or impossibility
example. Deliver a concise result note, reproducible tables and figures, immutable inputs and
receipts, a list of assumptions that change conclusions, and a runnable handoff example. A green
test suite alone does not meet this endpoint.

## Sprint 2 — Claude: independent replication and the biological conclusion

### 1. Challenge M2 with independent source material

After reviewing sprint 1, freeze a ranked external-source roster and a transparent search/admission
rule. Define three endpoints separately: independence of material/source from Murzuq, successful
reuse or justified extension of the inference contract, and agreement/contradiction for the same
estimand under comparable assumptions. A cross-study transport comparison can be conditional
corroboration without replicating a within-study contrast; incompatible estimands or failed admission
are not biological contradictions. The held-source reconnaissance identifies these starting points;
they are leads, not admitted
designs:

| Candidate | Intended role | Current limit to resolve |
|---|---|---|
| Le Hérissé et al. 2017, QSIM-801, with Wellman et al. 2015 Qusaiba-1 | Primary candidate for older Saudi material plus a trilete-positive reference: reconcile the reported 42 QSIM samples and 37 Qusaiba samples | Cross-core and cross-study, not a within-study rate contrast. Verify complete E1 reporting, counted/search scope, ages, preservation and transport. Acritarch scope alone supplies no E1 zero. |
| Badawy et al. 2014, Röstånga-1; the existing Baltic source family | Independent geographic corroboration and a search for a complete linked reference | Twenty-one processed samples do not by themselves supply a trilete-positive reference; Katian–Rhuddanian material may inform a later interval but not the older side of M2 |
| Rubinstein et al. 2016, Caspalá/Lipeón | Independent occurrence, age and reworking challenge to the temporal interpretation | Eight sampled levels and seven productive samples; host ages, reworked constituents and unidentified miospores prevent automatic conversion to an older-zero/reference contrast |

Use the source register and held full texts, then a bounded targeted acquisition round for missing
companions or genuinely stronger frame candidates. Record criteria, routes, successes and blocked
targets; stop acquisition when further retrieval cannot change the admission decision. Do not
restart an unbounded bibliography harvest. Reconcile companion publications and reused material;
Qusaiba reused as reference cannot be counted as a second independent reference study.

Build and qualify every admitted primary combination under a declared transport/reference model,
using sprint 1's extension only if its observation protocol applies. Report M2-era comparisons
separately from informative later windows. Test both agreement and contradiction with Murzuq;
report source-specific estimates before considering any pooling. Do not pool automatically across
laboratories, facies or incompatible estimands, or use a combined pass to conceal a failing source.

If none admits, deliver the full rejected-design ledger and the closest attainable independently
observed challenge to the Murzuq interpretation. Distinguish no admissible replication design from
failed biological replication. The manuscript remains a single-study quantitative analysis with
an independently audited limit, rather than claiming geographic generality.

### 2. Turn the M1/M3 gaps into specific scientific tests

Before this tranche, select one inference-changing M1 target and one M3 denominator target, naming
the reading or admission decision each can alter. The source families below supply candidates,
not an instruction to repeat every audit. Continue a target only while it can change that decision
or support a newly quantified design requirement; otherwise retain the Loop 1 disposition and
prioritise the external M2 comparison and synthesis.

For M1, use the adopted E2 rule to reconcile the held Cambrian affinity evidence: Taylor & Strother
2024, Strother 2016, Baldwin 2004 and Wang 2022, with the existing Samphire/Argentina evidence where
it changes a reading. Retain specimen identities, microscopy, morphology and affinity as separate
fields. Determine exactly which readings change the accepted occurrence support and the
cryptospore-to-node implication. Date the relevant evidence without treating a stage boundary as
an occurrence. Only exposure older than 515.5 Ma can test M1's older interval directly.

For M3, extend the existing Irish/Loděnice assessment only where a specific held source or archive
lead adds searched-material information. Produce a joined opportunity ledger for reported
lithologies, beds, collections and field layers, preserving which are actually searched and which
are only described. Include Châteaupanne/dating evidence only where it changes the age or sampling
question; a mapped position is not a negative search. A numerical model starts only if a real
denominator, target ascertainment and reference comparison are recovered.

For both maxima, prepare focused, source-specific requests for the missing sample or field ledgers
and any decisive specimen re-examination. Drafts name the material and the precise missing fields;
Barry sends them. No external reply is a completion dependency. Where acquisition cannot resolve
the gap, calculate the information a specified new roster could supply under declared detection
and dependence scenarios, retaining uncertainty rather than quoting the earlier known-p example
as an empirical collecting requirement.

### 3. Complete the biological pilot and private paper package

Integrate the existing specimen, ancestral-state and persistence evidence with the new sampling
results. Recheck only changed or pivotal claims; do not rerun the published-state extraction or
the R persistence analysis without a reason. For each M1–M3 conclusion, show the full implication:
observed material → named event reading → encounter or relative output → trait persistence →
node interpretation. The crown-state marginals of separately modelled characters do not supply
a joint ancestral phenotype. A finite bound on sampled producer encounter does not by itself
date a crown node.

Deliver a full internal manuscript with methods and supplement, a curated-data release candidate,
and figures generated from declared source tables. The intended figure set is:

1. Sampled time/region/observation support, including the unsampled intervals and failures.
2. Murzuq bounds and the transport/contamination/chronology assumptions that change them.
3. External-source agreement, conflict or non-admission, with source dependence visible.
4. The three maximum-age arguments and their specimen-to-node links, separating supported,
   contested and unresolved steps.

A claim-to-evidence table links every headline number, morphological statement and biological
implication to its source/adjudication and, where relevant, qualified run. Report the central B4
limitation wherever its window is interpreted. Include full AI system/version roles and the
human–AI review history. Copyrighted sources stay local; the release candidate contains only
shareable derivatives and provenance. Assess novelty against the closest actual studies without
claiming priority from our workflow alone. Public release, submission and external messages are
not part of this pair.

**Sprint-2 acceptance:** every declared external candidate has an inspectable disposition; an
admitted result has frame-specific qualification; M1/M3 have updated evidence/mapping verdicts or
a precise, newly tested information limit; and the complete draft, figures, data package and
claim table agree. A prose outline, another source list or a promise to draft later is insufficient.

The manuscript has two explicit branches: a source-specific two-source comparison if an external
frame admits, or a single-study Murzuq analysis with an independently tested replication limit if
none admits. The latter cannot claim independent replication or geographic generality. Both require
an end-to-end rendered manuscript and supplement, regenerated figures, a provenance/licensing
manifest for the shareable data package, and claim statuses consistent across title, abstract,
results and conclusions. Keep the sources needed for private reproduction distinct from the files
that may eventually be distributed.

## Verification, compute and completion

- Preserve Loop 1 source/config/output bytes and their receipts. New versions carry explicit
  provenance and dependency bindings. When shared code must change, trace live callers and either
  preserve a reproducible baseline at its pinned commit or regenerate every affected result under
  a declared new version. Never rewrite old receipt hashes to make new code appear qualified.
- Use mini for extraction and small known-answer checks. Heavy qualification runs on Nectar after
  reading/updating the control-plane records and a timing/memory smoke. Use the authorised
  `c3.3xlarge` tranche with one BLAS thread per worker, batch independent work there, then return to
  `c3.large` after verified collection. Estimate the grid, attempted replicates, storage and wall time
  before launching; change approach if computational cost prevents the decision-relevant test.
- Counter-review reconstructs a decisive mapping independently and checks a numerical result using
  another calculation or implementation, plus the integrity/selection contract. Reproduce failure
  or non-identifiability evidence where there is no admitted result. Fixes propagate to all dependent
  outputs before handoff. New model/source risks justify new checks; unchanged green checks need
  not be repeated merely to increase counts.
- Commit and push coherent tranches to `main`, post results and ownership handoff to the Board, and
  report material findings to Barry. Board messages do not activate the other collaborator: Barry
  re-prompts them. No scheduled monitoring or waiting for an unprompted reply.
- Each close updates questions, decisions, source register when holdings change, and AI roles.
  Distinguish adopted methods, qualified results, exploratory sensitivities and unresolved proposals.

## Questions for Claude's critique

Please revise the plan concretely, particularly: is the sprint-1 model/robustness scope proportionate
to the recoverable counts; is the Saudi cross-study comparison scientifically worth its transport
assumption; which M1/M3 target is most likely to change an inference rather than repeat the first
audit; and does the proposed manuscript endpoint earn a result beyond one regional absence bound?
Resolve routine choices in the revised plan. Preserve the user's role order and the boundary between
an authorised study and a separately authorised public release.
