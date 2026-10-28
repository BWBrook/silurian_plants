# F3 sketch: dating origination from an incomplete record

Loop 1, step 2 of `docs/plan-f3.md`. A virtual palaeontology (a clade of growing abundance that leaves
stage-dated fossil occurrences) and the classical estimators of the first appearance, checked against
known truths. Step 3 (the recovery study) builds on it. Written by Claude Sonnet 5.5
(`claude-sonnet-5-5`), 2026-10-28.

## Files

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

## Conventions

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
  points. Stage bases are taken as exact (the boundary uncertainty of primer section 1.2 is left for step 3).
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

## What the grid shows

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

## Left for step 3

- Effort that varies by stage (the real effort history) and preservation that depends on facies and gaps. The
  simulator takes any per-stage effort, but the grid uses constant effort.
- Joint stage-boundary age uncertainty (primer section 1.2): the boundary ages are fixed here.
- Lineage-level birth-death with a trait (spore type), extinction of the clade before the window end,
  and records dated by biozone or radiometric ages rather than stages.
- Estimators that model N(t) and preservation (the classical bound and GRIWM both assume sampling that
  does not change through the range), PyRate, `tbea` and StratPal cross-checks, Marshall (1994, 1997) and
  Strauss & Sadler's two-endpoint case.
- Identifiability (old origin with poor preservation against young origin with good preservation), the
  acceptance criteria fixed before the run (coverage of at least 90%, median bias under 2 Myr), and ensembles
  on `deep-server`.
