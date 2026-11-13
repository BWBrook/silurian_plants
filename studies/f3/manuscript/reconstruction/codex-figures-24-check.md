# Audit: built Figures 2 and 4

Independent Codex audit, 11 November 2026, of the reconstruction figures at `f6ba666`. Inspected
`figures_step4.py`, the current legends and frozen case selectors; viewed both original PNGs and fresh
renders of both PDF pages. No model or figure-generator runs, source-table changes, or edits outside
this review note. PDF render intermediates were written only under `/tmp/`.

**Decision:** numerical content and graphical encodings pass. Two internal label repairs remain before
acceptance; they make the figures agree with the distinctions already stated in their captions.

## Material repairs

| Figure / source location | Finding | Narrow repair |
|---|---|---|
| Figure 2(b), `figures_step4.py`, panel title and endpoint annotations | The image calls the whole row “the 95% older bound T” and shows 428.8, 431.0 and 448.1 under that heading. Only 428.8 is the displayed fixed-history confidence bound; the other two are data-selected step sensitivities with no nominal or selection-adjusted 95% coverage claim. “Retrospective” appears in the caption but nowhere in the image. The standalone graphic therefore loses the agreed distinction. | Title the panel “Fixed-history bound and retrospective step/delay scenarios”, or equivalent. Keep “one-sided 95%” attached specifically to constant-recording 428.8. Mark the halved/tenth endpoints as retrospective compatibility endpoints; the assumed 20 Myr bridge is a scenario, not an inferred ancestor date. |
| Figure 4(b), panel title and y-axis | “Contrast or delay needed” and “Required later / earlier recording ratio” turn the equality contours into unrestricted biological requirements. The caption correctly calls them retrospective compatibility scenarios, but the graphic itself omits that scope. | Use a title such as “Retrospective recording and delay scenarios” and y-axis “Later / earlier recording ratio”. Preserve the actual ratios, clock shading and curve labels. An internal retrospective/compatibility label makes the panel independently interpretable. |

No layout changes are requested. The plotted labels and lines are legible in PNG and PDF, there is no
material clipping or overlap, and no missing glyphs were apparent in these two figures.

## Exact case and rendering checks

**Figure 2.** The dots are all 48 guaranteed B2/main locality–age units, positioned at their maximum
support ages and stacked at ties; they are not a selected exact-age chronology. This convention is
stated in the image and caption. The anchor is 426.7 Ma and cutoff 393.47 Ma. `F.primary_bound` selects
`B2/main/locality_age/primary/Emsian/flat/no excluded region`, giving 428.84000595 Ma. `F.suppressed`
selects flat-baseline B2/main sensitivities with break 426.7 and multipliers 0.5 or 0.1, giving
430.9800119 and approximately 448.1000595 Ma. These round correctly to 431.0 and 448.1. The assumed
20 Myr bridge from the constant endpoint gives 448.84000595 Ma, correctly labelled 448.8. The
different arrow positions are distinguishable and the reversed age axis is correct.

Sources: C27/V003, C53/V108, C32, C33; `loop3/out/primary_unit_membership.csv`,
`reviewed_bounds.csv`, `suppression_sensitivity.csv`; `manuscript/figures.py::{primary_bound,suppressed}`.
The model history is constant later and changed before the data-selected anchor; the half/tenth
numbers must retain the retrospective status recorded in the saved rows and ledger limits.

**Figure 4(a).** There are 50 primary B2/main age bars. Forty-eight have `min_ma>=393.47`; the two
cutoff-straddlers both have supports 387.95–399.5 Ma and are separately marked with dashed orange
lines. The panel does not replace their age ranges with point dates. No support is clipped by the
437–386 Ma plotting window. The constant bound is correctly left of the age bars, and the 432.38–434.05
region–stage/curated sensitivity band is correctly older than the dashed 431.2 maximum. The legend's
48 guaranteed / 2 straddling distinction agrees with the caption's 50 possible / 48 guaranteed counts.

**Figure 4(b).** All drawn case parameters agree with `loop3/out/frontier.csv`, `reading=main`:

| Treatment | Guaranteed count | Anchor / cutoff (Ma) | Assumed delay drawn |
|---|---:|---|---|
| primary locality–age | 48 | 426.7 / 393.47 | 0, 10, 20 Myr |
| region–stage | 19 | 426.7 / 393.47 | 0 Myr |
| curated oldest records | 15 | 426.7 / 393.47 | 0 Myr |

The script checks every stored main-reading contour row against the closed form

\[
1/r=\frac{t-d-A}{(A-c)(0.05^{-1/n}-1)}.
\]

The 800-point display curves use that same formula and the stored case parameters. The checks compare
raw ratios, before the declared display floor at one, with tolerance `1e-6`. Undefined `t-d<=A`
combinations become NaN and are absent, rather than being plotted at one. Defined ratios below one
are drawn at one, as the caption states; those floor segments are a display convention, not equality
contours. Saved primary zero-delay markers are 8.084089678 at 444 Ma and 11.82239704 at 452 Ma, correctly
drawn and rounded to 8.1×/11.8×.

The conditional maximum-age CDF at these raw equality contours is 0.05 under the fixed scenario. The
curves estimate neither historical rates nor a joint confidence region. The selected delays and
unit alternatives are declared scenarios, not optimised biological histories.

**Clock bands.** The plotted source values in `manuscript/figures.py::CLOCKS[tracheophyta]` are
Morris 450.8–419.3 Ma, Harris 452–447 Ma and Hooper 432–428 Ma. Their positions and overlap are correct.
The Morris younger end is outside the 456–426 Ma panel and the visible band continues to that edge;
“Morris (to 451 Ma)” refers to its rounded older end. Preserve this as a clipped published summary,
rather than presenting the right panel edge as its younger endpoint. Figure 1 supplies the full
published ranges and statistical-summary distinctions.

**Provenance.** Every input and output SHA-256 in `figures/figures.json` matches the files inspected,
including PNG and PDF versions of both figures. The existing formula assertions cover the selected
contour cases; the count/support inspection above independently checks the plotted unit selections.
The PDF renders agree with the PNGs on data, labels, curve shapes and shading.

After the two wording repairs, one focused visual acceptance read of the rebuilt figures is enough.
