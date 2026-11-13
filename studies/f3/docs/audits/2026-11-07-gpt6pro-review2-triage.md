# GPT-6 Pro follow-up review of `342153a`: triage, source adjudication and split

Claude Opus 5.5, 7 November 2026. Barry, through the Board messenger, 7 November: "I commissioned a
second-round review of the written component of this first study from GPT-6 Pro, prior to my
focused-attention round, to make the process as efficient as possible. As the next step, please work
with Codex (but you should start) to process the new review, and revise the three parts of the paper
accordingly." The cover note, the full report (about 7,500 words) and a file of proposed replacement
text are held outside the repository at `~/input/gpt-6-pro_review_2_cover_note.md`,
`~/input/silurian_plants_followup_review_342153a.md` and `~/input/proposed_reframing_342153a.md`. The
reviewer worked on a disposable copy and changed nothing here.

Verdict: one focused consolidation round before Barry reads in detail. Priorities are a new B1
admission error, semantic errors in the brief, an audit-led narrative, and two reproduction-gate
defects. No new measurements, correspondence or clock analyses. I agree.

## Source adjudication (both agents; written before any code change)

**B1: an unenumerated event is not an absent character.** Codex's stage 2 repair set B1 from E3 or
E5 events only. That rule is sound for tracheid-only material, but `data/occurrences/README.md`
enumerated E3 claims only from the Homerian and older, while E4 and E5 run to the Pridoli. A younger
record without an E3 label was never assessed for branching. Read against the primary sources:

| Record | Primary evidence of branched fertile axes | Decision |
|---|---|---|
| `M-bohemica` (Kosov, Pridoli) | Libertín et al. 2022 (Hist. Biol. 35: 2504–2514, DOI 10.1080/08912963.2022.2144286; `library/closed/libertin2023_bohemica.pdf`): emended diagnosis "Axes branched isotomously"; holotype JE-Sch0260A/B "six- (locally seven-) times isotomously divided cluster of branches"; sporangia "borne terminally on the ultimate branches"; D 554 "twice isotomously branched terminal" (pp. 2507–2510, Figs 2, 5) | **Admit to B1 on branching (E3).** The tracheid reading (E4) and the lycophyte reading (E5, inclusive) stay separate interpretations. |
| `M-capel-horeb-ludlow` (Upper Roman Camp Beds, Whitcliffian) | Edwards & Rogerson 1979 (Geol. Mag. 116: 93–98, DOI 10.1017/S0016756800042503; read in full from Cardiff ORCA, eprint 10902): Plate 1(e) "Branching specimen of *Steganotheca striata*, Ludlow Series, NMW 77 34G 11"; Plate 1(g) "Branching specimen of *Cooksonia* sp., Ludlow Series, NMW 76 10G 1"; §3.a.2: Whitcliffian *Cooksonia* fragmentary, "only one showing characteristic branching" | **Admit to B1 on branching (E3).** The branched fertile specimens are from the same Ludlow beds as the tracheid-bearing sterile axis, which remains the separate E4 interpretation; tracheids are not transferred to the fertile specimens. |
| `M-lang-tracheid-axis` (Lochkovian) | Sterile tracheid-bearing axis only (Edwards & Kenrick 2015, fig. 2f) | **Stays out of B1.** No branching or sporangia on the represented material. |

The general rule stands: tracheids alone do not admit a unit to B1, and no blanket E4-to-B1 rule is
restored. The repair is in the data, not the rule. Each admitted record gets an E3 interpretation
citing its specimens and plates, so `b1 = E3 or E5` stays correct and the absence of an E3 row once
again means "not assessed", never "assessed absent". The reviewer's in-memory restoration gives main B1
71/69 units and constant 434.649615 Ma (from 69/67 and 434.703019). B2 is unchanged, and inclusive B1
changes only through Capel Horeb (447.397755 → 447.367027 Ma). Codex implements, regenerates and
re-binds; I check the biological descriptions.

**Yea Table 1 cell.** Libertín et al. 2024 (Rev. Palaeobot. Palynol. 320: 105017, p. 2): "Neither the
Czech nor the Australian Silurian records of *Baragwanathia* show reproductive structures (Garratt,
1978; Kraft and Kvaček, 2017)." Our card attributes sporangia to Lang & Cookson's type material, which
is now Early Devonian. **Accepted:** the cell names microphyllous leafy axes and records that no
reproductive structures are reported from the material claimed as Silurian. The B2 assignment and the
full age range are unchanged.

## Dispositions

| ID | Finding | Check | Disposition | Owner |
|---|---|---|---|---|
| F1 | B1 exclusion of *C. bohemica* and Capel Horeb | Sources above | **Accepted.** E3 interpretations and reading assignments; test asserts the two are B1 by E3 and Lang is not; regenerate B1 counts, bounds, influence and figure inputs; update C25, C39, C52 values | Codex (data, code, outputs, bindings); Claude (prose) |
| F2 | Interval results: finite-sample reference primary; conservative-rejection reading | Summary CSV: 48 units 0.03522, 49 units 0.04916, 50 units 0.06713 (finite) | **Accepted.** Table S7b shows finite-sample *p*, flags asymptotic-only passes; main text leads with the 50-unit witness and the 49-unit borderline. Replace "optimising invalidates the tests" by the sup-p argument (Berger & Boos 1994), with its conditions: supports contain the true ages, finite-sample reference, fixed history, independent observation model. A pass is a possibility, not a fit | Claude (prose, table); Codex (check the argument) |
| F3 | Brief: 429 Ma "earliest start"; continuous Oman bar; "within ten million years"; "more advanced"; "matching the youngest clock"; categorical maximum | `figures.py` fig_brief; brief.md; strict cryptospores 469.4–458.2, Oman 452.8–445.2 | **Accepted, all.** Interval bars for first records; conditional-limit label; Middle Ordovician → Late Ordovician → Silurian sequence | Claude |
| F4 | Narrative led by the audit; 415-word abstract | Word count | **Accepted.** New title, ~240-word abstract, opening, finding-led results; audit history to S7 and the charter; AI roles condensed | Claude |
| F5 | Silvestro et al. 2015, Marshall 2019 novelty calibration, CladeDate | Crossref | **Accepted.** Substantive comparison in the discussion; no claim to a new general theory | Claude |
| F6 | Frontier deserves a main figure; Fig. 2 matrix better as a table/supplement | `out/frontier.csv` | **Accepted.** New main figure from the closed form, checked against every tabulated contour; matrix moves to the supplement and a compact table of the three maxima replaces it in the main text | Claude |
| F7 | Source-to-claim sentences: Sweden (oldest definite level below bentonite), Libya (explicit vs operational zeros), *Cooksonia* arithmetic (2.2 Myr same-scale, 2.9 Myr against 431.2), Oman anatomy | `libya_prose_evidence.csv` P04; timescale scenarios | **Accepted.** C47 re-stated with explicit scales | Claude |
| F8 | Murzuq 0.4 contour out of the abstract | — | **Accepted.** Kept in results and Table 4 as an unqualified sensitivity | Claude |
| F9 | Reproduction gates: fetch prerequisite; byte comparison of optimisation CSV | Reviewer logs | **Accepted.** `check-public` depends on the archived input; numeric tolerance for float columns, exact keys, schema and hashes | Codex |
| F10 | Supplement S2.2 should specify the Murzuq likelihood and the H0c/H0/H0m/H1 restrictions | `docs/f3-shape.md` | **Accepted.** One mathematical specification and a restriction table | Codex (draft, as model owner); Claude (edit) |
| F11 | Layout: isolated figure labels, Table S2 caption, empty S5.7 heading | PDFs | **Accepted** | Claude |
| F12 | Public route to the Abuhmida thesis | Receipt hash | **Accepted.** Document the public route and hash; no redistribution | Codex |
| F13 | Biological plausibility of a given recording contrast or delay | — | **Default adopted: agnostic.** Describe processes that could produce a contrast or delay; drop "not extreme" | Barry may override |

## Split and order

1. Claude (this turn): adjudication above; F2–F8, F11 in the paper, supplement, brief and guide;
   estimands updated for F2. B1 numbers in prose stay at their current ledger values until F1 lands.
2. Codex: F1, F9, F10, F12; then a semantic reading of the revised products against `estimands.md`.
3. Claude: integrate F1 numbers and the S2.2 draft, rebuild, close.
