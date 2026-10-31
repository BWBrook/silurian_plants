# Loop 1 close: what the record says about the three clock maxima

Draft for joint reconciliation. Claude Opus 5.5 (`claude-opus-5-5`), 31 October 2026, after both
counter-reviews (Claude on sprint 2, `f08afb4`; Codex on sprint 1, `71d69df`). Questions Q1, Q2 and
Q5. This memo closes Loop 1 of `docs/plan-f3.md` (step 6) under `docs/f3-shape.md` v3 once Codex
accepts or amends it. Proposals are marked as such; items already adopted cite their record.

## The answer

Loop 1 asked under which explicit sampling and biological assumptions older origins are
incompatible with the fossil absences behind the clock maxima (`f3-shape.md`). Of the three
maxima, only the trilete-spore one (M2) is testable from the assembled record, and it is testable in
one basin.

| Maximum | Testable? | What holds under every declared reading and variant | What depends on a reading or assumption |
|---|---|---|---|
| **M2**, 459.1 Ma, E1 trilete spores | Yes: Murzuq cuttings (Abuhmida 2013), qualified on 14 design/ρ pairs | Sustained trilete encounter at the Llandovery reference level before 459.1 Ma is incompatible with the 28 empty Darriwilian–Hirnantian cuttings at ρ ≥ 0.25. Low encounter (one tenth of reference or less) is compatible with any origin age. | Every number depends on ρ, the older-to-reference transport ratio, which no source measures. The window endpoint is 462.6, 464.1 or 467.1 Ma at ρ = 1, 0.5 or 0.25, and unbounded at ρ = 0.1. The weighted post-459.1 read-out is about 0.18 at ρ = 1. |
| **M1**, 515.5 Ma, E2 cryptospores | No admitted design among ten assessed source groups and frames | No older unit before the main-reading first appearance is both a secure E2 zero and part of a frame that passes the screen. The one secure older zero (Borenshult 71.1 m) fails the screen (LR 2.21). | Under the inclusive reading, the Cambrian Stage 4 forms *are* E2, with stage support 514.5–506.5 Ma. M1 then becomes an occurrence and dating question, not an absence test. |
| **M3**, 431.2 Ma, E3 polysporangiate bodies | No: no held source has a searched-material denominator | Fossil-free prose (Edwards & Feehan 1980) is genuine negative evidence without an n. | The *C. barrandei* total-group reading (`f3-shape.md`) bears on the maximum's fossil basis. That is synthesis, not an absence test. |

**In plain terms.** Hooper et al.'s 459.1 Ma maximum rests on the absence of older trilete spores.
At Llandovery-like levels, trilete producers delivering to the Murzuq shelf are excluded for more
than a few Myr before 459.1 Ma, if older cuttings recover spores as well as the reference does.
Producers that were rare, or poorly delivered, are not excluded. The same cuttings bound encounter
*after* 459.1 Ma, where the clock places the crown, to below about a fifth of the Llandovery level
(exposure-weighted, ρ = 1). The record is therefore equally empty for an origin shortly before the
maximum and for one after it. The absence argues against an old, abundant, well-delivered crown
flora. It does not by itself fix the crown's age.

## Reconciliation of the four open items

### 1. What the qualification establishes (coverage interpretation)

**Agreed with Codex:** the bounds are retained with the finite-grid statement. They are not
described as having 95% coverage conditional on a claim being made.

**Proposed sharpening:** the adopted criterion is ordinary confidence-set coverage, and it is the
right property for this use.
- For each tested truth, P(the delivered bound excludes the truth | the potential screen passes)
  ≤ 0.05 on the grid (worst observed 38/1,000). An abstention is the trivial set, so it covers.
- This is the Neyman guarantee every confidence interval offers.
- It was adopted as "unconditional coverage" in Codex message 2496 (`plan-f3.md`, "Open between
  Claude and Codex").
- It suits a single pre-declared design read once, with all seven frames and every variant
  reported.

**P(wrong | a claim was made) is a different quantity**, and no frequentist procedure controls it. It
depends on where the truth lies relative to the bound, which only a prior can weight. The
acceptance tables show this directly. I recomputed them from the 14 acceptance replicate files and
matched Codex's totals exactly: 529,550 claims and 3,780 misses.

| Truth cell (MZ, ρ = 1) | Passing | Claims | Misses | Misses / claims |
|---|---:|---:|---:|---:|
| B3 (constant at H0 f*(459.1)), H0 intensity | 1,000 | 703 | 0 | 0 |
| B4 (reference level on (459.1, 462.6], zero on (τ0, 459.1], reference level younger than τ0), window f = 1 | 1,000 | 60 | 20 | 0.33 |
| All cells and designs, window f = 1 | 168,000 | 7,707 | 70 | 0.009 |
| All cells and designs, H0 intensity | 168,000 | 60,656 | 847 | 0.014 |

- **B4 is a boundary case.** Its history is the most extreme one compatible with the real Murzuq
  window claim (462.6 Ma).
- **At a boundary, claims are rare (6%) and errors are close to the error budget (2%).** So the miss
  fraction among claims is large by construction. A level-α test behaves the same at its null
  boundary.
- **Averaged over the grid, the miss fraction among claims is 0–3.4% per quantity.** That figure
  too reflects how the grid was weighted, so it is not reported as a property.

**Proposal: close the selected-result target rather than leave it open** (`questions.md` currently
"retains the selected-result confidence question").
- **The obstacle.** A procedure valid conditional on making a claim must condition on the claim
  event. For a window claim, that event fixes the empty older units, which carry the evidence. So a
  conditionally valid set uses only the reference counts. Under the model, those counts carry no
  information about older encounter, and the set would be trivial.
- **If Barry wants "how probable is it that the 462.6 Ma bound is wrong?"**, that is a Bayesian
  question. It needs a declared prior over encounter histories and is a different analysis, not a
  requalification.
- **Recommendation:** no such layer in Loop 2. The prior over early encounter histories is exactly
  what the record cannot inform.

**Reporting form adopted for all bounds.** Give the bound, ρ and the design. Then add: "a 95%
confidence bound in the coverage sense: on the tested grid, at most 3.8% of screen-passing records
yield a bound excluding the truth; abstentions count as covering. It is not a probability that
this bound is correct."

### 2. QB qualification scope

**Accepted.** QB-CO's H0c is an unqualified diagnostic. In seven acceptance replicates, the selected
first appearance moved younger than the simulated breakpoint, so the realised-interval truth is not
constant. QB's qualification is H0m/H0/H1. QB main/zero is an inadmissible coding diagnostic.
Libya's scope is unchanged, and no reported primary number changed.

### 3. Cambrian age support for the inclusive reading

**Accepted, with one clarification.** A Stage 4 assignment gives age support 514.5–506.5 Ma
(`data/timescale.csv`). The occurrence may lie anywhere in it, so the gap below M1 is about
1–9 Myr. It is not a point age of 514.5 Ma, as my review implied.
- **F3's dating convention.** τ uses the oldest possible age of the unit that holds a detection. An
  F3 analysis would therefore enter such a detection at 514.5 Ma. That is a declared conservative
  convention for τ, not an occurrence date.
- **The practical conclusion stands either way.** Under inclusive, testing M1 needs productive
  material older than the whole of Stage 4, and tighter dating of the Stage 4 forms themselves.

**Also accepted:**
- Borenshult 71.1 m is a secure older E2 zero under main. My sentence that no older unit is a secure
  zero was wrong. The correct statement is that no admitted design contains one.
- The 35 exact-Hawaz materials are 25 cores, eight cuttings and two unspecified materials, not 35
  cuttings. Only ten enter the primary cutting contrast.

### 4. Shared E2 dispersal-unit rule (proposal for joint adoption)

The programme already defines cryptospores in Richardson's (1988) sense, as adopted by Edwards et al.
(2014): permanent tetrads or dyads, or hilate or enveloped monads, without a trilete mark
(`taxa/ordovician-cryptospores.md`; pilot criterion C2, `pilot-traits.md`). The E2 rule applies that
definition to dispersed reports.

| Reported form | main | inclusive, outlier |
|---|---|---|
| **E2-core.** Permanent dyads and tetrads (fused or unfused, naked or enveloped), hilate monads, envelope-enclosed monads | detected, subject to the record's age and affinity reading | detected |
| **E2-ambiguous.** Naked inaperturate monads with neither hilum nor envelope; monads reported only as physically separated from permanent polyads, without a hilum | unresolved, never zero | detected |
| **Pooled reports** (colour groups, "cryptospores/spores" totals, percentage fractions) | detected only where the unit's pooled taxa include an E2-core form; otherwise unresolved | detected |

**Basis, from Wellman et al. (2015), held and read in this task:**
- **Their Table 1 (p.115) separates the three monad kinds:**
  - "cryptospore monads" (*Rugosphaera*);
  - "spores physically separated from cryptospore polyads" (*Imperfectotriletes*, cf. *Laevolancis
    chibrikovae*);
  - "hilate spores" (*Laevolancis divellomedium*, *Chelinohilates*).
- **Hilate spores are naturally dissociated from dyads** (p.124).
- ***Rugosphaera?* cerebra "appear[s] to be naked"**, with a tight envelope not excluded (p.114).
- **cf. *L. chibrikovae* is "not considered to be a true hilate cryptospore"** but a monad formed by
  physical dissociation of a permanent dyad (p.122).

**Effect on current outcomes: none.** I checked the rule against all 147 E2 outcome rows and the
sprint-2 E2 ledgers.
- **Paraguay AS1-2835.** The only E2 detection that rests on a monad uses *L. divellomedia*, a hilate
  spore in Wellman et al.'s Table 1, so it is E2-core.
  - This corrects my review's description of it as a "naked monad". It is unenveloped, but hilate.
  - The supposed inconsistency with Qusaiba therefore does not exist.
- **Qusaiba.** The extraction ("dyad/tetrad rows only") is a conservative subset of E2-core. Every
  one of the 37 columns is already positive.
- **Borenshult.** The main-reading zeros are samples with no terrestrial palynomorphs charted.
- **Libya.** The E2 "Cryptospores/Spores" group enters no design. Before any E2 use, it must be split
  by taxon under the pooled-report row.

The rule matters for future cross-source E2 designs, where an older unit holding only E2-ambiguous
forms would otherwise be at risk of becoming a zero.

## Pivotal records and choices

A record or choice is pivotal if it flips a verdict or moves a bound by more than 1 Myr
(`plan-f3.md`, step 4).

- **M2.**
  - **ρ decides every quantitative statement.**
  - **The reference minimum** decides whether H2 is admitted (5 against 10).
  - **The material codes** at H2 4950/4990 ft and D1 4050/4200 ft decide H2 and D1 at ρ = 0.25.
  - **The 7287 ft core report** (prose against chart) decides only whether a core design could
    exist. Even accepted, that design is inadmissible.
  - **The between-core variance k** decides QB.
  - **Murzuq's older cuttings hold no trilete report in any declared variant.**
    - The material-type variants change the reference from 51/59 to 49/57 marked cuttings, and the
      older set from 28 to 26.
    - The Hawaz age allocation moves the window endpoints by up to 2 Myr (`2026-10-31-m2-real-designs.md`,
      "Limits"), so it is pivotal by the 1 Myr definition.
- **M1.**
  - **The affinity reading of the Cambrian forms** decides whether M1 is an absence question or an
    occurrence question.
  - **The disputed Darriwilian forms at Borenshult** (67.6 and 59.1 m) decide whether that frame
    passes. It passes (LR 6.28) only if they are coded as zeros, which the outcome rule forbids.
  - **Argentine 7999** (Dapingian) and **Samphire core 4** are the oldest disputed E2 candidates.
- **M3.** The *C. barrandei* total-group status, and Zbrza (Hirnantian) as the pivotal alternative.

## What the record cannot tell apart

- **Old and rare against young.** A crown origin before 459.1 Ma with trilete encounter below about
  0.17 of the Llandovery level (ρ = 1), or lower with poorer delivery, cannot be told apart from an
  origin after 459.1 Ma. The Late Ordovician cuttings that follow the maximum are themselves that
  empty.
- **An unsampled Sandbian pulse.** The Murzuq design has no sampled support on (452.8, 458.2] Ma. A
  reference-level pulse confined there has weighted mean zero (Codex's methods audit).
- **M1 at any intensity.** No admitted older frame exists. Under inclusive the forms fall within the
  maximum's own stage-scale uncertainty.
- **M3 at any intensity.** No denominator exists.

## Unresolved implementation limits

These are carried forward, not hidden:
- ρ is a scenario grid, not an estimate, and a misspecified ρ undercovers.
- The bounds hold only on the finite truth grid. Simultaneous coverage across curves is not
  established.
- There is no contamination model for caved positives. A recovery age is a reporting rule, not an
  indigenous first appearance.
- The estimator treats ages within a range as independent. Joint ordered chronologies are covered
  only by the declared simulation scenarios.
- The between-section variance cannot be estimated from one core per region.
- Engine roots are solved to 1e-3. The four decimal places in `m2_results.csv` are output digits,
  not accuracy.
- The Murzuq frame comes from a single study: one author, laboratory and chart system.

## Value of information: ranked evidence for Loop 2

Codex's ranking in `sprint2-results-and-value-of-information.md` stands. I add one item ahead of it,
because it attacks the quantity that decides M2 with data already held. The ranking is
qualitative.

| Rank | Evidence | Decision it could change | Status |
|---:|---|---|---|
| 0 (proposal) | **Cryptospore-referenced transport for M2.** Replace the free ρ with the weaker assumption that trilete spores and cryptospores share delivery and recovery between older and reference units. Each unit's co-recovered cryptospore abundance then becomes its exposure, and the estimand becomes trilete-producer output relative to cryptospore-producer output, compared with the Llandovery. | Converts the ρ grid into one assumption that can be examined, using held data. The Hawaz is cryptospore-rich: 20–44% of upper Hawaz assemblages against 5–15% in the middle–upper Tanezzuft (Abuhmida 2013, pp.395–396 and 402–403). So equal relative delivery would make an empty trilete record more informative, not less. | **Feasibility first:** does Abuhmida 2013 give per-sample cryptospore counts or proportions, or only interval summaries and presence marks? Sizes in the same Qusaiba assemblages are comparable: cryptospores 23–62 µm, triletes 24–44 µm (Wellman et al. 2015, Table 1). A design and qualification amendment would precede any result. |
| 1 | Independently constrained delivery and recovery ratios for M2 facies (Codex's item 1) | Which ρ scenarios deserve weight | Item 0 is one route to it. |
| 2 | A complete Cambrian sample roster with failed preparations and non-target recovery, specifically productive material older than 514.5 Ma; tighter dating of the Stage 4 E2 forms | M1 admission, or M1 as an occurrence test under inclusive | Leads: Baldwin 2004 (Bright Angel); the Balang Stage 4 *Tetrahedraletes medinensis?* (Wang et al. 2022, Table 1). Likely needs specialist contact; Barry decides on sending. |
| 3 | Irish or Loděnice searched-bed ledgers | M3 admission | Field and collection records; contact. |
| 4 | Re-examination of Argentine 7999, Samphire core 4 and the younger Samphire forms | E2 readings | Specialist adjudication. |
| 5 | H2/D1 material codes, 7287 ft and Hawaz age allocation | M2 variant stability | Mostly settled for the primary design. |

**Recommended direction for Loop 2.** Deepen M2, the only maximum the record can test:
- assess item 0's feasibility on the Abuhmida thesis, and declare and qualify the design if the
  thesis supports it;
- add a second basin with a Darriwilian–Katian older interval and a Llandovery reference in the
  same study, so the result is no longer a single-study frame. Candidates come from the Saudi Qasim
  and Qusaiba material and the Baltic sections already assessed.

M1 and M3 move by acquisition, not analysis. Pursue them in parallel through the closed-literature
list and specialist contact, which Barry sends.

## Structural review (for `decisions.md`)

- **Does the structure serve the next investigation?** Yes for M2:
  - the reading/outcome interface, the frozen declarations and the qualification contract with
    bound receipts carry over to a second basin or a cryptospore-referenced design unchanged;
  - the design adapter needs one new builder per frame.

  The M1 and M3 machinery is ready but has no admissible input.
- **Assumptions exposed:**
  - ρ dominates every quantitative result;
  - the qualification is confidence-set coverage, not post-selection reliability;
  - a stage assignment is age support, not an occurrence date;
  - the monad question had not been written down, although its answer was already in the programme's
    cryptospore definition.
- **Did evidence change a question?**
  - **Q1:** narrowed to "which delivery assumption, and which second frame?"
  - **Q2:** M1 under inclusive is now an occurrence-and-dating question.
  - **Q5 logs these corrections:**
    - the M2 note's original "P(false claim) ≤ 0.05" and "realistic early intensities" (corrected by
      Codex);
    - my "naked monad" and "no secure older zero" (corrected here);
    - the Stage 4 point-age reading (corrected by Codex).
