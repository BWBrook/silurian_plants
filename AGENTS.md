# silurian_plants: agent guidance

Exploratory, long-term programme on simulation modelling of early land-plant evolution, Late
Ordovician to Early Devonian (c. 458–393 Ma). Read `docs/charter.md` for purpose, stage and
route, and `docs/decisions.md` for what has been settled. Current stage: orientation; no
research question has been chosen, so do not start model code without a framing decision
recorded in `docs/decisions.md`.

## Layout

- `taxa/`: one information card per taxon. `taxa/_template.md` is the schema; `taxa/README.md`
  is generated.
- `docs/`: charter, decisions, primer, precedents review, candidate framings.
- `data/timescale.csv`: ICS v2024/12 stage base ages, the single source of numerical ages.
- `data/traits.csv`: generated trait matrix, one row per card.
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
- Separate observation, interpretation and speculation; present disputes with both sides.
- Cards record ages as ICS stage names; give finer ages in `range.notes` with their source.
  Older literature uses pre-GTS2020 Early Devonian boundaries, which differ by several Myr.
- Card traits: `absent` means observed absent, `unknown` means not preserved or not reported,
  `na` means not applicable. Add vocabulary to `tools/cards.py` when a real case needs it.
- A card is `draft` until a second agent or Barry has checked its facts; then `reviewed`.
- British spelling. Dense, precise prose; no filler.
- Record decisions that shape the programme in `docs/decisions.md`, naming who decided. Keep
  the AI-roles section of `docs/charter.md` current: the work will be published with a full
  statement of which systems did what.
- Commit to `main` when work reaches a coherent state, and push.
