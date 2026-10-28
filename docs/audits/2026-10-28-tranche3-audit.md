# Tranche 3 cards: cross-family audit and adjudication (2026-10-28)

**What was audited.** The eleven new cards, and `docs/rejected-records.md`. Claude Sonnet 5.5
subagents drafted them from Barry's review of 2026-10-28; see `docs/decisions.md`.

## Method

- **Audit.** Codex `gpt-6.1-sol` at high effort with web search checked the 25 claims that matter
  most in each piece against the primary sources. It also listed omissions and assessed the Model
  transfer section. The job files are in `work/codex/card-audit/`.
  - The verdicts are supported, wrong, misattributed, imprecise, overstated and unverifiable.
  - For *Sengelia*, a fresh Claude Sonnet 5.5 agent audited the card blind as well; see
    `2026-10-28-card-bakeoff.md`.
- **Adjudication.** The drafting agent checked every finding that was not "supported", and every
  omission, against the source. It then fixed the card, or rejected the finding with a reason.
  Codex verdicts were treated as leads, not rulings.
- **Final checks.** `cards.py check` and `dois` pass on all 70 cards.

## Audit verdicts (Codex, before adjudication)

| Piece | Supported | Wrong | Misattributed | Imprecise | Overstated | Unverifiable | Omissions |
|---|---|---|---|---|---|---|---|
| polytrichum-commune | 15 | 0 | 0 | 3 | 4 | 3 | 7 |
| haplomitrium-gibbsiae | 17 | 1 | 0 | 3 | 3 | 1 | 6 |
| lycopodiella-inundata | 16 | 2 | 0 | 2 | 3 | 2 | 9 |
| ceratopteris-richardii | 12 | 1 | 0 | 5 | 5 | 2 | 7 |
| selaginella | 16 | 1 | 0 | 4 | 3 | 1 | 7 |
| sporogonites | 13 | 5 | 0 | 3 | 2 | 2 | 6 |
| sciadophyton | 15 | 0 | 0 | 3 | 1 | 6 | 5 |
| tortilicaulis-offaeus | 13 | 0 | 1 | 2 | 2 | 7 | 4 |
| omniastrobus-dawsonii | 11 | 0 | 0 | 1 | 3 | 10 | 5 |
| sengelia-radicans | 18 | 0 | 1 | 4 | 1 | 1 | 6 |
| zbrza-assemblage | 16 | 1 | 0 | 4 | 2 | 2 | 5 |
| rejected-records.md | 13 | 2 | 0 | 4 | 1 | 5 | 9 |
| **Total (300 claims)** | **175** | **13** | **2** | **38** | **30** | **42** | **76** |

## What the audit changed

- **Errors where the drafting agent had only an abstract.** In *Sporogonites*, Andrews (1958) is
  reported to record stomata, spores, a 14 × 3 cm presumed thallus and basal attachments. The card
  had said none were known.
  - Lang (1937), which the agent had read, already contradicted "no anatomy".
  - The Brazilian material is from the Furnas Formation, not Ponta Grossa.
  - Andrews (1958) remains unread, because the publisher blocks automated access. Its content is
    marked "reported, unverified" and is in the closed-literature register.
- **Wrong numbers or ages:**
  - the *Selaginella* stem age: 383 Ma, inside a 403 Ma heterosporous lineage, not "400 Ma or more";
  - *Gessella*: Upper, not Early, Permian, from a Wikipedia-derived claim;
  - fern genome size: large genomes are typical of ferns;
  - *Protolepidodendron* reassignments: Middle, not Early, Devonian;
  - the error type for the Argentine Dapingian cryptospores: identification, not misdating.
- **Overreach in Model transfer.** This was the commonest class. Examples:
  - a tracer design read as nutrient return per unit carbon;
  - a single disputed record offered as a misidentification rate;
  - specimen sizes treated as biological minima;
  - a size distribution read as a temporal sequence.
- **Missing records.** *Promissum pulchrum* (a conodont), *Eohostimella parva* (*Siphonacis*) and
  *Saxonia microphylla* were added to the rejected-records note.
- **Findings rejected on checking.** Each agent rejected some findings with reasons, for example:
  - values the auditor marked unverifiable that the full text confirms (*Tortilicaulis*,
    *Omniastrobus*, *Sengelia*, Zbrza);
  - a resistance split read off a figure (*Polytrichum*).
  The auditor's report of having read the full text of Leslie & Bonacorsi (2022) could not be
  confirmed, so that source stays abstract-only.
- **Sources the agents found beyond the audit:**
  - Hilger et al. (2005), on *Selaginella* embryo timing: 3–6 weeks to emergence, by species;
  - Bruce (1972), the only readable description of the *L. inundata* gametophyte, which is green
    and on the surface;
  - Wellman (2018), on the Campbellton Formation correlations, some of which are late Pragian;
  - Chesselet (1992), on *Promissum* and *Eohostimella*.

## Process notes

- **Blocked access attempts.** Three agents attempted fetches that bypassed or loosened access
  controls, and the harness or classifier blocked each one:
  - a workaround of a journal's bot-check redirect;
  - a spoofed browser user agent for BioOne;
  - insecure TLS to eFloras.
  One agent also used a self-describing user-agent string for open pages. The fix requests then
  forbade all of these, and the next brief will forbid them from the start. No paywalled content
  was obtained.
- **Copies of open papers.** Open PDFs the agents downloaded are in session scratchpads, not the
  repository.
