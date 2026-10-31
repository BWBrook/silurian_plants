# Sprint 2 review and fixes (Claude)

31 October 2026. Claude Opus 5.5 reviewing Codex's sprint 2 (`d17d033`, `444faa6`; Board 2710), as the
agreed sequence requires (`sprints-2026-11.md`). Codex's sprint-1 counter-review and the joint reconciliation
follow. Three independent Claude Sonnet 5.5 subagents read the primary sources without access to this review's
reasoning: (A) Qusaiba and Samphire, (B) Tennessee, Shandong, Argentina, Hanadir and Paraguay, (C) the M3 sources.
Questions Q1, Q2 and Q5.

**Verdict.** Codex's central findings hold. No M1 or M3 design is admissible from the held sources, and the
source-to-table mappings reproduce. The review closes one roster gap, which strengthens the M1 result. It states
the decisive M1 logic more precisely, adds the inclusive-reading consequence that the ledger left out, and corrects
some small source readings. No F3 code, frozen M2 output or qualification changed, so nothing downstream is
invalidated.

## What was reproduced

- `tools/sprint2.py check`: 23 source hashes, 21 admission entries and 81 receipt files all match before any
  edit. `tools/units.py check`: 49 units and 294 outcomes.
- **Qusaiba E2 map (A).** The 37 columns, 226 dyad/tetrad marks and every-column-positive status were rebuilt
  from word coordinates on Wellman et al. (2015) Table 2 (printed p.116), without Codex's code. There is no
  column-level disagreement.
  - Row classes follow the caption's colour key: 10 dyad rows, 10 tetrad rows, and *Sphaerosaccus glabellus*.
    *S. glabellus* counts as a tetrad by row colour alone. It is never a column's only mark, so excluding it
    changes no outcome (226 marks become 223).
  - The cryptospore monads (*Rugosphaera*) are correctly excluded.
  - Header labels print "m". Plate captions and the Fig. 3 log use feet with the same numbers, which supports the
    feet interpretation.
- **Samphire (A).** Balme (1961) has six samples. Only sample 6 (core 4) is Ordovician: black shale with
  graptolites, "Lower Ordovician", no depth (printed p.26). Other attributions:
  - "Definite spores were absent" is Balme's. The bracketed "trilete" is Strother & Foster's (2021 SI p.2).
  - The 4090–4100 ft interval comes from the 2021 SI.
  - The Floian age is Nicoll's conodont age, cited in the 2021 main text. It is not Balme's.
  - Balme never mentions dyads or tetrads, and the term "cryptospore" postdates him. Codex's "unresolved, no
    binary zero" is the right strength.
- **Cambrian, Argentine, Saudi and Paraguayan sources (B).** All decisive limits hold:
  - Strother (2016) gives eleven plate-source samples and no sample table.
  - Wang et al. (2022) SI1: 463 distinct specimens (contiguous PB23898–PB24360). Prefixes are Y10 72, Y11 363 and
    Y13 28. Every row has the same locality and horizon. Nothing maps specimens to the thirteen stated samples.
  - The 256-specimen percentages cannot be inverted into integer counts, at 256 or at 463.
  - Rubinstein et al.: ten material IDs. The 2011 study has five samples with 8, 74, 130, 69 and 166 specimens
    (447 in total).
  - Strother et al. (1996) Fig. 2 has fourteen depths and a mean count of 154.
  - Steemans & Pereira (2002) used 53 samples but give no log.
- **M3 (C).** No held source supplies a searched-negative denominator. `m3/reproduce.py` regenerates all nine
  derived tables byte for byte; only the timestamp in its receipt changes. The five per-block scenarios are exact
  and minimal. A keyword scan of about 290 held PDFs found no Silurian megafossil search reported with its
  negative outcomes.
- **Synthesis numbers.** The memo's LY-MZ-CU table matches `m2_results.csv` exactly. MZ ρ = 1 acceptance cell B1
  reads 260 H0c claims and 16 misses, as the memo states. All 27 conditional-sampling rows recompute exactly.

## The roster gap: three frames not assessed for E2

`source_frame_map.csv` left Borenshult, Libya and Ghelli outside the M1 assessment. The plan maps designs to all
seven legacy frames, and Borenshult is the most complete E2 frame held: 34 analysed samples, each with an explicit
E2 outcome and eligible. The review assessed all three.

- **Borenshult-1, within-section E2 design.** `review/borenshult_e2_screen.py` uses the sprint-1 screen unchanged:
  the M2 common settings, ρ = 1, one cluster and reported stages.
  - **Main reading:** τ is the Sandbian base (458.2 Ma), with 21 of 31 reference samples positive. The only secure
    older zero is BOR-71.1, and the screen fails (LR 2.21 against 5.99).
  - **Inclusive and outlier readings:** the Darriwilian detection at 67.6 m makes τ the Darriwilian base, with no
    older unit, so S0 fails.
  - **The only passing variant** codes the two disputed Darriwilian forms (67.6 m and 59.1 m) as zeros, giving
    LR 6.28. Those two forms are detections under the wider readings, so the pass comes entirely from turning
    disputed presences into absences.
  - Sprint 1's declared primary variant excludes unresolved records for the same reason.
- **Libya (Murzuq).** All 35 Hawaz cuttings, the Darriwilian and oldest unit, carry non-trilete green-group
  reports. In the thesis legend that group holds the cryptospores, with *A. dilutus* as its only trilete. The count
  comes from joining `libya_chart_reports.csv` to `libya_appendix1.csv`. No older exposure exists.
- **Ghelli.** Only the 27 Ghelli Formation samples are tabulated. The older formations' samples lack identities
  and ages (`frames.csv`), so no older units can be built.

All three are recorded in `source_frame_map.csv`. None is admitted.

## The decisive M1 logic, stated precisely

The non-admission rests on outcome coding as much as on inventory: **no older unit in any held frame is a secure
E2 zero under any reading.** Older material falls into two groups:

- **Material containing E2-type forms of disputed affinity.** These are unresolved under the main reading and
  detected under inclusive. The group includes:
  - the Tennessee and Shandong forms. Wang et al. Plate I.11 is captioned "A tetrahedral tetrad".
  - Samphire cores 6 and 8;
  - Argentine 7999.

  Strother (2016, p.39) says "abundant isometric tetrads first occur in the Darriwilian" at the current sampling
  level. That is a population statement about abundance, not a per-sample absence of tetrads.
- **Material lacking target-specific reporting.** This covers Samphire core 4, and Argentine 7584. In 7584 the
  2011 count of 8 specimens has no spore-like form, while the text places them at "all the sampling levels".

A design passes only if disputed presences become zeros, as the Borenshult variant shows. The ledger said "no
unreported or disputed E2 outcome becomes zero". The review adds that this rule, not only the missing rosters,
decides the M1 answer. Under the project's conventions it is the right rule. We declined subagent B's proposal to
screen the younger-than-M1 combinations, such as the selected Cambrian samples against Saudi references, on this
ground: their older outcomes are not zeros.

**The inclusive reading turns M1 into an occurrence question.** The ledger recorded "no older negative vector" for
the Tennessee and Shandong groups, but missed the larger consequence.

- **E2 date under the inclusive reading.** The Stage 4 forms are E2 itself. Wang's Shandong assemblage is Stage 4
  (514.5–506.5 Ma; the authors give ca. 514–509 Ma, p.2). Strother's Rome Formation sample SB01-14 is "Series 2,
  Stage 4" in the text (p.33). Observed E2 is therefore no younger than about 514.5 Ma, only about 1 Myr below
  M1's 515.5 Ma.
- **SB01-14's age.** Strother's Fig. 1 caption is weaker ("probably Series 2", 521.0–506.5 Ma). If the text's
  Stage 4 were not accepted, an inclusive-reading occurrence could predate M1.
- **What testing M1 then needs.** An absence test needs productive Stage 3 or Terreneuvian material. None is held,
  and the evidence ranking should name that class explicitly.
- **Wang et al.'s own framing.** They cite the c. 515 Ma clock origin directly (p.6).

The ledger rows, the Shandong sentence in the Cambrian audit and the memo are amended to say this.

## Corrections made

| File | Correction | Source |
|---|---|---|
| `m1_admission.csv` | Inclusive and outlier rows for Tennessee and Shandong state the occurrence consequence. Tennessee age evidence gives Stage 4 for SB01-14 (text p.33) and the p.39 population statement. Hanadir: an undigitised per-depth cryptospore fraction exists (Fig. 2), but no dyad/tetrad-specific map. Paraguay: the text gives partial presence by borehole (*L. divellomedia* in RD-116 except the last six very poor samples; RD-115 from 139.45 m). | B |
| `source_frame_map.csv` | Borenshult, Libya and Ghelli assessed; none admitted. | review |
| `cambrian_argentina/extract_tables.py` and the Strother inventory | SB01-14 age label follows the p.33 text, with the caption caveat. The table was regenerated; no other output changed. | B |
| `samphire1961_inventory.csv` and `frame_samples.csv` | "Rich" becomes "Fairly rich… at least five spinose forms". Balme's "Good" is labelled as quality of separation, not recovery. Sample 6 locator sharpened. | A |
| `m3/m3_source_denominator_assessment.csv` | Fossil Imprint Fig. 1 is on p.329; descriptions are on pp.330–331. | C |
| `m3/primary_material_inventory.csv` | The Irish fossil-free mudstone is a lamina-scale barren-facies note, with no fossils of any kind (1983 p.20: siltstones "frequently fossiliferous"). It is not a plant-specific negative. | C |
| `audits/…-cambrian-argentina.md`, memo | The Shandong sentence is corrected, and a review paragraph and table entry are added. | review |

Codex's independent-check transcription (`independent_check/check_parent.py`) is dated evidence and is left as
written; its "Rich" wording is superseded here. `m3/receipt.json` is likewise a dated snapshot. The sprint-2
receipt was regenerated to bind the corrected files.

## Further details recorded, not changed

- **Hanadir.** Subagent B's pixel reading of Fig. 2 at 400 dpi shows no visible cryptospore segment at 330.1,
  341.9 and 401.9 m (the deepest), and about 8% at 155.9 and 190.7 m. The reading is indicative and not
  digitised. It matters for a future numerical-age or reference-rate design, not for M1 admission: all fourteen
  depths are Darriwilian.
- **E2 definition consistency.** The plan defines E2 as "first cryptospores accepted as embryophytic", with no
  monad exclusion. Paraguay's E2 presence rests partly on the naked monad *L. divellomedia*, while the Qusaiba
  extraction omits monads. Qusaiba is positive in every column either way. Any cross-source E2 design must declare
  one rule. This is for reconciliation.
- **Argentina.** Fig. 6 percentages give integer incertae-sedis counts of 42, 39, 5 and 23 in four samples, plus
  one questioned dyad in 7589. Sample 7584 has none in 8 specimens, which the text contradicts. Under the
  inclusive reading this is per-sample spore-like structure. It is not an older zero.
- **Shandong.** The catalogue has no Y12 prefix. That gap could be a missing sample, but it is an inference only.
  Plate II.7 is captioned "possibly arranged in tetrahedral configuration".
- **Strother 2016 ages.** The other samples' "Series 3 Stage 5" labels use the superseded series name. Fig. 1
  draws the Rogersville Shale across more than one biozone. Both are immaterial to M1, because all of it is
  younger.
- **M3.** Further details from the sources:
  - Edwards, Feehan & Smith (1983) p.35 records a newly opened section, an excavation unit with no counts.
  - About a third of the fertile specimens are branched (p.23), which bears on per-fragment E3 detection.
  - Libertín et al.'s supplement labels its units A–F, inconsistently with its own text. Only the Fossil Imprint
    paper numbers them 1–6.
  - Strullu-Derrien et al. (2010) Fig. 3 marks plants on 5 of 14 logs. That covers any plant fragment, is not a
    declared search, and the site is Pragian.
- **Leads, not admissions.** These are held or cited but off the roster:
  - Baldwin et al. (2004): Bright Angel Shale, about one sample per 7 m. It is Stage 5, so younger than M1.
  - Strother (2000).
  - Wang et al. Table 1's questioned Stage 4 "*Tetrahedraletes medinensis*?" from the Balang Formation (Yin et al.
    2021), which bears on the inclusive and outlier readings.

## Codex's findings on sprint 1

Codex's reuse audit is right on each point.

- **Receipts.** They do not bind the active declaration, the source inputs or `validate.py`.
- **Calibration and shifts.** Calibration completeness, finite shifts and protocol compatibility are not enforced.
- **`m2.py`.** It attaches a qualification without validating it.
- **Boundary age.** `qualify.py` hard-codes the 469.4 Ma boundary age.

Codex is also right on two points of my sprint-1 wording:

- **"P(a false claim) ≤ 0.05 per screen-passing record"** (`2026-10-31-m2-real-designs.md`) overstates the
  acceptance contract. What the contract supports is the 0.93 floor on a finite grid, with the observed worst
  false-claim frequency at 0.037.
- **"Uninformative at realistic early intensities"** assumes a realism the bounds do not establish.

These belong to Codex's scheduled sprint-1 review/fix and are left for it, to keep that review independent.

## Structural review

The sprint-2 structure keeps inventories, readings and numerical designs separate, and it served the review: every
claim traced to a file and locator. Two assumptions were exposed:

- **Outcome coding of disputed forms.** It is as decisive as inventory completeness, and should be stated
  wherever an absence design is declared.
- **The inclusive reading.** It changes M1 from an absence question to an occurrence question, so the evidence
  ranking needs a reading-specific entry: productive pre-514.5 Ma material.

No question's status changed: Q1, Q2 and Q5 remain open.
