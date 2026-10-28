# Card-drafting bake-off: Sengelia radicans, Claude Sonnet versus Codex Sol (2026-10-28)

**Question.** Can taxon-card drafting move from Claude subagents to Codex, saving Anthropic
tokens, without losing accuracy? `CLAUDE.md` keeps source-critical synthesis on Claude "until a
bake-off shows that Codex's sourcing holds up".

## Design

- **Drafts.** The same brief, with Barry's lead, the template and the same rules, went to:
  - a Claude Sonnet 5.5 subagent, which also drafted *Omniastrobus*;
  - Codex `gpt-6.1-sol` at high effort with web search, as a read-only job returning the card as
    JSON (`work/codex/card-bakeoff/`).
  Neither saw the other's draft.
- **Blind audit.** The drafts were labelled A (Sonnet) and B (Sol). The key was kept outside the
  repository until the audits finished. Each draft was audited twice:
  - by a fresh Claude Sonnet 5.5 subagent, which audited both drafts;
  - by Codex `gpt-6.1-sol` with web search, one job per draft
    (`work/codex/card-audit/out/sengelia_A.json`, `sengelia_B.json`).
  Each auditor checked the 25 claims that matter most against the primary sources.

## Results

| Auditor | Draft | Supported | Imprecise | Overstated | Misattributed | Unverifiable | Wrong |
|---|---|---|---|---|---|---|---|
| Claude Sonnet | A (Sonnet, 3,645 words) | 22 | 1 | 1 | 0 | 1 | 0 |
| Claude Sonnet | B (Sol, 1,180 words) | 21 | 4 | 0 | 0 | 0 | 0 |
| Codex Sol | A (Sonnet) | 18 | 4 | 1 | 1 | 1 | 0 |
| Codex Sol | B (Sol) | 25 | 0 | 0 | 0 | 0 | 0 |

- **Accuracy.** Neither auditor found a wrong claim in either draft.
  - Both auditors independently caught the same main flaw in A: a 12 cm rooting depth attributed
    to two museum specimens. It is an outcrop observation.
  - In B, the Sonnet auditor found:
    - a misused `from:` marker naming the card's own species, which would have polluted
      `data/traits.csv`;
    - an internal contradiction on whether the Emsian type locality is older or younger;
    - a non-vocabulary preservation term.
- **Completeness.** B is a third the length of A. The Sonnet auditor listed the omissions in B:
  - the K-branching rule, branching intervals and rooting depth;
  - leaf size, stele width and the sampling design;
  - the microconchid frequencies, the flood-burial cycle, sporangium distribution and the
    taxonomic transfers.
  B's Model transfer names three contrasts but supplies evidence for only one.
- **Each auditor favoured its own family's draft**, Sol more strongly: 25 of 25 for B, against
  18 of 25 for A. One card is an anecdote, not a measured bias, but it argues for cross-family
  audit rather than self-audit.
- **DOIs.** Sol could not reach Crossref from its sandbox and said so. The Sonnet auditor later
  verified every DOI in both drafts, and all pass.
- **Cost.**
  - The Sol draft took 293 s and 1.76 M Codex input tokens (1.62 M cached), with 10.7 k output.
  - The Sonnet subagent used 376 k Anthropic tokens for two cards.
  - The two Sol audits took about 4–5 min each. The Sonnet audit of both drafts used 205 k
    Anthropic tokens.

## Decision (Claude Opus 5.5)

- **Drafting stays with Claude Sonnet.** Sol's draft was accurate but not complete enough to stand
  as a card without substantial expansion. Its Model transfer section did not carry the evidence
  for its own contrasts.
- **Cross-family audit by Sol becomes the default check on Claude-drafted cards.**
  - In this tranche it found real errors that self-review had missed. In *Sporogonites*, it read
    the full text of Andrews (1958), which the drafting agent had seen only as an abstract, and
    showed that stomata, spores and thallus measurements are reported.
  - The drafting agent adjudicates each finding against the source; Codex verdicts are leads, not
    rulings.
- **A second bake-off could move drafting to Codex.** It would need a prompt that specifies depth:
  required content per section and a minimum number of sourced measurements. It is worth running
  when a large card tranche next comes up.
