# Independent mathematical and numerical check of C55 and C57

Codex, 13 November 2026. Source state: `75f2bb02b54e8d66cee0476d1f5a309d36a69c6e`.
This check owns this audit only. It did not change the ledger, analysis code, canonical outputs or
manuscript; regenerate outputs; rerun the historical qualification; post to the Board; or inspect
`docs/outreach`. Temporary independent calculations were run under `/tmp`.

## Verdict

- **C55: supported within its declared scope.** The count curve, real-valued crossing, integer-count
  examples and zero-delay ratios are correct. The three reviewed treatments have the asserted common
  oldest age and cutoff. A continuous effective-count curve is a sensitivity, not a fitted dependence
  model or a confidence procedure for fractional counts.
- **C57: mathematical and numerical content passes; retain provisional until the prose repairs below.**
  Every tabulated number checked agrees with independent calculations. A wording-only repair suffices:
  distinguish finite-age exponential thresholds from the exact unlimited-age condition, and restrict
  the integral statement to the assumed later plateau and the earlier part of the history. Neither
  numerical regeneration nor a new qualification run is needed for those repairs.

Read: `AGENTS.md`, `manuscript/estimands.md`, the two ledger entries, relevant charter/plan material,
`docs/plan-rulers.md`, `count_dial.py`, `rise_shapes.py`, `endpoint.py`, the relevant reviewed-bound and
frontier rows, all count/rise output rows, the spore effort and occurrence tables and timescale,
Methods (e–g), Results (d–f), the relevant Discussion, S5.2 and S5.9. The prior 12 November audit
receipts were leads only; the derivation and numerical checks below were performed independently.

## Derivation and numerical results

Write ages increasing into the past. Let `A = 426.7`, `c = 393.47`, `B = A-c = 33.23` Myr and
`alpha = 0.05`. Conditional on an integer count of independent occurrences, a fixed relative history
`w` has cumulative exposure `U(a) = integral[c,a] w(s) ds`, and

\[
P(M\le A\mid n,T,w)=\{U(A)/U(T)\}^n.
\]

This follows by taking the product of the individual cumulative probabilities, without using the
implementation. Inverting the lower tail gives `U(T) = U(A) alpha^(-1/n)`, exactly as
`endpoint.known_cutoff_summary` implements.

### Count curve (C55)

For constant recording,

\[
T(n)=c+B\alpha^{-1/n}=A+K(n),\qquad
K(n)=B(\alpha^{-1/n}-1).
\]

`T(n)` decreases strictly with positive `n`. Solving `T(n) = 431.2` gives

\[
n_* = \frac{-\log\alpha}{\log[(431.2-c)/B]}=23.587987756016.
\]

Thus an integer count of 23 permits 431.2 Ma, whereas 24 puts that age outside the constant-history
older bound. The fractional crossing locates a plotted curve, rather than an observed count.

| Independent count | Constant older bound (Ma) | Later/earlier at 444 Ma | At 452 Ma |
|---:|---:|---:|---:|
| 15 | 434.045667621245 | 2.355129702570 | 3.444207021677 |
| 19 | 432.375016533008 | 3.048449268716 | 4.458136791822 |
| 23 | 431.322700003716 | 3.742401623747 | 5.472991969988 |
| 24 | 431.117827890538 | 3.915951555527 | 5.726796205481 |
| 30 | 430.189605595022 | 4.957580313568 | 7.250103001924 |
| 40 | 429.284268992471 | 6.694349562836 | 9.790002539869 |
| 48 | 428.840005948580 | 8.084089678106 | 11.822397043705 |

The step frontier follows independently from setting the earlier relative rate to `r`:
`r(t-A) = K`, hence later/earlier `= (t-A)/K`, for zero delay and `t>A`. It is a compatibility contour;
its algebra does not estimate the historical rate.

`reviewed_bounds.csv` rows 74, 446 and 470 confirm common `A`, `c`, flat history and counts 48, 19 and
15. All three bounds and their six 444/452-Ma ratios agree with the reviewed outputs to stored
precision. Independent 65-digit Decimal arithmetic checked all 153 ordinary numeric cells of
`count_dial.csv` against the formulas: maximum difference `0.0000498573`, within four-decimal rounding.
The special crossing row agrees with `n_*` and the boundary ratios.

### Linear and exponential rises (C57)

With rate 1 on `[c,A]` and non-negative relative rate `r(s)` before `A`, let
`R(t) = integral[A,t] r(s) ds`. Then

\[
P(M\le A\mid n,t,r)=\left\{\frac{B}{B+R(t)}\right\}^n\ge\alpha
\quad\Longleftrightarrow\quad R(t)\le K(n).
\]

A candidate-specific straight line from zero at `t` to 1 at `A` has triangular area `(t-A)/2`.
Its compatibility boundary is therefore `t = A+2K`. This compares a family of ramps indexed by
their proposed start, rather than asserting that endpoint inversion of one fixed ramp, with zero
rate beyond its start, yields the same finite boundary.

For `r(s) = exp[-(s-A)/tau]`, with `L=t-A>0`,

\[
R(t)=\tau(1-e^{-L/\tau}),\qquad D=\tau\log 2.
\]

For a finite candidate with `L>K`, `R` increases strictly from zero to `L` as `tau` increases, so
there is a unique maximum compatible `tau`, strictly larger than `K`. If `L<=K`, even the constant-rate
limit fits and no finite upper restriction on `tau` is required. All scripted candidates have `L>K`.
As `t` tends to infinity, `R` tends to `tau`; hence **every finite older start fits if and only if
`tau<=K`, or equivalently `D<=K log 2`**. If `tau>K`, the finite endpoint is

\[
t_{\max}=A-\tau\log(1-K/\tau).
\]

| n | K (Myr) | Linear boundary (Ma) | D at 444 Ma | D at 452 Ma | D at 500 Ma | Unlimited-age threshold D |
|---:|---:|---:|---:|---:|---:|---:|
| 48 | 2.140005949 | 430.980011897 | 1.483797849 | 1.483349976 | 1.483339090 | 1.483339090 |
| 24 | 4.417827891 | 435.535655781 | 3.130088357 | 3.072405408 | 3.062205137 | 3.062204947 |
| 19 | 5.675016533 | 438.050033066 | 4.168368632 | 3.982338567 | 3.933631378 | 3.933621709 |
| 15 | 7.345667621 | 441.391335242 | 5.841547925 | 5.282680477 | 5.091865064 | 5.091628801 |

Independent Decimal integration formulas and bisection checked all 24 numeric cells of
`rise_shapes.csv`; maximum discrepancy was `0.0000499760`, within four-decimal rounding.
Separate calls to the native `known_cutoff_summary`, using independently constructed piecewise
histories, confirmed all four constant-history bounds and all eight exponential endpoints at 444
and 452 Ma. Maximum exponential endpoint error was `0.010413` Ma (48 finds, 452 Ma), within the
script's declared `0.05` Ma tolerance. S5.9 now describes that numerical scope correctly: linear and
exponential exposure checks, exponential endpoint inversion at 444/452, analytic unlimited-age proof.

The numerical histories stop at 700 Ma; a `beyond_domain` result there alone cannot prove an
unlimited-age statement. The closed-form limit above does prove it for the stated exponential
family. This extrapolation is distinct from the 469.4 Ma domain of the six held histories in S5.2.

### Spore reporting shares

The numerator can be independently recovered as distinct `record_id` values in
`data/spores/occurrences.csv`, restricted to `source=palynodata`, `usable=true`, non-rejected vetting,
`spore_class` starting with `trilete`, and age-support overlap with each stage. This gives 5, 43, 67
and 89 documents for Hirnantian, Rhuddanian, Homerian and Gorstian, respectively, matching the effort
table. The denominator values below are the held effort-table counts; the underlying Palynodata
denominator extraction was read in `tools/spores.py`, not regenerated or re-audited end to end.

| Stage pair | Older share | Younger share | Midpoint gap (Myr) | Equivalent doubling time (Myr) |
|---|---:|---:|---:|---:|
| Hirnantian–Rhuddanian | 5/307 = 0.016286644951 | 43/482 = 0.089211618257 | 2.35 | 0.957798903860 |
| Homerian–Gorstian | 67/492 = 0.136178861789 | 89/486 = 0.183127572016 | 2.80 | 6.552064165370 |

The calculation is `D = midpoint_gap * log(2)/log(younger_share/older_share)`, using ICS stage
midpoints from `data/timescale.csv`. These reproduce both rows of `rise_spore_share.csv`. Checking all
positive adjacent-stage share increases in `effort_global_by_stage.csv` also confirms the
Hirnantian–Rhuddanian pair has the shortest equivalent doubling time; it is not evidence for a
sustained exponential process.

Homerian and Gorstian midpoints are 428.65 and 425.85 Ma; their comparison spans `A=426.7`. Assigning
the Gorstian level to `A` would instead give `4.563044687` Myr. S5.9 correctly warns that the 6.55 Myr
comparison does not test a rise confined to before `A`. Neither share measures crown vascular-plant
finding rate, and the older 0.96 Myr episode does not establish the required rise near `A`.

## Interpretation and repairs

1. **Separate a finite-age fit from the unlimited-age threshold.** Main Results (f), lines 269–271,
   follows the finite-500-Ma values with “a rise this fast leaves no finite older limit”. Every exact
   finite-500 boundary has `tau>K` and therefore a finite endpoint at 500 Ma by construction. Its
   doubling-time excess over the asymptotic threshold is approximately `1.98e-15`, `1.91e-7`,
   `9.67e-6` and `0.000236263` Myr for n=48/24/19/15. Moreover, an exact 1.5 Myr doubling with 48 finds
   gives a finite endpoint at **436.438527 Ma**, and 5.1 Myr with 15 finds gives **473.879321 Ma**;
   3.9 Myr with 19 finds is below its threshold and genuinely has no finite endpoint. Abstract lines
   15–16 and Discussion lines 309–311 also attach categorical unlimited-age language to rounded
   thresholds. Give the exact criterion `D<=K log 2` before describing its approximate values. In
   Results, distinguish the 500-Ma examples from the asymptotic thresholds explicitly. Rounding the
   existing table is fine; rounding alone cannot carry an exact inequality at this transition.
2. **Say what the integral statement constrains.** Results lines 262–265 and Discussion lines 308–309
   should identify the earlier history under the stipulated later plateau, rather than imply the
   fossil record contains no shape information. Equal `R(t)` gives the same maximum-age probability.
   Because every candidate history is also 1 at every observed age, it gives the same full exact-age
   likelihood conditional on n: the observed-age numerator is common and the denominator is
   `(B+R)^n`. Their conditional-on-maximum within-record shape diagnostics are likewise identical to
   the flat-history diagnostic. The latter can challenge the shared later plateau but cannot
   distinguish the unobserved earlier shapes. This is a conditional indistinguishability result,
   not an estimate of the true earlier integral or a general non-identifiability result for all
   finding histories.
3. **Keep retrospective compatibility separate from confidence and origin.** The flat count curve
   retains the fixed-history conditional confidence interpretation for an actual independent
   integer count, with the stated age-support conditions. The rises are anchored at the observed
   oldest possible age and the plateau covers all observed ages by construction. This is not a
   numerical circularity: it honestly describes what specially chosen histories permit. It gives
   no independent evidence that a plateau, step, or exponential rise occurred and no demonstrated
   nominal 95% coverage for this data-dependent family. Methods (g), the C57 ledger qualification
   and S5.9 already acknowledge this. “Any older ancestor” is allowable only as a zero-delay,
   category-to-ancestor compatibility statement under the declared link; it is not an inferred
   lineage origin, a probability over origins, or rejection of the younger maximum.

After these wording repairs, both claims can be supported as explicitly bounded algebraic and
numerical results. No new scientific assumption, additional data or expensive computation is needed.

## Acceptance read of the integrated revision (13 November 2026)

Read the parent's uncommitted C55/C57 ledger changes, Methods (g), Results (d–f), first Discussion
paragraph, S5.9 and new estimands section. The previously substantive issues are resolved: the
unlimited-age assertion uses the exact count-specific `K ln 2` condition; S5.9 states the finite
endpoint for `tau>K`; the earlier-integral equivalence is conditional on the common later plateau;
the later-age diagnostic is retained; and the retrospective family is not given confidence or
historical-rate status. C55 also now distinguishes integer counting assumptions from the
real-valued crossing. **I accept promotion of both bounded claims to supported.** No new
calculations were required for this read.

Two small prose refinements remain advisable: make the Results (f) heading exponential-specific
(the linear family yields an age boundary, not a constant doubling-time requirement), and add
“about” to the rounded 1.5-Myr finite-age requirement. Neither changes the verified equations,
tables or substantive interpretation of the revised body text.
