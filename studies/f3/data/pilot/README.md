# Trait-pilot evidence

Evidence tables for the trait pilot (`docs/pilot-traits.md`).

## `hooper2026-asr/`

Codex's extraction of Hooper et al.'s (2026) deposited crown-node states, with its own README.

## `combinations.csv`

Each trait combination the pilot uses, as one row:
- the taxon and specimens;
- its evidence level: direct only when every member is on one specimen, otherwise composite;
- its member rows in `specimens.csv` (`source:characters`);
- age as stated and ICS stage;
- its qualifications.

It exists so that direct single-character rows are never read as a direct joint observation
(Codex's recommendation, 2026-10-30).

## `specimens.csv`

Specimen-level observations of the four pilot characters (C1 trilete production, C2 cryptospore
production, C3 branched sporophyte with several sporangia, C4 demonstrable tracheids) from 30
held primary sources (524 rows). Each row is one source, taxon or specimen, and character, with:
- state: present, absent, unknown or disputed;
- evidence level: direct, composite or transfer (`docs/pilot-traits.md`);
- the source's locality, horizon and age as stated, and the page;
- the source's own caveats;
- an adjudication note where Claude checked the row.

**How it was made (2026-10-30).**
- Six `gpt-6.1-sol` jobs, in two rounds, extracted 518 rows from `pdftotext` text, each with a
  verbatim quote of 8–40 words. Edwards 1979, Kenrick and Crane 1991 and Kerp et al. 2001 are
  scans and were read through `ocrmypdf`.
- Every quote was found in its source text by script: 505 exactly, 13 after normalising
  punctuation and layout.
- Claude added six rows from his own readings: Edwards and Davies 1976, and the Irish Homerian
  material in Edwards and Feehan 1980 and Edwards et al. 1983.
- Claude adjudicated the rows the pilot turns on.
- Codex reviewed the first round (`docs/audits/2026-10-30-frame-and-pilot-review.md`); its
  corrections are applied. The *Velatitetras* producer's C2 is now `disputed`, and the two Edwards
  and Davies rows have archived quotes.
- The quotes are copyrighted text, so they stay in the git-ignored
  `library/closed/pilot_specimen_quotes.json`. The table carries a 16-character SHA-256 prefix of
  each quote (`quote_sha256`) so a holder of the sources can check them.

**Limits.**
- Rows with evidence level `transfer` restate other works as the source cites them. They are
  leads, not observations.
- Ages are as stated, often in older stage names (Gedinnian, Siegenian, Whitcliffian). They are
  mapped to ICS stages only where the pilot uses them.
- Rows not adjudicated are Codex's reading of the text; check them before use.
- A `present` row can be conditional. The Irish TCD 22946d C3 row counts only if the terminal
  expansions are sporangia, and its combination is labelled `C3 (conditional)`. *Horneophyton*'s
  C3 is a taxon-level transfer (Kerp 2017), so its combination is composite with transferred C3
  (Codex, Correspondence 2629).
