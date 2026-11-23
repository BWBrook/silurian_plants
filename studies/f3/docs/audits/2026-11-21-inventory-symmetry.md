# Inventory-symmetry audit: execution record

Claude (Opus 5.5), from 21 November 2026. Specification and Fable's amendments:
`2026-11-21-inventory-symmetry-spec.md`. Frozen S3 rules: `2026-11-21-inventory-symmetry-s3-rules.md`
(committed `7b6e3ae` before any S3 parse). Board discussion 191.

**Stage 1 status (this record), 23 November 2026.**
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

## Stage 2 (after sign-off)

Run Tasks 3, 4 and 6 on S0, S1, S2a, S2b (with variants) and on the S3 readings, each S3 reading under the
four Yea treatments of S3-A18 and `yea_literal` at 425.0 Ma, and Task 5 on S0–S2b, under S3-A15 to S3-A19.
- Report the legacy region–stage pair beside the cell rule.
- For every set, report the expected count, the smallest count rejected high and the largest count
  rejected low (amendment 6).
- Run all six histories in Task 4.2 (amendment 7). Then build the gate table. Any outcome outside the stated
gate cases counts as "narrower, inventory-dependent" (amendment 5). The gate thresholds were set after
Gemini's preliminary sums on S1 and S2: they are decision rules, not a blind pre-registration. Ledger
changes follow both agents' verification and, while the texts stay frozen, are held as written proposals
here.
