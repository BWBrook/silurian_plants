# M2 on real designs: what the Libyan, Saudi and Baltic records say about 459.1 Ma

Claude Opus 5.5 (`claude-opus-5-5`), 31 October 2026. Sprint 1 of `docs/sprints-2026-11.md` (v2,
Codex's revision, accepted by starting against it). Questions Q1, Q2 and Q5. Code and outputs:
`models/f3/designs/m2.toml` (frozen declarations and dated amendments), `designs.py` (adapter), `m2.py`
(screen and read-outs), `qualify.py` (conditional qualification); `models/f3/out/m2_units.csv`,
`m2_screen.csv`, `m2_results.csv`, `out/qual/` (receipts and replicate tables).

Counter-reviewed and updated by Codex, 31 October 2026. The current qualification
and interpretation below incorporate both sprint counter-reviews; original
source and implementation attribution is retained above.

## Result

The first qualified empirical F3 statements exist, from the Murzuq Basin (Abuhmida 2013). They are about
trilete-spore (E1) encounter in drill cuttings, relative to the Tanezzuft cuttings of the same wells, primarily Cr4
(Rhuddanian–Telychian) with some Cr3 material, under a declared transport ratio ρ (older-cutting detection rate over
reference-cutting rate at equal intensity).

- **After the M2 maximum the record is already nearly empty.** In the multi-well cuttings design
  (LY-MZ-CU: 51 of 59 reference cuttings marked, 28 empty Late Ordovician and Darriwilian cuttings),
  the exposure/reference-rate-weighted mean encounter across sampled ranges within
  443.1–459.1 Ma has an upper read-out of about 0.18 of the Llandovery level at ρ = 1 (H0, any path up
  to the reference level), below 0.26 at ρ = 0.5, 0.42 at 0.25 and 0.92 at 0.1.
- **Before the maximum the constraint is the same size.** The window read-out (trilete encounter at
  least f before 459.1 Ma, anything afterwards) excludes reference-level encounter (f = 1) sustained
  further back than 462.6 Ma at ρ = 1, 464.1 at 0.5 and 467.1 at 0.25; at ρ = 0.1 nothing is excluded.
  Inverted at the Darriwilian base, the largest constant pre-459.1 encounter compatible with the
  record is 0.17 of the Llandovery level at ρ = 1 (0.35 at 0.5, 0.69 at 0.25; derived, see below). At
  f = 0.1 and 0.01 no pre-459.1 origin is excluded by any design.
- **What follows for M2.** Hooper et al.'s maximum rests on the absence of older trilete spores.
  Against reference-level trilete production the absence does tell, before 459.1 Ma as well as after.
  But the same cuttings bound encounter after 459.1 Ma, where the clock places crown embryophytes, as
  tightly as before it. An origin shortly before 459.1 Ma with encounter at the levels the Late
  Ordovician actually shows (below about a fifth of the Llandovery's at ρ = 1) leaves the same empty
  record as an origin after it. **The absence remains compatible with some low-encounter histories on either
  side of 459.1 Ma.** The post-maximum mean and pre-maximum window are different targets;
  these bounds do not demonstrate indistinguishability at every allowed intensity. The
  sources do not independently establish which early intensities are biologically realistic.
  No probability that the clock maximum is true follows from these calculations.

All fourteen primary design/transport pairs submitted to qualification pass the
counter-review grid, with zero critical-value shift and no stage 2. The largest
observed per-cell/quantity false-delivered-claim frequency is 0.038 among
screen-passing simulations. This is acceptance against a 0.93 floor on the
finite declared grid, not a universal 5% error guarantee. In the new MZ/rho=1
window-boundary test, 20 of 1,000 passing simulations exclude truth, but those
errors occur among only 60 non-abstaining results. The qualification therefore
must not be presented as 95% coverage conditional on obtaining a claim.
Codex's source and numerical reconstructions, contract repairs and rerun are
recorded in `2026-10-31-sprint1-codex-review.md`.

## Designs and their admission

Declared before any engine statistic (commit `d426423`); every variant is reported in
`out/m2_screen.csv` (512 variants: design × material/allocation/reading options × cluster k × ρ ×
reference minimum 5 or 10). Primary variants:

| Design | Units (reference marked/total; older) | Screen at ρ = 1, 0.5, 0.25, 0.1 | Status |
|---|---|---|---|
| LY-H2-CU, H2 within well, cuttings | 7/8; 9 (2 Bir Tlacsin, 7 Hawaz) | pass, pass, pass, fail | qualified at 1, 0.5, 0.25 |
| LY-D1-CU, D1 within well, cuttings | 13/16; 9 (6 Melez Shugran, 3 Hawaz) | pass, pass, pass, fail | qualified at 1, 0.5, 0.25 |
| LY-I3-CU, I3 within well, cuttings | 16/20; 10 (3 Bir Tlacsin, 7 Melez Shugran) | pass, pass, pass, fail | qualified at 1, 0.5, 0.25 |
| LY-MZ-CU, five wells, cuttings, k = 2 | 51/59; 28 | pass at every ρ | qualified at all four |
| LY-XW-CO, cores across wells, k = 2 | 1/5 (E1-NC174 7287 ft prose specimen); 46 | fail at every ρ | inadmissible: one reference detection |
| LY-H2-CUCO, H2 cuttings and cores, cores at the cutting rate × ρ | 7/8; 19 | pass | screen only (no core/cutting ratio is supported by a source) |
| QB-CO, Qusaiba-1 reference, Borenshult-1 older, k = 2 | 22/38; 26 | pass, fail, fail, fail | qualified at 1 |
| BOR, Borenshult alone | historical screen (2026-10-31) | not recomputed | no in-frame reference under main |

Under the 7287 ft "unresolved" reading the core design has no reference detection at all. Ages come from
the thesis abstract (printed pp. iv–v): Cr4 Tanezzuft late Rhuddanian–Telychian, Cr3 early–mid
Rhuddanian, Bir Tlacsin late Hirnantian, Melez Shugran and pre-glacial Memouniat early late
Katian–early Hirnantian, Hawaz mid–late Darriwilian. The primary Murzuq reference comprises 56 Cr4-only rows, two Cr3/Cr4-boundary
rows and one Cr3-only row (I3 4640 ft). The chart-priority interpretation retains
the recorded conflict with the prose's single-Cr3-specimen claim. Every Libyan
first appearance falls in the Rhuddanian, so τ = 443.1 Ma (Qusaiba: Katian, τ = 452.8).

**Reporting scope (source check).** The green chart group is headed "Cryptospores/Spores"; its only
trilete column is *Ambitisporites dilutus*, and the thesis systematics (printed pp. 327–328) describe
it as the only true trilete, distinguished from *Imperfectotriletes* (a simple split, an E2 cryptospore
here). A blank target cell in a chart row is therefore a full-category E1 report (reporting rule 3).
Eligibility is per-sample non-target recovery from the chart (rule 4). Rows in barren scopes and the
I3 Ash Shabiyat rows whose recovery the thesis calls possibly caved (printed p. 367) are excluded.

**The other five frames.** Hanadir (TAYM-4) has a figure inventory but no certified processed inventory
or in-frame reference; Paraguay's eight pilot depths were chosen through outcomes and its 53-sample log
is missing; Samphire's original report was unverified at the sprint-1 freeze (verified in sprint 2); Pelmis needs its 140-sample collection mapped to the
27 tabulated samples. None supplies an M2 design this sprint. Borenshult enters only as QB's older
units; Qusaiba only as QB's reference.

## Qualification after counter-review

The full rerun uses the same potential screen, fitted reference-rate nuisance
settings, transport ratios, cluster shapes and depth-ordered ages as the
original design. The declaration has twelve acceptance cells and three
calibration diagnostics. Original Q1–Q8 and B1/B2 are retained. B3 directly
tests the H0 f*(459.1) boundary. B4 tests reference-level encounter on
(459.1,462.6] Ma, zero encounter between tau0 and 459.1, and reference encounter
younger than tau0; this is an H0/H1 window test, not H0m. Fresh roots
20261111/20261112/20261113 separate calibration, acceptance and optional stage 2.
The amendments were declared with the older results known, before the rerun.

Each binding cell requires 1,000 screen-passing records, with a 20,000-attempt
cap. Calibration targets 0.955; independent acceptance assesses a 0.93 floor
for the nominal-95% procedure. All fourteen combinations passed stage 1 with
shift zero. The evidence loader reconstructs the counts, calibrated shift and
verdict, verifies the exact phase chain, binds consumed inputs/code/declarations
and retains every attempt. QB qualifies H0m/H0/H1 only; its H0c is an unqualified
class diagnostic. Other variants do not inherit primary qualification.

The criterion is the false-delivered-claim frequency among screen-passing
records, counting abstentions as non-errors. Across acceptance there are
529,550 quantity evaluations labelled as claims, with 3,780 misses. These are
correlated quantity evaluations, not independent experiments. `claims_*` means
non-abstaining under the implemented rule and does not itself guarantee an
informative finite exclusion; I3's unbounded windows illustrate that distinction.
Neither the 0.93 tolerance nor the observed worst frequency 0.038 establishes
a universal 5% error bound, simultaneous coverage across curves/designs, or
coverage conditional on an informative result.

The table shows the worst marginal coverage across each pair's acceptance
cells/quantities, plus the two new boundary checks. Misses/non-abstentions are
separate from their common denominator of 1,000 screen-passing records.

| Design | ρ | Worst 1 − false-claim rate | B3 H0 misses/non-abstentions | B4 window f=1 misses/non-abstentions |
|---|---:|---:|---:|---:|
| LY-H2-CU | 1 | 0.972 | 5/588 | 0/113 |
| LY-H2-CU | 0.5 | 0.962 | 32/682 | 0/194 |
| LY-H2-CU | 0.25 | 0.973 | 0/779 | 0/378 |
| LY-D1-CU | 1 | 0.985 | 1/874 | 0/397 |
| LY-D1-CU | 0.5 | 0.980 | 13/889 | 0/556 |
| LY-D1-CU | 0.25 | 0.965 | 15/917 | 0/687 |
| LY-I3-CU | 1 | 0.978 | 1/27 | 0/1000 |
| LY-I3-CU | 0.5 | 0.978 | 3/55 | 0/1000 |
| LY-I3-CU | 0.25 | 0.963 | 19/94 | 0/1000 |
| LY-MZ-CU | 1 | 0.980 | 0/703 | 20/60 |
| LY-MZ-CU | 0.5 | 0.982 | 2/827 | 7/107 |
| LY-MZ-CU | 0.25 | 0.985 | 4/843 | 0/247 |
| LY-MZ-CU | 0.1 | 0.982 | 12/839 | 0/466 |
| QB-CO | 1 | 0.985 | 14/916 | 0/670 |

MZ/rho=1's B3 H0 bound misses in 0/703 non-abstentions. Its B4 window misses in
20/60 (33.3%), versus 20/1,000 (2%) of passing records. This is a material limit
of the adopted selection/acceptance criterion, retained prominently rather than
hidden by the overall pass. It does not invalidate the arithmetic or authorise
a confidence statement for the selected subset.

Diagnostic X1 (true transport half that assumed) has worst marginal coverage
0.895, so a misspecified transport ratio matters. X2 (true between-well shape
0.8) and X3 (a count-based lower-rate scenario) have minima 0.975 and 0.983.
X3 uses a binomial Clopper–Pearson calculation and u=1 transformation; with
clustered reference data it is not a calibrated confidence limit for the
Gamma-mixture rate. Diagnostics are not included in binding acceptance.

The original `0780402` evidence is historical and remains recoverable from Git;
its independently reconstructed totals are in the counter-review audit. Current
code binding, runtime, cross-host checks and final run timings are recorded there.

## Results by design (primary variants, qualified shift 0)

f\* is the largest exposure/reference-rate-weighted mean encounter over (τ, T],
relative to the reference cuttings, not rejected by the nominal-95% rule. It is
not a calendar-time mean: unsampled intervals carry no weight.

| Design | ρ | H0c, all exposure | H0 to 459.1 | H0 to 469.4 | H1 to 469.4 | Origins excluded beyond (H0; f = 1 / 0.1) | Window (f = 1) |
|---|---|---|---|---|---|---|---|
| LY-MZ-CU | 1 | 0.058 | 0.18 | 0.12 | 0.31 | 444.1 / 452.6 | 462.6 |
| | 0.5 | 0.12 | 0.26 | 0.17 | 0.33 | 444.6 / none | 464.1 |
| | 0.25 | 0.23 | 0.42 | 0.28 | 0.42 | 445.1 / none | 467.1 |
| | 0.1 | 0.58 | 0.92 | 0.62 | 0.74 | 452.6 / none | none |
| LY-H2-CU | 1 | 0.21 | 0.91 | 0.34 | 0.85 | 445.6 / none | 464.1 |
| | 0.5 | 0.43 | 1 | 0.50 | 0.90 | 462.1 / none | 466.1 |
| | 0.25 | 0.85 | 1 | 0.87 | 1.17 | 467.6 / none | none |
| LY-D1-CU | 1 | 0.23 | 0.49 | 0.36 | 0.86 | 448.1 / none | 468.6 |
| | 0.5 | 0.46 | 0.74 | 0.54 | 0.93 | 450.6 / none | none |
| | 0.25 | 0.92 | 1 | 0.93 | 1.25 | 467.1 / none | none |
| LY-I3-CU | 1 | 0.21 | 0.33 | 0.33 | 0.78 | 444.6 / none | none (no Darriwilian) |
| | 0.5 | 0.42 | 0.50 | 0.50 | 0.86 | 445.6 / none | none |
| | 0.25 | 0.83 | 0.86 | 0.86 | 1.15 | 451.1 / none | none |
| QB-CO | 1 | 0.61 (unqualified diagnostic) | 0.69 | 0.62 | 0.72 | 456.8 / none | none |

H0m lies at most 0.05 below H0 in any variant (by construction it is never above). Origin sets at f = 0.01 are unbounded
everywhere. Inverting the window test in f (derived: the qualification covers f = 1, 0.1 and 0.01 only),
the largest constant pre-459.1 encounter over the whole Darriwilian is 0.17 / 0.35 / 0.69 (MZ, ρ = 1 /
0.5 / 0.25; 0.16 / 0.31 / 0.63 with the Hawaz placed wholly before 459.1), 0.30 / 0.61 for H2 (ρ = 1 /
0.5) and 0.79 for D1 (ρ = 1).

**Sensitivity across the declared variants (`m2_results.csv`; not independently qualified).** For MZ at ρ = 1, allocation (whole
Darriwilian or [459.1, 469.4] Ma), material type (chart code or appendix only), cluster k (2 or ∞) move
f\*_H0(459.1) within 0.175–0.191, the window endpoint within 462.6–463.6 Ma and the f = 0.1 origin
endpoint within 451.6–452.6 Ma. The within-well designs move by up to 0.12 in f\*.

## Pivotal readings

- **The reference minimum decides H2.** H2 has eight reference cuttings. Under the synthetic study's
  minimum of ten it is inadmissible; under the declared five it qualifies. The other designs pass
  under both.
- **The two unspecified material types decide H2 and D1 at ρ = 0.25.** With the chart's CU code, H2
  4950/4990 ft and D1 4050/4200 ft count as cuttings and both designs pass; excluded, both fail S1
  (5.57 and 5.90 against 5.99).
- **The 7287 ft core report decides whether a core design exists**, and even accepted it gives one
  reference detection in five cores: inadmissible at every ρ. The prose–chart conflict stays recorded
  under Q2; it does not affect the cuttings designs.
- **The declared between-core variance decides QB.** With k = 2 for two cores in different regions,
  QB passes only at ρ = 1 (main) or 0.5 (other variants). With no well effect (k = ∞) it passes down
  to ρ = 0.25 and gives f\* as low as 0.11. One core per region cannot estimate that variance. QB main/zero converts
  seven disputed Sandbian reports to zeros and is retained only as an inadmissible
  coding diagnostic; it does not contribute scientific sensitivity evidence.
- **The transport ratio ρ decides everything quantitative.** No source measures it. The thesis does
  show that land-derived spores reached and survived in the older samples: cryptospores are 20–44% of
  upper Hawaz assemblages (printed pp. 395–396) against 5–15% in the middle–upper Tanezzuft (pp.
  402–403), and each of the ten primary Hawaz cutting rows carries 6–10 marks in the chart's "Cryptospores/Spores"
  group. This establishes a preservation and delivery route for cryptospores. It does not
  identify, or place a quantitative lower bound on, trilete delivery/recovery per unit
  producer output; the relative producer outputs remain unknown.

## The three layers

1. **Encounter intensity (what is qualified).** The numbers above: E1 encounter in Murzuq cuttings,
   relative to the declared Tanezzuft reference cuttings, given ρ.
2. **Biological translation (conditional).** Encounter is spore output times transport into these
   shelf settings times recovery. Equal ρ means equal delivery and recovery per unit producer output;
   the Hawaz cryptospore evidence bears on delivery, not on how trilete producers' share of the land
   flora changed. The Katian Saudi triletes (Qusaiba, main reading) show producers existed in the Late
   Ordovician of Gondwana while the Libyan Katian–Hirnantian shelf recorded none: low encounter, not
   absence, is the empirical regime.
3. **Fossil-to-node (Hooper's mapping).** If the crown ancestor made trilete monads, the crown can be
   no older than the first trilete producers, and the producers' encounter before 459.1 Ma is bounded
   as above. A crown origin before 459.1 Ma is excluded only for producers at or near the Llandovery
   level; some low-encounter histories allowed after 459.1 Ma also remain compatible before it.
   This is not equivalence of all histories below the post-maximum mean bound. Node-retention
   scenarios (`models/pilot-asr/`) sit beside this and are not multiplied in.

## Limits

- The primary Murzuq design has no sampled age support in the Sandbian interval
  (452.8,458.2] Ma. An H0 history at the reference level throughout that gap and
  zero in the sampled older ranges has calendar-time mean 0.3375 over
  443.1–459.1 Ma, but exposure-weighted mean zero and the same older-data
  likelihood as complete absence. The approximately 0.18 bound therefore does
  not bound a calendar-time mean or exclude an unsampled pulse.
- ρ is a scenario grid, not an estimate. A misspecified ρ undercovers (diagnostic X1).
- One basin and one thesis. The reference and the older cuttings share an author, a laboratory and a
  chart system; this helps comparability but makes the frame a single-study frame (Q5 notes the
  internal conflicts it carries: 7287 ft, the Cr3 uniqueness claim against the I3 marks, sample-count
  wording).
- The Hawaz is placed at stage resolution (whole Darriwilian, or wholly before 459.1 Ma); the thesis
  says "mid–late Darriwilian", which neither captures exactly. Between the two declared allocations
  (with material type) the window endpoints move by at most 2 Myr.
- Caving: positive cuttings may hold caved material. τ is set from the age range of the material in which a spore is recovered;
  this is a reporting rule, not an indigenous first-appearance date. A younger caved
  fossil recovered from an older bed can move inferred τ older. No target mark occurs
  in the admitted older Libyan cuttings, but reference contamination could inflate
  the fitted rate. A smaller ρ illustrates some rate distortion; it does not qualify
  an additive, depth-dependent contamination process.
- Ages within a range are independent in the estimator and depth-ordered in the simulation; sorting exchangeable equal-range, equal-rate older units within a common
  cluster leaves their all-zero likelihood unchanged. This argument does not apply
  to arbitrary unequal multipliers, age ranges or mixed outcomes. The qualification
  is limited to its declared ordered-age scenarios, not every joint chronology.

## Repairs and amendments

- **Adapter bug, fixed before any statistic.** `designs.py` reversed the Katian–Hirnantian range; the
  first screen stopped on it. The declaration was right. Fixed with a test.
- **Amendment 1 (declared in `m2.toml`).** The frozen screen, computed on full outcomes, can only pass
  when the oldest older stage is empty, because a detection there moves τ past every older unit.
  Conditioning coverage on it would condition away the outcomes the bound uses: for H2 with true
  f = 0.3 about 1–2% of replicates would pass, all with an empty Hawaz, and coverage among them would be
  unattainable for any estimator. The screen is now evaluated with older outcomes set to 0, the frame's
  potential. Real-data verdicts change only for QB under inclusive; diagnostic X3 was added. This also
  corrects the rule adopted in `f3-shape.md` ("Frame screen and frame selection"), which did not
  anticipate it.
- **Amendment 2 (after the independent review, before the final run).** The criterion is stated as
  the false-claim rate, boundary cells are added so acceptance has power, claims and misses are
  reported per quantity, and a first appearance lost after the screen is an abstention, not an error.
  The window start, report ages and declaration file are read from the TOML so sprint 2 can reuse the
  code unchanged.

## Independent checks

- **Source-to-outcome (Codex, `gpt-6.1-terra`, high).** From the CSV tables and the written rule
  alone, without the adapter or its output, six jobs re-derived inclusion, material, outcome, stage
  range and older/reference role for all 164 appendix entries. Agreement: 164 of 164.
- **Engine and qualifier review (Claude Sonnet 5.5 subagent, code only, own numerical checks).**
  - Sound: multipliers everywhere a rate enters (analytic and finite-difference gradients agree to
    9e-9 with k = 2, mixed multipliers and numerical ranges); numerical ranges keep whole pieces under
    the lag and window cuts; the window read-out is never stronger than the origin test, and the engine
    matches an independent profile to four decimals; the screen and specification in the simulator
    match the data path; seeding does not depend on worker count.
  - Defect, repaired by amendment 2: the first grid's coverage was nearly all abstentions (H2, Q2:
    2,961 of 2,997), so acceptance could not detect miscalibration.
  - Latent defect, repaired: a lost first appearance in the analysis would have scored as an error.

## Structural review

The structure served the investigation: frozen declarations, an adapter with a source link per row,
one screen function shared by data and simulation, and receipts that pin code hashes made it possible
to run 512 variants and 14 qualifications in an afternoon and still say which choice moves which
number. The exposed assumption was the screen's interaction with the first-appearance rule, now
amended. Evidence changed Q1 (a first empirical answer, and its limit) and Q2 (the decisive record is
the Late Ordovician shelf, not the Darriwilian).

Source: Abuhmida F (2013). *Palynological analysis of the Ordovician to Lower Silurian sediments from
the Murzuq Basin, southwest Libya*. PhD thesis, University of Sheffield. Held complete thesis; no DOI.
