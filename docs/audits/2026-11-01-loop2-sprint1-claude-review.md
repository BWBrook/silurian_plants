# Review 1: Claude on Codex's Loop 2 sprint 1

Claude Opus 5.5 (`claude-opus-5-5`), 1 November 2026, reviewing `4bada50`–`8417725` under
`sprints-loop2.md` v2.1 and Board 2779–2784. Barry's prompt: "Back to you for review, and your sprint
(if ready)."

## Verdict

Sprint 1 stands, with one gate decision reversed for sprint 2 and two wording corrections. Its
observation audit, identification result and sensitivity surfaces reproduce and are correctly labelled.
The count gate is right for Murzuq and for any analysis that pairs Le Hérissé et al.'s counts with
Vecoli et al.'s trilete zero. It is too strong for QSIM-801 as a whole: Vecoli et al.'s own examination
supplies a conservative within-sample bound without those counts (below).

## What was checked independently

- **Numerical (another implementation).** I rebuilt the joint likelihood from the frozen frame. My
  version integrates over the Gamma(2, 2) well effect with adaptive quadrature and profiles the common
  rate continuously over [1e-3, 20], where the original uses 96 nodes and a grid plus bounded search
  over [1e-5, 8]. It roots the likelihood ratio against 5.991. All four no-transfer break-even values
  under independent uniform stage ages, stage allocation, reproduce to four decimals:

  | Target | Codex | Claude |
  |---|---:|---:|
  | Constant intensity from τ to 459.1 Ma | 0.0910 | 0.0910 |
  | Window 459.1–462.6 Ma | 0.9559 | 0.9559 |
  | Window 459.1–467.1 Ma | 0.2363 | 0.2363 |
  | Window 459.1–469.4 Ma | 0.1735 | 0.1735 |

- **Tests.** All 37 tests pass with `uv run --with numpy --with scipy --with pytest python -m pytest
  …` (3.2 s). This is the README command; the handoff's "pytest could not run" applied only to the
  bare environment. `tools/loop2_observations.py check` passes: 164 appendix rows, 153 exact chart
  matches, 11 and 5 unmatched.
- **Source mapping.**
  - **695.7 ft.** I re-read Le Hérissé et al. (manuscript p.37–38). The 10.4% belongs to
    *Micrhystridium*, and the next sentence gives cryptospores 0% in the distal prodelta facies. My
    v2 plan had posed this as a discrepancy to check; it was my misreading of the paragraph. Logged
    under Q5.
  - **QSIM-801 Table 1.** I reconstructed Vecoli et al.'s Table 1 independently from the rendered
    page and the text layer (below).
- **Frozen evidence.** Loop 1 outputs and receipts are untouched by the Loop 2 commits.

## Corrections

1. **H0c correspondence.** The results note says the constant-intensity origin comparison at g = 1,
   κ = 0 "matches the frozen H0c statistic". It matches under shared midpoint ages: 0.0955, which equals
   `fstar_H0c_459.1` at ρ = 1 in `m2_results.csv`. Under independent uniform ages it is 0.0910. The two
   differ only through the age treatment; the note should name the chronology.
2. **Caving (my v2 change 5).** Codex is right that the older zeros constrain caved reports in the
   older cuttings, not contamination of the reference cuttings, unless a transfer relation is
   assumed. My v2 wording overreached.

## The QSIM-801 gate: reversed in part

The gate rejected an empirical share bound because no microscopy denominator is reported. Le
Hérissé et al.'s counts cannot be linked to the examination behind Vecoli et al.'s zero. Both
statements are correct, but they do not exclude a bound built only on Vecoli et al.:

- **One examination produced both observations.** Vecoli et al.'s 20 Liège preparations gave the
  cryptospore occurrences of Table 1 (printed p.321) and the statement that "only cryptospores and no
  trilete spores have been observed" (p.330). No cross-preparation effort ratio is needed.
- **The marks lower-bound the denominator.** Each mark is at least one examined cryptospore unit.
  Table 1 holds 99 marks across 17 positive samples, counted on the rendered page as 72 in the upper
  panel and 27 in the lower, which matches the text layer.
  - Conditional on each sample's land-spore total N_i ≥ m_i, zero triletes has probability
    ∏(1 + hθ_i)^(−N_i) ≤ (1 + hθ)^(−M), where θ is a floor holding in every sample.
  - Rejecting θ when (1 + hθ)^(−99) ≤ 0.05 is therefore a valid level-0.05 test.
- **h is the declared parity, not an unknown preparation ratio.** It is the relative probability
  that a trilete unit in the examined material is recovered and recorded. Its scenarios (1, 0.5, 0.25,
  0.1) are declared, as ρ was in Loop 1.
- **The estimand is a persistent floor, not a mean.** Heterogeneity between samples raises the
  all-zero probability, so a pooled-mean reading would be anti-conservative. This is Codex's own
  beta-binomial warning, and the floor estimand answers it. Within-sample clustering is carried as a
  design effect.

The result, the known-answer check and its limits are in `docs/loop2-sprint2-results.md`. It is an
unqualified empirical bound under declared assumptions, not a replication: no counted reference share
was found.

## What sprint 1 established that the paper must carry

- **The 462.6 Ma window endpoint is fragile.** It flips at an indigenous reference fraction of 0.956,
  that is, at under 5% contaminant reference positives with no transfer to older cuttings. Under shared
  midpoint ages the interval has no sampled exposure. The paper should lead with the H0/origin
  comparison and the wider windows, reporting 462.6 Ma only with this caveat beside the B4 denominator.
- **Observational equivalence through a = ρgf and b = κ(1 − g).** This is the general statement of
  why the binary record cannot separate producer rarity from poor delivery or contaminated
  references.
- **Leave-one-well-out.** At ρ = 1 it moves the reference-level window endpoint between 462.6 and
  468.1 Ma; omitting H2 gives 468.1 Ma.
