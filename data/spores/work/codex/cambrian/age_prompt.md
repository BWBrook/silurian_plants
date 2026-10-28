You are extending a stratigraphic crosswalk for a palaeobotany research dataset in this repository (read AGENTS.md; do not edit any file).

Context: the project's timescale (`data/timescale.csv`, ICS v2024/12) now includes the ten Cambrian stages (Fortunian, Stage 2, Stage 3, Stage 4, Wuliuan, Drumian, Guzhangian, Paibian, Jiangshanian, Stage 10). The existing crosswalk `data/spores/crosswalks/age_names.csv` maps Palynodata age names to ICS stages; until now the table started at the Tremadocian, so Cambrian and Precambrian names were "clamped to Tremadocian" with low confidence. That clamping is now wrong. The crosswalk is used to count palynological documents per stage, including in the Cambrian, as evidence of where palynologists sampled.

Input: `data/spores/work/codex/cambrian/ages.csv` lists 71 age names (column age_name), with row and document counts, Palynodata's own numeric range for rows using the name (on Palynodata's 2006-era timescale, which places the Cambrian at about 570–505 Ma), and the current (to-be-replaced) mapping if any. Read the WHOLE file.

For EVERY age name (all 71; copy age_name exactly, including misspellings such as "Precambrain" or "Middle Cambria") return:
- ics_oldest and ics_youngest: stage names exactly as in data/timescale.csv.
  - Cambrian series names map by their standard correlations: e.g. a traditional "Early/Lower Cambrian" is Terreneuvian plus Series 2; a traditional "Middle Cambrian" is approximately the Miaolingian, but its base differs by region (say so, and set confidence accordingly); "Late/Upper Cambrian" is approximately the Furongian. Regional stages (Siberian Tommotian, Atdabanian, Botomian, Toyonian, Amgan, Mayan; Baltic and British Caerfai, Solvan/St David's, Menevian, Merioneth; Avalonian/Laurentian Acadian, Georgian, Potsdamian; Iberian Cordubian, Ovetian, Marianian; Estonian Pakerort, Varangu, etc.) need correlation charts: use web search to read them and cite what you read.
  - Names that are wholly Precambrian (Ediacaran, Vendian, Sinian, Riphean, Cryogenian, Algonkian, Brioverian, Torridonian, Longmyndian, Keweenawan, Archean, etc.): leave both fields empty ("") and say "wholly Precambrian; outside the table" in basis. Names that straddle the Precambrian–Cambrian boundary (e.g. Eocambrian, Yudoma, Late Proterozoic used loosely, Varangian if your sources say so): map to the Cambrian part if the name is commonly understood to include the basal Cambrian, with confidence low, and explain.
  - Names extending into the Ordovician or later (e.g. "Early Paleozoic", "Cambrian–Ordovician" wording): give the full span to the youngest stage in the table (Emsian or later) and set confidence low.
  - Leave both empty if the name is too broad or unmappable.
- confidence: high (standard global series or stage name with a defined correlation), medium (regional unit with a published correlation), low (broad, straddling, or uncertain).
- basis: a short phrase.
- source: a correlation source you actually read (author, year, title or URL), or "ICS v2024/12 stage and series list (data/timescale.csv)", or "none checked". Do not invent sources.

Return JSON only, matching the schema, with exactly 71 items.
