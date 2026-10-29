# Regional spore literature batch, 29 October 2026

Barry authorised the six shortlisted main texts and the Ghelli correction
companion. All seven PDF assets were acquired autonomously, plus one unique KML
map available through both Ghelli DOI records. No human intervention was needed.
Ten parked requests remained outside the batch.

## Holdings

Original publisher files are private and git-ignored under `library/closed/`.
`library/closed.tsv` records stable source URLs, versions, pages, bytes and SHA-256.
The receipt is `work/codex/literature/2026-10-29-regional-spores-batch.json`.

| Register ID | Verified work | File | PDF pages |
|---|---|---|---:|
| `ghavidelsyooki2016` | Ghavidel-Syooki 2016, Ghelli Formation; RPP 231, 48–71; DOI 10.1016/j.revpalbo.2016.04.006 | `ghavidelsyooki2016_bundle.pdf` | 49, including update and reissue |
| `ghavidelsyooki2017` | Ghavidel-Syooki 2017, publisher-labelled Erratum/Update; RPP 244, 217–240; DOI 10.1016/j.revpalbo.2017.05.010 | `ghavidelsyooki2017.pdf` | 24 |
| `al2018g` | El Diasty et al. **2019**, Tanezzuft Formation; Revue de Micropaléontologie 62, 45–58; DOI 10.1016/j.revmic.2018.06.002 | `eldiasty2019.pdf` | 14 |
| `ghavidelsyooki2021` | Ghavidel-Syooki 2021, High Zagros; RPP 292, 104457; DOI 10.1016/j.revpalbo.2021.104457 | `ghavidelsyooki2021.pdf` | 35 |
| `al2021i` | Xu et al. **2022**, Hezhang; RPP 297, 104561; DOI 10.1016/j.revpalbo.2021.104561 | `xu2022_hezhang.pdf` | 9 |
| `al2022c` | Filipiak et al. 2022, Holy Cross Mountains; RPP 302, 104666; DOI 10.1016/j.revpalbo.2022.104666 | `filipiak2022.pdf` | 22 |
| `wellman2017b` | Wellman **2018**, northern New Brunswick; RPP 249, 24–49; DOI 10.1016/j.revpalbo.2017.11.003 | `wellman2018.pdf` | 26 |

The bold years correct harvest labels based on DOI/online years; stable register
IDs were retained. Crossref metadata and the downloaded journal identities agree.

## Ghelli version relationship

The publisher's `mainext.pdf` is a 49-page bundle:

- PDF pages 1–24: original 2016 article, printed pages 48–71.
- PDF page 25: explicit **Update** cover identifying the 2017 DOI and the original
  article DOI, 10.1016/j.revpalbo.2016.04.006.
- PDF pages 26–49: 2017 reissued article, printed pages 217–240.

The separately downloaded 2017 PDF is text-identical to bundle pages 26–49 in a
layout-extracted comparison. Retain the two DOI identities and publisher update
relationship; they concern the same study and must not count as independent
assemblage evidence. The publisher labels the companion *Erratum* and *Free access*;
this run obtained it through the UTAS session, with no open reuse licence verified.

A paired check found all numerical values and rows of Table 1 matched between the
2016 and 2017 versions (original PDF page 4 / printed 51; reissue PDF page 4 /
printed 220). A raw text-layout diff does not establish changed numerical data.
This acquisition does not adjudicate all textual, taxonomic or presentation
changes; any later extraction must identify the version used.

Both article records link a KML study-area map. The original bytes are preserved
as `ghavidelsyooki2016_SI.kml` and `ghavidelsyooki2017_SI.kml`, each 1,258 bytes,
with identical SHA-256. XML/KML validation passed. These are two provenance routes
to **one unique map supplement**, not two independent data resources.

## Access, supplement search and verification

The in-app browser was used first for article access and linked-file inspection.
The Ghelli PDFs rendered there, but the automation could not operate the PDF
viewer's closed-shadow-root save control; its direct-download helper timed out,
and the save shortcut produced no file. Chrome's normal native PDF toolbar and
Save dialog worked. All seven original PDFs were saved directly to
`library/closed/` through that authorised fallback, without bypassing a challenge
or access control. All owned browser tabs were closed.

Article links and complete PDF text were checked for separate supporting files.
Only the shared Ghelli map was identified. Internal appendices remain inside the
main PDFs: Wellman's sample-details Appendix 1 is on PDF page 5, printed page 28;
El Diasty's taxon appendix is also internal. This records the search scope, not
proof that no other data deposit exists.

Every PDF has valid PDF magic, the expected DOI and identity, and non-empty text
on every page. Independent local QA checked structure and rendered endpoints;
the parent inspected a contact sheet and checked the sample-appendix location
against the actual file. The Ghelli bundle has an unsorted Name/Number-tree
warning; High Zagros and Filipiak have hint-table warnings. Extraction and checked
renders remain intact; the bundle also emits an annotation bounding-box warning
during text extraction. Original files were retained unchanged. No file repair or
conversion was substituted for the publisher download.

The two map files temporarily saved to Downloads were matched byte-for-byte to
their archives, moved to a recoverable Bin folder and checked again by SHA-256.
Downloads has no literature residue; no permanent deletion was performed.

The repository DOI scan checked 725 distinct strings and flagged 21: twenty
existing Markdown-backtick parsing failures and one incomplete Wellman citation
context in the earlier literature decision. That citation now includes author,
year and full title; a targeted recheck with the same checker functions passes.
The twenty scanner-formatting flags remain outside this acquisition task. All
seven acquired DOI identities were verified against Crossref in preflight.

The CSV now has 492 rows: **447 needed, 29 local-copy-held, 16 open-copy-held**.
Seven source rows were resolved, representing six studies plus the Ghelli update.
No active human-action item was added. Q1/Q2 and the MVD-B spore compilation can
now read these sources; cards, occurrence units, model inputs and scientific
adjudications were unchanged.

Codex desktop parent (exact model version not exposed) owned acquisition,
registers and integration. A bounded `gpt-5.6-luna` delegate checked metadata
before selection; a second bounded `gpt-5.6-luna` delegate checked local file QA
and the Ghelli version relationship. Parent checks corrected two preliminary QA
interpretations: Table 1 numerical values match, and Wellman's Appendix 1 is on
PDF page 5, not page 26. Concurrent scientific/code edits were preserved.
