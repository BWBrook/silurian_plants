You are extracting dispersed-spore records from one paper for a palaeobotany research dataset in this repository (read AGENTS.md; do not edit any file).

Paper: {CITATION} (DOI {DOI}). Full text: {TEXT_PATH}. Read the WHOLE text, including tables and figure captions; species lists are often in tables or plate explanations.

Extract every assemblage of Darriwilian–Emsian (Middle Ordovician to Early Devonian) dispersed spores that the paper reports: cryptospores (monads, dyads, tetrads, hilate forms) and trilete spores. An assemblage is one sample, one section interval or one formation-level list, whichever the paper reports; say which in scope. Do not extract acritarchs, chitinozoans or other marine palynomorphs as occurrences, but note in the assemblage notes if they were the main focus, or if spores were sought and not found.

For each assemblage:
- Place: locality, country, formation, section or core, and depth or level, as reported. Give coordinates only if the paper gives them (else ""). palaeogeo_unit_reported is the paper's own palaeogeographic term; palaeo_unit_proposed is your mapping to the schema's units (Avalonia: England, Wales, SE Ireland, Belgium, Rhenish Massif; Laurentia: Scotland, N America west of the Appalachian suture; Baltica; peri-Gondwana-Europe: Armorica, Iberia, Bohemia; Gondwana units by continent; South-China; and so on).
- Age, exactly as reported, never converted. age_as_reported is verbatim; age_basis is the evidence; age_circular is true if the spores themselves date the rock. stage_min_proposed and stage_max_proposed are your mapping to ICS v2024/12 stage names (data/timescale.csv); leave them "" if unclear.
- Setting: setting_as_reported, setting_class, n_samples, reworking_status.
- locator: where in the paper the assemblage is reported (section, table, figure or page).
- occurrences: every spore taxon reported for the assemblage.
  - taxon_as_reported: copied character for character as printed, including abbreviated genera
    (e.g. "A. parvus") and qualifiers such as "?" or "cf." in their printed position. Never expand
    or correct it here.
  - genus: the full genus name, with any abbreviation expanded from the paper. This is where expansion goes.
  - qualifier: one of "", cf., aff., ?, sp., spp., indet.
  - abundance: as reported, or "present".
  - illustrated: true or false.
  - locator: table, plate or page.

In doc:
- doi, citation and language.
- reports_window_spores: false if the paper has no Darriwilian–Emsian spore assemblage; then return an empty items list.
- comment: a short summary of anything a curator should know, such as disputed ages, reworking or the reuse of material from earlier papers (name the earlier paper).

Do not invent anything: if a field is not reported, use "" or the schema's unknown value. Return JSON only, matching the schema.
