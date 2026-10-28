You are checking the evidence for Cambrian and Early Ordovician cryptospore-like palynomorphs against the full text and supplement of Strother & Foster (2021), Science, "A fossil record of land plant origins from charophyte algae", for a research programme on early land-plant evolution (repository: this directory).

Why it matters: a recovery study showed that, for spore-based first appearances, the decisive evidence about how old land plants could be is documented palynological sampling in stages OLDER than the first appearance, and whether those samples contained (or lacked) embryophyte-type spores. The project's event E2 is "first cryptospores accepted as embryophytic". Strother & Foster's material lies in exactly that pre-Darriwilian interval.

Observations and current interpretations: `work/codex/loop1b/cambrian_observations.csv` and `work/codex/loop1b/cambrian_interpretations.csv` (2 observations, 6 interpretations). Also read entry 10 of `docs/rejected-records.md`.

Source files (paged text):
1. `library/closed/text/strother2021.paged.txt` (main article)
2. `library/closed/text/strother2021_SI.paged.txt` (supplementary materials)

Establish, with quotations:
- every assemblage or formation the paper uses: name, locality, region, palaeocontinent if stated, age as stated (series/stage, numerical age) and the basis of that age;
- for each, what kinds of palynomorphs occur (dyads, tetrads, polyads, envelope-enclosed forms, cuticle-like sheets, tubes, trilete or not), and how the authors classify them (charophyte, embryophyte, transitional/"cryptospore");
- the authors' explicit criteria for what counts as an embryophyte spore, and where in the sequence they place the first such spores;
- any statement about how many samples or sections were examined, sample yields, or samples barren of spores; any statement about the general state of Cambrian–Early Ordovician palynological sampling;
- the Tremadocian Australian assemblage (observation S-tremadocian-australia-polyads): exact locality, unit, age basis.
- In `comment`, give the ICS v2024/12 stage(s) each age implies (Cambrian stages in `data/timescale.csv` are Fortunian, Stage 2, Stage 3, Stage 4, Wuliuan, Drumian, Guzhangian, Paibian, Jiangshanian, Stage 10).

If the texts justify splitting the grouped observation S-cambrian-irregular-polyads into named assemblages, recommend `new_observation` for each, with locality, unit, stage range and the authors' classification in `detail`.

Expect 25–60 findings.
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
