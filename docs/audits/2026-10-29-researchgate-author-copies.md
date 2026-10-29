# ResearchGate author-copy batch, 29 October 2026

Barry authorised the two Stage B candidates in `docs/literature-next-batch.md`,
using the in-app browser first and Chrome as fallback. Both complete main texts
were recovered autonomously. No sign-in, account creation, author request or
challenge solving was needed. All successful and blocked work tabs were closed.

| Register ID | Verified main text | Private archive | Route |
|---|---|---|---|
| `w2080475227-fulltext` | Mehlqvist, Vajda & Steemans 2012, *Early land plant spore assemblages from the Late Silurian of Skåne, Sweden*, GFF 134(2), 133–144; DOI 10.1080/11035897.2012.683451; 12 pages | `library/closed/mehlqvist2012.pdf` | Public upload by Vivi Vajda on ResearchGate; Chrome fallback |
| `wellman2013-open` | Wellman, Steemans & Vecoli 2013, chapter 29, *Palaeophytogeography of Ordovician–Silurian land plants*, Geological Society, London, Memoirs 38, 461–476; DOI 10.1144/M38.29; 16 pages | `library/closed/wellman2013.pdf` | Public upload by Marco Vecoli on ResearchGate; Codex in-app browser |

Both are author-uploaded reproductions in published layout, rather than files
labelled accepted manuscripts. No open reuse licence was established for either
main text. Public availability does not transfer the separately registered
supplement's licence to the chapter. Copyright PDFs remain git-ignored.

## Access and version findings

- The first Mehlqvist in-app attempt ended at ResearchGate's temporary-access
  restriction/device-check page. That tab was closed. The ordinary Chrome route
  opened the public record without sign-in. Clicking Download reached a progress
  page but initially produced no saved file; downloading its displayed PDF link
  through the browser's file-download control saved `Mehlqvist_2012.pdf`.
- Wellman's in-app device check cleared automatically. The public record then
  exposed its PDF link, which saved `Wellman_Steemans_Vecoli_2013.pdf` directly.
  Thus the in-app outcome differed between the two targets; no general judgement
  about ResearchGate entitlement follows from the first failed route.
- Mehlqvist's complete 12-page article resolves the gap left by the earlier
  one-page ORBi proof. The old source file was preserved.
- The chapter's print citation and copyright year are 2013. Crossref records print
  publication in January 2013 and online publication on 22 January 2014; ResearchGate
  displays January 2014. The register retains the printed 2013 citation and now
  includes the Crossref-verified main-chapter DOI.

## Supplement reconciliation and checks

The old Figshare route in `wellman2013-open` points to the supplementary database,
not the main chapter. The matching 40-page *Supplementary Material: Ordovician–Silurian
dispersed spore assemblages*, compiled by Philippe Steemans, is already held at
`data/external/spores/wellman2013_supplement/18680.pdf`. Its identity, extent and
SHA-256 were checked; it was not downloaded again or counted as a new acquisition.
The existing supplement register identifies Figshare 10.6084/m9.figshare.3453524.v1 /
Geological Society SUP18680 and labels it CC BY 4.0. `library/open_unread.tsv` now
distinguishes the held main chapter from that supplement.

The parent matched titles, authors, DOI, volume and printed pagination to live
Crossref metadata; checked PDF magic and non-empty text on all 28 pages; rendered
all pages and inspected the contact sheet, including the occurrence tables,
plates and maps. Mehlqvist passes qpdf without warnings. Wellman has existing
linearisation/shared-object hint-table warnings, but all 16 pages extract and
render; its original downloaded bytes were retained. Download/archive hashes
match. The verified Downloads duplicates were moved to the recoverable Bin;
archive files remain in place. No permanent deletion was performed.

`library/closed.tsv` records stable source URLs, uploaders, versions, pages, bytes
and hashes. The receipt `work/codex/literature/2026-10-29-researchgate-author-copies.json`
records metadata and cleanup checks. The master register has 492 rows: **454 needed,
22 local-copy-held, 16 open-copy-held**. No new human-action item remains; the ten
parked requests are unchanged. Q1/Q2 and MVD-B scientific readings are pending;
no occurrence, sampling-unit or age adjudication changed.

Codex desktop parent (exact model version not exposed) performed acquisition,
metadata reconciliation, local verification and record updates. No subagent was
used for this bounded two-paper follow-up. Concurrent source/code edits were
preserved.
