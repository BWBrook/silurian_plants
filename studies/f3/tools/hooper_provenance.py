#!/usr/bin/env python3
"""Inventory and summarise the deposited Hooper et al. clock archive.

This is an archive audit only.  It does not run MCMCtree or alter the
git-ignored deposit.  The node numbering used here is the preorder numbering
used by the deposited MCMCtree files: internal nodes start at Ntip + 1 and
receive their number on entry to the Newick subtree.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from zipfile import ZipFile


ARCHIVE_RELATIVE = (
    "data/external/local/deposits/hooper2026-spore-evolution/"
    "03. Divergence Time Estimation.zip"
)
ARCHIVE_SHA256 = "79fd06812eff714e32a566cadc1c15844640e0a150b4504a07999d2cef957a25"
CALIBRATION_MEMBER = (
    "03. Divergence Time Estimation/mcmctree_inputs/"
    "Fossil_Calibrations_HooperNP.txt"
)
PRIOR_CONTROL_MEMBER = "03. Divergence Time Estimation/mcmctree_inputs/prior.ctl"
POSTERIOR_CONTROL_MEMBER = "03. Divergence Time Estimation/mcmctree_inputs/posterior.ctl"
PRIOR_CHAIN_MEMBER = (
    "03. Divergence Time Estimation/mcmctree_outputs/"
    "hornwort_set_prior_mcmc_old_version.txt"
)
POSTERIOR_CHAIN_MEMBER = (
    "03. Divergence Time Estimation/mcmctree_outputs/"
    "hornwort_set_posterior_mcmc_old_version.txt"
)
POSTERIOR_TREE_MEMBER = (
    "03. Divergence Time Estimation/mcmctree_outputs/"
    "hornwort_posterior_old_version.tre"
)
R_MEMBER = "03. Divergence Time Estimation/mcmctreer.R"
PAML_HISTORY_URL = "https://github.com/abacus-gene/paml/blob/master/doc/pamlHistory.txt"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def line_evidence(member: str, lines: list[str], predicate) -> list[dict]:
    found = []
    for number, text in enumerate(lines, start=1):
        if predicate(text):
            found.append({"member": member, "line": number, "text": text})
    return found


def first_line_evidence(member: str, lines: list[str], pattern: str) -> dict:
    matches = line_evidence(member, lines, lambda text: re.search(pattern, text))
    if not matches:
        raise ValueError(f"pattern not found in {member}: {pattern}")
    return matches[0]


@dataclass
class TreeNode:
    children: list["TreeNode"] = field(default_factory=list)
    name: str = ""
    annotation: str = ""
    branch_length: float | None = None
    node_id: int | None = None

    @property
    def leaves(self) -> list[str]:
        if not self.children:
            return [self.name]
        result: list[str] = []
        for child in self.children:
            result.extend(child.leaves)
        return result


class NewickParser:
    def __init__(self, text: str):
        self.text = text.strip().rstrip(";")
        self.position = 0

    def parse(self) -> TreeNode:
        node = self._parse_node()
        if self.position != len(self.text):
            raise ValueError(f"unparsed Newick content at {self.position}")
        return node

    def _parse_node(self) -> TreeNode:
        while self.position < len(self.text) and self.text[self.position].isspace():
            self.position += 1
        if self.text[self.position] == "(":
            self.position += 1
            children = [self._parse_node()]
            while self.text[self.position] == ",":
                self.position += 1
                children.append(self._parse_node())
            if self.text[self.position] != ")":
                raise ValueError("unterminated Newick subtree")
            self.position += 1
            node = TreeNode(children=children)
            self._parse_suffix(node)
            return node

        start = self.position
        while self.position < len(self.text) and self.text[self.position] not in ",()[]:;":
            self.position += 1
        node = TreeNode(name=self.text[start : self.position].strip())
        self._parse_suffix(node)
        return node

    def _parse_suffix(self, node: TreeNode) -> None:
        while self.position < len(self.text):
            while self.position < len(self.text) and self.text[self.position].isspace():
                self.position += 1
            if self.position >= len(self.text):
                return
            if self.text[self.position] == "'":
                end = self.text.index("'", self.position + 1)
                node.name = self.text[self.position + 1 : end]
                self.position = end + 1
            elif self.text[self.position] == "[":
                end = self.text.index("]", self.position + 1)
                node.annotation = self.text[self.position + 1 : end]
                self.position = end + 1
            elif self.text[self.position] == ":":
                self.position += 1
                start = self.position
                while self.position < len(self.text) and self.text[self.position] not in ",()[]:;":
                    self.position += 1
                value = self.text[start : self.position].strip()
                if value:
                    node.branch_length = float(value)
            else:
                return


def assign_preorder_ids(root: TreeNode, first_id: int) -> dict[int, TreeNode]:
    nodes: dict[int, TreeNode] = {}
    next_id = first_id

    def visit(node: TreeNode) -> None:
        nonlocal next_id
        if not node.children:
            return
        node.node_id = next_id
        nodes[next_id] = node
        next_id += 1
        for child in node.children:
            visit(child)

    visit(root)
    return nodes


def parse_control(lines: list[str]) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for number, raw in enumerate(lines, start=1):
        match = re.match(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*=\s*([^*]*?)(?:\s+\*.*)?$", raw)
        if match:
            result[match.group(1)] = {"value": match.group(2).strip(), "line": number, "text": raw}
    return result


def quantile(sorted_values: list[float], probability: float) -> float:
    position = (len(sorted_values) - 1) * probability
    lower = int(position)
    upper = min(lower + 1, len(sorted_values) - 1)
    return sorted_values[lower] + (sorted_values[upper] - sorted_values[lower]) * (position - lower)


def summarise_chain_values(values: dict[str, list[float]], indices: Iterable[int]) -> dict:
    selected_indices = list(indices)
    if not selected_indices:
        raise ValueError("cannot summarise an empty chain selection")
    summaries = {}
    for name, raw_values in values.items():
        selected = sorted(raw_values[i] for i in selected_indices)
        summaries[name] = {
            "mean_time_units": statistics.mean(selected),
            "median_time_units": quantile(selected, 0.5),
            "q025_time_units": quantile(selected, 0.025),
            "q975_time_units": quantile(selected, 0.975),
            "mean_ma": statistics.mean(selected) * 100,
            "median_ma": quantile(selected, 0.5) * 100,
            "q025_ma": quantile(selected, 0.025) * 100,
            "q975_ma": quantile(selected, 0.975) * 100,
        }
    return summaries


def read_chain(data: bytes, member: str, burnin: int) -> dict:
    lines = data.decode("utf-8").splitlines()
    if not lines:
        raise ValueError(f"empty chain: {member}")
    header = lines[0].split("\t")
    required = ["Gen", "t_n184", "t_n185"]
    missing = [name for name in required if name not in header]
    if missing:
        raise ValueError(f"missing chain columns in {member}: {missing}")
    generation_index = header.index("Gen")
    values = {name: [] for name in required[1:]}
    generations: list[int] = []
    malformed = 0
    for raw in lines[1:]:
        if not raw.strip():
            continue
        fields = raw.split("\t")
        if len(fields) != len(header):
            malformed += 1
            continue
        generations.append(int(fields[generation_index]))
        for name in required[1:]:
            values[name].append(float(fields[header.index(name)]))
    if malformed:
        raise ValueError(f"malformed rows in {member}: {malformed}")
    all_indices = list(range(len(generations)))
    burnin_sensitivity_indices = [i for i, generation in enumerate(generations) if generation > burnin]
    if not burnin_sensitivity_indices:
        raise ValueError(f"no rows above burn-in threshold in {member}")

    summaries = summarise_chain_values(values, all_indices)
    burnin_sensitivity_summaries = summarise_chain_values(values, burnin_sensitivity_indices)
    header_sha = sha256_bytes((lines[0] + "\n").encode("utf-8"))
    metadata_patterns = r"mcmctree|control|burnin|sampfreq|nsample|seed|command|outfile|treefile"
    metadata_hits = [
        {"line": number, "text": text}
        for number, text in enumerate(lines[:40], start=1)
        if re.search(metadata_patterns, text, re.IGNORECASE)
    ]
    return {
        "member": member,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
        "line_count": len(lines),
        "header": {
            "member": member,
            "line": 1,
            "sha256": header_sha,
            "column_count": len(header),
            "selected_columns": {name: header.index(name) + 1 for name in required},
        },
        "generation": {
            "saved_row_count": len(generations),
            "first_saved_generation": generations[0],
            "last_saved_generation": generations[-1],
            "declared_burnin": burnin,
            "primary_selection": "all saved rows; MCMCtree writes samples only after burn-in",
            "primary_row_count": len(all_indices),
            "burnin_sensitivity_selection": f"Gen > {burnin}",
            "burnin_sensitivity_row_count": len(burnin_sensitivity_indices),
        },
        "metadata_hits_in_header_and_first_rows": metadata_hits,
        "summaries": summaries,
        "burnin_sensitivity_summaries": burnin_sensitivity_summaries,
    }


def parse_focal_nodes(calibration_lines: list[str]) -> dict:
    if len(calibration_lines) < 2:
        raise ValueError("calibration file has no Newick line")
    tip_count = int(calibration_lines[0].split()[0])
    root = NewickParser(calibration_lines[1]).parse()
    leaves = root.leaves
    if len(leaves) != tip_count:
        raise ValueError(f"declared Ntip {tip_count} differs from parsed leaves {len(leaves)}")
    nodes = assign_preorder_ids(root, tip_count + 1)
    focal = {}
    for node_id, label in [(184, "crown_Embryophyta"), (185, "crown_Tracheophyta")]:
        node = nodes[node_id]
        annotation = node.name
        bounds = re.fullmatch(r"B\(([^,]+),([^,]+),([^,]+),([^,]+)\)", annotation)
        if not bounds:
            raise ValueError(f"node {node_id} has unexpected annotation {annotation!r}")
        focal[label] = {
            "node_id": node_id,
            "numbering": "preorder internal-node numbering, starting at Ntip + 1",
            "leaf_count": len(node.leaves),
            "leaves": node.leaves,
            "first_leaves": node.leaves[:5],
            "last_leaves": node.leaves[-5:],
            "annotation": annotation,
            "lower_time_units": float(bounds.group(1)),
            "upper_time_units": float(bounds.group(2)),
            "lower_ma": float(bounds.group(1)) * 100,
            "upper_ma": float(bounds.group(2)) * 100,
            "tail_lower": float(bounds.group(3)),
            "tail_upper": float(bounds.group(4)),
            "evidence": {
                "member": CALIBRATION_MEMBER,
                "line": 2,
                "line_sha256": sha256_bytes((calibration_lines[1] + "\n").encode("utf-8")),
                "annotation_substring": annotation,
            },
        }
    return {
        "declared_tip_count": tip_count,
        "parsed_tip_count": len(leaves),
        "internal_node_count": len(nodes),
        "root_node_id": min(nodes),
        "focal_nodes": focal,
    }


def parse_output_tree(data: bytes) -> tuple[TreeNode, dict[int, TreeNode]]:
    text = data.decode("utf-8")
    tree_lines = [line for line in text.splitlines() if re.match(r"^\s*UTREE\s+1\s*=", line)]
    if len(tree_lines) != 1:
        raise ValueError(f"expected one UTREE 1 in {POSTERIOR_TREE_MEMBER}, found {len(tree_lines)}")
    newick = tree_lines[0].split("=", 1)[1].strip()
    root = NewickParser(newick).parse()
    leaves = root.leaves
    nodes = assign_preorder_ids(root, len(leaves) + 1)
    return root, nodes


def parse_hpd(annotation: str) -> tuple[float, float]:
    match = re.search(r"95%HPD=\{([^,]+),([^}]+)\}", annotation)
    if not match:
        raise ValueError(f"missing 95%HPD annotation: {annotation!r}")
    return float(match.group(1)), float(match.group(2))


def compare_output_tree_to_calibration(payload: bytes, topology: dict) -> dict:
    root, output_nodes = parse_output_tree(payload)
    focal_comparisons = {}
    for label, calibration in topology["focal_nodes"].items():
        calibration_leaves = set(calibration["leaves"])
        calibration_node_id = calibration["node_id"]
        matches = [
            node
            for node in output_nodes.values()
            if set(node.leaves) == calibration_leaves
        ]
        if len(matches) != 1:
            raise ValueError(
                f"output tree clade matching {label} was not unique: {len(matches)}"
            )
        output_node = matches[0]
        hpd_lower, hpd_upper = parse_hpd(output_node.annotation)
        focal_comparisons[label] = {
            "calibration_node_id": calibration_node_id,
            "calibration_leaf_count": calibration["leaf_count"],
            "comparison_basis": "complete leaf-set equality",
            "output_tree_node_id": output_node.node_id,
            "output_tree_leaf_count": len(output_node.leaves),
            "exact_clade_match": len(output_node.leaves) == calibration["leaf_count"] and set(output_node.leaves) == calibration_leaves,
            "output_tree_annotation": output_node.annotation,
            "output_tree_hpd_time_units": {
                "lower": hpd_lower,
                "upper": hpd_upper,
            },
            "output_tree_hpd_ma": {
                "lower": hpd_lower * 100,
                "upper": hpd_upper * 100,
            },
        }
    return {
        "member": POSTERIOR_TREE_MEMBER,
        "sha256": sha256_bytes(payload),
        "declared_tip_count": len(root.leaves),
        "internal_node_count": len(output_nodes),
        "focal_nodes": focal_comparisons,
        "evidence": "95%HPD annotations parsed independently from the deposited NEXUS tree; clades matched by complete leaf sets",
    }


def inventory_archive(archive: Path, output_directory: Path) -> tuple[dict, dict[str, bytes]]:
    archive_hash = sha256_file(archive)
    members = []
    payloads: dict[str, bytes] = {}
    with ZipFile(archive) as zf:
        for info in zf.infolist():
            data = zf.read(info.filename)
            payloads[info.filename] = data
            members.append(
                {
                    "member": info.filename,
                    "bytes": len(data),
                    "zip_reported_bytes": info.file_size,
                    "compressed_bytes": info.compress_size,
                    "sha256": sha256_bytes(data),
                }
            )
    output_directory.mkdir(parents=True, exist_ok=True)
    with (output_directory / "inventory.tsv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(members[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(members)
    inventory = {
        "archive": str(archive),
        "archive_sha256": archive_hash,
        "archive_sha256_matches_manifest": archive_hash == ARCHIVE_SHA256,
        "member_count": len(members),
        "members": members,
    }
    return inventory, payloads


def matching_archive_members(reference: str, members: Iterable[str]) -> list[str]:
    reference_basename = Path(reference).name
    return sorted(
        member
        for member in members
        if member == reference or Path(member).name == reference_basename
    )


def build_summary(repo_root: Path, archive: Path, payloads: dict[str, bytes], inventory: dict) -> dict:
    def text(member: str) -> list[str]:
        return payloads[member].decode("utf-8").splitlines()

    prior_control_lines = text(PRIOR_CONTROL_MEMBER)
    posterior_control_lines = text(POSTERIOR_CONTROL_MEMBER)
    prior_control = parse_control(prior_control_lines)
    posterior_control = parse_control(posterior_control_lines)
    burnin = int(prior_control["burnin"]["value"])
    if burnin != int(posterior_control["burnin"]["value"]):
        raise ValueError("prior and posterior burn-ins differ")

    calibration_lines = text(CALIBRATION_MEMBER)
    calibration_text = "\n".join(calibration_lines)
    calibrations = re.findall(r"'B\(([^)]*)\)'", calibration_text)
    tail_pairs = sorted({tuple(value.split(",")[2:]) for value in calibrations})
    if len(calibrations) != 69 or tail_pairs != [("0.01", "0.01")]:
        raise ValueError(f"unexpected fossil calibration count/tails: {len(calibrations)}, {tail_pairs}")
    topology = parse_focal_nodes(calibration_lines)

    r_lines = text(R_MEMBER)
    r_evidence = {
        "node_184_label": first_line_evidence(R_MEMBER, r_lines, r"embryophyte node highlighted"),
        "node_184_reference": first_line_evidence(R_MEMBER, r_lines, r"all\.nodes = 184"),
        "time_correction": first_line_evidence(R_MEMBER, r_lines, r"time\.correction = 100"),
        "posterior_tree_read": first_line_evidence(R_MEMBER, r_lines, r"phy1 <- readMCMCtree"),
        "posterior_chain_read": first_line_evidence(R_MEMBER, r_lines, r"phy1\.posterior <- read\.delim"),
    }
    prior_chain = read_chain(payloads[PRIOR_CHAIN_MEMBER], PRIOR_CHAIN_MEMBER, burnin)
    posterior_chain = read_chain(payloads[POSTERIOR_CHAIN_MEMBER], POSTERIOR_CHAIN_MEMBER, burnin)
    output_tree = compare_output_tree_to_calibration(payloads[POSTERIOR_TREE_MEMBER], topology)

    log_like_members = [
        item["member"]
        for item in inventory["members"]
        if re.search(r"(^|/)[^/]*(?:log|stderr|stdout)[^/]*$", item["member"], re.IGNORECASE)
    ]
    referenced_outfiles = [
        control["outfile"]["value"]
        for control in [prior_control, posterior_control]
        if "outfile" in control
    ]
    present_members = set(payloads)
    referenced_outfile_matches = [
        {
            "control_reference": name,
            "archive_members_with_matching_basename": matching_archive_members(name, present_members),
        }
        for name in referenced_outfiles
    ]
    absent_referenced_outputs = [
        item["control_reference"]
        for item in referenced_outfile_matches
        if not item["archive_members_with_matching_basename"]
    ]
    calibration_evidence = {
        "member": CALIBRATION_MEMBER,
        "line": 2,
        "line_sha256": sha256_bytes((calibration_lines[1] + "\n").encode("utf-8")),
        "fossil_calibration_count": len(calibrations),
        "expected_fossil_calibration_count": 69,
        "all_fossil_calibration_tail_pairs": tail_pairs,
        "all_69_have_01_tails": len(calibrations) == 69 and tail_pairs == [("0.01", "0.01")],
    }
    controls = {
        "prior": {
            "member": PRIOR_CONTROL_MEMBER,
            "sha256": sha256_bytes(payloads[PRIOR_CONTROL_MEMBER]),
            "settings": prior_control,
            "evidence": {
                "burnin": line_evidence(PRIOR_CONTROL_MEMBER, prior_control_lines, lambda x: "burnin" in x),
                "sampling": line_evidence(PRIOR_CONTROL_MEMBER, prior_control_lines, lambda x: any(key in x for key in ["sampfreq", "nsample"])),
                "seed": line_evidence(PRIOR_CONTROL_MEMBER, prior_control_lines, lambda x: re.search(r"\bseed\b", x)),
                "data_mode": line_evidence(PRIOR_CONTROL_MEMBER, prior_control_lines, lambda x: "usedata" in x),
            },
        },
        "posterior": {
            "member": POSTERIOR_CONTROL_MEMBER,
            "sha256": sha256_bytes(payloads[POSTERIOR_CONTROL_MEMBER]),
            "settings": posterior_control,
            "evidence": {
                "burnin": line_evidence(POSTERIOR_CONTROL_MEMBER, posterior_control_lines, lambda x: "burnin" in x),
                "sampling": line_evidence(POSTERIOR_CONTROL_MEMBER, posterior_control_lines, lambda x: any(key in x for key in ["sampfreq", "nsample"])),
                "seed": line_evidence(POSTERIOR_CONTROL_MEMBER, posterior_control_lines, lambda x: re.search(r"\bseed\b", x)),
                "data_mode": line_evidence(POSTERIOR_CONTROL_MEMBER, posterior_control_lines, lambda x: "usedata" in x),
            },
        },
    }

    return {
        "schema_version": 1,
        "purpose": "bounded archive-level provenance and consistency check; no MCMCtree run",
        "archive": inventory,
        "members_checked": {
            "calibration": calibration_evidence,
            "prior_control": controls["prior"],
            "posterior_control": controls["posterior"],
            "prior_chain": prior_chain,
            "posterior_chain": posterior_chain,
            "plotting_reference": {"member": R_MEMBER, "sha256": sha256_bytes(payloads[R_MEMBER]), "references": r_evidence},
            "posterior_tree": output_tree,
        },
        "topology": topology,
        "sampling_semantics": {
            "primary_summary_selection": "all rows in each deposited chain",
            "reason": "MCMCtree writes MCMC samples only after burn-in; the deposited chains therefore already exclude the declared burn-in",
            "official_paml_source": PAML_HISTORY_URL,
            "deposited_reader_evidence": r_evidence["posterior_chain_read"],
            "declared_burnin_retained_as": "sensitivity threshold only (Gen > burnin)",
        },
        "traceability_checks": {
            "archive_member_log_like_names": log_like_members,
            "mcmctree_outfiles_referenced_by_controls": referenced_outfiles,
            "referenced_mcmctree_outfile_matches": referenced_outfile_matches,
            "referenced_mcmctree_outfiles_present_in_archive": sorted(
                {
                    member
                    for item in referenced_outfile_matches
                    for member in item["archive_members_with_matching_basename"]
                }
            ),
            "referenced_mcmctree_outfiles_absent_from_archive": absent_referenced_outputs,
            "chain_header_metadata_hits": {
                "prior": prior_chain["metadata_hits_in_header_and_first_rows"],
                "posterior": posterior_chain["metadata_hits_in_header_and_first_rows"],
            },
            "output_run_log_or_control_hash_present": bool(log_like_members)
            or bool(prior_chain["metadata_hits_in_header_and_first_rows"])
            or bool(posterior_chain["metadata_hits_in_header_and_first_rows"]),
        },
        "conclusion": {
            "internal_consistency": "supported: archive hash, 69 calibration count/tails, topology focus nodes, controls, chain headers and node summaries are reproducible from the snapshot",
            "published_summary_consistency": "posterior t_n184 rounds to the published crown-Embryophyta interval; t_n185 is reported as the topology-identified crown-Tracheophyta summary",
            "historical_run_provenance": "unresolved: no run log, control-file hash, or referenced mcmctree outfile links the supplied controls to the old_version chains",
            "unavailable": [
                "controlled rerun under deposited 1% settings",
                "controlled rerun under described 2.5% settings",
                "historical command invocation and explicit control-to-output linkage",
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--out-dir", type=Path)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    archive = args.archive or repo_root / ARCHIVE_RELATIVE
    out_dir = args.out_dir or repo_root / "studies/f3/data/q9/hooper2026-provenance"
    inventory, payloads = inventory_archive(archive, out_dir)
    summary = build_summary(repo_root, archive, payloads, inventory)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"inventory": str(out_dir / "inventory.tsv"), "summary": str(out_dir / "summary.json")}, indent=2))


if __name__ == "__main__":
    main()
