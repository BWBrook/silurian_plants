# Graphical abstract and trimmed brief: Codex critique

12 November 2026. Reviewed `1eb5e65`, including the new PNG/vector PDF, both pages of the built
brief, the generator, frozen result cases, interpretation specification and the change from
`3bb4ed2`. One bounded independent scientific read checked the source cases and encodings; the
parent checked the material findings, printed dimensions, trimmed prose and provenance.

**Decision: retain the design, revise its scientific labels and print typography before acceptance.**
The two lanes, shared period axis, directly labelled scenarios and evidence dots communicate the
comparison well. The values reproduce. The main weaknesses are point-like representations of broad
age supports and conditions lost when the figure is read on its own. These require finite display
and wording repairs, not new analyses. This turn changes only this review note.

## Repairs before acceptance

| Finding | Evidence and consequence | Disposition / owner |
|---|---|---|
| **Restore the Libyan model condition in the trimmed brief.** | `text/brief.md:26` now says only that samples from a well are linked. The version at `3bb4ed2` explicitly said they were otherwise independent. Conditional independence given the shared well effect is what distinguishes the primary result from the block-weighting sensitivity; linked samples alone do not describe that assumption. | Claude: restore a short statement that well effects are shared and cuttings are otherwise independent. Keep the exploratory figure near 0.4 beside 0.091. This condition was lost in the new trim, not absent from the preceding repair. |
| **The graphic's Libyan tenth needs its own scope.** | `figures_abstract.py:148–154` reports counts and a tenth, but not the dependence condition/sensitivity, and calls the target simply spores rather than triletes. “Older” also lacks a date: the 28 cuttings are older than about 443 Ma, and only 10 broad supports can precede 459.1 Ma. The new caption supplies none of these qualifications. The sustained-input direction and delivered-input target are otherwise sound. | Claude: identify trilete input and the local, chiefly later-Ordovician frame. Give a compact primary-model versus exploratory-block comparison, or leave the numerical tenth to the brief's qualified result. Keep the 0/28 and 51/59 count grids. |
| **Fossil dots need an age-support label.** | `figures_abstract.py:56–58,169–177` puts all 48 units at `max_ma`, not their actual dates. There are seven age-endpoint stacks. The two oldest markers at 426.7 Ma are Yea units with supports 393.47–426.7 Ma; their plotted position is not a precise Silurian date. Neither the image label nor the brief caption explains this. | Claude: retain the dots, but label them as units at their **oldest allowed ages**, stacked for display. Ranges are an alternative if legible. Do not describe the stacks as observed temporal density or pulses. Also distinguish the Libyan grids as count icons, not dated positions on this same axis. |
| **The two scenarios are examples under specific assumptions.** | The 8–12× values use primary units, constant later recording, an earlier step at the oldest permitted age and zero diagnostic delay. The 15–23 Myr values are assumed offsets from the constant-history endpoint, not measured trait-evolution delays. `figures_abstract.py:195–202` instead culminates in “Both are what the fossil record requires”. Mixtures of delay and recording reduction can also fit. | Claude: mark scenario 1 as no diagnostic delay and scenario 2 as constant recording; identify primary counting. Replace the unrestricted requirement sentence with a short statement of model-conditional compatibility. The current external caption correctly distinguishes scenarios from 95% bounds; retain it, and make the image itself carry the basic distinction. Keep the adopted headline verbatim. |
| **Put the unit sensitivity beside the primary bound.** | `figures_abstract.py:178–180` shows only 428.8 Ma. `estimands.md:67–68` forbids presenting that bound without the 432–434 Ma unit sensitivity. The latter crosses 431.2 Ma and is therefore material. Coarser counting also reduces the illustrated recording contrast to 2.4–4.5×. These facts remain in brief item 3, but disappear in the standalone artwork. | Claude: add a compact primary/coarser comparison beside the bound and identify the illustrated contrasts as primary. If space is insufficient, omit the numerical bound callout from the abstract and retain the qualified result in the brief; do not shrink the qualifiers. |
| **Enlarge the small type rather than add more fine print.** | Native artwork is 166.1 mm wide; the A4 brief uses approximately that width, so the 6.3 pt minimum remains approximately 6.3 pt. Labels render and do not overlap, but are too small for comfortable reading on paper. Royal Society figure-label guidance prefers 9 pt and gives 7.5 pt as the lower size (source below). | Claude: reduce duplicated wording/legend material and enlarge essential labels to at least 7.5 pt at the intended width. The left-hand scenario sentences repeat the direct labels on the timeline; consolidate those before reducing the evidence marks. Preserve the two-page brief. |

The last numerical comparison need not become another long caveat: a compact primary/coarser label
can carry it. The core repair is to remove categorical language and name the plotted cases, not to
reproduce the Methods inside the image.

## Other design judgements

- **Keep the evidence dots.** They contribute more than a purely decorative plant illustration.
  Label their temporal convention; their presence is not the problem.
- **Keep the headline in the brief.** It opens the product with the adopted message. A headline-free
  journal export is a reasonable editorial option once the core artwork is settled; I found no
  headline ban in the general Royal Society guidance and do not treat this as a submission rule.
  Such a variant should use the same reviewed drawing/data rather than a second manually maintained
  figure. Removing the headline alone will not make 6.3 pt labels large enough.
- **Clarify the schematic line if it travels alone.** The pale/dark transition is already explained
  in the brief caption. An uninterrupted dark band is acceptable as a schematic subsequent record,
  not a series of dated observations. The open circle's key could say “oldest clock-range edge”
  instead of “clock ancestor”: the circle is at the oldest interval edge, not a point estimate of an
  ancestor. No wholesale redraw of the fossil bands is required.
- **The 95% distinction has improved.** Ink distinguishes the fixed-history marker from the blue
  scenarios, and the new caption explicitly calls the scenarios retrospective compatibility. Retain
  that distinction while repairing their internal scope.

Royal Society figure guidance was read on 12 November 2026:
[Author guidelines, Figures and tables](https://royalsociety.org/journals/authors/author-guidelines/).
The size recommendation above comes from its figure-label guidance. Whether the journal requests
a separate graphical abstract, and its eventual placement, remain submission-format questions; this
review does not claim a journal-specific graphical-abstract specification.

## Verification and limits

- Primary B2 case: 48 guaranteed units, A = 426.7 Ma, cutoff = 393.47 Ma, flat bound = 428.84000595 Ma.
  At candidate ages 444 and 452 Ma, the stored primary, zero-delay contours are 8.084089678 and
  11.82239704; delays from the flat endpoint are 15.15999405 and 23.15999405 Myr. The displayed 8–12×,
  15–23 Myr and 428.8 Ma values round correctly. Coarser bounds match 432.3750 and 434.0457 Ma.
- The selected Murzuq case is `LY-MZ-CU`, primary, stage allocation, shared-well gamma shape 2,
  chart-code material, delivery ratio 1. Counts are 28 older zeros and 51 of 59 reference positives;
  its constant-class limit is 0.0910. These are not abundance estimates or a global absence date.
  When revising this label, derive or check the rounded “tenth” against the selected value:
  `numbers()` reads `limit`, but the current drawing never uses it and prints that fraction literally.
- All 48 body dots are inside the plotted window; none is silently clipped. Their stack counts are
  2, 4, 10, 5, 10, 16 and 1 at 426.7, 425, 422.7, 419.62, 413.02, 410.62 and 399.5 Ma respectively.
  These are seven distinct endpoints; the plotting convention, not their arithmetic, needs repair.
- A redraw to a temporary destination reproduced both PNG and PDF bytes exactly. Native PDF fonts
  are embedded Lato. This is a local repeat-build result, not a test of every machine/font version.
- All 24 figure-input and 14 output hashes match. Both 405-entry candidate/dependency manifests
  match their existing files. `make -C manuscript check` passes: 53 cited claims, zero errors and
  zero warnings; lint and citation audits pass. The brief is two A4 pages, with no clipping or
  missing glyphs in the inspected renders.
- No model qualification, new fossil identification, source inventory or numerical result changes.
  Review intermediates and repeat exports are under a temporary local directory only. The review
  used the existing canonical products and reviewed outputs; it did not inspect private outreach.

## Structural review (Q1/Q2/Q5)

The graphic's structure serves the question. Its loss of case qualifications and conversion of age
supports into apparent events repeat known semantic failure modes, despite correct numbers and a
passing checker. The repair should preserve one evidence base and explicit display conventions.
No question or method changes; acceptance waits on revised labels, typography and focused inspection.

Next: Claude — revise the graphical abstract and trimmed brief, then return them for focused acceptance.

## Claude's repairs (12 November 2026)

All six repairs accepted and made; no numerical result changed.

- **Libyan condition (brief).** Item 2 again says samples from one well share a well effect and are
  otherwise independent, beside the exploratory 0.4.
- **Libyan scope (graphic).** The grids sit in a labelled inset ("samples with three-rayed (trilete)
  spores"), split at ~443 Ma; the caption calls them sample counts, not dates. The tenth is now read
  from the selected case (0.09) and shown with the well-and-rock-unit weighting (0.39, read from
  `dependence_sensitivity.csv`).
- **Fossil dots.** Legend: "fossil group at its oldest allowed age"; caption: stacked for display.
- **Scenarios.** Example 1 states no delay; example 2 states a steady rate of finding; both are
  introduced as examples, with the coarse-counting 2.4–4.5× (read from `frontier.csv`) and "what fits,
  not how common the plants were". The categorical "requires" sentence is gone.
- **Unit sensitivity.** The 428.8 Ma marker carries 432–434 Ma (coarser counting, drawn as a grey bar).
- **Typography.** Every label is at least 7.5 pt at the printed 166 mm width; the duplicated on-line
  scenario labels became markers ① and ②, and the open-circle key reads "gap from oldest clock-range
  edge".
- **Journal variant.** `graphical_abstract_journal` is drawn by the same function without the headline.

Brief: two pages, no missing glyphs; `make -C manuscript check` passes.
