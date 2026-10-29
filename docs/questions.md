# Questions register

The programme's working list of provisional questions: what each needs, which gaps matter to it, and where it stands. It exists so that evidence work and questions develop together (`docs/charter.md`, "Purpose"):

- broad assembly exposes gaps;
- questions show which gaps matter;
- targeted work fills them;
- questions sharpen.

The register is updated at each loop's close. Started 2026-10-28 by Claude Opus 5.5 from Barry's programme principles; questions are added or reworded by either.

- **Linking.** Gaps elsewhere point here by question number:
  - the leads register (`docs/audits/2026-10-28-card-consistency-leads.csv`);
  - the closed-literature list (`docs/closed-literature.csv`, column `needed_for`);
  - the source register (`docs/sources.md`).
- **Status.**
  - **active**: work under way;
  - **provisional**: framed, not started;
  - **parked**: waiting on a named dependency;
  - **answered**: with a pointer to the result.
- **Kind of contribution.** Each has its own standard of success (charter): synthesis, statistics, simulation, phylogeny.

| ID | Question | Contribution | Status | Standard of success | Decisive gaps and dependencies | Next step |
|---|---|---|---|---|---|---|
| Q1 | Under which explicit sampling and biological assumptions are origins older than the land-plant clock maxima (515.5, 459.1, 431.2 Ma) incompatible with the fossil absences behind them, and where does the record not constrain them? (Reworded 2026-10-28 when F3 reshape v3 was adopted; formerly: when did the main lineages arise, and which clock scenarios do sampling-corrected windows allow?) | statistics | active | compatibility results per maximum and declared history class, in the four states of `docs/f3-shape.md`, from a procedure that passed its validation study; each verdict conditional on named detection assumptions, readings and fossil-to-node mappings; a demonstrated limit, with the observation that would resolve it, also counts | the contested oldest records for E1–E5 (assembled; pivotal ones rechecked against full texts 2026-10-28); Hooper et al.'s Supplementary Table 4 (read). The recovery study shows the most decisive evidence is palynological sampling *without* spores in stages older than the first appearance (`models/f3/README.md`). Cambrian effort extracted 2026-10-28 (Palynodata to 2006): about 175–185 documents per Middle and Late Cambrian stage and 418 in the Tremadocian, but almost none for Fortunian–Stage 3, because "Early Cambrian" papers fail the 25 Myr dating rule. The Cambrian cryptospore-like occurrences (Laurentia; Kaili Formation, South China) still need stage-level dating from their primary papers | F3 reshape v3 remains adopted. Codex checked repairs at e48d96d: chord/Jensen construction accepted and all 142 tests pass; saved 21 x 1,000 development results reproduce. A15 passes the 0.93-floor stage-1 gate at delta=0; its separate empirical-95% tuning shift is 0.1133. Claude resolved R2-R4 (55d7a58): true-rate target at the profiled rates, integrated normalisation, per-result status, and calibrate/accept phases with a hashed receipt. Rehearsed on the synthetic design: delta = 0, all 117 acceptance quantities pass stage 1 (lowest A15 H0c 946), one failed fit in 63,000 replicates, misses confirmed as sampling by re-optimisation; shared section ages (D7-D9) cost <= 0.01 coverage, so the independence assumption is declared. Open with Codex: calibrating delta to 0.955 (a cell at 0.948 fails acceptance with probability 0.105). Evidence: 15-block/90-outcome pilot plus three audited candidate frames and 14 Hanadir chart depths. Hanadir 190.7 m now has a primary study-scoped E1 negative with an exact specimen link; no complete analysis denominator yet. Next: Codex checks this tranche and the 0.955 proposal and integrates the productivity condition into the reporting rule; Codex targets complete sample inventories. Then binding validation on the real design, followed by M2, M1, M3. Correspondence 99; Q9 remains parked at its completed provenance audit. |
| Q2 | Which adjudications decide the early pattern? | synthesis | active | for each event, a short list of pivotal records with what each reading implies; every adjudication inspectable | readings for the contested tail (`docs/rejected-records.md`, cards); specialist judgement on the pivotal ones, flagged where contact is worth trying, and never waited on | `docs/plan-f3.md`, Loop 1 step 4. First pass done 2026-10-28 without any estimator (`models/f3/out/naive_pivotal.csv`). The decisive records are Borenshult-1 (E1), the Argentine Dapingian and Tremadocian polyads (E2), Zbrza, *Piterophyton* and *Volkhoviella* (E3), *Pinnatiramosus*, *Piterophyton* and Ordos (E4), and the ages of Yea and Bathurst Island (E5). Rechecked against full texts 2026-10-28 (`work/codex/loop1b/`): the Yea eastern localities are now unresolved, Gorstian to Emsian, in the main reading (rejected-records entry 17); Strother et al.'s (2015) specimen-level case against the Argentine Dapingian cryptospores is recorded beside Rubinstein et al.'s claim (entry 16); the Bolivian *Cooksonia* counts for E3; Zbrza, Capel Horeb, *Pinnatiramosus* and Hanadir are unchanged but now rest on full texts. M3's fossil basis (2026-10-28, `docs/audits/2026-10-28-m3-fossil-basis.md`): on Hooper et al.'s own criteria, *C. barrandei* (middle Sheinwoodian, horizon inferred from museum-box contents) predates their Homerian basis for the 431.2 Ma maximum by about 1–3 Myr |
| Q3 | How much of the Silurian–Devonian rise in first appearances and richness is biological, and how much is sampling? | statistics | active | a rise that survives correction for effort, region by region, or a stated limit; builds on Capel et al. (2022) | effort layer for both channels; regional coverage outside Europe | `docs/plan-f3.md`, event E7 |
| Q4 | Do spore types appear in step with the bodies of the plants known to produce them? | statistics | provisional | agreement or lag measured for producers with in situ spores, with the strength of each producer link stated | in situ spore records on the cards; how firm each spore–producer link is | after Q1's tail is assembled (event E6) |
| Q5 | Which widely repeated claims about early land plants fail when traced back to their sources, or have been overtaken by newer evidence but are still repeated, and which pattern-level statements rest on them? | synthesis (testing old narratives) | active, alongside other work | each claim traced to its origin, the source re-read, the correction recorded, and the dependent statements in the literature and in our own documents listed | tracing citation chains; closed sources for the originals | log each case as it is found, saying whether it failed against its source or was overtaken. Candidates so far, none yet traced through the wider literature: tracheids in *Cooksonia* known only from the Lochkovian (our own cards' claim; the 1976 Ludlow record predates it); basal Pridoli as the earliest charcoal (overtaken by Wenlock charcoal, Glasspool & Gastaldo 2022); *Horneophyton* tracheids (now disputed, Kenrick & Long 2026); Silurian *Baragwanathia* (traced to its primary sources 2026-10-28: the Gorstian rests on one contested graptolite identification at Ghin Ghin and spoil-heap graptolites at Limestone Road, so the age is unresolved rather than refuted; rejected-records entry 17); *Pinnatiramosus* as an early vascular plant (reassigned to Permian roots, Wang et al. 2013); Cambrian trilete spores (Soviet reports by Andreeva 1960 and 1962, and the Indian Bhima report of Venkatachala & Rawat 1972, whose basin is now Neoproterozoic; rejected or doubtful at vetting 2026-10-28, `data/spores/crosswalks/doc_vetting.csv`) |
| Q6 | Are vascularisation, sporophyte independence and size one evolutionary package, or separate transitions? | simulation | provisional | candidate mechanisms told apart by named observations, or shown indistinguishable with the deciding observation named | primer §6 and its six predictions; trait matrix with contested states carried as alternatives | F1/F2, after the first deliverable |
| Q7 | Which early land-plant relationships hinge on a few contested characters? | phylogeny | provisional | the influence of each character or contested coding on key nodes, from published matrices extended with our adjudications | published morphological matrices (Kenrick & Crane lineage; Clark et al. 2023); character-level adjudication | needs a decision before it starts (`AGENTS.md`) |
| Q8 | What replaced cryptospore plants with trilete-spore plants: a turnover of lineages or a shift in dominance? | statistics, simulation | provisional | spatial signatures of the competing explanations told apart after recovery tests (primer §8, question 4) | Q1 and Q4; palaeolatitude uncertainty | after Q1 and Q4 |
| Q9 | Does the Hooper et al. (2026) recalibration survive alternative maxima and placements of the eophytes? | phylogeny (clocks) | parked | the share of the 55 Myr shift owed to each calibration choice | alignment, calibration tables, prior/posterior outputs are held (`data/external/deposits/` and git-ignored `data/external/local/deposits/`); their version correspondence is not yet established. Hooper deposited input specifies 1% tails while the article describes 2.5% (Codex, 2026-10-28; review F3-R1). The bounded check reproduces the rounded node-184 summary but does not link the output to the control file. | Bounded check complete: all 5,001 saved rows and independently clade-matched output-tree HPDs recorded in `data/q9/hooper2026-provenance/` and `docs/audits/2026-10-29-q9-provenance-check.md`. Preliminary double burn-in deletion corrected; Board 2490–2494 is superseded by the final handoff. A controlled comparison of the deposited 1% and described 2.5% specifications is the next proposed diagnostic; it can quantify sensitivity but cannot prove historical provenance. No full clock reanalysis run |
| Q10 | How much did early vegetation weather, bury carbon and raise O2? | simulation | parked | which parameters dominate, with each input marked as observed or assumed (primer §3, §8 questions 1 and 6) | productivity, P release and fire-threshold inputs; charcoal record | F5, later |

### Literature access, 2026-10-29 (Q1, Q2)

The regional-spore follow-up secured six studies plus the Ghelli 2017 update in
seven publisher PDFs, with the shared Ghelli KML map. All seven queued rows are
now held; `docs/audits/2026-10-29-regional-spores-batch.md` records identities,
year corrections and checks. The 2016/2017 Ghelli pair is one study with an update,
not independent evidence. Scientific readings and occurrence adjudication remain
pending; Q1/Q2 are unchanged on acquisition alone.

Kraft & Kvaček 2017 is now held in full (`library/closed/kraft2017.pdf`, provenance
in `library/closed.tsv`). The earlier access obstacle is resolved through a joint
Chrome diagnosis; its scientific reading and the affected Baragwanathia claims
remain pending. No question or age interpretation changes on acquisition alone.

Garratt & Rickards 1984 is also now held in full (`library/closed/garrattrickards1984.pdf`,
provenance in `library/closed.tsv`). The UTAS-proxied reader completed loading and
downloaded successfully. The Yea age reading remains pending source re-check.

Garratt et al. 1984 is now held in full as well (`library/closed/garratt1984.pdf`,
provenance in `library/closed.tsv`). The LibKey route delivered the four-page
Oxford/Silverchair PDF without a new login or challenge; scientific re-reading
for Q1/Q2 remains pending.

The autonomous literature follow-up recovered Raevskaya 2016, Tang 2017 and
Strother et al. 1996 in publisher form, plus Strother 2000 as a 23-page author
preprint. The original Strother 1996 sample mapping can now be checked against the
primary text (Q1/Q2). The subsequent source check inventories 14 chart depths and links the 190.7 m specimen exactly to the 2015 re-examination, carrying the primary horizon-scoped trilete negative into that existing unit. Complete processed-sample coverage remains unverified; see `data/units/frames.csv` and the repair/frame audit. Across the
twenty-paper pilot, twelve full texts are now held and eight remain pending;
`docs/audits/2026-10-29-literature-recovery.md` records the versions and blockers.

On Barry's instruction, request candidates were parked separately on 29 October
2026 (`docs/literature-requests.md`). The subsequent authorised six-paper Stage A
in `docs/literature-next-batch.md` secured all six full texts and Wang 2023's supplement,
after Barry resolved Liu 2016 through an immediate in-app browser download. Versions, verification
and the Iranian paper's corrected publication year (2021) are recorded in
`docs/audits/2026-10-29-six-paper-batch.md`. Q1/Q2 and spore synthesis readings are
pending. Stage B's two public author-copy candidates were subsequently recovered
in full (Mehlqvist 2012, 12 pages; Wellman 2013 chapter 29, 16 pages); see
`docs/audits/2026-10-29-researchgate-author-copies.md`. The already held Wellman
supplement remains a separate asset. Scientific interpretation is unchanged. Existing one-page
abstracts and main-paper/SI mismatches require source-kind reconciliation before
being treated as missing articles. No scientific interpretation changed.

The autonomous expansion of 29 October 2026 secured a first checkpoint of 46
further main texts, 25 supporting files and the Kubásek Table 3 erratum. Q1/Q2
now have direct access to further regional spore records, the Cooksonia
conducting-strand paper, Aglaophyton, Baragwanathia and the Ordovician
plant-like fossils reinterpreted as animals. Scientific readings remain pending.
For Q5/source handling, use the Kubásek replacement Table 3 and retain the
Hawaz manuscript, Grahn proof and Mahmoudi DOI qualifications; acquisition alone
changes no occurrence, age or trait interpretation. See the autonomous-expansion
audit and per-file provenance register.

The second autonomous checkpoint supplies 39 further main texts and 16 supporting
files for Q1/Q2 and the wider source register. The Edwards cryptospore, eophyte and
transfer-cell papers, Ghelli 2011 and the Capel/Toledo supplements are now held.
For Q5/source handling, native text extraction from five scanned/partly scanned
older PDFs is sparse; temporary OCR supports reading but is not a verified numerical
transcription. The Hopkins/McBride DOI alias remains unresolved. No scientific
question or interpretation changed through acquisition; re-reading remains the
next evidence step. The second-checkpoint audit distinguishes entitlement gaps
from pending native-save controls.

The desktop-save follow-up subsequently recovered all ten Oxford candidates and
Edwards 1980/Mark 2011, including five original Mark supplements. These make the
corresponding Q1/Q2 source readings available. The earlier save blockers are
resolved; neither the new files nor their technical verification changes a
scientific interpretation. Use the rendered content of image-only plates rather
than treating an empty extracted-text page as missing evidence.
