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
| `effort_by_stage.csv` | Palynological sampling effort: per palaeogeographic unit × stage, the number of Palynodata documents with datable records of any palynomorph, and how many report spores (excluding documents whose spores were rejected in vetting) |
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
- **The oldest records are vetted, in two passes.** Raw first appearances were driven by early
  Soviet and French reports of Ordovician trilete spores that later work doubts.
  - `crosswalks/doc_vetting.csv` gives a verdict for each of the 121 documents with usable records
    older than the Wenlock: 53 accept, 54 doubtful, 14 reject.
  - `crosswalks/group_vetting.csv` refines this to 189 record groups (one document × age range ×
    location × class group): 91 accept, 86 doubtful, 12 reject. It catches cases such as a credible
    synthesis whose Floian age for a cryptospore row is not demonstrated.
  - Both passes are by Codex `gpt-6.1-sol`. Group verdicts override document verdicts.
    `first_appearances.csv` gives a `strict` set (accepted, curated and unvetted records) and an
    `inclusive` set (adding doubtful ones); rejected records are never used.
- **First appearances in the strict set** (all regions):
  - cryptospores certain by 458.2 Ma and possible from 469.4 Ma (Darriwilian);
  - trilete spores certain by 445.2 Ma and possible from 458.2 Ma (Katian).
  
  The Dapingian cryptospores of Rubinstein et al. (2010) are absent because Palynodata stops in
  2006. The post-2006 literature (MVD-B) is the next layer.
- **Ages are crosswalked, not re-dated.** Each record carries the ICS stage range implied by its
  age names. Palynodata's own numeric ages are 2006-era and are not used.
- **Spore classes are morphological.** Following Hooper et al. (2026), a trilete spore marks an
  embryophyte, not necessarily a vascular plant, and cryptospores may belong to stem-group plants.
- **Palaeogeographic units come from present-day locations** through terrane rules (Avalonia,
  Baltica, Laurentia, peri-Gondwanan Europe, Gondwanan regions, South China and others). No plate
  rotation is applied.
- **Sampling effort is represented, coarsely.** `effort_by_stage.csv` counts the palynological
  documents per stage. The crosswalks were extended to the non-spore rows by Codex (147 locations,
  188 age names, 2026-10-27).
  - The share of documents reporting spores rises from 1–4% (Tremadocian–Sandbian) to about 8%
    (Katian–Hirnantian), 15–18% (Llandovery–Wenlock), 22–25% (Ludlow–Pridoli) and 57–66% (Lochkovian–Emsian).
  - Sampling stays at 400–700 documents per stage through the Ordovician and Silurian.
  - Read this with care: a document counts in every stage its records overlap; marine studies
    may not report land-derived spores; and facies composition changes through time.
