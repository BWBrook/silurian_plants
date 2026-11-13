# Stage 2 interval-feasibility and shared-timescale audit

**Scope.** Codex implemented the bounded R5/R6 analyses on 7 November 2026. The target is the
conditional-on-maximum shape diagnostic and the conditional upper endpoint of a recoverable fossil
category. Neither calculation estimates a lineage origin, true fossil ages, a preferred recording
history or a probability distribution over geological boundaries. The governing interpretation is
`manuscript/estimands.md`.

## Decisive findings

1. The supplied reviewer's two decisive B2 possible-unit witnesses reproduce. With all 50 units whose
   support intersects the post-Eifelian window, the 25 Myr decline has attainable
   `D = 0.1824472`, asymptotic exact-age `p = 0.07661` and finite-sample exact-age `p = 0.06713`.
   Plant-excluded PBDB effort multiplied by the 10 Myr decline has attainable `D = 0.1866488`,
   `p = 0.06581` and `p = 0.05741`, respectively. The independently reported value of about 0.1185
   was not in the review package and was not reproduced; it was a rough handoff estimate, not evidence.
2. Those counterexamples depend on admitting the two cutoff-straddling B2 units. With only the 48 units
   guaranteed to enter the fixed 393.47 Ma window, the global best 25 Myr-decline discrepancy is
   `D = 0.2032896`: no permitted allocation reaches 5% under either reference distribution
   (asymptotic `p <= 0.04111`, finite-sample `p <= 0.03522`). The PBDB-excluded 10 Myr-decline
   combination is convention-sensitive: best asymptotic `p = 0.05195`, but finite-sample
   `p = 0.04484`. The two singleton 49-unit cases were also evaluated. The pure 10 Myr decline has no
   5% witness under any of the four support-consistent B2 inclusion states.
3. Canonical Oman-inclusive B0 has no 5% witness under any of the six declared histories in any of its
   four support-consistent inclusion states (76, either 77, or all 78 units). The closest is the
   all-possible 25 Myr decline, `D = 0.1967743`, asymptotic `p <= 0.005145`, finite-sample
   `p <= 0.004352`. This is a negative result for the declared conditional-age diagnostic and the
   recorded supports, not proof against every chronology or recording process.
4. Shared timescale uncertainty does not reverse the primary B2 constant or PBDB-history comparison
   with 431.2 Ma. Across the deterministic scenarios, the constant-history bound is 427.31--430.42 Ma;
   after mapping 431.2 to the same perturbed within-Sheinwoodian position, its margin remains
   -3.58 to -0.71 Myr. Under the separate source-rule comparison--shifted current Homerian base plus
   its quoted 1.3 Myr uncertainty--the margin is -4.65 to -0.93 Myr. The two PBDB histories also remain
   younger under both comparisons. The 25 Myr-decline result remains contingent: margins are -0.86 to
   +2.24 Myr under fractional mapping and -1.93 to +2.02 Myr under the source rule. Canonical B0's
   finite bounds remain more than 22 Myr older under either comparison.

## Evidence and methods

### Interval feasibility

For a fixed recording history, ages were transformed to cumulative exposure above the Eifelian cutoff.
Conditional on the allocated maximum, the other `n - 1` transformed ages should be uniform. Each fossil
support becomes an allowed interval for a uniform order-statistic rank. Compatibility of a unit with a
rank is active over one closed interval of possible maximum exposure, with rank support capped to [0,1].
The repository diagnostic enumerates every edge endpoint and every open cell between adjacent endpoints
and solves the resulting bipartite matching. Bisection brackets the global infimum of KS `D` to less than
`5e-11`.
This differs from the reviewer's 61-point maximum-age profile and removes the inference gap between a
failed finite search and interval-wide infeasibility. The decisive reviewer witnesses agree within
`3e-8` in `D`; a few non-decisive cells improve slightly because their gridded maximum was
not globally optimal.

The external review script checked for this reproduction had SHA-256
`28bbcda6923973fef22b71c95f17735009b7f50d648bb2cdbbe0b7f262c96321`; its summary CSV had SHA-256
`40eefaf1ea7b2dcacbb06021e0f59744a538151b085f43068674e74a20e0ddb4`. These external paths and files
are not runtime dependencies; the repository diagnostic contains only the attributed comparison targets.

The two units in each category that straddle the cutoff can fall below it and leave the conditional
sample. All four inclusion masks are therefore enumerated: B2 has 48, either 49, or 50 ages; B0 has 76,
either 77, or 78. An excluded partial unit means its admissible age is below the cutoff, not that the
fossil is removed from the inventory. This closes the gap that would arise from checking only the
all-guaranteed and all-possible values of `n`.

Each cell has a CSV with unit ID, recorded and analysis support, allocated age, maximum/conditional role, rank,
normalised exposure, member count and an explicit support check. The summary reports both the repository's
asymptotic KS reference and the finite-`n - 1` exact-age reference. These p values condition on the chosen
allocation. Optimising the allocation invalidates their interpretation as calibrated p values for a
latent-age search; they are used only to identify a permissible witness or bound the best attainable
exact-age diagnostic. The cutoff remains fixed at 393.47 Ma in this calculation, and its shared-boundary
sensitivity is analysed separately rather than hidden inside independent age jitter.

### Shared geological boundaries

Five deterministic scenarios derive from `data/timescale.csv`: baseline; every boundary one quoted
`base_unc_ma` younger; every boundary one uncertainty older; and two opposite alternating bases.
The alternating vectors are globally scaled to 0.7345 and 0.5610 of the quoted uncertainties so all
stages retain strict order, with a one-percent reserve at the limiting adjacent gap. These are sensitivity
bases, not independent uniforms, Gaussian errors or geological priors.

Each boundary moves once. The same shifted value is used for curated stage-based fossil endpoints, the
Eifelian cutoff, the Darriwilian analysis domain and effort-stage widths. PBDB fossil and effort intervals
move only when both numerical endpoints match project boundaries within `1e-6` Ma: 46 of 56 PBDB
B0 units and 27 of 35 PBDB B2 units meet that rule. Other PBDB numerical supports remain fixed because an
equal number alone does not establish that the source used this ICS boundary system. The same rule is
applied before recomputing raw-collection overlap, stage totals and per-Myr effort. The baseline
reconstruction reproduces every stored global effort total and density within `2e-10`.

The published numerical 431.2 Ma is retained as such and compared in two explicit same-scale scenarios.
First, its fractional position from the Homerian base to the Sheinwoodian base is held fixed. Second, the
source rule is reapplied on the current scale: shifted Homerian base plus the table's quoted 1.3 Myr
Homerian-base uncertainty, giving 431.9 Ma at baseline. The first is a deterministic fractional mapping;
the second preserves the published stage-base-plus-uncertainty construction. Neither is a formal
recalibration or a probability statement about the quoted uncertainty.

The largest primary B2 bound shifts are 1.58 Myr (constant), 1.47 Myr (all-PBDB), 1.45 Myr
(plant-excluded PBDB) and 1.78 Myr (25 Myr decline). Guaranteed counts change from 48 to 47 in scenarios
with an older cutoff because one PBDB support is 393.47--399.5 Ma: only its younger endpoint matches an
ICS boundary, so the interval is correctly held numerical rather than mechanically moved. This count
change is part of the stated support rule, not Monte Carlo variation.

## Failure modes and assumptions checked

- **Identifiability and selection.** Interval matching selects a favourable allocation; it neither
  identifies dates nor assigns histories probabilities. No interval-wide rejection is inferred from a
  failed heuristic search. Negative 5% classifications require exhaustive event-cell infeasibility.
- **Dependence and pseudoreplication.** The work retains the declared locality-age units. It does not
  repair unmodelled dependence among formations, publications or collecting campaigns; unit-definition
  sensitivity remains a separate, consequential result.
- **Observation and ascertainment.** Recording intensity still combines biological occupancy and output,
  diagnosability, delivery, preservation, collection and reporting. PBDB effort is an ascertainment proxy,
  not a measurement of that product.
- **Timescale correlation and non-stationarity.** Shared endpoints are perturbed coherently. Independent
  per-fossil boundary jitter is excluded. The exponential declines retain their declared numerical 10 or
  25 Myr scales and remain retrospective sensitivities.
- **Numerics.** The interval result uses finite event-cell enumeration, sparse maximum matching and a
  recorded double-precision tolerance. Witnesses are rechecked through the existing `shape_check` and
  against every unit's support. Scenario order, boundary magnitudes, mapping rules, effort reconstruction
  and the decisive reviewer witnesses have regression tests.

## Verification and artefacts

- `uv run --with numpy --with pandas --with scipy --with pytest python -m pytest
  models/f3/loop3/test_interval_feasibility.py models/f3/loop3/test_timescale_sensitivity.py -q`:
  **7 passed** after the canonical-inventory rerun and partial-inclusion repair. Both receipts bind
  `horizons_reviewed.csv` SHA-256
  `0cba53e0b70cd1d1cc180c2de3003fc16575b33d280dcd28dd04aefc06671f37` and record
  `canonical_horizons_reviewed` as the validated Oman-membership source.
- `uv run --with numpy --with pandas --with scipy --with matplotlib --with pytest python -m pytest
  models/f3/loop3 -q`: **48 passed**. The first broader invocation omitted matplotlib and stopped during
  collection of the independently owned Murzuq module; adding that module's declared runtime resolved it.
- `models/f3/loop3/out/stage2_interval/interval_feasibility_summary.csv` and the 48 witness CSVs record
  allocations and negative bounds. `partial_inclusion_sets.csv` and `partial_subset_synthesis.csv` expose
  the cutoff-straddling states; `reviewer_reproduction.csv` records the independent comparison.
- `models/f3/loop3/out/stage2_timescale/` records every boundary, unit-age mapping, recomputed effort
  stage, bound and maximum-influence cell.
- Each directory has a JSON receipt binding code, inputs, outputs, environment and interpretive scope.
- The independent audit in `docs/audits/2026-11-07-stage2-interval-review.md` requested no code change.
  It checked the continuum derivation, order and ties, all inclusion masks, witnesses, negative brackets
  and receipt hashes; an independent brute-permutation implementation matched 720 fixed-`D` decisions
  and 120 optimum brackets.

## Residual risks and recommendation

The analysis exhausts the numerical support rectangles currently recorded, not coherent section-level
chronologies that the global unit table does not encode. A support union can therefore admit ages that a
future source-specific ordering would exclude. Conversely, PBDB numerical supports that were held fixed
may derive from an undocumented older or newer timescale. Source-age correlation, biostratigraphic order,
competing Yea chronologies, horizon inference and fossil assignment remain structural uncertainty.

Use the interval results to narrow claims precisely: all-possible B2 does not reject the 25 Myr or combined
history across its recorded supports; guaranteed B2 does reject the 25 Myr history at 5% for this
diagnostic; the combined history depends on asymptotic versus finite-sample reference; the pure 10 Myr
decline and all six canonical B0 histories have rigorous negative 5% bounds under the encoded supports.
Report the timescale scenarios beside unit and recording-history sensitivities, and keep the endpoint
conditional on the adopted category, units, histories and source mapping. The completed independent
mathematical review materially increases confidence in the numerical optimisation without changing the
decision. Further scientific review could still change interpretation by checking the geological
admissibility and source-timescale identity of pivotal allocations, but is unlikely to change the
optimisation conditional on the encoded supports.
