# First-study Tier 1 literature acquisition, 29–30 October 2026

Barry authorised collection from `docs/first-study-literature.csv`, with Tier 1 first,
in-app browser first and Chrome as fallback. The curated input tiers and ranks are unchanged.
Tier 2, Bulls Head and the two still-parked sources were not collected in this pass.

## Result and counting units

| Tier 1 register rows | Result |
|---|---:|
| Main text held | 40 |
| Complete abstract held; no longer article established for this identity | 2 |
| Composite source partly held | 1 |
| No target full text acquired | 15 |
| Total | 58 |

The 40 main-held rows represent **39 newly acquired main texts**: `cookson1935b`
and `lang1935-open` are duplicate entries for Lang & Cookson (1935), served by one PDF.
The combined `zalesie-dating` row contains two different references; it is not another
single-paper identity. Sixteen rows remain unresolved or incomplete, including that partial row.
Acquisition does not establish that a source is an analytically usable sampling frame.

**55 files were filed:** 39 main texts, 13 supporting files, two abstracts and one
qualified component copy. Three Morris supporting/data files are byte-identical to
pre-existing project deposits, copied into the reading library for convenience.
Therefore **ten supporting files are newly secured**: seven original files and three
explicitly labelled browser-text captures. The file index below and JSON receipt keep
these units separate.

## Sources made available

For Q1, the new holdings include the Qusaiba-1 spores (Wellman et al. 2015) and acritarchs
(Le Hérissé et al. 2015), QSIM-801 (Le Hérissé et al. 2017), Borenshult-1
(Rubinstein & Vajda 2023), the Sandbian Swedish record (Rubinstein & Vajda 2019),
Kanosh (Vecoli et al. 2015), Hanadir environments (Le Hérissé et al. 2007), and the
2002 Pelmis chitinozoan companion. The 2001 and 2007 Pelmis companions remain gaps.
Kanosh's earlier BioOne/institution-lookup failures were resolved through the
**authenticated UTAS Cambridge proxy**, not by clearing BioOne's challenge.

For Q2/Q4 and the pilot, Hooper 2026 and Morris 2018 main texts are now held alongside
their previously held deposits; so are Morris 2024, Kenrick & Long, Cascales-Miñana 2019,
Kerp 2017, Kenrick & Crane 1991, the older Oxford spore papers, and the original
Lang & Cookson flora. Steemans 2009's original six-page supporting methods, age dating,
spore descriptions and affinity discussion are also held. The main Science Brevia is
one page and **is a complete article**, unlike the two abstracts below.

## Source identity and version qualifications

- `al2014f` is a **GEO 2014 poster presentation abstract**, one page, publicly uploaded by
  Marco Vecoli. It cites the systematic study in press. It is **not the same work** as
  the already-held Strother et al. 2015 journal paper. Parent inspection corrected a
  delegate's preliminary title-family conflation before registration.
- `w4380485474-fulltext` is Rubinstein & Vajda's one-page 2023 conference abstract in
  Estonian Journal of Earth Sciences 72(1):158. Its complete PDF is held; no longer
  journal article for this DOI was identified. The Borenshult GFF paper is a separate source.
  Both master rows now have `kind=abstract`; the focused status CSV calls them `abstract-only`.
- Le Hérissé 2015 (73 PDF pages), Le Hérissé 2017 (96) and Spaak 2017 (72) are
  repository manuscripts, not publisher-final page layouts. They remain qualified as such.
- Xu 2022 is **Research Square version 1, not peer reviewed**, with a separate 18-page
  methods PDF. The record explicitly says its Supplementary Video 1 is unavailable in this version.
- Kenrick & Long's issue is **2026**, New Phytologist 249(6):3149–3164, first online
  17 December 2025. The existing `kenrick2025` ID is retained. Rickards & Garratt is
  printed 1990 despite the publisher's download filename using 2022.
- The old Elsevier DOIs for `al1994` and `al1999` and their current Oxford delivery DOIs
  identify the same respective papers. Both identifiers are retained, never counted as extra works.
- T&F cover pages account for Badawy's 7-page and Rubinstein 2023's 35-page files;
  their journal texts span six and 34 pages respectively. The Sandbian copy has a cover
  plus ten journal pages. Kenrick & Crane has a cover plus 22 pages. File extents are measured,
  not inferred from bibliographic pagination.
- Cascales-Miñana SI3–SI5 were displayed as plain text by the publisher. The saved UTF-8
  files are **browser-decoded captures**, not claims of original byte streams. Their complete
  character counts and FNV-1a fingerprints match the displayed sources. SI5 retains a displayed
  replacement character in one author name. The supplied age table is retained as published,
  not adopted as the project timescale. No supplied analysis text was executed.
- The Masiak 2003 BazTech download completed after Chrome's ordinary automatic site check.
  It has 19 PDF pages, continuous printed 311–329, ending with the bibliography. Its citation
  says 311–330; page 330 is absent/unverified and is not assumed blank. The copy is retained
  as a qualified component of `zalesie-dating`; Trela & Szczepanik 2009 remains unheld.

## Verification and provenance

All 55 archive files have machine-derived sizes and SHA-256 hashes in
`library/closed.tsv` and the matching JSON receipt. All 45 PDFs were checked with
`pdfinfo`, native text extraction and `qpdf --check`: 30 clean results and 15 successes
with warnings. The warning-bearing publisher/scan files render legibly; their original
bytes were preserved. First/last pages and relevant sparse/image pages were rendered
and visually inspected by the parent or bounded QA delegate. Representative contact
sheets remain privately under `library/closed/_qa/2026-10-30-first-study/`.
Morris 2024 PDF pages 13–19 are sparse image plates; each was rendered and inspected.
Sparse extracted text does not indicate absent plates.

The repository DOI verifier checked 35 acquisition identifiers. Two incomplete citation
strings were corrected (the Le Hérissé surname particle and the Rubinstein 2019 title).
Their recheck plus the two Oxford delivery aliases returned **4 distinct DOIs, 0 flagged**,
for 37 distinct verified identifiers in total. Grey sources without DOIs were not assigned
invented identifiers. Only the 58 Tier 1 master rows changed; all 565 master rows are retained.
The master now has 379 needed, 126 local-copy-held and 60 open-copy-held rows. A held abstract
is complete as an abstract; it must not be promoted to a full-article reading downstream.

The complete 55-file inventory and QA are in
`work/codex/literature/2026-10-30-first-study-tier1.json`.
`docs/first-study-literature-status.csv` gives one outcome for every Tier 1 row.
A bounded independent review verified the counts, hashes, versions and identity distinctions.

## Remaining work and housekeeping

The 16 unresolved/incomplete rows are recorded in the first-study section of
`docs/barry-to-action.md`. The simplest actions are Ottone's JSTOR terms step and
the three exact Academia author-copy leads, which require account/terms action.
The latter includes the RPP *Further insights* paper, which is distinct from the
already-held 2012 *Ficoiditheca* paper. Open publisher/repository verification and ordinary
connectivity failures are separated from subscription and grey-literature gaps.
No request, purchase, account creation, personal-data submission or terms acceptance occurred.

Twenty-five verified Downloads duplicates and one task-generated icon were moved to a
recoverable macOS Bin subfolder. Nothing was permanently deleted; only `.DS_Store` and
`.localized` remained in Downloads. The cleanup receipt records every hash and destination.
All owned Chrome tabs were closed. One failed in-app CONICET tab could not be closed
because the browser tool rejects its generated `data:` error-page URL. It is unmarked and
temporary; automatic end-of-turn cleanup is expected, not independently verified here.

The parent Codex session owned browser operations, registration, identity reconciliation and
integration. Three bounded `gpt-5.6-luna` delegates handled public-route/metadata checks,
file QA and final register review. Scientific extraction and adjudication belong to the
main study agents; this acquisition tranche changes no occurrence, age, trait or model claim.

## File index

Paths below are relative to `library/`. Full source URLs, versions, sizes and hashes are
in `library/closed.tsv` and the JSON receipt.

| ID | Kind | File | PDF pages |
|---|---|---|---:|
| `al1994` | main | `closed/al1994_firststudy.pdf` | 22 |
| `al1999` | main | `closed/al1999_firststudy.pdf` | 46 |
| `al2002b` | main | `closed/al2002b_firststudy.pdf` | 21 |
| `al2003d` | main | `closed/al2003d_firststudy.pdf` | 4 |
| `al2003e` | main | `closed/al2003e_firststudy.pdf` | 15 |
| `al2007d` | main | `closed/al2007d_firststudy.pdf` | 14 |
| `al2014f` | abstract | `closed/al2014f_firststudy.pdf` | 1 |
| `al2015f` | main | `closed/al2015f_firststudy.pdf` | 24 |
| `badawy2014` | main | `closed/badawy2014_firststudy.pdf` | 7 |
| `burgess1991` | main | `closed/burgess1991_firststudy.pdf` | 25 |
| `cascalesminana2019` | main | `closed/cascalesminana2019_firststudy.pdf` | 9 |
| `cascalesminana2019` | supplement | `closed/cascalesminana2019_firststudy_SI1.xlsx` | — |
| `cascalesminana2019` | supplement | `closed/cascalesminana2019_firststudy_SI2.docx` | — |
| `cascalesminana2019` | supplement | `closed/cascalesminana2019_firststudy_SI3_browser-text.txt` | — |
| `cascalesminana2019` | supplement | `closed/cascalesminana2019_firststudy_SI4_browser-text.txt` | — |
| `cascalesminana2019` | supplement | `closed/cascalesminana2019_firststudy_SI5_browser-text.txt` | — |
| `cookson1935b` | main | `closed/cookson1935b_firststudy.pdf` | 40 |
| `crane1991` | main | `closed/crane1991_firststudy.pdf` | 23 |
| `edwards1979` | main | `closed/edwards1979_firststudy.pdf` | 30 |
| `elsaadawy1979` | main | `closed/elsaadawy1979_firststudy.pdf` | 29 |
| `garza2024` | main | `closed/garza2024_firststudy.pdf` | 15 |
| `garza2024` | supplement | `closed/garza2024_firststudy_SI1.xlsx` | — |
| `ghavidelsyooki2002` | main | `closed/ghavidelsyooki2002_firststudy.pdf` | 23 |
| `hooper2026` | main | `closed/hooper2026_firststudy.pdf` | 16 |
| `jaeger1966-open` | main | `closed/jaeger1966-open_firststudy.pdf` | 21 |
| `kenrick2025` | main | `closed/kenrick2025_firststudy.pdf` | 16 |
| `kenrick2025` | supplement | `closed/kenrick2025_firststudy_SI1.docx` | — |
| `kerp2017` | main | `closed/kerp2017_firststudy.pdf` | 16 |
| `leherisse2015` | main | `closed/leherisse2015_firststudy.pdf` | 73 |
| `leherisse2017` | main | `closed/leherisse2017_firststudy.pdf` | 96 |
| `morris2018` | main | `closed/morris2018_firststudy.pdf` | 11 |
| `morris2018` | supplement | `closed/morris2018_firststudy_SI1.pdf` | 47 |
| `morris2018` | supplement | `closed/morris2018_firststudy_SI2.zip` | — |
| `morris2018` | supplement | `closed/morris2018_firststudy_SI3.txt` | — |
| `morris2024` | main | `closed/morris2024_firststudy.pdf` | 19 |
| `naugolnykh2019` | main | `closed/naugolnykh2019_firststudy.pdf` | 10 |
| `naugolnykh2022` | main | `closed/naugolnykh2022_firststudy.pdf` | 17 |
| `rickardsgarratt1990` | main | `closed/rickardsgarratt1990_firststudy.pdf` | 6 |
| `rubinstein2019-open` | main | `closed/rubinstein2019-open_firststudy.pdf` | 11 |
| `rubinstein2023` | main | `closed/rubinstein2023_firststudy.pdf` | 35 |
| `spaak2017` | main | `closed/spaak2017_firststudy.pdf` | 72 |
| `steemans2009a` | main | `closed/steemans2009a_firststudy.pdf` | 1 |
| `steemans2009a` | supplement | `closed/steemans2009a_firststudy_SI1.pdf` | 6 |
| `strother2024` | main | `closed/strother2024_firststudy.pdf` | 20 |
| `taylor2024` | main | `closed/taylor2024_firststudy.pdf` | 17 |
| `w4380485474-fulltext` | abstract | `closed/w4380485474-fulltext_firststudy.pdf` | 1 |
| `wang2013` | main | `closed/wang2013_firststudy.pdf` | 5 |
| `wellman1996` | main | `closed/wellman1996_firststudy.pdf` | 34 |
| `wellman1998` | main | `closed/wellman1998_firststudy.pdf` | 31 |
| `wellman2015` | main | `closed/wellman2015_firststudy.pdf` | 16 |
| `wellman2017a` | main | `closed/wellman2017a_firststudy.pdf` | 10 |
| `wellman2017a` | supplement | `closed/wellman2017a_firststudy_SI1.xls` | — |
| `xu2022` | main | `closed/xu2022_firststudy.pdf` | 24 |
| `xu2022` | supplement | `closed/xu2022_firststudy_SI1.pdf` | 18 |
| `zalesie-dating` | main-component | `closed/zalesie-dating_masiak2003_firststudy.pdf` | 19 |
