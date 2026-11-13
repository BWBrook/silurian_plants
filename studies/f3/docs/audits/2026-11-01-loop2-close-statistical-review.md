# Loop 2 close: independent statistical review

Codex (OpenAI; independent methods delegate), 1 November 2026. Review of Loop 2 sprint 2 under
`docs/sprints-loop2.md`, with ownership limited to this audit. I inspected the primary QSIM-801
source and transcription, the declared code and outputs, the sprint notes, the frozen Murzuq
results and the manuscript/claim table. I independently derived the QSIM-801 test and recalculated
its decisive values rather than treating the simulation or test suite as validation.

## Verdict

The repaired QSIM-801 artefact is suitable for handoff as a conditional model calculation,
including when the 99-mark lower bound is random. It is no longer labelled as real-frame
qualification. Loop 2 can close on this statistical workstream only after the parent propagates that
status through the manuscript, claim table and sprint/review records. The source does not document
the target-search effort, stopping rule, recognition protocol or independence needed to interpret
99 taxon-presence marks as 99 target-detectable trials. It supports an exploratory compatibility
calculation, not an `unqualified empirical bound` or headline biological exclusion.

The manuscript also reports the wrong frozen H0c value at 459.1 Ma. The qualified primary row is
0.091, not 0.0955. This remains an independent closure blocker for the parent-owned results and
claim table.

## 1. Scientific target and observation process

The implemented QSIM-801 target is

\[
\psi=\min_i\theta_i,
\]

where \(\theta_i\) is the trilete:cryptospore unit ratio in each informative sample and the minimum
is a persistent floor. The observation consists of 99 cryptospore taxon-by-sample presence marks in
17 of 20 samples and a study-wide statement that no trilete spores were observed. The transcription
matches Vecoli et al. (2017), Table 1: the 17 row totals sum to 99, and the three zero rows are 695.7,
731.6 and 735.1 ft. The source states that 20 samples were prepared by acid maceration, brief
oxidation and 12-micrometre sieving and that the assemblages contained only cryptospores, with no
triletes observed. It does not report slide-traverse effort, specimens counted, a random-counting
rule, stopping, duplicate searches, target-recognition checks or how the occurrence roster was
assembled.

The manuscript's statement that `one examination per sample produced both observations` is
therefore stronger than the source. The defensible observation is that the table and the trilete
statement come from the same paper and stated sample/preparation set. Whether every specimen that
supports a table mark belonged to an observation process in which a trilete had the declared
relative detection probability is unverified.

## 2. What the random-M argument does and does not prove

Let \(N\) be the actual number of independently target-classifiable land-spore units and let the
observed marks satisfy \(M\leq N\) on an all-zero outcome. Under the declared independent Poisson
model, conditional on \(N\), a target has probability at least

\[
q_0={h\theta_0\over 1+h\theta_0}
\]

under the null \(H_0:\psi\geq\theta_0\). Define the rejection event by no targets and
\((1+h\theta_0)^{-M}\leq\alpha\). If \(m_\alpha\) is the first mark count crossing that threshold,
then

\[
P(R\mid N)\leq 1\{N\geq m_\alpha\}(1-q_0)^N\leq\alpha.
\]

Averaging over arbitrary random \(N\) preserves the level. Thus it is not necessary to pretend that
M was fixed, nor to condition on its realised value. A stopping rule driven only by accrued controls
also preserves the inequality if target detection remains active with the stated \(h\) for every
unit. This analytic result is stronger than the limited known-answer simulation.

It does not survive arbitrary ascertainment. Selection of fields, slides, specimens or reported
taxa after screening; different stopping for cryptospore richness and trilete presence; failure to
record common specimens; or a target search covering only part of the effort behind the species
roster all break the link between M and target-detectable \(N\). Such differences cannot be repaired
by merely naming \(h\): a finite bound needs a supported positive lower bound on the effective
target:control effort ratio. If the allowed value of \(h\) reaches zero, the bound is vacuous. The
source does not provide that lower bound.

Sample selection also limits scope. The 20-sample inclusion rule is not reported, so even a valid
conditional calculation concerns the examined QSIM-801 material, not an unbiased draw from the
regional or interval-wide land-spore rain.

## 3. Independent numerical reconstruction and estimand error

For \(M=99\), \(h=1\) and \(\alpha=0.05\), direct inversion gives

\[
U=0.05^{-1/99}-1=0.0307224065,
\]

with recovered target share \(U/(1+U)=0.0298066738\). These reproduce the code output exactly.

This is an upper confidence bound on the minimum \(\psi\), under the model. Its correct reading is:
ratios above 0.0307 in every informative sample are incompatible with the observation at the stated
level. Equivalently, the calculation supports that at least one informative sample is below the
bound. It does **not** show that every sample is below 0.0307, or that the pooled land-spore share is
below 3.0%. Consequently the manuscript phrases `the recovered trilete share is below 3.0% of
land-spore units` and `abundant trilete producers are excluded` exceed the declared estimand. A
trilete-rich assemblage in most samples plus one low-ratio sample is compatible with this floor
test.

A pooled, effort-weighted intensity-ratio estimand can instead be derived by summing independent
Poisson target and control intensities before conditioning on their total. That is a different
model and estimand; it should not be introduced silently, and it still depends on the undocumented
co-ascertainment contract.

## 4. Clustering is not handled by dividing M by an asserted design effect

The rows labelled design effects 2 and 4 are algebraic sensitivity scenarios, not validated 95%
bounds. No cluster definition, cluster-size distribution, intraclass correlation or tail model
connects those numbers to the specimens. A variance design effect does not in general determine the
probability of an all-zero tail, and taxon richness is especially liable to within-sample producer,
facies and slide-field dependence.

Two calculations show why this matters:

- treating the 17 positive samples as the only independent opportunities gives
  \(0.05^{-1/17}-1=0.19270\) at \(h=1\), rather than 0.03072; even independence among samples is not
  established for one core;
- under the manuscript's own design-effect-4 row, \(h=0.1\) and \(\theta=1\) give
  \(P(0)=1.1^{-99/4}=0.09452\), and the reported upper bound is 1.2867. The text nevertheless says
  that \(\theta\geq1\) is excluded for every \(h>0.031\). That statement holds only for the
  independence row and contradicts the declared clustering sensitivity.

The simulation does not repair this gap. It simulates independent Poisson target and control counts
under two chosen richness regimes; it neither simulates the proposed clustering nor validates the
unreported source protocol. Its maximum false-rejection rate of 0.0191 is a result for those cells,
not empirical coverage of the QSIM-801 bound.

## 5. Frozen H0c mismatch

The current `models/f3/out/m2_results.csv` qualified primary LY-MZ-CU row
(`allocation=stage;cluster_k=2.0;material_type=chart-code`, `min_ref=5`, `rho=1`) reports

- `fstar_H0c_459.1 = 0.091`;
- `fstar_H0_459.1 = 0.1835` (rounded to 0.184, not 0.189);
- `fstar_H0c_458.2 = 0.0955`.

The unqualified Loop 2 independent-uniform calculation gives 0.09102964956 and therefore agrees
with the frozen primary H0c result at 459.1 Ma. The value 0.0955 at 459.1 occurs in the
`allocation=pre459` sensitivity row and in the shared-midpoint contamination chronology
(0.09550475812); it is not the qualified primary value. Review 1's claim that 0.0955 equals
`fstar_H0c_459.1` in the frozen CSV is false. Manuscript section 3.1 and claim C04 must be corrected
from 0.0955 to 0.091, with H0 reported consistently from the same primary row. The review audit
should also be corrected so it does not remain a contradictory provenance record.

One related wording error should be fixed at the same time: \(g\) is the indigenous fraction of
reference **encounter intensity**, not the fraction of observed reference positives. The statement
that `under 5% contamination of reference positives defeats` the short window should say that the
declared model flips at \(g=0.9559\), about 4.4% non-indigenous encounter intensity under
\(\kappa=0\) and independent-uniform ages. It is an unqualified sensitivity, not an estimated
contaminant fraction.

## 6. Bounded repair and verification

The statistical implementation was repaired within `models/f3/loop2/replication/` after review:

- `qsim_share.py` now labels D = 1 as a model-conditional independent-unit calculation and D = 2/4
  as heuristic effective-M exponent sensitivities that are not confidence bounds;
- the output estimand is `minimum-sample-ratio-persistent-floor-not-pooled-share`, and the share
  column is `persistent_floor_share_limit = theta/(1+theta)` rather than a recovered pooled-share
  label;
- the 17-stratum simulation is explicitly a toy method stress, with its seed, 20,000 replicates per
  cell and regime parameters recorded; it is not real-frame qualification;
- the receipt binds the source CSV and inspected private PDF, runtime code, all three CSV outputs,
  runtime/package versions and identical pre/post hashes (`input_drift: false`);
- the README gives the exact random-M proof and the observation-process limit.

The focused suite passed 14 tests in 0.65 s. It checks the 99-mark/17-positive-row extraction, the
analytic D = 1 root, minimum-versus-mean semantics, the D = 4 and h = 0.1 non-rejection, invalid
inputs and status separation. The declared script run completed locally in 41.20 s with Python
3.14.4, NumPy 2.5.4 and SciPy 1.18.1. It reproduced the D = 1, h = 1 limit 0.03072 and the toy maximum
false-rejection frequency 0.0191. These checks verify code and declared mathematics, not the missing
microscopy observation contract.

## Recommendation

1. Retain the repaired 0.03072 calculation only as an exploratory conditional result: 99 marks are a
   lower bound on observed cryptospore specimens, and the result follows **if** all marks arose under
   a common, independent target-detectable process with fixed positive \(h\). The model artefact now
   carries this status; propagate it to every parent-owned claim.
2. Maintain the estimand as a persistent-floor/minimum bound, without pooled-share or every-sample
   biological readings. If a pooled intensity ratio is desired, declare and review that alternative
   model explicitly.
3. Treat D = 2/4 only as the repaired output labels specify: heuristic effective-M sensitivities.
   Do not attach confidence-bound language without a cluster model, and do not claim exclusion
   across h scenarios that fail under the displayed dependence scenarios.
4. The revised manuscript source now gives H0c/H0 from the qualified primary CSV and interprets
   \(g\) correctly. Propagate those exact values and statuses to the pending claim table, rendered
   outputs and review trail.
5. Seek the original counting/traverse protocol, laboratory notes or author confirmation before
   promoting QSIM-801 to an empirical exclusion. Independent palynological review would materially
   change confidence because the remaining issue is the undocumented microscopy observation
   process, not numerical implementation. Until then the paper can defensibly present Murzuq as its
   qualified quantitative result and QSIM-801 as a promising but protocol-limited external check.

## Final manuscript-source check

After the parent rewrite, I re-read the statistical methods, results and discussion in
`manuscript/manuscript.qmd` against the repaired replication README. The source now passes the
reviewed mathematical contract:

- QSIM is an exploratory model-conditional minimum/floor calculation, not a mean, pooled share,
  every-sample ceiling, empirical confidence bound or replication;
- the random-M argument states the target-detectable independent-unit condition and sends the full
  proof and its asymmetric-search/stopping exclusions to Supplement S3;
- D = 2/4 are heuristic exponent sensitivities, and the D = 4, h = 0.1 non-rejection is reported;
- the frozen primary 459.1 Ma read-outs are H0c = 0.0910 and H0 = 0.1835, distinguished from
  0.0955 and approximately 0.189 in other read-outs/sensitivities;
- constant-origin and pre-459.1 window hypotheses remain separate; and
- \(g\) is indigenous reference encounter intensity, not a contaminant estimate or fraction of
  positive samples.

I found no residual mathematical overclaim in those manuscript sections. This pass does not cover
the claim ledger or rendered HTML/PDF, which were pending regeneration; Loop 2 statistical closure
therefore remains conditional only on those artefacts agreeing with the checked source. No model
code or outputs changed in this final source check, and the already passing tests were not rerun.

