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
