# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Unqualified Murzuq contamination and identification sensitivity.

The frozen LY-MZ-CU binary design supplies reference detections and 28 older
non-detections.  This diagnostic asks how much of the reference signal may be
indigenous when reference contamination can also generate reports in the
older cuttings.  It is deliberately separate from the qualified Loop 1 model:
``-2 log(0.05)`` is only a likelihood-comparison convention here.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import itertools
import json
import math
import os
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
F3 = HERE.parent
ROOT = F3.parents[1]
if str(F3) not in sys.path:
    sys.path.insert(0, str(F3))

import designs
import envelope as ev

CONFIG = HERE / "robustness_design.json"
OUT = HERE / "out"
RATE_BOUNDS = (1e-5, 8.0)
TOL = 1e-10


@dataclass(frozen=True)
class Well:
    name: str
    reference_detected: int
    reference_total: int
    older_ids: tuple[str, ...]
    older_depths: tuple[float, ...]
    older_lo: tuple[float, ...]
    older_hi: tuple[float, ...]


@dataclass(frozen=True)
class Frame:
    allocation: str
    tau: float
    wells: tuple[Well, ...]
    nodes: int
    cluster_k: float

    @property
    def n_reference(self) -> int:
        return sum(w.reference_total for w in self.wells)

    @property
    def d_reference(self) -> int:
        return sum(w.reference_detected for w in self.wells)

    @property
    def n_older(self) -> int:
        return sum(len(w.older_ids) for w in self.wells)


@dataclass(frozen=True)
class Profile:
    r: float
    log_likelihood: float
    status: str
    boundary: str
    scan_index: int
    evaluations: int

    @property
    def valid(self) -> bool:
        return self.status in {"ok", "boundary-lower", "boundary-upper"}


def _config() -> dict:
    with CONFIG.open() as f:
        return json.load(f)


def _ly_mz_design(decl: dict) -> dict:
    return next(d for d in decl["design"] if d["id"] == "LY-MZ-CU")


def _guard_frozen_design() -> None:
    expected = (F3 / "designs" / "m2.toml").resolve()
    active = Path(designs.DESIGNS).resolve()
    if active != expected:
        raise RuntimeError(f"F3_DESIGNS must resolve to the frozen declaration {expected}; got {active}")


def build_frame(allocation: str) -> Frame:
    """Build the frozen primary LY-MZ-CU frame, forcing no new source reading."""
    _guard_frozen_design()
    cfg = _config()
    if allocation not in cfg["allocations"]:
        raise ValueError(f"allocation must be one of {cfg['allocations']}")
    decl = designs.declarations()
    built = designs.build(
        _ly_mz_design(decl),
        {"material_type": "chart-code", "allocation": allocation, "cluster_k": cfg["cluster_k"]},
    )
    units, _ = built.units(rho=1.0)
    age = ev.AgeModel.load()
    spec = designs.spec(decl, cfg["cluster_k"], decl["common"]["min_ref_units"][0])
    problem = ev.Problem(units, spec, age)

    first = problem.s_star - spec.reference_stages + 1
    is_reference = np.array([(r.old <= problem.s_star) and (r.young >= first) for r in built.rows])
    is_older = np.array([r.old > problem.s_star for r in built.rows])
    if any(r.d for r, old in zip(built.rows, is_older) if old):
        raise ValueError("the declared contamination diagnostic requires all older outcomes to be zero")

    wells = []
    for name in sorted({r.cluster_name for r in built.rows}):
        ref = [r for r, keep in zip(built.rows, is_reference) if keep and r.cluster_name == name]
        old = [r for r, keep in zip(built.rows, is_older) if keep and r.cluster_name == name]
        old.sort(key=lambda r: r.depth)
        lo, hi = [], []
        for r in old:
            lo.append(float(age.base[r.young - 1] if math.isnan(r.lo_ma) else r.lo_ma))
            hi.append(float(age.base[r.old] if math.isnan(r.hi_ma) else r.hi_ma))
        wells.append(
            Well(
                name,
                sum(r.d for r in ref),
                len(ref),
                tuple(r.unit_id for r in old),
                tuple(r.depth for r in old),
                tuple(lo),
                tuple(hi),
            )
        )
    frame = Frame(allocation, problem.tau, tuple(wells), cfg["quadrature_nodes"], cfg["cluster_k"])
    if (frame.n_reference, frame.d_reference, frame.n_older) != (problem.n_ref, int(problem.rd.sum()), problem.n_old):
        raise RuntimeError("frame reconstruction disagrees with the frozen envelope problem")
    return frame


def envelope_problem(allocation: str, rho: float) -> ev.Problem:
    """Frozen envelope problem used only for exact baseline cross-checks."""
    _guard_frozen_design()
    cfg, decl = _config(), designs.declarations()
    built = designs.build(
        _ly_mz_design(decl),
        {"material_type": "chart-code", "allocation": allocation, "cluster_k": cfg["cluster_k"]},
    )
    units, _ = built.units(rho=rho)
    return ev.Problem(
        units,
        designs.spec(decl, cfg["cluster_k"], decl["common"]["min_ref_units"][0]),
        ev.AgeModel.load(),
    )


def target_weights(frame: Frame, chronology: str, start: float | str, end: float) -> tuple[np.ndarray, ...]:
    """Per-unit exposure probabilities or deterministic shared-age indicators."""
    cfg = _config()
    if chronology not in cfg["chronologies"]:
        raise ValueError(f"chronology must be one of {cfg['chronologies']}")
    start_value = frame.tau if start == "tau" else float(start)
    if not (math.isfinite(start_value) and math.isfinite(end) and end >= start_value):
        raise ValueError("target ages must be finite with end >= start")
    out = []
    for well in frame.wells:
        lo, hi = np.asarray(well.older_lo), np.asarray(well.older_hi)
        if chronology == "independent-uniform":
            q = np.clip((np.minimum(hi, end) - np.maximum(lo, start_value)) / (hi - lo), 0.0, 1.0)
        else:
            pos = float(chronology.rsplit("-", 1)[1])
            ages = lo + pos * (hi - lo)
            if len(ages) > 1 and np.any(np.diff(ages) < -TOL):
                raise ValueError(f"shared chronology violates age-depth order in {well.name}")
            q = ((ages > start_value - TOL) & (ages <= end + TOL)).astype(float)
        out.append(q)
    return tuple(out)


def _validate_q(frame: Frame, q: Sequence[Sequence[float]]) -> tuple[np.ndarray, ...]:
    if len(q) != len(frame.wells):
        raise ValueError("q must have one vector per well")
    arrays = tuple(np.asarray(x, dtype=float) for x in q)
    for well, values in zip(frame.wells, arrays):
        if values.ndim != 1 or len(values) != len(well.older_ids):
            raise ValueError(f"q length mismatch for {well.name}")
        if np.any(~np.isfinite(values)) or np.any((values < 0) | (values > 1)):
            raise ValueError("q values must be finite probabilities")
    return arrays


def _parameters(r: float, a: float, b: float) -> tuple[float, float, float]:
    vals = tuple(float(x) for x in (r, a, b))
    if not all(math.isfinite(x) for x in vals):
        raise ValueError("r, a and b must be finite")
    if vals[0] < RATE_BOUNDS[0] * (1.0 - 1e-12) or vals[0] > RATE_BOUNDS[1] * (1.0 + 1e-12):
        raise ValueError(f"r must lie in {RATE_BOUNDS}")
    if vals[1] < 0 or vals[2] < 0:
        raise ValueError("a and b must be non-negative")
    return min(max(vals[0], RATE_BOUNDS[0]), RATE_BOUNDS[1]), vals[1], vals[2]


def _older_log_probability(ru: np.ndarray, a: float, b: float, q: np.ndarray) -> np.ndarray:
    total = np.full_like(ru, -ru * b * len(q), dtype=float)
    for qi in q:
        if qi <= 0:
            continue
        if qi >= 1:
            total -= ru * a
        else:
            total += np.logaddexp(math.log1p(-qi), math.log(qi) - ru * a)
    return total


def loglik(
    r: float,
    a: float,
    b: float,
    q: Sequence[Sequence[float]],
    frame: Frame | None = None,
    *,
    reference_only: bool = False,
) -> float:
    """Joint marginal log likelihood at common rate ``r``.

    ``a = rho*g*f`` and ``b = kappa*(1-g)``.  Each well has one
    Gamma(k,k) frailty shared by all of its reference and older units.
    """
    frame = build_frame("stage") if frame is None else frame
    r, a, b = _parameters(r, a, b)
    q_arrays = _validate_q(frame, q)
    u, logw = ev.gamma_nodes(frame.cluster_k, frame.nodes)
    total = 0.0
    for well, qi in zip(frame.wells, q_arrays):
        ru = r * u
        lr = well.reference_detected * np.log(np.maximum(-np.expm1(-ru), np.finfo(float).tiny))
        lr -= (well.reference_total - well.reference_detected) * ru
        if not reference_only:
            lr += _older_log_probability(ru, a, b, qi)
        total += float(ev._lse(lr + logw))
    return total


def _profile(
    a: float,
    b: float,
    q: Sequence[Sequence[float]],
    frame: Frame,
    *,
    reference_only: bool,
) -> Profile:
    _parameters(1.0, a, b)
    q_arrays = _validate_q(frame, q)
    n_grid = int(_config()["log_rate_grid"])
    grid = np.linspace(math.log(RATE_BOUNDS[0]), math.log(RATE_BOUNDS[1]), n_grid)
    evaluations = 0

    def objective(z: float) -> float:
        nonlocal evaluations
        evaluations += 1
        return -loglik(math.exp(float(z)), a, b, q_arrays, frame, reference_only=reference_only)

    values = np.array([-objective(z) for z in grid])
    best = int(np.argmax(values))
    if best == 0:
        return Profile(RATE_BOUNDS[0], float(values[0]), "boundary-lower", "lower", best, evaluations)
    if best == n_grid - 1:
        return Profile(RATE_BOUNDS[1], float(values[-1]), "boundary-upper", "upper", best, evaluations)
    result = optimize.minimize_scalar(objective, bounds=(grid[best - 1], grid[best + 1]), method="bounded",
                                      options={"xatol": 1e-11, "maxiter": 300})
    if not result.success or not math.isfinite(result.fun):
        return Profile(math.exp(grid[best]), float(values[best]), "optimiser-failed", "none", best, evaluations)
    z = float(result.x)
    boundary = "none"
    status = "ok"
    if z <= math.log(RATE_BOUNDS[0]) + 1e-8:
        boundary, status = "lower", "boundary-lower"
    elif z >= math.log(RATE_BOUNDS[1]) - 1e-8:
        boundary, status = "upper", "boundary-upper"
    return Profile(math.exp(z), float(-result.fun), status, boundary, best, evaluations)


def profile(a: float, b: float, q: Sequence[Sequence[float]], frame: Frame | None = None) -> Profile:
    """Profile the joint likelihood over the common rate on [1e-5, 8]."""
    frame = build_frame("stage") if frame is None else frame
    return _profile(a, b, q, frame, reference_only=False)


def profile_reference(frame: Frame, q: Sequence[Sequence[float]]) -> Profile:
    return _profile(0.0, 0.0, q, frame, reference_only=True)


def transformed_parameters(rho: float, g: float, kappa: float, f: float) -> tuple[float, float]:
    vals = tuple(float(x) for x in (rho, g, kappa, f))
    if not all(math.isfinite(x) for x in vals):
        raise ValueError("rho, g, kappa and f must be finite")
    if vals[0] <= 0 or not 0 < vals[1] <= 1 or vals[2] < 0 or not 0 <= vals[3] <= 1:
        raise ValueError("require rho>0, 0<g<=1, kappa>=0 and 0<=f<=1")
    return vals[0] * vals[1] * vals[3], vals[2] * (1.0 - vals[1])


def _comparison(
    frame: Frame,
    q: tuple[np.ndarray, ...],
    a: float,
    b: float,
    ref: Profile,
    f0: Profile,
    candidate: Profile,
    alpha: float,
) -> dict:
    crit = -2.0 * math.log(alpha)
    ll0_at_ref = loglik(ref.r, 0.0, b, q, frame)
    p_zero = math.exp(min(0.0, ll0_at_ref - ref.log_likelihood))
    baseline_deviance = max(0.0, 2.0 * (ref.log_likelihood - f0.log_likelihood))
    conflict_probability = p_zero < alpha
    conflict_deviance = baseline_deviance > crit
    conflict = conflict_probability or conflict_deviance
    lr = max(0.0, 2.0 * (f0.log_likelihood - candidate.log_likelihood))
    if not (ref.valid and f0.valid and candidate.valid):
        status = "profile-failure"
    elif conflict:
        status = "model-conflict"
    elif lr > crit:
        status = "rejected-by-comparison"
    else:
        status = "not-rejected-by-comparison"
    return {
        "critical_value": crit,
        "p_all_older_zero_at_reference_r_f0": p_zero,
        "baseline_deviance": baseline_deviance,
        "conflict_probability": conflict_probability,
        "conflict_deviance": conflict_deviance,
        "model_conflict": conflict,
        "candidate_lr_vs_f0": lr,
        "comparison_status": status,
    }


def _targets(cfg: dict) -> list[dict]:
    return [{**t, "start_value": t["start"], "end": float(t["end_ma"])} for t in cfg["targets"]]


def declared_rows() -> list[tuple]:
    cfg = _config()
    return list(itertools.product(
        cfg["rho"], cfg["indigenous_reference_fraction_g"], cfg["contaminant_transfer_kappa"],
        cfg["allocations"], cfg["chronologies"], [t["name"] for t in cfg["targets"]],
        cfg["relative_indigenous_intensity_f"],
    ))


def _group_key_rows() -> list[tuple[str, str, str]]:
    cfg = _config()
    return list(itertools.product(cfg["allocations"], cfg["chronologies"], [t["name"] for t in cfg["targets"]]))


def _break_even(
    frame: Frame,
    q: tuple[np.ndarray, ...],
    f0: Profile,
    alpha: float,
) -> dict:
    crit = -2.0 * math.log(alpha)
    cache: dict[float, Profile] = {0.0: f0}

    def lr_at(a: float) -> float:
        key = round(float(a), 13)
        if key not in cache:
            cache[key] = profile(key, 0.0, q, frame)
        return max(0.0, 2.0 * (f0.log_likelihood - cache[key].log_likelihood))

    check_a = np.linspace(0.0, 1.0, 41)
    check_lr = np.array([lr_at(x) for x in check_a])
    monotone = bool(np.all(np.diff(check_lr) >= -1e-7))
    if not monotone:
        return {"effective_a_critical": math.nan, "root_status": "non-monotone", "monotone": False,
                "lr_at_a0": check_lr[0], "lr_at_a1": check_lr[-1], "root_profiles_valid": False}
    if check_lr[-1] < crit - 1e-9:
        return {"effective_a_critical": math.nan, "root_status": "no-root-through-a1", "monotone": True,
                "lr_at_a0": check_lr[0], "lr_at_a1": check_lr[-1],
                "root_profiles_valid": all(p.valid for p in cache.values())}
    root = float(optimize.brentq(lambda x: lr_at(x) - crit, 0.0, 1.0, xtol=1e-9, rtol=1e-10))
    return {"effective_a_critical": root, "root_status": "finite", "monotone": True,
            "lr_at_a0": check_lr[0], "lr_at_a1": check_lr[-1],
            "root_profiles_valid": all(p.valid for p in cache.values())}


def _evaluate_group(key: tuple[str, str, str]) -> tuple[list[dict], list[dict]]:
    allocation, chronology, target_name = key
    cfg = _config()
    target = next(t for t in cfg["targets"] if t["name"] == target_name)
    frame = build_frame(allocation)
    q = target_weights(frame, chronology, target["start"], float(target["end_ma"]))
    ref = profile_reference(frame, q)
    alpha = float(cfg["alpha_comparison"])
    cache: dict[tuple[float, float], Profile] = {}

    def fit(a: float, b: float) -> Profile:
        key2 = (round(float(a), 13), round(float(b), 13))
        if key2 not in cache:
            cache[key2] = profile(*key2, q, frame)
        return cache[key2]

    rows = []
    for rho, g, kappa, f in itertools.product(
        cfg["rho"], cfg["indigenous_reference_fraction_g"], cfg["contaminant_transfer_kappa"],
        cfg["relative_indigenous_intensity_f"],
    ):
        a, b = transformed_parameters(rho, g, kappa, f)
        f0, candidate = fit(0.0, b), fit(a, b)
        result = {
            "allocation": allocation, "chronology": chronology, "target": target_name,
            "start_ma": frame.tau if target["start"] == "tau" else target["start"],
            "end_ma": target["end_ma"], "rho": rho, "g": g, "kappa": kappa, "f": f,
            "a_rho_g_f": a, "b_kappa_1_minus_g": b,
            "n_wells": len(frame.wells), "n_reference": frame.n_reference,
            "reference_detections": frame.d_reference, "n_older_zero": frame.n_older,
            "q_sum": sum(float(x.sum()) for x in q), "q_min": min(float(x.min()) for x in q if len(x)),
            "q_max": max(float(x.max()) for x in q if len(x)),
            "reference_r_mle": ref.r, "reference_log_likelihood": ref.log_likelihood,
            "reference_profile_status": ref.status,
            "f0_r_mle": f0.r, "f0_log_likelihood": f0.log_likelihood, "f0_profile_status": f0.status,
            "candidate_r_mle": candidate.r, "candidate_log_likelihood": candidate.log_likelihood,
            "candidate_profile_status": candidate.status,
        }
        result.update(_comparison(frame, q, a, b, ref, f0, candidate, alpha))
        rows.append(result)

    f0_zero = fit(0.0, 0.0)
    root = _break_even(frame, q, f0_zero, alpha)
    roots = []
    for rho, f in itertools.product(cfg["rho"], cfg["relative_indigenous_intensity_f"]):
        cap = rho * f
        acrit = root["effective_a_critical"]
        if root["root_status"] == "finite" and acrit <= cap + 1e-10:
            status, gcrit = "finite", min(1.0, acrit / cap)
        elif root["root_status"] == "finite":
            status, gcrit = "no-root-for-rho-f", math.nan
        else:
            status, gcrit = root["root_status"], math.nan
        roots.append({
            "allocation": allocation, "chronology": chronology, "target": target_name,
            "start_ma": frame.tau if target["start"] == "tau" else target["start"],
            "end_ma": target["end_ma"], "break_even_scope": "no-older-contamination",
            "kappa": 0.0, "b_kappa_1_minus_g": 0.0,
            "rho": rho, "f": f, "effective_a_at_g1": cap,
            "g_critical": gcrit, "status": status, **root,
            "critical_value": -2.0 * math.log(alpha),
        })
    return rows, roots


def _smoke_row(task: tuple) -> dict:
    rho, g, kappa, allocation, chronology, target_name, f = task
    cfg = _config()
    target = next(t for t in cfg["targets"] if t["name"] == target_name)
    frame = build_frame(allocation)
    q = target_weights(frame, chronology, target["start"], float(target["end_ma"]))
    ref = profile_reference(frame, q)
    a, b = transformed_parameters(rho, g, kappa, f)
    f0, candidate = profile(0.0, b, q, frame), profile(a, b, q, frame)
    return {
        "rho": rho, "g": g, "kappa": kappa, "allocation": allocation, "chronology": chronology,
        "target": target_name, "f": f, "candidate_lr_vs_f0": max(0.0, 2 * (f0.log_likelihood - candidate.log_likelihood)),
        "reference_profile_status": ref.status, "f0_profile_status": f0.status,
        "candidate_profile_status": candidate.status,
    }


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _input_paths() -> list[Path]:
    return [
        CONFIG, HERE / "contamination.py", HERE / "test_contamination.py",
        ROOT / "docs" / "audits" / "2026-11-01-loop2-count-gate.md",
        F3 / "designs.py", F3 / "envelope.py", F3 / "sim.py", F3 / "designs" / "m2.toml",
        ROOT / "data" / "timescale.csv", ROOT / "data" / "units" / "libya_appendix1.csv",
        ROOT / "data" / "units" / "libya_chart_reports.csv", ROOT / "data" / "units" / "libya_prose_support.csv",
    ]


def _input_hashes() -> dict[str, str]:
    _guard_frozen_design()
    return {str(p.relative_to(ROOT)): _sha256(p) for p in _input_paths()}


def _write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("cannot write an empty result table")
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _manifest(grid: Path, roots: Path, elapsed: float, workers: int, inputs: dict[str, str]) -> dict:
    return {
        "schema": "loop2-murzuq-contamination-v1",
        "status": "unqualified-identification-sensitivity-only",
        "comparison": "-2log(0.05) is a convention; no coverage or qualification claim",
        "break_even_scope": "kappa=0 and b=0 only; full factorial comparisons vary b=kappa*(1-g)",
        "inputs": inputs,
        "input_drift_check": "identical SHA-256 maps before and after numerical computation",
        "outputs": {str(grid.relative_to(ROOT)): _sha256(grid), str(roots.relative_to(ROOT)): _sha256(roots)},
        "rows": sum(1 for _ in grid.open()) - 1,
        "break_even_rows": sum(1 for _ in roots.open()) - 1,
        "elapsed_seconds": elapsed,
        "workers": workers,
        "runtime": {
            "python": sys.version.split()[0], "platform": platform.platform(),
            "numpy": importlib.metadata.version("numpy"), "scipy": importlib.metadata.version("scipy"),
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        },
    }


def run_full(workers: int) -> dict:
    if not 1 <= workers <= 4:
        raise ValueError("workers must be between one and four")
    before = _input_hashes()
    start = time.perf_counter()
    keys = _group_key_rows()
    if workers == 1:
        parts = [_evaluate_group(k) for k in keys]
    else:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            parts = list(pool.map(_evaluate_group, keys))
    rows = [row for part, _ in parts for row in part]
    roots = [row for _, part in parts for row in part]
    if len(rows) != 5760 or len(roots) != 384:
        raise RuntimeError(f"declared grid size changed: {len(rows)} rows and {len(roots)} roots")
    after = _input_hashes()
    if after != before:
        changed = sorted(set(before) | set(after), key=lambda p: (before.get(p) == after.get(p), p))
        changed = [p for p in changed if before.get(p) != after.get(p)]
        raise RuntimeError(f"bound inputs changed during computation: {changed}")
    OUT.mkdir(parents=True, exist_ok=True)
    grid_path, root_path = OUT / "contamination_grid.csv", OUT / "contamination_break_even.csv"
    _write_csv(grid_path, rows)
    _write_csv(root_path, roots)
    elapsed = time.perf_counter() - start
    manifest = _manifest(grid_path, root_path, elapsed, workers, before)
    (OUT / "contamination_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def run_smoke(n: int) -> dict:
    tasks = declared_rows()[:n]
    start = time.perf_counter()
    rows = [_smoke_row(t) for t in tasks]
    elapsed = time.perf_counter() - start
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "contamination_smoke.csv"
    _write_csv(path, rows)
    return {
        "rows": n, "elapsed_seconds": elapsed,
        "forecast_seconds_upper_bound": elapsed / n * len(declared_rows()),
        "output": str(path.relative_to(ROOT)),
        "all_profiles_valid": all(r["reference_profile_status"] in {"ok", "boundary-lower", "boundary-upper"}
                                  and r["f0_profile_status"] in {"ok", "boundary-lower", "boundary-upper"}
                                  and r["candidate_profile_status"] in {"ok", "boundary-lower", "boundary-upper"}
                                  for r in rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--smoke", type=int, metavar="ROWS")
    mode.add_argument("--full", action="store_true")
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    args = parser.parse_args()
    result = run_smoke(args.smoke) if args.smoke is not None else run_full(args.workers)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
