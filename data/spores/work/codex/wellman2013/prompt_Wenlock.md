You are digitising a published table for a palaeobotany research dataset in this repository (do not edit any file).

Input: data/spores/work/codex/wellman2013/chunk_Wenlock.txt is one series section (Wenlock) of the line-numbered text of the supplement to Wellman, Steemans & Vecoli 2013 (Geological Society Memoir 38, ch. 29; CC BY 4.0). It lists Ordovician–Silurian dispersed-spore assemblages under series headings (Tremadoc, Arenig, Llanvirn, Caradoc, Ashgill, then the Silurian series). Each entry reads "Region (subregion) – Country, locality: taxon list (references)." Entries wrap across lines, and page furniture may intrude.

Return one item per entry, in document order:
- series_as_given: the heading in force.
- region_as_given: the text before the dash, e.g. "Peri-Gondwana (Armorica)".
- country.
- locality: the text after the country and before the colon; empty if none.
- questionable_affinity: true if the entry's taxa are asterisked as spore-like palynomorphs of questionable affinity.
- taxa: one object per taxon.
  - as_written: exactly as printed, without the asterisk.
  - expanded: abbreviated genera expanded from the most recent genus with that initial in the same entry, keeping "?", "cf.", "aff." and "sp." qualifiers.
  - genus_ambiguous: true when that expansion is doubtful, for example when the same epithet appears elsewhere in the document under a different genus with the same initial.
- references: each citation as written, e.g. "Burgess 1991".
- source_line: the line number where the entry starts.

Do not drop, merge or invent entries. Return JSON only, matching the schema.

This chunk holds about 27 entries (count the lines containing " – " that start an entry). Read the WHOLE chunk file, not just its start, and return every entry. If your count differs from 27, say why in a final item with series_as_given "NOTE" and the explanation in locality.
