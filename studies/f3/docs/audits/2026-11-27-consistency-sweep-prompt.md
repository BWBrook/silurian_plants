Thank you for taking this on. It is a read-only consistency check of a scientific paper before its claims are locked. Do not edit any file and run no git commands that change state.

Repository: the current directory (silurian_plants), at commit c6139d5. Study F3 asks what fossil absences can say about molecular-clock maxima for land plants.

Read these in full:
- studies/f3/manuscript/text/main.md (the article)
- studies/f3/manuscript/text/figures.md (figure captions)
- studies/f3/manuscript/text/supplement.md and supplement_figures.md
- studies/f3/manuscript/text/brief.md (two-page brief)
- studies/f3/manuscript/text/for-agents.md (agent guide)
You may consult studies/f3/manuscript/claims.csv, value-bindings.csv and estimands.md, and the output tables they point to, to decide which of two conflicting statements is right.

Why: the texts took about two weeks of patches. The last large change was an inventory audit (supplement S5.12), which showed that several late-Silurian results depend on which occurrence inventory is used (reviewed; reviewed with Early Devonian collections restored; database-backed; database-backed with collections restored; Capel et al. species endpoints). Sentences written before that audit may still state as general what now holds only for the reviewed inventory. Later patches added: a locality shortfall against steady finding on the database-backed restored inventory; the distances between the limits and 444-452 Ma in the Discussion and Conclusion; and eight to nine related-work citations.

Find statements that are wrong or that contradict another statement. Report only these kinds:
1. Two passages (in the same or different files) that cannot both be true as worded.
2. A number, count, age, p-value or range that differs between two places that mean the same quantity, or that disagrees with the ledger or its output table.
3. A general statement ("every", "all", "in every inventory", "passes", "fails", "rejects", "steady finding fits") that the inventory audit made conditional, and that is not qualified where it stands.
4. A cross-reference to the wrong section, table, figure or panel, or to one that does not contain what is claimed.
5. A statement in the brief, the agent guide or a figure caption that says more, or something different, than the article supports.
6. Leftover wording from retired framings (for example "rulers" for the outside measures, the retired title "Older than their fossils?", or a claim that the late-Silurian finding rate was at least 0.79 of the later mean stated as a general result).

Do not report style, length, readability or missing citations. Do not report a difference that a stated qualifier in the same sentence already resolves. If you find nothing in a category, that is a fine answer.

For each finding give the file and line of each passage, a short verbatim quote of each (under 40 words), which one you judge right and why (name the evidence file or ledger row if you checked), a severity (error: a reader would be misled about a result; imprecision: true only with an unstated qualifier; crossref: wrong pointer; stale: leftover wording), and your confidence (high, medium, low). Use "uncertain" as the verdict rather than guessing. Stop at 30 findings, most serious first. Put them in a top-level "items" array. Add a "coverage" field saying which files you read in full and anything you could not check.
