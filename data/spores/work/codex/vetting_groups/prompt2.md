You are refining a vetting of early dispersed-spore records for a palaeobotany research dataset in this repository (read AGENTS.md; do not edit any file).

Input: data/spores/work/codex/vetting_groups/groups2.csv. Each row is one record group (94 in all): the reports of one spore class group (cryptospore, trilete or other) from one Palynodata document, at one location, with one assigned ICS stage range. All are older than the Wenlock. Each row also carries the document-level verdict and reason from an earlier pass, which judged whole documents. A document can be credible overall while one of its age–location groups is not, for example a Floian age attached to cryptospores whose demonstrated occurrences are younger.

For EVERY group (all 94; copy group_id exactly) return:
- verdict:
  - accept: this taxon group is credibly present at this location within this stage range;
  - doubtful: plausible but uncorroborated, a pooled or misassigned age, or an identification in question;
  - reject: the stage range is not supported for these taxa, or the identification is regarded as erroneous.
- reason: one sentence.

Points to weigh:
- trilete spores are accepted from the Katian onward and contested earlier;
- cryptospores are accepted from the Dapingian–Darriwilian;
- ages taken from co-occurring marine palynomorphs or from a whole formation may not apply to the spores;
- modern taxon names (e.g. living mosses) in old literature are not fossil records.

Use web search where it helps. Do not invent sources. Return JSON only, matching the schema, for all 94 groups.
