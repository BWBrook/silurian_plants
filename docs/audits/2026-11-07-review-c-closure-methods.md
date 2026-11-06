# Review C closure: independent methods and numerical audit

Codex specialist delegate (sol_high_specialist; configured GPT-5.6-sol/high), 7 November 2026.
Bounded review of repository `1067c88`, with
`manuscript/claims.csv` read again after the contemporaneous history-stamp repair. I changed no
analysis, data, manuscript, claim or frozen output. All numerical reproductions below were direct
in-memory calculations from the held inputs; no R analysis, remote job or output-writing entry point
was run.

## Decision

**Support C24, C28, C33 and C40 after the qualifications already attached to them. Support the
calculations in C31 and C41, but repair their description before promoting them: the reported
age-allocation intervals are 5th--95th percentiles, not full ranges, and the KS probabilities are
asymptotic p-values conditional on treating each imputed age as exact.** C40 must call 452.8 Ma the
Oman unit's **oldest possible age**, not its age or an observed first appearance.

The Oman result is a declared category and age sensitivity. It has no binding empirical coverage
qualification and does not estimate embryophyte origin, a biological lag, a preservation delay or a
clock age. The augmented sequence fits every declared recovery history poorly; this weakens the
scientific interpretation of the corresponding model-conditional endpoint rather than invalidating
the closed-form calculation.

## Target, data-generating claim and computation

The estimand is the older endpoint of a **recoverable B0 body-record process**, conditional on a
fixed recovery history, independent locality--age units, a known younger cut-off and the number of
guaranteed units. It is not the origin of Embryophyta. Given cumulative recovery exposure \(U\),
cut-off \(c\), oldest possible occurrence age \(m\), \(n\) guaranteed units and one-sided
\(\alpha=0.05\), the calculation is

\[
U(T_{0.95})=U(c)+\{U(m)-U(c)\}\alpha^{-1/n}.
\]

The observation and admission steps remain distinct:

- `S-w22-K12` records dispersed spores, spore masses and spore-filled sporangial fragments from
  Ghaba-1. The main and inclusive reading tables assign it to the Katian. The project timescale maps
  that stage to 452.8--445.2 Ma (old to young).
- The sensitivity admits those fragments as one B0 locality--age unit. It does not admit them to B1
  or B2, and it does not count 12 fragments as independent observations.
- The source and membership audit beside this one finds K12 to be the sole admitted pre-Silurian E2
  mesofossil in the present inventory. At the reviewed state its `main`, `inclusive` and `outlier`
  rows are all Katian. The numerical guard does not robustly require the first two readings: it tests
  strict-subset relation (`set(reading_id) < {"main", "inclusive"}`), so a set such as
  `{"main", "other"}` would pass. It also does not establish fossil identity, accepted land-plant
  affinity, sample independence or recovery-channel comparability.
- With the Emsian cut-off, the main frozen inventory has 75 guaranteed of 77 possible units. Adding
  Oman gives 76 guaranteed of 78 possible units. The hard-coded range is therefore used once in the
  count and uses 452.8 Ma only as the conservative oldest possible age.

This separation is essential because the Oman material came from palynological preparation, whereas
the recovery proxies are dominated by macrofossil collection. Treating the admission as a declared
sensitivity is defensible; treating it as a newly qualified empirical result is not.

## Independent results

### Endpoint claims C28 and C40

I reconstructed cumulative exposure and its inverse independently of `endpoint.py`, then applied the
formula above to the main-reading Emsian rows. Agreement with the stored CSV was within
`4.2e-9` Ma, the scale expected from its eight-decimal serialisation.

| Inventory | n | Oldest possible (Ma) | Constant | PBDB | Plant-excluded | Decline25 | Decline10 |
|---|---:|---:|---:|---:|---:|---:|---:|
| frozen E3--E5 tail | 75 | 432.9 | 434.50683364 | 436.37553200 | 435.73207857 | 437.15614611 | beyond 469.4 |
| plus Oman fragments | 76 | 452.8 | 455.18534542 | 456.62218261 | 456.08944908 | 465.20908134 | beyond 469.4 |

Against the certain cryptospore minimum of 458.2 Ma, the frozen bounded endpoints differ by
21.04--23.69 Myr. The augmented endpoints differ by 3.01, 1.58 and 2.11 Myr under constant, PBDB and
plant-excluded histories; decline25 lies 7.01 Myr older than the spore minimum. These are conditional
endpoint comparisons, not observed elapsed times. C28 and C40 report the rounded values correctly.

The Oman script's frozen guard merged 48 baseline **output cells**: two readings by four cut-offs by
six histories. This is not a 48-record fossil inventory. At the reviewed state all 48 cells match
`reviewed_bounds.csv` to its stored eight decimals. The implementation's phrase "exactly" is stronger
than its check: it applies default-tolerance `np.allclose` only to `older_bound_ma`, without requiring
exact equality of counts, statuses or oldest ages. Either call this a 48-cell floating-point match or
tighten the guard before claiming exact baseline identity. This does not change the present result.

### Shape claims C31 and C41

I independently transformed ages to recovery exposure, conditioned on the sample maximum, and ran
SciPy's asymptotic one-sample KS calculation. I replayed only the declared 256-draw seed stream. C41
matched the stored values to at most `3.4e-13` in p; C31 reproduced:

- B2 constant recovery: midpoint `0.00848083`; independent-uniform 5th--95th percentiles
  `0.0730803--0.764863`; shared-quantile 5th--95th percentiles
  `3.12387e-9--0.0164679`;
- B2 decline10: midpoint `3.08620e-13`; independent-uniform 5th--95th percentiles
  `2.16731e-11--8.41441e-7`;
- frozen B0, constant: midpoint `0.00656570`; independent-uniform 5th--95th percentiles
  `0.00413291--0.0623803`;
- B0 plus Oman, constant: midpoint `5.53558e-12`; independent-uniform 5th--95th percentiles
  `5.23977e-13--5.18771e-9`.

These are not full ranges. For example, the 256 constant-recovery draws span
`0.01225--0.91764` for B2, `0.00170--0.09927` for frozen B0 and
`3.75e-14--2.91e-8` for B0 plus Oman. The current rounded intervals are therefore numerically right
but must be named **5th--95th percentiles across 256 allocations** wherever they are described as a
range or as spanning all allocations.

The p-values are also not exact finite-sample KS probabilities: `shape_check()` explicitly requests
`method="asymp"`. "Exact-age" in the existing limit means conditional on treating an imputed age as
known exactly. A precise label is: **nominal asymptotic KS p-value conditional on exact imputed
ages**. Neither the percentile interval nor the midpoint test is a combined test for interval-dated
fossils, and no recovery model is selected by these diagnostics.

For the augmented B0 inventory, the largest main-reading 95th-percentile p-value among all six
declared histories is `0.000849` (decline25); the other histories are smaller. Thus the statement
that every declared history fits the augmented sequence poorly is supported for the main reading.
Inclusive-with-Oman diagnostics are also poor, but they are a separate inventory containing the
Hirnantian Zbrza unit and should not be used silently to qualify the main-reading claim.

### C24 and C33 arithmetic

The four primary Murzuq rows at 459.1 Ma give:

| delivery rho | H0c f | rho x f | H0 f | rho x f |
|---:|---:|---:|---:|---:|
| 1.00 | 0.0910 | 0.091000 | 0.1835 | 0.183500 |
| 0.50 | 0.1821 | 0.091050 | 0.2576 | 0.128800 |
| 0.25 | 0.3641 | 0.091025 | 0.4211 | 0.105275 |
| 0.10 | 0.9103 | 0.091030 | 0.9207 | 0.092070 |

C24 correctly confines the nearly invariant product to H0c and retains the delivery--producer
trade-off. The rows mark H0c, H0m, H0 and H1 as qualified for this primary design; no claim for a
different design or transport variant follows.

The constant-recovery B2 endpoint is `428.84000595` Ma. Direct subtraction gives minimum assumed
offsets of 15.16 Myr to 444 Ma, 18.16 Myr to 447 Ma and 23.16 Myr to 452 Ma; adding 20 Myr gives
448.84000595 Ma. C33's rounded 15--23, 18 and 448.84 values are correct. They remain assumed offsets
from a one-sided endpoint, not fitted delays.

## Receipts, failure modes and recommendation

All 13 input/output bindings in `analysis_receipt.json` and all 11 in `oman_receipt.json` match the
current bytes. The independent endpoint reconstruction, seeded shape reconstruction and arithmetic
checks above used those same bound inputs without invoking either output-writing `main()`.

The dominant failure modes are structural, not numerical: one admitted unit controls the endpoint;
age allocation controls the apparent adequacy of constant recovery; locality--age proxies may retain
dependence; the Oman and main body channels have different recovery processes; and fixed histories
are neither identified nor selected by these data. There is no optimiser or convergence issue in the
closed-form endpoint calculation, but correct arithmetic cannot repair recovery-model
misspecification or confer empirical coverage.

**Recommendation:** promote C24, C28, C33 and C40 after changing "oldest" to "oldest possible" in
C40. Promote C31 and C41 only after naming the reported intervals as 5th--95th percentiles of 256
allocations and naming the p-values as asymptotic conditional diagnostics. Keep all six claims
model-conditional; do not attach empirical qualification to the Oman sensitivity. Independent
scientific review has already materially improved the interpretation; another independent numerical
review would be unlikely to change these decisions unless the source admission, age assignment, unit
construction or recovery histories change.
