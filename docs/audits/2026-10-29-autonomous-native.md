# Autonomous literature expansion: native-save follow-up, 29 October 2026

After Barry returned and unlocked the desktop, Codex recovered **all ten Oxford candidates plus Edwards 1980 and Mark 2011**. Mark's five original supporting files (two JPEG tables and three isotope-data TXT files) are also held. This follow-up adds 12 main texts and five supporting files, bringing the autonomous total to **97 main texts, 46 supporting files and one erratum** (144 assets). The 492-row CSV now has 348 needed, 111 local-copy-held and 33 open-copy-held rows.

Files are in git-ignored `library/closed/`. The manifest is `library/closed.tsv`; the self-contained receipt is `work/codex/literature/2026-10-29-autonomous-native.json`. This follow-up supersedes the native-save pending status in the second-checkpoint audit and ledger. No source interpretation, occurrence record, model or card was changed.

## Verification and workflow diagnosis

All 12 main files have matching primary titles, authors, DOI identities and printed page extents. Parent checks recalculated bytes/SHA-256, qpdf status and per-page text counts; a bounded gpt-5.6-luna delegate inspected rendered article/end pages and identity. Figure-heavy pages are explicitly distinguished from sparse extraction caused by image-only scans. The DOI for Edwards's cuticle paper contains 1982, while the correct issue year is 1986. Publication identity follows the primary text and metadata, not the DOI year string.

Chrome's native Save works once the PDF is fully loaded and the Download control has hydrated. A first click can have no effect; inspecting fresh state before a second click resolved these cases. Save panels were checked for the current PDF identity and archive destination. One stale filename was caught by the OS replacement warning and cancelled before overwriting; the existing Fanning file's checksum remained unchanged. Subsequent explicit record state and save-name checks prevented recurrence. Direct saves created no Downloads duplicates for the twelve main files. Temporary CDN tokens were omitted from provenance; stable article/DOI routes and delivered file hashes are retained.

Mark's Appendix A exposes EA1/EA2 as JPEG tables and EA3–EA5 as raw isotope-data text files. EA1 was delivered through the browser; the remaining public CDN downloads succeeded without proxy cookies or credentials after browser download-event timeouts. JPEGs decoded and were visually inspected; TXT files were checked as non-HTML tabular data, without scientific transcription or execution. All five remain separate assets. The supporting-file receipt records exact publisher/proxy URLs and HTTP results.

## Remaining blockers and structure

Pertica's alternative JSTOR route works in Chrome and confirms UTAS access, but Download presents an explicit Terms and Conditions dialog with **Accept and download**. Codex cancelled it and closed the tab, leaving this precise Barry action in the ledger. The Breuer ResearchGate security check and Bulls Head JSTOR verification cases remain. The original ten parked requests were not retried; later archive-gap candidates remain qualified route results, with public alternatives still possible. No terms acceptance, request, purchase, outside message or access-control bypass occurred.

The existing CSV, asset manifest and separate action/request ledgers remain sufficient. This tranche resolved the desktop-save assumption without altering scientific questions. The highest-value remaining work is the three action-ledger routes, then targeted public-copy searches for old backfiles. No background monitoring or dispatch was created.

## Main-text index

| CSV ID | File under `library/closed/` | PDF pages |
|---|---|---:|
| al1983 | al1983_oup.pdf | 18 |
| edwards1986 | edwards1986_oup.pdf | 17 |
| liedwards1995 | liedwards1995_oup.pdf | 30 |
| fanning1992 | fanning1992_oup.pdf | 28 |
| shute1989 | shute1989_oup.pdf | 27 |
| edwards2004 | edwards2004_oup.pdf | 15 |
| edwards1988 | edwards1988_oup.pdf | 15 |
| al2012b | al2012b_oup.pdf | 29 |
| niklas1985 | niklas1985_oup.pdf | 13 |
| al2012e | al2012e_oup.pdf | 27 |
| edwards1980 | edwards1980_elsevier.pdf | 12 |
| mark2011 | mark2011_elsevier.pdf | 15 |

## Final feasibility and register checks

The remaining CSV was reconciled after acquisition: 43 priority-one rows remain needed. Sixteen are already in the parked/action/archive-gap categories; 27 remain eligible for further work, representing 14 unique nonblank DOIs plus metadata-only entries. Five focused public searches did not verify another full-article download. Two Estonian Academy targets are complete one-page conference abstracts, not truncated full research articles. Their target/source-kind mapping needs reconciliation; they were not counted as newly recovered main texts. Other unsearched leads remain opportunities, not declarations of unavailability. The corrected inventory is `work/codex/literature/2026-10-29-autonomous-remaining-priority1.json`; an initially misassigned Anticosti route was corrected to Richardson & Ausich 2007 before preservation.

The required repository DOI check examined 731 distinct strings and flagged 28: 20 known closing-backtick capture errors and 8 newly added ledger entries lacking full citation context. The 8 new contexts were corrected; the same checker then verified all 8 with zero flags. Existing scanner-formatting issues were left outside this acquisition scope. Diagnostics and the scoped-check method are preserved in `work/codex/literature/2026-10-29-autonomous-final-checks.json`. The final asset reconciliation verified 144 unique archive paths against recorded bytes/SHA-256 and Git ignore status, with 492 unique CSV row IDs. Across the three checkpoints, 100 verified Downloads staging duplicates were moved to recoverable Bin folders, never purged.
