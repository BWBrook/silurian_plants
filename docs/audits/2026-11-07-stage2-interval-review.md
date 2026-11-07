# Independent review of the Stage 2 interval-feasibility calculation

Codex (OpenAI), 7 November 2026. This is a read-only scientific audit of
`models/f3/loop3/interval_feasibility.py` at SHA-256
`630a5c9e755c0d628a2934a846c3737ed8b9105270870f6f5ce0cf425bc17101`. It reviews the
maximum-conditioned Kolmogorov--Smirnov (KS) calculation only; it does not re-review the body
inventory, timescale scenarios or endpoint model.

## Decisive findings

1. **The continuum search is complete for the model it declares.** For a fixed cumulative-exposure
   maximum `M`, the `k`th of `m = n - 1` conditional observations has KS discrepancy at most `D`
   exactly when its normalised exposure lies in

   `[k/m - D, (k - 1)/m + D]`.

   Writing the interval as a midpoint rank plus radius `D - 1/(2m)` gives the bounds implemented in
   `_matching_at_discrepancy`. A unit with exposure support `[l_i, u_i]` can occupy rank `k` exactly
   over the closed maximum interval `[l_i/q_upper, u_i/q_lower]`, with the zero-denominator case
   unbounded above and all rank bounds capped to `[0, 1]`. The designated maximum has the separate
   edge `[l_i, u_i]`. The bipartite graph can therefore change only at the collected edge endpoints;
   checking every endpoint and one point in every intervening open cell is exhaustive over the
   continuum of `M`, up to the recorded floating-point tolerance.
2. **The matching formulation does not introduce an ordering or tie error.** Rank-band lower and
   upper limits are both non-decreasing in rank. If independently selected values for matched ranks
   cross, sorting them still places the `k`th value inside the `k`th band: at least `k` matched
   values are no greater than that band's upper limit and at most `k - 1` can be below its lower
   limit. One unit is assigned the omitted maximum slot and every other unit a unique conditional
   rank. Closed-support ties are consequently handled consistently with the repository's direct KS
   recomputation.
3. **The cutoff-straddling partition is complete under rectangular supports.** B2 and B0 each have
   two units whose recorded interval crosses 393.47 Ma. The four inclusion masks enumerate every
   assignment of each unit above versus below the cutoff, giving B2 sample sizes 48, 49, 49 and 50
   and B0 sizes 76, 77, 77 and 78. Included supports are clipped at the cutoff; every excluded support
   has a non-empty portion below it. No probability is assigned to the masks. The canonical B0 input
   now requires exactly one main-reading K12 row with B0-only membership and 445.2--452.8 Ma support;
   there is no fallback construction.
4. **The positive and negative classifications are numerically well separated where the scientific
   conclusion depends on them.** Direct recomputation of the 50-unit B2/decline25 witness gives
   `D = 0.182447235454`, finite-sample `p = 0.067130176573`, and a 0.007831 margin below the finite
   5% critical value. Every allocated age is inside its recorded support. The combined
   plant-excluded-PBDB/10 Myr witness also remains above 5% for all 50 possible units
   (asymptotic `p = 0.06581`, finite-sample `p = 0.05741`). Conversely, guaranteed B2 under decline25
   has global `D > 0.203289614932`, above the asymptotic and finite critical values 0.198099046478 and
   0.194197250204. This is a robust computational non-feasibility result, not a failed heuristic
   search. Guaranteed B2 under the combined history remains convention-dependent: asymptotic
   `p <= 0.05195`, finite-sample `p <= 0.04484`.
5. **The synthesis accurately distinguishes existence from universal failure.** At least one
   support-consistent B2 subset attains nominal 5% non-rejection for decline25 and the combined
   history; none does for pure decline10. No B0 subset attains nominal 5% non-rejection under any of
   the six declared histories; its best cell is the 78-unit decline25 case
   (asymptotic `p <= 0.005145`, finite-sample `p <= 0.004352`). These are statements about the
   encoded support rectangles and this exact-age diagnostic. They are not calibrated tests after
   latent-age optimisation and do not identify true ages or select a recording history.

## Independent verification

- The targeted repository suite passes: `4 passed` from
  `uv run --with numpy --with pandas --with scipy --with pytest python -m pytest
  models/f3/loop3/test_interval_feasibility.py -q`.
- I independently enumerated every unit-to-rank permutation for small cases, rather than using sparse
  matching or event cells. Across 120 seeded four-unit interval systems, this agreed with the repository
  on 720 fixed-`D` feasibility decisions and all 120 global-`D` brackets; the largest bracket-midpoint
  difference was `1.74e-11`. Exact point-support fixtures separately recovered a positive
  case with `D = 1/6` and a negative case with `D = 0.97` against the same finite-sample critical value.
- The decisive positive witness was recomputed directly from its saved ages and recovery exposure,
  without invoking the optimiser. The saved `D`, finite-sample probability and support checks agree.
- The receipt binds seven inputs and 52 outputs, including all 48 witness files. All 59 recorded hashes
  match the live files. The receipt records `canonical_horizons_reviewed`; no external review path is
  read at runtime.

## Assumptions and residual risks

The scientific target is narrow: whether any exact age vector inside the admitted supports can attain
a nominal KS non-rejection threshold after conditioning on its maximum, for one fixed recovery history
and one chosen inclusion mask. The result assumes independent locality--age units, strictly positive
fixed recovery intensity, continuous rectangular age supports and no chronology coupling among units.
It does not address dependence within formations or collecting programmes, informative database entry,
taxonomic misclassification, source-timescale mismatch, or a fossil-to-lineage delay.

Optimising ages makes the reported KS probabilities non-uniform under the null. They are diagnostic
thresholds, not calibrated post-search `p` values. The negative results are exhaustive computational
certificates under double precision and the declared `2e-12` edge tolerance, not formal
exact-arithmetic proofs. The algorithm intentionally admits closed support endpoints and any ordering
that the independent rectangles allow; source-specific section order or correlated boundary motion
could shrink that feasible set. Those limitations affect geological interpretation, not the internal
validity of the encoded optimisation.

## Recommendation

Accept the interval-feasibility implementation without code changes. Report the two 50-unit B2 cases as
permissible witnesses, guaranteed-B2 decline25 as having no nominal 5% witness under either reference
distribution, and the guaranteed-B2 combined case as reference-distribution dependent. Phrase the pure
decline10 and canonical-B0 findings as **no allocation within the encoded supports attains nominal 5%
non-rejection for this diagnostic**, not as rejection of the biological history. Independent geological
review of the pivotal supports and their cross-unit ordering would materially change confidence in the
scope of inference, but further review of the optimisation arithmetic is unlikely to change the decision.
