You are helping maintain taxon information cards in this repository (read AGENTS.md; do not edit any file). Each card describes a fossil or living taxon, a group, or a fossil assemblage relevant to modelling early land-plant evolution (Late Ordovician to Early Devonian).

Barry, the programme's scientist, asked that each card state the contrast it is chosen to test and which of its traits can and cannot be carried into a simulation model. Your job is to propose that material for each card listed below, using ONLY what the card itself says. Do not use web search, memory or outside sources, and do not add facts, numbers or citations the card does not contain.

Cards (READ EACH IN FULL; there are exactly {N}):
{CARDS}

For each card return one item:

- slug: the file name without .md.
- contrasts: the mechanism contrasts the card's content genuinely informs (usually one to three; [] if none):
  - height: stature, mechanical support, the race for height;
  - water-transport: conduction, hydraulics, stomata and water control, desiccation tolerance;
  - sporophyte-independence: which generation dominates, dependence of one generation on the other, matrotrophy, life-cycle structure;
  - fungal-nutrition: fungal symbioses, mycorrhiza-like associations, mycoheterotrophy, nutrient acquisition through fungi;
  - reproductive-strategy: spore output, sporangia, homospory versus heterospory, dispersal;
  - clonal-growth: rhizomes, vegetative spread, persistence, recovery after burial or disturbance;
  - record-timing: evidence on when lineages or traits appear in the record, rather than on mechanism.
- chosen_to_contrast: one sentence, starting with a verb or noun phrase (no "This card"), saying what the exemplar is chosen to contrast and why it suits that contrast.
- can_transfer: two to five bullets. Each names a trait, rate or relationship a model may take from the card, WITH the species and specimens or site it was measured on and the source as the card cites it (author year). Numbers must be copied from the card.
- cannot_transfer: two to five bullets. Each names a trait that must not be carried over, and why: measured on another species, a derived or reduced condition, inferred rather than observed, uncertain affinity, unreliable dating, and so on.
- For every bullet, support: one passage copied EXACTLY, character for character, from the card (at most 200 characters) that justifies the bullet. It will be checked by script.
- borrowed: every trait in the card's front matter whose value was measured on a different taxon from the card's own (for example a congener used as a proxy). Give the trait key, the taxon it came from, and the supporting passage copied exactly. [] if none. Group and assemblage cards summarise their members, so they have no borrowed traits.
- doubts: anything in the card that looked inconsistent or that made a bullet hard to write; "" if none.

Style: British spelling; dense, precise prose; each bullet under 45 words; no hedging filler. Keep measurements on different species separate.

Return JSON only, matching the schema, with exactly {N} items in the order given.
