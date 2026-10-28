You are auditing a revision of `docs/primer.md` in this repository, a research programme on simulation modelling of early land-plant evolution (Late Ordovician to Early Devonian). Another AI model (Claude) made the revision after a human scientist reviewed the primer. Do not edit any file; return JSON only.

Read `AGENTS.md` (conventions), the revised `docs/primer.md` in full, and the diff of the revision in `work/codex/primer-audit/primer.diff`. Also read the revised card `taxa/horneophyton-lignieri.md`. Do not audit section 6 ("Biological transitions"); another job covers it.

The reviewer's points, paraphrased:
1. Section 1.2's rule for ages is unsafe if it re-assigns stages from radiometric dates; stages are defined by boundary stratotypes, so keep both the stratigraphic assignment and the independent numerical evidence, and investigate conflicts. Boundary resampling (open question 8) needs a joint, ordered age model, because the Devonian estimates (Harrigan et al.) have asymmetric uncertainty.
2. The phylogenetic diagram equated "lycopsids" with crown lycophytes although Asteroxylon is a stem lycophyte, and it implied a resolved branching order among extinct grades. Show a secure living backbone and attach fossil groups with their alternative placements.
3. Molecular clocks estimate lineage divergences, not a "developmental toolkit"; Hooper et al.'s 459.1 Ma bound is a soft maximum; an ancestral trilete spore does not exclude secondary cryptospory in crown descendants; the first occurrence of a total-group character is not a crown maximum without preservation and sampling assumptions; keep competing clock estimates as separate, assumption-dependent results, not a pooled range.
4. Horneophyton's tracheids are disputed by Kenrick & Long (2026; New Phytologist, doi 10.1111/nph.70850); Homerian charcoal predates the basal Pridoli "first" charcoal, and Glasspool & Gastaldo (2024; doi 10.1130/G52648.1) challenge the Devonian charcoal gap; charcoal presence constrains combustion, while scarcity also depends on fuel, preservation and sampling.
5. Environmental tables must separate proxy evidence, model outputs and assumed inputs (e.g. Lenton et al. 2016 assume CO2 = 8 PAL; their productivity estimate depends on ice cover); give each entry its target variable, coverage, method and status; tropical sea-surface and global-mean temperatures are not plant temperatures; the 1,000–3,000 ppm range should be a sensitivity scenario; observation tags should not be applied to reconstructions.
6. "Tractable" should be conditional on identifiability (can the evidence distinguish the scenarios?), with a simulation-recovery test first; fossils that calibrate a clock cannot also test it; ghost-lineage origination times are inferable under assumptions, not simply unsupported.
7. Add a section on the biological transitions (covered by the other job).
Also: the Ediacaran is part of the Neoproterozoic.

Tasks:
A. Select the 25 most consequential factual claims that the revision added or changed (the "+" lines of the diff), including every number, and check each against its primary source, using web search to read the sources (open versions, publisher pages, repositories, PMC). Give for each: claim (brief quote), section, verdict (supported | wrong | misattributed | imprecise | overstated | unverifiable), evidence (25 words or fewer), source (URL or DOI, and whether you read the full text or only an abstract).
B. Omissions: facts in the sources you read that would change the revised text.
C. For each reviewer point 1–6 and the Ediacaran correction, say whether the revision addresses it fully, partly or not, and where uncertainty is still lost (in the primer or the Horneophyton card).
D. Overall judgement in two or three sentences.

Rules: never invent a source or a quotation; if you cannot reach a source, say unverifiable. Never send an email address or other personal data to any service. Do not bypass paywalls or bot checks.
