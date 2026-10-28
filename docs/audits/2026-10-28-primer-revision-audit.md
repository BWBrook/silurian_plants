# Primer revision: cross-family audit and adjudication (2026-10-28)

**What was audited.** The revision of `docs/primer.md` that Claude Opus 5.5 made after Barry Brook's review of 2026-10-28; the new §6, "Biological transitions"; and the matching changes to `taxa/horneophyton-lignieri.md`. See `docs/decisions.md`.

## Method

- **Two audit jobs.** Codex `gpt-6.1-sol` at high effort, with web search, ran both. The job files are in `work/codex/primer-audit/`.
  - **Revision job.** It read the diff and checked the 25 most consequential added or changed claims against primary sources. It also judged whether each of Barry's points was addressed, from a paraphrased list.
  - **§6 job.** It checked §6's 25 most consequential claims against the sources behind the cards.

  Each job also listed omissions.
- **Adjudication.** Claude Opus 5.5 checked every finding that was not "supported" against the source before changing anything. The checks used the Harrigan et al., Kenrick & Long, Hooper et al., Su et al., Grossman & Joachimski, Lenton et al. and Witkowski et al. full texts, the Gess & Prestianni full text, the cards, and the repository's climate-slice table. Codex verdicts were treated as leads, not rulings.
- **Final checks.** `cards.py check` passes on all 70 cards, and `dois` passes on every DOI.

## Verdicts (Codex, before adjudication)

| Job | Supported | Wrong | Misattributed | Imprecise | Overstated | Unverifiable | Omissions |
|---|---|---|---|---|---|---|---|
| Revision (§1–5, §7–8, *Horneophyton* card) | 14 | 3 | 1 | 6 | 1 | 0 | 11 |
| §6, biological transitions | 10 | 3 | 0 | 9 | 1 | 2 | 10 |
| **Total (50 claims)** | **24** | **6** | **1** | **15** | **2** | **2** | **21** |

On Barry's six substantive points, the revision job judged all six "partly" addressed, and the Ediacaran correction "fully".

## What the audit changed

- **Wrong, and fixed:**
  - **Trotter et al. (2016).** The isotope variable had been mislabelled as seawater δ18O; it is conodont apatite δ18O, which records temperature and seawater composition together.
  - ***Horneophyton* corm.** Kenrick & Long (2026) describe brown-walled conducting cells in the corm, against Kerp (2017). Both accounts are now given. Their functional reading is solute transport, with no clear water-conducting cells; it is no longer stretched to "solutes and water".
  - **Ghost lineages.** "Extinction before the first fossil" was a slip. The text now says origination before the first fossil and extinction after the last, estimable with preservation models; clocks bear on origination only.
  - **Height reconstructions.** "No plants in situ" was wrong: Rhynie preserves plants in growth position.
  - **Euphyllophyte rooting.** The claim of no Early Devonian rooting structures was too strong. Doran & Tomescu (2025) propose a rooting role for emergences on *Psilophyton*.
  - **Transfer cells.** These are no longer said to be known only from Lochkovian fossils, and at a junction they would be strong evidence of nourishment, not proof.
- **Imprecise or misattributed, and fixed:**
  - **Lenton et al. (2016).** The 24-fold P weathering comes from a moss on granite, the liverwort figure is 9–13-fold, and productivity depends on assumed CO2 (7.8, 18.7 and 27.1 GtC yr⁻¹ at 4, 8 and 16 PAL) as well as on ice.
  - **Witkowski et al. (2018).** The Devonian data lie at 380–355 Ma, outside the window, and the Ordovician rise rests on assumed temperatures.
  - **Foster et al. (2017).** Their 2,000 ppm is a long-term level, not a maximum.
  - **HadCM3L CO2 in the window.** It is about 1,300–2,100 ppm, not 1,093–2,513, which spans all the slices extracted. The climate README is corrected too.
  - **Glacial cycles.** Ghienne et al.'s three cycles span the late Katian to the earliest Silurian.
  - **Hooper et al.'s bounds.** Both are soft, at 2.5%, and they doubt the Dalby trilete marks themselves.
  - **Su et al.'s three strategies.** All three are now given, including 518–500 Ma.
  - **Grossman & Joachimski's counts.** The counts after preservation screening are now given.
  - ***Asteroxylon* leaves.** They lack veins, so the early lycopsids are no longer called "microphyllous".
  - **Bathurst Island.** Measurements from two taxa had been pooled; they are now attributed to each.
  - ***Psilotum*.** Assimilation and hydraulic conductance are now reported separately.
  - **Wood.** The point now shows that wood is decoupled from axis width, not from height.
  - **Leaf timing.** The delay was mis-transferred from the trimerophytes card. It is about 23–30 Myr, not 10–25: that card's 10–25 Myr compares different events.
- **Omissions added:**
  - Harrigan et al.'s model already uses the Parry Rhynie date, so testing Rhynie against it is circular.
  - Clark et al. (2023) did place eophytes, as stem-tracheophytes.
  - *Elandia itshoba*, a further sporophyte–gametophyte attachment candidate (Gess & Prestianni 2021).
  - Rhynie gametophytes were unisexual, so homospory does not fix the mating system.
  - Trait dissociation rejects obligatory co-occurrence, not every correlated model, and a fixed-order package does not predict simultaneous first appearances.
  - Rootless hosts show that fungi did not need roots. They do not show that symbiosis came first.
- **New leads** (in `2026-10-28-card-consistency-leads.csv`):
  - eophyte placement (Clark against Hooper);
  - *Horneophyton* spore variation as possible taphonomy;
  - the height of *Pertica*.

  The Sonnet agent that drafted §6 also logged seven card conflicts.

## Findings not acted on, with reasons

- **The card's Rhynie dates labelled "Pragian and earliest Emsian".** The card states where the numerical dates fall on the project timescale, and the stage assignment rests on spores. That is consistent with the new rule.
- **"Tractable" still means buildable.** This is deliberate. §8 now defines the word that way and makes an identifiability test the first step of every question.
- **Two claims the auditor could not verify.** The *Tortilicaulis* specimen tally and the *Steganotheca* sporangium count come from full texts that the card agents read (Morris et al. 2024; Edwards 1970), so they are kept.
- ***Calyculiphyton* axes over 20 cm** (Kenrick 2017). Not added: no card covers it yet, and §6 makes no claim about gametophyte size limits.
