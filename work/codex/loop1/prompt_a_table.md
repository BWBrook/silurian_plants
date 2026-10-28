Digitise one published table. Do not edit any file; return JSON only.

Input: `work/codex/loop1/wellman2022_table1.txt`, the text layer of Table 1 of Wellman, Cascales-Miñana & Servais (2022), "Terrestrialization in the Ordovician", Geological Society London Special Publications 532 (CC BY). It lists dispersed spore assemblages reported from the Ordovician. The PDF text layout wraps cells across lines and page breaks interrupt the table ("Downloaded from ..." lines and running headers are not table content).

There are exactly 48 rows, with codes H1–H16, KH1–KH5, K1–K14, S1–S6, Dr1–Dr5, Dp1–Dp2. Return one item per row, in table order, with:
- code: as printed (e.g. "H1", "KH3", "Dp2");
- stage_printed: the stage text exactly as printed after the code, including any "?" or asterisks (e.g. "Hirnantian?", "Katian-Hirnantian?", "Sandbian*", "Dapingian**");
- location: the location cell, joined into one line (e.g. "Ontario, Canada");
- palaeocontinent: as printed;
- palaeoenvironment: as printed, joined into one line;
- age_dating: as printed (abbreviations kept: C, Ch, G, Inv, Palynology, Lithostratigraphy and combinations);
- references: the full references cell joined into one line, exactly as printed;
- footnote: "*" or "**" if the row carries that footnote mark, else "".
Also return the two footnote texts verbatim in `footnotes`.

Copy text exactly; do not correct spellings or expand abbreviations. If a cell is genuinely ambiguous because of the layout, give your best reading and say so in `note` for that row (otherwise "").
