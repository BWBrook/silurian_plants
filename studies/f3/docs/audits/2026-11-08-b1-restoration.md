# B1 restoration: *Cooksonia bohemica* and Capel Horeb

Date: 2026-11-08
Reviewer: sol_high_specialist (GPT-5.6-sol/high)
Scope: source adjudication and regeneration of F1 B1 occurrence-model outputs only. No manuscript, claims-ledger or figure rendering changes are included here.

## Target and estimand

B1 is the record of places with multi-sporangiate land plants: an occurrence enters through direct evidence for branched fertile axes (E3) or through the more inclusive lycophyte-total-group event (E5). The bound is a conditional, model-based 95% upper limit on the start of this recognisable record, not an origin date and not a fossilisation-rate estimate. The restoration asks whether two younger occurrences were absent from B1 because the sources lacked branching, or because E3 had not been assessed outside the originally enumerated Homerian-and-older inventory.

The observation process matters. Branching, terminal sporangia and conducting tissue can be preserved or described on different specimens. Neither E4 (conducting tissue) nor locality-level co-occurrence with E4 is by itself evidence for B1. The source-specific inclusion contract is therefore: include a record in B1 only when the cited material directly documents a branched fertile specimen, while retaining any conducting-tissue evidence as a separate event and without transferring anatomy among specimens.

## Source adjudication

### *Cooksonia bohemica*

The held publisher PDF is `library/closed/libertin2023_bohemica.pdf` (SHA-256 `a93a420d71a37abba7bc279ea97ac2aaa10104a03a2378bc0c7b4668b5c74412`), registered as `libertin2022` in `library/closed.tsv`. Its diagnosis and specimen descriptions identify repeatedly isotomously divided fertile axes, including the type material JE-Sch0260A/B and specimen D554, with sporangia at ultimate branch tips. The material is Pridoli. The same paper discusses conducting cells separately and qualifies their tracheid interpretation. E3 is therefore directly supported; E4 remains a distinct, qualified anatomical interpretation.

### Capel Horeb, Upper Roman Camp Beds

The source adjudicated was Edwards & Rogerson (1979), *New records of fertile Rhyniophytina from the late Silurian of Wales*, DOI `10.1017/S0016756800042503`, inspected in full at the Cardiff ORCA copy (`https://orca.cardiff.ac.uk/id/eprint/10902/1/Edwards%201979.pdf`). The paper places the Upper Roman Camp Beds in the Whitcliffian, late Ludlow, and illustrates a branching fertile *Steganotheca* specimen (NMW 77 34G 11, plate 1e) and a *Cooksonia* specimen with characteristic branching (NMW 76 10G 1, plate 1g). Its tracheids are demonstrated in separate sterile axes, not in those fertile specimens. E3 is directly supported for the locality-age occurrence, while E4 remains anatomically separate.

This work is not presently registered as `edwards1979b` in `library/open.tsv` or `library/closed.tsv`, and no local byte-identical source was available for hashing. The file registered as `edwards1979` at `library/closed/edwards1979_firststudy.pdf` (SHA-256 `c29931c327fe97adb8e725fd944779fc77334dafd8b39eb7e60d33aac478d77f`) is a different paper, the Freshwater East flora, and must not be treated as the Capel Horeb source. The ORCA PDF was inspected through the browser because direct command-line retrieval returned HTTP 403; no original-file hash is reported.

### Negative control

The Lang axis remains E4-only: neither branching nor capsules are documented. It stays outside B1 and B2 in both main and inclusive readings. The restoration therefore does not implement a general E4-to-B1 rule.

## Data correction

`M-bohemica` and `M-capel-horeb-ludlow` now carry E3 in `data/occurrences/observations.csv`. Their single main interpretations in `data/occurrences/interpretations.csv` count E3 and E4 but state which specimens support each event. Regenerating `data/occurrences/reading_assignments.csv` adds exactly six E3 assignments: the two observations under the main, inclusive and outlier readings.

The previous regression test treated the absence of an E3 entry as evidence of no branching, although E3 had only been systematically enumerated for Homerian and older fossils. This was informative missingness created by inventory scope. The replacement test asserts the two source-backed E3 inclusions, the reading-specific B2 status of *C. bohemica*, and exclusion of the E4-only Lang axis.

## Recomputed results

| Reading | B1 possible places | B1 guaranteed places | Oldest possible age (Ma) | Flat-rate 95% bound (Ma) | PBDB-all bound (Ma) | Plant-excluded PBDB bound (Ma) | 25-Myr decline bound (Ma) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Main | 71 | 69 | 432.9 | 434.649615 | 436.684364 | 435.983734 | 437.571872 |
| Inclusive | 75 | 73 | 445.2 | 447.367027 | 448.527161 | 448.067598 | 453.756036 |

For main B1, excluding *Cooksonia barrandei* changes the flat-rate bound from 434.649615 to 432.272324 Ma (difference -2.377291 Myr). Under the inclusive reading the corresponding values are 447.367027 and 447.397755 Ma (difference +0.030728 Myr).

The scientific CSV changes are confined to B1 rows, plus the added E3 reading assignments and resulting macro inventory rows. B0 and B2 rows are exactly unchanged in `reviewed_bounds.csv`, `simulation_results.csv` and `suppression_sensitivity.csv`; B2 membership is also exactly unchanged in `primary_unit_membership.csv`. The B2 primary flat-rate result remains 50 possible places, 48 guaranteed places and 428.840006 Ma. The interval-search and timescale-sensitivity scientific tables are unchanged; their receipts change only because the rebuilt horizon-input hash changed.

Affected generated artefacts are:

- `data/macro/horizons_reviewed.csv` and `data/macro/build_receipt.json`;
- `models/f3/loop3/out/reviewed_bounds.csv`, `age_sensitivity.csv`, `classical_comparison.csv`, `delay_sensitivity.csv`, `primary_unit_membership.csv`, `shape_diagnostics.csv`, `simulation_results.csv`, `suppression_sensitivity.csv` and `influential_taxa.csv`;
- their analysis, simulation, suppression and influence receipts, plus input-hash-only updates to the frontier, interval and timescale receipts.

## Verification

`uv run --with numpy --with pandas --with scipy --with matplotlib --with pytest python -m pytest models/f3/loop3 -q` passed: 48 tests. Direct comparisons against the pre-restoration committed outputs confirmed exact equality of all B0 and B2 result subsets described above. `git diff --check` passed.

`uv run tools/occurrences.py check` passes after refreshing the stale support-text locator for `I-capel-horeb-ludlow-attached` to the Morris wording retained in `taxa/cooksonia.md`. Only the locator text changed: the alternative interpretation, its `live` status, E4 assignment, age and biological reading are unchanged.

## Residual risk and recommendation

The repair settles these two false negatives, not the completeness of every younger E3 record. The inventory still lacks an explicit assessed-positive/assessed-negative/unassessed field, so future additions could repeat the same missing-as-absent error. A later schema revision should encode assessment status, but it is not required to accept these source-supported restorations.

Use the regenerated B1 outputs and rebind every B1 number in the claims ledger and products, including suppression and influence claims. Keep B2 headline results unchanged. Register the actual Edwards & Rogerson source separately from the Freshwater East paper and archive a hashed local copy when an authorised download is available. The source evidence and exact numerical rerun are sufficient for this correction; another independent scientific review is unlikely to change the inclusion decision, although the parent should independently recount the units and closed-form bounds before publication.
