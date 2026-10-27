# Post-2006 spore extraction (MVD-B): pilot and verification

2026-10-27, Claude Opus 5.5 orchestrating; Codex did the extraction.

## Pilot: Terra vs Sol, 5 papers

The task was full-paper extraction of assemblages and taxa to `data/spores/work/codex/mvdb/schema.json`.

| Paper | Terra: assemblages / taxa | Sol: assemblages / taxa | Genus overlap (Jaccard) |
|---|---|---|---|
| W1790452228 | 20 / 159 | 25 / 199 | 0.78 (Sol found 4 more genera) |
| W1963719278 | 10 / 33 | 12 / 35 | 1.00 |
| W2043417999 | 8 / 34 | 10 / 32 | 1.00 |
| W2068754956 | 1 / 41 | 41 / 305 | 0.95 |
| W2112523440 | 2 / 46 | 15 / 155 | 1.00 |

Sol resolves samples; Terra collapses them into formation composites. Sol was chosen; it takes
3–9 min per paper against Terra's 1–2.

Sol expanded abbreviated genera inside `taxon_as_reported` ("Ambitisporites parvus" where the paper
prints "A. parvus"). The prompt was tightened to require a verbatim copy, with the expansion going
in `genus`.

## Full run: 37 papers, Sol

376 assemblages and 2,594 taxa; 82.5% were verbatim on the first check.

**Abstracts held as full texts.** Six held "texts" were under 1,500 words.
- Three were complete conference abstracts. Sol returned one or two pooled records for each and
  said that no taxa were named.
- The other three (308, 359 and 705 words) were the abstracts or the first proof page of full
  papers. Sol ran with web search and found the full articles: two open-access *Acta
  Palaeontologica Polonica* PDFs, one with its supplement, and an author's transcription on
  ResearchGate. It extracted 79, 204 and 53 taxa from them and named those sources in its
  `comment` field.
- Those records failed the text check because they were checked against the abstracts.

All six papers are dropped until the records can be checked against the documents Sol used. The
harvester now flags short texts (`data/external/library/README.md`, full-text test).

*Correction, 2026-10-27.* The first version of this audit called those 336 records invented and
said Sol ran without web search. Both claims were wrong. The job logs show 20 to 40 web searches
per paper, and Sol's comments name its sources. Claude Opus 5.5 read the failed check without
reading the comments. Barry's question prompted the recheck.

**Record-level verification.** In real full texts, the misses came from formatting: genera
abbreviated in tables, column layouts, dash variants. A record is now `verified_in_text` if its
name, or its genus plus epithet, appears in the paper's text, and unverified records are not
usable. After dropping the six papers, 2,191 of 2,253 records (97%) verify.

## Lessons

- **Check that the input is the real thing.** The harvest held abstracts as full texts.
- **Know which source the job used.** With web search, Sol replaced a thin input with the full
  article it found online. State the permitted sources in the prompt, ask for the source of each
  record, and read the job's comments before diagnosing a failure.
- **Verify every record against its source text by script.** It costs nothing, and it flags
  every record whose source is not held.
- **Choose models per task by pilot.** Sol was better for extraction that needs judgement about
  samples and ages; Terra was adequate for flat digitisation.
