# Loop 3 review A: source identity and horizon independence

Codex (OpenAI; independent source reviewer), 1 November 2026. Scope: the v0 macrofossil horizon
table, its PBDB occurrence and collection inputs, the curated occurrence tail, and a stratified
sample of pivotal and later horizons. Detailed adjudications are in
`data/macro/source_adjudications.csv`. This audit assesses source identity, category admission and
whether rows can be treated as independent dated horizons. It does not validate the endpoint
estimator, which is reviewed separately in `2026-11-01-loop3-methods-review.md`.

## Verdict

The v0 table is a useful candidate inventory, not an analysis-ready set of independent horizons.
Its main defect is not the positive-record idea but unsupported equivalence at both ends: PBDB
collection numbers were treated as horizons, while 14 PBDB--tail matches inferred from shared
country, age and taxon were treated as exact duplicates. Several inferred matches are demonstrably
different localities; others are unresolved and need sensitivity analyses rather than deletion.

The recommended build repair admits an occurrence only when
the name first passes the early-embryophyte category gate, suppresses explicit PBDB--tail
aliases, restores distinct named PBDB localities, separates regional lists from source-resolved
outcrops, and records unit uncertainty instead of manufacturing independence. The primary table
still contains PBDB-derived horizons whose botanical identification or bed mapping was not
independently checked. Results therefore need locality- and region-stage collapse sensitivities and
must not be described as estimates from fully source-verified fossil horizons.

## Decisive findings

### Category admission had a logical leak

The v0 admission rule was effectively `b0 OR b1 OR b2`. Some classifiers correctly marked a name
as implausible in the Silurian--Early Devonian window but also assigned `b1=yes` or `b2=yes` from
the younger clade's biology. The OR rule then admitted the occurrence. *Asterocalamites*
(occurrence 209041, collection 22860) is the observed example; *Heidiphyllum*, *Taeniopteris* and
*Cladophlebis* in the extremely broad 538.8--201.4 Ma collection 222433 show the more severe
failure mode. Collection 222433 is identified in its own record as Middle Triassic. The reviewed
rule requires an accepted early-embryophyte category before B1 or B2 can be true. Collection 22860
remains through accepted co-occurring early plants, not through *Asterocalamites*.

### De-duplication mixed verified aliases with taxonomic resemblance

The v0 build replaced 21 PBDB collections with curated-tail rows. Seven replacements have explicit
collection or occurrence links and are defensible: collections 10594, 20754, 53919, 53920, 53660,
53664 and 14147. Even here, collection 53664 maps to the unresolved `M-yea-unspecified`; the alias
is real but the row does not establish an additional independent Yea horizon.

The other 14 replacements were inferred from some combination of country, age and a shared plant
name. That is not evidence of the same specimen, bed or locality. Direct counterexamples include:

- Targrove Quarry (10679) versus the unresolved site of the Lang tracheid axis;
- Perton Lane (10706) versus Freshwater East, listed as separate Pridoli localities;
- Suchomasty/Klonk (14043), Kosov Quarry (14045), Kolednik/Jarov Quarry (14131) and Zadni
  Kopanina (52698), which cannot all be collapsed into the *Cooksonia bohemica* specimen set merely
  because they are Czech Pridoli *Cooksonia* records;
- the Tokrau/Balkhash records, where named outcrops 1751, 1738 and 1737 are source-resolved units,
  but collection 53659 and several tail rows are regional lists compiled from overlapping
  literature; and
- Xiemisitai Bed 16 (278439), a named West Junggar bed that is not shown to be the same unit as the
  regional *Aberlemnia* tail record.

Unresolved cases are not promoted to certainty in the other direction. Podolia collections 13873
and 52702, Kosov collection 14045 and the Capel Horeb link for collection 153611 remain explicit
unit/link sensitivities. The reviewed primary retains source-resolved named localities, removes
regional checklist rows counted alongside them, and exposes plausible shared-locality cases as
collapses.

### PBDB collection numbers do not establish horizon independence

The plan defines a horizon as locality x bed. The v0 table had only collection identity and often
rounded locality coordinates. Battery Point alone contributes 24 PBDB collection rows in three
identical locality--age groups of 9, 9 and 6; no field in the table demonstrates 24 distinct beds.
The same mechanical check finds three rows at Beartooth Butte and two each at Burnotien,
Wiheries, Dundee and Williamsville. These are not proven duplicates, but neither are they proven
independent horizons. Treating every collection number as independent would narrow a range limit
through pseudoreplication.

The reviewed primary therefore collapses identical locality and age-range groups. Collection-level
counts remain a sensitivity, and region-stage collapse is the stronger dependence sensitivity.
Neither collapse repairs unknown bed identity; it measures how much the result depends on granting
independence to database rows.

### Pivotal oldest units need source-specific dependence and age treatments

The Czech *Cooksonia barrandei* fertile specimen supports B0/B1 but not B2. Its mid-Sheinwoodian
age is a reasoned correlation from a graptolite on the slab, other contents of the old collection,
lithology and relocated sterile fragments; it was not collected in place. Primary and
Sheinwoodian--Homerian age-route results should therefore be separate. The Hirnantian Zbrza axes
and sporangium-like bodies remain inclusive/outlier evidence: their association and land-plant
affinity are not secure enough for the main B1 history.

At Yea, the lower Ghin Ghin B3/Locality 1 horizon and B2 horizon 67 m above it are stratigraphically
distinct and should remain two units. Their Silurian age routes are disputed, so neither should be
assigned a fixed Gorstian age. The unidentified `M-yea-unspecified` row may be one of the mapped Yea
localities and adds no primary independent unit.

The secure 2026 *Zosterophyllum mangkeluense* specimen and the 1993 queried *Zosterophyllum* record
refer to the same named Mangkelu/Mongkelu section or general site. The available crosswalk does not
show whether they are separate beds. Keep the 2026 specimen as the primary B2 record; collapse the
1993 queried record in the primary analysis and reinstate it only as a bed-level uncertainty
sensitivity. The 1993 source itself warns that sterile branching fragments are insufficient for
assignment to *Zosterophyllum*.

### One source identifier conflated two 2026 papers

`library/closed/wang2026.pdf` is the cryptospore review, DOI
`10.1016/j.earscirev.2026.105476`. It is not the Annals of Botany paper describing
*Zosterophyllum mangkeluense*, DOI `10.1093/aob/mcaf337`, used by the occurrence source identifier
`wang2026`. The local PDF therefore cannot be cited as the held full text for the Mangkelu record.
The identifiers and provenance must remain separate: `wang2026-cryptospores` and
`wang2026-zosterophyllum`. The latter was checked through the journal web record, not through the
local cryptospore PDF.

## Stratified source check and evidential limits

The audit checked pivotal older records and a stratified set of later PBDB rows. It confirmed that
Rhynie collection 10721 is correctly one horizon despite its many taxa, and that accepted early
plant names can retain Wiheries collection 22860 after removing *Asterocalamites*. Later rows such
as Passage Gulf 20664, Balgavies 26755 and Hunsrueck 26904 are provisionally usable as PBDB-derived
density records, but their cited historical botanical sources were not re-read here. Collection
13895 is weaker: its cited collection reference is primarily stratigraphic/marine, and no
specimen-level botanical description was recovered in this bounded audit. It belongs in a strict
botanical-source exclusion sensitivity.

Two late Emsian--Eifelian collections, 10614 and 10617, cross the 393.47 Ma analysis edge. They may
affect the oldest admissible age within the window but cannot contribute a full certain horizon
count without conditioning on the in-window part of their age ranges. This is age censoring, not a
taxonomic disagreement.

## Verification and recommendation

`data/macro/source_adjudications.csv` records 48 auditable decisions with target, original and
adjudicated values, source locator, evidence, impact and confidence. The reviewed build records the
input/output hashes and dispositions in `data/macro/build_receipt.json`. These receipts establish
reproducibility of the transformation, not truth of every PBDB occurrence.

Proceed with the reviewed primary plus three predeclared sensitivity axes: collection versus
locality versus region-stage units; strict botanical-source versus PBDB-derived entries; and the
named uncertain material/age collapses in the adjudication ledger. Do not use the old 21-row
replacement set or call PBDB collection numbers independent horizons. The headline result should
be considered source-robust only if its qualitative clock comparison survives those axes and the
separate matched-coverage simulations.

Independent scientific review would materially improve confidence only for the few records that
control an endpoint or a large change in horizon count, especially the *C. barrandei* age route,
Yea correlations, Mangkelu bed equivalence and any database-only oldest B2 unit. Re-reading every
younger density source would be disproportionate unless the result proves sensitive to the strict
botanical-source exclusion. Residual uncertainty about bed independence cannot be eliminated from
the current database fields; it must remain in the inference.
