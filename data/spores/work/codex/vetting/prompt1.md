You are vetting early dispersed-spore records for a palaeobotany research dataset in this repository (read AGENTS.md; do not edit any file).

Input: data/spores/work/codex/vetting/docs1.csv lists 61 documents from Palynodata, a palynology literature database to 2006. Each document reports spore taxa in Ordovician to early Silurian rocks, older than the Wenlock. For each document you have its year, authors, title, journal, locations, the ICS stage range assigned to its records, and its taxa with our spore class: cryptospore monads, dyads and tetrads; trilete spores; and other spores. data/spores/work/codex/vetting/wellman2013_references.txt lists the references that Wellman, Steemans & Vecoli (2013) used for their curated list of Ordovician–Silurian spore assemblages, which omits poorly dated, poorly preserved or doubtfully identified assemblages.

For EVERY document (all 61; copy doc exactly) return:
- verdict:
  - accept: a credible record of these spore types at this age;
  - doubtful: plausible but questioned, poorly dated, possibly contaminated or reworked, or not corroborated;
  - reject: widely regarded as erroneous, e.g. trilete spores claimed from the Lower–Middle Ordovician in early studies and not confirmed, or a dating later revised out of this age.
- in_wellman2013: yes if the document's author-and-year citation appears among the Wellman et al. references; no; or unclear.
- reason: one or two sentences. Be specific about which taxa or age claim the verdict concerns. A document may be credible for its cryptospores but doubtful for its trilete spores; say so.
- checked: what you consulted (e.g. "Wellman 2013 list", a later review, or "title and taxa only").

Points to weigh:
- trilete spores are now generally accepted from the Katian onward (e.g. Steemans et al. 2009) and contested earlier;
- cryptospores are accepted from the Dapingian–Darriwilian (e.g. Rubinstein et al. 2010; Strother et al. 1996);
- Hooper et al. (2026) regard a Sandbian Swedish trilete record as doubtful;
- many pre-1980 Soviet and French reports of Ordovician trilete spores are considered contamination or misidentification.

Use web search where it helps. Do not invent sources. Return JSON only, matching the schema, for all 61 documents.
