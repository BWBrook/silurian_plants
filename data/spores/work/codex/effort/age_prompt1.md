You are extending a stratigraphic crosswalk for a palaeobotany research dataset in this repository (read AGENTS.md; do not edit any file).

Input: data/spores/work/codex/effort/ages1.csv lists 94 age names that Palynodata, a 2006 palynology literature database, uses for Ordovician–Devonian palynomorph records (mostly acritarchs and chitinozoans), with row counts. The existing crosswalk for other names is data/spores/crosswalks/age_names.csv; follow its conventions and correlations exactly, so that the two are consistent. The target stages are the ICS v2024/12 stages in data/timescale.csv, Tremadocian to Tournaisian.

For EVERY age name (all 94; copy age_name exactly; read the WHOLE file) return:
- ics_oldest and ics_youngest: the oldest and youngest stage names exactly as in data/timescale.csv. If the unit reaches beyond the table, clamp to the end stage, say so in basis and set confidence low. Leave both empty ("") if the name is too broad or unmappable.
- confidence: high | medium | low.
- basis: a short phrase.
- source: a correlation source you actually checked, or "existing crosswalk analogue", or "none checked". Do not invent sources.

Notes:
- British Ordovician series do not align with global stages: Llandeilo is now within the Darriwilian; Caradoc ≈ Sandbian–early Katian; Ashgill ≈ late Katian–Hirnantian.
- Regional names (Baltic, Russian, North American, Chinese) need regional correlation charts; use web search where needed.

Return JSON only, matching the schema.
