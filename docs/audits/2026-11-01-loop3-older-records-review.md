# Loop 3: older PBDB body-name audit

Codex (OpenAI), 1 November 2026. Scope: seven plausible or unplaced names among the PBDB rows older
than the 445.2--393.47 Ma pilot query but inside the 469.4--393.47 Ma inference domain:
*Alectorurus*, *Bythotrephis*, *Kazakhstanelia*, *Proaulopora*, *Zonotrichites lissaviensis*,
*Bojophyton pragensis* and *Phacelophyton yushanensis*. The complete older-only inventory contains
556 non-spore rows and 69 names; the parent review classifies the remainder at database-category
level. This audit does not claim source-level review of those other names and does not treat a PBDB
placement under Plantae as evidence of embryophyte affinity.

## Verdict

Among these seven candidates, no accepted embryophyte body was found. None belongs in B0, B1 or B2,
and none merits an inclusion sensitivity on the evidence read. Three are explicitly Nostocales cyanobacteria,
one is a dasycladalean green alga, two are algal/trace-fossil form genera, and one is the already
rejected *Boiophyton* dendroid graptolite. Their omission is a taxonomic exclusion, not a fossil
non-detection.

The important residual limit is narrower: the exact Czech specimen called *Alectorurus venosus*
and its 1956 source were not recovered for re-examination. The genus is an animal trace fossil and
the PBDB opinion assigning it to Plantae is explicitly “stated without evidence”; no positive
embryophyte character supports a sensitivity run. If the primary specimen is later shown to be a
different body fossil, it should be adjudicated afresh rather than admitted through the name alone.

## Evidence by candidate

### Explicit calcimicrobial taxa: no body-plant route

Liu et al. (2021; DOI `10.1017/jpa.2020.82`) systematically describe Middle--Late Ordovician
calcified cyanobacteria and associated microfossils from 1,330 thin sections across marine
carbonate-platform settings. Their abstract assigns *Zonotrichites*, *Proaulopora* and
*Phacelophyton* to Nostocales of cyanobacteria. This directly covers all nine PBDB
*Proaulopora ordosia* rows, the single *Zonotrichites lissaviensis* row and all three
*Phacelophyton yushanensis* rows. The PBDB filter inherited them through an unplaced Plantae branch
or curated name list; that database route does not supersede the describing source's affinity.

*Kazakhstanelia* is likewise a marine calcareous alga, not an unplaced terrestrial plant. Modern
systematic work treats it among Ordovician Dasycladales (Ulvophyceae), describing its calcareous
thallus in carbonate-platform assemblages. The Tennessee PBDB occurrence is incidental to a paper
on a rhombiferan cystoid and carries no land-plant characters. It is excluded from all three body
categories even though the exact incidental specimen was not re-read.

### Historical “fucoids”: the alternative readings are both non-embryophyte

The Argentine museum inventory identifies the holotype and paratype of *Bythotrephis cuyanus*
(MCNAM-PB 938 and 939) as Algae, Chondritaceae. Ichnological revision treats
*Bythotrephis*/*Buthotrephis* as branched feeding burrows, many historically confused with
*Chondrites*. Whether this particular material is a marine alga or an ichnofossil remains open
because Rusconi (1954) was not re-read. The distinction is immaterial to B0--B2: neither reading is
an embryophyte body.

*Alectorurus* has the same history of plant-like form naming. Its monotypic type species,
*Fucoides circinatus*, was re-examined from topotypical material as a vertically oriented spreite
burrow (Jensen & Bergstrom 1995; DOI `10.1080/11035899509546217`). Andrews's fossil-plant index
already gave the older reading only as “alga?”, and PBDB's later opinion placing the genus under
Plantae is “stated without evidence”. The queried occurrence, *A. venosus*, comes from a trilobite
monograph rather than a botanical treatment. The exact species identity is unresolved, but there
is no evidential basis for treating it as an uncertain land plant.

### *Bojophyton* is the existing rejected *Boiophyton* record

PBDB occurrence 51644 is linked in the curated tail to `M-boiophyton` and uses the spelling
*Bojophyton pragensis*. It is the same Prague Basin claim already traced in
`docs/rejected-records.md` entry 1. Internal structure led Kenrick et al. (1999) to reassign the
putative plant to a dendroid graptolite; Maletz (2020) retains the Darriwilian holotype NM-D418 as
the callograptid *Boiophyton*. The database occurrence is a formation-level alias, not a second or
unresolved embryophyte body.

## Consequence for the inference domain

Extending recovery histories back to 469.4 Ma does not require admitting every PBDB row in that
domain as a focal occurrence. These 17 occurrence rows are observed non-embryophyte or rejected
fossils. They may contribute to an all-taxa collecting-effort proxy if they belong to distinct
collections, but they must not enter the numerator for B0--B2. Conversely, excluding them cannot be
described as evidence that embryophyte bodies were searched for and absent at those localities.

`data/macro/older_candidate_adjudications.csv` gives occurrence and collection identifiers, age
ranges, source routes, adjudications and remaining limits. The seven rows reconcile to 17 PBDB
occurrences: 1 *Alectorurus*, 1 *Bythotrephis*, 1 *Kazakhstanelia*, 9 *Proaulopora*, 1
*Zonotrichites*, 1 *Bojophyton* and 3 *Phacelophyton*.

Both DOI strings introduced by this audit were verified directly against Crossref on 1 November
2026 without a contact email. Crossref returned `10.1017/jpa.2020.82` for “Diversity and
systematics of Middle-Late Ordovician calcified cyanobacteria and associated microfossils from
Ordos Basin, North China” (Cambridge University Press) and
`10.1080/11035899509546217` for “The trace fossil *Fucoides circinatus* Brongniart, 1828, from
its type area, Västergötland, Sweden” (Informa UK Limited).

## Residual risk and recommendation

The seven-name decision is robust to the unresolved alga-versus-trace distinction for the two
historical fucoids because both alternatives exclude embryophytes. Independent specialist review
would not materially change the Loop 3 decision unless it recovered evidence that the exact
*Alectorurus venosus* specimen is taxonomically unrelated to the trace-fossil genus. No such
evidence was found in two bounded searches.

Proceed with all seven excluded from B0--B2 and no inclusion sensitivity. The analytical pipeline's
exact 241-name roster over 445.2--393.47 Ma plus the curated tail remains the positive-record input;
the older screen documents its incompleteness and rejected alternatives rather than silently
turning older database names into tested positives or absences. Label the remaining older-only names
“database-category screened, not source-audited” unless the parent inventory finds another plausible
axial, fertile or anatomically preserved body. Do not infer a negative trial from these taxonomic
exclusions, and do not use the 556-row inventory as a denominator of searched rock.
