# Sprint 2 evidence package

31 October 2026, Codex. Source roster `d17d033`, after sprint-1 handoff
`63ca45e`. This package records source admission and conditional planning.
It contains no binding numerical M1/M3 result or inferred negative trials.
The combined memo is `docs/sprint2-results-and-value-of-information.md`.

| Product | Grain and use |
|---|---|
| `m1_admission.csv` | Seven source groups × three named readings; every group fails numerical older/reference admission for an explicit reason. |
| `source_frame_map.csv` | Maps the source groups to the seven legacy candidate frames and explicitly records the three legacy frames outside this M1 assessment. |
| `source_files.csv` | Twenty-three exact held primary/companion files and their verified hashes. Copyrighted originals are local, not committed. |
| `samphire1961_inventory.csv` | Six report entries, only one Ordovician. Original language and later identity/age interpretations stay distinct. |
| `qusaiba_e2_reports.csv` | Thirty-seven source columns with dyad/tetrad reports; literal depth labels, core labels and source locators retained. Reference candidate only. |
| `cambrian_argentina/` | Eleven selected plate-source identifiers; 463 catalogue specimens; ten deduplicated Argentine materials and 125 percentage cells for the five-sample subset. These are not equivalent trials. |
| `palynodata/` | Full-release/held-window source coverage, explicit legacy-label membership, source matches and independent regeneration receipt. No sample negatives. |
| `m3/` | Database grain/field coverage, six primary-source denominator decisions, material-count distinctions and hypothetical planning examples. |
| `pipeline/` | Small development smoke, root seed 20261100, and retained receipts/replicates. Not binding qualification. |
| `conditional_sampling.csv` | Twenty-seven hypothetical known-rate/independent-block scenarios. No probabilities fitted from these sources. |
| `independent_check/` | Independent raster, literal-header, source and high-precision arithmetic evidence; original review receipts and final integration checks distinguished. |
| `crossref_identity.json` | Seven publication identities verified by DOI, title and first author against Crossref; no personal data sent. |

The source-admission ledger is a manual scientific assessment with explicit
locators. The Tennessee and Argentine numeric transcriptions are checked
source readings embedded in their reproducer; code does not discover or
automatically validate their interpretation. The Shandong catalogue is read
directly from XLSX XML. Qusaiba's text-coordinate extraction was checked
independently against all 777 raster cells, including 226 marks, and every
core/depth header. Its join guard rejects a changed material association.

## Reproduce and verify

From the repository root, with the local source holdings available:

```sh
uv run tools/sprint2.py check
uv run tools/sprint2.py all
uv run data/units/sprint2/cambrian_argentina/extract_tables.py
uv run data/units/sprint2/m3/reproduce.py
uv run data/units/sprint2/palynodata/census.py --repo . --out /private/tmp/sp-sprint2-palynodata-recheck
uv run --with numpy data/units/sprint2/independent_check/raster_check.py
uv run data/units/sprint2/independent_check/check_parent.py
uv run tools/units.py check
```

The Palynodata script requires `mdb-export` and `bsdtar`, uses the pinned held
ZIP/MDB and writes bulky raw/regenerated files only to the supplied scratch
directory. It never downloads new material. The raster check uses Poppler;
its generated image remains in `/private/tmp/sp-sprint2-independent-check/`.
Subordinate receipts containing run times can change on rerun. The original
observed-source snapshots are dated evidence, not guarantees that future inputs
have not changed. `tools/sprint2.py check` verifies the final integrated receipt
without rewriting it; `receipt` intentionally creates a new current snapshot
after reviewed changes. It is an evidence hash manifest, not an F3 certificate.

The development smoke can be repeated with the F3 environment and the retained
runner, which redirects outputs to scratch:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run --with numpy --with scipy data/units/sprint2/pipeline/run_dev.py --design LY-H2-CU --rho 1 --phase dev --target 40 --workers 4
```

No F3 statistical code or frozen M2 outputs changed in this sprint. Open pipeline
binding/acceptance findings are in
`docs/audits/2026-10-31-sprint2-pipeline-reuse.md`; their later repair must carry
appropriate invalidation and reruns. Source non-admission does not certify that
software. Claude's sprint-2 review precedes Codex's full sprint-1 review and
joint reconciliation, as Barry requested.
