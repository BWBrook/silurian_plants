# Persistence of trilete production: re-running Hooper et al.'s stochastic mapping

Pre-declared by Claude Opus 5.5 on 30 October 2026, before any run. Authorised by Barry (Claude chat,
2026-10-30): "widened scope is fine, proceed with the new ancestral-state analysis as/when
appropriate." Part of the trait pilot (`docs/pilot-traits.md`, link 2, persistence).

## Question

P1, M2's mapping, needs more than a trilete ancestor. Had crown Embryophyta existed before a
candidate time *T*, at least one lineage must have kept producing trilete spores from the node
through the sampled interval. Hooper et al.'s deposit saves only node summaries, not mapped
histories (Codex, `data/pilot/hooper2026-asr/scm_workspace_audit.json`). This analysis regenerates
the histories under their own data, trees and settings, and reads off persistence.

## Inputs (read-only)

- `data/external/deposits/hooper2026-spore-evolution/02. Ancestral State Estimation.zip`:
  `asr_matrix.csv`; `extant.tre`, `eophyte sister.tre` and `zygnema sister.tre`; `ASE code chunk.R`.
  Its hash is checked against Codex's `data/pilot/hooper2026-asr/source_inventory.csv`.
- Characters: `X21`, the aperture (0 not present, 1 hilate, 2 proximal monolete, 3 proximal
  trilete, 4 lateral or distal), and `X26`, the dispersal unit. X21 is primary.
- Crown nodes as in Codex's `nodes.csv`: the MRCA of the extant land-plant tips and the MRCA of the
  extant vascular-plant tips.

## Methods

**A. Reproduction**, Hooper et al.'s settings, from their `ASE code chunk.R`:
- `phytools::make.simmap(tree, x, model = "ER", nsim = 1000, Q = "mcmc", vQ = 0.01, prior = list(use.empirical = TRUE), samplefreq = 10)`;
- `phytools::fitMk(model = "ER")` and `fitMk(model = "ARD")`, with `pi = "fitzjohn"`, and their
  marginal reconstructions;
- per tree and character, with fixed seeds.

**B. Persistence on the maps.** For X21, in each of the 1,000 maps per tree:
- whether the whole path from the crown-Embryophyta node to the crown-Tracheophyta node is in
  state 3 (proximal trilete) throughout;
- the number of departures from state 3 on that path, and of returns to it.

The same is read for the paths from the crown-Embryophyta node to the moss, hornwort and liverwort
crown nodes, as context. X26 is read for state 4 (trilete or inaperturate monad) on the same paths.

**C. Time-stretch.**
- The timetrees embed Hooper et al.'s calibrations, the M2 maximum among them, so B is conditional
  on the dates being tested. **Corrected after the run:** the deposited ancestral-state timetrees
  date crown Embryophyta at 508 Ma, from the earlier Harris et al. (2022) and Clark et al. (2023)
  divergence times. They do not use Hooper et al.'s recalibration (457–450 Ma). B is therefore
  conditional on those older dates, not on M2. C's estimands are unchanged.
- C asks a date-free question: given a lineage producing trilete spores at time *T*, what is the
  probability it keeps doing so, without departure, until the first appearance?
- Under a Markov model this is R(L) = exp(−q₃ L), where q₃ is the total rate out of state 3 and
  L = *T* − τ.
- It is reported for τ = 452.8 Ma (the base of the Katian, the certain first appearance) and
  *T* ∈ {459.1, 470, 480, 500, 515.5} Ma.
- q₃ comes from the fitMk ER and ARD fits and from the posterior Q samples of the stochastic maps
  (median and 95% interval).
- One lineage is the conservative case; a diversifying crown has several.

## Acceptance (before any result is read)

1. **Reproduction.**
   - Stochastic-mapping state frequencies at both crown nodes, for X21 and X26 on all three
     trees, must lie within 0.05 of the deposited `SCM_*` values (Monte Carlo error at 1,000 maps).
   - fitMk marginal values must lie within 0.005 of the deposited `ER_*` and `ARD_*` values.
2. If reproduction fails, the discrepancy is reported and B and C are not interpreted.
3. B and C are model-conditional (an equal-rates or all-rates-different Mk process on 38 tips).
   They say what Hooper et al.'s own model implies, not whether trilete production persisted.

## Outputs

- `out/reproduction.csv`: values against the deposited outputs.
- `out/persistence.csv`: B, by tree, character and path.
- `out/retention.csv`: C.
- `out/receipt.json`: input hashes, seeds, R and package versions.
- The run script is `asr_persistence.R`. Packages are pinned in `renv.lock`, the project-local renv
  this directory activates through `.Rprofile`; restore them with `Rscript -e 'renv::restore()'`.
  The lockfile was written with `renv::snapshot(force = TRUE)`, because phangorn (a phytools
  dependency) declares Bioconductor packages this analysis does not use. Nothing is installed
  globally.

## Results (2026-10-31)

Run with `Rscript asr_persistence.R` under the pinned `renv.lock` (R 4.6.1, ape 5.8-1,
phytools 2.5-2). It took 8 minutes on mini. Seeds, input hash and output hashes are in
`out/receipt.json`.

**Reproduction passes, 156 of 156** (`out/reproduction.csv`).
- Stochastic-mapping state frequencies differ from the deposited values by at most 0.036, within
  the 0.05 Monte Carlo tolerance.
- ER and ARD marginal values reproduce exactly (largest difference below 10⁻⁴).
- The deposited outputs are therefore regenerated by their own code and data under these package
  versions.

**B. Persistence on the maps** (`out/persistence.csv`, X21, the trilete aperture). In these trees
the path from crown Embryophyta to crown Tracheophyta is 58.2 Myr.

| Tree | Crown starts trilete | Trilete throughout the path to crown Tracheophyta | Same, given a trilete start | Departures per map |
|---|---|---|---|---|
| extant only | 0.876 | 0.862 | 0.984 | 0.016 |
| eophytes on the embryophyte stem | 0.969 | 0.969 | 1.000 | 0.000 |
| eophytes on the tracheophyte stem | 0.959 | 0.957 | 0.998 | 0.002 |

Other lineages, as context:
- **Liverworts**, where Hooper et al. infer an independent loss of the aperture: 0.305–0.338.
- **Mosses:** 0.83–0.94.
- **Hornworts:** 0.80–0.90.
- **X26:** the monad state persists on every path in at least 99.5% of maps.

**C. Retention without departure, single lineage** (`out/retention.csv`). The rate out of the
trilete state is q₃ = 0.0016 per Myr under ER on every tree. Under ARD it is 0.0021–0.0043 per Myr,
and the stochastic-mapping posterior median is 0.0016–0.0017.

| *T* (Ma) | L (Myr) | R, ER | R, ARD (range over trees) | R, stochastic-mapping posterior, 95% (widest tree) |
|---|---|---|---|---|
| 459.1 | 6.3 | 0.990 | 0.973–0.987 | 0.936–0.995 |
| 470 | 17.2 | 0.972–0.973 | 0.929–0.964 | 0.835–0.988 |
| 480 | 27.2 | 0.957–0.958 | 0.890–0.944 | 0.752–0.980 |
| 500 | 47.2 | 0.926–0.928 | 0.817–0.905 | 0.609–0.966 |
| 515.5 | 62.7 | 0.903–0.905 | 0.764–0.876 | 0.518–0.956 |

**Reading (I).** Under Hooper et al.'s own data and models:
- **The tracheophyte stem keeps it.** A crown ancestor making trilete spores passes that production
  down the tracheophyte stem with almost no interruption.
- **A single lineage is likely to keep it.** Started at any *T* the clocks propose (459–515 Ma), one
  lineage keeps making trilete spores to the Katian with probability 0.76–0.99 (point estimates).
  The low end is the all-rates-different fit on the extant tree at 515.5 Ma. The posterior 95%
  interval reaches 0.52 there.
- **Several lineages raise that.** A crown with several lineages makes persistence more likely
  still.
- **Status.** P1's persistence link moves from unresolved to **supported under these models**, and
  R(L) becomes an explicit, model-conditional factor in any node statement.

**Limits.**
- **Mk models.** An equal-rates or all-rates-different Mk process on 38 tips. Rates are
  tree-averaged, and the liverwort loss dominates them.
- **One aperture marginal.** It is reconstructed separately from the dispersal unit (A1).
- **Production, not abundance.** Persistence concerns production only; abundance is F3's history
  class.
- **Model behaviour.** This shows what the published model implies, not that trilete production
  persisted.
