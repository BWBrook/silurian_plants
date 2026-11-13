# Step 3c: reading the candidate references

Claude Opus 5.5, 11 November 2026. Receipt for the source reads behind the references added to the F3
article at step 3c (`manuscript/reconstruction/3c-full-draft.md`).

**Job.** One Codex job, `~/.claude/bin/codex-delegate -m sol -e high --search`, label `c3-cands`,
499 s, about 6.87M input tokens (6.55M cached) and 12.6k output tokens. Prompt:
`2026-11-11-3c-reference-reads-prompt.md`. Output (validated against a schema, 11 of 11 items):
`2026-11-11-3c-reference-reads.json`, which gives for each source the copy read and its URL, the
sections read, a verdict on the proposed sentence, the location of support, a quote of at most 15 words
and a rewritten sentence. The job read only legitimately hosted copies and was read-only in the
repository.

**Claude's check.** Claude downloaded four of the cited copies and found each returned quote verbatim
in the extracted text: Steemans et al. 2009 (Ghent repository), dos Reis et al. 2016 (UCL accepted
manuscript), Benton & Donoghue 2007 (Bristol-hosted PDF) and Peters et al. 2018 (author-hosted PDF).
The Utrecht copy of Cohen et al. returned an HTML page, and the Richmond copy of Kenrick & Crane did not
download, so those two were not rechecked. Codex's 3c review (`manuscript/reconstruction/codex-3c-argument-check.md`)
independently read targeted sections of Benton & Donoghue, dos Reis et al., Kenrick & Crane and Brown & Smith.

**Use.** Each draft sentence was narrowed to the job's `suggested_sentence` scope where the verdict was
"partly supports": Benton & Donoghue (absence from suitable older deposits), Ho & Phillips and
dos Reis et al. (calibration treatment can shape dates and dominate absolute-age uncertainty with large
datasets), Rubinstein et al. (Dapingian cryptospores reported as the earliest then known), and Peters
et al. (rock-unit compilations as proxies for rock availability). Gradstein et al. 2012 was read only
through the companion chart. It was dropped from the bibliography because its Crossref record lists
no authors or editors. Yang & Rannala and Parham et al. were read in Codex's 3b review
(`manuscript/reconstruction/codex-3b-reference-check.md`).

| Source | DOI | Copy read | Verdict on proposed sentence | Quote rechecked by Claude |
|---|---|---|---|---|
| lenton2012 | 10.1038/ngeo1390 | full text open | supports | — |
| benton2007 | 10.1093/molbev/msl150 | full text open | partly supports | yes |
| ho2009 | 10.1093/sysbio/syp035 | full text open | partly supports | — |
| dosreis2016 | 10.1038/nrg.2015.8 | accepted manuscript | partly supports | yes |
| brown2018 | 10.1093/sysbio/syx074 | full text open | supports | — |
| rubinstein2010 | 10.1111/j.1469-8137.2010.03433.x | full text open | partly supports | — |
| steemans2009 | 10.1126/science.1169659 | full text open | supports | yes |
| kenrick1997 | 10.1038/37918 | full text open | supports | — |
| peters2018 | 10.1029/2018GC007467 | full text open | partly supports | yes |
| cohen2013 | 10.18814/epiiugs/2013/v36i3/002 | full text open | supports | — |
| gradstein2012 | 10.1016/C2011-1-08249-8 | abstract only | partly supports | — |
