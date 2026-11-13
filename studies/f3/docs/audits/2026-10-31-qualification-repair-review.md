# Review of the scoped screen and ASR diagnostics

31 October 2026. Codex, with two bounded independent reviewers. Reviewed model
commit `4e0d757`, present at clean starting HEAD `4b60597`. Model and pilot
implementation remain Claude's. No ensemble or stochastic-map rerun was needed.

## Accepted repairs

The homogeneous independent screen now states its domain, reference membership,
class ceilings and conversion. Its zero-reference guard and the named invalid
bound-state rejection work. Eight relevant screen/parser tests passed. These
checks accept the restricted diagnostic; they do not revive the former universal
claim. The historical counterexamples in `2026-10-31-screen-counterexamples.py`
remain evidence against their reviewed commit `45adb8d`.

The ASR diagnostics reproduce from saved traces: chain sizes, seeds, map indices,
path identities, all published R-hat/ESS values and both output-hash receipt sets
check out. The longer extant chains pass the declared convergence/precision
criteria; the original extant chains fail. All retention medians and interval
endpoints reproduce within 5.6e-16. The extant 515.5 Ma retention scenario is
0.893863 (0.331526–0.955751). The earlier eo value of 1.000 was zero departures
among 969 trilete starts, not demonstrated certainty; the new traces include
three departures. These remain conditional model-derived scenarios.

## Bounded changes requested from Claude

1. **Specify what selection is covered.** Per-frame conditional coverage applies
   when each fixed frame is reported whenever it passes. It also supports a fixed
   search order or choosing the next independent frame before inspecting that
   frame's outcomes. It does not automatically cover ranking already-inspected
   passing frames and selecting their most favourable result. For independent
   U1,U2 ~ Uniform(0,1), define passing as U < 0.5 and coverage as U >= 0.0225.
   Each has conditional coverage 0.955. Selecting the smallest passing value
   gives coverage (0.9775² − 0.5²)/(1 − 0.5²) = **0.940675**. Narrow “whatever
   order” to the intended procedure, or jointly qualify the actual selection
   rule. Per-bound coverage also differs from simultaneous coverage.

2. **Keep calibration and acceptance distinct.** The empirical calibration
   target is 0.955; nominal coverage is 0.95; the independently assessed floor
   is 0.93 under the adopted two-stage rule. Reaching the calibration target in
   simulations is not a population guarantee. Conditional qualification needs
   passing-replicate denominators and a declared stopping/count rule: 1,000 or
   2,000 attempted replicates cannot be substituted for that many passing
   replicates. This is a remaining specification, not a failed completed binding
   run. Synthetic unconditional validation remains as declared.

3. **Check zero-exposure state against the other fields.** An injected A4 row
   with `state_H0c="zero-exposure"` and `fstar_H0c=NaN` is still accepted while
   retaining finite truth 0.508673, finite truth-point LR 1.588575, nontrivial
   status and 114 older units. The original 3/3 summary also passes. `_replicate`
   does not generate a finite truth-point LR for a zero-exposure bound. Enforce
   that cross-field invariant. This is a separate inconsistency from the repaired
   `"bogus"` tag; no corrupted stored ensemble is alleged.

4. **Label the constant-path threshold correctly.** The optimistic Borenshult
   diagnostic gives **2.358361** for constant paths. Full H1 in the same fixture
   gives **2.594364**: at f = 2.5 the constant-path LR is 6.280400 and the H1 LR
   is 5.703123. Thus “H1 finite above approximately 2.4” overstates this diagnostic.
   Report the constant-path threshold under that name or use the H1 engine's
   result. The classification at ceiling 3 and failure to exclude f = 1 remain
   unchanged.

5. **Pool independent-chain MCSEs through their variances.** The linearised
   ratio series is appropriate, but `sd(pooled_z)/sqrt(sum(chain_ESS))` is not
   generally the pooled mean's MCSE. For independent chains of lengths n_i and
   spectral variances S_i(0), use sqrt(sum(n_i S_i(0)))/sum(n_i). For four equal
   chains this is sqrt(sum(var(z_i)/ESS_i))/4. Constant chains contribute zero
   estimated variance; zero observed departures still do not prove zero
   underlying uncertainty.

| Run | R-hat q3 | ESS q3 | Departures / starts | Conditional persistence | Saved MCSE | Corrected MCSE |
|---|---:|---:|---:|---:|---:|---:|
| ext, original | 1.111320 | 415.70 | 101 / 3299 | 0.969385 | 0.004462 | 0.006814 |
| ext, longer | 1.006421 | 1750.48 | 77 / 3382 | 0.977232 | 0.002602 | 0.002617 |
| eo | 1.006707 | 3731.66 | 3 / 3876 | 0.999226 | 0.000447 | 0.000447 |
| zyg | 1.000294 | 3909.27 | 20 / 3788 | 0.994720 | 0.001178 | 0.001178 |

Correcting MCSE preserves the accepted runs' precision, reported rounding and
reproduction-agreement decisions. It matters most for the already-failed short
extant run, whose saved MCSE is about 35% below the corrected estimate. Recompute
summaries/receipts from existing traces; there is no numerical reason here to
regenerate maps.

## Reproducible evidence and scope

`2026-10-31-qualification-repair-check.py` reproduces the selection calculation,
threshold comparison and injected-state fixture against the reviewed model.
It uses a temporary directory and does not modify model outputs. Later repairs
should reject the inconsistent row; that is expected progress, not a reason to
rewrite the historical observation.

`2026-10-31-asr-diagnostics-check.R` runs from `models/pilot-asr` with its locked
environment and rechecks the saved traces, receipts and retention summaries.
`2026-10-31-asr-diagnostics-recomputed.csv` retains the independent calculation.
The R script optionally writes its table to a supplied scratch path.

Q1's next step remains declaring the Libya comparison and then qualifying that
actual design and selection procedure. Q4's persistence conclusion survives;
the wider retention uncertainty is accepted. These bounded corrections should
be integrated before binding qualification and final reporting, without another
unconditional Monte Carlo campaign.
