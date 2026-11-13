# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy", "pandas"]
# ///
"""Loop 3 pilot: first-appearance intervals from the positive macrofossil record.

Builds dated horizons for three body-fossil categories (B0 any embryophyte body, B1 polysporangiophyte
body, B2 crown-tracheophyte member) from vetted PBDB collections plus the curated occurrence tail, and
reports the older limit of the origination interval under three recovery assumptions:

  classical  horizons uniform over [oldest, cut-off]   Marshall (1990) / Strauss & Sadler (1989)
  constant   rate = effort proxy x constant abundance   ramp.py likelihood with a flat history
  logistic   rate = effort proxy x logistic abundance   ramp.py, capacity profiled
  bd         rate = effort proxy x exp(g s)             ramp.py, expected birth-death

Ages are Ma, older is larger. Pilot status: the horizon set is v0 and awaits audit (docs/plan-loop3.md).

  uv run models/f3/loop3/macro.py build      # data/macro/horizons_v0.csv
  uv run models/f3/loop3/macro.py estimate   # models/f3/loop3/out/pilot_intervals.csv
"""

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "models" / "f3"))
import estimators  # noqa: E402
import ramp  # noqa: E402

PBDB = ROOT / "data/eprp/record"
OCC = ROOT / "data/occurrences"
CLASSES = ROOT / "work/codex/loop3"
HORIZONS = ROOT / "data/macro/horizons_v0.csv"
OUT = Path(__file__).resolve().parent / "out"

WINDOW_YOUNG, WINDOW_OLD = 393.47, 445.2  # Eifelian base to Hirnantian base
MAX_SPAN = 20.0  # Myr; PBDB collections dated more loosely are dropped and counted
EMBRYOPHYTE = {"rhyniophytoid_cooksonioid", "lycophyte_line", "euphyllophyte", "tracheophyte_indet",
               "polysporangiophyte_indet", "embryophyte_axis_indet", "bryophyte_grade"}
TAIL_EVENTS = {"E3", "E4", "E5"}  # E3/E4 records are polysporangiophyte bodies; E5 adds crown-tracheophyte membership
COUNTRY = {"IE": "Ireland", "UA": "Ukraine", "UK": "United Kingdom", "AU": "Australia", "US": "USA", "CA": "Canada",
           "CZ": "Czech Republic", "KZ": "Kazakhstan", "CN": "China", "LY": "Libya", "PL": "Poland", "AR": "Argentina",
           "BO": "Bolivia", "VN": "Vietnam", "RU": "Russia", "BE": "Belgium", "DE": "Germany", "NO": "Norway", "FR": "France"}
CUTOFFS = {"Pridoli": 419.62, "Lochkovian": 413.02, "Pragian": 410.62, "Emsian": 393.47}
SEED = 20261101
N_AGE_DRAWS = 200


def stages() -> pd.DataFrame:
    t = pd.read_csv(ROOT / "data/timescale.csv")
    t["top_ma"] = t.base_ma.shift(1)
    return t[(t.base_ma <= 470) & (t.base_ma > WINDOW_YOUNG)].reset_index(drop=True)


def stage_of(age: float, t: pd.DataFrame) -> str:
    row = t[(t.base_ma >= age) & (t.top_ma < age)]
    return row.stage.iloc[0] if len(row) else ""


def load_classes() -> pd.DataFrame:
    items = []
    for f in sorted(CLASSES.glob("out_*.json")):
        items += json.loads(f.read_text())["items"]
    return pd.DataFrame(items)


def build() -> pd.DataFrame:
    cls = load_classes().set_index("name")
    occ = pd.read_csv(PBDB / "pbdb_plant_occurrences.csv", low_memory=False)
    occ = occ[(occ.d_record_type != "dispersed_spore") & (occ.min_ma < WINDOW_OLD) & (occ.max_ma > WINDOW_YOUNG)].copy()
    occ["nm"] = occ.accepted_name.fillna(occ.identified_name)
    occ = occ[occ.nm.isin(cls.index)]
    occ["category"] = occ.nm.map(cls.category)
    occ["b0"] = occ.category.isin(EMBRYOPHYTE)
    occ["b1"] = occ.nm.map(cls.polysporangiophyte).eq("yes")
    occ["b2"] = occ.nm.map(cls.crown_tracheophyte).eq("yes")
    col = pd.read_csv(PBDB / "pbdb_plant_collections.csv", low_memory=False,
                      usecols=["collection_no", "collection_name", "formation", "lat", "lng", "cc"])
    g = occ.groupby("collection_no").agg(max_ma=("max_ma", "max"), min_ma=("min_ma", "min"),
                                         b0=("b0", "any"), b1=("b1", "any"), b2=("b2", "any"),
                                         names=("nm", lambda s: "; ".join(sorted(set(s))))).reset_index()
    g = g.merge(col.drop_duplicates("collection_no"), on="collection_no", how="left")
    g = g[g.b0 | g.b1 | g.b2]
    loose = g.max_ma - g.min_ma > MAX_SPAN
    print(f"PBDB collections with accepted body fossils: {len(g)}; dropped for spans > {MAX_SPAN} Myr: {int(loose.sum())}")
    g = g[~loose]
    form = g.formation.fillna("").str.lower().str.strip()
    g["locality"] = g.cc.fillna("") + "|" + np.where(form != "", form, g.collection_name.fillna("").str.lower()) \
        + "|" + g.lat.round(1).astype(str) + "," + g.lng.round(1).astype(str)
    g["horizon_id"] = "pbdb:" + g.collection_no.astype(str)
    g["source"] = "pbdb"
    g["reading"] = "all"
    rows = [g[["horizon_id", "source", "reading", "max_ma", "min_ma", "b0", "b1", "b2", "cc", "locality", "names"]]]

    tail = tail_horizons()
    linked = tail_links(g, tail)
    print(f"PBDB collections replaced by the curated tail (same material): {len(linked)}")
    rows[0] = rows[0][~rows[0].horizon_id.isin(linked)]
    rows.append(tail)
    h = pd.concat(rows, ignore_index=True)
    h = h.groupby(["horizon_id", "reading"], as_index=False).agg(
        {"source": "first", "max_ma": "first", "min_ma": "first", "b0": "any", "b1": "any", "b2": "any",
         "cc": "first", "locality": "first", "names": "first"})
    h["stage_oldest"] = [stage_of(a - 1e-6, stages()) for a in h.max_ma]
    h["stage_youngest"] = [stage_of(a + 1e-6, stages()) for a in h.min_ma]
    HORIZONS.parent.mkdir(parents=True, exist_ok=True)
    h.to_csv(HORIZONS, index=False, lineterminator="\n")
    return h


def tail_horizons() -> pd.DataFrame:
    """Curated tail records (data/occurrences) as horizons, one row per observation and reading."""
    obs = pd.read_csv(OCC / "observations.csv")
    ra = pd.read_csv(OCC / "reading_assignments.csv")
    t = pd.read_csv(ROOT / "data/timescale.csv")
    base, top = dict(zip(t.stage, t.base_ma)), dict(zip(t.stage, t.base_ma.shift(1)))
    a = ra[ra.event.isin(TAIL_EVENTS) & ~ra.obs_id.str.startswith("M-pbdb-") & ra.same_material_as.isna()]
    a = a.merge(obs[["obs_id", "country", "locality", "reported_as"]], on="obs_id")
    a = a.assign(e5=a.event.eq("E5")).groupby(["obs_id", "reading_id"], as_index=False).agg(
        stage_oldest=("stage_oldest", "first"), stage_youngest=("stage_youngest", "first"), e5=("e5", "any"),
        country=("country", "first"), locality=("locality", "first"), reported_as=("reported_as", "first"))
    return pd.DataFrame({
        "horizon_id": "tail:" + a.obs_id, "source": "tail", "reading": a.reading_id,
        "max_ma": a.stage_oldest.map(base), "min_ma": a.stage_youngest.map(top),
        "b0": True, "b1": True, "b2": a.e5, "cc": a.country,
        "locality": a.country.fillna("") + "|" + a.locality.fillna("").str.lower(), "names": a.reported_as})


def _genera(text: str) -> set[str]:
    return {w.strip("?<>\"().,;") for w in str(text).replace(";", " ").split() if w[:1].isupper() and len(w) > 4}


def tail_links(pbdb: pd.DataFrame, tail: pd.DataFrame) -> set[str]:
    """PBDB collections that report material the curated tail already adjudicated: those its observations
    cite by collection or occurrence number, and those sharing country, overlapping age and a genus name
    with a tail observation. The tail's readings then govern that material."""
    import re
    obs = pd.read_csv(OCC / "observations.csv").fillna("").astype(str)
    text = " ".join(obs.agg(" ".join, axis=1))
    occ_nos = {int(x) for x in re.findall(r"occurrence_no=(\d+)", text)} | {int(x) for x in re.findall(r"PBDB (\d{6,7})", text)}
    occ = pd.read_csv(PBDB / "pbdb_plant_occurrences.csv", low_memory=False, usecols=["occurrence_no", "collection_no"])
    cited = set(occ[occ.occurrence_no.isin(occ_nos)].collection_no) | {int(x) for x in re.findall(r"collection (\d{4,6})", text, re.I)}
    links = {f"pbdb:{c}" for c in cited}
    t = tail.drop_duplicates("horizon_id")
    for _, p in pbdb.iterrows():
        country = COUNTRY.get(p.cc, p.cc)
        same = t[(t.cc == country) & (t.max_ma > p.min_ma) & (t.min_ma < p.max_ma)]
        if any(_genera(p.names) & _genera(n) for n in same.names):
            links.add(f"pbdb:{p.collection_no}")
    return links & set("pbdb:" + pbdb.collection_no.astype(str))


def records(h: pd.DataFrame, cat: str, reading: str) -> pd.DataFrame:
    keep = h[h[cat.lower()] & h.reading.isin(["all", reading])]
    return keep.drop_duplicates("horizon_id")


@dataclass(frozen=True)
class Constant:
    """Flat history: N(s) = 1 from origination. The rate grid is a placeholder."""

    name: str = "constant"
    default_rates = np.array([1.0])

    def grid(self, rates: np.ndarray) -> dict[str, np.ndarray]:
        return {"rate": rates}

    def cumulative(self, s: np.ndarray, rate: np.ndarray) -> np.ndarray:
        return s + 0.0 * rate


def effort_series(edges: np.ndarray) -> np.ndarray:
    e = pd.read_csv(OCC / "effort.csv")
    e = e[e.channel == "body"].groupby("base_ma")[["land", "marginal"]].sum().sum(axis=1)
    return np.array([e.get(round(b, 2), np.nan) for b in edges[1:]])


def stage_counts(ages: np.ndarray, edges: np.ndarray) -> np.ndarray:
    idx = np.searchsorted(edges, ages, side="left") - 1
    return np.bincount(idx[(idx >= 0) & (idx < len(edges) - 1)], minlength=len(edges) - 1)


def estimate() -> pd.DataFrame:
    h = pd.read_csv(HORIZONS)
    t = stages()
    edges = np.sort(np.concatenate([[WINDOW_YOUNG], t.base_ma.values]))
    effort = effort_series(edges)
    models = {
        "constant": ramp.RampModel(edges, Constant()),
        "logistic": [ramp.RampModel(edges, ramp.Logistic(k)) for k in (10.0, 30.0, 100.0, 300.0, 1000.0)],
        "bd": ramp.RampModel(edges, ramp.ExpectedBirthDeath()),
    }
    rng = np.random.default_rng(SEED)
    out = []
    for cat in ("B0", "B1", "B2"):
        for reading in ("main", "inclusive"):
            r = records(h, cat, reading)
            lo, hi = r.min_ma.values, r.max_ma.values
            mid = (lo + hi) / 2
            draws = rng.uniform(lo, hi, size=(N_AGE_DRAWS, len(r)))
            base = {"category": cat, "reading": reading, "n_horizons": len(r),
                    "n_localities": r.locality.nunique(), "oldest_max_ma": hi.max(), "oldest_mid_ma": mid.max()}
            for name, cut in CUTOFFS.items():
                sel = draws > cut
                limits = [estimators.marshall_1990(d[s], 0.95).hi for d, s in zip(draws, sel) if s.sum() >= 2]
                out.append({**base, "estimator": f"classical_to_{name}", "assumption": "uniform horizons to cut-off",
                            "older_limit_ma": float(np.median(limits)), "limit_q05": float(np.quantile(limits, 0.05)),
                            "limit_q95": float(np.quantile(limits, 0.95)), "bounded": True,
                            "n_used_median": int(np.median(sel.sum(axis=1)))})
            for name, m in models.items():
                fits = []
                for d in draws[:40]:
                    n = stage_counts(d, edges)[None, :]
                    f = ramp.fit(m, n, effort[None, :])
                    fits.append((f.hi if f.bounded else np.inf, f.t0))
                his = np.array([x[0] for x in fits])
                out.append({**base, "estimator": name, "assumption": f"rate = land+marginal PBDB effort x {name} abundance",
                            "older_limit_ma": float(np.median(his)), "limit_q05": float(np.quantile(his, 0.05)),
                            "limit_q95": float(np.quantile(his, 0.95)), "bounded": bool(np.isfinite(his).mean() >= 0.9),
                            "n_used_median": len(r)})
    df = pd.DataFrame(out)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "pilot_intervals.csv", index=False, lineterminator="\n", float_format="%.2f")
    return df


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "estimate"
    if cmd == "build":
        print(build().groupby("reading")[["b0", "b1", "b2"]].sum())
    else:
        print(estimate().to_string())
