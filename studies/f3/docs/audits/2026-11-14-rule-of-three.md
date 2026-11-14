# The rule of three behind the body-fossil results

Claude (Opus 5.5), 14 November 2026, answering Fable 5.2's issue 1 (relayed by Barry the same day).

## The rule and its derivation

With the finding rate level after the oldest possible age *A* = 426.7 Ma, zero delay, *n* finds counted in
[*c*, *A*] (*c* = 393.47 Ma) and the one-sided 95% limit, write *R* for the integral of the relative earlier
finding rate over [*A*, *t*] and *L* = *A* − *c*. Each find falls before *A* with probability
*p* = *R*/(*L* + *R*); no early find has probability (1 − *p*)^*n*, which equals 0.05 at
*R* = *K* = *L*(0.05^(−1/*n*) − 1). At the later rate *n*/*L*, the boundary holds
m\*(*n*) = *n*(0.05^(−1/*n*) − 1) expected early finds: 3.09 (48), 3.19 (24), 3.24 (19), 3.32 (15), tending
to ln 20 = 3.00. This is the binomial zero-numerator rule of three (Hanley and Lippman-Hand 1983, JAMA
249:1743–1745, DOI 10.1001/jama.1983.03330370053031, Crossref, second author from PubMed 6827763 because
Crossref omits her; Jovanovic and Levy 1997, Am. Stat. 51:137–139, DOI 10.1080/00031305.1997.10473947).

`studies/f3/models/loop3/rule_of_three.py` asserts that every steady-rate limit, step ratio, linear and
exponential rise, minimum delay, the 431.2 Ma crossing (n = 23.588, m\* = 3.19) and the outside-measure
matches sit at m\*(*n*) (`out/rule_of_three.csv`; claim C58, provisional until Codex or Barry checks it).

## Where it holds and where it misleads

- **Conditions.** A level finding rate after *A*; the count *n* and cutoff *c*; zero delay, or the count
  starting at *t* − *d*. It covers the crown vascular-plant body record, not the Libyan spore model or the
  515.5 Ma argument.
- **The count question stays.** The later rate is estimated from the same *n*, so "three finds" is fixed
  while the time three finds take scales as *L*/*n*. The rule localises the count dependence; it does not
  resolve it.
- **Expected, not missing.** Three is a ceiling on expected early finding for compatibility, not a count of
  unseen fossils.
- **Confidence.** For fixed histories the boundary is the 95% limit; for shapes placed after seeing the data
  (step, rises) it is compatibility only.
- **Outside measures.** Expected early counts under proxy scaling (7.6–11.5 for rock, 4.9–5.1 for the spore
  share, at 48 finds) assume finding proportional to the measure in both windows, which is untested.
- **Shape tests and declining histories** (Results (d), second paragraph) lie outside the rule.

## Text changes

The rule is stated once in Material and methods (g) with its derivation and sources, and opens Results (d);
(e)–(g), the Discussion and the Conclusion lean on it. The Abstract (200 words) fell from 21 numerals to 13.
Cut from the Abstract: the 28/18 Libyan counts (now "most"), 434.05 Ma, the doubling times, the rock and
spore ratios (3×, 5–7×). Cut from the Conclusion: the 0.091 and four-tenths Libyan figures, the 2.4–12 and
15–23 requirements and the proxy ratios, all kept in Results.

## Meaning checks

`gpt-6.1-sol` checked every changed passage (`2026-11-14-rule-of-three-meaning-check.json`): the rule holds;
six passages needed repair, including one error of mine (the Conclusion had dropped "steady" and "since
459.1 Ma" from the Libyan supply limit, generalising C24). All were repaired. The recheck
(`2026-11-14-rule-of-three-meaning-recheck.json`) resolved five; the remaining two (the Abstract's
steady-rate delay condition and proxy scope; Results (d)'s scope sentence) were then repaired as proposed.
Final small trims to fit 200 words ("by count", "take longer", "the literature's trilete-reporting share")
were not rechecked.
