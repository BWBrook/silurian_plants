# Independent raster checks

The source reviewer used these calculations separately from the production vector
extractor. Paths were made portable during integration; the integrated scripts
were rerun and agree with the retained checks. They use the held thesis and CSV,
not the production extractor. Run from any directory, supplying a scratch output
directory:

```bash
uv run --with pymupdf==2.0.0 docs/audits/2026-10-31-libya-independent-check/raster_check.py /tmp/libya-raster-check
uv run --with pymupdf==2.0.0 docs/audits/2026-10-31-libya-independent-check/marine_raster_check.py /tmp/libya-raster-check
```

The retained CSVs record all 134 target-column checks and 158 marine-presence
checks. A28i's 24 rows have no target column. The JSON also checks the source,
production script and table hashes, material joins and target headers. Raster
checks use the upper panel; the production extractor separately compares both
panels. Neither calculation assigns biological readings or binary outcomes.

The six rendered well headers/point alignments and pivotal prose/plate passages
were also inspected visually. Copyrighted source images remain local and are
not included here. Findings are integrated into `../2026-10-31-libya-event-map.md`.
