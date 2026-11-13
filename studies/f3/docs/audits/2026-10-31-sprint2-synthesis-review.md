# Independent sprint-2 synthesis review

31 October 2026. Bounded, read-only review of
`docs/sprint2-results-and-value-of-information.md` and
`docs/audits/2026-10-31-sprint2-m1.md`, against the frozen sprint v2 plan,
source-roster declaration, source-assessment reports, prior pipeline reuse
findings, current estimator definitions and stored M2 results. No repository
files or frozen outputs were modified. This is not the scheduled scientific
counter-review of sprint 1.

## Decision

The source-admission conclusions and the decision not to edit the F3 engine in
this sprint are supported. No arithmetic error was found. Three local wording
repairs should precede handoff; none requires a model rerun or changes the
reported non-admission decision.

1. **Name the weighted estimand** (synthesis table, original line 33).
   “H0 mean-intensity upper read-out over 443.1–459.1 Ma” can be read as an
   unweighted time mean. `envelope.py` defines the mean using integrated older
   sampling exposure and reference-rate weights; unsampled time is not equally
   represented. Use “H0 exposure/reference-rate-weighted mean-intensity upper
   read-out” and explain the weighting in one sentence. This matters when
   translating the sampled record into claims about a continuous interval.

2. **Define the window hypothesis beside its endpoint** (same table).
   “Window origin endpoint” risks being mistaken for a general biological-origin
   bound. `m2.py:127` calls `origin_set` with `start=459.1`; `envelope.py:994`
   defines the null as a(t) >= f on (459.1,T], with any a(t) in [0,1] on
   (tau,459.1]. Rename this “Older endpoint T for the stated pre-459.1 intensity
   window” and state that hypothesis. A low earlier intensity or an arbitrary
   production hiatus is not excluded by an endpoint calculated for f=1.

3. **State the qualification's marginal scope** (original lines 47–54).
   The distinction between false-claim frequency with abstention and coverage
   conditional on informative output is correct. Add that the reported 0.037
   maximum is over individual quantities and declared truth cells. It does not
   control the probability that any claim anywhere across the reported curves,
   scenarios or overlapping designs is wrong. The inherited framework explicitly
   gives marginal read-outs, not simultaneous coverage. Include a compact actual
   claim/miss example if retaining the numerical frequency: for LY-MZ-CU/rho=1,
   acceptance B1 records 260 non-trivial f_H0c evaluations among 1,000 passing
   replicates, with 16 misses (1.6% of passing replicates; 6.15% of those 260).
   These are the receipt's counts under its existing convention, not a new
   validation of that convention.

## Checks that hold

- All four primary LY-MZ-CU rows have tau=443.1, 51/59 marked reference units,
  28 older units and exactly the synthesis's H0 and window read-outs.
- All 27 conditional sampling values satisfy the stated formula and are the
  smallest qualifying integers under independent 70-digit Decimal arithmetic.
  The formula correctly scales Poisson encounter rate, not probability, by rho*f.
  Its known-rate, equal-opportunity and independence assumptions are explicit;
  it is not represented as an empirical collecting requirement or qualification.
- The M1 audit explicitly recognises that searched younger negatives could test
  persistent older production. Lack of exposure before 515.5 Ma only prevents
  the separate pre-515.5 window claim that allows any later history.
- Qusaiba's all-positive reference is correctly described as needing boundary
  treatment, not as intrinsically inadmissible. No complete sample denominator
  is inferred from selected specimens or repeated publications.
- No-admission is consistently separated from biological absence. The M3
  qualitative negative is retained without manufacturing independent trials.
- The later full M2 counter-review remains scheduled. Input/receipt binding
  gaps remain software work, not alleged scientific non-identifiability; no
  admitted M1 design required binding engine reuse during this sprint.

The cited `data/units/sprint2/m1_admission.csv` was not yet present at the initial
review read. Parent was notified as an integration item, not a scientific
finding. Ensure the final handoff contains the promised seven-group by
three-reading ledger and referenced Palynodata audit.

Source materials themselves were independently checked in the separate source
tranche. This review did not reopen them, rerun empirical fits, requalify M2,
or assess the full selection/first-appearance contract beyond the stated scope.

## Parent disposition

All three wording recommendations adopted in the combined memo: the weighted
mean, the explicit window hypothesis, and marginal error scope. The B1
claim/miss example is included. The final receipt binds the integrated versions.
