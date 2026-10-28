# Literature-sourcing pilot, 28 October 2026

The pilot checked 20 selected register entries for Q1/Q2 and spore sampling. Five
complete papers were acquired; 15 remain unresolved. The entries are research leads,
not a demonstrated set of eligible spore-negative sampling units. Acquisition alone
does not adjudicate fossil identity, dating or other scientific claims. Searches were
bounded and did not establish that every possible open or institutional route was tried.

## Twenty selected targets

The register IDs link the outcomes to full citations and DOIs in
`docs/closed-literature.csv`. Current files, URLs and hashes for acquired papers are in
`library/closed.tsv` or `library/open.tsv`; actionable routes for unresolved papers are
in `docs/barry-to-action.md`. The 19 DOI-bearing targets were checked against Crossref;
the Mehlqvist thesis has no DOI recorded.

| ID | Target | Outcome |
|---|---|---|
| `edwardsfeehan1980` | Edwards & Feehan 1980, Irish *Cooksonia*-type sporangia | Complete UTAS publisher PDF, printed pp. 41–42, `library/closed/edwardsfeehan1980.pdf`. |
| `libertin2018` | Libertín et al. 2018, early Silurian polysporangiophytes | Complete UTAS publisher article, pp. 269–271, plus reporting-summary pages, `library/closed/libertin2018.pdf`. Supporting information also held; see provenance below. |
| `kotyk2002` | Kotyk et al. 2002, Bathurst Island flora | Complete 10-page publisher-formatted article, pp. 1004–1013, from the University of Saskatchewan repository: `library/open/W2112174729.pdf`. Kotyk's thesis is a related source, not the journal article. |
| `kraft2017` | Kraft & Kvaček 2017, Silurian lycophytes | ScienceDirect displayed UTAS access, but the PDF viewer and download stalled; no complete PDF. The later nomenclatural paper is a partial surrogate. |
| `libertin2024` | Libertín et al. 2024, *Aberlemnia* | Complete 11-page UTAS publisher PDF, `library/closed/libertin2024.pdf`. The previously reported alternative-affinity claim has not been adjudicated here. |
| `garratt1984` | Garratt et al. 1984, Silurian *Baragwanathia* | Publisher security screen and stalled UTAS sign-in; a catalogue PDF route exists, but entitlement is unknown. |
| `garrattrickards1984` | Garratt & Rickards 1984, Yea graptolite correlations | Anonymous 403 and a stalled article page; a UTAS catalogue PDF route exists, but entitlement is unknown. Later Yea accounts are related sources, not this paper. |
| `taylor2017` | Taylor et al. 2017, spore-wall ultrastructure | Complete UTAS publisher PDF, printed pp. 281–288, `library/closed/taylor2017.pdf`. |
| `strother2000` | Strother 2000, cryptospore chapter | Cambridge access unresolved. The author describes a separately formatted preprint with different pagination; its download was blocked. Neither version was acquired. |
| `mehlqvist2013` | Mehlqvist 2013, Swedish spore thesis | Lund identifies the thesis, ISBN `978-91-86746-95-7`, but no complete PDF was found. Constituent papers are not the complete thesis. |
| `cesari2019` | Vecoli & Cesari 2019, Saq Formation conference paper | OnePetro security verification blocked the page; UTAS entitlement unknown. The indexed title includes an apparent “Manuscript Title” artefact that needs checking. |
| `al1996b` | Strother et al. 1996, Saudi Arabian spores | Publisher security verification blocked the page; UTAS entitlement unknown. The held 2015 Hanadir paper is a different work. |
| `al1996` | Steemans et al. 1996, southeastern Turkey | ScienceDirect reported no UTAS subscription for this item; Liège lists a PDF only by request. No request was sent. |
| `al2015f` | Vecoli et al. 2015, Kanosh Shale | Cambridge's UTAS institution lookup failed; entitlement unknown and no full text obtained. |
| `al2007d` | Le Hérissé et al. 2007, Hanadir environments | ScienceDirect reported no UTAS subscription for this item; its full-text-at-UTAS link returned “Invalid Library”. |
| `al2011n` | Vecoli et al. 2011, Anticosti and Estonia | ScienceDirect reported no UTAS subscription for this item; the article page is not the complete paper. |
| `al2015e` | Raevskaya et al., Siberian cryptospores | UTAS access was displayed but the viewer stalled. The university-hosted candidate has only page 1 of 10 and is not a full acquisition. Issue year 2016; online 2015. |
| `al2016i` | Tang et al., Tarim Basin cryptospores | UTAS access was displayed but the PDF viewer stalled; no complete PDF. Issue year 2017; online 2016. |
| `al2023b` | Rubinstein et al. 2023, Colombian cryptospores | Repository advertises a full open PDF, but the host timed out in both public checks and Chrome. A separate publisher supplement is also unverified. |
| `al2008f` | Vecoli et al., Ghadamis Basin palynology | ScienceDirect reported no UTAS subscription for this item. The issue is 2009; the register says 2008, but an advance-online date remains unverified. |

The Libertín et al. 2018 supporting information is
`library/closed/libertin2018_SI.pdf`. It was recovered from an earlier project scratch
copy, not downloaded from a verified original route in this pilot. Its hash and the
publisher's corroborating supplement link are recorded in `library/closed.tsv`; that
link is not evidence of the original transfer.

## Register reconciliation

An earlier input snapshot contained **489 rows**: 473 `needed`, 11 `open-copy-held`,
and 5 `local-copy-held`. These are row counts, not distinct works or a measure of
inaccessibility. Its `docs/closed-literature.csv` SHA-256 was
`77b25c4d2ce8a15cd451cf469374c460d6de3caad09396a18ad5aca924bfd122`. Automated
reconciliation flagged 42 rows without an exact DOI/OpenAlex identity, five short or
non-text copies needing review, four separately requested supplements, and two
potential already-held main works; these flags do not establish final acquisition status.
The other input hashes are listed below. After the five acquisitions and two verified
existing copies were recorded, the live register had 489 rows: 466 `needed`, 14
`open-copy-held`, and 9 `local-copy-held` at this audit.

Two works outside the 20 were already held and were reconciled, rather than newly
acquired: Kidston & Lang 1921 Part IV (`kidston1921-open`, 29 pages including plates,
`data/external/local/library/pdf/XU101.pdf`) and Field et al. 2016 (`field2016`,
13 pages, `data/external/local/library/pdf/W2176407474.pdf`). Their original harvest
routes and hashes are recorded in the external-library manifests.

Six **candidate duplicate pairs of main-work entries** were identified. Keep both
route and identifier aliases until identity and holdings are reconciled:

| Register entries | Evidence / qualification |
|---|---|
| `cookson1935-open` / `cookson1935` | Same linked main-work DOI. |
| `croft1942-open` / `lang1942` | Same linked main-work DOI. |
| `lang1935-open` / `cookson1935b` | Same linked main-work DOI. |
| `libertin2022-open` / `libertin2022` | Same linked main-work DOI. |
| `hopkins1976` / `mcbride1976` | Same title and OpenAlex work; the register contains two DOI strings, which need reconciliation. |
| `hueber1961-open` / `hueber1961` | Matching author, year, journal, volume and page; the BHL route points to a volume and needs article-level confirmation. |

`toledo2021` and `toledo2021-si` share a DOI but request the main paper and its
supplement respectively; keep them as separate artefacts. The same principle applies
to other supplements and to different versions such as author preprints.

## Follow-up

Use `docs/barry-to-action.md` for the 15 unresolved routes, including verification
screens, catalogue checks, stalled downloads, the one-page candidate and the
author-preprint lead. No library or author request was sent. Any request or purchase
is Barry's decision. In later scientific work, check methods, dates, facies, material
identity and reporting before treating a source as a positive or eligible negative;
post-2006 records require a matching sampling frame before use as denominators.

The reconciliation snapshot also used these SHA-256-identified inputs:

| Input | SHA-256 |
|---|---|
| `library/closed.tsv` | `396c9eeed24a5fe04f94e330aaf2f3b15c084c3a53ad2574650bf83e746c3a18` |
| `library/open.tsv` | `464caf3b3629ddb1446871c419534c77c0d7458f4aa84f00fa196fd5715fdcde` |
| `data/external/library/fetch_results.tsv` | `d0aa505168c114806a6f797d0e9e9235a2cb9d181e71057bf51016c18cd57070` |
| `data/external/library/works.tsv` | `32c6db6c344cbb166e235822608f03797242c1971141a97955d5fbb8a33e4806` |
| `data/external/library/cited_dois_resolution.tsv` | `933894d20d8366334637bfca384fcc90fd22175a55422d2731265e7a239f163d` |
| `data/external/library/cited_identity_check.tsv` | `2c8dad44c0066597a56dfb3b8b0a49a13f44691bd01ce444f96a7c55473d351a` |
| `data/external/library/open_unread_results.tsv` | `cc4e3bf2a14da5bd9555dbd9f8d53174bc476859d2a7120f7fdcf84ae5a92cf3` |
