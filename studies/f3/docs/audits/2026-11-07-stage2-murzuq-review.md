# Stage 2 Murzuq local-time and dependence review

7 November 2026. Independent read-only audit by Codex.

## Frame and exposure geometry

`models/f3/loop3/murzuq_stage2.py::units()` selects
`LY-MZ-CU`, `allocation=stage;material_type=chart-code`, non-excluded rows
with a non-missing `d`. The selected frame is 87 rows: 28 transported older
cuttings and 59 reference cuttings, with 51 reported reference detections.
The 28 older rows split into 10 Darriwilian rows in D1-200 and H2-NC186, 6
Katian–Hirnantian rows in D1-200, 7 Katian–Hirnantian rows in I3-NC186, and 5
Hirnantian rows in H2-NC186 and I3-NC186. Thus 10 rows have possible support
older than 459.1 Ma and 18 are wholly younger than it; the older-frame
assertion and stage split are reproduced by the committed tests.

The timescale mapping uses the base of the oldest stage as the older endpoint
and the base of the next younger stage as the younger endpoint. For each older
row, exposure is the overlap of that full stage enclosure with 459.1–443.1 Ma,
divided by the enclosure width; reference rows receive exposure one. The ten
Darriwilian rows each receive 0.9/11.2 = 0.0803571429, summing to
0.8035714286. Katian, Hirnantian and mixed Katian–Hirnantian older rows have
zero exposure to the pre-459.1 interval. No point ages or clipped intervals
are used.

## Likelihood checks

I independently reimplemented the Gamma(2,2) quadrature and profiled the
shared reference rate against the older relative intensity. It gives
`rho_f_contour = 0.0910296478764`, matching the generated
`dependence_sensitivity.csv` value 0.0910296478764 and the committed test
tolerance. Repeating the no-frailty, separate-well-rate calculation gives
0.0995125220124, matching the separate-well sensitivity row. The no-frailty
pooled-rate diagnostic is 0.0832422956131 and is correctly retained as a
separate row rather than conflated with the Gamma result.

The critical value is the declared likelihood-ratio threshold
`-2 log(0.05) = 5.9914645471`. It is labelled in the output as `critical`,
not as an achieved coverage result. The output scope explicitly states that
this is a retrospective, unqualified sensitivity and that inverse block
weights produce a composite likelihood.

## Dependence and well-drop sensitivities

For `well_formation`, inverse group sizes sum to one within each
well × old/reference × formation block: 7 effective reference blocks and 6
effective older blocks. For `well_stage_support`, they sum to one within each
well × old/reference × oldest-stage × youngest-stage block: 6 effective
reference blocks and 6 effective older blocks. These are transparent block
composite diagnostics, not calibrated independent-unit likelihoods.

The generated leave-one-well rows cover all five wells (B2-NC186, D1-200,
E1-NC174, H2-NC186 and I3-NC186), with contours 0.09317, 0.13673, 0.09382,
0.11000 and 0.18575 respectively. They are appropriately labelled as
unqualified sensitivities; no coverage claim is attached.

## Panel and provenance

`sample_time_support.csv` has endpoints 432.9–469.4 Ma. The panel limits are
469.4 Ma on the old side and 432.4 Ma on the young side, so every full-stage
interval is visible with a half-million-year margin. I inspected the rendered
PNG: all five wells and the 459.1 Ma line are visible, with no interval
clipping. The output receipt hashes match the current script, input tables,
and all five generated output files.

Conclusion: the implementation and outputs pass this limited audit. The
result is a retrospective local-time/dependence sensitivity, not a
recalibrated qualification or a new primary Murzuq estimate.
