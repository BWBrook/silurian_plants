# Loop 2 Murzuq observation-basis audit

`observation_basis.csv` has one row per literal row in `data/units/libya_appendix1.csv` (164 rows).
The audit joins `libya_chart_reports.csv` and `libya_prose_support.csv` by exact well plus Decimal
depth. It preserves source strings and current source E1 statuses; it does not derive or recode an
outcome. Five chart rows have no appendix key and are retained in `unmatched_chart_rows.csv`.

The thesis's nominal 200-organic-particle palynofacies denominator is recorded as protocol metadata.
No per-row count, cryptospore percentage or trilete count is copied: the palynofacies preparation
and aggregate cryptospore group are distinct from the oxidised-residue biostratigraphic slide and
additional rare-form scan used for E1. Thus no paired count-share likelihood is admitted here.
Panel page references are locators only and were not used to digitise values.

Run `python tools/loop2_observations.py build` to regenerate outputs, or `python tools/loop2_observations.py check`
to verify the deterministic reconstruction, counts, source hashes and generated output hashes without
writing files.
