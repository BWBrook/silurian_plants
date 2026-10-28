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
  design, synthesis, framings, tooling.
- Claude Sonnet 5.5 (Anthropic) subagents: literature research and first drafts of taxon cards,
  the primer (including its biological-transitions section, 2026-10-28), the precedents review and
  the rejected-records note; adjudication of audit findings
  against the sources and the resulting corrections; blind audits.
- OpenAI Codex CLI, `gpt-6.1-sol` and `gpt-6.1-terra` at high reasoning effort, run by Claude Opus
  5.5 as read-only, schema-constrained jobs through `~/.claude/bin/codex-delegate` (2026-10-27 and
  28). Records are in `docs/audits/` and the job files in `data/spores/work/codex/` and
  `work/codex/`. Work done:
  - spore genus, age-name and location crosswalks;
  - digitisation of the Wellman et al. (2013) supplement;
  - vetting of early spore records;
  - extraction of post-2006 spore assemblages;
  - the Model transfer retrofit of 59 cards, with a consistency review of them;
  - cross-family audits of the new cards and of the primer revision;
  - one card draft for a bake-off.
- OpenAI Codex (OpenAI, Codex desktop; exact model version not exposed in this session):
  private reading portal and taxon atlas, source-preserving rendering, image sourcing,
  independent implementation review and browser checks (2026-10-27).

`docs/decisions.md` records who decided what and when, for the eventual statement of AI roles.
