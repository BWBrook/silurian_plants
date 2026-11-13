# Mathematical review of the interval test and Murzuq specification

Codex specialist review (`sol_high_specialist`, configured GPT-5.6-sol/high), 8 November 2026.
Scope: F2 and F10 of `2026-11-07-gpt6pro-review2-triage.md`, at commit `8a2194e`. I read
`interval_feasibility.py`, its source diagnostic, `envelope.py`, `designs.py`, `m2.py`, the frozen
M2 declaration and qualification receipt, and the corresponding article, supplement and estimands.
I did not change a model, output, claim status or manuscript product.

## Decision

1. **The interval-wide rejection argument is valid under a slightly sharper statement of its
   conditions.** The exact-age KS test is finite-sample valid after conditioning on the count and
   maximum. Requiring every age allocation in the recorded supports to reject can only reduce its
   rejection set, provided the intervals contain the latent ages almost surely. The present proof has
   that core logic. The geological intervals are coarsened observations, however, not nuisance
   parameters in the Berger--Boos sense. If interval containment has failure probability $\delta$, the
   available unconditional size bound is $\alpha+\delta$, not $\alpha$; conditioning after the fact on
   the event of containment does not establish a level-$\alpha$ test. Revise the terminology and make
   the almost-sure-containment assumption explicit. No numerical result changes.
2. **S2.2 is materially under-specified but the implemented Murzuq model is coherent.** The current
   sentence $1-\exp(-rux)$ is only the constant-path, known-age kernel. It omits integration over each
   unit's age range, the joint well likelihood, the profiled nuisance rate, the exposure-weighted target,
   and the distinction between mean-intensity and pointwise origin/window read-outs. A paste-ready
   specification is below. It also separates the qualified Gamma-well model from the unqualified
   inverse-block-size sensitivities in S2.5.

An independent scientific review would not materially change these decisions after the two wording
repairs. A new simulation is not needed for F2. Extending the Murzuq result to a different within-well
dependence law would be a new model, not a documentation fix.

## 1. Interval-feasibility test

### Target and implemented statistic

For one fixed recording history with cumulative exposure $U$, fixed younger cutoff $c$, and $n$
independent continuous occurrence ages, let $A$ be the largest observed age. Conditional on $n$ and
$A$, the other $m=n-1$ transformed ages

$$Z_j=\{U(t_j)-U(c)\}/\{U(A)-U(c)\}$$

are independent Uniform$(0,1)$ variates under that history. The ordinary two-sided one-sample KS
statistic therefore has the finite-$m$ distribution used by `scipy.stats.kstwo`. Removing the unique
maximum is essential: the code does so in `shape_check`, and `interval_feasibility.py` constructs one
`profiled_maximum` slot plus $m$ conditional ranks.

The matching calculation is also the right finite optimisation. For ordered $Z_{(j)}$,

$$D_m=\max_j\{j/m-Z_{(j)},\ Z_{(j)}-(j-1)/m\}
     ={1\over2m}+\max_j|Z_{(j)}-(j-1/2)/m|.$$

That identity is exactly the radius used by `_matching_at_discrepancy`. Event endpoints and open cells
of the feasible matching graph are enumerated; bisection brackets the global minimum in $D$ to
$5\times10^{-11}$. The reported witness *p* is consequently within that numerical tolerance of the
supremum. More importantly for rejection, `threshold_certificate` directly establishes whether any
allocation is feasible at the exact finite-sample 0.05 critical value. The decision does not depend on
rounding the displayed optimum *p*.

### Why enveloping the intervals is conservative

Let $T_\alpha(z)$ be the exact-age rejection indicator and let $S$ be the Cartesian product of the
recorded intervals plus the enumerated cutoff-inclusion states. The implemented interval rule is

$$T_\alpha^S(S)=1\{p(z')<\alpha\ \hbox{for every }z'\in S\}.$$

If the latent exact age vector $Z$ belongs to $S$ almost surely, then pointwise
$T_\alpha^S(S)\le T_\alpha(Z)$, irrespective of how the reported intervals depend on $Z$. Therefore

$$\Pr_H\{T_\alpha^S=1\}\le\Pr_H\{T_\alpha(Z)=1\}\le\alpha.$$

The same argument covers a random inclusion state because all states consistent with cutoff-straddling
supports are enumerated and the true state is one of them. Conditioning on the count and maximum is
already part of the exact-age test and does not invalidate the dominance argument.

This is best described as a **support-enveloped exact-data test**, not a *p* value maximised over a
nuisance parameter. Berger and Boos (1994) study maximisation over a confidence set for a nuisance
parameter and add the confidence-set error probability $\beta$. Here the ages are unobserved data and the
repository does not attach joint coverage to the geological supports. The citation can remain as a
related maximised-*p* construction, but it is not the justification for omitting $\beta$.

The containment assumption must be structural: under the observation model the recorded interval
contains each latent age with probability one. If instead
$\Pr(Z\notin S)=\delta$, the direct bound is

$$\Pr_H\{T_\alpha^S=1\}\le\alpha+\delta.$$

The manuscript correctly says that the geological ranges have not been demonstrated simultaneous
confidence sets. It should avoid suggesting that nominal 0.05 coverage follows merely by conditioning
on the realised event $Z\in S$.

### Other conditions that remain material

- The history, cutoff, numerical timescale, unit inventory and unit rule are held fixed for the test.
  If a history were selected because it fit this same age sequence poorly, its nominal reference would
  need selection adjustment. The six declared histories may be compared individually; the calculation
  is not a familywise model-selection procedure.
- Conditional on count, ages must be independent draws from density proportional to the declared
  recording history. Pseudoreplicated locality-age units, shared stratigraphic ordering or spatial and
  collecting dependence can invalidate the finite KS reference. The interval rectangle is deliberately
  wider than a coherent section chronology; that can create a passing witness, but a coherent subset
  cannot rescue an interval-wide failure if it contains the truth.
- The result rejects only this **conditional age-distribution diagnostic**. It does not test the count
  process, establish a biological rate history, or compare clocks. “For this diagnostic” must stay next
  to “rejection”.
- A passing allocation is existential. Maximising its *p* does not estimate ages, provide a goodness-of-
  fit probability, or establish adequacy.

### Verification

I independently simulated 200,000 continuous iid samples for each $n=48,49,50,76$, removed the maximum,
divided the remaining values by it, and compared the two-sided KS statistic with
`kstwo.ppf(0.95,n-1)`. Rejection proportions were respectively 0.05019, 0.049745, 0.050735 and 0.05002.
This checks the finite reference and the loss of one degree of sample size; it does not test geological
interval containment or unit independence.

### Paste-ready replacement for the inferential paragraph in S5.2

> **What a failure and a pass mean.** For a fixed history, cutoff, timescale, inventory and unit rule,
> let $z$ be the latent exact ages and inclusion state, $S$ the set of allocations allowed by the
> recorded supports, and $p(z)$ the finite-sample conditional-on-count-and-maximum KS *p* value under
> independent continuous occurrence ages. The interval rule rejects only if every $z'\in S$ has
> $p(z')<\alpha$. Under an observation model in which the recorded intervals contain the latent ages
> almost surely, the true allocation belongs to $S$, so this rejection event is a subset of rejection by
> the level-$\alpha$ exact-age test and is conservative. If interval containment can fail with
> probability $\delta$, the direct size bound is instead $\alpha+\delta$; these geological ranges have
> no demonstrated joint coverage. The maximisation resembles maximised-*p* constructions
> [@berger1994PValuesMaximized], although here the intervals coarsen the observations rather than form a
> confidence set for a nuisance parameter. Enumerating every cutoff-inclusion state preserves the
> argument when the true state is included. A passing witness is only an admissible allocation, not an
> estimated chronology, evidence of model adequacy or a ranking of histories. The test remains
> conditional on the declared history and on independent units; coherent section chronologies could
> remove a passing allocation but cannot rescue an interval-wide failure if they contain the truth.

For the shorter article and `estimands.md`, replace “sup-*p* argument” with “support-enveloped exact-age
test” and add “fixed cutoff, timescale, inventory and unit rule” to the existing conditions. The current
finite-sample numbers and pass/fail labels can remain.

## 2. Paste-ready mathematical specification for S2.2

The following is deliberately self-contained. It describes the qualified primary `LY-MZ-CU` model.
The inverse-block-size calculations remain in S2.5 as unqualified composite sensitivities and should not
be folded into this likelihood.

### S2.2 Model, targets and qualification

Let $d_i\in\{0,1\}$ be the reported trilete outcome for eligible cutting $i$, $c(i)$ its eligibility
class, $k(i)$ its well, and $[l_i,h_i]$ its declared age range. Conditional on the fixed stage
boundaries, latent age is uniform on that range. Let $r_c>0$ be the nuisance reference encounter hazard
for class $c$. A mean-one well effect
$u_k\sim\mathrm{Gamma}(\kappa,\kappa)$ is shared by the reference and older cuttings in well $k$;
the primary across-well design fixes $\kappa=2$. Well effects are integrated out, not estimated.
Cutting outcomes are independent conditional on their well effect and latent ages.

The first-appearance rule gives $\tau=443.1$ Ma. Encounter intensity is scaled to $a(t)=1$ in the
five-stage reference window. For a candidate origin $T>\tau$, $a(t)=0$ for $t>T$. The declared older-to-
reference delivery and recovery multiplier is $m_i=\rho$ for transported older cuttings and 1 otherwise,
with $\rho\in\{1,0.5,0.25,0.1\}$ fixed in separate analyses rather than estimated. Partition
$(\tau,T]$ at stage and numerical-range boundaries. If $w_{ip}$ is the fraction of unit $i$'s age range
in piece $p$, $Q_i$ the fraction in the reference interval at or younger than $\tau$, and $x_p$ the mean
of $a(t)$ in piece $p$, its age-integrated detection probability conditional on $u$ is

$$
\pi_i(u;r,x)=Q_i\{1-\exp(-r_{c(i)}m_i u)\}
 +\sum_p w_{ip}\{1-\exp(-r_{c(i)}m_i u x_p)\}.
$$

The unshown remainder of the age range lies older than $T$ and contributes zero detection probability.
For piecewise-constant histories this expression is exact. The joint likelihood is

$$
L(r,x)=\prod_k\int_0^\infty
  g_{\kappa,\kappa}(u)
  \prod_{i:k(i)=k}\pi_i(u;r,x)^{d_i}
       \{1-\pi_i(u;r,x)\}^{1-d_i}\,du .
$$

Thus samples from the same well are marginally dependent. The likelihood profiles $r$ jointly with the
history; the reference-only fit supplies starting values, not a plug-in rate held fixed. In the primary
data there are 59 reference cuttings (51 positive) and 28 older zeros in five wells. At $T=459.1$ Ma,
18 older cuttings have all their age support in $(\tau,T]$, while each of the ten Darriwilian cuttings
has exposure weight $q_i=0.9/11.2=0.08036$. Under the constant history $a(t)=f$, its zero probability
reduces to

$$
1-q_i+q_i\exp(-r\rho u f),
$$

inside the same well integral as the reference outcomes.

For nonconstant histories the reported target is the fitted-rate-weighted mean intensity

$$
\bar a_r(T)=\sum_p c_p(r)x_p,\qquad
c_p(r)=\frac{\sum_i r_{c(i)}m_i w_{ip}}
             {\sum_i r_{c(i)}m_i\sum_q w_{iq}}.
$$

The rates in these weights are profiled in the likelihood. With the primary cutting-only design there is
one rate class, so class-rate uncertainty does not change the relative piece weights.

| Class | Restriction on $a(t)$ for $\tau<t\le T$ | Ceiling | Reported use |
|---|---|---:|---|
| H0c | $a(t)=x$, constant | 1 | exact constant-history bound and origin read-out |
| H0 | any path $0\le a(t)\le1$ | 1 | bound on $\bar a_r$; pointwise origin and window read-outs |
| H0m | H0 plus intensity non-decreasing towards $\tau$ | 1 | monotone bound; origin read-out permits the declared 10 Myr delay |
| H1 | any path $0\le a(t)\le3$ | 3 | higher-ceiling sensitivity for $\bar a_r$; no origin read-out |

For H0c the age-integrated likelihood is exact. For H0, H0m and H1 the implementation bounds each
piece using the convex chord for non-detections and Jensen's inequality for detections, then maximises
over piece means. With no older detections, as in the primary Murzuq design, the H0 and H1 bounds are
attainable. The H0m within-piece relaxation remains conservative because its extremal path need not be
monotone inside every piece.

For class $K$ and threshold $f$, let $\bar\ell_{0,K}(f;T)$ be the supremum of the implemented
chord/Jensen **upper log-likelihood envelope** over nuisance rates and piece means satisfying
$\bar a_r(T)\ge f$, and let $\ell_{A,K}(T)$ be the exact log likelihood of the best constant history up
to that class's ceiling. For H0c the null is also exact, so $\bar\ell_{0,K}=\ell_{0,K}$. For H0 and H1
the envelope is attained in the present no-older-detection application; for H0m it can remain strictly
above the likelihood supremum over monotone paths and therefore gives a conservative statistic. The
implemented statistic is

$$\Lambda_K(f;T)=\max\left[0,\ 2\{\ell_{A,K}(T)-\bar\ell_{0,K}(f;T)\}\right].$$

The reported $f_K^*(T)$ is the largest $f$ not excluded. H0c, H0m and H0 share the constant alternative
on $[0,1]$; H1 uses its ceiling of 3. The declared critical value is the one-sided count-matched value
for the number of older detections plus a simulation-calibrated nonnegative shift. Here there are no
older detections and the accepted shift is zero, giving $-2\log(0.05)=5.991$.

Origin read-outs impose pointwise restrictions rather than only the mean target. H0c requires a
constant $a\ge f$ on $(\tau,T]$; H0 requires $f\le a(t)\le1$ throughout that interval; H0m requires the
floor through $T-10$ Ma and permits zero intensity during the first 10 Myr after origin. The separate H0
window read-out beginning at 459.1 Ma requires $a(t)\ge f$ only on $(459.1,T]$ and allows any path in
$[0,1]$ between $\tau$ and 459.1 Ma. These are marginal read-outs, not a simultaneous confidence band.

“Qualified” means that the complete screen, first-appearance selection, likelihood fitting and test
inversion attained at least the declared 0.93 marginal-coverage floor on the frozen finite simulation
grid, with a calibration target of 0.955 and a separate acceptance run. It does not validate uniform age
within stages, Gamma$(2,2)$ well heterogeneity, conditional independence, equal reporting scope, the
chosen $\rho$, or the historical sampling process outside that grid. Inverse-block-size weighting and
leave-one-well-out results in S2.5 are retrospective unqualified sensitivities, not alternative qualified
dependence models.

## Residual risks and recommendation

- The qualified Murzuq result still rests on a specific frailty distribution and residual conditional
  independence. The stage-2 block weighting shows sensitivity but does not identify correlation. A
  fitted correlation model is weakly identified by five wells and would require a fresh calibration.
- Age is integrated uniformly within fixed ranges. The ten Darriwilian units carry only 0.08036 exposure
  each at 459.1 Ma under that model, so chronology and within-stage age density remain consequential.
- The binary chart outcome conflates production, delivery, preservation, preparation and reporting;
  $\rho f$ is identifiable more directly than producer intensity $f$.
- The finite qualification grid supports the stated operating claim only on its sampled histories and
  diagnostics. It does not turn the likelihood into a literal model of the historical process.

Adopt the S2.2 specification after editorial compression, and make the two precise S5.2 terminology
changes. Preserve all current F2 numbers and C49 status. No rerun is needed solely for these mathematical
repairs.

## Narrow figure-semantics addendum

The proposed Fig. 4 and first-record corrections are sufficient without a new analysis, subject to two
wording qualifications.

For Fig. 4, the contour target is the recoverable-body endpoint $T-d$, not the crown age $T$ when
$d>0$. The implementation and Table S9b define the contour only when $T-d>A$, where $A$ is the oldest
possible crown-member fossil age. Returning `NaN` when $T-d\le A$ is therefore the correct rendering of
an undefined contour and prevents an undefined value from becoming a false no-reduction plateau. For
the valid domain, the raw equality contour is

$$r^*(T,d)=\frac{(A-c)(0.05^{-1/n}-1)}{T-d-A}.$$

Displaying $\min(r^*,1)$ is legitimate as a reduction-only summary, but the plateau at one is not the
raw equality contour where $r^*>1$: it means that the target is already compatible at equal earlier and
later intensity. The caption should say explicitly that ratios at or above one are capped at the
no-reduction ceiling; ideally the vertical-axis wording should also avoid implying exact equality on
that capped segment. “At a fixed candidate crown age, an assumed delay reduces the required recording
contrast” is correct because increasing $d$ increases $r^*$ until no reduction is needed or the contour
leaves its domain. This replaces the less precise claim that delay moves the curve towards the fossils.

For a category with unit ages $a_i\in[l_i,u_i]$, `body_first` returns

$$\left[\max_i l_i,\ \max_i u_i\right],$$

which is the exact support of the category's oldest occurrence $\max_i a_i$ under the recorded
rectangular age supports. It is not necessarily one find's age range. The B2 upper endpoint is 426.7 Ma
from either of two Yea units; the lower endpoint is 419.62 Ma, shared by thirteen units, including four
Bathurst units. It should therefore not be attributed uniquely to Bathurst. Labelling the bands as
category first-record age supports, saying that their endpoints may come from different finds, and
retaining the values is accurate. This is a display-semantics correction, not a change to the inventory
or model outputs.
