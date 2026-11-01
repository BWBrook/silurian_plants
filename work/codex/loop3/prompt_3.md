Classify fossil plant names from a Paleobiology Database (PBDB) extract for a study of early land plants (Silurian to Middle Devonian, about 445-393 Ma). Do not edit any file.

Input: the CSV file `work/codex/loop3/names_3.csv` (read it; it has exactly 79 rows). Each row is one distinct PBDB name (`nm`) with context: occurrence and collection counts, the oldest max_ma and youngest min_ma in the extract, the identified-as strings, PBDB's broad group, organs, ISO country codes and PBDB lineage tail. Names in quotes or angle brackets are informal or uncertain PBDB identifications; classify the genus they denote.

For every row return one item, in input order, with:
- `name_id`, `name` (copy `nm` exactly).
- `category`, one of:
  - `rhyniophytoid_cooksonioid`: Cooksonia-grade and rhyniophytoid polysporangiate axes not demonstrably on the lycophyte or euphyllophyte lines (e.g. Cooksonia, Steganotheca, Salopella, Uskiella, Tortilicaulis, Rhynia, Aglaophyton, Horneophyton, Renalia).
  - `lycophyte_line`: zosterophylls, lycopsids and other plants placed on the lycophyte line (e.g. Zosterophyllum, Baragwanathia, Drepanophycus, Sawdonia, Gosslingia, Aberlemnia, Leclercqia).
  - `euphyllophyte`: trimerophytes, Psilophyton-grade, cladoxylopsids, early ferns/sphenophytes, progymnosperms.
  - `tracheophyte_indet`: vascular plant whose lineage is unclear.
  - `polysporangiophyte_indet`: branched sporophytes with sporangia whose tracheophyte status or lineage is unclear.
  - `embryophyte_axis_indet`: sterile axes or fragments accepted as land plant but not assignable (e.g. Hostinella-type axes).
  - `bryophyte_grade`: bryophyte or thalloid land-plant gametophyte/sporophyte material.
  - `nematophyte_or_problematic`: Prototaxites, Nematothallus, Pachytheca, Parka, Spongiophyton and other problematica not accepted as embryophytes.
  - `alga`.
  - `implausible_in_window`: a homonym, a much younger genus, or a likely misidentification for rocks of this age (say why).
  - `uncertain`: use instead of guessing.
- `polysporangiophyte`: yes / no / uncertain (branched sporophyte bearing several sporangia, the clade including all tracheophytes).
- `crown_tracheophyte`: yes / no / uncertain (member of the clade descended from the last common ancestor of lycophytes and euphyllophytes; lycophyte-line and euphyllophyte names are yes; rhyniophytoids are usually no or uncertain).
- `basis`: one or two sentences on the morphology or placement relied on.
- `source`: a specific published source (author, year, title or DOI) or a stable URL that you actually consulted for this name. Do not invent sources. If you consulted none, write `none checked` and set confidence to low.
- `confidence`: high / medium / low.

Return JSON matching the schema, with a top-level `items` array of exactly 79 items.
