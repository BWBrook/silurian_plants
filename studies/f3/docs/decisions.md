# F3 decisions

Dated record of decisions for study F3 (fossil absences and molecular-clock maxima). Newest first.
Programme and cross-study decisions are in `docs/decisions.md`. Entries before 14 November 2026 were
written before the study-first move and name pre-move paths (`models/f3/`, `data/units/`,
`manuscript/`, `docs/audits/`); `studies/f3/PATHS.tsv` maps each to its current location.

## 2026-11-14: the combined rock and spore measure is computed and tested (Barry with Fable; Claude)

Fable 5.2's issue 2, relayed by Barry (chat with Fable, 14 November 2026: "Yes, I thought that was a
strange stopping point too. 'Why not test it, if you're aware of it?' Let's be bolder, agreed."), asked
for the combined outside measure that Results (g) had left "untested". Claude wrote the specification
into `studies/f3/docs/plan-rulers.md` before computing (an addendum that departs from that plan's no-product rule
and is labelled post hoc), computed it in `studies/f3/models/loop3/combined_rulers.py` and entered C59
(provisional).

- **Combined case.** Rock x spore share, as the ratio of window means of the stage-by-stage product:
  21.7 at 444 Ma and 29.8 at 452 Ma, leaving 1.15-1.23 expected early finds with 48 finds against the
  3.09 boundary; multiplying the two single ratios, as Fable's sum did, gives 1.48-1.61. Every count
  fits. Fable's rough sum (1.5-1.6) holds; the stage-by-stage product is stronger because both
  measures are high in the Early Devonian.
- **Searching.** Not multiplied with rock (collections are made in rock; the product would count rock
  twice). Searching x spore share, the global alternative, leaves 3.6-4.1 expected early finds at 48
  finds (exceeds) and 1.8-2.0 at 24 (fits).
- **Overlap.** Across the 13 stages Katian-Emsian, Spearman rho rock-spore 0.30 (permutation p 0.31);
  13 stages cannot separate a shared cause from coincident trends.
- **Placement test (added by Claude, beyond Fable's list).** If finding were proportional to a measure,
  the later finds would sit where it is high. 13 of 48 finds lie wholly in the Pridoli or
  Ludfordian-Pridoli. Rock predicts 0.45 in the Gorstian-Pridoli, spore share 3.8, their product 0.14
  (p <= 0.003 throughout); a level rate and searching predict about 10 (compatible), and about 7.8
  from the Ludfordian base (p about 0.04). So the record contradicts finding that tracks rock or spores
  stage by stage, and the combined contrast supports older ancestors only under the separate assumption
  that mean finding rates share it between the windows.
- **Disposition.** "Yes, but": the product closes the gap arithmetically, and the same proportional
  model is contradicted by where the later finds lie. The Abstract, Methods (h), Results (g),
  Discussion, Conditions, Conclusion and figure 3b (a rock x spore curve) now say so; "remains
  untested" is gone.
- **Checks.** Sol (`gpt-6.1-sol`) recomputed every value by exact integration (within 0.011%) and found
  the placement interval mislabelled (it ran from the Gorstian base); corrected, both splits reported.
  Sol's meaning check flagged overstatement of "fits" for level and searching; repaired as
  non-rejection; Sol's recheck asked that 13 be stated as a minimum (up to 16 may lie there) and that the
  level-rate condition be limited to the window-mean reading; both repaired. Audits: `studies/f3/docs/audits/2026-11-14-c59-sol-*.json`. C59 awaits Codex's check.

## 2026-11-14: plain-wording repairs after Fable's review of issue 1 (Barry with Fable; Claude)

Fable 5.2 reviewed the rule-of-three revision and judged the substance right and the wording short of
its one-reading test. Barry (chat, 14 November 2026): "as Fable notes, no need to make another round of
this. Fix these yourself". Claude made the repairs without a further Codex or Sol round:

- **One phrase for the rule's condition.** "With finding level" and its variants became "if fossils turn
  up at a steady rate after the oldest find" in the Abstract, Methods (g), Results (d) and (f), the
  Discussion and the Conclusion.
- **Abstract (200 words).** Independent finds are glossed as separate discoveries; the delay route keeps
  its direction and loses its 15–23 Myr figure (still in Results (e)); the outside-measure sentence now
  states the matching counts (rock 20 or fewer, spore-reporting share 31 or fewer, both from C56 at
  444 Ma). Fable's suggested "fewer than about 30" holds for the spore share only; rock needs 14–20 or
  fewer across 444–452 Ma, so the Abstract gives each.
- **Results (f)** drops its opening sentence, which repeated (d)'s three durations, and points back to
  (d). Methods (g)'s "Longer delays reduce the reduction" now reads "The longer the delay, the smaller
  the reduction".
- **Jovanovic and Levy (1997)** is dropped: it was read at abstract level only, and Hanley and
  Lippman-Hand (1983), read in full, suffices. Removed from `references/dois.txt` and
  `docs/closed-literature.csv`; C58's basis updated.
- **Attribution.** Barry: Codex ran "sol, terra and astra"; how to attribute versions or named models
  is deferred to the pre-submission pass.

## 2026-11-14: C58 independently checked and supported (Codex)

Codex accepts the rule-of-three framing after an independent conditional-binomial derivation,
70-digit numerical checks of all 32 saved rows, and separate solutions for all 12 finite exponential
thresholds. Hanley and Lippman-Hand's original author-hosted reprint was read in full; the second
reference was checked at abstract level, with its full-text gap recorded. C58 is supported at the
exact finite-count boundary, using the later rate estimated from the finds. The manuscript now makes
the conversion from the binomial probability explicit; six numerical spans bind to their exact cases.
The script description is narrowed to its actual selected checks. Numerical outputs are unchanged.

**Structural review (Q1):** the common expected-count scale connects the count sensitivity, step,
rise and delay calculations without subsuming the later-age shape diagnostics or Libyan model.
The distinction between conditional expected counts and counts at the estimated later rate is now
explicit in the interpretation specification. The structure serves the next investigation; neither
the independent count nor transfer from the outside proxies is resolved. No question changes status.
The article returns to Barry's line edits; the companion products remain for the later agreed pass.
Audit: `docs/audits/2026-11-14-c58-review.md`.

## 2026-11-14: the rule of three organises the body-fossil results (Barry with Fable; Claude)

Fable 5.2, advising Barry, proposed that every body-fossil number follows from one unstated fact: at
the finding rate after the oldest find, the silence before it fits any earlier history expected to
yield about three finds or fewer. Barry put it to Claude (chat with Fable, 14 November 2026, relayed in
Barry's prompt): "Issue 1 is a great place to start ... So yes, let's put that to them first." Claude
derived it independently: each of the *n* finds falls before *A* with probability p, no early find has
probability (1 - p)^n = 0.05, and at the later rate the earlier interval holds n(0.05^(-1/n) - 1)
expected finds, 3.09 for 48 and 3.32 for 15, tending to ln 20. `studies/f3/models/loop3/rule_of_three.py`
confirms that every steady-rate limit, step ratio, rise, minimum delay, the 431.2 Ma crossing and the
outside-measure matches sit at that count (claim C58, provisional until checked by Codex or Barry).
Credit: Hanley and Lippman-Hand 1983 (DOI from Crossref; second author from PubMed, because Crossref
omits her) and Jovanovic and Levy 1997. The Abstract, Results (d)–(g), Discussion and Conclusion now
state the rule once and lean on it; the Abstract fell from 21 numerals to 13. Limits kept in the
Conditions paragraph: the expected count uses the later rate estimated from the same finds, so it is
conditional on the count and cutoff; a delay moves the start of the count; post hoc shapes carry
compatibility, not 95% confidence; the rule covers the body record, not the Libyan spore model.

## 2026-11-13: general-points revision independently reviewed (Codex)

- **Scope.** Review of the article revision through `75f2bb0`, requested by Barry on Board 158.
  The brief, graphical abstract and agent guide stay in their prior state until the article and
  Barry's planned line-edit pass settle, as specified in the handoff.
- **Claims.** C54 is supported only for the narrowed primary-source-supported Saudi/Turkish
  comparison, with overlapping stage ranges rather than exact contemporaneity. British review
  entries conflict with cited primary evidence; Belgium remains unverified here. C55–C57 are
  supported after independent source-table reconstruction and closed-form calculations, with the
  assumptions stated in `manuscript/estimands.md` and the three 13 November audit notes.
- **Interpretation.** A continuous count curve is an algebraic sensitivity, not a calibrated
  effective sample size. Proxy ratios put required finding-rate ratios in context without proving
  their mechanism. Earlier histories with the same integral cannot be distinguished under a common
  fixed later plateau. The exponential unlimited-age condition is exact; rounded finite-age
  thresholds cannot substitute for it. No new crown date or clock ranking is inferred.
- **Structural review (Q1/Q2/Q5).** The count → requirements → rise → outside-proxy sequence now
  separates dependence, assumed histories and descriptive external context. The source check
  exposed a false transfer from a review entry to a secure occurrence, and the mathematical check
  separated finite from unlimited compatibility. The structure serves the next investigation;
  no question changes status. The article is handed back for reconciliation and Barry's line edits,
  with the later product pass still pending.

## 2026-11-11: reconstructed F3 article becomes canonical (Claude and Codex, under Barry's method)

- **Integrated.** The reviewed step-4 draft (`manuscript/reconstruction/4-final-draft.md`) is now
  `manuscript/text/main.md`, with legends in `figures.md` and figures 1–4 drawn by
  `manuscript/figures_main.py` from `figures.py`. Codex proposed the integration after accepting the
  figures (Board 158); Barry set the reconstruction steps in chat, including step 4: "Think of step 3
  as building a solid house. Step 4 is the painting and decorating, to make it ready for sale."
- **Format.** *Proc B* structure and end matter; numbered *Proc B* citation style for article and
  supplement, with narrative citations written as "Author et al. [n]"; the brief keeps author-date.
  The brief now leads with the adopted main message.
- **Ledger.** C53 (half-rate bound, 430.98 Ma) added and confirmed by Codex. All 53 claims are cited
  across the four products with no errors or warnings; C03, C05, C26 and C37 moved to the agent guide.
- **Open for Barry:** byline and CRediT wording (deferred by Barry, 10 November 2026), competing
  interests, final review before any submission.
- **Structural review (Q1/Q2/Q5).** The stepwise reconstruction served: each expansion exposed a
  scope slip (a bound read as a date, aggregate contrasts read as separate mechanisms, interpolated
  scenario limits) that the paired review caught. No question changed status; the analysis programme
  is unchanged.

## 2026-11-10: main message for the F3 article (Barry; Claude and Codex)

- **Adopted** (Barry, chat, 10 November 2026: "Reconciled version! This is a team effort."):
  "Older dates for living land plants fit the fossil record if early plants were found several times
  less often, or recognisable features evolved later." (24 words.) It supersedes the message in the
  target-journal entry below ("maxima … conditional on assumed recording, or untestable").
- **How it was reached:** Claude's draft ("supports a young origin … only if … as often") failed
  Codex's check, because halving the earlier recording rate gives a bound of 430.98 Ma, still younger
  than the 431.2 Ma maximum (`models/f3/loop3/out/suppression_sensitivity.csv`). Codex proposed a
  positive compatibility statement; Claude added the size of the requirement and its target. Record:
  `manuscript/reconstruction/1c-main-message.md`, Board discussion 158.
- **Consequence:** the abstract states the quantities that "several times" compresses (8–12-fold,
  2.4–4.5-fold under coarser units, C48; the roughly tenfold Libyan spore-encounter limit, C24). The
  half-rate bound enters the ledger before any product quotes it.
- **Open:** hypotheses or questions. Working default (Claude): theory-based expectations labelled as
  such, attached to retrospective questions.

## 2026-11-10: target journal for the F3 article (Barry; Claude)

- **Target: *Proceedings of the Royal Society B*** (Barry, chat, 10 November 2026: "Proc B then, I
  agree. That feels right, and will stop us wasting time at the other venues. Still a good
  contribution, but I think our later work on the Silurian Plants repo has more chance of
  harder-hitting novelty/innovation."). Claude had argued for *PNAS* (where Morris et al. 2018
  appeared) and then conceded that, without an estimate of the earlier-to-later recording contrast,
  the result is a price on older clocks rather than an answer. That estimate (Macrostrat rock and
  palynological sampling, Late Ordovician–Llandovery against Wenlock–Ludlow) is noted as a candidate
  for later work, not added to F3.
- **Consequences for the supervisor round:** fit the article to Proc B's format; state the main
  message (the maxima that divide clocks are conditional on assumed recording, or untestable) in the
  abstract and the brief's first finding; add a concrete recommendation for clock builders.
- **Proc B format comparison** (Claude, Sonnet subagent): `docs/audits/2026-11-10-procb-format-comparison.md`,
  kept for the revision at Barry's request. Main gaps: 200-word abstract, methods into the main text,
  Proc B end matter, numbered references, length and table count.
- **AI byline deferred** (Barry, chat, 10 November 2026: "AI byline is important, but leave it as a
  placeholder for now. We'll craft it properly as one of the last tasks we do before submission").

## 2026-11-08: follow-up implementation and cross-product reconciliation (Codex)

Barry relayed Claude's `8a2194e` handoff. Codex completed F1/F9/F10/F12 and C47 verification,
with source/model, reproduction and mathematical delegates assigned disjoint files. The delivery
record is `audits/2026-11-08-review2-handoff.md`.

- **Source-backed B1 restoration.** E3 now explicitly records branched fertile material at Kosov and
  Capel Horeb, with the conducting-tissue evidence kept anatomically separate. The sterile Lang axis
  remains outside B1. Main B1 has 71 possible/69 guaranteed units and a constant bound of 434.649615 Ma;
  inclusive B1 has 75/73 and 447.367027 Ma. The parent independently recounted units and evaluated the
  constant and step bounds and the *C. barrandei* leave-out from closed forms. All B0/B2 result rows
  remain unchanged. C25/C39/C32/C52 and the affected simulation summary C34 are propagated.
- **Inference and specification.** The finite-sample interval-wide rejection is valid when the supports
  contain the true ages/inclusion almost surely under the observation model, with fixed history,
  cutoff, timescale, inventory and unit rule and independent continuous ages. If containment fails with
  probability delta, only an alpha + delta size bound follows. Berger–Boos is an analogy, not a
  geological coverage guarantee. S2.2 now specifies the age mixture, shared-well likelihood, nuisance
  rates, history restrictions, upper envelope, inversion and qualification scope without changing the
  model. C47's 2.2/2.9 Myr comparisons are independently source- and arithmetic-checked, hence supported.
- **Reproduction.** The public test target fetches the archived input first. Optimiser round-off has a
  declared absolute tolerance of 1e-9 for one CSV only, with exact identities/schema and both hashes
  retained. Both reproduction routes pass (65/76 tables, all byte-identical on this run), as does the
  63-test public target in a tracked-file copy with the raw input initially absent. Source checking
  reports the public thesis route and expected hash even when the copyrighted PDF is absent.
- **Semantic review.** The new frontier figure now omits undefined T-minus-delay combinations and
  states its no-reduction display ceiling. First-record bands are category supports whose endpoints
  can come from different finds, rather than the date range of a single specimen. The conclusion and
  brief retain conditional bounds and the shared well effect. Biological plausibility remains
  unranked, as adopted in Claude's triage; no new clock analysis, measurements or source requests.

**Structural review (Q1/Q2/Q5).** Event-enumeration scope is part of the evidence: absence from an
event list cannot substitute for a source-level character assessment. A precise numerical frontier
can also be misdrawn through domain clipping, and valid interval-wide rejection needs an observation
model for containment rather than a citation alone. Source-backed admissions, explicit mathematical
conditions, clean-copy execution and checks of plotted meaning serve this revision without a schema
redesign or another modelling tranche. Loop 3 stays closed; Claude's final editorial check of the new
S2.2 specification precedes Barry's review. Release and submission remain Barry's decisions.

## 2026-11-07: GPT-6 Pro follow-up review triaged; paper reframed around its findings (Claude; B1 restoration with Codex)

Barry, through the Board messenger, 7 November: "As the next step, please work with Codex (but you
should start) to process the new review, and revise the three parts of the paper accordingly." All
thirteen findings are accepted (`audits/2026-11-07-gpt6pro-review2-triage.md`).

- **B1 (both; written before code).** *C. bohemica* (Libertín et al. 2022, branched holotype and D 554)
  and Capel Horeb Ludlow (Edwards & Rogerson 1979, Plate 1e, g) have published branched fertile material
  and return to B1 through new E3 interpretations; the Lang axis stays out; no E4-to-B1 rule. Codex
  implements, regenerates and re-binds (expected main B1 71/69 units, constant about 434.65 Ma).
- **Claude, this turn.** New title and a 268-word abstract; finding-led results (§3.1 three maxima, §3.2
  Murzuq, §3.3 body-record requirements with a new frontier figure, §3.4 category and recovery route,
  §3.5 interval feasibility); Silvestro et al. 2015, Marshall 2019 and CladeDate placed in §4.2; Yea,
  Sweden, Libyan-zero provenance, *C. barrandei* arithmetic (C47, now provisional) and Oman anatomy
  corrected; the mapping matrix moved to Fig. S7 and replaced in the main text by a table of the three
  maxima; finite-sample interval results primary, with the sup-p conservative-rejection reading in
  S5.2 and `estimands.md`; brief figure relabelled (conditional limit, first-find age ranges) and its
  chronology, "more advanced" and "matching the youngest clock" wording repaired; AI roles condensed.
- **Default adopted on the one judgement the reviewer reserved for Barry:** the paper stays agnostic
  about the biological plausibility of any recording contrast or diagnostic delay, and describes
  processes that could produce one. "Not extreme" is removed. Barry may override.
- **Structural review.** The ledger caught every numeric drift but none of the three category or
  semantic errors this review found; those came from reading sources and rendered products. The event
  inventory's enumeration scope is now stated where it is used, so a missing row cannot be read as an
  assessed absence (guide trap 25). No question changed status; Q1 and Q2 are sharpened (below in
  `questions.md`).

## 2026-11-07: Loop 3 closed; F3 paper at a reviewable state (Claude, after Codex's semantic review)

Claude applied all repairs in `audits/2026-11-07-semantic-closure-review.md`: conditional independence
given the Murzuq well effect and the unqualified status of block contours (abstract, §3.2, Table 4, §5,
S2.5, brief, guide); the candidate-lineage-age definition and zero-delay condition of the frontier
(abstract, §3.3, §4.1, S5.4, brief); fossil-category bounds rather than event dates (Table 4, §4.1,
brief); the GTS2012 stage-base-plus-uncertainty rule and "tested" boundary scenarios (abstract); the
conditional link from the crown trilete state to local encounter (§3.2); the guide's B0 vocabulary; and
the Table S7b description. Supplementary figure identifiers were renumbered (makedoc numbers them from
the id suffix, and the new Murzuq panel had duplicated S2). PDFs rebuilt with Codex's refreshed
diagnostics; brief two pages. 52 claims, 0 errors.

**Structural review.** The stage split worked: estimands agreed first, analyses by Codex, independent
recomputation and integration by Claude, semantic review by Codex. The exposed assumption was
procedural: a numerical checker and a figure receipt both pass while a sentence changes its noun or a
figure uses stale inputs, so semantic review and figure-input checks are part of every closure. No
evidence changed a question at closure; Q1 and Q2 carry the open edges named in `questions.md`. Release
and submission remain Barry's decision.

## 2026-11-07: stage 2 semantic review; bounded repairs before closure (Codex)

Codex reviewed Claude's integration at `87ad964` against `manuscript/estimands.md`, with two bounded
independent semantic reads. The consolidated findings and exact loci are in
`audits/2026-11-07-semantic-closure-review.md`. C48–C52 remain supported. No new analysis or scientific
decision is required: summary prose must retain conditional independence given the Murzuq well effect,
the unqualified status of composite block contours, fossil-category bounds rather than event dates,
the zero-delay step-model assumption for the quoted frontier factors, and the scope of tested boundary
scenarios. Claude retains manuscript prose and final PDF integration.

Codex also repaired its own stage-2 omission: the three borrowed supplementary macrofossil diagnostic
figures still used the former inventory. Their renderer and images now match the accepted canonical
tables, with Oman visible and the correct primary suppression variant. Every figure-receipt hash
matches; all 73 scientific CSVs are unchanged. The emitted supplement PDF awaits Claude's rebuild.

**Structural review (Q1/Q2/Q5).** Numerical bindings cannot enforce the noun, conditioning or evidential
status of a sentence. A receipt for an old figure also does not establish that the figure uses current
inputs. The existing estimands specification plus targeted semantic and figure-input checks serve
closure; a broader checker or new modelling tranche is unnecessary. No scientific question changed.
Loop 3 remains open for the finite wording repairs and rendered-product reconciliation only.

## 2026-11-07: GPT-6 Pro stage 2 checked and integrated (Claude)

Claude recomputed the key values of C48–C52 by routes independent of Codex's code (closed forms, KS
distances from witness files, and a separate implementation of the Murzuq dependence likelihood) and
marked them supported (`audits/2026-11-07-stage2-integration.md`). The paper now reports the
age–intensity frontier in place of the single tenfold scenario, the interval-wide shape results, the
shared-timescale scenarios, the Murzuq dependence sensitivity and the influential-record changes.

**Structural review.** The split held: estimands agreed before code, analyses by Codex, independent
recomputation and prose by Claude. Two assumptions were exposed. The Murzuq "tenth" depends on treating
cuttings within a well and formation as independent (block weighting gives about 0.4), so the paper now
states that dependence alongside the limit. The 25 Myr decline, earlier described as fitting poorly, has
admissible allocations that pass, so only the 10 Myr decline is reported as failing over the recorded
supports. Evidence changed Q1 (M3 now has a quantified frontier: 8–12-fold rarer earlier records for
444–452 Ma under primary units) and Q2 (pivotal ages: the interval search treats supports as
independent rectangles, so section-level ordering for Yea and Bathurst is the next lever). The
structure serves the next step, Codex's semantic review against `manuscript/estimands.md`, after which
Loop 3 can close.

## 2026-11-07: GPT-6 Pro stage 2 implemented and independently checked (Codex)

Barry relayed Claude's 7 November stage-1 closure and the stage-2 handoff in Codex chat.
Codex agreed `manuscript/estimands.md` before implementation, with explicit scope for
retrospective frontiers, interval-support feasibility and deterministic shared-boundary scenarios.
The full delivery and reproduction record is `audits/2026-11-07-stage2-handoff.md`.

- Canonical B0 now includes K12 through an executable membership adjudication, with the former
  inventory an explicit exclusion variant. The builder reads committed name classifications,
  replacing its dependency on ignored delegate outputs. A new check exposed E4-only tracheid rows
  admitted to B1; B1 now requires E3 or E5. B2 primary bounds are unchanged. West Junggar is aligned
  across fossil and effort records; region-stage B2 has 19 units and a 432.38 Ma constant bound.
- The added frontier varies early recording intensity, candidate age, unit rule and assumed
  diagnostic delay. It is retrospective compatibility arithmetic, not a fitted intensity or a
  joint confidence region. Time-by-well and composite block sensitivities retain Murzuq's local,
  sustained and age-model-conditional scope.
- The interval implementation exhausts event cells and all cutoff inclusion masks. Independent
  permutation enumeration and witness recomputation checked the central algorithm. Negative
  results concern nominal conditional-age non-rejection within the encoded supports; no calibrated
  latent-age search test or biological-history rejection is adopted.
- Shared boundary scenarios move cutoffs, mapped fossil supports and effort coherently, without
  geological probability priors. Fixed published maxima, conditional fractional mapping and the
  published stage-base-plus-uncertainty rule remain separate comparisons.
- Under the standing authority for routine dataset deposits, Codex published the exact CC0 PBDB
  snapshot at DOI `10.5281/zenodo.24028289`; this is an input archive, not a paper release.
  Anonymous retrieval verified both compression and raw checksums. Clean tracked-file reproduction
  distinguishes derived results, raw rebuild and private source checks.
- Source checks support C45–C47. C48–C52 record the new analyses provisionally. Existing numerical
  quotations, generated tables and data-driven figures were refreshed for the category/region/seed
  corrections. Claude retains full new-result narrative integration and the final semantic review.

**Structural review (Q1/Q2/Q5).** Source channels and diagnostic-event codes cannot substitute for
executable category membership. Allocation quantiles and failed finite searches cannot establish
interval-wide incompatibility. A correct local source rebuild also cannot establish public
reproducibility without immutable raw inputs. The new membership contract, finite feasibility
algorithm, archive/fetch targets and case-specific value bindings address those exposed assumptions.
The structure now serves the next scientific decision: which age–intensity–diagnostic combinations
the record permits, with the uncertainty in geological identity and ordering still visible.

## 2026-11-07: GPT-6 Pro review actioned, stage 1; Oman-inclusive B0 canonical (Barry; Claude)

Barry, in Claude chat on 7 November: "I commissioned a detailed review from GPT-6 Pro that should also be
incorporated and actioned, in collaboration with Codex." Claude triaged all ten action areas
(`audits/2026-11-07-gpt6pro-triage.md`), accepted each after checking it against sources or frozen
outputs, and split the work: Claude the source accounts, cross-product rewrite and rendering; Codex the
inventory rebuild, new diagnostics and public reproduction.

- **M1** (Claude): the paper now states the published preservation-control argument and limits its
  claim to the absence of a quantifiable frame (`audits/2026-11-07-m1-rationale.md`).
- **B0** (Claude, accepting the review and Codex's membership audit): the Oman-inclusive inventory is
  canonical, the former inventory an exclusion sensitivity, and no spore-to-body lag or delay is stated in
  either direction. This supersedes the 2026-11-05 choice to report Oman only as a sensitivity: the
  omission was an assembly error against a declared definition, not a choice about the category.
- **Allowed claims** (Claude, for Codex's agreement): `manuscript/estimands.md` states what each analysis
  bounds and the phrasings not allowed; both agents change it before changing prose or code.
- **Recording rate:** the body-record history is the rate of recorded, identifiable occurrences, not
  fossilisation; the paper no longer ranks clocks.
- Codex's review C closure wording items are integrated, and C24, C28, C31, C33, C40 and C41 are promoted to
  supported on Codex's independent check (`audits/2026-11-07-review-c-closure.md`).

**Structural review.** The two reviews converged on one weakness: corrections made locally did not
propagate to every rendering, and the numerical checker cannot see a changed noun. `estimands.md` is the
structural response: a single statement of allowed claims, upstream of the ledger. The exposed
assumption was that our account of a published argument (M1) was complete; source accounts of the
calibrations need the same primary-source check as numbers. Loop 3 stays open for stage 2 analyses.

## 2026-11-07: Review C closure check and evidence-reference repair (Codex)

Barry relayed Claude's response and instructed that closing messages use the new `Next:`
convention. Codex checked the revised paper against the evidence with separate numerical/methods
and B0-membership audits. The membership review accepts the single Katian Oman unit under
the declared category and excludes the Hawaz sheets/cluster on identity grounds. The primary
Oman report's Caradoc age and the later synthesis's Katian assignment remain distinct.

Claude retains manuscript and scientific ledger integration. The closure review identifies
remaining summary wording that turns conditional older bounds into dated biological events;
Loop 3 is not yet closed. Codex repaired the ledger's obsolete commit references after the
privacy-history rewrite by matching rewritten commits and checking identical evidence objects,
then checked the corrected R5 addendum before refreshing C42/C43. No numerical value or claim
status changed, and no private history was restored.

**Structural review (Q1/Q2/Q5).** An event channel is not a body-membership rule: inspecting
all E2 rows plus their candidate primary sources resolves the Oman/Hawaz distinction without
silently selecting favourable endpoints. The ledger checks numbers but not the interpretation
of a bound in summary prose. Commit existence in an old checkout also fails to establish that
provenance is reachable for a new reader; the repaired ledger passed a fresh-clone check.
The next tranche is Claude's bounded final integration, with category, age and unit assumptions
kept explicit and no new model or external data request required by this review.

## 2026-11-05: Review C adjudicated and integrated; Oman fragments as a declared B0 sensitivity (Claude)

Barry resumed the research on 5 November through the Board Messenger, relaying Codex's review C, and
said: "Take your next turn." Claude accepted every review C finding after checking each against the
frozen outputs (`audits/2026-11-05-review-c-adjudication.md`) and integrated them into the ledger, the
four renderings and the figures.

- **B0 and the Oman fragments.** The declared B0 ("accepted land-plant macro- or mesofossil",
  `docs/plan-loop3.md`) admits the Katian Ghaba-1 sporangial fragments, which the build omitted.
  Rather than redefine B0 after seeing results, both inventories are reported: frozen (C28) and with
  the fragments (C40, `models/f3/loop3/oman_sensitivity.py`). The paper no longer calls the B0–spore
  separation an observed lag.
- **Borenshult.** The rubric's recommendation is adopted for the paper's account (S2.4, C42–C44); the
  spore compilation and frozen readings are unchanged, and Fig. 1 shows the describing authors'
  reading beside the compilation.
- **Wording.** ρf ≈ 0.09 restricted to H0c; QSIM described as a minimum ratio; all age treatments
  shown for shape diagnostics; suppression and delay magnitudes described as illustrative and minimum.

**Structural review.** The structure served: the ledger made every changed number traceable, and the
additive data interface let Codex add Borenshult readings without touching frozen inputs. The exposed
assumption was that an implementation (the E3–E5 tail) matched its declared category; nothing checked
that. Declared categories should carry an executable membership test against the observation channels.
Evidence changed Q1: the land-plant check is now a demonstration of oldest-unit dependence, not a lag
estimate. Loop 3 stays open for Codex's bounded closure check of C24, C28, C31, C33, C40 and C41.

## 2026-11-05: Review C and additive Borenshult alternatives (Codex; handoff to Claude)

Barry asked in Codex chat: "Okay, back to our research. You're up next: review C of the manuscript,
the Fig. 3 reading in data/units, the screen rerun and the rubric scoring."

Codex's review is `audits/2026-11-05-review-c.md`, with independent methods and source-rubric
audits beside it. Claude retains ownership of the paper, ledger and figures under the agreed
split. Review C requires revisions; it does not close Loop 3 or promote provisional claims.

The published Figure 3 and Figure 4 definite-only readings are recorded separately in
`data/units/borenshult_review/`. This additive interface preserves the frozen main/inclusive
inputs and the six-versus-five conflict at 41.1 m. Possible-only identifications remain
unresolved and cannot enter a zero denominator. A third, reviewer-proposed concordant subset
also excludes the conflicted 41.1 m sample from binary trials; it is not globally adopted.
The new homogeneous independent screen is
resource triage with all older exposure granted, not a fixed-459.1 Ma test or a qualified
fossil-absence result. No geological age-depth model or crown minimum is adopted.

**Structural review (Q1/Q2/Q5):** keeping source alternatives outside the nested frozen readings
lets us compare them without invalidating earlier qualifications. The single claims ledger
catches numerical drift but does not catch a ratio described as a percentage, a model-specific
product generalised to another history, or a conditional endpoint described as an observed
biological lag. The stored recovery-shape diagnostics also require all declared age treatments
to be shown: constant recovery's apparent adequacy depends on age allocation. Those are explicit
review findings, with required changes across all renderings.
The shared trilete rubric records evidence by dimension, not a summed score that can convert
author confidence into a crown-node assignment. Claude's adjudication and manuscript integration
are next; research questions and Loop 3 remain open.

## 2026-11-02: Loop 3 sprint C delivered (Claude)

Barry returned the work to Claude in chat on 2 November ("Back to you."). Claude adopted Codex's review A
and sprint B without reservation, after re-deriving the two headline numbers by hand. For crown
vascular-plant members, (426.7 − 393.47) × 0.05^(−1/48) + 393.47 = 428.84 Ma. With pre-426.7 Ma recovery
reduced tenfold, the suppression value is 448.10 Ma. Claude then rebuilt `manuscript/`:

- **Main text** leads with the clock disagreement and what a maximum claims. It reports one result per
  maximum: 515.5 Ma is untestable from the sampled record (affinity, not absence), 459.1 Ma has one
  conditional quantitative test, and 431.2 Ma is examined by the positive body record. It closes on
  what follows biologically: an older, sparsely recorded early flora is allowed but not required. A
  table states which conclusion rests on recovery assumptions and which on character-to-lineage
  mapping. Internal codes, loop history and outside requests are out of the main text.
- **New point from the existing frozen output.** The Murzuq limit constrains delivered encounter:
  H0c × ρ stays near 0.09 across delivery (0.091, 0.182, 0.364, 0.910). The comparison therefore excludes
  abundant, well-delivered Late Ordovician trilete producers, but cannot separate rare producers from poor
  delivery. The earlier wording ("abundant producers") overstated this.
- **Figures.** Four new or redrawn main figures: the problem, evidence by region and age, body-record
  bounds with a consistent age axis and all three clock comparators, and the plain-language
  specimen-to-node chain. Codex's reviewed figures move to the supplement unchanged.
- **Supplement** (S1–S8) holds the Murzuq model and qualification, the QSIM calculation, the affinity review,
  the endpoint derivation and every body-record sensitivity table (generated by script, not retyped), the
  specimen-to-node pilot, the superseded analyses and reproduction steps.

**Structural review (Q1/Q2/Q5):** the reconstruction changes no result; it changes what the paper is
about. The positive record and the single spore test now answer one question: how far the record can
see into an interval of sparse, poorly recoverable plants. The exposed assumption is that recovery
before the oldest find cannot be tested from within the record. That is now the paper's central
limitation rather than a caveat. Loop 3 remains open for Codex's review C; release remains Barry's.

## 2026-11-01: Loop 3 review A and sprint B delivered (Codex)

Barry returned the work to Codex after Claude posted the Loop 3 brief and pilot (Board 106,
message 2809). Under the authority quoted below, Codex adopted `plan-loop3.md`'s revised design
and completed the positive-record tranche; `loop3-design.md` and `loop3-results.md` govern its
methods and interpretation. Claude retains the main-paper/supplement reconstruction next.

- The absence-rate admission gate does not govern every positive-occurrence estimator. Use exact
  conditional endpoint inference under fixed recovery histories, with a conservative age envelope;
  report the estimates and their sensitivities without inherited F3 qualification.
- Replace the pilot's numerical interpretation. Source review corrected material matching and
  collection/bed pseudoreplication; methods review identified stage-total/per-Myr double weighting,
  unsupported pooling of confidence limits and profiled-shape boundary dependence.
- Primary units are locality–age proxies, with collection, locality, region–stage, age, source and
  geographic sensitivities. Preserve uncertain material and older rejected/non-embryophyte records
  explicitly. Neither PBDB labels nor taxonomic exclusion establish a searched fossil absence.
- A spore minimum challenges equating the B0 body-recovery endpoint with embryophyte origin; it
  does not supply a known origin or a preservation lag transferable to B2. Fixed-delay scenarios
  remain assumptions.
- The observed sequence can reject some recovery shapes within its range. A complete retrospective
  stage-break grid separately exposes recovery before the first possible occurrence: main B2's
  flat-history rule moves from 428.84 to 448.10 Ma at 0.1 pre-426.7 Ma recovery, with unchanged
  within-record shape; 0.01 has no bound through 469.4 Ma. This is sensitivity, not selected or
  simultaneous 95% inference, nor validation of a clock posterior.
- No new measurements, author assistance or outside requests are part of the next step. The next
  step is the authorised manuscript reconstruction from these existing results and sources.

**Structural review (Q1/Q2/Q5):** positive-record inference answers a question that the empty-rock
admission framework did not, and improves the paper beyond an account of non-admission. The
source-linked inventory, an exact small estimator and explicit recovery/history sensitivities
separate data defects from assumptions that remain unidentified. The result survives transparent
source qualification; it does not need to be suppressed because some assumptions fail. Independent
source and methods reviews changed both the numerical result and its biological interpretation.
Loop 3 remains open for Claude's reconstruction and Codex's paper review. Frozen F3 and R artefacts
are unchanged, and release remains Barry's decision.

## 2026-11-01: Loop 3 brief (Barry)

Barry, Claude chat, 1 November 2026 (exact quotations; the full message is in the session record):

- **No outside help.** "For this project, please work on the assumption that we will not receive
  additional measurements, sampling logs or other help from the original authors or outside
  specialists." "Please don't send the existing requests on my behalf." `AGENTS.md` and
  `data/units/loop2/m1-m3/requests.md` are updated accordingly.
- **Manuscript.** "I'd like a substantial reconstruction of the narrative, not just a lighter edit.
  Start with the biological problem and why it matters". Rigour and the audit trail stay, with "the
  detailed machinery in a proper supplement and the supporting repository materials".
- **Macrofossils.** "I would like you and Codex to explore a substantive occurrence-based macrofossil
  analysis for this paper, using the evidence we can actually assemble." A complete inventory of
  searched-but-empty rocks "is needed for the specific absence-rate approach you have developed; it
  is not necessary for every method of estimating a first appearance." Simulated poor coverage "is a
  reason to examine and communicate sensitivity, not automatically a reason to suppress every
  conditional estimate."
- **Authority.** "use your joint judgement to develop and carry out the next tranche, including the
  analysis, a reworked manuscript and your usual critical review of each other's work. You don't need
  to come back to me for routine decisions; as always, external correspondence and public release
  remain with me."

This reverses, for body fossils, the 2026-10-28 rule in `plan-f3.md` that made E3–E5 synthesis only.
Claude's proposed plan, with its challenges to the brief, is `plan-loop3.md`, for Codex's critique.

## 2026-11-01: Claude endorses the Loop 2 close

Barry, Claude chat: "Codex has responded, back to you." Claude checked the close against the
frozen outputs and sources (`audits/2026-11-01-loop2-close-claude-response.md`) and endorses it
without reservation on any claim. Codex's corrections to the primary H0c (0.0910 in the frozen
primary row), the D=4 counterexample, the Stage 4 age and the QSIM source contract all hold.
QSIM stays exploratory because its units are inferred from taxon marks under a study-level
non-detection, not because h is declared. No new decision on scope; Loop 3, release and any
external requests remain Barry's.

**Structural review:** the reversed-role pairing worked: the counter-review caught five
overclaims in sprint 2 before they reached a release candidate. The exposed assumption is
procedural, not scientific: corrective claims were asserted from memory of a check. Each
corrective claim now cites its row, page or receipt. No question's status changes.

## 2026-11-01: Loop 2 closed after Codex's review and repairs

Barry asked Codex to check Claude's Board updates and repository, critique sprint 2, and resolve
outstanding work before closure. Codex reviewed `2133389`/`cb70b36` and Board 2791–2793, using
independent statistical, QSIM-source and affinity reviews. `loop2-close.md` records the resolution.

- The 99 QSIM marks are correct, and the random-lower-bound argument is valid under its model.
  Its historical co-ascertainment and independent target-detectable units are not demonstrated.
  Adopt the calculation as exploratory, not a new empirical confidence bound or admitted primary
  frame. It bounds a minimum; D=2/4 rows are heuristic. The single-study manuscript branch applies.
- Correct primary Murzuq H0c/H0 at 459.1 Ma to 0.0910/0.1835, the values already in frozen outputs.
  g denotes indigenous encounter intensity; conditional windows do not imply constant-history
  compatibility. Qualification and all frozen files remain unchanged.
- Preserve the main Cambrian E2 reading and the expressly assumed inclusive alternative.
  Withdraw unsupported circularity and definitive affinity-rejection claims, distinguish source
  dates from ICS conversion, and retain Argentine 7999's named-reading outcomes.
- Correct Hanadir to separate TAYM-4 material, withdraw undocumented exhaustive reference-search
  claims and specimen-count readings of taxon prose, and add the missing specimen-to-node pilot
  synthesis. Re-render all dependent manuscript artefacts and update source/claim/package ledgers.

**Structural review:** the paired sprint delivered a complete private research package after
counter-review narrowed its external inference. It exposed both a useful marks-based method
and the observation contract needed to apply it. The existing versioned outputs supported
correction without re-running R or altering frozen qualifications. Q1/Q2 remain open scientific
questions; Loop 2's implementation/review tranche is closed. The next priority is a bounded
microscopy/ascertainment and matched-count evidence request, not another unconstrained model or
an automatic further sprint. Barry retains external contact, public release and submission.

## 2026-11-01: review 1 and Loop 2 sprint 2 (Claude)

Barry, in Claude chat: "Back to you for review, and your sprint (if ready)."

**Review 1** (`audits/2026-11-01-loop2-sprint1-claude-review.md`).
- **Sprint 1 stands.**
- **Independent reproduction.** The four no-transfer break-even thresholds reproduce exactly in a
  separate implementation, and the 37 tests pass.
- **Corrections:**
  - name the chronology behind the H0c match;
  - Claude's v2 caving wording overreached.
- **The QSIM-801 gate is reversed in part.** Vecoli et al.'s own examination supports a conservative
  persistent-floor bound with marks as a lower-bounded denominator. Le Hérissé et al.'s counts stay
  unused.

**Sprint 2** (`loop2-sprint2-results.md`).
- **QSIM-801 bound.** θ < 0.031 at h = 1. It is reported as an unqualified empirical bound, not a
  replication.
- **External dispositions.** Röstånga-1 and Caspalá are younger than 459.1 Ma. No counted reference
  share is held.
- **M1.** The Cambrian Stage 4 forms are not E2 under main, on all three describing sources. M3 stays
  at drafted requests.
- **Private manuscript package.** Rendered. Release and submission remain Barry's decision.

**Structural review.**
- **The structure served.** The v2.1 ownership split, the frozen receipts and the claim ledger let
  sprint 2 build a new frame without touching sprint 1 or Loop 1 files.
- **Assumptions exposed:**
  - The count gate equated "no reported denominator" with "no bound". A lower-bounded denominator from
    the same examination is enough for a floor test.
  - The reference comparison for any share bound is the programme's weakest link: published Llandovery
    trilete abundances are qualitative.
- **Questions changed.** Q1 now names a counted reference share as its decisive observation. Q2's M1
  occurrence route loses source support.

## 2026-11-01: Loop 2 sprint 1 delivered for Claude's review (Codex)

`loop2-sprint1-results.md` records the completed v2.1 tranche: the 164-entry observation audit,
protocol-limited count-share method, structural non-identification result, 36 frozen-engine
sensitivities and 5,760 joint delivery/contamination/chronology comparisons with 384 break-even
entries. The joint grid was committed before computation (`2fe6bef`). Independent review
reproduced the decisive likelihood root using separate numerical integration and corrected
extreme-effort and impossible-zero-effort cases in the count-share implementation.

- No empirical count-share design is admitted. No new primary result is released or given
  inherited qualification; the original Loop 1 inputs, engine and evidence are preserved.
- The joint model identifies only combinations `a=rho*g*f` and `b=kappa*(1-g)`, with further
  confounding when all age-exposure indicators equal one. Its constant indigenous-intensity
  estimand differs from the flexible H0 mean. Comparison contours are not confidence regions.
- For the short 459.1–462.6 Ma window, equal delivery and independent stage ages require
  `g>0.9559` to reject reference-level indigenous intensity under the no-transfer convention.
  Shared midpoint ages leave zero exposure in that interval. These sensitivities narrow what
  can be called robust; they do not estimate reference contamination or chronology probabilities.
- High transfer assumptions conflicting with the older zeros are flagged as model conflict,
  never described as evidence supporting an old origin.

**Structural review (Q1/Q5):** keeping protocol, estimand, identification and qualification separate
has exposed the useful next evidence: matched counts/effort, contamination-transfer information
and finer correlated dating. The versioned Loop 2 outputs support that work without destabilising
the frozen benchmark. No source-recoding or broader model framework is needed. Claude reviews
this tranche before sprint 2's external-source attempt and private manuscript package; Loop 2
remains open. No outside contact or public release was made.

## 2026-11-01: Loop 2 sprint 1 starts under v2.1 after the count gate (Codex)

Barry instructed: "Claude has critiqued and updated the plan on the Board. Check his changes,
resolve anything outstanding, and then proceed with sprint 1." Codex reviewed Board 2774 and
`309074f`, accepted the revised division of work and recorded the source/method gate before model
implementation (`audits/2026-11-01-loop2-count-gate.md`).

- Murzuq has per-sample aggregate palynofacies fractions, but these do not pair separate trilete
  and cryptospore counts under common effort. QSIM's 20-sample taxonomic search and 42-sample
  percentage tables have 18 exact depth matches, without demonstrated shared preparation/effort.
  Neither admits an empirical share bound. The 695.7-ft 10.4% value is *Micrhystridium*, not
  cryptospores (Q5).
- The conditional count-share method is developed and checked for a future documented protocol;
  Saudi empirical extraction/application remains sprint 2. Unknown effective effort approaching
  zero makes relative output unidentified. No fictitious 6,000-spore denominator is permitted.
- Caving into older cuts and contamination of the reference cuts are distinct. Direction alone
  does not link their magnitudes. New robustness calculations are labelled unqualified sensitivities
  or identification limits, preserving the frozen primary results and receipts.

**Structural review (Q1/Q5):** the count gate prevented a primary-text percentage from becoming a
false counting denominator. The model and evidence remain separate, and the required count-free
branch still aims at a new quantitative identified region/break-even result. No new empirical
statistical claim is adopted by starting this sprint.

## 2026-11-01: next paired sprint proposed, with roles reversed (Codex)

Barry requested more ambitious plans and specified: "Then you implement sprint 1, after which
Claude critiques and does sprint 2, and then you critique. Reverse order!" (Codex chat, 1 November).
`sprints-loop2.md` v1 is Codex's proposal for Claude to critique and update before implementation.

- **Sprint 1, proposed:** reconstruct the per-material observation/counting bases; determine whether
  a cryptospore-relative-output model is identified; quantify the effects of transport,
  contamination, chronology and well structure; qualify any new released primary results. If
  separate counts are unavailable, deliver a substantive partial-identification and robustness
  analysis rather than invented exposure counts.
- **Sprint 2, proposed:** attempt external-source replication, prioritising QSIM-801/Qusaiba with
  explicit cross-study transport; advance Cambrian affinity and M3 sampling-opportunity evidence;
  integrate the trait-to-node pilot and deliver the complete private manuscript, figures, data
  package and claim-to-evidence table. No second-frame admission or numerical exclusion is promised.
- **Adopted workflow, proposed methods:** Codex plans, Claude critiques/updates, Codex implements
  sprint 1, Claude reviews then implements sprint 2, Codex reviews, and both reconcile. Public
  release and external contact remain outside this authorisation. No Loop 2 implementation has run.

**Structural review (Q1/Q2/Q5):** the completed Loop 1 remains an immutable numerical benchmark.
Separate evidence and observation-model versions allow the next pair to test assumptions without
silently inheriting qualification. Independent source material and the full biological implication
are the intended scientific advance; if a second frame cannot be admitted, the package must say so
and identify the observation that would change that limit.

## 2026-11-01: first paired sprint and Loop 1 closed (Codex confirmation)

Barry instructed in the Codex chat: "Claude has responded. Check this, resolve the issues, and then
we close the first paired sprint." Codex checked Claude's `a40c549` response (Board 2762) and confirms
`loop1-close.md` revision 2, with two small clarifications: 13 qualified Murzuq design/ρ combinations
plus QB-CO at ρ = 1 make the 14 total; an indeterminate grain needs affirmative morphology or
producer-link evidence before it can be an E2 detection. The nominal coverage target and later
potential-screen conditioning are now stated separately from empirical qualification.
The final independent wording check also makes overlapping morphology/dissociation evidence explicit
and distinguishes uncertainty within a reading from disagreement between readings; the frozen rule's
conditions for a zero after an explicitly rejected identification remain in force.

- The coverage and E2 objections in Board 2758–2761 are resolved. The versioned E2 addendum is adopted;
  the frozen M2 reporting rule, code, numerical outputs and qualification receipts remain unchanged.
- Selected-result coverage remains "not pursued; not established". M1 and M3 still have no admitted
  absence design. Closure completes the first paired work tranche, not Q1, Q2 or Q5.
- Checks: all 392 regular-file hash comparisons across 28 qualification receipts match; computed
  declaration bindings were not rederived in this documentation-only review. All 23 source hashes,
  21 admission entries and 84 sprint-2 receipt hashes pass. Card validation gives 70 cards and no
  problems; regenerated index and matrix are unchanged. No statistical or ASR rerun was needed.

**Structural review (Q1/Q2/Q5):** separating the E2 addendum preserves the qualified M2 contract while
allowing a broader, source-faithful definition. The remaining scientific needs are differential
transport, independent source replication, and event-to-node implications. The next paired plan
will reverse the implementer/reviewer roles; its scientific choices remain proposed until Claude's
critique and the agreed version are recorded.

## 2026-11-01: Loop 2 sprint plan v2 (Claude's critique of Codex's v1)

Barry, in the Codex chat (quoted in `sprints-loop2.md`): Codex proposes, Claude critiques and updates, then
Codex runs sprint 1 and Claude sprint 2. Claude revised `sprints-loop2.md` to v2. It becomes the agreed plan
when Codex starts sprint 1 without objection, or after Codex amends it.
- **QSIM-801 is promoted to the counted test of the cryptospore-referenced M2 design.** Held sources give
  explicit trilete absence in Vecoli et al. 2017's 20 Darriwilian samples, with cryptospores in 17, and
  Le Hérissé et al. 2017's counts of at least 300 palynomorphs per sample.
- **Sprint 1 opens with a count-feasibility gate.** It builds the count-share model where counts exist,
  and cuts the Murzuq robustness work to analyses that can change a conclusion.
- **Caving is treated directionally.** It threatens the reference rate; the empty older cuttings bound its
  rate.
- **The M1 target is the Cambrian Stage 4 affinity.** M3 is reduced to drafted requests.
- **The paper's subject becomes the testability of the clock maxima.**

**Structural review.** The plan structure serves the next investigation, but v1 had placed the
relative-output model on the frame least able to identify it. Assumption exposed: the Saudi material was
assessed for its acritarch scope before its spore companion, which is held, was read. No question changed;
Q1 gains a candidate transport-light design.

## 2026-11-01: Loop 1 close, revision 2 (Claude, integrating Codex's amendments)

Barry activated Claude after Codex's amendments (Board 2758, 2760, 2761). Claude checked each against the
model and sources and accepted all of them; `loop1-close.md` revision 2 integrates them. It becomes Loop 1's
close once Codex confirms the revision. This entry supersedes the coverage and E2 items of the 31 October
entry below.

- **Coverage (agreed by both).** The qualification is finite-grid empirical confidence-set coverage against
  the 0.93 floor, conditional on passing the potential screen, with abstentions covering. The largest observed
  marginal miss proportion (38/1,000) is not a population bound. Population 95% coverage, coverage given a
  claim, simultaneous coverage and validity beyond the tested histories are not established. Codex's
  reporting sentence is adopted for all bounds.
- **Selected-result qualification: deferred** as a scope and value choice, recorded as "not pursued; not
  established". Claude's argument that it was impossible is withdrawn: conditional coverage with θ fixed is a
  frequentist target (Fithian, Sun & Taylor 2014), and the shared Gamma(k, k) well effects in
  `models/f3/units_sim.py` keep reference counts informative after conditioning (Codex's counterexample,
  arithmetic checked).
- **E2 rule (proposed, agreed in substance; Codex confirms wording).** A separate versioned addendum,
  `data/units/e2-unit-rule.md` v1, records morphology/producer evidence and reading-specific embryophyte
  affinity as two axes. Alete monads can qualify; no automatic promotion under wider readings.
  `reporting-rule.md` stays untouched because the 28 qualification receipts bind its hash. No recorded outcome
  changes.
- **Source correction.** The card and pilot C2 definition had dropped Richardson's alete monads; corrected
  against Edwards et al. (2014, pp.51–52). Logged under Q5.
- **Loop 2 framing.** The cryptospore-referenced M2 design is a changed relative-output estimand under a
  different declared assumption, not a weaker one, and it does not measure ρ. Feasibility comes first; the
  thesis's counting bases (p.35) must be kept.

**Structural review.** The structure held: the frozen, hash-bound reporting rule forced the E2 rule into a
versioned addendum, which keeps M2's contract intact and makes future E2 adapters declare their rule. Exposed
assumptions: a definition copied from our own card was trusted over its cited source, and a statistical
impossibility claim was made without checking the model's dependence structure. Q1 now records conditional
coverage as deferred, not closed; Q5 gains one case.

## 2026-10-31: Loop 1 reconciliation draft (Claude)

Barry activated Claude's reconciliation after Codex's sprint-1 review (`71d69df`, Board 2753). Claude's draft close
memo is `loop1-close.md`. It becomes Loop 1's close once Codex accepts or amends it. Items below are proposals
unless marked accepted.

- **Accepted from Codex's review:**
  - QB's qualification is H0m/H0/H1, with H0c an unqualified diagnostic;
  - a Stage 4 assignment is 514.5–506.5 Ma age support, not a point age;
  - BOR-71.1 is a secure older zero under main, in a design that fails;
  - the 35 Hawaz materials are not 35 cuttings.
- **Coverage (proposal).** Retain the bounds with the finite-grid statement, as Codex recommends.
  - The criterion is Neyman confidence-set coverage, with abstention as the trivial set. That is what
    "unconditional coverage" meant when adopted (Codex message 2496).
  - Close the selected-result target. A procedure conditionally valid on a window claim must
    condition on the empty older units that carry the evidence, so it would return trivial sets.
  - "P(this bound is wrong)" is a Bayesian question needing a prior over encounter histories. No
    such layer is proposed.
  - Claude recomputed Codex's totals exactly (529,550 claims, 3,780 misses). Misses among claims run
    from 0 at B3 to 20/60 at the B4 boundary; per quantity they are 0–3.4%.
- **E2 dispersal-unit rule (proposal; `loop1-close.md`, item 4).**
  - E2-core forms are dyads and tetrads, hilate monads and enveloped monads (Richardson 1988, the
    programme's existing cryptospore definition). They are detections.
  - E2-ambiguous forms are naked inaperturate monads, and separated monads without a hilum. They are
    unresolved under main and detected under inclusive and outlier, and never zero.
  - A pooled report counts under main only where it includes an E2-core taxon.
  - Checked against all 147 E2 outcome rows and the sprint-2 ledgers: no outcome or admission
    changes. Paraguay's *L. divellomedia* is a hilate spore (Wellman et al. 2015, Table 1). Claude's
    "naked monad" was wrong, and no inconsistency with Qusaiba exists.
- **Loop 2 direction (proposal; Barry may redirect).** Deepen M2, the only maximum the record can
  test:
  - first, a feasibility check of a cryptospore-referenced transport design on the held Abuhmida
    thesis, replacing the free ρ grid with equal relative delivery of triletes and cryptospores;
  - second, a basin from a second study.

  M1 and M3 advance by acquisition and specialist contact, which Barry sends.

**Structural review (Q1/Q2/Q5):**
- **Structure.** The interface, the declarations and the bound-receipt qualification serve a second M2
  frame or a cryptospore-referenced design unchanged. M1 and M3 lack input, not machinery.
- **Assumptions exposed:**
  - ρ dominates every quantitative result;
  - the qualification is coverage, not post-selection reliability;
  - a stage assignment is age support;
  - the monad rule was implicit in the existing cryptospore definition but had never been written
    down.
- **Questions changed:**
  - Q1 narrows to the delivery assumption and a second frame;
  - Q2 now holds M1 under inclusive as an occurrence-and-dating question;
  - Q5 logs this loop's corrected statements by both agents.

## 2026-10-31: sprint-1 counter-review, qualification scope and evidence repairs (Codex)

Barry activated Codex's review/fix of sprint 1 after Claude's sprint-2 review
(`f08afb4`, Board 2720). The review is in
`audits/2026-10-31-sprint1-codex-review.md`; joint reconciliation follows.

- **Scientific scope correction (Codex, independently checked):** QB-CO's
  H0c read-outs are unqualified diagnostics. In seven saved acceptance records,
  the selected first appearance moves younger than the simulated reference
  breakpoint, making the history nonconstant on the analysed interval. Its
  qualification scope is H0m/H0/H1; the Libyan scope is unchanged. The amended
  declaration is frozen before the new binding run. The rerun adds a boundary
  cell at H0 f*(459.1), because the original grid tested that age only at f=1
  and placed its informative boundary cells at 470 Ma. A second new cell tests
  the window at 462.6 Ma with reference-level encounter before 459.1 and zero
  afterwards; it belongs to H0/H1, not H0m. Fresh roots 20261111/12/13 separate
  calibration, acceptance and optional stage 2 from the already-reviewed runs.
  No missing/inapplicable
  constant-history test is silently counted as success.
- **Coding status:** QB main/zero remains visible only as an inadmissible coding
  diagnostic: it converts seven disputed Sandbian reports to zeros. Primary QB
  excludes them. Nonprimary variants cannot inherit primary qualification.
- **Evidence contract:** new receipts bind the active declaration, consumed
  inputs, generated units, statistical code, quantity grid and phase protocol.
  All attempts and failures are retained; complete calibration and the exact
  acceptance/stage-2 chain are checked before attaching qualification. Historical
  receipts are preserved as dated evidence and cannot certify changed code.
- **Interpretation:** MZ's approximately 0.18 bound is weighted by sampled
  exposure/reference rates. Its unsampled Sandbian gap permits a pulse with a
  larger calendar-time mean. Simulation acceptance assesses the declared 0.93
  floor; it does not prove a universal 5% error bound or conditional coverage
  among informative claims. Caving is not solved by the first-appearance rule.
- **Sprint-2 review correction:** accepting Stage 4 forms as E2 assigns them
  514.5–506.5 Ma stage support, not an observed age of 514.5 Ma. The oldest
  endpoint is not a minimum age. BOR-71.1 is a secure older E2 zero under main,
  although its design fails the screen. These corrections preserve non-admission
  while narrowing the synthesis. The E2 monad rule remains for reconciliation.

**Structural review (Q1/Q2/Q5):** separating source reports, numerical targets,
qualification scope and delivered claims exposed errors that agreement of
stored counts alone would not reveal. The existing inventory/reading separation
remains useful. Questions stay active; neither an unsampled interval nor a
rejected design proves biological absence. Repaired binding runs and their
propagation into the combined memo are recorded in the audit before handoff.

**Completed verification:** the final frozen code is `31fab51`; 239 F3 tests
pass. All fourteen current-code calibration/acceptance pairs pass with zero
shift; all 28 receipts independently reconstruct and load across Nectar/Mac.
The 168 empirical numerical rows are unchanged. The added central window cell
makes the selection limitation concrete: 20/1,000 screen-passing records miss,
but these are 20/60 non-abstentions. The result is retained under the declared
marginal criterion; selected-result confidence remains for reconciliation,
along with the shared E2 monad rule. Nectar has returned to `c3.large`.

## 2026-10-31: review and fixes of sprint 2 (Claude)

Claude reviewed Codex's sprint 2 (Board 2710) in the sequence Barry set on 31 October. Three independent Sonnet
source audits support it; the adjudication is in `audits/2026-10-31-sprint2-claude-review.md`.

- **Adopted (Claude, as reviewer):** the M1 and M3 non-admissions stand. Borenshult, Libya and Ghelli are added to
  the M1 assessment, and none is admitted. The ledger now states the decisive outcome-coding rule: a disputed E2
  form is never a zero. It also states the inclusive-reading consequence: E2 from c.514.5 Ma makes M1 an occurrence
  question.
- **Corrections (Claude):** source-reading fixes to the M1 ledger, the Samphire inventory, the Strother 2016 age
  label and the M3 locators and wording, all logged. No F3 code, M2 output or qualification changed, so no
  downstream result is invalidated.
- **Proposal for reconciliation:** declare one E2 monad rule across sources. Codex's points on sprint-1 receipt
  binding and wording are accepted and left to its scheduled sprint-1 review/fix.
- **Structural review:** the inventory/reading/design separation held up under review. Outcome coding of disputed
  forms and reading-dependent changes of question type need explicit treatment in every absence-design
  declaration. No question's status changed.

## 2026-10-31: sprint 2 source admission, evidence limits and draft synthesis (Codex)

Codex executed the second sprint after Barry's handoff of Claude's `63ca45e`
(chat, 31 October). `d17d033` froze the bounded source roster before detailed
extraction. Results and review route: `sprint2-results-and-value-of-information.md`.

- **Admission decision (Codex):** none of the seven M1 source groups supplies a
  defensible older/reference design under main, inclusive or outlier readings.
  The recovered inventories, specimen catalogue, quantitative subsamples and
  reporting gaps are retained in `data/units/sprint2/`; no unreported or disputed
  E2 outcome becomes zero. M3's bounded primary/database assessment likewise
  supplies no counted searched-rock denominator. These are source-admission
  findings, not biological absence or numerical engine failures.
- **Source correction (Codex, independently checked):** Balme's original is
  held and read, with six samples but only one Ordovician. Marine preservation
  and qualified spore language are primary evidence; the later trilete gloss
  stays attributed to 2021. The source/candidate records and six inventory
  entries are reconciled, with existing event outcomes unchanged.
- **Useful recovered reference:** Qusaiba has dyad/tetrad reports in every one
  of 37 columns, including the deepest. It is a reference candidate with an
  all-positive rate boundary and transport assumptions, not an older absence
  series. Independent raster checking matched 777 cells and 226 marks.
- **Pipeline disposition:** the development smoke passed. Active-input and
  receipt/protocol enforcement gaps are documented for the scheduled sprint-1
  counter-review. With no M1 numerical design admitted, no binding reuse,
  model repair or heavy qualification was needed in this sprint. Existing M2
  numbers remain attributed to sprint 1; the synthesis distinguishes marginal
  false-claim-with-abstention qualification from informative-claim coverage.
- **Structural review (Q1/Q2/Q5):** separate source inventories, interpretations
  and numerical designs continue to serve the programme. Recovered reports
  changed access/provenance and reference availability without licensing new
  negative trials. The decisive next evidence is independently justified
  detection transport, complete Cambrian sampling/reporting, and a megafossil
  searched-material ledger. Taxonomic adjudication alone cannot replace these.
  Q1/Q2/Q5 remain active; no clock maximum is settled by non-admission.

This completes sprint-2 execution, subject to the agreed Claude review/fix,
then Codex review/fix of sprint 1 and joint reconciliation. It does not close
Loop 1 or authorise publication/contact. No F3 model, frozen M2 result, ASR
code or taxon card was changed. Nectar was not resized or used for a new run.

## 2026-10-31: sprint 1, M2 on real designs (Claude)

Claude executed sprint 1 against Codex's v2 plan (`docs/sprints-2026-11.md`). Result note:
`docs/audits/2026-10-31-m2-real-designs.md`.

- **Designs frozen before any statistic** (`models/f3/designs/m2.toml`, commit `d426423`). They
  comprise H2, D1 and I3 within-well cuttings, Murzuq cuttings across five wells, Libyan cores across
  wells, H2 cuttings plus cores (screen only), Qusaiba with Borenshult, and Borenshult historical.
  The Libyan binary rule makes a blank *A. dilutus* chart cell a full-category E1 zero: it is the
  chart's only trilete column and the thesis's only true trilete (printed pp. 327–328).
- **Real-design settings (decision, Claude).** The first appearance is the base of the oldest stage
  any detected unit can occupy. The reference minimum is 5 units, with 10 reported for every variant.
  Cluster k is ∞ within one well and 2 across wells. The transport ratio ρ is a declared grid
  {1, 0.5, 0.25, 0.1}, never estimated. The M2 comparison is the window read-out: "a ≥ f before
  459.1 Ma, any path after it".
- **Amendment 1 (decision, Claude, before any qualification).** The screen is evaluated on the
  frame's potential, with older outcomes set to 0. On full outcomes, passing implies an empty oldest
  stage under the first-appearance rule, and conditioning on that removes the evidence the bound
  uses. This corrects the frame-selection rule in `f3-shape.md`.
- **Amendment 2 (decision, Claude, after an independent Sonnet review).** Claims are made only when
  older units are empty, so the criterion is the false-claim rate among screen-passing records
  (abstentions cover). Boundary cells at each design's own f\* give the acceptance power, and claims
  and misses are reported per quantity.
- **Result.** All 14 screen-passing design/ρ combinations qualified at stage 1 with no shift; the
  worst false-claim rate is 0.037.
  - The Murzuq cuttings bound trilete encounter after 459.1 Ma below 0.18 of the Llandovery level
    (ρ = 1).
  - They bound it before 459.1 at about the same level (0.17 over the Darriwilian, derived).
  - Reference-level encounter before 459.1 is excluded further back than 462.6–467 Ma
    (ρ = 1–0.25). Nothing is excluded at a tenth of it.
  - The absence cannot tell a crown origin before 459.1 Ma from one after it at the intensities the
    later Ordovician allows.
- **Structural review.** The structure served: declarations, adapter, a single shared screen and
  hashed receipts made 512 variants and 14 qualifications traceable. The assumption exposed was the
  screen's interaction with the first-appearance rule (amended). Q1 has its first empirical answer
  and its limit. Q2's decisive record moves from the Darriwilian to the Late Ordovician Libyan shelf.
  The transport ratio is now the quantity worth measuring.

## 2026-10-31: two autonomous sequential sprints, Codex revision for adoption

Barry instructed Claude to draft two substantive sprints, Codex to critique/revise,
then Claude to execute sprint 1 and Codex sprint 2, followed by Claude's review/fix
of sprint 2, Codex's review/fix of sprint 1, and reconciliation (chat, 31 October).
This authorises the execution sequence without routine scope re-approval; external
contact, public release and spending beyond authorised resources remain separate.

Claude proposed M2/pipeline followed by M1/M3 (`9443f4b`, Board 2678). Codex agrees
that division, with v2 in `sprints-2026-11.md` for Claude to adopt at sprint start.
Material revisions: unsupported H2 core rates need an explicit transport scenario;
caved positives cannot securely date indigenous first appearance; one-well
heterogeneity and formation chronology need declared assumptions; literature and
occurrence databases are source leads, not negative-trial denominators. Sprint 2's
source programme is bounded, and can deliver source/identifiability limits even if
no numerical design qualifies. Repairs invalidate affected downstream evidence;
qualification-budget exhaustion is not biological non-identifiability.

**Structural review (Q1/Q2/Q5):** larger owned tranches replace repeated small
handoffs while retaining source-to-result evidence and the two counter-reviews.
No new biological reading, binary outcome or empirical result is adopted by this
planning revision. Current repairs were inspected and the prior injected
zero-exposure reproducer now rejects its malformed record; full sprint counter-
review remains scheduled. The next action is Claude's sprint 1 against the revised
plan, with acceptance or any material objection recorded at its start.

## 2026-10-31: Libya reports mapped; reference conflict and bounded qualification repairs (Codex)

- **Completed evidence:** 164 appendix entries have prose-scope mapping, and 158
  chart rows have reproducible species/productivity reports. Independent raster
  checks agree with all 134 target-column states and 158 marine-presence states;
  153 exact appendix joins are retained. There are 52 *A. dilutus* chart reports,
  including 51 exact appendix matches, none on an appendix-confirmed core.
- **Source conflict, not adjudication:** the prose-positive E1 7287-ft core has a
  blank target cell; I3 4600/4640 marks contradict the sole-Cr3-specimen wording.
  Fourteen appendix entries lie in explicit barren scopes, while three I3 Ash
  Shabiyat rows show marine recovery with a possible-caving qualification. The
  existing interface stays at 49 blocks/294 outcomes; no new binary rule is adopted.
- **Proposed next design (Codex, pending joint adjudication):** H2 within well,
  with explicit core/cutting transport and shared chronology, followed by a
  separately declared core-only cross-well scenario if its reference is justified.
  This follows completeness of recoverable evidence, not a fitted F3 verdict.
  Details: `audits/2026-10-31-libya-event-map.md`.
- **Review:** accept the scoped screen, named invalid-state repairs and measured
  ASR convergence/retention results. Request the bounded corrections in
  `audits/2026-10-31-qualification-repair-review.md`: precise selection/conditional
  acceptance specification; cross-field zero-exposure consistency; constant-path
  versus H1 threshold label; correct independent-chain MCSE pooling. Accepted ASR
  precision/rounding conclusions survive; existing traces suffice. Model repairs
  and scientific readings remain Claude's.
- **Structural review (Q1/Q2/Q4/Q5):** the separate source tables expose rather
  than erase disagreements between prose, charts and physical samples. Q1 now
  has a concrete comparison to adjudicate; Q2's core reference rests on a specific
  unresolved source conflict; Q4's persistence conclusion survives measured
  uncertainty; Q5 records internal conflicts without alleging wider propagation.
  No question is answered. No author reply or new unconditional ensemble is needed
  to progress to the declared-design stage.

## 2026-10-31: screen scoped, frame selection conditional, state tags checked, ASR precision measured (Claude)

Responds to Codex's review (`audits/2026-10-31-screen-and-persistence-review.md`; Correspondence
2634–2638). All of its findings are accepted.
- **Screen** (Claude). The bound 2 m f r holds only in the homogeneous independent design: fixed
  reference membership, one comparable class, independent units. In that design it equals the
  engine's statistic at each class ceiling and is never weaker below it (`models/f3/test_screen.py`).
  The previous entry's claim that nothing in the real test can raise it is withdrawn, and is struck
  through in that entry's audit. Every screen row now names its frame, reading, reference
  conversion, design, class ceiling and target. Borenshult's verdict stands within that design:
  - no in-frame reference under main;
  - under inclusive, H0 cannot exclude f = 1 under either reference conversion;
  - under the optimistic conversion H1 is not ceiling-limited (constant-path threshold 2.36; full
    H1 engine bound 2.59, corrected after Codex's second review), which says nothing about absence.
- **Frame selection** (decision, Claude). Binding claims are conditional on passing the screen.
  - The binding qualification applies the same screen rule in every replicate, analyses only the
    replicates that pass, and must reach 0.955 coverage conditional on passing. It reports the pass
    rate.
  - For frames with independent data this covers a fixed candidate list that reports every passing
    frame, or a non-anticipating search order. It does not cover picking the most favourable among
    already-inspected passing frames. *Narrowed after Codex's second review.*
  - Frames that share units are simulated jointly.
  - Every examined frame is reported with its screen result.
  - The simulation is built with the first binding qualification. Stage-1 and stage-2 synthetic
    validation stay unconditional.
- **Checker** (Claude). `bound_state()` holds every scored state to the engine's invariants, so a
  renamed tag can no longer escape containment. All 66,000 current-format stored rows pass and
  re-score unchanged. 170 F3 tests pass.
- **Persistence** (Claude). `mean_returns` is split into entries and re-entries. The wording now
  says:
  - ER maps supply the paths, and ARD supplies rate scenarios only;
  - the trees have 27, 38 and 38 tips;
  - τ = 452.8 Ma is a stage-boundary scenario;
  - a node state does not date a trait's origin.

  Precision is measured with four independent chains per tree, under acceptance criteria declared
  before the run (`models/pilot-asr/README.md`, "Diagnostics").
  - At Hooper et al.'s settings the extant-tree rate chain did not converge (R-hat 1.11). Four
    longer chains do (1.006).
  - Persistence given a trilete start is 0.98 (MCSE 0.003), 0.999 and 0.99 on the three trees. The
    earlier 1.000 was a zero count.
  - The converged retention posterior on the extant tree is wider: down to 0.33 at 515.5 Ma, not
    0.52. The point estimates are unchanged.
  - Seeds alone move single-chain node frequencies on that tree by up to 0.09 (0.785–0.877 for the
    crown trilete state). Hooper et al.'s qualitative reading is unaffected.
- **Structural review (Q1, Q4).**
  - **Exposed:**
    - lack of power in a declared design is not impossibility under every observation model;
    - frame selection is part of the inferential design;
    - Monte Carlo precision of a model-derived scenario input must be measured before its decimals
      are quoted.
  - **Q1:** its next step is unchanged (Codex's Libya event map, then design comparison). The
    selection rule now travels with the first binding qualification.
  - **Q4:** persistence holds, with measured precision. The extant-tree retention scenarios are
    less certain than first stated.
- **Author contact.** Barry, 2026-10-31, in chat: "I just now sent a lightly modified version of
  your request!"

## 2026-10-31: screen scope challenged; Qusaiba and Libya inventories added (Codex)

- **Review finding, pending Claude's repair:** the homogeneous independent screen
  is correct, but it does not prove that every dependence model or history class
  is ceiling-limited. Existing-engine counterexamples give a finite H1 bound at
  ceiling 3 and a finite H0 bound under a different reference clustering. These
  are theorem counterexamples, not proposed Borenshult analyses. The prior entry's
  universal claim is therefore disputed; retain the diagnostic under its stated
  assumptions. Choosing a frame after observing its screen also needs an explicit
  selection target in qualification. See `audits/2026-10-31-screen-and-persistence-review.md`.
- **Implementation review:** all 166 tests pass and the named strict-parser repairs
  work. An injected unsupported state label still bypasses bound containment;
  no malformed stored row was identified. ASR path logic, deterministic fits and
  saved reproduction values check out; Monte Carlo precision/convergence remain
  unassessed, and entry counts, age-scenario wording and node-origin wording need
  the specified corrections. Model code and pilot adjudications remain Claude's.
- **Completed evidence:** Qusaiba adds 37 declared spore samples with 22 trilete-marked
  and 15 unmarked columns; its deepest sample is already positive and Katian.
  Libya adds 164 appendix entries with 158 chart labels and 153 exact depth matches.
  These are source inventories, not adopted binary trials. Seven candidate frames
  and 276 inventory entries now coexist with the unchanged 49 blocks/294 outcomes.
- **Structural review (Q1/Q2/Q4/Q5):** source-specific tables preserve complete sets,
  ambiguous matches and reporting conflicts without altering scientific readings.
  Exposed assumptions are reference comparability, core/cutting transport, frame
  selection and Monte Carlo precision. Q1's next evidence step is Libya event and
  productivity mapping followed by explicit within-well/cross-well design comparison;
  Qusaiba provides a separate reference candidate. No question is answered and no
  empirical exclusion is released. Author replies remain optional evidence.

## 2026-10-31: Borenshult readings kept; a design screen gates qualification (Claude)

- **Reading** (Claude, who owns reading definitions): Hooper et al.'s compression caution covers
  "the figured specimens", and the 2019 paper calls the whole Sandbian "Dalby Limestone". The
  caution therefore reaches the two Skagen specimens (Fig. 5E, 33.05 m; 5G, 34.0 m, itself queried).
  Main keeps all seven Borenshult E1 depths unresolved. No Skagen-only reading is added: no source
  holds it, and it would be chosen after seeing its effect.
- **Screen** (Claude): `models/f3/screen.py` bounds the zero-count statistic by 2 m r f, which
  nothing in the real test can raise. Borenshult fails under both readings: under main there is no
  in-frame reference, and under inclusive the bound is 3.2 against 5.99. A frame must now pass the
  screen under a declared reading before a binding grid is built on it. The shared-age cells move
  to the first frame that passes, with Borenshult's structure as their template. This replaces
  building them now on Borenshult.
- **Review repairs** (Claude, from Codex, Correspondence 2628–2631):
  - strict replicate ids and Boolean flags in `validate.py`; 166 F3 tests pass, and all 66,000
    current-format stored rows re-score unchanged;
  - the four pilot corrections: *Velatitetras* crown and secondary cryptospory unresolved,
    *Horneophyton* C3 transferred, Irish C3 conditional, review scope;
  - retention used as a scenario, not multiplied into an F3 verdict.
- **Structural review (Q1, Q2):** the unit interface carried a complete core end to end. Running
  the cheapest check first showed that the binding grid would have been wasted on this core.
  - **Exposed:** the M2 test needs in-frame reference support under main and tens of eligible
    older units. These are frame properties, not estimator properties.
  - **Q1's next step changes:** frame construction is now the critical path; no new estimator work
    is needed.
  - **Q2 gains a decisive specimen question:** the figured Borenshult triletes. Its re-examination
    is an expert flag (Barry's decision).
- **Author contact** (Barry, 2026-10-31, in chat): "Yes, worth asking them. Draft and I'll post it
  today." Claude drafted the request (`outreach/2026-10-31-rubinstein-vajda-borenshult.md`); Barry
  sends it. No reply is the default and blocks nothing. An author answer is a source and may
  define a reading; we adopt their specimen-level assessment as given, not a subset chosen by the
  screen.

## 2026-10-31: Borenshult event map and structural review (Codex)

- **Completed evidence:** 34 Borenshult physical samples now join the unit/outcome interface,
  giving 49 blocks/294 outcomes in total. Literal source reports, named reading choices,
  non-target productivity and separate age correlations are traceable. Eleven study-complement
  non-detections use the explicit 34/23 source statement; 16 E1 chart blanks remain
  `not_reported` with their reporting scope. No binary input or empirical fit is released.
- **Reading retained:** seven E1 reports remain unresolved in main and detected in inclusive/
  outlier. This leaves no positive E1 reference observation in Borenshult under main. The
  younger Skagen reports need specific adjudication because Hooper's stated concern names
  Dalby; no identification was silently changed. E2 retains two disputed Darriwilian reports.
- **Structural review:** the two-table interface still serves Q1/Q2. Two source-specific
  evidence tables preserve chart reports and conflicting age correlations without forcing
  either into a binary likelihood or a probability density. The exposed assumptions are
  positive reference support, cross-facies detectability, first-appearance selection,
  shared chronology and the trait-persistence/node mapping. These sharpen Q1's next design,
  not its substantive answer. Source gaps do not stop this mapping.
- **Review handoff:** core V1 repair accepted; strict CSV types remain a bounded correction.
  Expanded pilot links pass selected primary-source checks, with crown/secondary cryptospory,
  Horneophyton C3 transfer and review-scope wording returned to Claude (2628–2629). His
  separate ancestral-state work remains his. Full evidence and next tranche:
  `audits/2026-10-30-borenshult-event-map.md`.

## 2026-10-31: trilete persistence under Hooper et al.'s models; R under renv (Claude)

- **Analysis** (Claude Opus 5.5, under Barry's 2026-10-30 authorisation; `models/pilot-asr/`, pre-declared before the run):
  - **Reproduction:** Hooper et al.'s phytools stochastic mapping and fitMk are reproduced for X21 and X26 on all three trees, 156 of 156 node values within tolerance.
  - **Persistence:** given a trilete crown ancestor, the aperture persists along the whole path to crown Tracheophyta in 98.4–100% of maps.
  - **Retention:** a single lineage's probability of keeping trilete production from *T* to 452.8 Ma, under the fitted rates of 0.0016–0.0043 per Myr, is 0.93–0.97 at 470 Ma and 0.76–0.90 at 515.5 Ma (point estimates).
  - **Status:** P1's persistence link is supported under these models.
- **Correction recorded with the result:** the deposited timetrees date crown Embryophyta at 508 Ma (Harris and Clark dates), not at Hooper et al.'s recalibration, so the design's premise that they embed M2 was wrong. The estimands are unaffected.
- **Tooling** (Claude, endorsed by Barry mid-run: "feel free to set up a pinned renv if you deem appropriate"): R analyses get a project-local renv per analysis directory, with `renv.lock` committed and libraries ignored. `models/pilot-asr/` pins R 4.6.1, ape 5.8-1 and phytools 2.5-2.
- **Structural review (Q1, Q4):** persistence was the one link no published output could supply; a bounded re-run of the authors' own analysis settled it under their models without new tree inference. Exposed: every node statement now needs a model-conditional retention scenario, and the rates behind it are tree-averaged (dominated by the liverwort loss). *Corrected 2026-10-31 after Codex (Correspondence 2631): the retention probability is not multiplied into an F3 verdict; it defines conditional or sensitivity scenarios beside it, and fixed-rate stretches to older origins are sensitivity scenarios (2628).* M1's cryptospore persistence is not assessed. No question's status changed.

## 2026-10-30: wider scope authorised for a new ancestral-state analysis (Barry)

- **Decision** (Barry, Claude chat, 2026-10-30), answering Claude's note that settling persistence would need a new ancestral-state analysis and so widen the agreed scope: "widened scope is fine, proceed with the new ancestral-state analysis as/when appropriate. You two have my imprimatur to act as you think best, scientifically. I'm your collaborator, not your overseer, in this venture!"
- **Effect:**
  - This removes the pilot's consult trigger for re-estimating ancestral states (`docs/pilot-traits.md`).
  - It amends `innovation-scope.md`'s exclusion of re-estimation for this purpose. Joint origin inference (level 3) still needs its own design.
  - Claude claims the first such analysis on the Board: reproduce Hooper et al.'s stochastic mapping and read the branch histories that bear on persistence.

## 2026-10-30: the F3 stage-1 evidence re-scored; pilot round 2; M3 record identity audited (Claude)

- **Harness** (Claude Opus 5.5, to Codex's remaining V1 gap, Correspondence 2569):
  - stage 2 now reads the stage-1 replicate table and requires replicates 0..N1−1 once each per acceptance cell, and a summary over N1;
  - it re-scores every count from those rows under the delivered-coverage rules;
  - replicate tables are written with exact floats;
  - the test fixture is a real one-cell stage 1.
  - 163 tests pass; the smoke run's stage 2 re-scored and accepted its stage 1.
- **Specimen corrections** (Codex review, applied): the *Velatitetras* producer's C2 is `disputed`; *Aglaophyton*'s C3 without C4 is composite; branched tetrad producers are not tips in Hooper et al.'s trees; claims of first and oldest are restricted to the audited set; every row has an archived quote.
- **Round 2:**
  - `data/pilot/specimens.csv` reaches 524 rows from 30 primary sources, every quote verified.
  - `data/pilot/combinations.csv` names each combination's member rows and evidence level.
  - Within the audited set, trilete spores on branched plants with several sporangia run from the Sheinwoodian through the Přídolí (*C. barrandei*, *C. bohemica*, Lang's Perton *C. pertoni*) without tracheids shown on the same plants.
  - Tracheids on a fertile plant appear only in the Lochkovian.
  - *Nothia* gives C1 + C3 without C4 (composite).
  - *Horneophyton*'s C4 carries three published readings.
- **M3 record identity** (`docs/audits/2026-10-30-m3-record-identity.md`): contested.
  - The Homerian specimens show branching with terminal expansions that are assumed to be sporangia, with no spores and no anatomy. Their authors allowed a rhyniophytoid reading.
  - The calibration's tracheids, stomata and sterome are transferred from Lochkovian *C. pertoni*, whose placement is disputed (stem eutracheophyte or lycophyte sister).
  - *C. barrandei* predates the 431.2 Ma maximum.
- **M2's basis:** a single probable trilete spore at 48.2 m in Borenshult-1, one of the 34 depths in Codex's new frame, so F3's E1 test bears directly on M2's absence premise.
- **SCM:** Codex found that the deposit saves no mapped histories, so persistence stays unresolved. A new stochastic mapping would be a new analysis (consult trigger).
- **Structural review (Q1, Q2, Q4, Q9):** the evidence levels and combination table carried a second round without schema change. Exposed:
  - M3's basis is a transfer, and its node (total group or crown) depends on a disputed placement;
  - M2's basis sits inside the E1 frame;
  - P2 gains a lead (possible cryptospory in a probable tracheophyte) but no link.
  - No question's status changed.

## 2026-10-30: first-study Tier 2 literature acquisition (Codex, authorised by Barry)

- **Authority:** Barry, Codex chat: "Continue now with Tier 2." He asked that locked-mini or fresh-login blockers be held for his office session. All 77 targets were attempted; no unlock interruption was sent.
- **Result:** 30 new main texts plus twelve reconciled exact prior holdings make 42 available main texts. Two complete abstracts and an already-held dataset close different source kinds; one first-page partial, one supplement-only row and 30 blocked targets remain. The 92 filed assets include 33 byte-identical existing supporting/data holdings. Provenance and extent are preserved in the manifest, durable receipt and `docs/audits/2026-10-30-first-study-tier2.md`.
- **Structural review (Q1/Q2/Q4/Q5):** the existing focused status register now covers all 135 prioritised rows, with the input priorities and Tier 1 outcomes unchanged. An explicit master `abstract-only` status removes a misleading full-text implication. Exposed assumptions: a repository's year may be a deposit year; a full-text badge may deliver one page; an online/print alias or copied deposit is not a newly recovered work. The reading-library/manifest structure serves the next investigation; office save/terms actions remain separate from library requests. No empirical age constraint, frame admission, character interpretation or question status changed.

## 2026-10-30: Borenshult frame, specimen audit and validation follow-through (Codex)

- **Evidence:** 34 Borenshult analysed-sample depths are reconciled between Rubinstein & Vajda's 2019/2023 accounts and independently checked. The 2019 spore chart plots a 23-depth subset; no outcomes were inferred for its 11 omitted depths. The inventory now has five candidate frames/75 rows, with the 15-unit/90-outcome pilot unchanged. This post-2006 frame requires its own declared selection, reporting and age/dependence model before analysis.
- **Correction:** the 2002 Ghelli type section is not Pelmis Gorge. It cannot reconcile Pelmis's sample counts; the previous audit's same-section wording is corrected. Missing 2001/2007 sources remain specific Pelmis gaps, while the held Borenshult sources support further work now.
- **Independent review:** the three highlighted trait-specimen links hold. Recommended corrections for Claude are disputed C2 encoding, the composite Aglaophyton comparison, explicit placement-transfer assumptions, two missing quote records, and chronology limited to the audited evidence set. These recommendations are pending, not adopted edits to Claude's tables/specification.
- **Deposited histories:** the sole Hooper R workspace contains only a standard tree and RNG state. No saved stochastic branch paths were found; persistence remains unresolved. The inspection receipt supplements the existing extraction without rerunning ancestral-state inference. Q9 remains parked.
- **Methods:** 161 tests pass; V2–V4 and V1's labels/count bounds hold. V1 still verifies hashes without validating replicate rows against summary successes. Two injected counterexamples pass; Claude retains this bounded repair. This qualifies the earlier contract-closed claim, without disputing the stored rehearsal counts.
- **Structural review (Q1/Q2/Q4/Q5):** the existing frame/sample separation serves the next extraction. Exposed: a spore-only chart can omit analysed material; shared formation names do not prove shared collections; direct character observations can still form a composite combination. Next is Borenshult event reporting and age mapping, alongside Claude's repairs. No empirical age constraint or global trait order was established. Full evidence: `docs/audits/2026-10-30-frame-and-pilot-review.md`.

## 2026-10-30: first-study Tier 1 literature acquisition (Codex, authorised by Barry)

- **Scope:** Barry chose Tier 1 first. The scout collected 39 new main texts, ten new supporting files, two complete abstracts and a qualified component copy; three identical existing Morris supporting files were mirrored into the reading library. All 55 file entries have sizes, hashes and provenance. Input tiers and scientific files are unchanged.
- **Availability:** 40 of 58 focused rows have main texts, including one duplicate; two are abstract-only, one partly held and 15 blocked. Kanosh and Hanadir 2007 are resolved. Four reopened Tier 1 sources remain incomplete/unheld. Tier 2 and still-parked sources were not collected. The full audit and status register are `docs/audits/2026-10-30-first-study-tier1.md` and `docs/first-study-literature-status.csv`.
- **Structural review (Q1/Q2/Q4/Q5):** the existing library/manifest plus a focused outcome CSV serves the next readings. Exposed: abstract records had been treated as missing articles; a combined dating row contains two references; print/online and delivery-DOI aliases need explicit provenance. Preserve those identities, manuscript/preprint versions and copied-deposit distinctions. Acquiring a file does not establish a sampling frame or a scientific interpretation; no question's scientific status changed. The existing Barry-action/request ledgers now record only the outstanding actions for this tranche.

## 2026-10-29: pilot mapping review, published-state extraction and remaining acceptance checks (Codex)

- **Assessment:** Codex supports the trait-to-node pilot framing Barry approved. Its temporal propositions need an explicit node-to-event-history implication; an earlier trait origin on an extinct side branch does not guarantee production by an older crown. Crown-state support, transition histories and origin timing must remain distinct. Amendments are proposed to Claude in `docs/audits/2026-10-29-pilot-and-contract-review.md`; his specification remains unedited pending integration.
- **New source evidence:** `data/pilot/hooper2026-asr/` extracts both crown nodes, X21/X26, all four methods and three trees, with 208 reported values and 32 explicitly omitted state columns. Archive hashes and all 76 master/ASR character comparisons pass; an independent R/ape check verifies all six nodes and every extracted value. X21 consistently favours a trilete aperture, but the zyg-tree ARD X26 result favours dyads (0.701) and assigns zero to the pooled monad state. The independently modelled characters do not unanimously establish trilete monads or a joint ancestral phenotype. No ancestral states were re-estimated.
- **Specimens:** the held *C. pertoni* DE41 material links spores and anatomy but lacks the two-sporangium branching required for direct C1+C3+C4. *C. barrandei* D552a,b directly links C1+C3. *Ficoiditheca* supplies a useful held branching/dyad candidate, with an explicit conspecific bridge for the dyad diagnosis. Keep attached-specimen evidence distinct from taxon reconstructions. The Pridoli central-strand wording is not a demonstrated claim of observed tracheids; no Q5 error is inferred from it.
- **Methods:** all 159 F3 tests pass and the principal third repairs work. Injected counterexamples still bypass stage-one count/label consistency and successful-bound containment; a NaN receipt component can also pass. These are remaining checks for Claude, not observed errors in the saved ensembles. Retain the global shift and 0.955 target; binding validation still awaits the real frame and the remaining repairs.
- **Structural review (Q1/Q2/Q4/Q5/Q9):** the pilot can assess conditional biological claims without a joint origin model, but must state the implication from a node to the tested producer history. Published marginals and specimen transfers expose different uncertainties. Total group includes crown, so the *Cooksonia* question is record-specific transfer, not a contradiction of those labels. The bounded audit and extraction serve the next step; Q9 stays parked, and the separate reference scout owns acquisition while Codex retains frame reconciliation.

## 2026-10-30: pilot specimen evidence from held sources; a Q5 correction (Claude)

- **Evidence table** (Claude Opus 5.5 with `gpt-6.1-sol` extraction): `data/pilot/specimens.csv`.
  - 283 rows of C1–C4 observations from 17 primary sources, 15 of them landed by Barry's reference scout or already held.
  - Every quote was verified against its text by script. The quotes stay in the git-ignored library; the table holds their hashes.
  - Claude adjudicated the rows the pilot turns on.
- **Results:**
  - direct C1 + C3 by the middle Sheinwoodian (*C. barrandei*);
  - the oldest in situ tracheids on an isolated unbranched axis (late Ludlow);
  - direct C1 + C3 + C4 on one specimen first in the Lochkovian (*Tortilicaulis offaeus* HD743/01);
  - direct C2 + C3 in a branched tetrad producer, with C2 contested by the authors' own alternatives;
  - C3 without C4 in *Aglaophyton*.
  - Combinations cluster in the Lochkovian mesofossil window. That is observed order under a preservation window, not acquisition order.
- **Q5, failed against its source:** Morris et al. (2024) describe the late Ludlow tracheids as in branching stems terminated by *Cooksonia*-type sporangia. Edwards & Davies (1976) isolated them from an unbranched 10 mm axis with nothing attached. The *Cooksonia*, rhyniophytoid and *Tortilicaulis* cards are corrected; `cards.py check` passes.
- **Hooper et al.'s main text:** its conclusion calls the trilete monad robust across models, while its results report an enveloped ancestor under ARD on both fossil trees. The robustness holds for the aperture only. The Homerian *Cooksonia* cf. *pertoni* sets two calibrations (426.9 and 431.2 Ma).
- **Structural review (Q2, Q4, Q5):** the pilot's evidence levels absorbed the new sources without schema change. Exposed: M3's record identity rests on transferring Lochkovian anatomy to Wenlock bodies; trilete spores do not supply it under Hooper et al.'s reading; and P3b's specificity depends on eophyte placement. No question's status changed; Q5 gained a case.

## 2026-10-29: trait-pilot design adopted; harness contract closed (Claude and Codex)

- **Pilot** (Claude Opus 5.5, integrating Codex's review L1–L5 and A1, Correspondence 2565): `docs/pilot-traits.md` is the adopted design.
  - A node statement needs an older node to entail event-specific production. Crown state, persistence and origin timing are scored separately, as supported, contested, contradicted or unresolved.
  - P1 is broken only by a sourced reading placing trilete production after the crown.
  - M3's fossil basis is split into record identity (the Homerian *Cooksonia* cf. *pertoni* transfer in Hooper SI Table 4) and proxy specificity.
  - Specimen combinations carry direct, composite or transfer evidence levels.
- **First result, from Codex's extraction of Hooper et al.'s deposited outputs** (`data/pilot/hooper2026-asr/`):
  - every output reconstructs a trilete aperture at the embryophyte crown;
  - one output (ARD, eophytes as stem-tracheophytes) reconstructs a dyad dispersal unit there;
  - P1's crown state is supported for the aperture, P2's is contested, and persistence and timing are unresolved for both.
- **Harness** (Claude, to Codex's V1–V4, Correspondence 2564): `d2d34a0`.
  - Stage 2 derives every verdict from counts bound by hash to the stage-1 evidence.
  - Delivered *f\** coverage requires bound containment.
  - Every receipt part must be finite.
  - δ is a tuning proposal. 161 tests pass, and the stored runs are unchanged.
- **Structural review (Q1, Q2, Q4):** the pilot now scores links rather than whole mappings, so a missing transition history shows as unresolved, not as support or refutation. Exposed: persistence from the node to the sampled interval is an assumption in every node statement, and no published output supplies it. No question's status changed.

## 2026-10-29: first-study literature targets; parked requests reopened where needed (Barry, Claude)

- **Request** (Barry, Claude chat): list the closed papers important to the first study that are not held, including any not yet listed, as a target for the reference scout he runs on Codex.
- **Result:** `docs/first-study-literature.csv`, 135 works.
  - Tier 1 (58): an F3 test, a pivotal adjudication or pilot scoring cannot be finished without them. Most are E1 frame candidates, pilot specimen texts and pivotal records.
  - Tier 2 (77): to read before submission.
  - 73 works no register listed were appended to `docs/closed-literature.csv`, among them the main texts of Hooper et al. (2026) and Morris et al. (2018), Kerp (2017), Kenrick and Long (2025), Morris et al. (2024), Steemans et al. (2009) and the Pelmis companion inventories.
- **Decision** (Barry, Claude chat, 2026-10-29): "Those ones that are parked can get their engines started again if they're important! They just require a bit of extra legwork from me, which I'm happy to do if they're important to this current work." Eight of the ten parked requests are reopened (route `barry-reopen`); two stay parked as not needed for this study (`docs/literature-requests.md`).
- **Structural review (Q1, Q2, Q4):** the master register's priorities reflected the spore compilation and the cards, not F3, so the Sandbian Dalby record behind M2 (Rubinstein and Vajda 2019) sat at priority 2. The new file is the first-study view; the master stays the complete register. No question's status changed.

## 2026-10-29: the trait pilot tests the mappings behind the maxima (Barry)

- **Decision** (Barry, Claude chat, 2026-10-29): "Yes, frame it so", answering Claude's question "Should the trait pilot test the trait-to-node mappings behind M1–M3?" The bounded pilot agreed in `innovation-scope.md` therefore assesses, for each maximum, the evidence that its trait marks its node: cryptospores and the embryophyte crown (M1), trilete monads and the embryophyte crown (M2), polysporangiate bodies and total-group Tracheophyta (M3). It does so from specimen-level trait combinations and published placements and ancestral-state reconstructions, with no new tree inference.
- **Draft specification:** `docs/pilot-traits.md` (Claude Opus 5.5), pending Codex's review; no analysis run. Each mapping is a temporal proposition: the trait arose no later than the node. A `gpt-6.1-sol` audit (`docs/audits/2026-10-29-pilot-spec-audit.md`, 17 findings, all accepted) withdrew the first draft's claim that M1 and M2 rest on opposite readings. What stands: the traditional reading removes M2's bearing on the crown; under Hooper et al.'s reading M1's bearing depends on when cryptospore production arose relative to the crown.
- **Observation from the Hooper et al. deposit:** their two fossil-inclusive ancestral-state trees place the eophytes either as sister to the polysporangiophytes or as sister to all other embryophytes. Both trees put *Cooksonia* on the lycophyte line, inside crown Tracheophyta; M3's use of *Cooksonia* cf. *pertoni* as a total-group record is to be reconciled (Q9).
- **Structural review (Q1, Q2, Q4):** the pilot attaches to F3's existing node layer (`f3-shape.md` §3) rather than adding a parallel analysis. Exposed: the node statements depend on ancestral-state readings that the published reconstructions do not settle. No question's status changed.

## 2026-10-29: the F3 contract made executable; 0.955 adopted (Claude and Codex)

- **Repairs** (Claude Opus 5.5, to Codex's four findings in Correspondence 2557): stage 2 runs from a verified stage-1 verdict file and pools only borderline quantities; acceptance refuses a receipt outside its calibrated code, protocol and quantity scope or with a non-finite or negative δ; the acceptance quantities are delivered coverage (a failed bound or set never covers), with truth-point test coverage kept as a labelled diagnostic; summaries carry status. `models/f3/validate.py`; 159 tests pass.
- **Adopted** (Claude proposed, 2553; Codex agreed, 2557): calibrate δ to 0.955. Nominal coverage 0.95, the 0.93 floor and the 944/915/1,886 thresholds are unchanged.
- **Agreed condition on shared ages** (Codex, 2557; Claude accepts): independence is declared for development; before application the binding grid freezes the real frame's section sizes and coeval, depth-ordered and shared-boundary scenarios, and a claim that fails them is narrowed or the likelihood extended.
- **Evidence from the repair:** re-summarising the stored runs changes no acceptance quantity; the bound and the test never disagree; only shared-age D9 under H1 moves (0.996 to 0.995). Pooled over three batches, only A15 under H0c lies below 0.955 (0.948), and single-batch δ at 0.955 ranges 0.14–0.38.
- **Structural review (Q1):** the contract now runs as written, so the remaining gate to a binding validation is the real frame (Codex's Pelmis and Hanadir inventories). Exposed: one global δ lets the weakest long-gap cell set every bound's width. That costs informativeness, not validity, and is left as is unless the real design shows a large cost. No question's status changed.

## 2026-10-29: second-repair audit and Pelmis inventory (Codex)

- **Methods:** independent checks accept the rate-dependent target, integrated reference normalisation and core numerical-status repairs. The saved synthetic rehearsal's 117 pointwise acceptance quantities reproduce (minimum 946/1,000); its receipt matches historical source `55d7a58`, not the later shared-age code. No ensemble was rerun.
- **Remaining repairs for Claude:** enforce calibration-receipt cell/protocol scope; implement verified pooled stage-two decisions; distinguish successful truth-point tests from failed delivered bounds/sets; retain fixed-M2 status and make diagnostics status-aware. The full binding workflow is not yet executable as claimed. Details and counterexample rows: `docs/audits/2026-10-29-f3-response-and-ghelli-frame.md`.
- **Agreement** (Codex responding to Claude's proposal 2553): adopt 0.955 as the future empirical calibration target, keeping nominal 0.95, floor 0.93 and the existing sequential thresholds. It is a tuning cushion, not a proof of population coverage. Declare independent latent ages for development and test plausible shared-age structures at the actual design before application; those diagnostics do not guarantee robustness to all geological dependence.
- **Reporting:** integrated productive-assemblage eligibility with explicit outcome-dependence and conditional-inference qualifications. Barren/unknown preparations remain in the inventory; no new zeros or adapter.
- **Evidence:** the Pelmis 2017 reissue supplies 27 table-listed productive sample codes and explicit E1 source scope. The 140-sample collection/subset distinction and MG-130 discrepancy remain unresolved. The pilot stays at 15 blocks/90 outcomes; candidate inventories increase to four frames/41 rows. Related 2011/2025 Khoshyeilagh sources have different E1/E2 reporting scope and unresolved overlap.
- **Structural review (Q1/Q2):** separate source inventories from admitted trials and pointwise-test validation from successful interval delivery. Existing evidence tables and a focused audit suffice; no schema growth or empirical fit is needed yet. Pelmis companion inventories are the next evidence target; Claude retains methods implementation. Q9 remains parked and no scientific age/trait result changed.

## 2026-10-29: Codex's second review accepted; contract rehearsed (Claude, awaiting Codex's check)

- **Review accepted** (Claude Opus 5.5). R1–R4 of `docs/audits/2026-10-29-f3-repairs-and-frame-review.md` stand. Claude implemented them in `models/f3/`
  (`55d7a58`; `docs/f3-shape.md`, "Second review"):
  - **R2.** The target constraint is weighted at the rates being profiled, and the reference normalisation is integrated over the reference units' ranges.
  - **R3.** Each result carries the status of the run it used, and a failed statistic never covers.
  - **R4.** Calibrate and accept phases run on disjoint seeds, with a hashed receipt holding δ.
- **Rehearsal on the synthetic design** (binds nothing):
  - **Calibration** gave δ = 0.
  - **Independent stage-1 acceptance** passed all 117 acceptance quantities; the lowest was A15 under H0c, at 946 of 1,000.
  - **Numerics.** One fit failed in 63,000 replicates.
  - **Misses are sampling, not optimisation.** Each calibration miss was re-solved from about 65 further starts, and none became a cover.
  - **The repair leaves the statistic almost unchanged.** Re-running the development seeds with the repaired code leaves *f\** and coverage almost unchanged, so the development grid's δ = 0.11 was batch variation at a cell near 0.95.
- **Shared ages within sections (R1)** were tested rather than argued, in diagnostic cells D7–D9. They cost about 0.01 of coverage at ten units per section
  and nothing measurable at three. The independence assumption is declared, and the binding grid repeats the test at the real frame's cluster sizes.
- **Proposed, for Codex:** calibrate δ to 0.955 rather than 0.95. A cell at 0.948 fails the agreed acceptance rule with probability 0.105. Barry's
  decision is needed only if Claude and Codex disagree.
- **Reporting rule.** Claude accepts Codex's three qualifications (`data/units/reporting-rule.md`) and adds productivity as an eligibility condition, for
  Codex to integrate.
- **Compute.** The paired re-run, the re-optimisation check and D7–D9 ran on `nectar` at `c3.3xlarge`. Barry (chat, 2026-10-29): "feel free to put it on
  c3.3xlarge for this type of work, and leave it on that for as long as you need: I have plenty of allocated SU, so it's better to be liberal than
  conservative in your VM sizing." Recorded in nectar `02fb316` and `AGENTS.md`.
- **Structural review (Q1).**
  - **The harness now executes the contract it describes,** so the binding validation is one command on the real frame.
  - **Exposed assumptions:**
    - a one-batch δ is noisy at cells near 0.95, which is what the 0.955 proposal answers;
    - spread flags select hard data and do not by themselves indicate numerical error;
    - the independence of unit ages is an approximation, measured but not removed.
  - **No question changed.** Q1 waits on the frame tranche (Codex) and on Codex's check of this tranche.

## 2026-10-29: repaired F3 review and Hanadir frame follow-up (Codex; Claude response pending)

- **Access refreshed.** Codex re-read the current global instructions and Nectar guidance on
  Barry's request. Mac-origin Linux work uses `nectar`; the old campus routing assumptions
  are superseded. One harmless Correspondence read succeeded; no MCP reconnect or job restart
  was needed. Claude's handoff in messages 2498 and 2502 was checked.
- **Mathematical repairs accepted.** The chord/Jensen bounds and zero-older-detection
  attainment argument hold under the declared independent latent-age model. H0m remains a
  conservative relaxation. All 142 F3 tests pass. The saved 21,000-replicate development
  results reproduce; no development grid or completed Q9 analysis was rerun.
- **Binding validation is not ready.** The review at
  `docs/audits/2026-10-29-f3-repairs-and-frame-review.md` identifies three remaining matters:
  fitted-rate target weights versus generating-rate validation and realised versus integrated
  reference-age normalisation; incomplete convergence propagation and loss of per-result
  numerical flags; and the executable, frozen calibration/acceptance contract. These are
  response items for Claude, who retains the model files. No undercoverage is inferred from
  the target mismatch alone. Every development cell has flagged fits; A5 has 539 such fits
  across 129 replicates, not just 0.2% of replicates. The saved coverage counts remain reproducible.
- **Reporting rule: qualified agreement.** Codex agrees the frame-first, event-specific,
  reading-consistent and deduplicated core in message 2498. `data/units/reporting-rule.md`
  proposes precise exceptions and unknown handling: an explicit event-wide negative may
  establish source scope, but a pooled report must retain its scope; taxonomic reading choices
  do not turn missing material/reporting information into zeros. No binary adapter was built.
- **Hanadir evidence strengthened.** Strother et al. (1996) provides a study/horizon-scoped
  trilete non-detection; 2015 Plate V.1 links the 190.7 m specimen directly to 1996 figure 3k.
  That existing block's E1 outcome is updated in all three readings. The 14 depths in the
  older chart are separately inventoried, without invented per-depth outcomes. The 272.8 m
  link is provisional and 152.8 is not silently equated with 155.9. The pilot's erroneous
  plate VI–VII locators are corrected. There remain 15 material blocks and 90 outcomes.
- **Frame limits retained.** None of the three candidate inventories is analysis-ready.
  The Hanadir chart does not certify all processed samples; Paraguay still lacks the complete
  53-sample/event log; a bounded official GA catalogue/API check found no Balme scan. The
  original report remains needed. No external requests or collaborator messages were sent
  outside the authorised private Board.
- **Structural review (Q1, Q2).** Separating source-scope eligibility, material linkage and
  frame admission exposed a real older negative without manufacturing a denominator. The
  frame inventory and existing two-table interface serve the next investigation. Q1 now has
  stronger negative evidence, but still requires a complete frame and a reconciled validation
  contract; the scientific question and Q9's parked status do not change. The next owned
  tranches are Claude's methodological response and targeted recovery of complete sample logs.

## 2026-10-29: Codex's implementation review accepted; estimator repaired (Claude, awaiting Codex's check)

- **Review accepted** (Claude Opus 5.5). All four findings of `docs/audits/2026-10-29-f3-implementation-review.md` stand. Claude reproduced the three Bernoulli counterexamples (0.0979, 0.0297, 0.0885) and the sequential probabilities exactly. No scientific disagreement remains to put to Barry. Reply in Correspondence 2498.
- **Repairs** (`docs/f3-shape.md`, "Repairs after Codex's implementation review"):
  - **Fixed chart boundaries,** with two coherent shift scenarios replacing the sorted normal draws.
  - **An exact all-path H0.** With fixed boundaries, a path enters the likelihood only through its stage-piece means. The chord bound (non-detection) and Jensen (detection) then make H0 an optimisation over those means. It is exact when no older unit detects.
  - **H0m over all monotone paths,** conservatively.
  - **H1 on the same footing.**
  - **Logistic withdrawn** as a confidence class.
  - **Pointwise origin read-outs,** with a continuous 10 Myr lag for H0m.
  - **The critical value is a declared rule:** count-matched plus a shift δ, calibrated by simulation at the real design.
  - **Stage 2 at 1,886.**
- **Where Claude chose differently from Codex's recommendations:**
  - **H0 and H0m were repaired rather than renamed.** Fixed boundaries made the repair exact and cheap.
  - **Calibration is by a least-favourable shift, not a per-analysis bootstrap.** Resampling at a fitted null inside a composite class is itself unvalidated, and would nest the validation.
  - **Codex's counterexamples need thin reference windows.** The same enumeration at design-like sizes gives 0.019–0.031. Codex is asked to check both choices.
- **Validation re-planned.** The binding study simulates outcomes on the real unit table once its frame exists. A development grid of 15 correctly specified and 6 diagnostic cells now looks for failure modes, and binds nothing.
- **Pilot adjudication** (Claude). Codex's Paraguay readings are agreed. The eight depths cannot enter a denominator because they were selected through their outcomes. Claude proposed a binary reporting rule (frame first, full-category scope, outcome mapping per reading, dependence) for Codex to accept or amend. The complete-inventory frame tranche is agreed as Codex's.
- **Development grid** (21 cells × 1,000 replicates, synthetic design; `models/f3/README.md`; binds nothing):
  - **Acceptance cells.** Every one would pass stage 1 for every class that contains its truth. Coverage is 0.946–0.995 at δ = 0. The lowest is A15 under H0c, with a 47 Myr gap, where δ = 0.11 would restore 0.95.
  - **Diagnostics.** They stay at or above 0.945 against the effective target.
  - **Read against the nominal path,** confinement to half the regions gives 0.907 under H0c and 0.936 under H0, and older reporting at 0.7 gives 0.934 and 0.950. f\* bounds reported, range-averaged intensity, and the biological translation must say so.
  - **The all-path H0 costs little:** its f\* exceeds the constant's by only 0.01–0.06. In the Poisson limit the zero-count likelihood depends on a path only through the exposure-weighted target.
  - **Power at this design is low:** full-intensity origin sets end about 4–22 Myr beyond τ̂, and sets at f_min = 0.1 are almost always unbounded.
- **Structural review (Q1).** The structure now serves the next investigation:
  - the estimator implements the declared classes;
  - the harness stores the statistic at the truth, so calibration at the real design is a re-summary;
  - the binding validation waits only on the frame.

  Exposed assumptions:
  - Boundary uncertainty is no longer propagated; it is a scenario.
  - Regional confinement and lower older reporting are absorbed into "intensity", which the biological layer must carry.
  - Global optimality of the supremum rests on multi-start search and nesting checks, not proof.

  No question changed. Q1 now waits on the frame tranche (Codex) and on Codex's check of the repairs.

## 2026-10-29: implementation review, sampling-unit pilot and Q9 provenance (Codex; response pending)

- **Authority and cadence.** Barry asked Codex to check Claude's plan, implementation and test
  evidence, then proceed with the Q9 provenance check and bounded M2 pilot where relevant.
  He confirmed: "Claude will not see or know of your new work until I re-prompt him" and
  "This is the cadence we'll continue to use, throughout the project work" (Codex chat).
  Each session completes its owned tranche and posts a handoff; Board posts do not dispatch work.
- **Implementation checked.** The 117 F3 tests pass. Codex's independent review at `b2c6443`
  finds that the broad H0/H0m descriptions exceed their implemented subclasses, the logistic
  denominator lacks the claimed nesting, and a Poisson-matched cutoff is not exact for the
  profiled Bernoulli procedure. Exact enumeration supplies counterexamples. The two-stage
  acceptance rule passes with probability 0.06903 at true coverage 0.93; raising its pooled
  threshold from 1,880 to 1,886 would reduce that to 0.04837. Independent Normal perturbation
  and sorting of chart boundaries remain a toy assumption. Details and reproducible checks:
  `docs/audits/2026-10-29-f3-implementation-review.md`.
- **Coverage target retained.** Parent review challenged a proposed requirement to validate
  conditional on the unknown truth being older than the selected first appearance. Unconditional
  coverage of the complete origin set remains legitimate. The approximately 0.84 coverage in that
  truth-defined subset is a diagnostic, not automatically a failed conditional claim. Any additional
  observable reporting rule must be declared and calibrated; output must show the implicit younger
  part of the origin set.
- **Recommendations, not an amendment.** Codex proposes narrower class labels or repaired
  optimisation, calibrated tests, the corrected sequential rule, explicit age scenarios and an
  expanded validation grid. These await Claude's response. The adopted scientific question stays;
  neither plan nor model code was rewritten, and no full validation grid or real-data fit was run.
- **M2 pilot completed at the evidence-supported size.** `data/units/` has 15 identifiable blocks
  and 90 event-by-reading outcomes, with two ambiguous endpoints held as candidates. It tests the
  interface and source audit, not an analysis denominator. Eight named Paraguay depths come from
  a 53-sample study whose complete event table is unavailable; repeating its spore and chitinozoan
  reports would duplicate material. The sole explicit older E1 negative is a secondary quotation
  with unknown eligibility. A primary-verified negative/reference frame is still needed.
- **Q9 bounded check complete; historical linkage unresolved.** The archive hash matches;
  all 5,001 saved chain rows reproduce the rounded publication summary. Focal output-tree clades
  match by full leaf sets. Input fossil tails are 1%, not the described 2.5%; output filenames,
  controls and the R script do not identify the historical invocation. The preliminary Board
  messages 2490–2494 incorrectly removed burn-in twice; the final audit corrects that and retains
  the trimmed result only as sensitivity. No molecular-clock rerun was performed.
- **Structural review (Q1, Q2, Q9).** Separate unit and outcome tables preserve the distinction
  between material, event, reading and eligibility; the source-file ledger preserves main texts
  and supplements separately. The structure serves the next targeted denominator audit. This
  tranche exposed both a statistical class mismatch and the empirical scarcity of documented
  negatives, without changing the programme's questions. Next: Claude's methodological response,
  then a source-selected complete sample-frame tranche and a predeclared validation study.
- **Verification limits.** Unit integrity and five malformed-input checks passed; Q9 summaries
  and both statistical enumerations were reproduced independently. The global DOI scan flagged
  15 entries in unchanged `docs/barry-to-action.md` (14 trailing-backtick parse failures and one
  missing citation context). Both new source DOIs were verified directly with Crossref. No card,
  trait matrix, F3 model or existing occurrence interpretation was changed.

## 2026-10-29: F3 estimator built and reviewed; six refinements (Claude, awaiting Codex)

- **Built.** The compatibility estimator, simulator and validation harness are in `models/f3/`. A Claude Sonnet 5.5 subagent built them to Claude Opus 5.5's construction. Claude Opus 5.5 reviewed them. The as-built version and its smoke run are preserved at `c7729ad`.
- **Refinements** (Claude; recorded in `docs/f3-shape.md`, "Refinements from the estimator build"):
  - the critical value is matched to the exact one-sided Poisson limit for the older detections (5.99 at none), replacing χ²₁'s 3.84, which was anti-conservative in the zero-count regime: as-built f* coverage was 0.87–0.95;
  - H0c, H0, logistic and H1 share the best constant history as their alternative;
  - H1 is any path up to its ceiling, with the pulse duration dropped;
  - *a* = 1 is the realised reference window's intensity, stated in the biological layer;
  - τ is the base of the oldest certain-detection stage (the draft specification's "top" was a misnomer);
  - validation coverage is unconditional, with non-trivial coverage as a diagnostic.
- **Codex's review of these, and of H0 and the two-stage rule, is still open** (Correspondence 99). If Codex objects, both positions go to Barry.
- **Structural review.** The structure served: the smoke run found a calibration defect before any real data existed, which is what validating first is for. One assumption was exposed. A reference window anchored on the observed first appearance measures intensity relative to whatever that window holds, so "relative to the reference" needs care in the biological layer. No evidence changed a question; Q1's next step (the full validation grid) stands.

## 2026-10-28: F3 reshape v3 adopted

- **Adopted** (Barry, chat, 2026-10-28: "Yes, adopt v3"). `docs/f3-shape.md` v3 (`fd36a9c`) governs F3's statistical contribution as the third amendment to `docs/plan-f3.md`. The question becomes which explicit sampling and biological assumptions make older origins incompatible with the fossil absences behind the clock maxima. The deliverable is a layered compatibility analysis over eligible sampling units, validated as a complete procedure before any real-data result.
- **Still open with Codex:** the primary history class H0 and the two-stage acceptance rule (Correspondence 99, message 2485). If Codex objects, both positions go to Barry.
- **Work split** (agreed in discussion 99): Codex builds the sampling-unit interface and M2 pilot (`data/units/`) and the Q9 provenance check; Claude builds the readings definitions, analysis specifications, estimator and validation study (`models/f3/`) and continues occurrence adjudication.

## 2026-10-28: F3 reshape v3 (Claude)

- **v3 of `docs/f3-shape.md`** (Claude Opus 5.5, still a proposal for Barry). Accepts Codex's V2-R1–R5. The target is the reference-rate-weighted mean intensity over declared history classes, with four result states (finite data bound, ceiling-limited, unbounded, zero eligible exposure); reference rates come from the complete eligible reference frame, with scope taken from stated aims and methods; inference is by test inversion with marginal read-outs; the verdicts are compatible / incompatible / uninformative with the specified encounter histories, and "supports a maximum" needs a stated, independently justified rarity restriction; matching rounded clock ages is a consistency check only.
- **New in v3, awaiting Codex:** the primary history class H0 (no pre-appearance encounter intensity above the post-appearance reference); a two-stage acceptance rule per validation cell (pass on a one-sided 95% lower limit above 0.93; a correctly calibrated cell passes with probability 0.983); and four additions to the unit interface (message 2483).

## 2026-10-28: Codex response to F3 reshape v2

- **Review** (Codex; Correspondence 99, following Claude's messages 2474–2476): `docs/audits/2026-10-28-f3-reshape-v2-codex-review.md` supports the three-layer presentation, the M2 → M1 sequence and the separate Q9 diagnostic. It proposes explicit weighting and history-specific bounds, distinguishes a finite data bound from an imposed ceiling, requires a complete eligible reference frame, clarifies coverage and the 93% tolerance, and restricts maximum-support claims to stated encounter histories. Matching rounded published clock ages is a consistency check, not decisive provenance.
- **Ownership** (Codex accepts Claude's proposed division, message 2477): Codex owns the new sampling-unit design and Q9 provenance work; Claude retains the memo, plan, models and occurrence/spore pipelines. The review includes a draft unit/outcome interface for agreement before implementation. No unit dataset, estimator or clock analysis was built in this review.
- **Scientific status:** these are Codex's recommendations on v2, pending Claude's response and Barry's adoption of the reshaped deliverable. The adopted plan is not changed by this entry.
- **Structural review:** the existing evidence/interpretation split can support sampling units through linked IDs, with no duplicate occurrence adjudication layer. Q1 now needs explicit detection and reporting eligibility; Q9 needs file-to-run correspondence. The mathematical checks show why positive expected effort alone does not ensure an informative bound. Loop 1 remains open.

## 2026-10-28: Claude's response to the Codex F3 review

- **Concessions** (Claude Opus 5.5; Correspondence 99, message 2474). F3-R1: an absence likelihood is not a calibration-prior tail probability, so the first output is a compatibility surface and "overconfident by a measurable amount" is withdrawn. F3-R2: the envelope bounds an effort-weighted mean of relative encounter intensity in eligible units, not time-averaged abundance. F3-R5: "about 100 spore records bound origination to within a few Myr" overstated the grid; the adopted plan now carries a dated correction (median widths 24–45 Myr at mid preservation, Darriwilian–Sandbian).
- **Proposed in reply, not adopted:** a two-layer output (encounter intensity, then a labelled translation under a named detection assumption and a named node mapping); eligibility classes calibrated empirically from post-appearance positives; exact age marginalisation; extended origin domain for M1; a bounded synthesis check of *C. barrandei*'s total-group status; a Q9 test of whether the deposited posteriors reproduce the published ages; and file ownership (`docs/f3-shape.md`, `docs/plan-f3.md`, `models/f3/` and the occurrence and spore pipelines with Claude; Q9 provenance and a new `data/units/` sampling-unit design with Codex). A revised reshape goes to Barry once the two agents agree it.

## 2026-10-28: pivotal records rechecked; Cambrian effort added

- **Pivotal records against full texts** (Barry obtained eight of nine closed papers and three partial sources on Yea; Codex `gpt-6.1-sol` extracted 232 findings, every quotation verified by script; Claude Opus 5.5 adjudicated; `work/codex/loop1b/README.md`).
  - **Yea, eastern localities: main reading changed** (Claude). The Early Devonian baseline was a repository convention. No published work demonstrates it for Ghin Ghin Loc. 1 or Limestone Road Loc. 4, and none establishes the Gorstian beyond dispute: the Loc. 1 graptolite identification is contested (Earp's unreviewed 2023 draft), and the correctly identified Gorstian graptolites at Loc. 4 came from a spoil heap. The main reading is now "unresolved, Gorstian to Emsian". The Pridoli horizon B2, 67 m higher, is a separate observation. Under the main reading, E5 is certain from the Pridoli and possible from the Gorstian; accepting the Yea graptolites moves the certain age 5.4 Myr older (`models/f3/out/naive_pivotal.csv`). Rejected-records entry 17 gives both sides and what would settle it.
  - **Bolivian *Cooksonia*** (Claude): a branched axis with three terminal sporangia (Morel et al. 1995), so it counts for E3 whatever its lycophyte affinity. It is younger than the Homerian first appearance, so E3 does not move.
  - **Argentine Dapingian cryptospores:** Strother et al.'s (2015) specimen-level argument is now recorded beside Rubinstein et al.'s (2010) claim (entry 16). The main reading, not established, stands. A palynologist's check of the figured tetrad would settle it (consult flag; Barry's decision).
  - **Unchanged, now on full texts:** Capel Horeb (tracheids from an unbranched sterile axis, lower Whitcliffian), *Pinnatiramosus* (Edwards et al. 2007 add an intermediate younger-roots reading), Zbrza (Hirnantian on chitinozoans from the plant layer; no tracheids), Hanadir (Darriwilian), and the Canning Basin Tremadocian assemblage (two samples, one borehole, conodont-dated; read by its authors as charophyte).
- **Cambrian effort** (Claude, under the adopted amendment). The Palynodata extract was widened from 485 to 600 Ma on Palynodata's own timescale. The old edge dropped Tremadoc-only papers, which Palynodata dates at about 505–490 Ma. Tremadocian effort rises from 180 to 418 documents. The Middle and Late Cambrian gain about 175–185 documents per stage. Early Cambrian papers fall outside the 25 Myr dating rule. Cambrian age names were re-crosswalked (Codex `gpt-6.1-sol` with sources; 71 names) and 78 new locations mapped (Codex `gpt-6.1-terra`), all reviewed by Claude. No usable Ordovician–Devonian spore record changed.

## 2026-10-28: second amendment adopted; F3 reassessed

- **Second amendment adopted** (Barry, chat, 2026-10-28: "Yes, agreed, adopt it"). `docs/plan-f3.md`, step 3: the older limit is judged and reported, an interval counts only if it is informative, the capacity-profiled logistic fit is primary, spore effort and the tail extend through the Cambrian, and a test against mismeasured effort comes before any real-data verdict.
- **Shape of F3 reassessed** (Barry asked: "Then let's re-assess the full shape of F3 given this constraint"; Claude Opus 5.5 proposed; awaiting Barry). `docs/f3-shape.md` proposes that F3 test the fossil-absence maxima behind the clock results (515.5, 459.1 and 431.2 Ma) rather than estimate origination windows, using a non-parametric abundance envelope over the empty, sampled stages; E4 and E5 become synthesis only, E6 is parked under Q4 and E7 moves to Q3.

## 2026-10-28: Loop 1, step 3 (recovery study)

- **Recovery study** (`models/f3/`; written by a Claude Sonnet 5.5 agent, reviewed by a second Sonnet agent, checked by Claude Opus 5.5).
  - Grid: 2,880 rows, 1,000 replicates each. No estimator meets the original criteria across plausible scenarios.
  - The capacity-profiled logistic fit's older limit is usable.
  - Exponential growth leaves an exact trade-off between preservation and origination, so only empty, well-sampled older stages bound an origination.
  - The body-fossil channel is too thin to pass.
- **Second plan amendment proposed** (Claude; adopted the same day, entry above). Judge the older limit; require informativeness; make the profiled logistic fit primary; extend spore effort back through the Cambrian; test against mismeasured effort next. Spore effort was extended to the Tremadocian the same day (1,085 documents across the Tremadocian, Floian and Dapingian), which needs no decision.

## 2026-10-28: Loop 1, step 1 (the oldest records) and the sketch

- **Data model** (Claude Opus 5.5, under `docs/plan-f3.md`).
  - `data/occurrences/` holds observations, competing interpretations and sources for the oldest records bearing on E1–E5: 229 observations and 324 readings.
  - Built from the vetted spore dataset, and by Codex jobs that Claude checked: `gpt-6.1-terra` digitised Wellman et al. (2022) Table 1; `gpt-6.1-sol` compiled the literature readings for both channels.
  - Every quotation from a repository source is checked verbatim by script, and every DOI is matched on Crossref.
- **Rule for unassessed outliers** (Claude, set before any estimator saw the data). A claim that would make a first appearance more than one stage older than any independently accepted record does not enter the main reading unless it is peer reviewed and independently accepted. Applied to *Piterophyton* (Naugolnykh 2022) and the Ordos preprint, which are now tested as alternatives.
- **Timescale** (Claude). `data/timescale.csv` gains the Cambrian stages from ICS v2024/12. Most of their bases are approximate on the chart, and their uncertainty is left blank.
- **Effort layer** (Claude). PBDB collections of all taxa by stage, unit and setting. Terrestrial collections number at most about 8 per stage before the Lochkovian and about 104 in the Lochkovian.
- **Sketch and amendment.**
  - `models/f3/` (Claude Sonnet 5.5 agent; checked by Claude Opus 5.5): classical estimators under-cover badly when abundance ramps up after origination.
  - `docs/plan-f3.md` was amended, before any real data were analysed, to add estimators that model that ramp.
  - The published GRIWM code's arrival option is faulty, and the sketch uses the mirrored extinction algorithm. Barry: "can you please fix it locally for our use? I will let Corey/Fred know" (chat, 2026-10-28). `models/griwm_r/` holds patched copies of `griwm.R` and `criwm.R` (CRIWM shares the fault), a four-line patch per file and an R test. The test confirms the fault upstream and the fix against hand calculation and the project's Python implementation.
- **Compute** (Barry, chat, 2026-10-28). `deep-server` and `wsl-laptop` are unreachable after the university blocked Tailscale. The EPRP mirror is used from its backup on `nectar-vm`. At Barry's request ("Resize nectar-vm please to something more workable, such as c3 large"), Claude resized `nectar-vm` to `c3.large` with the nectar repo's script; this is recorded in `~/work/nectar`.
- **First pivotal pass** (Claude). Done without estimators: `models/f3/out/naive_pivotal.csv` and `docs/questions.md`, Q2. The new disputed records it surfaced are entries 18–20 in `docs/rejected-records.md`.
