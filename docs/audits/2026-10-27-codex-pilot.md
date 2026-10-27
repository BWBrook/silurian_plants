# Codex pilot: spore-genus classification, Codex vs Claude Sonnet

2026-10-27, run by Claude Opus 5.5 at Barry's request, to judge whether Codex can take bulk
extraction work.

## Task and set-up

The task was to classify 80 dispersed-spore genera (the 40 commonest in Palynodata's
Ordovician–Devonian spore records plus 40 drawn at random, seed 20261027) into the spore classes of
`docs/spore-compilation-plan.md`, with confidence, a diagnostic basis and a source. Both arms had
the same prompt (`data/spores/work/codex/genera_pilot/prompt.md`) and web search, and worked
independently.

- **Codex:** `codex --search exec -m gpt-6.1-sol -c model_reasoning_effort=high -s read-only
  --output-schema …`, with output constrained to a JSON Schema. It took 7.7 min and used about 204k
  Codex tokens.
- **Claude:** Claude Sonnet 5.5, as a subagent writing CSV. It took 20 min and used about 305k
  tokens.

## Result

- **Coverage:** both arms covered all 80 genera.
- **Class agreement:** 75 of 80. Among the 47 genera that both arms rated high confidence, all 47
  agreed.
- **The 5 disagreements** were all heterogeneous zonate or camerate trilete form genera
  (*Perotrilites*, *Trematozonotriletes*, *Trilobozonotriletes*, *Camarozonotriletes*,
  *Trilites*), whose species include smooth and sculptured forms. Codex returned `uncertain`;
  Sonnet assigned an ornament at medium or low confidence. Both treat them as trilete.
- **Resolution:** a `trilete-unspecified` class was added, and the five disagreements were set to it.
- **Sources:** Codex marked 14 genera "none checked"; Sonnet read primary sources directly for
  about 40.

## Decision

Codex `gpt-6.1-sol` at high effort ran the remaining 637 genera, split into six chunks of about
107, each validated for completeness. The quality was equivalent to Sonnet on this task, and the
work runs on Barry's OpenAI plan rather than his Claude budget.

## Lessons for running Codex

- `codex exec` waits on standard input when none is attached. Run it with `< /dev/null`.
- `--search` is a top-level flag: `codex --search exec …`.
- Do not trust a long single-file job to read the whole input. The first Wellman digitisation
  (`gpt-6.1-terra`) returned 6 of about 144 entries and still exited 0. Split inputs into chunks,
  state the expected count in the prompt, and check counts after the run. The chunked rerun
  returned all 144 entries, and all 1,430 taxa were found verbatim in the source.
