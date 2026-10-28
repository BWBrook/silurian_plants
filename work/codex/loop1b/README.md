# Loop 1b: pivotal records against the closed literature

2026-10-28. Barry obtained eight of the nine papers on the closed list, plus three partial sources on Yea (`library/closed.tsv`). Three Codex `gpt-6.1-sol` jobs (high effort, no web search) read them against the occurrence records they bear on. Claude Opus 5.5 wrote the prompts and adjudicated the findings into `data/occurrences/`.

| Job | Sources | Records | Findings | Quotes verified |
|---|---|---|---|---|
| `misc` | Edwards & Davies 1976; Edwards et al. 2007; Salamon et al. 2018 and supplement; Morel et al. 1995; Strother et al. 2015 | Capel Horeb, *Pinnatiramosus*, Zbrza, Bolivia, Hanadir | 89 | 89 |
| `yea` | Rickards 2000; Garratt & Rickards 1987; Garratt 1983; the 1978 map reproduced by Jelinek 2008; Earp's 2023 draft | Ghin Ghin, Limestone Road, unspecified Yea, Wilson Creek | 83 | 83 |
| `cambrian` | Strother & Foster 2021 and supplement | Cambrian polyads, Tremadocian Canning Basin | 60 | 60 |

- **Files here:** the prompts (`prompt_*.md`, with `common.md` appended to make `full_*.md`), the schema, the record subsets each job saw (`*_observations.csv`, `*_interpretations.csv`) and `verify.py`.
- **Outputs are not here.** They quote copyrighted texts at length, so they sit with the texts in the git-ignored `library/closed/extract/` on mac-mini (`<job>.json`, and `<job>.verified.json` with `verified_in_text` per finding). Rebuild the paged texts with `pdftotext` and the `=== PDF page N ===` markers used by `verify.py`.
- **Verification:** `python3 work/codex/loop1b/verify.py library/closed/extract/<job>.json` checks every quotation against its paged text, ignoring whitespace, line-break hyphens, curly quotes and ligatures. All 232 passed.
- **What changed** is recorded in `docs/decisions.md` (2026-10-28) and `docs/rejected-records.md` (entries 16 and 17). Short supporting quotations, with page numbers, are in the `support` fields of `data/occurrences/interpretations.csv`.
