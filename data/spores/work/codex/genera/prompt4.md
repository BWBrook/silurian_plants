You are classifying dispersed-spore genera for a palaeobotany research dataset in this repository (read AGENTS.md for its conventions; do not edit any file).

Input: data/spores/work/codex/genera/chunk4.csv holds 107 genera from Palynodata's Ordovician–Devonian spore records, with sample species names and Palynodata age spans.

For EACH genus (copy the name exactly) classify spore_class by the genus's diagnostic morphology:
- cryptospore-monad: single spores not in a trilete arrangement and of cryptospore affinity, including hilate monads (e.g. Laevolancis), alete monads and enveloped monads.
- cryptospore-dyad: permanent or dissociated dyads (e.g. Dyadospora, Pseudodyadospora, Segestrespora).
- cryptospore-tetrad: permanent tetrads, naked or enveloped (e.g. Tetrahedraletes, Velatitetras).
- trilete-laevigate: trilete spores with smooth exine, including retusoid forms (e.g. Ambitisporites, Retusotriletes).
- trilete-ornamented: trilete spores with sculpture, such as grana, verrucae, apiculae, muri or ribs (e.g. Emphanisporites, Apiculiretusispora).
- trilete-unspecified: trilete spores in heterogeneous form genera whose species include both smooth and sculptured forms, or whose sculpture is undetermined.
- other-spore: monolete spores, megaspores and other true spores outside these classes; say which in basis.
- not-a-spore: taxa that are not embryophyte spores (acritarchs, algal cysts, misfiled pollen), and names that are not genera ("Spore", "Tetrad", indet.).
- uncertain: a genus of disputed or unknown morphology.

confidence: high if the diagnosis is unambiguous and you know it; medium if inferred; low if unsure.
basis: the diagnostic feature, in a few words.
source: the original description or a standard reference (author and year). Do not invent sources: write "none checked" if you did not verify one.

Use web search for genera you are not sure of. Return JSON only, matching the schema, for all 107 genera; read the WHOLE file.
