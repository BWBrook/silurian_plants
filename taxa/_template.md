---
# Taxon card template. Copy to taxa/<slug>.md (lowercase, hyphenated: aglaophyton-major.md).
# The front matter is data: tools/cards.py validates it and builds taxa/README.md from it.
# Use null for "not yet looked up". For traits, distinguish observed `absent` from `unknown`
# (not preserved or not reported) and `na` (not applicable, e.g. stomata in a fungus).
name: Genus species            # as currently accepted; genus alone for a genus card
authority: Author year
rank: species                  # species | genus | morphogroup | assemblage
kind: megafossil               # megafossil | mesofossil | dispersed_spores | assemblage
group: rhyniophytoid           # see vocabulary in tools/cards.py (GROUPS)
lineage: >-
  One line on phylogenetic placement, e.g. "stem-group lycophyte (zosterophyll grade)".
placement_confidence: medium   # low | medium | high
range:
  first: Pragian               # ICS stage names from data/timescale.csv
  last: Pragian
  notes: >-
    Basis of the range: dated sections, biostratigraphy, radiometric ages, and disputes.
regions: [Laurussia]           # palaeocontinents/terranes: Laurentia, Baltica, Avalonia, Laurussia, Gondwana, South China, North China, Kazakhstania, Siberia
localities:
  - Locality, country (unit/formation, notes)
preservation: [permineralised]  # compression | permineralised | charcoalified | adpression | cast | dispersed
traits:
  height_cm: {min: null, max: null, note: null}
  axis_diameter_mm: {min: null, max: null, note: null}
  branching: {state: unknown, note: null}            # none | isotomous | anisotomous | pseudomonopodial | monopodial | K-branching | H-branching | mixed | unknown | na
  leaves: {state: unknown, note: null}               # absent | enations | microphylls | megaphylls | unknown | na
  stomata: {state: unknown, note: null}              # present | absent | unknown | na
  conducting_tissue: {state: unknown, note: null}    # absent | hydroids | non-lignified | tracheids-G | tracheids-S | tracheids-P | tracheids | unknown | na
  sporangium_position: {state: unknown, note: null}  # terminal | lateral | both | unknown | na
  spores: {state: unknown, note: null}               # cryptospores | trilete | both | unknown | na
  heterospory: {state: unknown, note: null}          # absent | present | unknown | na
  rooting: {state: unknown, note: null}              # rhizoids | rhizomes | roots | rooting-axes | unknown | na
  gametophyte: {state: unknown, note: null}          # known | unknown | na
habitat: >-
  Depositional setting and inferred habitat, with how firmly each is known.
status: draft                  # draft | reviewed (reviewed = facts checked by a second agent or by Barry)
updated: 2026-10-26
references:
  - cite: "Author A, Author B (Year). Title. Journal Volume: pages."
    doi: 10.xxxx/xxxxx         # verified against Crossref; use null only when no DOI exists
---

## In brief

Three or four sentences: what the organism was and why it matters for the origin and early
evolution of land plants.

## Morphology and anatomy

What is preserved and what has been reconstructed. Say which features are observed and which
are inferred, and where reconstructions disagree.

## Age and distribution

Stratigraphic range, key localities and palaeogeography, and the strength of the dating.

## Affinity and controversies

Phylogenetic placement, competing interpretations, and what evidence would settle them.

## Ecology and physiology

Habitat, growth form, water relations, nutrition (including symbionts), reproduction and life
cycle, as far as the evidence goes.

## Why it matters for modelling

Which traits, trade-offs, rates or patterns this taxon informs or constrains, with numbers where
the literature provides them.

## Open questions

Unresolved points worth tracking.
