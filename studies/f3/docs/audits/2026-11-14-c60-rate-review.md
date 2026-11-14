# C60: independent rate-bound and unit check

Codex, 14 November 2026. Bounded audit of `2735c40`. No production calculation
function was imported, and no numerical output, code, ledger or product was changed.
The parent reviewer owns integration and disposition.

## Independent numerical route

The timescale supplies A = 426.7 Ma, c = 393.47 Ma and L = 33.23 Myr. Starting
from `horizons_reviewed.csv`, I selected eligible-primary B2 rows with the main/all
reading and rebuilt the locality–age and canonical midpoint-stage regional groups.
This gives 50 locality–age groups, of which 48 are certain inside the window, and
19 regional groups. The selected unit ages and member sets agree with the saved
membership table.

For an interval I of width D, let p be its probability among independent finds in
the fixed window [c,A]. Its average finding rate relative to the whole window's
average is p/(D/L). I used the separate beta-quantile identity

`p_lower = Beta_quantile(0.05; k, n-k+1)`

for the one-sided Clopper–Pearson limit, and SciPy's binomial survival function
for P(X >= k). These are independent of the production bisection and direct
binomial summation. For the exponential family I integrated exp(g u) analytically
and solved the share equation with a separate bracketing root solver.

| Interval | n, k minimum | Level share | CP lower share | Lower relative mean rate | P(level) | Largest cutoff/A rate ratio |
|---|---|---:|---:|---:|---:|---:|
| Gorstian–Pridoli | 48, 13 | 0.2130604875 | 0.1682506595 | 0.7896849458 | 0.2079245358 | 1.7640652876 |
| Gorstian–Pridoli | 19, 6 | 0.2130604875 | 0.1474695656 | 0.6921488225 | 0.2025234095 | 2.3649034788 |
| Ludfordian–Pridoli | 48, 13 | 0.1619018959 | 0.1682506595 | 1.0392136461 | 0.0381909508 | 0.8996154681 |
| Ludfordian–Pridoli | 19, 6 | 0.1619018959 | 0.1474695656 | 0.9108575583 | 0.0734251885 | 1.2802638927 |

All four saved rows reproduce at their displayed precision. For the broader
interval the exponential share decreases with g. The narrower interval excludes
the first 1.7 Myr after A, so its share is not globally monotone: it peaks near
g = -0.2647585. There are two roots of the lower-share equation; the production
bracket selects the larger root, correctly giving the **largest** allowed endpoint
ratio. For the 48- and 19-find scenarios the upper roots are -0.0031835048 and
0.0074350353; the other roots are approximately -1.0462953 and -1.1245725. The
0.90 result is thus an upper endpoint, rather than an estimate of a slight fall.

## Unit and other factual checks

- Both intervals contain 13 guaranteed locality–age finds and six canonical
  regional units. Nine are dated only to the Pridoli; the other four are Bathurst
  finds with Ludfordian–Pridoli supports. Positive-length age overlaps permit
  13–16 locality–age finds and six or seven regional units.
- The six regions are Baltica, Gondwana–South America, Kazakhstania, Laurentia,
  South China and peri-Gondwanan Europe. These are pooled finds, not six separate
  demonstrations of the rate bounds.
- The two units setting A are the Ghin Ghin Road and Limestone Road Yea records,
  members `tail:M-ghin-ghin` and `tail:M-limestone-road`. Both have supports
  393.47–426.7 Ma and are absent from the guaranteed late-Silurian count. This
  excludes mechanical membership of those A-setting units, not the selection
  effect from choosing A and the intervals. An actual oldest fossil may still
  be among the 13.
- Independent `2L*expm1(-log(0.05)/n)` calculations give straight-line durations
  4.2800118972, 8.8356557811, 11.3500330660 and 14.6913352425 Myr for n = 48,
  24, 19 and 15, agreeing with C57 and the C60 roundings.
- Spore shares reconstructed directly from document counts are 0.1831275720,
  0.1906693712 and 0.1939953811 in the Gorstian, Ludfordian and Pridoli, versus
  0.5019920319 in the Lochkovian. Exact active-column integration gives zero
  rock area in the Gorstian and Ludfordian, 7074.375 in the Pridoli and
  40163.217 km² in the Lochkovian. The stored Lochkovian value 40160.6 (rounded
  to 40161 in prose) differs by about 0.0065% because it uses the documented
  midpoint quadrature. That difference changes no reading and requires no
  numerical repair under the existing approximation convention.
- The demographic arithmetic illustration is correct: log(2)/log(1.01) is
  69.6607169 years. It makes no estimate of ancient plant population growth.

## Meaning and limits

1. **Lower bound, not a measured plateau.** The primary result says the pooled
   late-Silurian average is not much lower than the whole [c,A] average, under
   the stated fixed-window model. It does not identify the rate immediately
   after A, a constant level, or equality to the later mean. The point estimates
   of the relative means are 1.271 and 1.482 for the two counts. Wording such as
   “was near its later level” should retain its one-sided meaning, for example
   “was not much lower than the later-window average”, rather than implying
   that a narrow interval about one or near-stationarity has been established.
2. **The comparison windows overlap.** “Later mean” here is the average over
   all 33.23 Myr from A to c, including the late Silurian. The exponential factor
   is the rate at c divided by the rate at A. “Across the following 33 Myr” must
   refer to A, not to the end of the late Silurian. Conditional wording such as
   “an exponential increase could be no more than…” avoids implying that an
   actual increase has been estimated.
3. **Retrospective status stays.** For fixed windows, error-free containing age
   supports make the minimum-count lower bound conservative: the true count
   cannot be smaller. But A and both interval splits were selected from the
   observed supports, so these are descriptive fixed-window benchmarks, not
   demonstrated 95% coverage after selection. Independent regional-stage event
   ages remain an assumed counting scenario, not a calibrated dependence model.
4. **No general switch is established.** C57's short durations are properties
   of the specified straight-line/exponential families, with the rise ending
   at A by assumption, a steady later rate and zero delay. C60 does not establish
   that later plateau, so reusing the durations must retain it as an assumption.
   The late-Silurian counts give an interval
   average, mostly from Pridoli supports. Combining them does not determine an
   abrupt change, its timing at A, its biological cause, or a lineage age.
   Labelled discussion of a switch can remain an interpretation; it must not
   become a conclusion that all histories fitting the data switch near A.

**Disposition:** the calculations, counts and conditional duration examples
pass. Support C60's numerical content with the fixed-window/selection conditions
and with a one-sided reading of the late-Silurian average. No numerical output
correction or new scientific calculation is required.
