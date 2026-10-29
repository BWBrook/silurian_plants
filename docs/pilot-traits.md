# Trait pilot: the mappings behind the maxima

Draft specification by Claude Opus 5.5, 29 October 2026. No analysis has been run; nothing here
is a finding. It becomes the adopted design once Codex has reviewed it, and objections go to the
Board (discussion 99).

**Decisions behind it.**
- **Scope** (Barry, Codex chat, 2026-10-29): "Excellent, we're aligned." This accepted F3 plus a
  bounded pilot on trait combinations and supported orderings (`innovation-scope.md`).
- **Framing** (Barry, Claude chat, 2026-10-29): "Yes, frame it so". This answered the question
  "Should the trait pilot test the trait-to-node mappings behind M1–M3?"

A `gpt-6.1-sol` audit of the first draft returned 17 findings, all accepted
(`audits/2026-10-29-pilot-spec-audit.md`). Observations (O), interpretations (I) and
speculation (S) are marked where it matters.

## Why this pilot

F3 asks whether the fossil absences are compatible with a *trait* being encountered before a
candidate time *T* (`f3-shape.md`, data layer). The clock maxima are claims about *nodes*. F3's
node layer rests on a named mapping from each trait to a node (`f3-shape.md`, first table and
§3), and so far that mapping is only named, not assessed.

The pilot assesses each mapping from two kinds of evidence: specimen-level trait combinations,
and published placements and ancestral-state reconstructions. Each node statement F3 makes then
says what it rests on. This makes the pilot the second half of F3's conditional claim, not a
separate trait table. Its biological result is which orderings and node statements survive the
alternative readings, and what observation would settle the rest.

## The mappings

An absence argument for a maximum needs the trait to have arisen **no later than the node**:
either in the node's ancestor, or earlier on its stem. The pilot tests these temporal
propositions. "Ancestral to the crown" is one way to satisfy them, not the only way.

| Maximum | F3 event | Proposition the absence argument needs | It fails if |
|---|---|---|---|
| M1, 515.5 Ma, crown Embryophyta (Morris et al. 2018) | E2 cryptospores | **P2:** cryptospore production arose no later than the crown node | cryptospores first arose after the crown's origin, for example secondarily within it with no earlier producers |
| M2, 459.1 Ma, crown Embryophyta (Hooper et al. 2026) | E1 triletes | **P1:** trilete production arose no later than the crown node. Hooper et al. reconstruct it in the crown ancestor | trilete production first arose inside the crown after its origin |
| M3, 431.2 Ma, crown Tracheophyta (Hooper et al. 2026) | E3 bodies | **P3a:** a branched sporophyte with several sporangia (C3, below) arose no later than the crown-tracheophyte node | the crown ancestor lacked C3, and C3 arose within the crown |

M3 also needs a second proposition for its fossil basis. **P3b:** C3 bodies belong to
total-group Tracheophyta. Without P3b, the oldest C3 body (*C. barrandei*, or M3's Homerian
basis) need not be a tracheophyte record, and F3's first appearance and reference window would
mix lineages. P3b fails if C3 also arose outside the total group. The P3 alternatives are those
named in `f3-shape.md` and the cards:
- polysporangiophyte bodies are total-group, not crown, tracheophytes;
- *Cooksonia* is a morphotype.

**What the competing readings do to P1 and P2** (I).
- **The traditional reading** (cryptospores first, triletes derived; `taxa/ordovician-cryptospores.md`)
  breaks P1, so E1 says nothing about the crown. P2 holds.
- **Hooper et al.'s reading** (`primer.md` §5.3) supports P1. P2 then turns on when cryptospore
  production arose:
  - P2 holds if cryptospores arose on the stem before the crown, for example in eophytes placed
    on the embryophyte stem with their cryptospory older than the crown node.
  - P2 fails if cryptospores arose only afterwards, secondarily within the crown.
  - The published trees place the eophytes but do not date their cryptospory relative to the
    crown.
- **The developmental-precursor reading** (Strother and Taylor 2024, as cited by
  `taxa/ordovician-cryptospores.md`) takes the oldest cryptospores out of the embryophyte stem
  and crown altogether.
- **Consequence:** M1 and M2 rest on different propositions with different support. F3's E2 and
  E1 verdicts are reported with the proposition each needs, never as two interchangeable
  constraints on one node.
- **Not settled by the maxima's ages:** which verdict constrains the crown more tightly. That
  depends on the data: exposure, reference rates and history class.

**A conditional inference the pilot can deliver** (I). Suppose F3, under a declared history
class *H*, finds trilete encounter before a time *T* within the Darriwilian (469.4–458.2 Ma)
incompatible with the absences. Those absences come from the interval whose units yield
cryptospores, the positive control. Then two statements follow, each conditional:
- **With P1**, together with the independently justified restriction that a crown lineage could
  not have been rarer, more confined or more delayed than *H* allows (`f3-shape.md` §3), the
  crown is younger than *T*.
  - The cryptospore producers in units older than *T* then predate the crown. They are stem
    embryophytes, or, on the developmental-precursor reading, not assignable to either.
  - Units younger than *T* are not placed by this argument.
- **Without P1**, the verdict constrains only the encounter of trilete producers. Reading that as
  their rarity needs the detection assumption D1.

So one F3 result becomes one of a few declared biological statements, the kind of tentative but
precise result `innovation-scope.md` asks for.

## Characters and coding rules

| ID | Character | Scored present when | Kept apart from |
|---|---|---|---|
| C1 | trilete production | in situ monads with a trilete aperture, either the mark observed or the spores assigned to a genus defined by it (say which) | separation from tetrads alone (it shows monads, not the aperture); dispersed triletes (first occurrences only, E1); irregular trilete-like marks (`taxa/zbrza-assemblage.md`) |
| C2 | cryptospore production | in situ permanent dyads or tetrads, or hilate or enveloped monads, without a trilete mark (the definition used by `taxa/ordovician-cryptospores.md`) | dispersed cryptospores (E2); dyads and aborted tetrads inside trilete-producing sporangia (`taxa/horneophyton-lignieri.md`) |
| C3 | branched sporophyte with several sporangia | an attached dichotomy with sporangia attached on at least two branches, or several sporangia attached to one branched plant | a branched axis with a single attached sporangium (scored "branched, C3 unconfirmed"); unbranched axes; isolated sporangia |
| C4 | demonstrable tracheids | elongate cells with secondary wall thickenings, shown in situ, with the organ examined stated | hydroids and leptoid-like cells; "disputed", which carries each reading |

The rules are those of the cards:
- `absent` means observed absent; `unknown` means not preserved or not reported. A combination
  is only established on one plant or one attached specimen.
- A dispersed spore does not identify a whole plant.
- A trait value borrowed from another taxon cannot establish a co-occurrence.

## Pivotal specimens (candidates; card facts, all cards draft)

Each fact below comes from a card or the primer and is checked against the primary text before
the analysis uses it.

| Specimen | Age | Combination | Tests | Primary source (held?) |
|---|---|---|---|---|
| *Partitatheca*, Brown Clee Hill | early Lochkovian | C2; one isotomously branched naked stem with one attached sporangium, so C3 unconfirmed; water conduction not shown | P3b, if branched eophytes bear several sporangia and are placed outside total-group Tracheophyta. A key taxon in Hooper et al.'s reconstructions: its enveloped dyads apparently drive their all-rates-different model's enveloped ancestor, a result about the envelope; their trilete result holds across all models (`primer.md` §5.3) | Edwards et al. 2012 (held); Morris et al. 2012 (held) |
| Eophytes generally, Ludford Lane and Brown Clee Hill | Pridoli–Lochkovian | C2; leptoid-like cells, no water-conducting cells; mostly single terminal sporangia, branching in some genera | P2's timing and P3b, under each placement below | Edwards et al. 2021a, card citation (library entry dated 2022; held) |
| *Cooksonia pertoni*, charcoalified, North Brown Clee Hill | Lochkovian | C1 + C3 + C4 (annular tracheids; in situ triletes) | the reference combination | Edwards et al. 1992 (held); Edwards and Kenrick 2015; Habgood et al. 2002 (closed-literature row). The Ambitisporites card attributes a conducting strand to *Pridoli* *Cooksonia* (Edwards et al. 1992, via Wellman et al. 2015), against the Cooksonia card's Lochkovian restriction: settle from the primary text (Q5 if a summary fails) |
| Whitcliffian tracheid-bearing axes, South Wales | late Ludlow | C4 on branched axes; attachment to *Cooksonia*-type sporangia reported by Morris et al. 2024, tabulated by Edwards 1979 as "Y-axes + tracheids" | the oldest C4, with an insecure producer link | Edwards and Davies 1976 (held) |
| *C. barrandei*, Barrandian | mid-Sheinwoodian | C1 (10–15 µm); C3 as "polysporangiate" in the source's title | the oldest C3 body, older than M3's Homerian basis; P3b | Libertín et al. 2018 (held) |
| Homerian *Cooksonia*, Co. Tipperary | Homerian | C3; what else is preserved is to be read | M3's stated fossil basis | Edwards and Feehan 1980; Edwards et al. 1983 (held) |
| *Tortilicaulis offaeus*, Brown Clee Hill | early–middle Lochkovian | C1 + C3 + C4 (synchrotron, three of five specimens) | C4 in a plant long read as bryophyte-like | Morris et al. 2024 (to check) |
| *Aglaophyton major*, Rhynie | Pragian–?earliest Emsian | C1 + C3; hydroid-like cells without differential thickening | C1 and C3 without C4: polysporangiate bodies need not be crown tracheophytes. The library title reads "a non-vascular land-plant" (D.S. Edwards 1986) | D.S. Edwards 1986 (held) |
| *Horneophyton lignieri*, Rhynie | as above | C1 + C3; C4 disputed | whether a second polysporangiophyte without tracheids exists | Kenrick and Long 2026, via card (to check) |
| *Nothia aphylla*, Rhynie | as above | C1 inferred from the in situ genus *Retusotriletes* (mark not described in the sources read); C3 with lateral sporangia; no thickenings, shown mainly in rhizome strands | C1 and C3 without C4, with both qualifications | Kerp 2017, via card |
| *Rhynia gwynne-vaughanii*, Rhynie | as above | C1 + C3 + C4 (S-type) | the same-deposit C4 comparator | Kerp 2017, via card |
| Dispersed record | Darriwilian (C2); Katian, Sandbian contested (C1) | first occurrences only | observed order of C2 before C1 | F3's E1 and E2 evidence |
| Zbrza | Hirnantian host rock: a conditional minimum for the fragments | C3 claimed; plant status disputed; no in situ spores | M3 alternative reading only | Salamon et al. 2018, via card |
| Living bryophytes and tracheophytes | — | spore type from Hooper et al.'s matrix, not from the cards (which record `unknown`) | P1 and P2 at the crown node; P3a from the cards and Clark et al.'s matrix | `data/external/deposits/` |

## Published placements to compare

No new phylogenetic inference is run.
- **Hooper et al. (2026), ancestral-state trees** (deposit, `02. Ancestral State
  Estimation.zip`; read 2026-10-29, O):
  - `zygnema sister.tre` places the eophytes (*Partitatheca*, *Lenticulatheca*) as sister to the
    polysporangiophytes, inside total-group Tracheophyta.
  - `eophyte sister.tre` places them as sister to all other embryophytes, on the embryophyte stem.
  - Both trees put *Cooksonia* on the lycophyte line, sister to (*Renalia*, (*Zosterophyllum*,
    lycophytes)), and *Tortilicaulis* with *Horneophyton*.
  - **To reconcile in review:** M3 uses *Cooksonia* cf. *pertoni* as a total-group record for a
    crown-tracheophyte maximum, while these trees place *Cooksonia* inside the crown (I). Read
    against Hooper et al.'s calibration text (Supplementary Table 4, held), with Q9.
- **Hooper et al. (2026), ancestral-state outputs:**
  - Methods: parsimony, equal rates, all rates different and stochastic character mapping, on
    the extant tree and both fossil trees.
  - Read the embryophyte crown-node states, every state including state 0, for two characters:
    - the aperture character `X21`: not present, hilate, proximal monolete, proximal trilete,
      lateral or distal;
    - the dispersal-unit character `X26`: n/a, tetrad, dyad, hilate, trilete spore or
      inaperturate monad.
  - `X26`'s last state pools trilete and inaperturate monads, so `X21` decides the trilete
    aperture.
  - The labels come from `labelsperchar.csv`; their correspondence to the master matrix's
    columns is to be confirmed.
- **Clark et al. (2023):** the morphological analysis that recovers eophytes as
  stem-tracheophytes. Matrix and trees are held in the deposits.
- **Card-level placements** (Edwards et al. 2021a; Kenrick and Crane 1997, as cited by Kerp 2017
  and by Morris et al. 2024): context only, unless their trees are obtained.

## Comparison rules (declared before any F3 verdict is read)

1. **Status of P1, P2 and P3a, per placement scenario and per ancestral-state method.**
   - *Supported:* the published reconstructions agree that the trait was present at or before
     the node.
   - *Contested:* methods or placements disagree, or the timing relative to the node is not
     dated (as for stem cryptospory).
   - *Contradicted:* every method puts the trait's origin after the node.
   - Marginal probabilities are reported as published, with every state kept, never pooled
     across methods. No method is ranked (`primer.md` §5.3).
2. **P3b is scored from specimens and placements:**
   - A well-documented C3 plant placed outside total-group Tracheophyta, under a scenario,
     contradicts P3b for that scenario.
   - A disputed specimen, or an unconfirmed C3, makes P3b contested, not contradicted.
3. **Observed order and acquisition order stay separate.** First occurrences (with their age
   evidence) give observed order. Acquisition order is stated only conditional on a placement.
   Unresolved pairs and repeated origins are allowed.
4. **Node statements combine three things:** an F3 verdict, a proposition's status, and, for any
   statement about a lineage's existence, the independent restriction on rarity, confinement or
   delay (`f3-shape.md` §3). They are reported as "verdict, under history class *H*, under
   reading *R*, under placement *S*". A contested proposition makes the statement conditional,
   not void.

## Outputs

1. A mapping table for M1–M3: the status of P1, P2, P3a and P3b under each placement and method,
   the pivotal specimens, and the single observation that would most change each status.
2. The observed chronology of C1–C4: earliest secure specimens, age basis and alternative
   readings (level 1 of `innovation-scope.md`).
3. The supported combinations and orderings (level 2), including dissociations: C1 + C3 without
   C4, and C2 with branching but no C1.
4. The conditional node statements of the kind above, written once F3's verdicts exist.

## Division of work (proposal)

- **Claude:** this specification, the reading of the pivotal primary texts, scoring and
  synthesis. This continues the occurrence adjudication assigned in `f3-shape.md`.
- **Codex:**
  - a review of this specification;
  - a cross-family audit of the pivotal-specimen facts against the primary texts;
  - extraction of the crown-node states from Hooper et al.'s output files by script, which is
    checkable work.
- **Codex (frame tranche):** continues independently; the pilot does not depend on it until the
  conditional node statements are written.

## Consult triggers

- **Barry decides** if the pilot comes to need re-estimating ancestral states on altered trees or
  matrices, or any tree inference, rather than reading published outputs. That would enlarge the
  agreed scope (`innovation-scope.md`).
- **Flag, do not wait,** where a specimen reading turns on an expert's judgement (Horneophyton's
  conducting cells; the Homerian material). Sending is Barry's decision.
- **Report unresolved, not escalate,** if no published placement separates the readings.

Questions served: Q2 (pivotal records), Q4 (producer links), Q6 (observations only), Q1 (node
layer). Q7's reanalysis and level-3 origin intervals stay out of scope; the *Cooksonia* placement
tension also touches Q9.
