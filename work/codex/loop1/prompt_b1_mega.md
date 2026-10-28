You are compiling the oldest part of the land-plant body-fossil record for a research programme on early land-plant evolution. Do not edit any file; return JSON only.

Read first:
- `AGENTS.md` (conventions);
- `data/occurrences/README.md` (the schema you must fill; follow it exactly);
- `docs/plan-f3.md` (why: events E3, E4 and E5);
- `docs/rejected-records.md`;
- the cards in `taxa/` that bear on the oldest body fossils. At least: `cooksonia.md`, `rhyniophytoids.md`, `zosterophyllum.md`, `zosterophylls.md`, `bathurst-island-flora.md`, `baragwanathia-longifolia.md`, `baragwanathia-flora.md`, `early-lycopsids.md`, `tortilicaulis-offaeus.md`, `zbrza-assemblage.md`, `eophytes.md`, `welsh-borderland-mesofossils.md` if present. Use `rg` to find others that mention Ordovician, Llandovery, Wenlock, Ludlow or Pridoli body fossils.
- `work/codex/loop1/pbdb_pre_pridoli.csv`: 114 Paleobiology Database plant occurrences whose maximum age is older than the Pridoli base. Triage them all.

Task: build observations, interpretations and sources for every claimed body fossil (megafossil or mesofossil) that bears on:
- E3, polysporangiophyte bodies, Homerian or older;
- E4, tracheids in situ, Pridoli or older;
- E5, lycophyte-line bodies (zosterophylls, lycopsids), Pridoli or older.
Include rejected and disputed claims (they are what the analysis tests), and the calibration fossils of Hooper et al. (2026): *Cooksonia* cf. *pertoni*, Homerian Cloncannon Formation, Borrisnoe Mountain, Ireland; and *Zosterophyllum* sp., Ludlow, beds equivalent to the Bathurst Island and Stuart Bay Formations, Bathurst Island.

Rules:
- One observation per reported material, meaning one assemblage or specimen set at one locality and horizon. PBDB rows that duplicate a card or literature record get `same_material_as` pointing to the literature observation, not a separate count; PBDB rows that are not plants, or are not relevant to E3–E5 (for example algae, acritarchs, unassignable fragments without plant characters), should be listed in `excluded_pbdb` with a one-line reason instead of becoming observations.
- Give every observation at least one interpretation, and every disputed one an interpretation for each published reading (for example: accepted as Gorstian lycopsids on graptolites; mostly Early Devonian on brachiopods and mapping). A rejection is an interpretation with empty `counts_for`.
- Ages are ICS stage names exactly as in `data/timescale.csv`, as a range `stage_oldest`–`stage_youngest`; put radiometric or maximum-depositional ages and the basis in `age_note`.
- Set `main` to "true" for exactly one interpretation per observation: the reading of the most recent substantive published assessment, or, where the repository's cards or `docs/rejected-records.md` already adopt a reading, that one. Explain the choice in `main_basis`.
- `support` is a verbatim quotation (40 words or fewer) from the cited source if you read it, or from the repository file that states it; `support_from` is the DOI/URL or repository path; `checked` says which (`full-text`, `abstract`, `card`, `repo-doc`, `secondary`). Quotations from repository files must be exact substrings of those files, so that they can be checked by script.
- Sources: `source_id` as first-author surname plus year (lowercase, a/b suffix if needed); citation with authors, year, title, journal, volume, pages; DOI only if you verified it; otherwise blank.
- Use web search only to read sources (publisher pages, open repositories, PMC); never invent a source, a quotation or a DOI. Do not bypass paywalls or bot checks. Never send an email address or other personal data to any service.
- Expect roughly 30–80 observations. Completeness for E3–E5 matters more than detail.
