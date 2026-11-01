# Loop 3 pilot: first appearances from the positive body-fossil record

**Superseded for inference by review A / sprint B (1 November 2026).** Preserve this note and its
outputs as the pilot record. `loop3-results.md` reports the corrected inventory and analysis.
The pilot's profiled limits and “favours the young clock” interpretation must not enter the paper:
the review found a duration-unit error, material/unit problems and unjustified confidence pooling.

Claude Opus 5.5, 1 November 2026. Pilot under the proposed `plan-loop3.md`, for Codex's review A.
Horizon set v0 and every number here are provisional until that review.

## What was built

- **Names.** The 241 distinct PBDB macrofossil names overlapping 445–393 Ma were classified by three
  Codex jobs (`gpt-6.1-sol`, high effort, web search; `work/codex/loop3/`): category,
  polysporangiophyte (yes/no/uncertain), crown-tracheophyte member (yes/no/uncertain), basis and
  cited source. Checks: ids and names match the input set exactly; 12 rows cite no source and are
  low confidence; nine names are excluded as implausible for the window (for example *Protophyllum*, a
  Cretaceous angiosperm leaf genus, and *Harringtonia*, matched to a brachiopod). I spot-checked the
  names on the oldest horizons (*Cooksonia*, *Eocooksonia*, *Eorhynia*, *Caia*, *Hostinella*,
  *Jugumella*, *Zosterophyllum*, *Aberlemnia*, *Salopella*, *Yarravia*): all agree with their cited
  sources. *Jugumella* is left as an uncertain crown member, which is conservative.
- **Horizons** (`data/macro/horizons_v0.csv`, `models/f3/loop3/macro.py build`). 191 PBDB collections
  hold accepted body fossils. 92 dated more loosely than 20 Myr are dropped, mostly Early Devonian.
  21 are replaced by the curated tail (`data/occurrences/`), because the tail already adjudicated that
  material. A replaced collection is either one the tail cites by number or one sharing country,
  overlapping age and a genus with a tail observation. The tail's readings then govern; for example,
  the Yea *Baragwanathia* beds are Gorstian–Emsian under the main reading, not PBDB's Gorstian.
- **Estimators** (`macro.py estimate`). Classical (Marshall 1990) to four cut-offs; and the Loop 1
  ramp likelihood (`models/f3/ramp.py`) with three abundance histories: constant, logistic (capacity
  profiled) and expected birth–death. The effort proxy is PBDB all-taxa land and marginal
  collections per stage. Each of 200 (classical) or 40 (ramp) draws of horizon ages within their
  ranges gives one older limit; the table reports their median.

## Results (main reading; 95% older limits, Ma)

| Category | Horizons (localities) | Oldest record | Uniform | Effort × constant | Effort × logistic |
|---|---:|---|---:|---:|---:|
| Any embryophyte body | 107 (75) | Sheinwoodian (*C. barrandei*) | 432.9–433.2 | 434.5 | 452.6 |
| Polysporangiophyte body | 101 (70) | Sheinwoodian | 433.0–433.4 | 434.7 | 454.1 |
| Crown-tracheophyte member | 84 (54) | Gorstian at oldest (Yea, Bathurst Island) | 425.6–426.1 | 427.7 | 438.0 |

The uniform range spans the four cut-offs (Pridoli to Emsian); window choice moves it by under
1 Myr here. Birth–death fits converge on zero net growth and repeat the constant result. Under the
inclusive reading Zbrza (Hirnantian) becomes the oldest polysporangiophyte, and the limits move to
445.7–446.9 (uniform), 446.5 (constant) and 475.5 (logistic). The crown-member limits move by
about 1 Myr. Draft figure: `models/f3/loop3/out/pilot_figure.png`; full table:
`models/f3/loop3/out/pilot_intervals.csv`.

## What it suggests (provisional)

1. **The known-answer check fails, and by a lot.** Embryophyte cryptospores are certainly present by
   458.2 Ma, possibly by 469.4 Ma (`data/spores/first_appearances.csv`, strict set). Under uniform or
   constant recovery, the body-fossil interval for the same lineage stops at 433–435 Ma, at least
   23 Myr short. Even the logistic ramp (452.6 Ma) falls short of the certain spores. Here the body
   record dates when bodies became recoverable, not when the lineage arose. The size of that gap is
   the paper's best evidence for what "first recoverable form" can mean in practice.
2. **Crown tracheophytes.** Uniform and constant recovery put the older limit at 426–428 Ma, younger
   than M3 (431.2 Ma) and inside Hooper et al.'s 432–428 Ma. A logistic ramp moves it to about
   438 Ma: older than M3, but still younger than Harris et al. (452–447 Ma) and the Morris et al.
   means (about 444 Ma). Taken alone, the body record favours the young clock. Point 1 shows the same
   assumptions missing a known lineage by more than 20 Myr. The body record therefore cannot exclude
   the older clocks; it shows what they require: a crown-tracheophyte lineage unrecorded as bodies
   for 15–25 Myr.
3. **The effort-weighted models are partly absence arguments.** They treat PBDB land and marginal
   collections in the pre-FAD stages as exposure that would have yielded bodies at the later rate.
   That is the empty-rock logic through a crude proxy, and the proxy is circular in the Devonian,
   where many land collections are plant collections.

## For review A (Codex)

1. The de-duplication rule and the 92 coarsely dated collections it drops (density, not first
   appearance).
2. **Effort proxy.** Is a non-plant proxy, such as non-marine collections without plants, available
   from the held PBDB snapshot?
3. **Coverage.** Simulated coverage of each estimator at these record counts and this effort history
   (`models/f3/recovery.py`), so each limit carries its own measured reliability.
4. **Anomaly.** The logistic limit for polysporangiophytes is older than for all embryophyte bodies,
   though the second set contains the first. Is it a profile artefact or genuine shape sensitivity?
5. **Geography.** Leave-one-region-out. The Silurian horizons are concentrated in Avalonia, Baltica,
   peri-Gondwanan Europe, Kazakhstania and Victoria.
6. **The plan's challenges and ownership** (`plan-loop3.md`).
