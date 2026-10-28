# GRIWM and CRIWM, with the arrival branch fixed (local copy)

These are patched copies of `Rextinct/R/griwm.R` and `Rextinct/R/criwm.R` from [github.com/cjabradshaw/CRIWM](https://github.com/cjabradshaw/CRIWM), taken at commit `8eb6f51` (MIT licence, `LICENSE`). They implement the estimators of Bradshaw et al. (2012, doi:10.1016/j.quascirev.2011.11.021) and Saltré et al. (2015, doi:10.1016/j.quascirev.2015.01.022). The functions themselves were written by Salvador Herrando-Pérez.

We fixed them locally on 2026-10-28, at Barry's request, so the project can use the arrival option (`signor_lipps = "arr"`). Barry will tell the authors. `rextinct_arrival_fix.patch` is the change, four lines in each file, ready to forward. The line endings in our copies are LF; upstream's are CRLF.

## The fault

The inner loop (`griwm.R` line 361, `criwm.R` line 408 upstream) maps each series of dates onto time measured forward from its oldest member:

```r
date.mci.it <- rev(max(date.it) + 1 - date.it)
```

That is correct for extinction, where `date.samp` is sorted youngest first. For arrival, `date.samp` is sorted oldest first, so the oldest date maps to 1 and `t.n`, the last element after `rev`, is 1 for every series. The estimate then becomes `max(date.it) + log(alpha) / n`. That lies a fraction of a year *younger* than the oldest record, instead of extending beyond it.

For example, take ages 100, 90 and 60, with alpha = 1/e:
- upstream returns 99.53, rounded to 100;
- the correct arrival estimate is 107.13.

## The fix

For arrival, measure each series backwards from its youngest member, and convert back from there:

```r
if (signor_lipps == "arr") {date.mci.it <- rev(date.it - min(date.it) + 1)}
...
if (signor_lipps == "arr") {T.mci.lst.vec[i_griwm] <- min(date.it) - 1 + i}
```

This is the extinction algorithm on a mirrored time axis. Bradshaw et al. (2012) say the method "could also be applied reciprocally"; that quotation was read by the sketch agent and is recorded in `models/f3/README.md`. The extinction branch is unchanged.

## Checks

```bash
Rscript models/griwm_r/test_arrival_fix.R path/to/upstream/griwm.R
```

Needs `data.table`. The dates are given zero error, so the resampling is deterministic. The script checks:

- **Toy series.** For both functions on 100, 90, 60, arrival gives 107 and extinction gives 45, matching hand calculation (107.13 and 45.29).
- **Random series.** On five random series of 4–12 dates, arrival matches a by-hand implementation of the estimator to within rounding, and is always older than the oldest record.
- **The fault itself.** Given the path to the unpatched upstream file, it confirms that the upstream arrival branch returns 100 on the toy series.

All checks passed on 2026-10-28 (R 4.6.1). The project's Python implementation (`models/f3/estimators.py`, `weighted_mcinerny` with `unit = 1`) gives 107.133 on the same toy series.
