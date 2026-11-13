# Loop 2 sprint 1: independent methods review

Codex, 1 November 2026. Read-only scientific audit of the count-share method, the
Murzuq contamination/identification likelihood, its declared grid and the frozen-engine
sensitivities. The audit used the final source and output hashes in the method receipts; it did
not reassess the primary literature or alter the frozen Loop 1 analysis.

## Decision

**Accept as a method and unqualified sensitivity handoff. Do not treat it as a qualified
empirical count analysis, an estimate of caving or indigenous production, or a replacement for
the frozen Loop 1 results.** The likelihood and parameter reductions are correct under their
declared assumptions. Three defects found during review were repaired before acceptance:

1. the stratified zero-count solver now works on a scale-free root, avoiding an
   anti-conservative zero or inaccurate upper limit at large finite effort ratios;
2. a positive target count with known zero target effort is rejected as impossible under the
   declared observation model, rather than reported as weak identification; and
3. every break-even row and the manifest now state that the root surface has `kappa=0` and
   `b=0`; the full factorial grid, not the root table, covers positive contaminant transfer.

`docs/loop2-sprint1-results.md` preserves these limits and does not overstate the new results.

## Scientific target and observation model

The count-share target is the target/control rate ratio `theta`, and secondarily
`theta/(1+theta)`, conditional on a documented effective-effort ratio. Independent Poisson
target and control counts become binomial after conditioning on each observed total. A producer
interpretation additionally requires the effective-effort ratio to include relative delivery,
recovery, preparation and counting. Neither held fossil frame supplies that observation
contract, so the method has no empirical estimand in this sprint.

The Murzuq diagnostic instead uses the frozen binary frame: 51 detections among 59 reference
units and 28 older reported zeros in five wells. Its scientific target is an identification
surface, not a point estimate. With total observed reference intensity `r`, indigenous fraction
`g`, delivery ratio `rho`, older indigenous intensity `f`, and contaminant transfer `kappa`, the
older likelihood depends on

```
a = rho * g * f
b = kappa * (1 - g).
```

Each well has one shared Gamma(2,2) frailty. Independent-uniform chronology marginalises each
unit's age separately; the shared 10%, 50% and 90% chronologies are fixed, ordered stress
scenarios, not a fitted or marginalised age-depth model. Reference and older outcomes share the
well frailty, and the common `r` is profiled jointly.

The reduction to `(a,b)` is exact in the implemented likelihood. Thus `rho`, `g`, `f` and
`kappa` are not separately identifiable. If every relevant age weight is one, only `a+b` is
present in the likelihood; partial or zero weights can in principle distinguish `a` from `b`. The model-conflict guard also
correctly separates a contamination assumption that already predicts implausibly few all-zero
older outcomes from the incremental comparison for `a`.

These conclusions require a common reference rate across wells, the declared shared frailty,
binary reporting as the observation, and the proportional transfer relation in `b`. The source
record does not establish those as geological mechanisms. They are transparent sensitivity
assumptions.

## Independent numerical and analytic checks

- The focused suite passes: **37 tests** across `test_count_share.py` and
  `test_contamination.py`. It includes analytical Clopper--Pearson identities, zero-event
  identities, extreme finite effort ratios, impossible data, the Gamma-Laplace likelihood,
  frozen-frame reconstruction, equivalence, chronology order, conflict and source-override
  guards, root monotonicity and explicit no-transfer scope.
- Exact binomial enumeration covers 77 declared cells. All pass the nominal 0.95 check; the
  minimum exact coverage is **0.9504055350**. This validates the stated conditional construction,
  not either fossil design. Deliberate misspecification is decisive: using `h=1` when the true
  effort ratio is 0.1 gives coverage `2.37e-18` for the chosen producer-odds target, and the
  beta-binomial stress gives **0.3732** versus **0.9763** under the independent comparator.
- I independently integrated the Gamma frailty with adaptive quadrature in `u`, rather than the
  implementation's log-grid quadrature, and independently profiled `r`. For the stage allocation,
  independent-uniform chronology, origin-to-459.1 target and `b=0`, the critical effective
  intensity was **0.0910296496004**; the implementation gives **0.0910296495610**, a difference
  of `3.94e-11`. The independent likelihood ratio was **5.991464547108**, the declared
  `-2 log(0.05)` convention.
- The final contamination artefacts contain **5,760** factorial rows and **384** break-even rows.
  All 5,760 reference, null and candidate profiles have valid finite results. All 384 root scans
  are monotone and have valid profiles; 312 have a root through `a=1` and 72 do not. Across
  1,056 duplicated `(a,b,frame)` groups, numerically equivalent parameter tuples give identical
  profiled results and status.
- The final manifest's input and output hashes reconstruct without drift. The full grid has
  2,304 model-conflict rows, 561 rejected comparisons and 2,895 unrejected comparisons. These
  counts describe the declared grid, not probabilities over geological states.

The short-window result is therefore a real sensitivity finding but not an empirical bound.
At `rho=f=1`, `kappa=0` and independent-uniform stage ages, the 459.1--462.6 Ma comparison crosses
the convention at `g=0.9558967`. Under the shared midpoint chronology the same window has zero
exposure and no root. The contrast shows scale and chronology mismatch directly; it does not
select either chronology. The separate 36-case engine exercise reproduces the frozen baselines,
has no failed fits and varies one well, boundary-age scenario or allocation at a time. It is an
influence analysis, not joint robustness or transferred qualification.

## Residual risks and recommendation

The decisive residual risks are structural, not computational: unknown effective count effort;
differential delivery and preservation; binary reporting rather than matched counts; five-well
pseudoreplication handled only through the chosen frailty; common-rate and proportional-transfer
assumptions; coarse chronology scenarios; and an uncalibrated likelihood-comparison threshold.
No multiple-scenario probability or coverage statement follows from the factorial grid. The
new contamination likelihood has no recovery or coverage study, so a numerical rejection is
only rejection by the declared convention.

Retain the code, receipts and result surfaces as the sprint-2 protocol and value-of-information
handoff. Withhold any empirical count-share, caving-rate, indigenous-fraction or crown-age claim
until matched counts/search effort, a defensible relative-effort model and a new validation design
exist. A further independent statistical review is unlikely to change this method-handoff
decision after the analytical and alternative-quadrature checks. Independent palaeontological
and observation-protocol review would materially affect any attempt to promote the sensitivities
to geological inference, because that promotion depends on source linkage and mechanisms not
identified by these data.
