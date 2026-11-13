# Review C: Claude's adjudication and integration

Claude Opus 5.5, 5 November 2026. Barry resumed the research through the Board Messenger with Codex's
review C (`2026-11-05-review-c.md`), its methods audit (`2026-11-05-review-c-methods.md`) and the trilete
rubric (`2026-11-05-trilete-evidence-rubric.md`), and the instruction "Take your next turn." Each finding
was checked against the frozen outputs before it was accepted. All are accepted; one became a new
declared sensitivity rather than a wording repair.

## Findings and dispositions

| Finding | Checked against | Disposition |
|---|---|---|
| C1/R2: B0–spore separation is conditional, not an observed lag | `reviewed_bounds.csv`; `docs/plan-loop3.md` B0 definition; observation S-w22-K12 | Accepted. B0 was declared as "accepted land-plant macro- or mesofossil, sterile axes included"; the build took curated records from E3–E5 only, so the Katian Oman sporangial fragments (E2) never entered B0. Not fixable by relabelling: added `models/f3/loop3/oman_sensitivity.py` (C40–C41). |
| C2/R1: ρf ≈ 0.09 holds for H0c only | `m2_results.csv` rows 54–57 | Accepted. Products recomputed: H0c 0.091 throughout; H0 0.184/0.129/0.105/0.092. C24 rewritten. |
| C3: QSIM ratio described as a percentage | `qsim_share_bounds.csv`; 0.3072/1.3072 = 0.2350, 0.03072/1.03072 = 0.0298 | Accepted. C12 now names the minimum trilete:cryptospore ratio and its share equivalents. |
| C4/R5: Borenshult readings, the 459.1 Ma derivation and Fig. 1–2 | Rubinstein & Vajda (2019) Figs 3–4; Hooper et al. Supplementary Table 4 | Accepted, including R5's correction of my 2026-11-04 addendum: a crown minimum from the definite triletes needs an added fossil-to-crown mapping, and would sit at the bentonite's young uncertainty edge (about 454.24 Ma), not at 454.4 Ma. New S2.4; C42–C44. |
| C5/R3: shape diagnostics shown for one age treatment | `shape_diagnostics.csv` rows 24–35 | Accepted. Constant recovery: independent-uniform p 0.073–0.765, midpoint 0.0085, shared quantile 3.1e-9–0.0165. Table S7 now shows all three treatments; C31 demoted to provisional because its values changed. |
| C6/R4: tenfold suppression and 15–23 Myr delays | `suppression_sensitivity.csv`, `delay_sensitivity.csv` | Accepted. Wording now "one illustrative scenario" and "minimum assumed offsets at the endpoint bound"; C32–C33 limits rewritten. |
| Smaller corrections (brief counts, "single assumption", cutoff wording, Fig. 3 caption, M1 scope, "robust to most data choices") | the cited files | All accepted and applied. |
| Rubric | rubric source checks | Accepted: five concordant Borenshult depths, with the six-depth Fig. 3 reading as alternative and the Hooper exclusion as sensitivity; Turkish record keeps its original Ashgillian–Hirnantian wording; Zbrza outside strict trilete occurrences; Qusaiba-1 the secure comparator. No composite score. `taxa/ambitisporites.md` updated. |

## The Oman sensitivity

`oman_sensitivity.py` reads the frozen inventory, reproduces the 48 frozen B0 rows exactly (it fails
otherwise), then adds S-w22-K12 as one Katian locality–age unit (452.8–445.2 Ma).

| Main reading, Emsian cutoff | Constant | PBDB density | Plant-excluded | Decline 25 Myr | Decline 10 Myr |
|---|---:|---:|---:|---:|---:|
| Frozen inventory (75 units) | 434.51 | 436.38 | 435.73 | 437.16 | none ≤ 469.4 |
| With Oman fragments (76 units) | 455.19 | 456.62 | 456.09 | 465.21 | none ≤ 469.4 |

The separation from the certain cryptospore minimum (458.2 Ma) falls from 21–24 Myr to 1.6–3.0 Myr, and
reverses under the 25 Myr decline. With the fragments, every declared history fits the sequence poorly
(constant: midpoint p 5.5e-12), because one Katian unit is followed by more than 12 Myr without another
body unit. Without them, constant recovery fits only marginally (independent-uniform p 0.0041–0.062).

**Interpretation.** Neither inventory measures a lag. The comparison is a demonstration of how an
endpoint bound is controlled by its oldest admitted unit. I kept both inventories rather than redefining
B0 after seeing the result. The fragments came from palynological preparation of borehole material,
not from the macrofossil collections that dominate the recovery proxies, which is an argument for
treating them separately; but the axial mesofossils already in B0 also come from bulk maceration, so
that argument does not justify the original omission. The paper therefore reports both, with the
declared definition favouring inclusion.

**Consequence for M3.** None directly: the fragments enter B0 only. The lesson transfers: B2's bound
rests in the same way on Yea and Bathurst Island.

## What changed in the products

`manuscript/claims.csv` (C12, C24, C28, C29, C31–C33 revised; C40–C44 added), `text/main.md`,
`text/supplement.md` (S2.4 new; S5.1 Oman paragraph and Table S3b; Table S7 all age treatments; S7 review
C entry), `text/brief.md`, `text/for-agents.md`, `text/figures.md`, `mapping.csv`, `figures.py` (Fig. 1
Borenshult and Oman bars; Fig. 4 Oman markers), `tables.py`, references (Rubinstein & Vajda 2019;
Wellman et al. 2003). Frozen analyses untouched.

## Checks

- `make -C manuscript check`: 44 claims, all cited, 0 errors, 0 warnings; makedoc lint and citation
  audit pass for all profiles.
- 38 tests pass (26 Loop 3, 12 Borenshult screen); `tools/units.py check` passes.
- Borenshult profile likelihood ratios reproduced independently by direct maximisation (1.3157, 1.0753,
  1.1155); the known-rate value 2·m·rate = 1.3908 also checks.
- Brief renders as two A4 pages; Figs. 1, 2 and 4 inspected.

## For Codex's closure check

Provisional and needing the other agent's check: C40 and C41 (new), C31 (values changed), plus the
earlier provisional C24, C28 and C33. Please also check whether any E2 record other than S-w22-K12
qualifies as a pre-Silurian land-plant mesofossil under the declared B0; I found none in
`data/occurrences/observations.csv`.
