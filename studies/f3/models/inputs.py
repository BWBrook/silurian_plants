# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy"]
# ///

"""Per-stage sampling effort for the window Darriwilian to Emsian, from data/occurrences/effort.csv.

    uv run models/f3/inputs.py

Two series, each summed over palaeogeographic units: spores are the Palynodata documents with datable
palynomorph records (`n_docs`); bodies are the PBDB collections of all taxa from land and marginal
settings (`land` + `marginal`). Stages run youngest first, as in data/timescale.csv, and their
boundaries are the fixed ICS v2024/12 ages of that file.
"""

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

import sim

EFFORT_CSV = sim.ROOT / "data" / "occurrences" / "effort.csv"
OUT = Path(__file__).resolve().parent / "out"
OLDEST, YOUNGEST = "Darriwilian", "Emsian"


@dataclass(frozen=True)
class EffortSeries:
    stages: tuple[str, ...]
    edges: np.ndarray  # stage boundaries, ascending, one more than there are stages
    spores: np.ndarray
    bodies: np.ndarray

    @property
    def top(self) -> np.ndarray:
        return self.edges[:-1]

    @property
    def base(self) -> np.ndarray:
        return self.edges[1:]

    def as_mapping(self, channel: str) -> dict[str, float]:
        return dict(zip(self.stages, getattr(self, channel).tolist()))


def effort_series(path: Path = EFFORT_CSV, timescale: sim.Timescale | None = None) -> EffortSeries:
    ts = timescale or sim.Timescale.load()
    first, last = ts.index(YOUNGEST), ts.index(OLDEST)
    stages = ts.names[first : last + 1]
    spores = dict.fromkeys(stages, 0.0)
    bodies = dict.fromkeys(stages, 0.0)
    seen = {"spore": set(), "body": set()}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            stage = row["stage"]
            if stage not in spores:
                continue
            seen[row["channel"]].add(stage)
            if row["channel"] == "spore":
                spores[stage] += float(row["n_docs"] or 0.0)
            else:
                bodies[stage] += float(row["land"]) + float(row["marginal"])
    for channel, found in seen.items():
        missing = set(stages) - found
        if missing:
            raise ValueError(f"{path} has no {channel} rows for {sorted(missing)}")
    edges = np.concatenate([ts.top[first : first + 1], ts.base[first : last + 1]])
    return EffortSeries(stages, edges, np.array([spores[s] for s in stages]), np.array([bodies[s] for s in stages]))


def write_csv(series: EffortSeries, path: Path) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["stage", "top_ma", "base_ma", "spore_effort", "body_effort"])
        for i, stage in enumerate(series.stages):
            writer.writerow([stage, f"{series.top[i]:g}", f"{series.base[i]:g}", f"{series.spores[i]:g}", f"{series.bodies[i]:.2f}"])


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    series = effort_series()
    write_csv(series, OUT / "effort_series.csv")
    print(f"{len(series.stages)} stages, {series.stages[-1]} to {series.stages[0]} -> {OUT / 'effort_series.csv'}")
