# Table S17: independent pointer review

Codex, 15 November 2026. Bounded review of Table S17 at `49c8cb0`, requested
by the parent reviewer. Only this audit file was written. No analysis was run,
and no manuscript, ledger, code or numerical output was changed.

## Disposition

All **34 condition rows** are present and have a supportable home in the named
methods, results, supplement or implementation. No section number points to a
non-existent section. The main repairs concern one wrong result label, ambiguous
relative file locators, and distinguishing an assumption's statement from a test
of that assumption. Two confidence phrases should match the adopted distinction
between nominal levels and calibrated confidence.

### Exact repairs

1. **Row 13, rule of three:** `Bears on: Results (f)` is too narrow and misses
   where the result is introduced. Use `Results (d)–(f), (h)` (or equivalent
   coverage of the level-later-rate calculations). Methods (g), its existing
   support pointer, is correct.
2. **Relative script/output locators:** add before the table: `Script and output
   paths in this table are relative to studies/f3/models/loop3/.` Alternatively
   expand the four script locators and the membership-file locator. All named
   files exist under that base; they are not relative to the manuscript folder.
3. **Row 20, stage permutation:** the exchangeable-label assumption is stated
   in this table, rather than explicitly in S5.10 or the code. The code
   implements the shuffling comparison. A precise locator is `Stated here;
   combined_rulers.py: spearman_exact_p (implementation)`. This avoids implying
   that exchangeability or temporal independence has been empirically tested.
4. **Row 22, placement independence/age support:** add `Methods (h)` before
   the existing pointers. It defines the actual binomial allocation. S5.2
   supplies the general independence/support framework but is not itself the
   placement calculation; `combined_rulers.py: placement` is the implementation.
5. **Row 29:** replace `Collection density measures searching` with
   `Collection density is used as a rough proxy for searching`. S5.8 explicitly
   says that the proxies do not estimate the finding rate and that the
   collections are dominated by marine animals. The targeted-searching effect
   and its existing pointers are sound.
6. **Rows 14 and 19:** use `without calibrated 95% confidence` and `no calibrated
   confidence level`, respectively, to match the distinction deliberately
   retained in the new main Conditions paragraph. Nominal probability levels
   still exist in these retrospective calculations.

Other useful precision changes are listed in the matrix: figure 3a rather than
figure 2 for the count curve; describing the exponential family as examined,
rather than as a statement of historical truth; and saying that the lower
bounds do not establish a plateau rather than give no evidence of one.

## Row-by-row trace

Row numbers exclude the four italic group dividers. “Stated” identifies a model
assumption or interpretation; “examined” identifies an actual sensitivity or
comparison, without suggesting that the historical assumption was verified.

| Row | Condition (short label) | Trace and outcome |
|---:|---|---|
| 1 | Indigenous Llandovery spores | S2.3 explicitly varies indigenous encounter fraction and contaminant transfer, derives observational equivalence, and flags conflicts even at zero older intensity. Correct; examined as a sensitivity, not an empirical determination of indigenous fraction. |
| 2 | Comparable reporting | Methods (c) distinguishes explicit negatives from complete-chart negatives; S2.1 identifies the chart/prose frame and S2.2 models reported binary outcomes. Correct stated observational condition. |
| 3 | Uniform within-stage ages | S2.2 explicitly states latent uniform ages; S2.3 compares fixed depth-ordered 10/50/90% positions; S2.5 explains the pre-459.1 mixture. Existing S2.3/S2.5 pointers support the comparison; adding S2.2 would locate the base assumption directly. |
| 4 | Conditional independence with shared well effect | S2.2 states conditional independence and the Gamma well effect; S2.5/Table S1b examines block reweighting and well alternatives. Existing pointer is correct for the effect; S2.2 could be added for the base assumption. |
| 5 | Exploratory four-tenths weighting | S2.5 explicitly calls it retrospective, unqualified and composite, and distinguishes its comparison contour from the qualified model. Correct. |
| 6 | Stage-resolution regional comparison | Methods (c) declares the compilation and filters; S2.6 distinguishes overlapping stage enclosures from actual simultaneity and excludes insecure entries. Correct. |
| 7 | Trilete production, persistence and catchment | Main Table 1 lists all three links in the 459.1 Ma row. S6 gives the trait-to-node and persistence limits. Correct stated links, not established ancestral facts. |
| 8 | Independent continuous ages; uncertain count | Methods (e), Results (d) and S5.2 support the model and count direction. Figure 2 illustrates the endpoint calculation, but figure 3a is the direct count-sensitivity figure. S5.6 tests duplicate-horizon calibration failures; add it if the pointer is intended to cover the effect cell's calibration statement directly. |
| 9 | Fixed history, cutoff, timescale, inventory and units | Methods (e)–(f) fixes the model; S5.3 explicitly varies cutoff, units, age treatments and timescale scenarios. Correct. Methods (a)/(d) and S5.1 locate the adopted timescale/inventory definitions if fuller navigation is wanted. |
| 10 | Containing age supports | S5.2 states the envelope and almost-sure support argument, including alpha plus delta and lack of demonstrated joint geological coverage. S5.6 contains the exact-age simulations. Correct; the simulation result does not establish geological containment. |
| 11 | Crown membership | Methods (d) declares B2; S5.1/Table S13 records fossil-specific placement requirements; S6 distinguishes total/stem and crown assignments. Correct. |
| 12 | Recognisability delay | Methods (g) gives the shifted count start and reduction formula; S5.5 declares fixed-delay mapping and its status. Correct. |
| 13 | Count-derived later rate in rule of three | Methods (g) explicitly estimates n/(A-c) and converts to expected early finds. Correct pointer; widen `Bears on` from only Results (f) to the rule's main presentation/applications in (d)–(f), (h). |
| 14 | Retrospective step and rise placement | Methods (g) explicitly states selection after seeing the data; S5.9 gives the corresponding limitation. Correct pointers; say `without calibrated 95% confidence` to preserve the nominal/calibrated distinction. S5.4 is the direct step-grid declaration if an extra pointer is desired. |
| 15 | Later plateau versus proportional history | Methods (f) supplies the age-shape diagnostic; Methods (g)/(h) and S5.9 distinguish the steady-later assumption and varying proportional history. Correct. S5.4 and S5.10 are more direct extra pointers for the step comparison and integral-based proportional product, respectively. |
| 16 | Doubling requirements, not measured spread | Results (f) and S5.9 explicitly state requirements and coarse spore context rather than estimated spread. Correct. |
| 17 | Proxy object and sufficient proportionality | Methods (h) and S5.8 define the objects and the sufficient same-constant transfer. Correct; current wording properly uses `if`, not `only if`. |
| 18 | Transfer of a mean contrast | Results (g) gives the failed later-record comparison; S5.10 reports the underlying product/placement examples. Correct interpretation of evidential support, not an empirical estimate of mean finding rates. |
| 19 | Combined measure chosen after singles | Methods (h) and S5.10 state retrospective selection, possible shared causes and lack of confidence status. Correct pointers; `no calibrated confidence level` is consistent with the main paragraph and preserves the existence of nominal levels. |
| 20 | Exchangeable stage labels | S5.10 reports the overlap statistic; `combined_rulers.py: spearman_exact_p` implements free shuffles. The exchangeability assumption itself is stated only here. Use a statement/implementation locator, not language implying that it was tested. |
| 21 | Guaranteed minimum late counts | Results (g), S5.10 and Table S16 give the minimum counts and comparison. Correct. At a fixed total, extra true late finds make upper-tail discrepancies stronger and raise the lower share benchmark; the non-rejection of level/searching need not survive. |
| 22 | Placement iid units and valid age supports | S5.2 gives the general support framework; S5.10 describes the minimum count; `combined_rulers.py: placement` states the iid-scenario and selection limitations. Add Methods (h), which directly defines the placement probability. |
| 23 | Inventory imbalance inherited by allocation | `Stated here` is honest: this is an observational caveat, not a tested even-sampling assumption. The effect cell is appropriate. No independent validation is claimed. |
| 24 | Data-selected intervals and A | S5.10 states retrospective intervals; the `switch_reading.py` opening docstring explicitly states both A and intervals come from age supports and that nominal fixed-window coverage does not calibrate selection. Correct once the script base path is clear. |
| 25 | Regional-cell iid is a scenario | Results (d) explicitly calls the coarse counts scenarios, not estimates of independence; S5.10 compares the regional allocation. Correct. The `combined_rulers.py: placement` docstring is the most explicit additional statement. |
| 26 | Non-rejection at the minimum count | Table S16 reports the specified minimum-count Gorstian–Pridoli cases; S5.10 also reports the narrower split. Correct; no general model validation follows. |
| 27 | Nine Pridoli-only age enclosures | The named membership file supports it after filtering B2/main, certain inside [c,A], and wholly within the late interval. A read-only pointer check gives 48 eligible, 13 whole late supports, nine with the Pridoli-only 419.62–422.7 enclosure. Correct; clarify the base path and optionally the filter. No new scientific analysis was run. |
| 28 | One exponential later family | S5.10 defines exp(g u) and its endpoint factor. Correct family restriction; prefer `Only one exponential family is examined for later change` over wording that can assert the actual historical rate belongs to it. |
| 29 | Searching proxy; unmeasured targeted effort | Main Conditions states targeted searching; Methods (h) defines the collection proxy; S5.8 gives its roughness and limitations. Correct pointers. Replace unqualified `measures searching` with `is used as a rough proxy for searching`. |
| 30 | Lower bounds on interval averages | S5.10 explicitly distinguishes lower benchmarks from a measured plateau. Correct pointer. `They do not establish a plateau` is more exact than the stronger `give no evidence of a plateau`. |
| 31 | Exponential factor spans A to c | S5.10 explicitly gives the A-to-c window including the late Silurian. Correct. |
| 32 | Steady later rate and zero delay for early lengths | Results (f)/(h) and S5.9 specify these assumptions and the linear 2K length. Correct; the effect is shape-specific, as the table says. |
| 33 | A-setting units outside guaranteed count | S5.10 identifies the two Australian units and their long supports; `switch_reading.py` explicitly states remaining selection and possible overlap with the true oldest fossil. Correct once the file path base is clear. |
| 34 | Finding recognisable bodies, not lineage origin | The Discussion distinguishes record start from ancestor timing and labels the switch interpretation. Correct. `Discussion, Interpretation; Methods (e)` would be a more focused locator than `Discussion` alone. |

No numerical result needs changing for these pointer repairs. The table does not
turn the conditions into empirically verified historical facts. In particular,
`Stated here` is appropriate for a caveat newly collected into this table.
