You are vetting the oldest dispersed-spore reports for a palaeobotany research dataset in this repository (read AGENTS.md; do not edit any file).

Input: data/spores/work/codex/cambrian/vet_docs.csv lists 10 documents from Palynodata, a palynology literature database to 2006. Each document reports taxa that Palynodata classes as "spores or pollen" in rocks it dates to the Precambrian, Cambrian or Early Ordovician (Tremadocian–Floian). They entered the project's window when it was widened to the Cambrian on 2026-10-28. For each document you have its year, authors, title, journal, locations, the ICS stage range assigned to its records, and its taxa with our spore class (cryptospore monads, dyads and tetrads; trilete spores; other spores; "unclassed" where our genus crosswalk has no class). data/spores/work/codex/vetting/wellman2013_references.txt lists the references that Wellman, Steemans & Vecoli (2013) used for their curated Ordovician–Silurian spore list.

For EVERY document (all 10; copy doc exactly) return:
- verdict:
  - accept: a credible record of embryophyte-type spores (or of the cryptospore-like palynomorphs that some authors include with cryptospores) at this age;
  - doubtful: plausible but questioned, poorly dated, possibly contaminated or reworked, or not corroborated;
  - reject: widely regarded as erroneous, e.g. Precambrian or Cambrian "spores" later shown to be acritarchs, other algae, contamination, or misdated rocks.
- in_wellman2013: yes, no or unclear.
- reason: one or two sentences, specific about which taxa or age claim the verdict concerns. Where the material is Cambrian–Early Ordovician cryptospore-like palynomorphs (irregular dyads and polyads, envelope-enclosed clusters), say so explicitly and say which reading the literature gives (charophyte-grade, transitional, or embryophyte), because the project carries those as a separate disputed reading.
- checked: what you consulted.

Points to weigh:
- Soviet reports from the 1950s–1970s (e.g. Naumova, Timofeev) of Precambrian and Cambrian land-plant spores are generally regarded as acritarchs, contamination or misidentification;
- Cambrian cryptospore-like palynomorphs (e.g. Strother and colleagues; Taylor and Strother) are real microfossils of disputed affinity, not demonstrated embryophyte spores (Wellman et al. 2022; Hooper et al. 2026);
- cryptospores are accepted from the Dapingian–Darriwilian (Rubinstein et al. 2010; Strother et al. 1996), and trilete spores from the Katian, with Sandbian reports contested;
- a document with only Ordovician-younger spores but some Cambrian-dated rows may be a dating or database error: say so.

Use web search where it helps. Do not invent sources. Return JSON only, matching the schema, for all 10 documents.
