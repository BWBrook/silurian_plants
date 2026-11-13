# GPT-6 Pro independent review of `60c406b`: triage, dispositions and split

Claude Opus 5.5, 7 November 2026. Barry commissioned an independent review from GPT-6 Pro and asked, in
Claude chat on 7 November: "I commissioned a detailed review from GPT-6 Pro that should also be
incorporated and actioned, in collaboration with Codex." The cover note and package (report of about
11,700 words, five scripts, tables and logs) are held outside the repository at
`~/input/gpt6pro_review_cover_note.md` and `~/input/silurian_plants_review_60c406b.zip`. The reviewer
worked on a disposable copy and changed nothing in the repository.

Verdict: major revision before submission; the calculations reproduce and are stronger than several
conclusions drawn from them. I agree with the verdict. Codex's review C closure
(`2026-11-07-review-c-closure.md`) reaches the same points on B0 wording independently.

## Dispositions

Each item was checked against sources or frozen outputs before acceptance. "Owner" follows the existing
split: Claude owns the paper, ledger, figures and source accounts; Codex owns inventory, model code,
diagnostics and reproduction.

| ID | Finding | Check | Disposition | Owner |
|---|---|---|---|---|
| R1 | M1 misrepresented: Morris et al. give a preservation-control absence argument | Morris 2018 main text and SI node 110; reply (PNAS 115: E9512) | **Accepted; our Q5 error.** `2026-11-07-m1-rationale.md`; C46 | Claude |
| R2 | Oman belongs in primary B0; retire the lag | Declared B0; Wellman et al. 2003; Codex membership audit | **Accepted.** Oman-inclusive B0 canonical; former inventory an exclusion sensitivity; no lag in either direction | Claude (prose, ledger, figures now); Codex (canonical rebuild of `horizons_reviewed.csv` with an executable membership test) |
| R3 | Intensity is recorded, identifiable occurrence, not fossilisation; frontier; no clock ranking | `histories.py`; suppression code | **Accepted.** Wording now; age–intensity frontier for B2 with unit and delay alternatives | Claude (wording); Codex (frontier analysis and table) |
| R4 | 18 of 28 Murzuq older zeros are younger than 459.1 Ma | `m2_units.csv`, LY-MZ-CU stage chart-code: 10 Darriwilian (D1 3, H2 7), 13 Katian–Hirnantian, 5 Hirnantian | **Accepted; verified.** C45; lead with sustained local encounter; define "qualified" | Claude (wording); Codex (time-by-well panel; small formation/block dependence sensitivity) |
| R5 | Shape rejection claims need interval-aware checks | reviewer witnesses (not yet reproduced) | **Accepted in scope.** Rejection language narrowed now to what survives; interval-feasibility analysis to reproduce and extend the witnesses | Codex (analysis); Claude (final wording) |
| R6 | Unit sensitivity crosses 431.2 Ma; timescale boundaries fixed; Xiemisitai mislabelled Tarim | C30 values 432.07, 434.05 | **Accepted.** Unit sensitivity moved beside the headline now; shared-boundary scenarios and region fix | Claude (placement); Codex (boundary scenarios, region correction, influential-taxon check) |
| R7 | Pivotal-evidence table; *C. barrandei* in M3; tracheid and ASR wording | `2026-10-28-m3-fossil-basis.md`; cards | **Accepted.** | Claude |
| R8 | PBDB all-taxa snapshot missing from public tree; makedoc unpinned; source-dependent tests fail in a clean clone | `build_reviewed.py`; Makefile | **Accepted.** Archive the frozen CC0 extract (Zenodo routine deposit), pin makedoc, separate derived-input and source-rebuild targets with honest skips | Codex |
| R9 | Checker pools values within a claim; manifests incomplete | reviewer's C27 swap example | **Accepted.** Structured selectors (category, reading, unit, cutoff, history, estimand) and dependency-closure manifests | Codex (tooling); Claude (ledger rows and citations once selectors exist) |
| R10 | Products disagree; supplement table collisions (S3, S3b, S11); brief overstates; agent guide stale | rendered PDFs | **Accepted.** | Claude |

One correction to the review itself: the link it gives for the Morris et al. reply is the original 2018
paper; the reply is PNAS 115: E9512–E9513 (DOI 10.1073/pnas.1812816115). Both state the argument.

## Agreed interpretation

`manuscript/estimands.md` states what each analysis bounds and which phrasings are not allowed. Both agents
change it before changing prose or code.

## Stages

1. **Settle evidence and claims (Claude, this turn):** R1, R2 wording, R7, estimands, all wording that does
   not depend on new numbers, R10 rendering fixes, Codex's closure wording items.
2. **Analyses (Codex, next):** R2 canonical rebuild, R3 frontier, R4 panel and block sensitivity, R5
   interval feasibility, R6 boundary scenarios and region fix.
3. **Reproduction (Codex):** R8, R9.
4. **Integration and semantic review (Claude, then Codex):** fold Stage 2 numbers into ledger and products;
   Codex reviews sentences against `estimands.md`, separately from the numerical checker.
