# S3 mapping rules: Capel, Monnet and Cascales-Miñana (2025) Table S1 (Task 1B)

Claude (Opus 5.5), 21 November 2026. Written and committed before any S3 row was parsed into units and
before any Silurian/Devonian share was computed on S0–S3. Part of the inventory-symmetry audit
(`2026-11-21-inventory-symmetry-spec.md`). **Status: awaiting Codex sign-off.** No share is computed on S3
until the second agent signs off on these rules and the mapping tables they produce. Any later change is
recorded below as a dated amendment with its reason, and the frozen version stays in git history.

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

None.
