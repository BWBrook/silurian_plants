# Outside rulers for the earlier/later finding-rate ratio (pre-specification)

Claude Opus 5.5, 12 November 2026, written before the rulers were computed. Barry, chat, 12 November
2026: the paper says older vascular-plant dates need early fossils found 2.4–12 times less often, "A
reader's next question is obvious: is ten times a lot or a little?"; he proposed three rough outside
measures, rock, searching and spores, shown side by side.

## Target

The frontier (C48, C55) gives the ratio R(t) of the later to the earlier constant finding rate at which a
candidate ancestor age t (zero delay) sits on the 95% limit, with the step at A = 426.7 Ma and the
younger cutoff c = 393.47 Ma. Each ruler is a proxy density x(s) through time, and its ratio is

    Q(t) = mean of x over [c, A] / mean of x over [A, t],

time-weighted within stages. Q is computed for t = 431.2, 444, 447 and 452 Ma and as a curve over
427–456 Ma for figure 3b. Q > 1 means the proxy was lower before A.

## Rulers (fixed before computing)

1. **Rock.** Macrostrat units in active North American columns (`data/eprp/record/macrostrat_units_window.csv`).
   x(s) = summed column area of units with `d_env_class` non-marine spanning s. Variant: non-marine plus
   `both`. Secondary: South America, reported but not used for the band (coarse).
2. **Searching.** PBDB land and marginal-marine collection equivalents per Myr (`data/macro/effort_reviewed.csv`,
   global), all collections and plant-excluded. Disclosed in advance: a rough hand sum of the all-collection
   series gave about 1.4 at 444–452 Ma before this plan was written; Barry's rock sum gave about 3.
3. **Spores.** Fraction of Palynodata documents reporting a usable trilete record among all Palynodata
   documents with a usable-age record, per stage, distinct documents across regions (new output
   `data/spores/effort_global_by_stage.csv`; same age, span, location and exclusion filters as
   `effort_by_stage.csv`; trilete rows exclude reworked or caved flags). Palynodata stops in 2006.

## Reading

The rulers are proxies, not estimates of the finding rate, and they enter no 95% inference. Rock and
searching bear on the chance of preservation and collection; spores bear on how common trilete producers
were, a wider group than crown vascular plants. They are reported side by side; no product or combined
factor is formed. Each Q is compared with R(t) for 48 finds (8.1–11.8 at 444–452 Ma) and for 19 or 15
(2.4–4.5). The paper states which counts and delays each ruler is consistent with, whichever way it falls.

## Addendum: shapes of an early rise (12 November 2026, before computing)

Barry, chat, 12 November 2026, proposed a rise in finding rate followed by a level stretch, as plants
spread from a few patches, in place of the step, with his hand sums: a straight-line rise from the
ancestor reaches only about 431, 438 and 441 Ma (48, 19, 15 finds); an exponential rise reaches 444–452 Ma
if finds doubled about every 1.5, 4 and 5–6 Myr. To be computed in `models/f3/loop3/rise_shapes.py`, with
the finding rate level after A = 426.7 Ma and rising before it:

- For any fixed history, an ancestor age t is compatible with the 95% limit when the integral of the
  relative finding rate over [A, t] is at most K(n) = (A − c)(0.05^(−1/n) − 1); the step frontier is the
  special case of a constant earlier rate. Tabulate K for n = 48, 24, 19, 15.
- Linear rise from zero at t to the later level at A: the oldest compatible t, A + 2K.
- Exponential rise (time constant τ, doubling time τ ln 2): the τ at which t = 444, 452 and 500 Ma sits on
  the limit, and the limiting τ = K as t grows without bound.
- Cross-check both against the reviewed `endpoint.known_cutoff_summary` with piecewise-constant
  histories.
- Spore context: the stage-level share of Palynodata documents reporting usable triletes
  (`effort_global_by_stage.csv`) and the doubling time implied between the midpoints of Hirnantian and
  Rhuddanian, and of Homerian and Gorstian. Disclosed in advance: an earlier, uncorrected numerator gave
  shares near 0.02 (Katian), 0.03 (Hirnantian) and 0.10 (Rhuddanian). As with the rulers, these are
  guides for comparison and enter no 95% inference; the shapes are placed after seeing the record.
