# What EPRP offers this project, beyond data and references

Extracted 2026-10-26 from EPRP (`BWBrook/eprp`, commit `ac42dfb`, read-only checkout at
`/Users/bwbrook/git/eprp` on mac-mini) by Claude Opus 5.5. Every DOI below was checked against
Crossref on 2026-10-26. Statements about EPRP's register, notes and software entries are EPRP's
own; framing assignments (F1–F7, from `docs/framings.md`) are this extraction's inference.

EPRP is Barry's quantitative-palaeobiology programme (Claude and Codex, from 7 October 2026). It
builds a register of research questions, a catalogue of data sources mirrored on `deep-server` (backed up on `nectar`), a
literature library and a software catalogue with validation benches. None of its 50 applied or
18 blue-sky questions is about early land plants: this project works in territory EPRP has not
entered, so EPRP's value here is mostly infrastructure, method lessons and a few adjacent
questions.

## Reaching EPRP directly

- Catalogue entries (caveats, column meanings, tested recipes): `resources/sources/<id>/README.md`.
  Bulk data: `nectar:/data/codex/artifacts/eprp-paleodata-backup/latest/<id>/`, same ids (the backup of EPRP's
  own mirror, `deep-server:/data/paleodata/<id>/`, which the Macs cannot reach).
- Literature: `ssh nectar 'cd /data/codex/artifacts/eprp-paleodata-backup/latest/library && python3 _tools/library.py search --store . "<query>"'`
  ranks titles, abstracts and about 3,000 open full texts; matches in publisher text-and-data-mining
  copies are reported without passages.
- Software builds and run outputs: `deep-server:/data/paleosoft/<id>/` (not in the nectar backup, which holds `/data/paleodata` only); entries in
  `resources/software/<id>/README.md`; the full survey in `resources/software/LANDSCAPE.md`.
- Treat the checkout as read-only: update it only by `git fetch` and fast-forward. Development
  happens elsewhere.

## Register questions next to this project

- **Q-018: Do plants and terrestrial biotas have mass extinctions in the same sense?** (under
  review). It asks whether the marine–terrestrial asymmetry in extinction is biological buffering
  or an artefact of rank and sampling, by projecting species losses to genus and family in both
  realms under the same preservation models. Bears on F6 and on F3's observation model. Its prior
  check gives a compact plant-extinction reading list:
  - McElwain et al. 2026, preprint, 10.21203/rs.3.rs-9282628/v1: metrics for plant mass
    extinction and ecosystem collapse;
  - Nowak et al. 2019, 10.1038/s41467-018-07945-w: no land-plant mass extinction at the
    Permian–Triassic once undersampling is considered;
  - Cascales-Miñana & Cleal 2013, 10.1111/ter.12086: the plant record shows two great extinctions;
  - McElwain & Punyasena 2007, 10.1016/j.tree.2007.09.003; Lucas 2021, 10.2517/2021pr004;
    Wilf et al. 2023, 10.1017/ext.2023.13; Thompson & Ramírez-Barahona 2023,
    10.1098/rsbl.2023.0314; Berry 2020, 10.35535/acpa-2020-0016.
  The project already cites Silvestro et al. 2015 from the same list.
- **Q-021: Biological control of Earth-system recovery** (under review). Mostly Permian–Triassic,
  but it carries a methodological warning for F5: published studies prescribe vegetation change as
  model input (Xu et al. 2025, 10.1038/s41467-025-60396-y, fossil-constrained vegetation collapse
  in SCION) or select simulations on the outcome, so the same vegetation assumption can end up as
  both input and evidence. EPRP's contract requires those uses to be kept apart.
- **Q-035: Do land ecosystems collapse before marine ones?** and **Q-032: insect crises that family
  counts miss** are further from this project; Q-032's damage-census framing would matter only if
  arthropod–plant interactions become a framing.

## Community question lists that name this territory

EPRP holds the community's Big Questions in paleontology (Smith et al. 2025,
10.1017/pab.2025.10042) and 1,224 questions from 392 published agendas. Questions bearing on
early land plants, with their sources:

- Boyce & Nelsen 2025, *Terrestrialization: toward a shared framework for ecosystem evolution*,
  10.1017/pab.2024.15. Asks when fungi evolved relative to their host plants, when insect flight
  evolved relative to Devonian trees, how plants changed floodplains and river meandering, and
  argues that terrestrialisation needs more attention to soil and litter. Not cited by the
  project; directly relevant to F1, F5 and F7.
- Matthaeus et al. 2023, *A systems approach to understanding how plants transformed Earth's
  environment in deep time*, 10.1146/annurev-earth-080222-082017. Asks for the quantitative
  impact of early vascular plants on erosion, weathering and pCO2; for time-appropriate plant
  physiology in Earth-system models; for fossil-based plant functional traits. Not cited by the
  project; F5 and F2.
- Goddéris et al. 2023, *What models tell us about the evolution of carbon sources and sinks over
  the Phanerozoic*, 10.1146/annurev-earth-032320-092701. Asks whether vegetation enhances
  weathering directly or indirectly, and where palaeo-vegetation was. The project's primer cites
  other Goddéris work; F5.
- Smith et al. 2025, final questions AIO1 (drivers of the origins of major groups, plants
  included) and AIO2 (terrestrialisation among the major transitions); raw questions on how the
  evolution of terrestrial floras changed marine nutrients and productivity, and what mass
  extinctions look like on land.
- Jablonski 2017, 10.1007/s11692-017-9434-7: "Do plants evolve differently from animals?"

The full term-matched set is `community_questions_plants.tsv` (69 rows). It is a term match, so
it includes false hits (industrial "plants", Holocene vegetation); `matched_terms` shows why each
row is there.

## Software and models

`software_relevant.tsv` lists 177 of the 364 tools in EPRP's survey, selected by EPRP's domain
labels and mapped to framings by rule. Tools with a full EPRP entry (`eprp_entry` column) have
been installed and checked against known truths; the rest carry the survey's facts only.

**For F3 (dating origination from incomplete records)**, EPRP's checks found pitfalls that apply
directly:

- **tbea** (`stratCI`; Strauss–Sadler 1989 and Marshall 1994 confidence intervals on range
  endpoints): Marshall's method returned no upper bound in any test case (an apparent off-by-one
  that needs at least 110 gaps at 95%/95%); `endpoint = "first"` and `"last"` swap meaning
  between age and forward time; hiatuses near the endpoint cut Strauss–Sadler coverage to about
  0.83. The Silurian megafossil record is gap-dominated, so the last point matters.
- **StratPal** (Hohmann et al. 2025, 10.1111/2041-210X.14507; stratigraphic forward model):
  pipelines that map back to time through `admtools::strat_to_time` are wrong above hiatuses,
  and `last_occ` does so.
- **PyRate**: preservation-rate intervals undercover (81% at ψ = 1.0, 66% at ψ = 0.25) because q
  is biased high as preservation falls; at low preservation μ is covered only 80% of the time.
  Work from a pinned commit; the last release is from 2022.
- **DeepDive**: without a present-diversity anchor it overestimated richness in every bin of one
  scenario, and read an evenness change as a decline.
- **FossilSim** (10.1111/2041-210x.13170), **paleobuddy** (10.1111/2041-210x.13996) and
  **RevBayes** (FBD-range, total-evidence dating) are installed; RevBayes has no validated use yet.

**For F5 and F7 (plants, climate and carbon)**, from the survey:

- **SCION** (Mills et al. 2021, 10.1016/j.gr.2021.02.011) is MATLAB; **pySCION** (Merdith et al.
  2025, 10.1126/sciadv.adm9798) is an open Python port that lags MATLAB v1.3.0.
- **FLORA**, a simplified deep-time dynamic global vegetation model coupled to SCION (Gurung et
  al. 2022, *Climate windows of opportunity for plant expansion during the Phanerozoic*,
  10.1038/s41467-022-32077-7). MATLAB; code on request and in the supplement. Gurung et al. is
  not cited by the project and speaks directly to the Silurian–Devonian expansion.
- **TREED** (Rogger et al. 2026, 10.5194/gmd-19-4931-2026): trait- and optimality-based
  eco-evolutionary vegetation model for deep time. Julia, which is installed nowhere on the mesh.
  Its deposit is mirrored at `nectar:/data/codex/artifacts/eprp-paleodata-backup/latest/register-deposits/rogger2026-treed-vegetation-model/`.
- **COPSE** and **GEOCARBSULF** (MATLAB), **DCESS II** (Fortran, with a land biosphere;
  10.5194/gmd-18-2161-2025), and **cGENIE.muffin**, which EPRP has built and regression-tested
  (bitwise identical across gfortran 9 and 11 at v0.9.78).
- **goSPL** (landscape evolution on PALEOMAP elevations) for rivers and soils.

**For F4 (spore biogeography)**: gen3sis (Hagen et al. 2021, 10.1371/journal.pbio.3001340), a
spatial eco-evolutionary engine on palaeo-landscapes. EPRP's bench found its own tests incomplete
(nine author-skipped tests, CRLF reference files) and recompiled the authors' deposited 4°
landscapes for version 1.6.0. EPRP lead L-015 records a published goSPL-to-gen3sis pipeline over
125 Myr (Lorcery 2025). Plate models: pyGPlates and GPlates (Müller et al. 2018,
10.1029/2018GC007584) and the hosted GPlates Web Service; EPRP's palaeogeography entry records
Wright et al. 2013 as PBDB's default model for palaeocoordinates (see `../context/`).

## Not extracted

EPRP's dated notes in `ideas/` mention plants only in passing (blue-sky maps, nomination cards);
none develops an early-land-plant question. EPRP's test-bench results, benchmark data and
correspondence board were not copied.
