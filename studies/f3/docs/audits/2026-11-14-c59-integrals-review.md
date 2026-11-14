# C59: independent combined-proxy integral and correlation check

Codex, 14 November 2026. Bounded independent review of the combined-proxy evidence at
`1a399f6`. The parent owns interpretation and integration; another reviewer checks
the late-Silurian placement counts and binomial test. No production function was
imported, and no numerical output, model, manuscript or ledger was changed here.

## Derivation

Let finding intensity be `lambda*x(s)` and write `I_later` and `I_early` for the
integrals of the specified non-negative proxy over `[c,A]` and `[A,t]`. Conditional
on `n` independent finds over `[c,t]`, the probability that all are in the later
window is

`(I_later/(I_later+I_early))^n`.

With `Q=mean_later(x)/mean_early(x)`, the early expectation calculated at the scale
estimated from the later count is

`E=n*I_early/I_later = n*(t-A)/((A-c)*Q)`.

Thus the probability is `(1+E/n)^(-n)` and the 0.05 boundary is
`E=n*(0.05^(-1/n)-1)`. This uses the integrated later intensity; it does **not**
require a level later rate. As in C58, `E` is not the conditional binomial mean
given total count `n`; that mean would be `E/(1+E/n)`.

For finding proportional to the pointwise product `x(s)=rock(s)*spores(s)`, the
appropriate `Q` is the ratio of the two window means of that product. The product
of the two single-proxy ratios is generally different. It can be used as a
separate assumed contrast between mean finding rates, but its probability column
does not then describe the same pointwise-product history. Multiplication of
proxy functions itself requires no statistical independence; interpreting the
factors as distinct causal components does require an additional argument.

## Independent numerical route

An ad hoc Python implementation read the primary reviewed B2 row for
`A=426.7`, `c=393.47`, the raw Macrostrat unit table, stage document counts, the
timescale and the reviewed collection-density table. It used rational arithmetic
and exact partitioning at every stage, rock-unit and density boundary, rather
than the production scripts' 0.01-Myr midpoint quadrature.

Inputs:

- `data/eprp/record/macrostrat_units_window.csv`: active North American columns,
  `d_env_class=non-marine`; 54 unit rows and 36 distinct columns. At any age each
  active column's area is counted once, even when units overlap.
- `data/spores/effort_global_by_stage.csv`: the exact integer ratio
  `n_docs_with_triletes/n_docs`, assigned by `data/timescale.csv`.
- `studies/f3/data/macro/effort_reviewed.csv`: global all-collection and
  plant-excluded densities, integrated exactly within their declared stage bins.
- `studies/f3/models/loop3/out/reviewed_bounds.csv`: the declared B2/main,
  locality-age, primary, Emsian-cutoff, flat-history row.

All 48 rows of `combined_rulers.csv` were checked for the single ratios, combined
ratio, expected count, count-specific threshold, no-early-find probability and
verdict. **Every verdict agrees.** Main values from exact integration are:

| Combination | Ancestor (Ma) | Ratio of product means | Product of single ratios | Expected early finds at n=48, pointwise product | Expected early finds at n=48, multiplied ratios |
|---|---:|---:|---:|---:|---:|
| Rock × spore share | 444 | 21.668070 | 16.931202 | 1.153285 | 1.475942 |
| Rock × spore share | 452 | 29.757330 | 22.655354 | 1.228111 | 1.613097 |
| Searching × spore share | 444 | 6.452961 | 6.953928 | 3.872558 | 3.593576 |
| Searching × spore share | 452 | 8.994708 | 10.048570 | 4.062977 | 3.636865 |
| Plant-excluded searching × spore share | 444 | 4.921525 | 5.492388 | 5.077586 | 4.549836 |
| Plant-excluded searching × spore share | 452 | 6.862743 | 7.960846 | 5.325173 | 4.590629 |

The rock-product ratios differ from the saved midpoint values by about 0.011%
or less in the main 444/452 Ma cases. Searching-product differences are below
the saved precision apart from rounding. Rock-product mean expectations are
below the threshold for all four counts; both searching variants exceed it at
48 finds and fall below it at 24 or fewer.

All 255 rows of `combined_rulers_curve.csv` were integrated independently.
The largest relative difference in a finite combined ratio is 0.0635%, at
439.5 Ma for rock × spore share. Small displayed expected counts have larger
relative rounding errors; **no count-specific boundary classification changes**.
Infinite ratios correctly correspond to zero early integral and zero expected
early finds in the declared proxy model.

The ratio of product means divided by the product of single ratios is 1.27977
at 444 Ma and 1.31348 at 452 Ma for rock × spore share. This is the ratio of
the normalized within-window cross-moments, which explains why multiplying
window means and averaging the product are different operations.

## Stage correlations and their interpretation

Exact integration of all 13 stage means preserves the saved ranks. The largest
relative difference in a rock stage mean is 0.0398% (Telychian), reflecting
midpoint quadrature. Independent rank calculations give:

| Pair | Spearman rho |
|---|---:|
| Rock–spore share | 0.3038720411 |
| Rock–searching | −0.0939240854 |
| Searching–spore share | 0.5219780220 |
| Rock–plant-excluded searching | −0.0165748386 |

A separate NumPy permutation implementation, with an independent seed and one
million permutations per comparison, gives probabilities 0.31310, 0.76336,
0.07092 and 0.96339 respectively. These agree with the stored 200,000-shuffle
results within Monte Carlo variation. Their independent Monte Carlo standard
errors are about 0.00046, 0.00043, 0.00026 and 0.00019.

These permutation probabilities describe a null in which stage labels are
exchangeable. Consecutive geological stages and temporally structured series
are not exchangeable by design. The probabilities therefore should not be
presented as an unrestricted probability of the observed chronological
association arising by chance. In particular, neither a weak correlation nor
non-rejection demonstrates independent mechanisms or validates multiplication.
The correlation can remain a descriptive check, with this limitation stated.

## Disposition

The numerical combination is correct and the saved approximation is adequate
for every reported decision. Two interpretive distinctions should remain
explicit in the ledger/estimands and applicable prose:

1. The pointwise-product history and the multiplied-mean-ratio contrast are
   different assumptions. Only the former has the stated stage-by-stage
   proportionality interpretation.
2. The stage permutation probabilities require exchangeability and do not
   identify independent causal contributions. Prefer descriptive wording to
   the unqualified phrase “within the range chance gives”.

Keeping searching outside the rock product is a sensible choice: a collection
density already reflects where collectable rock and searching coincide, so
multiplying it by rock area risks counting availability twice. That is a
modelling rationale, rather than an empirically established decomposition of
the collection process. Searching × spore share is a useful alternative
contrast, with the same transfer limitations.

North American column area, global spore-reporting share and a global fossil
inventory have different geographical and observational scopes. Neither the
arithmetic nor the stage correlations establish proportional transfer to
body-fossil finding. Whether the detailed product history fits later finds is
separately assessed by the placement review. No new substantive analysis or
change to the scientific outputs is required by this integral check.
