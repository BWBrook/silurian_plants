# Draft combined results and value of information

31 October 2026. Codex, sprint 2 of the agreed sequential programme. This is the
execution handoff for Claude's review of sprint 2. Codex's full counter-review
of sprint 1 and joint reconciliation follow; this is not the final Loop 1 close
memo or a public manuscript.

## What the evidence presently supports

| Maximum and fossil channel | Result/status | What it does not establish |
|---|---|---|
| M1, 515.5 Ma; E2 cryptospores | Bounded source assessment complete; no older/reference numerical design admitted under main, inclusive or outlier readings | No empirical rate, origin bound, maximum-age probability or evidence of biological absence follows from failed admission. |
| M2, 459.1 Ma; E1 trilete spores | Sprint 1 returns conditional bounds from Murzuq cuttings and records stage-1 acceptance for fourteen primary design/transport combinations. Stored numbers and the bounded pipeline smoke were checked; full scientific counter-review and receipt/protocol repairs remain open. | The bounds are not probabilities that a crown date is true. The acceptance contract does not establish coverage conditional on an informative claim, or a universal 5% error guarantee. |
| M3, 431.2 Ma; E3 polysporangiate bodies | Bounded database/primary-literature denominator assessment complete; no numerical absence design admitted | Occurrence lists, fifty selected axes, eleven fragments or six lithological units are not independent searched-negative rock trials. |

The source synthesis and numerical claims have different scopes. Recovering a
complete report can change admissibility without producing a usable comparison.
Balme's six samples are an example: the original is now verified, but only one
sample is Ordovician and its E2 report is uncertain. Argentina's five quantified
samples are genuine per-sample evidence, but overlap the earlier paper and retain
affinity/reporting qualifications. Qusaiba's 37 E2-positive columns supply a
later reference candidate, with boundary-rate and transport issues; they do not
create an older empty interval.

## M2: preserve the result and its qualification limits

The table below is read directly from the primary LY-MZ-CU rows in
`models/f3/out/m2_results.csv`, with minimum reference support 5, chart-code
material interpretation, full-stage age allocation and cluster shape k = 2.
Those rows have 51 marked reference cuttings among 59 and 28 older cuttings.
No new empirical M2 computation or interpretation is adopted in this sprint.

| Assumed older/reference transport ratio, rho | H0 exposure/reference-rate-weighted mean-intensity upper read-out over 443.1–459.1 Ma | Window endpoint T for f = 1 on (459.1,T] Ma | Window at f = 0.1 or 0.01 |
|---:|---:|---:|---|
| 1 | 0.1835 | 462.6 Ma | unbounded |
| 0.5 | 0.2576 | 464.1 Ma | unbounded |
| 0.25 | 0.4211 | 467.1 Ma | unbounded |
| 0.1 | 0.9207 | unbounded | unbounded |

These values show why a reference-level production assumption matters. The
declared designs can exclude sustained high encounter, while allowing a low
encounter history across the proposed maximum. They do not establish that low
encounter equals low biological abundance: production, delivery, preservation
and search all intervene. Nor is a claim that early intensities were
"realistic" established merely by fitting their observational upper bound.
The mean is weighted by the sampled exposure and class rates, not uniformly
over geological time. The window imposes a(t) at least f on (459.1,T] and leaves
younger history free; its endpoint is not a general biological-origin bound.

The amended qualification quantity is the probability of a false delivered
claim **among records passing the frame-potential screen**, counting abstentions
as non-errors. It is not error conditional on obtaining an informative bound.
Calibration targets 0.955, the nominal confidence level is 0.95, and independent
acceptance assesses the 0.93 floor on the declared finite grid. The reported
worst observed false-claim frequency of 0.037 is a simulation result, not a
proof of universal error at most 0.05. Claim frequencies and misses must remain
beside the coverage summaries.
The frequencies are marginal for each quantity/truth cell, not the probability
that any of the many reported curves or design results is wrong. For example,
MZ/rho=1 acceptance cell B1 has 260 non-trivial H0c f-star evaluations among
1,000 passing records, with 16 misses: 1.6% of passing records and 6.15% of
those evaluations. That distinction is the reason to report both denominators.

The independent reuse check verified all 28 receipts' currently recorded code
hashes and the complete H2/rho=1 calibration/acceptance row-to-summary counts.
It also found that the implementation does not bind the active declaration,
source inputs and every statistical dependency, or fully enforce calibration
completeness and receipt compatibility. M1 boundary cells also cannot inherit
the hard-coded M2 age. These are open software requirements, not evidence that
the checked stored simulations are wrong. No M1 design required binding reuse,
so this sprint preserves the frozen M2 results and carries the repair list into
the agreed later counter-review. See `audits/2026-10-31-sprint2-pipeline-reuse.md`.

## M1 and M3: what changed through source work

M1 now has an explicit admission ledger for seven source groups and all three
readings, with exact file hashes and report-to-material mappings. Among the
recoveries are eleven selected Tennessee identifiers, 463 Shandong catalogue
specimens, ten deduplicated Argentine materials with five quantitative samples,
the six-sample Balme original and the 37-column Qusaiba E2 map. These are
different units of evidence; none is silently counted as an independent
negative trial. The 256-specimen Shandong percentages cannot be inverted into
integer counts as printed. Qualitative Argentine observations need not all
occur in its quantitative subsamples; the reporting differences remain visible
without treating every difference as an error.

The Palynodata archive and database match their pinned hashes, and all eight
held derivatives reproduce byte-for-byte. The named-endpoint Cambrian/
Tremadocian union contains 23,718 taxon mentions across 956 documents, including
340 S-coded mentions from 111 documents. The S code denotes spores or pollen,
not secure embryophytes. These counts describe literature coverage on explicit
legacy-label rules, not numbers of suitable samples or E2 absences. They do not
replace the former stage-overlap counts with a comparable statistic.

M3's source audit preserves genuine negative evidence where it exists: Edwards
& Feehan (1980) report fossil-free interlaminated mudstone. It lacks the counted
searched-material denominator and comparable preservation needed for a rate.
The Czech reports' approximately fifty historical axes and eleven fresh sterile
fragments concern selected plants and one field layer. PBDB and GBDB provide
valuable section/bed leads, but their omitted E3 records are not failed searches.
The source-specific next data are field/material ledgers, not more publication
or specimen counts. Full assessments: `audits/2026-10-31-sprint2-m1.md` and
`audits/2026-10-31-sprint2-m3.md`.

## Ranked evidence that could change a decision

The ranking is qualitative and conditional on the current programme, not an
estimated expected value or an acquisition commitment.

| Priority | Evidence | Decision it could change | Why the present substitute is insufficient |
|---:|---|---|---|
| 1 | Independently constrained M2 delivery/recovery ratios for relevant facies and protocols, supported by controls, modern/experimental analogues or other evidence of comparable producer output | Whether a high-encounter M2 exclusion is biologically defensible, and which rho scenarios deserve weight | Target counts alone confound producer abundance with delivery/recovery; cryptospore preservation does not identify trilete rho. |
| 2 | A complete Cambrian sample roster selected independently of E2 detection, with failed preparations, non-target recovery, per-sample reporting, age support and a comparable younger reference | Admission of an M1 statistical design; persistent high-production histories could then be tested | Specimen catalogues, plate sources, broad Series 2 ages and literature mentions do not identify the missing trials. |
| 3 | Bounded Irish or Loděnice searched-rock/bed ledgers, including unsuccessful searches, effort, preservation class, diagnostic uncertainty and comparable references | Admission of an M3 absence design | Fossil-free prose has no n; museum specimens and fragments are not a field-search denominator. |
| 4 | Re-examination/reconciliation of Argentine 7999, Samphire core 4 and the younger Samphire spore-like forms | E2 first-appearance and producer-affinity readings; candidate preservation controls | Affinity resolution alone does not reconstruct missing sampling coverage or identify reference transport. |
| 5 | Resolve H2/D1 material-code ambiguity, the Libyan 7287-ft prose/chart discrepancy and relevant age allocations | Stability of M2 variant screens and core-reference admission | The primary cuttings results are not all driven by these records; the core design still has weak reference support even with 7287 accepted. |

Repairing and rechecking qualification receipts is an immediate implementation
dependency before the next binding numerical tranche, separate from this ranking
of scientific evidence. External inquiries may help recover ledgers or specimens,
but Barry sends them; no external contact or publication occurred here.

## Transparent conditional sampling calculations

For planning only, suppose an eligible independent material block has **known**
reference detection probability p, Poisson encounter rate -log(1-p), an assumed
transport ratio rho and relative target intensity f. Then the chance of zero
reports in n comparable older blocks is `(1-p)^(n*rho*f)`. The smallest integer
n making it at most 0.05 is `ceil(log(0.05)/(rho*f*log(1-p)))`.

At the illustrative p = 0.5 and rho = 1, this requires 5, 44 or 433 independent
empty blocks for f = 1, 0.1 or 0.01 respectively. With rho = 0.1 and f = 0.1 it
requires 433. All 27 combinations of p in {0.1, 0.5, 0.9}, rho in {1, 0.5, 0.1}
and f in {1, 0.1, 0.01} are saved in `conditional_sampling.csv`; a separate
high-precision calculation verified every value and its minimality. M3's
per-independent-block illustration is saved separately in its evidence folder.

None of these p values comes from the assembled sources. Finite reference
uncertainty, uneven exposure, positive dependence, event ascertainment and the
biological link to a crown node are absent from this simple calculation. It
illustrates the sensitivity of a proposed design; it is not F3 qualification,
an empirically estimated collecting requirement, or a probability for a clock
maximum. Several fragments or repeated papers from one bed cannot supply n.

## Review handoff

Source, model and review statuses are separate throughout. The package changes
evidence tables, reproducible extraction/planning scripts and programme records;
it changes no F3 estimator, frozen M2 output, ASR code or taxon card. Moderate
checks ran locally; no heavy run or Nectar resize was needed.

Verification: all 23 source-file hashes match the holdings; all 21 admission
entries pass the identity/path checks; the 49-unit/294-outcome interface passes
its validator and every outcome/eligibility value matches the sprint-1 handoff.
Independent checks reproduced the Qusaiba raster and joins, Balme inventory,
four reported M2 table rows and all 27 sampling calculations. An injected wrong
core label is rejected by the new extraction guard. The Cambrian/Argentina
extractor and M3 database census reproduce their tables; Palynodata's eight
derivatives match the full-release reconstruction. The seven newly checked
publication identities match Crossref DOI, title and first author. Final
file hashes are bound by `data/units/sprint2/receipt.json`. The required full DOI
scan checked 736 distinct strings and returned the same 26 pre-existing flags
in four unchanged request/action/outreach files (captured Markdown/URL suffixes
and citation-context checks). No flag concerns a changed sprint-2 source; the
log is retained as `data/units/sprint2/doi-scan.log`.

Claude's next owned step is review/fix of sprint 2: independently reconstruct
the decisive non-admission evidence, check the Qusaiba/Samphire mapping, and
challenge whether any declared reading really supplies an admissible contrast.
Then Codex reviews/fixes sprint 1, prioritising the specific receipt gaps and
the reporting, first-appearance, selection and acceptance assumptions. A repair
that changes an empirical result or qualification invalidates affected downstream
claims. Joint reconciliation, not this draft, closes Loop 1.
