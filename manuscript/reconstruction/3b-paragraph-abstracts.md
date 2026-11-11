# Reconstruction step 3b: paragraph abstracts

Claude Opus 5.5 draft, revised by Codex (`gpt-6.1-sol`), 11 November 2026, built from the reconciled
step 3a at `dabd5b9`. Claude's original is preserved at `fca1069`. Barry's instruction (chat,
10 November 2026), in summary:
- first design the paragraph framework, one key message per paragraph;
- write a one-sentence summary of each paragraph, then check the order and the coverage of 3a;
- write each paragraph as "3–4 short, sharp sentences. No more!", with []-enclosed comments
  signposting the references to cite.

**Signpost conventions**
- `[@key]` is a work already in `references/refs.yaml`.
- `[cand: Author Year, DOI]` proposes a future bibliography entry. Claude reports Crossref identity
  checks on 10 November 2026; content-reading status is recorded below and in
  `codex-3b-reference-check.md`. Read the relevant source before using a candidate to support prose.
- `[S…]`, `[Fig. …]` and `[Table …]` point to the supplement and to display items from 1d.

Numbers retain their ledger bindings. The half-rate bound (431.0 Ma) still awaits ledger entry. The
framework has **27 paragraphs**: 5 in the Introduction, 8 in Material and methods, 8 in Results and 6
in the Discussion. A 150-word average would give about 4,050 words; the eventual paragraph lengths
follow their content. The nearest *Proc B* comparators run 5,300–5,900 words.

---

## Introduction

### Framework

| ¶ | Key message (one sentence) |
|---|---|
| I1 | Recent clocks disagree by tens of millions of years on when living land plants and vascular plants shared their ancestors, and the dates matter for plant and Earth history. |
| I2 | Absence-based maxima require recovery assumptions, and soft bounds express uncertainty about older ages. |
| I3 | Two uncertain intervals separate an ancestor from its first recognisable fossil, and early land plants make both hard to bound. |
| I4 | The three maxima that divide current clocks rest on different kinds of evidence. |
| I5 | Three questions, each with an expectation from established theory, ask what those maxima require of the record. |

**Order.** The sequence runs from the problem (I1), to one source of the disagreement (I2), to the
limits of maxima in this setting (I3), to the specific cases (I4), to the questions (I5). Each paragraph needs the
one before it.

**Coverage of 3a.**
- The clock intervals, Hooper's recalibration and "extinct lineages earlier" are in I1.
- The minimum/maximum distinction is in I2.
- Marshall's two intervals, spores before bodies, and scarce deposits in western Europe are in I3.
- The three maxima are in I4.
- The questions, their expectations and the closing aim are in I5.
- Added beyond 3a: soft bounds and calibration best practice in I2, as context the comparators
  carry.

### Paragraph abstracts

**I1.** Molecular clocks combine DNA differences and fossil age limits to date shared ancestors.
Morris et al., Harris et al. and Hooper et al. place the ancestor of living land plants at
515–474, 515–493 and 457–450 million years ago (Ma), respectively. Their intervals for vascular
plants (ferns, seed plants and relatives) are 451–419, 452–447 and 432–428 Ma; Hooper reused
Harris's DNA with revised calibrations, moving the land-plant mean 55 Myr younger. These dates
frame hypotheses about plant character assembly, weathering and climate; extinct lineages may
have occupied land earlier.
[@morris2018TimescaleEarlyLand; @harris2022DivergentEvolutionaryTrajectories;
@hooper2026ReconstructingSporeEvolution; @su2021LargescalePhylogenomicAnalyses;
@kenrick2012TimelineTerrestrializationConsequences; @donoghue2021EvolutionaryEmergenceLand;
@strother2021FossilRecordLand; cand: Lenton 2012, 10.1038/ngeo1390; Fig. 1]

**I2.** A fossil minimum shows that a lineage existed by a given age. An absence-based maximum
adds an argument that older rocks would probably have preserved and yielded recognisable remains
had the lineage existed. A soft maximum permits older ages through a specified tail of the
calibration prior. Whether absence can set a maximum is contested, and best practice asks each
calibration to state its justification.
[cand: Benton 2006, 10.1093/molbev/msl150; cand: Yang 2005, 10.1093/molbev/msj024; cand: Ho 2009,
10.1093/sysbio/syp035; cand: Parham 2011, 10.1093/sysbio/syr107; @hedges2018AccurateTimetreesRequire;
@morris2018ReplyHedgesEt; cand: dos Reis 2015, 10.1038/nrg.2015.8]

**I3.** Linking a fossil to an ancestor crosses two intervals: from divergence to the first
recognisable character, and from that character to its first recorded fossil. Both remain
uncertain for early land plants. Dispersed spores precede branched bodies by tens of millions of
years, and terrestrial deposits in western Europe are scarce before the latest Silurian. The
oldest well-known parent plants are minute.
[@marshall2019UsingFossilRecord; @wellman2000MicrofossilRecordEarly; cand: Rubinstein 2010,
10.1111/j.1469-8137.2010.03433.x; cand: Steemans 2009, 10.1126/science.1169659;
@kenrick2012TimelineTerrestrializationConsequences; @edwards2014CryptosporesCryptophytesReveal;
cand: Kenrick 1997, 10.1038/37918]

**I4.** Morris et al. set 515.5 Ma for living land plants. They argued that older marine rocks
rich in algal cysts would also have yielded land-plant spores. Hooper et al. set 459.1 Ma from
the oldest possible trilete (three-rayed) spores, and 431.2 Ma for vascular plants from Irish
*Cooksonia*. The three maxima therefore rest on a preservation analogy, on dispersed spores and
on plant bodies.
[@morris2018TimescaleEarlyLand; @morris2018ReplyHedgesEt; @hooper2026ReconstructingSporeEvolution;
@rubinstein2019BalticaCradleEarly; @edwards1980RecordsCooksoniatypeSporangia; Table 1]

**I5.** Our retrospective questions ask what supports each maximum, what Libyan spores
constrain, and which rates of recording identifiable fossils or diagnostic delays accommodate
older vascular-plant ancestors. Absence arguments require documented opportunities for delivery,
preservation and discovery. With comparable exposure, accumulating zeros increasingly constrain
high sustained spore encounter. At fixed oldest age, younger cutoff and recording history,
additional independent finds narrow the start bound; reducing earlier recording extends it.
[@strauss1989ClassicalConfidenceIntervals; @marshall1990ConfidenceIntervalsStratigraphic;
@marshall2019UsingFossilRecord; cand: Parham 2011, 10.1093/sysbio/syr107]

---

## Material and methods

### Framework

| ¶ | Key message (one sentence) |
|---|---|
| M1 | All analysed ages share one timescale, and disputed identifications enter as named readings. |
| M2 | Each maximum was audited from its original sources. |
| M3 | The Libyan frame compares 28 older cuttings with 59 younger reference cuttings from one high-latitude basin. |
| M4 | An encounter model converts the cutting reports into limits on older spore input, qualified by simulation. |
| M5 | Locality–age groups provide proxy units for three nested body-fossil categories. |
| M6 | A range-confidence method gives a conditional older bound on when the recognisable record began. |
| M7 | Six fixed recording histories are compared with the observed age sequence. |
| M8 | A retrospective step and an assumed delay size what older ancestors require. |

**Order.** Shared conventions come first (M1), then the three analyses in the order the Results report
them: audit (M2), spores (M3–M4), bodies (M5–M8). The body method moves from data to estimator,
then to the histories that test it, then to what it requires.

**Coverage of 3a.** Ages and audit are in M1–M2. The spore data and model are in M3–M4, including
the simulation qualification rule against the 0.93 floor. The body inventory and units are in M5, the formula and age envelope in M6,
the six histories and the Kolmogorov–Smirnov search in M7, and the step, contrast and delay in M8.
Added: the polar setting (M3), and the statement that the bound is a confidence statement (M6).

### Paragraph abstracts

**M1.** Analysed ages use stage bases from the International Commission on Stratigraphy's chart
(ICS v2024/12), mapping literature ages by stage. Published maxima keep their source timescale,
the Geologic Time Scale 2012 (GTS2012), so they can be compared as their authors set them. Each
analysis declares its reading of disputed identifications, main or inclusive, so contested
fossils enter as alternatives.
[cand: Cohen 2013, 10.18814/epiiugs/2013/v36i3/002, chart v2024/12; cand: Gradstein 2012,
10.1016/C2011-1-08249-8; `data/timescale.csv`]

**M2.** For each maximum we traced the calibration fossil, its age rule and its recovery route
to the original descriptions. We recorded each published reading of the fossil's identity and
the evidence it cites. Non-detections apply to the material examined. A missing report becomes a
zero only after a full reporting audit.
[@morris2018TimescaleEarlyLand; @hooper2026ReconstructingSporeEvolution; primary descriptions in R1–R2;
cand: Parham 2011, 10.1093/sysbio/syr107]

**M3.** Abuhmida (2013) reported palynology from Ordovician to lower Silurian wells in the
Murzuq Basin, southwest Libya; we transcribed all [164]{.C38} appendix samples. The primary
frame uses the chart-coded cuttings (drilled rock chips) of five wells: [28]{.C01} older than
the Llandovery and [59]{.C02} Llandovery reference cuttings. The basin lay near the Ordovician
South Pole, in the region affected by Hirnantian glaciation.
[@abuhmida2013PalynologicalAnalysisOrdovician; @cocks2021OrdovicianPalaeogeographyClimate;
@scotese2021PhanerozoicPaleotemperaturesEarths; Fig. 3a]

**M4.** Each cutting reports trilete spores through an encounter process with a shared effect
for each well. Older input is a fraction *f* of reference input, and a fixed delivery ratio *ρ*
covers transport, preservation and preparation. Ages are uniform within stages, and limits are
computed for constant input and for the exposure-weighted mean of bounded variable histories. On
a declared finite scenario grid, a two-stage simulation rule accounts for Monte Carlo
uncertainty and qualifies coverage against a 0.93 floor conditional on passing the potential
screen.
[S2; S2.5]

**M5.** We assembled land-plant body fossils dated to 453–393 Ma from classified Paleobiology
Database occurrences and a source-reviewed set of the oldest records. Collections, taxa or
papers sharing a locality–age key count once, as proxies for independent fossil horizons. Three
nested categories carry competing readings: land-plant bodies, branched plants bearing multiple
spore capsules (polysporangiophytes), and crown vascular plants (clubmoss relatives, ferns and
seed plants). Crown vascular plants supply [50]{.C25} possible units and [48]{.C25} certain
units within the window.
[PBDB download as a dataset citation; @wellman2003FragmentsEarliestLand;
@libertin2018SporophytesPolysporangiateLand; @kotyk2002MorphologicallyComplexPlant;
@earp2024NotanopliidBrachiopodsAssociated; @libertin2024GenusAberlemniaSiluriandevonian; S5.1; Table 1]

**M6.** Above the end-Emsian cutoff $c=393.47$ Ma, cumulative exposure is $U(a)=\int_c^a
w(s)\,ds$ for fixed relative recording rate $w$. The one-sided 95% older bound $T$ on record
start solves $U(T)=U(A)\,0.05^{-1/n}$, with oldest age $A$ and count $n$. Constant recording
gives the classical confidence interval on a stratigraphic range. Age ranges enter through the
greatest possible oldest age and the minimum count guaranteed inside the window.
[@strauss1989ClassicalConfidenceIntervals; @marshall1990ConfidenceIntervalsStratigraphic;
@marshall1994ConfidenceIntervalsStratigraphic; @wang2016AdaptiveCredibleIntervals; Fig. 2]

**M7.** Six fixed histories use constant recording, two collection-density proxies, exponential
declines into the past over 25 or 10 Myr, and plant-excluded density times the 10 Myr decline.
The collection proxies count Paleobiology Database land and marginal-marine collections per Myr,
including or excluding plant matches. Finite-sample Kolmogorov–Smirnov tests condition on count
and oldest find, searching every admissible age allocation and cutoff-inclusion state.
Conservative rejection of that fixed history for this diagnostic requires failure throughout
those supports, independent continuous ages, and supports containing the true ages and inclusion
state with probability one under the observation model.
[@marshall1997ConfidenceIntervalsStratigraphic; S5.2 for the support-containment argument;
@berger1994PValuesMaximized as a related nuisance-parameter method]

**M8.** The primary step uses constant later recording and lowers earlier recording before
[426.7]{.C32} Ma, the oldest possible crown-member find. The recording contrast is the
later-to-earlier rate ratio that puts candidate ancestor age minus assumed diagnostic delay on
the record-start contour. The step was placed after inspecting the record. Longer assumed delays
reduce the recording contrast required for a given candidate age.
[@marshall2019UsingFossilRecord; Fig. 2; Fig. 4b; S5; evaluate contours only where candidate age minus
assumed delay is older than the oldest possible find, as specified in 1d]

---

## Results

### Framework

| ¶ | Key message (one sentence) |
|---|---|
| R1 | The 515.5 Ma maximum rests on a qualitative preservation control and affinity judgements about Cambrian spore-like packets. |
| R2 | The younger maxima apply a stage-base rule, and an older Czech fossil is a further candidate anchor. |
| R3 | The Libyan zeros limit sustained constant input from 459.1 Ma to about a tenth of the reference under equal delivery. |
| R4 | Those limits chiefly concern the later Ordovician, after the 459.1 Ma maximum. |
| R5 | Primary constant and collection-density recording histories give body-record bounds near 429 Ma, while declining histories change bounds and age-sequence fit. |
| R6 | Alternative units or a curated inventory move the constant-recording bound across 431.2 Ma, exceeding the tested timescale shifts. |
| R7 | Older ancestors need earlier recording several times lower, or a long delay before recognisable bodies. |
| R8 | One Ordovician fragment assemblage moves the broader land-plant bound by about 20 Myr. |

**Order.** Results follow the questions: calibration evidence (R1–R2, Q1), spores (R3–R4, Q2) and
bodies (R5–R8, Q3). Within the body results, the bound comes first, then its sensitivity, then what
older ancestors require, and last the broader category.

**Coverage of 3a.**
- All calibration findings are in R1–R2.
- The Libyan counts and the three limits are in R3; the 18 younger cuttings are in R4.
- The primary bounds and the 10 Myr decline are in R5; the unit and timescale ranges are in R6.
- The half-rate bound, the contrasts and the delays are in R7; Oman is in R8.
- Added: the constant-history delivered-encounter product (R3), the Darriwilian age supports (R4) and the recovery route of
  the Oman fragments (R8), all from the frozen article.

### Paragraph abstracts

**R1.** Morris et al.'s 515.5 Ma maximum uses older marine algal cysts as a preservation control
for land-plant spores. The control shows that walled microfossils survived and were recovered.
Spore delivery, catchment and search effort remain unquantified in the sources assessed. All
[three]{.C15} sources examined assign the Cambrian spore-like packets to algae or pre-land-plant
lineages.
[@morris2018TimescaleEarlyLand; @morris2018ReplyHedgesEt; @strother2016SystematicsEvolutionarySignificance;
@taylor2024UltrastructureCambrianCryptospores; @wang2022PalynologicalAssemblageCambrian;
@strother2021FossilRecordLand; S4; Table 1]

**R2.** Hooper et al. set both younger maxima as a GTS2012 stage base plus its uncertainty. They
keyed 459.1 Ma to a possible trilete in the Borenshult-1 core, Sweden; definite triletes from
the same Sandbian stage give the same value. They keyed 431.2 Ma to Irish Homerian *Cooksonia*.
The older Czech *Cooksonia barrandei* is a candidate under the same character criterion, with a
current-scale stage-rule outer value of [434.1]{.C47} Ma.
[@hooper2026ReconstructingSporeEvolution; @rubinstein2019BalticaCradleEarly;
@edwards1980RecordsCooksoniatypeSporangia; @libertin2018SporophytesPolysporangiateLand; S2.4; Table 1]

**R3.** Trilete spores occur in [51 of 59]{.C02} reference cuttings and in zero of [28]{.C01}
older cuttings. At a start of 459.1 Ma and equal delivery, the upper compatibility limit is
[0.091]{.C24} of reference input for constant histories, and [0.184]{.C24} for exposure-weighted
mean input over bounded variable histories. With delivery at a tenth of the reference, constant
input near the reference fits ([0.910]{.C24}). For constant histories, the constrained quantity
is the product of delivery and source input.
[@abuhmida2013PalynologicalAnalysisOrdovician; Fig. 3b]

**R4.** Most older exposure comes from [18]{.C45} Katian–Hirnantian cuttings wholly younger than
459.1 Ma. Only [10]{.C45} broadly dated Darriwilian cuttings in two wells have age supports
extending before the maximum. Their contribution to exposure at a start of 459.1 Ma depends on
the within-stage age treatment. The limits therefore chiefly concern the later Ordovician in one
high-latitude basin.
[@abuhmida2013PalynologicalAnalysisOrdovician; Fig. 3a; S2]

**R5.** The [48]{.C25} crown vascular-plant units give a one-sided 95% older bound of
[428.8]{.C27 .V003} Ma under constant recording. Histories tracking collection density give
[428.5]{.C27 .V010}–[428.9]{.C27 .V009} Ma, and a 25 Myr decline into the past gives
[431.6]{.C27 .V011} Ma. The pure 10 Myr decline leaves record start unresolved through 469.4 Ma
and fails the shape diagnostic under every admissible age allocation[]{.C49}.
[Fig. 4a; S5; S5.2]

**R6.** Alternative units or a curated inventory move the constant-recording bound across 431.2
Ma. Coarser region–stage units or the curated oldest-record set give [432.4–434.05]{.C30} Ma,
older than the 431.2 Ma maximum. Shifting stage boundaries for primary units in the tested
shared-boundary scenarios gives [427.31]{.C50 .V062}–[430.42]{.C50 .V063} Ma. Among these
scenarios, unit treatment moves the bound more than the tested timescale perturbations.
[Fig. 4a; S5.3]

**R7.** In the primary step with constant later recording, halving earlier recording gives 431.0
Ma, younger than the 431.2 Ma maximum. With zero assumed delay, candidate ancestors at 444–452
Ma, spanning the Morris et al. mean dates and the Harris et al. interval, need earlier recording
[8]{.C48 .V054}–[12]{.C48 .V055} times lower. Alternative units reduce that contrast to
[2.4]{.C48 .V056}–[4.5]{.C48 .V057} times. Alternatively, constant recording needs assumed
delays of at least [15–23]{.C33} Myr between ancestor and recognisable bodies.
[Fig. 4b; @marshall2019UsingFossilRecord; S5; half-rate value to be entered in the ledger]

**R8.** Adding Oman's Katian sporangial fragments (spore capsules) moves the broader land-plant
bound under constant recording from [434.5]{.C28} to [455.2]{.C40 .V022} Ma. The augmented
sequence fails the conditional shape diagnostic under all six fixed histories[]{.C49}. The
fragments came from palynological preparation of borehole material. This inventory combines
those fragments with later body fossils collected from bedding planes.
[@wellman2003FragmentsEarliestLand; @edwards1979RecordsFertileRhyniophytina; S5.2]

---

## Discussion

### Framework

| ¶ | Key message (one sentence) |
|---|---|
| D1 | The record constrains two specific histories, and each admits its own route to older ancestors. |
| D2 | Biological and recovery processes offer possible routes to lower earlier recording, with their separate contributions left open. |
| D3 | Earlier fossil-based estimates target different quantities and complement this assessment. |
| D4 | The results rest on stated conditions, gathered here once. |
| D5 | Four kinds of published evidence would narrow the compatible histories. |
| D6 | Clock builders can state and test the assumptions behind each maximum; older dates fit the fossil record under stated conditions. |

**Order.** Interpretation (D1), mechanism (D2), relation to the literature (D3), conditions (D4),
evidence that would sharpen the result (D5), and the recommendation and main message (D6). The
conditions paragraph follows the interpretation so that D1–D3 read as positive findings, and precedes
D5, which answers it.

**Coverage of 3a.**
- The two constrained histories and their routes are in D1.
- Rarity, range, searching and tissue traits are in D2.
- Silvestro and CladeDate are in D3.
- The spore and body assumptions, block weighting and the retrospective step are in D4.
- The four evidence types are in D5.
- The recommendation, the transfer to other maxima and the main message are in D6.
- Added: an early branched sporophyte from marine rocks (D2), and soft-bound practice (D6).

### Paragraph abstracts

**D1.** The record constrains two specific histories: sustained local trilete input in one polar
basin, and the start of the recognisable vascular-plant body record. For spores, lower delivery
or producers outside the catchment accommodate older ancestors. For bodies, lower earlier
recording or later diagnostic features accommodate them. The quantitative requirements describe
aggregate input, recording and delay scenarios.
[Fig. 3b; Fig. 4b]

**D2.** Rarity, restricted ranges and limited searching would lower the frequency of recorded
occurrences. Body size, cuticle and lignified tissue could also affect preservation and
recognition. *C. barrandei* is preserved in marine sediments, while Oman's fragments demonstrate
preservation of small sporangia (spore capsules). The models quantify combined recording
requirements, leaving the contribution and plausibility of each process open.
[@kenrick2012TimelineTerrestrializationConsequences; @edwards2014CryptosporesCryptophytesReveal;
@libertin2018SporophytesPolysporangiateLand; @wellman2003FragmentsEarliestLand;
cand: Kenrick 1997, 10.1038/37918]

**D3.** Silvestro et al. estimated the origin of vascular plants near 433.5 Ma from genus
occurrences with fitted preservation rates. Their genus-origin estimates and our fixed-history
category bounds target different quantities from overlapping data. CladeDate builds calibration
densities from fossil times, and Hooper et al. link spore-character reconstruction to revised
calibrations. We quantify what the specific maxima that divide current clocks require of the
record.
[@silvestro2015RevisitingOriginDiversification; @claramunt2022CladedateCalibrationInformation;
@hooper2026ReconstructingSporeEvolution]

**D4.** The spore limits assume an indigenous younger reference, comparable reporting, uniform
within-stage ages, and cuttings independent given a well effect. Weighting cuttings by well and
formation gives an exploratory contour near [0.4]{.C51 .V081}, with coverage unqualified.
Mapping local encounter to ancestors requires recognisable trilete production, persistence of
the trait and producers in the catchment. The body bounds assume independent units, true ages
within recorded ranges and the stated histories; the rate step is retrospective, and mapping
bodies to ancestors requires crown membership and a specified diagnostic delay.
[Table 2 (optional); @hooper2026ReconstructingSporeEvolution; S2.5; S5; S6]

**D5.** Four kinds of published evidence would narrow these histories. Searched Silurian
terrestrial beds with stated effort would help constrain early recording opportunities. A second
complete older-zero, younger-positive spore sequence outside polar Gondwana would test the
generality of the spore result. Finer ages for the Yea (Australia) and Bathurst Island (Canada)
horizons would refine the body bound; character evidence could revise the oldest branched
plants' crown-membership assignments.
[cand: Peters 2018, 10.1029/2018GC007467 (consider for rock-availability context after reading);
@earp2024NotanopliidBrachiopodsAssociated;
@kotyk2002MorphologicallyComplexPlant; @libertin2018SporophytesPolysporangiateLand]

**D6.** Clock builders can state each maximum's character, geographical and recording
assumptions, and justify the probability assigned to older ages against them. Testing
alternative defensible maxima then shows how much each assumption moves the timescale. This
separation of evidence, recording and mapping applies to any maximum argued from absence. Older
dates for living land plants fit the fossil record if early plants were found several times less
often, or recognisable features evolved later.
[cand: Parham 2011, 10.1093/sysbio/syr107; cand: Ho 2009, 10.1093/sysbio/syp035; cand: Brown 2017,
10.1093/sysbio/syx074; cand: dos Reis 2015, 10.1038/nrg.2015.8]

---

## Notes for review

- **Reference coverage.** The signposts identify 34 existing works and 13 additional candidate works.
  The 52–75 references in the *Proc B* comparators prompt a coverage check; sources enter for the
  claims or methodological comparisons they support. The additional candidates cover:
  - calibration practice and soft bounds (Benton, Yang, Ho, Parham, dos Reis, Brown);
  - early spore evidence (Rubinstein 2010, Steemans 2009);
  - plant phylogeny and terrestrialisation (Kenrick 1997);
  - weathering and climate (Lenton 2012);
  - macrostratigraphy (Peters 2018);
  - the timescale (Cohen 2013, Gradstein 2012).

  Relevant original sections of Yang and Rannala and Parham et al. were read during this review for
  I2's definition and justification requirement. Other additional candidates remain unread in this
  review. The Peters signpost is provisional rock-availability context, pending reading; D5 makes
  the narrower inference that documented searches could constrain recording opportunities.
  Strother 2021 was already `@strother2021FossilRecordLand`, so its duplicate candidate signpost is
  replaced by that key. Wilkinson was read as a distinct fossil-informed-prior precedent; it is
  omitted from D3 because its present sentences need the closer plant comparison and CladeDate.
  The bounded primary-source reads and access limits are in `codex-3b-reference-check.md`.
  Add candidates to `references/dois.txt` when their relevant content has been read and cited in full
  prose; the bibliography stays frozen in this step.
- **Crossref years** differ from the familiar volume years for Parham (2011 online, 2012 volume),
  Yang (2005/2006), Benton (2006/2007), dos Reis (2015/2016), Brown (2017/2018) and Wilkinson
  (2010/2011). `refs.py build` takes the registered metadata.
- **Paragraph contract.** There are 27 paragraph abstracts, each with 3–4 sentences, excluding the
  citation signposts. I5 and M7 now use ordinary sentences, so their counts include every question
  and history without treating question marks as list punctuation. The eventual 150-word average is
  a budget estimate; expansion follows the evidence needed by each paragraph.
- **Review dispositions for reconciliation:**
  - Keep R5 and R6 separate. R5 reports the primary conditional bounds; R6 shows that unit or inventory
    treatment crosses the comparator maximum and scopes the smaller tested timescale shifts.
  - Omit Wilkinson from D3 unless a later revision explains its distinct branching-and-sampling
    contribution. A citation alone adds no comparison.
  - I2 defines a soft calibration prior with Yang and Rannala and cites Parham for justification.
    The unsupported prevalence claim is removed.
  - Keep Conditions at D4, after the interpretation and methodological comparison and before the
    evidence that would sharpen the results. Base treatments remain explicit in Methods; Conditions
    gathers their inferential limits. The support-containment argument in M7 is this study's own
    justification, with Berger and Boos signposted as related work.
- **Pending full prose.** Bind the independently checked half-rate value in the ledger before using
  it in a canonical product. Preserve the domain and case labels in the body sensitivities and
  distinguish aggregate scenario requirements from separately measured biological mechanisms.
