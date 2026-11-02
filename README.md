# silurian_plants

> **Status:** developed in the open as a working record. This is work in progress: contents may change, and nothing here is peer-reviewed unless stated.

A long-term programme on simulation modelling of the evolution of early land plants, from the
Late Ordovician to the Early Devonian (c. 458–393 Ma). See [docs/charter.md](docs/charter.md) for
the purpose, the criteria a framing must meet and the planned route.

## Contents

- Reading portal (private; not publicly accessible): illustrated
  reading room, searchable taxon atlas and full-text search, generated from the Markdown.
  Build and refresh instructions are in [portal/README.md](portal/README.md).

- [taxa/](taxa/README.md): information cards on key taxa, one per file. Each card's front matter
  is a structured trait record; the prose covers morphology, age, affinity, ecology and relevance
  to modelling.
- [docs/primer.md](docs/primer.md): timescale, palaeogeography, climate, phylogeny and the nature
  of the fossil record.
- [docs/precedents.md](docs/precedents.md): what has already been modelled, and the gaps.
- [docs/framings.md](docs/framings.md): candidate research questions and a recommendation.
- [docs/sources.md](docs/sources.md): register of every data source held or still needed.
- [docs/spore-compilation-plan.md](docs/spore-compilation-plan.md): plan for the dispersed-spore
  occurrence dataset.
- [docs/decisions.md](docs/decisions.md): dated decision record.
- [data/timescale.csv](data/timescale.csv): ICS v2024/12 stage ages.
- [data/eprp/](data/eprp/README.md): literature, PBDB and Macrostrat records, Earth-system context
  and software pointers extracted from Barry's EPRP programme.
- [docs/audits/](docs/audits/): independent checks of the cards and of the EPRP deposit.
- [tools/cards.py](tools/cards.py): card validation, Crossref DOI checks and index generation
  (`uv run tools/cards.py check|dois|index`).

## People and AI systems

Barry W. Brook (University of Tasmania) with Claude Opus 5.5 and Claude Sonnet 5.5 (Anthropic)
working in Claude Code. Roles are recorded in [docs/charter.md](docs/charter.md).

OpenAI Codex implemented the private reading portal; its role is recorded in the charter.

## Third-party data

Third-party datasets, supplements and code deposits are not stored in this repository. Fetch the
openly licensed deposits with `python3 data/external/scripts/deposits_fetch.py`: it reads
[data/external/deposits/MANIFEST.tsv](data/external/deposits/MANIFEST.tsv), writes into the git-ignored
`data/external/local/deposits/` and checks every file against its sha256. Licences and the other
fetch-only sources are in [THIRD_PARTY.md](THIRD_PARTY.md).

## Licence

Code is released under the [MIT Licence](LICENSE). Text, figures and data created for this project are released under [CC BY-SA 4.0](LICENSE-CONTENT). Third-party material keeps its own terms where stated: see [THIRD_PARTY.md](THIRD_PARTY.md).
