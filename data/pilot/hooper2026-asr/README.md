# Hooper et al. (2026): deposited crown-node states

Extracted by Codex, 29 October 2026. This reads published output tables; it does
not fit a tree, reconstruct characters again, or estimate innovation dates.
The source archive and its retrieval metadata remain in
`data/external/deposits/hooper2026-spore-evolution/`.

```bash
python3 tools/hooper_asr.py
Rscript tools/check_hooper_asr.R
```

The extractor needs only Python's standard library and the existing repository
Newick parser. The independent checker requires R package `ape`; checked here
with ape 5.8-1, installed in a temporary library, and R 4.6.1. It independently
uses `read.tree`, `getMRCA` and `extract.clade`, then reads every selected output
value directly from the archive. No global package installation was made.

## Contents and checks

- `crown_states.csv`: 240 rows, covering two characters, three trees, four
  methods, two crown nodes and all five labelled states per character. It holds
  208 reported values and 32 explicit `column_absent` entries. An omitted state
  column is not silently converted to zero. Reported zeros remain zeros.
- `nodes.csv`: six node identities, their defining extant tips and all descendant
  tips. Crown Embryophyta is the MRCA of the 24 extant land-plant tips; crown
  Tracheophyta is the MRCA of the 13 extant vascular-plant tips. The algal tips
  are excluded. Fossil placement changes the node's descendants, not its definition.
- `matrix_crosswalk.csv`: all 76 X21/C21 and X26/C26 comparisons for the 38
  ancestral-state matrix taxa. Each matches the master matrix exactly. This
  checks column identity and deposited coding, not the underlying biological
  observations or the twelve additional unplaced fossil samples.
- `source_inventory.csv`: the two archive hashes and the hashes of all used
  members. Archives must match the retrieval manifest before extraction.
- `receipt.json`: extraction/parser hashes and output hashes. No run timestamp
  is included, so unchanged inputs and code regenerate byte-identical outputs.

All output row labels must match the expected tree nodes and, where supplied,
tips. Every reported vector is finite, non-negative and sums to one. Every
parsimony/SCM tip assignment agrees with the focal matrix coding. The additional
`PARS_X21_ext2.csv` is byte-identical to `PARS_X21_ext.csv`; it is inventoried,
but not counted as another analysis. Numeric support labels in the eophyte tree
are ignored when deriving node indices; the original tree bytes remain hashed.

| Tree suffix | Embryophyte crown | Tracheophyte crown |
|---|---:|---:|
| ext | 31 | 32 |
| eo | 44 | 57 |
| zyg | 42 | 47 |

The independent R check agrees on all six nodes and their descendant sets,
all 208 reported values, and all 32 omitted state columns.

## Interpretation limits and a material result

X21 describes aperture: state 0 is not present; 1 hilate; 2 proximal monolete;
3 proximal trilete; 4 lateral or distal. X26 describes dispersal: state 0 is n/a;
1 tetrad; 2 dyad; 3 hilate; 4 trilete spore **or inaperturate monad**. In the extant
tree, X26 has no state-3 output column; X21 lacks a state-4 column in all trees.
These absences are retained explicitly.

These are different kinds of output: parsimony assignments, stochastic-map
frequencies, and marginal state support under ER/ARD. They are not interchangeable
probabilities, and they are not pooled. The characters were reconstructed
separately; no joint state probability or joint evolutionary history is supplied.

At the embryophyte crown, X21's modal state is proximal trilete in every method
and tree. Its ER/ARD/SCM support ranges from 0.770018 to 0.977218; parsimony assigns
state 3. However, the zyg-tree ARD reconstruction of **X26** assigns 0.700981 to
dyads, 0.297664 to hilate dispersal and **0 to state 4**, while its X21 trilete
support is 0.977218. Thus the outputs do not unanimously reconstruct *trilete
monads*. Nor do they establish an ancestor simultaneously producing dyads and
triletes: that would require a biological/joint-state interpretation these
independent marginal outputs do not supply. An extant-only or alternative-tree
result must not silently replace this scenario.

The archive's original licence and source identity remain applicable; extraction
does not confer new rights. See `docs/audits/2026-10-29-pilot-and-contract-review.md`
for the scientific review and amendments proposed to Claude.
