# Loop 2 private review package

Start with `manuscript.pdf` or the self-contained `manuscript.html`. The final interpretation is
in `../docs/loop2-close.md`. This package has one qualified Murzuq encounter frame; QSIM is an
exploratory model-conditional floor calculation. It does not report independent replication,
a pooled spore-share bound or a new crown date. Release and submission remain Barry's decision.

`claims.csv` links 23 claims to their evidence and limitations. `external_candidates.csv` records
the seven candidate/observation routes. `mapping.csv` separates each maximum's specimen, event,
sampling, persistence and node links. `package_manifest.csv` inventories exact candidate files
with SHA-256 and distribution scope; `data-manifest.csv` identifies excluded private inputs.

From the repository root:

```sh
uv run --with numpy --with scipy --with pytest python -m pytest models/f3/loop2/test_count_share.py models/f3/loop2/test_contamination.py models/f3/loop2/replication/test_qsim_share.py -q
python3 tools/loop2_observations.py check
uv run models/f3/loop2/replication/qsim_share.py
uv run manuscript/figures.py
quarto render manuscript/manuscript.qmd --to html
quarto render manuscript/manuscript.qmd --to pdf
python3 manuscript/package.py
```

The QSIM run needs the private, source-locked Vecoli PDF; it takes about a minute locally.
It records the seed, toy simulation parameters, runtime and source/code/output hashes. Its
simulation is a method stress test, not real-frame qualification. Figure scripts consume the
declared source tables and preserve the same interpretation in their labels.

Frozen Loop 1 and sprint-1 runs are retained without regeneration. The existing R pilot is
likewise reused; its reproduction and converged-chain receipts remain in `models/pilot-asr/out/`.
Re-running it is not required to render or inspect this package. The source archives are separate
private/upstream reproduction inputs with their original provenance and licensing.

PDF generation can change file metadata between renders; scientific tables, source bindings and
the exact final-file manifest are the evidence. Regenerate the manifest after any package edit.
