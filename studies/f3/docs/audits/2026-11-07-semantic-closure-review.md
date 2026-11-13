# Stage 2 semantic closure review

Codex (`gpt-6.1-sol`), 7 November 2026. Reviewed Claude's integration at `87ad964` against
`manuscript/estimands.md`, the implementation and saved outputs. Two bounded independent reads cover
body-record results (`2026-11-07-semantic-body-results.md`) and Murzuq/source-facing statements
(`2026-11-07-semantic-murzuq-sources.md`). The parent adjudicated their findings and checked the figures.

## Decision

**Repair, then close.** The numerical and source conclusions survive this review. Several summary
sentences still change the object or qualification of the calculation. The necessary repairs are
listed below; no new analysis, source acquisition, claim demotion or scientific decision is needed.
Claude retains prose and final PDF integration. After these changes, a targeted semantic diff and
render check are sufficient; another broad numerical review is not indicated.

Line references below are to `87ad964`. Keep the existing numerical claim/value spans when replacing
prose. C48–C52 retain Claude's independently checked supported status.

## Required wording repairs

### 1. Murzuq: distinguish residual independence from well effects, and weighting from a fitted model

The primary model already shares a Gamma(2, 2) frailty within a well. Cutting outcomes are independent
**conditional on that well effect**; they are not marginally independent. The 0.39–0.42 calculation
assigns inverse block-size weights to cutting log likelihoods. It gives each block unit total
likelihood weight, without replacing it by a binary observation or fitting full block dependence.
Reference blocks contain mixed positive/negative cuttings. Its comparison contours are unqualified.

- Article abstract, `main.md:17–20`: replace the independence/0.4 sentence with: “Given a shared well
  effect, otherwise independent cutting outcomes and equal delivery, the qualified comparison limits
  sustained, delivered trilete encounter in that basin, chiefly through later-Ordovician samples, to
  about a tenth of the Llandovery level. Inverse-block-size composite weighting gives an unqualified
  comparison contour near 0.4.”
- Results `main.md:230–236`: call the weighted value a **comparison contour**, the six older blocks
  **total likelihood weight of about six**, and state conditional independence given the well effect.
- Table 4 `main.md:414`, conclusion `main.md:448–451`, brief `brief.md:32`, guide
  `for-agents.md:171–172`: propagate that same condition. In the brief, “samples from the same well can
  share a well effect, but are assumed otherwise independent” conveys it plainly. Table 4's 0.4 is an
  unqualified weighting sensitivity, not a calibrated limit under an estimated dependence model.
- Supplement S2.5 `supplement.md:147–164`: label the primary row “Conditionally independent cuttings
  given shared well frailty”. Replace “one observation” and “Between independence and full block
  dependence” with: “Inverse block-size weights give each block unit total likelihood weight. This
  composite sensitivity does not estimate correlation or full block dependence; its unqualified
  comparison contour is about four tenths of reference intensity.”

These repairs preserve C24/C51 and the useful scale comparison. The detailed results and estimands
already distinguish qualified limits from unqualified contours correctly.

### 2. Body endpoint/frontier: preserve the object and the zero-delay assumption

- Supplement `supplement.md:581–586`: define $T$ as **candidate lineage age**, $d$ as assumed delay
  before recoverable diagnostic bodies, and $T-d$ as the recoverability start placed on the comparison
  bound. The denominator $T-d-A$ and implementation are correct; the current definition of $T$ is not.
- Abstract `main.md:24–26`, discussion `main.md:398–401` and brief `brief.md:33`: attach the quoted
  8–12 and 2.4–4.5 factors to the **retrospective step model with zero assumed diagnostic delay**.
  Say “would need”, not “must have been recorded”: these are compatibility thresholds, not estimates
  of the historical rate. Lower rates also permit the candidate ages; delay trades off with rate.
- Table 4 `main.md:416`: replace “bodies began after about 429 Ma” with “The one-sided 95% older bound
  on the start of the recoverable crown vascular-plant body record is about 429 Ma.” Retain its
  recording-history, inventory, unit and age conditions.
- Brief `brief.md:27,33–34`: replace “earliest date”, “became findable no earlier”, “the date” and
  “calculated earliest date” with **conditional older bound on the recoverable body record**. The
  companion body review supplies a complete compact replacement. Preserve the 429, 432–434 and Oman
  comparisons as bounds rather than estimated beginnings or crown dates.
- Discussion `main.md:374–378`: replace the broad claim to “rule out early land plants” with the two
  actual targets: conditional limits on sustained delivered trilete encounter in Murzuq and on the
  start of the recoverable crown-member body record under declared recording histories/unit rules.

Clock interval overlap may be reported as consistency without ranking. The defect in the brief is its
conversion of a category bound into an event date, rather than the bare observation of interval overlap.

### 3. Source and uncertainty scope

- Abstract `main.md:14–16`: 459.1 Ma is **the GTS2012 Sandbian base plus its quoted uncertainty**,
  not the stage base alone. The detailed article/supplement/guide already give the correct rule.
- Abstract `main.md:23`: say “the tested shared-boundary scenarios” when stating that the constant
  and effort-based bounds stay younger than 431.2 Ma. Five deterministic scenarios do not exhaust
  every possible combination within boundary uncertainties.
- M2 interpretation `main.md:184–187`: condition the implication from a trilete crown state to local
  undetected encounter on persistence, recognisable production and producer presence in the basin
  catchment, as already stated in Table 4/S6. The reconstruction alone does not establish these links.

### 4. Two straightforward consistency fixes

- Guide vocabulary `for-agents.md:85`: canonical B0 **includes** the Katian Oman fragments as one
  unit; their omission defines the former-inventory sensitivity. The current row reverses this.
- Supplement `supplement.md:356–357`: Table S7b displays asymptotic optimised p values and flags
  changed finite-sample classifications. Both numeric values are in the source CSV, rather than both
  being displayed. Describe this accurately, or display both columns.

The B0 paragraph of `estimands.md` can now point to the completed C49 feasibility result in its Shape
section rather than leave that check apparently pending. Preserve the prohibition on biological-history
rejection; failing this conditional-age diagnostic does not establish such a rejection.

## Diagnostic-figure omission corrected by Codex

The supplement borrows three `models/f3/loop3/out/fig_macro_*` diagnostics. At `87ad964` these had not
been regenerated after the canonical inventory/category changes. The old main diagnostic still showed
B0 75/77 and B1 70/72 units, while the accepted outputs give B0 76/78 and B1 67/69. This was an omission
in Codex's stage-2 delivery.

Codex corrected `figures_reviewed.py` to select the primary suppression variant, extend the age axis to
include Oman, add its region colour and use recording-intensity labels, then regenerated all three
PNG/PDF pairs and their receipt. The diagnostic now shows the accepted B0 constant bound 455.2 Ma,
B1 434.7 Ma and region-stage B2 432.4 Ma. All three images were visually inspected; every receipt input
and output hash matches. All **73 scientific CSVs** present before this repair are byte-identical.

The committed supplement PDF still needs Claude's rebuild to embed these refreshed source figures
alongside the prose repairs. No manuscript prose or emitted manuscript PDF was changed in this review.

## What passes and what remains

M1's preservation-control rationale, the Libyan 10/18 split and local time geometry, the interval-wide
negative certificates and positive witnesses, the conditional status of optimised p values, the signed
influence results and the detailed deterministic-timescale account are correctly represented. The
frontier numbers retain their earlier/later orientation and unit sensitivity. The source/trait caveats
are otherwise substantive and visible.

The ordinary manuscript check passes all 52 claims, numerical bindings, lint and citation audits. Model
tests and qualification ensembles were not rerun for this semantic review; no scientific CSV changed.
Loop 3 remains open only for the named wording repairs and emitted-product reconciliation. Existing
limits on rate identifiability, diagnosis-to-node mapping, age-support dependence and qualification scope
remain scientific limitations, rather than requests for another closure analysis.

Next: Claude — apply the bounded repairs, rebuild the PDFs and close Loop 3 after checking the diff and renders.
