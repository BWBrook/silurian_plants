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
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.special import betaln, gammaln
from scipy.stats import binom

from count_share import common_effort_bound, zero_target_stratified_bound


ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
SOURCE_GATE = ROOT / "studies" / "f3" / "docs" / "audits" / "2026-11-01-loop2-count-gate.md"
NS = [1, 3, 10, 30, 100, 300, 1000]
PGRID = [0.0, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0]
ALPHA = 0.05
H = 1.0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_sha256(payload: object) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def coverage_from_pmf(n: int, pmf: np.ndarray, threshold_share: float,
                      alpha: float = ALPHA, h: float = H,
                      threshold_theta: float | None = None) -> float:
    """Sum an exact count PMF over outcomes whose reported bound covers truth."""
    covered = 0.0
    for target in range(n + 1):
        b = common_effort_bound(target, n - target, h, alpha)
        upper = b.rate_ratio_upper if threshold_theta is not None else b.share_upper
        threshold = threshold_theta if threshold_theta is not None else threshold_share
        if upper + 1e-13 >= threshold:
            covered += float(pmf[target])
    return covered


def exact_coverage(n: int, p: float, alpha: float = ALPHA, h: float = H) -> float:
    return coverage_from_pmf(n, binom.pmf(np.arange(n + 1), n, p), p, alpha, h)


def beta_binomial_pmf(n: int, p: float, concentration: float) -> np.ndarray:
    """Exact beta-binomial PMF for deterministic clustered-count stress tests."""
    if not 0.0 < p < 1.0 or concentration <= 0.0:
        raise ValueError("beta-binomial stress parameters must be interior and positive")
    k = np.arange(n + 1, dtype=float)
    a = p * concentration
    b = (1.0 - p) * concentration
    log_pmf = (gammaln(n + 1.0) - gammaln(k + 1.0) - gammaln(n - k + 1.0)
               + betaln(k + a, n - k + b) - betaln(a, b))
    return np.exp(log_pmf)


def run() -> tuple[dict, list[dict]]:
    rows = []
    for n in NS:
        for p in PGRID:
            coverage = exact_coverage(n, p)
            rows.append({"n": n, "true_share": p, "alpha": ALPHA, "effort_ratio": H,
                         "exact_coverage": coverage, "nominal": 1 - ALPHA,
                         "passes_numeric_check": coverage + 1e-12 >= 1 - ALPHA})

    # Deterministic misspecification stresses.  These are not qualification:
    # each deliberately violates one assumption of the declared construction.
    wrong_h = 0.1
    true_theta = 1.0
    wrong_h_share = wrong_h * true_theta / (1.0 + wrong_h * true_theta)
    wrong_h_pmf = binom.pmf(np.arange(101), 100, wrong_h_share)
    wrong_h_coverage = coverage_from_pmf(
        100, wrong_h_pmf, wrong_h_share, ALPHA, h=1.0, threshold_theta=true_theta
    )

    clustered_p = 0.1
    clustered_pmf = beta_binomial_pmf(100, clustered_p, concentration=2.0)
    clustered_coverage = coverage_from_pmf(100, clustered_pmf, clustered_p,
                                           ALPHA, h=1.0)
    independent_comparator = exact_coverage(100, clustered_p, ALPHA, h=1.0)
    diagnostics = {
        "wrong_effort_ratio": {
            "n": 100,
            "true_effort_ratio": wrong_h,
            "assumed_effort_ratio": 1.0,
            "true_producer_odds": true_theta,
            "true_observed_share": wrong_h_share,
            "exact_reported_theta_upper_coverage": wrong_h_coverage,
            "nominal": 1 - ALPHA,
            "status": "misspecified-assumption-stress; no qualification",
            "interpretation": "Using h=1 when the true h is 0.1 undercovers producer odds 1.",
        },
        "clustered_counts": {
            "n": 100,
            "true_observed_share": clustered_p,
            "beta_binomial_concentration": 2.0,
            "exact_naive_independent_cp_coverage": clustered_coverage,
            "exact_independent_binomial_comparator": independent_comparator,
            "nominal": 1 - ALPHA,
            "status": "misspecified-assumption-stress; no qualification",
            "interpretation": "Beta-binomial clustering is outside independent-binomial coverage.",
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
            "independent Poisson strata; conditional on each stratum total, target counts are binomial",
            "a common rate ratio theta across strata and fixed, known target/control effort ratios h_i",
            "an unknown h_i whose allowed set reaches zero contributes no information; if all do, the supremum is vacuous",
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
    receipt["scientific_payload_sha256"] = payload_sha256({"summary": summary, "rows": rows})
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
