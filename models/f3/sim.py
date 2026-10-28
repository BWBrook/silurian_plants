"""Virtual palaeontology for F3: a clade of abundance N(t) leaves stage-dated fossil occurrences.

Ages are Ma, decreasing towards the present, so older means larger. A clade originates at the
true age t0 with N = 1. Each channel (for example spores or bodies) records occurrences as an
inhomogeneous Poisson process with intensity psi * N(age) * E(age), where E is a sampling effort
that is constant within each ICS stage. Records exist only between the window end and t0. Each
record keeps its true age and the age range of the stage it falls in.

Seeds: every random call descends from one seed through child_seed, so a (seed, arguments) pair
reproduces a run. The abundance path and each channel's occurrences have separate child streams,
so changing psi or the channel set leaves the abundance path unchanged.
"""

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Protocol

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
TIMESCALE_CSV = ROOT / "data" / "timescale.csv"
LOGISTIC_DT = 0.01  # Myr; cell width when the deterministic logistic is discretised
MAX_SURVIVAL_TRIES = 10_000


@dataclass(frozen=True)
class Timescale:
    """ICS stages from youngest to oldest. Stage i spans [top[i], base[i]); top[0] is unknown."""

    names: tuple[str, ...]
    base: np.ndarray
    top: np.ndarray

    @classmethod
    def load(cls, path: Path = TIMESCALE_CSV) -> "Timescale":
        with open(path, newline="") as f:
            rows = list(csv.DictReader(f))
        base = np.array([float(r["base_ma"]) for r in rows])
        if np.any(np.diff(base) <= 0):
            raise ValueError("timescale.csv must list stages from youngest to oldest")
        top = np.concatenate([[np.nan], base[:-1]])
        return cls(tuple(r["stage"] for r in rows), base, top)

    def index(self, name: str) -> int:
        return self.names.index(name)

    def stage_of(self, age: np.ndarray) -> np.ndarray:
        """Index of the stage containing each age; an age on a base belongs to the older stage."""
        idx = np.searchsorted(self.base, age, side="right")
        if np.any(idx >= len(self.names)) or np.any(idx == 0):
            raise ValueError("age outside the stages covered by the timescale")
        return idx


@dataclass(frozen=True)
class Abundance:
    """Piecewise-constant N: values[i] holds on [edges[i], edges[i+1]), ages ascending to t0."""

    edges: np.ndarray
    values: np.ndarray

    def at(self, age: float) -> float:
        if age < self.edges[0] or age >= self.edges[-1]:
            return 0.0
        return float(self.values[np.searchsorted(self.edges, age, side="right") - 1])


class Growth(Protocol):
    def abundance(self, t0: float, window_end: float, rng: np.random.Generator) -> Abundance: ...


def _from_time_since_origin(t0: float, window_end: float, s_edges: np.ndarray, values: np.ndarray) -> Abundance:
    edges = t0 - s_edges
    edges[-1] = window_end
    return Abundance(edges[::-1], values[::-1])


@dataclass(frozen=True)
class Constant:
    """N jumps to k at t0 and stays there: the control case with no ramp."""

    k: float

    def abundance(self, t0: float, window_end: float, rng: np.random.Generator) -> Abundance:
        return Abundance(np.array([window_end, t0]), np.array([float(self.k)]))


@dataclass(frozen=True)
class Logistic:
    """Deterministic N(s) = k / (1 + (k - 1) exp(-r s)) after s Myr from t0, so N(0) = 1."""

    r: float
    k: float

    def abundance(self, t0: float, window_end: float, rng: np.random.Generator) -> Abundance:
        s_max = t0 - window_end
        s_edges = np.linspace(0.0, s_max, max(2, int(np.ceil(s_max / LOGISTIC_DT)) + 1))
        mid = (s_edges[:-1] + s_edges[1:]) / 2
        values = self.k / (1.0 + (self.k - 1.0) * np.exp(-self.r * mid))
        return _from_time_since_origin(t0, window_end, s_edges, values)


@dataclass(frozen=True)
class BirthDeath:
    """Linear birth-death process from one lineage, conditioned to survive to the window end."""

    lam: float
    mu: float

    def abundance(self, t0: float, window_end: float, rng: np.random.Generator) -> Abundance:
        s_max = t0 - window_end
        p_birth = self.lam / (self.lam + self.mu)
        for _ in range(MAX_SURVIVAL_TRIES):
            s, n = 0.0, 1
            times, counts = [0.0], []
            while True:
                s += rng.exponential(1.0 / ((self.lam + self.mu) * n))
                counts.append(n)
                if s >= s_max:
                    times.append(s_max)
                    break
                times.append(s)
                n += 1 if rng.random() < p_birth else -1
                if n == 0:
                    break
            if n > 0:
                return _from_time_since_origin(t0, window_end, np.array(times), np.array(counts, dtype=float))
        raise RuntimeError("birth-death clade never survived; check lam > mu and the window")


@dataclass(frozen=True)
class Channel:
    """One record channel: psi records per lineage per Myr, and stage effort (default 1)."""

    psi: float
    effort: Mapping[str, float] | None = None


@dataclass(frozen=True)
class Records:
    """Occurrences of one channel, oldest first, with the stage each is dated to."""

    age: np.ndarray
    stage: np.ndarray
    young: np.ndarray
    old: np.ndarray


@dataclass(frozen=True)
class Run:
    t0: float
    window_end: float
    abundance: Abundance
    records: dict[str, Records]


def child_seed(seed: int | np.random.SeedSequence, index: int) -> np.random.SeedSequence:
    """The index-th child stream of a seed. Unlike SeedSequence.spawn it never changes its input,
    so the same (seed, index) always gives the same stream."""
    ss = seed if isinstance(seed, np.random.SeedSequence) else np.random.SeedSequence(seed)
    return np.random.SeedSequence(ss.entropy, spawn_key=(*ss.spawn_key, index))


def effort_by_stage(timescale: Timescale, effort: Mapping[str, float] | None) -> np.ndarray:
    values = np.ones(len(timescale.names))
    for name, e in (effort or {}).items():
        if e < 0:
            raise ValueError(f"effort for {name} must be non-negative")
        values[timescale.index(name)] = e
    return values


def sample_records(
    abundance: Abundance,
    channel: Channel,
    timescale: Timescale,
    rng: np.random.Generator,
) -> Records:
    stage_bases = timescale.base[(timescale.base > abundance.edges[0]) & (timescale.base < abundance.edges[-1])]
    edges = np.unique(np.concatenate([abundance.edges, stage_bases]))
    lo, hi = edges[:-1], edges[1:]
    mid = (lo + hi) / 2
    n_lineages = abundance.values[np.searchsorted(abundance.edges, mid, side="right") - 1]
    effort = effort_by_stage(timescale, channel.effort)[timescale.stage_of(mid)]
    counts = rng.poisson(channel.psi * n_lineages * effort * (hi - lo))
    age = np.repeat(lo, counts) + rng.random(counts.sum()) * np.repeat(hi - lo, counts)
    age = np.sort(age)[::-1]
    stage = timescale.stage_of(age)
    return Records(age, stage, timescale.top[stage], timescale.base[stage])


def simulate_abundance(
    growth: Growth, t0: float, window_end: float, seed: int | np.random.SeedSequence
) -> Abundance:
    if not window_end < t0:
        raise ValueError("the window must end after the clade originates")
    return growth.abundance(t0, window_end, np.random.default_rng(seed))


def simulate_records(
    abundance: Abundance,
    channels: Mapping[str, Channel],
    timescale: Timescale,
    seed: int | np.random.SeedSequence,
) -> dict[str, Records]:
    return {
        name: sample_records(abundance, channels[name], timescale, np.random.default_rng(child_seed(seed, i)))
        for i, name in enumerate(sorted(channels))
    }


def simulate(
    growth: Growth,
    t0: float,
    channels: Mapping[str, Channel],
    window_end: float,
    timescale: Timescale,
    seed: int | np.random.SeedSequence = 0,
) -> Run:
    """One virtual palaeontology; seed fixes the abundance path and every channel's records."""
    abundance = simulate_abundance(growth, t0, window_end, child_seed(seed, 0))
    return Run(t0, window_end, abundance, simulate_records(abundance, channels, timescale, child_seed(seed, 1)))
