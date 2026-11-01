# Loop 2 close: independent affinity and biological-integration review

1 November 2026. Codex. Reviewed the sprint-2 package at `cb70b36aff22bd2c387196fc223cd62dedb39925`; findings below concern that reviewed version. The integrator subsequently assigned the bounded corrections in `data/units/loop2/m1-m3/` to this reviewer; their disposition is recorded below. No occurrence reading, frozen analysis, receipt or primary source file was changed.

**Verdict:** the three-source review supports excluding the assessed Cambrian forms from E2 under main, and it finds no new absence design for M1 or M3. The package needs corrections before closure: withdraw the unsupported circularity claim; distinguish evidence for precursor characters from acceptance as embryophytes; state the age and node implications explicitly; and integrate the existing trait pilot. These are interpretive and synthesis corrections, not grounds for another model run.

## Sources checked

Read the relevant text of the held full PDFs: Strother (2016), *Systematics and evolutionary significance of some new cryptospores from the Cambrian of eastern Tennessee, USA*, printed pp.28–33, 39–41; Taylor & Strother (2024), *Ultrastructure of Cambrian cryptospores and the early evolution of the plant spore wall*, pp.90–93, 97–103; Wang et al. (2022), *A palynological assemblage from the Cambrian (Series 2, Stage 4) of Shandong Province, China*, article 104645, pp.2, 6; Vecoli et al. (2017), *Middle Ordovician cryptospores from the Saq-Hanadir transitional beds in the QSIM-801 well, Saudi Arabia*, p.320. Taylor & Strother p.103 was also rendered and visually checked. Source files are respectively `strother2016_macbook20261030.pdf`, `taylor2024_firststudy.pdf`, `wang2022_macbook20261030.pdf` and `vecoli2017.pdf`, under `library/closed/`.

Compared these sources with the E2 addendum, the new M1 ledger and requests, existing occurrence interpretations and sample outcomes, the adopted Loop 2 plan, the manuscript, `docs/pilot-traits.md`, `models/pilot-asr/README.md` and the previous M3 denominator audit. This is a bounded primary-source and integration review, not an exhaustive literature search or a new anatomical adjudication.

## 1. Main exclusion stands; the stronger wording does not

Strother (2016, p.32) places the taxa under Charophyta. His p.29 discussion explicitly avoids claiming a particular ancestral lineage, while describing some wall structures as apparently homologous to liverwort walls and interpreting the producers as aeroterrestrial algae. The systematic assignment and developmental argument support main exclusion; they do not demonstrate that all shared characters lack relevance to embryophyte evolution.

Taylor & Strother (2024, pp.90–91, 100, 103) interpret the forms as pre-embryophytic, with spore-wall development preceding embryophyte sporangia. Their conclusion favours meiotic stages of terrestrial charophytic algae and likely formation without a sporangium. It also recognises developmental and wall similarities to extant embryophytes. Material identity matters: the unnamed lamellated dyad/monad compared with *Riccia* on p.103 is Rogersville material (p.97, specimen Rog 2ox-1-1), not direct evidence that the Stage 4 Rome packets were liverwort products. The Rome TEM packets include R1O and R2A (Figs 8–10). Their endogenous wall construction supports precursor-character interpretation without establishing E2.

Wang et al. (2022, p.6) prefer an ancestral streptophyte-algal interpretation but describe the investigation as still premature and direct embryophyte affinity as unlikely. This is not a definitive exclusion of every alternative. Their cryptospore definition is explicitly broad and does not itself assert embryophyte affinity.

**Required replacement:** none of these three sources explicitly accepts the assessed Stage 4 producers as embryophytes. Their morphology, ultrastructure and developmental interpretation support an evolutionary precursor account, but do not independently establish E2 under main. An inclusive E2 assignment remains a declared alternative assumption requiring its record-specific rationale. Do not write that there is no affinity-relevant evidence, that all describing sources conclusively reject affinity, or that a morphological label alone establishes E2. Limit the claim to the three assessed sources/materials. The historical inclusive assignments in `data/units/sprint2/m1_admission.csv` and `data/occurrences/interpretations.csv` are not silently revoked by this review.

## 2. Withdraw the circularity accusation

Taylor & Strother (2024, p.90) invoke molecular dates to motivate examining an older spore record, then explicitly favour a pre-embryophytic interpretation. That passage does not establish that the clock prediction is the principal reason for treating the fossils as embryophytic. The sprint-2 README and manuscript currently make that unsupported causal claim.

Delete it. A valid methodological statement is narrower: affinity used in a test of a clock maximum must be justified independently of the clock date. That requirement does not show that these authors, or the project's historical inclusive reading, committed circular inference.

## 3. Age support and the maximum answer different questions

Strother's p.33 supplies the Stage 4 assignment; 514.5–506.5 Ma is the project's conversion using `data/timescale.csv` (ICS v2024/12), not numerical dating reported there. Wang's own age wording is approximately 514–509 Ma. The new ledger should retain both source age wording and the modern stage conversion separately. The existing Tennessee inventory also preserves the broader uncertainty in Strother's Fig.1 caption; this should not be erased by an unqualified precise age claim.

Every age in 514.5–506.5 Ma is younger than 515.5 Ma. Even if a Stage 4 record is accepted as E2, it does not itself falsify the M1 maximum. Nor does an embryophyte-related spore establish crown membership. It changes the accepted occurrence support and the biological/calibration discussion; direct challenge to the maximum requires the appropriate event/node link and evidence on its older side. For an absence argument, productive, completely reported pre-515.5 Ma material and an admissible reference/encounter design remain missing. A stage boundary is an age-support endpoint, not a measured first appearance.

## 4. Argentine 7999: keep the actual reading distinction

Vecoli et al. (2017, p.320) identify small, thin-walled Argentine tetrads as incorrectly named *Tetrahedraletes medinensis* in Rubinstein et al. (2010), but still recognise tetrads and monads in the assemblage. This is a taxonomic correction, not a new embryophyte-affinity demonstration or a conversion to absence. Its Dapingian age makes it irrelevant to direct pre-515.5 Ma exposure; that fact alone cannot settle its E2 status.

Explicitly retain the inspected sample-level disposition: `RIOCAP-7999` is E2 unresolved under main and detected under inclusive/outlier (`data/units/outcomes.csv`). The correction does not remove all named-reading acceptance of its cryptospores, reconstruct other sample outcomes or supply a complete denominator. The new note can close this particular lead as changing no current outcome, but should give that reasoning rather than age alone.

## 5. The missing trait-pilot synthesis is a substantive acceptance gap

The reviewed manuscript contains the maximum/node labels but omits the existing specimen, ancestral-state and persistence synthesis required by `docs/sprints-loop2.md`, section 3. Add a compact mapping table and explanatory text, with links in the claim ledger and distributable-data manifest:

- **M1:** E2 affinity is reading-dependent; the pilot's crown-state mapping is contested and cryptospore persistence has not been assessed. Do not infer absence of E2 from X26's modal monad state alone: its combined trilete/inaperturate-monad category does not separate the morphology accepted by the E2 addendum. The aperture and dispersal-unit marginals need their stated separate treatment. Shared walls or a stem precursor do not date crown Embryophyta.
- **M2:** the sampled data constrain trilete-producer encounter or a within-sample recovered-spore ratio. A crown implication additionally assumes a trilete crown state, persistence and the stated abundance/delivery history. The existing Mk analyses support persistence conditionally on their trees and models; their trees date the embryophyte crown at 508 Ma, not Hooper's recalibrated 457–450 Ma. Fixed-rate extensions to older origins are sensitivity scenarios. Retention probabilities must not be multiplied into F3 coverage or a rejection probability. Separately modelled character marginals do not supply a joint ancestral phenotype.
- **M3:** the missing searched-material denominator is only one gap. The pilot records that anatomy attributed to the Homerian calibration material is transferred from younger *C. pertoni*, and that placement is contested. The older *C. barrandei* E3 occurrence does not by itself contradict a crown-tracheophyte maximum: stem/total-group occurrence and crown membership are distinct.

These findings already exist in the accepted pilot and source audits. No new ASR run is needed to meet the synthesis requirement. Their omission makes the reviewed conclusion that M2 is defensible against an abundant crown flora stronger than the manuscript's demonstrated implication chain.

## 6. M3 non-admission and request scope

The current M3 non-admission agrees with the existing source-specific audit: Irish fossil-free mudstone is genuine qualitative evidence, but no enumerated comparable search roster follows; historical Czech axes are selected specimens, not search trials. The request is a useful draft, but should explicitly request all eligible searched units, positive/negative/unresolved target outcomes, age evidence, selection boundaries and comparable younger reference units, with links among beds, blocks, visits and specimens. Those fields distinguish an admissible opportunity ledger from a list of failed searches. Preserve lithology and protocol differences; a returned denominator alone would not establish exchangeable detection.

Use the bounded claim that no assessed held-source frame admits the requested design. The manuscript's unrestricted assertion that M1/M3 are untestable from the published record exceeds this audit's scope. Sending requests remains Barry's decision and is not a condition for closing this tranche.

## Closure criterion from this review

The scientific review can close once the integrator corrects the M1 wording/age provenance, explicitly retains the Argentine named readings, and adds the existing biological implication chain to the manuscript and claim/data tables. Main E2 exclusion and both M1/M3 non-admissions remain unchanged. No missing external reply or additional computation is required by these findings.

## Bounded corrections completed

Codex corrected `data/units/loop2/m1-m3/m1_affinity.csv`, `README.md` and `requests.md` after the integrator assigned those files. The ledger retains the original source quotations and adds material-specific locators, separates Stage 4 Rome evidence from younger Rogersville comparisons, and distinguishes source ages from the ICS conversion. The README removes the circularity accusation, retains inclusive acceptance as an explicit alternative, explains the younger-than-maximum occurrence limit, and records Argentine 7999's unchanged main/inclusive/outlier outcomes. Both requests now specify complete rosters, selection boundaries, same-material target and non-target ascertainment, effort, age evidence, specimen joins and comparable reference candidates. Nothing was sent.

The CSV was parsed as three source rows with its original eight-column schema; required source quotations, the named-reading distinction and the bounded age claims were checked. No scientific reanalysis was performed. Manuscript, claim-ledger and programme-level integration remain with the parent reviewer and were not edited or re-reviewed in this bounded implementation. This resolves the local ledger/README/request findings; it does not certify the final integrated manuscript.

## Final integration check

The integrator subsequently requested a bounded read of the revised `manuscript/manuscript.qmd`, `manuscript/mapping.csv` and `manuscript/claims.csv`. **Pass for the source and biological issues in this audit.** The manuscript now separates Stage 4 occurrence support from the older M1 maximum, retains the named affinity alternatives, and distinguishes direct *C. barrandei* observations from the conditional Irish sporangial interpretation and younger anatomical transfer. Its biological synthesis keeps X21/X26 marginals separate, states the upstream 508 Ma tree conditioning, treats fixed-rate extensions as scenarios, and does not multiply retention into F3 coverage. Crown interpretation remains conditional on the missing or model-dependent links.

The reported 77 departures among 3,382 trilete starts, conditional persistence 0.977 and Monte Carlo standard error 0.0026 agree with `diagnostics_summary_ext_b10000_s100.csv`. The stated retention medians and intervals at 459.1 and 515.5 Ma agree with the extant-tree rows of `retention_chains.csv`. These were table checks, not reruns. A minor wording recommendation was sent to the integrator: call these aperture-state retention scenarios rather than production-persistence scenarios, because X21 models aperture state and its production interpretation uses the separately stated biological mapping.

No material source or biological blocker remains in these three revised manuscript artefacts. This scoped pass does not cover the statistical derivation, package rendering or complete manifest verification, which belong to the other reviews and the integrator. No new primary-source campaign or scientific reanalysis was undertaken.
