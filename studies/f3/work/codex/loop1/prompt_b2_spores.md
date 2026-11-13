You are compiling the oldest part of the dispersed-spore record of land plants, with its disputes, for a research programme on early land-plant evolution. Do not edit any file; return JSON only.

Read first:
- `AGENTS.md`;
- `data/occurrences/README.md` (the schema; follow it exactly);
- `docs/plan-f3.md` (events E1 trilete spores, E2 cryptospores);
- `docs/rejected-records.md`, especially entries 10 (Cambrian–Tremadocian polyads), 15 (Swedish Sandbian trilete spores) and 16 (Argentine Dapingian cryptospores);
- the cards `taxa/ordovician-cryptospores.md`, `taxa/ambitisporites.md`, `taxa/eophytes.md`;
- `docs/primer.md` §5.3 (Hooper et al. 2026 calibrations).

Inputs:
1. `work/codex/loop1/out/a_table.json`: the 48 rows of Table 1 of Wellman, Cascales-Miñana & Servais (2022), "Terrestrialization in the Ordovician" (dispersed spore assemblages reported from the Ordovician, codes H1–Dp2, with two footnotes). The full text is `library/open/W4306698490.txt` (CC BY). Read its text on cryptospores and trilete spores, to learn which assemblages contain trilete spores and which records the authors doubt.
2. `data/occurrences/observations.csv` and `interpretations.csv`: 110 spore observations already built from the project's vetted dataset (IDs `S-palynodata-...`, `S-mvdb-...`, `S-wellman2013-...`). Do not repeat them; link to them.

Task:
- **Wellman 2022 rows.** Make one observation per Table 1 row, `obs_id` `S-w22-<code>` (e.g. `S-w22-K11`). Set `channel` "spore". Set `events` to "E2", or "E1;E2" where the paper or its cited sources report trilete spores in that assemblage. Set `same_material_as` to the existing observation's ID when an existing observation reports the same assemblage (same region, unit and age); otherwise leave it blank.
- **Interpretations for those rows.** Give each row Wellman et al.'s reading: stage range from the printed stage. A "?" widens the range by one stage on the uncertain side; "Katian-Hirnantian?" becomes Katian–Hirnantian, and the "?" is noted in `age_note` with the dating basis. Where a footnote or another source disputes the record, add the competing interpretation:
  - the "*" footnote on S2: Rubinstein & Vajda 2019;
  - the "**" footnote on Dp2: Strother et al. 2015.
- **Records outside the table.** Add observations, with all published readings, for:
  - the Swedish Sandbian trilete spores of the Borenshult-1 core (Rubinstein & Vajda 2019), which Hooper et al. (2026) use as the soft maximum (459.1 Ma), while doubting that the trilete marks are real;
  - the *Ambitisporites avitus* record of the Qusaiba-1 core, core 56 at 551.0 m, Qasim Formation, Saudi Arabia, which Hooper et al. use as the earliest unequivocal trilete spore. Link it to an existing observation if one matches;
  - the Cambrian to Tremadocian irregular polyads (`docs/rejected-records.md`, entry 10);
  - the Ordovician spore-filled sporangial fragments of Oman (Wellman et al. 2003), if not covered by K12.
- **Main reading.** Set `main` "true" for exactly one interpretation per observation: the most recent substantive published assessment, or the reading `docs/rejected-records.md` or a card already adopts. Explain it in `main_basis`.
- **Support.** `support` is a verbatim quotation of 40 words or fewer. Quotations from repository files, including `library/open/W4306698490.txt`, must be exact substrings so they can be checked by script; give that path in `support_from`. `checked` uses the schema's values.
- **Sources.** `source_id` is the first author's surname plus year, lowercase, with an a/b suffix if needed: for example `wellman2022`, `rubinstein2019`, `strother2015`, `hooper2026`. Add a DOI only if you verified it; leave it blank otherwise.
- **Web search.** Use it only to read sources. Never invent a source, quotation or DOI. Do not bypass paywalls or bot checks. Never send an email address or other personal data to any service.
- **Leave `excluded_pbdb`** as an empty list. Use `notes` for anything the orchestrator must know, especially any record whose reading would move the first appearance of E1 or E2 by a stage or more.
