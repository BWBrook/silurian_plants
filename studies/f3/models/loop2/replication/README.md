# QSIM-801 persistent-floor calculation

This directory contains a **model-conditional method calculation**, not an admitted empirical
replication or a qualified fossil-frame exclusion. Vecoli et al. (2017) report 99 cryptospore
taxon-by-sample presence marks in 17 of 20 QSIM-801 samples and no observed trilete spores. The
source does not document microscopy search effort, stopping, recognition checks, or independent
target-detectable units. Those missing observation-process facts prevent empirical qualification.

## Estimand and assumptions

For informative sample \(i\), let \(\theta_i\) be its trilete:cryptospore unit ratio and let

\[
\psi=\min_i\theta_i.
\]

The estimand is the persistent floor \(\psi\), not an arithmetic mean, pooled share, or ceiling on
every sample. The D = 1 calculation assumes:

- every taxon-presence mark proves at least one independently target-classifiable cryptospore unit;
- the observation process would record a trilete with fixed relative effort \(h>0\) whenever it
  records a cryptospore unit;
- target detection remains active throughout the effort that generated the marks;
- the declared floor holds in every informative sample.

At \(h=1\), the model-conditional limit is 0.0307224. This excludes only the hypothesis that the
ratio exceeds 0.0307224 in **every** informative sample under the assumptions. It does not show
that every sample or the pooled land-spore assemblage lies below that value.

## Exact random-denominator argument

Let \(N\) be the actual number of independent target-classifiable units and let the observed mark
count satisfy \(M\leq N\) on an all-zero outcome. Under
\(H_0:\psi\geq\theta_0\), each unit has target probability at least

\[
q_0={h\theta_0\over1+h\theta_0}.
\]

Let \(m_\alpha\) be the first mark count for which
\((1+h\theta_0)^{-m_\alpha}\leq\alpha\). For the rejection event \(R\),

\[
P(R\mid N)
\leq 1\{N\geq m_\alpha\}(1-q_0)^N
\leq\alpha.
\]

Averaging over random \(N\) preserves the level. The mark count therefore need not be fixed. A
control-driven stopping rule also preserves the inequality when target detection remains active on
every observed unit. The proof does not cover asymmetric searches, post-screen selection, or a
target search that covered only part of the effort behind the taxon roster.

The closed-form D = 1 limit is

\[
U={\alpha^{-1/M}-1\over h}.
\]

The script checks this against `count_share.zero_target_stratified_bound`.

## Dependence sensitivities and simulation

D = 2 and D = 4 merely replace \(M\) by \(M/D\) in the exponent. They are labelled heuristic
effective-M sensitivities. No cluster model, intraclass correlation, or all-zero tail result makes
them confidence bounds. In particular, with D = 4, \(h=0.1\), and \(\theta=1\), the zero
probability is 0.09452, so that scenario does not reject a ratio of one.

The 20,000-replicate simulation retains the original 17-stratum design as a toy method stress
because 17 is the number of positive source-table rows. It checks implementation behaviour under
the specified independent Poisson regimes only. It does not qualify the real QSIM-801 observation
frame or clustering assumptions.

## Run and verify

The script carries PEP 723 dependency metadata, so its declared run is:

```bash
uv run models/f3/loop2/replication/qsim_share.py
```

Run the focused tests with:

```bash
uv run --with numpy --with scipy --with pytest \
  python -m pytest models/f3/loop2/replication/test_qsim_share.py -q
```

Outputs are written to `out/`:

- `qsim_share_bounds.csv`: D = 1 model calculation and explicitly heuristic D = 2/4 rows;
- `qsim_share_scenarios.csv`: D = 1 all-zero probabilities;
- `qsim_share_known_answer.csv`: toy simulation cells, each labelled non-qualifying;
- `qsim_share_receipt.json`: source/code/output hashes, pre/post drift check, seed, simulation
  parameters, runtime and package versions.

The private source PDF must be present at `library/closed/vecoli2017.pdf` for the receipt to bind
the inspected source. It is never distributed.
