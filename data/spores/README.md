# Dispersed-spore dataset (minimum viable version)

The project's spore channel for framing F3 (`docs/framings.md`): occurrences, first appearances
and stage-by-stage presence of cryptospores and trilete spores, Darriwilian to Emsian and
beyond. This is MVD-A of `docs/spore-compilation-plan.md`, built from open sources only. The
post-2006 literature (MVD-B) is still to add.

Rebuild with `uv run tools/spores.py build`. `uv run tools/spores.py check` validates the
crosswalks, and `uv run tools/spores.py inputs` regenerates the work lists they are built from.

## Sources

- **Palynodata 2006** (GSC Open File 5793, OGL-Canada), as extracted in `data/external/spores/`:
  14,114 spore rows in the window from 985 documents, 14,059 after exclusions. Its literature stops
  in 2006.
- **Wellman, Steemans & Vecoli 2013**, supplement (CC BY 4.0): 144 curated Ordovician–Silurian
  assemblages, 1,430 taxon records, digitised into `sources/`.

## Outputs

| File | Contents |
|---|---|
| `occurrences.csv` | One row per taxon record from either source: genus and taxon, location, palaeogeographic unit, spore class, ICS stage range and ages, age confidence, flags (reworked or caved, synonym list, new taxon, questionable affinity), and `usable` |
| `first_appearances.csv` | Per spore class (and class group) × palaeogeographic unit (and all units): number of sources; `fa_certain_ma`, the oldest age at which a record is certainly present (its youngest bound); `fa_possible_ma` (its oldest bound); and the records behind each |
| `presence_by_stage.csv` | Number of distinct sources per spore class × unit × ICS stage, from usable records whose range overlaps the stage |

`usable` means all of the following:
- a real spore class;
- age confidence high or medium;
- an age range of 25 Myr or less;
- not reworked, caved, from a synonym list or of questionable affinity;
- a known palaeogeographic unit.

## Crosswalks (`crosswalks/`)

| File | Maps | Made by |
|---|---|---|
| `age_names.csv` | 189 Palynodata age names (Gedinnian, Ludlovian, Caradoc, …) to ICS v2024/12 stage ranges, with confidence and source | Claude Sonnet 5.5 with literature; reviewed by Claude Opus 5.5, who narrowed Gedinnian to the Lochkovian |
| `locations.csv` | 286 Palynodata location strings to palaeogeographic units, by stated terrane rules | Codex `gpt-6.1-terra`; reviewed by Claude Opus 5.5 |
| `spore_genera.csv` | 717 genera and labels to spore classes | 80 genera by pilot consensus (Codex `gpt-6.1-sol` and Claude Sonnet 5.5, 47/47 agreement on confident calls); 637 by Codex `gpt-6.1-sol`; informal type labels reclassified by Claude Opus 5.5 |
| `wellman_series.csv`, `wellman_regions.csv` | Wellman et al.'s series headings and regional labels | Claude Opus 5.5, consistent with `age_names.csv` |
| `exclusions.csv` | Documents excluded as entry errors | as listed |

The pilot is recorded in `docs/audits/2026-10-27-codex-pilot.md`.

## Read before use

- **Rows are reports, not samples.** Palynodata rows are mentions in documents, so one assemblage
  can recur across papers. Count sources (documents or Wellman entries), not rows.
- **The oldest records need vetting.** Raw first appearances of trilete spores are driven by early
  Soviet and French reports of Ordovician triletes that later work doubts. `crosswalks/doc_vetting.csv`
  (in progress) records a verdict for every document with usable records older than the Wenlock,
  and first appearances should be read with it.
- **Ages are crosswalked, not re-dated.** Each record carries the ICS stage range implied by its
  age names. Palynodata's own numeric ages are 2006-era and are not used.
- **Spore classes are morphological.** Following Hooper et al. (2026), a trilete spore marks an
  embryophyte, not necessarily a vascular plant, and cryptospores may belong to stem-group plants.
- **Palaeogeographic units come from present-day locations** through terrane rules (Avalonia,
  Baltica, Laurentia, peri-Gondwanan Europe, Gondwanan regions, South China and others). No plate
  rotation is applied.
- **Absence of spores is not yet represented.** Documents reporting marine palynomorphs but no
  spores (sampling effort) are in `data/external/spores/` but not yet in this dataset.
