# MacBook literature return integrated on mini, 30 October 2026

Barry and his counterpart Codex agent worked through the 48-row access queue on the
MacBook. Barry requested integration of the entire folder and said: “The outstanding
items are just going to have to be flagged as unobtainable.” This closes the acquisition
round; it does not declare the scientific source gaps resolved.

## Result

- 35 exact focal main-text gaps closed; one complete intended conference abstract
  (Wellman 2026) closed separately.
- Twelve remain unobtainable: four Tier 1, eight Tier 2. Ten exact sources remain
  unheld; two have partial holdings (the composite Zalesie/Masiak row and Canning
  Part One). Their citations, remaining requirements, authority and retained components
  are in `docs/unobtainable-literature.csv`.
- The full 135-row focused register now has 117 rows with main texts (105 main-held
  and twelve already-held), five complete abstracts, one data archive and twelve
  unobtainable rows. The original input priorities are unchanged. The main-text count
  includes the earlier Lang/Cookson alias; it is not 117 unique newly acquired works.
- All 42 returned PDFs are filed/indexed. They comprise 35 exact main texts, one exact
  abstract, the complete Trela component of the still-incomplete combined row, and
  five additional/related/supporting assets: Ghavidel-Syooki 2000, a duplicate Mehlqvist
  2012 article, a Masiak component copy, Abuhmida's 2013 thesis and the EPPC abstract book.
  Only Mehlqvist is byte-identical to a previously registered local file; none of these
  five additional assets is counted as another focal closure.

## Complete-folder transfer and retained evidence

The complete MacBook folder `/Users/bwbrook/input/silurian-plants-literature-2026-10-30/`
was pulled through the configured `macbook` SSH alias. All **982 files / 616,180,427 bytes**,
including intake, results, acquired PDFs, QA images, original snapshots and ancillary
list packs, match an independently generated source path/size/SHA-256 inventory, with
no missing, extra or mismatched files. The unchanged complete copy is retained at
`library/closed/_incoming/macbook-2026-10-30/` (git-ignored). New reading copies use
`library/closed/<source-id>_macbook20261030.pdf`; original bytes were preserved. Neither
MacBook sources nor Downloads were removed. The original reduced HTML is also archived
as `docs/audits/2026-10-30-macbook-reduced-list.html`.

`work/codex/literature/2026-10-30-macbook-return.json` retains the transfer inventory,
per-file source manifest, local QA, outcome history and independent reconciliation.
`library/closed.tsv` adds 42 provenance entries; some original serving URLs were not
recorded by the supplying session. Those are explicitly Barry-provided copies with an
unknown original serving route; DOI/catalogue URLs are identity locators, not invented
retrieval evidence. Supplied deep-research archive routes remain attributed to their
supplier. All PDFs, full-text extracts, original archive material and QA renders stay
ignored and uncommitted. Scientific interpretation/extraction was not performed.

## Verification and bibliographic qualifications

Independent mini QA recomputed all 42 byte counts, hashes and page counts, checked
pdfinfo/qpdf/text extraction, rendered first/last pages for all PDFs and ten additional
source/plate pages. Twenty-eight PDFs pass qpdf cleanly; fourteen retain warning-only
source structure/hint issues. No original was repaired or re-encoded. First/last,
plate/appendix and target-section evidence is retained. The independent mapping audit
reconciles all 48 initial source IDs against the twelve-row reduced list.

The repository DOI checker passed all 31 distinct acquired DOI references. Three
remaining DOIs also resolve in official Crossref metadata. Its author-name checker
flags the registered `Quintvalle` spelling (the actual first-page PDF says Quintavalle)
and the registered family field `K.T. Higgs`; these are documented metadata/format
mismatches, not failed DOI identities. Correct source citations are retained. The
Higgs original journal DOI 10.3318/ijes.2014.32.55 replaces the earlier MUSE delivery
alias 10.1353/ijes.2014.0001, with both preserved in provenance. Its printed pp.55–70
and three authors are carried from the supplied original-first-page verification;
Crossref's page field says50, so that metadata discrepancy remains explicit.

- **Garratt 1978:** complete nine-page PDF including publisher front matter, target
  printed pp.217–224. It is now held in full; prior map/later-paper surrogates stay
  separate. No Yea-age adjudication is changed merely by obtaining it.
- **Tims 1980:** complete 313-leaf repository OCR scan, title leaf gives the 1980
  unpublished PhD. Numbered body runs 1–232 with preliminary/errata/interleaved plate
  leaves and final chart; the old 233-page citation is retained as a pagination caveat.
- **Balme 1961:** target printed pp.22–26 verified at PDF pp.26–30 inside a 43-page
  PSSA5 report. The closure is for the target section, not a scientific audit of the volume.
- **Zalesie dating:** Trela & Szczepanik 2009 is complete, eleven pages (147–157).
  Both Masiak copies show printed pp.311–329; the header/issue cites pp.311–330 and physical
  p.330 remains unverified. The combined row is therefore retained as an unobtainable
  remainder with components, rather than marked fully held. This may be a pagination
  discrepancy, but acquisition has not established that explanation.
- **Canning:** Part One has one page of88 and twelve advertised plates remain unheld;
  Part Two is a separate 89–131 paper. Stable IDs retain their historical spelling.
- **Distinct related works:** Ghavidel-Syooki 2000 does not replace the requested 2001
  proceedings chapter; Mehlqvist 2012 does not replace the full 2013 doctoral thesis;
  the complete 641-page Abuhmida (2013) thesis does not reproduce the exact 2011 abstract.
- **Versions:** `al2016h` is a complete Just-IN accepted manuscript, not version of record;
  Gonez2010a is a publisher-layout proof; Academia reproductions and public scans retain
  their declared versions. Vecoli/Césari2019 is an SPE conference manuscript, not a
  peer-reviewed journal article. Wellman (2026) is a complete one-page official abstract,
  matched to printed p.117/PDF p.118 of the supporting abstract book.

## Remaining twelve

“Unobtainable” is Barry's current-study access disposition after the completed round.
It removes these entries from automatic retry/action queues while keeping scientific
gaps and partial/related holdings visible. Reopening would be a new Barry decision.

| ID / tier | Source | Held / missing |
|---|---|---|
| `zalesie-dating` / 1 | Masiak, M., Podhalańska, T., and Stempień-Sałek, M. (2003). Ordovician–Silurian boundary in the Bardo Syncline, Holy Cross Mountains, Poland — new data on fossil assemblages and sedimentary succession. Geological Quarterly 47(4): 311–330 as cited in the article header and official issue record; observed publisher PDF contains printed pp. 311–329. | Partial/related files retained. No authoritative physical/full-issue scan of page 330 was obtained. Whether 330 is blank, contains omitted material, or results from pagination/citation practice remains unverified. Keep the composite dossier row partial. The Trela and Szczepanik (2009) companion is already complete in the user’s holdings and was not downloaded again. |
| `ghavidelsyooki2001` / 1 | Ghavidel-Syooki, M. (2001). Palynostratigraphy and palaeobiogeography of the Lower Palaeozoic sequence in the Northeastern Alborz Range (Kopet–Dagh Region) of Iran. In D. K. Goodman & R. T. Clarke (eds), Proceedings of the IX International Palynological Congress, Houston, Texas, U.S.A., 1996, pp. 17–35. American Association of Stratigraphic Palynologists Foundation. | Partial/related files retained. No complete public electronic copy found. A concrete publisher route now exists for the complete physical proceedings; purchasing was not undertaken. |
| `mehlqvist2013` / 1 | Mehlqvist, Kristina (2013). Early land plant spores from the Paleozoic of Sweden – taxonomy, stratigraphy and paleoenvironments. Doctoral compilation thesis, Department of Geology, Lund University. Litholund Theses 23. 106 pp. ISBN 978-91-86746-95-7. | Partial/related files retained. Exact thesis metadata is accessible, but the checked Lund records expose no full-thesis file, and no legitimate public mirror was located. |
| `abuhmida2011` / 1 | Abuhmida, Faisal Hadi (2011). Ordovician-Lower Silurian palynology of the Murzuq Basin, southwest Libya. Abstract, 44th Annual Meeting of AASP–The Palynological Society, Southampton, UK, 4–7 September 2011. Original pagination unverified. | Partial/related files retained. The original contribution page currently returns an access error, and the exact abstract page was not found among available Wayback captures. The indexed abstract is useful but cannot close the exact-source completeness requirement without inspecting the original abstract or proceedings. |
| `richardson1988` / 2 | Richardson, J. B. (1988). Late Ordovician and Early Silurian cryptospores and miospores from northeast Libya. In A. El-Arnauti, B. Owens & B. Thusu (eds), Subsurface Palynostratigraphy of Northeast Libya, pp. 89–109. Garyounis University Press, Benghazi, Libya. | No public complete chapter or parent-book scan located. Exact paper remains a physical-library/document-delivery requirement. |
| `quintavalle2006` / 2 | Quintavalle, M. & Playford, G. (2006). Palynostratigraphy of Ordovician strata, Canning Basin, Western Australia. Part Two: chitinozoans and biostratigraphy. Palaeontographica Abteilung B 275(4–6): 89–131. https://doi.org/10.1127/palb/275/2006/89 | Publisher preview only; no complete legitimate public copy located. Live UQ repository access is currently hindered by human verification; archives do not expose a full file. |
| `quintvalle2006` / 2 | Quintavalle, M. & Playford, G. (2006). Palynostratigraphy of Ordovician strata, Canning Basin, Western Australia. Part One: acritarchs and prasinophytes. Palaeontographica Abteilung B 275(1–3): 1–88. https://doi.org/10.1127/palb/275/2006/1 | Partial/related files retained. Publisher preview only; no complete legitimate public copy located. Live UQ repository access is currently hindered by human verification; archives do not expose a full file. |
| `vecoli1999` / 2 | Vecoli, M. (1999). Cambro-Ordovician palynostratigraphy (acritarchs and prasinophytes) of the Hassi-R’Mel area and northern Rhadames Basin, North Africa. Palaeontographia Italica 86: 1–112. | No full monograph located. The journal society exposes indexes/abstracts, UNICA has no attached file, and live UQ access was blocked by human verification in this browser. Archived UQ record was only an application shell without attached files. |
| `edwardsedwards1986` / 2 | Edwards, Dianne & Edwards, D. S. (1986). A reconsideration of the Rhyniophytina Banks. In: Spicer, R. A. & Thomas, B. A. (eds), Systematic and Taxonomic Approaches in Palaeobotany: Proceedings of an International Symposium held at Goldsmiths’ College, London, April 1985. Systematics Association Special Volume 31. Oxford: Clarendon Press. pp. 199–220. ISBN 0-19-857704-4. | The exact author-repository record and parent-volume catalogue are accessible, but neither supplies chapter full text; no legitimate public scan was located. |
| `kenrick1997book` / 2 | Kenrick, Paul & Crane, Peter R. (1997). The Origin and Early Diversification of Land Plants: A Cladistic Study. Smithsonian Series in Comparative Evolutionary Biology. Washington, DC and London: Smithsonian Institution Press. Catalogued as xi + 441 pp.; preliminary extent varies in secondary records. | An exact digitization exists at Internet Archive, but access is restricted. Google Books offers snippets, and no unrestricted complete institutional/author copy was located. |
| `garratt1988` / 2 | Garratt, M. J. & Wright, A. J. (1988). Late Silurian to Early Devonian Biostratigraphy of Southeastern Australia. In McMillan, N. J., Embry, A. F. & Glass, D. J. (eds), Devonian of the World: Proceedings of the 2nd International Symposium on the Devonian System, Memoir 14, Volume III: Paleontology, Paleoecology and Biostratigraphy, pp. 647–662. Canadian Society of Petroleum Geologists. | Publisher browser page explicitly states Full Text (subscription required); purchase options shown. No open author or repository copy located. No purchase, login or contact submitted. |
| `al2014c` / 2 | Higgs, K. T., Boyd, J. D. & Williams, B. P. J. (2014). An early Devonian age for the Bulls Head Formation, Lower Old Red Sandstone, Dingle Peninsula. Irish Journal of Earth Sciences 32: 55–70. https://doi.org/10.3318/IJES.2014.32.55 | JSTOR displays first-page preview; Read and download requires school/library login; Free online reading is advertised separately. MUSE blocked current browser with repeated Friendly Captcha verification page. ResearchGate is request-only. No complete source obtained. |

## Reading index of returned files

| Source ID | PDF pages | File / role |
|---|---:|---|
| `rubinstein2016` | 12 | [rubinstein2016_macbook20261030.pdf](../../library/closed/rubinstein2016_macbook20261030.pdf) — original publisher PDF |
| `strother2016` | 14 | [strother2016_macbook20261030.pdf](../../library/closed/strother2016_macbook20261030.pdf) — original publisher PDF |
| `wang2022` | 14 | [wang2022_macbook20261030.pdf](../../library/closed/wang2022_macbook20261030.pdf) — original publisher PDF |
| `al2018d` | 42 | [al2018d_macbook20261030.pdf](../../library/closed/al2018d_macbook20261030.pdf) — original publisher PDF |
| `edwardsrichardson2004` | 28 | [edwardsrichardson2004_macbook20261030.pdf](../../library/closed/edwardsrichardson2004_macbook20261030.pdf) — original publisher PDF |
| `zalesie-dating` | 11 | [zalesie-dating_macbook20261030.pdf](../../library/closed/zalesie-dating_macbook20261030.pdf) — original publisher PDF |
| `hoffmeister1959` | 5 | [hoffmeister1959_macbook20261030.pdf](../../library/closed/hoffmeister1959_macbook20261030.pdf) — publisher scan/PDF served by JSTOR, including cover |
| `ottone1999` | 27 | [ottone1999_macbook20261030.pdf](../../library/closed/ottone1999_macbook20261030.pdf) — publisher scan/PDF served by JSTOR, including cover |
| `gonez2010a` | 17 | [gonez2010a_macbook20261030.pdf](../../library/closed/gonez2010a_macbook20261030.pdf) — author-uploaded publisher-layout proof |
| `lakova1992` | 20 | [lakova1992_macbook20261030.pdf](../../library/closed/lakova1992_macbook20261030.pdf) — publisher scan with OCR text layer |
| `al2012c` | 30 | [al2012c_macbook20261030.pdf](../../library/closed/al2012c_macbook20261030.pdf) — author-uploaded publisher-layout reproduction (Ghostscript-derived PDF) |
| `al2011f` | 31 | [al2011f_macbook20261030.pdf](../../library/closed/al2011f_macbook20261030.pdf) — author-uploaded publisher-layout reproduction (Ghostscript-derived PDF) |
| `morris2012` | 30 | [morris2012_macbook20261030.pdf](../../library/closed/morris2012_macbook20261030.pdf) — author-uploaded publisher-layout reproduction with Elsevier author-personal-copy cover (Ghostscript-derived PDF) |
| `eggert1974` | 10 | [eggert1974_macbook20261030.pdf](../../library/closed/eggert1974_macbook20261030.pdf) — publisher scan/PDF served by JSTOR, including cover |
| `earp2024-open` | 31 | [earp2024-open_macbook20261030.pdf](../../library/closed/earp2024-open_macbook20261030.pdf) — original publisher PDF |
| `cardona2016` | 16 | [cardona2016_macbook20261030.pdf](../../library/closed/cardona2016_macbook20261030.pdf) — original publisher PDF |
| `tims1980` | 313 | [tims1980_macbook20261030.pdf](../../library/closed/tims1980_macbook20261030.pdf) — Minerva repository OCRscan of PhDthesis |
| `balme1961` | 43 | [balme1961_macbook20261030.pdf](../../library/closed/balme1961_macbook20261030.pdf) — scanned1961report with text/OCR layer; targetsection embedded |
| `edwards2001-open` | 18 | [edwards2001-open_macbook20261030.pdf](../../library/closed/edwards2001-open_macbook20261030.pdf) — publisher-layout PDF; original retrieval route unrecorded |
| `ghavidelsyooki2007` | 20 | [ghavidelsyooki2007_macbook20261030.pdf](../../library/closed/ghavidelsyooki2007_macbook20261030.pdf) — publisher-layout PDF; original retrieval route unrecorded |
| `ghavidelsyooki2008a` | 18 | [ghavidelsyooki2008a_macbook20261030.pdf](../../library/closed/ghavidelsyooki2008a_macbook20261030.pdf) — publisher-layout PDF; original retrieval route unrecorded |
| `ghavidelsyooki2000-context` | 14 | [ghavidelsyooki2000-context_macbook20261030.pdf](../../library/closed/ghavidelsyooki2000-context_macbook20261030.pdf) — publisher-layout PDF; original retrieval route unrecorded |
| `ghavidelsyooki2006` | 15 | [ghavidelsyooki2006_macbook20261030.pdf](../../library/closed/ghavidelsyooki2006_macbook20261030.pdf) — publisher-layout PDF; original retrieval route unrecorded |
| `mehlqvist2012-duplicate-wsl` | 12 | [mehlqvist2012-duplicate-wsl_macbook20261030.pdf](../../library/closed/mehlqvist2012-duplicate-wsl_macbook20261030.pdf) — byte-identical duplicate of already-held2012publisher-layout reproduction |
| `al2023b` | 16 | [al2023b_macbook20261030.pdf](../../library/closed/al2023b_macbook20261030.pdf) — publisher-layout PDF served with BioOnecover |
| `rubinstein2011` | 15 | [rubinstein2011_macbook20261030.pdf](../../library/closed/rubinstein2011_macbook20261030.pdf) — publisher-layout PDF; original retrieval route unrecorded |
| `al2011n` | 18 | [al2011n_macbook20261030.pdf](../../library/closed/al2011n_macbook20261030.pdf) — publisher-layout PDF; original retrieval route unrecorded |
| `zalesie-dating-masiak2003-wsl` | 19 | [zalesie-dating-masiak2003-wsl_macbook20261030.pdf](../../library/closed/zalesie-dating-masiak2003-wsl_macbook20261030.pdf) — publisher-layout component, printed pp.311–329; cited330unverified |
| `al2016h` | 28 | [al2016h_macbook20261030.pdf](../../library/closed/al2016h_macbook20261030.pdf) — Just-IN accepted manuscript, before copy-editing and page composition; not version of record |
| `careybolger1995` | 16 | [careybolger1995_macbook20261030.pdf](../../library/closed/careybolger1995_macbook20261030.pdf) — Taylor & Francis scanned article with download/terms front matter; serving route unknown |
| `garratt1978` | 9 | [garratt1978_macbook20261030.pdf](../../library/closed/garratt1978_macbook20261030.pdf) — Taylor & Francis scanned article with download/terms front matter; serving route unknown |
| `glasspool2006` | 6 | [glasspool2006_macbook20261030.pdf](../../library/closed/glasspool2006_macbook20261030.pdf) — Elsevier publisher-layout PDF; serving route unknown |
| `gonez2010b` | 9 | [gonez2010b_macbook20261030.pdf](../../library/closed/gonez2010b_macbook20261030.pdf) — Elsevier publisher-layout PDF; serving route unknown |
| `marshall1990` | 10 | [marshall1990_macbook20261030.pdf](../../library/closed/marshall1990_macbook20261030.pdf) — User-provided publisher-layout PDF; original serving URL unrecorded |
| `marshall1997` | 9 | [marshall1997_macbook20261030.pdf](../../library/closed/marshall1997_macbook20261030.pdf) — User-provided publisher-layout PDF; original serving URL unrecorded |
| `al1996` | 42 | [al1996_macbook20261030.pdf](../../library/closed/al1996_macbook20261030.pdf) — User-provided publisher-layout PDF; original serving URL unrecorded |
| `cesari2019` | 8 | [cesari2019_macbook20261030.pdf](../../library/closed/cesari2019_macbook20261030.pdf) — Society of Petroleum Engineers conference manuscript/presentation paper, not a peer-reviewed final journal article |
| `delapuente2013` | 20 | [delapuente2013_macbook20261030.pdf](../../library/closed/delapuente2013_macbook20261030.pdf) — Publisher-layout PDF deposited in CONICET; retrieved unchanged from an archived public repository capture |
| `snigirevskaya1992` | 12 | [snigirevskaya1992_macbook20261030.pdf](../../library/closed/snigirevskaya1992_macbook20261030.pdf) — Published Russian article scan uploaded by coauthor; original scan preserved without alteration |
| `wellman2026` | 1 | [wellman2026_macbook20261030.pdf](../../library/closed/wellman2026_macbook20261030.pdf) — Official conference-generated contribution PDF, unchanged |
| `abuhmida2013-thesis-related` | 641 | [abuhmida2013-thesis-related_macbook20261030.pdf](../../library/closed/abuhmida2013-thesis-related_macbook20261030.pdf) — Complete official final thesis as supplied; repository/archive provenance reported by acquisition agent; originalbytes unchanged |
| `eppc2026-abstract-book-supporting` | 131 | [eppc2026-abstract-book-supporting_macbook20261030.pdf](../../library/closed/eppc2026-abstract-book-supporting_macbook20261030.pdf) — Official conference abstract-book PDF as supplied; original bytes unchanged |
