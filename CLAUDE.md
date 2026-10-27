@AGENTS.md

## Claude-specific practice: delegating to Codex

Barry's allocation (chat, 2026-10-27): his Codex (OpenAI) allocation is much larger than his
Anthropic one, and he values Claude models for higher-level work. So spend Anthropic tokens on
design, synthesis, judgement and adjudication. Outsource legwork to Codex freely: "you can be
rather spendthrift on what legwork you outsource to Terra or Sol".

- **Route to Codex:** structured extraction, classification, digitisation, crosswalks and
  table-building, meaning any job whose output can be constrained to a schema and checked by
  machine. Use `gpt-6.1-terra` at high effort for mechanical work and `gpt-6.1-sol` at high for
  knowledge-heavy classification.
- **Keep on Claude:** source-critical synthesis (cards, reviews, the primer) until a bake-off
  shows that Codex's sourcing holds up, plus the judgement calls and the integration.
- **Invocation:** `codex [--search] exec -m <model> -c model_reasoning_effort=high -s read-only
  -C <repo> --skip-git-repo-check --ephemeral --output-schema <schema.json> -o <out.json>
  "<prompt>" < /dev/null`. `--search` goes before `exec`. Without `< /dev/null` the job hangs
  waiting on standard input. Run jobs in parallel in the background.
- **Guard against silent truncation.** A long single-file job can return part of its input and
  still exit 0. Chunk inputs (about 100 items or one section per job), state the expected count in
  the prompt, and check coverage after every run.
- **Verify, then audit across model families.** Check schema, vocabulary, completeness and
  verbatim presence in the source by script; spot-check by hand; have the other model family audit
  a sample. Record pilots and audits in `docs/audits/` (see `2026-10-27-codex-pilot.md`).
- **Limits on Codex jobs:** read-only sandbox, no git, no personal data. Codex reads `AGENTS.md`,
  so the project conventions apply to it too.
