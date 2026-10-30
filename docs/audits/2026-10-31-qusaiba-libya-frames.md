# Qusaiba and Murzuq sampling-frame evidence

31 October 2026. Codex, with independent source scouts; Q1/Q2 and source-conflict
tracking under Q5. Held sources only. This tranche adds two candidate frames and
201 inventory entries, bringing `data/units/` to seven frames and 276 inventory
entries. The accepted material/outcome interface remains 49 blocks/294 rows.
No new binary outcomes, empirical reference rates or F3 bounds are released.

## 1. Qusaiba-1: a complete reference candidate, without older exposure

Wellman, Steemans & Miller (2015), methods pp.112–113 and Table 2 p.116, explicitly
enumerate all 37 processed spore samples. All are reported productive (p.122).
The table contains trilete marks in 22 columns and no trilete mark in 15. These
are literal reports, not 22 newly adjudicated main-reading positives and 15
adopted zeros. Complete category reporting provides a basis for a proposed
reported-encounter conversion after the event/reading audit.

The deepest sample, core 56 at 551.0 in Table 2, already reports *Ambitisporites
avitus* and *Aneurospora* sp. A. Plate IV.23 (caption p.122, image p.123) independently
locates *Aneurospora* at 551 ft, slide 64163, England Finder X42/3. The existing
occurrence reading accepts the core-56 *A. avitus* report under main. No sampled
pre-appearance interval lies below this deepest positive. The focused companion
stratigraphy places it in the late Katian, and no supported stage reading makes
any of these sampled deposits older than 459.1 Ma.

The 37 spore columns comprise 12 Quwarah, four basal Sarah, 20 Baq'a Shale and
one Baq'a Sandstone sample. Le Hérissé et al.'s author manuscript enumerates
40 acritarch samples (p.4, Fig.2 p.55): 36 exact numerical matches, one unresolved
302.11/302.40 pair, and three additional Rhuddanian depths at 254.8, 255.75 and
256.4 ft. `qusaiba_inventory.csv` preserves **41 reported depth records**, not
41 independent physical trials. Only the 37 spore-table entries enter
`frame_samples.csv`. The companion-only three are not spore negatives.

Material qualifications preserved in the inventory:

- **Depth units:** Table 2 labels its numbers in metres; the core log, plate
  captions and companion explicitly support feet. Both are recorded; no silent
  conversion or exact 302.xx material merge is made. The questioned `?341.0m`
  label also remains visible.
- **Ages:** the spore paper gives early-Katian and mid-Katian wording in different
  passages; the companion assigns the basal sample to late Katian and the broader
  Quwarah assemblage to late Katian–early Hirnantian. No exact numerical age or
  sample-specific Katian/Hirnantian boundary is invented.
- **Reporting:** prose about naturally dissociated spores groups hilate and trilete
  forms; it does not make every sample E1-positive. Two plate/table disagreements
  (*Chelinospora prisca* at 438.7 ft and *Aneurospora* at 452.75 ft) leave the union
  of E1-marked depths unchanged because other triletes occur in those columns.
- **Effort:** the 2009 supplement describes 10–25 g and 10 µm processing; the 2015
  paper describes approximately 30 g and 12 µm at Liège, plus selected Sheffield
  duplicates using 10 µm and no oxidation. Both report comparable duplicate
  preparations. Per-depth masses, exact duplicate membership and search effort
  are not recovered. Neither papers nor preparations are additional material trials.
- **Facies/reworking:** this sequence crosses shelf/delta, glacial and deglacial
  facies. Reworked Middle Ordovician acritarchs in younger Baq'a deposits do not
  supply sampled older depositional trials. Abundant marine palynomorphs establish
  productivity, not equal terrestrial-spore encounter probabilities across cores.

This is a useful candidate reference frame for Q1, subject to identification and
reporting rules. Pooling it with Hanadir or Borenshult would require explicit
reference transport, facies/effort and dependence assumptions. No such pooling
is adopted here.

## 2. Murzuq Basin: 164 declared samples, with a recoverable inventory conflict

Abuhmida's complete 2013 thesis states that 164 core/cutting samples were selected
from six wells (p.32); Appendix 1 (printed p.611, PDF p.627) describes the list as
all samples collected, prepared and analysed. An independent visual transcription
of its native raster confirms exactly 164 unique well/depth entries. Grey
unavailable-material cells and red unconformity bands are not samples.

The six palynomorph range-chart enclosures yield 158 explicit depth/type labels.
The repeated range/presence display panels are collapsed. Exactly 153 well/depth
keys match the appendix. The source components are retained separately in
`libya_appendix1.csv` and `libya_enclosures.csv`; neither is silently overwritten.

| Well | Appendix entries | Chart labels | Exact depth matches | Appendix-only depths (ft) | Chart-only depths (ft) |
|---|---:|---:|---:|---|---|
| A28i-NC186 | 24 | 24 | 22 | 4499.5, 4557.5 | 4500, 4558 |
| B2-NC186 | 17 | 17 | 17 | — | — |
| D1-200 | 39 | 35 | 35 | 5150, 5250, 5350, 5450 | — |
| E1-NC174 | 16 | 15 | 14 | 7150, 7200 | 6750 |
| H2-NC186 | 29 | 28 | 27 | 5250, 5300 | 5150 |
| I3-NC186 | 39 | 39 | 38 | 5230 | 5220 |
| **Total** | **164** | **158** | **153** | **11 entries** | **5 labels** |

A28i's half-foot differences are plausible rounding, and I3's 5230/5220 may be a
transcription difference; neither is an established physical-sample match. B2
4100 and 4200 are cuttings in Appendix 1 but labelled CO in the enclosure. The
appendix conservatively resolves 53 core, 105 cutting and six unspecified type
cells. Four unspecified types are labelled CU in the enclosures; the source
distinction is retained. Enclosure locators are printed pp.614, 616, 618, 620,
622 and 624 (PDF pp.630, 632, 634, 636, 638 and 640).

**Preparation and reporting.** Methods pp.32–37 specify cleaning, 20-g aliquots,
acid processing, 10-µm screening, variable 5–10 minute nitric-acid oxidation,
three to four palynological slides, a first-slide specimen census and scanning
of another slide. The separate 200-particle count is for palynofacies, not a
fixed 200-spore or palynomorph search. Samples were selected for suitable
lithology and availability; a complete declared laboratory set is not random
sampling of the basin or continuous stratigraphic coverage.

**Event and age evidence.** Assemblage descriptions pp.379–383 supply a useful
sequence: Darriwilian Hawaz cryptospores (Cr-1); late Katian–Hirnantian Cr-2,
explicitly characterised by absence of true triletes; a single *A. dilutus* in
E1-NC174 core 7287 ft assigned early Rhuddanian (Cr-3); and later Llandovery
triletes in Cr-4. The systematic account on pp.327–328 distinguishes a defined
laesura from the splitting in *Imperfectotriletes*, but gives mid-Rhuddanian–
Telychian occurrence wording, differing from the early-Rhuddanian Cr-3 passage.
Preserve the age statements separately. Cr-2's pooled absence has not been
copied onto every sample in its broad interval. Cr-1's taxon list alone is not
an explicit sample-by-sample E1 negative.

The thesis says Ash Shabiyat is palynomorph-barren (p.384); those eight appendix
entries remain in the inventory, subject to individual mapping. A range-chart
omission is neither a failure nor a target-negative report without more evidence.

**The main design issue is reference comparability.** All five clearly typed
younger Tanezzuft core samples in the appendix are in E1-NC174; the other 48
clearly typed cores are in older formations of other wells. Thus the unambiguous
appendix core subset does not supply both older and younger cores within one
well. A within-well analysis of D1, H2 or I3 would also rely on younger cuttings;
a core-only comparison would transport reference information across wells.
The B2 CO/CU conflict must be resolved before it alters that assessment.
Caving, preservation, shared ages and effort need explicit treatment in either
design. This is a source-derived design constraint, not an assumed correction.

## 3. Verification, structural review and next tranche

All five source-file hashes match the acquisition register. The three journal
DOIs were rechecked against Crossref by DOI, title and first author. The source
files remain local and git-ignored. The inventory receipt hashes all three new
evidence tables. `tools/units.py check` passes with seven candidate frames and
276 inventory entries; the material/outcome counts are unchanged.

The Qusaiba scout read methods, full tables, enlarged charts and pivotal plates,
and cross-checked table marks against PDF text coordinates. The Libya scout
transcribed Appendix 1 independently without seeing the enclosure extraction;
the parent compared the two inventories, verified methods/event passages and
rendered the inventory and selected chart evidence. This is not a full
sample-by-event extraction of the 641-page thesis.

The current structure serves the next investigation: complete declared inventories
can coexist with reporting gaps and contradictory source labels. These sources
move Q1 from finding a positive reference towards specifying a defensible
reference comparison. Q2 needs source-level taxonomic/reporting adjudication;
Q5 records internal source discrepancies here, without claiming a demonstrated
error propagated through the literature. No question becomes answered.

**Next owned tranche:** map the Libya event/productivity reports to the reconciled
inventory, keeping failures and core/cutting distinctions; then compare a declared
within-well core-plus-cutting design with a core-only cross-well design. Qusaiba
is a separately available positive-reference candidate. Design selection and
transport must be explicit before binding qualification, as discussed in
`2026-10-31-screen-and-persistence-review.md`. No acquisition retry or author
reply is required to make that progress.

## Sources read

- Abuhmida F (2013). Palynological analysis of the Ordovician to Lower Silurian sediments from the Murzuq Basin, southwest Libya. PhD thesis, University of Sheffield. [Repository record](https://etheses.whiterose.ac.uk/id/eprint/4475/). Complete held thesis; no DOI.
- Wellman CH, Steemans P, Miller MA (2015). Spore assemblages from Upper Ordovician and lowermost Silurian sediments recovered from the Qusaiba-1 shallow core hole, Qasim region, central Saudi Arabia. DOI: 10.1016/j.revpalbo.2014.09.003.
- Steemans P et al. (2009). Origin and Radiation of the Earliest Vascular Land Plants. DOI: 10.1126/science.1169659. Main text and supplement.
- Le Hérissé A, Molyneux SG, Miller MA (2015). Late Ordovician to early Silurian acritarchs from the Qusaiba-1 shallow core hole, central Saudi Arabia. DOI: 10.1016/j.revpalbo.2014.08.016. Held 73-page author manuscript; page locators above refer to that version.
