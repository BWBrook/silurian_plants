# GPT-6 Pro stage 2: Claude's check and integration

Claude Opus 5.5, 7 November 2026. Barry relayed Codex's stage-2 closure through the Board Messenger
("Next: Claude — integrate the analyses and complete the semantic review."). Codex's handoff is
`2026-11-07-stage2-handoff.md` (commits `78c8c69`, `a61d120`).

## Independent checks before acceptance

Each new claim was checked against its evidence by a route separate from Codex's code.

| Claim | Check | Result |
|---|---|---|
| C48 frontier | Closed form $(A-c)(0.05^{-1/n}-1)/(T-A)$ with $A$ = 426.7, $c$ = 393.47, $n$ = 48 | 0.475557, 0.123700, 0.105419, 0.084585 at 431.2/444/447/452 Ma: exact match |
| C49 interval witnesses | KS $D$ recomputed from `normalised_exposure` in the witness files; allocated ages checked against supports | B2 possible decline25 0.1824472; combined decline10 0.1866488; B2 guaranteed decline25 0.2032896; pure decline10 0.3464309: exact match; all allocations inside supports |
| C50 timescale | Constant-history endpoint $c + (A-c)\,0.05^{-1/n}$ from each scenario's $A$, $c$, $n$ | all_younger 427.307, all_older 430.421: match |
| C51 Murzuq dependence | Own implementation (scratch, not committed): Gamma(2,2) frailty by Gauss–Laguerre quadrature, profiled reference rate, block weights from the sample table | First pass used fractional exposure $q\,r f$ for Darriwilian cuttings and gave 0.0906/0.0830/0.0991/0.3889/0.4147. With Codex's convention, a uniform-age mixture $(1-q)+q\,e^{-rf}$, all five match exactly (0.091030, 0.083242, 0.099513, 0.393002, 0.418871). The convention is the defensible one (a cutting older than 459.1 Ma has no producers under the sustained history); the fractional-exposure alternative moves results by under 1%. |
| C52 influence | Constant-history endpoint from $A$ and $n$ after each removal | Yea 427.170, Bathurst 429.098, *C. barrandei* (B1) 432.324: match |

C48–C52 are therefore marked supported. C48 and C49 values were extended (later/earlier ratios,
region–stage and curated contours, the guaranteed-unit decline25 bound, the negative certificates)
from the same evidence files; C50 gained the margins to the maximum, C51 the leave-one-well range and
C52 the B0 *C. barrandei* change.

## What changed in the paper

- **Abstract and §3.2.** The Murzuq limit is stated as conditional on independent cuttings; block
  weighting by well and formation or stage support gives 0.39–0.42. New Supplement S2.5, Table S1b and
  Fig. S2 (time support by well). "Rejects" became "under the model, excludes".
- **§3.3 and §4.1.** The illustrative tenfold scenario is now one point on the age–intensity frontier
  (Table S9b): starts at 444–452 Ma need earlier records 8–12 times rarer under primary units, 2.4–4.5
  times under coarser units; 431.2 Ma needs no reduction under coarser units. Shared timescale
  scenarios (Table S6b) keep the constant and effort-tracking bounds younger than the maximum under all
  three comparisons; the 25 Myr decline crosses. Influential-record changes are reported with signs.
- **Shape diagnostics.** The interval-feasibility result replaces "disfavoured" language: the 10 Myr
  decline fails under every admissible allocation (B2, all four inclusion states); the 25 Myr decline
  and plant-excluded density × 10 Myr decline have passing allocations when straddling units are
  counted; every canonical B0 history fails in every state (Table S7b). Earlier drafts had listed the
  25 Myr decline as fitting poorly on drawn allocations; S7 records this.
- **S5.1.** The B1 admission repair (E4-only tracheid records) and the Xiemisitai West Junggar
  correction are explained (Liu et al. 2024 added to references after Crossref check).
- **Brief.** Finding 2 notes the independence assumption; finding 3 replaces the tenfold case with the
  frontier. Still two A4 pages.
- **Agent guide and estimands.** Stage-2 section integrated; traps 21–24 added; `estimands.md` now
  allows the interval-wide statements and forbids reading witnesses or optimised p values as dates or
  calibrated tests.
- **Bindings.** 51 new value bindings (V053–V103) for C48–C52 spans. Legacy pooled claims are not yet
  migrated.

## Semantic review (Claude's pass)

All four renderings were scanned against `estimands.md` for: lag or delay statements, "fossilisation",
"rejects"/"falsified" for biological histories, clock ranking, constant intensity as preferred,
witnesses as dates, and frontier contours as fitted rates. One sentence was changed (§3.2, "rejects" to
"under the model, excludes"). This is a self-review; Codex's independent semantic review is the
remaining step of stage 4.

## Checks

- `make -C manuscript check`: 52 claims (50 supported, 2 superseded), all cited, 0 errors, 0 warnings;
  makedoc lint and reference audits pass.
- `make check-public`: 60 passed.
- PDFs rebuilt: manuscript 20 pages, supplement 24, brief 2. Tables S1b, S6b, S7b, S9b and Fig. S2
  inspected in the rendered supplement.
