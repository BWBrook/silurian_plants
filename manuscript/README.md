# Manuscript package (Loop 3 reconstruction)

Start with `manuscript.pdf` (or the self-contained `manuscript.html`), then `supplement.pdf`. The
paper asks what the Ordovician–Silurian record can test about the three fossil maxima behind
land-plant molecular clocks (515.5 and 459.1 Ma for crown land plants, 431.2 Ma for crown vascular
plants). It reports one qualified spore absence comparison (Murzuq), an exploratory QSIM floor
calculation, and a conditional positive-record analysis of dated body fossils. It does not report
a new crown date or independent validation of any clock. Release and submission remain Barry's decision.

`claims.csv` links each main claim to its evidence and limits. `mapping.csv` separates each maximum's
specimen, identification, sampling, persistence and node links. `external_candidates.csv` records the
spore-frame routes examined. `package_manifest.csv` inventories exact candidate files with SHA-256;
`data-manifest.csv` names excluded private inputs.

From the repository root:

```sh
uv run --with numpy --with pandas --with scipy --with pytest python -m pytest models/f3/loop3 -q
uv run manuscript/figures.py
python3 manuscript/tables.py
quarto render manuscript/manuscript.qmd
quarto render manuscript/supplement.qmd
python3 manuscript/package.py
```

`figures.py` draws the four main figures and the QSIM supplement figure from frozen or reviewed
tables, recording input and output hashes in `figures/figures.json`. `tables.py` writes the
supplement's body-record tables from `models/f3/loop3/out/`. The body-record analysis itself is
reproduced by the scripts in `models/f3/loop3/` (see its README); frozen Loop 1 and Loop 2 outputs
and the R pilot are reused without regeneration. Copyrighted sources stay in the ignored
`library/closed/`; third-party deposits are fetched by script and hash-checked.

PDF generation can change file metadata between renders; the scientific tables, source bindings and
the final-file manifest are the evidence. Regenerate the manifest after any package edit.
