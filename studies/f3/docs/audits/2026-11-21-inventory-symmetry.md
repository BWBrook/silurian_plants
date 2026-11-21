# Inventory-symmetry audit: execution record

Claude (Opus 5.5), from 21 November 2026. Specification and Fable's amendments:
`2026-11-21-inventory-symmetry-spec.md`. Frozen S3 rules: `2026-11-21-inventory-symmetry-s3-rules.md`
(committed `7b6e3ae` before any S3 parse). Board discussion 191.

**Stage 1 status (this record): Tasks 1A and 1B are done. No share or test has been computed on S1, S2a, S2b
or S3: Fable's order puts the S3 sign-off before any share, and this record reads that strictly. Only the
Tasks 3–4 harness for C59, C60 and C27/C48 exists, and it has run on S0 alone to prove it reproduces the
committed values. Task 4.2, Task 5 and Task 6 are not built yet. The S3 mapping awaits Codex's sign-off.** No text, figure, ledger, estimand or frozen output was changed.

## Code and outputs

| File | Role |
|---|---|
| `studies/f3/models/loop3/inventory_symmetry.py` | Task 1A: disposition table; builds S0, S1, S2a, S2b and variants from `horizons_reviewed.csv` without changing it |
| `studies/f3/models/loop3/capel_s3.py` | Task 1B: S3 parse under the frozen rules; mapping tables; no counts |
| `studies/f3/models/loop3/inventory_symmetry_tests.py` | Tasks 3–4 harness (C59 placement, C60, C27/C48 arithmetic) |
| `out/inventory_symmetry_dispositions.csv` | SHA-256 `2885c100e3a2ef3b81f2da958e2fad89ce6410d38abc65cd0590886b71ed311e` |
| `out/inventory_symmetry_units.csv` | `ad76a374292b309fb1a4b28afbbb70159a55a32ec342fe721f65c1a09db6ba29` |
| `out/capel_s3_rows.csv` | `aa0cc0216efed9cda81e52427ebdb8788f13cb437a78a217263c1b7868c43e44` |
| `out/capel_s3_age_map.csv` | `9c5bc82f9851492137dc1848e03563656ecadb328169d207840117ca2f0a9e1f` |
| `out/capel_s3_region_map.csv` | `ba49e1650304b98395c670e8e3797e2102b0f9b07adc04c3dbf2a1823171787d` |
| `out/capel_s3_fuzzy_merges.csv` | `48b30d8e474b0eab9ef028d3ebe388ddd309aebcca4ea632f1e8ceecce792736` |
| `out/inventory_symmetry_tests_S0.csv` | `850e32b4a90ce302bda469433e4b87dea3d9bf35b4614d239fcb6d13e5c668dd` |

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

The frozen rules held for crown assignment, ages and regions, with no conflict between F3's genus
classification and Capel's group (328 rows assigned by F3 genus, the rest by group). Crown rows: 999;
unresolved (Basal eutracheophytes and Incertae sedis without an F3 decision): 123; not crown: 76. Ages:
401 rows reach into the window, 796 lie outside it and 1 is blank.

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

### Crosswalk of Silurian crown units, S0 and S3 (amendment 3)

S3 rows are Capel crown rows whose literal range reaches above 419.62 Ma. Yea rows carry F3's envelope in
S3 main.

| S0 unit and its taxa (13 Silurian-only, 3 Yea) | S3 match | Basis |
|---|---|---|
| Rinconada, Argentina (`M-rinconada`; *Aberlemnia caledonica*) | none | Capel has no Argentine Silurian crown row; its nearest is *Aberlemnia* cf. *caledonica* in Bolivia |
| Xiemisitai, West Junggar (`pbdb:278439`; *Aberlemnia* sp.) | none | |
| Mangkelu II, Wutubulake, Hoboksar (`M-mangkelu-ii`; *Zosterophyllum mangkeluense*) | Wutubulake Fm, Hoboksar (*Wutubulaka multidichotoma*, Late Pridoli) | locality and formation; taxa differ |
| West Junggar (`M-aberlemnia-junggaria`; *Aberlemnia junggaria*) | none | Capel lists no *A. junggaria* |
| Bathurst Island US383, US384, US385, US688 (cf. *Bathurstia*, *Distichophytum*, *Macivera gracilis*, *Zosterophyllum* spp.) | Bathurst Island Fm, Polar Bear Pass: one locality, the same six taxa, Ludfordian | locality and taxa; S0's four units are one in S3, and Capel's age (425.0–422.7 Ma) is narrower than S0's (425.0–419.62 Ma) |
| Qujing (`M-qujingense`; *Z. qujingense*) | Upper Yulongsi Fm, Qujing (*Z. qujingense*, Pridoli) | locality and species |
| Karlštejn, Bohemia (`M-baragwanathia-karlstejn`; *Baragwanathia brevifolioides*) | Požáry Fm, Kosov Hill (*B. brevifolioides*, Early Pridoli) | same species and formation, different locality name; unresolved without outside search |
| Rashkovskie Beds, Podolia (`pbdb:52702`; *Cooksonia*, *Protosawdonia* and others) | Upper Rashkovskie Beds Fm, Trubchin (*Zosterophyllum ?* sp., Pridoli) | locality and formation; taxa differ |
| Skala, Podolia (`pbdb:13873`; *Zosterophyllum*) | none | |
| Van Canh, Vietnam (`M-van-canh`; putative zosterophylls) | Van Canh Fm, Dô Son (*Aberlemnia ?* sp., Pridoli) | locality and formation |
| Yea: Ghin Ghin Road (two units), Limestone Road | Upper Yea Fm (*Baragwanathia longifolia*); Ghin Ghin Road (*Parazosterophyllum timsiae*) | Capel's Limestone Road rows are not crown |
| — | Lipeon Fm, Jarcas, Bolivia (*Aberlemnia cf. caledonica*, Ludlow) | in S3, not S0 |
| — | Tokrau Horizon, Balkhash, Kazakhstan (*Baragwanathia? sp.*, *Jugumella burubaensis*, Pridoli) | in S3, not S0 |

**Bias, as far as the Silurian side shows.** S3 has 8 Silurian-only crown locality–age units (Podolia,
Bolivia, Balkhash, Wutubulake, Bathurst, Van Canh, Qujing, Kosov) against S0's 13. Six match S0 units,
counting Kosov and Karlštejn as one pair. S3 also:
- collapses Bathurst's four units to one;
- lacks Rinconada, Xiemisitai, the West Junggar *Aberlemnia* and Skala;
- adds Bolivia and Balkhash.

S3's Silurian side is therefore thinner than S0's, not richer. Gemini's statement that S3's construction
favours a higher Silurian share is not shown. Its direction depends on how far endpoint-only listing thins
the Devonian side, and that waits for stage 2. On region–stage, S3's Silurian crown cells are six
(Baltica, Gondwana-South-America, Kazakhstania, Laurentia, South-China, peri-Gondwana-Europe). S0's six
regions are the same set, with Gondwana-South-America from Bolivia in S3 rather than Argentina.

## For Codex's sign-off (stage-1 gate)

1. The S3 rules, including §1: only region–stage enters the gates on S3, and Task 5 is not run on S3. This
   departs from the specification's gates 1, 2 and 4; S3-A9 restates those gates.
2. Amendments S3-A1 to S3-A9, including the proposals to drop `S3_fuzzy` and `S3_plus_unresolved`, the
   Capel-groups-only variant and the two Task 6 runs on S3.
3. The crown and region mappings (`capel_s3_rows.csv`, `capel_s3_region_map.csv`) and the age map
   (`capel_s3_age_map.csv`).
4. The Task 1A dispositions, especially the evidence for `pbdb:28216`, `28302` and `28303`, and whether the
   `_merged` variant should be primary.
5. Whether the crosswalk's Karlštejn–Kosov pairing should count as one locality.
6. The region "multiple" (Germany, Russia, Poland, following F3's PBDB rule) lumps much of S3's Devonian side
   into one region and lowers its region–stage count. S0–S2b use the same rule, so the comparison is
   like for like, but the S3 region–stage n depends on it.

## Stage 2 (after sign-off)

Run Tasks 3, 4 and 6 on S0, S1, S2a, S2b (with variants) and S3 (region–stage), and Task 5 on S0–S2b.
Report region–stage k both ways: switch_reading.py's distinct (region, min, max) among late locality–age
units, and late region–stage units counted directly, because n and k use different definitions. Report for
each S2a and S2b test the expected count and the largest count rejected (amendment 6), and run
all six histories in Task 4.2 (amendment 7). Then build the gate table. Any outcome outside the stated
gate cases counts as "narrower, inventory-dependent" (amendment 5). The gate thresholds were set after
Gemini's preliminary sums on S1 and S2: they are decision rules, not a blind pre-registration. Ledger
changes follow both agents' verification and, while the texts stay frozen, are held as written proposals
here.
