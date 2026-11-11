# Canonical integration review

Codex, 11 November 2026. Reviewed `c207fe0` against accepted reconstruction `aa176df`.
This is a review, not an implementation tranche. Product sources, numerical evidence and PDFs are
unchanged. Two bounded independent reads covered article/supplement and brief/agent guide;
the parent checked the integration diff, figure bytes, manifests and the material findings.

**Disposition: return to Claude for finite repairs before Barry's reading.** The article's science
survives integration, the restored tables agree with their earlier versions, and the numbered
citations work. The rewritten brief and agent-guide synthesis lose distinctions that the agreed
interpretation specification requires. The rendered article also loses symbols. No model rerun is
needed.

## Findings and dispositions

| Priority | Finding and checked evidence | Required repair | Owner |
|---|---|---|---|
| High | `manuscript/text/brief.md:34` changes the Murzuq target to producer "abundance", omits conditional independence given the shared well effect, and omits the approximately 0.4 block-weighting sensitivity. C24 is a limit on sustained local delivered spore input/encounter, not a separate abundance estimate; `estimands.md`, M2, explicitly keeps the dependence sensitivity beside it. | Describe spore input or encounter. State the shared-well conditional-independence assumption in plain language and retain the roughly 0.4 sensitivity as an unqualified comparison. Preserve the local and chiefly later-Ordovician scope. | Claude |
| High | `brief.md:17` calls the purple tenfold arrow a movement of "that" 95% limit. This transfers the green fixed-history bound's confidence interpretation to a data-selected step scenario. C32 and the accepted main Figure 2 legend call the latter retrospective compatibility. The half-rate wording in `brief.md:35` needs the same explicit distinction. | Label half/tenth scenarios as retrospective compatibility endpoints. Attach 95% specifically to the fixed-history calculation. | Claude |
| Medium | `manuscript/text/for-agents.md:55` attributes the quantities behind "several times" to both C48 and C24. Only C48 supplies the vascular-body recording contrast; C24 is a different local spore-input limit. The additional "provided" condition in `brief.md:40` similarly extends the body result to every living-land-plant date. | Keep Barry's adopted headline sentence verbatim. Scope the explanatory recording-contrast sentences to vascular-plant bodies, and describe the spore conclusion separately. | Claude |
| High | The article PDF silently drops raw text rho at `main.md:117` (PDF p4) and twice in the Figure 3 legend (`figures.md:5`, p14), and the less-than-or-equal sign in the Figure 4 legend (`figures.md:7`, p15). Visual inspection confirms blank symbols, and text extraction returns replacement characters. The graphics themselves retain their glyphs. | Use supported mathematical glyphs, e.g. `$\rho$` and `$\le$`, and rebuild. Inspect the actual integrated PDFs; source lint and citation checks do not detect this failure. | Claude |
| Medium | `manuscript/settings/build.yaml` selects `manuscript/csl/proceedings-of-the-royal-society-b.csl`, but neither the 403-entry package manifest nor the dependency manifest includes it. `manuscript/package.py:101–103` still lists only the Chicago style, and dependency traversal does not parse YAML configuration. All existing entry hashes match. | Add the active numbered style to the candidate dependency set and regenerate manifests after the source/PDF repairs. The full Git checkout contains it; the omission concerns the claimed candidate package closure. | Claude |
| Low | `for-agents.md:250–251` says C53 is quoted in the Figure 4 legend; it is in Figure 2's legend (`figures.md:3`). | Correct the figure reference. | Claude |

## Checks that pass

- The integrated article matches the accepted step-4 prose except narrative-author citation
  expansion, S12/S13 pointers, author placement and the contribution-inventory path. No changed
  numerical result or analysis was found.
- Tables S12 and S13 retain the former main Tables 3 and 2, including their subjects and values.
  Their rendered layouts are legible (supplement pp4 and 8–9). Numbered citations identify the
  intended authors and references.
- All eight canonical main PNG/PDF figure files are byte-identical to the accepted reconstruction
  exports. The moved generator changes its entry point and paths, not the drawing calculations.
- All 23 figure-input and 14 figure-output hashes match. All 403 existing package entries and all
  candidate dependency-entry hashes match; this does not rescue the missing active style above.
- `make -C manuscript check` passes: 53 claims cited, zero errors and zero warnings; all profile
  lint and citation audits pass. Bibliography entries unused by an individual profile are non-fatal.
- The brief is two A4 pages and visually legible without clipping or missing glyphs. The article is
  15 pages and supplement 29. No new analysis, source authentication or model qualification was
  attempted; those numerical artefacts are unchanged by this integration.
- Primary row selectors, reproduction commands and the spore input/dependence distinctions remain
  present in the detailed agent-guide result inventory. The defect is in its new synthesis paragraph.

One renderer-specific observation is not promoted to an authored-layout finding: Poppler masks part
of the Figure 2/4 headings, whereas PyMuPDF renders them intact; PDF heading and image boxes are
separate. Retain this as a compatibility observation if it recurs in the final reader's viewer,
rather than changing the scientific graphic to address an unconfirmed box collision.

## Structural review and handoff

For Q1/Q2/Q5, the rebuilt structure still serves the investigation. No question or method changes.
The integration exposed three ways meaning can drift while every number still passes: an encounter
limit becomes abundance, a retrospective scenario inherits confidence language, and a synthesis
joins different estimands. The correct main article and explicit figure contracts provide the repair
template. This review does not close the integration loop; Claude should repair the products, rebuild
and refresh the manifests, then check the changed sentences and PDF glyphs before Barry reads.

Next: Claude — repair the integration findings, then return the products for Barry's reading.
