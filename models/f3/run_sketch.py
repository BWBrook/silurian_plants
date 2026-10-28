# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy"]
# ///
"""Demonstration grid: coverage and bias of first-appearance estimators against a known origination.

    uv run models/f3/run_sketch.py

Writes models/f3/out/sketch_grid.csv and sketch_grid.meta.json (seeds, settings, timescale hash).
One row per growth form x channel psi x channel x dating x estimator. In each replicate the true
origination age T0 is drawn uniformly within the Telychian, so results average over where in its
stage the origination falls. Coverage is judged against T0; bias is point - T0 in Myr, positive
meaning older than the truth.
"""

import csv
import hashlib
import json
import time
from functools import partial
from pathlib import Path

import numpy as np

import estimators as est
import sim

OUT = Path(__file__).resolve().parent / "out"
ROOT_SEED = 20261028
N_REPS = 2000
N_DRAWS = 300
ORIGIN_STAGE = "Telychian"  # T0 is drawn uniformly within this stage in each replicate
PSI = (0.005, 0.02, 0.08)  # records per lineage per Myr in the spore channel
BODY_FRACTION = 0.2  # body-fossil psi as a fraction of the spore psi
GROWTH = {
    "constant": sim.Constant(k=50),
    "logistic": sim.Logistic(r=0.35, k=100),
    "birthdeath": sim.BirthDeath(lam=0.25, mu=0.15),
}
ESTIMATORS = {
    "oldest": est.oldest,
    "marshall1990": est.marshall_1990,
    "strauss_sadler1989": est.strauss_sadler_1989,
    "griwm_alpha0.05": partial(est.weighted_mcinerny, alpha=0.05),
    "griwm_alpha0.5": partial(est.weighted_mcinerny, alpha=0.5),
}
COLUMNS = [
    "growth", "channel", "psi", "dating", "estimator", "n_reps", "frac_undefined", "median_records",
    "coverage_upper", "coverage_interval", "median_bias_ma", "median_upper_excess_ma",
]


def one_replicate(
    abundance: sim.Abundance,
    t0: float,
    psi: float,
    timescale: sim.Timescale,
    record_seed: np.random.SeedSequence,
    dating_seed: np.random.SeedSequence,
) -> dict[tuple, tuple[int, float, est.Interval]]:
    channels = {"spores": sim.Channel(psi), "bodies": sim.Channel(psi * BODY_FRACTION)}
    records = sim.simulate_records(abundance, channels, timescale, record_seed)
    out = {}
    for c_i, (channel, rec) in enumerate(sorted(records.items())):
        for name, estimator in ESTIMATORS.items():
            out[(channel, "exact", name)] = (len(rec.age), t0, estimator(rec.age))
            draw_rng = np.random.default_rng(sim.child_seed(dating_seed, c_i))
            pooled = est.stage_resampled(estimator, rec.young, rec.old, draw_rng, N_DRAWS)
            out[(channel, "stage", name)] = (len(rec.age), t0, pooled)
    return out


def summarise(results: list[tuple[int, float, est.Interval]]) -> dict:
    n = np.array([r[0] for r in results])
    t0 = np.array([r[1] for r in results])
    lo, point, hi = (np.array([float(r[2][i]) for r in results]) for i in range(3))
    ok = ~np.isnan(point)
    if not ok.any():
        return {"n_reps": len(n), "frac_undefined": 1.0, "median_records": float(np.median(n))}
    return {
        "n_reps": len(n),
        "frac_undefined": float(1 - ok.mean()),
        "median_records": float(np.median(n)),
        "coverage_upper": float(np.mean(hi[ok] >= t0[ok])),
        "coverage_interval": float(np.mean((lo[ok] <= t0[ok]) & (t0[ok] <= hi[ok]))),
        "median_bias_ma": float(np.median(point[ok] - t0[ok])),
        "median_upper_excess_ma": float(np.median(hi[ok] - t0[ok])),
    }


def run_grid(n_reps: int = N_REPS, psis: tuple = PSI, growths: dict = GROWTH) -> list[dict]:
    timescale = sim.Timescale.load()
    window_end = float(timescale.base[timescale.index("Eifelian")])
    origin = timescale.index(ORIGIN_STAGE)
    rows = []
    for g_i, (growth_name, growth) in enumerate(growths.items()):
        collected: dict[tuple, list] = {}
        for rep in range(n_reps):
            seed = np.random.SeedSequence(ROOT_SEED, spawn_key=(g_i, rep))
            t0 = np.random.default_rng(sim.child_seed(seed, 99)).uniform(timescale.top[origin], timescale.base[origin])
            abundance = sim.simulate_abundance(growth, t0, window_end, sim.child_seed(seed, 0))
            for p_i, psi in enumerate(psis):
                record_seed = sim.child_seed(seed, 10 + p_i)
                dating_seed = sim.child_seed(seed, 100 + p_i)
                result = one_replicate(abundance, t0, psi, timescale, record_seed, dating_seed)
                for key, value in result.items():
                    collected.setdefault((p_i, *key), []).append(value)
        for (p_i, channel, dating, name), results in collected.items():
            psi = psis[p_i] * (1.0 if channel == "spores" else BODY_FRACTION)
            rows.append({"growth": growth_name, "channel": channel, "psi": psi, "dating": dating,
                         "estimator": name, **summarise(results)})
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    order = {name: i for i, name in enumerate(ESTIMATORS)}
    rows = sorted(rows, key=lambda r: (list(GROWTH).index(r["growth"]), r["channel"], r["psi"], r["dating"], order[r["estimator"]]))
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, restval="")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()})


def main() -> None:
    start = time.time()
    OUT.mkdir(exist_ok=True)
    rows = run_grid()
    write_csv(rows, OUT / "sketch_grid.csv")
    meta = {
        "root_seed": ROOT_SEED, "n_reps": N_REPS, "n_stage_draws": N_DRAWS, "t0": f"uniform within the {ORIGIN_STAGE}",
        "window_end": "base of Eifelian (end of Emsian)", "psi_spores": PSI, "body_fraction": BODY_FRACTION,
        "growth": {k: repr(v) for k, v in GROWTH.items()},
        "timescale_sha256": hashlib.sha256(sim.TIMESCALE_CSV.read_bytes()).hexdigest(),
        "numpy": np.__version__, "seconds": round(time.time() - start, 1),
    }
    (OUT / "sketch_grid.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(f"{len(rows)} rows in {meta['seconds']} s -> {OUT / 'sketch_grid.csv'}")


if __name__ == "__main__":
    main()
