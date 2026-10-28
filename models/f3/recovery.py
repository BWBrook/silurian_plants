# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///
"""Loop 1, step 3 of docs/plan-f3.md: the recovery study.

    uv run models/f3/recovery.py

Simulates a clade of known origination T0 under growth, effort and preservation scenarios, estimates
T0 from the stage-binned records, and measures coverage, bias, interval width and identifiability.
Writes out/recovery_grid.csv and out/recovery_grid.meta.json.

Scenario = origination window x growth x effort x preservation level. In each replicate T0 is drawn
uniformly within the window and the abundance path is simulated once, and every effort and
preservation level is sampled from that path. Preservation is set by the expected number of records:
psi of each channel is the target count divided by the channel's effort-weighted abundance integral,
so a replicate with an older origination has a lower psi, and the realised count is Poisson about the
target. Real effort is out/effort_series.csv (inputs.py) scaled to mean 1; constant effort is 1.

Estimators, each on spores alone, bodies alone, and both channels (`joint`: pooled records for the
classical and GRIWM estimators, shared N(t) and T0 for the ramp fits):
  classical      Strauss and Sadler's bound (Marshall's single-endpoint interval; point = 50% bound),
                 records drawn uniformly within their stages
  griwm          mirrored GRIWM point estimate (alpha 0.05), stage-resampled
  ramp_logistic  ramp.fit with logistic growth, capacity fixed at 100
  ramp_logistic_kfree  the same with the capacity profiled over CAPACITIES
  ramp_bd        ramp.fit with the expected birth-death curve

Acceptance: docs/plan-f3.md fixes coverage of at least 0.90 and |median bias| under 2 Myr for an
interval estimator. How each estimator is judged was fixed here before the first grid run. Classical is judged on its
nominal one-sided bound (hi >= T0), the ramp fits on their two-sided profile interval. GRIWM is a
point estimator: |median bias| under 2 Myr and an interval calibrated by simulation, built from the
error quantiles of the same estimator in the constant-growth scenario with the same window, effort and
preservation, that covers at least 0.90. An unbounded profile counts as covering; `identified` records
whether at most 10% of fits are unbounded, and `usable` needs both.
"""

import csv
import hashlib
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import cache, partial
from pathlib import Path

import numpy as np
import scipy

import estimators as est
import inputs
import ramp
import sim

OUT = Path(__file__).resolve().parent / "out"
ROOT_SEED = 20261029
N_REPS = 1000
CHUNK = 100
N_DRAWS = 300
COVERAGE_MIN = 0.90
BIAS_MAX_MYR = 2.0
UNBOUNDED_MAX = 0.10
CALIBRATION_Q = (0.025, 0.975)
WINDOWS = {  # (oldest stage, youngest stage) of the window in which T0 is drawn
    "darriwilian-sandbian": ("Darriwilian", "Sandbian"),
    "katian-hirnantian": ("Katian", "Hirnantian"),
    "telychian-sheinwoodian": ("Telychian", "Sheinwoodian"),
}
GROWTH = {
    "constant": sim.Constant(k=50),
    "logistic_r0.15": sim.Logistic(r=0.15, k=100),
    "logistic_r0.3": sim.Logistic(r=0.3, k=100),
    "logistic_r0.6": sim.Logistic(r=0.6, k=100),
    "logistic_r0.3_k30": sim.Logistic(r=0.3, k=30),
    "logistic_r0.3_k300": sim.Logistic(r=0.3, k=300),
    "bd_g0.05": sim.BirthDeath(lam=0.20, mu=0.15),
    "bd_g0.10": sim.BirthDeath(lam=0.25, mu=0.15),
}
EFFORTS = ("real", "constant")
LEVELS = {"low": (30, 10), "mid": (100, 30), "high": (300, 100), "very_high": (1000, 300)}  # expected records: spores, bodies
CHANNEL_SETS = {"spores": (0,), "bodies": (1,), "joint": (0, 1)}
ESTIMATORS = ("classical", "griwm", "ramp_logistic", "ramp_logistic_kfree", "ramp_bd")
CAPACITIES = (10.0, 30.0, 100.0, 300.0, 1000.0)  # ramp_logistic_kfree profiles over these; ramp_logistic fixes 100
COLUMNS = [
    "window", "growth", "effort", "level", "target_spores", "target_bodies", "median_n_spores", "median_n_bodies",
    "channels", "estimator", "n_reps", "frac_undefined", "coverage_interval", "coverage_upper", "coverage_calibrated",
    "median_bias_ma", "median_width_ma", "median_upper_excess_ma", "frac_unbounded", "calibrated_width_ma", "passes", "identified", "usable",
]


@dataclass(frozen=True)
class Context:
    timescale: sim.Timescale
    first: int
    last: int
    window_end: float
    effort: dict[str, np.ndarray]
    stages: tuple[str, ...]
    models: dict[str, ramp.RampModel | list[ramp.RampModel]]


@cache
def context() -> Context:
    ts = sim.Timescale.load()
    series = inputs.effort_series(timescale=ts)
    real = np.array([series.spores, series.bodies])
    real = real / real.mean(axis=1, keepdims=True)
    return Context(
        ts, ts.index(inputs.YOUNGEST), ts.index(inputs.OLDEST), float(series.edges[0]),
        {"real": real, "constant": np.ones_like(real)}, series.stages,
        {
            "ramp_logistic": ramp.RampModel(series.edges, ramp.Logistic(100.0)),
            "ramp_logistic_kfree": [ramp.RampModel(series.edges, ramp.Logistic(k)) for k in CAPACITIES],
            "ramp_bd": ramp.RampModel(series.edges, ramp.ExpectedBirthDeath()),
        },
    )


def window_bounds(ts: sim.Timescale, window: str) -> tuple[float, float]:
    older, younger = WINDOWS[window]
    return float(ts.top[ts.index(younger)]), float(ts.base[ts.index(older)])


def psi_for_targets(effort: np.ndarray, mass: np.ndarray, targets: tuple[int, int]) -> np.ndarray:
    """psi of each channel so that its expected record count is the target."""
    return np.asarray(targets, dtype=float) / (effort @ mass)


def estimate(
    name: str, ctx: Context, counts: np.ndarray, effort: np.ndarray, young: np.ndarray, old: np.ndarray,
    rng: np.random.Generator,
) -> tuple[float, float, float, float]:
    """(point, lo, hi, unbounded) of one estimator for one set of channels; NaN where undefined."""
    if name in ("classical", "griwm"):
        estimator = est.strauss_sadler_1989 if name == "classical" else partial(est.weighted_mcinerny, alpha=0.05)
        lo, point, hi = est.stage_resampled(estimator, young, old, rng, N_DRAWS)
        return float(point), float(lo), float(hi), 0.0
    if counts.sum() == 0:
        return np.nan, np.nan, np.nan, np.nan
    f = ramp.fit(ctx.models[name], counts, effort)
    return f.t0, f.lo, f.hi, float(not f.bounded)


def replicate(ctx: Context, window: str, growth: str, rep: int) -> tuple[float, dict, dict]:
    ts = ctx.timescale
    seed = np.random.SeedSequence(ROOT_SEED, spawn_key=(list(WINDOWS).index(window), list(GROWTH).index(growth), rep))
    t0 = float(np.random.default_rng(sim.child_seed(seed, 99)).uniform(*window_bounds(ts, window)))
    abundance = sim.simulate_abundance(GROWTH[growth], t0, ctx.window_end, sim.child_seed(seed, 0))
    mass = sim.stage_exposure(abundance, ts)[ctx.first : ctx.last + 1]
    n_stages = ctx.last - ctx.first + 1
    results, n_records = {}, {}
    for e_i, effort_name in enumerate(EFFORTS):
        effort = ctx.effort[effort_name]
        for l_i, level in enumerate(LEVELS):
            psi = psi_for_targets(effort, mass, LEVELS[level])
            channels = {
                name: sim.Channel(psi[c], None if effort_name == "constant" else dict(zip(ctx.stages, effort[c].tolist())))
                for c, name in enumerate(("spores", "bodies"))
            }
            records = sim.simulate_records(abundance, channels, ts, sim.child_seed(seed, 10 + len(LEVELS) * e_i + l_i))
            by_channel = [records["spores"], records["bodies"]]
            counts = np.array([np.bincount(r.stage - ctx.first, minlength=n_stages) for r in by_channel])
            n_records[(effort_name, level)] = counts.sum(axis=1)
            for c_i, (channel_set, idx) in enumerate(CHANNEL_SETS.items()):
                young = np.concatenate([by_channel[c].young for c in idx])
                old = np.concatenate([by_channel[c].old for c in idx])
                for k_i, name in enumerate(ESTIMATORS):
                    rng = np.random.default_rng(sim.child_seed(seed, 1000 + ((e_i * len(LEVELS) + l_i) * 3 + c_i) * len(ESTIMATORS) + k_i))
                    results[(effort_name, level, channel_set, name)] = estimate(
                        name, ctx, counts[list(idx)], effort[list(idx)], young, old, rng
                    )
    return t0, results, n_records


def run_chunk(window: str, growth: str, reps: range) -> dict:
    ctx = context()
    t0s, cells, counts = [], {}, {}
    for rep in reps:
        t0, results, n_records = replicate(ctx, window, growth, rep)
        t0s.append(t0)
        for key, value in results.items():
            cells.setdefault(key, []).append(value)
        for key, value in n_records.items():
            counts.setdefault(key, []).append(value)
    return {
        "window": window, "growth": growth, "t0": np.array(t0s),
        "cells": {k: np.array(v) for k, v in cells.items()}, "counts": {k: np.array(v) for k, v in counts.items()},
    }


def merge(chunks: list[dict]) -> dict:
    merged = {"t0": np.concatenate([c["t0"] for c in chunks]), "cells": {}, "counts": {}}
    for key in chunks[0]["cells"]:
        merged["cells"][key] = np.concatenate([c["cells"][key] for c in chunks])
    for key in chunks[0]["counts"]:
        merged["counts"][key] = np.concatenate([c["counts"][key] for c in chunks])
    return merged


def calibration_interval(reference_errors: np.ndarray) -> tuple[float, float]:
    """Quantiles of (point - T0) in the reference scenario; T0 is estimated to lie in
    [point - upper, point - lower]."""
    ok = reference_errors[~np.isnan(reference_errors)]
    return float(np.quantile(ok, CALIBRATION_Q[0])), float(np.quantile(ok, CALIBRATION_Q[1]))


def verdict(estimator: str, coverage: float, bias: float, frac_unbounded: float) -> tuple[bool, bool, bool]:
    """(passes, identified, usable): the plan's criteria, the identifiability screen, and both."""
    passes = bool(coverage >= COVERAGE_MIN and abs(bias) < BIAS_MAX_MYR)
    identified = bool(not estimator.startswith("ramp") or frac_unbounded <= UNBOUNDED_MAX)
    return passes, identified, passes and identified


def summarise(t0: np.ndarray, res: np.ndarray, estimator: str, reference: np.ndarray | None) -> dict:
    ok = ~np.isnan(res[:, 0])
    out = {"n_reps": len(t0), "frac_undefined": float(1 - ok.mean())}
    if not ok.any():
        return out
    t0, (point, lo, hi, unbounded) = t0[ok], res[ok].T
    out["median_bias_ma"] = float(np.median(point - t0))
    out["frac_unbounded"] = float(unbounded.mean())
    if estimator == "griwm":
        q_lo, q_hi = calibration_interval(reference)
        out["coverage_calibrated"] = float(np.mean((point - q_hi <= t0) & (t0 <= point - q_lo)))
        out["median_width_ma"] = q_hi - q_lo
        own_lo, own_hi = calibration_interval(point - t0)
        out["calibrated_width_ma"] = own_hi - own_lo
        coverage = out["coverage_calibrated"]
    else:
        out["coverage_interval"] = float(np.mean((lo <= t0) & (t0 <= hi)))
        out["coverage_upper"] = float(np.mean(hi >= t0))
        out["median_width_ma"] = float(np.median(hi - lo))
        out["median_upper_excess_ma"] = float(np.median(hi - t0))
        coverage = out["coverage_upper"] if estimator == "classical" else out["coverage_interval"]
    out["passes"], out["identified"], out["usable"] = verdict(estimator, coverage, out["median_bias_ma"], out["frac_unbounded"])
    return out


def build_rows(merged: dict[tuple[str, str], dict]) -> list[dict]:
    rows = []
    for (window, growth), m in merged.items():
        for (effort, level, channel_set, estimator), res in m["cells"].items():
            reference = None
            if estimator == "griwm":
                ref = merged[(window, "constant")]["cells"][(effort, level, channel_set, estimator)]
                reference = ref[:, 0] - merged[(window, "constant")]["t0"]
            n = m["counts"][(effort, level)]
            rows.append({
                "window": window, "growth": growth, "effort": effort, "level": level,
                "target_spores": LEVELS[level][0], "target_bodies": LEVELS[level][1],
                "median_n_spores": float(np.median(n[:, 0])), "median_n_bodies": float(np.median(n[:, 1])),
                "channels": channel_set, "estimator": estimator, **summarise(m["t0"], res, estimator, reference),
            })
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, restval="", lineterminator="\n")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


def run(n_reps: int = N_REPS, workers: int | None = None, windows=WINDOWS, growth=GROWTH) -> list[dict]:
    tasks = [(w, g, range(lo, min(lo + CHUNK, n_reps))) for w in windows for g in growth for lo in range(0, n_reps, CHUNK)]
    with ProcessPoolExecutor(max_workers=workers or os.cpu_count()) as pool:
        chunks = list(pool.map(run_chunk, *zip(*tasks)))
    by_cell: dict[tuple[str, str], list[dict]] = {}
    for c in chunks:
        by_cell.setdefault((c["window"], c["growth"]), []).append(c)
    return build_rows({k: merge(v) for k, v in by_cell.items()})


def main() -> None:
    start = time.time()
    OUT.mkdir(exist_ok=True)
    rows = run()
    write_csv(rows, OUT / "recovery_grid.csv")
    seconds = round(time.time() - start, 1)
    meta = {
        "root_seed": ROOT_SEED, "n_reps": N_REPS, "n_stage_draws": N_DRAWS, "windows": WINDOWS,
        "growth": {k: repr(v) for k, v in GROWTH.items()}, "efforts": EFFORTS, "levels_spores_bodies": LEVELS,
        "ramp_logistic_capacity": 100.0, "capacities_profiled": CAPACITIES, "t0_max": ramp.T0_MAX, "t0_step": ramp.T0_STEP, "profile_level": ramp.PROFILE_LEVEL,
        "criteria": {"coverage_min": COVERAGE_MIN, "bias_max_myr": BIAS_MAX_MYR, "unbounded_max": UNBOUNDED_MAX},
        "max_coverage_se": round(0.5 / np.sqrt(N_REPS), 4),
        "timescale_sha256": hashlib.sha256(sim.TIMESCALE_CSV.read_bytes()).hexdigest(),
        "effort_csv_sha256": hashlib.sha256(inputs.EFFORT_CSV.read_bytes()).hexdigest(),
        "numpy": np.__version__, "scipy": scipy.__version__, "workers": os.cpu_count(), "seconds": seconds,
    }
    (OUT / "recovery_grid.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{len(rows)} rows in {seconds} s -> {OUT / 'recovery_grid.csv'}")


if __name__ == "__main__":
    main()
