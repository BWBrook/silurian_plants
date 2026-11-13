# Semantic review of the integrated body-record results

Codex (`gpt-6.1-sol`), 7 November 2026. Read-only review of commit `87ad964` against
`manuscript/estimands.md`, the integrated products and the source CSVs. Scope: article §§3.3, 4 and 5;
supplement §§S5.2–S5.5 and the new stage-2 tables; brief; agent guide. I inspected the prose, table
fields, `frontier.py`, `frontier.csv`, `interval_feasibility_summary.csv`, `bound_sensitivity.csv` and
`influential_taxa.csv`. I did not rerun models or repeat the numerical audit.

## Verdict

**Does not yet pass semantic closure.** The integrated numbers agree with the reviewed outputs, and the
interval, timescale and influence claims are mostly scoped correctly. Seven small prose repairs remain.
Four are consequential noun/estimand errors: one frontier definition, two article synthesis statements
and the brief's conversion of a fossil-category endpoint into a date that “agrees” with a clock. These
are not repaired by caveats elsewhere.

## Required repairs

### 1. Frontier variable is given the wrong scientific object — high

`manuscript/text/supplement.md:581–586` calls $T$ “a candidate start of the recoverable record” but
then computes the earlier interval as $T-d-A$. The implementation and CSV define $T$ as
`candidate_lineage_ma`; the recoverability start is $T-d$. Table S9b's caption is correct. At zero
delay the two ages coincide, which hides the error in the headline row, but the 5–20 Myr alternatives do
not.

Minimal replacement for the first sentence:

> The frontier inverts it: for a candidate lineage age $T$ and an assumed delay $d$ before
> recoverable diagnostic bodies, what ratio of earlier to later recording intensity puts the
> corresponding recoverability start $T-d$ exactly on the 95% bound?

Evidence: `models/f3/loop3/frontier.py` computes
`candidate_recoverability = candidate_lineage_ma - diagnostic_delay_myr`; `frontier.csv` names both
fields separately.

### 2. The brief substitutes a body-record endpoint for a crown date and omits zero delay — high

`manuscript/text/brief.md:27,33–34` successively calls the result an “earliest date”, says vascular-plant
bodies “became findable no earlier than about 429 Ma”, says this “agrees with the youngest clock”, calls
432–434 Ma “the date”, and reports the C48 rate contrasts for clock ages without stating their zero-delay
assumption. The calculation is a conditional one-sided older bound on a recoverable fossil category, not
a crown date or an estimate of when bodies became findable. The final delay caveat does not change those
nouns.

Minimal replacements:

- Line 27: “From how these finds are spread through time, a standard method gives a one-sided older
  bound on when the recoverable record of a group could have begun, conditional on how often recorded,
  identifiable occurrences accumulated.”
- Line 33: “Under steady recording and the primary unit rule, the one-sided 95% older bound on the
  start of the recoverable crown-member body record is about 429 Ma; it is a fossil-category endpoint,
  not a crown date. Coarser unit treatments move that conditional bound to about 432–434 Ma. If
  crown-diagnostic bodies were recoverable from lineage origin (zero assumed delay), lineage ages of
  444–452 Ma would need earlier identifiable occurrences to have been recorded 8–12 times less often
  than later (2.4–4.5 times under the coarser unit treatments); an origin-to-diagnostic-body delay
  reduces the required contrast.”
- Line 34 heading and first sentence: “**One fossil can move the bound by 20 million years.** Counting
  one set of tiny spore-capsule fragments from Late Ordovician Oman moves the conditional older bound
  for the recoverable land-plant body record about 20 million years older.”

### 3. Table 4 states a confidence bound as an actual beginning — high

`manuscript/text/main.md:416` says “Recoverable crown vascular-plant bodies began after about 429 Ma”.
The calculation does not estimate that event; it places a conditional one-sided 95% older bound on the
start of the recoverable category.

Minimal replacement for the first-column cell:

> The one-sided 95% older bound on the start of the recoverable crown vascular-plant body record is
> about 429 Ma.

The existing “Rests on” and “Fails if” cells can remain.

### 4. Section 4.1 broadens two observation-process results to “early land plants” — high

`manuscript/text/main.md:374–378` says the analyses “rule out early land plants that were both abundant
and readily recorded”. The calculations concern sustained delivered trilete encounter in Murzuq and the
start of a recoverable crown-member body category under a fixed recording history. They do not jointly
exclude abundant early land plants lacking the relevant diagnostic or outside the catchment; the later
caveats do not repair the broader subject.

Minimal replacement for the first two sentences:

> Taken together, the three analyses support a specific, conditional conclusion. Where the record can
> be interrogated, it places conditional limits on two specific observation histories: sustained,
> well-delivered Llandovery-level trilete encounter through the later Ordovician in the Murzuq Basin,
> and the start of the recoverable crown vascular-plant body record under the later
> Silurian–Devonian recording rate and primary unit rule (one-sided 95% older bound near 429 Ma).

### 5. The agent guide reverses the canonical Oman inventory — medium

`manuscript/text/for-agents.md:85` says the frozen B0 inventory omits the E2 Oman fragments. The current
canonical B0 includes the Katian Oman fragments as one unit; omission is the former-inventory exclusion
sensitivity. This contradicts the same guide at lines 69–75 and C40.

Minimal replacement in the B0 vocabulary cell:

> any land-plant body (declared: any accepted macro- or mesofossil; the canonical inventory includes
> the Katian Oman fragments as one unit, while excluding them is the former-inventory sensitivity,
> C40/C28)

### 6. S5.2 overstates what displayed Table S7b contains — medium

`manuscript/text/supplement.md:357` says Table S7b gives both asymptotic and finite-sample optimised
$p$ values. The displayed table gives asymptotic values and uses a dagger to flag a classification that
changes under the finite-sample reference; both numeric values are in
`interval_feasibility_summary.csv`.

Minimal replacement:

> Table S7b gives the asymptotic $p$ value for each state and history and flags cases whose 0.05
> classification differs under the finite-sample reference; the source CSV gives both values.

### 7. Section 4's frontier restatement should name its zero-delay edge — medium

`manuscript/text/main.md:398–401` correctly presents lower earlier recording and delayed diagnostic
bodies as alternatives that trade off, but the quoted 8–12 and 2.4–4.5 factors are specifically the
zero-delay C48 contours. Add “with zero assumed diagnostic delay” after the unit-rule parenthesis. This
prevents the numerical pure-rate edge from being read as applying across the delay alternatives.

## Statements that pass

- Article §3.3 reports the frontier in the correct earlier/later orientation, explicitly at zero assumed
  delay, and gives the primary, region–stage and curated unit alternatives. It calls the values
  retrospective compatibility contours rather than fitted rates.
- The interval-feasibility account searches all four cutoff-inclusion states, distinguishes witnesses
  from negative certificates, limits negative conclusions to the encoded independent support rectangles
  and diagnostic, and says that optimised $p$ values are not calibrated. The claims that pure decline10
  fails for every B2 inclusion state and that canonical B0 fails for all six histories match the CSV.
- The timescale account correctly describes five deterministic shared-boundary scenarios and three
  separate comparisons with the maximum. It does not call them a posterior, propagated age uncertainty
  or a worst-case envelope.
- The supplement gives the signed leave-outs correctly: Yea removal moves the main constant B2 bound
  1.67 Myr younger; Bathurst removal moves it 0.26 Myr older. It identifies these as leverage diagnostics,
  not fossil reidentifications. The article's sign convention is consistent with those values.
- Apart from the brief and Table 4 sentences above, the products do not rank clocks or substitute a
  recoverability endpoint for a crown date. The main text explicitly states the rate–delay trade-off and
  that agreement with the youngest clock is not independent support.

## Recommendation and residual risk

Apply the seven local replacements, refresh the rendered products, and run the ordinary manuscript
checks. No model rerun or estimand change is indicated. After those repairs, this semantic tranche passes
and Loop 3 can close, subject to the separate display-item consistency check. The remaining scientific
limits are already stated: unobserved pre-record intensity, diagnostic delay, unit dependence, independent
rectangle age supports, deterministic rather than probabilistic timescale perturbations, and calibration
reuse. Another independent scientific review is unlikely to change the closure decision after the named
sentences and display items are reconciled.
