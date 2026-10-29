# Six-paper institutional collection, 29 October 2026

Barry authorised Stage A of `docs/literature-next-batch.md` after refreshing the
access guidance. All six full texts and one supplementary document are now held.
Five papers were collected autonomously; Barry resolved Liu 2016 through the
in-app browser. The two ResearchGate candidates and ten parked requests were
outside this run.

## Holdings

Files are private, git-ignored, under `library/closed/`. `library/closed.tsv` records
source URLs, versions, pagination, bytes and SHA-256 for each asset. Machine-readable
metadata and verification: `work/codex/literature/2026-10-29-six-paper-batch.json`.

| Register ID | Work | File | Extent and version |
|---|---|---|---|
| `al2025b` | Strother et al. 2025; RPP 338, 105322; DOI 10.1016/j.revpalbo.2025.105322 | `strother2025.pdf` | 26 pages; PDFium print export of the loaded publisher PDF |
| `wang2026` | Wang et al. 2026; Earth-Science Reviews 277, 105476; DOI 10.1016/j.earscirev.2026.105476 | `wang2026.pdf` | 30 pages; original publisher PDF |
| `al2017c` | Vecoli et al. 2017; Revue de Micropaléontologie 60(3), 319–331; DOI 10.1016/j.revmic.2017.06.003 | `vecoli2017.pdf` | 13 pages; original publisher PDF |
| `pirikangarshahi2020` | Ghavidel-Syooki & Piri-Kangarshahi **2021**; RPP 284, 104337; DOI 10.1016/j.revpalbo.2020.104337 | `ghavidelsyooki2020.pdf` | 25 pages; original publisher PDF; legacy ID/filename retained |
| `al2023c` | Wang et al. 2023; Journal of Asian Earth Sciences 255, 105769; DOI 10.1016/j.jseaes.2023.105769 | `wang2023.pdf` | 13 pages; original publisher PDF |
| `al2016e` | Liu et al. 2016; RPP 233, 146–160; DOI 10.1016/j.revpalbo.2016.02.003 | `liu2016.pdf` | 15 pages; original publisher PDF, downloaded by Barry in Codex in-app browser |
| `al2023c` | Same work, Appendix A, Supplementary data 1 | `wang2023_SI.docx` | Publisher DOCX; comparison table of early Silurian non-marine palynomorphs and references |

All main articles used the UTAS ScienceDirect route. Barry downloaded Liu in
Codex's in-app browser; the other five used authenticated Chrome. Wang 2026 also displayed “Complimentary access”. Strother 2025 rendered
all 26 pages, but the native download returned security-verification HTML. Chrome's
normal print-to-PDF function preserved the already loaded document. This is a
browser-generated copy, not the original publisher byte stream; its metadata and
hash describe that derivative. It passed all-page text and rendered-page checks.

The Iranian paper's PDF and Crossref both identify the publication as 2021.
The DOI contains 2020, and the harvest ID used 2020; the register citation is now
corrected while retaining the stable source ID and filename.

## Resolved blocker and access history

`al2016e`: Liu et al. 2016, *Palynomorphs from massive metamorphosed rocks in
Lvchun, Yunnan, Southwest China*, RPP 233, 146–160,
DOI 10.1016/j.revpalbo.2016.02.003.

The [UTAS article](https://www-sciencedirect-com.ezproxy.utas.edu.au/science/article/pii/S0034666715300142)
shows **Full text access**, but its PDF route stalled. A bounded retry through the
previously verified [library resolver](https://libkey.io/libraries/729/articles/58299695/content-location?utm_source=api_3637&allow_speedbump=true)
also stalled. The article's download control timed out; its saved `pdfft.html`
was an Elsevier PDF-challenge page naming this exact PII, not a PDF. No challenge
was solved or bypassed. A public CAS news-page lookup did not yield a usable copy.
Barry subsequently reported immediate click-through in Codex's in-app browser
and saved the original PDF to Downloads. The parent verified all 15 pages and
printed endpoints 146–160, the title/DOI, PDF structure, first/last renders and
matching source/archive SHA-256. It is now `local-copy-held`, archived as
`library/closed/liu2016.pdf`; the ledger action is resolved and its PDF tab closed.
The earlier delivery/challenge failure did not establish an entitlement problem;
its exact cause remains unproven.

## Verification and limits

- Exact DOI metadata was checked against Crossref, including authors, journal,
  volume and pagination/article number. Each PDF contains the expected DOI and
  identity, has valid PDF magic, and yields non-empty text on every page.
- Independent read-only QA of the first five papers checked PDF structure, first/last renders, and the
  supplementary DOCX ZIP/XML. The parent inspected rendered contact sheets.
  Minor existing hint-table/outline warnings in Wang 2026, the Iranian paper and
  Wang 2023 do not prevent complete extraction or rendering; the original files
  were retained unchanged. Liu's follow-up checks were performed by the parent;
  qpdf reported no syntax or stream errors.
- Authenticated article links and main-PDF text were checked for supporting
  material. Only Wang 2023 identified a separate supplementary asset. This records
  the scope of the search, not proof that no other data deposit exists.
- The supplement's Downloads copy matched its archive SHA-256. That duplicate and
  the identified Liu challenge HTML were moved to a recoverable Bin folder,
  `/Users/bwbrook/.Trash/silurian-literature-20261029-batch/`, with post-move hash
  verification. Liu's later successful PDF download was also checksum-matched to
  its archive and moved to the same recoverable Bin folder. Archive files remain
  in place; Downloads has no new literature residue. No permanent deletion was
  performed.

The register now has 492 rows: **456 needed, 22 local-copy-held, 14 open-copy-held**.
No fresh human-action item remains; the ten parked requests are unchanged.
Acquisition does not adjudicate any occurrence, fossil-to-node mapping or age.
Q1/Q2 and the MVD-B spore compilation can now re-read these sources; extraction
and scientific interpretation remain pending.

## Access refresh and roles

The parent re-read `~/.codex/AGENTS.md`, `~/work/nectar/README.md` and the relevant
canonical access workflow. Current short aliases and the public `nectar` hub route
supersede historical campus routing; no remote job or backup was run here.
Exactly one harmless Correspondence `list_threads` read succeeded. No MCP
reconnection, acknowledgement or message was needed.

Codex desktop parent (exact model version not exposed) owned browser acquisition,
version decisions, registers, provenance and integration. Two existing bounded
`gpt-5.6-luna` delegates independently checked public metadata and local file QA.
Barry supplied the final Liu download; the parent verified and archived it.
Concurrent scientific changes were untouched.
