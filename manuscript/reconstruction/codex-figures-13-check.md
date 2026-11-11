# Built Figures 1 and 3: independent check

Codex, 11 November 2026. Base: `f6ba666`. Inspected both committed PNGs, both PDFs rendered with
Poppler, the plotting functions and their selected frozen table rows. Only this note is edited.

**Decision.** The plotted clock values, first-appearance endpoints, Libyan sample frame and selected
model outputs agree with their declared inputs. Repair the Borenshult reading display and the
unevaluated interpolation claim, then improve well-group and 10/18 visibility. No model rerun or source
re-extraction is needed. One focused acceptance read of the revised exports and relevant code will
complete this check.

## Material repairs

1. **Figure 1 combines the two Borenshult readings.** The legend promises separate possible and
   definite bars, but `fig1()` draws one “possible and definite” row. Split the source levels: possible
   at 48.2 m and definite at 43.1 m. They may legitimately share the coarse 458.2–454.41 Ma support:
   both are Sandbian and below the Kinnekulle ash. Shared numerical endpoints do not make the two
   affinity readings interchangeable. State that age support is conditional on the named fossil
   reading, so the queried specimen's right tick does not assert a certain trilete identity. Retain
   the existing broad supports rather than converting historical approximate source dates to precise
   new ages.

2. **Figure 3's joined lines are not evaluated compatibility contours between markers.** Four
   delivery ratios were selected from the frozen table. Straight segments on the logarithmic delivery
   axis overstate the intermediate constant-history limit. For example, halfway between 0.25 and 0.1
   in log space, *ρ* ≈ 0.158: the drawn segment gives about 0.637, whereas the declared constant-product
   relation gives about 0.576. Use evaluated markers with thin dotted visual guides and apply
   compatibility statements only at the marked scenarios, as the parent proposes. This also avoids
   inventing intermediate bounded-history fits. Existing point values and their qualification remain
   unchanged.

3. **Make well membership and the pre-maximum exposure visible.** All 87 rows are drawn, but at the
   native PDF size the 3.2-point symbols overlap vertically, and the absence of well separators makes
   some older rows appear attached to the preceding label. In particular, the three Darriwilian rows
   visually near B2's label belong to D1; the other seven belong to H2. Delineate well blocks and give
   their counts, reducing symbol size or increasing height as needed. Add direct “10 potentially
   pre-459.1” and “18 wholly younger” annotations rather than relying on the long legend to explain
   the diagnostic split. This improves the scientific reading of a limited pre-maximum frame.

The parent also proposes saying that symbols are placed at support midpoints for display. Retain
that clarification: the plotted supports are correct, but the primary model integrates uniform ages
over them rather than assigning every cutting its midpoint.

## Figure 1 checks that pass

The bars use the declared source clock constants: Morris 515.2–473.5 and 450.8–419.3 Ma, Harris
515–493 and 452–447 Ma, and Hooper 457–450 and 432–428 Ma. Labels round these as the article does.
The legend correctly distinguishes Morris's envelope over seven topology-specific 95% HPD intervals
from the other study intervals. Source numerical clock/maximal ages remain separate from the current
stage mapping and published ash date. The 515.5, 459.1 and 431.2 Ma lines are placed correctly.

The strict-compilation rows match `first_appearances.csv`: cryptospores 469.4–458.2 Ma and triletes
458.2–445.2 Ma. The Oman row is 452.8–445.2 Ma, and the main crown-vascular first-appearance support is
426.7–419.62 Ma, matching reviewed unit membership. The glyphs, source names and age labels render
correctly in PNG and PDF. No other material clipping or overlap was found in this figure.

## Figure 3 checks that pass

The selected input rows have 87 distinct unit IDs. All are chart-coded cuttings in the declared
stage-allocation frame. Counts by well are B2-NC186 6, D1-200 25, E1-NC174 9, H2-NC186 17 and
I3-NC186 30. There are 59 reference cuttings with 51 positives and 28 older zeros. Ten Darriwilian
cuttings, three in D1 and seven in H2, span 469.4–458.2 Ma and can extend before 459.1 Ma; the other
18 older-frame cuttings are wholly younger.

The age-support groups reproduced from the stage names are:

| Support (Ma) | Count |
|---|---:|
| 443.1–432.9, Rhuddanian–Telychian | 58 |
| 443.1–440.5, Rhuddanian | 1 |
| 452.8–443.1, Katian–Hirnantian | 13 |
| 445.2–443.1, Hirnantian | 5 |
| 469.4–458.2, Darriwilian | 10 |

The result selector matches `LY-MZ-CU`, `primary=True` and
`allocation=stage;cluster_k=2.0;material_type=chart-code`. It selects these four rows, each with
qualification `pass` and finite limits for both plotted classes:

| Older/reference delivery *ρ* | Constant input | Exposure-weighted mean, bounded variable input |
|---:|---:|---:|
| 1 | 0.0910 | 0.1835 |
| 0.5 | 0.1821 | 0.2576 |
| 0.25 | 0.3641 | 0.4211 |
| 0.1 | 0.9103 | 0.9207 |

The chosen columns are `fstar_H0c_459.1` and `fstar_H0_459.1`; neither a midpoint-age allocation nor
an unqualified dependence sensitivity was substituted. Axis direction, constant/variable labels,
reference shading and the 459.1 Ma line agree with the legend. The legend correctly defines *f*,
older/reference *ρ*, equal delivery and audited target zeros.

## Evidence and limits

Inspected `figures_step4.py`, imported helpers/constants in `manuscript/figures.py`,
`figures/figures.json`, `data/timescale.csv`, the strict spore first-appearance rows, main B0/B2 unit
membership, selected `m2_units.csv` and `m2_results.csv` rows, the legends and the existing Borenshult
age/source audit tables. Every declared input and output hash in the figure manifest matches its
current file. The stage-allocation unit rows leave numerical age fields empty; support reconstruction
therefore correctly uses their stage names and the project timescale.

This check verifies the plotting and its existing evidence contract. It does not freshly authenticate
the thesis, repeat candidate-paper reads, re-estimate compatibility limits or rerun qualification.
Print inspection used the native one-page PDF exports, approximately 7.2 inches wide, plus their PNGs;
the eventual article-page placement remains to be checked at canonical integration.
