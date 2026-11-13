# Audit: step 3b science and case bindings

Independent science audit by Codex, 11 November 2026. This is a review note, not a reconstruction
step. Base reviewed: `fca1069`, `3b-paragraph-abstracts.md`, paragraphs M1–M8, R1–R8 and scientific
dependencies in D1/D2/D4/D5. The parent owns draft revisions; this note records findings against that
base, including repairs already being integrated. No analyses were run, and no model, ledger or frozen
product was edited.

**Decision:** retain the analysis and question-led structure. Repair the scope and case descriptions
below before accepting this step. The saved calculations support the numerical findings; they do not
identify historical abundance, individual biological mechanisms or the true recording history.

## Material dispositions

| Paragraph | Finding and narrow repair |
|---|---|
| M4 | “Coverage reaches 0.93” replaces the actual acceptance rule with a point-estimate threshold. Describe independent finite-grid qualification against the 0.93 floor under the adopted lower-bound/two-stage gate, among records passing the potential screen, per declared quantity; abstentions count as non-errors. Exact gate and sources follow below. |
| M5 | Locality–age matching is a grouping rule and independence proxy. It does not establish that all reports from one verified horizon were merged, or that each resulting group is an independent horizon. Say collections sharing the locality–age key count once as proxies. B1's branched axes bearing sporangia and B2's two extant vascular branches are acceptable category descriptions, conditional on the admitted readings. |
| M6 | Keep the explicit one-sided confidence interpretation, fixed recording history and cutoff. Use the greatest possible oldest age together with the **minimum guaranteed count**, rather than midpoints or all possible units. The endpoint is a confidence bound on recognisable record start under the model, not the greatest biologically possible origin. The displayed exposure formula is correct once rendered as mathematical notation. |
| M7 | Finite-sample KS is primary. State that the test conditions on count and the oldest allocated occurrence and uses the remaining transformed ages. Conservative rejection over all allocations requires a fixed independent continuous occurrence model, history, cutoff, timescale, inventory and unit rule, with supports containing the true ages **and inclusion state almost surely**. Realised containment alone does not establish calibration. Put the full support/model conditions in Methods and grouped Conditions rather than repeating them throughout. |
| M8 | Define contrast on the specified-delay contour: candidate lineage age minus assumed delay is the body-record start. The 8–12 and 2.4–4.5 contrasts are the zero-delay cases. Keep the data-selected step explicitly retrospective. Its contour is not a fitted rate or joint confidence region. Exact equation follows below. |
| R1–R2 | Avoid stratigraphic “below the maximum” for the Cambrian packets; name the packets directly. For the Czech comparison, “same characters” must mean the calibration's branching/terminal-sporangium criterion, not demonstrated identical anatomy or crown membership. The 434.1 Ma figure is the **current-scale stage-rule outer value**, not a dated slab or demonstrated crown minimum. |
| R3 | Attach all three values to a hypothetical sustained start at **459.1 Ma**, the primary Murzuq frame and the stated delivery ratio. The 0.091 constant-history limit and 0.184 exposure-weighted mean over bounded variable histories target different quantities. Their product with delivery is local encounter; neither is historical producer abundance. |
| R4 | The ten Darriwilian age supports **extend before** 459.1 Ma; they are not a dated pre-maximum zero sequence. Under the start-at-459.1 scenario, only the part younger than that start contributes modelled spore exposure. Say their contribution depends on the within-stage age treatment, rather than implying that older-than-origin exposure constrains input. |
| R5–R6 | Preserve 469.4 Ma as the finite analysis domain. The 432.4–434.05 Ma unit comparison is for **constant recording**. The 427.31–430.42 Ma values are **primary B2, constant recording**, across the tested deterministic shared-boundary treatments. This is a comparison among tested cases, not an exhaustive geological uncertainty interval or universal ranking of sensitivities. |
| R7–R8 | R7's rate contrasts are zero-delay compatibility scenarios; the 15–23 Myr offsets are **minimum assumed delays** under constant recording, not inferred historical delays. Keep 431.0 Ma visibly pending ledger entry. R8's Oman bound belongs to broader B0, not vascular B2; every one of the **six fixed** B0 histories fails the conditional shape diagnostic. The draft's separate gap statement can be omitted without changing this result. |
| D1–D2 | Replace “size of each route”/“sizes these routes”: the calculations size **aggregate recording contrasts and assumed diagnostic delays**. They do not size geographic occupancy, rarity, tissue effects, deposition or search effort separately. Tissue and size effects need source-specific support or conditional wording; the model supplies no monotonic effect for each trait on preservation, finding and recognition. The unread Kenrick candidate is not supporting evidence yet. |
| D4–D5 | Keep well/formation 0.4 as an **unqualified exploratory contour**. Align the body/KS conditions with M7. Searched-bed effort and macrostratigraphic coverage can help constrain recording; they do not alone make an early aggregate rate identifiable. An eligible positive/zero sampling frame, comparable recovery and geographical/diagnostic assumptions remain necessary. Additional character evidence can change admission to the category, not merely tighten its bound. Peters 2018 remains a candidate source until its content is checked. |

## Qualification: exact current gate and scope

`studies/f3/models/validate.py::lower_limit`, `stage1`, `stage2` supply the numerical rule used by
`qualification_contract.py::assessment`:

- Nominal coverage is 0.95; calibration targets empirical coverage 0.955 on an independent batch.
- Stage 1 takes 1,000 **screen-passing** replicates. A declared quantity passes when its one-sided 95%
  exact Clopper–Pearson lower confidence limit is **strictly greater than 0.93**: at least **944/1,000**
  successful delivered outputs. An upper limit below 0.93 fails (at most 915); otherwise it is borderline.
- A borderline quantity receives the preplanned additional 1,000 passing replicates and passes at
  **1,886/2,000** pooled successes. This is the adopted two-stage gate accounting for the interim look;
  reapplying a single-stage lower limit after pooling is not the rule.
- Every acceptance quantity must pass. Each stage caps attempts at 20 times the required passing
  count. Missing/incomplete or pre-screen numerical-error evidence does not silently pass.

Sources: `studies/f3/models/qualification_contract.py::protocol`, `summarise`, `assessment`;
`studies/f3/models/qualify.py` module contract and `run_cell`; `studies/f3/docs/f3-shape.md`, “Conditional qualification”
and its counter-review amendment. The current saved Murzuq receipt
`studies/f3/models/out/qual/LY-MZ-CU_rho1_accept.json` has `phase=accept`, `result=pass`, `complete=true`,
`target=1000`, `shift=0`, and binds this protocol in `binding.protocol`.

The certificate is marginal per design and declared quantity on a finite scenario grid, conditional on
passing the **potential** screen; abstentions are non-errors. It does not establish universal population
95% coverage, conditional coverage given an informative claim, simultaneous coverage across designs or
coverage for a retrospectively selected favourable design. This qualifies the procedure, not a claim
that the model reconstructs the historical generating process.

## M8 contour, including specified diagnostic delay

Let `A` be the oldest possible admitted body age, `c` the young cutoff, `n` the guaranteed count,
`T` a candidate lineage age, `d` an assumed diagnostic delay and `r` the earlier/later recording ratio.
With constant later recording and the step at `A`, the reported contour is

\[
\left[\frac{A-c}{(A-c)+r(T-d-A)}\right]^n=0.05,
\qquad
r=\frac{(A-c)(0.05^{-1/n}-1)}{T-d-A}.
\]

The reported later/earlier contrast is `1/r`. The definition requires `T-d>A`; otherwise the stored
status is `candidate_not_older_than_envelope_anchor`, with no defined contrast. It is not an exclusion.
For primary B2, `A=426.7`, `c=393.47`, `n=48`. Longer assumed delays reduce the required suppression
within this domain. Source: `studies/f3/models/loop3/frontier.py::contour` and `out/frontier.csv`.

## Exact evidence selectors

| Result | Saved case / derivation selector |
|---|---|
| Age envelope and 428.8/428.5–428.9/431.6 | `loop3/analysis.py::envelope`: possible `max_ma>c`, guaranteed `min_ma>=c`, `A=max(possible.max_ma)`; `endpoint.py::known_cutoff_summary`. `loop3/out/reviewed_bounds.csv`: `category=B2, reading=main, units=locality_age, variant=primary, cutoff=Emsian`, histories `flat`, `pbdb_plant_excluded`, `pbdb_all`, `decline25`; guaranteed 48, possible 50. |
| Murzuq 0.091/0.184/0.910 | `studies/f3/models/out/m2_results.csv`: primary `design=LY-MZ-CU`, `allocation=stage`, `cluster_k=2.0`, `material_type=chart-code`; start 459.1 Ma, `rho=1`, classes `H0c` versus `H0`; `rho=0.1`, `H0c` for 0.910. C24. |
| 10 versus 18 | C45, stage-2 sample-support output. Darriwilian support 469.4–458.2 Ma; under uniform allocation at start 459.1 Ma, the eligible portion is `(459.1-458.2)/(469.4-458.2)=0.080357…` for each such cutting. The other 18 supports are wholly younger. |
| 434.1 outer value | `data/timescale.csv`: Sheinwoodian 432.9 + 1.2 = 434.1; Homerian 430.6 + 1.3 = 431.9 on the current scale. Difference 2.2 Ma current/current, 2.9 Ma versus published 431.2. `studies/f3/docs/audits/2026-11-08-c47-source-check.md`; C47. |
| Unit and timescale cases | C30 `reviewed_bounds.csv`, B2 main `flat`: `region_stage` 19 units gives 432.38; curated oldest set 15 gives 434.05. C50 `out/stage2_timescale/bound_sensitivity.csv`: `category=B2_primary, history=flat`, `all_younger` 427.31 and `all_older` 430.42. Five deterministic treatments, not draws from a geological age distribution. |
| Six-history shape claim | `out/stage2_interval/interval_feasibility_summary.csv`, finite-sample columns, all four B2 inclusion states: pure `decline10` fails throughout; `decline25` has a passing 50-unit witness (p≈0.067), not 49 or 48. Every canonical B0 inclusion state fails all six. The optimised allocations are feasibility witnesses, not estimated dates or adequate fitted histories. C49. |
| Contrasts / delay / half rate | `out/frontier.csv`: B2 main, primary or named coarser `unit_treatment`, `assumed_diagnostic_delay_myr=0`, candidate 444–452 Ma; C48. `out/delay_sensitivity.csv`: B2 `flat`, bound 428.84000595; minimum assumed offsets `T-bound` give 15.16–23.16 Myr; C33. Half-rate stored bound 430.9800119 remains pending ledger entry. |
| Oman and exploratory dependence | C40 canonical B0 `flat` 455.185345419 versus legacy B0 434.5; keep inventory case explicit. C51 well/formation weighting is the unqualified exploratory dependence sensitivity, not a newly qualified 0.4 bound. |

Paths abbreviated `loop3/` above are under `studies/f3/models/loop3/`. The current `estimands.md` age-allocation
section states the full almost-sure support conditions: with support failure probability delta, the
direct size bound becomes alpha + delta; geological ranges have no demonstrated joint coverage. That
condition must travel with any conservative-rejection interpretation in step 3b.

No further scientific tranche is needed for these repairs. Source-dependent character/mechanism
sentences should remain qualified or explicitly pending, rather than being made supported by the
existing numerical claims check.
