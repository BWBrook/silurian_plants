# Trait pilot: the mappings behind the maxima

Adopted design, 29 October 2026. Claude Opus 5.5 drafted it. Codex reviewed it and supported the
framing, and its amendments L1–L5 and A1 are integrated
(`audits/2026-10-29-pilot-and-contract-review.md`). Two first results are below:
published crown states, and specimen combinations from the held sources (with an M3
record-identity audit).

**Decisions behind it.**
- **Scope** (Barry, Codex chat, 2026-10-29): "Excellent, we're aligned." This accepted F3 plus a
  bounded pilot on trait combinations and supported orderings (`innovation-scope.md`).
- **Framing** (Barry, Claude chat, 2026-10-29): "Yes, frame it so". This answered the question
  "Should the trait pilot test the trait-to-node mappings behind M1–M3?"

**Audits.**
- `gpt-6.1-sol` on the first draft: 17 findings, all accepted (`audits/2026-10-29-pilot-spec-audit.md`).
- Codex on the second draft: L1–L5 and A1.

Observations (O), interpretations (I) and speculation (S) are marked where it matters.

## Why this pilot

F3 asks whether the fossil absences are compatible with a *trait's producers* being encountered
before a candidate time *T* (`f3-shape.md`, data layer). The clock maxima are claims about *nodes*.
F3's node layer rests on a named mapping from each trait to a node (`f3-shape.md`, first table and
§3).

The pilot assesses those mappings from two kinds of evidence: specimen-level trait combinations,
and published placements and ancestral-state reconstructions. Each node statement F3 makes then
says what it rests on. This makes the pilot the second half of F3's conditional claim, not a
separate trait table. Its biological result is which orderings and node statements survive the
alternative readings, and what observation would settle the rest.

## What a node statement needs

For an absence argument to bound a node, an older node must entail an event-specific production
history of the kind F3 tests (L1). That is: had the node existed before *T*, producers of the
event would have existed from then on, in the declared history class. Three separate links
carry this, and each is assessed on its own (L2).

1. **Crown state:** the trait was present in the node's ancestor. Published ancestral-state
   reconstructions bear on this; a reconstruction is model-conditional support, not a dated
   transition.
2. **Persistence:** at least one lineage carried the trait from the node to the sampled interval
   without a loss-and-regain gap. Alternatively, a declared history assumption covers inheritance,
   loss and recurrence. Without one, persistence is an assumption, and F3's rarity restriction
   (§3) does not supply it: a restriction on how rare a lineage was says nothing about whether it
   still made the trait.
3. **Origin timing** (kept separately): when the trait first arose. Temporal precedence alone is
   not enough. A trait can arise on an extinct stem side branch before the crown, vanish, and
   arise again within the crown. A surviving stem lineage can also gain it after the crown
   originated.

Each link is scored **supported**, **contested**, **contradicted** or **unresolved**.
- *Unresolved* means the temporal evidence is missing.
- A modal crown state that lacks the trait does not make the link *contradicted*: it does not
  refute an earlier gain followed by loss.

## The mappings

| Maximum | F3 event | Node | Trait whose production the node must entail | Breaks it |
|---|---|---|---|---|
| M1, 515.5 Ma (Morris et al. 2018) | E2 cryptospores | crown Embryophyta | **P2:** cryptospore production | the crown ancestor did not make cryptospores and no persisting crown lineage did from the node on (for example, cryptospory only on stem side branches, or arising later within the crown) |
| M2, 459.1 Ma (Hooper et al. 2026) | E1 triletes | crown Embryophyta | **P1:** trilete production | a reading, with its source, that places the first relevant trilete production *after* the crown node (L3). "Cryptospores first, triletes derived" is not enough: both could arise on the stem before the crown |
| M3, 431.2 Ma (Hooper et al. 2026) | E3 bodies | crown Tracheophyta | **P3a:** branched sporophytes with several sporangia (C3) | the crown ancestor lacked C3 and C3 bodies arose within the crown |

**M3's fossil basis needs two further checks** (L4), each assessed separately.
- **Record identity.** Does each calibration specimen belong where it is placed?
  - Hooper et al.'s Supplementary Table 4 assigns the Homerian *Cooksonia* cf. *pertoni*
    (TCD22944–22956) by explicitly transferring anatomy from younger *C. pertoni* (PDF
    pp. 16–17, 23–24; Codex audit).
  - That transfer is audited here.
  - A total group includes its crown, so their trees' placement of a generic *Cooksonia* tip inside
    crown Tracheophyta does not by itself contradict a total-group label for another record (L5).
- **Proxy specificity.** Do several producer lineages make C3 bodies an incomparable encounter
  proxy across the admitted event and reference frame?
  - A C3 plant outside total-group Tracheophyta falsifies the universal claim that every C3 plant
    is a tracheophyte.
  - It does not by itself refute the Homerian placement or an aggregate C3 encounter result.

**Competing readings of the oldest spores.**
- **Traditional:** a bryophyte-grade first flora (`taxa/ordovician-cryptospores.md`).
- **Hooper et al.:** an ancestral trilete aperture (`primer.md` §5.3; below).
- **Developmental precursors** (Strother and Taylor 2024, via the card): the oldest cryptospores
  come off the embryophyte tree.

Each reading bears on P1 and P2 only through the three links above. A fossil's stem position does
not date its characters relative to the crown.

## First result: published crown states (O, from deposited outputs)

Codex extracted every state of the aperture character (`X21`) and the dispersal-unit character
(`X26`), at both crown nodes, for all four methods and three trees. The extraction is in
`data/pilot/hooper2026-asr/`, reproduced by an independent R check.

| Crown node | Aperture (`X21`) | Dispersal unit (`X26`) |
|---|---|---|
| Embryophyta | proximal trilete is modal in every output. Parsimony assigns it; ER, ARD and stochastic mapping give 0.770–0.977. The largest alternative is hilate, 0.229 (ARD, eophytes on the embryophyte stem) | "trilete or inaperturate monad" is modal in eleven of twelve outputs (0.957–1.000). The exception is ARD with eophytes on the tracheophyte stem: dyad 0.701, hilate 0.298, monad 0. Its aperture there is still trilete, 0.977 |
| Tracheophyta | proximal trilete in every output, 0.799–1.000 | monad in every output, 0.946–1.000 |

What this gives the mappings, under these published models only:
- **P1, crown state: supported for the aperture.**
  - The dispersal unit is contested by one model, which does not reconstruct trilete *monads*.
  - The joint reading of a dyad with a trilete aperture is unresolved. The two marginals were
    estimated separately and are not multiplied (A1).
  - Persistence: **supported under these models** (third result, below). Origin timing is
    **unresolved**.
- **P2, crown state: contested.** Eleven outputs reconstruct a monad. One reconstructs a dyad.
  - Hilate apertures take at most 0.229.
  - Under most published outputs, M1's node implication would need persistence of cryptospory
    from the node by some other route, and nothing here supplies one.
  - Persistence and timing are **unresolved**.
- **Crown Tracheophyta:** a trilete monad aperture throughout. P3a concerns sporophyte
  architecture, which these spore characters do not score.

Model agreement among one study's methods is not independent validation. These results are
conditional on Hooper et al.'s matrix, trees and methods, and are not re-estimated (consult
trigger below).

Hooper et al.'s main text (read 2026-10-30) adds three points.
- **Their conclusion is broader than their results.** It calls the naked trilete monad "robust to
  different evolutionary models and phylogenetic hypotheses". Their results section reports that
  the all-rates-different model, on both fossil trees, reconstructs an enveloped ancestral spore.
  The deposited dispersal-unit output on one of those trees is a dyad. The robustness holds for
  the aperture only.
- **Persistence.** They infer that liverworts lost the aperture independently. Persistence of
  trilete production from the embryophyte crown must therefore run through another lineage. The
  tracheophyte stem is trilete at both of its ends in every output. That is consistent with
  persistence but does not establish it. Codex found that the deposit saves no mapped histories,
  only node summaries (`data/pilot/hooper2026-asr/scm_workspace_audit.json`). With Barry's
  authorisation, Claude re-ran their mapping to read the histories (third result, below).
- **One fossil, two calibrations.** The Homerian *Cooksonia* cf. *pertoni* sets both the
  crown-embryophyte minimum (426.9 Ma) and the crown-tracheophyte maximum (431.2 Ma) ("Fossil
  calibrations").

## Second result: specimen combinations (O, held sources, 2026-10-30)

From `data/pilot/specimens.csv`: 524 rows from 30 primary sources, every quote checked against its
text, and the decisive rows adjudicated by Claude. Codex reviewed the first 283 rows
(`audits/2026-10-30-frame-and-pilot-review.md`). `data/pilot/combinations.csv` names each
combination's member rows and evidence level, so direct single-character rows cannot become an
unstated direct joint claim.

"Oldest", "first" and "only" below mean within this audited set, not across the record.

| Combination | Taxon and specimens | Level | Stage |
|---|---|---|---|
| C1 + C3 | *C. barrandei* D552a,b | direct | Sheinwoodian, by correlation |
| C3 | Irish *Cooksonia* cf. *pertoni*, TCD 22946d (expansions assumed to be sporangia; C1 and C4 unknown) | direct | Homerian |
| C4 alone | Capel Horeb axis, unbranched, nothing attached | direct | Ludfordian |
| C1 + C3 | *C. bohemica* JE-Sch0260A,B; Lang's *C. pertoni* 124 Z b and 124 X (Perton) | direct | Přídolí |
| C1 + C3 | *C. pertoni* subsp. *apiculispora* NMW 94.60G.14 | direct | Lochkovian |
| C1 + C3 + C4 | *C. pertoni*: C4 on UF597/UF1877, C1 + C3 on NMW 94.60G.14 | composite | Lochkovian |
| C1 + C3 + C4 | *Tortilicaulis offaeus* HD743/01 (tracheid ultrastructure unresolved) | direct | Lochkovian |
| C2 + C3 | *Velatitetras* producer NMW96.11G.3. C2 is **disputed**: the authors list immature tetrads of a trilete producer as an alternative, and judge the plant probably a tracheophyte (pp. 141–143, 149) | direct | Lochkovian |
| C2 + C3 | *Ficoiditheca aenigma* | composite | Lochkovian |
| C2 without C1 | *Lenticulatheca* spp. (C3 not shown), one of Hooper et al.'s eophyte tips | direct | Lochkovian |
| C3 without C4 | *Aglaophyton major*: pairs on Pb 4601 peels, C4 absence on NMW 85.49G.5 | composite | Pragian–Emsian |
| C1 + C3 without C4 | *Nothia aphylla*: eight sporangia on one dichotomy (91/1-366); no differential thickening in aerial axes (pooled) and rhizome (P 3032) | composite | Pragian–Emsian |
| C1 + C3, C4 disputed | *Horneophyton lignieri*: trilete monad in situ (Eggert 1974); tracheids (Kerp 2017; Cascales-Miñana et al. 2019) against transfer-cell-like cells (Kenrick and Long 2025) | composite | Pragian–Emsian |

What this does to the mappings (I):
- **Observed order**, within the audited set and by direct evidence:
  - trilete spores on branched plants with several sporangia from the Sheinwoodian through the
    Přídolí, with no tracheids demonstrated on the same plants;
  - tracheids by the late Ludlow, on an axis with nothing attached;
  - trilete spores, several sporangia and tracheids on one fertile plant only in the Lochkovian.

  This is the order of preservation windows (Silurian compressions, then charcoalified Lochkovian
  mesofossils), not acquisition order (rule 4).
- **P3b, proxy specificity.**
  - C3 without C4 occurs in *Nothia* and *Aglaophyton*, both composites.
  - The branched tetrad producers (*Velatitetras*, *Ficoiditheca*) are not tips in Hooper et al.'s
    trees. Carrying the eophyte placements over to them needs a further assumption, and Edwards et
    al. (1999) judge the *Velatitetras* plant probably a tracheophyte.
  - So the audited set does not show C3 outside total-group Tracheophyta. It shows only that C3 is
    not a crown-tracheophyte (tracheid-bearing) character.
- **P2, persistence (new).** If the *Velatitetras* tetrads are permanent, cryptospore production
  occurs in a probable tracheophyte in the Lochkovian. That would be cryptospory within the crown
  under Hooper et al.'s reading: the secondary cryptospory `primer.md` §5.3 allows. With C2 disputed,
  this is a lead, not a link.
- **M3 record identity: contested** (`audits/2026-10-30-m3-record-identity.md`).
  - The Homerian specimens show branching with terminal expansions, with no spores and no anatomy.
    Their original authors allowed a reading without conducting tissue.
  - The calibration's tracheids, stomata and sterome are transferred from Lochkovian *C. pertoni*.
  - *C. pertoni* itself is placed either on the eutracheophyte stem (outside the crown) or as sister
    to the lycophytes (inside it, as in Hooper et al.'s own trees).
  - *C. barrandei* is older than the 431.2 Ma maximum.
- **M2's fossil basis** (Hooper SI Table 4, C_4). One probable trilete spore (*Chelinospora*? sp.) at
  48.2 m in the Borenshult-1 core, lower Sandbian, sets the 459.1 Ma maximum. That core is now a
  complete 34-sample frame, and 48.2 m is one of its inventoried depths (Codex, Correspondence
  2570; `data/units/frame_samples.csv`). F3's E1 test on it therefore bears directly
  on the absence premise behind M2. Hooper et al.'s own justification ("first appearance must
  pre-date the origin of crown-Embryophyta") states that premise without testing it.
- **Q5.** Morris et al. (2024) describe the late Ludlow tracheids as in branching stems terminated
  by *Cooksonia*-type sporangia. Edwards and Davies (1976) isolated them from an unbranched axis
  with nothing attached. The cards repeated the later wording and are corrected.

## Third result: persistence under Hooper et al.'s own models (2026-10-31)

`models/pilot-asr/` re-runs Hooper et al.'s stochastic mapping and fitMk under a pinned renv.
- **Reproduction:** 156 of 156 deposited node values are reproduced within the pre-declared
  tolerances. Stochastic-mapping values differ by at most 0.036; ER and ARD reproduce exactly.
- **Persistence on the maps.** Given a trilete crown ancestor, the aperture stays trilete along
  the whole path to crown Tracheophyta in 98.4–100% of maps on the three trees. On the
  liverwort path it does so in only about a third.
- **Retention, single lineage.**
  - Fitted rates out of the trilete state are 0.0016–0.0043 per Myr.
  - A lineage making trilete spores at *T* keeps doing so without interruption to the base of
    the Katian with probability 0.93–0.97 for *T* = 470 Ma, and 0.76–0.90 for *T* = 515.5 Ma.
    These are ER and ARD point estimates; the widest posterior 95% interval reaches 0.52.
- **Correction to the design's premise.** The deposited ancestral-state timetrees put crown
  Embryophyta at 508 Ma, from the earlier Harris and Clark dates, not at Hooper et al.'s
  recalibrated 457–450 Ma. The map-based persistence is therefore conditional on those older dates,
  not on M2.

**Effect.** P1's persistence link is now **supported under these models**. Every M2 node statement
carries R(L) as an explicit, model-conditional factor. M1's cryptospore persistence is not
assessed: under most outputs the crown is not cryptosporous.

## Characters and coding rules

| ID | Character | Scored present when | Kept apart from |
|---|---|---|---|
| C1 | trilete production | in situ monads with a trilete aperture, either the mark observed or the spores assigned to a genus defined by it (say which) | separation from tetrads alone (it shows monads, not the aperture); dispersed triletes (first occurrences only, E1); irregular trilete-like marks (`taxa/zbrza-assemblage.md`) |
| C2 | cryptospore production | in situ permanent dyads or tetrads, or hilate or enveloped monads, without a trilete mark (the definition used by `taxa/ordovician-cryptospores.md`) | dispersed cryptospores (E2); dyads and aborted tetrads inside trilete-producing sporangia (`taxa/horneophyton-lignieri.md`) |
| C3 | branched sporophyte with several sporangia | an attached dichotomy with sporangia attached on at least two branches, or several sporangia attached to one branched plant | a branched axis with a single attached sporangium (scored "branched, C3 unconfirmed"); unbranched axes; isolated sporangia |
| C4 | demonstrable tracheids | elongate cells with secondary wall thickenings, shown in situ, with the organ examined stated | hydroids and leptoid-like cells; "disputed", which carries each reading |

**Evidence levels.** Every combination carries one of three levels, and they are never merged:
- **direct:** shown on one attached or serially reconstructed specimen;
- **composite:** assembled across specimens assigned to one species;
- **transfer:** taken from a broader taxon.

Composites and transfers stay informative when their identity assumption is written beside
them. The cards' rules also apply:
- `absent` is observed absence; `unknown` means not preserved or not reported;
- a dispersed spore does not identify a whole plant;
- a borrowed trait value cannot establish a co-occurrence.

## Pivotal specimens

Rows marked "Codex audit" were checked against the held primary text
(`audits/2026-10-29-pilot-and-contract-review.md` §3). The rest are card facts, to be checked
before use.

| Specimen | Age | Combination (evidence level) | Tests | Source (held?) |
|---|---|---|---|---|
| *C. barrandei*, holotype D552a,b, Barrandian | middle Sheinwoodian by correlation (associated material, lithology, fauna, relocated locality; the holotype's direct graptolite association is *M. flemingii*) | C1 + C3 **direct**; C4 unknown | the oldest C3 body; P3a; record identity for M3 | Libertín et al. 2018 + SI (held; Codex audit) |
| *C. pertoni* DE41, Welsh Borderland | Lochkovian | C1 (in situ *Streelispora newportensis*) + C4 evidence, on a single-sporangium fragment. The authors favour tracheids but cannot exclude tubes in incomplete elements. C3 only by taxon bridge (**composite**) | the reference combination, with its bridge stated | Edwards et al. 1992 (held; Codex audit) |
| Pridoli *C. pertoni* central strands | Pridoli | strand present; tracheidal identity inferred by comparison with younger forms (**transfer**) | keeps direct anatomy apart from inference; no Q5 error (the Ambitisporites card codes the tissue as unknown) | Edwards et al. 1992 p. 685 (held; Codex audit) |
| Whitcliffian tracheid-bearing axis, Capel Horeb, Powys | lower Whitcliffian (late Ludlow) | C4 **direct** on an isolated unbranched axis 10 mm long; no sporangium or branch attached; found with *Cooksonia*-type sporangia | the oldest C4, with no producer link (Q5: Morris et al. 2024 overstate it) | Edwards and Davies 1976 (held, read); Edwards 1979 (held, OCR) |
| Homerian *Cooksonia* cf. *pertoni*, TCD22944–22956, Co. Tipperary | Homerian | C3; anatomy transferred from younger *C. pertoni* in Hooper SI Table 4 (**transfer**) | M3 record identity | Edwards and Feehan 1980, Edwards et al. 1983 (held); Hooper SI (held; Codex audit) |
| *Ficoiditheca aenigma*, V.68228(1), V.68258(1), Brown Clee Hill | early Lochkovian | two sporangia on each branched axis with in situ palynomorphs. The permanent-dyad diagnosis is best shown in V.68222(1) and V.68263(1): C2 + C3 **composite** | P3a/P3b proxy specificity: a branched cryptospore plant | Morris et al. 2012 (held; Codex audit) |
| *Partitatheca horrida*, Brown Clee Hill | early Lochkovian | C2. The branched axis with one terminal sporangium is Habgood's older fragment, reassigned on a stated spore interpretation, so C3 is unconfirmed. Conducting tissue unknown | proxy specificity; trace the original specimen in Habgood 2000 | Edwards et al. 2012 (held; Codex audit) |
| Eophytes generally | Pridoli–Lochkovian | C2; leptoid-like cells, no water-conducting cells; mostly single terminal sporangia | P2 links under each placement | Edwards et al. 2021a (held) |
| *Tortilicaulis offaeus*, HD743/01, Brown Clee Hill | early–middle Lochkovian | C1 + C3 + C4 **direct** on one specimen (SEM spores, two attached sporangia, SRXTM thickenings); tracheid ultrastructure unresolved | the first direct C1 + C3 + C4; a plant long read as bryophyte-like | Morris et al. 2024 (held) |
| *Velatitetras*-producing plant, NMW96.11G.3, Brown Clee Hill | early Lochkovian | C2 + C3 **direct**; C2 contested (immature-tetrad alternative, p. 141); C4 not demonstrated | proxy specificity: a branched tetrad producer | Edwards et al. 1999 (held) |
| *Aglaophyton major*, Rhynie | Pragian–?earliest Emsian | C3 **direct** (connected sporangial pairs Pb4601/B/R/10 and /24; Pb4601/C/L/2); conducting cells without differential thickening. Its trilete statement reviews older work, so C1 is a **transfer** until an aperture is tied to a connected specimen | C1 and C3 without C4 | D.S. Edwards 1986 (held; Codex audit); Rhynie age from its dating sources |
| *Horneophyton lignieri*, Rhynie | as above | C1 + C3; C4 disputed: tracheids (MGLame-18) against transfer-cell-like cells (NHMUK slides) | whether a second polysporangiophyte without tracheids exists | Kenrick and Long 2025, Cascales-Miñana et al. 2019 (held); Wellman et al. 2003 (needed) |
| *Nothia aphylla*, Rhynie | as above | C1 inferred from the in situ genus *Retusotriletes*; C3 with lateral sporangia; no thickenings, shown mainly in rhizome strands | C1 and C3 without C4, with both qualifications | Kerp 2017, El-Saadawy and Lacey 1979 (needed, tier 1) |
| *Rhynia gwynne-vaughanii*, Rhynie | as above | C1 + C3 + C4 (S-type) | the same-deposit C4 comparator | Kerp 2017, Kenrick and Crane 1991 (needed, tier 1) |
| Dispersed record | Darriwilian (C2); Katian, with Sandbian contested (C1) | first occurrences only | observed order | F3's E1 and E2 evidence; Rubinstein and Vajda 2019, Steemans et al. 2009 (needed, tier 1) |
| Zbrza | Hirnantian host rock: a conditional minimum for the fragments | C3 claimed; plant status disputed; no in situ spores | M3 alternative reading only | Salamon et al. 2018 (held) |

Sources marked "needed" are in `first-study-literature.csv`, and the reference scout is collecting
them. Scoring of a row waits for its source.

## Published placements to compare

No new phylogenetic inference is run.
- **Hooper et al. (2026)** (deposit, read 2026-10-29, O):
  - two fossil-inclusive trees: `zygnema sister.tre`, with eophytes as sister to the
    polysporangiophytes, and `eophyte sister.tre`, with eophytes as sister to all other
    embryophytes;
  - both put *Cooksonia* on the lycophyte line and *Tortilicaulis* with *Horneophyton*;
  - crown states as above.
- **Clark et al. (2023):** eophytes as stem-tracheophytes. Matrix and trees held; main text needed.
- **Card-level placements** (Edwards et al. 2021a; Kenrick and Crane 1997, as cited by Kerp 2017
  and Morris et al. 2024): context only, unless their trees are obtained.

## Comparison rules (declared before any F3 verdict is read)

1. **Three links per proposition** (crown state, persistence, origin timing), each scored
   supported, contested, contradicted or unresolved, per placement and per method.
   - Marginal outputs are reported as published, with every state kept.
   - They are never multiplied, pooled across methods or ranked (`primer.md` §5.3; A1).
2. **P3b splits into record identity and proxy specificity.**
   - Record identity is scored per calibration specimen.
   - Proxy specificity is scored for the admitted frame. A well-documented C3 plant outside
     total-group Tracheophyta falsifies only the universal claim.
3. **Evidence levels stay separate.** A composite or transfer never becomes direct.
4. **Observed order and acquisition order stay separate.** First occurrences (with their age
   evidence) give observed order. Acquisition order is stated only conditional on a placement.
   Unresolved pairs and repeated origins are allowed.
5. **Node statements combine four things:**
   - an F3 verdict;
   - the status of each of the three links;
   - the evidence levels;
   - for any statement about a lineage's existence, the independent restriction on rarity,
     confinement or delay (`f3-shape.md` §3).

   They are reported as "verdict, under history class *H*, reading *R*, placement *S*". An
   unresolved link makes the node statement conditional on an explicit assumption, not void.

## A conditional inference the pilot can deliver (I)

Suppose F3, under a declared history class *H*, finds trilete encounter before a time *T* within
the Darriwilian (469.4–458.2 Ma) incompatible with the absences. Those absences come from the
interval whose units yield cryptospores, the positive control.

The crown is then younger than *T* if three things hold:
- P1's crown state (supported for the aperture under every published output above);
- P1's persistence, supported under Hooper et al.'s models, with retention R(L) carried as an
  explicit factor (third result);
- the independently justified rarity restriction.

Cryptospore producers in units older than *T* then predate the crown. They are stem
embryophytes, or, on the developmental-precursor reading, not assignable to either. Units
younger than *T* are not placed by this argument.

Without persistence, the verdict constrains only the encounter of trilete producers. Reading
that as their rarity needs the detection assumption D1.

## Outputs

1. A mapping table for M1–M3: each link's status under each placement and method, the pivotal
   specimens and their evidence levels, and the single observation that would most change each
   status.
2. The observed chronology of C1–C4: earliest secure specimens, age basis and alternative
   readings (level 1 of `innovation-scope.md`).
3. The supported combinations and orderings (level 2), including dissociations: C1 + C3 without
   C4, and C2 + C3 without C1.
4. The conditional node statements, written once F3's verdicts exist.

## Division of work

- **Claude:** specification, reading the pivotal primary texts as they arrive, scoring and
  synthesis.
- **Codex:**
  - the deposited-output extraction (done);
  - cross-family audits of specimen facts against primary texts;
  - the frame tranche.
- **Reference scout:** acquisition, from `first-study-literature.csv`.

## Consult triggers

- **Re-estimating ancestral states is authorised** (Barry, 2026-10-30: "widened scope is fine,
  proceed with the new ancestral-state analysis as/when appropriate"). Claude and Codex judge
  further scientific scope themselves and report it. Joint origin inference (level 3) and new tree
  inference still get their own design before they start.
- **Flag, do not wait,** where a specimen reading turns on an expert's judgement (Horneophyton's
  conducting cells; the Homerian material). Sending is Barry's decision.
- **Report unresolved, not escalate,** if no published placement separates the readings.

Questions served: Q2 (pivotal records), Q4 (producer links), Q6 (observations only), Q1 (node
layer). Q7's reanalysis and level-3 origin intervals stay out of scope; M3's record-identity audit
also touches Q9.
