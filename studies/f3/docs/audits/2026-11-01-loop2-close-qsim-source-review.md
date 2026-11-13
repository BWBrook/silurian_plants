# Loop 2 close: independent QSIM source review

Codex, 1 November 2026. Scope: primary-source check of the QSIM extraction and the
source assumptions behind sprint 2, plus bounded checks of the already named comparator
sources. This review owns only this audit; it changes no data, model or manuscript.
Findings below concern the received sprint-2 package, before the integrator's corrections.

## Verdict

The Table 1 transcription passes: **99 marks = 72 + 27, in 17 of 20 samples**, with
all row-level taxon assignments matching the rendered primary table. The explicit
trilete non-detection applies to the same study sequence. This supports a new
occurrence-mark lower-bound argument, distinct from the rejected use of the companion
paper's palynomorph percentages. It does **not** establish a counted, independent or
non-selective search protocol. Keep the share calculation exploratory and conditional
on an observation model, rather than treating recovery parity alone as the remaining
empirical uncertainty.

The claim that no counted reference is held exceeds the documented search evidence.
No reproducible file roster, exact query, extraction coverage or candidate adjudication
for the claimed 346 PDFs/195 texts was located. The bounded primary checks here do not
constitute a replacement whole-library search.

## Primary table and row check

Vecoli et al. (2017), printed p.321 / PDF p.3, Table 1, was rendered with Poppler and
inspected visually. I separately entered the occupied column positions in both panels
and compared their taxon-name sets and counts against
`data/units/loop2/replication/qsim801_vecoli2017_table1.csv`. The comparison found no
row or taxon-assignment errors. The literal source labels, including its inconsistent
`Segestrspora`/`Segestrespora` spelling, are retained in the CSV; this is transcription,
not a new taxonomic adjudication.

| Depth (ft) | Upper panel | Lower panel | Total |
|---:|---:|---:|---:|
| 675.1 | 4 | 1 | 5 |
| 677.9 | 8 | 9 | 17 |
| 682.2 | 5 | 2 | 7 |
| 685.9 | 6 | 2 | 8 |
| 688.6 | 3 | 1 | 4 |
| 693.1 | 5 | 0 | 5 |
| 695.7 | 0 | 0 | 0 |
| 699.9 | 2 | 1 | 3 |
| 704.3 | 6 | 4 | 10 |
| 715.6 | 4 | 0 | 4 |
| 719.9 | 3 | 3 | 6 |
| 725.4 | 3 | 0 | 3 |
| 731.6 | 0 | 0 | 0 |
| 735.1 | 0 | 0 | 0 |
| 741.5 | 2 | 1 | 3 |
| 746.5 | 3 | 1 | 4 |
| 751.5 | 3 | 2 | 5 |
| 756 | 1 | 0 | 1 |
| 762.3 | 9 | 0 | 9 |
| 767.8 | 5 | 0 | 5 |
| **Total** | **72** | **27** | **99** |

There are 22 column categories, including informal morphotypes, rather than 22
necessarily formally named biological species. Treating a mark as evidence of at least
one observed object is reasonable if the authors' within-sample categories are mutually
exclusive. Different morphotypes in one sample and occurrences in different depth samples
support distinct recorded objects; they do not establish independent biological dispersal
events. Monads, dyads and tetrads are different physical units, and the table is not a
count of their component cells or of producer individuals. It supplies no measured
clustering factor or probability of preparation-induced break-up.

Two internal source discrepancies should not be silently reconciled. Printed p.320 says
the 20 samples extend to 586.9 ft, whereas Table 1's shallowest listed sample is 675.1 ft.
Printed p.330 describes *T. grayae* in the uppermost four samples but Table 1 marks five
depths (675.1, 677.9, 682.2, 685.9, 688.6 ft). The CSV correctly follows the table; neither
discrepancy changes its 99-mark sum. Keep the table-defined frame and do not extend its
observations to 586.9 ft.

## Scope of zero and unmeasured observation process

Vecoli printed p.330 / PDF p.12, section 6.1, explicitly reports cryptospores in all
but 735.1, 731.6 and 695.7 ft, then states that the recovered spore assemblages
throughout the sampled sequence contain cryptospores and no observed triletes.
The three blank rows match Table 1. This is an explicit sequence-wide non-detection,
not a zero inferred from a missing trilete column. It is scoped to the authors' study
material, without borrowing another paper's count.

Printed p.320 / PDF p.2, section 3, reports 20 samples, approximately 30 g per sample,
HCl–HF–HCl treatment at Liège, brief HNO3/KClO3 oxidation, 12-µm sieving, and a hot
25% HCl bath. Figured objects have slide details and England Finder coordinates.
The methods do **not** give a number of slides or fields searched, inspected area,
random/systematic selection rule, specimen-count stopping rule, exhaustive-search claim,
or a prospectively defined rule for recording triletes during the cryptospore survey.
Systematic descriptions provide morphological comparisons and measured examples, but
not an estimated recognition-error rate or an operational search classifier.

Consequently, the received phrase “one examination per sample” is stronger than the
source. “The same study material” is supported; a single matched count/search experiment
is not demonstrated. The non-detection could encompass more work than the occurrence
table, which may help a lower-bound argument, but its search coverage is unmeasured.
Neither selective search nor a particular stopping rule is alleged to have occurred;
the source does not identify which observation model generated the table and zero.

The received `qsim_share.py` correctly names an independent-Poisson/binomial model and
a persistent-floor estimand, but its opening observation contract presents the single
examination and dispersal-unit mapping as established. Recovery/recognition ratio `h`,
independence/exchangeability, non-selective comparable search, classification into
distinct units, and the sampling/stopping mechanism remain assumptions. Dividing 99 by
design effects 2 or 4 is a sensitivity scenario, not a source-measured effective sample
size. Simulation under the assumed model cannot validate the historical search protocol.
Nor does a bound on recovered or delivered units become a bound on producer abundance
without relative delivery, preservation and output assumptions.

Recommended source gate: retain the verified occurrence table and explicit non-detection;
retain the conditional calculation as exploratory; do not claim a protocol-qualified
empirical exclusion from the source alone. The lack of a reported exact count does not
mathematically invalidate every lower-bound method, but a lower bound does not by itself
establish the method's sampling model.

## Companion-count gate and age scope

Le Hérissé et al. (2017), held author manuscript PDF pp.9–10 / manuscript pp.8–9,
describes 42 samples, an earlier Aramco preparation series, and subsequent Brest/Liège
preparations including soft digestion and unfiltered residues in Brest. It reports at
least 300 palynomorphs counted per sample. These methods do not identify those counted
preparations with Vecoli's trilete-search material. The earlier companion-count rejection
therefore stands. The new 99 marks are not those counts and must not inherit their
300-specimen effort. This review did not repeat the full 42-row depth reconciliation.

Vecoli printed p.319 / PDF p.1 gives late Dapingian–early Darriwilian in the abstract.
The geological-setting paragraph distinguishes an early-to-late Darriwilian Hanadir
succession from the older Sajir member spanning the Dapingian/Darriwilian boundary,
and says definitive age control for the latter is lacking. The late Dapingian–early
Darriwilian assignment is an older-side context for M2 = 459.1 Ma; it does not supply
dated per-sample exposures, a continuous persistence interval or a precise duration.
The project's `data/timescale.csv` gives 471.3, 469.4 and 458.2 Ma for Dapingian,
Darriwilian and Sandbian bases. In particular, a generic **Darriwilian** assignment
alone does not prove a sample predates 459.1 Ma: the full stage extends past that age.
Keep the source's narrower qualifier and its dating limitation together.

## Bounded comparator/source-claim checks

| Source checked | Primary evidence | Consequence |
|---|---|---|
| Strother et al. 2015, printed p.98 / PDF p.2, rendered | All described material is from TAYM-4; additional core preparations were examined. Original material included RA cuttings and TAYM-4/KAHF-1 cores. Residues were not oxidised. | These are different boreholes/material from QSIM-801. Same region and broad age do not establish reused observations or statistical dependence. Say separate Hanadir material, not separately admitted or protocol-qualified. Regional correlation can remain a concern without claiming specimen reuse. |
| Wellman et al. 2015, printed pp.112–113, methods; p.116 / PDF p.6, rendered Table 2 | Qusaiba-1 has 37 samples; primary Liège processing and selected duplicate Sheffield preparations are distinguished. The occurrence table is taxon presence, and prose describes relative abundance qualitatively. | No matched counted trilete/cryptospore reference was recovered in this bounded check. This does not assert that all material behind the study lacks counts. |
| Abuhmida 2013, printed p.382 / PDF p.398, rendered | Cr-3 is early Rhuddanian; the discussion lists rare cryptospores and one named true-trilete taxon, *A. dilutus*, with very rare triletes. | The wording about one true trilete occurs in taxonomic assemblage prose, not a specimen tally. Do not convert it to “a single trilete” observation or a numerical relative share. The zone covers intervals in three wells, rather than one counted sample. |
| Abuhmida 2013, printed p.383 / PDF p.399, rendered | Cr-4 contains moderately abundant true-trilete specimens and is explicitly assigned late Rhuddanian–Telychian from independent zonations. An Ashgillian–Rhuddanian Saudi zone is a comparison. | State the actual age assignment; the received manuscript's “another Ashgillian–Rhuddanian-correlated zone” omits the source's more precise age. No trilete:cryptospore count ratio follows from the adjective. |
| Abuhmida 2013, printed p.350 / PDF p.366, text checked | Summarises Gray et al. 1992 as moving a zonal top to mid-Telychian, when triletes begin to dominate assemblages. | This is secondary, qualitative context. Gray et al. 1992 was not independently read here; no numeric persistent floor follows from this summary. |
| Badawy et al. 2014, printed p.16 / PDF p.2, rendered abstract | Röstånga-1 study spans Katian–Rhuddanian; reported cryptospores are late Katian–early Hirnantian. | Younger than 459.1 Ma; correct to exclude it as an older-side M2 frame. This age decision does not by itself decide its value as reference context. |
| Rubinstein et al. 2016, printed p.14 / PDF p.1, rendered abstract | Caspalá material includes early-to-late Katian chitinozoans, with a Hirnantian age if spores are indigenous; Lipeón triletes are Telychian. | Both stated age readings are younger than 459.1 Ma. The older-side exclusion stands; retain the reworked/indigenous distinction if used as reference context. |

These source checks are not an exhaustive inspection of all figures or supplements for
reference tallies. No additional source acquisition or broad new reference hunt was run.

## Search-completeness wording

The numbers 346 held PDFs and 195 held text files occur in the sprint-2 results and the
claim ledger; the manuscript instead says 346 held texts. The three declarations do
not identify the actual scanned file list, deduplication rule, exact regular expression,
text-extraction failures, image/table coverage, or an adjudicated list of matches. A
search through the report, audit, model, tool and replication surfaces found no associated
search script/receipt supplying these. `docs/sprint2-source-roster.md` is an earlier
source-assessment roster, not evidence of this Loop 2 346/195 search.

The correct conclusion from the available evidence is “no matched counted reference
was recovered in this bounded review”, accompanied by the named candidates and their
actual dispositions. “No counted reference exists”, “no held source gives tallies”, and
“none in 346 PDFs/195 texts” are not independently reproducible from the retained
evidence. A regex looking for percentage prose would in any event not establish absence
of graphical counts, taxon tallies, supplementary data or synonyms.

This limitation also constrains the claimed priority of a counted reference: such a
reference could enable a comparison only after matching its observation units, recovery,
search and dating to the older-side design. It does not alone cure QSIM's protocol gap.

## Evidence identity and verification limits

| File | SHA-256 |
|---|---|
| `library/closed/vecoli2017.pdf` | `5932b8da36d10be365089f06cab55ad472ade98c238186432058e9493459936b` |
| `data/units/loop2/replication/qsim801_vecoli2017_table1.csv` | `325e97fa006e7f2fd3f50cb5f193fbd843356a646341f871088aa4644dd66754` |
| `library/closed/strother2015.pdf` | `902f183848f947a638de283fc9b566278c83f2b9b653ecdd0eca481d8d53691e` |
| `library/closed/abuhmida2013-thesis-related_macbook20261030.pdf` | `c0e3bf798fb3c27db0bf9cbb155396be5b4b8e003ee2228defb615a65abf3211` |

Verification comprised primary-page rendering, targeted primary text reads, independent
table-position entry, and exact comparison with all CSV rows and taxon sets. The model
contract and simulation setup were read, but its numerical simulations were not rerun in
this source review. Statistical validity and release qualification need the separate
methods/integration review. All interpretations above are review findings for Q1/Q5;
the integrator records adopted decisions and downstream edits.

## Documentation addendum after integration

At the integrator's request, this review added
`data/units/loop2/replication/README.md` and `manuscript/external_candidates.csv`.
The README states the table's observation semantics, unchanged source contradictions
(Q5), source hashes and conditional admission status. The seven-row candidate ledger
separates material, age, role, admission, status, dependence, evidence and limitations.
It preserves separate Hanadir material and a bounded, non-exhaustive reference-search
conclusion. All nine fields in all seven rows parse and are non-empty. The occurrence
CSV still has SHA-256 `325e97fa006e7f2fd3f50cb5f193fbd843356a646341f871088aa4644dd66754`.

The revised manuscript sections 2.4, 2.5 and 3.2 now distinguish the mathematical
calculation from empirical admission, describe the protocol gap, restrict the estimand
to a persistent floor, qualify the design-effect scenarios, correct Abuhmida's
taxon-versus-specimen and Cr-4-age interpretations, and avoid an exhaustive library
claim. Their source statements agree with this review. The QSIM age assignment is
documented in the README and candidate ledger; including it beside the manuscript's
first QSIM description would make the older-side context easier to assess without
opening the supplement. No further primary-source correction is required in those
revised passages. This addendum does not review the separate statistical proof or
other biological/numerical sections of the manuscript.
