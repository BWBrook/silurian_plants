# Inventory-symmetry audit: execution record

Claude (Opus 5.5), from 21 November 2026. Specification and Fable's amendments:
`2026-11-21-inventory-symmetry-spec.md`. Frozen S3 rules: `2026-11-21-inventory-symmetry-s3-rules.md`
(committed `7b6e3ae` before any S3 parse). Board discussion 191.

**Status, 23 November 2026.** Stage 1 is signed off (`088f592`). Stage 2 has run and awaits Codex's check:
see "Stage 2 results" at the end.

**Stage 1 status, 23 November 2026.**
- Codex signed off Task 1A (`f22b451`) and returned the S3 mapping for four repairs.
- The repairs, the counting rules and the tail rules became amendments S3-A10 to S3-A17 (`65ff1d2`).
  Codex's reconciliation review (`f6e2d10`) accepted them except for two repairs, now S3-A18 (Yea
  identity treatments) and S3-A19 (the exponential upper factor), with record corrections in S3-A20.
  Codex signed off S3-A18 to S3-A20 at `480ed4a` and released Stage 2 on 23 November.
  [Stage 1 acceptance](2026-11-23-inventory-symmetry-stage1-acceptance.md)
- No share or test has been computed on S1, S2a, S2b or S3.
- The Tasks 3–4 harness implements the new counting and tail rules. It has run on S0 alone, where it
  reproduces the committed values.
- Task 4.2, Task 5 and Task 6 are not built yet.

No text, figure, ledger, estimand or frozen output was changed.

## Code and outputs

| File | Role |
|---|---|
| `studies/f3/models/loop3/inventory_symmetry.py` | Task 1A: disposition table; builds S0, S1, S2a, S2b and variants from `horizons_reviewed.csv` without changing it |
| `studies/f3/models/loop3/capel_s3.py` | Task 1B: S3 parse under the frozen rules, S3-A10 to S3-A14 and the Yea treatments of S3-A18; mapping tables; row-level check of disputed cases; no counts |
| `studies/f3/models/loop3/inventory_symmetry_tests.py` | Tasks 3–4 harness (C59 placement, C60, C27/C48 arithmetic) under S3-A15, S3-A16, the bed order of S3-A18 and the upper factor of S3-A19 |
| `out/inventory_symmetry_dispositions.csv` | SHA-256 `2885c100e3a2ef3b81f2da958e2fad89ce6410d38abc65cd0590886b71ed311e` |
| `out/inventory_symmetry_units.csv` | `ad76a374292b309fb1a4b28afbbb70159a55a32ec342fe721f65c1a09db6ba29` |
| `out/capel_s3_rows.csv` | `4059893f1238393c3591481fd6033617c588cbcac4cb2ad9bd42cc0217b8f3a3` |
| `out/capel_s3_disputed_rows.csv` | `0f8ac2ba7a1b2edb8260671128ea793cc8e02c572fd391b4a32d822fea93e4f9` |
| `out/capel_s3_yea_units.csv` | `0051293e494eda7b24742190fbe1f4e281a0bd41405b54a1afda417f4703e78a` |
| `out/capel_s3_age_map.csv` | `500942d9f3bbc8528761353ac0f6b73aaad06e15191b9912b46b7ab967e66ca0` |
| `out/capel_s3_region_map.csv` | `90239102179339db18b4f7581c3da7bd3b55e99770565d005a9186cc71a73f76` |
| `out/inventory_symmetry_tests_S0.csv` | `a07e1dc59b87debd4953b0bab09b485d6dc7fcd4e07aa864c540dce229d1dcd9` |

`capel_s3_fuzzy_merges.csv` was removed with the fuzzy variant (S3-A5); its last version is at `34a36ad`. The
stage-1 hashes of the other files are in this record at `34a36ad`.

`capel_s3_rows.csv` reproduces Capel, Monnet and Cascales-Miñana (2025) Table S1 rows with derived columns,
under its CC BY 4.0 licence (Figshare `10.6084/m9.figshare.30281263.v1`).

Reproduce: `uv run studies/f3/models/loop3/inventory_symmetry.py`, `uv run studies/f3/models/loop3/capel_s3.py`,
`uv run studies/f3/models/loop3/inventory_symmetry_tests.py S0`.

## Facts reproduced before building on them

- **Fact A and Fact B** reproduce at `9ac5946`. Of the 48 guaranteed S0 crown units, 13 are Silurian-only
  (10 curated `tail:` units, 3 PBDB), 32 Devonian-only (30 PBDB, 2 curated) and 3 are the curated Yea
  straddlers. Raw `wide_age` gives 73 guaranteed units (`reviewed_bounds.csv`, the B2 `wide_age` rows).
- **Amendment 1 is correct.** In `macrostrat_units_window.csv`, columns 37 and 38 (Huntersville Fm, Rocky Gap
  Sandstone) and 305 (Old Port Fm members, Keyser Fm) list surface Early Devonian units; only column 304
  holds them all in the subsurface. Column 304's centroid is the nearest to Kinzua Dam (0.25°); column 38 is
  nearest Cloyds Mountain (0.12°) and 305 nearest Baker Run (0.49°). Capel Table S1 has 13 Price Fm rows,
  all Late Tournaisian, and 11 Pocono rows, 10 Late Tournaisian and 1 Late Famennian.
- **Amendment 7:** `reviewed_bounds.csv` row 96 (B2, locality–age, primary, Pridoli cutoff, decline10)
  gives 429.804907 Ma.
- **Harness check:** run on S0, `inventory_symmetry_tests.py` reproduces every row of `switch_reading.csv`
  (n, k, least rate ratio 0.790 and 0.692, change factors), every row of `combined_rulers_placement.csv`
  (shares and p values) and C27/C48 (T = 428.84 Ma; folds 8.0841 and 11.8224). It asserts these on each run.

## Task 1A: wide-age PBDB rows

Scope: every `wide_age_sensitivity` PBDB row with 393.47 ≤ min and max ≤ 422.7 Ma, any group: 45 rows
(39 crown).

| Decision | Rows (crown) | Rows |
|---|---|---|
| Restore (wholly Early Devonian, no contrary evidence in held sources) | 35 | 40 |
| Miscoded post-Early Devonian, by formation name | 2 | `pbdb:28216` (Price Fm), `pbdb:28302` (Pocono Fm) |
| Miscoded, weak evidence; carried both ways | 1 | `pbdb:28303` (Kinzua Dam; no formation; nearest Macrostrat column all-subsurface) |
| Duplicate of a curated unit | 1 | `pbdb:27917` (Wutubulake Bed 5 = `tail:M-xinjiang-zosterophyllum`, L3S-037) |
| Range reaches the Silurian; not restored | 0 | `pbdb:24903` (Fairhill, Australia, Tracheophyta; 422.7–393.47 Ma) |

The evidence for each excluded row is in the `evidence` column of the disposition table. Each restored row
carries its PBDB reference and interval coding. Checks on the restored rows:

- **Capel Table S1 corroborates Early Devonian ages** for the restored rows it covers, for example Campbellton
  Fm at Dalhousie Junction (Emsian), Battery Point Fm (mid- to late Emsian), Jbel ben Aarab (Early Emsian)
  and Rebreuve (Early Emsian). Andrews et al. (1974), cited by `pbdb:23007` and `pbdb:26650`, has "Middle
  Devonian" in its title, but Capel dates the same Campbellton plants Emsian.
- **Three restored crown rows share a locality key with an S0 unit:** `pbdb:20841` and `pbdb:21266`
  (Battery Point) and `pbdb:26179` (Beartooth Butte). Under the locality–age rule their broader age code
  makes each a separate unit. They may be the same horizons coded coarsely. The variant `_merged` adds none
  of them.
- **`pbdb:28768` (Milesburg, Helderberg)** comes from the same SUNY-Binghamton accession list (ref 6895) as the
  three exclusions. Macrostrat columns 304 and 305 date the Helderberg Gp 417.97–413.02 Ma, so its Early
  Devonian coding stands; the disposition table records this.
- **Duration filter on B0 and B1.** Five restored rows are B0 or B1 only. Task 1A builds every group, but
  Fable's order confines Tasks 3–6 to the crown group.

### Sets built (units with max_ma > 393.47)

| Set | Locality–age | Region–stage | Definition |
|---|---:|---:|---|
| S0 | 50 | 19 | reviewed primary; reproduces `primary_unit_membership.csv` |
| S1 | 71 | 21 | S0 + 40 restored rows |
| S1_with_28303 | 72 | 21 | also restores Kinzua Dam |
| S1_merged | 68 | 21 | restored rows at S0 locality keys add no unit |
| S2a | 40 | 16 | PBDB rows ≤ 20 Myr + curated rows linked to a PBDB collection |
| S2a_coord | 39 | 16 | linked curated rows take their collection's 0.1° key (Bathurst US384 and US385 share one) |
| S2b | 61 | 18 | S2a + restored rows |
| S2b_with_28303, S2b_merged, S2b_coord | 62, 58, 60 | 18 | as above |

The guaranteed counts are two fewer in each row (the two units straddling 393.47 Ma), which matches
Gemini's 69 (S1), 38 (S2a) and 59 (S2b). Silurian counts and shares are held for stage 2.

## Task 1B: S3 parse

The frozen rules held for crown assignment, ages and regions. F3's genus classification and Capel's group
never conflict: 328 rows are assigned by F3 genus, one by F3's material reading (S3-A12) and the rest by
group.

After S3-A10 to S3-A12 the sheet has 1,197 biological rows:
- crown 997;
- unresolved 123 (Basal eutracheophytes and Incertae sedis without an F3 decision);
- not crown 77.

On ages, 401 rows reach into the window and 796 lie outside it. In the first parse, 999/123/76 and the one
blank age came from the footnote row and from row 6 before its material reading.

### Amendments made after parsing and before any S3 count (for sign-off)

The dated text of S3-A1 to S3-A9 is in the rules file's Amendments section, which overrides its frozen text.
S3-A1 to S3-A5 came from the mapping tables, and S3-A6 to S3-A8 from the list of rows reaching above
419.62 Ma; none came from a tally. S3-A7 adds a Capel-groups-only variant, S3-A8 sets the Task 6 rule for
S3 (Lipeon Fm keeps A at 426.7 Ma once Yea is excluded) and S3-A9 restates the gates for S3.

- **S3-A1. Species counts.** The sheet has 810 one-row species and 194 two-row species, and no three-row
  species. Amendment 2's 809/195/1 is off by one row. The rule document's statement is corrected here.
- **S3-A2. UK regions.** 30 UK rows name no country token. Brown Clee Hill and Targrove (Shropshire) and
  Perton Lane (Hereford) are English localities, so Shropshire, Hereford and other English and Welsh county
  names now map to Avalonia. No UK row remains "multiple".
- **S3-A3. Yea re-ageing.** The rule re-aged every row naming Yea. Norton Gully Sandstone
  (*Taungurungia garrattii*, Late Pragian–Emsian) is a younger unit, not the disputed Yea anchor, so it keeps
  Capel's age. Four rows take the 393.47–426.7 Ma envelope: Upper Yea Fm and Ghin Ghin Road (crown), and two
  Limestone Road rows (not crown).
- **S3-A4. One locality alias.** "Altholville" and "Atholville" (Campbellton Fm) are one locality; the main
  key now merges them.
- **S3-A5. Fuzzy sensitivity over-merges.** Of the six merges at ratio 0.92, one was the Atholville
  variant (now S3-A4); the other five, still listed in `capel_s3_fuzzy_merges.csv`, join distinct units:
  Zhichang and Changputang sections; Tashtyp and Kalguty Fms; Tokrau and Ainasu horizons; Upper Rashkovskie
  and Rashkovskie Beds; Wood Bay and Wijde Bay Fms. **Proposal:** drop `S3_fuzzy`, since S3-A4 handles the
  one true variant.
- **S3-A6. `S3_plus_unresolved` is not a crown sensitivity.** Its added rows are mostly *Cooksonia*,
  including *C. barrandei* (Sheinwoodian) and Borrisnoe (Homerian). They would move A to 432.9 Ma and turn
  the set into a branched-plant inventory. **Proposal:** drop it from the crown runs.
- The age-map display had taken a re-aged Yea row as each string's first value; it now shows Capel's
  literal ages. The age logic was unchanged. "Tournaisian" stages map to a zero-length interval at 358.86 Ma
  because the timescale file ends there; they lie outside the window.

### Repairs after Codex's review (S3-A10 to S3-A17)

Codex's review ([2026-11-21-inventory-symmetry-stage1-review.md](2026-11-21-inventory-symmetry-stage1-review.md))
is accepted in full. The repairs:

1. **Worksheet boundaries (S3-A10).** The first parse counted the footnote in row 1201 as a species.
   Without it there are 1,197 rows in 1,003 entries (809 one-row, 194 two-row). Merged references now fill
   the rows they span.
2. **Yea by horizon (S3-A11).** Rows 1199 and 904 (Ghin Ghin Road, no "Yea" in the text) had escaped the
   Yea rule. Every Yea-area row now maps to a named F3 horizon with that horizon's envelope. Rows 734 and
   1199 form one Ghin Ghin Loc. 1 unit, and Task 6 removes rows 124, 734 and 1199 before aggregation.
3. **Material readings and the oldest age (S3-A12, S3-A13).**
   - Row 6, the Bolivian *Aberlemnia*, follows F3's Negra Muerta reading (B1 in main) in S3 main. With Yea
     excluded, A is then 425.0 Ma from the data in main, f3_strict and capel_groups.
   - `S3_permissive` keeps row 6 and 426.7 Ma. Its 425.0 Ma run is labelled as forced, with the rows it
     removes.
   - A new `S3_f3_strict` drops the 12 window rows where F3 reads the genus as uncertain and Capel's group
     admits it. Only one of the 12 is Silurian: *Jugumella*, at Balkhash, which shares row 128's unit.
   - `yea_literal` has A = 425.0 Ma even with Yea included, because Capel dates row 124 Ludfordian.
4. **Regional grouping (S3-A14).** Row 477 (Argentina, Eifelian midpoint) no longer raises an error. The
   disputed-rows file records its midpoint stage, its possible-only status and the variants that admit it.
   Every variant runs at both grains.
5. **Counting and tail rules (S3-A15, S3-A16).**
   - Cells use the same region × stage units in numerator and denominator, and the named-region rule
     decides.
   - Units that straddle the interval boundary are placed in every stage their range allows. Each test
     takes its largest p over the admissible (n, k) pairs, and a two-sided rejection needs every pair.
   - On S0 the harness still reproduces every committed value. On S0, k is 13 to 16 at locality–age, and
     cells run 6 to 9 of 19 to 22 (pooled) or 17 to 20 (named).
   - Neither a level deficit nor a two-sided departure is established on S0.
   - S0's region–stage lower rate ratios move from the committed legacy pair's 0.692 and 0.911 to 0.692 and
     0.862 (named, Gorstian–Přídolí and Ludfordian–Přídolí).
   - No S0 test outcome changes between pooled, named and legacy.
6. **Gates on S3 (S3-A17).**
   - S3 enters gates 1–3 at region_stage_named as listed endpoint cells, with S3 main deciding.
   - A gate outcome that changes under another S3 reading counts as "narrower, inventory-dependent".
   - Gate 4 has no S3 evidence.

### Crosswalk of Silurian crown units, S0 and S3 (amendment 3)

Superseded in part by the review. The table below is the stage-1 locality match, with corrections in its
Basis column. The region–stage comparison after it replaces the stage-1 bias paragraph.

S3 rows are Capel crown rows whose literal range reaches above 419.62 Ma. Yea rows carry F3's envelope in
S3 main.

| S0 unit and its taxa (13 Silurian-only, 3 Yea) | S3 match | Basis |
|---|---|---|
| Rinconada, Argentina (`M-rinconada`; *Aberlemnia caledonica*) | none | Capel has no Argentine Silurian crown row; its nearest is *Aberlemnia* cf. *caledonica* in Bolivia |
| Xiemisitai, West Junggar (`pbdb:278439`; *Aberlemnia* sp.) | none | |
| Mangkelu II, Wutubulake, Hoboksar (`M-mangkelu-ii`; *Zosterophyllum mangkeluense*) | Wutubulake Fm, Hoboksar (*Wutubulaka multidichotoma*, Late Pridoli) | formation and district; does not identify Mangkelu II |
| West Junggar (`M-aberlemnia-junggaria`; *Aberlemnia junggaria*) | none | Capel lists no *A. junggaria* |
| Bathurst Island US383, US384, US385, US688 (cf. *Bathurstia*, *Distichophytum*, *Macivera gracilis*, *Zosterophyllum* spp.) | Bathurst Island Fm, Polar Bear Pass: one locality, the same six taxa, Ludfordian | locality and taxa; S0's four units are one in S3, and Capel's age (425.0–422.7 Ma) is narrower than S0's (425.0–419.62 Ma) |
| Qujing (`M-qujingense`; *Z. qujingense*) | Upper Yulongsi Fm, Qujing (*Z. qujingense*, Pridoli) | locality and species |
| Karlštejn, Bohemia (`M-baragwanathia-karlstejn`; *Baragwanathia brevifolioides*) | Požáry Fm, Kosov Hill (*B. brevifolioides*, Early Pridoli) | one published holotype (KR 1) under conflicting locality labels: one occurrence, both labels kept |
| Rashkovskie Beds, Podolia (`pbdb:52702`; *Cooksonia*, *Protosawdonia* and others) | Upper Rashkovskie Beds Fm, Trubchin (*Zosterophyllum ?* sp., Pridoli) | village and member; bed not established |
| Skala, Podolia (`pbdb:13873`; *Zosterophyllum*) | none | no separately identifiable equivalent |
| Van Canh, Vietnam (`M-van-canh`; putative zosterophylls) | Van Canh Fm, Dô Son (*Aberlemnia ?* sp., Pridoli) | locality and formation |
| Yea: Ghin Ghin Road (two units), Limestone Road | Ghin Ghin Loc. 1 (rows 734, 1199, and 124 as a possible duplicate) | S3-A11, S3-A18 (`ref`; 124 and B2 separate in the sensitivities); Capel's Limestone Road rows are not crown |
| — | Lipeon Fm, Jarcas, Bolivia (*Aberlemnia cf. caledonica*, Ludlow) | S3_permissive only (S3-A12) |
| — | Tokrau Horizon, Balkhash, Kazakhstan (*Baragwanathia? sp.*, *Jugumella burubaensis*, Pridoli) | in S3, not S0 |

**Region–stage comparison (Silurian-only units).** Cells are region × midpoint stage.

| Inventory | Locality units | Cells |
|---|---:|---|
| S0 | 13 | Baltica, Gondwana-South-America, Kazakhstania, Laurentia, South-China, peri-Gondwana-Europe (all Přídolí) |
| S3 main, S3 f3_strict | 7 | Baltica, Kazakhstania, South-China, peri-Gondwana-Europe (Přídolí); Laurentia (Ludfordian) |
| S3 yea_literal | 8 | as main, plus Gondwana-Australia-Antarctica (Ludfordian; row 124 at its literal age) |
| S3 permissive | 8 | as main, plus Gondwana-South-America (Ludfordian) |
| S3 capel_groups | 6 | as main |

- Four cells coincide. Laurentia sits in the Ludfordian in S3 because Capel dates Bathurst Ludfordian, where
  S0 has Ludfordian–Přídolí.
- Neither the shared regions nor the unit counts establish which way S3 moves the late-Silurian fraction.
  Gemini's statement that S3 favours a higher Silurian share remains not shown, and so does the opposite.

### Repairs after Codex's reconciliation review (S3-A18 to S3-A20)

Codex's reconciliation review ([2026-11-22-inventory-symmetry-reconciliation-review.md](2026-11-22-inventory-symmetry-reconciliation-review.md))
is accepted in full.

1. **Yea identity (S3-A18).** The A11 claim that the identity of rows 124 and 1199 changes only locality
   counts was wrong: under the boundary placements of S3-A15, two Yea horizons can fill a Gorstian and a
   Přídolí cell where one horizon fills one. `ref` (deciding) follows F3: row 124 joins Loc. 1 as a possible
   duplicate (L3S-015) and row 1199 sits at Loc. 1 (assumed). `y124`, `b2` (1199 at B2, Přídolí–Emsian) and
   `y124_b2` are sensitivities, and B2 never takes an older stage than Loc. 1. The Yea units have 6, 21, 18
   and 38 admissible stage sets under the four treatments, and every treatment except `ref` lets the Yea
   units fill two Silurian cells. A structural run of the placement code on S3 main and f3_strict under each
   treatment finishes and gives different sets of admissible pairs; the pairs themselves were not printed
   and no share or test was computed.
2. **Placement enumeration.** Placements are now enumerated per region as sets of occupied stages and then
   combined, as in Codex's independent check. This scales to S3, which has more boundary units than S0. On
   S0 it gives the same nine pairs per interval, with or without the bed order, and every S0 output column
   is unchanged apart from the factor.
3. **Upper factor (S3-A19).** The factor is now the upper crossing of the smallest lower share over the
   admissible pairs. On S0 named cells it is 2.364903 (Gorstian–Přídolí) and 1.472918 (Ludfordian–Přídolí),
   reproducing Codex; the old fixed-pair factors (1.809959, 0.928215) and the committed `switch_reading.csv`
   factors stay in `fixed_pair_factor_legacy`, and the harness asserts both sets.
4. **Record corrections (S3-A20).** S0's Kazakhstania crown cell is West Junggar, not the Kazakh PBDB
   outcrops; the nine-pair result is conditional on the midpoint convention (17 pairs if every unit varies).

## For Codex's sign-off (repairs)

Second round, 23 November 2026: S3-A18 to S3-A20, `capel_s3_yea_units.csv` and the S0 factors in
`inventory_symmetry_tests_S0.csv`. The first-round items follow.

1. S3-A10 to S3-A14 and the row-level check in `capel_s3_disputed_rows.csv`: rows 6, 8, 124, 128, 297,
   477, 530, 734, 904, 906, 1130, 1146, 1191 and 1199, and the pooled rows 47, 158 and 556.
2. The counting rules (S3-A15) and tail rules (S3-A16), as implemented in `inventory_symmetry_tests.py` and
   run on S0.
3. The S3 gate restatement (S3-A17), including S3 main as the deciding reading and the reading-dependence
   rule.
4. Whether `S3_f3_strict` should be the deciding S3 reading in place of main, since it matches F3's crown
   definition more closely. Recommendation: keep main as frozen in §3 and let f3_strict trigger
   "narrower" through S3-A17.

## Stage 2 results (23 November 2026)

Codex signed off Stage 1 at `480ed4a` (`088f592`). The conventions the gates left open were frozen as
S3-A21 to S3-A24 and committed (`fbe79ef`) before any S1–S3 number existed. Everything below is
preliminary until Codex has checked it.

Codex independently reproduced the submitted rows and returned the missing regional comparisons, a
Capel selector and wording repairs before ledger integration. [Stage 2 review, 23 November](2026-11-23-inventory-symmetry-stage2-review.md)
The repairs follow, under the post hoc convention S3-A25; they change no verdict of gates 1–4c.

**Code and outputs.** `studies/f3/models/loop3/inventory_symmetry_stage2.py` imports the signed-off harness
(`inventory_symmetry_tests.run`) and the functions of `analysis.py`, `groups.py` and
`interval_feasibility.py`. It never calls their `main` or `run`, and writes only these files:

| File | SHA-256 |
|---|---|
| `out/inventory_symmetry_stage2_tests.csv` (Tasks 3 and 6: C59 placement, C60, C27/C48 arithmetic) | `517c05f03ce43b685959ed3d9eafa6683ef1873d02603b87fe3792d0ceec928f` |
| `out/inventory_symmetry_stage2_task4.csv` (Tasks 4.1, 4.2 and 6, with jointly possible columns) | `e459a6af2c8e4cb76dd42252fb9da7dbc3355106d40671079d1093c8119dff97` |
| `out/inventory_symmetry_stage2_groups.csv` (B1, B0 on S0 and S1: limits, folds, gap and spore benchmarks) | `0b1393e4cf473e665bb396d160d22cc892fe6c21efc2a3a560c99ee28c4472cb` |
| `out/inventory_symmetry_stage2_shape.csv` (Task 5: KS feasibility over four inclusion states) | `f2b2612550235d3a241e0d8cbc4e22e67f8e475c51ef50f350e3eea9c7918c3a` |
| `out/inventory_symmetry_stage2_gates.csv` (gate evaluator, gates 1–5) | `96ebf23993debb394d80bec50fd82750a00858a41d553f012912549c6670afdd` |

Reproduce: `uv run studies/f3/models/loop3/inventory_symmetry_stage2.py` (about 40 s on `mini`).

**Reproduction checks.** All sets are computed first. `check_s0` then asserts the S0 values below before any output is written; a failure writes nothing.
This departs from S3-A24, which asked for the S0 assertions before any other set is read. Gemini's
preliminary S1 and S2 sums had also informed the gate thresholds before the conventions were frozen.
- The S0 rows of the tests table equal the signed `inventory_symmetry_tests_S0.csv` byte for byte.
- `reviewed_bounds.csv`: all six histories at the Emsian and Přídolí cutoffs (B2 main primary). This
  includes 429.80490705 Ma for decline10 at the Přídolí cutoff, and the two decline10-type rows that are
  beyond the domain.
- `groups.csv` and `groups_inside.csv` for B1 and B0: steady limits under all four counting rules, the folds,
  the gap and Homerian benchmarks, and the spore-anchored factors.
- `interval_feasibility_summary.csv` (B2) and `groups_shape.csv` (B0 with and without Oman, B1 main and
  inclusive): p values and finite-sample verdicts in every inclusion state.
- Gemini's preliminary values where comparable:
  - S1: 69 units, lower ratios 0.541 (locality–age) and 0.622 (legacy pair, 6 of 21).
  - S2b: 5 of 59, ratio 0.160; legacy pair 3 of 18.
  - Spore-share placement p: 0.174 (S2a) and 0.496 (S2b).
  - S1 folds 11.73–17.16 with T = 428.17 Ma.
  - Bathurst anchoring: T = 427.17 Ma, folds 8.75–12.44.
  - Devonian-free bound 428.53 Ma at k = 13.

### Gate outcomes

Deciding sets: S1, S2b and S3 main with Yea treatment `ref` (S3-A21). "Changed by" lists alternative sets
that would change the outcome if swapped in.

| Gate | Outcome | What decides it | Changed by |
|---|---|---|---|
| 1. C59: rock and rock × spore fail later-find placement | **Holds** | An excess is established in every required cell: S1 and S2b at both grains, S3 cells, both intervals, A = 426.7 and 425.0 Ma. The largest p is 0.00051 on the deciding sets and 0.0022 with S2b_coord. | none (every variant, S3 reading and Yea treatment holds) |
| 2. C59: spore share alone fails | **Narrower, inventory-dependent** under S3-A17. Under the specification's literal wording (S2b and S3 at locality–age): **withdrawn** | Established on S1 (p ≤ 0.0045) and on S3 named cells (p 0.016–0.042); not on S2b (locality–age p 0.27–0.50; cells 0.060–0.144). S3's locality–age p is 0.49–0.76, but S3-A17 makes those rows descriptive. With the pooled codes counted, S3's Gorstian–Přídolí cell is not established (0.064); Ludfordian–Přídolí still is (0.026–0.028). | none |
| 3. C60: late-Silurian rate near the window mean | **Narrower** (the specification's narrower form) | No set rejects level at region–stage, and no deficit is established at cells. Lower ratios at cells: S1 0.62–0.78; S2b 0.23–0.31 (3 regions); S3 0.39–0.49 (5 regions). At locality–age, S2b establishes a Gorstian–Přídolí deficit (largest p 0.047). The withdrawal conditions are not met. | none |
| 3b. Gate 3 at A = 425.0 Ma | Narrower | S1 0.71/0.86; S2b 0.21/0.33; S3 0.48. The S2b locality–age deficit is not established at 425.0 Ma (p 0.060). | none |
| 4a. C27: flat passes the shape test | **Holds**; 428.8 Ma stands | flat passes in every inclusion state on S0, S1 and S2b | none |
| 4b. C49: decline10 fails the shape test | **Narrower** | Fails in every state on S0 and S1 (best p 0.0064). Passes in every state on S2b (best p 0.24–0.30). Withdrawal would need S3, which has no shape test. | S2a and S2a_coord: decline10 fails there too, so swapping either in for S2b gives "holds" |
| 4c. C49: decline25 fails on the guaranteed finds | **S0-specific; drop** | S0 guaranteed state fails (0.035). S1 and S2b pass in the guaranteed and all-possible states (S1 0.83–0.88; S2b 1.0). | none |
| 5. C48, C58, C61, C62: requirements | **Holds, with sensitivity in both directions** | Full-window locality–age folds at 444/452 Ma rise from 8.08/11.82 (S0) to 11.73/17.16 (S1) and 10.00/14.62 (S2b). The Devonian-free regional folds fall below the specification's 3.0–9.4 baseline: on S2b, 1.43/2.08 with every cell, and without Bathurst 1.43/2.08 jointly possible (0.70/1.03 under the envelope). See the repairs below. | — |

**Gate code edited after the first run.** Only the conventions (S3-A21 to A24) preceded the numbers. After
the first run I redefined gate 4c to the specification's wording (decline25 in the guaranteed and
all-possible states, rather than in any state) and added gate 3b, which S3-A22 requires. After Codex's
review (S3-A25) the 425.0 Ma selector for `yea_literal` reads its run without Yea, and a gate 5 row was
added. No edit changed an outcome of gates 1–4c.

**Pooled region–stage cells (S3-A15).**
- No deficit and no two-sided rejection changes between pooled and named cells in any set.
- Pooled lower ratios are lower: S0 0.62/0.78, S1 0.56/0.71, S2b 0.21/0.28, S3 0.34/0.44.
- Some C59 excess verdicts change, all with p 0.034–0.047 named and 0.051–0.070 pooled:
  - the spore share and search × spore share on S3 Gorstian–Přídolí (the spore cell bears on gate 2,
    above);
  - plant-excluded searching × spore share on S3 Ludfordian–Přídolí;
  - the spore share and search × spore share on S2a at 425.0 Ma.
- No gate outcome changes.

The S3 Yea treatments and readings change no gate outcome. The one exception
is the region count: S3 permissive and `yea_literal` reach six regions in one interval. S3's locality–age
rows reject a level rate in both directions (two-sided) and establish a deficit (lower ratios 0.14–0.19).
They are descriptive under S3-A17 and enter no gate.

### Gate table by set and counting rule (B2)

Each p is the largest over admissible pairs (S3-A16); "n.s." marks an excess not established. The lower
ratio is the smallest over admissible pairs. The upper factor is S3-A19's largest compatible change in
the finding rate from A to 393.47 Ma. "est." marks a deficit established at every admissible pair. Rows
at A = 425.0 Ma are Task 6. Every proxy, the expected counts and the smallest and largest rejecting counts
(amendment 6) are in `inventory_symmetry_stage2_tests.csv`.

| Set | A (Ma) | Interval | Counting | n | k | Rock / rock×spore p | Spore-share p | Level: lower ratio | Level: deficit p | Two-sided rejected | Upper factor | Regions |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| S0 | 426.7 | Gorstian–Přídolí | locality–age | 48 | 13–16 | 6.4e-16 | 5.9e-05 | 0.790 | 0.983 | no | 1.76 | 6 |
| S0 | 426.7 | Ludfordian–Přídolí | locality–age | 48 | 13–16 | 6.4e-16 | 3.6e-06 | 1.039 | 0.999 | no | 0.90 | 6 |
| S0 | 426.7 | Gorstian–Přídolí | cells, named | 17–20 | 6–9 | 1.7e-08 | 0.003 | 0.692 | 0.996 | no | 2.36 | 6 |
| S0 | 426.7 | Ludfordian–Přídolí | cells, named | 17–20 | 6–8 | 2.4e-08 | 0.00089 | 0.862 | 0.999 | no | 1.47 | 6 |
| S0 | 425 | Ludfordian–Přídolí | locality–age | 45 | 13 | 2.5e-16 | 2e-06 | 1.056 | 0.985 | no | 0.88 | 6 |
| S0 | 425 | Ludfordian–Přídolí | cells, named | 17 | 6 | 7.8e-09 | 0.00037 | 0.975 | 0.983 | no | 1.06 | 6 |
| S1 | 426.7 | Gorstian–Přídolí | locality–age | 69 | 13–16 | 1.1e-13 | 0.003 | 0.541 | 0.708 | no | 3.95 | 6 |
| S1 | 426.7 | Ludfordian–Přídolí | locality–age | 69 | 13–16 | 1.1e-13 | 0.00022 | 0.712 | 0.954 | no | 2.33 | 6 |
| S1 | 426.7 | Gorstian–Přídolí | cells, named | 19–22 | 6–9 | 3.3e-08 | 0.004 | 0.622 | 0.990 | no | 2.97 | 6 |
| S1 | 426.7 | Ludfordian–Přídolí | cells, named | 19–22 | 6–8 | 4.5e-08 | 0.002 | 0.778 | 0.997 | no | 1.89 | 6 |
| S1 | 425 | Ludfordian–Přídolí | locality–age | 66 | 13 | 5.8e-14 | 0.00016 | 0.707 | 0.773 | no | 2.18 | 6 |
| S1 | 425 | Ludfordian–Přídolí | cells, named | 19 | 6 | 1.7e-08 | 0.00072 | 0.864 | 0.968 | no | 1.41 | 6 |
| S2a | 426.7 | Gorstian–Přídolí | locality–age | 38 | 5–7 | 2.9e-05 | 0.174 (n.s.) | 0.250 | 0.421 | no | 16.19 | 3 |
| S2a | 426.7 | Ludfordian–Přídolí | locality–age | 38 | 5–7 | 2.9e-05 | 0.076 (n.s.) | 0.329 | 0.734 | no | 11.12 | 3 |
| S2a | 426.7 | Gorstian–Přídolí | cells, named | 14–15 | 3–5 | 0.00035 | 0.108 (n.s.) | 0.267 | 0.921 | no | 14.51 | 3 |
| S2a | 426.7 | Ludfordian–Přídolí | cells, named | 14–15 | 3–5 | 0.00035 | 0.058 (n.s.) | 0.351 | 0.976 | no | 9.88 | 3 |
| S2a | 425 | Ludfordian–Přídolí | locality–age | 36 | 5 | 2.2e-05 | 0.067 (n.s.) | 0.330 | 0.406 | no | 9.14 | 3 |
| S2a | 425 | Ludfordian–Přídolí | cells, named | 13 | 3 | 0.00022 | 0.042 | 0.387 | 0.832 | no | 6.92 | 3 |
| S2b | 426.7 | Gorstian–Přídolí | locality–age | 59 | 5–7 | 0.00024 | 0.496 (n.s.) | 0.160 | 0.047 (est.) | no | 33.91 | 3 |
| S2b | 426.7 | Ludfordian–Přídolí | locality–age | 59 | 5–7 | 0.00024 | 0.282 (n.s.) | 0.210 | 0.240 | no | 24.52 | 3 |
| S2b | 426.7 | Gorstian–Přídolí | cells, named | 16–17 | 3–5 | 0.00051 | 0.144 (n.s.) | 0.234 | 0.866 | no | 18.10 | 3 |
| S2b | 426.7 | Ludfordian–Přídolí | cells, named | 16–17 | 3–5 | 0.00051 | 0.079 (n.s.) | 0.308 | 0.956 | no | 12.54 | 3 |
| S2b | 425 | Ludfordian–Přídolí | locality–age | 57 | 5 | 0.00021 | 0.271 (n.s.) | 0.206 | 0.060 | no | 19.92 | 3 |
| S2b | 425 | Ludfordian–Přídolí | cells, named | 15 | 3 | 0.00035 | 0.060 (n.s.) | 0.333 | 0.755 | no | 9.00 | 3 |
| S3 main, ref | 426.7 | Gorstian–Přídolí | locality–age | 109 | 7–8 | 8.4e-05 | 0.759 (n.s.) | 0.143 | 6.9e-05 (est.) | yes | 40.21 | 5 |
| S3 main, ref | 426.7 | Ludfordian–Přídolí | locality–age | 109 | 7–8 | 8.4e-05 | 0.487 (n.s.) | 0.189 | 0.005 (est.) | yes | 29.37 | 5 |
| S3 main, ref | 426.7 | Gorstian–Přídolí | cells, named | 25–26 | 5–6 | 3.3e-06 | 0.042 | 0.386 | 0.690 | no | 7.53 | 5 |
| S3 main, ref | 426.7 | Ludfordian–Přídolí | cells, named | 25–26 | 5–6 | 4.1e-06 | 0.018 | 0.488 | 0.885 | no | 5.24 | 5 |
| S3 main, ref | 425 | Ludfordian–Přídolí | locality–age | 108 | 7 | 7.9e-05 | 0.497 (n.s.) | 0.181 | 0.001 (est.) | yes | 24.60 | 5 |
| S3 main, ref | 425 | Ludfordian–Přídolí | cells, named | 25 | 5 | 3.3e-06 | 0.016 | 0.482 | 0.755 | no | 4.63 | 5 |

Variants, at natural A:
- S1_with_28303 and S1_merged give locality–age ratios 0.53–0.75.
- S2b_with_28303, S2b_merged and S2b_coord give 0.11–0.22.
- The S2b locality–age deficit at Gorstian–Přídolí is established on S2b, S2b_with_28303 and S2b_coord,
  and not on S2b_merged (p 0.068).
- Every S1 and S2 variant matches its base set at region–stage.

### Task 4: requirements and limits

**4.1, full window (c = 393.47 Ma).**

| Set, A | n locality–age; T (Ma); folds 444/452 | n region–stage; T; folds |
|---|---|---|
| S0, 426.7 | 48; 428.84; 8.08/11.82 | 19; 432.38; 3.05/4.46 |
| S1, 426.7 | 69; 428.17; 11.73/17.16 | 21; 431.80; 3.40/4.97 |
| S2a, 426.7 | 38; 429.43; 6.35/9.28 | 16; 433.54; 2.53/3.70 |
| S2b, 426.7 | 59; 428.43; 10.00/14.62 | 18; 432.72; 2.88/4.20 |
| S3 main ref, 426.7 (descriptive) | 109; 427.63; 18.68/27.32 | 28; 430.45; 4.61/6.74 |
| S0, 425.0 (Task 6) | 45; 427.17; 8.75/12.44 | 19; 430.38; 3.53/5.01 |
| S1, 425.0 | 66; 426.46; 12.98/18.44 | 21; 429.83; 3.93/5.58 |
| S2b, 425.0 | 57; 426.70; 11.17/15.87 | 17; 431.08; 3.13/4.44 |

- **Six-history older bounds (C27).** These are at natural A, locality–age.
  - S1: flat 428.17, PBDB 428.20, plant-excluded 427.91, decline25 429.99, plant-excluded × decline10
    438.42; decline10 sets no limit within 469.4 Ma.
  - S2b: flat 428.43, decline25 430.61, plant-excluded × decline10 444.99; decline10 none.
  - At 425.0 Ma, S0 flat gives 427.17 and decline25 429.78.
  - The full table, including S3, is in `task4.csv`.
- **B1 and B0 (C61, C62), S0 → S1.**
  - B1 main: steady limits by counting rule 434.09–437.19 → 433.76–436.77 Ma, still older than 431.2 Ma.
    Folds 6.34/10.92 → 8.60/14.80.
  - B0 spore anchor: 8.41 → 11.29 with Oman (region–stage 3.24 → 3.58); without Oman 13.39 → 17.94
    (5.19 → 5.74).

**4.2, Devonian-free window (c = 419.62 Ma, guaranteed Silurian-only units; conservative envelope — the
jointly possible limits are in the repairs below).**

| Set, A | k | Constant T (Ma); folds 444/452 | decline10 T | Bathurst collapsed (k; T) | Bathurst removed (k; A; T) |
|---|---|---|---|---|---|
| S0 = S1, 426.7 | 13 | 428.53; 9.43/13.79 | 429.80 | 10; 429.17 | 9; 426.7; 429.50 |
| S0 = S1, region–stage | 6 | 431.28; 3.77/5.52 | — | — | — |
| S2b, 426.7 | 5 | 432.51; 2.98/4.35 | 445.35 | 4; 434.59 | 3; 426.7; 438.84 |
| S3 main ref, 426.7 | 7 | 430.48; 4.57/6.69 | 434.69 | — (one unit) | 6; 426.7; 431.28 |
| S0 = S1, 425.0 | 13 | 426.39; 13.63/19.37 | 427.04 | 10; 426.88 | 9; 422.7; 423.92 |
| S2b, 425.0 | 5 | 429.41; 4.30/6.12 | 433.79 | 4; 431.00 | 3; 422.7; 427.98 |

S1 adds only Devonian units, so its Silurian-only counts equal S0's. Removing the Bathurst section at
425.0 Ma moves A to 422.7 Ma.

### Task 5 (C49), and outcomes outside the gates

Best finite-sample p over the four inclusion states, by history (`shape.csv` holds every state):

| Set | flat | decline25 | decline10 | plant-excluded × decline10 |
|---|---|---|---|---|
| S0 | 0.985–0.998 | 0.035 (00) – 0.067 (11) | ≤ 9.3e-06 | 0.045–0.057 |
| S1 | 1.0 | 0.83–0.88 | 0.0043–0.0064 | 0.28–0.31 |
| S2a | 1.0 | 0.57–0.77 | 0.0031–0.0061 | 1.0 |
| S2b | 1.0 | 1.0 | 0.24–0.30 | 1.0 |
| S0, A = 425.0 | 0.71–0.82 | 0.011–0.025 (fails in all four states) | ≤ 2.0e-06 | 0.030–0.039 |
| S1, A = 425.0 | 1.0 | 0.64–0.70 | 0.0021–0.0034 | 0.23–0.26 |
| S2b, A = 425.0 | 1.0 | 1.0 | 0.19–0.24 | 1.0 |

With A at 425.0 Ma, decline25 fails on S0 in every state, including the all-possible state that passes at
426.7 Ma. It still passes on S1 and S2b. The pattern of gate 4 is unchanged at 425.0 Ma.

Results that bear on other claims (amendment 5: narrower, inventory-dependent):
- **C61, branched plants (B1).** On S1, decline25 passes in every inclusion state (best p 0.071–0.093).
  On S0 it fails in every state. "Declines into the past fail" holds for decline10 on both, and for
  decline25 only on S0.
- **C61, isolated early finds.** On S1, decline25 passes in every inclusion state for land-plant bodies with
  Oman (0.061–0.068) and for branched plants with Zbrza (B1 inclusive, best 0.084). "Each isolated early
  find makes every declared history fail the shape test in every inclusion state" is therefore S0-specific
  for both records. Every other history still fails on S1 for both. B0 without Oman: decline25 fails on S1
  (≤ 0.027), as on S0.
- **C61, gap benchmarks on S1** (S0 in brackets):
  - after Oman: at least 10.26 times lower (7.65); longest gap 16.60 (12.38); region–stage 3.28 (2.97);
  - after Zbrza: 8.16 (6.09); 9.84 (7.34); 2.81 (2.55);
  - Homerian after *C. barrandei*: 2.21 (1.61); 3.51 (2.56); region–stage 0.70 (0.62), still no reduction.

### Repairs after Codex's Stage 2 review (S3-A25, 23 November)

Every earlier row of `task4.csv` (1,330) and `tests.csv` (2,175) is unchanged; the repairs add rows and
columns. `groups.csv` and `shape.csv` are byte-identical. Gates 1–4c keep their verdicts and details.

**Two calculations for the oldest limit.** The conservative envelope pairs the guaranteed count with the
oldest possible age, which can come from a unit outside the guaranteed set. The jointly possible limit is
the oldest over allocations that can occur together (S3-A25). They agree in every full-window row, so
428.84 Ma (48 guaranteed locality–age units, c = 393.47 Ma) is itself a jointly possible allocation. They
differ in the Devonian-free window, where Yea straddles 419.62 Ma.

**Devonian-free window, Bathurst removed before forming cells** (c = 419.62 Ma, natural A; steady rate,
zero delay):

| Set | Counting | Envelope: k, A, T (Ma), folds 444/452 | Jointly possible: k@A, T (Ma), smallest folds |
|---|---|---|---|
| S0 = S1 | locality–age | 9, 426.7, 429.50, 6.19/9.05 | 10@426.7, 429.17, 7.00/10.23 |
| S0 = S1 | region–stage | 5, 426.7, 432.51, 2.98/4.35 | 6@426.7, 431.28, 3.77/5.52 |
| S2b | locality–age | 3, 426.7, 438.84, 1.43/2.08 | 4@426.7, 434.59, 2.19/3.21 |
| S2b | region–stage | 2, 426.7, **451.28**, 0.70/1.03 | 3@426.7, **438.84**, 1.43/2.08 |
| S3 main ref | locality–age | 6, 426.7, 431.28, 3.77/5.52 | 7@426.7, 430.48, 4.57/6.69 |
| S3 main ref | region–stage | 4, 426.7, 434.59, 2.19/3.21 | 5@426.7, 432.51, 2.98/4.35 |

- On S2b by region and stage, removing Bathurst leaves Baltica and Kazakhstania as the two guaranteed
  cells (both 422.7 Ma). Only the Australian Yea cell reaches 426.7 Ma, and placing it there adds a third
  cell. The 451.28 Ma envelope combines two Yea placements that cannot occur together. The oldest jointly
  possible steady-rate limit is 438.84 Ma, which excludes 444 Ma. With Yea outside the window the limit is
  433.39 Ma (folds 1.99/2.74). This reproduces Codex's independent check.
- Six histories on S2b without Bathurst, by region and stage (jointly possible; envelope in brackets):
  steady 438.84 (451.28), PBDB 443.08 (465.77), plant-excluded 440.79 (458.46), decline25 447.30 (beyond
  469.4 Ma); the two decline10 histories set no limit within 469.4 Ma under either. Excluding 444 Ma
  therefore holds for the steady, PBDB and plant-excluded histories, and not for decline25 or the decline10
  pair.
- With every unit kept, the published-style Devonian-free figures are envelopes too. S0: 428.53 Ma at
  k = 13 (jointly possible 428.39 at 14); region–stage 431.28 (430.48). S2b: 432.51 (431.28); region–stage
  438.84 (434.59). At 425.0 Ma the two calculations coincide on S0–S2b, because Yea is gone.
- The proposal's "3.0–9.4 at 444 Ma" describes locality–age envelopes with Bathurst kept. Gate 5 now
  records the downward regional sensitivity.

**Full-window six-history bounds by pooled midpoint region–stage cells** (c = 393.47 Ma; envelope and
jointly possible agree):

| Set, A | cells | steady | PBDB | plant-excluded | decline25 | decline10, plant-excluded × decline10 |
|---|---|---|---|---|---|---|
| S0, 426.7 | 19 | 432.38 | 432.16 | **431.21** | 442.78 | none within 469.4 Ma |
| S1, 426.7 | 21 | 431.80 | 431.67 | **430.83** | 440.58 | none |
| S2a, 426.7 | 16 | 433.54 | 433.54 | 431.99 | 447.92 | none |
| S2b, 426.7 | 18 | 432.72 | 432.45 | 431.44 | 444.18 | none |
| S3 main ref, 426.7 (descriptive) | 28 | 430.45 | 430.52 | 429.78 | 436.11 | none |
| S0, 425.0 | 19 | 430.38 | 430.61 | 429.52 | 439.14 | none |
| S1, 425.0 | 21 | 429.83 | 430.05 | 429.07 | 437.27 | none |
| S2b, 425.0 | 17 | 431.08 | 431.20 | 430.08 | 441.71 | none |

The plant-excluded bound lies just older than 431.2 Ma on S0 and just younger on S1. Codex's values
(431.2127, 430.8263; steady 432.3750, 431.7952) reproduce.

**Capel's two 425.0 Ma runs.** In the literal reading, row 124 itself reaches 425.0 Ma.

| Run | Regions | Lower ratio, named cells | Spore-share p, named cells (pooled) |
|---|---|---|---|
| `yea_literal` natural (Yea kept) | 6 | 0.619 | 0.0042 (0.0075) |
| `yea_literal` without Yea (`bathurst_425`, units equal to S3 main's) | 5 | 0.482 | 0.016 (0.026) |

Gates 1, 2 and 3b now read the run without Yea for the 425.0 Ma comparison. Before, gates 1–2 skipped it and
gate 3b used the Yea-kept run. No verdict changes. With Bathurst also removed, the Yea-kept run stays at
425.0 Ma and the run without Yea moves to 422.7 Ma.

**Spore share against C56 at the same anchor.** Reproduced from `rulers.py`'s functions: the spore-share
contrasts are 5.1403/7.1049 at 444/452 Ma with A = 426.7 Ma (matching counts 31.05/29.43) and
4.9559/6.7120 with A = 425.0 Ma (26.11/24.95). S2b's regional counts (16–18 at 426.7 Ma; 15–17 at 425.0 Ma)
lie below both pairs.

**All-collection searching.** It predicts too few late-Silurian finds on S0 by locality and age in the
Ludfordian–Přídolí: upper-tail p 0.040 at 426.7 Ma and 0.035 at 425.0 Ma (13 of 48 and of 45). No other
set, grain or interval establishes an excess for searching, and plant-excluded searching establishes none
anywhere.

**Capel locality rows (C60).** All 40 descriptive S3 locality–age rows establish a deficit and 39 reject a
level rate two-sided; the exception is S3 permissive with Yea treatment `y124_b2` in the Ludfordian–Přídolí
(deficit p 0.038, ratio 0.183).
Codex's 39 and 38 counted the rows before the literal run without Yea was added.

### Claims that change: proposed ledger wording (held, not applied)

`claims.csv`, `estimands.md`, the four texts and the figures are unchanged. Changing a bound value would
break its text bindings while the texts are frozen, so the wording is held here.

- **C60, narrowed.**
  - **Claim.** A post hoc fixed-window reading of the crown vascular-plant record. The guaranteed
    late-Silurian counts set a lower bound on the interval-average finding rate relative to the whole
    later-window mean, and that bound depends on the inventory:
    - reviewed inventory: 0.69–0.86 by named region and stage, 0.79–1.04 by locality and age;
    - with the Early Devonian PBDB collections that the duration filter had set aside restored: 0.62–0.78
      and 0.54–0.71;
    - PBDB-backed units alone: 0.23–0.31 and 0.16–0.21;
    - Capel et al.'s species-endpoint list: 0.39–0.49, by region and stage only.

    These are relative to the mean over the whole window after the oldest find (A to 393.47 Ma). Capel's
    0.39–0.49 describes how listed species endpoints fall; reading it as a fossil-finding rate would need a
    model of the intermediate occurrences the list omits.

    No inventory rejects a level rate by region and stage. Counted by locality and age, the PBDB-backed
    inventory shows a one-sided deficit for the Gorstian–Přídolí (largest p 0.047; the two-sided
    benchmark is 0.094, not rejected). The deficit is lost for the Ludfordian–Přídolí (p 0.24), with A at
    425.0 Ma (p 0.060), and with merged localities (p 0.068). Capel's locality–age rows, descriptive under
    S3-A17, show a deficit in all 40 readings and treatments and reject level two-sided in 39. Within the
    exponential family, the largest compatible rise in finding from A to 393.47 Ma (the upper crossing of
    each one-sided benchmark) is 1.5–2.4-fold on the reviewed inventory's named cells, 1.9–3.0-fold with
    the restored collections, and 12.5–18.1-fold on PBDB-backed cells (24.5–33.9 by locality and age; a
    33.91-fold rise gives p 0.0247 in the narrower locality interval). Late-Silurian finds are
    multiregional: guaranteed finds lie in six regions on the curated inventories, five in Capel's list
    and three even on PBDB-backed units. A Devonian rise in finding is a permitted interpretation; its
    timing and size remain open. A rise concentrated near A and a ramp through the Early Devonian both
    fit. C57's rise times apply to its stated shapes with a steady later rate and zero delay.
  - **Value.** The rows above, from `inventory_symmetry_stage2_tests.csv`.
  - **Limit.** Add: the inventories differ in curation (literature curation went mainly to the Silurian);
    Capel's endpoint list omits intermediate localities; the gate thresholds were set after preliminary
    sums.
- **C59, narrowed for the spore share.**
  - **Holds on every inventory:** retrospective later-window allocation strongly disagrees with finding
    proportional to rock area or to rock × spore share (S0, S1, S2a, S2b and S3 cells; p ≤ 0.00051).
  - **Spore share alone, inventory-dependent:**
    - The disagreement holds on the literature-curated inventories (S0, S1; p ≤ 0.0045) and on S3 cells
      (p 0.016–0.042).
    - Capel's support is weak: p 0.016–0.042 with named cells, and the Gorstian–Přídolí cell is not
      established when the pooled codes are counted (0.064).
    - It does not hold on PBDB-backed units (S2a, S2b; locality–age p 0.07–0.50, cells 0.04–0.14). The
      one exception is S2a's named cells at A = 425.0 Ma, where p is 0.042.
    - On PBDB-backed counts, then, the spore share is not contradicted by the later record. With A at
      426.7 Ma its 5.14- and 7.10-fold contrasts at 444 and 452 Ma exceed the required contrasts for up
      to 31.05 and 29.43 independent finds (C56); with A at 425.0 Ma the contrasts are 4.96 and 6.71 and
      the matching counts 26.11 and 24.95. S2b's regional counts (16–18 at 426.7 Ma, 15–17 at 425.0 Ma)
      lie below both, assuming the same proportional change in finding and zero delay. The later-window
      test concerns where finds fall; carrying the spore share back to earlier finding is an assumption.
      S1's cells reject the spore share.
    - The spore share's failure is therefore not confined to curated inventories: Capel's named cells and
      S2a's named cells at A = 425.0 Ma also reject it. It is inventory-dependent.
  - Searching (upper tail, P(X ≥ k_min)): plant-excluded searching is compatible in every comparison.
    All-collection searching predicts too few late-Silurian finds on the reviewed inventory by locality
    and age in the Ludfordian–Přídolí (p 0.040 at 426.7 Ma; 0.035 at 425.0 Ma) and is compatible in every
    other comparison. The existing C59 phrase "does not reject ... the searching measure" refers to the
    Gorstian–Přídolí minimum count and should say so.
- **C49, narrowed.**
  - Pure decline10 fails in every inclusion state on the reviewed and restored inventories (S0, S1) and on
    PBDB-backed units without the restored Early Devonian collections (S2a). It passes in every state on
    PBDB-backed units with them (S2b; best p 0.24–0.30). All 21 guaranteed S2b units beyond S2a's span the
    whole Early Devonian. For S2b's 59 guaranteed units decline10 admits a best finite-sample p of 0.2384,
    against less than 10⁻¹⁹ at midpoint placement (Codex's check): the test shows that a compatible allocation exists.
  - Keep the S0 decline25 values with their counts at the natural anchor (48 guaranteed units p 0.03522;
    50 possible units 0.06713) and drop the general statement that decline25 fails: it passes in every
    state on S1 and S2b.
  - Qualify the land-plant-body (B0) result for Oman, as for C61: on S1 decline25 passes in every
    inclusion state with Oman (0.061–0.068) and fails without it (at most 0.027). On the Zbrza-inclusive
    branched reading (B1 inclusive) it passes (0.077–0.084).
- **C27, holds; add sensitivity.**
  - 428.84 Ma is the steady-rate limit for S0's 48 guaranteed locality–age units with c = 393.47 Ma, and
    it is a jointly possible allocation. Steady-rate limit on the other sets: S1 428.17 Ma, S2b 428.43,
    S2a 429.43 (S3 describes endpoints only: 427.63). With A at the Bathurst Ludfordian (425.0 Ma): 427.17
    (S0) and 426.46 (S1).
  - With c = 393.47 Ma, decline10 sets no limit within 469.4 Ma on S0–S2b. With the Silurian-only cutoff
    (c = 419.62 Ma) it gives 429.80 Ma on S0 under the envelope (429.52 jointly possible).
  - By pooled midpoint region–stage cells the plant-excluded history gives 431.21 Ma on S0 (19 cells) and
    430.83 Ma on S1 (21 cells), on either side of 431.2 Ma.
- **C48 and C58, hold; add sensitivity.** Zero-delay folds at 444/452 Ma are 8.08/11.82 on S0, 11.73/17.16
  on S1 and 10.00/14.62 on S2b. Region–stage folds change little: 3.05/4.46 on S0, 3.40/4.97 on S1 and
  2.88/4.20 on S2b. Bathurst anchoring gives 8.75/12.44 (S0). S1's spore-anchored B0 requirement with
  Oman is 11.29 by locality and age and 3.58 by region and stage, conditional on recognisability.
  - The Devonian-free check (c = 419.62 Ma), locality–age envelope with every unit: 9.43/13.79 on S0 and
    S1 and 2.98/4.35 on S2b (5 Silurian units). By region and stage on S2b it falls to 1.43/2.08. With
    Bathurst removed before forming the cells, S2b's oldest jointly possible steady-rate limit is 438.84 Ma
    (folds 1.43/2.08), which excludes 444 Ma; the envelope's 451.28 Ma (0.70/1.03) pairs two Yea placements
    that cannot occur together. Each quoted fold names its calculation.
- **C61, narrowed.**
  - The steady-rate limits stay older than 431.2 Ma on S1 (433.76–436.77 Ma).
  - "Declines into the past fail" for the branched record becomes "decline10 fails; decline25 fails on the
    reviewed inventory and passes once the Early Devonian collections are restored".
  - The statement that each isolated early find (Oman, Zbrza) makes every declared history fail in every
    inclusion state becomes S0-specific: on S1, decline25 passes for both.
  - Gap benchmarks rise on S1: Oman 7.65 → 10.26, Zbrza 6.09 → 8.16. The Homerian benchmark is 1.61 → 2.21,
    and still shows no reduction by region and stage.
- **C62, holds; add sensitivity.** The factor rises from 8.4 to 11.3 with the restored collections
  (region–stage 3.2 → 3.6), and without Oman from 13.4 to 17.9.

### Text changes the proposals require (not made)

- **Abstract.**
  - Replace "Late-Silurian fossils turned up at two-thirds or more of their average rate after the oldest
    find" with the inventory-dependent statement: at least two-thirds in the curated inventory, as low as
    about a sixth to a third in PBDB-backed counts, and multiregional in every inventory.
  - Restate "neither matches the finds": rock area fails on every inventory; the spore share's failure
    depends on the inventory (it holds on S1 and on Capel's named cells, not on PBDB-backed units).
  - The 2.4–12 range and the limits keep the reviewed-inventory baseline, naming the calculation; the
    Devonian-free regional check without Bathurst reaches folds of 1.43/2.08 on S2b (gate 5).
- **Results (d)** (C49, not in the requested list, but bound to the same claim). The decline25 sentence
  ("fails under every assignment of the 48 finds") needs qualifying as reviewed-inventory-specific. The
  decline10 sentence ("predicts a spread of fossil ages unlike the one observed, however the uncertain
  ages are assigned") holds for the curated inventories and not for S2b. The land-plant-body statement
  needs the Oman qualification (C49, C61).
- **Results (g).**
  - Keep the rock-area and product statements.
  - The spore share's failure becomes inventory-dependent.
  - "Searching, the one measure compatible with this minimum-count allocation" names plant-excluded
    searching, records that all-collection searching fails the reviewed inventory's Ludfordian–Přídolí
    locality check (p 0.040; 0.035 at 425.0 Ma), and adds the spore share on PBDB-backed inventories. The
    spore share's fall is large enough for ancestors at 444–452 Ma at regional counts, compared at the
    same anchor (C56).
- **Results (h).**
  - Retitle from "two-thirds or more".
  - Replace 0.79/0.69 with the inventory ranges.
  - Replace the 1.8- and 2.4-fold exponential bounds with the S3-A19 values and their inventory range,
    which reaches 12–34-fold on PBDB-backed counts.
  - "six regions" becomes five to six, three on PBDB-backed units.
  - The steep-rise passage (C57) stays conditional on a steady later rate. Note that a Devonian ramp
    removes that premise.
- **Interpretation paragraph.** Demote the switch to one conditional reading alongside a ramp of finding
  through the Early Devonian, which the PBDB-backed counts allow. The paragraph's population-growth
  arithmetic applies only under the switch reading.
- **Conclusion.**
  - Rock area keeps "carries little weight". The spore share's dismissal becomes inventory-dependent.
  - "The pooled late-Silurian finds limit how low the interval's average rate could be, and come from six
    regions" becomes inventory-dependent.
  - The steep-climb sentence is conditional on a steady later rate, which the PBDB-backed counts do not
    require.
- **Elsewhere.** These follow the same claims:
  - Results (i) and Table 2 ("Yes; declines fail" for branched plants; C61);
  - the supplement's C49, C59, C60 and C61 passages;
  - the brief and the agent guide;
  - Figure 3b's hard-coded searching and spore labels (`figures_main.py`) and the matching `estimands.md`
    wording, held with the ledger proposals: neither file is edited in this tranche.
