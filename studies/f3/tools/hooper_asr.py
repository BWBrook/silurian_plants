#!/usr/bin/env python3
"""Extract deposited crown-node states without re-estimating ancestral states."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import re
from pathlib import Path
from zipfile import ZipFile

from hooper_provenance import NewickParser, assign_preorder_ids, sha256_bytes


DEPOSIT = "data/external/local/deposits/hooper2026-spore-evolution"
PREFIX = "02. Ancestral State Estimation/"
TREES = {"ext": "extant.tre", "eo": "eophyte sister.tre", "zyg": "zygnema sister.tre"}
METHODS = {
    "PARS": ("pars", "parsimony_assignment"),
    "SCM": ("SCM", "stochastic_map_frequency"),
    "ER": ("ER", "marginal_state_support"),
    "ARD": ("ARD", "marginal_state_support"),
}
CHARACTERS = ("X21", "X26")
ALGAE = {"Chlorella", "Coleochaete", "Spirogyra"}


def csv_rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def read_tree(data):
    # Internal numeric support labels do not determine ape's node indices.
    text = re.sub(
        r"(?<=\))[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?(?=[:),;])",
        "", data.decode("utf-8").strip(),
    )
    tree = NewickParser(text).parse()
    nodes = assign_preorder_ids(tree, len(tree.leaves) + 1)
    return tree, nodes


def mrca(nodes, tips):
    candidates = [n for n in nodes.values() if tips <= set(n.leaves)]
    if not candidates:
        raise ValueError(f"MRCA not found for {sorted(tips)}")
    return min(candidates, key=lambda n: len(n.leaves))


def write_csv(path, rows):
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def extract(root, out):
    deposit = root / DEPOSIT
    with (root / "data/external/deposits/MANIFEST.tsv").open(encoding="utf-8", newline="") as handle:
        expected = {Path(r["path"]).name: r["sha256"]
                    for r in csv.DictReader(handle, delimiter="\t", quoting=csv.QUOTE_NONE)
                    if r["path"].startswith("deposits/hooper2026-spore-evolution/")}
    archives, inventory = {}, []
    for name in ("01. Data.zip", "02. Ancestral State Estimation.zip"):
        data = (deposit / name).read_bytes()
        digest = sha256_bytes(data)
        if digest != expected[name]:
            raise ValueError(f"Archive differs from retrieval manifest: {name}")
        archives[name] = ZipFile(io.BytesIO(data))
        inventory.append({"archive": name, "member": "", "sha256": digest})

    def read(archive, member):
        data = archives[archive].read(member)
        inventory.append({"archive": archive, "member": member, "sha256": sha256_bytes(data)})
        return data

    archive = "02. Ancestral State Estimation.zip"
    labels = csv_rows(read(archive, PREFIX + "labelsperchar.csv"))
    asr = {r["Genus"]: r for r in csv_rows(read(archive, PREFIX + "asr_matrix.csv"))}
    master = {r["Genus"]: r for r in csv_rows(read("01. Data.zip", "01. Data/matrix.csv"))}
    read(archive, PREFIX + "ASE code chunk.R")
    crosswalk = []
    for taxon, row in asr.items():
        for char in CHARACTERS:
            state, master_state = row[char[1:]], master[taxon]["C" + char[1:]]
            if state != master_state:
                raise ValueError(f"Master/ASR state mismatch: {taxon} {char}")
            crosswalk.append({"taxon": taxon, "asr_character": char,
                              "master_character": "C" + char[1:], "state": state})

    parsed = {scenario: read_tree(read(archive, PREFIX + member))
              for scenario, member in TREES.items()}
    ext, ext_nodes = parsed["ext"]
    crown_tips = set(ext.leaves) - ALGAE
    vascular_tips = set(mrca(ext_nodes, {"Cycas", "Lycopodium"}).leaves)
    targets = {"crown_Embryophyta": crown_tips, "crown_Tracheophyta": vascular_tips}
    node_rows, states = [], []
    for scenario, (tree, nodes) in parsed.items():
        if not crown_tips <= set(tree.leaves) or len(tree.leaves) != len(set(tree.leaves)):
            raise ValueError(f"Missing or duplicate tree tips: {scenario}")
        selected = {name: mrca(nodes, tips) for name, tips in targets.items()}
        for name, node in selected.items():
            node_rows.append({"scenario": scenario, "target": name,
                              "tree_member": PREFIX + TREES[scenario], "node_id": node.node_id,
                              "n_tips": len(tree.leaves),
                              "mrca_extant_tips": ";".join(sorted(targets[name])),
                              "descendant_tips": ";".join(sorted(node.leaves))})
        for char in CHARACTERS:
            defined = {r["state"]: r[char] for r in labels if r[char]}
            for method, (folder, kind) in METHODS.items():
                member = PREFIX + f"ase outputs/{folder}/{method}_{char}_{scenario}.csv"
                raw = read(archive, member)
                rows = csv_rows(raw)
                table = {r[""]: r for r in rows}
                if len(table) != len(rows):
                    raise ValueError(f"Duplicate row labels: {member}")
                expected_rows = {str(n) for n in nodes}
                if method == "PARS":
                    expected_rows |= {str(n) for n in range(1, len(tree.leaves) + 1)}
                elif method == "SCM":
                    expected_rows |= set(tree.leaves)
                if set(table) != expected_rows:
                    raise ValueError(f"Unexpected node/tip rows: {member}")
                present_states = set(rows[0]) - {""}
                if not present_states <= set(defined):
                    raise ValueError(f"Unlabelled state: {member}")
                for row in rows:
                    values = [float(row[s]) for s in present_states]
                    if any(not math.isfinite(v) or not 0 <= v <= 1 for v in values):
                        raise ValueError(f"Invalid state value: {member} {row['']}")
                    if not math.isclose(sum(values), 1, abs_tol=1e-8):
                        raise ValueError(f"State values do not sum to one: {member} {row['']}")
                if method in {"PARS", "SCM"}:
                    for tip_id, taxon in enumerate(tree.leaves, 1):
                        row_id = str(tip_id) if method == "PARS" else taxon
                        state = asr[taxon][char[1:]]
                        if float(table[row_id][state]) != 1:
                            raise ValueError(f"Tip does not match matrix: {member} {taxon}")
                for name, node in selected.items():
                    row = table[str(node.node_id)]
                    for state, label in defined.items():
                        states.append({"scenario": scenario, "target": name,
                                       "node_id": node.node_id, "character": char,
                                       "method": method, "value_kind": kind, "state": state,
                                       "state_label": label, "value": row.get(state, ""),
                                       "status": "reported" if state in row else "column_absent",
                                       "source_member": member, "source_sha256": sha256_bytes(raw)})

    duplicate = read(archive, PREFIX + "ase outputs/pars/PARS_X21_ext2.csv")
    canonical = archives[archive].read(PREFIX + "ase outputs/pars/PARS_X21_ext.csv")
    if duplicate != canonical:
        raise ValueError("The additional PARS_X21_ext2 output differs; adjudication required")
    out.mkdir(parents=True, exist_ok=True)
    write_csv(out / "crown_states.csv", states)
    write_csv(out / "nodes.csv", node_rows)
    write_csv(out / "matrix_crosswalk.csv", crosswalk)
    write_csv(out / "source_inventory.csv", inventory)
    receipt = {"operation": "extract published outputs; no ancestral-state inference",
               "node_numbering": "tips in Newick order; internal nodes in preorder from Ntip+1",
               "missing_state_policy": "empty value and column_absent; never imputed zero",
               "duplicate_PARS_X21_ext2": "byte-identical to PARS_X21_ext; not a separate analysis",
               "state_rows": len(states), "node_rows": len(node_rows),
               "matrix_comparisons": len(crosswalk),
               "script_sha256": sha256_bytes(Path(__file__).read_bytes()),
               "parser_sha256": sha256_bytes((root / "studies/f3/tools/hooper_provenance.py").read_bytes()),
               "outputs": {p.name: sha256_bytes(p.read_bytes()) for p in sorted(out.glob("*.csv"))}}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: receipt[k] for k in ("state_rows", "node_rows", "matrix_comparisons")}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--out", type=Path, default=Path("studies/f3/data/pilot/hooper2026-asr"))
    args = parser.parse_args()
    extract(args.root, args.out if args.out.is_absolute() else args.root / args.out)
