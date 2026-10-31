# Independent review: Samphire, Qusaiba E2 extraction and conditional sampling

31 October 2026, Codex. Scope: read-only review of the parent’s sprint-2 source conclusions and `tools/sprint2.py`. Outputs only under `/private/tmp/sp-sprint2-parent-review`; the parent’s functions were imported with bytecode disabled and their output directory redirected to scratch. No repository files were changed by this review.

**Result: the source conclusions and current numerical extraction are accepted. No substantive error was found in the 37-column Qusaiba output, six-sample Balme inventory or 27 conditional-sampling rows. One narrow join-validation improvement is recommended for the reproducer.** Input/output hashes for the reviewed snapshot are in `receipt.json`.

## 1. Balme’s original report

I read the original printed pp.22–26 (PDF pp.26–30) and visually checked printed p.26. The independently transcribed inventory is `balme_inventory_independent_check.csv`.

- Six samples were received: samples 1–3 are Jurassic cuttings; samples 4–5 are Permian cores; sample 6 alone is Lower Ordovician, black shale with graptolites from core 4. Five samples cannot serve as an early-Palaeozoic E2 reference class.
- Sample 6 yielded a rich spinose-hystrichosphaerid assemblage after maceration and other well-preserved organic entities. This is direct recovery evidence, not a source-missing gap.
- The original states that definite spores were absent while allowing that small, smooth spherical bodies might be primitive alete spores. It provides no secure E2 assignment, no secure E2 zero and no modern target-specific search-effort measure.
- The words identifying “definite spores” as trilete spores occur in square brackets in Strother & Foster (2021), SI PDF p.2; they are a later interpretation. The parent preserves that distinction.
- The Balme target section gives only core 4, without a numerical depth. The 2021 SI supplies 4090–4100 ft and explicitly says all core depths are three feet greater than in the well-completion report, consistent with WAPIMS. Keep the corrected depth’s later attribution.

The parent’s current `samphire1961_inventory.csv`, `frames.csv`, `units.csv` and core-4 outcome rows correctly update primary-source access while retaining E2 as unresolved. E1’s evidence-only label does not authorise a binary analytical zero.

## 2. Qusaiba: independent raster and joins

The source is the verified held `library/closed/wellman2015_firststudy.pdf`, Table 2, printed p.116/PDF p.6. I independently inspected the full raster and three enlarged column panels, then checked the complete blue/pink dyad/tetrad matrix using raster pixels rather than the script’s PDF-word coordinates.

The independent raster check covers **21 taxon rows × 37 columns = 777 cells**. It finds **226 marks**, all matching the parent’s reported taxon lists exactly. **Every one of the 37 columns has at least one dyad/tetrad mark.** The marked-cell pixel counts are at least 138; every empty cell has zero dark pixels after masking grid lines, so the result is insensitive to the 50-pixel threshold. All 37 core labels and literal depth labels were also transcribed from the enlarged raster and matched to the inventory and output. See `qusaiba_raster_check.csv` and `qusaiba_raster_cells.csv`; `raster_check.py` reproduces the pixel check from the scratch PPM render.

The printed depth labels include the `m` suffix and `?341.0m`; all are retained literally. The separate numerical feet interpretation agrees with the paper’s feet-based plate captions, including 551 ft on printed p.122, and the existing inventory’s provenance. It must remain an interpretation beside the source labels, not a silent source correction.

Printed pp.112–113 state that 37 samples were collected and Table 2 details all processed samples; selected duplicate preparations from a second laboratory are not additional samples. Around 30 g was processed per primary preparation. The paper explicitly reports abundant marine palynomorphs in all samples (pp.112,122), independently supporting productivity. The deepest tabulated sample, 551.0m as printed/core C56, has eight dyad/tetrad marks. The source therefore contains no sampled pre-E2-appearance interval under the repository’s accepted main reading. It is a complete source-specific reference candidate, not evidence that all sampling classes have detection probability one.

**Join-validation recommendation, `tools/sprint2.py` around lines 41–61.** The current script joins extracted columns to inventory records solely by declared order, checking only that there are 37 records. The present joins are all correct, but a changed order or label can silently associate correctly extracted outcomes with the wrong material IDs. Validate the source depth headers and core labels against every inventory row before writing. This is a safeguard for the reproducer, not a finding of incorrect current data.

One bounded implementation is to import `re`, extract the 37 numeric metre-labelled header words, and assert:

```python
depths = sorted((x, text) for x, y, text in words
                if 135 < y < 150 and re.fullmatch(r"\??\d+(?:\.\d+)?m", text))
assert len(depths) == 37
assert [int(r["wellman_table2_order_top_to_base"]) for r in records] == list(range(1, 38))
assert all(abs(core[0] - depth[0]) < 0.01 for core, depth in zip(columns, depths))
assert [(core[1], depth[1]) for core, depth in zip(columns, depths)] == [
    (r["wellman_core"], r["wellman_literal_depth_label"]) for r in records
]
```

I tested those header assertions against the current PDF and inventory: all pass. The numerical feet interpretation remains outside this literal-header validation. The source PDF hash should remain in the extraction receipt, as it is in this independent receipt.

## 3. Conditional sampling arithmetic

All 27 rows of `conditional_sampling.csv` match a separate 60-digit Decimal calculation based directly on

`p_old = 1 - (1 - p_reference) ** (transport * relative_intensity)`

and

`P(all n empty) = (1 - p_reference) ** (transport * relative_intensity * n)`.

For every row the stated integer n is the smallest satisfying probability ≤0.05; n−1 gives probability >0.05. Values of n span 2–28,434. The probability and older-detection columns agree within 1e-14; `conditional_sampling_independent_check.csv` retains higher-precision values. Re-running both parent functions with output redirected to scratch reproduced both CSVs byte for byte, including the parent’s current LF formatting.

These formulae are correct only under their stated hypothetical interpretation: transport multiplies the **Poisson encounter intensity**, not detection probability directly; relative intensity is another assumed multiplicative factor; blocks are independent and of the declared comparable exposure. The input probabilities are chosen scenarios, not fits to Qusaiba, Samphire or M3. These are zero-count sampling calculations, not F3 qualification, estimated sample requirements or probabilities that a clock maximum is true. The current status column appropriately marks every row hypothetical.

## 4. What is and is not available for M1

The current source conclusions should preserve a descriptive comparison under both readings:

- Qusaiba supplies 37 reported E2-positive source samples under the main and inclusive reading, with independently documented marine recovery.
- Samphire core 4 remains unresolved under both readings: its undifferentiated alete-body report is neither a securely identified E2 occurrence nor a verified E2 absence.
- Samphire cores 6 and 8 remain unresolved for embryophyte affinity under the current main reading; the existing inclusive reading counts their published cryptospore interpretation as detected. A non-counting/unresolved main interpretation is not a zero. Two preparations/core intervals do not become multiple independent trials through specimen or publication counts.

This gives a useful source/reading contrast but **does not yet supply an absence-based empirical M1 design** from these sources: secure older E2 non-detections, comparable class/reference support and cross-source transport remain missing. Adding Qusaiba cannot by itself resolve those missing ingredients. Whether the separate Cambrian/Argentina source tranche supplies any admissible contrast must follow its own inventory and reporting findings; this review did not re-read those sources.

Do not equate lack of samples older than 515.5 Ma with mathematical impossibility of testing an origin at 515.5 Ma. Properly eligible non-detections in younger material could constrain a lineage assumed to have persisted since that origin. The actual reasons for non-admission here are outcome ambiguity, sampling/reporting completeness, dependence and unsupported reference transport. Conversely, counting disputed early occurrences under an inclusive reading does not create missing earlier negatives or prove a clock maximum.

## Verification and retained evidence

`check_parent.py` verifies the three primary-PDF hashes against `library/closed.tsv`, re-runs the parent functions into scratch, checks every conditional-sampling row independently, and records hashes of the script, inputs and output tables. `raster_check.py` uses an independently rendered PPM and manually read header labels; its code, 777-cell result and 37-column join result are retained. The primary source text and page images under `text/` and `render/` remain copyrighted scratch and should not be committed. The derived checks, scripts and this paraphrased review can be integrated by the parent.

## Parent disposition

The header-order/core/depth assertions were adopted in `tools/sprint2.py`. Both
outputs regenerated byte-identically after the guard. The retained independent
receipt describes the pre-guard reviewed code; the final sprint receipt binds
the updated code and unchanged scientific output. Derived checks are retained
in `data/units/sprint2/independent_check/`; original render/text scratch stays local.
