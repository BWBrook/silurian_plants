# Reconstructing the F3 article from first principles

Barry's method for rebuilding a paper after its first draft (chat, 10 November 2026). The files form a
working reconstruction. Claude's first version of steps 1–2 is preserved at `1fe577c`; those steps have
been reconciled and Barry adopted their main message at `0306623`. Steps 3a and 3b are reconciled at
`dabd5b9` and `2169670`, and step 3c at `ef253d6`; Codex's step 4 revision awaits Claude's reconciliation. The target remains
*Proceedings of the Royal Society B*. AI byline wording remains a placeholder for the submission phase.

## Steps 1–2

| File | Current content and status |
|---|---|
| `1a-working-abstract.md` | Seven organising questions and answers. Retrospective analytical questions replace the “a priori” H1–H3 narrative. |
| `1b-abstract.md` | Abstract under 150 words, including the conclusion-changing unit sensitivity. |
| `1c-main-message.md` | The adopted 24-word message, with the earlier proposals, disagreement and stored-model counterexample preserved. |
| `1d-display-items.md` | Four figures and up to two tables as an editorial allocation; revised contracts for geography, delivery–input trade-offs and unit/delay sensitivities. |
| `2-one-page-paper.md` | Revised complete-paper outline, about 600 words, with detailed conditions gathered in one section. Result values retain ledger/case links. |

Barry called the earlier display allocation “much more rational”. The target venue and prose rules
remain adopted decisions. The reconciliation below records the accepted question-led framing and
brief display choice, followed by Barry's adoption of the reconciled main message.

## Review record and disagreements

The independent checks are `codex-science-check.md` and `codex-message-display-check.md`. They are
review notes within steps 1–2, rather than new reconstruction steps. Codex (`gpt-6.1-sol`) integrated
the checks, independently verified the half-rate counterexample against the stored table and closed
form, and revised the drafts directly.

| Point in Claude's draft | Codex's disposition and reason |
|---|---|
| H1–H3 described as predictions made in advance | Replace with retrospective questions. The body design follows the pilot and the original plan separates estimator checks from predictions about the right clock. The published method predicts how a bound changes with count, not which clock it overlaps. |
| “Producers ... were below a tenth ... abundance” | Use the model's upper compatibility limit on sustained local spore encounter. The counts do not reconstruct historical producer abundance. |
| “15–23 million years after the origin” | State minimum assumed delays in the constant-rate alternative, varying with the candidate age. They specify scenarios. |
| “Young origin ... only if ... as often” | Disagree. At half-rate earlier recording, the stored primary step bound remains younger than 431.2 Ma. Coarser units cross that maximum under equal recording. One equality cannot establish global clock support. Both main-message versions remain in 1c. |
| Measuring recording would decide between clocks | Narrow to constraining compatible histories. Character mapping, geography, ages, units and the molecular analysis also affect the comparison. |
| Four figures / up to two tables | Retain as the working allocation. Add explicit ages/models for palaeogeography, identify the delivery–input ridge, and show the 432–434 Ma unit sensitivity beside 429 Ma. |
| Replace the brief timeline with the full frontier | Retain as a visible design disagreement. Codex keeps the timeline as default until a simplified alternative is compared in the actual two-page layout. |

### Claude's reconciliation, 10 November 2026

| Point | Outcome |
|---|---|
| Main message | Claude concedes the half-rate counterexample (430.98 Ma, checked in `suppression_sensitivity.csv`). The reconciled wording in 1c keeps Codex's positive form, both routes and the alternatives, and adds the size of the requirement ("several times") and its target ("dates for living land plants"). All three versions are visible. |
| Hypotheses or questions | Codex's change is accepted: the questions are retrospective, and the paper must not present them as prior predictions. **Open for Barry:** his method asks for hypotheses grounded in theory. The proposal is that the Introduction gives a theory-based expectation for each question (for example, that confidence intervals on a range narrow as finds accumulate), labelled as an expectation, not a preregistered prediction. |
| One-page paper | Codex's corrections are kept. Claude's plain-language pass rewrites the Approach, the Libya results and the body results for a new reader, adds the half-rate bound (from the stored table, not yet in the ledger) and puts the reconciled message in the Conclusions. |
| "Decide between clocks" narrowed | Accepted. |
| **Main message adopted** | Barry, chat, 10 November 2026: "Reconciled version! This is a team effort." |
| Figure for the brief | Accepted: the timeline stays the default until the two layouts are compared on the page. |

Original complete drafts are available in the
[1fe577c reconstruction directory](https://github.com/BWBrook/silurian_plants/tree/1fe577c/manuscript/reconstruction).

## Scope, checks and structural review

Only `manuscript/reconstruction/` is edited in this tranche. The manuscript sources, evidence ledger,
models, generators and rendered products remain frozen. Reconstruction files lie outside the sources
listed in `scrivmark.toml`; direct edits implement the ownership agreed in Board discussion 158 and
leave Barry's supervisor-review sources untouched.

The numerical check covers the frozen four products plus the revised working abstract, abstract and
one-page outline, using the existing ledger/value bindings. Scientific checks separately cover meaning,
retrospective status and the actual row selectors. A new-reader and scientific writing pass checks
positive findings, term definitions and consolidated conditions. Word counts refer to the paper body
between the horizontal rules, with numerical citation markup removed; the title is excluded.

At Codex's first review (`1ef04ea`): 52 claims cited, zero numerical errors or warnings; abstract 144 words, one-page
body 638, proposed message 22. The abstract and one-page body contain none of the scanned explicit
negation terms. The independent science check of the revised drafts passed after clarifying that the
48-unit calculation concerns vascular-plant bodies. The writing scanner's heading flags reflect the
required outline structure; its “features” flag is a scientific noun and is retained. No model or
render rebuild was needed for this reconstruction-only edit.

**Structural review (Q1/Q2/Q5).** Compression had changed an encounter limit into a measured biological
history and a scenario into a necessary condition for a young origin. Removing negation alone leaves
such meaning errors intact. Naming the result's object, separating research questions from a prospective
history and keeping source/case checks beside the drafting exercise serve the next prose step. No
scientific result, question status or analysis programme changed.

**Working default for hypotheses or questions** (Claude, pending Barry or Codex objection): each
research question carries a theory-based expectation in the Introduction, labelled as an expectation
and not a preregistered prediction.

## Step 3a: section abstracts (Codex revision, 10 November 2026)

`3a-section-abstracts.md` revises Claude's draft at `9e42e71`. The sections contain **272, 261, 275 and
280 words**, respectively. Counts split on whitespace after removing ledger attributes, exclude
section headings, and include paragraph labels and formula spans. Each is below Barry's strict
300-word ceiling, also when hyphens and dashes are counted as word separators. Barry: "There's no strong need for me to
intervene at these stages of the reconstructions, it's the Socratic reflection (and collaboration with
Codex) that matters more at this stage: I come in on the final drafts."

The independent checks are `codex-3a-methods-check.md` and `codex-3a-argument-check.md`. Their focused
acceptance reads passed after the revisions below. These are review notes, rather than further
reconstruction steps.

| Compression issue | Revision |
|---|---|
| Zero detections treated as decisive on their own | The encounter expectation requires comparable exposure. The observed spore–body gap remains distinct from unmeasured divergence and recognition delays. |
| Locality–ages treated as verified horizons; interval ages assigned to oldest endpoints | Name the proxy units and use the greatest possible oldest age with the minimum guaranteed count. The formula now defines its cutoff and cumulative recording exposure. |
| Two Murzuq numbers treated as one intensity limit | Distinguish constant input from the exposure-weighted mean over bounded variable histories. Keep their local, relative-input targets. |
| Open body bound and failed histories stated without domains | Name the 469.4 Ma search domain, the pure 10 Myr decline and the six fixed Oman-inclusive histories. |
| Recording scenarios read as estimated biological histories | Identify the primary half-rate step, zero-delay contrasts and minimum assumed delays. The step retains its retrospective status. |
| A body delay used to explain both spore and body constraints | Keep the spore and body mappings separate. Gather the reference, age, dependence and character assumptions in Conditions. |
| Block comparison presented as a raised calibrated limit | Retain the exploratory contour near 0.4 with unqualified coverage. |
| 0.977 attributed to Hooper's fitted models | Reserve this project's conditional stochastic-map reanalysis for the supplement, with its coding, model, tree and chronology. |

**Placement decisions for reconciliation.** Calibration-audit findings stay in Results; the audit
protocol belongs in Methods. Keep the conditional shape finding, because an unresolved older bound
and a history passing the age-sequence diagnostic answer different questions. Stage-boundary and
coverage ranges remain in the Results outline; their details go to the supplement. The adopted main
message closes Discussion unchanged. Proc B and the display allocation remain settled.

**Observed checks.** The numerical check includes all four frozen products and reconstruction steps
1a, 1b, 2 and 3a: 52 claims cited, zero errors and zero warnings. The four section bodies contain none
of the scanned explicit negation terms. The half-rate value remains pending ledger integration before
full prose; its saved output and independent algebra were checked in steps 1–2. The checker passes
the existing bindings and does not confer support on that unbound value. No model runs or product
builds were needed; the ledger, analyses and canonical products remain frozen.

**Structural review (Q1/Q2/Q5).** Compression again changed the subject of several sound numbers.
Keeping the age-envelope rule, object labels and scenario selectors visible, while gathering detailed
conditions, serves the full-prose step. This review changes the reconstruction wording and placement;
the scientific results, question statuses and analysis programme remain as adopted. The frozen
question and decision registers can record the completed reconstruction loop when it closes.

### Claude's reconciliation of step 3a, 10 November 2026

Codex's repairs are accepted in full. Restored for a new reader, within the cap: numbered questions,
the classical stratigraphic confidence interval as the method's anchor, a definition of recording
contrast, Hooper's keying of 459.1 Ma to the possible trilete, the role of the 18 younger cuttings,
body-size and tissue traits as recording mechanisms (attached to the body comparison only), and the
transfer to other absence-based maxima. Simulation coverage moves to the supplement. Counts: 272, 295,
290 and 292 words; claims check 0 errors. Step 3a is locked as a draft.

## Step 3b: paragraph abstracts (Codex revision, 11 November 2026)

`3b-paragraph-abstracts.md` revises `fca1069`. It has **27 paragraph abstracts** (Introduction 5,
Material and methods 8, Results 8, Discussion 6), each with a one-sentence framework message and
3–4 sentences, excluding citation signposts. Every section retains an order and coverage check
against the reconciled 3a. The adopted main message closes D6 unchanged.

The bounded checks are `codex-3b-science-check.md` and `codex-3b-reference-check.md`. Their acceptance
reads passed after restoring the specific cases and correcting R4: the Darriwilian supports extend
older than 459.1 Ma, but their exposure contribution under a postulated start at that age depends on
the within-stage treatment. These review notes give source sections, output selectors and model
contracts; the numerical checker separately checks the existing bindings.

| Review question or issue | Disposition |
|---|---|
| Keep R5 and R6 separate? | Yes. R5 gives primary conditional bounds and the fixed-history diagnostic; R6 shows unit/inventory sensitivity across 431.2 Ma and the smaller shifts in the tested primary constant-rate timescale cases. |
| Add Wilkinson to D3? | Omit from the current paragraph. Its branching-and-sampling route to a molecular prior is distinct, but the present contrast needs Silvestro, CladeDate and Hooper. The reference audit preserves that distinction. |
| I2's soft-bound practice | Replace the unsupported prevalence claim with a definition supported by original Yang and Rannala material; original Parham sections support explicit justification. |
| Place Conditions at D4? | Keep after interpretation/comparison and before evidence that would sharpen the results. State the base treatment in Methods and gather limits at D4. |
| Qualification, confidence and age diagnostics | Name the screened-design two-stage qualification rule, proxy units, minimum guaranteed count, finite-sample count/oldest-find conditioning, and the observation-model support condition for conservative rejection. Restore proper TeX. |
| Step, timescale and causal claims | Define the contrast at ancestor age minus assumed delay, retain the retrospective step, and label the primary constant-rate timescale cases. The models quantify aggregate scenarios; separate biological mechanisms remain open. |
| Proposed future evidence | Documented search effort could constrain recording opportunities. Rock availability alone does not identify a recording rate; new character evidence may change fossil admission as well as the node link. |

**Reference coverage.** The revised signposts identify 34 existing works and 13 additional candidates.
Strother 2021 was already in the bibliography and is now signposted by its existing key. Relevant
original sections of Yang and Rannala and Parham were read for I2; Wilkinson was read to assess its
distinct role, then omitted from D3. The remaining candidates are explicitly pending content reads.
Comparator reference counts prompt a coverage check, rather than a citation quota. Bibliography
integration waits for relevant source reading and full prose.

**Observed checks.** All 27 abstracts have 3–4 sentences; counts include every sentence in I5 and M7,
which now use ordinary prose. Existing citation keys resolve to the bibliography. The checker covers
the four frozen products and reconstruction 1a, 1b, 2, 3a and 3b: 52 claims cited, zero errors or
warnings. The half-rate example remains independently checked but pending ledger integration before
canonical prose. The ledger, bibliography, models, reconciled 3a and canonical products stay frozen;
no model runs or renders were needed.

**Structural review (Q1/Q2/Q5).** Expansion reintroduced ambiguity about proxy horizons, simulation
acceptance and the time exposed after a candidate start. The paragraph plan now keeps each result
attached to its case and each mechanism distinct from the aggregate contrast. Separate primary-bound
and sensitivity paragraphs preserve the conclusion-changing unit result. Question statuses and the
analysis programme remain unchanged; the registers can record the reconstruction loop when it closes.

**Claude's reconciliation (11 November 2026).** Codex's repairs are accepted in full. M7 keeps the
operational rejection rule; its independence and support-containment conditions join D4's body
conditions. Claude's draft miscounted its own framework as 26 paragraphs; there are 27. Step 3b is
locked as a draft. Barry, via the Board, 11 November 2026: "await my guidance for step 3c before
expanding the prose."

## Step 3c: full draft (Codex revision, 11 November 2026)

Barry's instruction (chat, 11 November 2026): "add the flesh to the bones. But do it judiciously. Don't
overwrite!" `3c-full-draft.md` revises Claude's full draft at `c0f83fc`. It has a **189-word abstract**
(196 when dashes split words) and approximately **3,041 words of main text**: Introduction 568,
Material and methods 930, Results 766 and Discussion 777. Counts split whitespace after removing
ledger attributes and citation keys; Table 1, captions and end matter are excluded. Keep this lean
length. Comparator counts give no reason to expand it; building the figures and checking their
agreement with the text is the next substantive communication task.

The bounded checks are `codex-3c-science-check.md` and `codex-3c-argument-check.md`; focused acceptance
reads passed after clarifying the pure exponential-decline label. They record case selectors,
qualification contracts, source sections and access limits. The revisions make the following changes:

| Point | Revision and verification |
|---|---|
| 429 Ma interpreted as a beginning | Restore a one-sided older confidence bound under specified histories, with the 432.4–434.05 Ma unit/inventory sensitivity beside it. |
| Potential screen and qualification | Explain the joint shared-well likelihood, potential-screen zeroing, identical screening of simulations, independent acceptance, finite grid, withheld claims and separate second-stage rule. |
| Age-search inference | Distinguish a feasible passing allocation from failure over every allocation. Gather the fixed-model probability-one support condition and unestablished joint geological coverage in Conditions. |
| Dependence cases | Identify both changes in the 0.0995 case: per-well reference rates and removal of the random well effect. Label the retrospective contours and well deletions as unqualified. |
| Source and prior scope | Define absence-based maxima; compare effective marginal joint-prior ages with posteriors; retain deposition as a hypothetical mechanism in Discussion; distinguish excluded copyrighted texts from fetched licensed deposits. |
| Repetition | Move region/Yea numerical details and the 20 Myr delay example back to the supplement. Keep the sensitivities that cross the comparator maximum. |
| Captions | Preserve study-specific clock summaries, the age-envelope rule, primary spore model, constant-recording unit comparison and retrospective contrast domain. Figures remain unbuilt. |

**C53 confirmed.** V108 selects the correct primary B2 flat-baseline half-rate row. Its evidence blob
is unchanged from stamp `813b43c`, and the closed form independently gives 430.980011897 Ma, matching
the saved 430.9800119 Ma and displayed 431.0 Ma. The claim's limits correctly retain the data-selected
step and retrospective status. The ledger and binding need no change.

**Reference provenance.** Claude reports the remaining eleven-candidate source-reading job and four
verbatim spot checks; twelve DOIs were added at `c0f83fc`, with Gradstein omitted. This review checked
targeted original material for Benton/Donoghue, dos Reis et al., Kenrick/Crane and Brown/Smith, retaining
the earlier Yang/Rannala and Parham checks. The eleven-source job receipt was not found in the bounded
project search. Its source URLs, sections and claim scopes remain to be preserved during
reconciliation; the current checks do not attest to every delegated read.

**End matter.** Funding now states “This research received no specific funding”, following Barry's
chat reply on 11 November: "No specific funding for this project." The proposed AI-use declaration
credits the recorded systems, versions and tasks, including independent critiques, and correctly
keeps Barry's final manuscript review prospective.

**Observed checks.** The draft-inclusive numerical check cites all 53 claims with zero errors or
warnings. Existing citation keys resolve, the abstract meets 200 words under both counts, and the
adopted closing message matches exactly. `make -C manuscript check` passes lint and reference audits;
its canonical-only numerical check has one expected warning because C53 is cited only in the new
draft. The writing audit's formatting flags reflect the section labels and table; “shape” and
“features” are retained scientific terms, and the two fossil intervals retain their necessary
parallel description. The canonical products, models, ledger, bibliography and earlier reconstruction
steps remain untouched. No model reruns or figure renders were needed for this prose review.

**Structural review (Q1/Q2/Q5).** The full prose again exposed shifts from a bound to a date and from
specified model comparisons to broader causal claims. Explicit result objects, case labels and a
source-role audit resolve them without lengthening the article towards comparator sizes. Conditions
remain gathered in two paragraphs. Question statuses and the analysis programme remain unchanged;
the registers can record the reconstruction loop when it closes.

**Claude's reconciliation (11 November 2026).** Codex's repairs are accepted in full. The
reference-reading receipt is now preserved in `docs/audits/2026-11-11-3c-reference-reads.md`, with the
job prompt and its JSON output. Step 3c is locked as a draft; Barry has said step 4 comes next.

## Step 4: final detailing (Codex revision, 11 November 2026)

Barry's instruction (chat, 11 November 2026): references, formatting and display-item legends; "a hard
edit, to cut verbiage"; strategic repetition of the main message; then a second pass for context,
clarity and a general audience, with "no re-structures at this stage". `4-final-draft.md` revises
`7e560c5` without moving paragraphs or changing the adopted message. The unnumbered sections,
finding-led Results headings, separate Conclusion and front/end matter remain. The abstract is
**191 words** (200 when dashes split words); main text is approximately **3,063 words**, excluding
Table 1, legends, end matter and citation keys.

The bounded independent checks are `codex-4-science-check.md` and `codex-4-argument-check.md`.
Their focused acceptance reads passed. The main numerical results and Conditions survived the cuts;
the repairs restore the following distinctions:

| Point | Revision |
|---|---|
| Strategic repetition | Keep the adopted Abstract/Conclusion endings and conditional body message in the Results, Discussion and standalone legends. The audit remains qualitative where the assembled frame prevents a numerical test. |
| Conclusion opener | Scope it to an absence-based maximum and distinguish ancestral character production from recovery in older rocks. |
| Plain-language crown gloss | Define crown groups as the shared living ancestor and all descendants, including extinct members. Replace “among living plants” with placement within the crown. |
| Shortened model account | Restore the fixed younger cutoff in the count expectation, full-exposure/zero-outcome potential screen, identical screening in simulations and acceptance independent of calibration. |
| Figure 1 | Preserve source-era clock/maximal ages, current stage mapping for fossil supports, published radiometric dates, HPD summaries versus a topology envelope, and labelled spore/source readings. |
| Figures 2 and 4 | Keep fixed-history confidence interpretation distinct from retrospective step/delay compatibility. Figure 4 shows 50 possible units, 48 guaranteed, with cutoff-straddlers marked; the contour cases, counts, cutoff, anchor, omitted domain and display floor are explicit. |
| Figure 3 | Define input and older/reference delivery, audited target-zero coding, the 18/10 sample-support split and model-conditional curves. |

**Prepared submission material.** `4-submission-materials.md` contains an exact **100-word media
summary**, its evidence trace, and a contribution inventory grounded in the project record and NISO
role descriptors. It makes no byline decision. Barry's exact deferral is preserved there; final byline
and CRediT wording remain for the submission phase. A competing-interest question was asked during
this review; its answer remains pending, so the article retains that placeholder. The funding
statement remains the previously confirmed absence of specific project funding.

**Provenance closed.** The source-reading receipt, prompt and eleven-item JSON output are preserved
and inspected. The dataset bibliography entry matches the registered DataCite metadata. These checks
close the missing-record and new-reference checks; they do not re-download dataset bytes or count as
eleven fresh source audits.

**Observed checks.** The draft-inclusive numerical check covers 53 claims with zero errors or
warnings. All 46 citation keys resolve. The abstract meets 200 words under both counts; the media
summary is exactly 100 words. The adopted sentence matches in both Abstract and Conclusion.
`make -C manuscript check` passes lint and reference audits, with the expected canonical-only C53
uncited warning while the canonical text stays frozen. The writing scanner's formatting and term
flags were reviewed manually; required section labels and scientific terminology remain. No model
reruns, figure builds or canonical changes were made.

**Structural review (Q1/Q2/Q5).** The remaining risks were claims broadened by strategic repetition
and figure captions hiding differences in timescale, unit counts or inference type. Analysis-specific
wording and explicit display contracts resolve those risks without restructuring. Actual figure
construction and inspection remain the next substantive tranche. Question statuses and the analysis
programme remain unchanged; the registers can record the reconstruction loop when it closes.

Next: Claude — reconcile step 4 and take up the figure-building tranche.
