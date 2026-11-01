# Loop 3: what the macrofossil record says, and a paper readers can follow

**Review A / adopted revision, 1 November 2026 (Codex).** Barry's authorised positive-record
analysis and narrative reconstruction proceed. The decisions in this box supersede the pilot
design below; that proposal remains as the record of what was reviewed. Sprint B is specified
in `loop3-design.md`. Its outcome and handoff are in `loop3-results.md`.

- Estimate the start of a **recoverable body-fossil process**, with a separate stated mapping to
  lineage origin. B2 supplies crown-member minima; neither B1 nor a body-recovery endpoint is
  automatically a crown date.
- Use an exact conditional positive-occurrence endpoint calculation under fixed recovery
  histories. The pilot's profiled logistic limits are superseded: stage duration was counted
  twice, and its preferred capacity lay on the grid boundary. Old code and outputs remain
  provenance, not the current paper results.
- Count locality–age proxies in the primary analysis; retain collection, locality and region–stage
  sensitivities. Restore distinct localities removed by country/genus/age matching and keep
  unresolved regional lists out of the primary count. A PBDB identifier is not proof of a bed.
- Report a conservative age-range envelope. Uniform-age and shared-quantile allocations are
  sensitivities, not 95% confidence intervals. Retain wide-age records in an explicit sensitivity.
- Treat PBDB collections per Myr as a conditional recovery proxy. Remove matches to the held
  plant-filtered collection list as an additional proxy; this does not establish non-plant-only
  search or independent effort. Geographic omissions change both records and proxy exposure.
- Compare B0 with the accepted spore minimum as a check on shared recovery/origin assumptions,
  not a known origin, empirical coverage calibration or transferable preservation lag. Report
  conditional estimates even where that comparison, simulated misspecification or clustering
  exposes failure. Do not turn conditional bounds into votes for a molecular-clock posterior.
- Keep the agreed division: Codex delivers review A and sprint B; Claude reconstructs the main
  paper and supplement; Codex reviews that reconstruction. No outside measurements, requests
  or automatic activation are assumed.

Proposed by Claude Opus 5.5, 1 November 2026, for critique by Codex (Board) before either agent treats
it as adopted. Barry's brief is quoted in `decisions.md` (2026-11-01, "Loop 3 brief"). It supersedes,
for body fossils, the 2026-10-28 rule in `plan-f3.md` that made E3–E5 synthesis only because "about
30 body-fossil records do not pass" the recovery-study criteria.

## The question this loop adds

Clock studies disagree about crown tracheophytes as much as about crown embryophytes (`primer.md`
§5.3): Morris et al. (2018) give 450.8–419.3 Ma across topologies, Harris et al. (2022) 452–447 Ma,
Hooper et al. (2026) 432–428 Ma under their 431.2 Ma soft maximum (M3). M3 is a fossil-absence
argument resting on *Cooksonia* in the Homerian. The question:

**Taking the dated positive record of early vascular-plant bodies at face value under stated recovery
assumptions, how far before the oldest fossil do the lineages probably extend, and which clock ages
does that make easy or hard to hold?**

This uses the positive occurrences, which the absence-rate approach could not, and it needs no
inventory of empty rocks. It replaces that inventory with an assumption about how recovery behaved
before the first find. The loop's job is to state that assumption, vary it, and show the answers.

## Challenges to the brief (for Barry and Codex)

1. **The assumption does not disappear; it changes form.** A range-extension interval assumes the
   occurrence rate just before the oldest find resembles the rate after it (or follows a declared
   function). The empty-rock inventory was how we would have checked that. Without it, the result
   is conditional by construction. That is acceptable if it is labelled so.
2. **For body fossils the likely bias has a direction.** Preservability evolved with the characters
   being dated: early polysporangiophytes were millimetre-scale, and the cuticle, lignified tissue
   and size that make bodies preservable were acquired along the way. Silurian non-marine rock is
   scarce. Both make recovery near the origin lower than later, so uniform-recovery intervals should
   be too young, not merely uncertain. The Loop 1 recovery study measured the size of this effect for
   classical intervals under ramps: coverage 4–81%, median bias 2–27 Myr young (`plan-f3.md`).
3. **The record itself supplies a known-answer check.** Accepted embryophyte cryptospores reach the
   Dapingian; embryophyte bodies first appear in the Sheinwoodian. Running the same estimators on
   "any embryophyte body fossil" therefore has a known minimum for the lineage. If the body-fossil
   interval falls far short of the spores, that measures how far "first recoverable form" can lag
   "lineage" in this system. It does not prove the same lag for tracheophytes; it shows the scale.
4. **The conditioning window dominates classical intervals.** The Early Devonian record is far
   denser than the Silurian. A uniform-recovery interval over a window ending in the Emsian will be
   tiny for that reason alone. Effort weighting and window sensitivity are required, not optional.
5. **Body fossils bear on M3 and crown tracheophytes, not on M1 or M2.** Embryophyte spores precede
   bodies by about 40 Myr, so the macrofossil record cannot test the crown-embryophyte maxima. The
   paper should say this plainly rather than imply a general test.
6. **Independence.** The oldest lycophyte-line and *Cooksonia* fossils are minimum calibrations in
   the clocks compared. Extending them tests an absence-based maximum, which is legitimate, but it
   does not validate a clock posterior.

## Design

### Fossil categories (characters, not taxa)

| Category | Definition | Event | Node it can bear on |
|---|---|---|---|
| B0 any embryophyte body | accepted land-plant macro- or mesofossil, sterile axes included | — | known-answer check against spores |
| B1 polysporangiophyte body | branched sporophyte with several sporangia, any lineage | E3 | total-group tracheophytes (upper bound on the crown only if the form was recoverable from the lineage's start) |
| B2 crown-tracheophyte member | lycophyte line or euphyllophyte | E5 and later | crown Tracheophyta directly |

Tracheids in situ (E4) are too few for an estimate; they stay in the synthesis. Each analysis declares
its reading (`main`, `inclusive`).

### Data

- **Unit:** a dated horizon (locality × bed); several taxa, specimens or papers from one horizon count
  once. Sensitivity: locality and region-stage cell as the unit, to expose clustered sampling.
- **Ages:** stage ranges from `data/timescale.csv`; finer ages kept beside them with their source.
- **Sources:** the curated tail (`data/occurrences/`) for the oldest records and their readings;
  vetted PBDB collections (`data/eprp/record/`) for the later sequence, whose density sets the rate;
  literature additions for regions PBDB under-covers. PBDB names are classified by a Codex job with
  cited sources and then audited (PBDB holds homonyms such as *Protophyllum*).
- **Geography:** every horizon carries its palaeogeographic unit, so the concentration of the
  Silurian record in Avalonia, Baltica and peri-Gondwanan Europe is shown, with a leave-one-region-out
  sensitivity.

### Estimators, from naive to conditional

| Label | Assumption | Implementation |
|---|---|---|
| A. Classical | horizons uniform over the range; window ends at a declared cut-off | Marshall (1990) / Strauss & Sadler (1989), `models/f3/estimators.py`; cut-offs Pridoli, Lochkovian, Pragian, Emsian |
| B. Effort-weighted | occurrence rate ∝ effort proxy × constant abundance from origin | `models/f3/ramp.py`, birth–death family at net rate 0 |
| C. Ramp | abundance rises after origin (logistic, capacity profiled; birth–death) | `ramp.py`, as in the recovery study |
| D. Age uncertainty | as A–C, with horizon ages drawn within their ranges | Monte Carlo over stage allocation |

Effort proxies: PBDB all-taxa land and marginal collections per stage (`data/occurrences/effort.csv`),
with Macrostrat non-marine units as an alternative. Neither is independent of collecting history;
both are stated as proxies.

Each result reports the older limit, whether it is bounded, the simulated coverage of that estimator
at this record count and effort history (from `models/f3/out/recovery_grid.csv` or a matched
re-run), and the clock ages it excludes or admits. A weak or unbounded result is reported as found.

### Figure for the paper

Dated horizons as age bars by category and region; beside each category, the older limits under
A–C; vertical bands for M3 and the crown-tracheophyte clock intervals; the spore first appearances
for B0.

## The paper

Rebuild, not edit. Main text for a quantitative palaeontologist who has not read the repository:

1. The disagreement among clocks and why fossil maxima carry it.
2. What a fossil maximum assumes, in plain terms.
3. What we tested: the three maxima, the spore absence test where it is possible (Murzuq), and the
   macrofossil positive-record analysis.
4. What we found, with the essential limitations in prose: one quantitative spore comparison, from
   one region; its dependence on recovery; what the macrofossil record allows under each assumption.
5. What follows for early land-plant evolution, keeping "first recoverable form" apart from "lineage
   origin".

The supplement holds the machinery: units and rules, qualification, derivations, sensitivity grids,
the QSIM calculation, source adjudications. The repository holds the audit trail. Internal labels
(M1–M3, E1–E5, frame codes, loop and sprint history) leave the main text.

## Sequence and ownership

| Step | Owner | Output |
|---|---|---|
| A. Plan, horizon dataset v0, pilot estimates | Claude (now) | this file; `data/macro/`; `models/f3/loop3/` |
| Review A and sprint B | Codex | critique; independent re-derivation of a stratified sample of horizons; matched simulation coverage; age and unit sensitivity; final macrofossil figure |
| Sprint C | Claude | reconstructed main text and supplement |
| Review C | Codex | critique of the paper against the evidence |
| Close | Claude | adjudication, final render; Barry decides release |

Agreement between the two agents is not independent validation; disagreements stay visible. No step
depends on outside correspondence.
