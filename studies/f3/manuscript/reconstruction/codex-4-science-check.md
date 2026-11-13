# Audit: step 4 science after cuts

Independent Codex review, 11 November 2026, of `4-final-draft.md` at `7e560c5`, compared with the locked
step 3c at `ef253d6`, `estimands.md`, the saved case bindings and current model contracts. This is an
audit note, not another reconstruction step. Only this note was edited; no analyses, ledger changes,
canonical-product changes or figure builds were performed.

**Verdict:** retain the structure and numerical results. The grouped Conditions, pure-decline label,
minimum assumed delays and aggregate-mechanism wording remain scientifically sound. Restore the
following scope distinctions before accepting the display contracts and shortened prose.

## Bounded repairs

| Location at the reviewed commit | Consequential issue | Narrow repair |
|---|---|---|
| Methods (d), lines 127–133 | “Enough older cuttings that all-zero reports would exclude” is only an informal description of frame potential. It no longer says that older outcomes are set to zero for the screen, that the screen evaluates full older exposure, or that precisely this screen is applied in every simulated replicate. “Independent simulations” also leaves independence from calibration unstated. | Restore: “The potential screen uses a usable younger reference and sets older reports to zero, testing constant reference-level input with all older cuttings exposed; the same screen is applied to every simulation. Acceptance simulations are independent of calibration.” Retain the finite-grid, per-quantity qualification and abstentions-as-non-errors text. The actual analysis uses all actual outcomes. |
| Introduction, lines 82–84 | The theoretical count–precision statement dropped the **fixed younger cutoff** condition retained in step 3c. Increasing count while moving the cutoff is not covered by the stated monotonicity. | “For a fixed oldest find, younger cutoff and recording history, more independent finds narrow the bound …”. |
| Figure 2, lines 380–385 | The caption starts with a conditional one-sided 95% bound, then moves the same `T` using the step without identifying the data-selected step as retrospective. The final “older ancestors therefore need” is an unrestricted necessity statement, although the calculation holds the unit rule, cutoff and specified recording/delay construction fixed. | Distinguish the fixed-history confidence calculation from the retrospective step/delay contour. For example: “In the retrospective step scenarios, lower earlier recording moves the compatibility endpoint older; an assumed delay connects body-record start to candidate ancestor age. These scenarios describe how ages older than the chosen bound can be accommodated.” Do not imply nominal or selection-adjusted 95% coverage for the selected step. |
| Figure 4(a), lines 395–398 | The caption calls the displayed inventory “the 48 … units”; the primary inventory has **50 possible units and 48 guaranteed** at the cutoff. The endpoint uses the latter count with the oldest possible age from the former set. | Prefer “50 possible locality–age units, 48 guaranteed within the window” if all age bars will be shown. Alternatively explicitly state that only the 48 guaranteed units are plotted and identify the two cutoff-straddlers omitted. Declare the plot's actual unit set before rendering. |
| Figure 4(b), lines 398–401 | The standalone legend labels the curves retrospective and gives the age-minus-delay domain, but still leaves their fixed unit treatment and constant-later-rate construction implicit. “The contrast … requires” can be read as an estimated or universal biological necessity rather than the equality contour for that scenario. | Name the unit treatment(s) drawn and the flat later rate, step at the oldest possible age, and 0.05 endpoint contour. Describe plotted ratios as retrospective compatibility contours, not fitted rates or a joint confidence region. For primary units, the count is 48 and cutoff 393.47 Ma. Where curves use other units, label their own counts and anchors. Actual delay values must be labelled on the curves or in the legend. |
| Discussion, lines 280–281 | “Recording contrasts and delays … at each maximum” implies that the 515.5 Ma maximum has a quantified recording/delay requirement. The paper expressly says the assembled M1 frame cannot provide one. M2 supplies encounter limits; the body contrasts/delays belong to M3/B2. | “We make the observational requirements of these maxima explicit, quantifying local spore-encounter limits and body-recording/delay scenarios where the published frames permit.” Preserve the distinction between the qualitative M1 audit, local M2 limits and B2 frontiers. |

The same scenario qualifier should govern the new “need/require/demand” language in the Introduction,
Results (g), Discussion and legends. The wording is defensible for the stated vascular candidates,
units and 0.05 compatibility construction; it does not establish that these processes actually occurred
or exhaust every possible history. This does not reopen the adopted main-message choice. In the
Conclusion's opening, “an **absence-based** fossil maximum” is the precise scope already used in the
Introduction and at the end of the Conclusion.

## Exact evidence and case checks

- **Potential screen:** `studies/f3/models/m2.py::potential` sets declared older/transported outcomes to zero.
  `screen` tests `H0c`, `f=1`, at the far domain edge where every older unit is exposed, against the
  unshifted count-matched critical value. `designs/m2.toml`, `[screen]` and `amendment_1`, require the
  identical amended rule for data and each replicate. Screening on realised older outcomes would be a
  materially different selection rule.
- **Qualification:** `validate.py::stage1` requires a one-sided 95% exact lower limit strictly above
  0.93, at least 944/1,000 screen-passing replicates. A borderline quantity uses `stage2`'s preplanned
  1,886/2,000 pooled rule. `qualification_contract.py::protocol/assessment` fixes per-quantity marginal
  false-claim control among potential-screen-passing replicates with abstentions as non-errors, on
  the declared finite grid. The shortened account should not imply universal 95% coverage or coverage
  conditional on an informative claim.
- **Counts/envelope:** C25/C40 and `loop3/analysis.py::{select_records,envelope}` give primary B2
  `reading=main, units=locality_age, variant=primary, cutoff=Emsian`: 50 possible (`max_ma>393.47`),
  48 guaranteed (`min_ma>=393.47`), oldest possible 426.7 Ma. C27/V003, `history=flat`, gives
  428.84000595 Ma. The displayed formula and minimum-count/maximum-age rule remain correct.
- **Unit alternatives:** C30 `region_stage`, 19 units, `flat`, gives 432.38 Ma; `curated_tail_only`,
  15 units, gives 434.05 Ma. The nearby 432–434 Ma sensitivity correctly prevents the 429 Ma result
  from standing as an unconditional origin bound. The tested stage-boundary extrema remain the
  primary B2 constant-history deterministic cases C50/V062–V063, not a probability interval.
- **Frontier:** C48, `loop3/out/frontier.csv`, and `frontier.py::contour` define
  `r=(A-c)(0.05^(-1/n)-1)/(t-d-A)`, with `t-d>A`; the later/earlier contrast is `1/r`.
  Curves are equality contours under a fixed unit rule and assumed delay, not fitted historical
  rates. Primary zero-delay 444 and 452 Ma candidates give 8.084 and 11.822; coarser/curated cases
  span 2.355–4.458. C33's 15–23 Myr are minimum assumed offsets from the constant B2 endpoint.
  C53/V108's half-rate illustration remains the B2/main/primary/flat row, break 426.7, multiplier
  0.5, endpoint 430.9800119 Ma. No case changed in this edit.
- **Shape/Conditions:** C49's pure decline10 fails over all four B2 inclusion states; this does not
  apply to the combined plant-excluded-density × decline10 history, which has passing 49/50-unit
  witnesses. The revised pure label, 25 Myr witness-versus-universal-failure distinction, 469.4 Ma
  finite domain and probability-one support/inclusion condition all survive the cuts. All canonical
  B0 histories fail the stated diagnostic; this is not rejection of biological histories generally.
- **Spore inputs:** C24 still distinguishes constant input from the exposure-weighted mean of
  bounded variable histories in the primary Murzuq shared-well model at start 459.1 Ma. The
  exploratory 0.0995, approximately 0.4 and C07 leave-well contours remain correctly labelled
  unqualified in Conditions, with their different targets identified.

The figure contents have not been built, so this accepts no rendered plot or exact graphical encoding.
One focused read of the repaired phrases and legends is sufficient; no new science tranche is needed.
