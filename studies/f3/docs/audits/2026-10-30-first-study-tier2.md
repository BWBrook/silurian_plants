# First-study Tier 2 literature acquisition, 30 October 2026

Barry authorised the Tier 2 pass and asked that locked-mini or login cases be held for
his office session. All 77 rows were attempted through public repositories, publishers,
existing project holdings and authorised UTAS browser routes. The input priorities in
`docs/first-study-literature.csv` are unchanged. This is acquisition and source QA;
scientific reading, occurrence adjudication and frame admission remain separate.

| Outcome | Rows |
|---|---:|
| Newly secured main texts | 30 |
| Exact works already held, now reconciled | 12 |
| Complete abstracts (source-kind corrections) | 2 |
| Data archive (already held elsewhere) | 1 |
| First page only | 1 |
| Supplement held, main missing | 1 |
| Blocked/unheld | 30 |
| Total | 77 |

Thus 42 rows have a main text, and 32 remain incomplete or unheld. The 30 new main
texts comprise 29 original PDF files and one explicitly derived BHL page-image
reconstruction. Twelve other works were already held; their newly filed reading copies
are not new discoveries. `library/closed.tsv` adds 92 asset entries, with hashes, byte
counts, source URLs and versions. They include reading copies, nine supplements,
34 selected data files, original archives, abstracts, XML and the first-page partial;
92 is a file count, not a count of papers. Thirty-three supporting/data assets are
byte-identical to existing holdings (11 Clark, 21 Harris and the White archive); the
remaining eleven examined supporting/data files were not matched by that audit.

The durable receipt is `work/codex/literature/2026-10-30-first-study-tier2.json`.
It retains per-file QA, original route observations, metadata checks, supporting-file
omissions, an independent review and prior-holdings reconciliation. The focused status
register now covers all 135 input rows; its 58 Tier 1 rows are unchanged. The master
register retains 565 IDs; only the 77 Tier 2 rows changed. Copyrighted files and QA
renders stay ignored, under `library/closed/`.

## Source identity and version qualifications

- `libertin2022-open` is the same work as `libertin2022`: online 2022, printed 2023.
  The status row uses the previously held publisher PDF `libertin2023_bohemica.pdf`;
  the new DiVA manuscript/copy has its own additional-copy provenance entry.
- `steemans2009` is Philippe Steemans's IPC 2008 conference abstract, not two authors
  named Philippe and Steemans and not the separate 2009 Science Brevia. The two-page
  file and the GSA web abstract `strother2017` are marked `abstract-only`, including in
  the master register. No missing longer article was inferred.
- `mcsweeney2024` is the January 2022 RMIT doctoral thesis, deposited in the current
  repository in 2024. The migrated Figshare record preserves the old Esploro identifier;
  archival DOI 10.25439/rmt.27597750 is a repository identifier. All 280 PDF pages extract;
  20 representative pages, including photographic plates and appendices, rendered legibly.
  The original contains recoverable qpdf stream/hint warnings; it was not repaired.
- `mawson1994` is a 40-page reconstruction from BHL image IDs 59608302–59608341
  (printed pp.31–70), not an original bundled publisher PDF.
- `quintvalle2006` (Canning Part One) is only a one-page title/abstract extract, despite
  ResearchGate's full-text label. The 88-page text, twelve plates and appendices remain
  missing. `quintavalle2006` (Part Two) is a separate request-only target.
- The ORCA `edwards2015_tier2.pdf` file cover identifies an accepted manuscript despite
  repository metadata saying Published Version. The already-held 12-page PMC publisher
  PDF is now mirrored as `edwards2015_tier2_published.pdf`, the canonical reading copy.
  Full-text XML and an auxiliary inline-image ZIP are retained separately. The latter
  is provenance-qualified against Europe PMC/PMC, recorded in the receipt and excluded
  from the 92 registered source assets and from supplementary-dataset counts.
- `kozowski1959` is Kozłowski & Greguss (1959), nine printed text pages plus four plates.
  Original source IDs are retained when citation spelling/year/kind is corrected.
- `edwards2003` has null padding/xref reconstruction warnings; all fifteen pages extract
  and rendered completely. Parry's NORA copy is an accepted manuscript. Baldwin's public
  CiteSeerX PDF bears a historical Lyell Collection imprint; that is not evidence of a
  live redirect. Lang 1937, Cookson 1935 and both Kidston parts include their plates.
- White 2008 is the NRCan data/software archive, not a journal PDF. Selected Clark,
  Harris and Puttick deposit files are indexed individually. Harris's larger chains,
  reconciliations and alternate-calibration archives and Su's linked alignment/tree
  deposit remain outside this acquisition; no complete-deposit claim is made.

## Verification and access findings

All 92 asset sizes/SHA-256 values were computed from actual files, independently checked
against the draft manifest, and confirmed ignored/untracked. DOI checking used the
repository's `tools/cards.py` against the 34 distinct acquired DOI references: zero
flags. PDF checks combined pdfinfo, qpdf, title/extent extraction and representative
rendering, with sparse/plate pages checked where applicable. Original source warnings
are retained in per-file receipts. Archives and spreadsheets were inspected without
executing embedded content. No card/model code or scientific datasets were edited.

The independent review caught an ambiguous master status for the two abstract-only
items and insufficient route notes for two files; integration repaired them. It also
confirmed the main counts, all hashes, manifest linkage and unchanged input priorities.
The support-duplicate audit prevented existing datasets from inflating new acquisition
counts. Minor malformed hash strings in temporary receipts were transcription errors;
the receipts were corrected to the independently computed file hashes.

The mini remained locked. Springer downloads, Cardiff links and Chrome's Wiley reader
could nevertheless save several originals. ScienceDirect full text opened for four
remaining targets but native save was unavailable and automated delivery stalled.
Edwards–Richardson 2004's Chrome reader loaded all 28 pages but its download timed out.
These five are the fastest office follow-up. Hoffmeister 1959 needs Barry's explicit
JSTOR acceptance. Three targets hit browser security checks; three others still need
entitlement established. Ten have explicit institutional subscription gaps and ten
need library/archive/full-source searches. Bulls Head's older browser-block diagnosis
is superseded by an explicit JSTOR no-access result. All acquisition tabs were closed;
user-owned UTAS/staff tabs were left untouched. No challenge was bypassed, explicit
terms accepted, request sent or purchase made.

The 32 exact actions and reopen links are in `docs/barry-to-action.md`. Twenty
library/archive candidates are separated in `docs/literature-requests.md`, so ordinary
save/login work is not conflated with interlibrary requests. Downloads cleanup moved
only hash-matching, successfully filed copies to a recoverable timestamped Bin folder;
its receipt records each retained library path and hash.

## Main-text reading index

`main-held` means newly secured in this tranche; `already-held` means reconciled with
an exact prior holding. Both point to a readable local copy. Full citations, source URLs,
versions and qualifications are in the status register and manifest.

| Source ID | Outcome | Reading file | PDF pages |
|---|---|---|---:|
| `ghavidelsyooki2008` | main-held | [ghavidelsyooki2008_tier2.pdf](../../library/closed/ghavidelsyooki2008_tier2.pdf) | 33 |
| `leherisse2013` | already-held | [leherisse2013_tier2.pdf](../../library/closed/leherisse2013_tier2.pdf) | 22 |
| `baldwin2004` | main-held | [baldwin2004_tier2.pdf](../../library/closed/baldwin2004_tier2.pdf) | 24 |
| `yin2013` | main-held | [yin2013_tier2.pdf](../../library/closed/yin2013_tier2.pdf) | 7 |
| `clark2023` | already-held | [clark2023_tier2.pdf](../../library/closed/clark2023_tier2.pdf) | 20 |
| `harris2022` | already-held | [harris2022_tier2.pdf](../../library/closed/harris2022_tier2.pdf) | 20 |
| `hedges2018` | main-held | [hedges2018_tier2.pdf](../../library/closed/hedges2018_tier2.pdf) | 2 |
| `kenrick1997nature` | main-held | [kenrick1997nature_tier2.pdf](../../library/closed/kenrick1997nature_tier2.pdf) | 7 |
| `puttick2018` | main-held | [puttick2018_tier2.pdf](../../library/closed/puttick2018_tier2.pdf) | 17 |
| `strother2023` | already-held | [strother2023_tier2.pdf](../../library/closed/strother2023_tier2.pdf) | 4 |
| `su2021` | already-held | [su2021_tier2.pdf](../../library/closed/su2021_tier2.pdf) | 34 |
| `wellman2014a` | main-held | [wellman2014a_tier2.pdf](../../library/closed/wellman2014a_tier2.pdf) | 3 |
| `al2013d` | main-held | [al2013d_tier2.pdf](../../library/closed/al2013d_tier2.pdf) | 3 |
| `al2013f` | main-held | [al2013f_tier2.pdf](../../library/closed/al2013f_tier2.pdf) | 9 |
| `kielan1959` | main-held | [kielan1959_tier2.pdf](../../library/closed/kielan1959_tier2.pdf) | 283 |
| `mawson1994` | main-held | [mawson1994_tier2.pdf](../../library/closed/mawson1994_tier2.pdf) | 40 |
| `mcgregor1986` | main-held | [mcgregor1986_tier2.pdf](../../library/closed/mcgregor1986_tier2.pdf) | 84 |
| `temple1965` | main-held | [temple1965_tier2.pdf](../../library/closed/temple1965_tier2.pdf) | 93 |
| `psenicka2021` | already-held | [psenicka2021_tier2.pdf](../../library/closed/psenicka2021_tier2.pdf) | 22 |
| `strauss1989` | main-held | [strauss1989_tier2.pdf](../../library/closed/strauss1989_tier2.pdf) | 17 |
| `edwards2003` | main-held | [edwards2003_tier2.pdf](../../library/closed/edwards2003_tier2.pdf) | 15 |
| `edwards2003a` | main-held | [edwards2003a_tier2.pdf](../../library/closed/edwards2003a_tier2.pdf) | 16 |
| `edwards2015` | already-held | [edwards2015_tier2_published.pdf](../../library/closed/edwards2015_tier2_published.pdf) | 12 |
| `hetherington2017` | already-held | [hetherington2017_tier2.pdf](../../library/closed/hetherington2017_tier2.pdf) | 9 |
| `kerp2001` | main-held | [kerp2001_tier2.pdf](../../library/closed/kerp2001_tier2.pdf) | 32 |
| `kidston1917-open` | main-held | [kidston1917-open_tier2.pdf](../../library/closed/kidston1917-open_tier2.pdf) | 34 |
| `kidston1920-open` | main-held | [kidston1920-open_tier2.pdf](../../library/closed/kidston1920-open_tier2.pdf) | 36 |
| `lang1937` | main-held | [lang1937_tier2.pdf](../../library/closed/lang1937_tier2.pdf) | 64 |
| `libertin2022-open` | already-held | [libertin2023_bohemica.pdf](../../library/closed/libertin2023_bohemica.pdf) | 12 |
| `cookson1935` | main-held | [cookson1935_tier2.pdf](../../library/closed/cookson1935_tier2.pdf) | 29 |
| `geng1986` | main-held | [geng1986_tier2.pdf](../../library/closed/geng1986_tier2.pdf) | 15 |
| `kozowski1959` | main-held | [kozowski1959_tier2.pdf](../../library/closed/kozowski1959_tier2.pdf) | 13 |
| `libertin2018a` | already-held | [libertin2018a_tier2.pdf](../../library/closed/libertin2018a_tier2.pdf) | 7 |
| `mcsweeney2021` | already-held | [mcsweeney2021_tier2.pdf](../../library/closed/mcsweeney2021_tier2.pdf) | 13 |
| `mcsweeney2022` | already-held | [mcsweeney2022_tier2.pdf](../../library/closed/mcsweeney2022_tier2.pdf) | 17 |
| `mcsweeney2024` | main-held | [mcsweeney2024_tier2.pdf](../../library/closed/mcsweeney2024_tier2.pdf) | 280 |
| `pacyna2022` | main-held | [pacyna2022_tier2.pdf](../../library/closed/pacyna2022_tier2.pdf) | 20 |
| `porebski2019` | main-held | [porebski2019_tier2.pdf](../../library/closed/porebski2019_tier2.pdf) | 5 |
| `retallack2019` | main-held | [retallack2019_tier2.pdf](../../library/closed/retallack2019_tier2.pdf) | 33 |
| `tims1984` | main-held | [tims1984_tier2.pdf](../../library/closed/tims1984_tier2.pdf) | 15 |
| `trela2019` | main-held | [trela2019_tier2.pdf](../../library/closed/trela2019_tier2.pdf) | 4 |
| `yang2004` | main-held | [yang2004_tier2.pdf](../../library/closed/yang2004_tier2.pdf) | 6 |
