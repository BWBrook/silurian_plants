# Autonomous literature expansion, 29 October 2026

Barry authorised autonomous selection and collection beyond the previous fixed batches (chat, 29 October 2026). This checkpoint records 46 newly secured main texts, 25 supporting files and one erratum: 72 assets, 412,482,009 bytes and 918 PDF pages, of which 854 belong to the main texts. Copyrighted files remain in git-ignored `library/closed/`; the register and receipt contain their provenance and SHA-256 values.

## Selection and delivery

The run reconciled needed CSV rows against existing holdings and then used the routes already shown to work. Seventeen modern Elsevier papers were delivered through UTAS, with in-app article and supporting-link inspection followed by Chrome native PDF save. Ten further Taylor & Francis papers downloaded through the authenticated in-app reader. Seven priority-one papers used Nature, Wiley or Oxford delivery. Twelve main texts came from public author/repository/publisher routes; those are retained separately from institutional access in the register. These counts sum to 46 main texts, including Hueber 2001, which was added after the 45-paper checkpoint.

There are 36 original publisher deliveries, eight publisher-layout author/reprint copies, one accepted manuscript and one publisher proof. Public availability is not evidence of an open reuse licence. All eight ResearchGate records used here were downloaded without sign-in; seven are publisher-layout copies and the eighth is the Grahn proof. White Rose supplied the Hawaz accepted manuscript. AJS's Save article as PDF action downloaded the two original journal PDFs; an initial download-event timeout was not a failure, because completed files were subsequently found and verified in Downloads.

Hueber 2001's public reprint was visible to the search service but its browser viewer remained blank. A standalone public HTTP retrieval of that exact URL succeeded, without browser cookies or credentials. The four Ibarra code/data files were likewise fetched from the exact links in the Yale directory cited by the paper. That R source was inspected as a file and was not executed.

## Material source and version qualifications

- **Kubásek 2021:** the linked erratum, DOI 10.1111/nph.17473, supplies replacement Table 3 because the original Table 3 duplicated Table 2. Both texts and the 16-page supporting figures are held. Later extraction must use the correction; no model/card values were changed here.
- **Hawaz:** White Rose explicitly labels the 55-page file an accepted manuscript. The published article spans pages 31–56. Manuscript page count and journal pagination describe different formats.
- **Grahn:** the complete 18-page copy is an early publisher proof labelled 2011 with `xxx` pagination. Crossref gives final publication in 2013, volume 198, pages 27–44. This is usable full text with a version qualification; the final publisher PDF remains unheld.
- **Mahmoudi:** the first-page title, four authors, Geopersia 4(2), 2014 and pages 125–140 establish article identity. The supplied DOI returns Crossref 404 and remains unverified. No replacement DOI was inferred.
- **Kenrick:** the Wiley filename says 2003, but the primary text and journal pagination establish the 1999 paper. File naming is not publication-year evidence.
- **Edwards 1992:** the first PDF page begins with the end of a preceding Nature letter, followed by the correct target title/authors. All three target pages, 683–685, are present.
- **Cascales 2016:** the main paper now completes the gap beside two supplements already held in `data/external/local/deposits/cascales2016-ordovician-mississippian/`. Those old supplements were not counted as newly acquired.
- Several harvest IDs retain online-first years; citations now use Crossref's printed issue year. The IDs remain stable. A search result misattributed a Czech thesis to both Mahmoudi and Spina; direct record inspection disproved the attribution, and the thesis was excluded. The two actual articles were recovered by other routes.

## Verification and limits

Independent `gpt-5.6-luna` executors supplied metadata reconnaissance and PDF QA; the Codex desktop parent selected routes, operated authenticated browsers, resolved identity exceptions and integrated the records. Crossref identity was checked for all main works except the explicitly unresolved Mahmoudi DOI. File signatures, extent, extraction, original-byte hashes and PDF structure were checked. All 854 main-text PDF pages contain extractable text. Endpoint renders were checked; minor qpdf hint-table/name-tree warnings were recorded, and original files were retained. Supporting archives, XML, media, text data and OOXML files passed format checks. The machine-readable receipt preserves per-file results and the all-page extraction counts.

The earlier ten request candidates were left parked. New route failures are recorded with their observed scope in `docs/barry-to-action.md`; they do not establish that no copy exists. The Mac locked once; Barry unlocked it while in-app acquisitions continued. A stale PDF asset briefly offered an HTML download; that save was cancelled, and a fresh publisher route supplied the actual PDF. Native tab cleanup stalled twice; the browser-management API subsequently verified and removed the remaining owned residue. No credentials, personal details, requests, purchases or outside messages were submitted.

This is source acquisition, not scientific adjudication. No occurrence units, timescales, cards or model inputs changed. Q1/Q2/Q5 readings and duplicate-study decisions remain with the scientific synthesis.

Downloads cleanup moved 46 byte-matching staging files (234,761,635 bytes) into the recoverable Bin folder `/Users/bwbrook/.Trash/silurian-literature-20261029-autonomous-checkpoint1`. Every destination hash was checked; archive copies were retained and the Bin was not emptied. Other active work’s downloads were left alone.

## Main-text file index

| CSV ID | PDF in `library/closed/` | PDF pages |
|---|---|---:|
| al2014g | xu2014_westjunggar.pdf | 13 |
| al2020d | garciamuro2021_tacobo.pdf | 20 |
| al2025 | lima2025_riodopeixe.pdf | 12 |
| cascales2016 | cascales2016.pdf | 9 |
| morris2014 | morris2014.pdf | 27 |
| bonacorsi2020 | bonacorsi2020.pdf | 2 |
| conway2020 | conway2020.pdf | 10 |
| al2015b | field2016_huperzioideae.pdf | 23 |
| al2015c | trotter2016_silurian.pdf | 15 |
| al2018e | xue2018_southchina.pdf | 34 |
| al2020b | xu2020_leclercqia.pdf | 9 |
| al2021c | edwards2022_mesofossils.pdf | 32 |
| al2023 | liu2024_aberlemnia.pdf | 11 |
| arens2021 | dahl2021_reply.pdf | 2 |
| retallack2022 | retallack2022.pdf | 13 |
| rose2019 | rose2019_ireviken.pdf | 18 |
| wilson2016 | wilson2016.pdf | 12 |
| wellman2017 | abuhmida2017_hawaz.pdf | 55 |
| al2014d | mahmoudi2014_ghelli.pdf | 16 |
| al2017d | strother2017_thalli.pdf | 13 |
| gerrienne2006 | gerrienne2006.pdf | 8 |
| lenton2012 | lenton2012.pdf | 4 |
| strother2008 | beck2008_allenport.pdf | 27 |
| al2010h | strulluderrien2010.pdf | 14 |
| al2011k | grahn2013_apucarana.pdf | 18 |
| al2014b | cascales2015_mezquita.pdf | 10 |
| al2019c | ibarra2019_weathering.pdf | 43 |
| al2020c | ludman2020_maine.pdf | 33 |
| higgs2022 | higgs2022.pdf | 24 |
| spina2014 | spina2015_hirnantian.pdf | 16 |
| al2015d | cascales2016_nogueras.pdf | 8 |
| al2026e | rubinstein2026_puna.pdf | 25 |
| ghavidelsyooki2025 | ghavidelsyooki2025.pdf | 59 |
| al2017b | daners2017_cordobes.pdf | 18 |
| libertin2022 | libertin2023_bohemica.pdf | 12 |
| al2020 | mcsweeney2020.pdf | 19 |
| al2021f | mcsweeney2021_yarravia.pdf | 17 |
| al2021g | mcsweeney2021_alexandra.pdf | 15 |
| al2011m | tian2011_qujing.pdf | 10 |
| edwards1992 | edwards1992_cooksonia.pdf | 3 |
| edwardsds1986 | edwards1986_aglaophyton.pdf | 32 |
| hueber1983 | hueber1983_baragwanathia.pdf | 23 |
| kenrick1999 | kenrick1999.pdf | 12 |
| kubasek2021 | kubasek2021.pdf | 14 |
| renault1992 | renault1992_polytrichum.pdf | 8 |
| hueber2001 | hueber2001.pdf | 36 |
