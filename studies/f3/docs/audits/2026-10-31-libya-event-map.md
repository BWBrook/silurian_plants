# Libya event and productivity mapping

31 October 2026. Codex, with independent source and chart checks. Q1/Q2; source
conflicts retained under Q5. This completes the bounded mapping of the declared
164-sample appendix against the six enclosure charts and relevant prose. It does
not resolve every sample identity or adopt a binary observation rule.

## Source reports and their grain

The held 641-page Abuhmida (2013) thesis is unchanged, SHA-256
`c0e3bf798fb3c27db0bf9cbb155396be5b4b8e003ee2228defb615a65abf3211`.
The preceding inventory audit is `2026-10-31-qusaiba-libya-frames.md`.

- `data/units/libya_chart_reports.csv`: 158 chart-labelled well/depth records.
  It records the *Ambitisporites dilutus* column, marine-group coloured point
  symbols, other green point symbols and exact appendix membership. Counts are
  plotted symbols, not specimens, abundance, search effort or independent trials.
- `libya_prose_evidence.csv`: 27 paraphrased source statements with printed/PDF
  locators, covering methods, productivity, assemblages, specimen reports and
  conflicts. Every statement concerns this thesis.
- `libya_prose_support.csv`: all 164 appendix entries linked to those statements,
  preserving appendix formation/type and separating sample-specific reports from
  assemblage context. Its binary-outcome field is blank throughout.

Join by well and numeric depth in feet, **only for exact matches**. There are 153.
The five chart-only labels remain source reports without additional material
trials; the eleven appendix-only entries retain their prose evidence. In
particular, A28i's half-foot differences and I3's 5230/5220 difference remain
unresolved. Source labels are not corrected by inferred aliases.

| Well | Chart rows | A. dilutus marks | Marks on exact appendix matches | Rows with marine symbols | Completely blank rows |
|---|---:|---:|---:|---:|---:|
| A28i-NC186 | 24 | 0: column absent | 0 | 24 | 0 |
| B2-NC186 | 17 | 6 | 6 | 6 | 11 |
| D1-200 | 35 | 13 | 13 | 35 | 0 |
| E1-NC174 | 15 | 10 | 9 | 15 | 0 |
| H2-NC186 | 28 | 7 | 7 | 28 | 0 |
| I3-NC186 | 39 | 16 | 16 | 38 | 1 |
| **Total** | **158** | **52** | **51** | **146** | **12** |

The remaining target-column states are 82 `no-mark` and 24 `column-absent`.
Neither means an adopted E1 absence. The extraction is specifically for the
named species: it is not a taxonomic adjudication of every possible E1 report.

## Discrepancies that matter to inference

**The only sample-specific core trilete report is absent from its chart.**
The Cr3 account (printed pp.381–382, PDF pp.397–398) reports one *A. dilutus*
specimen from E1-NC174 core 7287 ft and calls it the only true trilete in that
assemblage. Neither enclosure panel marks its target cell. All five E1 cores
are blank in that column. The 52 chart marks, including 51 exact appendix
matches, contain no clearly typed appendix core. Two marked D1 samples have
unspecified appendix types but CU chart labels; the other 49 exact positives
are appendix cuttings. The chart-only positive is E1 6750 ft, also labelled CU.

**Cr3's reported uniqueness also conflicts with I3.** The I3 chart marks
*A. dilutus* at 4600 and 4640 ft, both inside the named Cr3 interval. The 4600-ft
endpoint also belongs to the printed Cr4 interval; 4640 does not. Keep the chart
reports, prose uniqueness claim and overlapping zonal boundaries separately.
Plate 4, figure 7 (caption printed p.601, image p.602; PDF pp.617–618) supports
a different specimen at I3 4200 ft, England Finder O20/2, which the chart also
marks. It cannot verify the 7287-ft core specimen or prove that any cutting
occurrence is indigenous.

**Ash Shabiyat is not uniformly barren.** Printed p.367/PDF p.383 explicitly
excepts some I3 cuttings at 5250–5340 ft, with sparse acritarchs possibly caved
from above. Each of the three appendix/chart depths 5250, 5320 and 5340 has
three marine-group symbols. Thus the charts provide individual recovery reports
where prose alone supplied an uncertain interval. The indigenous preservation
opportunity remains uncertain. Later blanket barren wording (pp.384, 395)
must retain this exception.

**Fourteen appendix entries lie within explicit barren scopes.** They comprise
nine B2 Memouniat levels, B2 Ash Shabiyat 4800/4900, H2 Ash Shabiyat 5250/5300,
and I3 Ash Shabiyat 5400 ft. The twelve with exact chart labels are completely
blank; the two H2 entries are omitted from the charts. These are reported
productivity failures, not ecological E1 zeros. The differing B2 Memouniat
interval endpoints on pp.357 and 398 remain formation-qualified.

**The taxon spelling changes internally.** Systematics pp.299–300/PDF pp.315–316
describe *Chelinohilates maculatus* as a hilate cryptospore; chart headers use
*Chelinohilates maculates*, whereas assemblage prose uses *Chelinotriletes
maculatus*. This spelling discrepancy is not evidence of another true-trilete
taxon. No new E1 reading follows from it.

Other limits persist: methods/abstract enumerate 164 samples and six wells,
but pp.351 and 406 state 167, with five wells on p.351; Cr3's early-Rhuddanian
age differs from the systematic occurrence wording beginning in mid Rhuddanian;
the A28i appendix/prose formation names differ; and B2 4100/4200 have conflicting
core/cutting labels. None is silently reconciled.

## What the evidence permits next

Cr2 explicitly lacks true triletes at assemblage scope, with named intervals
in D1, I3, A28i and H2 (p.381). Its explicit list omits the I3 Melez Shugran
interval that broader formation-level prose associates with Cr2. Cr1's taxon
list is not an explicit E1-negative statement. Sample-level conversion therefore
needs the declared reporting rule and reading, even when chart cells are blank
and marine palynomorphs occur.

| Candidate comparison | Available inventory evidence | Assumptions still required |
|---|---|---|
| H2 within well, cores plus cuttings | Eight Tanezzuft cuttings, seven A. dilutus marks; 17 Hawaz entries with exact chart matches and marine symbols, comprising ten cores, five cuttings and two unspecified appendix types | Named event reading and chart conversion; core/cutting and facies comparability; caving treatment; shared chronology; age allocation within Darriwilian |
| D1 within well | Sixteen Tanezzuft entries, 13 marks; seven Hawaz entries but only three chart matches; no clearly typed Hawaz cores | Four missing productivity links at 5150/5250/5350/5450 ft; cutting contamination and reference transport across formations; shared ages |
| I3 within well | Twenty Tanezzuft/hot-shale cuttings, 16 marks; younger Ordovician material is charted, but older Ash Shabiyat has three possibly caved recovery reports and one barren sample | No demonstrated indigenous productive older Ash Shabiyat comparison; caving and age uncertainty cannot be replaced by chart zeros |
| Cross-well core-only | Twenty-six Hawaz cores (16 A28i, ten H2), with 25 exact chart matches; all five clearly typed younger Tanezzuft cores are in E1 | Cross-well/facies transport plus resolution or explicit alternative treatment of the sole prose-positive core at 7287 ft; no chart-positive core reference |

These are inventory counts, not eligible-trial denominators or measured reference
rates. In particular, a Darriwilian assignment does not make every Hawaz sample
older than the 459.1 Ma target. The geological age model must allocate exposure.
Qusaiba remains a distinct reference candidate; using it changes the transport
assumptions rather than solving them automatically.

**Recommendation for Claude's design adjudication:** start with H2's within-well
comparison and carry a core-only comparison as a separately declared transport
scenario if its reference can be justified. H2 has the most complete recoverable
Hawaz/younger mapping; this is an evidence-completeness recommendation, not a
choice based on a fitted F3 result. No design, positive count or binary conversion
is adopted here. Declare the candidate comparisons and selection procedure
before screening and binding qualification; the remaining contract points are
in `2026-10-31-qualification-repair-review.md`.

## Verification and structural review

`tools/libya_charts.py` pins the inspected source hash and uses PyMuPDF 2.0 to
locate labelled sample rows and coloured filled point symbols. It excludes LOG
stratigraphic boundaries. Every symbol has an unambiguous sample row; none is
unmapped. The upper range panel and lower presence panel agree separately for
every sample's target, marine and other-green counts. All 158 keys and type
codes reproduce the previous enclosure transcription. The receipt records input,
script and output hashes. Symbols are collapsed across duplicate panels.

The independent source scout mapped 27 statements to all 164 appendix entries.
A separate follow-up inspected all six wells' spore headers and independently
rendered the key target/sample alignments, confirming the 7287-ft blank, the
I3 4200/4600/4640 marks and the hilate taxon account. Independent pixel detection
also agrees on all 134 target-column states and all 158 marine-presence states;
its scripts, row checks and receipt are retained in
`2026-10-31-libya-independent-check/`. Parent and scout agree on these
discrepancies. The source PDF remains local and git-ignored.

`tools/units.py check` now checks both mapping tables' unique complete keys,
source-evidence links, preserved type/formation identities, symbol totals and
absence of adopted binary outcomes. The accepted interface remains 49 material
blocks/294 outcomes, with seven candidate frames and 276 inventory entries.
Scratch corruption checks reject both a fabricated binary outcome and a
duplicated chart key replacing a missing sample.

The structure serves the next investigation: exact source reports, source
conflicts and scientific readings can remain separate. Q1 gains a concrete
design comparison; Q2 gains a potentially decisive core reference discrepancy;
Q5 records internal conflicts without claiming that they propagated through
later literature. No question is answered, no empirical F3 exclusion is released,
and no outside reply is needed for the next design step.

Source: Abuhmida F (2013). *Palynological analysis of the Ordovician to Lower
Silurian sediments from the Murzuq Basin, southwest Libya*. PhD thesis,
University of Sheffield. Held complete thesis; no DOI.
