# What each analysis bounds: the allowed claims

The interpretation specification for the F3 paper. Every rendering (article, supplement, brief, agent guide)
states these results only in these terms. Claude and Codex maintain it jointly; change it before changing
the prose. Adopted 7 November 2026 after review C and the GPT-6 Pro review (`studies/f3/docs/audits/2026-11-07-gpt6pro-triage.md`).

Codex agrees this specification on 7 November 2026 for the stage 2 work. Timescale perturbations
are shared-boundary scenarios, not a probability distribution over ages; intensity frontiers and
diagnostic delays are retrospective compatibility calculations. Interval-feasibility witnesses test
what the admitted ranges permit and do not select the true ages or a preferred history.

A sentence passes only if its subject is the same object as the calculation. A caveat attached to a
sentence does not rescue it if its noun has changed, for example from a fossil-category endpoint to an
origin.

## M1 (515.5 Ma, crown Embryophyta)

- **Published argument:** placement below the oldest possible total-group records (affinity), plus a
  qualitative preservation-control argument from older marine-palynomorph-only sequences (C46).
- **Allowed:** the assembled material contains no enumerated, comparably searched pre-515.5 Ma frame, so
  the control argument cannot be given a calibrated non-detection probability; its unquantified links are
  terrestrial delivery, geographic coverage, search sensitivity and production of recognisable spores.
- **Not allowed:** "rests only on affinity"; "untestable as an absence"; "the Stage 4 material is younger
  than the maximum" as a criticism.

## M2 (459.1 Ma, crown Embryophyta)

- **Number:** GTS2012 Sandbian base plus its uncertainty, keyed to the oldest possible Borenshult trilete;
  the oldest definite trilete gives the same value (C42, C43).
- **Murzuq allows:** a model-conditional limit on *sustained*, delivered trilete encounter in one basin,
  relative to a Llandovery reference, chiefly from later-Ordovician samples: 18 of the 28 older cuttings
  are wholly younger than 459.1 Ma, and the pre-maximum window rests on 10 broadly dated Darriwilian
  cuttings in two wells (C45). Constant class: ρf ≈ 0.091; exposure-weighted class: 0.092–0.184 (C24).
  Both assume conditionally independent cuttings given a well effect. Block weighting by well and
  formation or stage support gives about 0.39–0.42 (C51): an unqualified composite-likelihood
  sensitivity, reported beside the limit, never in place of it.
- **Not allowed:** a dated global absence before 459.1 Ma; an estimate of producer abundance separate from
  delivery; local absence read as global absence (the lineage may have lived outside the catchment).
- **"Qualified"** means the procedure passed a 0.93 coverage floor on a declared simulation grid. It is
  not verification of the historical sampling process.
- **Borenshult:** its three older samples cannot exclude reference-level intensity under the examined
  screen (C44). It remains positive character and age evidence.
- **QSIM-801:** exploratory; the qualitative report of no triletes points the same way; its numbers are a
  minimum ratio under unverified sampling assumptions (C11–C14).

## M3 (431.2 Ma, crown Tracheophyta)

- **Body endpoint:** a one-sided 95% older bound on the start of a *recoverable fossil category*,
  conditional on a fixed relative intensity of recorded, identifiable occurrences, independent
  locality–age units, the adopted numerical timescale and the admitted inventory.
- **The intensity** combines biological abundance and range, diagnosability, delivery and preservation,
  and collection and reporting. Say "rate of recorded, identifiable occurrences", not "fossilisation".
- **Allowed:** under constant or effort-tracking intensity, crown vascular-plant bodies give bounds near
  428.5–428.9 Ma; unit treatments move the constant bound to 432.4 (region–stage; 19 units after the West Junggar correction) or 434.05 Ma (curated
  subset), across 431.2 Ma; reduced earlier intensity moves it further. The frontier (C48) states the
  earlier/later intensity at which a candidate start lies on the bound, for a declared unit rule and
  assumed delay; say "would need", never "was". Shared stage-boundary scenarios (C50) are deterministic:
  "stays younger under each scenario", not "with probability".
- **Not allowed:** a crown date; a ranking of clocks; "the simplest assumption favours the young clock";
  constant intensity as the adequate or preferred history.
- **Fossil basis:** *C. barrandei* (Sheinwoodian, horizon inferred) is older than the Irish Homerian
  anchor. On the current scale the stage-base-plus-uncertainty rule gives 431.9 Ma (Homerian) and
  434.1 Ma (Sheinwoodian), about 2.2 Myr apart; the 2.9 Myr difference from the published 431.2 Ma mixes
  GTS2012 and ICS v2024/12 (C47). Neither number dates the slab, and an older positive anchor does not
  show that a documented absence began earlier. An older stem fossil does not contradict a younger crown
  maximum (C21).
- **Not allowed:** "earliest start" or "earliest date" for the 429 Ma bound; the bound alone without
  the 432–434 Ma unit sensitivity; its overlap with the youngest clock as support for that clock.

## Count, proxy and early-rise comparisons

The general-points revision adds three descriptive/retrospective results, independently checked by
Codex on 13 November 2026. They do not add a fitted finding-rate or dependence model:

- **C55:** the steady-rate curve is a sensitivity to the assumed integer count of independent finds
  at fixed oldest age and cutoff. Its real-valued crossing is algebraic interpolation, not an
  estimated or calibrated effective sample size.
- **C56:** outside rulers are ratios of the specified proxy means in the same two time windows.
  Numerical overlap with a required finding-rate ratio does not show that the proxy supplies that
  change. Such transfer is not established; proportionality to finding intensity across both windows
  would be one sufficient assumption. The rock object is column area, not measured outcrop area; the spore object is a
  share of distinct database document IDs, not producer prevalence. No combined factor is fitted.
- **C57:** with the later rate fixed at one and zero delay, the oldest-find calculation constrains
  the earlier integral to K. Equal earlier integrals are indistinguishable under that fixed later
  plateau; this does not establish the plateau or remove the later fossil-age diagnostic. In the
  exponential family, unlimited older compatibility requires exactly a doubling time at most K ln 2.
  Finite-age thresholds and rounded values such as 1.5 Myr must not be read as exact unlimited-age
  thresholds. These are data-selected compatibility scenarios, not estimated rates of spread or
  selection-adjusted confidence bounds.
- **C58:** the rule of three re-expresses the same oldest-find calculation. With later exposure
  L = A - c and earlier relative-rate integral R, the no-early-find probability conditional on n is
  (L/(L+R))^n. Its 0.05 boundary is K = L(0.05^(-1/n) - 1). At the later rate estimated as n/L,
  K translates to m* = n(0.05^(-1/n) - 1), about 3.09–3.32 for 48–15 finds. This is the exact
  transformation n p/(1-p) of the binomial zero-count boundary, not the conditional expectation n p,
  a known absolute rate, or a count of actual missing fossils. A delay shifts the early interval's
  start to t - d. Fixed histories retain their conditional confidence interpretation; shapes chosen
  after seeing the record have compatibility only. The exponential infinite-tail limit approaches
  the boundary, while the proxy-scaled 48-find expectations exceed it. The rule does not cover the
  age-shape tests, declining later-rate histories, Libyan spore model or 515.5 Ma argument.
- **C59:** the combined rock × spore measure is a retrospective scenario, not a fitted finding rate.
  For a time-varying measure x, integrals I_E over [A,t] and I_L over [c,A] give a conditional
  no-early-find probability (I_L/(I_L+I_E))^n. The scale E = n I_E/I_L uses the later fitted intensity;
  no constant later rate is required for this proportional history. Multiplying the two separate
  ratios instead defines a different assumed contrast between mean finding rates. The combined
  contrast permits the tested older ancestors in the absence calculation; it does not rescue a
  proportional history that predicts almost none of the observed late-Silurian finds.
  Placement expectations and binomial tails are retrospective fixed-window allocation benchmarks:
  A and both splits were chosen from age supports, so these are not calibrated rejection levels
  after selection, nor tests conditional on an exact oldest find. Regional-cell independence is
  another assumed counting scenario. The 13 and six counts are guaranteed minima under containing
  age supports; non-rejection at those minima does not establish fit. The stage-permutation benchmark
  assumes exchangeable labels and ignores temporal dependence; weak correlation cannot establish
  independent causes or justify multiplying proxies. Omitting searching from the rock product is
  a choice to avoid possible shared rock availability, not an empirical causal decomposition.
- **C60:** the minimum late-Silurian counts give a one-sided lower benchmark on the interval's
  average rate relative to the mean over the whole later window [c,A], which includes the late
  Silurian. On the reviewed inventory the 0.79/0.69 lower ratios support at least about two-thirds of that mean under the
  48/19-count scenarios (other inventories: see Inventory sensitivity); they establish neither equality nor a near-constant plateau. The exponential
  factor compares the rate at c with that at A, over 33.23 Myr, not a further 33 Myr after the Silurian.
  Coverage is nominal for fixed windows and iid draws; A and both splits are selected, as for C59.
  The absence of A-setting units from the 13 guarantees no mechanical overlap, not independence
  from that selection; a counted late find could be the true oldest fossil. Six represented regions
  do not supply six independently established rate histories. C57 rise durations require its steady
  later rate and zero delay and end at A by assumption. Neither arbitrary histories nor a switch's
  timing, biological cause or lineage age is bounded. Shared inheritance orders an innovation before
  the crown split without bounding the gap to first fossils. A young-ancestor reading additionally
  assumes prompt spread, recognisable crown bodies and adequate finding. The 1%-annual-growth example
  is arithmetic, not an ancient demographic estimate or a lower bound excluding slow net growth.
- **C61:** the three nested body groups (land-plant bodies B0, branched plants B1, crown vascular
  plants B2) on the steady-rate footing of C25–C30. Each limit is a conditional one-sided 95% upper
  confidence limit on the start of that recoverable category's record under the steady-rate absence
  model, with ages contained in their ranges. It is not a calibration-prior tail point: a clock
  maximum built from the B1 record would equal it only if the builder adopts this endpoint method,
  and the limit does not exclude a B1 start at 431.2 Ma. Hooper et al. key 431.2 Ma to the first
  unequivocal total-group tracheophyte, Irish Homerian *Cooksonia*; B1 is broader (any branched
  sporophyte), so it tests the branched-body record relevant to that rationale, not the source's own
  category. Branching and conducting cells do not establish crown placement. B1 limits span
  434.09–437.19 Ma across the four counting rules (collection 101, locality 67, locality–age 69,
  region–stage 29 units); "434.6 Ma or older" holds only for the 69-unit count and smaller counts.
  Shape verdicts cover all four inclusion states of the two cutoff-straddling units per group; a
  passing allocation shows non-exclusion, not adequacy. Gap factors are selected after seeing the
  finds and are conditional benchmarks under a two-rate model (oldest unit fixed, other units iid,
  rate ratio over a stretch against the later window): they bound average integrated finding over
  the stretch, not a sustained low rate or its cause, and carry no calibrated level after selection.
  The one-to-four extra later units are a sensitivity to named leads, not a bound on the unassessed
  younger E3 inventory.
- **C62:** a conditional requirement on the land-plant body record anchored by spores. Definite
  Borenshult-1 triletes lie below the Kinnekulle K-bentonite (454.41 +/- 0.17 Ma, C43); the analysis fixes
  the nominal age as a start before which land plants lived. Over 454.41-432.9 Ma the accepted B0
  inventory holds one unit (Oman) among 76. The quantity is the one-sided 95% upper limit on the relative
  rate rho in that span under the C48 two-rate model (all units independent draws on [c, 454.41], k = 1),
  reported as 1/rho; the without-Oman sensitivity (k = 0 of 75) equals C48's zero-delay fold at
  t = 454.41. Changes in which body forms were recognisable can contribute to lower average finding;
  any onset shared by all recognisable bodies must precede Oman. Reading: the land-plant record, which
  spores show spanned the interval, requires under this model a reduction comparable in size with C48's
  8-12 for vascular ancestors; the same rule makes them comparable. It is not a measured historical
  reduction and not a demonstration that vascular bodies shared it. Land-plant continuity leaves open
  continuity of producers, body forms and diagnostic features. Oman, if Katian, shows some B0 bodies
  recognisable within the span, weakening an explanation in which all became recognisable only at 432.9
  Ma; it does not separate encounter, preservation and searching. The comparison was chosen after seeing
  the record.

## Inventory sensitivity (Stage 2 body-fossil audit, accepted 23 November 2026)

The reviewed inventory (S0) carries every primary number. The audit repeats the body-record
calculations on S1 (S0 with Early Devonian PBDB collections restored), S2a (PBDB-backed units), S2b
(S2a with those collections restored) and Capel et al.'s species endpoints (S3). Literature curation
went mainly to the Silurian, and a duration filter had removed collections dated only to the Early
Devonian, so these are sensitivities to how the record was assembled. The gate thresholds were set
after preliminary sums: the results are a retrospective sensitivity analysis.

- **Bind every inventory value to its case:** inventory, anchor (A 426.7 Ma or the Bathurst
  Ludfordian 425.0 Ma) and run, interval, counting rule, test and proxy. Shape values also keep group,
  history and inclusion state. A minimum reduction at 444 or 452 Ma keeps its cutoff, Bathurst
  treatment, and whether it is the conservative envelope or the oldest jointly possible limit.
- **Three questions, kept apart.** C49 asks whether some assignment of ages within their ranges fits a
  declared shape over the whole window. C60 asks how finds divide between a shorter interval and the
  rest of the window. C57 asks how fast early finding must rise **before** the oldest find if the later
  rate stays level. A history can pass one and fail another: a 10 Myr exponential time constant implies
  a 27.74-fold rise across the window, beyond S2b's upper regional benchmarks, while C49 admits it on S2b.
- **Allowed:** late-Silurian crown fossils lie in six named regions in the literature-augmented
  inventories, five in Capel's main-reading endpoints (six with the literal Yea ages) and three in PBDB-backed
  units, a minimum geographical extent.
  The change in finding frequency into the Devonian depends on the inventory; a rise near the oldest
  find and a rise continuing into the Devonian both remain possible, and their timing and cause are
  unresolved. Rock area and rock × spore share predict too few late-Silurian finds on every inventory;
  the spore share predicts too few in the literature-reviewed inventories, and on PBDB-backed counts its
  verdict depends on the placement of the coarsely dated finds (only S2a's named cells, Ludfordian–Přídolí,
  A 425.0 Ma, predict too few at every admissible placement); all-collection searching predicts too few
  at every admissible placement only in S0's Ludfordian–Přídolí locality check. The 13 certain late-Silurian finds on S0 set the
  six-region minimum; the two Yea localities that reach A 426.7 Ma lie outside them. Capel's counts describe where species' first and last
  localities fall.
- **Allowed for C49 on S2b:** some age assignment within the recorded ranges passes the 10 Myr test,
  whether two or all 21 restored units are younger than 400 Ma; midpoint ages fail.
- **Not allowed:** a count of region–stage cells as a dispersal speed or population density; the
  Devonian/Silurian raw count ratio as a rate ratio (the intervals span 26.15 and 7.08 Myr); a passing
  S2b assignment as the fossils' ages; the conservative envelope where its count and age cannot occur
  together (S2b's Silurian-only regional 451.28 Ma); Capel's endpoint ratios as finding rates; a
  searching verdict without naming all-collection or plant-excluded searching and the direction tested; a
  spore-share "fit" on PBDB-backed counts without its placement; 426.7 Ma as the age of an actual find;
  a non-integer matching count rounded up across a whole-find boundary (24.95 matches 24 whole finds).
- **Figure 3b** names the proxies by what they measure; its caption states the inventory dependence
  of the spore comparison.

**C54 source limit:** use only the primary-source-supported Saudi and Turkish review entries for
the stage-level comparison with Libya. The British review entries conflict with cited primary
evidence for true triletes, and the Belgian entry lacks a primary-source check here. Raw extraction
is preserved; overlapping stage enclosures do not establish actual contemporaneity or crown affinity.

## B0 and the spore comparison

- **Canonical B0** includes the Katian Oman sporangial fragments as one locality–age unit with oldest
  possible age 452.8 Ma (C40). The former inventory is an exclusion sensitivity (C28).
- **Allowed:** including the fragments moves the main-reading constant and collection-density bounds about
  20 Myr older (other histories and readings move by other amounts; Table S3b); the endpoint is
  controlled by the oldest admitted unit; the allocated-age diagnostics fit the augmented sequence poorly (C41); in the
  completed interval-feasibility search on the reviewed inventory, no admissible allocation of the
  recorded supports lets any declared history pass that conditional-age diagnostic (C49; see Shape
  diagnostics); with the Early Devonian collections restored, the 25 Myr decline passes with the fragments
  (C49, C61). This is not a rejection of a biological history.
- **Not allowed:** any lag, delay or "interval" between lineage origin and body recoverability, in either
  direction ("about 20 Myr after", "almost at once"); 458.2 Ma as an origin (it is a fossil minimum).

## Shape diagnostics

- Asymptotic KS p values, computed on allocated ages treated as exact; ranges are 5th–95th percentiles
  over 256 allocations (C31, C41).
- **Allowed:** on the reviewed inventory, the 10 Myr decline fails the conditional-age diagnostic under every admissible allocation
  of the recorded supports, for B2 in all four inclusion states and for canonical B0; every canonical B0
  history fails likewise; the 25 Myr decline and plant-excluded density × 10 Myr decline have passing B2
  allocations when cutoff-straddling units are counted (C49). Constant intensity is not shown adequate.
- **Finite-sample reference primary** (GPT-6 Pro follow-up review, 7 November). The 25 Myr decline
  passes with all 50 possible B2 units, falls just short with 49 (passes only asymptotically) and fails
  with 48; the combined history passes with 49 or 50 but not 48.
- **Allowed:** a failure over every admissible allocation as a conservative rejection of that fixed
  history for this diagnostic, under an observation model in which the supports contain the true ages
  and inclusion state almost surely. The finite-sample reference, independent continuous occurrence
  model, history, cutoff, timescale, inventory and unit rule are fixed. The rejection event is contained
  in that of the exact-age test; if support containment can fail with probability delta, the direct
  error-rate bound is alpha + delta. Geological ranges have no demonstrated joint coverage. Maximised-p
  nuisance-parameter methods (Berger and Boos 1994) are related, rather than the justification for
  treating these coarsened observations as an error-free support set.
- **Not allowed:** "rejected" or "falsified" for a biological history without those conditions, or as
  an unconditional error rate (geological ranges are not demonstrated simultaneous confidence sets); a
  witness allocation read as the true ages, a probable chronology or evidence of adequacy; the asymptotic
  reference as primary; model selection.

## Trait-to-node links

- Tracheids would improve anatomical placement but would not by themselves place a fossil inside crown
  Tracheophyta.
- The 0.977 persistence (C19) is conditional on character coding, model, tree and chronology; it is not the
  share of extinct local producers that made recognisable trilete monads.
- A trilete mark alone does not place its producer in the crown.

B1 admission requires E3 branching or E5 crown membership; E4-only tracheid evidence is insufficient.
