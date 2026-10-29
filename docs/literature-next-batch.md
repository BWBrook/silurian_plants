# Literature batch — proposal and Stage A outcome, 29 October 2026

**Stage A authorised and completed as an access attempt:** five of six papers plus
one supplement acquired; Liu 2016 remains a fresh challenge/delivery blocker.
See `docs/audits/2026-10-29-six-paper-batch.md`. Stage B remains a proposal.

**Original recommendation:** first collect six priority-one recent Elsevier papers through
the existing UTAS session, then attempt two public ResearchGate author copies.
This is a proposed eight-text tranche, with a six-text first stage. No new paper
or supplement was downloaded in this planning pass.

## Current register and exclusions

The preflight CSV had **492 rows: 462 needed, 16 local-copy-held and 14
open-copy-held**. Ten needed entries are parked in `docs/literature-requests.md`:
eight remaining from the original pilot, the earlier Garratt 1978 case, and Paris
et al. 2012, whose exact signed-in catalogue result was request-only today. That
leaves 452 unparked needed rows, not 452 verified downloadable full articles.
Keep parked status separate from scientific need; all ten remain `needed` in the
master register and their notes link to the parked list.

Select acquisition targets by work identity **and asset kind/version**. A repeated
DOI may represent a paper and its supporting information, both legitimately
needed. Rows without DOIs also include alternate routes to the same work.

## Stage A: preflight evidence for six institutional candidates

All six exact DOI searches in signed-in UTAS **Everything** returned the matching
article with an available-online route. For two, the actual UTAS-proxied
ScienceDirect article was also inspected and showed **Full text access** plus an
enabled **View PDF** link. The other four are catalogue-level preflights only;
their publisher entitlement and saved-file integrity remain to be established.
A catalogue/LibKey link is not, by itself, evidence of entitlement.

| Order | ID | Target and purpose from the register | Current evidence |
|---:|---|---|---|
| 1 | `al2025b` | Strother et al. 2025, Hirnantian freshwater palynological assemblage, Saudi Arabia; primary spore assemblage | Catalogue route and actual ScienceDirect full-text/PDF access verified. [UTAS route](https://libkey.io/libraries/729/articles/656610825/content-location?utm_source=api_3637&allow_speedbump=true) |
| 2 | `wang2026` | Wang et al. 2026, *Dynamic evolution of cryptospores*; latest global review and possible occurrence-table source | Exact catalogue match, Available Online; [UTAS route](https://libkey.io/libraries/729/articles/702347248/content-location?utm_source=api_3637&allow_speedbump=true). Actual article/PDF not yet checked |
| 3 | `al2017c` | Vecoli et al. 2017, Middle Ordovician cryptospores from QSIM-801, Saudi Arabia; primary spore assemblage | Actual UTAS ScienceDirect full-text/PDF access verified. [UTAS route](https://libkey.io/libraries/729/articles/152828174/content-location?utm_source=api_3637&allow_speedbump=true). Duplicate catalogue records share this route |
| 4 | `al2016e` | Liu et al. 2016, Ludlow palynomorphs from Lvchun, Yunnan; Chinese assemblage | Exact catalogue match, Available Online; [UTAS route](https://libkey.io/libraries/729/articles/58299695/content-location?utm_source=api_3637&allow_speedbump=true). Actual article entitlement not verified |
| 5 | `pirikangarshahi2020` | Ghavidel-Syooki & Piri-Kangarshahi 2020, Upper Ordovician palynology of Kuh-e Boghou, Iran | Exact catalogue match, Available Online; DOI `10.1016/j.revpalbo.2020.104337`. Actual article/PDF not yet checked |
| 6 | `al2023c` | Wang et al. 2023, Llandovery palynoflora of southern Xinjiang; Tarim/Gondwana context | Exact catalogue match, Available Online; DOI `10.1016/j.jseaes.2023.105769`. Actual article/PDF not yet checked |

Why this lane: native Chrome PDF controls and the UTAS-proxied ScienceDirect route
have now worked repeatedly. The six are already priority one, have exact source
identities and are relevant to Q1/Q2 or the spore compilation. Today's Paris 2012
request-only result in the same journal shows why access must still be checked
per paper; there is no assumed publisher-wide or date-wide entitlement.

After the authorised Stage A attempt, the CSV has **457 needed, 21 local-copy-held
and 14 open-copy-held**. The files, versions and sole blocker are in the batch audit
and `library/closed.tsv`. The table above preserves the evidence before collection.

## Stage B: two public author-copy candidates

| ID | Target | Route and acceptance requirement |
|---|---|---|
| `w2080475227-fulltext` | Mehlqvist, Vajda & Steemans 2012, Late Silurian Skåne spore assemblages (GFF, pp. 133–144) | [ResearchGate author record](https://www.researchgate.net/publication/233859796_Early_land_plant_spore_assemblages_from_the_Late_Silurian_of_Skane_Sweden) lists author content `Mehlqvist_2012.pdf`, with a 12-page article indexed. Current ORBi copy is only page 1 of a 12-page proof. Recover and verify all pages; retain version. This paper is distinct from the parked Mehlqvist 2013 thesis |
| `wellman2013-open` | Wellman, Steemans & Vecoli 2013, *Palaeophytogeography of Ordovician–Silurian land plants*, chapter 29, pp. 461–476 | [ResearchGate author record](https://www.researchgate.net/publication/261700238_Palaeophytogeography_of_Ordovician-Silurian_Land_Plants) exposes main-chapter text. The old Figshare URL is supplementary material, not the chapter. Retrieve the actual main chapter, retain author/publisher version label, and reconcile the supplement separately |

Chrome's normal public full-text download worked for Strother's author preprint,
even though direct shell requests failed. That supports a bounded browser attempt
for these two; it does not guarantee ResearchGate access or full-file availability.

## Reconcile separately; do not inflate the collection count

Parent inspection of existing local PDFs exposed four traps in the initial
metadata-based shortlist:

- `w4380485495-fulltext`, Wellman et al. 2023, DOI `10.3176/earth.2023.03`:
  the held PDF is explicitly **ABSTRACT**, the complete one-page published item
  on p. 164. A fresh download of the same file would not recover a missing full
  research article. Record its abstract evidence status rather than assume a
  longer version exists under that DOI.
- `w4380485474-fulltext`, Rubinstein & Vajda 2023, DOI
  `10.3176/earth.2023.42`: the held item is the one-page p. 158 contribution in
  the same issue; the primary issue identifies it as an abstract. It is not
  Rubinstein et al. 2023's Colombian paper. The one-page/word-count rule needs
  source-kind adjudication, not automatic re-fetching.
- `gerrienne2011-open`: the direct public ORBi `Gerrienne et al 2011b.pdf` is
  labelled **Annexes**. The main Science paper `Gerrienneetal2011.PDF` is
  request-only on [ORBi](https://orbi.uliege.be/handle/2268/97121). Supplement
  availability must not be counted as main-paper acquisition; an institutional
  main-paper route remains untested.
- `capel2023-si`: the held nine-page HAL PDF is the main Capel et al. 2023
  article, not the supporting information that the CSV row requests. Keep the
  SI gap open.

These are reconciliation findings, not holdings/status changes in this pass.
The raw harvest and existing manifests remain unchanged. The scientific use of
an abstract or an author version must stay visible.

## Deferred lane

BHL historical volumes, Royal Society scans, DiVA, Durham and the older
subscription-only papers remain useful but have weaker current evidence of an
automatic route. Public checks still returned challenges/403s for several.
Do not use these to fill a nominal twenty-paper batch. Prove one representative
route before treating a whole host as an efficient collection lane.

## Execution and reporting after approval

For each target, verify title/DOI/version and expected printed pagination, identify
relevant supplements, save directly to the library where supported, then check
local file completeness and record URL, bytes and SHA-256. Use Downloads only
when forced by the site's download behaviour. Distinguish full publisher copy,
complete author copy, supplement, abstract and incomplete excerpt.

Close each completed or blocked work tab promptly. A bounded redirect/rendering
check plus native Chrome/screenshot fallback precedes a failure verdict. A fresh
human-action blocker goes into `docs/barry-to-action.md`; a request-only candidate
goes directly to `docs/literature-requests.md`. Do not retry BioOne, schedule
monitors or submit requests. Report the batch as verified acquisitions out of the
eight chosen **texts**, with publisher/author versions separated and supplements
counted separately. A successful viewer alone is not a verified acquisition.

## Downloads cleanup completed

On 29 October 2026, 19 Downloads files were verified byte-for-byte against the
archived PDFs/supporting document using the recorded SHA-256 values. Two further
literature HTML landing/download residue files were identified. The 21 files
(67,084,004 bytes) were moved to the recoverable Bin folder
`/Users/bwbrook/.Trash/silurian-literature-20261029-123807`; the Bin was not emptied.
Every moved file's hash was checked after the move. All archive copies remain.
Receipt: `work/codex/literature/2026-10-29-downloads-cleanup.json`.

## Roles and scope

Codex desktop parent owns the proposal, live authenticated catalogue/publisher
checks, local PDF identity inspection, request-queue separation and Downloads
cleanup. A `gpt-5.6-luna` scout reconciled manifests; a `gpt-5.6-luna` executor
checked public routes. Their initial metadata shortlist included version traps;
parent inspection and the targeted follow-up corrected them before recommendation.
No new scientific reading or occurrence adjudication was undertaken. The subsequent
authorised Stage A collection and its delegate roles are recorded in the batch audit.
