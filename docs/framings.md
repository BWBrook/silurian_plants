# Candidate framings

Draft, 2026-10-26, Claude Opus 5.5; facts updated 2026-10-27 after the review of the EPRP deposit
(`docs/audits/2026-10-27-eprp-deposit-review.md`). I drafted it before reading `docs/precedents.md`
and revised it afterwards, so where the two agree they are independent assessments, and where they disagree the
disagreement is stated. It is written for Barry to react to; choosing a framing is his call
(charter, test 4). Each framing gives the question, why it is open, the model, the evidence that
could discriminate between explanations, and an assessment against the charter's tests. Full
references are in `docs/precedents.md`, `docs/primer.md` and the cards, plus the short list at the
end.

## A design principle common to all of them

Whatever the question, the simulated world has to be compared with a record filtered by
preservation. Spores are produced in vast numbers, travel far and fossilise in marine shales. The
bodies of small plants fossilise rarely, mostly in wetland and fluvial settings, and anatomically
only in a few Lagerstätten. A model that predicts which plants existed cannot be tested against
what is found without an explicit **observation model**: spore production and transport,
fossilisation probability by habitat and body size, and sampling effort by stage and region. That
layer is the same for every framing below, so it is worth designing once. It is also where
methods for inferring event times from incomplete records, including Barry's own (Bradshaw et
al. 2012), apply directly.

## F1. Why did the sporophyte take over?

**Question.** Living bryophytes have a gametophyte-dominant life cycle, with a small sporophyte
nourished by the gametophyte. Within a few tens of millions of years of the first megafossils,
the vascular-plant sporophyte was branched, photosynthetically independent, vascularised and the
larger generation. In the Rhynie Chert the gametophytes were still free-living, axial and of
broadly similar organisation to their sporophytes, though smaller (`taxa/rhynie-chert-gametophytes.md`).
Which ecological conditions select for elaborating the diploid generation, and in what order
should the enabling traits appear?

**Why it is open.** The competing explanations are more than a century old and remain verbal.
Bower's antithetic (interpolation) theory (Bower 1890, 1908) holds that the sporophyte was
inserted into an algal life cycle and elaborated to multiply the spore output of each
fertilisation, because on land fertilisation is limited by the need for liquid water.
Alternatives include diploid genetic advantages such as masking of deleterious mutations (Mable &
Otto 1998); the dispersal benefit of raising sporangia above the boundary layer; and the
homologous (transformation) view, in which near-isomorphic generations like those of the Rhynie
Chert were ancestral and the gametophyte was later reduced (Haig 2008; Niklas & Kutschera 2010;
Kenrick 2018). Bryophyte monophyly (Puttick et al. 2018) reopens whether bryophyte sporophytes are
primitively simple or secondarily reduced, and Hooper et al. (2026) now infer that the crown
embryophyte already produced trilete spores from tetrahedral tetrads. The precedents review
confirms the gap: haploid–diploid theory (Hughes & Otto 1999; Scott & Rescan 2017), conflict and
parental-care models (Haig & Wilczek 2006; Bessho & Sasaki 2024) and the shadie simulator
(Sorojsrisom et al. 2022) have no dispersal, water-limited fertilisation or sporophyte size.

**Model.** A spatially explicit, individual-based eco-evolutionary model on a landscape with a
moisture gradient (wet margins to drier interfluves) and wet–dry variability. Individuals
alternate generations. Heritable allocation traits set gametophyte size, sporophyte size,
sporangium number (branching), sporangium height, and the degree of sporophyte photosynthetic
independence, which carries the costs of cuticle, stomata and conducting tissue. Fertilisation
requires gametophytes within sperm-swimming distance during wet events; spores disperse with a
kernel that lengthens with release height; establishment depends on moisture. Each mechanism is a
switchable module, so every hypothesis can be run alone and in combination.

**Evidence that could discriminate.**
- *Habitat.* Bower's mechanism predicts that sporophyte dominance arises first where
  fertilisation is rarest, in drier or more variable settings. Genetic masking predicts no
  habitat association.
- *Trait order.* Dispersal-driven elaboration predicts height before independence;
  amplification predicts more sporangia per zygote (branching) before height. The fossil series
  tests this: eophytes with tiny cryptospore-bearing sporophytes (`taxa/partitatheca.md`),
  Cooksonia-type axes that Boyce (2008) argued were too slender to be photosynthetically
  self-sufficient (contested for the 1–1.5 mm axes of C. barrandei; Libertín et al. 2018), Rhynie
  near-isomorphy, then gametophyte reduction.
- *Sizes.* Gametophyte-to-sporophyte size ratios across matched Rhynie pairs (Gerrienne & Gonez
  2011 compile the data).

**Assessment.** Discriminating evidence: moderate if tested alone; the precedents review ranks
this gap among the most data-limited, and I agree for F1 on its own. Novelty: high, confirmed by
the review. Tractability: high; the model is small and the constraints come from the cards. Main
risk: qualitative predictions that any reasonable parameterisation reproduces. Coupling with F2
answers both weaknesses, because the same engine then has to reproduce the best-recorded trait
series of the interval, sporophyte size.

## F2. The first height race

**Question.** Maximum sporophyte height rose from a few centimetres (Silurian Cooksonia) through
about 20–45 cm at Rhynie (Raven 2018) to a metre or more by the Emsian (Psilophyton, Pertica),
while branching shifted from isotomous to pseudomonopodial with overtopping. Was this an arms race
for light, a by-product of selection for spore dispersal, or the release of constraints
(lignified tracheids, stomatal control, rooting, falling CO2)?

**Why it is open.** Niklas's adaptive walks through a branching morphospace (Niklas 1994, 2004)
optimised a fixed fitness function for an isolated plant: no competition, no frequency dependence,
no demography and no fit to dated fossils, a limitation Niklas himself stated. Height games exist
only for leafy trees (Falster & Westoby 2003; Falster et al. 2017). The review found no
quantitative height or buckling model for leafless axes.

**Model.** The F1 engine with sporophyte architecture made explicit (design references: TREED's
carbon-economy trade-offs, Rogger et al. 2026; fossil-based whole-plant function, Matthaeus et al.
2023): light competition among
axes, hydraulic and mechanical limits on height set by axis diameter and conducting-tissue type
(Wilson & Fischer 2011), gas exchange against a CO2 path (Dahl et al. 2022), and dispersal by
height. Run with and without competition, and with innovations unlocked at their fossil dates or
left to evolve.

**Evidence.** Height and axis-diameter series through time (the cards' trait records are the
start of that compilation: `data/traits.csv`); branching-mode frequencies through time (Chomicki
et al. 2017); the observed rate of size increase against rates expected under competition and
under constraint release.

**Assessment.** Discriminating evidence: moderate to good, because size is the best-recorded
trait. Novelty: high (the review's Gap 1). Tractability: high.

## F3. Does the record support the new timescale? Origination from two imperfect records

**Question.** Hooper et al. (2026) have just moved crown embryophytes from the Cambrian (Morris et
al. 2018) to 457–450 Ma and placed crown tracheophytes at 432–428 Ma, treating cryptospores as
stem-group. The first megafossils of crown tracheophytes are late Silurian zosterophylls
(Ludfordian, about 425 Ma; `taxa/zosterophyllum.md`), the oldest polysporangiophyte is Cooksonia
barrandei at about 432 Ma, and Hg isotopes have been read as widespread vascular plants by about
444 Ma (Yuan et al. 2023). Given how the record was sampled, are the first appearances in the
spore and megafossil channels consistent with the new timescale, and how much of the apparent
Silurian–Devonian radiation is the rock record?

**Why it suits this team.** It is the mirror image of extinction dating. A first appearance
post-dates origination as a last appearance pre-dates extinction, and the methods built for
extinction times (confidence intervals on stratigraphic ranges, Marshall 1990, 1997; the
Gaussian-resampled, inverse-weighted estimator of Bradshaw et al. 2012) apply in reverse. The spore
and megafossil records are two partly independent sighting series of the same lineages. The
review found no study that puts simulation-validated intervals on early land-plant first
appearances; the nearest are preservation-aware birth–death inference (Silvestro et al. 2015) and
sampling-standardised diversity (Capel et al. 2022, 2023).

**Model.** A virtual palaeontology: lineages under birth–death with trait evolution, plants that
shed spores and leave bodies, and the observation model. Measure which estimators recover known
origination times and with what bias, then apply the validated estimators to the real occurrence
records (Paleobiology Database and published megafossil compilations; compiled spore
occurrences).

**Evidence.** Strong and quantitative: occurrence data exist, and the simulation tests the
estimators where the truth is known. Calibrating clock studies sets soft maximum ages by expert
judgement, so a sampling-based estimate of each clade's probable origination window is directly
useful to them as well as a test of their result. Circularity has to be handled: the clock uses
these same first appearances as minimum constraints, so the test is of the maxima and of the
consistency between spore and megafossil channels, not of the minima.

**Data in hand (EPRP review, 2026-10-27).** The megafossil channel exists but is thin: PBDB has
259 core land-plant occurrences before the Emsian, 2 of them in the Sheinwoodian. The spore channel
does not exist yet: PBDB holds one Ordovician spore record, so dispersed-spore occurrences must be
compiled from the literature. Macrostrat's rock record is North American and mostly marine, while
the early plant record is mainly European, peri-Gondwanan and South Chinese, so the observation
model needs another sampling proxy. EPRP's validation of the candidate tools (`tbea`, PyRate,
StratPal) has already found pitfalls that bite on a gap-dominated record
(`data/eprp/pointers/eprp_pointers.md`).

**Assessment.** Discriminating evidence: strong once both channels exist. Novelty: high for land
plants, confirmed by the review (its Gap 6) and made timely by Hooper et al. (2026); the approach
itself is established for birds and winged insects (Crouch 2022; Schachat et al. 2022). Tractability:
moderate, because the spore compilation is real work, although a megafossil-only first pass is
possible now. Interest: depends on Barry's appetite for a record-focused study, though it builds
the observation model that F1 and F2 need.

## F4. From cosmopolitan to provincial: dispersal and spore biogeography

**Question.** Ordovician–Silurian cryptospore assemblages look broadly cosmopolitan, while Early
Devonian floras have regional character, such as the Baragwanathia floras of eastern Gondwana and
the zosterophyll-rich floras of South China. Does a shift from tiny, globally dispersing spores to
larger, sporophyte-dominated and more dispersal-limited plants, set on the palaeogeography and
climate belts of the time, reproduce the transition?

**Model.** A spatially explicit metacommunity on palaeogeographic reconstructions with
palaeoclimate fields, spore dispersal kernels and trait evolution, producing simulated assemblage
similarity among regions through time.

**Evidence.** Similarity matrices of spore and megafossil assemblages by stage and region.

**Assessment.** Discriminating evidence: good in principle. Novelty: probably high (not covered
by the review's strands, so unchecked). Tractability: moderate. The palaeogeographic and
palaeoclimate inputs are now on the mesh: 21 PALEOMAP elevation maps, HadCM3 and cGENIE climate
fields and a plate-model index, plus gen3sis as an engine (EPRP review, 2026-10-27). The spore
compilation shared with F3 remains, and no reliable full-plate model exists before 410 Ma. A strong
second-phase project.

## F5. Closing the loop between evolving plants and the carbon cycle

**Question.** Could plausibly evolving early vegetation have driven Late Ordovician cooling, the
Siluro-Devonian fall in CO2 and the rise of O2? Every Earth-system treatment prescribes the plant
effects (Lenton et al. 2012, 2016; Porada et al. 2016; Dahl et al. 2022), and the published
verdicts on shallow versus deep rooting conflict. Eco-evolutionary vegetation has been coupled to
the carbon cycle for later intervals (Rogger et al. 2024; TREED, Rogger et al. 2026), and FLORA with
SCION finds an Ordovician window of opportunity for plant expansion (Gurung et al. 2022). What
remains open is the coupling for leafless early plants in this interval.

**Where the review and I differ.** The review ranks this among its three most promising gaps (its
Gap 4): replace the prescribed colonisation, C:P and weathering factors with outputs of an
eco-evolutionary module, and ask which trait trajectories satisfy the carbon mass balance and the
proxies together. I agree that it is important and open. I rank it lower as a starting point
because it inherits the full uncertainty of COPSE-type models and contested weathering
mechanisms, its targets are low-resolution proxies, and it needs a credible plant module first,
which is what F1 and F2 would provide. It is the natural third stage of a programme that starts
with F1–F3, not a first study.

**Tractability note (EPRP smoke test, 2026-10-27).** SCI-FI, the SCION climate–carbon model coupled
to the FLORA vegetation model (Gurung et al. 2024), runs headless in MATLAB on mac-mini in about
8 s per 250 Myr run, so a 1,000-member ensemble takes hours. It reproduced the paper's peak
habitable area (92% near 145 Ma) but not its Triassic value (80% against 65%); that gap should be
resolved against the archived run before building on the code. Its climate stack reaches 540 Ma,
so retargeting to 485–383 Ma is mostly configuration. But FLORA's three vegetation types are
parameterised for an angiosperm and gymnosperm world. Early-plant physiology would have to be
built, and that is where both the novelty and the work lie. Outputs:
`deep-server:/data/codex/silurian_plants/runs/scifi-smoke-2026-10-27/`.

## F6. Vulnerability and recovery of early land floras

**Question.** How vulnerable were early plant populations, with a gametophyte that needs free
water, to the Hirnantian glaciation and the Silurian climate perturbations, and how did they
recover? Spore richness has been correlated with climate descriptively (Pšenička et al. 2021),
and a late Silurian–Early Devonian cooling has been inferred from Sr and δ18O (Avila et al. 2025).

**Assessment.** This is the framing closest to Barry's extinction-risk work: a stochastic
metapopulation model with a gametophyte bottleneck and climate-dependent niches. It is the most
data-limited of the set (spore richness by climate belt is coarse), so I would treat it as an
application of the F1 engine and the F3 observation model once both exist, not as a study to
build towards.

## F7. A whole-flora eco-evolutionary world

The long-run synthesis of F1, F2, F4 and F6: digital plants with heritable life cycle,
architecture and physiology, evolving on palaeogeographic landscapes and observed through the
observation model. Worth naming as the destination so that early modules are built to compose,
and worth refusing as a starting point. The review's other gaps (rivers and mud, rooting and
fungal partnerships) attach to this world as modules rather than standing as separate studies.

## Comparison

| Framing | Discriminating evidence | Novelty | Tractability | Role |
|---|---|---|---|---|
| F1 Sporophyte takeover | moderate alone; good with F2 | high (confirmed) | high | core mechanism |
| F2 Height race | moderate–good | high (confirmed) | high | core mechanism, same engine as F1 |
| F3 Record and timescale | strong once spores are compiled | high for plants (confirmed); timely | moderate (spore compilation) | first deliverable; observation model for all |
| F4 Spore biogeography | good | probably high (unchecked) | moderate (inputs on the mesh) | second phase |
| F5 Closed-loop carbon cycle | moderate (low-resolution proxies) | moderate (coupling built for later intervals) | low as a first study | third stage |
| F6 Vulnerability and recovery | weak–moderate | moderate | moderate | application once F1 and F3 exist |
| F7 Whole-flora world | — | — | low | destination |

## Recommendation

One programme with two strands, built on shared machinery.

1. **First deliverable: F3.** A self-contained, data-rich study whose central question, whether
   the fossil record supports the new young timescale, became sharp with Hooper et al. (2026),
   published on 22 October 2026. It builds the observation model the rest of the programme needs, and its methods
   are those Barry already knows from extinction dating.
2. **Core science: F1 and F2 as one model of the rise of the sporophyte.** Why the diploid
   generation became independent, branched and tall. It is the most direct simulation of the
   evolution of early land plants among the options, its novelty is confirmed, and coupling the
   life-cycle question to the height series gives it a strong test against data.

F4, F5 and F6 follow once there is a working world to put on a map, couple to a carbon cycle or
stress with climate.

The EPRP review lowers F3's tractability but not its standing: the recommendation holds, with a
dispersed-spore compilation as its first task, and that compilation also serves F4.

The choice is not urgent, and the next tranche serves every framing: card review, the size and
trait compilation, an audit of occurrence data and its licensing (Paleobiology Database, the Capel
et al. compilations, spore records), and a reading of Hooper et al. (2026) in full.

## References not given elsewhere

- Bower FO (1890). On antithetic as distinct from homologous alternation of generations in plants. Annals of Botany 4: 347–370. https://doi.org/10.1093/oxfordjournals.aob.a090569
- Bower FO (1908). The Origin of a Land Flora: A Theory Based upon the Facts of Alternation. Macmillan, London. (no DOI)
- Bradshaw CJA, Cooper A, Turney CSM, Brook BW (2012). Robust estimates of extinction time in the geological record. Quaternary Science Reviews 33: 14–19. https://doi.org/10.1016/j.quascirev.2011.11.021
- Haig D (2008). Homologous versus antithetic alternation of generations and the origin of sporophytes. The Botanical Review 74: 395–418. https://doi.org/10.1007/s12229-008-9012-x
- Marshall CR (1990). Confidence intervals on stratigraphic ranges. Paleobiology 16: 1–10. https://doi.org/10.1017/s0094837300009672
- Marshall CR (1997). Confidence intervals on stratigraphic ranges with nonrandom distributions of fossil horizons. Paleobiology 23: 165–173. https://doi.org/10.1017/s0094837300016766
