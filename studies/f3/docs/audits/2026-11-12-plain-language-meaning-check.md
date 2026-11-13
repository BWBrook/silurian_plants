# Plain-language rewrite of the article: meaning check

Claude Opus 5.5, 12 November 2026. Barry's general point 1 on the article (chat, 12 November 2026): the
text had become "prose shaped by review", with safeguards placed before the point and an internal
dialect ("guaranteed units", "potential screen", "retrospective compatibility", "readings"). He asked
for point first, condition second, number last; one name per thing; borrowing the brief's phrasing; and
for each rewording to "go back through Sol's meaning check".

## What changed

- One vocabulary across `manuscript/text/main.md`, `text/figures.md` and the figure labels in
  `figures_main.py`: *find* (collections, taxa or papers sharing a locality and age, counted once);
  *finding rate* / *found* (replacing recording, recovery and encounter); *supply* (spore input);
  *delivery ratio*; *interpretation* (reading); *samples* (chart-coded drill cuttings); *finds certainly
  inside the window* (guaranteed units); *counting fewer independent finds* (region–stage cells or the
  curated oldest records); *95% confidence limit* for the body-fossil bound.
- Abstract, Methods (d) and (h), Results (c), (e)–(g) and the Conditions paragraphs rewritten
  plain-first. Abstract is 200 words.
- C24 gains the derived display value ~9% (0.091 as a percentage), used in the abstract.

## Sol meaning check

`gpt-6.1-sol` (high), read-only, compared old and new wording against `manuscript/estimands.md`,
`claims.csv`, the supplement and model code. First pass: 16 findings
(`2026-11-12-plain-language-meaning-check.json`), 9 rated high. The draft had (i) worded the 95% bound
as "the oldest the record could begin" and a section heading as a date; (ii) misdescribed the checking
procedure: qualification counts withheld claims as covering, among simulations passing the screen,
with a lower confidence limit on coverage above 0.93, which differs from "each reported limit contained
the truth in more than 93% of trials"; (iii) claimed the six histories were "fixed in advance", which
`docs/loop3-design.md` does not support; (iv) gave the data-selected step scenarios 95% status in the
figure 2 and 4 captions; (v) called samples "empty" rather than reporting no triletes; and (vi) changed δ
from a joint-containment failure to a single range's miss. Claude accepted all 16 and repaired them, using
Sol's wording or plainer equivalents.

Recheck (`2026-11-12-plain-language-meaning-recheck.json`): 14 resolved, 2 partly (the weighting rule for
varying supply), and 1 new problem (figure 4's 0.05 statement does not hold on the flat portions drawn at
one). All three were then repaired with Sol's wording. `make -C manuscript check` passes: 53 claims,
0 errors, 0 warnings.

## Not yet carried over

The supplement, brief and agent guide still use the earlier vocabulary. The brief follows the article
(Barry, 12 November 2026); the supplement and guide should adopt the same terms once the article settles.

## Title and message against the evidence (Barry's general point 2)

Barry, chat, 12 November 2026: the title and closing sentence concern living land plants, while the
quantitative core concerns vascular plants; "The land-plant question itself gets only the audit and one
polar basin". He proposed five titles, preferring "How long could land plants have existed before
leaving fossils?".

Sol (`2026-11-12-title-message-check.json`) judged that title, in Claude's variant "How long could land
plants have lived before their first known fossils?", to overpromise: the paper gives no such duration
for land plants, and for vascular plants only conditional bounds and data-selected scenarios. It also
rejected Claude's draft message "For living land plants and vascular plants alike…" as presenting a
shared quantitative reconciliation that was never calculated. Claude adopted Barry's second option,
"Missing fossils as evidence: what the rocks can say about the age of land plants", and rewrote the
abstract's end, Discussion paragraph 1 and the Conclusion so that each clade carries its own evidence.
The shared message is now: "Missing fossils allow older ancestors if early plants were found less often
or became recognisable later, and these records state how much less often." Sol's recheck
(`2026-11-12-title-message-recheck.json`) accepted the title and found two dropped conditions (steady
supply since 459.1 Ma; zero delay for 8–12), both restored. The title and message await Barry's
confirmation; the brief and graphical-abstract headline still carry the earlier message.

## Libya recast as a worked case of a local absence (Barry's general point 3)

Barry, chat, 12 November 2026: the Murzuq analysis rests on three wells, mostly the wrong age for the
459.1 Ma maximum, in an unusual polar basin, and its limit moves from 0.09 to about 0.4 under one
dependence check; "Present Libya as a worked case of what an absence can and cannot show, not as a test
of 459.1 Ma", with the model and its checking moved to the supplement, both ends of the limit given and
one clause in the abstract. He asked that Sol check the reading against the Swedish and Libyan ages.

Claude checked the spore compilation first. Beyond the Sandbian Borenshult triletes, trilete-bearing
assemblages in Saudi Arabia, Turkey, southern Britain and Belgium fall in the same Katian–Hirnantian
stages as the 18 later-Ordovician Murzuq samples (new provisional claim C54, from
`data/spores/occurrences.csv` and the curated Wellman et al. 2013 assemblages). Changes: Methods (d)
removed and replaced by two sentences in (c), which now also describe the spore compilation (Palynodata
and Wellman et al. 2013 added to the bibliography, DOIs from Crossref); Results (c) and (d) merged into
one paragraph giving both limits (0.091 main model; about 0.4 with well-and-unit weighting); old figure 3
moved to supplement figure S2 (`figS_murzuq`), replacing the narrower time-by-well panel; figure 4 is now
figure 3 (`fig3_requirements`).

Sol (`2026-11-12-libya-worked-case-check.json`) confirmed the ages (all 18 younger than the 454.41 Ma
bentonite; 13 Katian–Hirnantian and 5 Hirnantian), the Ashgill mapping, the C54 records and command, and
the conditions on both limits. Its one finding: overlapping stage ranges do not establish simultaneous
production, so "trilete spores were therefore being produced while these Libyan rocks accumulated" was
replaced by a stage-resolution statement, noting that five Libyan samples and Saudi and British
assemblages are all Hirnantian (about 2 Myr). C54 needs a check by Codex or Barry before it is supported.

## Counting independent finds as a headline (Barry's general point 4)

Barry, chat, 12 November 2026: "the unit choice rivals the effect… The paper reports this honestly but
treats it as a sensitivity when it is arguably a headline", and lead with the range. Claude found that the
primary (48), region–stage (19) and curated (15) bounds share the oldest find and cutoff, so all three lie
on one closed-form curve, T(n) = c + (A − c)·0.05^(−1/n), which crosses 431.2 Ma at n = 23.6, the
duplication-factor-2 case that held 0.78 coverage in Table S11. New script
`models/f3/loop3/count_dial.py` checks the curve against the reviewed bounds and frontier (provisional
claim C55). Figure 3a now plots the limit against the number of independent finds. Abstract, Methods (e),
Results (d)–(e), Discussion and Conclusion lead with the count.

Sol (`2026-11-12-count-dial-check.json`) passed the arithmetic and found three problems, all repaired with
its wording: the three treatments are counting scenarios, not estimates of the true count ("most plausibly
lies between" removed); the 15–23 Myr delays assume all 48 finds independent (now said in the abstract
and Conclusion); and the Discussion's range and crossing hold for constant recording only.

## Outside rulers for the required reduction (Barry's general point 5)

Barry, chat, 12 November 2026: "is ten times a lot or a little? The paper doesn't say"; he proposed
three rough rulers (rock, searching, spores) shown beside the requirement. Claude pre-specified them in
`docs/plan-rulers.md`, computed them in `models/f3/loop3/rulers.py` (provisional claim C56) and added
Methods (h), Results (f), supplement S5.8 with Table S14, ruler curves on figure 3b, and sentences in
the abstract, Discussion and Conclusion. At 444–452 Ma: North American non-marine rock area 3.2–3.5
times lower before the oldest find, PBDB collections 1.35–1.41, and the share of Palynodata documents
reporting usable triletes 5.1–7.1. Rock alone matches the requirement with about 14–20 or fewer
independent finds, spores with about 29–31 or fewer; the 48-find requirement (8–12) exceeds each.

Sol (`2026-11-12-rulers-check.json`) reproduced the calculations and the count inversion and found eight
problems: a spore-numerator bug (rejected groups and synonym-list rows were counted, against the plan;
fixed, raising the spore ratios from 4.98/6.67 to 5.14/7.10); "needs both / act together" exceeding the
side-by-side plan; document reporting share described as producer rarity; rock said to cover both cautious
counts at 452 Ma, where it does not; North America generalised; an endpoint range; supplement gap
boundaries and unit counts; and a narrowed figure range. Recheck (`2026-11-12-rulers-recheck.json`): six
resolved, two partly and two new endpoint points; all then repaired with Sol's wording.

## Early-rise shapes (Barry's general point 6, the gradual-spread analysis)

Barry, chat, 12 November 2026: replace the step by "a rise followed by a level stretch" as plants spread,
with hand sums for linear and exponential rises; "it gives a rate" and "shows a limit of the method".
Pre-specified in the `docs/plan-rulers.md` addendum; computed in `models/f3/loop3/rise_shapes.py`
(provisional claim C57). For any fixed history, compatibility depends only on the summed earlier
finding R(t) ≤ K(n) = (A − c)(0.05^(−1/n) − 1): 2.14, 5.68 and 7.35 Myr-equivalents for 48, 19 and 15
finds. Barry's sums were right: a linear rise reaches 431.0/438.1/441.4 Ma; an exponential rise fits
444–452 Ma with doubling times of 1.48, 4.0–4.2 and 5.3–5.8 Myr, and below the limits 1.48/3.93/5.09
Myr no older limit exists. Added: Methods (g) sentence, Results (f), Discussion sentence, figure 2a
curve, supplement S5.9 and Table S15.

Sol (`2026-11-12-rise-shapes-check.json`) passed the derivation and reproduced both outputs; four
repairs, all made: requirements stated as requirements, not as a measured rate of spread ("the record
measures how quickly plants became findable" removed); the Homerian–Gorstian spore comparison spans A and
is coarse context only; the script's cross-checks described exactly; and the figure's limiting rise given
as 1.48 Myr, since a literal 1.5 Myr doubling has a finite endpoint near 436 Ma.

Abstract (Barry, chat, 12 November 2026: "Yes, make room"): the rise result now has one clause in the abstract, at 200 words. Sol (`2026-11-12-abstract-rise-check.json`) found it had dropped the exponential form and the count dependence; both restored with its wording.

## 13 November: plain wording for Codex's precision repairs

Codex's review (`07e9866`, `docs/audits/2026-11-13-general-points-review.md`) corrected C54–C57 and
was accepted in substance. Its new wording reintroduced the dialect and in-claim negations the
12 November pass removed ("oldest-find calculation", "finite older compatibility limit", "does not
establish"). Claude (Opus 5.5) restated those passages plainly and moved the plateau, spread and
proxy-transfer qualifications into the Discussion's Conditions paragraph. The abstract quotes the
exact-safe thresholds 1.48–5.09 Myr (below K ln 2 for 48 and 15 finds). The Conclusion restores the
agreed message, scoped to vascular-plant ancestors, with the Libyan spores kept to local absence.

Sol meaning check (`2026-11-13-codex-repair-plain-check.json`, 12 passages): 7 ok, 5 risk or error,
all repaired as Sol proposed except where noted:
- delays "15–23 Myr" are rounded minima (15.16, 23.16), so exactly 15 falls short: now "about 15–23
  Myr or more" in the abstract, Results (e) and Conclusion (an error that predates this pass);
- the proxy comparison overlaps *some* cautious requirements (abstract, Results (g) heading);
- the Discussion now says an older limit needs an assumption restricting the early history, the
  general form, not specifically its rise speed;
- proportionality in Conditions is stated as sufficient, with a common constant, not necessary;
- the Conclusion keeps Barry's message instead of Sol's replacement, scoped to vascular plants and
  separated from the spore result by a semicolon.

Claims check after the repairs: 57 claims cited, 0 errors, 0 warnings; abstract 199 words.
