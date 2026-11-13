# F3 implementation review: inferential guarantees do not yet match the code

29 October 2026. Author: Codex (`gpt-5.6-sol`, high reasoning). Reviewed the F3 implementation at commit `b2c6443`:

- `docs/f3-shape.md` — SHA-256 `0fbe41a8498ca3c227ae45cc965df6855bc78efa843d794375738a2c1f4346da`;
- `models/f3/envelope.py` — `560901bd68b2bf8f9295177ce99fd55357ce76e5c580f447226b3312df029f38`;
- `models/f3/validate.py` — `1a48e3380aab76b3407b291cbc7eb734ee1e0bda21948d4318713f0ba696cdfc`;
- `models/f3/units_sim.py` — `4a9c8ac428ec27d8072ed571d3a01cafe454067342c2d4269a3072181934c313`.

**Review status:** parent-reviewed Codex recommendations for Claude's response. They are not an adopted method or a decision on Barry's behalf.

**Decision:** do not apply this implementation to the real F3 units as a 95% confidence procedure. It is a useful prototype for likelihood and data-interface work, but its named history classes, critical values, age model and validation programme do not support the guarantees claimed in `docs/f3-shape.md`. The least disruptive remedy is to narrow the class names to what is actually implemented, replace the count-matched critical value with simulation calibration of the complete procedure, correct the two-stage rule, and calibrate any additional predeclared observable reporting rule. A true all-bounded-path H0 can then be added as a separate extension.

This review does not change F3's scientific target. It remains a compatibility analysis: for a candidate origin `T`, estimate the largest reference-rate-weighted pre-appearance encounter intensity `abar_r(T)` not rejected under a declared history class, and invert tests for origin sets under declared lower-intensity restrictions. It does **not** estimate the probability that a clock node predates a maximum. The intended observation process is binary detection in eligible units, with class-specific reference rates, latent ages, shared stage boundaries and Gamma cluster effects. The computational pipeline selects the first appearance and reference window from the outcomes, profiles reference rates, integrates ages and cluster effects, evaluates history-specific likelihoods, and inverts a likelihood-ratio statistic. The defects below arise where that pipeline ceases to represent the declared history or where its sampling distribution is replaced by an unrelated one.

## I1. The three central history-class guarantees are not implemented

### H0 is an equal-duty surrogate, not “any path `0 <= a(t) <= 1`”

`docs/f3-shape.md:52–55` defines primary H0 as every bounded pre-appearance path, including every monotone rise, logistic path and bounded pulse. `envelope.py:41–56` and `:461–477` instead set every older unit's mean intensity to the same duty parameter `x`, apart from its overlap with the interval. The Bernoulli convex-order calculation bounds histories with those **fixed per-unit means**. It does not optimise over the unequal means induced when one common path concentrates intensity in periods, classes or regions with lower encounter rates.

The code acknowledges this at `envelope.py:52–56` and `docs/f3-shape.md:161–163`, but still reports the result as H0. The quoted 0.06 log-probability gap for one ten-fold class contrast is an example, not a uniform error bound. It cannot justify a general conservative guarantee. The only simulated H0 truth is the 0.4-Myr comb in `units_sim.py:67–75`; it has constant duty through time and is specifically aligned with the implemented approximation. `validate.py` has no time-varying class-composition or low-rate-allocation cell that could expose the mismatch. The logistic truth is also scored as a member of H0 (`units_sim.py:95–103`) even though the implemented equal-duty class need not contain its vector of unit means.

**Consequence:** an `H0` result cannot be described as a bound for every path below the reference ceiling, and the associated confidence statement has no stated coverage outside the equal-duty subclass.

**Remedy:** immediately rename the implemented class, for example `H0_equal_duty`, and treat the previously quoted allocation difference only as a sensitivity result. To recover the intended H0, discretise the common path over the actual age support and maximise the likelihood over feasible bounded paths at fixed `abar_r`, including stage/class composition and the shared age draws. Validate the optimisation against exact enumeration on small designs and adversarial allocations before using it as the primary class.

### H0m is a finite collection of delayed steps, not the monotone class

`docs/f3-shape.md:54` calls H0m the monotone non-decreasing subset of H0. `envelope.py:38–40`, `:569–585` and `:663–684` implement only a constant path and delayed constant steps at the finite grid `delays_ma = (0, 2, 6, 10)`. A gradual monotone path, a step at 4 Myr, and a multi-step monotone rise are not members. The sole validation truth uses the on-grid 6-Myr delay (`validate.py:78`).

**Consequence:** the reported H0m origin set is a confidence set for a small, preselected step family, not for monotone encounter histories. It can exclude an origin that a monotone off-grid history would retain.

**Remedy:** call the current class `H0m_delayed_step_grid`. If the scientific target is the full monotone class, use an isotonic representation over age intervals or establish and prove an extremal reduction to steps, with the change point optimised continuously rather than only at four declared values.

### The logistic statistic is not a likelihood ratio for a nested family

The logistic path in `envelope.py:57–60` and `:587–626` has no multiplicative intensity parameter. All profiled `g` values are strictly positive and normalisation forces `a(tau) = 1`. Consequently the best constant history on `[0, 1]`, used as the denominator at `envelope.py:609`, is not a member of the logistic family except for the single limiting constant 1; constants `0 < f < 1` are absent. The assertion in `docs/f3-shape.md:157` that the constant alternative “belongs to each of those classes” is false for logistic. A larger constant likelihood can inflate the statistic relative to the logistic family's own supremum, so there is no general conservative-test argument.

The validation cell is favourable: `g = 0.5` and `h = 11.6` lie exactly on the estimator grid (`validate.py:80`, `envelope.py:166–167`). It does not test between-grid shapes or a scaled logistic history.

**Remedy:** add a multiplicative `f` and a genuine `g = 0` member so the family contains its constant submodel, then calibrate the resulting profile statistic. Alternatively use the supremum over the union of constant and logistic families as the denominator and calibrate that union statistic. Merely sharing the present constant denominator does not supply nesting or coverage.

## I2. The “exact count-matched” critical value is not exact for this model

`exact_count_crit` (`envelope.py:229–235`) converts a one-sided Poisson Garwood upper limit for the observed number of older detections into a Poisson deviance. The F3 statistic is not that deviance. Outcomes are Bernoulli with complementary-log-log probabilities; the reference rate is estimated from finite reference data; Gamma clusters create dependence; ages are integrated; and the first appearance, reference window and older set are selected from the same outcomes. The older detection count is not sufficient for this profile likelihood. Matching a Poisson count limit therefore does not calibrate the test.

An exact enumeration gives a direct counterexample in a strict submodel of the code. Take `R` independent reference Bernoulli units with detection probability `p`, `N` independent older units with probability

\[
q = 1-(1-p)^f,
\]

test `H: f = 1` against `0 <= f <= 1`, profile `p` in both models, and reject when the profile statistic exceeds `exact_count_crit(Y)`, where `Y` is the older count. There are no clusters or uncertain ages in this toy case.

| `R` | `N` | true `p` | sampling frame | exact rejection probability |
|---:|---:|---:|---|---:|
| 10 | 50 | 0.84 | unconditional | 0.0978796 |
| 10 | 200 | 0.04 | unconditional | 0.0296682 |
| 10 | 200 | 0.04 | conditional on at least one reference detection | 0.0885177 |

The last conditioning is relevant because F3 has no first appearance or analysis when no certain detection exists. For that case, `P(X > 0) = 0.3351674`; exact summation over the profiled likelihood ratios gives the values above. This is a counterexample to the claim of exactness, not an estimate of the full F3 error rate. The real data-dependent choice of `tau`, clustering and age integration make analytic transfer from Garwood still less defensible.

The enumeration uses only base R and can be reproduced from the repository root:

```sh
Rscript - <<'RS'
crit <- function(y, a=.05) {
  mu <- qchisq(1-a, 2*(y+1))/2
  2*(mu-y+if (y) y*log(y/mu) else 0)
}
lb <- function(k,n,p) {
  a <- if (!k) 0 else if (p <= 0) -Inf else k*log(p)
  b <- if (k == n) 0 else if (p >= 1) -Inf else (n-k)*log1p(-p)
  a+b
}
ll <- function(x,y,R,N,p,f) lb(x,R,p)+lb(y,N,1-(1-p)^f)
alt <- function(x,y,R,N) {
  ph <- x/R; qh <- y/N
  if (qh <= ph) lb(x,R,ph)+lb(y,N,qh)
  else { z <- (x+y)/(R+N); lb(x,R,z)+lb(y,N,z) }
}
fhat <- function(x,y,R,N) {
  ph <- x/R; qh <- y/N
  if (qh >= ph) 1 else if (!qh || ph >= 1) 0 else log1p(-qh)/log1p(-ph)
}
null <- function(x,y,R,N) {
  if (fhat(x,y,R,N) >= 1-1e-12) alt(x,y,R,N)
  else -optimize(function(p) -ll(x,y,R,N,p,1), c(0,1), tol=1e-12)$objective
}
size <- function(R,N,p,condition=FALSE) {
  reject <- total <- 0
  for (x in 0:R) for (y in 0:N) {
    pr <- dbinom(x,R,p)*dbinom(y,N,p)
    if (condition && x == 0) next
    total <- total+pr
    reject <- reject+pr*(2*(alt(x,y,R,N)-null(x,y,R,N)) > crit(y))
  }
  reject/total
}
print(c(high_p=size(10,50,.84), low_p=size(10,200,.04),
        low_p_given_detection=size(10,200,.04,TRUE)), digits=8)
RS
```

Expected output is `0.09787955`, `0.02966824`, and `0.08851767`.

At zero older detections, `-2 log(0.05) = 5.991` is exact only for a fully specified zero-count probability with the appropriate test ordering. It is not automatically exact after profiling the reference rate and selecting the window. The current unit tests check that the code returns the intended Poisson numbers; they do not establish their sampling distribution under the F3 procedure.

**Remedy:** calibrate each reported statistic under the complete null-generating procedure, including reference-rate estimation, first-appearance/window selection, clusters and age treatment. A parametric bootstrap or a precomputed least-favourable critical surface is defensible if nuisance coverage is demonstrated. Retain the Garwood value only as a diagnostic for the fixed-rate independent-Poisson limiting case.

## I3. The sequential acceptance rule is miscalibrated and the smoke grid is incomplete

### The two-stage threshold is not sequentially calibrated

The code and document agree on stage 1: pass at 944/1,000, fail at at most 915/1,000, otherwise continue (`validate.py:91–105`; `docs/f3-shape.md:130–144`). Stage 2 passes at 1,880/2,000 because the ordinary one-sided Clopper–Pearson lower limit then exceeds 0.93 (`validate.py:107–124`). Reapplying a fixed-sample confidence rule after an interim opportunity inflates the chance of certifying a procedure whose true coverage is exactly the floor:

| pooled stage-2 threshold | `P(pass | p = 0.93)` | `P(pass | p = 0.95)` |
|---:|---:|---:|
| 1,880 | 0.0690335 | 0.9832220 |
| 1,886 | 0.0483732 | 0.9503944 |

Thus the published 0.069 operating characteristic is evidence that the rule does **not** control a one-sided 0.05 false-certification probability at the declared floor. With the existing stage-1 boundaries, 1,886 is the smallest simple pooled threshold among the checked values that restores approximately 0.05 overall error. It is not the same as applying an unadjusted 95% interval at stage 2. If another operating trade-off is preferred, design it explicitly as a group-sequential test.

The operating characteristics can be reproduced with:

```sh
Rscript - <<'RS'
pass <- function(p,K) {
  k <- 0:1000; pk <- dbinom(k,1000,p); mid <- k >= 916 & k <= 943
  sum(pk[k >= 944]) + sum(pk[mid]*pbinom(K-k[mid]-1,1000,p,lower.tail=FALSE))
}
print(rbind(K1880=c(p93=pass(.93,1880),p95=pass(.95,1880)),
            K1886=c(p93=pass(.93,1886),p95=pass(.95,1886))), digits=8)
RS
```

### Unconditional coverage is the valid primary target; the truth-defined subset is diagnostic

`OriginSet.contains` (`envelope.py:294–297`) explicitly includes every candidate true origin at or younger than the first grid point, which is `tau` (`envelope.py:647–654`). Thus, for coverage calculations, the complete confidence set implicitly contains the whole younger side through `tau`, as well as its reported runs above `tau`. At a fixed true origin, unconditional repeated-sampling coverage legitimately includes replicates in which the selected `tau` lies at or above that truth. Those successes are not invalid padding.

`validate.py:22–34`, `:173–215` and `:235–279` separately report coverage among replicates for which the simulated true origin is older than the selected `tau`. In the stationary smoke cell, coverage was 0.955 over all valid replicates and about 0.84 over the 55 such non-trivial replicates. This is evidence of strongly non-uniform coverage and should remain visible, but the conditioning event uses the unknown true origin. It is not an observable reporting rule and cannot replace unconditional coverage as the acceptance target. The 0.84 value is therefore a diagnostic, not by itself a coverage failure.

There is one reporting ambiguity to fix. `OriginSet.runs` (`envelope.py:264–276`) serialises only runs from `tau` upwards, even though `contains` treats every younger origin as included. Any result described as a complete confidence set must explicitly show the younger interval from the analysis-domain lower edge through `tau`, or clearly state that it is included by construction. A finite older endpoint can then be reported without implying that the set starts at `tau`.

**Remedy:** retain unconditional coverage as the primary acceptance quantity and retain the known-truth subset as a non-uniformity diagnostic. If the eventual analysis suppresses, privileges or labels results using an **observable** rule—such as finite versus unbounded endpoint, minimum older exposure, or reference-information thresholds—declare that rule first and calibrate the selected/reporting procedure. Do not define a reporting rule by `T_true > tau`, which cannot be evaluated on real data.

### The smoke grid is matched to the implementation, not to the promised failure modes

The six cells in `validate.py:74–83` contain no H1 truth; only one equal-duty H0 comb; one on-grid H0m delay; and one on-grid logistic shape. `units_sim.py` draws class independently with a constant class mixture through time, generates ages from the same model assumed by the estimator, and omits eligibility misassignment, reporting/facies differences and regional confinement. These are among the required scenarios in `docs/f3-shape.md:118–126`. The grid therefore cannot discriminate the intended broad H0 from the equal-duty surrogate, or diagnose age-model misspecification, class/age confounding, leakage from first-appearance selection, or extrapolation across sampling regimes.

The full predeclared validation grid has not been run. The smoke outputs remain useful development evidence, not acceptance evidence.

## I4. The boundary draws are not a defensible joint age model

`AgeModel.draw_boundaries` (`envelope.py:107–127`) interprets every non-blank `base_unc_ma` as an independent Normal standard deviation and sorts each draw to restore order. This conflicts with the source interpretation already recorded in `docs/primer.md:32–34,58,351` and `docs/decisions.md:109`:

- the confidence level of the Ordovician and Silurian chart “±” values is undetermined;
- the Devonian values are the wider side of asymmetric 95% intervals from one correlated Bayesian age–depth model, not standard deviations;
- blank Cambrian uncertainties mean unresolved/unstated, not known exactly;
- the boundary ages require a joint ordered model.

Sorting independent draws is not such a model. It replaces crossings with order statistics, changing marginal distributions and inducing arbitrary dependence while retaining stage labels by array position. Under the implemented Normal-SD interpretation, the Pragian and Emsian bases cross before sorting with probability about 0.190. The code then silently swaps their order statistics. Treating the quoted Devonian 95% half-widths as one standard deviation also makes their distributions roughly twice as wide as the cited posterior intervals.

The simulator uses the same construction (`units_sim.py:123–137`), so matched-model recovery cannot reveal this error. Shared draws across units correctly preserve computational dependence conditional on a draw, but they do not make the geological distribution evidence-based.

**Remedy:** until joint posterior draws or a defensible joint reconstruction are available, analyse fixed chart boundaries and state that numerical-age uncertainty is not propagated. Add coherent sensitivity scenarios for boundary shifts and durations if they can change the verdict. When joint samples become available, consume them directly; do not reconstruct them by independent perturbation and sorting.

## Verification and residual risks

- The complete `models/f3` test suite passed: **117 tests in 11.50 s** using the repository's declared Python dependencies. This verifies the present mechanics. Several tests explicitly encode the disputed choices: independent-Normal sorted ages, a stage-2 threshold of 1,880, and the Poisson count critical values. Green tests therefore do not validate the inferential claims.
- The sequential probabilities above were recomputed by exact binomial summation. The Garwood counterexample was recomputed by enumerating all reference and older counts and profiling the Bernoulli complementary-log-log likelihood in each cell.
- No real F3 units were fitted and no full validation grid was run. No conclusion about M1, M2 or M3 follows from this review.
- `Problem._profile_theta` (`envelope.py:487–500`) does not inspect optimiser success, gradients or boundary solutions. This is a secondary but material risk once the statistical specification is repaired; record convergence status per profile and test multi-start recovery before a large grid.
- The observation model still assumes transportability of reference rates, correct eligibility classes and the declared Gamma dependence. Those are empirical sensitivity questions even after code calibration. M3 remains outside the inferential scope unless a comparable positive/eligible-negative body-fossil inventory is assembled.

## Recommendation

1. Freeze real-data application, not the prototype.
2. Rename H0 and H0m to their implemented subclasses; either repair logistic nesting or withhold its confidence labels.
3. Replace `exact_count_crit` as the inferential calibration with a full-procedure bootstrap or least-favourable simulation calibration.
4. Change the pooled stage-2 threshold to 1,886 if the intended operating criterion is at most 5% false certification at true coverage 0.93; update the operating-characteristic table and tests.
5. Keep unconditional coverage as the primary acceptance criterion, make the confidence set's implicit younger interval explicit, and retain the observed ~0.84 truth-defined subset coverage as a diagnostic of non-uniformity. Calibrate an additional selected-reporting target only after defining an observable reporting rule.
6. Use fixed boundary ages until an evidence-based joint age model is available.
7. Expand and freeze the validation grid before rerunning it: unequal class composition through time, off-grid monotone and logistic truths, H1, reporting/eligibility error, regional confinement, cluster misspecification, age-model sensitivity, and the full first-appearance selection.

Independent scientific review would materially improve confidence **after** these repairs, especially for the all-path extremal argument and calibration of any observable reporting rule that is eventually adopted. It is unlikely to change the present stop decision: the class mismatches, sequential error and age-model conflict are direct discrepancies between the declared estimand and the executed code, and the Bernoulli enumeration supplies a counterexample to the claimed exact calibration.
