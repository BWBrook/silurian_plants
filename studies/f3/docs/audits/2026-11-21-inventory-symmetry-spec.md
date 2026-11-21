# Inventory-symmetry audit: specification and amendments

Filed by Claude (Opus 5.5), 21 November 2026. The specification below was written by Google's Gemini
(Gemini 4 Carbon at high reasoning effort, in the Antigravity app) in an independent review of F3 that Barry requested, and relayed
with amendments by Fable (Claude Fable 5.2, advisory reader). Its links are rewritten as repository-relative
paths; its text is otherwise as received. Every number in it is preliminary until reproduced, including
numbers inside the gates. Execution record: `2026-11-21-inventory-symmetry.md`; frozen S3 rules:
`2026-11-21-inventory-symmetry-s3-rules.md`.

## Fable's amendments (relayed with Barry, 21 November 2026)

Fable verified the two central facts at `9ac5946` (the 20 Myr duration filter at `build_reviewed.py`
line 196 drops every collection dated only to the Early Devonian; curated literature units skip that
filter and curation went mostly to the Silurian) and noted that the fault sits under C59 and C60. Fable's
amendments, summarised:

1. Only Macrostrat column 304 is all subsurface; columns 37, 38 and 305 list surface Early Devonian units.
   The case against `pbdb:28216` and `28302` rests on the formation names (Capel Table S1: 24 Price and
   Pocono rows, 23 Late Tournaisian, one Late Famennian). `pbdb:28303` (Kinzua Dam) has no formation and is
   the weakest. Record the evidence behind each exclusion.
2. An S3 locality is a first or last record of some species; say whether locality–age counts and the
   Task 5 shape tests mean anything on S3, or only region–stage.
3. S3's bias is not shown (no Argentine Silurian row; one Bathurst Island string against four S0 units;
   Balkhash Silurian rows absent from S0). Produce the S0–S3 Silurian crosswalk as a by-product of Task 1B.
4. Gate 3 is already decided by Gemini's preliminary S2b region–stage count (3 of 18): neither "holds" nor
   "withdrawn" can fire, so C60 as worded is superseded; treat gate 3 as deciding what replaces it. On S2b
   locality–age, 5 of 59 gives P(X ≤ 5) = 0.008 under a level rate.
5. Outcomes outside the stated cases count as "narrower, inventory-dependent"; say which sets disagree.
   The thresholds were set after preliminary sums on S1 and S2: decision rules, not a blind
   pre-registration.
6. For each test on S2a and S2b, report the expected count and the smallest count that would reject.
7. Task 4.2 should run all six histories; `reviewed_bounds.csv` row 96 already gives 429.80 Ma under
   decline10 with the Pridoli cutoff.

Order: Tasks 1A and 1B first, with the second agent's sign-off on the S3 mapping before any share is
computed; then Tasks 3–6 for the crown group; Task 2 optional. Rules: ledger first, no edits to the four
texts or the figures, no outside search.

---

# Specification: Body-Fossil Inventory Symmetry Audit and Reruns (`C27`, `C48`, `C49`, `C58`–`C62`)

**Pinned repository commit:** `9ac5946` (`main`)
**Execution roles:** Claude Opus 5.5 and OpenAI Codex (agree file/step ownership on the Board per [AGENTS.md](../../../../AGENTS.md); independent cross-verification required at two gates below).

## 1. Operational Rules (Read First)

1. **Ledger and estimands first; no prose or figure edits in this tranche.** Do **not** edit [main.md](../../manuscript/text/main.md), [supplement.md](../../manuscript/text/supplement.md), [brief.md](../../manuscript/text/brief.md), [for-agents.md](../../manuscript/text/for-agents.md), or `studies/f3/manuscript/figures*.py`. Implement reproducible scripts, tests, CSV outputs, and SHA-256 receipts under `studies/f3/models/loop3/` and `studies/f3/docs/audits/`, apply the pre-declared decision gates in §5, and draft the resulting updates to [estimands.md](../../manuscript/estimands.md) and [claims.csv](../../manuscript/claims.csv) only after both agents verify the outputs.
2. **No external search or new fossil acquisition.** Use only tracked repository files and already-manifested CC0/CC BY deposits in [MANIFEST.tsv](../../../../data/external/deposits/MANIFEST.tsv) (`python3 data/external/scripts/deposits_fetch.py --only capel2025` if not already unpacked under `data/external/local/deposits/capel2025-global-plant-diversity/`).
3. **Preserve existing outputs.** Do not overwrite frozen/reviewed Loop 3 CSVs (`reviewed_bounds.csv`, `primary_unit_membership.csv`, etc.) during the diagnostic phase; write new outputs to clearly named tables (e.g. `studies/f3/models/loop3/out/inventory_symmetry_*.csv`).

## 2. The Problem in Plain Words (Checked vs Preliminary Facts at `9ac5946`)

Loop 3 built [primary_unit_membership.csv](../../models/loop3/out/primary_unit_membership.csv) (`B2`, `main`: `48` guaranteed locality–age units inside `[393.47, 426.7]` Ma) to set a **conservative older bound `T` on the start of the crown vascular-plant record (`C27`)**. Two design choices in [build_reviewed.py](../../models/loop3/build_reviewed.py) were conservative for `T` (because shrinking Devonian `n` and enriching oldest Silurian finds both push `T` older), **and became anti-conservative when `C59` and `C60` reused the same `48` units to test the Silurian-vs-Devonian share within `[393.47, 426.7]` Ma**:

- **Checked Fact A — Duration-filter asymmetry ([build_reviewed.py](../../models/loop3/build_reviewed.py), line 196):** PBDB collections with `max_ma - min_ma > 20` Myr receive `disposition = "wide_age_sensitivity"` and are excluded from `primary`. Because the Early Devonian (`393.47–419.62` Ma) spans `26.15` Myr (`> 20` Myr) whereas Ludlow–Pridoli (`419.62–426.7` Ma) spans `7.08` Myr (`<= 20` Myr), **every PBDB collection dated to `"Early Devonian"` is dropped from `n = 48`**, while curated `tail:` units face no `20` Myr filter (retaining the `33.23` Myr Yea ranges). Raw `variant="wide_age"` ([reviewed_bounds.csv](../../models/loop3/out/reviewed_bounds.csv) row 452) raises guaranteed `B2` units from `48` to `73` (`24` Devonian-only `393.47–419.62` Ma units + `1` straddler `pbdb:27917`), leaving Silurian-only units unchanged at `13` and dropping `C60`'s Gorstian–Pridoli lower rate bound from `0.790` (`13/48`) to `0.510` (`13/73`).
- **Checked Fact B — Source-curation asymmetry ([primary_unit_membership.csv](../../models/loop3/out/primary_unit_membership.csv), lines 151–200; [material_links.csv](../../data/macro/material_links.csv)):** Of the `48` guaranteed `B2` (`main`) units:
  - `13` are **Silurian-only** (`min_ma >= 419.62` Ma): `3` unreplaced `pbdb:` units (`pbdb:13873`, `52702`, `278439`) and `10` `tail:` units (`2` linked to PBDB collections in `material_links.csv`—`M-bathurst-us384` = `pbdb:53920`, `M-bathurst-us385` = `pbdb:53919`—and **`8` curated from primary literature absent from PBDB**: `M-rinconada`, `M-bathurst-us383`, `M-bathurst-us688`, `M-mangkelu-ii`, `M-qujingense`, `M-aberlemnia-junggaria`, `M-baragwanathia-karlstejn`, `M-van-canh`).
  - `3` are **Silurian–Devonian straddlers** (`393.47–426.7` or `393.47–422.7` Ma): all `3` Yea `tail:` units (`2` linked to PBDB: `M-ghin-ghin` = `pbdb:53660`, `M-limestone-road` = `pbdb:20754`; `1` non-PBDB: `M-ghin-ghin-b2`).
  - `32` are **Devonian-only** (`max_ma <= 419.62` Ma): `30` unreplaced `pbdb:` units and `2` `tail:` units (`1` linked to PBDB: `M-svalbard` = `pbdb:20839`; `1` non-PBDB: `M-wilson-creek`). Early Devonian primary literature outside PBDB received no matching curation pass.
- **Checked Fact C — Contamination inside raw `wide_age` ([horizons_reviewed.csv](../../data/macro/horizons_reviewed.csv), [pbdb_plant_collections.csv](../../../../data/eprp/record/pbdb_plant_collections.csv)):** Raw `variant="wide_age"` (`n = 73`) must **not** be used unscreened because:
  1. Three `"Early Devonian"` PBDB collections from the unpublished 2002 SUNY-Binghamton accession dump (`reference_no = 6895` in [pbdb_plant_references.csv](../../../../data/eprp/record/pbdb_plant_references.csv)) are Famennian–Tournaisian localities miscoded as `"Early Devonian"`: `pbdb:28216` (`Price` Fm, Cloyds Mountain VA), `pbdb:28302` (`Pocono` Fm, Baker Run PA, *Lepidodendropsis*), and `pbdb:28303` (`Kinzua Dam`, Allegheny Reservoir PA). Held `Capel 2025 Table S1` (rows 16–21, 193, 201, 221–224, 439–443, 566–567, 596–597, 604, 886, 966; citing Arnold 1932; Read 1955; Knaus 1995; Smith & Jacobi 2003; Gensel & Pigg 2010) dates the Price and Pocono floras to Late Famennian–Late Tournaisian, and held [macrostrat_units_window.csv](../../../../data/eprp/record/macrostrat_units_window.csv) (`col_id = 37, 38, 304, 305`) confirms zero surface Early Devonian outcrop at Kinzua Dam and Baker Run (`outcrop == "subsurface"`).
  2. `pbdb:27917` (`393.47–422.7` Ma, Wutubulake Fm Bed 5, `?Zosterophyllum sp.`) is an unlinked PBDB twin of `tail:M-xinjiang-zosterophyllum` (Cai et al. 1993 Bed 5, excluded from `primary` in [source_adjudications.csv](../../data/macro/source_adjudications.csv) `L3S-037`).
  3. Multi-epoch pre-Devonian `wide_age` rows (`pbdb:20683` `413.02–443.1` Ma; `pbdb:20890` `419.62–443.1` Ma) corrupt `B1`'s `A` (`432.9` $\rightarrow$ `443.1` Ma), and `22` Middle/Late Devonian straddlers (`min_ma < 393.47` Ma) exceed [interval_feasibility.py](../../models/loop3/interval_feasibility.py) (lines 76–77)'s `len(partial) <= 10` limit.
- **Preliminary Calculations (for Opus and Codex to verify from scratch):**
  - Restoring clean window-contained Early Devonian PBDB collections (`S1`, expected `B2` `n_guar = 69`, `13` Silurian-only; `region_stage = 6 of 21`) gives `C60` lower rate ratio `~0.541` (`0.622` `region_stage`) and `C48` `444–452` Ma folds `~11.7–17.2×`.
  - Restricting to PBDB-backed units (`S2a` `<= 20` Myr: `5 of 38`; `S2b` + clean Early Devonian: `5 of 59`, `region_stage = 3 of 18`) gives `C60` lower rate ratio `~0.160–0.250` and **`C59` `spore_share` placement `p ~ 0.174` (`S2a`) and `0.496` (`S2b`)** (no longer rejected!).
  - Held CC BY 4.0 deposit **Capel, Monnet & Cascales-Miñana (2025)** (`data/external/local/deposits/capel2025-global-plant-diversity/Table_S1_revised_Hist_Biol.xlsx`, `10.6084/m9.figshare.30281263.v1`) provides a global specialist-curated Silurian–Early Carboniferous species list (`1,004` species rows + `194` continuation sub-rows, recording FAD and LAD localities per species with locality-specific ages). Preliminary parse gives `~7–9` Silurian-only vs `~105–110` Early-Devonian-only `B2` locality–age pairs (`~8%` Silurian, where FAD/LAD truncation omits intermediate Devonian localities and is therefore conservative in favour of a higher Silurian share).

---

## 3. Candidate Inventory Sets (`B2` `main` Core; `B0`/`B1` as Noted)

Define four sets on `[393.47, A]`, evaluated at both `locality_age` and `region_stage`:

- **`S0` (`endpoint_primary`):** Current `select_records(..., variant="primary")` (`B2` `n_guar = 48`). **Role:** Retained conservative baseline for record-start limits (`C27`, `C61`) and minimum rate-reduction hurdles (`C48`, `C61` folds, `C62`), because smaller Devonian `n` yields older `T` and smaller minimum hurdles. Not valid alone for within-window Silurian/Devonian shares (`C59`, `C60`).
- **`S1` (`early_devonian_restored`):** `S0` plus hygiene-screened `wide_age_sensitivity` PBDB rows in [horizons_reviewed.csv](../../data/macro/horizons_reviewed.csv) that lie **wholly within the Early Devonian** (`min_ma >= 393.47` and `max_ma <= 419.62` Ma). Removes the `<= 20` Myr filter artefact without altering `A` or `partial`; still source-asymmetric (`tail` in Silurian only).
- **`S2b` (`pbdb_symmetric_ed`; report `S2a` `<= 20` Myr alongside):** Units backed by a PBDB collection: hygiene-screened `source == "pbdb"` (`<= 20` Myr plus clean Early Devonian `393.47–419.62` Ma) **plus** `source == "tail"` rows linked to a PBDB collection in [material_links.csv](../../data/macro/material_links.csv) (preserving curated age/duplicate repairs on PBDB collections while omitting non-PBDB `tail:` additions). Report both named-site grouping on linked Bathurst rows (`US384` vs `US385`) and strict `0.1°` coordinate binning. **Role:** Single-database protocol across `419.62` Ma.
- **`S3` (`capel2025_benchmark`):** Global literature-curated `B2` window records extracted from `Table_S1_revised_Hist_Biol.xlsx` under pre-registered rules (`Task 1B`), carrying F3's `main` age-envelope treatment for disputed anchors (specifically `393.47–426.7` Ma for Yea, matching `S0–S2b`, with Capel's literal `'Ludfordian'` / `'Pridoli-Pragian'` coding reported as a sub-variant). **Role:** Single specialist-literature protocol (FAD/LAD species localities + `region_stage`) across `419.62` Ma.

---

## 4. Tasks (Marked CORE or OPTIONAL)

### Task 1A [CORE]: Hygiene audit of Early Devonian `wide_age_sensitivity` PBDB rows
Inspect all guaranteed `wide_age_sensitivity` PBDB collections with `min_ma >= 393.47` and `max_ma <= 422.7` Ma in [horizons_reviewed.csv](../../data/macro/horizons_reviewed.csv) (`39` `B2` rows; `45` `B0/B1` rows) against [pbdb_plant_collections.csv](../../../../data/eprp/record/pbdb_plant_collections.csv), [pbdb_plant_references.csv](../../../../data/eprp/record/pbdb_plant_references.csv), [macrostrat_units_window.csv](../../../../data/eprp/record/macrostrat_units_window.csv), `Capel 2025 Table S1`, and [source_adjudications.csv](../../data/macro/source_adjudications.csv). Record a cited disposition table excluding verifiable post-Early-Devonian miscodings (`pbdb:28216`, `28302`, `28303`, plus any others found) and unlinked duplicates (`pbdb:27917` = `M-xinjiang-zosterophyllum`). Build `S1`, `S2a`, and `S2b`.

### Task 1B [CORE — Pre-Registration Gate]: Written `Capel 2025` (`S3`) mapping specification
**Before computing any Silurian/Devonian share on `S3`**, write a deterministic rule document and mapping table specifying:
1. Mapping from Capel's `Group/affinity` + genus (`Lycopsida`, `Zosterophyllopsida`, `Barinophytopsida`, `Basal euphyllophytes`, `Euphyllophyta inc sed`, `Cladoxylopsida`, `Filicopsida`, `Sphenopsida`, `Progymnospermopsida`, `Stenokoleales`, `Spermatophyta`, plus crown-assigned genera inside `Basal eutracheophytes` / `Incertae sedis` cross-walked against [name_classifications.csv](../../data/macro/name_classifications.csv), e.g. *Aberlemnia*) to `B2` (`main`).
2. Mapping of `Temporal distribution` strings (including `'Gordstian'`, early/mid/late substages, and cross-stage ranges) to [timescale.csv](../../../../data/timescale.csv) `(min_ma, max_ma)`.
3. Deterministic normalisation of `Locality/ies` strings into `(formation_site_key, age_group)` (`locality_age` analogue) and `(palaeoregion, midpoint_stage)` (`region_stage` analogue, using F3's palaeoregions in [occurrences.py](../../tools/occurrences.py)).
**Gate:** Second agent reviews and signs off on the mapping rules and edge cases *before* `Task 3` runs on `S3`.

### Task 2 [OPTIONAL]: Database vintage and China cross-checks
*(Skip only if time-boxed; do not block Core tasks.)*
- Tabulate pre-2003 vs post-2002 reference shares and country counts in [pbdb_plant_references.csv](../../../../data/eprp/record/pbdb_plant_references.csv) across Silurian vs Early Devonian `S2b`.
- Compare Chinese Silurian-only vs Early-Devonian-only `B2` section counts in [gbdb_plant_fossils.csv](../../../../data/external/gbdb/gbdb_plant_fossils.csv) (`derived_in_core == "yes"`, `derived_group_conflict == "no"`, GTS2012 `419.2`/`393.3` Ma) against `S2b` and `S3`.
- Extend `S3` mapping from `B2` to `B1` and `B0` (`Capel 2025` + local `capel2022/mmc5.xlsx` locality count check).

### Task 3 [CORE]: Rerun `C59` and `C60` on `B2` across `S0`, `S1`, `S2a`, `S2b`, and `S3`
For both `Gorstian–Pridoli` (`419.62–426.7` Ma) and `Ludfordian–Pridoli` (`419.62–425.0` Ma), at both `locality_age` and `region_stage`:
- **`C59` ([combined_rulers.py](../../models/loop3/combined_rulers.py)):** Expected count and upper binomial tail `P(X >= k_obs)` for `level`, `rock`, `spore_share`, `search`, `search_plant_excluded`, `rock × spore_share`, and `search × spore_share` (report `k_min` guaranteed in interval, plus `k_max` reaching into interval).
- **`C60` ([switch_reading.py](../../models/loop3/switch_reading.py)):** Clopper–Pearson one-sided 95% lower share, `least_rate_relative_to_mean`, upper tail `P(X >= k_obs | level)`, **lower tail `P(X <= k_obs | level)`** (to test downward departure from a steady rate), `largest_change_factor_cutoff_over_A`, and `n_regions`.

### Task 4 [CORE]: Endpoint and requirement arithmetic outside `C59`/`C60` + Silurian-only window check
1. **Full Emsian window (`c = 393.47` Ma):** Compute `T`, `m*(n)`, `K(n)`, `444` & `452` Ma zero-delay folds (`C27`, `C48`, `C53`, `C55`, `C57`, `C58`) for `B2` across `S0`, `S1`, `S2b`, and `S3` (`locality_age` and `region_stage`), plus `B1` (`C61`) and `B0` (`C62` with/without Oman) on `S0` vs `S1` (trivial from `horizons_reviewed.csv`).
2. **Devonian-free Silurian window (`c = 419.62` Ma, extending `C30`'s pre-declared `Pridoli` cutoff):** Apply $K = (A - 419.62)(0.05^{-1/k} - 1)$, $T = A + K$, and `444/452` Ma folds $(t - A)/K$ using only guaranteed Silurian `B2` units `k` across `S0`/`S1`, `S2b`, and `S3` (`locality_age` and `region_stage`), at both `A = 426.7` Ma (`L = 7.08` Myr) and `A = 425.0` Ma (`L = 5.38` Myr), plus leave-Bathurst-section-out (`k - 4` or `1` collapsed section unit) to quantify single-section leverage.

### Task 5 [CORE]: Exact interval-wide KS shape feasibility (`C49`, [interval_feasibility.py](../../models/loop3/interval_feasibility.py))
Run all six declared histories (`flat`, `pbdb_all`, `pbdb_plant_excluded`, `decline25`, `decline10`, `pbdb_excluded_decline10`) across all young-cutoff straddler inclusion states on `B2` (`main`) for `S0`, `S1`, `S2a`, `S2b`, and `S3` (finite-sample `kstwo` reference primary; also check `B1` and `B0` on `S1`). *(If `S3` has `> 10` young-cutoff straddlers, group exchangeable straddlers sharing `(clipped_min_ma = 393.47, max_ma)` by integer count rather than $2^{|\text{partial}|}$ bitmasks.)* Record whether `flat`, `decline25`, and `decline10` attain `p >= 0.05` in any inclusion state.

### Task 6 [CORE]: Parallel Bathurst-hinge run (`A = 425.0` Ma, Yea excluded)
Repeat Tasks 3, 4, and 5 for `B2` (`main`) with the three Yea units (`M-ghin-ghin`, `M-ghin-ghin-b2`, `M-limestone-road`, and their `S3` Yea counterpart) excluded so `A = 425.0` Ma (Ludfordian base, Bathurst Island—the oldest *certainly* Silurian crown find).

---

## 5. Pre-Declared Outcome Gates (`Task 7`)

A claim is **withdrawn** only when **both balanced protocols (`S2b` and `S3`) agree** against it; disagreement between sets narrows the claim to its supported domain.

1. **`C59` (`rock` and `rock × spore_share` fail later-find placement):**
   - **Holds:** `P(X >= k_min) < 0.05` on `S1`, `S2b`, and `S3` (`locality_age` and `region_stage`, both `A = 426.7` and `425.0` Ma).
   - **Holds in narrower form:** Fails (`p < 0.05`) on `locality_age` across all sets and `S1/S3` `region_stage`, with `p >= 0.05` only on small-`n` `S2b` `region_stage`.
   - **Withdrawn:** `p >= 0.05` on **both `S2b` and `S3`**.
2. **`C59` (`spore_share` alone fails later-find placement):**
   - **Holds:** `P(X >= k_min) < 0.05` on `S1`, `S2b`, **and** `S3` (`locality_age` and `region_stage`).
   - **Holds in narrower form:** `p < 0.05` on `S1` (or one grain of `S3`) while `p >= 0.05` on `S2b` **or** `S3` (not both) $\rightarrow$ report as inventory-dependent rather than an unqualified failure.
   - **Withdrawn (for `spore_share` alone):** `P(X >= k_min) >= 0.05` on **both `S2b` and `S3`** at `locality_age` $\rightarrow$ withdraw the claim that the trilete-reporting share fails the later-find check (retaining `rock` and `rock × spore_share` if Gate 1 holds, and noting that `spore_share` alone falls `5.1–7.1×` earlier—matching older ancestors at `<= 31` independent finds, `C56`!).
3. **`C60` (Late-Silurian finding rate & Discussion "switch" reading):**
   - **Holds (reframed to regional establishment):** At `region_stage`, `S1`, `S2b`, and `S3` are all compatible with a level rate (`two-sided p_level >= 0.05`) with Clopper–Pearson lower 95% rate ratio `>= 0.40` across `>= 5` regions (meaning geographic finding was near its window mean by the late Silurian even if per-region locality density grew later).
   - **Holds in narrower form:** `locality_age` drops (`lower ratio < 0.40` or downward `P(X <= k_obs | level) < 0.05` on `S2b`/`S3`) while `region_stage` stays compatible with level (`P(X <= k_obs | level) >= 0.05`, lower ratio `~0.20–0.65`) $\rightarrow$ replace `"two-thirds or more"` with the explicit range across `S0/S1/S2b/S3` and separate multi-regional Pridoli presence from Early Devonian locality proliferation; demote the rapid "switch" to one conditional reading alongside a Devonian ramp.
   - **Withdrawn:** On **both `S2b` and `S3`** at **both `locality_age` and `region_stage`**, a level rate is rejected downward (`P(X <= k_obs | level) < 0.05` and lower 95% ratio `< 0.25`) $\rightarrow$ withdraw the near-average late-Silurian rate claim and the switch reading.
4. **`C27` (`428.8` Ma steady-rate limit) and `C49` (`decline25` / `decline10` shape rejections):**
   - **Effect on `428.8` Ma (`C27`):** If `flat` attains `p >= 0.05` on `S0`, `S1`, `S2b`, and `S3`, the **`428.8` Ma steady-rate limit (`S0`) holds untouched** as the conservative `locality_age` bound (supported further by `S1`'s `~428.2` Ma and the Devonian-free `c = 419.62` Ma bound of `428.5` Ma at `k = 13`), because shape tests do not select `flat` over other passing histories ([estimands.md](../../manuscript/estimands.md) Trap 15). It is withdrawn/modified only if `flat` fails (`p < 0.05` across all allocations) on **both `S2b` and `S3`**.
   - **Effect on `decline25` and `decline10` (`C49`):**
     - **Holds:** `decline10` fails (`p < 0.05` across all inclusion states) on `S0`, `S1`, `S2b`, **and** `S3`.
     - **Holds in narrower form:** If `decline25` passes on `S1`, `S2b`, and `S3` (guaranteed as well as possible), drop the `S0`-specific statement that `decline25` fails on guaranteed finds. If `decline10` fails on `S0`, `S1`, and `S3` while passing on `S2b` (or vice versa), state explicitly that `decline10` is rejected on literature-curated inventories (`S0/S1/S3`) and not on database-only `S2b` (or vice versa).
     - **Withdrawn (`decline10` rejection):** If `decline10` attains `p >= 0.05` on **both `S2b` and `S3`**, withdraw the statement that the observed age spread rules out the `10` Myr exponential decline (and state the direct consequence: without an external bound on how steeply finding rose from the Silurian into the Early Devonian, the `10` Myr decline—which sets no limit within `469.4` Ma—also fits the balanced fossil age spread).
5. **`C48`, `C58`, `C61`, `C62` (minimum rate-reduction requirements) & Bathurst `425.0` Ma (`Task 6`):**
   - **Holds (with upward sensitivity recorded):** Keep `S0` (`8–12×` `B2`, `6.3–10.9×` `B1`, `8.4×` `B0`) + `region_stage` (`2.4–4.5×`, `2.6–4.5×`, `3.2×`) + the Devonian-free `c = 419.62` Ma check (`3.0–9.4×` at `444` Ma) as the conservative baseline, and record in the ledger/supplement that restoring Early Devonian localities (`S1`/`S3`) raises `locality_age` hurdles (`~12–17×` on `S1`) while `region_stage` changes little, and that anchoring on Bathurst (`425.0` Ma) shifts `T` to `~427.2` Ma and leaves `444–452` Ma folds at `~8.8–12.4×` (`S0`).
