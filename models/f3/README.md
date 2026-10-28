# F3: dating origination from an incomplete record

Loop 1, steps 2 and 3 of `docs/plan-f3.md`. A virtual palaeontology (a clade of growing abundance that leaves
stage-dated fossil occurrences), the classical estimators of the first appearance (step 2, the sketch), and the
ramp-aware likelihood estimators with the recovery study that tests all of them (step 3, below). Written by
Claude Sonnet 5.5 (`claude-sonnet-5-5`), 2026-10-28.

## Step 2: files

- `sim.py`: the simulator. `Constant`, `Logistic` and `BirthDeath` give the abundance N(t) behind one
  interface. `Channel(psi, effort)` records occurrences as a Poisson process with intensity
  psi * N(t) * E(t), E constant within each ICS stage (`data/timescale.csv`). `simulate` returns the true
  origination age `t0`, the abundance path and, for each channel, the true age of each record and the age
  range of its stage.
- `estimators.py`: `oldest` (naive baseline), `marshall_1990`, `strauss_sadler_1989`,
  `weighted_mcinerny` and `griwm` (Bradshaw et al. 2012, first appearance), and `stage_resampled`, the wrapper
  for stage-dated records. All return an `Interval(lo, point, hi)`.
- `test_sketch.py`: 31 checks (simulator invariants, hand-checkable tiny cases, the direction convention,
  the GRIWM cross-check against the authors' code, coverage under the classical assumptions, and the ramp
  degradation, which is printed and not asserted).
- `run_sketch.py`: the demonstration grid. About 40 s on mac-mini. Writes `out/sketch_grid.csv` and
  `out/sketch_grid.meta.json` (root seed, settings, `timescale.csv` hash, numpy version).

```bash
uv run models/f3/run_sketch.py
uv run --with pytest --with numpy --with scipy pytest models/f3 -p no:cacheprovider -s
```

## Conventions (steps 2 and 3)

- **Ages** are Ma, decreasing towards the present: older is larger. The first appearance is the oldest
  record, and every upper bound lies at an older age. There is no `first`/`last` switch and no forward-time
  axis anywhere, which avoids the `tbea` swap EPRP found. `test_classical_bounds_extend_towards_older_ages`
  checks the direction.
- **Effort and window.** E(t) is a per-stage dictionary (default 1; any non-negative value). The window ends
  at the base of the Eifelian (end of the Emsian) unless set otherwise. Records exist only between the window
  end and `t0`.
- **Birth-death.** Linear process from one lineage, simulated exactly (Gillespie) and conditioned on
  survival to the window end by rejection. N counts lineages; psi is per lineage per Myr.
  **Logistic.** N(s) = k / (1 + (k-1) e^{-r s}), s Myr after `t0`, so N(0) = 1; discretised in 0.01 Myr cells.
  **Constant.** N = k from `t0`: the control with no ramp.
- **Seeds.** Everything descends from one seed through `child_seed(seed, index)`, which never mutates its input.
  The abundance path, each channel's records and the dating draws have separate child streams, so a seed plus
  the arguments reproduces a run, and changing psi leaves the abundance path unchanged. The grid root seed is
  20261028; replicate `i` of growth form `g` is `SeedSequence(root, spawn_key=(g, i))`.
- **Stage-dated records.** Each record keeps the range [`young`, `old`] of its stage. `stage_resampled` draws every
  record's age uniformly within its range, applies the estimator to each draw, and pools: `lo` and `hi` are the
  2.5% quantile of the draws' `lo` and the 97.5% quantile of their `hi`, and `point` is the median of their
  points. Stage bases are taken as exact (the boundary uncertainty of primer section 1.2 still waits for the joint age model; see step 3).
- **`Interval`.** For the classical estimators `lo` is the oldest record and `hi` the one-sided upper bound on
  the origination. Coverage in the grid is `hi >= t0` (`coverage_upper`, the convention of Saltre et al. 2015:
  the truth lies between the first record and the upper bound) and, more strictly, `lo <= t0 <= hi`
  (`coverage_interval`, Bradshaw et al. 2012). Replicates with fewer than two records have no estimate; the
  share is `frac_undefined`, and coverage is over the rest.

## Sources read, by estimator

| Estimator | Read in this task | Not read |
|---|---|---|
| Marshall 1990 | Hammer's PAST manual page "Confidence intervals on stratigraphic ranges" (https://www.nhm.uio.no/english/research/resources/past/help/rangeconf.html): one endpoint, alpha = (1-C)^(-1/(H-1)) - 1 with H the number of horizons; two endpoints, C = 1 - 2(1+alpha)^-(H-1) + (1+2 alpha)^-(H-1); random (Poisson) horizons assumed. Also `tbea`'s `stratCI.R` (gaballench/tbea at 53a1e7ff, GPL-3), which labels the same one-endpoint formula Eq. 20 of Strauss & Sadler. | The paper, doi 10.1017/s0094837300009672 (paywalled; in `docs/closed-literature.csv`). |
| Strauss & Sadler 1989 | The same two sources. The point estimate follows Saltre et al. (2015), who took median estimates at alpha = 0.5: the 50% bound. | The paper, doi 10.1007/bf00897326. |
| GRIWM | Bradshaw et al. (2012), doi 10.1016/j.quascirev.2011.11.021, in full (the author's copy at conservationbytes.com); Saltre et al. (2015), doi 10.1016/j.quascirev.2015.01.022, the methods (same copy source); the authors' R code `Rextinct/R/griwm.R` in github.com/cjabradshaw/CRIWM at 8eb6f51 (MIT), in full. | McInerny et al. (2006), doi 10.1111/j.1523-1739.2006.00377.x, the estimator that GRIWM extends (paywalled); its form is taken from Bradshaw et al. and the code. |

**What the sources say, and what is implemented.**

- *Classical bounds.* Marshall's single-endpoint interval and Strauss & Sadler's one-parameter bound are the
  same formula in every source read, so `marshall_1990` and `strauss_sadler_1989` return the same `hi`. They
  differ only in `point`: the sources give Marshall an interval and no estimate, so `point` is the oldest record
  (the Signor-Lipps bias, in the grid's bias column for `oldest` and `marshall1990`). The two-endpoint
  (joint) case is not needed for a first appearance and is not implemented.
- *GRIWM.* For each series of the m oldest records (m = 2..n), the estimate lies beyond the oldest record by
  (span + unit) * (-ln alpha) / m, where span is the age range of the m records (the continuous form of
  McInerny's sighting-rate probability, as in the code). The series are weighted by 1/span, so series reaching
  further from the oldest record count less (Bradshaw et al. eq. 4; the code normalises the weights by the
  first, which cancels). Each date is first redrawn from a normal with its own sd, 10,000 times, and the 2.5%,
  50% and 97.5% quantiles of the weighted estimates are the interval and point. `weighted_mcinerny` is one
  such estimate; `griwm` adds the Gaussian resampling. With stage-dated records `stage_resampled` replaces the
  Gaussian by the uniform draw within the stage. `unit` (0.001 Myr) is the discrete time step of the sighting
  rate, the "+1 year" of the code; the code also rounds resampled dates to whole years, which is dropped here.
- *Reverse direction.* Applied to first appearances by mirroring the age axis. `test_sketch.py` checks four
  cases against the authors' inner loop run in R on negated ages (agreement to 1e-10).
- **Fault in the authors' arrival branch.** `griwm(signor_lipps = "arr")` in that code sets `t.n` to 1 for every
  series, so it returns an arrival estimate younger than the oldest record (99.53 for ages 100, 90, 60 at
  alpha = 1/e, where the mirrored extinction algorithm gives 107.13). Bradshaw et al. state only that the method
  "could also be applied reciprocally". The mirror implemented here is that reading; the `arr` option of
  `Rextinct` should not be used for first appearances until corrected.

## Step 2: what the sketch grid shows

`run_sketch.py`: three growth forms, three values of psi, two channels (spores at psi; bodies at psi/5),
2000 replicates per cell, origination drawn uniformly within the Telychian in each replicate, window to the
end of the Emsian. Constant: N = 50. Logistic: r = 0.35, k = 100 (half capacity about 13 Myr after the
origination). Birth-death: lambda = 0.25, mu = 0.15. Effort is constant. Monte Carlo error on a coverage
figure is at most 0.011 (0.005 near 0.95). The table shows the spore channel; `out/sketch_grid.csv` has both channels, the
`oldest` baseline, `strauss_sadler1989` coverage and the GRIWM alpha = 0.5 variant. "Exact" dates use the
true ages, "stage" the stage-resampling wrapper. Bias is median(point - t0) of the Strauss & Sadler point
estimate and of GRIWM (alpha = 0.05), in Myr; coverage is `coverage_upper`.

| growth, psi | median records | Marshall/S&S cover, exact | Marshall/S&S cover, stage | S&S bias, exact | S&S bias, stage | GRIWM cover / bias, exact | GRIWM cover / bias, stage |
|---|---|---|---|---|---|---|---|
| constant, 0.005 | 10 | 0.95 | 0.98 | +0.0 | +0.6 | 0.71 / +2.6 | 0.88 / +4.1 |
| constant, 0.02 | 42 | 0.94 | 0.98 | +0.0 | +1.4 | 0.77 / +1.0 | 0.97 / +3.1 |
| constant, 0.08 | 168 | 0.95 | 1.00 | +0.0 | +2.4 | 0.81 / +0.3 | 1.00 / +3.0 |
| logistic, 0.005 | 14 | 0.22 | 0.34 | -10.2 | -10.1 | 0.17 / -6.6 | 0.29 / -6.5 |
| logistic, 0.02 | 58 | 0.07 | 0.15 | -7.1 | -6.7 | 0.13 / -5.1 | 0.26 / -4.6 |
| logistic, 0.08 | 234 | 0.04 | 0.35 | -4.0 | -3.5 | 0.13 / -3.0 | 0.40 / -2.5 |
| birth-death, 0.005 | 6 (18% undefined) | 0.38 | 0.50 | -16.4 | -16.1 | 0.23 / -11.3 | 0.30 / -12.0 |
| birth-death, 0.02 | 23 | 0.28 | 0.37 | -9.0 | -8.9 | 0.29 / -5.0 | 0.39 / -5.3 |
| birth-death, 0.08 | 91 | 0.20 | 0.41 | -4.2 | -4.1 | 0.31 / -2.0 | 0.50 / -1.8 |

- **Under its own assumptions** (constant N and effort, exact dates) the classical 95% bound covers the true
  origination 0.94 to 0.95 of the time at every record count, and the Strauss & Sadler point estimate is
  unbiased in the median. `test_classical_interval_covers_at_its_nominal_rate_under_its_own_assumptions`
  asserts this over 2000 replicates at a fixed seed (0.95 +/- 0.02). In a scratch run of 12,000
  replicates (psi = 0.02, constant) the coverage was 0.950.
- **Under a ramp** the classical bound in the spore channel covers the truth 0.04 to 0.4 of the time, with
  median bias of -4 to -16 Myr. More records shrink the bias, but with exact dates coverage falls as they
  increase, because the bound narrows faster than the bias. Where records are scarce, coverage rises (bodies
  at psi = 0.001) only because the bound is then very wide (median 25 Myr beyond the truth for the logistic).
- **GRIWM** at its default alpha = 0.05 is not a calibrated bound even under uniform sampling: the estimate
  lies older than the truth in 0.64 to 0.81 of replicates across the grid, not 0.95. With exact dates its 95% interval has zero
  width, because the interval comes only from dating resampling. Under a ramp it is biased and under-covers
  like the classical bound, less severely in median bias.
- **Stage dating** adds an upward bias that grows with the record count: every record in the stage that holds
  the origination is dated to the whole stage, so the oldest drawn age tends to the stage base, older than the
  truth. Coverage by `hi` goes up for that reason (0.98 to 1.00), and the strict `coverage_interval` falls (to
  0.29 at psi = 0.08, constant).

## Step 3: the recovery study

Loop 1, step 3 of `docs/plan-f3.md`. Written by Claude Sonnet 5.5 (`claude-sonnet-5-5`), 2026-10-28. The step-2 amendment
established that classical estimators under-cover when abundance ramps up after origination. This step builds estimators
that model the ramp, and asks which estimators may be used on real data and whether the record can identify the
origination at all.

### What was added

- `ramp.py`: likelihood estimators of T0 from **stage-binned counts**.
  - Records in stage j and channel c are Poisson with mean psi_c * E_cj * integral of N(t) over the stage, with N(t) = 0 before
    T0 and N(T0) = 1. E is a known effort series.
  - Two growth forms with closed-form stage integrals. Logistic: N(s) = k / (1 + (k - 1) exp(-r s)), s = T0 - t, capacity k
    fixed (or profiled over several values) and rate r free. Expected birth-death curve: N(s) = exp(g s), g = lambda - mu >= 0
    free; g = 0 is constant abundance.
  - psi_c is profiled out exactly (its maximum-likelihood value is n_c / sum_j E_cj I_j), so the likelihood surface depends on
    T0 and the rate only. `RampModel` caches the stage integrals on a 0.5 Myr grid of T0 (up to 515.5 Ma, the oldest clock
    maximum named in the plan) and 80 logistic rates (0.01 to 3 per Myr) or 100 net rates (0 and 1e-4 to 1 per Myr). `fit` takes
    the grid maximum, polishes it with scipy (Nelder-Mead), and returns the 95% profile interval for T0 (a log-likelihood drop of
    1.92; the hull of the T0 values inside it). The profile over the rate is the grid maximum refined by a parabola in log rate. If
    the interval is narrower than 1.5 Myr, or the grid profile lies more than 0.2 below the polished maximum, the grid is too coarse
    for the likelihood and the interval is recomputed on a fine grid of T0 and rate. Capacity can be profiled by passing several
    models, one per capacity: the profile is their pointwise maximum. The profile is **unbounded** when it is still inside the
    interval at 515.5 Ma.
  - Channels share N(t) and T0 and have separate psi and E: the **joint fit** adds the channels' log-likelihoods. A channel
    without records adds nothing, so the joint fit with an empty second channel is the one-channel fit.
- `inputs.py`: per-stage effort series for the window Darriwilian to Emsian, read from `data/occurrences/effort.csv` and written
  to `out/effort_series.csv`. Spores: `n_docs` summed over palaeogeographic units. Bodies: `land + marginal` summed over units.
  **Stage boundaries are the fixed ICS v2024/12 ages of `data/timescale.csv`.** Propagating boundary-age uncertainty needs the
  joint, ordered age model of primer section 1.1 (the Harrigan et al. posterior), which is not yet in hand, so it is not
  approximated here by perturbing boundaries independently. The spore series stops at 2006 (the post-2006 literature is not yet
  counted).
- `recovery.py`: the recovery study; writes `out/recovery_grid.csv` and `out/recovery_grid.meta.json`.
- `report.py`: aggregates the grid into `out/recovery_summary.csv` and prints the tables below.
- `identifiability.py`: the profile-likelihood surfaces, `out/identifiability_surface_435.png` and `..._460.png`.
- `test_ramp.py`: 43 tests of the likelihood (against numerical quadrature, the simulator's abundance integral, and a dense-grid
  reference for the interval), parameter recovery in large samples, the joint fit, the age convention, the inputs, and the
  recovery machinery. `sim.py` gained `stage_exposure`, the integral of N over each stage, with `sample_records` refactored onto the
  same cell routine; the step-2 grid regenerates byte-identical.

### Design of the study

```bash
uv run models/f3/inputs.py          # out/effort_series.csv
uv run models/f3/recovery.py        # out/recovery_grid.csv and .meta.json (about 28 min under heavy load)
uv run models/f3/report.py          # out/recovery_summary.csv and the tables below
uv run models/f3/identifiability.py # out/identifiability_surface_*.png
```

A **scenario** is an origination
window x growth x effort x preservation level; each is replicated 1000 times (Monte Carlo error on a coverage figure at most 0.016,
0.010 near 0.90) from the root seed 20261029, replicate `i` of window `w` and growth `g` being
`SeedSequence(root, spawn_key=(w, g, i))`. In each replicate T0 is drawn uniformly within the window and the abundance path is
simulated once; every effort and preservation level is sampled from that path.

| Factor | Values |
|---|---|
| Origination window | Darriwilian to Sandbian (469.4 to 452.8 Ma, the spore case), Katian to Hirnantian (452.8 to 443.1), Telychian to Sheinwoodian (438.6 to 430.6, the body case) |
| Growth | constant; logistic with k = 100 and r = 0.15, 0.3, 0.6 per Myr; logistic with r = 0.3 and k = 30 or 300 (the capacity the fit assumes is wrong); birth-death with lambda - mu = 0.05 (0.20, 0.15) and 0.10 (0.25, 0.15) |
| Effort | the real series (`out/effort_series.csv`, scaled to mean 1) or constant |
| Preservation | expected records in the window, spores / bodies: low 30 / 10, mid 100 / 30, high 300 / 100, very high 1000 / 300 |

Preservation is set by the expected count: psi of each channel is its target divided by its effort-weighted abundance integral
in that replicate, so a clade that originates earlier has a lower psi, and the realised count is Poisson about the target. The
realised medians equal the targets (`median_n_spores`, `median_n_bodies` in the grid; the spore series is the
higher-count channel throughout, as in the real record). Pinning the count builds in the question the study asks: an earlier origination of the same record is one with poorer
preservation.

Estimators, each on spores alone, bodies alone, and both channels (`joint`):

| Estimator | What it is | Point | Interval |
|---|---|---|---|
| `classical` | Strauss and Sadler's bound (Marshall's one-endpoint interval) on records drawn uniformly within their stages | 50% bound | oldest record to 95% bound; stage draws pooled as in step 2 |
| `griwm` | mirrored GRIWM (alpha 0.05), stage-resampled | median of draws | calibrated by simulation, below |
| `ramp_logistic` | `ramp.fit`, logistic, capacity 100 fixed | maximum | 95% profile |
| `ramp_logistic_kfree` | the same with capacity profiled over 10, 30, 100, 300, 1000 | maximum | 95% profile |
| `ramp_bd` | `ramp.fit`, expected birth-death curve | maximum | 95% profile |

In the joint case the classical and GRIWM estimators use the pooled records of both channels.

**Acceptance.** The plan fixes the first criterion; how each estimator is judged under it was fixed in `recovery.py` before the first grid run.
- An interval estimator needs coverage of at least 0.90 and |median bias| under 2 Myr (the plan).
- Coverage is of the estimator's own nominal interval: the classical bound's one-sided 95% (hi >= T0), the ramp fits' two-sided 95% profile interval (lo <= T0 <= hi). The grid has both conventions for every estimator.
- GRIWM is a point estimator: |median bias| under 2 Myr and an interval calibrated by simulation. The interval is the 2.5% to 97.5% quantile range of (point - T0) from the same estimator in the constant-growth scenario with the same window, effort and preservation, shifted to the point. It is in-sample for the constant scenario itself. `calibrated_width_ma` gives the width of the interval calibrated in the scenario itself.
- An unbounded profile counts as covering, so `identified` records whether at most 10% of fits are unbounded, and `usable` requires both. The 10% limit was set before the run.

### Results

The final grid is 3 windows x 8 growth forms x 2 efforts x 4 preservation levels x 3 channel sets x 5 estimators = 2880 rows
(`out/recovery_grid.csv`, 1000 replicates each; seeds, constants and file hashes in `out/recovery_grid.meta.json`; aggregated in
`out/recovery_summary.csv`). It took 1704 s on mac-mini (10 workers) while other sessions held the load average at 70 to 140; an
earlier, smaller design (1728 rows, no capacity-profiled estimator) took 485 s under a load of about 20.

**Record counts.** The realised median counts equal the targets in every level.

| level | spores target | spores realised (median of cell medians) | bodies target | bodies realised |
|---|---|---|---|---|
| low | 30 | 30 | 10 | 10 |
| mid | 100 | 100 | 30 | 30 |
| high | 300 | 300 | 100 | 100 |
| very_high | 1000 | 1000 | 300 | 300 |

**Which estimators pass.** Scenarios meeting the plan's criteria (coverage of at least 0.90 and |median bias| under 2 Myr), out of the
scenarios in each growth family. A family has 24 scenarios per growth form (3 windows x 2 efforts x 4 preservation levels):

| channels | estimator | constant | logistic, capacity right | logistic, capacity wrong | birth-death |
|---|---|---|---|---|---|
| spores | classical | 12/24 | 1/72 | 1/48 | 6/48 |
| spores | griwm | 5/24 | 1/72 | 1/48 | 3/48 |
| spores | ramp_logistic | 4/24 | 37/72 | 4/48 | 1/48 |
| spores | ramp_logistic_kfree | 10/24 | 30/72 | 19/48 | 2/48 |
| spores | ramp_bd | 24/24 | 0/72 | 0/48 | 0/48 |
| bodies | classical | 12/24 | 0/72 | 0/48 | 0/48 |
| bodies | griwm | 4/24 | 2/72 | 0/48 | 0/48 |
| bodies | ramp_logistic | 10/24 | 11/72 | 4/48 | 0/48 |
| bodies | ramp_logistic_kfree | 14/24 | 4/72 | 4/48 | 2/48 |
| bodies | ramp_bd | 21/24 | 0/72 | 0/48 | 0/48 |
| joint | classical | 11/24 | 1/72 | 1/48 | 4/48 |
| joint | griwm | 5/24 | 1/72 | 1/48 | 4/48 |
| joint | ramp_logistic | 4/24 | 41/72 | 3/48 | 2/48 |
| joint | ramp_logistic_kfree | 7/24 | 29/72 | 21/48 | 3/48 |
| joint | ramp_bd | 24/24 | 0/72 | 0/48 | 0/48 |

Requiring also that at most 10% of profiles be unbounded (`usable`) changes only constant-growth rows of the ramp fits
(`ramp_bd` joint 24 to 16; `ramp_logistic` on bodies 10 to 4); the table is in `report.py`'s output.

The two criteria separately show why. Scenarios meeting the coverage criterion alone (the estimator's own interval, at least 0.90):

| channels | estimator | constant | logistic, capacity right | logistic, capacity wrong | birth-death |
|---|---|---|---|---|---|
| spores | classical | 24/24 | 1/72 | 2/48 | 7/48 |
| spores | griwm | 24/24 | 1/72 | 1/48 | 3/48 |
| spores | ramp_logistic | 6/24 | 52/72 | 9/48 | 4/48 |
| spores | ramp_logistic_kfree | 12/24 | 72/72 | 48/48 | 14/48 |
| spores | ramp_bd | 24/24 | 0/72 | 0/48 | 1/48 |
| bodies | classical | 18/24 | 1/72 | 0/48 | 0/48 |
| bodies | griwm | 24/24 | 8/72 | 5/48 | 0/48 |
| bodies | ramp_logistic | 13/24 | 53/72 | 28/48 | 13/48 |
| bodies | ramp_logistic_kfree | 18/24 | 72/72 | 48/48 | 31/48 |
| bodies | ramp_bd | 24/24 | 8/72 | 3/48 | 14/48 |
| joint | classical | 24/24 | 1/72 | 2/48 | 6/48 |
| joint | griwm | 24/24 | 1/72 | 1/48 | 4/48 |
| joint | ramp_logistic | 6/24 | 53/72 | 8/48 | 3/48 |
| joint | ramp_logistic_kfree | 10/24 | 71/72 | 48/48 | 12/48 |
| joint | ramp_bd | 24/24 | 0/72 | 0/48 | 2/48 |

Scenarios meeting the bias criterion alone (|median bias| under 2 Myr):

| channels | estimator | constant | logistic, capacity right | logistic, capacity wrong | birth-death |
|---|---|---|---|---|---|
| spores | classical | 12/24 | 32/72 | 16/48 | 26/48 |
| spores | griwm | 5/24 | 42/72 | 22/48 | 32/48 |
| spores | ramp_logistic | 16/24 | 43/72 | 7/48 | 22/48 |
| spores | ramp_logistic_kfree | 18/24 | 30/72 | 19/48 | 26/48 |
| spores | ramp_bd | 24/24 | 4/72 | 1/48 | 21/48 |
| bodies | classical | 16/24 | 5/72 | 4/48 | 7/48 |
| bodies | griwm | 4/24 | 14/72 | 10/48 | 15/48 |
| bodies | ramp_logistic | 17/24 | 13/72 | 6/48 | 7/48 |
| bodies | ramp_logistic_kfree | 18/24 | 4/72 | 4/48 | 7/48 |
| bodies | ramp_bd | 21/24 | 1/72 | 0/48 | 5/48 |
| joint | classical | 11/24 | 32/72 | 18/48 | 25/48 |
| joint | griwm | 5/24 | 43/72 | 25/48 | 34/48 |
| joint | ramp_logistic | 16/24 | 48/72 | 6/48 | 24/48 |
| joint | ramp_logistic_kfree | 16/24 | 30/72 | 21/48 | 27/48 |
| joint | ramp_bd | 24/24 | 5/72 | 1/48 | 22/48 |

**Findings.**

- **No estimator passes across the plausible scenarios.** Each passes where its assumptions hold and enough records exist, and
  nowhere else. At 30 spore and 10 body records, no estimator passes more than 3 of the 42 non-constant scenarios (per channel set);
  at 1000 and 300, `ramp_logistic` passes all 18 scenarios with the capacity right.
- **Classical bound and GRIWM fail every ramp**, as in the sketch. Under constant growth both are calibrated (the classical
  one-sided bound covers 24/24; the calibrated GRIWM interval is built from that scenario), and fail on bias alone: stage dating moves
  the classical point older by +2.3 to +4.0 Myr for an origination in the Darriwilian to Sandbian, +1.2 to +2.5 in the Katian to
  Hirnantian, +1.3 to +1.9 in the Telychian to Sheinwoodian (joint, real effort). They pass under constant growth only for late
  origination or few records.
- **`ramp_bd` is the constant-abundance likelihood with known effort when g = 0, and passes constant growth 24/24. It fails every
  ramp, its own birth-death scenarios included (0/48).** Its profile interval is too narrow: joint coverage at birth-death growth
  0.82 (low), 0.77 (mid), 0.66 (high) and 0.47 (very high). The Poisson likelihood ignores the variance of the realised path,
  and the simulated clade is conditioned on survival, so its mean rises faster in the first Myr than exp(g s). Under logistic
  growth its coverage is 0.01 to 0.53 at mid and high preservation.
- **`ramp_logistic` (capacity 100) is calibrated when form and capacity are right and the record is large enough**: joint passes
  41/72 capacity-right scenarios, by level 0/18 (low), 6/18 (mid), 17/18 (high; one fails on coverage),
  18/18 (very high). Coverage over those 72 scenarios has median 0.93 and minimum 0.84 (0.93 or more at very high). Median bias is
  -5.96 Myr at low, -1.69 at mid, -0.37 at high and -0.11 at very high preservation: the maximum sits young of the truth when records are few. It
  fails when the capacity is wrong by a factor of three (3/48; median bias +1.9 for k = 30 and -4.0 for k = 300 at mid and real effort; coverage 0.85 and 0.75) and
  under birth-death growth (2/48).
- **`ramp_logistic_kfree` (capacity profiled over 10 to 1000) has near-nominal intervals for every logistic ramp, whatever the capacity**:
  joint coverage meets 0.90 in 71/72 capacity-right and 48/48 capacity-wrong scenarios (minimum 0.89, median 0.95). It fails the
  plan only on bias: its maximum is young of the truth by a median 0.2 Myr at very high preservation, 1.5 at high, 3.8 at mid and
  7.5 at low (those logistic scenarios, joint), so it passes 29/72 and 21/48. Intervals are two to three times as wide as the fixed-capacity ones: median width 24 Myr at mid, 16.5 at high and
  10.8 at very high preservation. Under birth-death growth coverage is 0.85 and 0.87 at mid and 0.77 and 0.79 at high preservation, and
  under constant growth 0.90 at mid and 0.75 at high, where the lower end of the interval misses (hi >= T0 is met).
- **The joint fit is the spore fit in practice.** `ramp_logistic` passes 57% of capacity-right scenarios jointly and 51% on spores alone;
  bodies alone pass 15%, because they have a third of the records and, in the real effort series, a threefold step in
  land-plus-marginal collections at the Lochkovian. The joint profile is less unbounded than both single channels by more than 0.05 in
  34 of 576 ramp-estimator cells (at most 0.12; 24 of the 34 at low counts) and never more than 0.003 more unbounded than spores alone.

**Joint fit, real effort, mid preservation** (100 spore and 30 body records expected; median over the three origination windows).
Cells are own-interval coverage / median bias in Myr / median interval width in Myr / fraction of unbounded profiles (ramp fits only):

| growth | classical | griwm | ramp_logistic | ramp_logistic_kfree | ramp_bd |
|---|---|---|---|---|---|
| constant | 1.00 / +2.1 / 3.2 | 0.95 / +2.8 / 7.1 | 0.80 / +1.5 / 11.1 / 0.00 | 0.90 / +1.2 / 16.6 / 0.00 | 0.95 / +0.1 / 3.9 / 0.00 |
| logistic_r0.15 | 0.36 / -4.1 / 4.2 | 0.33 / -2.1 / 7.1 | 0.91 / -1.5 / 10.9 / 0.00 | 0.93 / -3.0 / 26.1 / 0.00 | 0.53 / -4.5 / 6.6 / 0.03 |
| logistic_r0.3 | 0.36 / -5.2 / 3.6 | 0.23 / -3.5 / 7.1 | 0.91 / -1.3 / 12.0 / 0.00 | 0.95 / -5.1 / 21.9 / 0.00 | 0.08 / -6.7 / 2.8 / 0.00 |
| logistic_r0.6 | 0.50 / -2.0 / 3.4 | 0.32 / -1.0 / 7.1 | 0.90 / -1.4 / 11.0 / 0.00 | 0.97 / -3.3 / 17.8 / 0.00 | 0.05 / -5.2 / 2.3 / 0.00 |
| logistic_r0.3_k30 | 0.64 / -1.7 / 3.8 | 0.50 / +0.2 / 7.1 | 0.85 / +1.9 / 13.5 / 0.00 | 0.97 / -1.8 / 23.5 / 0.00 | 0.17 / -4.5 / 2.8 / 0.00 |
| logistic_r0.3_k300 | 0.18 / -7.6 / 3.9 | 0.10 / -6.2 / 7.1 | 0.75 / -4.0 / 10.7 / 0.00 | 0.95 / -7.1 / 21.1 / 0.00 | 0.08 / -9.5 / 3.3 / 0.00 |
| bd_g0.05 | 0.68 / -0.6 / 3.6 | 0.62 / +1.1 / 7.1 | 0.78 / -0.8 / 9.5 / 0.00 | 0.87 / -1.0 / 14.1 / 0.00 | 0.72 / -1.9 / 5.7 / 0.03 |
| bd_g0.10 | 0.38 / -3.6 / 3.6 | 0.38 / -1.6 / 7.1 | 0.39 / -4.6 / 5.0 / 0.00 | 0.85 / -3.1 / 14.0 / 0.00 | 0.82 / -3.3 / 22.5 / 0.47 |

**The upper limit**, which is what a test against a clock maximum needs. Coverage of hi >= T0 / median (hi - T0) in Myr, joint fit, real
effort, mid preservation. Every estimator's one-sided coverage is in `out/recovery_grid.csv` (`coverage_upper`,
`median_upper_excess_ma`); the high-preservation version is in `report.py`'s output.

| growth | classical | ramp_logistic | ramp_logistic_kfree | ramp_bd |
|---|---|---|---|---|
| constant | 1.00 / +3.6 | 1.00 / +10.3 | 1.00 / +15.4 | 0.97 / +2.0 |
| logistic_r0.15 | 0.36 / -2.2 | 0.92 / +5.3 | 0.93 / +20.0 | 0.53 / +0.5 |
| logistic_r0.3 | 0.36 / -2.0 | 0.92 / +6.4 | 0.95 / +14.9 | 0.08 / -4.7 |
| logistic_r0.6 | 0.50 / +0.0 | 0.91 / +6.2 | 0.97 / +12.4 | 0.05 / -3.6 |
| logistic_r0.3_k30 | 0.64 / +1.3 | 0.96 / +10.3 | 0.97 / +19.1 | 0.17 / -2.4 |
| logistic_r0.3_k300 | 0.18 / -5.5 | 0.75 / +2.5 | 0.95 / +11.8 | 0.08 / -7.5 |
| bd_g0.05 | 0.68 / +2.0 | 0.85 / +5.9 | 0.88 / +10.9 | 0.73 / +2.1 |
| bd_g0.10 | 0.38 / -1.8 | 0.40 / -1.1 | 0.85 / +6.1 | 0.83 / +16.4 |

### Identifiability

Can T0 and the ramp be told apart? **Only through the shape of the rise, and only if its form is right or profiled.** The first record
does not do it.

![Profile-likelihood surfaces for a clade originating 460 Ma](out/identifiability_surface_460.png)

`out/identifiability_surface_435.png` and `..._460.png` show one realisation each (real effort, 100 spore and 30 body records expected).
Rows: the log-likelihood over (T0, rate) with psi profiled out; the profile for T0; and the psi implied at each T0 by the best rate.

- **Exponential growth leaves an exact ridge.** Expected counts depend on psi * exp(g T0): an origination Delta Myr older with
  preservation lower by exp(-g Delta) predicts the same count in every stage the younger clade occupied. The bottom row of
  the figures shows the implied psi falling log-linearly with T0 along the ridge (the dashed lines). What breaks it is the older stages in which no
  record was found: an older origination predicts records there. A fast-growing clade predicts few, so in the unbounded cases the profile stays within 1.92
  of its maximum back to 515.5 Ma. For birth-death clades with g = 0.10 fitted by `ramp_bd`, the fraction of unbounded joint
  profiles is 0.66 at 30/10 expected records, 0.46 at 100/30, 0.28 at 300/100 and 0.15 at 1000/300; at g = 0.05, 0.32, 0.13, 0.06 and 0.04.
- **A logistic ramp with a known capacity ties psi to the plateau**, so psi and T0 separate and T0 is bounded: for spores and the joint
  fit at 100 expected records or more, at most 0.02 of `ramp_logistic` profiles are unbounded in the logistic scenarios (0.00 to 0.04 for the
  capacity-profiled fit). The price is the capacity: a wrong capacity shifts T0 along the ridge (bias +1.9 and -4.0 Myr for k = 30 and 300 at mid
  preservation, coverage 0.85 and 0.75). Profiling the capacity puts the ridge back into the interval: coverage returns to 0.95 and the interval widens to about 24 Myr at mid.
- **The window edge limits what can be known about an early origin.** The data stop at the Darriwilian, so an origination older than 469.4 Ma
  cannot be told from one at the edge. Joint profiles are unbounded in 0.074 (`ramp_logistic`), 0.131 (capacity profiled) and 0.191 (`ramp_bd`)
  of fits for origination in the Darriwilian to Sandbian, against at most 0.005 (0.076 for `ramp_bd`) from the Katian onwards.
- **Two channels add little unless each is thin.** In a noise-free test (`test_joint_fit_bounds_the_origination_when_neither_channel_does`),
  15 expected records per channel leave a logistic origination at 460 Ma unbounded for spores alone and for bodies alone, and
  bounded jointly (458.2 to 499.6 Ma). At the real count ratio the spore channel carries almost everything.
- **Old origin with poor preservation against young origin with good preservation** is therefore answered by the rise, not by the
  first record: under a logistic ramp with its capacity profiled the interval covers the truth 95% of the time but is 16 Myr wide (median, at 300/100
  records; 24 Myr at 100/30). Under birth-death growth it is not answered (above), and the finding is a demonstrated limit: what would resolve it is an
  independent measure of psi or of the abundance at origination, such as a denser record of the earliest stages or a count of
  the clade's later plateau.

### What step 4 should use

- **Do not use the classical bound, GRIWM or `ramp_bd` alone on a clade whose abundance rises.** They fail on coverage in nearly every ramp
  scenario (of the 168 joint ramp scenarios, classical meets the coverage criterion in 9, GRIWM in 6, `ramp_bd` in 2). Report the classical bound as the lower-limit view (its range-extension logic holds
  only for constant abundance and exact dating).
- **Primary: `ramp_logistic_kfree`, on spores and on both channels, as a conditional interval.** State it as "if abundance followed a logistic rise
  with a capacity between 10 and 1000, T0 lies in [lo, hi]". Use the interval, and in particular the **upper limit hi** for the tests against
  clock maxima (E1 to E3): its one-sided coverage is 0.93 to 0.98 for logistic ramps at mid and high preservation (0.81 to 0.88 under
  birth-death growth), with a median excess over T0 of 6 to 20 Myr at mid, so a clock maximum younger than hi cannot be excluded.
  Do not use its maximum as a point estimate: it is young of the truth by 1.5 to 7.5 Myr at 300/100 or fewer records.
- **Sensitivity: `ramp_logistic` with capacity 100 and `ramp_bd`.** Report them beside the primary fit and say which they agree with.
  A verdict that holds for the profiled-capacity interval but not for them is a statement about assumptions.
- **An unbounded profile is the result**: the record does not bound the origination, down to the 515.5 Ma search limit.
- **Check each event's record count against the levels above** before reading its interval. If E1 and E2 (spore documents)
  reach the 100 to 300 range and E3 to E5 (megafossil records) fall at or below 30 to 100 (an assumption to check against the occurrence data), the
  latter lie where no estimator in this study passes a ramp scenario and only the interval is defensible.
- **Inputs.** Build counts per stage and channel under the main reading, then under each alternative reading (`inputs.effort_series()` gives the
  effort; `ramp.RampModel(edges, family)` and `ramp.fit(models, n, effort)` do the rest). `ramp.fit` accepts non-integer counts, so a record
  dated to a range of stages can be apportioned among them; that is an approximation, not a mixture likelihood.
- **Propagate boundary-age uncertainty** (primer section 1.1) once the joint age model is in hand; it is fixed here.

### Limits of this study

- **Effort is known exactly and sampling is proportional to it.** The real effort series are proxies (all-taxa PBDB collections from land and marginal
  settings; Palynodata documents to 2006), so the coverage here is optimistic. Testing the fit against a mismeasured effort series is the first thing to do next.
- **Boundaries are fixed** at ICS v2024/12 (see above); origination is drawn uniformly within three windows; preservation counts are pinned by design.
- **One clade, one preservation process.** No extinction before the window end, no reworking, no facies or gap structure beyond the effort series, no
  producer-link uncertainty between spores and bodies (they share N(t) and T0 by assumption).
- **The birth-death scenarios are conditioned on survival**, so `ramp_bd` is approximately, not exactly, the generating mean (in a scratch check of 600 simulated paths with lambda = 0.25, mu = 0.15 and T0 = 437 Ma, the mean stage integral is 1.5 times
  that of exp(g s) in the origination stage and 2.0 to 2.4 times in the later ones). The logistic path is deterministic and exact.
- **The lower end of an interval can be conservative by up to 0.5 Myr** when the profile meets the top of the oldest occupied stage (the grid sets it to that edge).
  This cannot affect coverage, since T0 lies above that edge, and it widens intervals slightly.
- **Not done:** the PyRate, `tbea` and StratPal cross-checks, Marshall (1994, 1997) and Strauss and Sadler's two-endpoint cases, lineage-level birth-death with preservation,
  and the `deep-server` run (the grid ran on mac-mini).
- **Review.** An independent Claude subagent (run with the `sonnet` model alias) reviewed `ramp.py` and `recovery.py` against dense-grid references. It found no error in the likelihood (it matches
  `scipy.stats.poisson` to 1e-13), the age orientation, the seeding or the verdict logic, and four interval-construction defects: a gap in the birth-death rate grid, a rate box in the
  fine interval that excluded the best rate at the interval ends, the fine interval ignoring all but the best capacity, and the fine path not triggering when the grid profile was far below the polished
  maximum. All four were fixed before the final grid, with a dense-reference test (`test_interval_agrees_with_a_dense_reference_and_contains_the_maximum`).

### Carried over from step 2

- Effort that varies by stage: used (the real series). Preservation that depends on facies and gaps: through effort only.
- Joint stage-boundary age uncertainty: not done (fixed boundaries; see above).
- Lineage-level birth-death with a trait, extinction before the window end, dating by biozone or radiometric ages: not done.
- Estimators that model N(t) and preservation: done (`ramp.py`). Cross-checks against PyRate, `tbea` and StratPal: not done.
- Identifiability and the acceptance criteria: done above. Ensembles on `deep-server`: not done.

## Step 4: the compatibility estimator (F3 reshape v3)

Implements the estimator and validation harness of `docs/f3-shape.md` (v3, "What F3 reports" and "Validation before any real-data
result"). Written by Claude Sonnet 5.5 (`claude-sonnet-5-5`), 2026-10-28, to the construction designed by Claude Opus 5.5. Nothing
here has been run on real data: there is no real unit table yet. The smoke run below is a check that the machinery works, not the
validation study; the full grid and its acceptance run are for the parent and Codex to fix.

### Files

- `envelope.py`: the estimator. `Units` (eligible binary units: stage range, class, cluster, outcome), `AgeModel` (stage bases and
  their uncertainty from `data/timescale.csv`, via `sim.Timescale`), `Spec` (the inference fields of a specification; `Spec.from_toml`),
  and `Problem`, which takes one unit table and finds its own first appearance, reference window and calibrated classes. Methods:
  `fstar(cls, T)` (the bound and its state), `origin_tables`, `origin_set` and `lr_origin` (test inversion), `abar_truth` (the target
  for a known path), `grid`. Also `no_detection_probability`, `p0_bound` and `exact_count_crit`.
- `units_sim.py`: unit tables on the real design. Units per stage are `round(scale * n_docs)` with `n_docs` the spore effort of
  `data/occurrences/effort.csv` summed over palaeogeographic units; a fraction have ranges widened by up to three stages; true ages are
  uniform within the (true-boundary) range; clusters are runs of consecutive true age with Gamma(k, k) effects; two classes. The true
  history (`Truth`: H0c, H0m, H0, logistic, H1) fixes a(t) = 1 up to `tau0`, a class path to the origin `t0`, 0 beyond.
  The estimator sees only ranges, classes, clusters and outcomes and must find tau itself.
- `validate.py`: the harness and the two-stage acceptance rule (`stage1`, `stage2`, `pass_probability`). `uv run models/f3/validate.py`
  runs the smoke grid (6 cells, 200 replicates each, about 17 min on mac-mini with 8 workers under a load average of 10 to 17) and
  writes `out/validation_smoke.csv` (one row per cell), `out/validation_smoke_reps.csv` (one row per replicate) and
  `out/validation_smoke.meta.json` (root seed 20261030, spawn keys, settings, file hashes).
- `test_envelope.py`: 40 tests; the whole of `models/f3` is 114 tests, all passing (about 12 s).

```bash
uv run --with pytest --with numpy --with scipy python -m pytest -q models/f3
uv run models/f3/validate.py [--reps N] [--cells NAME ...] [--workers W] [--tag TAG]
```

### The construction, as implemented

- **Detection.** Unit i detects with probability 1 - exp(-r_c u_k a(t_i)); r_c = -log(1 - p_c); u_k ~ Gamma(k, rate k) is shared by
  the units of cluster k (k = inf: none). A cluster has no detection with probability (1 + Lambda_k / k)^-k, Lambda_k = sum r_i a(t_i).
- **Boundaries and ages.** Each of `age_draws` draws takes independent normal stage bases (sd `base_unc_ma`, 0 where blank), sorted;
  all units share the draw. Within a draw a unit's age is uniform in its range, and that is integrated analytically (the fractions
  Qref of the range younger than tau and Qmid inside (tau, T]), not sampled. `age_draws` therefore counts boundary draws.
- **Likelihood.** L = mean over draws of the product over clusters of the integral over u of Gamma(u) times the product over the
  cluster's units of D_i(u) (detected) or 1 - D_i(u) (not), where D_i(u) is the unit's detection probability given u, averaged over its
  age. Units are independent given u and the draw. This replaces the enumeration for small clusters and Monte Carlo for large ones
  with one route for every cluster size: a trapezoid sum in log u (48 nodes; for k = 1, 2, 5 and any total rate the absolute error is below 6e-8 and
  the relative error below 5e-4 wherever P0 exceeds 1e-6; `test_gamma_nodes_reproduce_the_closed_form_and_monte_carlo`). Enumeration is the test oracle. Reference units (a = 1) and older units
  share the integral, so a cluster spanning the first appearance is treated jointly; with finite k the reference likelihood is
  therefore not a plain binomial.
- **First appearance and windows.** tau is the older boundary (base) of the oldest stage holding a certain detection (a detected unit
  whose whole range lies in that stage; broad-range detections do not count). That stage and the `reference_stages - 1` stages
  younger than it are the reference window; units wholly inside it are reference units; units with any part older than tau are older
  units; units wholly younger than tau but outside the window are dropped. A class with fewer than `min_units_per_class` reference
  units is uncalibrated and loses its units (reported in `n_dropped_uncalibrated`). No certain detection raises `NoFirstAppearance`.
- **Histories** (origin T > tau, a(t) = 0 beyond T): H0c, a = f; H0m, constant or delayed step (a = f up to T - d, d on `delays_ma`);
  H0, any 0 <= a <= 1; logistic; H1, ceiling `h1_ceiling`.
  - **H0 bound.** For fixed age-averaged intensities m_i, P(no detection) is largest when each a(t_i) is an independent Bernoulli(m_i),
    because exp(-r x) and (1 + x/k)^-k are convex and Bernoulli(m) dominates every [0, 1] variable with mean m in the convex order. So
    P0_max(m) = prod_k E_B[(1 + sum_{i in k} r_i B_i / k)^-k], which is the u-integral with phi_i = 1 - m_i (1 - e^(-r_i u)). It is
    attained by bang-bang paths (a fine comb of 0 and 1 with duty cycle m_i). Implemented as the proportional allocation m_i = Qref_i + x Qmid_i
    (the reference part stays exact); H1 is the same with Bernoulli height `h1_ceiling`. A detected older unit takes the opposite extreme,
    the constant path (Jensen), which maximises its detection probability; each unit's bound depends only on its own mean, so the
    product bounds every path with those means. `test_convex_order_bound_dominates...` checks P0_max >= P0 over 60 random cluster draws
    for k = inf, 2 and 0.8, and equality for bang-bang atoms; `test_engine_likelihood_matches_enumeration_*` checks the whole engine
    (clusters spanning tau, a detected straddler, the bound with C = 1 and 3) against explicit enumeration to 2e-5.
  - **Logistic.** a(t) = L(t) / L(tau_s), L(t) = 1 / (1 + exp(-g ((T - t) - h))), nodes at six ages per unit; g in (0.001, 0.15, 0.5, 2) and
    h in (0, 0.5, 1, 1.5) times (T - tau). g = 0.001 is the near-constant member (the ceiling).
- **Target and bound.** abar(T) = E[sum r_i a(t_i) 1{tau < t_i <= T}] / E[sum r_i 1{tau < t_i <= T}] over draws and ages. f*_H(T) is the
  largest abar(T) over paths in H whose profile likelihood-ratio test is not rejected; the reference rates are profiled jointly (L-BFGS-B
  on log r_c). H0c, H0, logistic and H1 share one alternative, the best constant history on [0, ceiling], which belongs to each of
  them, so the test stays conservative where the H0 bound is not attained; H0m uses its exact supremum over its explicit members.
  States: `finite`, `ceiling-limited` (the class ceiling, 1 for H0, `h1_ceiling` for H1, is not rejected), `unbounded` (no ceiling:
  `H1-no-ceiling`, where the bound is trivial), `zero-exposure`.
- **Critical value** (`Problem.crit(T)`, review change of 2026-10-29). f* and the origin sets are one-sided upper limits on the older
  exposure, so the statistic is referred to `exact_count_crit(n)`, n the older detections with part of their range in (tau, T]: the value
  that reproduces the exact one-sided Poisson (Garwood) limit, 5.99 at n = 0 (P0 >= alpha) and falling towards 2.71. Chi-square(1) at 3.84,
  the as-built default, rejects whenever P0 < 0.147 in the zero-count regime where F3's data lie.
- **Origin sets.** T is excluded when the LR for "a >= f_min on (tau, T]" (maximum over f in [f_min, 1] against the maximum over f in [0, 1]
  at the same T) exceeds the critical value. H0m takes the best delay d for both: the null is "some d on the grid and f >= f_min explain the
  absences". A set is a list of runs on the 2 Myr grid from tau to the oldest possible unit age plus the longest delay, then the
  domain edge; each run end is widened to the next grid point, so a set contains the whole bracket in which its boundary lies. It is
  `unbounded` when the last point is not rejected, and `connected` is reported. A detected older unit lying wholly older than T makes
  T inadmissible (LR = inf). Each f_min read-out is a marginal statement; the whole curve is not claimed.
- **Acceptance rule.** `stage1(944) = pass`, `stage1(915) = fail`, 916 to 943 `borderline`; `stage2(1880) = pass`.
  P(pass) is 0.983, 0.57, 0.069 and 0.002 at true coverage 0.95, 0.94, 0.93 and 0.92 (`test_acceptance_operating_characteristics`).

### What was checked

- Engine against enumeration (above); the quadrature against the closed gamma-cluster result and 2e6 Monte Carlo draws; the bound
  against random paths.
- **Chi-square calibration in a regular case** (`test_profile_lr_is_calibrated_in_a_regular_case`): 100 reference units, 120 older
  units with true f = 0.5, one class, reference rate profiled jointly. Over 500 replicates the LR at the true f is within chi-square(1)
  at 0.95 +/- 0.03 (0.947, 0.937, 0.952 over three seeds of 1000 in a scratch run; mean LR 1.01 to 1.07).
- **Four states on constructed cases**, including Codex's counterexample (`test_codex_counterexample...`): one eligible unit whose age
  falls in the window with probability 0.1. Under H0 the ceiling is not rejected; under H1 it is not rejected for ceilings 3, 10 and 1000
  (f* = C grows without bound); with no ceiling the state is `unbounded`; with 40 units certain to be in the window f* is finite.
  A finite f* equals an independent scipy solution of the zero-count problem to 0.2%.
- **tau selection**: the oldest certain-detection stage, broad detections ignored, the window, outside units and uncalibrated classes, and
  `NoFirstAppearance`. **Boundary draws**: sorted, stated sd, blank stages fixed, shared by all units.
- The boundary shortcut in the f maximisation (`ell` is taken to fall from f = 0 when it falls at f = 0.02 and f = 1) against a dense scan with a detected
  older unit; and, on four replicates, equal results to the full search (the shortcut made the harness six times faster).
- Not done: an independent review of `envelope.py`; a cross-check of the profile against a different implementation of the same
  likelihood.

### Smoke results

Six cells, 200 replicates each (`out/validation_smoke.csv`), re-run on 2026-10-29 after the review changes: 989 s on mac-mini with 8 workers at a load average near 19.
- **Truth and design:** T0 = 476 Ma; tau0 = 452.8 Ma, with a = 1 at younger ages; reference detection p = (0.12, 0.04) with class weights 0.6 / 0.4; scale 0.05, giving 505 units (about 110 reference and 90 to 135 older).
- **Settings:** 60 boundary draws, 48 nodes, a 2 Myr origin grid, read-outs 1, 0.1 and 0.01.
- **Error:** the Monte Carlo error of a coverage near 0.95 is 0.015.
- **Status:** no replicate failed, and every replicate had a certain detection.

The as-built run, with χ²₁ as the default and f* coverage counted over non-trivial replicates only, is in `c7729ad`.

A replicate is **trivial** when T0 is at or below the estimated tau. Its null is vacuous, its origin set contains T0 by construction, and f* has no exposure, so it makes no claim and counts as covered. Coverage is over all replicates (`docs/f3-shape.md`: no conditioning on where the first appearance fell). Coverage over non-trivial replicates is reported beside it as a diagnostic.

The estimator measures intensity relative to its own reference window, wherever the first appearance puts it. The true target is therefore abar_rel = abar_true / a_ref, where a_ref is the true path averaged over the realised reference units.

| Cell | Non-trivial | tau (median) | a_ref | H0c f_min = 1: bounded / older end | f_min = 0.1: unbounded |
|---|---|---|---|---|---|
| H0c f = 1, k = 2 | 55/200 | 477.1 | 0.99 | 0.965 / 493.1 | 1.00 |
| H0c f = 0.3, k = 2 | 135/200 | 471.3 | 0.57 | 0.73 / 489.3 | 0.995 |
| H0c f = 0.3, k = inf | 138/200 | 471.3 | 0.56 | 0.785 / 489.4 | 0.99 |
| H0m f = 0.3, d = 6, k = 2 | 200/200 | 469.4 | 0.72 | 0.89 / 477.4 | 0.975 |
| H0 comb duty 0.3, k = 2 | 134/200 | 471.3 | 0.56 | 0.675 / 485.3 | 1.00 |
| logistic g = 0.5, h = 11.6, k = 2 | 197/200 | 469.4 | 0.90 | 0.955 / 475.4 | 0.985 |

The older-end median is over bounded sets only. At f_min = 0.01, every set is unbounded.

Coverage over all replicates, shown as estimator / χ²₁ (3.84) for comparison. The origin columns use the exact test at T0 at the largest read-out that is true of the truth. The f* columns cover the classes that contain the truth. n is given where it is not 200.

| Cell | Origin H0c | Origin H0m | f* H0c | f* H0m | f* H0 | f* logistic | f* H1 |
|---|---|---|---|---|---|---|---|
| H0c f = 1, k = 2 | 0.955 / 0.945 | 0.995 | 0.955 / 0.945 | 0.955 / 0.945 | 0.955 / 0.945 | - | 0.96 / 0.95 |
| H0c f = 0.3, k = 2 | 1.00 | 1.00 | 0.985 / 0.935 | 0.985 / 0.95 | 0.99 / 0.95 | - | 0.99 / 0.985 |
| H0c f = 0.3, k = inf | 1.00 | 1.00 | 0.97 / 0.91 | 0.975 / 0.915 | 0.975 / 0.91 | - | 0.98 / 0.935 |
| H0m f = 0.3, d = 6, k = 2 | none true | 1.00 | - | 0.965 / 0.94 | 0.965 / 0.95 | - | 0.985 / 0.98 |
| H0 comb 0.3, k = 2 | 1.00 (n 66) | 1.00 (n 163) | - | - | 0.97 / 0.935 | - | 0.98 / 0.95 |
| logistic, k = 2 | 1.00 (n 3) | 1.00 | - | - | 0.94 / 0.92 | 0.93 / - | 0.95 / 0.94 |

**What the smoke run shows.**

1. **The count-matched critical value restores nominal coverage.**
   - **Count-matched value:** f* coverage over all replicates is 0.93 to 0.99.
   - **χ²₁ at 3.84:** 0.91 to 0.95, and below 0.93 in two cells.
   - **The as-built run** showed the cause. In the zero-count regime the statistic is -2 log P0, and 3.84 rejects whenever P0 < 0.147.
   - **Lowest values:** the logistic cell gives 0.94 for H0 and 0.93 for the logistic class. The logistic grid contains the truth only approximately, because h is a fraction of T - tau and the normalisation uses the estimated tau. The full grid must watch this cell.
2. **Coverage concentrates where it can fail.** In the stationary cell (f = 1, the null at its boundary), coverage over the 55 non-trivial replicates is 0.84, against 0.955 overall. The test's size is spent on the few replicates in which the first appearance falls below the origin. This is the relevant-subset behaviour of any test whose rejection needs an observed gap; it is reported, not accepted against.
3. **The reference window is not at a = 1 when the history is below 1 for some stages after tau0.** The first appearance falls inside that era, and a_ref is 0.56 to 0.72 for f = 0.3, the comb and the delayed step. f* reads relative to the window: "f* = 0.5" means 0.5 of whatever intensity the window holds.
4. **Informativeness is low at this scale (505 units).**
   - The f_min = 1 set is bounded in 67 to 97% of replicates, and its older end lies 6 to 18 Myr beyond the median tau.
   - Sets at f_min = 0.1 and 0.01 are unbounded in 97.5 to 100% of replicates.
   - Among non-trivial replicates, 16 to 55% give a finite f* under H0, and 59 to 90% under H1. H1 is finite more often because a ceiling of 3 is rejected at lower exposure, and its state says so.
5. **H0m origin sets end the longest delay (10 Myr) beyond H0c's when no older unit detects** (10 to 12 Myr on the 2 Myr grid). They end sooner in 8 of about 800 bounded pairs, where older detections favour a delayed step as the alternative. H0m informs the origin only through its declared delay bound.

### Open choices

- **Scale 0.05 of the Palynodata document counts** (505 units). Documents are counted in every stage they overlap, so a table of unique
  blocks will be smaller than `n_docs`; 0.05 gives about 110 reference and 100 older units and 0.5 to 11 s per replicate. The scale of the real table is unknown. It sets the power,
  not the construction.
- **Grids**: origin step 2 Myr (the full run should use 0.5 or 1 and `age_draws` 400); H0m delays (0, 2, 6, 10) Myr; logistic g and h
  grids above; 60 boundary draws and 48 nodes in the harness; 400 draws and 48 nodes in `Spec` and the draft specification. The 48 nodes
  need 64 for k < 1.
- **Design**: classes p = (0.12, 0.04), weights 0.6 / 0.4; 12% broad-range units; clusters of mean size 3; T0 = 476 and tau0 = 452.8 chosen
  so that the first appearance falls below the origin often enough (T0 at 466 gave 81% trivial replicates under f = 1).
- **Boundary draws** (checked 2026-10-29, `out/validation_draws60*` and `out/validation_draws400*`). Cell H0c f = 0.3, k = 2 was run for 100 paired replicates on the same simulated data, at 60 and at 400 boundary draws.
  - f* changed by at most 0.006 for H0c and H0. One H1 value moved by 0.15; the median change was 0.
  - Coverage verdicts agreed in 100 of 100 replicates, and states in 99 of 100.
  - Origin endpoints moved by at most one grid step.
  - 400 draws cost seven times as much: 36 s against 5.3 s per replicate.
  - So the validation grid can run at 60 draws. Real-data runs keep 400.
- **Critical value**: `exact_count_crit`; the harness also records f* under chi-square(1) (`_chi2` columns) and stores the origin
  statistic `lr0`, so 3.84, 2.71 and 5.99 can be applied afterwards.
- **Boundary shortcut and tolerances**: L-BFGS-B `ftol` 1e-10, f searched to 5e-3, f* root to 1e-4; `fcover` tolerance 1e-3.

### Limits

- Cells are correctly specified; no misassigned classes, reporting or facies differences, regional confinement or H1 truths. The H1 and
  logistic truths are not run beyond one cell each.
- H0 and H1 use the proportional duty allocation, which is the worst case only when stages alike in class mix. For two classes of p = 0.30
  and 0.03 in separate stages of 100 units, the best allocation differs by at most 0.06 in log P0, so f* is understated by a few per cent.
  H1 is "any path up to `h1_ceiling`": the bound holds for pulses of any duration, so the specification no longer carries one.
- The logistic members are on a grid and their normalisation is at the estimated tau, so a true logistic with tau0 different from the estimated tau is not exactly a member.
- `Spec.from_toml` requires every inference field; the draft specification declares the `Spec` defaults (`test_draft_specification_sets_every_inference_field`).
