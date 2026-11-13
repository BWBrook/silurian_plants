# Loop 1 close: what the record says about the three clock maxima

Closed by joint reconciliation on 1 November 2026. Claude Opus 5.5 (`claude-opus-5-5`) drafted this on 31 October after both
counter-reviews (Claude on sprint 2, `f08afb4`; Codex on sprint 1, `71d69df`). Revision 2, 1 November
2026: integrates Codex's amendments (Correspondence 2758, 2760 and 2761) on the coverage statement,
the E2 rule, the table scope and the Loop 2 framing. Codex confirmed the revision on 1 November,
with the primary-design count and E2 wording clarified. Questions Q1, Q2 and Q5. This memo closes
Loop 1 of `docs/plan-f3.md` (step 6) under `docs/f3-shape.md` v3; it does not close those research
questions or qualify the proposed Loop 2 analyses.

## The answer

Loop 1 asked under which explicit sampling and biological assumptions older origins are
incompatible with the fossil absences behind the clock maxima (`f3-shape.md`). Of the three
maxima, only the trilete-spore one (M2) is testable from the assembled record, and it is testable in
one basin.

| Maximum | Testable? | What holds in the qualified primary designs | What depends on a reading or assumption |
|---|---|---|---|
| **M2**, 459.1 Ma, E1 trilete spores | Yes: Murzuq cuttings (Abuhmida 2013), with 13 qualified design/ρ pairs; the fourteenth qualified pair is QB-CO at ρ = 1, which supplies no older M2 interval | Sustained trilete encounter at the Llandovery reference level before 459.1 Ma is incompatible with the 28 empty Darriwilian–Hirnantian cuttings at ρ ≥ 0.25. Low encounter (one tenth of reference or less) is compatible with any origin age. | Every number depends on ρ, the older-to-reference transport ratio, which no source measures. The window endpoint is 462.6, 464.1 or 467.1 Ma at ρ = 1, 0.5 or 0.25, and unbounded at ρ = 0.1. The weighted post-459.1 read-out is about 0.18 at ρ = 1. |
| **M1**, 515.5 Ma, E2 cryptospores | No admitted design among ten assessed source groups and frames | No older unit before the main-reading first appearance is both a secure E2 zero and part of a frame that passes the screen. The one secure older zero (Borenshult 71.1 m) fails the screen (LR 2.21). | Under the inclusive reading, the Cambrian Stage 4 forms *are* E2, with stage support 514.5–506.5 Ma. M1 then becomes an occurrence and dating question, not an absence test. Only exposure older than 515.5 Ma tests M1's older interval directly; material in (514.5, 515.5] is older than Stage 4 but not older than M1. |
| **M3**, 431.2 Ma, E3 polysporangiate bodies | No: no held source has a searched-material denominator | Fossil-free prose (Edwards & Feehan 1980) is genuine negative evidence without an n. | The *C. barrandei* total-group reading (`f3-shape.md`) bears on the maximum's fossil basis. That is synthesis, not an absence test. |

**Sensitivity, reported separately from the primary findings.** Nonprimary variants are unqualified
sensitivity calculations, and some fail admission. Under the material variants the central older
contrast falls from 28 units to 26 (reference 51/59 to 49/57); no older cutting holds a trilete report
in any declared variant.

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

**Agreed (Codex 2758, amending my first draft):** the bounds are retained with the finite-grid
statement, and they are not described as having 95% coverage conditional on a claim.

**What the adopted target is.** Nominal 95% repeated-sampling coverage for each declared quantity,
conditional on passing the potential screen, with an abstention represented by the full, covering
set. Marginal treatment of abstentions was adopted as "unconditional coverage" in Codex message
2496; the real-design potential-screen conditioning was added later (`f3-shape.md`). The target
and the empirical qualification achieved below are distinct.

**What was achieved.** Empirical qualification on a finite simulation grid against the 0.93
coverage floor, with nominal 0.95 and calibration target 0.955 kept distinct (`f3-shape.md`). The
largest observed marginal miss proportion was 38/1,000. That is an observed proportion at sampled
truths, not a population upper confidence bound, and it does not demonstrate a population miss rate
≤ 0.05 even at those truths. Both collaborators recomputed the 14 acceptance replicate files
independently and agree: 529,550 non-abstaining quantity evaluations and 3,780 misses.

**Coverage given a claim is a separate property, and Loop 1 does not establish it.**

| Truth cell (MZ, ρ = 1) | Passing | Claims | Misses | Misses / claims |
|---|---:|---:|---:|---:|
| B3 (constant at H0 f*(459.1)), H0 intensity | 1,000 | 703 | 0 | 0 |
| B4 (reference level on (459.1, 462.6], zero on (τ0, 459.1], reference level younger than τ0), window f = 1 | 1,000 | 60 | 20 | 0.33 |
| All cells and designs, window f = 1 | 168,000 | 7,707 | 70 | 0.009 |
| All cells and designs, H0 intensity | 168,000 | 60,656 | 847 | 0.014 |

- **B4 sits at the edge of the real Murzuq window claim (462.6 Ma).** There 20 of 1,000 passing
  records miss (2%), within the marginal target, while 20 of the 60 claims miss (33%). Claims are
  rare at a boundary, so misses form a large share of them.
- **Pooled over the grid, misses among claims run 0–3.4% per quantity.** That figure depends on how
  the grid was weighted and is not reported as a property.
- **Conditional coverage is a legitimate frequentist target.** P_θ{θ ∉ C(X) | claim} has θ fixed and
  needs no prior; selective inference by conditional test inversion targets it (Fithian, Sun &
  Taylor 2014, arXiv:1410.2597). My draft wrongly said no frequentist procedure controls it.
- **My argument that it would force trivial sets was also wrong.** Reference and older units share
  Gamma well effects, so reference counts stay informative after conditioning on empty older units.
  Codex's counterexample: one unit of each, well effect u ~ Gamma(2, 2), reference rate 1, older
  relative intensity f, Laplace transform L(a) = (2/(2+a))². Then P(R ≥ 1 | O = 0) = 1 − L(f+1)/L(f),
  which is 0.5556 at f = 0 and 0.4375 at f = 1; I checked the arithmetic. This does not show that
  useful conditional bounds exist for the full design.
- **"How probable is it that this bound is wrong?"** is a posterior question. It needs a prior over
  encounter histories, and is a different analysis again.

**Joint decision: defer selected-result qualification** as a scope and value choice. It
is recorded as "not pursued; not established", not as impossible. No Bayesian layer and no new
compute in Loop 1.

**Reporting form for all bounds** (Codex's wording, adopted): give the bound, ρ and the design, then
"Nominal 95% compatibility bounds, qualified per declared quantity and design against a 0.93
coverage floor on a finite simulation grid, conditional on passing the potential screen. Abstentions
count as covering. The largest observed marginal miss proportion was 38/1,000. Population 95%
coverage, coverage conditional on a non-abstaining result, simultaneous coverage and validity beyond
the tested histories are not established." Where the central window is interpreted, give the B4
example (20/1,000 against 20/60) beside it.

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

### 4. Shared E2 dispersal-unit rule

**Replaced.** My first proposal treated a hilum or envelope as necessary for a cryptospore monad,
citing the programme's definition. That definition was itself narrower than its source. Edwards et
al. (2014, pp.51–52, held and re-read) adopt Richardson (1988), which keeps Richardson et al.'s (1984)
"single grains or monads" and adds hilate monads. Codex's independent source reviewer found this, and
I confirmed it on the held pages. My proposal also promoted ambiguous forms to detections under
inclusive and outlier, against the agreed reporting rule's "wider readings need explicit event-level
support, not automatic promotion" (`reporting-rule.md`, qualification 3).

**The rule is now a separate versioned addendum, `data/units/e2-unit-rule.md` (v1)**, drafted from
Codex's replacement (2760). `reporting-rule.md` is hash-bound in the 28 qualification receipts and is
untouched. The addendum records two axes separately:
- **morphology and producer evidence**, with distinct categories for permanent polyads, hilate,
  enveloped and alete monads, demonstrated dissociated-polyad products (cf. *L. chibrikovae*, Wellman
  et al. 2015, p.122) and indeterminate grains;
- **identity and embryophyte affinity under the named reading.** E2 is "cryptospores accepted as
  embryophytic", so a cryptospore label alone is not E2.

A form is detected when it passes both axes under that reading. A form whose identity or affinity
remains undecided within that reading is unresolved, not a zero. A wider reading detects it only by
accepting it explicitly; an explicit rejection yields no zero without the full-category reporting
and other conditions of the frozen rule. Morphology and dissociation evidence can overlap.

**Present effect: none on recorded outcomes.** Every current E2 detection among the 147 outcome rows
and the sprint-2 ledgers rests on a permanent polyad or, at Paraguay AS1-2835, the hilate *L.
divellomedia* (Wellman et al. 2015, Table 1). My review's "naked monad" for it was wrong, and the
supposed Paraguay–Qusaiba inconsistency does not exist. This was a source and outcome audit, not a
machine application of the rule, so it does not validate the rule for future monad-only samples.

**Corrected at source:** the definition on `taxa/ordovician-cryptospores.md` and pilot criterion C2
(`pilot-traits.md`) now state Richardson's definition in full. C2 stays an in situ trait, so its
scored forms are unchanged. Logged under Q5.

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
| 0 (proposal) | **Cryptospore-referenced M2 design.** Use co-recovered cryptospores to inform each unit's exposure, changing the estimand to trilete-producer output relative to cryptospore-producer output, compared with the Llandovery. This replaces the free ρ grid with a different, declared assumption, not an established weaker one, and it does not measure ρ. Common exposure cancels in a trilete/cryptospore ratio only under a declared joint sampling model; differential delivery and preservation, changing cryptospore production, denominator uncertainty and zeros remain. | Whether the M2 bounds can rest on an examinable assumption instead of a scenario grid. Overlapping sizes in the same Qusaiba assemblages (cryptospores 23–62 µm, triletes 24–44 µm; Wellman et al. 2015, Table 1) motivate examining equal transport; they do not establish it. The Hawaz's 20–44% cryptospores against 5–15% in the middle–upper Tanezzuft (Abuhmida 2013, pp.395–396 and 402–403) are compositional summaries, not per-sample exposure. | **Feasibility first:** does Abuhmida 2013 give per-sample cryptospore counts with their counting basis? The thesis distinguishes 200-particle palynofacies counts from palynomorph counts of all specimens on a first slide plus a scan of the second, with "cryptospore/spore" named as one assemblage group (p.35, checked); the extraction must keep those bases and the search effort, and must establish whether cryptospores and triletes were tallied separately. A design and qualification amendment would precede any result. |
| 1 | Independently constrained delivery and recovery ratios for M2 facies (Codex's item 1) | Which ρ scenarios deserve weight | Item 0 is one route to it. |
| 2 | A complete Cambrian sample roster with failed preparations and non-target recovery, specifically productive exposure older than 515.5 Ma (material in (514.5, 515.5] does not test M1 directly); tighter dating of the Stage 4 E2 forms | M1 admission, or M1 as an occurrence test under inclusive | Leads: Baldwin 2004 (Bright Angel); the Balang Stage 4 *Tetrahedraletes medinensis?* (Wang et al. 2022, Table 1). Likely needs specialist contact; Barry decides on sending. |
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
  - the qualification is finite-grid empirical confidence-set coverage against a 0.93 floor;
    coverage given a claim is not established and was deferred, not shown impossible;
  - a stage assignment is age support, not an occurrence date;
  - the programme's own cryptospore definition was narrower than its cited source, and the E2 rule
    first inherited the error; reading the source again, not consistency with our own documents,
    caught it.
- **Did evidence change a question?**
  - **Q1:** narrowed to "which delivery assumption, and which second frame?"
  - **Q2:** M1 under inclusive is now an occurrence-and-dating question.
  - **Q5 logs these corrections:**
    - the M2 note's original "P(false claim) ≤ 0.05" and "realistic early intensities" (corrected by
      Codex);
    - my "naked monad" and "no secure older zero" (corrected here);
    - the card and pilot cryptospore definition, which dropped Richardson's alete monads (corrected
      2026-11-01 after Codex's source check);
    - my coverage-draft claims that no frequentist procedure controls coverage given a claim and that
      conditioning forces trivial sets (corrected by Codex);
    - the Stage 4 point-age reading (corrected by Codex).
