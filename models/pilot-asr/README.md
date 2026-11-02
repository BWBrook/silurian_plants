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

- `data/external/local/deposits/hooper2026-spore-evolution/02. Ancestral State Estimation.zip`:
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
- the number of departures from state 3 on that path, and of entries into it. As first run this
  was labelled "returns" but counted every entry, first acquisition included; it is now split into
  entries and re-entries (see "Diagnostics").

The same is read for the paths from the crown-Embryophyta node to the moss, hornwort and liverwort
crown nodes, as context. X26 is read for state 4 (trilete or inaperturate monad) on the same paths.

**C. Time-stretch.**
- The timetrees embed Hooper et al.'s calibrations, the M2 maximum among them, so B is conditional
  on the dates being tested. **Corrected after the run:** the deposited ancestral-state timetrees
  date crown Embryophyta at 508 Ma, from the earlier Harris et al. (2022) and Clark et al. (2023)
  divergence times. They do not use Hooper et al.'s recalibration (457–450 Ma). B is therefore
  conditional on those older dates, not on M2. C's estimands are unchanged.
- C asks: given a lineage producing trilete spores at time *T*, what is the probability it keeps
  doing so, without departure, until the first appearance? The question is not date-free. The rates
  are fitted on dated trees (corrected after Codex's review, 2026-10-31).
- Under a Markov model this is R(L) = exp(−q₃ L), where q₃ is the total rate out of state 3 and
  L = *T* − τ.
- It is reported for τ = 452.8 Ma and *T* ∈ {459.1, 470, 480, 500, 515.5} Ma. τ is the base of
  the Katian, a chosen stage-boundary scenario, not a measured first-appearance date. With fixed
  rates, a younger τ lengthens L and lowers retention.
- q₃ comes from the fitMk ER and ARD fits and from the posterior Q samples of the stochastic maps
  (median and 95% interval).
- One lineage is the conservative case; a diversifying crown has several.

## Acceptance (before any result is read)

1. **Reproduction.**
   - Stochastic-mapping state frequencies at both crown nodes, for X21 and X26 on all three
     trees, must lie within 0.05 of the deposited `SCM_*` values (Monte Carlo error at 1,000 maps).
   - fitMk marginal values must lie within 0.005 of the deposited `ER_*` and `ARD_*` values.
2. If reproduction fails, the discrepancy is reported and B and C are not interpreted.
3. B and C are model-conditional (an equal-rates or all-rates-different Mk process on the 27-, 38-
   and 38-tip trees).
   They say what Hooper et al.'s own model implies, not whether trilete production persisted.

## Outputs

- `out/reproduction.csv`: values against the deposited outputs.
- `out/persistence.csv`: B, by tree, character and path.
- `out/retention.csv`: C.
- `out/receipt.json`: input hashes, seeds, R and package versions.
- `out/diagnostics_maps*.csv` and `out/diagnostics_receipt*.json`: the kept chains, from
  `asr_diagnostics.R`. The generation receipts' hashes for the chain and summary tables refer to the
  first summaries, which are superseded.
- `out/diagnostics_chains*.csv`, `out/diagnostics_summary*.csv`, `out/retention_chains.csv` and
  `out/summary_receipt.json`: summaries of the kept chains, from `summarise_chains.R`. Shared inputs
  and path readers are in `common.R`.
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

- **Which maps.** The paths are read from ER stochastic maps only. ARD enters C as fitted-rate
  scenarios, not as stochastic-path evidence.
- **The 1.000.** It is 969 of 969 sampled trilete starts without a departure, a Monte Carlo count
  and not a certainty. Its precision is in "Diagnostics".
- **Package version.** The pinned phytools is 2.5-2; Hooper et al.'s Methods name 2.4.4. The
  numerical reproduction above succeeds under the pinned version.

Other lineages, as context:
- **Liverworts**, where Hooper et al. infer an independent loss of the aperture: 0.305–0.338.
- **Mosses:** 0.83–0.94.
- **Hornworts:** 0.80–0.90.
- **X26:** the monad state persists on every path in at least 99.5% of maps.

**C. Retention without departure, single lineage** (`out/retention.csv`). The rate out of the
trilete state is q₃ = 0.0016 per Myr under ER on every tree. Under ARD it is 0.0021–0.0043 per Myr,
and the stochastic-mapping posterior median is 0.0016–0.0017.

The last column comes from the reproduction run's single chain per tree. It is superseded by the
converged intervals in "Diagnostics results" (`out/retention_chains.csv`).

| *T* (Ma) | L (Myr) | R, ER | R, ARD (range over trees) | R, stochastic-mapping posterior, 95% (widest tree; single chain) |
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
  interval reaches 0.33 there on the converged chains. The table's last column, from one unconverged
  chain, said 0.52; see "Diagnostics results".
- **Several lineages raise that.** A crown with several lineages makes persistence more likely
  still.
- **Status.** P1's persistence link moves from unresolved to **supported under these models**.
- **How R(L) is used (corrected 2026-10-31, after Codex, Correspondence 2628 and 2631).** It is not
  multiplied into an F3 verdict or confidence level, whose conditioning and uncertainty differ; no
  joint coverage follows from a product. It defines named conditional or sensitivity scenarios
  beside the F3 result until an inferential combination is justified and validated. C holds the
  fitted rates fixed while lengthening L; re-fitting on a tree rescaled to an older crown would
  change them, so C's values are sensitivity scenarios.

## Diagnostics (pre-declared 2026-10-31, before the run)

Codex's review (`docs/audits/2026-10-31-screen-and-persistence-review.md` §4) found the
implementation sound but the Monte Carlo precision unassessed. Each fit had one thinned rate chain,
and no rate trace, path indicators, ESS or MCSE was kept. `asr_diagnostics.R` addresses that.
- **Runs.** X21 on each tree, four independent chains with their own seeds, under the reproduction's
  settings. Each chain has 1,000 maps.
- **Retained.** Every map's sampled rate out of state 3, and its path indicators: held throughout,
  departures, entries, re-entries and start state.
- **Outputs.** `out/diagnostics_maps.csv`, `out/diagnostics_chains.csv`,
  `out/diagnostics_summary.csv` and `out/diagnostics_receipt.json`.
- **Counting fix.** `mean_returns` counted every entry into state 3, first acquisition included. It
  is replaced by `mean_entries` and `mean_reentries`, the latter counting only entries after the path
  has already been in state 3. `asr_persistence.R` now shares its inputs and path readers with the
  diagnostics through `common.R`. Re-running it with the same seeds must reproduce every earlier
  value exactly.

**Acceptance.** The run leaves the settings untouched; nothing is tuned to pass.
1. **Rate chain.** For each tree, R-hat of q₃ across the four chains is at most 1.01, and the
   pooled ESS of q₃ is at least 400.
2. **Precision.** Conditional persistence (held throughout, given a trilete start) is quoted with
   its MCSE. The MCSE comes from the linearised ratio, with each chain's autocorrelation counted.
   Three decimals are quoted only if the MCSE is at most 0.0005; otherwise two decimals or fewer,
   with the MCSE. Where no departure occurs in any chain, the result is given as an upper bound on
   the departure probability (rule of three on the effective number of trilete starts), not as
   1.000.
3. **Agreement.** Each reproduction value (0.984, 1.000, 0.998) must lie within the range of the
   four new chains, widened by two MCSE. A miss is reported as a precision finding.

If 1 fails, the persistence result is restated as unconverged at these settings, and a longer chain
is the next step.

**Longer chain (pre-declared 2026-10-31, after the first diagnostic run and before this one).** The
extant tree failed criterion 1 at Hooper et al.'s settings. It is re-run with four new chains:
- `Rscript asr_diagnostics.R ext 10000 100`;
- burn-in 10,000, thinning every 100, so 100,000 generations for the same 1,000 maps;
- the model, prior and proposal (vQ = 0.01) unchanged, so the target posterior is the same;
- outputs tagged `_ext_b10000_s100`.

The same three criteria apply. If it still fails, the extant-tree persistence is reported as
unconverged, with the chain spread as its uncertainty.

## Diagnostics results (2026-10-31)

Outputs: `out/diagnostics_*.csv` and receipts. The four-chain run at Hooper et al.'s settings took
6 minutes on mini; the longer extant-tree run took 11. The reproduction script, re-run after the
refactor, reproduces every earlier value exactly; `mean_returns` is renamed `mean_entries`, and
`mean_reentries` is added.

| Tree | Chain settings | R-hat q₃ | Pooled ESS q₃ | Persistence given a trilete start | MCSE | Range over chains | Reproduction value inside? |
|---|---|---|---|---|---|---|---|
| extant only | Hooper | **1.111 (fails)** | 416 | 0.97 (0.969; 101 departures in 3,299 starts) | 0.007 | 0.030 | (unconverged) |
| extant only | burn-in 10,000, thin 100 | 1.006 | 1,750 | **0.98** (0.977; 77 in 3,382) | 0.003 | 0.010 | 0.984: yes |
| eophytes on the embryophyte stem | Hooper | 1.007 | 3,732 | **0.999** (3 in 3,876) | 0.0005 | 0.002 | 1.000: yes |
| eophytes on the tracheophyte stem | Hooper | 1.000 | 3,909 | **0.99** (0.995; 20 in 3,788) | 0.001 | 0.004 | 0.998: yes |

Every criterion passes on the converged runs. MCSEs pool independent chains through the variances of
their means (corrected after Codex's second review; the first summary under-stated the failed
extant run's MCSE, 0.004 against 0.007). What changes:
- **The 1.000 was a zero count.** Departures do occur on the embryophyte-stem tree, 3 in 3,876
  starts. The reproduction chain happened to draw none of its 969.
- **Extant-tree mixing.** At Hooper et al.'s settings the rate chain on the extant tree does not
  converge. Four seeds put the crown-Embryophyta trilete frequency at 0.785–0.877. The longer chains
  agree at 0.837–0.852, and the deposited value is 0.84. Single-chain stochastic-mapping summaries on
  that tree therefore carry seed error of several hundredths. Their qualitative reading, trilete as
  the modal crown state, is unaffected.
- **Re-entries are rare.** On the tracheophyte path, entries after a departure are 0.006 per map on
  the extant tree (long chains) and 0.001–0.005 on the others. Almost every entry is the first
  acquisition.
- **The retention posterior is wider on the extant tree.** The converged q₃ posterior there has a
  heavier upper tail than the single chain sampled. The point estimates (ER and ARD fits) are
  deterministic and unchanged.

  | *T* (Ma) | R, posterior median and 95%, extant (long chains) | Embryophyte stem | Tracheophyte stem |
  |---|---|---|---|
  | 459.1 | 0.989 (0.895–0.995) | 0.990 (0.979–0.995) | 0.989 (0.977–0.995) |
  | 470 | 0.970 (0.739–0.988) | 0.972 (0.943–0.987) | 0.971 (0.939–0.987) |
  | 480 | 0.952 (0.619–0.981) | 0.956 (0.912–0.979) | 0.955 (0.906–0.979) |
  | 500 | 0.919 (0.436–0.967) | 0.925 (0.852–0.964) | 0.923 (0.842–0.964) |
  | 515.5 | 0.894 (0.332–0.956) | 0.902 (0.808–0.953) | 0.899 (0.796–0.953) |

  These come from `summarise_chains.R`, which reads the kept rate traces. The widest interval at
  515.5 Ma now reaches 0.33, not 0.52.

**Reading.** P1's persistence link stays supported under these models. Given a trilete crown
ancestor, the aperture is held to crown Tracheophyta with probability 0.98–1.00 on every tree, now
with measured precision. Retention scenarios for old origins on the extant tree are less certain
than first reported.

**Limits.**
- **Mk models.** An equal-rates or all-rates-different Mk process on trees of 27 (extant), 38 and
  38 tips. Rates are
  tree-averaged, and the liverwort loss dominates them.
- **One aperture marginal.** It is reconstructed separately from the dispersal unit (A1).
- **Production, not abundance.** Persistence concerns production only; abundance is F3's history
  class.
- **Model behaviour.** This shows what the published model implies, not that trilete production
  persisted.
