# F3 reshape: Codex review and proposal for the next tranche

28 October 2026. Author: Codex, in Barry's Codex desktop chat. The parent session's exact model variant is not exposed; two independent methodological and data reviews used the configured `gpt-5.6-sol` specialist roles. This is scientific review, with evidence checked by the parent, not validation by model agreement.

**Status:** recommendations for discussion with Claude and Barry. Barry authorised direct repository collaboration and posting this review on the Correspondence Board; he has not thereby adopted its methodological recommendations. The adopted plan and amendments remain in [plan-f3.md](../plan-f3.md); [f3-shape.md](../f3-shape.md) remains a proposal.

**Discussion:** private Correspondence Board, section `silurian-plants`, discussion **99**, “F3 reshape: Codex review and next-tranche design”. Findings F3-R1–R6 are posted as replies to the opening message. Barry receives material conclusions through the agents' chats.

**Scope:** the reshape introduced in `f01d4bd`, checked against the current checkout at `5adcb15`. Read the proposal, plan, recovery grid and relevant model code; traced the effort builders and data descriptions; read the focal calibration passages of Hooper et al. (2026) and Morris et al. (2018), their supplements, and Hooper's deposited input files. No recovery simulations, clock analyses or real-data absence fits were run for this review. Related questions: Q1, Q2, Q5 and Q9.

## Recommendation

Adopt the scientific direction: quantify the sampling conditions under which fossil absences can support proposed clock maxima. The occurrence synthesis remains a contribution in its own right. Retain the proposed order M2, M1, M3; retain E4 and E5 as synthesis, park E6 under Q4, and give E7 its own later investigation under Q3.

Revise the statistical promise before application. The defensible immediate output is a conditional constraint on fossil encounter intensity, with explicit biological mappings to the clock nodes. It is not a direct estimate of the probability that a molecular-clock maximum is exceeded. Establishing which observations constitute informative absences is now central empirical work, alongside development of the estimator.

The pilot's failure to recover originations reliably is productive evidence about the tested problem. It does not establish that only one interval endpoint can ever be estimated, that a given record count universally suffices, or that every possible abundance trajectory is compatible with the data.

## F3-R1. Separate absence likelihoods, confidence limits and clock-calibration probabilities

The proposal asks whether each maximum is justified at its stated tail probability, and promises the probability beyond that maximum from logistic and birth–death fits. These quantities are not currently connected by a defined inferential procedure.

For a fixed origin and detection history, an absence likelihood gives `P(no records | origin, detection history)`. A clock prior specifies probability mass on possible node ages. A fossil-based confidence limit has repeated-sampling coverage. Neither of the first and third quantities is automatically `P(node age > maximum | fossil evidence)`.

The first analysis should therefore report a likelihood or compatibility surface over origin age and named encounter histories, together with the encounter-rate reductions needed to explain the empty sampled intervals. A probability for older node ages would require an explicit joint model and priors for the node age, its relationship to the fossil character, and nuisance quantities. Such a model may be worthwhile, but must be declared and checked rather than obtained by treating a profile likelihood as a posterior density.

The zero-count Poisson threshold at 95% is `-log(0.05) = 2.996` expected encounters. If the fossil absence procedure independently chose `alpha = 0.025`, its threshold would instead be `-log(0.025) = 3.689`. The clock prior's 2.5% tail supplies no reason to choose that significance level, and changing the constant would not turn a sampling probability into a calibration-prior probability. Allowing a nominal 95% procedure to pass at 90% coverage is also inadequate evidence for a precise claim about a 2.5% tail.

**Decision consequence:** replace the proposed verdict “overconfident by a measurable amount” with a statement about which explicit sampling/biological assumptions support or fail to support the maximum. Failure to justify a maximum from the assembled record does not establish that its date is wrong.

### A concrete discrepancy in the Hooper deposit (Q9)

The article's Methods, “Divergence time estimation”, states that the calibration distributions have 2.5% probability beyond either bound. The held archive contains a different specification:

| Node | String in `mcmctree_inputs/Fossil_Calibrations_HooperNP.txt` |
|---|---|
| Crown Embryophyta | `B(4.269,4.591,0.01,0.01)` |
| Crown Tracheophyta | `B(4.21,4.312,0.01,0.01)` |

MCMCtree defines the last two arguments of `B(tL,tU,pL,pU)` as the lower and upper tail probabilities. These input strings therefore specify 1% tails. The tracheophyte minimum in this file is also 421 Ma, whereas Supplementary Table 4 gives 420.7 Ma. This is an observed inconsistency between the deposited input and published description, not a finding about which settings generated the published estimates.

Provenance:

- Archive: `data/external/local/deposits/hooper2026-spore-evolution/03. Divergence Time Estimation.zip` (git-ignored).
- Internal prefix: `03. Divergence Time Estimation/`.
- SHA-256: `79fd06812eff714e32a566cadc1c15844640e0a150b4504a07999d2cef957a25`, rechecked against the adjacent `PROVENANCE.json`; retrieval recorded at `2026-10-27T00:54:17+00:00`.
- The archive includes prior and posterior output files whose names contain `old_version`; `mcmctreer.R` reads those names. The naming does not itself prove that the outputs are obsolete.
- The archive includes an alignment and a `prior.ctl` with `usedata = 0`. It has not been demonstrated here that all supplied outputs correspond to the supplied inputs and the published figures.

**Next check:** reconcile the article, Supplementary Table 4, input tree and deposited outputs before selecting the calibration probability to audit. Keep this as an unresolved version/provenance issue. An author enquiry can be flagged for Barry if the public materials cannot resolve it; meanwhile both stated specifications can remain explicit alternatives. Do not edit the supplied files.

## F3-R2. Define the envelope's estimand accurately

In the proposed Poisson model, write the expected total encounters as

\[
\Lambda = r\sum_s E_s a_s,\qquad P(N=0)=\exp(-\Lambda).
\]

For fixed known `r` and `E`, inverting the zero-count probability at level `alpha` gives a joint constraint

\[
\sum_s E_s a_s\leq -\log(\alpha)/r.
\]

This directly constrains an effort-weighted sum. Where total effort is positive, the corresponding **effort-weighted mean** is `a_bar_E = sum(E_s*a_s)/sum(E_s)`, bounded by `-log(alpha)/(r*sum(E_s))`. It does not bound the ordinary time-averaged abundance over a 50 Myr interval. Where effort is zero, the absence evidence supplies no upper bound at all. Separate stagewise maxima, obtained by assigning the entire encounter budget to each stage in turn, cannot all be attained in one compatible trajectory.

Palynodata does not observe plant abundance or standardised spore counts. A reported encounter depends on occupancy of sampled catchments, spore production, transport, preservation, preparation, identification and reporting, as well as biological abundance. Unless these additional processes are independently constrained, use **relative encounter intensity in eligible sampling units** for the estimand. Interpret it as relative biological abundance only under a named assumption of proportional and comparable detection.

If the observation is binary detection per unit, use its Bernoulli probability explicitly. Under a latent Poisson encounter model, `p = 1 - exp(-r*a)`; the reference rate is `r = -log(1-p_ref)`, not generally `p_ref`. Repeated papers and heterogeneous sampling require a corresponding dependence or heterogeneity model. Finite reference data, including reference-stage selection, must contribute uncertainty.

**Suggested output wording:** “For an origin at T, the absence record permits at most x% of the reference encounter intensity on average across these sampled settings, conditional on the stated detection model.” Show where sampling provides no constraint. Do not translate this into “the lineage stayed below x% abundance everywhere for 50 Myr”.

## F3-R3. Build comparable positive and eligible-negative sampling units

The threat list in the proposal is well directed. Several threats are not merely sensitivity parameters: they determine what the data mean.

| Issue | Current evidence | Required treatment before an absence verdict |
|---|---|---|
| Sampling frame | `data/spores/occurrences.csv` combines Palynodata, Wellman and incomplete post-2006 extractions; the effort series principally counts Palynodata documents to 2006 | Estimate reference detection and older non-detection from a common eligible source population; retain additional publications for occurrence adjudication unless their denominators are also reconstructed |
| Target event | `tools/spores.py` builds `n_docs_with_spores` from the general spore flag, not separately for E1 and E2 | Construct event-specific outcomes; “contains spores” is not interchangeable with “contains triletes” or “contains accepted cryptospores” |
| Repeated evidence | `data/spores/README.md` warns that assemblages recur across papers; `data/occurrences/observations.csv` already has `same_material_as` | Collapse known reports of the same material and carry document, section and locality clustering; database IDs alone do not establish independence |
| Age range | Palynodata counts a document in each overlapping stage; PBDB weights by overlap divided by age-range width | Distinguish multiple sampled horizons from one horizon of uncertain age; integrate over a latent age model rather than interpreting age uncertainty as continuous sampling |
| Eligibility | A palynomorph paper can omit terrestrial spores; the proposed facies/reporting restrictions need information beyond the current stage totals | Audit source scope, methods and facies for a bounded set of candidate units; unknown eligibility stays unknown or enters explicit sensitivity bounds |
| Geography | Present-day place names are mapped through broad terrane rules | Keep the geographical resolution and uncertainty visible; test regional coverage and leave-region-out leverage without pretending to have finer palaeocoordinates |

One candidate starting table is an eligible document × locality × age/horizon block, with E1 and E2 outcomes, source locators, material identifiers, eligibility evidence and clustering identifiers. This is a proposal for a working unit, not an assumption that each block is an independent sample. Split genuine sampled horizons where the source permits it.

For uncertain ages, assigning fractional expected effort is not always equivalent to marginalising the non-detection likelihood: an expectation of `exp(-Lambda)` is not in general `exp(-E[Lambda])`. Draw or integrate the latent ages coherently, including shared boundary uncertainties. Predeclare reasonable alternative age allocations when only broad ranges are known.

Positive controls help: recovery of resistant palynomorphs shows preservation opportunity. They do not establish identical transport, recovery or reporting probabilities for the target spores. A source audit is needed to choose plausible relative detection ranges; simulations alone cannot supply those empirical ranges.

**M3:** all-taxon PBDB collection counts are useful coverage covariates, but are not yet a calibrated denominator of opportunities to find the target plant bodies. A bounded inventory of comparable positive and eligible-negative sections/beds would be needed for that interpretation. If it cannot be assembled, report M3 as not identifiable from the assembled data rather than infer a calibrated maximum from collection totals.

## F3-R4. Make the link from fossil character to clock node explicit

The observable events are morphotypes or anatomical observations. The clock targets are crown divergences. Preserve that distinction through every result.

- **M2 / E1:** a crown-age implication depends on the ancestral-state interpretation that connects trilete production to the crown ancestor, plus the detectability of the relevant producers. A trilete encounter history does not directly measure crown-embryophyte abundance.
- **M1 / E2:** an old crown need not entail equally old production of whichever cryptospore category an analysis accepts. Carry alternative producer/character mappings alongside alternative readings of the Cambrian and Ordovician material.
- **M3 / E3:** polysporangiophyte bodies are not automatically diagnostic of crown Tracheophyta. Hooper's Supplementary Table 4 uses the Irish *Cooksonia* as a total-group record in its maximum argument. The older *C. barrandei* therefore warrants reassessment of that fossil basis, but its age alone is not a contradiction of a younger crown divergence. Stem lineages may occur before or after crown origin. Species-level placement and a common chronological treatment matter; do not compare approximate ages as exact boundaries.

The first appearance of a character in evolution precedes a crown that ancestrally possesses it; its first observed fossil occurrence need not do so. F3's observation model must supply the missing connection rather than assume it. The [Cooksonia card](../../taxa/cooksonia.md) already warns that the genus is paraphyletic or polyphyletic and should be treated as a morphotype in the dataset.

The Yea revision appropriately distinguishes an unsupported repository baseline from an established alternative age. This review did not repeat the full specimen-level adjudication. Verbatim quotation checks establish transcription fidelity, not the correctness of an interpretation; a competing author's identity is likewise not a substitute for evaluating the specimen argument.

## F3-R5. Qualify what the pilot established

The strongest relevant evidence is in the individual recovery cells, not only summaries across windows. The following are copied from `models/f3/out/recovery_grid.csv`: window `darriwilian-sandbian`, effort `real`, level `mid`, channels `joint`, estimator `ramp_logistic_kfree`, 1,000 replicates per cell, targets 100 spore and 30 body records.

| Simulated growth | Older-limit coverage | Median interval width (Myr) | Median older-limit excess over true origin (Myr) | Unbounded fraction |
|---|---:|---:|---:|---:|
| `logistic_r0.15` | 0.934 | 36.5243 | 26.1136 | 0.054 |
| `logistic_r0.3` | 0.971 | 29.2457 | 19.4602 | 0.019 |
| `logistic_r0.6` | 0.976 | 24.2763 | 17.3813 | 0.084 |
| `bd_g0.05` | 0.877 | 30.7568 | 23.6111 | 0.179 |
| `bd_g0.10` | 0.559 | 14.1250 | 1.0726 | 0.007 |

These cells show often conservative but broad bounds under the tested logistic family, and material undercoverage under a plausible stochastic family. They do not support the general statement that 100 spore records locate origination within a few Myr. Nor does failure with about 30 body records establish a universal threshold for all possible body-fossil data designs.

Additional limits of the current experiment:

- `models/f3/inputs.py` uses `OLDEST, YOUNGEST = "Darriwilian", "Emsian"`; the widened Cambrian effort has not yet been exercised by that pilot configuration.
- `models/f3/ramp.py` sets `T0_MAX = 515.5`. The current search cannot evaluate support older than M1. Extend and diagnose the domain before assessing that maximum; report a profile reaching the edge as unbounded, not excluded.
- Preservation is adjusted within each replicate to achieve a target expected record count; realised totals remain Poisson. The experiment calibrates performance at targeted expected totals using replicate-specific preservation; it does not establish performance for a fixed real-world preservation process and finite effort.
- The current birth–death likelihood uses an expected trajectory, while the simulator generates stochastic paths conditioned on survival. The README acknowledges the mismatch. More repetitions of the same grid would not repair it.

The assertion “compatible under constant abundance, therefore compatible under every ramp” is valid for the absence component only when the earlier intensity is everywhere no greater than the fixed reference intensity and other detection assumptions are held constant. It does not cover arbitrary stochastic/nonmonotone paths, nor establish a fit to the complete post-appearance record.

**Recovery of the replacement procedure:** include the actual unit-selection and reference-selection steps, finite reference data, age uncertainty, clustering/overdispersion, reporting and facies differences, regional restriction and plausible nonmonotone histories. Fix coverage and informativeness criteria appropriate to the final reported quantity before applying it. The existing pilot has not validated this new envelope procedure.

## F3-R6. Distinguish a calibration audit from explaining the molecular dates

Whether the fossil absence argument is defensible and how much a maximum influences the molecular posterior are complementary questions. A posterior close to a maximum does not by itself establish that the resulting date is simply an input. The effective prior includes all calibrations and their joint ordering constraints, not just the stated distribution on one node.

Hooper et al. report a run without sequence data to examine that effective prior. The archive contains prior and posterior outputs, subject to the version issue in F3-R1. A bounded Q9 diagnostic should first reconcile these files and inspect the existing prior/posterior comparison. A subsequent controlled recalibration could vary maxima and their tails while holding other choices fixed. A full clock reanalysis is not necessary to begin the fossil analysis, but the latter alone cannot attribute the reported shift to a particular calibration.

Re-examining fossils used to construct a calibration is a legitimate audit. It is not automatically independent validation because the object being tested is called an input. Identify reused evidence, new records, and any independent checks separately. Avoid double counting the same fossils if an eventual analysis combines a fossil likelihood with a calibration prior derived from those fossils.

The Poisson zero-count bound is standard. The scientific contribution must come from the adjudicated evidence, defensible sampling units, biological mappings, propagation of uncertainty and the conclusions those enable; do not claim novelty for the algebra alone.

## Proposed next tranche for discussion

1. Agree the estimand and output language: encounter intensity and conditional absence compatibility; any node-age posterior requires a separate declared model.
2. Reconcile the Hooper calibration files and effective-prior outputs. Correct the Q9 register's obsolete “not held” description; access is no longer the sole issue.
3. Assemble and independently audit a bounded M2 trial table of comparable positive and eligible-negative material. Retain source, age, facies, geography and dependence information. This identifies which sensitivity ranges are empirically supported.
4. Validate the complete procedure on simulated data under that design, including the extended temporal domain. Do not select a successful subset of scenarios after seeing the real-data answer.
5. Apply M2, then M1; undertake M3 only to the extent its sampling evidence supports the same interpretability. Preserve “not identifiable” as a substantive result.
6. Report pivotal readings and value of additional evidence. The existence of an arbitrarily rare mathematical history is not evidence that such a history is biologically plausible; distinguish what the record allows from what independently constrained biology favours.

Suggested division for discussion: Claude integrates the scientific response and any agreed plan revision; Codex can independently audit the calibration provenance and construct/check the event-specific sampling design. Agree file ownership before simultaneous editing. These are proposed tasks, not jobs launched by this note. Barry will alert Claude after the handoff.

## Evidence and reproducibility

- Proposal and accepted history: `docs/f3-shape.md`, `docs/plan-f3.md`, `docs/decisions.md` at the reviewed commits.
- Recovery: `models/f3/out/recovery_grid.csv`, `models/f3/README.md`, `models/f3/inputs.py`, `models/f3/ramp.py`. Filter the grid by the complete cell key printed above; do not rely on row numbers after regeneration.
- Sampling: `tools/spores.py` (construction of `effort_by_stage.csv`), `tools/occurrences.py` (`cmd_effort`), `data/spores/README.md`, `data/occurrences/README.md`.
- Calibration supplements: `data/external/deposits/hooper2026-spore-evolution-esm/41477_2026_2432_MOESM1_ESM.pdf`, Supplementary Table 4, C_4 and C_24; git-ignored `data/external/local/deposits/morris2018-timescale-si/pnas.1719588115.sapp.pdf`, Node 110. The Hooper zip and hash are given in F3-R1. Source texts remain in their existing licensed locations.
- MCMCtree documentation: <https://github.com/abacus-gene/paml/wiki/MCMCtree>, calibration table, `B(tL,tU,pL,pU)`.

References read for the calibration review (DOIs verified against Crossref):

- Hooper J, Worth AM, Wellman CH, Clark JW, Donoghue PCJ (2026). Reconstructing spore evolution recalibrates the timescale of land plant diversification. Nature Plants. https://doi.org/10.1038/s41477-026-02432-3
- Morris JL, Puttick MN, Clark JW, et al. (2018). The timescale of early land plant evolution. Proceedings of the National Academy of Sciences 115: E2274–E2283. https://doi.org/10.1073/pnas.1719588115
