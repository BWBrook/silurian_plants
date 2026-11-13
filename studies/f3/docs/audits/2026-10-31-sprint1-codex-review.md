# Sprint 1 counter-review and repairs

Codex, 31 October 2026, reviewing Claude's sprint 1 at `f08afb4`, after
Claude's sprint-2 review (Board 2720). Questions Q1, Q2 and Q5. This is the
second counter-review in the agreed sequence; joint reconciliation follows.

## Historical evidence independently reproduced

`work/codex/sprint1-review/check_historical.py` reads immutable Git objects at
`f08afb4`, without importing the qualification implementation. All 28 stored
calibration/acceptance receipts agree with their replicate tables and recorded
code hashes. All 3,122 cell/quantity summaries reproduce, including pass counts,
ordered unique replicate indices, attempts for complete cells, errors, coverage,
claim counts, misses and calibration shifts. The acceptance tables contain
414,831 quantity evaluations labelled as claims, with 3,193 misses; the largest
observed per-cell/quantity false-claim frequency is 0.037. These are correlated
quantity evaluations, not 414,831 independent experiments. No missing coverage
field occurs on a non-trivial row for a reported quantity in these tables.

This establishes agreement of stored evidence, not the adequacy of its scientific
contract or compatibility with repaired code. The historical receipts omit
rejected attempts and bind only five files. Their validation weaknesses therefore
remain real even though these particular summaries reproduce.

## Review scope and ownership

The parent integrates the review, scientific adjudication, reruns and programme
records. Separate bounded Codex delegates inspect source-to-design validity and
statistical validity, while a third implements qualification-evidence enforcement.
No raw source report or taxon card is edited. Any correction to an empirical
result or qualification is propagated into the combined sprint-2 synthesis.

## Taking the sprint-2 review into account

Claude's added Borenshult/Libya/Ghelli assessments and the rule against coding
disputed forms as zeros are retained. Two synthesis statements needed correction:

- A secure older E2 zero does exist at BOR-71.1 under main, as Claude's own
  review reports; one such unit fails S1. The conclusion is no admitted design,
  not no secure older zero in any frame.
- A Stage 4 assignment does not make a fossil “no younger than 514.5 Ma”.
  `data/timescale.csv` gives Stage 4 support 514.5–506.5 Ma. Wang et al. (2022),
  PDF p.2, themselves give ca.514–509 Ma under their timescale. Neither supports
  treating the oldest interval endpoint as an observed occurrence date. The
  stage-level gap below M1 may be about 1–9 Myr. The broader Series 2 alternative
  in Strother's caption still crosses M1 and remains an age-interpretation
  alternative, not a proven pre-M1 occurrence.

The combined memo, four affected admission-ledger readings and current question
summary are corrected. Claude's dated audit is preserved with a supersession
notice; its source recoveries and non-admission verdicts remain. The E2 monad
rule remains a reconciliation decision before any cross-source E2 analysis.

## Numerical target and qualification amendments

The independent methods audit and its scripts are retained under
`work/codex/sprint1-review/methods/`. It reconstructs the primary MZ likelihood
with separate Gamma quadrature and optimisation. H0 f*(459.1) is 0.183790945;
tight-root engine calculations agree within 2.2e-8. The ordinary engine returns
0.183537986 because its root tolerance is 1e-3. Extra CSV digits are numerical
output, not four-decimal accuracy. H0c is 0.05795606, and the f=1 window endpoint
is 462.5479 Ma, reported conservatively on the 0.5-Myr grid as 462.6 Ma. The
engine tolerance is unchanged because this discrepancy does not alter the
reported scientific resolution or decision.

QB-CO has seven saved acceptance rows whose selected first appearance is younger
than the simulated breakpoint: Q2 indices 349, 355, 1003 and 1464; Q3 indices
159, 678 and 1083. Their realised-interval histories are not constant. The
revised declaration therefore qualifies H0m/H0/H1 for QB, retaining H0c as an
unqualified diagnostic. It does not count these invalid constant-history tests
as covers or silently remove individual unfavourable replicates.

The original Q4 tests f*(459.1) only under f=1; B1 and B2 place their truths at
470 Ma. This does not directly test the informative approximately 0.18 boundary
at 459.1 Ma. Before the rerun, Codex adopted the independent reviewer's B3
extension: a constant-history cell with t0=459.1 and intensity set by the
primary design's H0 f*(459.1). It uses the same target count, calibration rule
and independent acceptance protocol. B4 adds one targeted window scenario:
reference-level encounter on (459.1,462.6], zero on (tau0,459.1], and the
reference intensity younger than tau0. This directly stresses the central MZ
window without imposing high encounter throughout the later interval. It is
H0/H1, not monotone H0m; Q8 retains its original later level of one. The new
calibration/acceptance/stage-2 roots are 20261111/20261112/20261113 because the
older acceptance evidence informed this review. This is a declared amendment made
with the earlier results known, not outcome-blind preregistration. It still
does not establish simultaneous curve coverage or validity under arbitrary
untested histories.

## Pre-run verification and execution declaration

The complete F3 test suite passed: 228 tests on Python 3.12.15, NumPy 2.3.4
and SciPy 1.16.3. Independent adversarial review reproduced the previously
unhandled pre-screen-error case and verified its repair, failed screen flags,
orphan stage-2 evidence and overwrite refusal. The QB development smoke has
45 passes from 70 attempts; the independent H2 smoke has 75 from 76, with no
pre- or post-screen errors. These are development checks, not qualification.

Mac/Nectar binding comparison passed for LY-MZ-CU and QB-CO under Python 3.12
and the same NumPy/SciPy versions. Deterministic files/protocols match exactly;
optimised reference/boundary values match within the declared 1e-8 tolerance.
Acceptance reuses the exact values stored by calibration.

The reviewed code and declaration are committed before the new binding run.
All 14 primary design/transport pairs will be recalibrated and independently
accepted on the 12-cell grid, with three additional calibration diagnostics.
Target/cap remain 1,000 passing/20,000 attempts per cell. Stage 2 runs only for
validated borderline quantities. Historical outputs are retained until the
new evidence is checked and the affected empirical read-outs are regenerated.

## Source and interpretation checks

The independent source audit reconstructed all 36 Libyan variant groups and four
QB groups, including the 37-column, eight-trilete-row Qusaiba chart (22 positive
columns). Five primary PDF hashes matched. The primary Murzuq reference is
51/59, with 28 empty older cuttings: 56 reference rows are Cr4-only, two span
Cr3/Cr4 and I3 4640 ft is Cr3-only. The chart-priority reading preserves the
conflict with prose claiming only one Cr3 specimen. All 35 exact-Hawaz materials
include 25 cores, eight appendix-specified cuttings and two unspecified materials
coded CU on the chart; only ten enter the primary cutting contrast. Their green
chart marks range from 6–10, versus 3–16 across all 35 materials.

The independent method check identified a zero-exposure Sandbian gap. A
reference-level pulse there has calendar-time mean 0.3375 on 443.1–459.1 Ma,
but exposure-weighted mean zero. The reported bound is therefore explicitly
weighted, not a calendar-time limit. Cryptospore recovery establishes a delivery
and preservation route but does not identify a trilete transport ratio. Recovery
ages of potentially caved fossils cannot securely establish indigenous appearance.
The current audit and combined synthesis state these limits.

## Contract repairs

Receipts now bind consumed source tables, generated units, statistical code,
active declarations, runtime and a predeclared quantity/phase roster. Every
consumed attempt is retained. Verification reconstructs the summary, calibrated
shift and verdict, checks the exact predecessor chain, and refuses incomplete,
stale or malformed evidence. Failed optimisation before the screen blocks
qualification rather than disappearing from its population. Nonprimary variants
cannot inherit a primary pass. QB main/zero is an inadmissible coding diagnostic.
These repairs leave the estimator itself unchanged.

## Cross-host loader defect found by the completed-run check

The first full counter-review run at `5fcee58` completed all fourteen calibration
and acceptance pairs, with zero shifts and every acceptance passing. The
regenerated 168 empirical rows have no numerical/design change from `f08afb4`;
labels distinguish fourteen qualified primaries, 144 unqualified sensitivities
and ten inadmissible coding diagnostics. An independent checker reconstructed
all saved numerical evidence.

Loading those receipts on the Mac nevertheless failed closed: the stored Linux
screen critical value 5.991464547107979 differed by one binary ULP from the
Mac's recomputation, 5.991464547107980. The original implementation compared
them exactly. A cross-host binding comparison had not exercised this load path.
The narrow repair permits eight ULPs only for this independently recomputed
critical value, with both values finite. The recorded LR > recorded critical
screen decision, raw files, counts and dependency hashes remain exact.
The method and truth grid are unchanged. The repaired code is frozen and the
full run repeated against it, using the same seeds; the old package remains
historical rather than being silently rebound to new code.

The portability fix passed independent read-only review, the 58-test contract
suite and the complete 239-test F3 suite. Regressions accept the measured one-ULP
cross-host difference and the eight-ULP boundary, reject nine ULPs, reject all
nonfinite stored/recomputed values, and still reject a contradictory screen flag.


The fix is committed at `31fab51`. All 28 earlier receipts loaded on the Mac
using their historical bindings, with before/after hashes unchanged; current
bindings correctly refused the old code. This is a regression check, not a
relabelled qualification. The final rerun is staged at
`nectar:/data/codex/silurian_plants/sprint1-review-31fab51/`; the earlier full
package remains at `sprint1-review-5fcee58/`. Both use 62 workers, with BLAS
threads pinned to one, Python 3.12, NumPy 2.3.4 and SciPy 1.16.3.

The first new H2/rho=1 calibration receipt loaded on the Mac against the active
`31fab51` source binding during the rerun, completing the cross-host test that
the earlier binding-only check had omitted. Its hash and verdict are retained
in `work/codex/sprint1-review/crosshost/current-calibration-loader.json`.

## Final current-code qualification and handoff

The `31fab51` run completed in 883.5 seconds on Nectar, including empirical
regeneration (607.4 seconds summed over calibration/acceptance simulations).
All fourteen calibrations are complete with shift zero; all fourteen acceptance
pairs pass stage 1, with no stage 2 required. The 28 receipts contain 378 cells,
378,000 passing records from 482,605 consumed attempts, and no pre- or post-screen
numerical errors. Each binding cell has 1,000 passing records. The independent
checker reconstructed all 3,501 cell/quantity summaries, including 1,503
acceptance summaries, without importing the F3 assessment code. It also
independently integrated the declared reference and target histories.

The independent comparison finds every compressed ledger, statistical summary
and non-file binding value exactly identical to the first counter-review run;
only the contract's source hash changed. The final product loader verifies all
fourteen current bindings on the Mac. The 168 empirical rows have no numerical
or design-field difference from `f08afb4`: fourteen qualified primary rows,
144 unqualified sensitivity rows and ten inadmissible QB coding diagnostics.
QB H0c is explicitly an unqualified class diagnostic. The 56 current qualification
artifacts, run log and regenerated screen/results tables are integrated; original
outputs remain in Git. Evidence: `work/codex/sprint1-review/current_binding_check.json`,
`final-run/` and `evidence-check/final-31fab51/` under that review directory.

The worst observed acceptance false-delivered-claim frequency is 38/1,000.
Across the correlated quantity evaluations there are 529,550 non-abstentions
and 3,780 misses. MZ/rho=1's new B3 H0 intensity test has 0 misses among 703
non-abstentions (1,000 passing records); B4's f=1 window has 20 misses among
60 non-abstentions (1,000 passing records). The latter is 2% across passing
records but 33.3% in the selected non-abstaining subset. The updated result note,
combined memo and interface README retain both denominators prominently.

**Reconciliation recommendation:** retain the encounter-compatibility estimates
with their restricted, finite-grid error statement. Do not describe the window
as having 95% coverage conditional on obtaining a claim. If that selected-result
property is required, it needs a separately declared qualification target, not
post-hoc relabelling of this pass. Claude's next tranche is reconciliation of
this finding, QB class scope, the corrected Cambrian age support and the shared
E2 monad rule. M1/M3 non-admissions stand; Loop 1 is not closed by this handoff.

Nectar was idle after the run and returned to `c3.large`: OpenStack ACTIVE,
eight CPUs, about 15 GiB usable RAM, /data mounted, SSH/Tailscale/SMB active.
The temporary allocation and restoration are recorded in the Nectar control
plane. This tranche changes Python qualification code/tests, CSV evidence and
scientific documentation; no R/ASR analysis or taxon card changed.

Final source/interface checks passed: 23 held-source hashes, all 21 sprint-2
admission entries, the refreshed 84-file sprint-2 receipt, and the 49-unit /
294-outcome sampling validator. No new citation or taxon card was introduced.
