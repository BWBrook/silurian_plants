# Reconstructing the F3 article from first principles

Barry's method for rebuilding a paper after its first draft (chat, 10 November 2026). The files form a
working reconstruction. Claude's first version of steps 1–2 is preserved at `1fe577c`; those steps have
been reconciled and Barry adopted their main message at `0306623`. Codex's step 3a revision awaits
Claude's reconciliation before the next reconstruction step. The target remains
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

## Step 3b: paragraph abstracts (Claude draft, 10 November 2026)

`3b-paragraph-abstracts.md`: 26 paragraphs (Introduction 5, Material and methods 8, Results 8,
Discussion 6), each with a one-sentence key message, order and coverage checks against 3a, and an
abstract of 3–4 sentences with citation signposts. The signposts use 34 existing references and 14
candidates whose DOIs were checked against Crossref; candidates are to be read before citing. Claims
check: 0 errors.

Next: Codex — review step 3b.
