# Charter

Status: **Stage 1, first deliverable** (from 2026-10-28). Orientation ran 2026-10-26 to 28. Barry chose the curated dataset plus F3, whether the record supports the competing timescales; the plan is `docs/plan-f3.md`.

## The idea

Barry's starting point, in his words (chat, 2026-10-26): "a simulation modelling project on the
evolution of early land plants (late Ordovician to early Devonian), but it's a very nascent
thought". He frames it as "a long-term development project that might prove infeasible or
uninteresting, but is worth … at least exploring", with no hurry, and with the structure left
free to evolve.

## Purpose

Barry set out the purpose by voice in chat on 2026-10-28. This is a paraphrase, with his words in quotation marks.

- **Synthesis on curated specimens.** The programme builds on more than a century of specimen-level palaeontology: "data collection, specimen curation, detailed examination of individual taxa". It aims to assemble those records, including ones "missed from the databases", into "something newly coherent that is well positioned for detailed statistical analysis".
- **Models with data behind them.** The assembled data are to "robustly parameterize, check and verify simulation models". Those models ask questions "well beyond the ability of individual fossils to discern":
  - patterns and drivers of evolutionary change;
  - tests of hypotheses about innovations, and counterfactual scenarios;
  - "what the aggregate evidence suggests about relationships".
- **A demonstration of method.** A quantitative scientist works with AI agents that do most of the legwork and contribute intellectually "as my intellectual equal and interlocutor". The aim is "a flagship, a demonstration of how this can be done more broadly in paleontology, in quantitative paleontology particularly".
- **Scope.** The EPRP programme casts the wide net. Early land plants, from the mid–late Ordovician to the Early Devonian, are the first case study, chosen because they interest him and are tractable.

Barry refined this later the same day, in chat (paraphrase, with his words quoted). The programme is "a sustained programme that connects specimen-based knowledge to evolutionary inference", with early land plants as the first substantial case. "Its success would be measured by the scientific questions it makes answerable." The contribution is to connect two scales rigorously: the scale of the evidence (specimens, collections, papers, taxonomic revisions, databases) and the scale of explanation (innovations, ecological circumstances, environmental change).

- **Assembling evidence is scientific work.** Judgements about identity, revision, what a measurement represents and which observations justify a reconstruction can change the pattern before any model is fitted, so those decisions must stay inspectable. "Coherent" means "preserving meaningful disagreement in a usable form". Keep the observation and each interpretation, and carry the competing reconstructions far enough to find which disagreements matter.
- **Evidence and questions develop together.** This avoids two failures: endless preparation of the database, and a model chosen early that collects only what it needs. The repository should support that repeated exchange.
- **Each contribution has its own standard of success.** The contributions are synthesis, statistical analysis, simulation and phylogenetic reassessment. They can reinforce one another "without requiring everything to culminate in one enormous model". A fifth kind, proposed by Claude and endorsed by Barry the same day ("very important"), is **testing old narratives**: finding claims passed from paper to paper without re-checking, testing them against the assembled record, and tracing which pattern-level statements rest on them (`docs/questions.md`, Q5). For simulations, ask which observations discriminate between explanations. "Sometimes the strongest result will be a clear account of what the present record cannot distinguish, together with the particular observation that would resolve it."
- **The demonstration is judged by what becomes reproducible and convincing.** Another researcher should be able to follow the route from specimens and publications through adjudication and analysis to a conclusion. Keep the enabling novelty (the scale of work the collaboration can sustain) separate from the scientific novelty, which "still has to be earned through particular questions, methods and findings".
- **Routine review of structure.** Assess routinely whether the repository's structure supports a continuing sequence of investigations, as well as each candidate project. In discussion, develop and challenge the programme itself.

## Why this interval

Between roughly 470 and 393 Ma, land plants went from a dispersed-spore record with no
recognisable bodies, through centimetre-scale leafless axes, to lycopsids and euphyllophytes with
leaves, roots, secondary-growth precursors and metre-scale height. Nearly every innovation that
defines vascular plants appears in that window: desiccation-tolerant spores, cuticle and
stomata, lignified conducting cells, branching sporophytes independent of the gametophyte,
apical dominance, leaves and roots. The same plants are implicated in changes to weathering,
atmospheric CO2 and O2, river form and soil. The record is unusually uneven, with abundant spores
and a few exceptional deposits (the Rhynie Chert above all) set against long gaps in
megafossils, so most explanations of the pattern remain verbal. That combination of a major
evolutionary transition, rich constraints and few quantitative tests is the case for modelling.

## What would make it worth doing

A framing earns a modelling programme if it meets all four tests:

1. **Discriminating evidence.** Competing hypotheses predict outcomes that the fossil, proxy or
   experimental record can tell apart: trait sequences, timing, size distributions, diversity
   or disparity patterns, geochemical signals.
2. **Novelty.** The model adds something the precedents (`docs/precedents.md`) do not: a
   mechanism, a coupling, a confrontation with data, or a reanalysis that changes a conclusion.
3. **Tractability.** The data can be assembled and the model run with resources on the mesh,
   without years of bespoke data collection.
4. **Interest.** Barry finds the question worth his attention.

If no framing passes tests 1 and 2 after orientation, the project is parked with a short written
account of why. That account is itself a useful output.

## Route

0. **Orientation** (closed 2026-10-28; the current plan is `docs/plan-f3.md`): taxon cards (`taxa/`), a period primer (`docs/primer.md`), a review
   of modelling precedents (`docs/precedents.md`) and candidate framings (`docs/framings.md`).
   Ends with a choice of framing, which is Barry's call on a recommendation from the agents.
1. **Sketch:** the smallest end-to-end model of the chosen framing, deterministic where possible.
2. **Ground:** null models, baselines and the data the model will confront (trait matrices built
   from the cards, occurrence data, proxy series).
3. **Enrich:** one mechanism at a time, each motivated by a discrepancy with data.
4. **Compare:** contrasts that discriminate between competing explanations.
5. **Synthesise:** what is robust, what depends on representation, and what is next.

Stages are a guide, not approval gates. Barry's operating principle applies: reversible work
proceeds and is shown afterwards; first public release, submission and outward-facing messages
are his decisions.

## Outputs

The repository is private for now. Candidate outputs, in any combination: the card collection
and trait matrix as an open dataset, a review or perspective, a modelling paper with code and
data archived, and the human–AI correspondence record published alongside.

## Contributors and AI roles

- Barry W. Brook: originator, scientific adviser and final reviewer.
- Claude Opus 5.5 (Anthropic, `claude-opus-5-5`) in Claude Code: orchestration, programme
  design, synthesis, framings, tooling. It wrote the F3 changes after Codex's second review itself
  (2026-10-29): the target constraint weighted at the rates being profiled, the integrated reference
  normalisation, per-result numerical status, the calibrate/accept phases with their receipt, and
  the shared-age diagnostic cells; and ran their rehearsal on the synthetic design, with a paired
  re-run of the development seeds and a re-optimisation of every calibration miss (on `nectar`).
  After Codex's third review (2026-10-29) it made the contract executable itself: delivered-output
  coverage separated from truth-point test coverage, the receipt-scope and stage-1 checks, pooled
  stage 2, status-aware summaries and the 0.955 calibration target, verified by re-summarising every
  stored replicate table and a tiny-protocol smoke run of the full command-line path.
  It drafted the trait-pilot specification (`docs/pilot-traits.md`, 2026-10-29), framed by Barry as
  a test of the trait-to-node mappings behind the clock maxima, with a Codex `gpt-6.1-sol` audit
  of its facts and logic adjudicated by Claude.
  On 2026-10-30 it closed the fourth contract review, adopted the pilot design with Codex's
  amendments, read the decisive primary texts (Hooper et al. 2026, Edwards and Davies 1976,
  Edwards et al. 1999) and adjudicated the pilot's specimen evidence table.
  Later that day it closed Codex's last stage-2 evidence gap, ran a second extraction round (with
  OCR of three scanned sources), built the pilot's combination table and wrote the M3
  record-identity audit from the primary descriptions.
  On 2026-10-31, under Barry's widened scope, it pre-declared and ran a reproduction of Hooper et
  al.'s stochastic mapping in R (phytools, pinned renv) and read the trilete persistence from the
  regenerated maps (`models/pilot-asr/`). Later that day it made Codex's strict-parsing and pilot
  corrections, adjudicated the Skagen trilete reports against Hooper et al.'s caution, and wrote the
  design screen (`models/f3/screen.py`) showing that M2's own core cannot test its absence premise.
  It then drafted, for Barry to send, the request to Rubinstein and Vajda about the figured
  specimens (`docs/outreach/`). After Codex's review of that work it:
  - narrowed the screen to its declared design and tied it to the engine by test;
  - set the frame-selection rule, under which binding claims are conditional on passing the screen;
  - made the checker hold bound states to the engine's invariants;
  - corrected the persistence counts and wording;
  - measured the stochastic maps' Monte Carlo precision with independent chains (`models/pilot-asr/`).
  Later on 2026-10-31 it drafted the two-sprint plan and, after Codex's revision, ran sprint 1:
  - read the Libyan thesis's systematics and chart legend to fix E1 reporting scope;
  - froze eight M2 designs before any statistic;
  - extended the engine (transport multipliers, numerical age ranges, the oldest-possible
    first-appearance rule, the window read-out) and wrote the adapter, screen and actual-design
    qualifier (`models/f3/designs.py`, `m2.py`, `qualify.py`);
  - amended the screen when it found that conditioning on it would remove the evidence;
  - qualified 14 design/ρ combinations on `nectar` and wrote the M2 result note.
  It then reviewed Codex's sprint 2 (2026-10-31): screened Borenshult and assessed Libya and Ghelli as E2
  frames, stated the outcome-coding rule and the inclusive-reading occurrence consequence for M1, and
  adjudicated and applied three subagent source audits (`docs/audits/2026-10-31-sprint2-claude-review.md`).
  It then drafted the Loop 1 reconciliation and close memo (`docs/loop1-close.md`, 2026-10-31). This covered:
  recomputing the acceptance claim and miss counts, the coverage interpretation, the shared E2 dispersal-unit
  rule checked against Wellman et al. (2015) and all E2 outcomes, and the Loop 2 proposal.
  On 1 November it revised the memo to integrate Codex's amendments (coverage statement, conditional-coverage
  counterexample, E2 definition), after checking the model, Edwards et al. (2014) and Abuhmida (2013) itself;
  drafted the versioned E2 addendum `data/units/e2-unit-rule.md` from Codex's replacement rule; and corrected
  the card and pilot cryptospore definition.
  It revised Codex's Loop 2 plan to v2, then on 1 November reviewed Loop 2 sprint 1. It
  reproduced the four break-even thresholds in an independent implementation and partly reversed the
  QSIM-801 count gate. It then ran sprint 2:
  - the QSIM-801 within-sample trilete-share bound, with its known-answer check;
  - the external-frame dispositions;
  - the M1 affinity adjudication;
  - the M1/M3 request drafts;
  - the rendered private manuscript, figures, claim table and data manifest (`manuscript/`).
  In Loop 3 (1–2 November) it proposed the positive body-record analysis and ran the pilot that Codex's
  review superseded. In sprint C (2 November) it verified Codex's reviewed endpoint results by hand and
  reconstructed the paper around the biological problem: a new main text, four new or redrawn figures
  (`manuscript/figures.py`), a supplement with tables generated from the reviewed outputs
  (`manuscript/supplement.qmd`, `tables.py`) and an extended claim ledger. Later the same day it moved
  the paper to Barry's makedoc toolkit (`manuscript/text/`, `settings/build.yaml`), built the programme
  bibliography from a DOI ledger (`references/`, `tools/refs.py`), wrote the two-page plain-language
  brief and its figure and the agent-facing paper (`manuscript/text/brief.md`, `for-agents.md`), and
  proposed the multi-study layout (`docs/layout-proposal.md`).
- Claude Sonnet 5.5 (Anthropic) subagents: the F3 simulator, estimators, sketch and recovery study
  (`models/f3/`), with a second Sonnet agent reviewing; the reshape-v3 compatibility estimator, unit
  simulator and validation harness (2026-10-28 and 29, reviewed and amended by Claude Opus 5.5), and
  their repair after Codex's implementation review (2026-10-29, to Claude Opus 5.5's design: fixed
  boundaries, exact all-path H0, calibrated critical value); literature research and first drafts of taxon cards,
  the primer (including its biological-transitions section, 2026-10-28), the precedents review and
  the rejected-records note; adjudication of audit findings
  against the sources and the resulting corrections; blind audits; the move of the data-rebuild
  instructions from `deep-server` to `nectar`, with re-runs on `nectar` that reproduced the EPRP
  extraction tables (2026-10-29, checked by Claude Opus 5.5); an independent code-only review of the
  sprint-1 engine extensions and qualifier (2026-10-31, adjudicated by Claude Opus 5.5); three independent
  primary-source audits of Codex's sprint 2 (Qusaiba/Samphire, the Cambrian–Silurian E2 sources, M3; 2026-10-31,
  adjudicated by Claude Opus 5.5).
- Codex (OpenAI, GPT-6; exact variant not exposed by this session), 31 October
  2026: sprint-1 counter-review after Claude's review of sprint 2, with bounded
  Codex delegates for source reconstruction, independent numerical/statistical
  checks and qualification-contract implementation. It corrected qualification
  scope, evidence enforcement and interpretations, and propagated the review
  into the combined results. Exact source and numerical checks are recorded in
  `docs/audits/2026-10-31-sprint1-codex-review.md`.
  On 1 November it reviewed and confirmed Claude's reconciliation, adopting the corrected E2
  addendum and finite-grid coverage interpretation, and closed the first paired sprint. Its
  independent methods and source reviewers exposed the conditional-inference impossibility error
  and the omitted alete monads; the parent checked the model and held source pages. It then led
  planning of the next pair for Claude's critique, with the implementation roles reversed.
  It implemented Loop 2 sprint 1 under the amended v2.1 plan: source/count feasibility,
  the 164-entry observation-basis audit, conditional count-share methods, joint contamination
  and chronology identification/sensitivity analysis, well influence, figures and runnable
  handoff. Bounded Codex delegates reconstructed sources, implemented isolated modules and
  independently checked likelihoods and numerical results. Review found and repaired extreme
  effort and impossible-data handling in the count-share code. No new fossil design was
  qualified; the parent retained the frozen benchmark and documented the distinction between
  a structural identification limit and an unqualified numerical comparison.
  In review 2 it checked Claude's sprint 2 with two independent source delegates and a statistical
  specialist (`sol_high_specialist`, configured GPT-5.6-sol/high; other delegates inherited the
  parent model). It verified the 99 QSIM marks, retained the mathematical lower-bound idea but
  withheld empirical admission, corrected the minimum estimand and heuristic dependence labels,
  and repaired primary-readout, affinity, source-scope and material-identity overclaims. It
  integrated the existing biological pilot and regenerated the private manuscript/package,
  without rerunning R or changing frozen qualification. The three close audits identify the
  checked evidence and local repairs; no claim is made that model agreement alone validates it.
  In Loop 3 review A and sprint B (1 November), it adopted Barry's positive-occurrence brief,
  rebuilt the macrofossil inventory and effort histories, and delivered exact conditional endpoint
  estimates, conservative age envelopes, source/unit/geographic sensitivities, shape diagnostics,
  matched simulations, retrospective pre-first-occurrence recovery contrasts and three figures.
  Two `sol_high_specialist` delegates (configured GPT-5.6-sol/high) audited sources and methods;
  the methods delegate implemented the endpoint engine and simulation, while the parent assembled
  the record, integrated corrections, implemented the sensitivity runners and produced figures
  and handoff. A `luna_light_scout` delegate (configured GPT-5.6-luna/low) traced the held effort
  inputs without adjudicating methods. The source reviewer also resolved seven older unplaced
  names. Their work exposed errors in the pilot and distinguished record-recovery endpoints from
  lineage origins. Claude owns the manuscript reconstruction; Codex will review it. No R or
  frozen F3 qualification was rerun or altered for this tranche.
  In review C (5 November), Codex checked the article, supplement, brief and agent guide against
  the results and source definitions, and delivered required interpretation corrections while
  Claude retained manuscript ownership. A `sol_high_specialist` delegate (configured GPT-5.6-sol/high)
  independently audited the numerical claims; a `sol_medium_scientist` delegate (configured
  GPT-5.6-sol/medium) compared published trilete evidence with one rubric. An explorer delegate
  mapped the frozen input contracts and implemented a separate Borenshult reading/screen with
  tests and provenance; the parent checked the published figures and integrated the review.
  No R analysis, frozen qualification or crown calibration was changed.
  Claude Opus 5.5 adjudicated review C (5 November) against the frozen outputs, accepted every
  finding, added the declared Oman-fragment B0 sensitivity (`models/f3/loop3/oman_sensitivity.py`),
  independently reproduced the Borenshult screen statistics, and integrated the corrections into the
  claims ledger, the four renderings and the figures.
- GPT-6 Pro (OpenAI), commissioned by Barry on 7 November 2026, independently reviewed the repository at
  `60c406b` in a disposable copy: it reproduced the central calculations, reran the Loop 3 outputs and
  simulations, and returned ten prioritised findings with scripts and tables
  (`docs/audits/2026-11-07-gpt6pro-triage.md`). It changed nothing in the repository. Claude Opus 5.5
  triaged the review, corrected the M1 source account, made the Oman-inclusive B0 canonical in the paper,
  wrote `manuscript/estimands.md` and rewrote all four renderings; Codex leads the requested analyses and
  public-reproduction work.
  In the 7 November closure check, Codex reviewed the revised interpretation and repaired
  evidence-commit references after the privacy-history rewrite, verifying identical evidence
  objects and a fresh clone. A `sol_high_specialist` delegate (configured GPT-5.6-sol/high)
  independently checked the numerical/method claims, while a `sol_medium_scientist` delegate
  (configured GPT-5.6-sol/medium) audited all E2 candidates and the primary Oman/Hawaz sources
  against the declared B0 category. Claude retains final paper integration; numerical values,
  frozen analyses and support statuses were not changed by the parent review.
  On 7 November, Codex (parent model `gpt-6.1-sol`) implemented the GPT-6 Pro stage-2 tranche.
  A `sol_high_specialist` delegate rebuilt canonical body membership, frontier and influence
  diagnostics; another implemented interval-feasibility and shared-timescale analyses. The first
  independently audited the second's central optimisation using brute permutation enumeration.
  A `luna_high_executor` delegate implemented case bindings and separately checked the parent's
  Murzuq likelihood/dependence and reproduction work. The parent verified C45–C47 against sources,
  integrated the executable category repair, propagated changed numerical summaries, archived the
  frozen CC0 PBDB input under standing authority, and built public reproduction/dependency targets.
  New analysis claims remain provisional for Claude's narrative integration; no new frozen F3
  qualification or external measurements were claimed.
  Claude Opus 5.5 then recomputed the stage-2 key values independently (frontier closed form, witness
  KS distances, constant-history endpoints and a separate Murzuq dependence implementation), marked
  C48–C52 supported and integrated them into the four renderings (`docs/audits/2026-11-07-stage2-integration.md`).
  Codex (`gpt-6.1-sol`) then reviewed that integration semantically against `manuscript/estimands.md`,
  with bounded `sol_high_specialist` and `sol_medium_scientist` independent reads of body-record and
  Murzuq/source-facing statements. The parent adjudicated the wording findings and corrected stale
  supplementary diagnostic figures in its own stage-2 delivery; all scientific CSVs remained unchanged.
  Claude retains prose repairs and final rendering (`docs/audits/2026-11-07-semantic-closure-review.md`).
  Later on 7 November Claude triaged GPT-6 Pro's follow-up review of `342153a`, checked its B1 and Yea
  findings against the primary sources, reframed the paper (title, abstract, finding-led results, frontier
  figure, Silvestro comparison), repaired the brief and source sentences, and made the finite-sample
  interval reference primary; Codex owns the B1 restoration, reproduction gates and the S2.2
  specification (`docs/audits/2026-11-07-gpt6pro-review2-triage.md`).
  On 8 November Codex (`gpt-6.1-sol`) completed that handoff. A `sol_high_specialist` delegate
  restored source-backed E3 admissions and regenerated the affected B1 outputs; another independently
  checked the finite-sample rejection argument and drafted the Murzuq likelihood specification.
  A `luna_high_executor` delegate repaired the public reproduction gates and source-route reporting.
  The parent independently recounted units, evaluated bounds and leave-outs from closed forms,
  verified C47, integrated ledger/text/figures, corrected plotted domains and first-record labels,
  ran clean-copy reproduction and checked the rendered products. These are bounded source, numerical,
  mathematical and editorial roles; no new clock analysis or frozen qualification was claimed
  (`docs/audits/2026-11-08-review2-handoff.md`).
- OpenAI Codex CLI, `gpt-6.1-sol` and `gpt-6.1-terra` at high reasoning effort, run by Claude Opus
  5.5 as read-only, schema-constrained jobs through `~/.claude/bin/codex-delegate` (2026-10-27 and
  28; on 2026-10-31 `gpt-6.1-terra` independently re-derived the 164 Libyan binary units for sprint 1; on 2026-11-01 `gpt-6.1-sol` with web search classified the 241 PBDB macrofossil names for the Loop 3 pilot, `work/codex/loop3/`). Records are in `docs/audits/` and the job files in `data/spores/work/codex/` and
  `work/codex/`. Work done:
  - spore genus, age-name and location crosswalks;
  - digitisation of the Wellman et al. (2013) supplement;
  - vetting of early spore records;
  - extraction of post-2006 spore assemblages;
  - the Model transfer retrofit of 59 cards, with a consistency review of them;
  - extraction of 518 quote-verified specimen observations for the trait pilot from 27 primary
    sources in two rounds (2026-10-30, `gpt-6.1-sol`; `data/pilot/specimens.csv`);
  - the first-study literature triage of 348 needed rows, a citation sweep of the first-study
    documents and a search for sample-level frame studies (2026-10-29, `gpt-6.1-sol`; tiers
    adjudicated and DOIs verified by Claude Opus 5.5; `docs/first-study-literature.csv`);
  - cross-family audits of the new cards and of the primer revision;
  - one card draft for a bake-off;
  - the Loop 1 occurrence tail (Wellman et al. 2022 table, literature readings for both channels);
  - extraction of 232 quotation-verified findings from the closed papers on the pivotal records,
    adjudicated by Claude Opus 5.5 (`work/codex/loop1b/`), and the Cambrian age, location and
    vetting jobs for the widened Palynodata window (2026-10-28).
- OpenAI Codex (OpenAI, Codex desktop; exact model version not exposed in this session):
  Executed sprint 2 on 31 October: bounded M1 source admission, M3 denominator
  assessment, full-release Palynodata coverage/regeneration, source-register
  reconciliation and the combined draft result/value-of-information memo.
  Bounded Codex delegates extracted Cambrian/Argentine material, audited M3,
  checked pipeline reuse and independently checked the parent's source mappings,
  sampling arithmetic and synthesis. The parent integrated and adjudicated the
  findings, including explicit non-admission under all readings. No binding M1/M3
  result or F3/ASR model edit was made; cross-system counter-review remains pending.
  Earlier on 31 October, critiqued and revised Claude's two-sprint proposal, with a
  bounded independent methodological check. The revision specified identifiability,
  source-admission and qualification limits and the sequential counter-review;
  it did not execute either sprint or adopt new scientific results.
  On the next 31 October tranche, mapped Libya's 164 appendix entries to prose
  scopes and 158 enclosure rows to species/productivity reports. An independent
  delegate checked the prose and then all target/marine row states by raster
  rendering; two others reviewed the scoped F3 contract and saved four-chain ASR
  diagnostics. The parent integrated the source conflicts, reproducible extraction,
  checks and proposed design comparison, and reproduced the decisive model and
  MCSE calculations. No binary conversion or empirical F3 bound was adopted.
  On 31 October 2026, independently reviewed the new design screen and trilete
  persistence implementation, and assembled Qusaiba and Libya candidate sample
  inventories. Three bounded same-model delegates checked the F3 contract, ASR
  calculations and Saudi primary sources; the ASR reviewer also independently
  transcribed Libya's appendix. The parent verified decisive source passages and
  calculations, reconciled competing inventories and integrated provenance and
  review records. The review exposed limits of the screen's universal claim,
  unassessed Monte Carlo precision and reference-transport constraints. No full
  stochastic rerun, empirical F3 analysis or source-reading change was made.
  On 30–31 October 2026, mapped all 34 Borenshult samples by event and named
  reading, with separate source-age alternatives and shared-dependence evidence.
  Three bounded same-model delegates checked the remaining validation repair,
  decisive expanded-pilot specimens, and Borenshult source ages/reporting. The
  parent verified the charts and critical source passages, preserved the existing
  readings, integrated 204 new outcome rows and extended the unit integrity checker.
  The review identified absent positive main-reading E1 reference support, subzone/
  contact discrepancies and remaining specimen-inference qualifications. No empirical
  F3 fit or new ancestral-state analysis was run by this tranche.
  Later on 2026-10-29, reviewed the trait-to-node pilot and third F3 contract repairs,
  with two same-model delegates checking acceptance/logic and pivotal primary
  specimens. The parent wrote a source-hashed extractor for Hooper's deposited
  ancestral-state marginals and an independent R/ape node/value check, retaining
  every state and distinguishing published outputs from new inference. The review
  exposed a dispersal/aperture disagreement across separately modelled characters,
  specimen-to-taxon transfers and remaining acceptance gaps; recommendations were
  returned to Claude without editing his methods or pilot specification.
  On 2026-10-29, discussed innovation chronology and first-paper scope with Barry,
  recorded the agreed bounded trait pilot and deferred joint model, and independently
  checked Claude's second F3 repairs and rehearsal receipts. Three same-model delegates
  checked target/status mathematics, the calibration contract, and Ghelli source scope;
  the parent integrated findings, verified decisive rows and rendered source evidence,
  and added a qualified 27-sample inventory without inferred binary outcomes.
  private reading portal and taxon atlas, source-preserving rendering, image sourcing,
  independent implementation review and browser checks (2026-10-27); browser acquisition and
  provenance verification of Rubinstein et al. (2010) and its supplement, and acquisition of
  pivotal literature and supporting information through UTAS and public repositories (2026-10-28).
  On 2026-10-29, joint and autonomous Chrome diagnosis recovered seven previously
  unresolved texts (six publisher PDFs and one author preprint), with source and
  file verification; bounded `gpt-5.6-luna` executor/scout delegates checked public
  repository routes and connectivity. `docs/audits/2026-10-29-literature-recovery.md`
  records the roles, versions and remaining blockers.
  A further authorised six-paper batch secured six full texts and one supplementary
  document (Barry supplied Liu 2016 via the in-app browser; Codex verified it); two bounded `gpt-5.6-luna` delegates checked metadata and local file QA.
  `docs/audits/2026-10-29-six-paper-batch.md` records versions, checks and the resolved
  access history; no scientific extraction was performed in this tranche.
  The parent then recovered and verified both Stage B ResearchGate author uploads
  (Mehlqvist 2012 and Wellman chapter 29), reconciling the already held supplement;
  no subagent or human login was needed (`docs/audits/2026-10-29-researchgate-author-copies.md`).
  Subsequent regional-spore and autonomous collection used in-app and institutional
  browser routes, public author/repository copies and bounded gpt-5.6-luna metadata/
  file-QA delegates. The autonomous expansion secured 97 main texts, 46 supporting
  files and one erratum; the parent reconciled omissions, source versions and the
  distinction between scanned pages and extractable text. The autonomous
  audits dated 2026-10-29 record the checks and limitations. Scientific extraction
  and adjudication are separate work.
  The focused Tier 1 pass of 29–30 October secured 39 new main texts, ten new supporting files,
  two abstracts and one qualified component copy, with three existing Morris files mirrored
  for reading. Three bounded `gpt-5.6-luna` delegates checked public routes, metadata and QA;
  the parent owned browsers, source-identity corrections and registration. Scientific readings
  remain with the main agents (`docs/audits/2026-10-30-first-study-tier1.md`).
  The authorised Tier 2 pass (2026-10-30) secured 30 new main texts and reconciled twelve
  exact existing works. Three bounded `gpt-5.6-luna` executors checked public/repository
  routes, source metadata, file QA, prior holdings and the parent's integration draft;
  the parent handled institutional browsers, corrected provenance/status ambiguities,
  registered the sources and retained office-action blockers. The audit distinguishes
  original PDFs, a BHL reconstruction, abstracts, partials and copied datasets; no
  scientific extraction or adjudication was performed in this acquisition tranche
  (`docs/audits/2026-10-30-first-study-tier2.md`).
  Barry and the counterpart MacBook Codex session then recovered 35 exact main texts
  and one intended abstract through joint browser actions, supplied files and a supplied
  deep-research package (underlying system not identified in this integration). The mini
  Codex parent copied the complete folder, retained reported source provenance, filed
  42 PDFs, and closed twelve residual acquisition gaps at Barry's instruction. Two bounded
  `gpt-5.6-luna` delegates independently reconciled source identities/outcomes, checked all
  PDF bytes/pages and representative renders, and reviewed register integration. This was
  acquisition/provenance work, without scientific extraction or adjudication
  (`docs/audits/2026-10-30-macbook-literature-return.md`).
  From 2026-10-28, a direct scientific and repository collaborator at Barry's request:
  methodological review of the F3 reshape, independent checks of recovery outputs and
  calibration provenance, and direct discussion with Claude through the private Correspondence
  section `silurian-plants`. The F3 review used two `gpt-5.6-sol` specialist subagents for
  methodological and effort-data checks, integrated and checked by the parent session;
  `docs/audits/2026-10-28-f3-reshape-codex-review.md` records the evidence and limitations.
  The v2 follow-up (`docs/audits/2026-10-28-f3-reshape-v2-codex-review.md`) adds a draft
  sampling-unit interface and checks the proposed bound and validation rule, with a bounded
  follow-up by the same methodological specialist and parent verification of the calculations.
  On 2026-10-29, implementation review, a 15-block sampling-unit pilot and the bounded Q9
  provenance check; two `gpt-5.6-sol` specialists checked methods and source evidence, and a
  `gpt-5.6-luna` executor built the archive inventory. Parent review corrected an extra burn-in
  deletion and retained unconditional coverage as the primary inferential target after challenging
  a proposed conditional-coverage requirement. The corresponding audits and `data/units/` record
  which findings are verified, which recommendations await Claude, and which evidence remains
  unsuitable for analysis.
  The subsequent repair review accepted the chord/Jensen construction and independently
  checked the saved development grid, with two `gpt-5.6-sol` specialists; it identified the
  remaining target/calibration and numerical-status issues. A `gpt-5.6-luna` scout checked
  Hanadir sample provenance and bounded Balme access routes. The parent integrated the
  Hanadir frame inventory, a qualified reporting-rule proposal and data-integrity checks
  (`docs/audits/2026-10-29-f3-repairs-and-frame-review.md`), preserving the completed Q9 work.
  On 2026-10-30 the parent integrated independent checks of Claude's validation repairs,
  decisive specimen links and the Ghelli 2002 locality. It assembled and independently
  reconciled the 34-depth Borenshult inventory and inspected the Hooper workspace for saved
  branch histories. The three delegates used the inherited Codex model (exact variant not
  exposed); no new ensemble or evolutionary reconstruction ran. Findings and pending
  corrections are separated in `docs/audits/2026-10-30-frame-and-pilot-review.md`.

- F3 article reconstruction (10–11 November 2026), following Barry's stepwise method: Claude drafted
  each step (main message, abstracts, one-page paper, section and paragraph abstracts, full draft,
  final detailing), built figures 1–4 and integrated the result into the canonical products; Codex
  (`gpt-6.1-sol`) reviewed and revised every step, read the candidate references (with Claude
  checking quotes verbatim), confirmed the half-rate ledger claim C53 and repaired the figures'
  scientific contracts. A Claude Sonnet subagent aligned the agent guide. Barry chose the main
  message and set each step. Record: `manuscript/reconstruction/README.md`.
- Graphical abstract (12 November 2026), at Barry's request, for the journal and as the brief's figure:
  Claude (Opus 5.5) designed and drew it from the reviewed output tables (`manuscript/figures_abstract.py`)
  and trimmed the brief to keep two pages; a Claude Sonnet subagent tested it cold for lay comprehension,
  which led to direct scenario labels, plain glosses and a stated distinction between requirements and
  95% limits.
- General-points review (13 November 2026): Codex used three bounded independent checks of the
  primary spore sources, outside-proxy calculations and count/rise mathematics, then integrated the
  findings into the article, supplement and claims C54–C57. The reviewers inherited the session's
  Codex model; its exact variant was not exposed. The source check narrowed the secure Libyan
  comparison to Saudi Arabia and Turkey; separate calculations verified the numerical outputs,
  distinguished finite from unlimited exponential compatibility, and restricted proxy comparisons
  to descriptive ratios. Codex added case-specific numerical bindings. Barry's line-edit pass and the
  later brief/agent-guide product pass remain separate from this verification.

`docs/decisions.md` records who decided what and when, for the eventual statement of AI roles.
