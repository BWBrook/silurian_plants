# F3 analysis specifications

One TOML file per analysis. A specification fixes everything that is a choice rather than evidence, before the analysis runs (`docs/f3-shape.md` v3, "Sampling units"):
- the event and the reading;
- the fossil-to-node mapping;
- the first-appearance rule and the reference window;
- the older units and the origin domain;
- the history classes;
- the inference settings.

The evidence lives in Codex's sampling-unit tables (`data/units/`), and a specification pins them by SHA-256 when it is run. Claude owns this folder.

- **Draft specifications** carry `status = "draft"`. They may change until the validation study is fixed.
- **Frozen specifications** carry `status = "frozen"`, a date and the commit that froze them. A frozen specification is never edited: a change makes a new file with a new `id`. Real-data runs use frozen specifications only.

## Fields

| Table | Field | Meaning |
|---|---|---|
| `spec` | `id`, `status`, `maximum`, `event`, `reading`, `node`, `max_ma`, `mapping` | which maximum is tested, against which event, under which named reading (`data/occurrences/readings.csv`) and which fossil-to-node mapping |
| `data` | `units`, `outcomes`, `units_sha256`, `outcomes_sha256` | the evidence tables and their hashes (filled when frozen) |
| `first_appearance` | `rule`, `reference_stages` | how the reference boundary τ is set from the record, and how many stages after it form the reference window |
| `reference` | `class_field`, `min_units_per_class` | the eligibility-class field, and the reference support a class needs before its rate is used |
| `older` | `domain_ma` | the origin domain; it extends past the oldest unit, and a profile reaching its edge is unbounded |
| `history` | `classes`, `h1_ceiling`, `delays_ma`, `logistic_g`, `logistic_h_frac` | the declared history classes; H1's ceiling (any path up to it, so pulses of any duration); H0m's delays; the logistic grid (steepness per Myr, midpoint as a fraction of T − τ) |
| `inference` | `alpha`, `readouts`, `cluster_shape_k`, `age_draws`, `nodes`, `boundary_model` | test level (the critical value is matched to the exact one-sided Poisson limit for the older detections: `envelope.exact_count_crit`), the f* read-outs, cluster heterogeneity (gamma shape; `inf` = none), draws of the stage boundaries (ages within a range are integrated exactly), quadrature nodes for the cluster effect, and how stage-boundary uncertainty is drawn |
