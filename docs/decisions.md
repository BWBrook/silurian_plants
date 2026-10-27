# Decisions

Dated record of decisions that shape the programme. Newest first. Say who decided, and quote
Barry exactly (with source) or label a paraphrase.

## 2026-10-27: spore dataset (MVD-A), Codex delegation, closed-literature register

- **Codex as the legwork engine** (Barry, chat, 2026-10-27): "you can be rather spendthrift on what
  legwork you outsource to Terra or Sol". Codex does schema-constrained, machine-checkable work;
  Claude keeps synthesis, judgement and adjudication. The pilot is in
  `docs/audits/2026-10-27-codex-pilot.md`; the practice is in `CLAUDE.md` and the global
  `codex-delegate` skill.
- **Closed literature** (Barry, chat, 2026-10-27): "we should keep a register of it, such that I
  can secure it via institutional login if/as required". The register is
  `docs/closed-literature.csv` (419 rows, priority-sorted, with DOI links). Copies Barry obtains go
  in git-ignored `library/closed/`.
- **Spore dataset MVD-A** (Claude, built with Codex and Sonnet): `data/spores/`, combining
  Palynodata and the digitised Wellman et al. (2013) assemblages through age, location and genus
  crosswalks.
  - Early records were vetted in two passes, then a blind cross-family audit checked a sample:
    83% agreement on accept vs not-accept, and two verdicts were adjudicated.
  - Strict first appearances: cryptospores certain by 458.2 Ma, trilete spores by 445.2 Ma.
  - Not yet included: the post-2006 literature (MVD-B) and spore-absent sampling effort.
- **Literature harvest** (EPRP, item 8): phase 1 committed (6,312 works; 183 priority spore
  papers). Phase 2, open texts for the spore and card subsets only, was approved by Claude under
  Barry's go-ahead.

## 2026-10-27: evidence base, tranche 2

- **Scope** (Barry, chat, 2026-10-27): before commenting further on the hypothesis, fill out the
  core evidence base, "to make sure all the relevant data on the time period in question and all
  the specimens (from databases) are properly sourced, indexed and extracted", continuing to work
  with the EPRP session as required.
- **Source register** (Claude): `docs/sources.md` lists every held and missing source with status,
  licence and who does the work. Database and deposit work goes to the EPRP session (request sent
  2026-10-27); literature extraction stays here.
- **Cards, tranche 2.** Barry proposed:
  - the Victorian taxa *Yarravia*, *Hedeia* and *Pluricaulis biformis*; *Dawsonites*; *Palaeostigma*;
  - living comparison taxa *Psilotum*, *Tmesipteris* and *Lycopodium squarrosum*;
  - *Parka*, *Ulothrix* and *Ulva*;
  - group cards on lycopods and trimerophytes; *Archaeopteris*.

  Claude added:
  - *Coleochaete*, *Chara* and the Zygnematophyceae, because the streptophyte relatives are the
    phylogenetically apt life-cycle exemplars; *Ulva* and *Ulothrix* stay as theory exemplars;
  - hornworts and *Marchantia*;
  - group cards for eophytes, rhyniophytoids and zosterophylls;
  - five site cards (Rhynie, Posongchong, Xitun, Bathurst Island, Welsh Borderland mesofossils)
    and a Baragwanathia-flora card, as sampling units for an observation model;
  - the taxa that tranche-1 agents flagged as missing (*Nothia*, *Baragwanathia brevifolioides*,
    *Metzgeriothallus*, *Franhueberia*, *Salopella*);
  - *Wattieza* and *Leclercqia* as anchors beyond the window.

  35 cards in all, drafted by Claude Sonnet 5.5 subagents.
- **Schema** (Claude): card kinds `extant` and `group`, ranks `grade` and `clade`, and groups for
  chlorophyte algae, ferns, progymnosperms and cladoxylopsids. `data/timescale.csv` gains the
  Frasnian, Famennian and Tournaisian bases (ICS v2024/12) for the anchors; the existing rows are
  unchanged.
- **Dispersed spores** (Claude): a scoping study (`docs/spore-compilation-plan.md`) runs in
  parallel with EPRP's check of Palynodata, before any compilation starts.
- **Spore and climate sources found** (EPRP session; reviewed by Claude):
  - Palynodata (GSC Open File 5793, OGL-Canada), with 14,114 window spore rows from 985
    documents, extracted as-is into `data/external/spores/`;
  - HadCM3L land climate (`scotese_02` suite, CC BY 4.0) in `data/external/climate/`.

  Asking Wellman, Steemans and Vecoli for their full 2013 assemblage database is an external
  contact and therefore Barry's decision.
- **Tranche-2 card audit** (two independent Sonnet agents, 8 cards, 99 claims): 80 supported,
  0 wrong, 2 misattributed, 9 imprecise, 9 unverifiable; all fixed
  (`docs/audits/2026-10-27-tranche2-audit-*.md`). The audit confirmed that *Hedeia* is a junior
  synonym of *Yarravia* (McSweeney et al. 2021) and that *Pluricaulis biformis* is an unpublished
  manuscript name. It corrected the *Prototaxites* first-occurrence basis. Both cards stay, with
  their status stated, because they are the names in older literature and in PBDB.
- **Process lapses** (Claude, reported to Barry): a card agent sent Barry's email address to
  Unpaywall's API once; the agent brief now forbids it. A `git add -A` briefly committed the EPRP
  session's unreviewed files; it was reverted within minutes, and only explicit paths are staged
  while another session writes in the tree.

## 2026-10-27: EPRP deposit reviewed and committed

- **Deposit accepted** (Claude, reviewing at Barry's request): `data/eprp/` is committed except
  `local/`, which stays git-ignored. Review: `docs/audits/2026-10-27-eprp-deposit-review.md`.
  All 88 files match their manifest, and the PBDB counts reproduce independently.
- **Facts that changed** (Claude): PBDB holds almost no pre-Emsian spores and only 259 pre-Emsian
  core megafossil occurrences, so F3 needs a dispersed-spore compilation from the literature, and
  its tractability is now moderate. F4's inputs are now on the mesh, so its tractability is
  moderate. Eco-evolutionary vegetation has already been coupled to the carbon cycle for later
  intervals (Rogger et al. 2024, 2026; Gurung et al. 2022), so F5's novelty is moderate.
  `docs/precedents.md` gains an addendum and loses an overstatement; `docs/framings.md` is updated
  to match. The framing choice remains Barry's.

## 2026-10-26: orientation tranche 1 delivered

- **Delivered** (Claude): 24 draft cards, `docs/primer.md`, `docs/precedents.md`,
  `docs/framings.md`, the card index and `data/traits.csv`.
- **Framing recommendation** (Claude, pending Barry's choice): F3 (whether the record supports
  the new timescale, with an observation model) as the first deliverable, and F1 with F2 (the
  rise of the sporophyte) as the core simulation. The precedents review, drafted independently,
  ranked a closed-loop plant–carbon-cycle model (F5) among its top three; `docs/framings.md`
  records the disagreement.
- **Literature that changed the plan.** Hooper et al. (2026, Nature Plants, 22 October) moved
  crown embryophytes to 457–450 Ma and crown tracheophytes to 432–428 Ma, which sharpened F3.
  Loron et al. (2026) argue that Prototaxites was not a fungus. Earp (2024) places the Yea
  Baragwanathia beds mostly in the Early Devonian, which weakens the Silurian-Baragwanathia
  claim. Each is recorded in the relevant card.
- **Card quality** (Claude): a separate Sonnet agent audited a sample of four cards
  (`docs/audits/2026-10-26-card-sample-audit.md`). Of 58 claims, 44 were supported, 0 wrong,
  2 misattributed, 7 overstated and 5 unverifiable. The errors were lost hedges and citation
  drift, not wrong numbers. The nine flagged claims are fixed. All cards stay `draft`: no number
  in them should become a model prior until it has been checked against its primary source.
- **Card conventions settled in use** (Claude): names follow current nomenclature (`Aglaophyton
  majus`, file `aglaophyton-majus.md`); citations use the conventional volume year, and the DOI
  checker accepts the print or online year; DOIs may contain brackets (SICI form).

## 2026-10-26: programme opened

- **Scope** (Barry, chat): Late Ordovician to Early Devonian; exploratory, long-term, may be
  abandoned. Cards and context first, workflows and science later.
- **Repository** (Claude, under Barry's stated intent "we'll want to set up a private GitHub
  repo"): private `BWBrook/silurian_plants`, branch `main`, minimal structure that grows with the
  work.
- **Taxon cards** (Barry proposed; Claude designed the format): one Markdown file per taxon with
  YAML front matter that doubles as a trait record, so the cards can later be compiled into a
  character matrix without re-reading the prose. Traits distinguish `absent`, `unknown` and `na`.
  `tools/cards.py` validates the schema, checks DOIs against Crossref and builds the index.
- **Timescale** (Claude): ICS International Chronostratigraphic Chart v2024/12, held once in
  `data/timescale.csv`. Its Ordovician and Silurian ages are GTS2020's, but its Devonian ages come
  from Harrigan et al. (2022), not GTS2020 (Cohen et al. 2025). The primer agent caught that the
  original wording of this entry, "GTS2020 ages", was wrong; `docs/primer.md` §1.2 compares the
  three scales. Cards record stage names, and ages are derived from the table,
  so a later timescale revision is a one-file change.
- **First tranche** (Claude): 24 cards across five themes (earliest embryophyte evidence,
  rhyniophytoids and the Rhynie Chert, lycophyte lineage, early euphyllophytes, non-embryophyte
  terrestrial organisms), a period primer and a review of modelling precedents, drafted by
  Claude Sonnet 5.5 subagents with web literature search, then checked by Claude Opus 5.5.
