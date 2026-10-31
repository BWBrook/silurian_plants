# M2 on real designs: what the Libyan, Saudi and Baltic records say about 459.1 Ma

Claude Opus 5.5 (`claude-opus-5-5`), 31 October 2026. Sprint 1 of `docs/sprints-2026-11.md` (v2,
Codex's revision, accepted by starting against it). Questions Q1, Q2 and Q5. Code and outputs:
`models/f3/designs/m2.toml` (frozen declarations and amendment 1), `designs.py` (adapter), `m2.py`
(screen and read-outs), `qualify.py` (conditional qualification); `models/f3/out/m2_units.csv`,
`m2_screen.csv`, `m2_results.csv`, `out/qual/` (receipts and replicate tables).

## Result

The first qualified empirical F3 statements exist, from the Murzuq Basin (Abuhmida 2013). They are about
trilete-spore (E1) encounter in drill cuttings, relative to the Rhuddanian–Telychian (Cr4) Tanezzuft
cuttings of the same wells, under a declared transport ratio ρ (older-cutting detection rate over
reference-cutting rate at equal intensity).

- **After the M2 maximum the record is already nearly empty.** In the multi-well cuttings design
  (LY-MZ-CU: 51 of 59 reference cuttings marked, 28 empty Late Ordovician and Darriwilian cuttings),
  mean encounter over 443.1–459.1 Ma is below 0.18 of the Llandovery level at ρ = 1 (H0, any path up
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
  record as an origin after it. **The absence cannot distinguish a crown origin before 459.1 Ma from
  one after it at any intensity the later Ordovician record allows.** The soft maximum is not
  contradicted; its absence premise is uninformative at realistic early intensities.

All primary results qualify in the sense the procedure can support: among replicates that pass the
screen, the probability of reporting a bound, origin set or window read-out that the truth violates
stays below 0.037 in every cell (nominal 0.05, floor 0.07), with no critical-value shift, at stage 1
for every design and ρ. Codex independently re-derived all 164 Libyan binary units from the source
tables with no disagreement. An independent review showed that the first acceptance grid was mostly
abstentions; the grid was amended and rerun (amendment 2, below).

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
Katian–early Hirnantian, Hawaz mid–late Darriwilian. Every first appearance falls in the Rhuddanian, so
τ = 443.1 Ma (Qusaiba: Katian, τ = 452.8).

**Reporting scope (source check).** The green chart group is headed "Cryptospores/Spores"; its only
trilete column is *Ambitisporites dilutus*, and the thesis systematics (printed pp. 327–328) describe
it as the only true trilete, distinguished from *Imperfectotriletes* (a simple split, an E2 cryptospore
here). A blank target cell in a chart row is therefore a full-category E1 report (reporting rule 3).
Eligibility is per-sample non-target recovery from the chart (rule 4). Rows in barren scopes and the
I3 Ash Shabiyat rows whose recovery the thesis calls possibly caved (printed p. 367) are excluded.

**The other five frames.** Hanadir (TAYM-4) has a figure inventory but no certified processed inventory
or in-frame reference; Paraguay's eight pilot depths were chosen through outcomes and its 53-sample log
is missing; Samphire's original report is unread; Pelmis needs its 140-sample collection mapped to the
27 tabulated samples. None supplies an M2 design this sprint. Borenshult enters only as QB's older
units; Qusaiba only as QB's reference.

## Qualification

Conditional on the amended screen, at the actual designs (`qualify.py`, commit `0780402`). Truth: the data's fitted
reference rate, the declared ρ and cluster k, depth-ordered true ages within each well and formation,
τ0 = the data's τ; eight acceptance cells (constant f = 1, 0.3, 0.1 from 470 Ma; f = 1 from 459.1 Ma;
the least favourable H0 and H1 paths; a ramp; reference level after 459.1 with 0.1 before), two
boundary cells at the design's own reported f\* (B1: f\*_H0c with all exposure; B2: f\*_H0 to 469.4),
and three diagnostics. Quantities: f\*_K(t0) for each class containing the truth, origin-set coverage of t0 at
each applicable f_min (H0c, H0m, H0), and window coverage (H0, start 459.1). The calibration and
acceptance seeds are independent (20261101, 20261102).

**What the qualification certifies (amendment 2).** When the truth has appreciable older intensity,
older cuttings detect, τ moves past them and the analysis makes no claim; an abstention covers. A
claim is made only when the older units are empty, so coverage *given that a claim is made* is not a
property any procedure here can have: at the boundary truths a large share of the few claims are
wrong (I3 at ρ = 1, B2: 15 of 22). The certified property is the ordinary one of a 95% procedure:
P(a false claim) ≤ 0.05 per screen-passing record. Every cell reports its claims and the misses among
them (receipts, `claims_*`, `claimmiss_*`); across the grid, 3,193 of 414,831 claims missed.

| Design, ρ | Shift | Acceptance (stage 1) | Worst 1 − false-claim rate | Boundary-cell claims (B1 / B2, of 1,000) |
|---|---|---|---|---|
| LY-H2-CU 1 / 0.5 / 0.25 | 0 | pass ×3 | 0.975 / 0.972 / 0.971 | 38/5, 42/25, 38/35 |
| LY-D1-CU 1 / 0.5 / 0.25 | 0 | pass ×3 | 0.988 / 0.981 / 0.974 | 328/146, 309/236, 328/311 |
| LY-I3-CU 1 / 0.5 / 0.25 | 0 | pass ×3 | 0.983 / 0.975 / 0.963 | 86/22, 84/79, 96/96 |
| LY-MZ-CU 1 / 0.5 / 0.25 / 0.1 | 0 | pass ×4 | 0.984 / 0.984 / 0.984 / 0.979 | 260/101, 241/160, 238/220, 237/226 |
| QB-CO 1 | 0 | pass | 0.985 | 366/363 |

Diagnostics (calibration batch): halving the true transport ratio (X1) drops coverage to 0.89–0.97 at
ρ ≥ 0.5, so ρ is the assumption that matters and every result is reported across its grid. A true
between-well shape of 0.8 (X2) and a reference rate at its lower 95% limit (X3) keep coverage at
0.974 or above, although X3 passes the screen only 5% of the time for H2 and D1 at ρ = 0.25. Each full
grid ran in about 7 minutes on Nectar `c3.3xlarge` (numpy 2.3.4, scipy 1.16.3); the receipts hold the
code hashes of commit `0780402`. The first run (`e1cd198`, before amendment 2) gave the same verdicts
and the same read-outs.

## Results by design (primary variants, qualified shift 0)

f\* is the largest mean encounter over (τ, T], relative to the reference cuttings, not rejected at 95%.

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
| QB-CO | 1 | 0.61 | 0.69 | 0.62 | 0.72 | 456.8 / none | none |

H0m lies at most 0.05 below H0 in any variant (by construction it is never above). Origin sets at f = 0.01 are unbounded
everywhere. Inverting the window test in f (derived: the qualification covers f = 1, 0.1 and 0.01 only),
the largest constant pre-459.1 encounter over the whole Darriwilian is 0.17 / 0.35 / 0.69 (MZ, ρ = 1 /
0.5 / 0.25; 0.16 / 0.31 / 0.63 with the Hawaz placed wholly before 459.1), 0.30 / 0.61 for H2 (ρ = 1 /
0.5) and 0.79 for D1 (ρ = 1).

**Sensitivity across the declared variants (`m2_results.csv`).** For MZ at ρ = 1, allocation (whole
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
  to ρ = 0.25 and gives f\* as low as 0.11. One core per region cannot estimate that variance.
- **The transport ratio ρ decides everything quantitative.** No source measures it. The thesis does
  show that land-derived spores reached and survived in the older samples: cryptospores are 20–44% of
  upper Hawaz assemblages (printed pp. 395–396) against 5–15% in the middle–upper Tanezzuft (pp.
  402–403), and every eligible Hawaz chart row carries 6–10 marks in the chart's "Cryptospores/Spores"
  group. That argues against small ρ
  for the Hawaz, not for any particular value.

## The three layers

1. **Encounter intensity (what is qualified).** The numbers above: E1 encounter in Murzuq cuttings,
   relative to Cr4 Tanezzuft cuttings, given ρ.
2. **Biological translation (conditional).** Encounter is spore output times transport into these
   shelf settings times recovery. Equal ρ means equal delivery and recovery per unit producer output;
   the Hawaz cryptospore evidence bears on delivery, not on how trilete producers' share of the land
   flora changed. The Katian Saudi triletes (Qusaiba, main reading) show producers existed in the Late
   Ordovician of Gondwana while the Libyan Katian–Hirnantian shelf recorded none: low encounter, not
   absence, is the empirical regime.
3. **Fossil-to-node (Hooper's mapping).** If the crown ancestor made trilete monads, the crown can be
   no older than the first trilete producers, and the producers' encounter before 459.1 Ma is bounded
   as above. A crown origin before 459.1 Ma is excluded only for producers at or near the Llandovery
   level; at the levels the post-459.1 record allows, the absence has nothing to say. Node-retention
   scenarios (`models/pilot-asr/`) sit beside this and are not multiplied in.

## Limits

- ρ is a scenario grid, not an estimate. A misspecified ρ undercovers (diagnostic X1).
- One basin and one thesis. The reference and the older cuttings share an author, a laboratory and a
  chart system; this helps comparability but makes the frame a single-study frame (Q5 notes the
  internal conflicts it carries: 7287 ft, the Cr3 uniqueness claim against the I3 marks, sample-count
  wording).
- The Hawaz is placed at stage resolution (whole Darriwilian, or wholly before 459.1 Ma); the thesis
  says "mid–late Darriwilian", which neither captures exactly. Between the two declared allocations
  (with material type) the window endpoints move by at most 2 Myr.
- Caving: positive cuttings may hold caved material. τ is set at the oldest stage any detected cutting
  can occupy, so caving from younger beds cannot move it older; caving into the older cuttings would add
  false positives, of which there are none. Caving that inflates the reference rate relative to
  indigenous encounter acts like a smaller ρ.
- Ages within a range are independent in the estimator and depth-ordered in the simulation; for one
  class of all-empty older units the two give the same likelihood (exchangeability), and coverage held
  with ordered truth.

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
