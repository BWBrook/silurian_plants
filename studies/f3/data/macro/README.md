# Positive body-fossil record for Loop 3

This directory holds an inspectable occurrence inventory, not an inventory of searched empty rocks.
The reviewed analysis estimates a recoverable-record endpoint under explicit assumptions; see
`../../docs/loop3-design.md` and `../../docs/loop3-results.md`.

| File | Role |
|---|---|
| `horizons_v0.csv` | Preserved Claude pilot; superseded for inference |
| `horizons_reviewed.csv` | PBDB collection and curated observation rows, readings, ages, region/unit keys, inclusion and exclusion dispositions |
| `name_classifications.csv` | Exact 241-name classifier output, with source citations and confidence; only a stratified subset independently source-audited |
| `accepted_occurrence_links.csv` | Occurrence-to-collection and category links after the accepted-category gate |
| `material_links.csv` | Explicit source occurrence/collection IDs linking PBDB to curated material; inferred country/taxon matches are not used |
| `source_adjudications.csv` | Independent source review and material/unit decisions |
| `source_identity_map.csv` | Distinguishes the two papers called `wang2026` in different source namespaces without changing frozen source tables |
| `older_records_screen.csv` | Every older-only non-spore PBDB row in the inference domain, with database/source screen status |
| `older_candidate_adjudications.csv` | Source-specific decisions for the seven plausible/unplaced older names |
| `effort_reviewed.csv` | Stage collection-equivalents and densities per Myr, globally and by approximate region, with/without matches to the plant-filtered extract |
| `build_receipt.json` | Source, code and generated-file SHA-256 bindings |

Rebuild from the repository root with `uv run models/f3/loop3/build_reviewed.py`. It reads the held
PBDB extracts, the curated occurrence tail, the source-adjudication ledgers, original classification
outputs, project timescale and the existing all-taxa PBDB collection snapshot. The latter is at
`data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv` and is git-ignored; its
hash is in the receipt. No private literature text is copied here.

`eligible_primary` describes an input row. The primary counting units are **locality–age proxies**,
assembled separately for each category/reading by `analysis.py`. Exact memberships are in
`models/f3/loop3/out/primary_unit_membership.csv`. PBDB locality keys use formation and coordinates
rounded to 0.1 degree; these are not verified beds. Missing geographical fields preserve the
collection ID. Region assignment is the existing approximate country/state mapping for PBDB and
the source-curated assignment for the tail. These distinctions matter for dependence sensitivity.

Older records excluded as algae, cyanobacteria, trace fossils or graptolites are not observed
absences of embryophytes. Likewise, removing plant-filter matches from a collecting proxy does not
establish non-plant-only searches. Main and inclusive readings are alternatives, not samples from
an estimated probability distribution. The source audits state what primary evidence was actually
read and where decisions still rely on database records or abstracts.
