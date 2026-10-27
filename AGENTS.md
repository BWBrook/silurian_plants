# silurian_plants: agent guidance

Exploratory, long-term programme on simulation modelling of early land-plant evolution, Late
Ordovician to Early Devonian (c. 458–393 Ma). Read `docs/charter.md` for purpose, stage and
route, and `docs/decisions.md` for what has been settled. Current stage: orientation; no
research question has been chosen, so do not start model code without a framing decision
recorded in `docs/decisions.md`.

## Layout

- `taxa/`: one information card per taxon. `taxa/_template.md` is the schema; `taxa/README.md`
  is generated.
- `docs/`: charter, decisions, primer, precedents review, candidate framings, the source register
  (`docs/sources.md`, the index of all data held and needed: update it when a source changes) and
  the spore-compilation plan.
- `data/timescale.csv`: ICS v2024/12 stage base ages, the single source of numerical ages.
- `data/traits.csv`: generated trait matrix, one row per card.
- `data/eprp/`: material extracted from Barry's EPRP programme: literature, PBDB and Macrostrat
  records, climate and palaeogeography context, and software pointers. Treat it as inputs, not
  verified facts. Read each area's README before use, and regenerate tables with its scripts
  rather than editing them. `data/eprp/local/` is git-ignored (unlicensed, no-derivatives or bulky
  material) and exists only on mac-mini; rebuild it from `deep-server` with the scripts.
- `docs/audits/`: independent checks of cards and deposits.
- `tools/cards.py`: card validation, DOI checking and index generation.

## Commands

```bash
uv run tools/cards.py check   # schema and vocabulary
uv run tools/cards.py dois    # DOIs in taxa/ and docs/ against Crossref
uv run tools/cards.py index   # regenerate taxa/README.md
uv run tools/cards.py matrix  # regenerate data/traits.csv
```

Run `check`, `index` and `matrix` after editing cards, and `dois` after adding references.

## Conventions

- Facts, numbers and citations come from sources read in the task, never from memory. Every
  DOI is verified against Crossref; never guess one. In references lists, one reference per line
  with first author, year, title and DOI, so `dois` can compare them.
- When a source cannot be read in full (paywall, blocked supplement, print only), add it to
  `docs/closed-literature.csv` with what it would settle; Barry obtains these through his
  institutional login. Never bypass access controls. PDFs he obtains go in `library/closed/`,
  which is git-ignored: copyrighted texts are never committed.
- Never send Barry's email address or other personal data to any service or API, including ones
  that ask for a contact email.
- Separate observation, interpretation and speculation; present disputes with both sides.
- Cards record ages as ICS stage names; give finer ages in `range.notes` with their source.
  Literature before 2024 mostly uses the GTS2012 Early Devonian boundaries (Lochkovian 419.2,
  Pragian 410.8, Emsian 407.6 Ma), which differ from ours by up to 3 Myr; see `docs/primer.md` §1.
- Card traits: `absent` means observed absent, `unknown` means not preserved or not reported,
  `na` means not applicable. Add vocabulary to `tools/cards.py` when a real case needs it.
- A card is `draft` until a second agent or Barry has checked its facts; then `reviewed`.
- British spelling. Dense, precise prose; no filler.
- Record decisions that shape the programme in `docs/decisions.md`, naming who decided. Keep
  the AI-roles section of `docs/charter.md` current: the work will be published with a full
  statement of which systems did what.
- Commit to `main` when work reaches a coherent state, and push.
