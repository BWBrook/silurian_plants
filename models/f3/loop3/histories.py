"""Declared recovery histories, common to occurrence analysis and simulation."""

from pathlib import Path

import numpy as np
import pandas as pd

from endpoint import PiecewiseRecovery

ROOT = Path(__file__).resolve().parents[3]
YOUNG, DOMAIN = 393.47, 469.4
CUTOFFS = {"Emsian": YOUNG, "Pragian": 410.62, "Lochkovian": 413.02, "Pridoli": 419.62}
LABELS = {
    "flat": "Constant recovery",
    "pbdb_all": "PBDB collection density",
    "pbdb_plant_excluded": "PBDB, plant-filter matches removed",
    "decline25": "Recovery declines into past: 25 Myr",
    "decline10": "Recovery declines into past: 10 Myr",
    "pbdb_excluded_decline10": "Plant-excluded PBDB × 10 Myr decline",
}


def stage_table():
    t = pd.read_csv(ROOT / "data/timescale.csv")
    t["top_ma"] = t.base_ma.shift(1)
    return t[(t.base_ma <= DOMAIN) & (t.top_ma >= YOUNG)].sort_values("top_ma")


def stage_bounds(ages):
    t = stage_table()
    edges = np.r_[t.top_ma.values, DOMAIN]
    a = np.asarray(ages)
    if (a < YOUNG).any() or (a > DOMAIN).any():
        raise ValueError("age outside declared stage domain")
    j = np.minimum(np.searchsorted(edges, a, side="right") - 1, len(edges) - 2)
    return edges[j], edges[j + 1]


def load_histories(exclude_region=None):
    table = pd.read_csv(ROOT / "data/macro/effort_reviewed.csv")
    t = table[table.region == "global"].sort_values("young_ma").copy()
    if exclude_region is not None:
        removed = table[table.region == exclude_region].set_index("stage")
        for key in ("all_collection_equivalents", "plant_excluded_equivalents"):
            t[key] -= t.stage.map(removed[key]).fillna(0)
        for source, target in (("all_collection_equivalents", "all_density_per_myr"),
                               ("plant_excluded_equivalents", "plant_excluded_density_per_myr")):
            t[target] = t[source] / t.duration_myr
    edges = np.unique(np.r_[np.arange(YOUNG, DOMAIN, .05), t.young_ma, t.old_ma, DOMAIN])
    mid = (edges[:-1] + edges[1:]) / 2
    j = np.searchsorted(t.old_ma.values, mid)
    all_density = t.all_density_per_myr.values[j]
    excluded = t.plant_excluded_density_per_myr.values[j]
    densities = {
        "flat": np.ones_like(mid), "pbdb_all": all_density, "pbdb_plant_excluded": excluded,
        "decline25": np.exp(-(mid - YOUNG) / 25), "decline10": np.exp(-(mid - YOUNG) / 10),
        "pbdb_excluded_decline10": excluded * np.exp(-(mid - YOUNG) / 10),
    }
    if any((w <= 0).any() for w in densities.values()):
        raise ValueError("a declared geographic proxy has zero exposure; no positive-density model")
    return {key: PiecewiseRecovery(edges, w) for key, w in densities.items()}
