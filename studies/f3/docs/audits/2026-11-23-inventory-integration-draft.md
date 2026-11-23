# Draft passages for the inventory revision

Codex, 23 November 2026. Proposed copy for Claude’s integration, following the [Stage 2 decision](2026-11-23-inventory-symmetry-stage2-acceptance.md) and [review of Gemini’s feedback](2026-11-23-gemini-integration-review.md). Each passage below names its evidence for binding at integration.

## Abstract

Molecular clocks date living land plants’ common ancestor from the Cambrian to the Late Ordovician. We examined three fossil maxima. The oldest, 515.5 million years ago (Ma), draws on marine rocks that preserve algal cysts. Spore delivery there remains unmeasured. The 459.1 Ma maximum uses spores with a three-rayed scar. Ordovician Libyan samples lack reported spores of this kind in stages that yield them elsewhere. The 431.2 Ma maximum for living vascular plants draws on a branched fossil. Under steady recording, 48 independent finds give a 95% limit of 428.8 Ma on the start of their recognisable record. The broader branched-plant record gives a limit older than 431.2 Ma. With steady later recording, the gap before the oldest crown fossil allows about three expected earlier finds or fewer. For those 48 finds, ancestors at 444–452 Ma require 8–12-fold lower early recording if their bodies were immediately recognisable. Later diagnostic features reduce that requirement. Late-Silurian crown fossils occur in several regions. Finding proportional to North American non-marine rock area predicts too few. The inferred change in finding frequency into the Devonian depends on the inventory.

Claims for the abstract are C01/C45/C54 for Libya, C42/C46/C47 for the three maxima, C25/C27/C48/C58/C61 for the body calculation, and C59/C60 for distribution and finding frequency.

## Results

### (g) Rock area predicts too few late-Silurian finds

If finding had tracked the area of North American rock columns holding non-marine deposits, the expected late-Silurian count would be below one in the reviewed inventory, where at least 13 finds occur. The shortfall persists across occurrence inventories and in the regional distribution of listed species endpoints. Multiplying rock area by the trilete-reporting share gives the same result. The spore share alone predicts too few finds in the literature-augmented inventory and passes the same check on database-backed occurrences with restored Devonian records. The density of all land and marginal-marine PBDB collections predicts 10.1 finds in the reviewed inventory’s Gorstian–Přídolí interval. Its later-to-earlier ratios at 444 and 452 Ma were 1.35 and 1.41, respectively (figure 3b).

### (h) The geographical record is clearer than the change in finding frequency

Late-Silurian crown fossils occur in six named palaeoregions in the reviewed inventory and three when only database-backed localities are counted. Counting occupied region–stage cells, each occurrence inventory admits the late-Silurian share expected under steady finding. Capel’s species endpoints also admit that share. The locality counts depend more strongly on how the record was assembled. Restoring broadly dated Early Devonian finds and restricting the comparison to database-backed localities leaves five to seven of 59 finds in the late-Silurian interval. Finding could have continued to rise into the Devonian. Changes in plant abundance, preservation or collecting could each affect the counts.

Retain (g) and (h) as separate pointers for existing cross-references. Bind the primary expected and observed counts to C59 (including V204 for searching), the two collection ratios to C56/V130–V131, the regional comparison and the five-to-seven range to the accepted C60 rows. Identify figure 3b’s 48-, 19- and 15-unit treatments as the original inventory. Methods should give the sourcing difference in one sentence and point to the subsection below.

Suggested Methods sentence. “We tested how an age-range filter and the concentration of literature curation in the Silurian affected the comparison by restoring broadly dated Devonian collections, repeating it on database-backed finds, and checking the regional distribution of species endpoints in an independent compilation (electronic supplementary material, S5.12).”

### Shape test in (d)

The steep decline in finding into the past fails the fossil-age test in the reviewed and restored literature-augmented inventories. On database-backed finds alone, restoring 21 units dated only to the Early Devonian admits age assignments that pass. The test establishes compatibility within those ranges. It leaves the actual ages of those finds unresolved.

This passage concerns the 10 Myr history (C49). The 25 Myr history passes on the original crown inventory with all 50 possible units and fails with the 48 guaranteed units. On the restored inventory it passes for each choice of the two cutoff-straddling units. Bind that distinction wherever Results (d) or Table 2 retains a shape verdict.

## Supplement, proposed S5.12 and Table S20

Literature curation added chiefly to the Silurian record. A duration filter also removed collections dated only to the Early Devonian. We retained the original inventory for the primary record-start limit and varied both its sources and the age filter. The comparison below uses the 426.7 Ma oldest-age envelope and the 393.47 Ma cutoff. The first three numbers in each row count locality–age units certainly inside that window whose ranges lie wholly in the late Silurian, wholly in the Early Devonian, or across their boundary. The regional columns use named regions and the Gorstian–Přídolí interval. The lower ratio is a nominal one-sided 95% benchmark for this retrospectively chosen interval relative to the entire window, which includes it. The spore column gives the upper-tail probability of finding at least as many occupied cells as observed if placement followed the trilete-reporting share. The last column gives the best finite-sample age-shape *p* for the 10 Myr history on the guaranteed locality–age units.

| Inventory | Silurian / Devonian / crossing | Silurian regions | Regional lower ratio | Spore *p*, regions | 10 Myr *p*, localities |
|---|---:|---:|---:|---:|---:|
| Reviewed (S0) | 13 / 32 / 3 | 6 | 0.692 | 0.00257 | 0.0000034 |
| Reviewed with Devonian collections restored (S1) | 13 / 53 / 3 | 6 | 0.622 | 0.00449 | 0.00425 |
| Database-backed (S2a) | 5 / 31 / 2 | 3 | 0.267 | 0.108 | 0.00312 |
| Database-backed with Devonian collections restored (S2b) | 5 / 52 / 2 | 3 | 0.234 | 0.144 | 0.238 |
| Capel, main reading | 7 / 101 / 1 | 5 | 0.386 | 0.0419 | — |

Capel lists the first and last localities of each species. Its regional comparison describes where those endpoints occur. Intermediate occurrences would be needed for the age-shape test. At the alternative oldest age of 425 Ma, the spore share also predicts too few on S2a’s named cells. All-collection searching predicts too few in the original inventory’s narrower Ludfordian–Přídolí locality check at both anchors. The plant-excluded measure gives no upper-tail rejection. On S2b it predicts 13.82 localities in the broader late-Silurian interval, where five to seven occur. A check in one direction can miss a discrepancy in the other. [Counts and tests](../../models/loop3/out/inventory_symmetry_stage2_tests.csv) · [Shape tests](../../models/loop3/out/inventory_symmetry_stage2_shape.csv)

All 21 restored S2b units share a 26.15 Myr range. Among the 59 guaranteed finds, possible assignments pass the 10 Myr shape test with two of these units younger than 400 Ma or with all 21 younger than 400 Ma. Midpoint ages fail. The broad ranges allow very different age assignments to fit. C49 tests the spread of fossil ages over the full window, C60 compares counts in a shorter interval, and C57 asks how fast early finding would have to rise **before** the oldest find if recording then stayed level. Each answers a different question. [Age examples](2026-11-23-inventory-age-examples.csv) · [Age-range check](2026-11-23-inventory-age-examples.py)

With Devonian collections restored, the 25 Myr history passes across all four inclusion states for crown vascular plants (*p* = 0.832–0.882), the main branched-plant record (0.0712–0.0925), land-plant bodies including Oman (0.0612–0.0675), and branched plants including the disputed Zbrza axes (0.0767–0.0836). Land-plant bodies with Oman removed still fail (maximum 0.027). In the original crown inventory, 48 or 49 finds fail and 50 pass. [Shape results by group and inclusion state](../../models/loop3/out/inventory_symmetry_stage2_shape.csv)

The [1,918 counting and history calculations](../../models/loop3/out/inventory_symmetry_stage2_task4.csv) retain both the conservative envelope and the oldest limit over jointly feasible count–age pairs, conditional on fixed midpoint groups in the regional rows. The [Bathurst comparison](2026-11-23-inventory-symmetry-stage2-acceptance.md) identifies the placements behind the bounds and the minimum reductions. The [group table](../../models/loop3/out/inventory_symmetry_stage2_groups.csv) gives the branched and land-plant-body sensitivities. These are separate from the placement and age-shape tests above.

## Reader’s brief

Suggested replacement for the staged brief’s paragraph on the late Silurian and the passage interpreting it:

> By the late Silurian, plants from the group that includes today’s ferns, clubmosses and seed plants had left fossils in several parts of the world. One compilation records them in six regions. Even the fossil database alone records them in three. How often these plants turned up is harder to tell. Adding Early Devonian finds makes the earlier record look sparser. Preservation and the beds people searched could both have contributed.
>
> An older ancestor fits if early plants left fewer fossils that we can recognise and find, or if their familiar features appeared later. The fossil record lets us calculate how large a difference each explanation needs. The timing of any rise in finding remains open.

Keep the rule of three in the brief. With the original 48 finds and steady recording, the gap allows about two million years of earlier recording at that rate. Older starts would have yielded too many expected finds under this model. The figure and its caption should identify the original inventory. The writer can carry the C62 conditional into the Oman paragraph and distinguish the limits of each group’s fossil record from the ages of their ancestors. [Primary bounds](../../models/loop3/out/reviewed_bounds.csv) · [C62 check](2026-11-23-inventory-symmetry-stage2-acceptance.md)
