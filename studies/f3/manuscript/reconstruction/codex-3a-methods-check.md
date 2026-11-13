# Step 3a: Methods, Results and persistence check

Codex, 10 November 2026, against draft `9e42e71`. This is a bounded review note. Only this file was
edited; the ledger, models, saved outputs and frozen manuscript remain unchanged. No analysis was rerun.

## Verdict

**Repair the named objects and cases, then accept this outline.** The displayed numerical results
match the saved cases. Compression has changed several meanings: the primary age-envelope rule,
verified-horizon status, the domain of an absent bound, the two Murzuq targets and the attribution of
the persistence result. These are local repairs, not grounds for another modelling tranche.

## Required repairs

| Draft passage | Finding | Compact repair |
|---|---|---|
| “Units are locality–ages, so each horizon counts once” | A locality–age is a proxy built from named/coordinate and formation/age keys; it is not a verified bed or horizon. C25 explicitly retains this limit. | “Each locality–age proxy counts once.” Keep the unverified-bed condition in the grouped assumptions. |
| “crown vascular-plant members…supply 48 units” | There are 50 possible units and 48 guaranteed within the Emsian-cutoff window. | “The crown-member category has 48 units certain to lie in the window.” |
| “Interval-dated units enter at their oldest possible age” | The envelope uses the greatest possible oldest age and the minimum guaranteed count. It does not assign every fossil to its oldest endpoint or count every possible unit. | “For age ranges we combine the greatest possible oldest age with the minimum count guaranteed inside the window.” |
| The rendered-text form `0.05^−1/*n*^` | The intended formula is correct but the source syntax is ambiguous. Define its cutoff and cumulative exposure explicitly. | Use the TeX expression below. |
| “a 10 Myr decline leaves the start open” | The output is `beyond_domain`, through 469.4 Ma, not an unbounded-age conclusion. | “The 10 Myr decline gives no bound within 469.4 Ma.” |
| “that decline combined with density” | The sixth history is specifically plant-excluded density multiplied by the 10 Myr decline. | Name that combination once; the six fixed histories are listed below. |
| “constant producer intensity…reaches at most 0.091…0.184 under exposure weighting” | These are upper compatibility limits under different classes: constant H0c and variable-path H0 exposure-weighted mean. The second is not a reweighting of the same constant parameter. Neither is measured historical abundance. | “At 459.1 Ma and equal delivery, upper compatibility limits are 0.091 for constant encounter and 0.184 for an exposure-weighted mean over bounded variable histories.” |
| The Czech anchor “gives 434.1 Ma under that rule” | The number is a current-scale stage-base-plus-uncertainty outer value. The Irish published 431.2 uses GTS2012, while the fertile Czech horizon is correlated. | “Applied on the current timescale, the Czech Sheinwoodian anchor gives an outer value of 434.1 Ma.” |
| “Candidate ancestors…need earlier recording 8–12 times lower” | C48 quotes the data-selected flat-plus-step case at zero assumed diagnostic delay. | Add “with zero assumed diagnostic delay”; retain the retrospective-step condition. |
| “recognisable bodies 15–23 Myr after the ancestor” | C33 is an assumed minimum offset at the constant-history one-sided endpoint, not an estimated delay. | “Under constant recording, minimum assumed delays of 15–23 Myr provide an alternative route.” |
| “Simulations reproduce nominal coverage…when assumptions hold” | C34 reports matched exact-age simulation results, rather than qualification of the historical fossil record or a new uniform guarantee. | “Matched exact-age simulations gave coverage 0.941–0.958.” |
| “stage-boundary shifts give 427.31–430.42” | C50 is the range over five deterministic tested scenarios. | Say “tested shared-boundary scenarios”. |
| The 10 Myr shape failure and “every recording history” for Oman | The relevant sets are the pure decline 10 history and the six fixed histories. The combined density×decline 10 can pass for B2; arbitrary/post hoc step histories are outside this six-history certificate. | “The pure 10 Myr decline fails…; with Oman, all six fixed histories fail the conditional-age diagnostic.” |
| The 0.4 well-block “limit” | C51 is an unqualified inverse-block-size composite sensitivity. It does not inherit the primary model’s coverage qualification. | “Block weighting gives an exploratory comparison contour near 0.4.” |
| “persists…0.977 under Hooper et al.’s fitted models” | C19 is this project’s Claude-led stochastic-map reanalysis, checked by Codex, of Hooper’s deposited data. The number comes from the extant-tree equal-rates aperture maps, conditional on a trilete start and the coding, model, tree and dated chronology. | Use the attribution and scope below, or omit the number from this compressed outline. |

The Methods paragraph can keep the formula self-contained in very few words:

> For independent units above fixed cutoff $c$, define $U(a)=\int_c^a w(s)\,ds$. The 95% older bound
> solves $U(T)=U(A)0.05^{-1/n}$. For interval ages, $A$ is the greatest possible oldest age and $n$ the
> minimum guaranteed count.

Use ordinary spacing around the mathematical spans when integrating this suggested wording.
The conditional meaning is the declared fixed recording history, independent units, adopted
timescale and true ages contained in their intervals. A retrospective step is an additional
compatibility scenario rather than a nominal, selection-adjusted 95% procedure.

## Exact evidence cases

### Primary body envelope and finite domain

`studies/f3/models/loop3/analysis.py`, `envelope`, selects `max_ma > cutoff`, counts only `min_ma >= cutoff`
and passes the largest possible `max_ma` plus that count to `known_cutoff_summary`.
`studies/f3/models/loop3/endpoint.py` inverts the maximum order statistic under a fixed recording density.
`histories.py` fixes `YOUNG=393.47` and `DOMAIN=469.4`.

In `reviewed_bounds.csv`, select:

`category=B2; reading=main; units=locality_age; variant=primary; excluded_region=""; cutoff=Emsian`.

| History | Possible / guaranteed | Oldest possible (Ma) | Bound(Ma) | State |
|---|---:|---:|---:|---|
| flat |50 /48 |426.7 |428.84000595 | bounded |
| pbdb_all |50 /48 |426.7 |428.87982431 | bounded |
| pbdb_plant_excluded |50 /48 |426.7 |428.45494734 | bounded |
| decline 25 |50 /48 |426.7 |431.62788677 | bounded |
| decline 10 |50 /48 |426.7 |— | beyond_domain |
| pbdb_excluded_decline 10 |50 /48 |426.7 |— | beyond_domain |

The last two rows share domain maximum 469.4 Ma. The selected case is B2, while the Oman admission
comparison concerns B0. The object labels must remain visible even when detailed assumptions are grouped.

### Murzuq target classes

`studies/f3/models/out/m2_results.csv`, select `design=LY-MZ-CU`, `primary=True`,
`variant=allocation=stage;cluster_k=2.0;material_type=chart-code`:

| Fixed rho | `fstar_H0c_459.1` | `fstar_H0_459.1` |
|---:|---:|---:|
|1 |0.091 |0.1835 |
|0.1 |0.9103 |0.9207 |

The constant parameter and the variable-history exposure-weighted mean are different estimands.
Equal delivery does not alone identify actual producer abundance: production, preservation,
recognition and reporting also enter the encounter process. The conditional-independence assumption
is given a shared well effect, as the Discussion already states correctly.

### Step, offsets and shape certificates

- `frontier.csv`: `reading=main; unit_treatment=primary; assumed_diagnostic_delay_myr=0`.
  Later/earlier contrasts are 8.0841, 9.4860 and 11.8224 at 444,447 and 452 Ma. The break is fixed after
  inspection at 426.7 Ma. The retrospective construction uses the 0.05 comparison contour.
- `delay_sensitivity.csv`: `category=B2; history=flat` gives recoverability bound 428.84000595 Ma.
  Differences to 444 and 452 Ma are 15.15999405 and 23.15999405 Myr; these establish the stated minimum
  assumed offsets, not fitted delays. Rate change and delay can be combined.
- `interval_feasibility_summary.csv` contains exactly `flat`, `pbdb_all`, `pbdb_plant_excluded`,
  `decline25`, `decline10`, `pbdb_excluded_decline10`. For B2 the pure `decline10` fails the finite
  reference in every inclusion state. The combined history passes with 49 or 50 units. For B0, every
  one of these six fails in all 76/77/78 inclusion states. This does not certify failure of every
  conceivable history or select a fitted biological history.
- The saved half-rate step value 430.9800119 Ma is consistent with the earlier independent scalar
  inversion. It remains unbound in the frozen ledger at this review; the parent should keep that
  status explicit until authorised ledger integration.

### C47’s outer value

`data/timescale.csv` gives Homerian 430.6±1.3 and Sheinwoodian 432.9±1.2 Ma. The current-scale rule
gives 431.9 and 434.1 Ma, a 2.2 Myr difference. Against the published historical 431.2 Ma the comparison is
2.9 Myr. `studies/f3/docs/audits/2026-11-08-c47-source-check.md` records the source interpretation and decimal
arithmetic. The outer rule does not date the fertile slab, establish crown membership or predict a
clock-posterior shift.

## C19: whose calculation, and what persisted

`studies/f3/models/pilot-asr/README.md` identifies this as a new analysis, predeclared and run by Claude on
Hooper’s deposited inputs because the deposit contained node summaries but no saved mapped paths.
`docs/charter.md` records Claude’s mapping, diagnostics and corrections after Codex review.

`studies/f3/models/pilot-asr/common.R` generates equal-rates(`model="ER"`) stochastic maps for character X21;
state 3 is the proximal trilete aperture. Its path reader requires the state to remain unchanged along
the full path from crown Embryophyta to crown Tracheophyta. Ending with a trilete state after a loss
and regain is insufficient.

The row `tree=ext` of `diagnostics_summary_ext_b10000_s100.csv` has four chains, 4,000 maps,
3,382 trilete starts and 77 departures. Conditional persistence is
$(3382-77)/3382=0.9772324069$, with Monte Carlo SE0.0026167. It is conditional on the character coding,
equal-rates model, extant-only tree and its embedded older chronology. ARD retention scenarios and
other trees are different outputs. It is neither a published Hooper persistence estimate nor the
fraction of extinct local producers that made recognisable spores.

Compact positive replacement:

> Our reanalysis of Hooper’s deposited data gives conditional trilete-aperture retention of 0.977 on
> the extant-only tree, given its character coding, equal-rates model and dated chronology.

This correctly credits the present study and keeps the character-retention result separate from
local abundance and the qualification of the spore bound.

## Scope and stopping point

All listed repairs can be made inside reconstruction. They preserve the accepted numbers and
require neither new analyses nor edits to the frozen products. They also preserve Barry’s prose
rule: name the correct object in Results and collect detailed conditions once in the dedicated
paragraph. If the 300-word limit forces a choice, an explicit primary envelope and correct target
labels take priority over secondary sensitivity numbers.

Next: Codex — integrate these bounded repairs and check the revised section counts.
