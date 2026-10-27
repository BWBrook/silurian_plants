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

**Invention on non-texts.** Three "held" texts were abstracts or landing pages of 308, 359 and
705 words. For them, Sol, running without web search, produced 79, 204 and 53 taxa that were
almost entirely absent from the text: invented records. All six held texts under 1,500 words are
now dropped, and the harvester's identity check (title match) is being extended.

**Record-level verification.** In real full texts, the misses came from formatting: genera
abbreviated in tables, column layouts, dash variants. A record is now `verified_in_text` if its
name, or its genus plus epithet, appears in the paper's text, and unverified records are not
usable. After dropping the six papers, 2,191 of 2,253 records (97%) verify.

## Lessons

- **Check that the input is the real thing.** A Codex job given a thin input may fill it from
  memory, and the output looks fine.
- **Verify every record against its source text by script.** Here this catches invention and
  costs nothing.
- **Choose models per task by pilot.** Sol was better for extraction that needs judgement about
  samples and ages; Terra was adequate for flat digitisation.
