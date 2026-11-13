# Sprint 1 statistical counter-review

Audit began against repository commit `f08afb4`. Read-only repository audit;
all new numerical work is in this scratch directory. The implementation agent
subsequently started the receipt repair while this audit ran; the calculations
below do not depend on that receipt machinery. No ensemble was run.

## Required qualification-scope repair

`qualify.members()` assigns H0c by the generating cell label, but the analysis
reselects the first appearance. In the saved QB-CO/rho1 acceptance output,
Q2 replicates 349, 355, 1003 and 1464 and Q3 replicates 159, 678 and 1083 have
analysis tau=445.2 Ma, younger than the generating tau0=452.8 Ma. Their path is
1 on (445.2,452.8] and 0.3 (Q2) or 0.1 (Q3) farther back. These are not constant
histories on the analysis interval. The existing H0c membership assertion is
wrong for these seven records; Q3/159 was counted as a miss, the other six as
covers. This is not evidence of a primary Murzuq numerical failure.

Recommended bounded disposition: QB qualification covers H0m, H0 and H1;
retain H0c read-outs as explicitly unqualified sensitivity calculations. Keep
all four classes for the Libyan designs. Do not convert out-of-class rows to
successful covers or suppress them silently. A future general qualifier must
check the history class after its data-dependent reference change.

All nontrivial saved acceptance paths across all 14 primary design/rho cases
remain within their declared H0/H1 normalised ceilings. The QB monotone cells
remain monotone after either direction of tau shift. Nontrivial QB hiding-path
cases keep reference intensity approximately 1. These checks are finite-grid
evidence, not a theorem for future source designs or histories.

## Reference normalisation and required quantities

The reference intensity changes materially in simulated records: e.g. MZ/rho1
Q3 has a_ref=0.78961 in 119/1000 records; B1 has a_ref=0.77978 in 207/1000.
`_analyse()` divides the f* target by a_ref, whereas origin/window applicability
uses a_ref=1 and the original tau0. Replacing only the denominator in applicability
with each saved a_ref changes none of the currently declared origin/window
read-outs in nontrivial acceptance records across the 14 cases. No additional
normalisation patch is needed for these fixed M2 quantities.

The quantities should remain predeclared and be required explicitly. Missing
nontrivial coverage fields must not default to True; explicit no-first-appearance
abstentions are different. The parent independently checked that the original
stored nontrivial rows did not have missing required fields; the implementation
agent owns fail-closed receipt repair.

Replacing the *interval start* by selected tau can remove an empty H0m interval
from `applicable()`, but this is a vacuous lower-bound condition, not a new
coverage failure. It must not be confused with the a_ref denominator check.

## Target interpretation: a concrete counterexample

The H0 f* target is an exposure-weighted mean over older unit age ranges, not a
calendar-time mean. MZ has no age-range exposure in the Sandbian interval
(452.8,458.2) Ma. A history equal to 1 throughout those 5.4 Myr and zero throughout
all sampled older ranges has exposure-weighted target 0 and the maximum older
likelihood. Yet its calendar mean on (443.1,459.1] is 5.4/16=0.3375, above the
reported H0 limit of approximately 0.18. Accordingly, every interpretation of
that number must name its sampling/exposure weighting. It cannot support a
uniform or calendar-average statement about the whole intervening time.

## Independent primary MZ numerical calculation

`independent_mz.py` constructs the all-empty older-unit likelihood separately,
integrates Gamma(2,2) well effects using 120-node generalised Gauss-Laguerre
quadrature, profiles the common reference rate, and uses independently defined
H0 constraints with SLSQP and tight roots. It uses source-built rows and the
timescale; it does not use the engine likelihood or optimiser for these direct
values. Engine calls are separate comparisons.

| Quantity, MZ rho=1 | Independent calculation | Engine/comparison |
|---|---:|---:|
| H0c f*, all older exposure | 0.05795606051 | 0.05795602465 |
| H0 f*(459.1) | 0.18379094499 | 0.18353798563 at ordinary root tolerance |
| H0 f*(459.1), engine tight root, 48 nodes | — | 0.18379092333 |
| H0 f*(459.1), engine tight root, 96 nodes | — | 0.18379093585 |
| Window f=1 exact endpoint | 462.54790318 Ma | conservative 0.5-Myr grid endpoint 462.6 Ma |
| Constant pre-459.1 intensity, whole Darriwilian | 0.17346661918 | reported derived value 0.17 |

The apparent 0.000253 H0 discrepancy comes from the engine root tolerance
`xtol=rtol=1e-3`: tight engine roots agree with the separate calculation within
2.2e-8, and doubling engine quadrature nodes changes the root by 1.3e-8.
Four decimal places in the CSV overstate root accuracy. The 0.18 headline is
unchanged. Leave engine tolerance unchanged for the present repair and describe
the numerical precision accurately.

The quadrature script can issue a log(0) warning at mathematically zero nodewise
probabilities; their log-likelihood contribution is correctly minus infinity.

## Scope limits

For the primary designs, each ordered-age group shares its range, cluster,
class and multiplier. Sorting iid uniform ages preserves their multiset, and
the estimator is invariant to the corresponding within-group permutation of
outcomes. These simulations therefore do not establish protection against
shared geological boundary uncertainty or other dependent chronologies. The
all-empty older likelihood equivalence is valid for the groups used here.

The reference rate, transport ratio and well-effect shape are not separately
estimated by this exercise. Rho and k are scenario assumptions, with especially
strong dependence in the two-core, cross-region QB comparison. Coverage is
conditional on each fixed design and the potential screen, on the finite truth
grid and declared nuisance settings; it is not simultaneous coverage across
searched designs, variants, history classes or read-outs, nor 95% conditional
coverage given an informative claim.

## Artifacts

- `check_reference.py` and `reference-results.json`: saved acceptance-table
  reference, class and threshold checks. `origin_thresholds_changed` includes
  changing the interval start; `origin_normalisation_thresholds_changed` isolates
  denominator changes and is absent (zero) everywhere.
- `independent_mz.py` and `independent-mz-results.json`: independent likelihood
  calculation and engine precision comparison.

No repository file was edited by this auditor. Receipt/protocol changes and the
QB class-scope amendment require the binding rerun planned by the parent; the
primary empirical MZ values themselves survived the independent calculation.
