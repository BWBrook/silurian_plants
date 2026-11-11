# Reconstruction step 3c: full draft

Claude Opus 5.5 draft, revised by Codex (`gpt-6.1-sol`), 11 November 2026, expanded from the reconciled
step 3b at `2169670`. Claude's original is preserved at `c0f83fc`. Barry's
instruction (chat, 11 November 2026): "add the flesh to the bones. But do it judiciously. Don't
overwrite!" Numbers carry ledger bindings. Citation keys resolve in `references/refs.yaml`; source-reading
provenance and its review limits are recorded in the drafting notes. The frozen
canonical products in `manuscript/text/` stay unchanged until this draft is reviewed.

---

# When did living land plants arise? What their fossil age limits require

## Abstract

Three recent molecular clocks place the ancestor of living land plants between the Cambrian and Late
Ordovician, using different fossil maximum ages. We examined three such maxima:
515.5 and 459.1 million years ago (Ma) for living land plants, and 431.2 Ma for living vascular plants
(ferns, seed plants and relatives).
We audited their sources, modelled spore reports from Libyan wells and bounded the start of the
vascular-plant body record. The oldest maximum rests on a qualitative preservation argument. In Libya,
trilete spores occur in [51 of 59]{.C02} younger well cuttings (rock chips) and zero of [28]{.C01} older ones; with
equal delivery, constant local spore input from 459.1 Ma fits at up to [0.091]{.C24} of the younger
level. For vascular-plant bodies, constant recording gives a one-sided 95% older bound of
[428.8]{.C27 .V003} Ma, and alternative units give [432.4–434.05]{.C30} Ma. Assuming recognisable bodies
appeared at the ancestor's age, ancestors at 444–452 Ma fit if earlier bodies were recorded
[8]{.C48 .V054}–[12]{.C48 .V055} times less often, or [2.4]{.C48 .V056}–[4.5]{.C48 .V057} times under
alternative units. Older dates for living land plants fit the fossil record if early plants were found
several times less often, or recognisable features evolved later.

## 1. Introduction

Molecular clocks estimate when lineages diverged by combining DNA differences with fossil limits on
the ages of selected ancestors. For the ancestor shared by all living land plants (crown embryophytes),
@morris2018TimescaleEarlyLand obtained 515–474 Ma across seven topologies and
@harris2022DivergentEvolutionaryTrajectories obtained 515–493 Ma.
@hooper2026ReconstructingSporeEvolution reanalysed Harris et al.'s DNA data with revised fossil
calibrations and obtained 457–450 Ma, a mean 55 Myr younger. For the ancestor of living vascular
plants (crown tracheophytes: clubmosses and their relatives, ferns and seed plants), the three studies
give 451–419, 452–447 and 432–428 Ma (Fig. 1); @su2021LargescalePhylogenomicAnalyses obtained older
land-plant ages still, under a Proterozoic maximum. These dates bear on the order in which plant
characters were assembled, and on hypotheses about early terrestrial productivity, weathering and climate
[@kenrick2012TimelineTerrestrializationConsequences; @donoghue2021EvolutionaryEmergenceLand;
@strother2021FossilRecordLand; @lenton2012FirstPlantsCooled]. They date the ancestors of living plants; extinct
lineages may have occupied land earlier.

A fossil sets a minimum age: its lineage existed by the age of its oldest secure member. An absence-based maximum
adds an argument from absence, that older rocks would probably have preserved and yielded recognisable
remains had the lineage existed [@benton2006PaleontologicalEvidenceDate]. How calibrations are
specified can strongly shape the estimated dates, and with large sequence datasets the calibrations can
dominate the uncertainty in absolute ages [@ho2009AccountingCalibrationUncertainty;
@dosreis2015BayesianMolecularClock]. A soft maximum permits older ages through a
specified tail of the calibration prior [@yang2005BayesianEstimationSpecies]. Whether absence can set a
maximum is contested [@hedges2018AccurateTimetreesRequire; @morris2018ReplyHedgesEt], and best practice
asks each calibration to justify its maximum from the relevant geological, geographical and taphonomic
record [@parham2011BestPracticesJustifying].

Linking a fossil to an ancestor crosses two intervals: from divergence to the first recognisable
character, and from that character to its first recorded fossil [@marshall2019UsingFossilRecord].
Early land plants make both uncertain. Dispersed spores appear tens of millions of years before
branched plant bodies [@wellman2000MicrofossilRecordEarly; @rubinstein2010EarlyMiddleOrdovician; @steemans2009OriginRadiationEarliest],
terrestrial deposits are scarce before the latest Silurian, at least in western Europe
[@kenrick2012TimelineTerrestrializationConsequences], and the oldest parent plants known in detail are
minute [@edwards2014CryptosporesCryptophytesReveal]. Three kinds of fossil therefore bear on the
maxima: dispersed spores with a particular wall or mark, spore capsules (sporangia) and other fragments, and bodies
diagnostic enough to place within a crown group. Each has its own phylogenetic meaning and its own route
into the record.

Three maxima divide the current clocks (Table 1). Morris et al. set 515.5 Ma for living land plants,
arguing that older marine rocks rich in algal cysts would also have yielded land-plant spores
[@morris2018TimescaleEarlyLand; @morris2018ReplyHedgesEt]. Hooper et al. set 459.1 Ma from the oldest
possible trilete (three-rayed) spores, in the Borenshult-1 core of southern Sweden
[@rubinstein2019BalticaCradleEarly], and 431.2 Ma for living vascular plants from Irish *Cooksonia*
[@edwards1980RecordsCooksoniatypeSporangia]. The three maxima therefore rest on a preservation analogy,
on dispersed spores and on plant bodies, and each calls for its own test.

We ask three retrospective questions. What evidence supports each maximum, and which links connect it
to the dated ancestor? How much sustained spore input before the Silurian do the records of one Libyan
basin allow? Which rates of recording identifiable fossils, or which delays before recognisable bodies,
accommodate older vascular-plant ancestors? Established theory sets an expectation for each. An absence
argument requires documented opportunities for delivery, preservation and discovery
[@parham2011BestPracticesJustifying; @marshall2019UsingFossilRecord]. With comparable exposure,
accumulating zero records increasingly constrain high sustained spore encounter. For a fixed oldest
find, younger cutoff and recording history, more independent finds narrow the bound on when a record
began, and lower earlier recording extends it [@strauss1989ClassicalConfidenceIntervals;
@marshall1990ConfidenceIntervalsStratigraphic]. We quantify these requirements at the maxima that divide
the clocks.

**Table 1.** The three maxima: the evidence each rests on, the test the record allows, and the links
that remain to be assumed.

| Maximum | Set by | Evidence | Test available | Links assumed |
|---|---|---|---|---|
| 515.5 Ma, living land plants | Morris et al. | Base of the *Olenellus* Biozone, below the oldest possible Cambrian spore-like packets; older marine sequences with algal cysts | Affinity of the Cambrian packets; any enumerated older sequence | Spore delivery to marine basins, catchment, search effort, spore production by the earliest crown members |
| 459.1 Ma, living land plants | Hooper et al. | GTS2012 Sandbian base plus uncertainty, keyed to the oldest possible trilete (Borenshult-1, Sweden) | Older zeros against younger positives in the Murzuq Basin, Libya | Crown status of trilete producers, persistence of the trait, producers in the catchment |
| 431.2 Ma, living vascular plants | Hooper et al. | GTS2012 Homerian base plus uncertainty, keyed to Irish Homerian *Cooksonia* | A bound from the positive body record, and the requirements of older ancestors | Recording before the oldest find, delay before recognisable bodies, crown membership of the anchor |

## 2. Material and methods

**(a) Timescale and readings.** Analysed ages use the stage bases of the International
Chronostratigraphic Chart, v2024/12 [@cohen2013IcsInternationalChronostratigraphic]. Literature ages were mapped by stage, keeping
source-specific statements. Published maxima keep their source timescale, the Geologic Time Scale 2012
(GTS2012), so they can be compared as their authors set them. Each analysis
declares its reading of disputed identifications, main or inclusive, so that contested fossils enter as
alternatives.

**(b) Source audit.** For each maximum we traced the calibration fossil, its age rule and its recovery
route to the original descriptions, and recorded each published reading of the fossil's identity with
the evidence cited for it [@parham2011BestPracticesJustifying]. A reported non-detection applies to the
material examined. A missing report became a zero only after we had confirmed that the source reports
the target fully.

**(c) Libyan spore records.** @abuhmida2013PalynologicalAnalysisOrdovician reported palynology from
Ordovician to lower Silurian wells in the Murzuq Basin, southwest Libya. We transcribed all
[164]{.C38} appendix samples with their chart and prose reports. The primary frame uses the chart-coded
cuttings (rock chips returned during drilling) of five wells: three supply [28]{.C01} cuttings older
than the Llandovery, and all five supply [59]{.C02} Llandovery reference cuttings. For part of the
sequence the source states the absence of trilete spores explicitly; for the Hawaz Formation, the zeros
rest on complete reporting charts and the stated microscopy protocol. The basin lay near the Ordovician
South Pole, in the region affected by Hirnantian glaciation
[@cocks2021OrdovicianPalaeogeographyClimate; @scotese2021PhanerozoicPaleotemperaturesEarths] (Fig. 3a).

**(d) Spore encounter model.** We jointly fitted the reference encounter rate and older input,
integrating a mean-one gamma-distributed effect shared by older and reference cuttings within each
well (shape and rate both two). Cutting outcomes are independent conditional on this effect and
their ages, which are uniform within each cutting's stage range. Older input is a fraction *f* of
Llandovery reference input; a fixed delivery ratio *ρ* covers differences in transport, preservation
and preparation. We computed upper 95% compatibility limits for constant input and the exposure-weighted
mean of variable histories beginning at a postulated start, with input constrained between zero and
the reference level in both classes. A potential screen requires a
usable younger reference and a frame capable of excluding constant reference-level input when all
older cuttings are exposed and their outcomes are set to zero. The same screen is applied in every
simulation; the analysis uses the actual reports. Acceptance simulations independent of calibration
qualified each declared quantity on a finite scenario grid among screen-passing replicates, with
abstentions (withheld claims) counted as non-errors. At the first stage the
one-sided 95% lower confidence limit on coverage must exceed 0.93; borderline quantities proceed to a
preplanned pooled acceptance rule (electronic supplementary material, S2).

**(e) Body-fossil units.** We assembled land-plant body fossils dated to 453–393 Ma from Paleobiology
Database (PBDB) occurrences, whose names an AI model classified with cited sources before our audit, and from a
source-reviewed set of the oldest records with their competing readings. Collections, taxa or papers
sharing a locality and age count once, as proxies for independent fossil horizons. Three nested
categories are declared. Land-plant bodies include any accepted macro- or mesofossil; polysporangiophytes
need documented branched axes bearing sporangia, or placement within the vascular crown; crown vascular plants
belong to the lycophyte line (clubmosses and relatives) or the euphyllophytes (ferns and seed plants)
[@kotyk2002MorphologicallyComplexPlant; @libertin2018SporophytesPolysporangiateLand;
@earp2024NotanopliidBrachiopodsAssociated; @libertin2024GenusAberlemniaSiluriandevonian]. The main
reading gives [78]{.C25}, [71]{.C25} and [50]{.C25} units in the three categories, of which
[76]{.C40 .V021}, [69]{.C25} and [48]{.C25} are certainly older than the end of the Emsian
([393.47]{.C25} Ma) (supplementary S5.1).

**(f) Bound on record start.** Let *w*(*s*) be a fixed relative rate at which identifiable occurrences
of a category are recorded at age *s*, and $U(a)=\int_c^a w(s)\,ds$ the cumulative recording above a
younger cutoff *c*, here the end of the Emsian. For *n* independent units with oldest age *A*, the
one-sided 95% older bound *T* on the start of the recognisable record solves
$U(T)=U(A)\,0.05^{-1/n}$ (Fig. 2). With constant *w* this is the classical confidence interval on a
stratigraphic range, and the absolute rate cancels [@strauss1989ClassicalConfidenceIntervals;
@marshall1990ConfidenceIntervalsStratigraphic]; varying *w* follows the extensions to non-random fossil
horizons [@marshall1994ConfidenceIntervalsStratigraphic; @marshall1997ConfidenceIntervalsStratigraphic].
Units dated by ranges enter through the greatest possible oldest age
and the minimum number guaranteed to lie within the window. The bound concerns the start of the record;
§4 treats its link to ancestors.

**(g) Recording histories and shape tests.** Six fixed histories were compared: constant recording;
recording proportional to PBDB land and marginal-marine collections per Myr, with or without collections
matching plant occurrences; exponential declines into the past with 25 or 10 Myr timescales; and
plant-excluded collection density multiplied by the 10 Myr decline. The collection records extend to
[469.4]{.C27 .V007} Ma, which sets the analysis domain. Finite-sample Kolmogorov–Smirnov tests compared
each history with the observed age sequence, conditional on the count and the oldest find. We searched
every admissible allocation of ages within their ranges, and each inclusion state of the units straddling
the cutoff, for the allocation most favourable to each history [compare @berger1994PValuesMaximized]. A
history that fails under every allocation and state is rejected for this diagnostic (supplementary S5.2).

**(h) Recording contrast and diagnostic delay.** The primary step model keeps later recording constant
and lowers earlier recording before [426.7]{.C32} Ma, the oldest possible age of a crown vascular-plant
find. For a candidate ancestor age *t* and an assumed delay *d* before recognisable bodies, the earlier
to later rate ratio that places *t* − *d* exactly on the bound is
$r=(A-c)(0.05^{-1/n}-1)/(t-d-A)$, defined where $t-d>A$; the recording contrast is $1/r$. The step was
placed after inspecting the record, so its contours describe retrospective compatibility. Longer assumed
delays reduce the contrast required for a given candidate age [@marshall2019UsingFossilRecord].

## 3. Results

**(a) The 515.5 Ma maximum.** Morris et al. placed this maximum below the oldest possible total-group
records, spore-like packets and polyads from the Cambrian Stage 4 Rome Formation, at the base of the
*Olenellus* Biozone (about [515.5]{.C46} Ma). Their absence argument holds that land-plant spores share
the preservation potential of the marine algal cysts with which they usually occur, so older sequences
with cysts and without land-plant spores record a real absence [@morris2018TimescaleEarlyLand;
@morris2018ReplyHedgesEt]. The control establishes that walled microfossils survived and were recovered;
spore delivery to those basins, the land areas they drained and the search effort remain unquantified
in the sources we assessed[]{.C16}. All [three]{.C15} sources we examined assign the Cambrian packets to
algae or pre-land-plant lineages: Charophyta [@strother2016SystematicsEvolutionarySignificance], a
pre-embryophytic grade [@taylor2024UltrastructureCambrianCryptospores] or ancestral aeroterrestrial
algae [@wang2022PalynologicalAssemblageCambrian] (supplementary S4).

**(b) The younger maxima.** Hooper et al. set both younger maxima as a GTS2012 stage base plus its
uncertainty. They keyed 459.1 Ma ([458.4 + 0.7 = 459.1]{.C42} Ma) to a possible trilete at 48.2 m in the
Borenshult-1 core [@rubinstein2019BalticaCradleEarly]. The oldest definite trilete level, at 43.1 m, is
also Sandbian and lies below the [454.41]{.C43} Ma Kinnekulle K-bentonite, so the rule gives the same
value from either level (supplementary S2.4). They keyed 431.2 Ma ([430.5 + 0.7 = 431.2]{.C47} Ma) to
Irish Homerian *Cooksonia* [@edwards1980RecordsCooksoniatypeSporangia]. The older Czech
*Cooksonia barrandei*, a branched sporophyte with terminal sporangia from a Sheinwoodian horizon inferred
from slab fauna and correlation [@libertin2018SporophytesPolysporangiateLand], meets the same character
criterion. On the current timescale the rule gives outer values of [431.9]{.C47} Ma for the Homerian and [434.1]{.C47} Ma
for the Sheinwoodian.

**(c) Libyan spore limits.** Trilete spores occur in [51 of 59]{.C02} reference cuttings and in none of
the [28]{.C01} older cuttings (Fig. 3a). For input starting at 459.1 Ma with equal delivery, the upper
compatibility limit is [0.091]{.C24} of reference input for constant histories, and [0.184]{.C24} for the
exposure-weighted mean of bounded variable histories (Fig. 3b). With delivery at a tenth of the
reference, constant input near the reference level fits ([0.910]{.C24}). For constant histories the
record constrains the product $\rho f$, which stays at [0.091]{.C24} across delivery scenarios.

**(d) Time covered by the Libyan limits.** Most older exposure comes from [18]{.C45} Katian–Hirnantian
cuttings, all younger than 459.1 Ma. Only [10]{.C45} broadly dated Darriwilian cuttings, from two wells,
have age ranges extending before 459.1 Ma. Their contribution under a start at that age depends on how
ages are spread within the stage, and shared midpoint ages give them none[]{.C09}. The limits therefore
concern sustained input through the later Ordovician in one high-latitude basin.

**(e) Vascular-plant body bounds.** The [48]{.C25} crown vascular-plant units give a one-sided 95% older
bound of [428.8]{.C27 .V003} Ma under constant recording (Fig. 4a). Histories tracking collection density
give [428.9]{.C27 .V009} Ma, or [428.5]{.C27 .V010} Ma with plant-matched collections removed, and a
25 Myr decline into the past gives [431.6]{.C27 .V011} Ma. The pure 10 Myr exponential decline leaves the start unresolved
through [469.4]{.C27 .V007} Ma and fails the shape diagnostic under every admissible allocation and
inclusion state[]{.C49}. With all [50]{.C49 .V107} possible units, an admissible age allocation for the
25 Myr decline gives *p* = [0.067]{.C49 .V104}; with the [48]{.C49 .V069} guaranteed units, every
allocation fails (best *p* = [0.035]{.C49 .V106}).

**(f) Sensitivity to units and timescale.** Unit treatment moves the constant-recording bound across
431.2 Ma. Collapsing units to region–stage cells ([19]{.C30} units) gives [432.4]{.C30} Ma, and the curated
oldest-record set alone ([15]{.C30} units) gives [434.05]{.C30} Ma. Shifting stage boundaries by their
quoted uncertainties, in the tested shared-boundary scenarios, moves the primary bound between
[427.31]{.C50 .V062} and [430.42]{.C50 .V063} Ma (supplementary S5.3).

**(g) What older vascular-plant ancestors require.** In the primary step model, halving earlier
recording gives [431.0]{.C53 .V108} Ma, younger than the 431.2 Ma maximum. With zero assumed delay,
candidate ancestors at 444–452 Ma, spanning the Morris et al. mean dates and the Harris et al. interval,
need earlier recording [8]{.C48 .V054}–[12]{.C48 .V055} times lower than later recording (Fig. 4b).
Under region–stage or curated units the contrast falls to [2.4]{.C48 .V056}–[4.5]{.C48 .V057} times, and
431.2 Ma needs no reduction. With constant recording, the same ancestors instead need assumed delays of
at least [15–23]{.C33} Myr before recognisable bodies. Smaller contrasts can combine with shorter
delays (Fig. 4b).

**(h) Oman and the broader land-plant category.** Sporangial fragments with in situ cryptospores from the
Ghaba-1 borehole, Oman, dated to the Katian on later correlation [@wellman2003FragmentsEarliestLand],
form one land-plant body unit. Adding them moves the broader category's constant-recording bound from
[434.5]{.C28} to [455.2]{.C40 .V022} Ma. With them, the sequence fails the shape diagnostic under all six
fixed histories[]{.C49}. The fragments came
from palynological preparation of borehole material, whereas most later units are compressions collected
from bedding planes [@edwards1979RecordsFertileRhyniophytina].

## 4. Discussion

The record constrains two specific histories. In the Murzuq Basin, sustained, well-delivered trilete
input at the Llandovery level through the later Ordovician conflicts with the zero records. Under
constant or collection-density recording histories, the primary one-sided 95% older bounds on the
recognisable crown vascular-plant record lie near [429]{.C27 .V018} Ma. Coarser or curated treatments put
the constant-recording bound at [432.4–434.05]{.C30} Ma. For spores, lower delivery,
lower local input or producers outside the catchment accommodate older ancestors. For bodies, lower
earlier recording or later recognisable features accommodate them. The models quantify encounter
limits, aggregate recording contrasts and assumed diagnostic delays.

Several processes could lower earlier recording. Producers may have been rarer, more geographically
restricted, concentrated in settings with little terrestrial deposition, or represented in intervals
searched less often. Body size, cuticle and lignified tissue could also raise the chance that a body is preserved,
found and recognised. Branched sporophytes and conducting tissue were acquired stepwise along the
lineages being dated [@kenrick1997OriginEarlyEvolution], and the earliest parent plants known in detail
were minute [@edwards2014CryptosporesCryptophytesReveal]. The early branched sporophyte
*C. barrandei*, is preserved in marine sediments [@libertin2018SporophytesPolysporangiateLand], and the
Oman fragments show that small sporangia can survive [@wellman2003FragmentsEarliestLand]. The models
quantify the combined recording contrasts a candidate age requires; the contribution and plausibility
of each process remain open.

@silvestro2015RevisitingOriginDiversification modelled genus-level PBDB plant occurrences with a joint
Bayesian model of preservation and diversification, and estimated the origin of vascular plants at a
mean of 433.5 Ma (95% highest posterior density 449.0–424.0 Ma). They estimate when the earliest
vascular-plant genus lineage arose, with a fitted, varying preservation rate; we bound the start of the
recognisable record of a declared crown category under fixed recording histories, then ask what older
ancestors require. The two analyses target different quantities from partly shared data and test
different assumptions. CladeDate builds calibration densities directly from fossil times
[@claramunt2022CladedateCalibrationInformation], and Hooper et al. link spore-character reconstruction to
revised calibrations. We add a quantified account of what the specific maxima that divide current clocks
require of the record.

**Conditions.** The spore limits assume an indigenous younger reference, comparable reporting in older
and younger cuttings, ages uniform within stages, and cutting outcomes independent given a shared well
effect. Exploratory dependence checks use separate reference rates for each well with the random well
effect removed (constant-history contour [0.0995]{.C51 .V058}), well–formation block weighting
(contour near [0.4]{.C51 .V081}), and one-well deletions (exposure-weighted contours
[0.185–0.365]{.C07}). Coverage remains unqualified for these retrospective comparisons. Mapping local
encounter to ancestors requires that the earliest crown members produced recognisable trilete spores,
that the trait persisted, and that producers lived in the catchment (supplementary S6).

The body bounds and conservative shape rejections assume independent continuous ages, fixed histories,
cutoff, timescale, inventory and unit rules, and an observation model whose supports contain all true
ages and inclusion states with probability one. Geological
ranges have no demonstrated joint coverage; if containment can fail with probability $\delta$, the
direct test-size bound is $\alpha+\delta$, where $\alpha$ is the fixed-history exact-age significance
level. Matched exact-age simulations gave coverage [0.941–0.958]{.C34}, falling to about
[0.78]{.C34} when paired duplicate horizons were treated as independent (supplementary S5.6).
The step model is retrospective. Mapping bodies to ancestors requires crown membership of the oldest
finds and a specified delay before recognisable bodies.

Records of searched Silurian terrestrial beds, with effort and empty beds included, would help constrain
early recording opportunities, and compilations
of rock units could supply proxies for the terrestrial rock available at each age
[@peters2018MacrostratPlatformGeological]. A second
complete older-zero, younger-positive spore sequence outside polar Gondwana, with counted target and
control grains, would test whether the Libyan result is general. An enumerated marine sequence older
than 515.5 Ma, with comparable recovery and reference encounter documented, would help quantify the
oldest maximum's conditional absence argument. Finer, independent ages for the Yea
(Victoria, Australia) and Bathurst Island (Arctic Canada) horizons, which hold the oldest possible crown
vascular-plant finds, would sharpen the body bound [@earp2024NotanopliidBrachiopodsAssociated;
@kotyk2002MorphologicallyComplexPlant]. Characters placing the oldest branched sporophytes on the
lycophyte or euphyllophyte side of the vascular crown could change which fossils enter the category, as
well as their link to the ancestor.

Clock builders can state each maximum's character, geographical and recording assumptions, and justify
the probability assigned to older ages against them [@parham2011BestPracticesJustifying;
@yang2005BayesianEstimationSpecies]. Testing alternative defensible maxima then shows how much each
assumption moves the timescale. Sampling the joint age prior without molecular data and comparing its
effective marginal age distributions with the corresponding posteriors shows what the molecular data
add [@brown2017PastSureTense]. This separation
of evidence, recording and mapping applies to any maximum argued from absence. Older dates for living
land plants fit the fossil record if early plants were found several times less often, or recognisable
features evolved later.

## Figure captions

**Figure 1.** Clock intervals for the ancestors of living land plants and living vascular plants
[@morris2018TimescaleEarlyLand; @harris2022DivergentEvolutionaryTrajectories;
@hooper2026ReconstructingSporeEvolution], the three maxima, and the age ranges of the oldest spores,
the Oman fragments and the oldest vascular-plant bodies. Labels identify each published clock summary,
preserving its stated statistical meaning. Each fossil bar spans its earliest possible to earliest
certain age.

**Figure 2.** How the bound works. Recorded finds above the younger cutoff, the oldest find *A* and the
count *n* give the one-sided 95% older bound *T* on record start under a fixed recording history. For
range-dated data, *A* is the greatest possible oldest age and *n* the minimum guaranteed count. A step
in earlier recording and an assumed delay *d* connect *T* to a candidate ancestor age *t*.

**Figure 3.** Murzuq Basin, Libya. (a) Age ranges of the chart-coded cuttings by well, with trilete
reports, the Llandovery reference and 459.1 Ma marked. (b) Upper 95% compatibility limits on constant
input and exposure-weighted mean input over bounded variable histories, relative to reference input,
as the delivery ratio varies. Both curves use the primary cutting frame and shared-well model.

**Figure 4.** Vascular-plant bodies. (a) Crown vascular-plant units with the primary constant-recording
bound and coarser or curated alternatives. (b) Later-to-earlier recording contrasts required by
candidate ancestor ages, for zero and non-zero assumed delays, with the clock intervals marked. The
step is retrospective; contrasts are evaluated where candidate age minus assumed delay exceeds the
oldest possible find.

## Data accessibility

The repository <https://github.com/BWBrook/silurian_plants> holds the source-linked derived tables,
model code, qualification evidence, body-record outputs with hash receipts, figure and table scripts and
the claims ledger that binds every reported number to its evidence. The frozen PBDB collections extract
used by the effort histories is archived under CC0 at <https://doi.org/10.5281/zenodo.24028289>.
Copyrighted full texts are excluded from the repository; source routes and held-file hashes are
recorded separately. Openly licensed third-party deposits are fetched by script and hash-checked.

## Declaration of AI use

Claude Opus 5.5 (Anthropic) developed and ran analyses and drafted and revised the manuscript.
OpenAI Codex (`gpt-6.1-sol` and `gpt-6.1-terra`) curated and checked source data, implemented analyses,
audited statistical methods and reproduction, and revised the manuscript. Earlier Codex work used
`gpt-5.6-sol` and `gpt-5.6-luna` for source recovery and methodological checks. Claude and Codex reviewed
each other's work. GPT-6 Pro (OpenAI) supplied independent critiques, which were checked against
sources and saved outputs before integration. Barry W. Brook originated and guided the programme and
contributed scientific decisions; he will review the final manuscript before submission. Task-specific
roles, model versions and the limits of sessions whose exact variant was unavailable are recorded in
`docs/charter.md`, `docs/audits/` and `manuscript/reconstruction/`, with adopted decisions in
`docs/decisions.md`.

## Funding

This research received no specific funding.

---

## Drafting notes

- **Length.** Main text (Introduction to Discussion, excluding Table 1, captions and end matter):
  see the count recorded in `README.md`. The abstract is under the 200-word limit stated in the Royal
  Society guidance (1d).
- **What 3c added to 3b.** The specific provenance needed to follow each result: the Hawaz reporting
  basis (2c), the qualification gate (2d), category definitions and unit counts (2e), the extensions for
  varying recording (2f), the analysis domain (2g), the contour equation (2h), the dated Borenshult and
  Kinnekulle levels (3b), the 25 Myr pass/fail witnesses (3e), the region and Yea sensitivities (3f), the
  20 Myr delay example (3g), and the dependence and simulation checks in Conditions. Everything else in
  the frozen article stays in the supplement.
- **Half-rate bound.** Now ledger claim C53, binding V108 (430.9800119 Ma, `suppression_sensitivity.csv`,
  step at 426.7 Ma, multiplier 0.5). Codex checked the closed form on 10 November; Claude recomputed it on
  11 November: $U(A)=33.23$, $U(T)=33.23\times20^{1/48}=35.37$, so $T=426.7+2(35.37-33.23)=430.98$.
- **References.** The 3b candidates were read before citing. Codex read Yang and Rannala, and Parham et
  al., in its 3b review; a delegated Codex job read the other 11 (`gpt-6.1-sol` with web search,
  legitimately hosted copies only; receipt in `docs/audits/2026-11-11-3c-reference-reads.md` with its
  prompt and JSON output). Claude checked four of the quotes it
  returned verbatim against the source PDFs
  (Steemans, dos Reis, Benton, Peters) and rewrote each sentence to the scope the source supports: Ho and
  dos Reis now support calibration sensitivity in the Introduction; Kenrick and Crane support stepwise
  acquisition of branched sporophytes and conducting tissue; Peters et al. support rock-unit
  compilations as proxies for rock availability. Gradstein et al. (2012) is dropped: its Crossref record
  lists no authors or editors, so `refs.py` cannot build it, and the GTS2012 values are cited through
  Hooper et al. Twelve DOIs were added to `references/dois.txt`; existing entries are unchanged.
  Codex's 3c review independently checked targeted original material for Benton and Donoghue, dos Reis
  et al., Kenrick and Crane, and Brown and Smith, with the scope and access limits in
  `codex-3c-argument-check.md`. The receipt records each source's copy, URL, sections read, verdict and
  claim scope.
- **Codex review.** The scientific and source checks are `codex-3c-science-check.md` and
  `codex-3c-argument-check.md`. They confirm C53 and preserve the lean length. The revisions define
  the potential screen, restore the 429 Ma older-bound meaning, distinguish a passing age allocation
  from universal failure, state the support-containment condition, and label all retrospective
  dependence comparisons as unqualified. Region/Yea details and the illustrative 20 Myr delay remain
  in the supplement. Figure captions retain the contracts for statistical meaning, age envelopes and
  retrospective contrasts; figures remain to be built.
- **Claude's reconciliation (11 November 2026).** All of Codex's 3c repairs are accepted: 429 Ma
  restated as an older confidence bound, the potential screen and acceptance rule defined, the
  25 Myr result stated as a witness allocation, the containment condition stated with its α + δ size
  bound, all dependence comparisons labelled unqualified, the Oman gap dropped as a cause, scoped
  claims for the 515.5 Ma evidence, Brown and Smith's effective-prior comparison, the regional scope
  of deposit scarcity, and the source-access wording. Claude checked the Gamma(2, 2) shared-well
  effect against `models/f3/envelope.py` and `cluster_k=2.0` in `m2_results.csv`. Step 3c is locked as
  a draft.
- **End matter.** The AI-use statement credits recorded systems and tasks and keeps Barry's final
  review prospective. Funding follows Barry's chat reply, 11 November 2026: "No specific funding for
  this project."
- **Positive prose.** Conditions sit in two paragraphs of the Discussion. Results report each number with
  its case; the Discussion's first two paragraphs read as findings.
