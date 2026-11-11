---
document: agent-facing paper
study: F3, fossil maxima behind land-plant molecular clocks
status: internal draft; Loop 3 closed 2026-11-07; follow-up review implemented 2026-11-08 (docs/audits/2026-11-08-review2-handoff.md); article reconstructed to Proc B structure 2026-11-10 to 2026-11-11 (manuscript/reconstruction/README.md); release and submission are Barry's decision
human_paper: manuscript/text/main.md (+ supplement.md, brief.md)
claims_ledger: manuscript/claims.csv (single source for all renderings; checked by tools/claims.py)
governing_docs: [docs/charter.md, docs/decisions.md, docs/plan-f3.md, docs/f3-shape.md, docs/loop3-design.md, docs/loop3-results.md]
authority: Barry W. Brook decides public release, submission and any correspondence outside Claude and Codex
updated: 2026-11-11
---

# F3 for agents: what this study established, how to verify it, and how not to break it

This is the version of the paper written for an agent arriving cold. The human paper argues; this one
indexes. It says what is claimed, where each number lives, which commands regenerate it, what has been
superseded, and where the open edges are. When this file and a primary artefact disagree, the
artefact wins and this file is wrong: fix it in the same commit.

## 1. Read order and trust

1. This file, then `manuscript/estimands.md`, which says what each analysis bounds and which
   phrasings are not allowed, then `manuscript/claims.csv`, the single claims ledger behind every
   rendering of this study (C01–C53). Each row gives the claim, its value, its status, its basis, its evidence
   files, the commit at which that evidence was verified, the command that reproduces it, its limit
   and, if superseded, its replacement. Quote a claim only with its limit.
2. `manuscript/text/main.md` for the argument; `supplement.md` for the machinery. The article follows
   the Proceedings B structure: Abstract, Keywords, Introduction, Material and methods (a)–(h), Results
   (a)–(h) with finding-led headings, Discussion (its "Conditions" paragraph states the assumptions behind
   the limits), Conclusion, then Ethics, Data accessibility, Declaration of AI use, Authors' contributions,
   Conflict of interest, Funding, References and Figure legends. The old numbered sections (§2 Evidence,
   §3.1–3.5, §4.1–4.4, Methods in brief) and old Tables 2–5 no longer exist there; their content lives in
   the supplement (S-numbered sections and tables) or in the Discussion prose. The reconstruction record
   (steps 1a–4, Codex reviews, the adopted main message) is indexed in `manuscript/reconstruction/README.md`.
3. `docs/decisions.md` (newest first) for what was settled, by whom, and why.
4. `docs/questions.md` for the programme's open questions (Q1–Q10). This study answers part of Q1.

`status` is one of *supported* (verified by a second agent against its evidence), *provisional*
(awaiting that check), *refuted* or *superseded*. `basis` says what kind of result it is, from
strongest to weakest: *source extraction* and *frozen qualified result*; *reviewed inventory*;
*conditional endpoint inference*; *declared* or *retrospective sensitivity*; *exploratory
model-conditional calculation*; *procedure check*. A procedure check (for example, simulation
coverage) tests the method, never the fossils.

The article, supplement, brief and this guide all cite the ledger. The article and supplement use Proc B numbered citations (`manuscript/csl/proceedings-of-the-royal-society-b.csl`); the brief keeps author-date. In the Markdown, `[428.8]{.C27 .V012}`
binds a quoted number to C27 (invisible when rendered), and `tools/claims.py check` fails if the number
no longer equals one of C27's values at the precision shown, if a cited claim is superseded, or if a
ledger value cannot be found in its evidence. Change a result in the ledger first; the check then lists
every sentence that must follow.

## 2. The answer, as claims

**Main message** (adopted by Barry, 10 November 2026; `manuscript/reconstruction/1c-main-message.md`):
"Older dates for living land plants fit the fossil record if early plants were found several times less
often, or recognisable features evolved later." It is a statement of compatibility under stated
conditions: the quantity behind "several times" is the vascular-body recording contrast (C48); the
Libyan limit (C24) is a separate, local constraint on delivered spore input. The record neither
supports nor rejects an older ancestor.

- **M1 (515.5 Ma, crown Embryophyta).** Placed below the oldest possible cryptospores (base of the
  *Olenellus* Biozone, [515.5]{.C46} Ma), with a qualitative preservation-control absence argument from older
  marine-palynomorph-only sequences (C46). No assessed source supplies an enumerated frame to quantify it
  (C16). The Stage 4 material ([514.5–506.5]{.C16} Ma) lies below the maximum by design and is not accepted as
  embryophyte by the three assessed sources (C15).
- **M2 (459.1 Ma, crown Embryophyta).** The value is the GTS2012 Sandbian base plus its uncertainty,
  [458.4 + 0.7 = 459.1]{.C42} Ma, keyed to a possible trilete at Borenshult-1 48.2 m; definite triletes start at
  43.1 m, also Sandbian, so the value does not depend on the doubtful specimen (C42, C43). Borenshult
  cannot exclude reference-level intensity under the examined screen (C44). One qualified comparison,
  Murzuq Basin (C01–C06, C24), constrains sustained local encounter, chiefly through [18]{.C45} later-Ordovician
  cuttings; only [10]{.C45} Darriwilian cuttings reach before 459.1 Ma (C45). It constrains the product of delivery and producer intensity, not either alone: ρ·f ≈ [0.091]{.C24} for the
  constant class H0c, [0.092–0.184]{.C24} for the exposure-weighted class H0 (C04 gives the ρ = 1 readouts).
  Both assume cutting outcomes independent given a shared well effect; unqualified inverse-block-size
  weighting by well and formation gives a comparison contour of [0.393]{.C51 .V103} (C51).
  QSIM-801 is exploratory only (C11–C14, C23); C12 is a minimum trilete:cryptospore ratio, not a share.
- **M3 (431.2 Ma, crown Tracheophyta).** No absence design (C17). Positive-record endpoints for B2:
  [428.84]{.C27 .V013} / [428.88]{.C27 .V014} / [428.45]{.C27 .V015} / [431.63]{.C27 .V016} Ma / none within domain, for constant, PBDB-density,
  plant-excluded-density, 25 Myr decline and 10 Myr decline histories (C27). Recovery reduced tenfold
  before [426.7]{.C32} Ma gives [448.10]{.C32} Ma; a hundredfold gives no bound (C32, retrospective). Region–stage and
  curated-only units give [432.38]{.C30} and [434.05]{.C30} Ma under constant intensity (C30), across 431.2 Ma. The anchor
  of 431.2 Ma omits the older *C. barrandei*. On the current scale the stage-base-plus-uncertainty rule gives [431.9]{.C47} Ma (Homerian) and [434.1]{.C47} Ma (Sheinwoodian), [2.2]{.C47} Myr apart; [2.9]{.C47} Myr is the difference from the published GTS2012 value and mixes scales (C47).
  Halving recording before 426.7 Ma (flat baseline, primary units) gives a bound of [431.0]{.C53 .V108} Ma, still younger
  than the maximum (C53). The tested shared-boundary scenarios move the constant bound within [427.31]{.C50 .V098}–[430.42]{.C50 .V099} Ma, younger than the maximum under
  all three comparisons (C50). Lineage ages of 444–452 Ma would need earlier/later intensity [0.124]{.C48 .V100}–[0.085]{.C48 .V101} (primary units,
  zero delay; C48). No admissible age allocation rescues the 10 Myr decline; some rescue the 25 Myr
  decline when cutoff-straddling units are counted (C49). Removing Yea moves the bound [−1.67]{.C52 .V102} Myr (C52).
- **Land-plant bodies (B0).** Canonical B0 includes the Katian Oman sporangial fragments as one unit,
  oldest possible age [452.8]{.C40 .V031} Ma: bounds [455.19]{.C40 .V032}–[456.62]{.C40 .V033} Ma under constant and effort-like histories and
  [465.21]{.C40 .V034} Ma under decline25, and every history fails the shape diagnostic under every admissible age
  allocation (C40, C41, C49). Excluding them (C28) gives
  [434.51–437.16]{.C28} Ma. Neither is a lag, a delay or a date of body recoverability; 458.2 Ma is a fossil minimum.
  The canonical inventory and its exclusion variant now rebuild through `build_reviewed.py` and
  `analysis.py`, with explicit body-membership tests.
- **Synthesis.** An older, sparsely recorded flora is allowed, not required. The record cannot test the
  rate of recorded, identifiable occurrences before its oldest find, and no result ranks the clocks.

- **Supporting details carried here and in the supplement.** A reference-level Murzuq interval beginning
  at 459.1 Ma reaches back no further than [462.6]{.C03}, [464.1]{.C03} and [467.1]{.C03} Ma at ρ = 1,
  0.5 and 0.25, and is unbounded at ρ = 0.1 (C03); intervals at a tenth or a hundredth of reference
  intensity are unbounded within the domain[]{.C05}. The body record is geographically concentrated:
  [16]{.C26} B2 units have age support older than 419.62 Ma, from seven regions (C26); Laurentia
  supplies [29 of 78]{.C37} land-plant units, and of [34]{.C37} wholly Silurian units Laurentia holds
  [11]{.C37} and peri-Gondwanan Europe [8]{.C37} (C37).

## 3. Vocabulary that the files use

| Term | Meaning |
|---|---|
| M1, M2, M3 | The 515.5, 459.1 and 431.2 Ma maxima |
| E1–E5 | Event channels: trilete spores; cryptospores accepted as embryophytic; polysporangiate bodies; tracheids; crown vascular-plant members |
| B0, B1, B2 | Body categories: any land-plant body (declared: any accepted macro- or mesofossil; the canonical inventory includes the Katian Oman fragments as one unit, while excluding them is the former-inventory sensitivity, C28, C40); polysporangiophyte; crown vascular-plant member (lycophyte line or euphyllophyte) |
| main / inclusive / outlier | Named readings of disputed records; every analysis declares one (`supplement.md` §S1) |
| unit | Locality–age proxy: PBDB formation + 0.1° coordinates + identical age support, or a curated site |
| possible / guaranteed | Units counted at oldest possible age / only those certainly older than the cutoff |
| cutoff | Younger end of the window; primary is end-Emsian, 393.47 Ma |
| domain | 469.4 Ma, where the held PBDB effort series ends; "none" means no bound inside it |
| history | Fixed relative recovery w(t): `flat`, `pbdb_all`, `pbdb_plant_excluded`, `decline25`, `decline10`, `pbdb_excluded_decline10` |
| ρ, f | Murzuq older/reference delivery ratio (declared, not estimated); older producer intensity as a fraction of reference |
| H0c, H0, H0m, H1 | Murzuq history classes: constant; exposure-weighted; modified; higher ceiling |
| qualified | Passed the simulation-calibrated 0.93 coverage floor on the declared grid (`docs/f3-shape.md`) |

The endpoint formula is U(T) = U(A)·0.05^(−1/n), where U(a) = ∫_c^a w(s) ds. With constant w it reduces
to the Strauss–Sadler/Marshall interval. Code: `models/f3/loop3/endpoint.py`.

## 4. Provenance map

| Result | Inputs | Code | Output | Claims |
|---|---|---|---|---|
| Murzuq frame | `data/units/libya_*.csv` (transcribed from Abuhmida 2013; the thesis is local-only) | `models/f3/` engine, Loop 1 | `models/f3/out/m2_results.csv`, `out/qual/` (frozen) | C01–C06, C24 |
| Murzuq sensitivities | as above | `models/f3/loop2/contamination.py` | `models/f3/loop2/out/` (frozen) | C07–C10 |
| QSIM floor | `data/units/loop2/replication/qsim801_vecoli2017_table1.csv` | `models/f3/loop2/replication/` | `.../out/qsim_share_bounds.csv` | C11–C14, C23 |
| Cambrian affinity | sources in `data/units/loop2/m1-m3/m1_affinity.csv` | none (adjudication) | same | C15–C16 |
| Persistence pilot | Hooper et al. deposits (fetched, hash-checked) | `models/pilot-asr/` (R, renv) | `models/pilot-asr/out/` | C18–C20 |
| Body record | PBDB extract and `data/macro/*` (names, adjudications, older screen) | `models/f3/loop3/build_reviewed.py`, `analysis.py` | `models/f3/loop3/out/reviewed_bounds.csv`, `primary_unit_membership.csv`, `shape_diagnostics.csv`, `age_sensitivity.csv`, `delay_sensitivity.csv` | C25–C31, C33 |
| Suppression grid | as above | `suppression_sensitivity.py` | `suppression_sensitivity.csv` | C32, C53 |
| Canonical B0 and Oman exclusion | as above; `body_membership.csv` admits S-w22-K12 | `build_reviewed.py` and `analysis.py` | `reviewed_bounds.csv`, `shape_diagnostics.csv` (`variant=primary` or `without_oman_fragments`) | C28, C40–C41 |
| Borenshult readings | `data/units/borenshult_review/` | `models/f3/borenshult_review.py` | `models/f3/out/borenshult_review/` | C42–C44 |
| Simulations | unit counts from above | `simulation.py` | `simulation_results.csv` | C34 |
| Paper figures | the outputs above, `data/spores/first_appearances.csv`, `data/timescale.csv` | `manuscript/figures.py`, which calls `manuscript/figures_main.py` for the four main figures | `manuscript/figures/`, hashes in `figures.json` | — |
| Supplement tables S3–S11 | `models/f3/loop3/out/` | `manuscript/tables.py` (rewrites marked blocks in `supplement.md`) | `manuscript/text/supplement.md` | — |
| Bibliography | `references/dois.txt`, `references/manual.yaml` | `tools/refs.py build` (Crossref CSL-JSON) | `references/refs.yaml` | — |

The primary row of `reviewed_bounds.csv` is: `reading=main`, `units=locality_age`, `variant=primary`,
`excluded_region` empty, `cutoff=Emsian`. Most misquotations come from leaving out one of these filters.

## 5. Traps: superseded results and known misreadings

Do not reintroduce any of these. Each was caught in review; the record is in `supplement.md` §S7 and
`docs/audits/`.

1. **Loop 3 pilot numbers (C35, superseded by C27).** The logistic-ramp limits [452.6 / 454.1 / 438.0]{.C35 .superseded} Ma, "favours the young
   clock" and "a measured 15–25 Myr lag" are retired (`docs/loop3-pilot.md` is marked provisional).
   The defects: stage collection totals used as per-Myr density, which counts duration twice; medians
   of imputed limits presented as 95% limits; PBDB localities merged by country, genus and age
   overlap; collections treated as independent beds.
2. **"Murzuq excludes abundant producers" (C36, superseded by C24).** It excludes abundant, *well-delivered* producers. Only ρ·f
   is constrained (C24).
3. **QSIM as a second qualified test.** It is not; search coverage and independence are undocumented.
4. **Age-allocation quantiles as confidence bounds** (Table S8). They are descriptive.
5. **The suppression grid as a nominal 95% result, a fitted reduction or a threshold.** The tenfold case
   is one illustrative scenario, chosen after seeing the shape diagnostics.
6. **Any spore-to-body lag or delay, in either direction.** "About 20 Myr after" and "almost at once" are
   both wrong: the bounds are model-conditioned endpoints and 458.2 Ma is a fossil minimum (C28, C40). The record estimates no delay for B2; C33's 15–23 Myr are minimum
   assumed offsets at the endpoint bound.
7. **Agreement between Claude and Codex as validation.** The two systems review each other; neither is
   independent ground truth.
8. **Clocks as validation targets.** The oldest *Cooksonia* and Ludlow *Zosterophyllum* are themselves
   clock calibrations. Agreement tests whether a maximum is reasonable, not whether a clock posterior
   is right.
9. **The Yea *Baragwanathia* age.** It is unresolved, Gorstian to Emsian, and carried as the full range.
   Do not fix it to either end.
10. **Wells.** The Murzuq frame has five wells; the 28 older cuttings come from three of them.
11. **Figure numbering.** The main figures are `fig1_dispute`, `fig2_bound`, `fig3_murzuq` and
    `fig4_requirements` (from `figures_main.py`); the graphical abstract, also the brief's figure, is
    `graphical_abstract` (from `figures_abstract.py`); the mapping matrix is `figS7_mapping`. The names
    `fig1_problem`, `fig2_evidence`, `fig3_bodies`, `fig4_frontier` and `figB1_brief` are retired, and older audits and
    supplement text may still use them.
12. **GTS2012 against ICS v2024/12.** Literature Early Devonian boundaries differ from ours by up to
    3 Myr; `data/timescale.csv` is the only source of numerical ages.
13. **ρ·f ≈ 0.09 for both Murzuq classes.** It holds for H0c only (C24).
14. **QSIM 0.307 as "31% of spores".** It is a minimum trilete:cryptospore ratio; the share is 0.235 (C12).
15. **Constant recovery as the adequate history.** It fits B2 only under independent age draws; it fails
    at midpoint ages and shared quantiles (C31). The shape tests discriminate against steep declines; they
    select nothing.
16. **"M2 rests on a doubtful specimen."** The value is a stage base; the definite 43.1 m triletes give
    the same number (C42).
17. **"M1 rests only on affinity" or "M1 is untestable as an absence."** Its authors give a qualitative
    preservation-control argument; what is missing is a quantifiable frame (C16, C46).
18. **"Fossilisation" for w(t).** The rate combines abundance, range, diagnosability, preservation and
    collection; say "recorded, identifiable occurrences".
19. **Murzuq as a dated global absence before 459.1 Ma.** 18 of 28 older zeros are younger than 459.1 Ma,
    and a local absence is not a global one (C45).
20. **The checker as semantic validation.** It matches numbers to claims and, for claims listed in
    `value-bindings.csv`, each number to one evidence row and field. It does not match sentences to
    estimands; check meaning against `estimands.md`.
21. **"The 25 Myr decline fits poorly."** Only on drawn allocations. Some admissible allocations pass when
    cutoff-straddling units are counted (C49). The 10 Myr decline fails under every admissible allocation.
22. **Frontier contours as fitted rates.** They are retrospective compatibility contours with a
    data-chosen step; delay and earlier intensity trade off and are not separately identified (C48).
23. **"Murzuq limits intensity to a tenth."** Only with cutting outcomes independent given a shared well
    effect; unqualified inverse-block-size weighting gives a comparison contour near four tenths (C51).
24. **B1 from tracheids.** E4-only tracheid evidence does not admit a polysporangiophyte; B1 needs E3 or
    nested E5. An earlier build broke this for three records.
25. **A missing event row as a negative.** E3 was enumerated only for the Homerian and older, so a
    younger record without an E3 row was not assessed for branching. *C. bohemica* and Capel Horeb have
    published branched fertile material and belong in B1; the Lang axis does not
    (`docs/audits/2026-11-07-gpt6pro-review2-triage.md`).
26. **429 Ma as an earliest start.** It is a conditional one-sided 95% older bound on the start of the
    recognisable record under constant recording and primary units, not an earliest possible start or
    an origin date; quote it beside the 432–434 Ma unit sensitivity.
27. **Interval failures and passes.** Use the finite-sample reference. A failure across every
    admissible allocation is a conservative rejection of that fixed history for the diagnostic only if
    the supports contain the true ages and inclusion state almost surely under the observation model,
    with fixed history, cutoff, timescale, inventory and unit rule and independent continuous ages.
    Containment failure probability delta gives only an alpha + delta size bound; the geological
    ranges have no demonstrated joint coverage. A pass is a possibility, not a fit or a ranking (C49).


## Stage 2 results (integrated 7 November 2026)

C48–C52 are supported: Claude recomputed their key values independently (frontier closed form,
witness KS distances, constant-history endpoints, and all Murzuq contours). They are written into
the article (Results (e), (f) and (g), Discussion and its "Conditions" paragraph), supplement (S2.5, S5.1–S5.4, Tables S1b, S6b, S7b, S9b) and brief.
Codex's semantic review (`docs/audits/2026-11-07-semantic-closure-review.md`) found wording repairs only;
all are applied.
The 8 November follow-up restored two source-backed B1 records (C25/C39/C32), with the E4 anatomical
interpretations kept separate, and refreshed B1 influence (C52) and simulation summaries (C34).
Codex independently recounted the units and checked the constant and step bounds and leave-outs by
closed forms. B0 and B2 result rows are unchanged (`docs/audits/2026-11-08-b1-restoration.md`).

- **Frontier (C48):** with the primary B2 units and zero assumed diagnostic delay, candidate ages
  [431.2]{.C48 .V035}, [444]{.C48 .V036}, [447]{.C48 .V037} and [452]{.C48 .V038} Ma have earlier/later recording contours
  [0.475557]{.C48 .V039}, [0.123700]{.C48 .V040}, [0.105419]{.C48 .V041} and [0.084585]{.C48 .V042}.
  Unit and diagnostic-delay alternatives are in `frontier.csv`; they are retrospective contours.
- **Intervals (C49):** a permitted allocation of all [50]{.C49 .V043} possible B2 units gives the 25 Myr
  decline an asymptotic conditional-age p of [0.07661]{.C49 .V044}. This defeats a blanket rejection of
  that history across the recorded age supports. The output also enumerates cutoff-straddling
  inclusion states and provides negative certificates where the best attainable diagnostic fails.
  Finite-sample p is primary: 25 Myr decline [0.067]{.C49 .V104} with 50 units, [0.049]{.C49 .V105} with 49,
  [0.035]{.C49 .V106} with 48. A failure over all admissible allocations is a conservative rejection under
  the almost-sure support-containment and fixed-model conditions in trap 27; a passing witness is a
  possibility, not a fitted chronology.
- **Timescale (C50):** the primary constant B2 bound ranges from [427.31]{.C50 .V045} to [430.42]{.C50 .V046} Ma
  across the shared-boundary scenarios. This is sensitivity to stated deterministic boundary
  movements, with source-scale mapping explicit; it is not a probability interval.
- **Murzuq (C51):** the constant-history contour with cutting outcomes conditionally independent given
  the shared well effect is [0.091030]{.C51 .V047}; separate well
  rates give [0.099513]{.C51 .V048}, and inverse block-size weighting gives [0.393002]{.C51 .V049} for
  well–formation blocks and [0.418871]{.C51 .V050} for well–stage-support blocks. The latter are
  unqualified composite-likelihood sensitivities.
- **Halved early recording (C53):** with earlier recording at 0.5 of later recording before 426.7 Ma,
  a flat baseline and the primary B2 units (48 guaranteed), the retrospective step endpoint is
  [431.0]{.C53 .V108} Ma, younger than 431.2 Ma. It is a compatibility scenario, without nominal 95% confidence; the closed form
  was checked independently by Codex (10 November) and Claude (11 November). It is quoted in Results (g)
  and the Figure 2 legend.
- **Influence (C52):** removing the three Yea units changes the main constant B2 bound by
  [−1.669552]{.C52 .V051} Myr; removing the five Bathurst units changes it by [0.257617]{.C52 .V052} Myr.
  The same-unit leave-out table records both readings; effects can change direction.

## 6. Checks before and after any change

From the repository root:

```sh
make check-public                        # fetch/hash the archived PBDB input, then public regression tests
make reproduce-derived                   # selected tracked-input outputs; declared optimiser tolerance
make rebuild-source                      # exact archived raw input, inventory and downstream rebuild
make check-sources                       # route/hash and held-source check, or explicit skip
uv run manuscript/figures.py              # rewrites figures/ and figures.json hashes
python3 manuscript/tables.py              # supplement tables; on unchanged inputs, a no-op diff
uv run tools/refs.py build                # bibliography; key collisions fail loudly
make -C manuscript check                  # claims drift check, then makedoc lint and citation audit
make -C manuscript                        # PDF and DOCX for main, supplement and brief into manuscript/build/
python3 tools/units.py check              # unit tables and source hashes
python3 manuscript/package.py             # release inventory with SHA-256
```

Reproduction compares bytes except for the Murzuq optimisation CSV, where numerical fields have
absolute tolerance $10^{-9}$ and keys, schema and categorical fields remain exact. Receipts retain
both reference and regenerated hashes. The source check reports the public White Rose thesis route
and expected hash even when the copyrighted PDF is absent; it does not redistribute the thesis.

Invariants worth asserting when you touch the body-record code: B2 constant bound [428.84]{.C27 .V017} Ma at
n_guaranteed [48]{.C25} and oldest possible 426.7 Ma; B0 exclusion constant bound [434.51]{.C28} Ma (the canonical B0 is C40); exact-age simulation coverage
[0.941–0.958]{.C34}. Any change to these needs a decision entry and a ledger update, not just a passing test.

## 7. Open edges

Assume no new measurements, logs or help from original authors or outside specialists (Barry,
2026-11-01). Each edge below can be worked from the published record and the held data alone.

- **Q1 (pre-Ludlow recovery for B2).** This decides M3. It is untestable within the body record. The
  candidates are an independent effort proxy for Silurian non-marine rock, or published, documented
  searched-but-barren beds.
- **Q1 (second M2 frame).** An older-empty, younger-positive spore sequence outside polar Gondwana with
  counted target and control grains. `manuscript/external_candidates.csv` lists the routes already
  tried.
- **Q2 (pivotal ages).** Yea and Bathurst Island set the B2 tail; leave-one-region-out spans
  [427.22–430.45]{.C30} Ma. The interval search treats age supports as independent rectangles; encoding
  section-level orderings for the pivotal records would narrow what it admits.
- **Q4 (character-to-node links).** The tracheid status of the oldest polysporangiate bodies and the
  timing of crown-diagnostic body features. See `data/pilot/combinations.csv` and `supplement.md` §S6.
- **Q9 (clock sensitivity).** Parked. Rerunning a clock with the M3 bound replaced by the conditional
  alternatives would turn this study's arithmetic into posterior consequences.

## 8. Conduct in this repository

- Read `AGENTS.md`. Facts and citations come from sources read in the task; every DOI is checked.
- Codex and Claude share one checkout. Check that the git index is empty, stage explicit paths only,
  and agree file ownership on the Board (project `silurian-plants`) before concurrent edits.
- To add or change a claim, edit `manuscript/claims.csv`, reverify the evidence, run
  `python3 tools/claims.py stamp manuscript/claims.csv ID`, then make every document pass the check.
- To cite a new work, add its DOI to `references/dois.txt`, run `tools/refs.py build`, and cite the
  printed key as `[@key]`.
- Record decisions in `docs/decisions.md` with who decided. Keep `docs/charter.md`'s AI-roles section
  current.
- Do not edit generated artefacts by hand: `refs.yaml`, the table blocks in `supplement.md`, figures,
  `package_manifest.csv`, or `models/*/out/`.
