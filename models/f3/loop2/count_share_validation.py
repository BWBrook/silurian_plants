"""Deterministic validation and provenance receipt for ``count_share``.

The coverage check enumerates the exact Binomial distribution for a finite,
declared grid.  It is a mathematical check of the CP construction, not a
simulation certificate and not qualification of either fossil frame.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import math
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.stats import binom

from count_share import common_effort_bound, zero_target_stratified_bound


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
SOURCE_GATE = ROOT / "docs" / "audits" / "2026-11-01-loop2-count-gate.md"
NS = [1, 3, 10, 30, 100, 300, 1000]
PGRID = [0.0, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0]
ALPHA = 0.05
H = 1.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_coverage(n: int, p: float, alpha: float = ALPHA, h: float = H) -> float:
    covered = 0.0
    for target in range(n + 1):
        b = common_effort_bound(target, n - target, h, alpha)
        if b.share_upper + 1e-13 >= p:
            covered += float(binom.pmf(target, n, p))
    return covered


def run() -> tuple[dict, list[dict]]:
    rows = []
    for n in NS:
        for p in PGRID:
            coverage = exact_coverage(n, p)
            rows.append({"n": n, "true_share": p, "alpha": ALPHA, "effort_ratio": H,
                         "exact_coverage": coverage, "nominal": 1 - ALPHA,
                         "passes_numeric_check": coverage + 1e-12 >= 1 - ALPHA})
    # These are intentionally labelled stress diagnostics, not coverage claims.
    wrong_effort = common_effort_bound(0, 30, 1.0, ALPHA)
    clustered = common_effort_bound(0, 30, 1.0, ALPHA)
    diagnostics = {
        "wrong_effort_example": {
            "observed_target": 0, "observed_control": 30,
            "reported_effort_ratio": 1.0, "true_effort_ratio_not_used": 0.25,
            "reported_upper_biological_share": wrong_effort.biological_share_upper,
            "status": "stress-only; wrong effort ratio is misspecification, not covered",
        },
        "clustered_counts_example": {
            "observed_target": 0, "observed_control": 30,
            "independent_count_bound": clustered.biological_share_upper,
            "status": "stress-only; shared preparation/frailty violates independent-binomial construction",
        },
        "zero_stratified_examples": [
            zero_target_stratified_bound([10], [1.0], ALPHA),
            zero_target_stratified_bound([10, 20], [0.5, 2.0], ALPHA),
            zero_target_stratified_bound([10, 20], [0.0, 0.0], ALPHA),
        ],
    }
    summary = {
        "schema": "loop2-count-share-method-validation-v1",
        "status": "method-validation-only; not real-design qualification",
        "assumptions": [
            "independent Poisson strata or conditional binomial counts",
            "known target/control effective effort ratio",
            "shared relative intensity within the declared stratum",
            "producer interpretation additionally assumes the supplied effort ratio captures relative delivery/recovery",
        ],
        "parameters": {"alpha": ALPHA, "effort_ratio": H, "n": NS, "pgrid": PGRID},
        "rows": len(rows), "minimum_exact_coverage": min(r["exact_coverage"] for r in rows),
        "all_grid_rows_pass": all(r["passes_numeric_check"] for r in rows),
        "source_gate": str(SOURCE_GATE.relative_to(ROOT)),
        "source_gate_sha256": sha256(SOURCE_GATE),
        "diagnostics": diagnostics,
    }
    return summary, rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary, rows = run()
    csv_path = OUT / "count_share_validation.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    receipt = dict(summary)
    receipt["code_sha256"] = sha256(HERE / "count_share.py")
    receipt["validation_sha256"] = sha256(Path(__file__))
    receipt["csv_sha256"] = sha256(csv_path)
    receipt["runtime"] = {
        "python": sys.version.split()[0], "platform": platform.platform(),
        "numpy": importlib.metadata.version("numpy"), "scipy": importlib.metadata.version("scipy"),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (OUT / "count_share_validation.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: receipt[k] for k in ("status", "rows", "minimum_exact_coverage", "all_grid_rows_pass")}, sort_keys=True))


if __name__ == "__main__":
    main()
