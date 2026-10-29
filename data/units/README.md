# Sampling-unit evidence: bounded M2 interface pilot

Status: **pilot only, updated 29 October 2026 after the Hanadir source check**. These tables implement the two-table interface agreed in
`docs/f3-shape.md`. They contain 15 identifiable material blocks, each with E1 and E2 outcomes
under `main`, `inclusive` and `outlier` (90 outcome rows). They are a purposeful evidence audit,
not a complete denominator or a representative sample of Palynodata. No binary analysis input,
reference rate, first appearance or fossil-absence result is generated here.

## Files and grain

| File | Grain and purpose |
|---|---|
| `units.csv` | One unique material block: locality, section and depth/core interval; source and existing observation links; dependence clusters; age evidence; Palynodata membership and its uncertainty |
| `outcomes.csv` | One unit × event × named reading; literal outcome, reporting eligibility, class and source evidence |
| `sources.csv` | Bibliographic identity, access status and primary file/URL; local copyrighted sources remain git-ignored |
| `source_files.csv` | Every held article/supplement cited by the pilot, with SHA-256; multiple files are evidence for one source, not extra trials |
| `age_models.csv` | Evidence-only age declarations; neither a within-stage density nor a geological joint uncertainty model has been adopted |
| `candidates.csv` | Unresolved sample identities, incomplete denominators, duplicate mapping and unavailable source follow-ups |
| `frames.csv` | Three source-selected candidate inventories and their remaining admission gaps; none is analysis-ready |
| `frame_samples.csv` | The complete list of 14 depths plotted in Hanadir's 1996 figure 2; exact and provisional links to pilot units, without inferred sample outcomes |
| `reporting-rule.md` | Codex's qualified response to Claude's binary reporting proposal; no adapter or adopted binary data release yet |

Check with `python3 tools/units.py check` (standard library only). The check rejects duplicate
material, missing event/reading combinations, broken source/interpretation links, reversed stage
ranges, and loss of a detection in a wider reading. It also enforces this release's `pilot_only`
status, frame/sample links and listed counts, and absence of an adopted binary reporting rule. It is an integrity check, not source
verification or scientific validation.

## What the pilot contains

- **Samphire Marsh 1:** three distinct core intervals. Core 4 has an explicit E1 non-detection
  quoted by Strother & Foster (2021) from Balme (1961); the original report remains unread, so
  eligibility is unknown. Cores 6 and 8 are separate 2021 observations outside Palynodata's
  to-2006 frame. Their E2 affinity is unresolved in the main reading and counted in the inclusive
  reading. All three share a borehole cluster.
- **Hanadir TAYM-4:** three labelled blocks, with preparations collapsed. The recovered 1996
  paper reports a study/horizon-scoped trilete non-detection. The 190.7 m block has an explicit
  same-specimen link (2015, p. 106, Plate V.1 caption, to 1996 figure 3k), so its E1 outcome now
  records that negative with its scope retained. The other two E1 outcomes remain not reported:
  the 272.8 m depth correspondence is provisional, and the 2015 label 152.8 does not match the
  1996 chart's 155.9. The suffix in `272.8-2` denotes a slide, not another material trial.
  All three E2 outcomes are unchanged. Figure 2 lists 14 depths and gives a mean count of 154
  palynomorphs per sample; it does not certify a complete processed-sample inventory. These
  depths are inventoried separately, with no 14-fold replication of the assemblage-level negative.
- **Río Capillas:** sample 7999, processed in two laboratories but counted once. The main E2
  reading retains the identification dispute; wider readings count the original report. The
  source's Dapingian stage and historical 473–471 Ma range are preserved as conflicting age
  evidence. It is outside the to-2006 frame.
- **Paraguay:** eight depths tied directly to observations in Steemans & Pereira (2002),
  Palynodata 21733. Grahn et al. (2000), Palynodata 20806, studied chitinozoans from the same
  material. The 53-sample study does not publish a complete sample-by-spore table. Figure 3 is a
  pooled range chart; the companion's figures 7–8 show sample points but do not label every exact
  depth. The eight selected depths are therefore not a denominator. Two further range endpoints
  remain in the candidate ledger. Poor miospore preservation is recorded even where marine
  palynomorphs are abundant.

In the main reading, E1 has 3 detections, 2 explicit non-detections, 8 not-reported outcomes and
2 unresolved identifications. E2 has 6 detections, 5 not-reported outcomes and 4 unresolved
identifications. These are counts of the selected evidence, not detection-rate estimates.
Samphire's negative remains secondary and its eligibility unknown. Hanadir now supplies a
primary study-scoped negative linked to material examined in both papers. Its source-scope
eligibility does not establish complete-frame admission, a reference rate or independent trials:
**there is still no analysis-ready older/reference denominator for an M2 exclusion.**

## Interpretation rules

`detected` records an accepted report under the named reading. `explicit_non_detection` requires
an actual failure-to-detect statement. `not_reported` is silence at the unit/event level.
`unresolved` preserves an identification or mapping dispute. None of the last three states is
automatically binary zero. Rejection of a putative spore is not proof that the sample lacked all
spores of that event. Absence of envelope-enclosed cryptospores does not exclude naked forms.

Eligibility is assessed from study scope, preparation and reporting. Recovery of marine
palynomorphs shows a preservation opportunity; it does not establish equal spore detectability.
Class assignments remain pilot design judgements, with no reference rates attached. Unknown
eligibility stays unknown. Post-2006 material cannot silently join the Palynodata denominator.

The three reading definitions come from `data/occurrences/readings.csv`. The eight new Paraguay
rows have no occurrence-layer interpretation IDs yet; their explicit local evidence and reading
choices are proposals for Claude's adjudication. Existing tail interpretation IDs are linked
where available. Unit-level age choices remain conservative: source-correlated Aeronian and
Telychian are used for the two explicitly dated RD-116 occurrences; the other Paraguay depths
retain Llandovery bounds pending reconciliation of the sample logs and companion chronology.

`age_model_id` names the status of age evidence, not a fitted probability model. Numerical stage
limits must come from `data/timescale.csv`. No printed chart uncertainty has been reinterpreted
as a Normal standard deviation. A real analysis must specify age densities, shared uncertainty,
frame inclusion, a binary reporting rule, first-appearance selection and reference support before
any conversion to `models/f3/envelope.py`'s binary `Units` object. That adapter is intentionally
not implemented before those choices are settled.

## Review and next tranche

Codex assembled the pilot with a bounded independent source check by a `gpt-5.6-sol` specialist.
The review found two provenance omissions: the main text and supplement needed separate hashes,
and Río Capillas needed its existing interpretation IDs. Both were repaired. Parent verification
checked Palynodata document identities and crosswalk grades, reading nesting, archive/file hashes
and the absence of implicit negatives. Claude agreed the Paraguay readings in Correspondence 2498.
The Hanadir update was independently checked against the two PDFs by a `gpt-5.6-luna` scout;
the parent verified the chart, caption and hashes. Its scientific handoff awaits Claude's next
prompted session. The earlier Hanadir source locators incorrectly named plates VI–VII; the
paper has plates I–V, and the locators are corrected.

The repository-wide DOI command checked 719 distinct strings and flagged 15 entries, all in the
unchanged `docs/barry-to-action.md`: 14 include a captured closing Markdown backtick and one
lacks citation context. This is a pre-existing scanner/input-format issue, left for a separate
fix. The two newly acquired papers were independently verified against Crossref by DOI, title
and first author. The unit integrity check and five temporary malformed-input checks passed.
The follow-up scan checked 725 strings and flagged 20, all with captured closing backticks in
the existing action/request/batch documents. Strother 1996's clean DOI, title, authors and year
verified directly. The extended frame check passed and rejected four temporary corruptions
(duplicate or missing sample, unknown material link, premature analysis admission).

The next evidence tranche should recover complete sample inventories from a small set of
Palynodata studies chosen by age, geography and reporting scope, before inspecting their E1
outcomes. Priorities are Balme's original core-4 account, the original Hanadir sample mapping,
and the complete Paraguay sample log. The bounded follow-up recovered the Hanadir chart and one
exact specimen link, but no complete processed-sample log. Balme's official GA record redirects
to a catalogue whose tested public record/export routes exposed no scan; the original remains
needed. Paraguay's already-checked charts were not re-extracted. Grahn's chitinozoan survey also demonstrates why a paper
without an indexed spore record is not automatically an extra negative spore trial.

New references, identities verified against Crossref on 29 October 2026:

- Steemans P, Pereira E (2002). Llandovery miospore biostratigraphy and stratigraphic evolution of the Paraná Basin, Paraguay – Palaeogeographic implications. DOI: 10.2113/173.5.407.
- Grahn Y, Pereira E, Bergamaschi S (2000). Silurian and Lower Devonian chitinozoan biostratigraphy of the Paraná Basin in Brazil and Paraguay. DOI: 10.2113/0240147.
- Strother PK, Al-Hajri S, Traverse A (1996). New evidence for land plants from the lower Middle Ordovician of Saudi Arabia. DOI: 10.1130/0091-7613(1996)024<0055:neflpf>2.3.co;2.
