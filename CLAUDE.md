@AGENTS.md

## Claude-specific practice: delegating to Codex

The global `codex-delegate` skill and `~/.claude/bin/codex-delegate` carry the general method:
when to route work to Codex, the run command, prompts, schemas, chunking, verification, the
cross-family audit and the limits on Codex jobs. This project's routing:

- **To Codex:** structured extraction, classification, digitisation, crosswalks and
  table-building, that is, any job whose output can be constrained to a schema and checked by
  machine. Use `terra` (`gpt-6.1-terra`) at high effort for mechanical work and `sol`
  (`gpt-6.1-sol`) at high for knowledge-heavy classification.
- **On Claude:** source-critical synthesis (cards, reviews, the primer) until a bake-off shows
  that Codex's sourcing holds up, plus the judgement calls and the integration.
- **Cross-family audit:** `sol` with web search audits each Claude-drafted card. The drafting
  agent then adjudicates every finding against the source. The 2026-10-28 bake-off
  (`docs/audits/2026-10-28-card-bakeoff.md`) kept drafting on Claude: Sol's draft was accurate
  but thin.
- Record pilots and audits in `docs/audits/` (see `2026-10-27-codex-pilot.md`).
