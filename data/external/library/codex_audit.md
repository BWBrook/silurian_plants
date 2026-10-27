# Codex runs for the literature library (phase 2), 2026-10-27

Run by Claude Sonnet 5.5 (`claude-sonnet-5-5`) at the project's request, following Barry's practice of routing legwork to Codex
(`docs/audits/2026-10-27-codex-pilot.md` is the earlier pilot). Codex did first-pass checks that a script can verify; I designed the
jobs, checked coverage by script, spot-checked the output and adjudicated every disagreement. Agreement between models is not independent
validation, and where Codex and the screen disagreed the adjudication below is mine.

## How the jobs ran

- **Inputs** sit in `data/external/local/library/codex/<job>/` (git-ignored): `chunk_NN.json` (the items), `prompt_NN.txt`, `schema.json`,
  `manifest.json` (expected ids per chunk), `out_NN.json` (Codex's reply), `results.json` (merged) and `run_NN.log`. Scripts: `scripts/library_codex.py`
  (prepare, run, check, rerun), `library_codex_export.py` and `library_text_export.py` (server side exports).
- **Isolation.** Codex ran read-only in the job folder, with no keys, no git, no network search and no access to the store. Items were chunked to
  about 100, each prompt stated the exact item count, and each output schema fixed the id and verdict vocabulary (`additionalProperties: false`).
- **Coverage check.** After every job `library_codex.py check` compared the returned ids with the chunk's expected ids (none missing, none duplicated, none unexpected,
  every value in the vocabulary), and a rerun path for gaps exists (`rerun`); it was not needed.
- **Two ways of running.** The `cited` and `screen` jobs ran earlier with raw `codex exec -m MODEL -c model_reasoning_effort=high -s read-only -C JOBDIR
  --skip-git-repo-check --ephemeral --output-schema SCHEMA -o OUT PROMPT < /dev/null`. My first launch of both exited at once with status 1 because
  `--output-schema` resolves a relative path against the launching directory, not `-C`; I relaunched with absolute paths and the jobs completed. The `quarantine` and
  `identity` jobs ran after the coordinator's method update, through the shared wrapper
  `~/.claude/bin/codex-delegate -m terra -e high -f PROMPT --schema SCHEMA --expect N --count '.results | length' -o OUT -C JOBDIR --label silurian-library-<job>-<chunk>`.
  Raw runs are not in the wrapper's cost log; their token totals come from the `tokens used` line each run prints.

## Jobs

| Job | Question | Model | Run via | Chunks (items) | Returned | Time | Codex tokens |
| --- | --- | --- | --- | --- | ---: | --- | --- |
| `cited` | Is the OpenAlex record for each cited DOI the work the project's citation line names? | gpt-6.1-terra | raw `codex exec` | 6 (104, 104, 104, 104, 104, 103) | 623 of 623 | 44-47 s, parallel | 333,925 |
| `screen` | Independent re-screen of `priority_spores` and a random excluded sample, from title and abstract | gpt-6.1-sol | raw `codex exec` | 4 (96, 96, 96, 95) | 383 of 383 | 132-192 s, parallel | 310,569 |
| `quarantine` | Are the quarantined PDFs the expected work? | gpt-6.1-terra | `codex-delegate` | 1 (6) | 6 of 6 | 18 s | 82,524 input (36,480 cached), 451 output |
| `identity` | Do the first two pages of each accepted text match the expected metadata? | gpt-6.1-terra | `codex-delegate` | 2 (107, 106) | 213 of 213 | 47 s and 56 s, parallel | 732,231 input (590,848 cached), 8,047 output |

Cost-log lines for the wrapper jobs (`~/.local/state/codex-delegate/jobs.jsonl`):

```
{"label":"silurian-library-quarantine-01","model":"gpt-6.1-terra","seconds":18,"status":0,"problem":"","tokens":{"input":82524,"cached":36480,"output":451,"reasoning":89}}
{"label":"silurian-library-identity-02","model":"gpt-6.1-terra","seconds":47,"status":0,"problem":"","tokens":{"input":289925,"cached":239872,"output":3831,"reasoning":90}}
{"label":"silurian-library-identity-01","model":"gpt-6.1-terra","seconds":56,"status":0,"problem":"","tokens":{"input":442306,"cached":350976,"output":4216,"reasoning":264}}
```

## `cited`: intended-work check

- **Input.** For each of the 623 cited works, the project's own citation lines (from `taxa/*.md` cards, where the `doi:` line carries its `cite:` line before it, and from `docs/*.md`) and OpenAlex's title, first-author surnames, year, venue and type.
- **Result.** 623 `same_work`, none `different_work`, none `unclear` (`library/cited_identity_check.tsv`).
- **Checked.** Uniform acceptance needs a check. A script found that the OpenAlex title shares at least 60% of its words with a project line for 622 works (the 623rd, a Spanish title, 57%), and no project year differs from OpenAlex's by more than one. Codex's notes flag the one-year differences and OpenAlex oddities (a missing author, a section numeral) without changing the verdict.
- **Outcome.** No cited DOI resolves to a different work. No change to the seeds or the resolution table.

## `screen`: independent re-screen

- **Input.** 383 works shuffled together: all 183 `priority_spores` works of phase 1 and 200 drawn at random (seed 20261027) from the 606 excluded candidates. Codex saw year, type, the candidate rule that found each work, title and abstract (cut to 1,800 characters), and the rule text from `screen.tsv`; it did not see my decisions, reasons or regions. The key to which items were which stayed outside the job folder's chunk files (`screen/key.json`).
- **Output.** `include`, `include_borderline` or `exclude`, a reason class, a region and a short reason.
- **Agreement.** Same include-or-exclude call: 176 of 183 `priority_spores` (96.2%), 183 of 200 excluded (91.5%), 359 of 383 overall (93.7%). Same three-way grade: 281 of 383 (73.4%); Codex graded 73 of my `include` as borderline and five the reverse, because the abstract alone cannot confirm an assemblage's age. Region agreed for 175 of 176.
- **Disagreements.** 24 include-or-exclude and 78 grade-only differences, all in `library/screen_codex_check.tsv` with Codex's reason class and reason and my adjudication.
- **Adjudication.** Codex was right on three `priority_spores` works (W2075902280: spores only from the Middle Devonian assemblage; W4298208550: a synthesis; W7135205057: Eifelian-Givetian), which I removed. I re-graded three to borderline (W1479948401, W1762144596, W3171257164). Of the 17 excluded works Codex would include, I added two (W2776142699 Rhynie chert dispersed spores, W2033254699 Chigua Formation) and kept 15 excluded (palynofacies, stratigraphy, Late Devonian or macrofossil papers whose spore content is incidental).
- **Change logged.** `priority_spores` 183 to 182 works (154 `include`, 28 `include_borderline`); `library_screen_decisions.tsv` and `scripts/library_screen_codex_adjudication.tsv` hold the decisions.
- **Limit.** Both screens read the same title-and-abstract text; neither read the papers. The sample covers the 606 candidates the rules found, not works the rules missed.

## `quarantine`: six files, five works

Codex saw the expected metadata and the first three pages of each quarantined PDF. Five `same_work` (W1820528062, W2140021911 and both W2314927738 files are supplementary material of the expected work; W2312953052 is the main text of the expected Treatise chapter) and one `unreadable` (W4401715016, extracted text is download footers only).
`library.py` has no release command, so none was released. The excerpt text sent to Codex came from `quarantine/` through the Mac, because the Codex CLI is installed only on the Mac; I removed the excerpt text from the Mac after the review (the PDFs were never copied), keeping the ids, verdicts and a hash of each excerpt.

## `identity`: accepted texts

- **Input.** 213 held copies: the first two pages as extracted text, or for nine scans without a text layer the OCR of those pages (`pdftoppm` and `tesseract`, used only for this check).
- **Result.** 204 `match`, 7 `mismatch`, 2 `unclear`. The seven mismatches were withdrawn with `library.py withdraw`; the reasons are in `manifest.tsv`: three supplementary-material PDFs, a conference abstract volume, a different conference abstract, a whole journal issue's front matter and a newsletter issue. The two `unclear` were kept (a preprint under a different title; an OCR notice with no bibliographic text).
- **Note.** The library's own title check had already accepted all seven (60% of title words in the first three pages). Four of the seven are documents that contain or accompany the expected work (a supplement, a volume, a newsletter), so withdrawal means the work is not held, not that the document is wrong.

## `open_unread`

The `open_unread` fetch used no Codex job of its own: its 15 fetched files were part of the 213 in the `identity` job, and all 15 matched (`library/open_unread_results.tsv`).

## What this does not show

- Codex read only the text in each chunk. A `same_work` verdict from the first two pages does not show that the whole PDF is intact.
- The screen check measures agreement with one other reader on titles and abstracts, not the truth about each paper.
- Cost is Codex tokens only; no Anthropic token figures are recorded for the orchestrating session.
