# Occurrence data: observations, interpretations, readings

The data for the first deliverable (`docs/plan-f3.md`). They are structured so that disagreement stays usable: what a source observed is held apart from each reading of it, and every analysis declares which reading it uses. Built from 2026-10-28 by Claude Opus 5.5, with Codex extraction jobs (`work/codex/loop1/`). Loop 1 covers only the **tail**: the oldest records bearing on events E1–E5.

## Files

| File | One row per | Key |
|---|---|---|
| `observations.csv` | thing a source reports: an assemblage, a specimen, a set of specimens | `obs_id` |
| `interpretations.csv` | coherent reading of one observation: what it is, how old, which events it evidences, who holds it | `interp_id`; `obs_id` refers to an observation |
| `sources.csv` | publication or document | `source_id` |
| `effort.csv` | stage × palaeogeographic unit × channel: sampling effort | |

### observations.csv

- `obs_id`: `S-` for spores, `M-` for megafossils and mesofossils, then a short stable slug.
- `channel`: `spore`, `megafossil` or `mesofossil`.
- `reported_as`: the taxon or material as the source reports it.
- Where it was found:
  - `locality`, `country`;
  - `unit`: formation, member or core;
  - `horizon`: bed, level or depth, where given.
- `palaeo_unit`: the vocabulary of `data/spores/occurrences.csv` (for example `Baltica`, `Gondwana-North-Africa-Arabia`, `Laurentia`, `peri-Gondwana-Europe`, `South-China`).
- `source_ids`: the primary report or reports, separated by semicolons.
- `locator`: page, figure, table or row code.
- `events`: the events this observation is considered for, from E1 to E5.
- `same_material_as`: the `obs_id` of another observation reporting the same material. For example, a dataset row and a published table row for one assemblage. Analyses count linked observations once.
- `notes`.

### interpretations.csv

- `interp_id`, `obs_id`.
- `label`: a short description, such as "Sandbian trilete spores (accepted)" or "folded sphaeromorphs, not spores".
- `counts_for`: the events this reading makes the observation evidence of, separated by semicolons. Empty means none, as for a rejection.
- `stage_oldest`, `stage_youngest`: ICS stage names from `data/timescale.csv`. Uncertainty is a stage range, never a "?".
- `age_note`: the numerical evidence and the basis of the stage assignment (primer §1.2: the stage is the primary datum; dates sit beside it).
- `held_by`: the published authors who hold this reading.
- `held_by_source_ids`: their source IDs.
- `adjudicator`: blank when the reading is published. Otherwise the project member who made it (`Claude Opus 5.5`, `Codex gpt-6.1-sol`, `Barry Brook`), with the reason in `support`.
- `main`: `true` for exactly one interpretation per observation, the reading used by the main analysis. Choose it before any analysis is run.
- `support`: a verbatim quotation of at most 40 words that supports the reading.
- `support_from`: the path of a repository file, or a DOI or URL.
- `checked`: how the support was read: `full-text`, `abstract`, `card`, `repo-doc` or `secondary`.

### sources.csv

`source_id` (first author, year, letter if needed: `wellman2022`), `citation`, `doi` (blank if none), `access` (`open`, `closed`, `print`, `unknown`).

## Events (`docs/plan-f3.md`)

| Event | What counts | Loop 1 tail |
|---|---|---|
| E1 | trilete spores of embryophytes | every claim of trilete spores from the Hirnantian or older |
| E2 | cryptospores of embryophytes | every claim of embryophytic cryptospores or polyads from the Sandbian or older, including Cambrian–Tremadocian polyads |
| E3 | polysporangiophyte bodies (branched axes with terminal sporangia, *Cooksonia* and relatives) | every claim from the Homerian or older |
| E4 | tracheids in situ in a body fossil | every claim from the Pridoli or older |
| E5 | lycophyte-line bodies (zosterophylls, lycopsids) | every claim from the Pridoli or older |

The tail runs one stage past the oldest record that is not disputed, so that the sequence has an anchor.

## Readings

- **Main reading.** The interpretation marked `main` for each observation. It is chosen before any analysis runs.
- **Unassessed outliers** (rule set by Claude Opus 5.5 on 2026-10-28, before any estimator was run on these data). Some claims would make an event's first appearance more than one stage older than the oldest record accepted by an independent assessment. Such a claim enters the main reading only if it has been peer reviewed and accepted by at least one later independent assessment. Otherwise its main reading is "unassessed outlier, not counted", and the claim as published becomes an alternative for the pivotal analysis to test. This keeps the baseline from resting on a single unchecked report, while the claim is still tested.
- **Pivotal-records analysis.** Each observation with more than one interpretation is switched to each of its alternatives in turn, one at a time and in combinations of the most influential.
- **Named readings.** Defined in code. For example:
  - `strict`: every disputed record is rejected;
  - `inclusive`: every claimed record is accepted;
  - `hooper2026`: Hooper et al.'s calibration choices.

## Effort layer (`effort.csv`)

`uv run tools/occurrences.py effort data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv`

- **Body fossils** (`channel` = `body`). Paleobiology Database collections of **all taxa**, not only plants, are counted per stage × palaeogeographic unit.
  - **What it measures:** effort, meaning how much of each stage's rock was collected, independent of whether plants were found.
  - **Apportioning:** each collection is split across stages in proportion to the overlap of its age range with each stage.
  - **Environment split:** `land` (terrestrial, fluvial, lacustrine, delta plain), `marginal` (coastal, lagoonal, estuarine, deltaic, peritidal, foreshore), `marine` and `unknown`.
  - **Units:** taken from the country, and for the UK and China from the state or province (`UNIT_BY_CC` in the script). This is approximate, and spanning countries are marked `multiple`.
  - **Raw pull:**
    - query: `https://paleobiodb.org/data1.2/colls/list.csv?interval=Darriwilian,Emsian&show=loc,strat,paleoloc,env,stratext&limit=all`;
    - fetched 2026-10-28; 27,830 collections; CC0;
    - SHA-256 `e0d1f772c1617c218948d1d2605661e93edcfe75e0fe8ce92afee91d3350a8b8`;
    - kept in git-ignored `raw/` on mac-mini. It is to be copied to `deep-server:/data/codex/silurian_plants/raw/pbdb/` when that host is reachable; it was not on 2026-10-28.
  - **Ages:** PBDB's numerical ages are on its own scale, so the overlap weights are approximate near boundaries.
- **Spores** (`channel` = `spore`). Palynodata documents with datable palynomorph records of any kind, per stage × unit, from `data/spores/effort_by_stage.csv`. These run to 2006 only; the post-2006 literature is not yet counted.

First look (2026-10-28):
- **Terrestrial collections.** Collections of any taxon from terrestrial settings number at most about 8 per stage from the Darriwilian to the Pridoli. They rise to about 104 in the Lochkovian, then 49 and 93 in the Pragian and Emsian.
- **Marginal-marine collections.** These stay at about 18–72 per stage throughout.

The body-fossil channel's land effort therefore steps up by more than an order of magnitude at the Silurian–Devonian boundary. Any first appearance or richness rise near that boundary has to be read against this.

## Status

Loop 1, step 1, in progress (2026-10-28).
