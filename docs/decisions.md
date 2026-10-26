# Decisions

Dated record of decisions that shape the programme. Newest first. Say who decided, and quote
Barry exactly (with source) or label a paraphrase.

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
- **Timescale** (Claude): ICS International Chronostratigraphic Chart v2024/12 (GTS2020 ages),
  held once in `data/timescale.csv`. Cards record stage names, and ages are derived from the table,
  so a later timescale revision is a one-file change.
- **First tranche** (Claude): 24 cards across five themes (earliest embryophyte evidence,
  rhyniophytoids and the Rhynie Chert, lycophyte lineage, early euphyllophytes, non-embryophyte
  terrestrial organisms), a period primer and a review of modelling precedents, drafted by
  Claude Sonnet 5.5 subagents with web literature search, then checked by Claude Opus 5.5.
