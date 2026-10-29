# Autonomous literature expansion: second checkpoint, 29 October 2026

The second checkpoint adds **39 main texts and 16 supporting files**: 55 private assets, 137,824,077 bytes and 658 PDF pages (592 main-text pages). Together with the first checkpoint, the autonomous tranche recovered **85 main texts, 41 supporting files and one erratum**: 127 assets. The full CSV now contains 492 unique IDs: 360 needed, 99 local-copy-held and 33 open-copy-held. The 41 newly resolved rows in this checkpoint include two supplement-only rows; row counts are not independent-study counts.

Files are in git-ignored `library/closed/`. Per-file URLs, versions, extents and SHA-256 values are in `library/closed.tsv`; the self-contained receipt is `work/codex/literature/2026-10-29-autonomous-wave2.json`. The first checkpoint is preserved separately. No scientific extraction, occurrence adjudication, card, age, trait or model change was made.

## Routes and important qualifications

Thirty-four main texts came through the UTAS Wiley route. Four Lethaia papers came through SCUP's public free-access route, with two original supporting files. The 2011 Ghelli/Soltan Maidan paper was recovered from Caltech's public author-hosted PDF after the UTAS Elsevier route showed a preview. That 22-page file has a publisher personal-copy cover plus printed pages 251–271. Public availability is not an open reuse licence.

Capel's four supporting files and Toledo's 29-page supplement close two existing supplement-only gaps; their main papers are not newly counted for Capel and are counted once for Toledo. Other supporting files cover Falster, Labandeira, Klaus, Strullu-Derrien, Testo, Horinouchi and Winther. Legacy DOC/XLS files were format-checked; DOCX/XLSX containers passed integrity checks. No supplied code was executed.

The three Edwards rows whose DOI fields were blank now carry their verified DOI strings from the explicit links: 10.1111/nph.12645, 10.1111/nph.17703 and 10.1111/nph.17704. The latter two have 2021 online dates and 2022 print issues. Petersen & Burd's heterospory review and Klaus's Selaginella study have 2017 print issues despite 2016 filenames. Stable harvest IDs are retained. `mcbride1976` remains unresolved as a catalogue alias: its Crossref identity overlaps the held Hopkins–McBride paper, but its publisher DOI route returned 404; it was not counted as a second recovered paper or silently merged.

## Verification

Every delivered file was rehashed against its register entry, and every main text was checked for identity and page extent, with first/last representative pages rendered and inspected. All originals are retained unchanged and excluded from Git. Small qpdf linearisation, xref or name-tree warnings are documented rather than repaired.

Parent verification found and corrected two delegate omissions (Strother's 2015 review and Klaus's supplement), erroneous transcribed QA size/hash fields, and an overstatement about native text extraction. The authoritative receipt uses machine-derived hashes and explicitly supersedes those earlier narrative fields. Five older PDFs (Hopkins 1976, the two Graham 1985 papers, Xue 2009 and Hao & Xue 2011) are scanned or partly scanned. Their native extraction is sparse; temporary OCR succeeded for all five and all their pages yielded text after OCR. These OCR derivatives remain temporary reading/verification aids, outside the archive asset count. Adjacent article fragments in old journal scans are retained; original bytes were not cropped or replaced.

All 53 matching Downloads staging duplicates were checked against archive hashes, moved to the recoverable Bin folder `~/.Trash/silurian-literature-20261029-autonomous-checkpoint2`, then rehashed there. Trash was not emptied. Both browsers had zero collection tabs at close. No request, purchase, account creation, terms acceptance, CAPTCHA solving or external message was performed.

## Remaining routes

Chrome's native PDF save remains blocked by the Mac locking again. Shute 1989, Fanning 1992, Edwards 1980 and Mark 2011 have observed article/PDF routes but no acquired file; the ledger groups these as a save-control follow-up. Eight other Oxford candidates remain metadata-identified and unattempted in this second pass, not entitlement failures.

Kasper 1972 and 1974 returned access/purchase options through UTAS Wiley. An exact JSTOR alternative for Pertica is verified, but its institutional reader/menu did not render a usable download control. Five further Elsevier backfile candidates showed previews. The public-copy check rescued the sixth, Ghelli 2011; the Urubu and Saudi glacial-sediment searches exposed request-only records. Remaining author/repository routes for the other backfile candidates have not been exhausted. The original ten parked requests were left untouched. The action and request ledgers distinguish these outcomes.

The working priority now is the Oxford/native-save group when the desktop is unlocked, then targeted public copies for backfile gaps. There is no automated polling or author contact. Earlier Kubásek Table 3, Hawaz manuscript, Grahn proof and Mahmoudi DOI qualifications still apply.

## Roles and structural review

Codex parent selected and integrated the tranche, operated the final collection readers, verified assets and updated registers. Bounded gpt-5.6-luna executors/scouts checked metadata, public routes and file QA; their claims were reconciled against actual files. The Caltech author route changed one preview-only outcome to a held text. Parent verification caught the omissions and scan/text distinction above. Source availability remains separate from scientific interpretation. Existing CSV, manifest and two ledgers support the next investigation; no new data structure or scientific assumption was adopted.

## Main-text index

| CSV ID | File under `library/closed/` | PDF pages |
|---|---|---:|
| burd2016 | burd2016_wiley.pdf | 16 |
| klaus2017 | klaus2017_wiley.pdf | 12 |
| hopkins1976 | hopkins1976_wiley.pdf | 8 |
| al1985b | al1985b_wiley.pdf | 8 |
| al1985 | al1985_wiley.pdf | 6 |
| al2007b | al2007b_wiley.pdf | 10 |
| al2010b | al2010b_wiley.pdf | 17 |
| al2013c | al2013c_wiley.pdf | 12 |
| al2013g | al2013g_wiley.pdf | 13 |
| al2013h | al2013h_wiley.pdf | 8 |
| al2018b | al2018b_wiley.pdf | 19 |
| al2018c | al2018c_wiley.pdf | 13 |
| al2019b | al2019b_wiley.pdf | 9 |
| beerling2009 | beerling2009_wiley.pdf | 10 |
| dolan2016 | dolan2016_wiley.pdf | 7 |
| duckett2019 | duckett2019_wiley.pdf | 11 |
| edwards1969 | edwards1969_wiley.pdf | 13 |
| hemsley1994 | hemsley1994_wiley.pdf | 13 |
| kenrick1994 | kenrick1994_wiley.pdf | 38 |
| kutschera2009 | kutschera2009_wiley.pdf | 15 |
| runions2012 | runions2012_wiley.pdf | 21 |
| strother2015b | strother2015b_wiley.pdf | 27 |
| taylor2007 | taylor2007_wiley.pdf | 14 |
| trewin2003 | trewin2003_wiley.pdf | 43 |
| winther2008 | winther2008_wiley.pdf | 12 |
| xue2009 | xue2009_wiley.pdf | 9 |
| xue2011 | xue2011_wiley.pdf | 12 |
| yoshida2010 | yoshida2010_wiley.pdf | 7 |
| edwards2014-open | edwards2014-open_wiley.pdf | 29 |
| edwards2021-open | edwards2021-open_wiley.pdf | 16 |
| edwards2021-open2 | edwards2021-open2_wiley.pdf | 10 |
| wilson2011 | wilson2011_wiley.pdf | 10 |
| al2012h | al2012h_wiley.pdf | 29 |
| toledo2021 | toledo2021_wiley.pdf | 14 |
| al1979 | al1979_scup.pdf | 12 |
| gray1985 | gray1985_scup.pdf | 20 |
| meyerberthaud2013 | meyerberthaud2013_scup.pdf | 11 |
| cascalesmiana2014 | cascalesmiana2014_scup.pdf | 16 |
| al2011j | ghavidelsyooki2011_caltech.pdf | 22 |
