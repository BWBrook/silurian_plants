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

**C54 source limit:** use only the primary-source-supported Saudi and Turkish review entries for
the stage-level comparison with Libya. The British review entries conflict with cited primary
evidence for true triletes, and the Belgian entry lacks a primary-source check here. Raw extraction
is preserved; overlapping stage enclosures do not establish actual contemporaneity or crown affinity.

## B0 and the spore comparison

- **Canonical B0** includes the Katian Oman sporangial fragments as one locality–age unit with oldest
  possible age 452.8 Ma (C40). The former inventory is an exclusion sensitivity (C28).
- **Allowed:** including the fragments moves the conditional bounds about 20 Myr older; the endpoint is
  controlled by the oldest admitted unit; the allocated-age diagnostics fit the augmented sequence poorly (C41); in the
  completed interval-feasibility search, no admissible allocation of the
  recorded supports lets any declared history pass that conditional-age diagnostic (C49; see Shape
  diagnostics). This is not a rejection of a biological history.
- **Not allowed:** any lag, delay or "interval" between lineage origin and body recoverability, in either
  direction ("about 20 Myr after", "almost at once"); 458.2 Ma as an origin (it is a fossil minimum).

## Shape diagnostics

- Asymptotic KS p values, computed on allocated ages treated as exact; ranges are 5th–95th percentiles
  over 256 allocations (C31, C41).
- **Allowed:** the 10 Myr decline fails the conditional-age diagnostic under every admissible allocation
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
