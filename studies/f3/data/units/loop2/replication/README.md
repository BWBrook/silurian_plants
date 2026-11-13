# QSIM-801 occurrence extraction and external-frame disposition

Loop 2 close, 1 November 2026. The directory name records the attempted replication;
it does not imply that a second empirical frame was admitted or qualified.

## Verified source extraction

`qsim801_vecoli2017_table1.csv` transcribes Vecoli et al. (2017), Table 1, printed
p.321 / PDF p.3 of `library/closed/vecoli2017.pdf`. An independent visual check of
the rendered page, followed by exact comparison of all taxon-name sets and counts,
confirmed 20 depth-labelled rows, 22 taxon/morphotype categories, and 99 occurrence
marks: 72 in the upper panel and 27 in the lower. Seventeen rows contain marks.
The blank rows are 695.7, 731.6 and 735.1 ft. No transcription edits were needed.

Each `cryptospore_marks` value counts occupied taxon categories, not raw specimens,
individual spore cells or producer individuals. The semicolon-separated `taxa` field
preserves the source's column labels, including informal morphotypes and inconsistent
`Segestrspora`/`Segestrespora` spelling. A mark supports at least one observed object
if the within-sample categories are mutually exclusive. It does not establish an
independent biological dispersal event or a random count trial.

`trilete_reported=0` encodes the authors' explicit study-wide non-detection in
section 6.1, printed p.330 / PDF p.12. It is not an enumerated zero from a reported
specimen-count table. That passage describes the same three cryptospore-free depths
and extends the non-detection throughout the sampled sequence.

## Source inconsistencies retained (Q5)

- The 20 table depth labels span **675.1–767.8 ft**. Printed p.320 says the samples
  extend to **586.9 ft**. The extraction follows Table 1 and does not invent rows or
  extend its observation scope to the shallower number in the methods.
- Table 1 marks *Tetrahedraletes grayae* at **five** depths: 675.1, 677.9, 682.2,
  685.9 and 688.6 ft. Printed p.330 says the uppermost **four** samples. The five
  table marks are retained; the discrepancy is not repaired by deleting evidence.

These are inconsistencies within the primary source, not CSV transcription errors.

## Admission and model scope

**No new primary admission.** The 99 marks and study-wide trilete non-detection are
verified observations. The associated share calculation remains an exploratory
conditional method pending evidence of comparable ascertainment: the search over
which cryptospores and triletes could have been found and recorded.

Vecoli's printed p.320 reports approximately 30 g per sample, Liège acid maceration,
oxidation and 12-µm sieving. It supplies no slide/field search effort, stopping rule,
random/systematic counting scheme or measured recognition probability. Therefore
“one examination per sample” and a binomial independent-unit observation process
are assumptions, not demonstrated protocol facts. The recovery/recognition scenarios
for `h` and the design-effect scenarios do not measure or resolve this gap. The
conditional bound concerns a persistent floor across samples, not a mean ratio;
producer abundance additionally needs delivery, preservation and output assumptions.

Le Hérissé et al.'s companion percentages and at-least-300 palynomorph counts are
not used as the denominator. Its 42-sample, mixed-preparation protocol lacks a
demonstrated link from those counted preparations to Vecoli's trilete search.
The new mark-based argument and that rejected companion-count construction are
different designs.

The source's late Dapingian–early Darriwilian assignment is older-side M2 context,
not per-sample dating or a measured persistence duration. The full Darriwilian stage
extends from 469.4 to 458.2 Ma in `data/timescale.csv`, so a generic stage label alone
would not establish that every sample predates 459.1 Ma.

## External candidates and search limits

`manuscript/external_candidates.csv` records the seven bounded candidate/design
dispositions and their source locators. No matched counted Katian–Llandovery
reference was recovered in the bounded review. No claim of exhaustive coverage of
346 PDFs or 195 text files is supported: a reproducible roster, exact query,
extraction-coverage report and adjudicated match list for that earlier assertion
were not located. A matched counted reference would still require compatible
observation units, search, recovery and age support.

Hanadir/TAYM-4 is separate material from QSIM-801. It was not independently admitted
or protocol-qualified in this close; same-region occurrence does not establish
reused specimens or, by itself, statistical non-independence.

## Provenance

- Primary PDF SHA-256: `5932b8da36d10be365089f06cab55ad472ade98c238186432058e9493459936b`.
- Extraction CSV SHA-256: `325e97fa006e7f2fd3f50cb5f193fbd843356a646341f871088aa4644dd66754`.
- Primary-source audit: `docs/audits/2026-11-01-loop2-close-qsim-source-review.md`.
- Method implementation: `models/f3/loop2/replication/qsim_share.py`; numerical outputs
  retain their declared conditional/scenario scope and do not validate the historical
  microscopy protocol.

The copyrighted primary PDF remains local. The CSV is a derived occurrence extraction;
its source identity, limitations and source contradictions travel with it.
