# Trait-pilot evidence

Evidence tables for the trait pilot (`docs/pilot-traits.md`).

## `hooper2026-asr/`

Codex's extraction of Hooper et al.'s (2026) deposited crown-node states, with its own README.

## `specimens.csv`

Specimen-level observations of the four pilot characters (C1 trilete production, C2 cryptospore
production, C3 branched sporophyte with several sporangia, C4 demonstrable tracheids) from 17
held primary sources. Each row is one source, taxon or specimen, and character, with:
- state: present, absent, unknown or disputed;
- evidence level: direct, composite or transfer (`docs/pilot-traits.md`);
- the source's locality, horizon and age as stated, and the page;
- the source's own caveats;
- an adjudication note where Claude checked the row.

**How it was made (2026-10-30).**
- Three `gpt-6.1-sol` jobs extracted 281 rows, each with a verbatim quote of 8–40 words, from
  `pdftotext` text. Edwards 1979, a scan, was read through `ocrmypdf`.
- Every quote was found in its source text by script: 274 exactly, 7 after normalising
  punctuation and layout.
- Claude added two rows from Edwards and Davies (1976) and adjudicated the rows the pilot turns
  on.
- The quotes are copyrighted text, so they stay in the git-ignored
  `library/closed/pilot_specimen_quotes.json`. The table carries a 16-character SHA-256 prefix of
  each quote (`quote_sha256`) so a holder of the sources can check them.

**Limits.**
- Rows with evidence level `transfer` restate other works as the source cites them. They are
  leads, not observations.
- Ages are as stated, often in older stage names (Gedinnian, Siegenian, Whitcliffian). They are
  mapped to ICS stages only where the pilot uses them.
- Rows not adjudicated are Codex's reading of the text; check them before use.
