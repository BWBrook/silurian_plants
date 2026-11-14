# C58: independent mathematical and numerical check

Codex, 14 November 2026. Bounded audit of `rule_of_three.py` and its saved table at
`afa1d2d`, without importing or executing the script under review. The parent reviewer
owns the ledger, manuscript, source checks and integration. No scientific output was
changed in this audit.

## Derivation and interpretation

Let the rate be `lambda` times a relative history, with that history equal to one
over the later interval `[c,A]`. Write `L=A-c` and let `R` be its integral over
the earlier interval `[A,t]`. Conditional on a total of `n` independent finds
over `[c,t]`, the probability of no find in `[A,t]` is

`(L/(L+R))^n = (1-p)^n`, where `p=R/(L+R)`.

Setting this probability to `alpha` gives

`R=K=L*(alpha^(-1/n)-1)`.

Translating this early exposure into finds at the fitted later rate `n/L`
gives

`m*=n*(alpha^(-1/n)-1)`.

The finite-count expression is correct and tends to `-ln(alpha)`, which is
2.99573227355 at `alpha=0.05`. The usual binomial zero-count upper limit is
`p*=1-alpha^(1/n)`; the translation here is `m*=n*p*/(1-p*)`, not `n*p*`.
Thus `m*` is an expected number under the later-rate estimate, rather than
the expected early count conditional on the fixed total `n`. The latter is
`n*p*`: 2.90416364875 at `n=48`, versus `m*=3.09119125886`; and
2.71554408783 at `n=15`, versus `m*=3.31582950101`. The manuscript's explicit later-rate
qualification is scientifically necessary; a bare claim that a conditional
binomial count has expectation `m*` would be wrong.

| Independent finds | K (Myr) | m* at fitted later rate | Exact asymptotic exponential doubling threshold (Myr) |
|---|---:|---:|---:|
| 48 | 2.14000594858 | 3.09119125886 | 1.48333908964 |
| 24 | 4.41782789054 | 3.19072733593 | 3.06220494653 |
| 19 | 5.67501653301 | 3.24481836073 | 3.93362170949 |
| 15 | 7.34566762125 | 3.31582950101 | 5.09162880100 |

For a fixed history and exact ages this is the endpoint confidence calculation
expressed on a different scale. The equivalence of early histories concerns
the oldest-find event with the same later plateau. It does not certify their
biological mechanism, fit all aspects of the fossil record, estimate the
number of independent finds, or calibrate a history selected after examining
the record. It does not apply to the Libyan spore model or to histories whose
later rate is not level.

## Independent numerical route

An ad hoc Python calculation used `decimal.Decimal` at 70 digits, reading
`A=426.70000000`, `c=393.47000000` and `alpha=0.05000000` from the primary B2
row in `reviewed_bounds.csv`. No function from the analysis scripts was
imported. All 32 rows of `rule_of_three.csv` were assessed.

- Steady endpoints were computed as `A+K`; the saved primary, region-stage
  and curated endpoint rows agree within 3.1e-9 Myr.
- Linear endpoints were computed from their triangular early exposure:
  `t=A+2*K`.
- Exponential asymptotic thresholds were computed as `K*ln(2)`. At equality
  the integral over the entire infinite early tail is `K`. Every finite
  candidate age then has an integral below `K`; it approaches the boundary
  only as the age tends to infinity. The rounded saved thresholds are all
  slightly below the exact threshold, so remain compatible with every finite
  age. They are not finite-age boundary histories.
- For completeness, all 12 finite exponential doubling thresholds in
  `rise_shapes.csv` were independently solved at 60-digit precision using
  `tau*(1-exp(-(t-A)/tau))=K` and multiplied by `ln(2)`. All agree at the
  saved four-decimal precision. These finite candidate columns are distinct
  from the asymptotic threshold.
- Step ratios were computed as `(t-A)/K`, the crossing count as
  `ln(20)/ln((431.2-c)/L)`, and minimum delays as `t-A-K`.
- For a proxy ratio `q`, the expected earlier count is
  `48*(t-A)/(L*q)`. The algebraic count at which that proxy would put the
  candidate at the boundary is `ln(20)/ln(1+(t-A)/(L*q))`.

| Proxy and candidate | Expected earlier finds at the fitted 48-find later rate | Algebraic matching count from the saved proxy ratio |
|---|---:|---:|
| North American non-marine column area, 444 Ma | 7.58612894229 | 20.41625817975 |
| North American non-marine column area, 452 Ma | 11.46015566504 | 13.99185601496 |
| Trilete-reporting share, 444 Ma | 4.86148033165 | 31.05225549786 |
| Trilete-reporting share, 452 Ma | 5.14367414042 | 29.42818403379 |

Every value cell agrees at its source precision: four decimal places except
matching counts, imported after rounding to two decimals. Every expected-count
and limit-count cell agrees at four decimal places when recomputed from the
same saved input values. Matching counts give small boundary residuals
because they were rounded first; the largest relative residual in the saved
table is approximately 0.000208, for rock at 444 Ma and `n=20.42`. That is
well below the script's relative tolerance of 0.002. The arithmetic supports
the reported 7.6–11.5 rock and 4.9–5.1 spore examples.

These proxy examples require an untested proportional transfer from each
proxy to body-fossil finding rates over both windows. They are expected counts
under that assumption, rather than inferred missing fossils. Real-valued
matching counts are algebraic interpolations, rather than fitted or
calibrated effective sample sizes.

## Read for meaning

The Abstract, Results (d)–(g), Discussion's Conditions and Conclusion have
been read against this derivation. The stated later-rate qualification
keeps their expected-count language valid; the scopes of the proxy examples
and the fixed-history confidence statement are preserved. The asymptotic
thresholds in Results (f) are rounded down sufficiently to make the unlimited
age statement safe, and its finite-candidate examples remain approximate
requirements. Apart from making the exact odds transformation explicit in
Methods (g), no numerical or scientific prose correction is required by this
mathematical check. Calling the approximate rule a new finding or equating
its expected counts with actual missing fossils would go beyond this result;
the present text does neither.

## Script coverage and disposition

The calculations are correct, but the script's verification description is
broader than its assertions at `afa1d2d`:

- Steady endpoints and delays are constructed from hard-coded `A`, `c` and
  `alpha`, rather than compared with their saved `reviewed_bounds.csv` and
  C33 delay evidence. The script would not notice a change in those source
  results.
- Only the four asymptotic exponential thresholds are checked. The 12
  finite-age columns in `rise_shapes.csv` are not checked by this script,
  although this independent audit confirms them.
- Four proxy-scaled 48-find expectations intentionally exceed `m*`; only
  their matching-count rows sit approximately on the boundary. Calling
  every output a boundary case would be false.

Before supporting C58, either narrow its basis and script description to the
actual selected checks, or bind the relevant saved endpoints and delay rows
and add the finite exponential checks. Describe asymptotic exponential rows
as a limiting boundary, and the proxy-scaled 48-find rows as comparisons
against it. This is a verification-description repair, not a correction to
the numerical results or a request for new scientific analyses.
