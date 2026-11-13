# Audit: step 3c science and exact cases

Independent Codex audit, 11 November 2026, of `3c-full-draft.md` at `c0f83fc`. This is a review note,
not another reconstruction step. Focus: Methods (d)–(h), Results, Conditions and their immediate
interpretation. No model runs or edits to the ledger, evidence, canonical products or draft. A scalar
closed-form calculation independently checks C53. The parent owns integration.

**Verdict:** the principal values and primary scenarios are supported, including the newly bound
half-rate example. The draft needs the repairs below before science acceptance. The largest error is
the Discussion converting the 429 Ma confidence bound into a historical beginning.

## Material repairs

| Location in the reviewed commit | Finding | Narrow repair |
|---|---|---|
| Discussion, lines 249–254 | “The … body record begins near 429 Ma” states an estimated event date; C27 is an older confidence bound conditional on a fixed recording history. This is expressly prohibited by `estimands.md`. | “Under constant or collection-density recording histories, the recognisable crown vascular-plant body record has a one-sided 95% older bound near 429 Ma.” Keep the alternative-unit result nearby as already provided in Results. |
| Methods (g), lines 160–164; Conditions, lines 288–294 | The maximised finite-sample diagnostic is correctly described, but “supports that contain each true age” loses the observation-model probability-one condition. The direct size argument is not justified by conditioning after the fact on realised containment. Geological age ranges have no demonstrated joint coverage. | State that conservative rejection requires support/inclusion containment **almost surely under the observation model**, with the history, cutoff, timescale, inventory and unit rule fixed. If containment failure has probability delta, the direct bound is alpha + delta; do not imply that delta is known here. State that simultaneous geological coverage has not been demonstrated. Berger–Boos is related, rather than the justification for treating these supports as error-free. |
| Methods (d), lines 126–129 | The lower-confidence-limit gate is correct at stage 1. “Preliminary screen” and unspecified “coverage” omit two consequential parts of the certificate: the **potential** screen and the fact that abstentions count as non-errors. The acceptance batch is independent of calibration, marginal per declared quantity. | Name independent acceptance among potential-screen-passing replicates, per declared quantity, with abstentions as non-errors. Keep the finite-grid restriction. The second stage uses its preplanned pooled threshold, not a new application of the stage-1 confidence limit. Exact contract below. |
| Spore Conditions, lines 281–284 | C51/V058 = 0.0995 also sets frailty shape to infinity: it removes frailty while fitting separate well reference rates. It is not a one-factor change from the primary Gamma(2,2) shared-well model. All these retrospective dependence and leave-one-well cases are unqualified; the current grammar assigns that label only to the block contour. | Call it the “separate-well-rate, no-frailty contour” and identify the whole set of retrospective comparisons, including C07, as unqualified. Distinguish the qualified primary model from these comparison contours. |
| Results (e), lines 217–219 | “The 25 Myr decline passes with all 50 …” can read as adequacy across age assignments. The saved p = 0.067 is the best attainable finite-sample witness, not a probable chronology or demonstration that the history fits the unknown true ages. | “With all 50 possible units, an admissible allocation gives p = 0.067; no allocation passes with the 48 guaranteed units (best p = 0.035).” The failure statement is stronger than a witness non-rejection and should remain so. |
| Results (h), lines 242–244 | The age-support gap is real, but “because” presents the gap alone as the proved cause of failure under six differently weighted models. The certificate concerns the complete admitted sequence and model, not a gap-only test. | Separate the statements: the sequence contains an isolated Katian unit and fails all six fixed-history diagnostics. The gap need not be retained to communicate the result. |
| Evidence that would sharpen inference, lines 300–302 | An enumerated older marine sequence alone supplies an opportunity count, not a calibrated absence probability: comparable recovery, reference encounter and the delivery/recognisability assumptions remain necessary. | Say it would **help quantify** a conditional absence argument when those opportunities and observation assumptions are documented; do not promise that enumeration alone settles M1. |

One source-scope dependency remains outside this saved-case audit: the Introduction qualifies pre-latest
Silurian scarcity of terrestrial deposits by western Europe (lines 60–61), while the Discussion drops
that geographical qualification (lines 257–258). Preserve the qualification unless the source audit
supports the broader statement. Newly read literature claims were not independently re-audited here.

## C53 / V108: confirmed against the actual evidence

`studies/f3/manuscript/value-bindings.csv`, V108, selects exactly one row of
`studies/f3/models/loop3/out/suppression_sensitivity.csv` (CSV line 79):

| Field | Saved value |
|---|---|
| category / reading / inventory | `B2` / `main` / `primary` |
| unit rule | Primary `locality_age`; `suppression_sensitivity.py` calls `analysis.select_records` with this default |
| baseline / break / older multiplier | `flat` / `426.7` Ma / `0.5` |
| guaranteed / possible / oldest possible | 48 / 50 / 426.7 Ma |
| older endpoint / status / domain | 430.9800119 Ma / `bounded` / 469.4 Ma |
| interpretation | Retrospective 0.05 endpoint sensitivity; no nominal or selection-adjusted confidence claim |

C53 is `supported` and stamped `813b43c`, which is an ancestor of the reviewed commit. The stamped
and current CSV Git blobs are identical (`30973f9a11e85bdd4d3e0f88bb66cec1b8f1bbb0`). The current
SHA-256 is `f772e4436eb1113d89c750b0f2d02029a0ac712651a9612dc9b260f7b424ad2c`, matching
`out/suppression_receipt.json`. The receipt binds the relevant model, timescale and reviewed inputs.

With `A=426.7`, `c=393.47`, `n=48`, earlier/later rate `r=0.5`, the scalar check is

\[
E=(A-c)(0.05^{-1/n}-1)=2.14000594858,
\quad T=A+E/r=430.98001189716\ \mathrm{Ma}.
\]

This agrees with the saved row and rounds to the V108 rendering, 431.0 Ma. No observed age support
extends above this data-selected break. The example demonstrates compatibility under the specified
step; it is not an estimated past recording rate, a necessary threshold or selection-adjusted 95%
inference.

## Other case checks and the acceptance contract

- **Methods (e)–(f):** locality–age keys are correctly called proxies. The canonical counts are
  B0 78/76, B1 71/69 and B2 50/48 (possible/guaranteed). `analysis.py::envelope` takes
  `A=max(max_ma)` over possible units and the count with `min_ma>=c`; the displayed fixed-history
  exposure formula is correct.
- **Methods (h), Results (g):** the contour correctly targets candidate age minus assumed delay,
  requires `t-d>A`, and remains retrospective. C48's 8–12 and 2.4–4.5 cases have zero assumed delay.
  C33's 15–23 Myr values are minimum assumed offsets from the constant B2 endpoint, not inferred delays.
- **C24/C45/C09:** primary `LY-MZ-CU`, stage allocation, Gamma(2,2) well effects, start 459.1 Ma:
  H0c/rho1 = 0.091, H0/rho1 = 0.184 (a different, exposure-weighted estimand), H0c/rho0.1 = 0.910.
  The Darriwilian supports extend before the maximum, but only their postulated-post-start portion
  contributes; shared midpoint allocation gives none at this start. The revised Results wording is correct.
- **C49:** use `out/stage2_interval/interval_feasibility_summary.csv`, finite-sample columns.
  `B2_possible/decline25` has p = 0.06713; `B2_guaranteed/decline25`, 0.03522. Pure decline10 fails
  over all four B2 inclusion states; all six fixed histories fail over all canonical B0 states.
  The 469.4 Ma bound domain is correctly retained; failure to reach a bound by that endpoint is not
  unboundedness over all geological time.
- **C30/C50/C52:** the unit, deterministic shared-boundary and Yea-removal figures are correctly
  attached to constant recording. The quoted timescale extrema are `B2_primary/flat/all_younger`
  (427.31) and `all_older` (430.42), not a probabilistic geological interval.
- **C51/C07:** `stage2_murzuq/dependence_sensitivity.csv`, `independent/inf/True/no exclusion`, gives
  0.0995125220; `well_formation/2.0/False/no exclusion`, 0.3930024633. C07's 0.1850–0.3646 is the
  older engine's **H0 exposure-weighted** five-well-deletion sensitivity, not this script's H0c range.

Qualification sources are `studies/f3/models/validate.py::{lower_limit,stage1,stage2}` and
`qualification_contract.py::{protocol,assessment}`. Stage 1 requires the one-sided 95% exact lower
limit **strictly above 0.93**, at least 944/1,000 screen-passing replicates. Borderline quantities get
the preplanned second 1,000 passing replicates and need at least 1,886/2,000 pooled successes. Calibration
targets 0.955 independently; the nominal level is 0.95. Abstentions are non-errors. The finite-grid,
per-quantity certificate does not supply universal 95% coverage or coverage conditional on an
informative claim. The primary Murzuq acceptance receipt reports complete/pass under that contract.

Minimal self-contained model/screen wording, checked against `m2.py::{potential,screen}` and S2.2:

> The primary likelihood jointly profiles the reference encounter hazard and older input, integrating
> a mean-one Gamma(2,2) effect shared by older and reference cuttings within each well; cutting outcomes
> are independent conditional on that effect and their latent ages. The potential screen requires a
> usable younger reference and enough older exposure to exclude constant reference-level input when
> all older cuttings are exposed and their outcomes are set to zero; the same screen is applied in
> every simulation.

The zeroing is essential: the screen evaluates frame potential rather than selecting the observed
older outcomes. The full analysis still uses every actual outcome.

These are bounded wording and scope repairs. They require no new model runs or evidence changes.
