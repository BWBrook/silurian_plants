---
document: agent-facing paper
study: F3, fossil maxima behind land-plant molecular clocks
status: internal draft; Loop 3 sprint C delivered, awaiting Codex review C and Claude's loop close
human_paper: manuscript/text/main.md (+ supplement.md, brief.md)
claims_ledger: manuscript/claims.csv
governing_docs: [docs/charter.md, docs/decisions.md, docs/plan-f3.md, docs/f3-shape.md, docs/loop3-design.md, docs/loop3-results.md]
authority: Barry W. Brook decides public release, submission and any correspondence outside Claude and Codex
updated: 2026-11-02
---

# F3 for agents: what this study established, how to verify it, and how not to break it

This is the version of the paper written for an agent arriving cold. The human paper argues; this one
indexes. It says what is claimed, where each number lives, which commands regenerate it, what has been
superseded, and where the open edges are. When this file and a primary artefact disagree, the
artefact wins and this file is wrong: fix it in the same commit.

## 1. Read order and trust

1. This file, then `manuscript/claims.csv`, the ledger of 34 claims (C01–C34). Each row gives the
   value, its status class, its evidence path and its limit. Quote a claim only with its limit.
2. `manuscript/text/main.md` for the argument; `supplement.md` for the machinery.
3. `docs/decisions.md` (newest first) for what was settled, by whom, and why.
4. `docs/questions.md` for the programme's open questions (Q1–Q10). This study answers part of Q1.

Status classes in `claims.csv`, from strongest to weakest: *source extraction* and *frozen qualified
result*; *reviewed inventory*; *conditional endpoint inference*; *declared* or *retrospective
sensitivity*; *exploratory model-conditional calculation*; *procedure check*. A procedure check (for
example, simulation coverage) tests the method, never the fossils.

## 2. The answer, as claims

- **M1 (515.5 Ma, crown Embryophyta).** Untestable from sampled absence. No admitted older-zero design
  (C16). The Stage 4 material is younger than the maximum (514.5–506.5 Ma) and is not accepted as
  embryophyte by the three assessed sources (C15).
- **M2 (459.1 Ma, crown Embryophyta).** One qualified comparison, Murzuq Basin (C01–C06, C24). It
  constrains the product of delivery and producer intensity, ρ·f ≈ 0.09, not either alone. QSIM-801
  is exploratory only (C11–C14, C23).
- **M3 (431.2 Ma, crown Tracheophyta).** No absence design (C17). Positive-record endpoints for B2:
  428.84 / 428.88 / 428.45 / 431.63 Ma / none within domain, for constant, PBDB-density,
  plant-excluded-density, 25 Myr decline and 10 Myr decline histories (C27). Recovery reduced tenfold
  before 426.7 Ma gives 448.10 Ma; a hundredfold gives no bound (C32, retrospective).
- **Known-answer check.** B0 bounds of 434.51–437.16 Ma sit 21–24 Myr after cryptospores are certainly
  present at 458.2 Ma (C28). This shows that a body lag has occurred once in this system. It is *not* a
  lag estimate to transfer to B2.
- **Synthesis.** An older, sparsely recorded flora is allowed, not required. The record cannot test
  recovery before its oldest find.

## 3. Vocabulary that the files use

| Term | Meaning |
|---|---|
| M1, M2, M3 | The 515.5, 459.1 and 431.2 Ma maxima |
| E1–E5 | Event channels: trilete spores; cryptospores accepted as embryophytic; polysporangiate bodies; tracheids; crown vascular-plant members |
| B0, B1, B2 | Body categories: any land-plant body; polysporangiophyte; crown vascular-plant member (lycophyte line or euphyllophyte) |
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
| Suppression grid | as above | `suppression_sensitivity.py` | `suppression_sensitivity.csv` | C32 |
| Simulations | unit counts from above | `simulation.py` | `simulation_results.csv` | C34 |
| Paper figures | the outputs above, `data/spores/first_appearances.csv`, `data/timescale.csv` | `manuscript/figures.py` | `manuscript/figures/`, hashes in `figures.json` | — |
| Supplement tables S3–S11 | `models/f3/loop3/out/` | `manuscript/tables.py` (rewrites marked blocks in `supplement.md`) | `manuscript/text/supplement.md` | — |
| Bibliography | `references/dois.txt`, `references/manual.yaml` | `tools/refs.py build` (Crossref CSL-JSON) | `references/refs.yaml` | — |

The primary row of `reviewed_bounds.csv` is: `reading=main`, `units=locality_age`, `variant=primary`,
`excluded_region` empty, `cutoff=Emsian`. Most misquotations come from leaving out one of these filters.

## 5. Traps: superseded results and known misreadings

Do not reintroduce any of these. Each was caught in review; the record is in `supplement.md` §S7 and
`docs/audits/`.

1. **Loop 3 pilot numbers.** The logistic-ramp limits 452.6 / 454.1 / 438.0 Ma, "favours the young
   clock" and "a measured 15–25 Myr lag" are retired (`docs/loop3-pilot.md` is marked provisional).
   The defects: stage collection totals used as per-Myr density, which counts duration twice; medians
   of imputed limits presented as 95% limits; PBDB localities merged by country, genus and age
   overlap; collections treated as independent beds.
2. **"Murzuq excludes abundant producers."** It excludes abundant, *well-delivered* producers. Only ρ·f
   is constrained (C24).
3. **QSIM as a second qualified test.** It is not; search coverage and independence are undocumented.
4. **Age-allocation quantiles as confidence bounds** (Table S8). They are descriptive.
5. **The suppression grid as a nominal 95% result.** It was chosen after seeing the shape diagnostics
   and is retrospective.
6. **The B0 lag as a B2 lag.** The record does not estimate any delay for B2 (C33 is arithmetic on an
   assumed delay).
7. **Agreement between Claude and Codex as validation.** The two systems review each other; neither is
   independent ground truth.
8. **Clocks as validation targets.** The oldest *Cooksonia* and Ludlow *Zosterophyllum* are themselves
   clock calibrations. Agreement tests whether a maximum is reasonable, not whether a clock posterior
   is right.
9. **The Yea *Baragwanathia* age.** It is unresolved, Gorstian to Emsian, and carried as the full range.
   Do not fix it to either end.
10. **Wells.** The Murzuq frame has five wells; the 28 older cuttings come from three of them.
11. **Figure numbering.** Files are named in citation order (`fig2_mapping`, `fig3_evidence`,
    `fig4_bodies`, `figS2_qsim`). Older audits use earlier names.
12. **GTS2012 against ICS v2024/12.** Literature Early Devonian boundaries differ from ours by up to
    3 Myr; `data/timescale.csv` is the only source of numerical ages.

## 6. Checks before and after any change

From the repository root:

```sh
uv run --with numpy --with pandas --with scipy --with pytest python -m pytest models/f3/loop3 -q  # 26 tests
uv run manuscript/figures.py              # rewrites figures/ and figures.json hashes
python3 manuscript/tables.py              # supplement tables; on unchanged inputs, a no-op diff
uv run tools/refs.py build                # bibliography; key collisions fail loudly
make -C manuscript check                  # makedoc lint and reference audit, all profiles
make -C manuscript                        # PDF and DOCX for main, supplement and brief into manuscript/build/
python3 tools/units.py check              # unit tables and source hashes
python3 manuscript/package.py             # release inventory with SHA-256
```

Invariants worth asserting when you touch the body-record code: B2 constant bound 428.84 Ma at
n_guaranteed 48 and oldest possible 426.7 Ma; B0 constant bound 434.51 Ma; exact-age simulation coverage
0.941–0.958. Any change to these needs a decision entry, not just a passing test.

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
  427.22–430.45 Ma.
- **Q4 (character-to-node links).** The tracheid status of the oldest polysporangiate bodies and the
  timing of crown-diagnostic body features. See `data/pilot/combinations.csv` and `supplement.md` §S6.
- **Q9 (clock sensitivity).** Parked. Rerunning a clock with the M3 bound replaced by the conditional
  alternatives would turn this study's arithmetic into posterior consequences.

## 8. Conduct in this repository

- Read `AGENTS.md`. Facts and citations come from sources read in the task; every DOI is checked.
- Codex and Claude share one checkout. Check that the git index is empty, stage explicit paths only,
  and agree file ownership on the Board (project `silurian-plants`) before concurrent edits.
- To cite a new work, add its DOI to `references/dois.txt`, run `tools/refs.py build`, and cite the
  printed key as `[@key]`.
- Record decisions in `docs/decisions.md` with who decided. Keep `docs/charter.md`'s AI-roles section
  current.
- Do not edit generated artefacts by hand: `refs.yaml`, the table blocks in `supplement.md`, figures,
  `package_manifest.csv`, or `models/*/out/`.
