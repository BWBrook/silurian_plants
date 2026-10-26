# Review of the EPRP deposit (`data/eprp/`)

Reviewed 2026-10-27 by Claude Opus 5.5 at Barry's request. The deposit was extracted on 2026-10-26
by the EPRP session on mac-mini (Claude Opus 5.5 with three Claude Sonnet 5.5 subagents) from EPRP
commit `ac42dfb` and the `deep-server:/data/paleodata/` mirror.

## Verdict

Accept, and commit everything outside `local/`. The deposit is careful, reproducible and candid
about its limits: every filter is documented, observation is kept apart from inference, and nothing
was converted between timescales. It contradicts nothing in the cards. It does change four
judgements in `docs/framings.md` and corrects one claim in `docs/precedents.md`.

## What was checked

- **Documentation.** Read the top-level README, the four area READMEs and `pointers/eprp_pointers.md`
  in full.
- **Integrity.** `scripts/build_manifest.py` recomputed the sha256 and row counts of all 88
  delivered files; all match, and the manifests were unchanged by the run. One file is unlisted:
  `context/deposits/rogger2026-treed-vegetation-model/Manifest.toml`, the Julia lockfile of the
  TREED deposit.
- **Numbers.** Recomputed the PBDB core and flagged totals and the per-stage counts, collections,
  genera and dispersed-spore rows with DuckDB. All are identical to `record/README.md` §3
  (2,628 core and 1,076 flagged occurrences).
- **Licences.** Every committable file is CC0, CC BY 4.0, Apache 2.0 or project-written, except
  `context/rothman2017_events_window.csv` (CC BY-NC 4.0, flagged in the manifest). Everything held
  without a redistribution licence, under no-derivatives terms or as publisher text, and all
  rasters, sits in `local/`. `git check-ignore` confirms that `local/` is ignored. Sizes: 622 MB
  local and 17 MB committable, with no committable file over 3.2 MB.
- **Missed literature.** Rogger et al. (2024), Rogger et al. (2026), Gurung et al. (2022),
  Matthaeus et al. (2023) and Boyce & Nelsen (2025) resolve in Crossref, and their abstracts
  support what the deposit says of them.
- **Not checked.** Script reruns, because they need `deep-server`; the extraction reports a
  byte-identical second run. Library screen decisions beyond the 51 `CORE` works. The contents of
  the third-party deposits.

## What it changes

**F3 (the record and the timescale).**
- *The megafossil channel exists but is thin.* PBDB gives 259 core occurrences before the
  Emsian: 2 in the Sheinwoodian, 3 in the Gorstian, 83 in the Ludfordian and Pridoli (which PBDB
  bins together), 58 in the Lochkovian and 54 in the Pragian.
- *There is no spore channel yet.* PBDB holds one Ordovician spore record (*Tetrahedraletes*,
  Hirnantian) and nothing before it. The spore side of F3 needs a compilation from the
  literature, so F3's tractability falls from high to moderate.
- *Macrostrat cannot serve as the sampling proxy.* It is a North American, 88% marine rock record,
  while the early plant record comes mainly from Avalonia, Baltica, peri-Gondwana and South China.
  The observation model will need a different proxy for sampling effort in those regions.
- *EPRP has already validated the tools F3 would use.* `tbea`'s Marshall interval returns no upper
  bound unless there are at least 110 gaps, and its endpoint labels swap meaning between age and
  forward time. PyRate's preservation intervals undercover at low preservation. StratPal maps
  wrongly above hiatuses. All of these bite on a gap-dominated Silurian record.
- *The method has precedents in other clades.* Origination dating from first appearances has been
  done for birds (Crouch 2022) and winged insects (Schachat et al. 2022), and Lole Durbin et al.
  (2026) revisit clock maxima. F3 remains new for land plants, but it applies an established approach
  rather than inventing one, and should say so.
- *PBDB re-dated its intervals in 2024–2025.* Any PBDB extract made before about 10 April 2025
  carries GTS2012-era Silurian and Devonian ages. Use this snapshot (2026-10-23) or later, and
  never mix vintages.

**F5 and F7 (vegetation, climate and carbon).**
- *Three precedents were missed by the precedents review:*
  - Rogger et al. (2024): eco-evolutionary vegetation coupled to a carbon-cycle model, for
    large-igneous-province hyperthermals;
  - TREED (Rogger et al. 2026): a trait- and optimality-based eco-evolutionary vegetation model for
    deep time, with its code deposited here;
  - Gurung et al. (2022): FLORA coupled to SCION, which finds an Ordovician window of opportunity
    for plant expansion.
- *A correction.* The review's statement that every Earth-system treatment prescribes the plant
  effects is wrong in general. It still holds for leafless early plants and for the
  Ordovician–Devonian specifically. F5's novelty falls from high to moderate, which reinforces
  leaving it until later.
- *Design references for F1 and F2.* TREED's carbon-economy trade-offs are one, although it is
  leaf-based and written in Julia, which is installed nowhere on the mesh. Matthaeus et al. (2023)
  review the reconstruction of early vascular plant function and is required reading for F2.
- *Climate forcing.* PhanDA GMST and CO2 by stage, Song et al. (2021) SST and the Scotese
  temperature maps are available. There is no independent CO2 or O2 proxy compilation. PhanDA and
  the Scotese-derived GMST differ by 3–16 °C in the Silurian, so the choice of forcing will matter.
  PhanDA is held locally only, pending a licence answer.

**F4 (spore biogeography).** The inputs that made F4 look hard now exist on the mesh: 21 PALEOMAP
elevation maps across the window, HadCM3 SST and cGENIE climate fields (400–480 Ma), an index of 27
plate models, and gen3sis, an eco-evolutionary engine for palaeo-landscapes, with EPRP's bench
notes on it. Tractability rises from lower to moderate. The caveats: no reliable full-plate model
exists before 410 Ma, and palaeolatitudes differ by a median of 12–16° between models.

**F6 (vulnerability and recovery).** EPRP's register question Q-018, on whether plants have mass
extinctions in the same sense as marine animals, sits next to F6 and comes with a reading list.

**Cards.** `record/card_taxa_pbdb_summary.csv` is a useful cross-check, but PBDB ranges follow
contributors' interval assignments and are not re-evaluated, so they should not overwrite card
ranges. Several card taxa are absent from PBDB or misnamed there: *Aglaophyton* appears only as
"*Rhynia major*", *Horneophyton* as "*Hornea*", and *Partitatheca*, *Riccardiothallus* and
*Tortotubus* have no occurrences.

## Limits to keep in view

- The library is thin on palaeobotany: it holds only 59 of the project's 393 DOIs. It complements
  the card literature; it is not a substitute for it.
- The climate series are on GTS2020 or GTS2012. Any forcing put on the project's timescale needs an
  explicit conversion.
- One agent screened the library and nobody has reviewed the screen. A random sample of 100 dropped
  works contained none that is relevant.
- `local/` exists only on mac-mini. Other machines must rebuild it from `deep-server` with the
  scripts.

## Follow-ups

1. Compile a dispersed-spore occurrence dataset for the Darriwilian to Emsian. It is the largest
   data gap for F3, and the deposit confirms that no existing source covers it.
2. Add TREED's `Manifest.toml` to the context manifest, on the EPRP side.
3. Precedents and framings were updated on 2026-10-27 to reflect this review (`docs/decisions.md`).

## References

- Boyce CK, Nelsen MP (2025). Terrestrialization: toward a shared framework for ecosystem evolution. Paleobiology 51: 174–194. https://doi.org/10.1017/pab.2024.15
- Crouch NMA (2022). Interpreting the fossil record and the origination of birds. bioRxiv preprint. https://doi.org/10.1101/2022.05.19.492716
- Gurung K, Field KJ, Batterman SA, Goddéris Y, et al. (2022). Climate windows of opportunity for plant expansion during the Phanerozoic. Nature Communications 13: 4530. https://doi.org/10.1038/s41467-022-32077-7
- Lole Durbin OM, Anttila ESC, Briggs DEG, Macdonald FA, Anderson RP (2026). Re-evaluating molecular clock maximum age calibrations revives pre-Ediacaran divergence estimates for animals. Science Advances 12: eaeg6289. https://doi.org/10.1126/sciadv.aeg6289
- Matthaeus WJ, Macarewich SI, Richey J, Montañez IP, et al. (2023). A systems approach to understanding how plants transformed Earth's environment in deep time. Annual Review of Earth and Planetary Sciences 51: 551–580. https://doi.org/10.1146/annurev-earth-080222-082017
- Rogger J, Judd EJ, Mills BJW, Goddéris Y, et al. (2024). Biogeographic climate sensitivity controls Earth system response to large igneous province carbon degassing. Science 385: 661–666. https://doi.org/10.1126/science.adn3450
- Rogger J, Gurung K, Kopp EB, Matthaeus WJ, et al. (2026). TREED (v1.0): a trait- and optimality-based eco-evolutionary vegetation model for the deep past and the present. Geoscientific Model Development 19: 4931–4960. https://doi.org/10.5194/gmd-19-4931-2026
- Schachat SR, Goldstein PZ, Desalle R, Bobo DM, et al. (2022). Illusion of flight? Absence, evidence and the age of winged insects. Biological Journal of the Linnean Society 138: 143–168. https://doi.org/10.1093/biolinnean/blac137
