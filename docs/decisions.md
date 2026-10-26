# Decisions

Dated record of decisions that shape the programme. Newest first. Say who decided, and quote
Barry exactly (with source) or label a paraphrase.

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
