# Sampling-unit evidence: bounded M2 interface pilot

Status: **pilot only, 29 October 2026**. These tables implement the two-table interface agreed in
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

Check with `python3 tools/units.py check` (standard library only). The check rejects duplicate
material, missing event/reading combinations, broken source/interpretation links, reversed stage
ranges, and loss of a detection in a wider reading. It also enforces this release's `pilot_only`
status and absence of an adopted binary reporting rule. It is an integrity check, not source
verification or scientific validation.

## What the pilot contains

- **Samphire Marsh 1:** three distinct core intervals. Core 4 has an explicit E1 non-detection
  quoted by Strother & Foster (2021) from Balme (1961); the original report remains unread, so
  eligibility is unknown. Cores 6 and 8 are separate 2021 observations outside Palynodata's
  to-2006 frame. Their E2 affinity is unresolved in the main reading and counted in the inclusive
  reading. All three share a borehole cluster.
- **Hanadir TAYM-4:** three labelled samples, with multiple slides collapsed within each sample.
  E2 is detected. E1 is not reported. The 2015 study expands the 1996 material represented by
  Palynodata 18701, but the exact mapping of these sample labels to the original report is
  provisional until that report is read. Later re-examinations never create new trials.
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

In the main reading, E1 has 3 detections, 1 explicit non-detection, 9 not-reported outcomes and
2 unresolved identifications. E2 has 6 detections, 5 not-reported outcomes and 4 unresolved
identifications. These are counts of the selected evidence, not detection-rate estimates. The sole
explicit E1 non-detection has unknown eligibility and secondary-source status: **this pilot has
no primary-verified eligible older E1 negative on which to base an M2 exclusion.**

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
and the absence of implicit negatives. The data have not been adjudicated by Claude or Barry.

The repository-wide DOI command checked 719 distinct strings and flagged 15 entries, all in the
unchanged `docs/barry-to-action.md`: 14 include a captured closing Markdown backtick and one
lacks citation context. This is a pre-existing scanner/input-format issue, left for a separate
fix. The two newly acquired papers were independently verified against Crossref by DOI, title
and first author. The unit integrity check and five temporary malformed-input checks passed.

The next evidence tranche should recover complete sample inventories from a small set of
Palynodata studies chosen by age, geography and reporting scope, before inspecting their E1
outcomes. Priorities are Balme's original core-4 account, the original Hanadir sample mapping,
and the complete Paraguay sample log. Grahn's chitinozoan survey also demonstrates why a paper
without an indexed spore record is not automatically an extra negative spore trial.

New references, identities verified against Crossref on 29 October 2026:

- Steemans P, Pereira E (2002). Llandovery miospore biostratigraphy and stratigraphic evolution of the Paraná Basin, Paraguay – Palaeogeographic implications. DOI: 10.2113/173.5.407.
- Grahn Y, Pereira E, Bergamaschi S (2000). Silurian and Lower Devonian chitinozoan biostratigraphy of the Paraná Basin in Brazil and Paraguay. DOI: 10.2113/0240147.
