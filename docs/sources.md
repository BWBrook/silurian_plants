# Evidence base: source register

The index of the data the project holds and the data it still needs, for the window 485–383 Ma,
with Frasnian–Famennian anchors where noted, and Cambrian palynological effort as the control on
spore first appearances (from 2026-10-28). Status as of 2026-10-27, after EPRP tranche 2. Update
this file whenever a source is added, extracted or ruled out. A gap that bears on a question names its ID
in `docs/questions.md`.

Status values:
- **held**: in the repository, committed;
- **local**: on mac-mini in a git-ignored `local/` or `library/` folder because of licence or size;
- **limited**: access blocked or on request;
- **missing**: not yet sourced;
- **ruled out**: checked and unusable, with the reason given.

Provenance: `data/eprp/` holds material from Barry's EPRP mirror; `data/external/` holds material
acquired from outside EPRP. Both came from the EPRP Mac-Mini session. Each area README gives
filters, licences and caveats; read it before use. Raw pulls before 2026-10-28 are on `deep` (`deep-server`) under
`/data/codex/silurian_plants/raw/` (4.9 GB), which the Macs cannot reach. The EPRP mirror backup,
`nectar:/data/codex/artifacts/eprp-paleodata-backup/latest/<id>/`, is the canonical location for EPRP
data files until Barry says otherwise (`AGENTS.md`); check individual snapshots before use. The EPRP
extraction scripts read it directly, and their re-runs on 2026-10-29 reproduced the committed tables.
New raw pulls and rebuilds go to `nectar:/data/codex/silurian_plants/raw/`. The `local/` folders hold
2.5 GB on mac-mini.

The private backup workflow targets `nectar:/data/codex/silurian_plants/backups/mac-mini/`
and includes git-ignored material. See `docs/backup-nectar.md` and the verification receipts before
relying on a particular generation.

## 1. Fossil occurrences

| Source | What it gives | Status | Where | Licence |
|---|---|---|---|---|
| PBDB plant occurrences, collections, references | 3,704 occurrences (2,628 core), 1,302 collections; snapshot 2026-10-23 | held | `data/eprp/record/` | CC0 |
| PBDB anchors, Frasnian–Famennian | 163 occurrences (*Archaeopteris*, *Callixylon*, *Eospermatopteris*, *Elkinsia*) | held | `data/eprp/record/` | CC0 |
| PBDB taxa and opinions | window subsets (413 taxa, 653 opinions) tracked; whole plant tree local | held / local | `data/eprp/record/`, `data/eprp/local/record/` | CC0 |
| PBDB specimens and measurements | none links to a window plant occurrence: plant sizes must come from the literature | held (as a negative result) | `data/eprp/record/` | CC0 |
| Palynodata 2006 | 109,687 window rows to 600 Ma on Palynodata's timescale, widened 2026-10-28 to take in the Cambrian and Tremadoc-only documents (14,629 spore, 69,483 acritarch, 17,254 chitinozoan) from 3,540 documents; literature to 2006, 2006-era ages, no coordinates | held | `data/external/spores/` | OGL-Canada |
| Wellman, Steemans & Vecoli 2013 supplement | Ordovician–Silurian spore assemblages (abridged PDF) | held | `data/external/spores/` | CC BY 4.0; full database on request (Barry's decision) |
| Loop 1 occurrence tail (`data/occurrences/`) | observations, competing interpretations and sources for the oldest records of E1–E5 (229 observations, 324 readings), and an effort layer | held | `data/occurrences/` | derived; see its README |
| PBDB collections, all taxa, Darriwilian–Emsian | 27,830 collections, the effort layer for body fossils; snapshot 2026-10-28 | local (raw) | `data/occurrences/raw/` (git-ignored) | CC0 |
| Project spore dataset (MVD-A) | occurrences, vetted first appearances and stage presence from Palynodata plus Wellman 2013 | held | `data/spores/` | derived; see its README |
| M2 sampling-unit interface pilot (Q1, Q2) | 15 material blocks, 90 E1/E2-by-reading outcomes; five candidate frames and 75 inventory rows (14 Hanadir, 27 Pelmis, 34 Borenshult). Hanadir 190.7 m now carries a primary study-scoped E1 negative with exact specimen linkage. Complete analysis denominator still unavailable | held | `data/units/`; validate with `tools/units.py check` | derived observations and paraphrases; source files remain local |
| Steemans & Pereira 2002; Grahn et al. 2000 (Q1, Q2) | Miospore and companion chitinozoan studies of shared Paraguay borehole material; Palynodata 21733 and 20806. Eight observation-linked depths extracted; the stated 53-sample denominator cannot yet be reconstructed from their range charts | local | `library/open/steemanspereira2002.pdf`, `library/open/grahn2000.pdf`; URLs and hashes in `library/open.tsv` and `data/units/source_files.csv` | Public copies; no reuse licence assessed; full texts not committed |
| Post-2006 spore literature | 182 priority papers; 33 open full texts extracted (370 assemblages, 97% of records verified in text; two texts fetched into `library/open/`); other papers remain to be obtained or extracted | partly held | `data/spores/sources/mvdb_*.csv` | access varies; see `docs/closed-literature.csv` |
| Rubinstein et al. 2010 (Q1, Q2) | Paper and original supporting document, including stratigraphy and colour plate; acquired 2026-10-28, not yet incorporated in MVD-B or the occurrence adjudication. The supplement's plain-text extract `library/open/W1820528062_SI.txt` omits its four figures; use the original document for them | local | `library/open/W1820528062.pdf`, `library/open/W1820528062_SI.doc`; URLs and hashes in `library/open.tsv` | Publisher labels article Free Access; Crossref records Wiley terms, not a CC licence; keep local |
| Pivotal literature for Q1 and Q2 | Eight requested full papers, including Edwards et al. 2007, Edwards & Davies 1976, Rickards 2000, Salamon 2018 and Strother et al. 2015; original supplements for Salamon 2018 and Strother & Foster 2021. Acquired 2026-10-28 for the next source recheck; acquisition does not itself revise the occurrence adjudication | local | `library/closed/`; individual access routes and SHA-256 hashes in `library/closed.tsv` | Publisher and institutional copies; public availability does not by itself establish an open licence. Garratt 1978 remains unavailable in full; see `docs/closed-literature.csv` |
| Literature pilot, 28 October 2026 (Q1, Q2) | Full articles by Edwards & Feehan 1980, Libertín et al. 2018 and 2024, Taylor et al. 2017 and Kotyk et al. 2002; Libertín's 2018 supporting information was recovered from an earlier project scratch copy. Acquisition does not itself revise the scientific readings | local | `library/closed/edwardsfeehan1980.pdf`, `library/closed/libertin2018.pdf`, `library/closed/libertin2018_SI.pdf`, `library/closed/libertin2024.pdf`, `library/closed/taylor2017.pdf`, `library/open/W2112174729.pdf`; hashes and provenance in `library/closed.tsv` and `library/open.tsv`; unresolved routes in `docs/barry-to-action.md` | Institutional and public repository copies; the recovered supplement's original download route is unproven |
| Joint literature-access diagnosis, 29 October 2026 (Q1, Q2) | Kraft & Kvaček 2017, all 11 pages (180–190), Garratt & Rickards 1984, all 8 pages (377–384), and Garratt et al. 1984, all 4 pages (355–358); scientific re-reading pending | local | `library/closed/kraft2017.pdf`, `library/closed/garrattrickards1984.pdf`, `library/closed/garratt1984.pdf`; access routes and SHA-256 in `library/closed.tsv`; successful Chrome procedures in `docs/barry-to-action.md` | UTAS institutional copies; copyrighted texts remain git-ignored |
| Autonomous literature-access follow-up, 29 October 2026 (Q1, Q2) | Raevskaya et al. 2016, Tang et al. 2017 and Strother et al. 1996 publisher PDFs; Strother 2000 author preprint (23 pages; published chapter unheld). Strother 1996 sample/scope audit now recorded in data/units; other scientific re-reading pending | local | `library/closed/raevskaya2016.pdf`, `library/closed/tang2017.pdf`, `library/closed/strother1996.pdf`, `library/closed/strother2000_preprint.pdf`; hashes and versions in `library/closed.tsv`; `docs/audits/2026-10-29-literature-recovery.md` | Institutional and public author copies; keep copyrighted files local |
| Literature access queues and next-batch proposal, 29 October 2026 (Q1, Q2) | Ten request candidates parked separately; proposed six-paper UTAS/ScienceDirect tranche followed by two public author copies. No new texts acquired in this planning pass | planning | `docs/literature-requests.md`, `docs/literature-next-batch.md`; active blockers use `docs/barry-to-action.md` | Source versions and main-paper/supplement/abstract distinctions govern acquisition counts |
| Reconciled existing literature | Field et al. 2016 and Kidston & Lang 1921 Part IV were already held in the external-library harvest, despite being marked needed | local | `data/external/local/library/pdf/W2176407474.pdf`, `data/external/local/library/pdf/XU101.pdf`; original hashes and routes in `data/external/library/fetch_results.tsv` and `data/external/library/open_unread_results.tsv` | Field PDF states CC BY 4.0; Kidston access and reuse terms not assessed |
| Garratt 1978 context (Q1, Q2) | A 2008 public submission reproduces its geological map; Garratt 1983 gives a later primary account of the graptolites; Earp 2023 reviews the older evidence in detail. The full 1978 article remains needed, and the Earp review is an unreviewed first draft | local | `library/closed/jelinek2008_garratt1978_map.pdf` p. 12; `library/closed/garratt1983.pdf` p. 81; `library/closed/earp2023_yea_review_first_draft.pdf`; provenance in `library/closed.tsv` | Garratt 1983 is an article extract from the Biodiversity Heritage Library/Internet Archive scan, whose article record states CC BY-NC-SA 4.0; the other files have no assessed reuse licence |
| GBDB (Zenodo 2020) | 410 core window plant records (131 genera, mostly China), 3,217 window sections; GTS2012 ages | held | `data/external/gbdb/` | CC BY 4.0 |
| Diversity compilations | Xiong 2013, Silvestro 2015, Capel 2025 mirrored; Capel 2021, 2022, Cascales-Miñana 2016, Ball 2022 local; Capel 2023 limited | mixed | `data/external/deposits/` | per deposit |
| Fossil Record 2 plant families | Harland 1990 ages | local | `data/eprp/local/record/` | none stated |

## 2. Museum specimens

| Source | What it gives | Status | Where | Licence |
|---|---|---|---|---|
| GBIF, iDigBio, ALA (merged) | 39,417 open-licence rows, 26,102 physical specimens, duplicates linked; full iDigBio table local | held | `data/external/specimens/` | per record; open subset tracked |

GBIF files *Prototaxites* and the nematophytes under Fungi. Most Ordovician "Plantae" are
receptaculitid green algae, and these are flagged. There are no Museums Victoria *Baragwanathia*
among GBIF fossil specimens.

## 3. Names and taxonomy

| Source | Status | Notes |
|---|---|---|
| PBDB taxa and opinions | held | see §1 |
| International Fossil Plant Names Index; Plant Fossil Names Registry | ruled out for bulk use | no export, API or licence: manual lookups only |

## 4. Characters, traits and measurements

| Source | Status | Where |
|---|---|---|
| Card trait matrix (59 taxa) | held, draft | `data/traits.csv` |
| Clark et al. 2023 (548 × 410), Claisse et al. 2025, Hooper et al. 2026 spore matrix | held | `data/external/deposits/` |
| Kenrick & Crane 1997 matrix | ruled out | print only |
| Toledo et al. 2021 | limited | Wiley blocks the supplement |

## 5. Phylogenies and timetrees

| Source | Status | Where |
|---|---|---|
| Hooper et al. 2026 (MCMCTree files, calibrations); Morris et al. 2018 (alignments, calibrations); Harris et al. 2022 | held; Hooper input/publication discrepancy unresolved (Q9) | `data/external/deposits/`; large and licence-restricted files in git-ignored `data/external/local/deposits/` |

Hooper archive inspected by Codex, 2026-10-29: checksum matches its retrieval manifest; all 69 fossil calibrations specify 1% tails whereas the article states 2.5%. Using all 5,001 saved rows, the deposited crown-embryophyte posterior has mean 453.70 Ma and empirical 2.5–97.5% interval 450.05–457.36 Ma. The independently clade-matched output tree reports a 449.91–457.21 Ma HPD interval. These different interval definitions agree with the rounded publication summary but no run log or control-file hash links the outputs to the supplied settings. A second burn-in deletion in the preliminary extraction was corrected; the old 4,800-row result is a sensitivity only. Evidence, inventory and reproducible summaries are in `docs/audits/2026-10-29-q9-provenance-check.md` and `data/q9/hooper2026-provenance/`. Q9 remains unresolved.

Hooper ancestral-state outputs extracted separately by Codex, 2026-10-29:
`tools/hooper_asr.py` and `data/pilot/hooper2026-asr/` retain X21/X26 at both crown
nodes under every deposited method/tree. The two source archives match their
retrieval hashes; 76 master/ASR matrix comparisons agree. Independent R/ape
verification checks six MRCAs, 208 reported values and 32 absent columns without
zero imputation. The zyg-tree ARD X26 result favours dyads, although X21 favours
trilete aperture: these separate marginals do not unanimously recover trilete
monads or establish a joint ancestral phenotype. No inference was rerun; see
`docs/audits/2026-10-29-pilot-and-contract-review.md` (Q1/Q4, distinct from Q9's
clock audit).

## 6. Earth-system proxies and series

| Series | Status | Where |
|---|---|---|
| PhanDA GMST and CO2; PhanSST | local | `data/eprp/local/context/` |
| Song et al. 2021 SST; Scotese 2021 GMST (derived); Rothman 2017 events | held | `data/eprp/context/` |
| CO2: Foster et al. 2017, Dahl et al. 2022, Witkowski et al. 2018 | held | `data/external/deposits/` |
| Carbon cycle: Cai et al. 2026 data and COPSE code; COPSE (Mills) | held | `data/external/deposits/` |
| COPSE (Daines); Krause et al. 2018; Glasspool & Scott 2010 | local | `data/external/local/deposits/` |
| Lenton et al. 2016 | limited | PNAS supplement blocked |
| δ13C, Sr, δ18O: Grossman & Joachimski 2022, DM-SED 2025 held; Veizer 1999, Veizer & Prokoph 2015, Prokoph 2008 local | mixed | `data/external/deposits/` |
| Seawater Sr look-up (McArthur LOWESS) | limited | on request from the authors |
| Sea level: van der Meer 2025 held; Haq & Schutter 2008 limited; Franziskakis 2025 maps link only (1.3 GB) | mixed | `data/external/deposits/` |
| Weathering and land-plant proxies: Yuan 2023, Avila 2025, Wu 2026 | held | `data/external/deposits/` |

## 7. Palaeogeography and climate fields

| Source | Status | Where |
|---|---|---|
| PALEOMAP PaleoDEMs, 21 slices | local | `data/eprp/local/context/paleodem/` |
| Plate-model index (27 models) | held | `data/eprp/context/plate_models.csv` |
| HadCM3 SST (Balembois et al. 2025); cGENIE 400–480 Ma | local | `data/eprp/local/context/deposits/` |
| HadCM3L land climate, suite `scotese_02`, `tas` and `pr`, 21 slices | held (tables), local (fields) | `data/external/climate/` |
| Seven further HadCM3L suites (5.8 GB) | on hold | only if an ensemble is needed |

## 8. Rock record and sampling proxies

| Source | Status | Where | Notes |
|---|---|---|---|
| Macrostrat units | held | `data/eprp/record/` | North American, 88% marine |
| BGS DiGMapGB-625 | held | `data/external/rock-record/` | 2,634 Silurian–Devonian polygons, 48,575 km²; 2008 BGS age scale; no marine/terrestrial split |
| BGS Lexicon prose | local | `data/external/local/rock-record/` | no licence stated |
| ASUD | held | `data/eprp/record/` | 3,753 Australian Silurian–Devonian units, CC BY 4.0 |
| Palynological sampling effort | held | `data/external/spores/`, GAD in `data/external/deposits/` | documents reporting marine palynomorphs without spores |

## 9. Literature

The 30 October frame/source review (`audits/2026-10-30-frame-and-pilot-review.md`)
reconciles the held Rubinstein & Vajda 2019/2023 Borenshult accounts into one
34-sample inventory, including the 23 plotted spore-bearing depths. No event
outcomes were inferred for omitted depths. The held Ghavidel-Syooki &
Winchester-Seeto 2002 paper concerns the Ghelli type section, not Pelmis, and
cannot fill its inventory gap. Three source identities and their file hashes
are added to `data/units/sources.csv` and `source_files.csv`; all DOIs were
checked against Crossref. The same review records the absent saved branch
histories in the Hooper deposit (`data/pilot/hooper2026-asr/scm_workspace_audit.json`)
and independent specimen-source qualifications pending in Claude's pilot.

The subsequent regional-spore batch (29 October 2026) secured six studies plus
the linked Ghelli 2017 update: Ghavidel-Syooki 2016/2017 and 2021, El Diasty 2019,
Xu 2022, Filipiak 2022 and Wellman 2018. Seven publisher PDFs and the shared Ghelli
map are in `library/closed/`; versions, source URLs and hashes are in
`library/closed.tsv` and `docs/audits/2026-10-29-regional-spores-batch.md`.
The Ghelli bundle preserves the original, update cover and reissue; these are
one study, not independent assemblage evidence. Wellman's sample-details
Appendix 1 is internal (PDF page 5, printed 28). Most scientific extraction is pending.
The subsequent bounded Ghelli frame assessment read the 2017 methods, table 1,
figure 2 and conclusions: 27 productive Pelmis codes are now inventoried in
`data/units/frame_samples.csv`, with collection/subset and MG-130 discrepancies
retained. The 2011 and 2025 Khoshyeilagh sources were checked for admission scope,
not taxonomic adjudication. The latter is an E2 inventory lead; neither provides
an established complete E1-negative denominator. Source hashes, locators and the
companion-inventory leads are in `audits/2026-10-29-f3-response-and-ghelli-frame.md`.

Stage B's two ResearchGate main texts were recovered on 29 October 2026:
Mehlqvist et al. 2012 (12 pages) and Wellman et al. 2013 chapter 29 (16 pages), in
`library/closed/mehlqvist2012.pdf` and `library/closed/wellman2013.pdf`.
They are public author uploads in published layout; no reuse licence was
established for the main texts. Provenance is in `library/closed.tsv` and
`docs/audits/2026-10-29-researchgate-author-copies.md`. The separate Wellman
40-page supplement was already held in `data/external/spores/`; it is not a new
acquisition. Scientific extraction remains pending.

In `docs/closed-literature.csv`, `local-copy-held` records an institutionally accessed or Barry-supplied local copy;
`open-copy-held` records a publicly available copy and does not imply a particular licence.
`abstract-only` explicitly marks a held abstract without implying a held research article;
interpret availability alongside `kind` and the focused status register.

**First-study targets (2026-10-29, Claude).** `docs/first-study-literature.csv` ranks the
literature the first study (F3, the curated occurrence dataset and the trait pilot) still lacks:
- 135 works: tier 1 (58), needed to finish an F3 test, a pivotal adjudication or pilot scoring,
  and tier 2 (77), to read before submission;
- `route` separates what the reference scout can collect (`scout`) from parked requests that
  Barry reopens (`barry-reopen`) and his pending access action (`barry-action`);
- 73 works no register listed were appended to `docs/closed-literature.csv` as `needed`. Every
  supplied DOI was checked against Crossref, and `doi_check` says how.

The triage was a `gpt-6.1-sol` pass over the 348 needed rows plus a sweep of the first-study
documents and a search for sample-level frame studies; Claude adjudicated the tiers. Frame leads
are candidates whose sample-level reporting is still to be confirmed from the full text (Q1).

On 29 October 2026 the authorised six-paper institutional batch secured six full
texts (Strother 2025, Wang 2026, Vecoli 2017, Liu 2016, Ghavidel-Syooki & Piri-Kangarshahi
2021, Wang 2023) and Wang 2023's supplementary DOCX in `library/closed/`.
Strother is a verified browser print export; the other five are original publisher
PDFs. `library/closed.tsv` and `docs/audits/2026-10-29-six-paper-batch.md` preserve
versions and hashes. Barry resolved Liu 2016 by immediate download in Codex's
in-app browser; the earlier Chrome delivery stall did not establish an entitlement
problem. No fresh access action remains. Scientific extraction is pending; ten
older requests remain parked separately.

| Source | Status | Notes |
|---|---|---|
| EPRP library extract (426 works; 97 open texts local) | held | strong on methods, thin on palaeobotany |
| Palaeobotany and palynology harvest, plus the project's cited DOIs (EPRP item 8) | phase 1 held; phase 2 (open texts) running | `data/external/library/`; closed works in `docs/closed-literature.csv` |

Library store targets from 30 October 2026, under Barry's 29 October decision
recorded in Nectar's `docs/decisions.md`:

- Shared EPRP library: `nectar:/data/codex/paleodata/library` (the default in
  `data/external/scripts/library_eprp_library.py`).
- This project's harvest: `nectar:/data/codex/silurian_plants/library` (pass
  `--store` explicitly to the shared engine; `library_open_unread.py` uses this
  path directly). Run deployed helpers from the store's `_tools/` directory.

Use the `nectar` SSH alias and preserve the store's manifests, provenance and
read-only held PDFs. API credentials stay in the account's private `~/.config`
paths, never in this repository. Deep's original library copies are retained
until Barry approves their removal; their old locations are provenance, not
the destination for new library work. Transfer verification is recorded in
Nectar's machine and exchange notes. This changes library storage only; the
historical raw-data and model-run locations elsewhere in this register remain
unchanged.

## 10. Models and software

Pointers: `data/eprp/pointers/`. TREED code: `data/eprp/context/deposits/`. COPSE variants and the
GAD code: `data/external/deposits/`. gen3sis, FossilSim, paleobuddy, PyRate and cGENIE are on
`deep-server` (not reachable from the Macs). SCI-FI (SCION with FLORA; Gurung et al. 2024) runs headless in MATLAB on mac-mini (smoke test 2026-10-27; outputs in `deep-server:/data/codex/silurian_plants/runs/scifi-smoke-2026-10-27/`). The Codex CLI (0.164) runs non-interactively here with schema-constrained output,
which makes it a candidate for bulk extraction (2026-10-27 smoke test).

## Open items for Barry

1. Whether to ask Wellman, Steemans and Vecoli for their full assemblage database (an external
   contact).
2. Five Elsevier supplements (Capel 2021, 2022; Cascales-Miñana 2016; Prokoph 2008; Veizer &
   Prokoph 2015) were fetched from Elsevier's public supplement server with file names inferred
   from the article ID, because the article pages block automated requests. They are held
   locally only. Keep them, or delete them and re-download through a browser.
3. Supplements behind Wiley, Science and PNAS walls (Toledo 2021, Capel 2023, Haq & Schutter 2008,
   Lenton 2016): a browser or library download would resolve these.
4. The go-ahead for EPRP item 8 and for the spore compilation (possibly on Codex).

## 11. Autonomous literature expansion, 29 October 2026

The first autonomous checkpoint adds 46 main texts, 25 supporting files and a
linked erratum to `library/closed/`. The CSV records 34 institutional copies and
12 public copies; `library/closed.tsv` records every asset, URL, format, extent
and SHA-256. The full file index and qualifications are in
`docs/audits/2026-10-29-autonomous-expansion.md`; the machine-readable receipt is
`work/codex/literature/2026-10-29-autonomous-expansion.json`.

This includes the Cooksonia conducting-strand anchor, Aglaophyton, Hueber's
Baragwanathia and Prototaxites papers, Kenrick's Ordovician reinterpretation,
regional spore papers and plant-physiology sources. The Hawaz text is an accepted
manuscript and Grahn's Apucarana text is an early proof; final-version equivalence
is not established. Mahmoudi's DOI remains unverified. Kubásek's Table 3 erratum
is held with the main article and supporting figures; later readings must use the
replacement table. The published Ibarra R source is held as a file and has not
been executed. Scientific extraction remains pending.

The second checkpoint adds 39 main texts and 16 supporting files, including the
Edwards cryptospore/eophyte papers, older Wiley descriptions, four SCUP/Lethaia
articles and a Caltech author copy of the 2011 Ghelli paper. Capel's four supporting
files and Toledo's supplement close two separate SI gaps. The autonomous total is
85 main texts, 41 supporting files and one erratum. The current CSV has 360 needed,
99 local-copy-held and 33 open-copy-held rows. See
`docs/audits/2026-10-29-autonomous-wave2.md` and
`work/codex/literature/2026-10-29-autonomous-wave2.json` for the file index, scan/OCR
qualifications and remaining save/access routes. Scientific readings are pending.

The subsequent native-save follow-up recovered all ten Oxford candidates plus
Edwards 1980 and Mark 2011, with Mark's five supporting files. The autonomous total
is now 97 main texts, 46 supporting files and one erratum. The CSV has 348 needed,
111 local-copy-held and 33 open-copy-held rows. The earlier desktop-save blockers
are resolved; see `docs/audits/2026-10-29-autonomous-native.md` and its matching
receipt. Pertica now has a confirmed JSTOR institutional route requiring Barry's
explicit terms action, recorded separately from entitlement gaps.

## 12. First-study Tier 1 acquisition, 29–30 October 2026

The focused pass secured 39 new main texts, ten new supporting files (seven originals and
three qualified browser-text captures), two complete conference abstracts and a qualified
Masiak 2003 component copy. Three already-held Morris supporting/data files were also copied
into the reading library, giving 55 file entries. Forty of 58 Tier 1 rows now have main texts
(one Lang/Cookson duplicate); two are abstract-only, one partly held and 15 blocked.
Sixteen rows remain unresolved or incomplete. Tier 2 was not collected in that pass
(and is reported separately below); the two still-parked sources remain parked. See `docs/audits/2026-10-30-first-study-tier1.md`,
`docs/first-study-literature-status.csv` and `library/closed.tsv`.

Q1 gains Qusaiba, QSIM-801, Borenshult, Kanosh, Hanadir and one Pelmis companion;
Q2/Q4 gain the pivotal pilot and anatomical sources. New holdings are reading inputs,
not verified sampling frames or adopted trait/age interpretations. Preserve the
repository-manuscript, preprint, print/online-year and Masiak extent qualifications.
For Q5, al2014f is a distinct 2014 GEO poster abstract, not an alias of the 2015 systematic
paper. The Sweden one-page source is also an abstract; Steemans 2009's one-page Brevia
is a complete article, with its original supporting methods now held.

## 13. First-study Tier 2 acquisition, 30 October 2026

All 77 Tier 2 rows were attempted: 30 new main texts, twelve exact works already held,
two complete abstracts, one already-held data archive, one first-page partial, one
supplement-only holding and 30 blocked rows. Thus 42 main texts are available and 32
rows need further action. The 92 filed assets include 33 supporting/data copies already
held elsewhere; file counts do not measure newly recovered papers. Original/accepted
versions, the Mawson BHL reconstruction, McSweeney thesis/deposit years and Canning's
first-page limit are explicit in `audits/2026-10-30-first-study-tier2.md`.

Reading copies are under `library/closed/`; `library/closed.tsv` and
`work/codex/literature/2026-10-30-first-study-tier2.json` preserve provenance and QA.
`first-study-literature-status.csv` covers all 135 prioritised rows without changing
the original priority input. Five reader/save cases and Hoffmeister's JSTOR terms
step are the first office actions in `barry-to-action.md`; request candidates are
separate in `literature-requests.md`. Source acquisition does not validate an F3
sampling frame, absence, trait transfer or chronology. No scientific status changed.

## 14. MacBook return and acquisition closure, 30 October 2026

Barry's MacBook access/search round closed 35 main-text gaps plus Wellman (2026)'s intended
conference abstract. The full 982-file folder is retained, source-inventory verified,
at `library/closed/_incoming/macbook-2026-10-30/`. All 42 supplied PDFs have mini reading
copies under `library/closed/`, original bytes and provenance in `library/closed.tsv`;
see `audits/2026-10-30-macbook-literature-return.md` for versions, extent and the file index.
Garratt (1978), the 2007 Pelmis companion, Vecoli (2011), Rubinstein (2023) and the other exact
recoveries can now be read. Ghavidel-Syooki (2000), Abuhmida (2013)'s complete thesis and the EPPC
abstract book are additional contextual/supporting sources; Mehlqvist (2012) is a duplicate.

The focused 135-row register now has 117 main-held rows (one earlier alias), five complete
abstracts, one dataset and twelve **unobtainable** rows. At Barry's instruction, the
remaining four Tier 1/eight Tier 2 sources are closed for this acquisition round and listed
in `unobtainable-literature.csv`. Ten remain unheld, two partly held. The Masiak physical
p.330 issue and Canning one-page limit remain explicit; no component, thesis or related
paper closes the wrong source. The master uses `unobtainable` for this disposition,
separately from `needed`; evidence gaps remain and no automatic retry is queued.
The two previously parked background sources stay parked. Original input priorities,
scientific interpretations and source-identity distinctions are unchanged.
