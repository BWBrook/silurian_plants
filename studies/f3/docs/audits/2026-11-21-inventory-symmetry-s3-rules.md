# S3 mapping rules: Capel, Monnet and Cascales-Miñana (2025) Table S1 (Task 1B)

Claude (Opus 5.5), 21 November 2026. Written and committed before any S3 row was parsed into units and
before any Silurian/Devonian share was computed on S0–S3. Part of the inventory-symmetry audit
(`2026-11-21-inventory-symmetry-spec.md`). Codex signed off the rules through S3-A20 and their mapping
tables at `480ed4a` on 23 November 2026, before the first S3 share. Later changes are recorded below as
dated amendments with their reasons. [Stage 1 acceptance](2026-11-23-inventory-symmetry-stage1-acceptance.md)

Source: `Table_S1_revised_Hist_Biol.xlsx`, Figshare `10.6084/m9.figshare.30281263.v1`, CC BY 4.0
(`data/external/local/deposits/capel2025-global-plant-diversity/PROVENANCE.json`), SHA-256
`d310a56da8139373a02015b2963da0d6b28a122884e1a82a031a4e21f18f1471`. Sheet `Feuil1`, 1,198 data rows below
the header: 1,004 species rows and 194 continuation rows (blank species and group cells).

## 1. What an S3 unit is, and which tests it can carry (amendment 2)

A Table S1 row is one species at one locality. A species with one row is listed at one locality. A
species with two rows is listed at its first and last localities; intermediate localities are omitted.
Of 1,004 species, 809 have one row, 195 two and one three (Fable's count, rechecked by the parser).

An S3 locality therefore enters the inventory because at least one species has an endpoint there. Its
inclusion depends on species turnover as well as on finding:

- **Locality–age counts.** The number of S3 localities in a stage grows with the number of species whose
  ranges start or end there. A stage of rapid origination and extinction gains localities. A stage
  crossed by long-ranging species loses the intermediate localities. Both effects act on the
  Silurian/Devonian share, in directions that depend on diversification, so the share of S3
  locality–age units is a composite of finding and turnover. S3 locality–age results are reported as
  descriptive only.
- **Region–stage counts.** A region–stage cell is present when any crown species has an endpoint there.
  Presence saturates: one endpoint makes the cell, so turnover adds little once a cell is occupied. A
  cell holding only range-through species is missed. Most species in the window are single-row, so such
  cells should be few; the crosswalk (§6) reports the Silurian cells S0 holds and S3 lacks. **Region–stage
  is the only S3 grain used in the gates.**
- **Shape tests (Task 5).** The interval-wide KS test treats units as independent draws from a finding
  history. S3 endpoint ages follow the timing of origination and extinction as well, so a pass or failure
  on S3 does not test a finding history. **Task 5 is not run on S3.** This departs from the specification,
  which lists S3 in Task 5 and uses S3 locality–age in gates 1, 2 and 4.

## 2. Rows and species

- Rows 4 onward of the sheet (1-based) are data. Species and group cells are forward-filled into
  continuation rows. Each row keeps its sheet row number as `capel_row`.
- Genus: the first token of the species name after removing leading `cf.`, `aff.`, `?` and quotation
  marks, and trailing `?`.

## 3. Crown vascular plants (B2, main)

Precedence, applied per row:

1. **F3 genus classification.** Collect every name in `studies/f3/data/macro/name_classifications.csv`
   whose genus (same rule) matches. If all its `crown_tracheophyte` values are `yes`, the row is B2; if
   all are `no`, it is not B2. Mixed values fall through to rule 2. This keeps S3's crown boundary the
   same as S0's wherever F3 has adjudicated the genus.
2. **Capel group.**
   - B2: Lycopsida, Zosterophyllopsida, Barinophytopsida, Basal euphyllophytes, Euphyllophyta inc. sed.,
     Cladoxylopsida, Filicopsida, Sphenopsida, Progymnospermopsida, Stenokoleales, Spermatophyta.
   - Not B2: Rhyniophytoids, Eophyta, Paratracheophyta, Horneophytopsida, Protracheophyta.
   - Unresolved: Basal eutracheophytes, Incertae sedis. Excluded from S3 main; included in the
     sensitivity `S3_plus_unresolved`.
3. Rows where rule 1 and the Capel group disagree are listed in the mapping output (`conflict`), with
   rule 1 applied.

## 4. Ages

- Stage names map to `data/timescale.csv` (ICS v2024/12). A stage's interval runs from its base to the
  next younger stage's base.
- Qualifiers (`Early`, `Middle`, `Mid-`, `Late`, `Mid- to late`, `early`, `mid`, `late`) are dropped:
  the row takes the whole stage, the stage-level convention F3 uses for curated units.
- A range `X-Y` runs from the base of X to the top of Y, after qualifiers are dropped from each part.
- Series: `Ludlow` = Gorstian–Ludfordian; `Early Devonian` = Lochkovian–Emsian; `Middle Devonian` =
  Eifelian–Givetian; `Late Devonian` = Frasnian–Famennian.
- Spelling variants: `Gordstian` = Gorstian; `Fammenian` = Famennian.
- Strings wholly younger than 393.47 Ma (including `Post-Tournaisian*` and every Middle Devonian or younger
  stage) are mapped where the timescale allows and fall outside the window; a blank cell is `unmapped`.
- **Yea.** Rows whose locality names Yea, Victoria, take F3's main envelope for the disputed Yea anchor,
  393.47–426.7 Ma, the same treatment S0–S2b give the Yea units. Capel's own ages for these rows are kept
  as the sub-variant `S3_yea_literal`. No other row is re-aged.
- Every distinct age string must map, or be listed as outside the window or unmapped; the parser fails
  otherwise.

## 5. Localities and regions

- **Locality key.** Unicode NFKD with accents removed, case-folded, `formation` written as `fm`, every
  character other than letters, digits, commas and spaces removed, whitespace collapsed. The key is the
  whole normalised string. Main S3 uses exact keys.
- **Fuzzy sensitivity** (`S3_fuzzy`): within one region, keys whose `difflib` ratio is 0.92 or more are
  merged by single linkage over the sorted key list. The merged pairs are listed for review.
- **Locality–age unit:** (key, max_ma, min_ma). **Region–stage unit:** (region, stage of the midpoint of the
  age range, capped at 469.4 Ma), the rule `select_records` uses for S0–S2b.
- **Region** follows F3's palaeoregion scheme (`studies/f3/tools/occurrences.py`, `UNIT_BY_CC`, `UK`,
  `CHINA`), applied to the last comma-separated field of the locality string, with these explicit rules:
  - `USA`, `New York`, `Canada`, `North Greenland` → Laurentia. `Norway` or `Western Norway` →
    Baltica, except localities naming Spitsbergen or Svalbard → Laurentia (F3's `SJ` and `M-svalbard`).
  - `UK`: the token Scotland → Laurentia; England or Wales → Avalonia; neither → multiple (F3's `UK`
    default). `Scotland` → Laurentia; `England` → Avalonia.
  - `Ireland`, `Belgium` → Avalonia. `France`, `Spain`, `Czech Republic` → peri-Gondwana-Europe.
    `Germany`, `Poland`, `Russia`, `Russian Federation` → multiple. `Ukraine` → Baltica.
  - `Kazakhstan`, `Central Kazakhstan`, `Southern Kazakhstan` → Kazakhstania.
  - `China`: a locality naming Xinjiang and any of Junggar, Hoboksar, Xiemisitai or Wutubulake →
    Kazakhstania (F3's curated West Junggar units); other Xinjiang → Tarim; North China provinces per
    F3's `CHINA`; South China provinces per F3's list → South-China; otherwise multiple.
  - `Vietnam` → South-China (F3's curated `M-van-canh`, not the PBDB `VN` default).
  - `Australia`, `Victoria`, `Antarctica`, `West Antarctica` → Gondwana-Australia-Antarctica.
  - `Morocco`, `Niger`, `Chad`, `Northeast Chad`, `Egypt` → Gondwana-North-Africa-Arabia.
  - `Argentina`, `Bolivia`, `Brasil`, `Brazil`, `Colombia`, `Chile`, `Venezuela` → Gondwana-South-America.
  - `South Africa`, `India`, `Falkland Islands` → Gondwana-other.
  - Blank → unknown.
  Every distinct final field must map; the parser fails otherwise.

## 6. Crosswalk with S0 (amendment 3)

The crosswalk lists every S0 B2 unit whose age range reaches above 419.62 Ma (13 Silurian-only units and
3 Yea straddlers) beside every S3 B2 row whose range reaches above 419.62 Ma, matched by locality,
formation and taxon. It necessarily shows S3's Silurian units. It reports no Devonian tally and no share.
The bias of S3 relative to S0 is described from the matches and the unmatched rows on each side.

## 7. Window and counting

S3 units enter the window when `max_ma > 393.47`; guaranteed units have `min_ma >= 393.47` and
`max_ma <= A` (426.7 Ma main; 425.0 Ma in the Bathurst-hinge run of Task 6). Region–stage n and k are
counted by the rules S0 uses (`switch_reading.py`): n from region–stage units; k as distinct (region,
min_ma, max_ma) among guaranteed late locality–age units.

## Amendments

All dated 21 November 2026, made after the parse was first run and before any S3 count or share. Each
came from reading the mapping tables or the list of rows reaching above 419.62 Ma, not from a tally. The
frozen text above is unchanged; these override it where they differ.

- **S3-A1, species counts (§1), superseded by S3-A10.** The sheet has 810 one-row species and 194 two-row species, and no
  three-row species. The counts in §1 (809, 195, 1) were relayed and are wrong by one row; the parser
  asserts 810/194.
- **S3-A2, UK regions (§5).** UK localities naming Shropshire, Hereford, Worcestershire, Gloucestershire,
  Devon, Cornwall or Somerset map to Avalonia, like England and Wales. Found because Brown Clee Hill,
  Targrove and Perton Lane fell to "multiple".
- **S3-A3, Yea (§4), superseded by S3-A11.** The re-ageing applies only to the disputed Yea anchor units. Norton Gully Sandstone
  (*Taungurungia garrattii*, Late Pragian–Emsian) keeps Capel's age.
- **S3-A4, locality alias (§5).** "Altholville" and "Atholville" (Campbellton Fm) share one key.
- **S3-A5, fuzzy sensitivity (§5), removed (Codex review, f22b451).** Five of the six 0.92 merges join distinct sections
  or formations, and S3-A4 handles the sixth. Proposal: drop `S3_fuzzy`.
- **S3-A6, unresolved sensitivity (§3), removed (Codex review, f22b451).** Found in the list of rows reaching above
  419.62 Ma. Its added rows are mostly *Cooksonia*, including the Sheinwoodian *C. barrandei*, which would
  move A to 432.9 Ma and make the set a branched-plant inventory. Proposal: drop `S3_plus_unresolved` from
  the crown runs.
- **S3-A7, Capel-groups-only variant (§3).** Two Silurian crown rows are crown only through F3's genus rule:
  *Aberlemnia* cf. *caledonica* (Lipeon Fm, Bolivia) and *Aberlemnia* ? sp. (Van Canh Fm), both in Capel's
  Basal eutracheophytes. `S3_capel_groups` applies Capel's groups alone, with no F3 override; it is
  reported beside S3 main.
- **S3-A8, oldest age and Task 6 on S3 (§7), superseded by S3-A13.** S3 main's oldest non-Yea crown row is Lipeon Fm (Ludlow,
  426.7–422.7 Ma), so excluding Yea leaves A at 426.7 Ma. Task 6 on S3 is run twice: Yea excluded with A
  from the data (426.7 Ma), and Yea and Lipeon both excluded so that A = 425.0 Ma (Bathurst Island Fm), the
  hinge the specification intends.
- **S3-A9, gates (§1), superseded by S3-A17.** Without S3 locality–age or shape tests, the specification's gates are restated for
  S3. Every other condition stands as written.
  - Gate 1 (rock, rock × spore share): holds if p < 0.05 on S1 and S2b at both grains and on S3
    region–stage, at A = 426.7 and 425.0 Ma; withdrawn if p ≥ 0.05 on S2b at both grains and on S3
    region–stage.
  - Gate 2 (spore share alone): holds if p < 0.05 on S1 and S2b at both grains and on S3 region–stage;
    withdrawn if p ≥ 0.05 on S2b locality–age and on S3 region–stage.
  - Gate 3 (C60): the S3 conditions use region–stage only.
  - Gate 4 (C27, C49): S3 carries no shape test, so withdrawal, which needs S2b and S3 to agree, cannot
    fire. A failure on S2b alone counts as "narrower, inventory-dependent".
  - Any other outcome counts as "narrower, inventory-dependent" (Fable's amendment 5). Each gate is
    reported for S3 main and `S3_capel_groups`.

### Second set of amendments, after Codex's Stage 1 review

Dated 22 November 2026, made in response to Codex's review
([2026-11-21-inventory-symmetry-stage1-review.md](2026-11-21-inventory-symmetry-stage1-review.md), f22b451)
and before any Devonian tally, share or test on S1, S2a, S2b or S3. The only S3 counts are the
Silurian-only units and cells of the crosswalk and the oldest age of each reading. The only test outputs
are on S0, the frozen published inventory, to show that the code reproduces it. They override the text and the amendments above
where they differ. The row-level check of every disputed case is
[capel_s3_disputed_rows.csv](../../models/loop3/out/capel_s3_disputed_rows.csv).

- **S3-A10, worksheet boundaries (supersedes A1).** Observations occupy rows 4–1200. Row 1201 is a merged
  footnote explaining "Post-Tournaisian", which the first parse read as a species and assigned to
  Filicopsida. The sheet therefore has 1,197 biological rows in 1,003 species entries: 809 entries with one
  row, 194 with two, none with three. Every row has a time and a locality. The 809 in the relayed count was
  right; its 195 and 1 were not. The 18 vertically merged reference cells (for example E9:E10) now give their
  reference to every row they span; E845 is blank in the source and stays blank. The parser asserts 1,197
  rows and 809/194.
- **S3-A11, Yea by named horizon (supersedes A3 and the Yea rule of §4).** Every Capel row naming Yea, Ghin
  Ghin or Limestone Road (except Norton Gully) maps to an F3 horizon in
  [observations.csv](../../data/occurrences/observations.csv). It takes that horizon's main-reading envelope
  from [interpretations.csv](../../data/occurrences/interpretations.csv), and the horizon becomes its
  locality key, so rows from one horizon form one unit. Capel's literal ages stay in `literal_max_ma` and
  `literal_min_ma`, and the `yea_literal` variant uses them.

  | Row | Taxon (crown?) | Capel age | Horizon | Envelope | Basis |
  |---|---|---|---|---|---|
  | 124 | *Baragwanathia longifolia* (B2) | Ludfordian | M-yea-unspecified | Gorstian–Emsian | Garratt & Rickards 1984 is F3's source for the unspecified Yea record (L3S-015) |
  | 734 | *Parazosterophyllum timsiae* (B2) | Přídolí–Pragian | M-ghin-ghin (Loc. 1) | Gorstian–Emsian | M-ghin-ghin lists the species and McSweeney et al. 2020 |
  | 1199 | cf. *Zosterophyllum* sp. B (B2) | Pragian–Emsian | M-ghin-ghin (Loc. 1) | Gorstian–Emsian | Bed not stated; F3 attaches McSweeney et al. 2022 to Loc. 1 |
  | 904 | *Salopella caespitosa* (not B2) | Ludlow | Ghin Ghin Road, bed unidentified | Gorstian–Emsian | Loc. 1 or B2 |
  | 906, 1146 | *Salopella laidae*, *Yarravia oblonga* (not B2) | Pragian; Ludlow | M-limestone-road (Loc. 4) | Gorstian–Emsian | Loc. 4 named |

  Where the bed is uncertain (row 1199), the alternative is B2, 67 m higher (Přídolí–Emsian, L3S-014). It
  would add one locality–age unit to Yea-inclusive runs. It leaves region–stage cells unchanged, because
  both envelopes have Emsian midpoints (410.1 and 408.1 Ma) in Gondwana-Australia-Antarctica. Task 6 excludes rows 124, 734 and
  1199 before aggregation. Row 124 stays its own unit. F3 counts no unspecified Yea record (L3S-015), and the
  difference affects only Yea-inclusive locality counts.
  *(The treatment of rows 124 and 1199, and the claim that only locality counts change, are superseded by
  S3-A18.)*
- **S3-A12, material readings and F3 classifications (extends §3).**
  - **The Bolivian *Aberlemnia*.** In S3 main, row 6 (*Aberlemnia* cf. *caledonica*, Lipeon Fm, Jarcas,
    Negra Muerta; Capel: basal eutracheophytes) follows F3's reading of its Negra Muerta cf. *caledonica*
    (`tail:M-bolivia-caledonica`): B1 in the main reading, B2 in the inclusive one. The formation,
    reference and specimen identity differ or are open, so this follows F3's material reading rather than
    asserting the same specimen. `S3_permissive` applies the genus rule alone and counts row 6 as B2.
  - **Labels.** `f3_crown` now separates unanimous `uncertain` from `mixed`. No window row is mixed.
  - **Departures from F3.** Twelve window rows enter S3 main through Capel's group where F3 reads the genus as
    uncertain. Only one is Silurian: *Jugumella burubaensis* (row 530, Balkhash, Přídolí). The other eleven
    are Devonian: *Enigmophyton* (371); *Huia* (512–514); *Jugumella* (531–533); *Krithodeophyton* (561, 562);
    *Loganophyton* (629); and *Nothia* (708). A new variant, `S3_f3_strict`, drops these rows.
  - **How each reading admits Balkhash** (Tokrau Horizon, Kokbaital Mountains).

    | Row | Taxon | F3 | Capel | Main | F3-strict | Permissive | Capel groups |
    |---|---|---|---|---|---|---|---|
    | 128 | *Baragwanathia*? sp. | yes, genus | Lycopsida | B2 | B2 | B2 | B2 |
    | 530 | *Jugumella burubaensis* | uncertain (N109) | Zosterophyllopsida | B2 | dropped | B2 | B2 |

    The locality enters every reading through row 128. F3 keeps the queried record in its regional reading
    (`I-kazakh-lycophytes-tentative`). S0 counts Kazakhstan through PBDB outcrops, not the regional
    assemblage (L3S-033). Rows 128 and 530 both map to 422.7–419.62 Ma at the same locality key, so they *(Provenance corrected in S3-A20.)*
    form one unit. Row 530 adds no locality–age unit and no cell in any reading.
- **S3-A13, oldest age per variant (supersedes A8).** A is derived from the data after each run's exclusions.

  | Variant | Yea included | Yea excluded |
  |---|---|---|
  | main | 426.7 Ma | 425.0 Ma |
  | f3_strict | 426.7 Ma | 425.0 Ma |
  | capel_groups | 426.7 Ma | 425.0 Ma |
  | permissive | 426.7 Ma | 426.7 Ma |
  | yea_literal | 425.0 Ma | 425.0 Ma |

  - The Yea-excluded age of 425.0 Ma comes from Bathurst Island Fm, Ludfordian (rows 149, 338, 662, 1184,
    1192, 1193). In permissive, row 6 holds 426.7 Ma.
  - With Capel's literal Yea ages, row 124 is Ludfordian (425.0–422.7 Ma) and row 734 is Přídolí–Pragian.
    So `yea_literal` has A = 425.0 Ma even with Yea included.
  - Task 6 therefore runs on main, f3_strict and capel_groups at 425.0 Ma with no forcing.
  - The permissive run at 425.0 Ma is labelled "forced: rows 124, 734, 1199 and 6 removed". Its unforced
    426.7 Ma run is reported beside it.
- **S3-A14, midpoints outside the F3 domain.** Region–stage midpoints below 393.47 Ma take their stage from the
  full ICS table ([timescale.csv](../../../../data/timescale.csv)); inside the domain `stage_bounds` is
  unchanged. Row 477 (*Haplostigma baldisii*, Argentina, 410.62–372.15 Ma, midpoint Eifelian) keeps both
  endpoints. It straddles the young cutoff, so it is possible-only and outside guaranteed n. Every parse runs
  all five retained variants (main, f3_strict, permissive, capel_groups, yea_literal) at both grains.
- **S3-A15, counting rules, for all inventories (S0 to S3).**
  - **n.** n is conditioned on the guaranteed whole-window inventory: units with `min_ma >= 393.47` and
    `max_ma <= A`.
  - **locality_age.** n is fixed. k runs from units wholly in the interval (k_min) to units reaching into
    it (k_max).
  - **region_stage** (cells). A cell is region × stage of a guaranteed locality–age unit, and the same cells
    form the numerator and the denominator.
    - A unit wholly inside or wholly outside the interval takes its midpoint stage.
    - A unit that reaches into the interval without lying wholly inside it is placed, in turn, in every
      stage its range allows. Moving such a unit can create or remove cells, so n and k change together.
    - Every admissible (n, k) pair is kept. The reported n is the midpoint placement.
    - Multi-stage units wholly outside the interval keep their midpoint cell. This is the inherited
      midpoint convention, and it fixes n apart from the straddlers.
  - **region_stage_named.** As region_stage, omitting the pooled codes `multiple` and `unknown` from both
    numerator and denominator and from regional breadth. This is the decisive regional rule.
    region_stage (pooled) is reported beside it. Any decision that changes with pooling is reported.
  - **region_stage_legacy.** `switch_reading.py`'s pair (n from region–stage units; k as distinct (region,
    min, max) among late locality–age units). It is kept only to reproduce the committed S0 values.
  - **Check on S0.** The harness reproduces every committed value, including the 48-unit C48 values. Under
    the new rules, S0 gives:

    | Interval | Rule | n | k | Lower 95% rate ratio | Committed ratio |
    |---|---|---|---|---|---|
    | Gorstian–Přídolí | locality–age | 48 | 13–16 | 0.790 | 0.790 |
    | Gorstian–Přídolí | cells, pooled | 19–22 | 6–9 | 0.622 | 0.692 (legacy) |
    | Gorstian–Přídolí | cells, named | 17–20 | 6–9 | 0.692 | 0.692 (legacy) |
    | Ludfordian–Přídolí | locality–age | 48 | 13–16 | 1.039 | 1.039 |
    | Ludfordian–Přídolí | cells, pooled | 19–22 | 6–8 | 0.778 | 0.911 (legacy) |
    | Ludfordian–Přídolí | cells, named | 17–20 | 6–8 | 0.862 | 0.911 (legacy) |

    - No deficit and no two-sided departure from level is established on S0.
    - Pooling against named changes no test outcome on S0, and neither does legacy against named.
- **S3-A16, tail rules.**
  - **Directions.** Every test is evaluated at each admissible (n, k), and its p is the largest over them.
    An excess (upper tail; C59 placement and the C60 level upper tail) or a deficit (lower tail) is
    established only if every admissible pair rejects. At locality–age this is the upper tail at k_min and
    the lower tail at k_max.
  - **Two-sided.** The two-sided p is twice the smaller one-sided tail. A two-sided rejection needs
    rejection at every admissible pair. A set is "compatible with level" when some pair is not rejected.
  - **Lower share.** The Clopper–Pearson lower share is the smallest over the admissible pairs, which is at
    k_min at locality–age.
  - **Change factor** *(superseded by S3-A19)*. The largest change factor is reported at the reported n and k_min, as in
    `switch_reading.py`. For an interval short of A the share is not monotone in the factor, so no range
    over placements is defined.
  - **Reported for every set.** Per proxy, the expected count and the smallest count an upper-tail test at
    0.05 rejects. Under level, the largest count a lower-tail test at 0.05 rejects. Both are at the
    reported n. And whether an excess, a deficit or a two-sided departure is established.
  - **The specification's gates read accordingly.** "P(X ≤ k_obs | level)" is the largest lower tail over
    the admissible pairs. "P(X ≥ k_min)" is the largest upper tail. "Two-sided p_level ≥ 0.05" means
    compatible with level as defined here.
  - **Preliminary numbers.** Any earlier deficit figure is reported only with its age assignment until rerun
    under this rule.
- **S3-A17, gates on S3 (supersedes A9).**
  - **What S3 can carry.** S3 lists species endpoints, so S3 enters gates 1–3 only at region_stage_named,
    as a comparison of listed endpoint cells. Its binomial tails are described as such. They have no
    demonstrated calibration as a fossil-finding rate. S3 locality–age counts and endpoint arithmetic (Task
    4) are descriptive.
  - **Which reading decides.** S3 main is the deciding reading. f3_strict, permissive and capel_groups are
    reported beside it. A gate outcome that changes under any of them counts as "narrower,
    inventory-dependent".
  - **Gate 1** (rock, rock × spore share) holds if p < 0.05 on S1 and S2b at locality_age and
    region_stage_named, and on S3 region_stage_named, at A = 426.7 and 425.0 Ma. It is withdrawn if p ≥ 0.05
    on S2b at both grains and on S3 region_stage_named.
  - **Gate 2** (spore share alone) holds on the same conditions. It is withdrawn if p ≥ 0.05 on S2b
    locality_age and on S3 region_stage_named.
  - **Gate 3** (C60) uses S3 region_stage_named, with the tail rules of S3-A16.
  - **Gate 4** (C27, C49). S3 evidence is unavailable: S3 carries no shape test. S0, S1, S2a and S2b are
    judged on their own stated inventories. Withdrawal needs S2b and S3 to agree, so it cannot fire. A
    failure on S2b alone counts as "narrower, inventory-dependent".
  - **Any other outcome** counts as "narrower, inventory-dependent" (Fable's amendment 5).
  - **Labelling.** Each gate result names the S3 reading and counting rule it used.

### Third set of amendments, after Codex's reconciliation review

Dated 23 November 2026, in response to Codex's review
([2026-11-22-inventory-symmetry-reconciliation-review.md](2026-11-22-inventory-symmetry-reconciliation-review.md),
f6e2d10, Board 3651). Still before any Devonian tally, share or test on S1, S2a, S2b or S3; the only test
output is S0. They override the amendments above where they differ.

- **S3-A18, Yea identity treatments (supersedes the row 124 and 1199 treatment in S3-A11).** Capel's
  Yea crown rows are 124 (unspecified Yea), 734 (Ghin Ghin Loc. 1) and 1199 (Ghin Ghin Road, bed not
  stated). They are the only Australian crown rows whose main envelopes reach the Silurian. Under S3-A15
  each straddles the interval boundary, so the number of distinct Yea horizons sets how many Australian
  cells the Silurian can hold: one horizon occupies one stage, two can occupy the Gorstian and the Přídolí
  together. Identity therefore changes region–stage counts as well as locality counts. Every S3 reading
  other than `yea_literal` carries four treatments (`units(..., yea=)` in `capel_s3.py`):

  | Treatment | Row 124 | Row 1199 | Yea crown units | Stage sets the units can occupy |
  |---|---|---|---:|---:|
  | `ref` (deciding) | joins Loc. 1: not independent of the named horizons (L3S-015) | Loc. 1 (assumed) | 1 | 6 |
  | `y124` | its own unit, Gorstian–Emsian | Loc. 1 (assumed) | 2 | 21 |
  | `b2` | joins Loc. 1 | B2, Přídolí–Emsian (L3S-014) | 2 | 18 |
  | `y124_b2` | its own unit | B2 | 3 | 38 |

  - **Bed order.** B2 lies 67 m above Loc. 1, so B2 never takes an older stage than Loc. 1. The harness
    places the two units jointly (`BED_ORDER` in `inventory_symmetry_tests.py`). The same constraint
    applies to S0's `tail:M-ghin-ghin` and `tail:M-ghin-ghin-b2`. It does not bind there: S0's nine named
    pairs per interval are identical with and without it.
  - Row 124 stays in the source table under every treatment; `ref` places it in the Loc. 1 unit as a
    possible duplicate.
  - `yea_literal` keeps Capel's own localities and ages and runs at its natural oldest age, 425.0 Ma.
  - **Gates.** `ref` decides within each reading. A gate outcome that changes under `y124`, `b2`,
    `y124_b2` or `yea_literal` counts as "narrower, inventory-dependent" (S3-A17), and the gate table
    names the treatment or comparison that changed it.
  - The oldest-age table of S3-A13 is unchanged: every treatment keeps the Yea envelopes' 426.7 Ma, and
    removing rows 124, 734 and 1199 leaves Bathurst's 425.0 Ma except in permissive.
  - Output: [capel_s3_yea_units.csv](../../models/loop3/out/capel_s3_yea_units.csv) lists the Yea units and
    their admissible stage sets per reading and treatment. It holds unit structure only.
- **S3-A19, the exponential upper factor (supersedes the change-factor bullet of S3-A16).** For a pair
  (n, k), an exponential history passes the upper-tail benchmark exactly when its interval share reaches
  that pair's one-sided 95% Clopper–Pearson lower share. A history compatible with at least one admissible
  pair must therefore reach the smallest lower share over the pairs. The reported factor (rate at
  393.47 Ma over rate at A) is the largest factor whose share reaches it. For an interval short of A the
  share rises then falls with the factor, and the upper crossing is taken. The harness reports
  "unbounded" when k can be zero or no crossing lies in the search range, and "none" when no factor
  reaches the share. The fixed-pair factor at the reported n and k_min stays in
  `fixed_pair_factor_legacy`, where it reproduces `switch_reading.csv`.

  | S0 interval | Rule | Lower rate ratio | Fixed-pair factor (legacy) | Upper factor (S3-A19) |
  |---|---|---:|---:|---:|
  | Gorstian–Přídolí | locality–age | 0.790 | 1.764065 | 1.764065 |
  | Gorstian–Přídolí | cells, named | 0.692 | 1.809959 | 2.364903 |
  | Gorstian–Přídolí | legacy pair | 0.692 | 2.364903 | 2.364903 |
  | Ludfordian–Přídolí | locality–age | 1.039 | 0.899615 | 0.899615 |
  | Ludfordian–Přídolí | cells, named | 0.862 | 0.928215 | 1.472918 |
  | Ludfordian–Přídolí | legacy pair | 0.911 | 1.280264 | 1.280264 |

  The named-cell upper factors reproduce Codex's 2.364903 at (19, 6) and 1.472918 at (20, 6), and the
  harness asserts both. One assignment realising (20, 6) for Ludfordian–Přídolí (Codex) places Ghin Ghin Loc. 1 in
  the Gorstian, B2 in the Lochkovian and Limestone Road in the Pragian. Under the named-cell rule S0 is
  compatible with a 47% rise in the finding rate over the later window; the fixed-pair 0.928 had read as
  a decline.
- **S3-A20, corrections to the record.**
  - **Kazakhstania in S0 (corrects S3-A12).** S0's Silurian crown cell for Kazakhstania comes from three West
    Junggar units in China. The Kazakh PBDB outcrops 53609, 53610 and 53656 qualify for B0 and B1 only;
    their B2 flags are false ([horizons_reviewed.csv](../../data/macro/horizons_reviewed.csv)). The
    Balkhash table of S3-A12 and the four shared Silurian region–stage cells stand.
  - **Scope of the placement pairs (qualifies S3-A15).** The nine named pairs per S0 interval hold units
    wholly inside or wholly outside the interval at their midpoint stage. Letting every unit's range vary
    gives 17 pairs per interval (Codex). Results are stated as conditional on the midpoint convention.

### Stage 2 conventions, frozen before any S1–S3 share

Dated 23 November 2026, after Codex's Stage 1 acceptance
([2026-11-23-inventory-symmetry-stage1-acceptance.md](2026-11-23-inventory-symmetry-stage1-acceptance.md),
`088f592`) and before any tally, share or test on S1, S2a, S2b or S3. They fix the choices the gates
leave open; the gate code in `inventory_symmetry_stage2.py` applies them mechanically.

- **S3-A21, deciding sets and variants.**
  - The gates read the base sets S1 and S2b, and S3 main with Yea treatment `ref`. S2a, the variants
    `_with_28303`, `_merged` and `_coord`, the other S3 readings and Yea treatments, and `yea_literal` are
    reported beside them. A gate outcome that changes under any of them counts as "narrower,
    inventory-dependent", and the gate table names the set that changed it.
  - S0 is reported throughout and decides nothing in gates 1–3. Gate 4 reads S0, S1 and S2b as the
    specification states.
- **S3-A22, the Bathurst-anchored runs (Task 6).**
  - S0–S2b drop `tail:M-ghin-ghin`, `tail:M-ghin-ghin-b2` and `tail:M-limestone-road` before aggregation;
    S3 drops rows 124, 734 and 1199. A is re-derived from the remaining units and asserted to be 425.0 Ma,
    except S3 permissive, whose 426.7 Ma run is reported unforced and whose 425.0 Ma run also drops row 6
    and is labelled forced.
  - At A = 425.0 Ma the Gorstian–Přídolí and Ludfordian–Přídolí intervals coincide (419.62–425.0 Ma).
    Each test is reported once, as Ludfordian–Přídolí.
  - Gates 1 and 2 read both the natural-A run and the 425.0 Ma run. Gate 3 reads the natural-A run; a
    change at 425.0 Ma counts as narrower.
- **S3-A23, gate reading of the test outputs.**
  - Gates 1 and 2: "p < 0.05" means an excess established under S3-A16, at locality_age and
    region_stage_named for S1 and S2b and at region_stage_named for S3, in both intervals. A gate holds
    only if every required cell holds.
  - Gate 3: "compatible with level" is S3-A16's definition (some admissible pair not rejected two-sided).
    The lower ratio is the smallest over admissible pairs. "Regions" counts the named regions of units
    wholly inside the interval at their midpoint placement. Withdrawal reads S2b at both grains and S3 at
    region_stage_named only, since S3 locality counts are descriptive (S3-A17).
  - Gate 4: an inclusion state is one of the four inclusion masks of the two units straddling 393.47 Ma
    (every set has exactly two). A history "attains p ≥ 0.05" in a state when the finite-sample `kstwo`
    certificate finds an admissible allocation with D at or below the 5% critical value. Gate 4 reads S0,
    S1 and S2b; S3 has no shape test, so withdrawal cannot fire and a failure on S2b alone counts as
    narrower.
- **S3-A24, Task 4.**
  - Task 4.1 reports T, m*(n) = n(0.05^(−1/n) − 1), K(n) = (A − c)(0.05^(−1/n) − 1) and the zero-delay folds
    at 444 and 452 Ma from guaranteed counts at locality_age and at the pooled midpoint region_stage rule
    that C48 and C55 use. It also reports the older bound under all six histories (C27). B1 and B0 (C61,
    C62) are computed on S0 and S1 with `groups.py`'s functions.
  - Task 4.2 counts guaranteed Silurian-only units (min ≥ 419.62 Ma) with c = 419.62 Ma under all six
    histories, at natural A and at 425.0 Ma. Leave-Bathurst-out uses the Bathurst Island Silurian units
    (min ≥ 419.62 Ma) in two forms: collapsed to one unit with A held, and removed with A re-derived.
  - Every new piece first reproduces its committed S0 values (`interval_feasibility_summary.csv`,
    `groups.csv`, `groups_inside.csv`, `groups_shape.csv`, the Přídolí-cutoff rows of
    `reviewed_bounds.csv`) and asserts them before any other set is read.

## S3-A25: repairs after Codex's Stage 2 review (23 November 2026)

Post hoc: these follow Codex's review of the Stage 2 outputs and were not frozen before any number existed.
They change no verdict of gates 1–4c. [Stage 2 review](2026-11-23-inventory-symmetry-stage2-review.md)

- **S3-A25, jointly possible allocations, region–stage Bathurst removal, the literal-Yea selector and the
  gate 5 row.**
  - Every Task 4 row keeps the conservative range envelope (the guaranteed count paired with the oldest
    possible age), the published convention of `reviewed_bounds.csv`. Beside it, the `admissible_*` columns
    give the oldest bound over allocations that can occur together. Each straddling unit lies either outside
    the window or inside it at its oldest age. More units tighten a bound and an older A loosens it, so the
    candidates are the guaranteed units alone and the guaranteed units plus one straddling unit older than
    all of them. A beyond-domain bound ranks oldest. Constant-formula rows also give the smallest fold at
    444 and 452 Ma over the candidates. A quoted fold or limit names the calculation it uses.
  - Region–stage rows use the pooled midpoint cells at a stipulated anchor. The jointly possible columns
    move only units that straddle the cutoff; they do not re-form cells. At c = 393.47 Ma the Australian
    midpoint cell is guaranteed, so its 426.7 Ma oldest age and the 19-cell S0 count come from different
    Ghin Ghin placements, as in the committed C48 and C55 rows. Locality–age counts do not depend on
    placement.
  - Task 4.1 reports the six-history bounds at the pooled midpoint region–stage rule as well as at
    locality_age.
  - Task 4.2's leave-Bathurst-out at region_stage removes the Bathurst Silurian units (S3-A24) before the
    cells are formed. Collapsing Bathurst to one unit is not repeated at region_stage, where its units
    already share one cell.
  - `yea_literal` gains a 425.0 Ma run without rows 124, 734 and 1199, labelled `bathurst_425`. Its units
    are asserted equal to S3 main's run without those rows. The literal natural run keeps Yea, also at
    425.0 Ma, and stays the natural-A run. Gates 1, 2 and 3b read the `bathurst_425` run for the 425.0 Ma
    comparison.
  - The specification gives gate 5 only a "holds" branch. Its row records the full-window locality_age folds
    on S0–S2b, the smallest jointly possible fold at 444 Ma over every S0–S2 Task 4 row, and the rows whose
    fold at 444 Ma falls to 1 or below under either calculation. Upward sensitivity: the S1 and S2b
    full-window folds are at least S0's. Downward sensitivity: the smallest jointly possible Devonian-free
    fold at 444 Ma is below the smallest Devonian-free locality_age envelope fold of S0, S1 and S2b with
    every unit kept (2.98, where the specification's 3.0–9.4 baseline starts).
