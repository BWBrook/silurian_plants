# F3 paper: fossil maxima behind land-plant molecular clocks

The paper asks what the Ordovician–Silurian record can test about the three fossil maxima behind
land-plant molecular clocks (515.5 and 459.1 Ma for crown land plants, 431.2 Ma for crown vascular
plants). It reports one qualified spore absence comparison (Murzuq), an exploratory QSIM floor
calculation, and a conditional positive-record analysis of dated body fossils. It does not report a new
crown date or independent validation of any clock. Release and submission remain Barry's decision.

The same study is written three ways, all in `text/`, all from one evidence base:

| File | Reader | Rendered |
|---|---|---|
| `main.md` + `figures.md`, `supplement.md` + `supplement_figures.md` | scientists; the journal snapshot | `build/manuscript.pdf`, `build/supplement.pdf` |
| `brief.md` | anyone: two A4 pages, one sheet printed double-sided | `build/brief.pdf` |
| `for-agents.md` | an agent arriving cold: claims, provenance, traps, checks | read as Markdown |

`claims.csv` is the single claims ledger: every claim's ID, status (supported, provisional, refuted,
superseded), value, evidence files, verifying commit, reproduce command and limits. All four
renderings cite it, binding quoted numbers as `[428.8]{.C27}` (invisible in PDF and DOCX), and
`make -C manuscript check` runs `tools/claims.py check` to catch any drift. `mapping.csv` separates each maximum's
specimen, identification, sampling, persistence and node links. `external_candidates.csv` records the
spore-frame routes examined. `package_manifest.csv` inventories the candidate files with SHA-256;
`data-manifest.csv` names the excluded private inputs.

## Build

The paper builds with [makedoc](https://github.com/BWBrook/makedoc), expected at `~/work/makedoc`.
Profiles are in `settings/build.yaml`; `makedoc.lock.json` pins the build tool revision, checked before builds. TeX/Pandoc remain system dependencies; `uv` supplies a Python with PyYAML. From the repository root:

```sh
uv run --with numpy --with pandas --with scipy --with pytest python -m pytest models/f3/loop3 -q
uv run manuscript/figures.py      # figures and figures/figures.json hashes
python3 manuscript/tables.py      # supplement tables S3–S11, written between markers in text/supplement.md
uv run tools/refs.py build        # references/refs.yaml from references/dois.txt via Crossref
make -C manuscript check          # makedoc lint and citation audit for every profile
make -C manuscript                # PDF and DOCX into build/ (PDFs are tracked; DOCX is not)
python3 manuscript/package.py
```

Citations are Pandoc keys (`[@key]`) from the programme bibliography `references/refs.yaml`. To cite a
new work, add its DOI to `references/dois.txt` (or a CSL entry to `references/manual.yaml` if it has no
DOI), rebuild, and cite the printed key. Keys follow Better BibTeX's pattern, so a Zotero export of
the same DOIs matches. The CSL is a placeholder (Chicago author-date) until a journal is chosen;
`make -C ~/work/makedoc csl-source JOURNAL="..."` fetches a journal style.

Generated content is not edited by hand: the table blocks in `supplement.md`, `figures/`,
`references/refs.yaml`, `build/` and the manifests. The body-record analysis itself is reproduced by
`models/f3/loop3/` (see its README); frozen Loop 1 and Loop 2 outputs and the R pilot are reused
without regeneration. Copyrighted sources stay in the ignored `library/closed/`; third-party
deposits are fetched by script and hash-checked.

## Public reproduction and source access

From the repository root, `make reproduce-derived` regenerates the core Loop 3 bounds, age/shape
diagnostics, simulations, suppression/frontier tables, Murzuq sensitivities and interval witnesses in a temporary copy made only from tracked files,
then compares CSV bytes. `make rebuild-source` first restores the exact archived CC0 PBDB input
from <https://doi.org/10.5281/zenodo.24028289>, checks its compressed and raw SHA-256, rebuilds
the inventory/effort tables and performs the downstream and shared-timescale comparisons. The derived-only target explicitly skips
raw-collection timescale recomputation; the source target exercises it. Neither substitutes a
live database query. `make check-public` runs the public Loop 3 and case-binding regression tests.

`make check-sources` is separate: it reports an explicit skip when the copyrighted thesis is
unavailable and otherwise checks the held thesis-linked observation extraction. It does not
authenticate all palaeontological identifications or rerun frozen qualification. The printed receipts
state the scope; the R pilot is reused rather than rebuilt.

`dependency-manifest.csv` traverses declared ledger evidence, receipt input/output paths and local
Python imports from the candidate products. Public bulk inputs have immutable retrieval locations;
private sources are recorded without copying them. This is a declared dependency closure, not a
claim that static inspection discovers every possible runtime dependency. Numerical citation
metadata can use `value-bindings.csv` to bind a claim span to a specific table selector and field;
C27, C40 and the new C48–C52 result spans are migrated; C27 rejects the reviewer's cross-case value swap. Further
claim migration belongs with Claude's final ledger/prose integration.
