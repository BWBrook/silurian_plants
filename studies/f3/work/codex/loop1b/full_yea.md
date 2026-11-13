You are checking the age evidence for the Baragwanathia-bearing "Lower Plant Assemblage" localities near Yea, Victoria, Australia, against primary and secondary full texts, for a research programme on early land-plant evolution (repository: this directory). Whether these lycopsids are Silurian (Gorstian/Ludlow or Pridoli) or Early Devonian decides the first appearance of event E5 (lycophyte-line bodies) and bears on E4. The project carries several readings for each locality and needs to know exactly what the sources say, who observed what, and where the graptolites are relative to the plants.

Observations and their current interpretations: `work/codex/loop1b/yea_observations.csv` and `work/codex/loop1b/yea_interpretations.csv` (5 observations, 13 interpretations). Also read `taxa/baragwanathia-flora.md` and entry 17 of `docs/rejected-records.md`.

Source files (paged text):

1. `library/closed/text/rickards2000.paged.txt` — Rickards (2000), Geological Magazine, "The age of the earliest club mosses".
2. `library/closed/text/garrattrickards1987.paged.txt` — Garratt & Rickards (1987), Bulletin of the Geological Society of Denmark, Pridoli graptolites with Baragwanathia.
3. `library/closed/text/garratt1983.paged.txt` — Garratt (1983), Proceedings of the Royal Society of Victoria 95: 77–98, Silurian and Devonian biostratigraphy of the Melbourne Trough. It is part of a scanned volume: use only the pages belonging to this paper. Printed p. 81 is said to carry the Yea graptolite evidence.
4. `library/closed/text/jelinek2008_garratt1978_map.paged.txt` — a 2008 public submission that reproduces Garratt's 1978 geological map (PDF page 12). Treat it as a secondary reproduction; report only what it shows about locality positions and units, and note its non-scientific context.
5. `library/closed/text/earp2023_yea_review_first_draft.paged.txt` — Earp (2023), an unreviewed author-posted first draft reviewing earlier geological work in the Yea district, including Garratt (1978). Report its arguments as arguments of an unreviewed draft, and keep its observations (what it says was or was not found where) separate from its interpretations.

Garratt (1978, Alcheringa 2: 217–224) itself is NOT available. Report what each of these texts says Garratt (1978) claimed, labelled as secondary reports.

For each locality (Ghin Ghin Road; Limestone Road / Brackley's Cutting; the unspecified "Yea" PBDB record; and the Wilson Creek Shale type material if any source mentions it), establish:
- which graptolite taxa were found, by whom, and the zone or series age assigned;
- whether the graptolites come from the same bed as the plants, a nearby bed (how far above or below), or a different section correlated by mapping;
- what other age evidence exists (brachiopods, conodonts, shelly faunas, mapping), and which way it points;
- the arguments for and against a Silurian age, including any evidence of misidentified graptolites, disturbed or redeposited material, or locality confusion (for example a road-making stockpile);
- the ICS v2024/12 stage(s) each reading implies (Gorstian, Ludfordian, Pridoli, Lochkovian, Pragian, Emsian).

Return findings across all five files. Expect 40–100 findings.
## Rules for every job

- Do not edit any file. Return JSON only, matching the schema.
- Read the project conventions in `AGENTS.md`, the schema in `data/occurrences/README.md`, events E1–E5 in `docs/plan-f3.md` ("Target events"), and the stage table `data/timescale.csv`.
- Your sources are ONLY the paged text files named below (full texts the project obtained legally; extracted from PDFs, with `=== PDF page N ===` markers). Do not use web search. Do not use memory for facts: every finding must rest on a quotation from one of these files.
- `quote` is a verbatim, contiguous quotation from the file, 40 words or fewer. Copy it exactly as it appears in the text file, including odd OCR spellings, ligature artefacts and abbreviations; do not expand, correct or join across a page marker. A script will check every quote by exact substring match after whitespace and line-break hyphen normalisation, and unverifiable findings are discarded.
- `pdf_page` is the number in the nearest preceding `=== PDF page N ===` marker. `printed_page` is the journal page number if visible on that page, else "".
- `obs_ids`: the observation ids from the supplied CSVs that the finding bears on (may be empty for a finding about something not yet in the data). `bears_on`: the `interp_id` it bears on, or "new" for a reading not yet recorded, or "" if none.
- `effect`: whether the finding supports, contradicts or qualifies that interpretation, proposes a new reading, corrects a recorded field (locality, horizon, unit, locator, stage, held_by, label), or has no bearing.
- Separate observation from interpretation: say in `claim` whether the source reports something it saw (specimens, samples, graptolites in the same bed) or argues an interpretation (correlation, affinity).
- Ages: map any age statement to ICS stage names in `data/timescale.csv` in `comment`, and say which stage(s) the source's wording allows. Note where the source uses an older series/stage scheme (e.g. "Ludlow", "Whitcliffian", "Ashgill", "Caradoc", "Middle Cambrian") and what that implies in ICS v2024/12 stages. Do not resolve a disagreement between sources: report both sides.
- `recommendations`: one or more per observation id supplied (and any new observation the texts justify), each citing the finding_ids it rests on. Use `upgrade_checked` when a reading previously checked only from a card or abstract is now confirmed in the full text. Use `uncertain` rather than guess.
- Aim for completeness on what decides each reading (identity, age and its basis, stratigraphic relation between dated fossils and plants, evidence for or against reworking or later contamination). Typically 6–20 findings per source file.
