# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Conditional qualification of an M2 real design (designs/m2.toml, [qualification] and amendment 1).

    uv run models/f3/qualify.py --design LY-H2-CU --rho 1 --phase calibrate --workers 8
    uv run models/f3/qualify.py --design LY-H2-CU --rho 1 --phase accept --workers 8     # reads the calibration receipt
    uv run models/f3/qualify.py --design LY-H2-CU --rho 1 --phase stage2 --workers 8     # borderline quantities only

The simulator keeps the design fixed: the same units, stage or numerical ranges, classes, clusters and
transport multipliers as the data. Truth: the data's fitted reference rate (X3: its one-sided 95% lower
limit), the declared rho (X1: half of it), well effects Gamma(k, k) (X2: k = 0.8), true ages sorted by
depth within each well and range group, tau0 = the data's tau, and the cell's history a(t) between tau0
and t0 (1 younger than tau0, 0 older than t0). Each replicate applies the amended screen (potential
outcomes) and, when it passes, the full analysis at the phase's critical-value shift. Replicates are taken
in index order until `target` pass or `max_attempts` are used, so the result does not depend on the
number of workers.

Acceptance quantities (delivered coverage among passing replicates, at the truth point t0):
  f_<K>         f*_K(t0) contains abar_rel and LR_K(abar_rel) <= crit, both converged (K containing the truth);
  o_<K>_<f>     the origin set at f_min = f contains t0: exact statistic at t0 <= crit and the grid point
                at or below t0 kept, both converged (H0c only for constant truths; H0m for monotone ones);
  w_<f>         the window read-out (H0, start 459.1) likewise, when a >= f on (459.1, t0].
A replicate whose first appearance reaches t0 makes no claim there and covers. Margins (statistic minus
the unshifted critical value; inf for a failed output) give the calibration shift, as in validate.py.
"""

import argparse
import gzip
import hashlib
import io
import csv
import json
import math
import platform
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy import stats

import designs as dz
import envelope as ev
import m2
import validate as va

OUT = Path(__file__).resolve().parent / "out" / "qual"
STEP = 0.5
TOL = va.ROOT_TOL


# --- truth -------------------------------------------------------------------------------------------

def path_for(cell: dict, tau0: float, ctx: dict):
    """a(t) for the cell, vectorised; 1 younger than tau0, 0 older than t0."""
    t0, f, h = cell["t0"], cell.get("f", 1.0), cell["history"]
    if h == "H0c":
        mid = lambda t: np.full_like(t, f)
    elif h == "ramp":
        mid = lambda t: (t0 - t) / (t0 - tau0)
    elif h == "window":
        mid = lambda t: np.where(t <= 459.1, 1.0, f)
    elif h in ("hide", "hide_h1"):
        height = cell.get("pulse", 1.0) if h == "hide_h1" else 1.0
        edges = np.unique(np.r_[tau0, t0, ctx["bases"][(ctx["bases"] > tau0) & (ctx["bases"] < t0)]])
        dens = np.array([ctx["density"](lo, hi) for lo, hi in zip(edges[:-1], edges[1:])])
        need = f * (t0 - tau0) / height
        on = []
        for p in np.argsort(dens, kind="stable"):
            lo, hi = edges[p], edges[p + 1]
            take = min(hi - lo, need)
            if take <= 0:
                break
            on.append((hi - take, hi))
            need -= take
        mid = lambda t: height * sum(((t > lo) & (t <= hi)).astype(float) for lo, hi in on)
    else:
        raise ValueError(h)
    return lambda t: np.where(t <= tau0, 1.0, np.where(t > t0, 0.0, mid(np.asarray(t, float))))


def members(cell: dict) -> set[str]:
    h = cell["history"]
    if h == "H0c":
        return {"H0c", "H0m", "H0", "H1"} if cell["f"] <= 1 else {"H1"}
    if h in ("ramp", "window"):
        return {"H0m", "H0", "H1"}
    if h == "hide":
        return {"H0", "H1"}
    return {"H1"}


class Context:
    """The fixed design, its data fit and the truth settings shared by a cell's replicates."""

    def __init__(self, design_id: str, rho: float):
        self.decl = dz.declarations()
        self.design = next(d for d in self.decl["design"] if d["id"] == design_id)
        p = self.design["primary"]
        self.variant = {k: p[k] for k in p if k != "min_ref_units"}
        self.min_ref, self.k = p["min_ref_units"], p["cluster_k"]
        self.rho = rho
        self.built = dz.build(self.design, self.variant)
        self.units, _ = self.built.units(rho)
        self.transported = np.array([r.transported for r in self.built.rows])
        self.data = m2.problem(self.built, self.decl, rho, self.k, self.min_ref)
        self.tau0 = self.data.tau
        rates = np.full(int(self.units.cls.max()) + 1, np.nan)
        rates[self.data.calibrated] = self.data.r_ref
        self.r_data = rates
        self.age = ev.AgeModel.load()
        base = self.age.base
        u = self.units
        self.lo = np.where(np.isnan(u.lo_ma), base[u.young - 1], u.lo_ma)
        self.hi = np.where(np.isnan(u.hi_ma), base[u.old], u.hi_ma)
        depth = np.array([r.depth for r in self.built.rows])
        keys = [(r.cluster_name, lo, hi) for r, lo, hi in zip(self.built.rows, self.lo, self.hi)]
        self.groups = [np.array(sorted((i for i, k in enumerate(keys) if k == g), key=lambda i: depth[i]))
                       for g in dict.fromkeys(keys)]
        self.descending = {r.source for r in self.built.rows}
        self.spec0 = m2.problem(self.built, self.decl, rho, self.k, self.min_ref).spec

    def rates(self, cell: dict) -> np.ndarray:
        r = self.r_data.copy()
        if cell.get("reference_p") == "lower-95":
            for c in self.data.calibrated:
                ref = (self.units.cls == c) & ~self.transported
                n, k = int(ref.sum()), int(self.units.d[ref].sum())
                p = va.lower_limit(k, n)
                r[c] = -math.log(1 - p)
        return r

    def density(self, rates: np.ndarray, mult: np.ndarray):
        w = rates[self.units.cls] * mult / (self.hi - self.lo)
        return lambda lo, hi: float((w * np.clip(np.minimum(self.hi, hi) - np.maximum(self.lo, lo), 0, None)).sum() / (hi - lo))


def simulate(ctx: Context, cell: dict, rng: np.random.Generator):
    rates = ctx.rates(cell)
    mult = ctx.units.mult * np.where(ctx.transported, cell.get("rho_true_factor", 1.0), 1.0)
    k = cell.get("k_true", ctx.k)
    path = path_for(cell, ctx.tau0, dict(bases=ctx.age.base, density=ctx.density(rates, mult)))
    t = np.empty(len(ctx.units.d))
    for g in ctx.groups:
        # deeper units are older: sorted uniforms assigned by depth (Qusaiba/Borenshult depths in metres
        # or feet, Libya in feet; each increases downwards)
        t[g] = np.sort(rng.uniform(ctx.lo[g[0]], ctx.hi[g[0]], len(g)))
    nclu = int(ctx.units.cluster.max()) + 1
    u = np.ones(nclu) if math.isinf(k) else rng.gamma(k, 1 / k, nclu)
    p = 1 - np.exp(-rates[ctx.units.cls] * mult * u[ctx.units.cluster] * path(t))
    d = (rng.uniform(size=len(t)) < p).astype(int)
    U = ctx.units
    return ev.Units(U.young, U.old, U.cls, U.cluster, d, U.mult, U.lo_ma, U.hi_ma), path, rates, mult


# --- one replicate -----------------------------------------------------------------------------------

def applicable(cell: dict, path, tau0: float, a_ref: float, start: float | None, lag: float) -> list[float]:
    t0 = cell["t0"]
    lo = tau0 if start is None else start
    hi = t0 - lag
    if hi <= lo:
        return []
    grid = np.linspace(lo + 1e-6, hi, 2000)
    m = float(path(grid).min()) / a_ref
    return [f for f in (1.0, 0.1, 0.01) if f <= m + 1e-9]


def replicate(job) -> dict:
    design_id, rho, cell, rep, root, shift = job
    ctx = _ctx(design_id, rho)
    ss = np.random.SeedSequence(root, spawn_key=(ctx.design_index, ctx.rho_index, cell["index"], rep))
    rng = np.random.default_rng(ss)
    out = dict(cell=cell["name"], rep=rep, passed=False, error="")
    try:
        units, path, rates, mult = simulate(ctx, cell, rng)
        out["n_old_det"] = int(units.d[ctx.transported].sum())
        try:
            pot = ev.Problem(m2.potential(units, ctx.transported), ctx.spec0, ctx.age)
            ok, lr1, _ = m2.screen(pot)
        except ev.NoFirstAppearance:
            ok, lr1 = False, 0.0
        out["screen_lr"] = lr1
        if not ok:
            return out
        out["passed"] = True
        spec = ev.Spec(**{**ctx.spec0.__dict__, "crit_shift": shift})
        pr = ev.Problem(units, spec, ctx.age)
        out.update(_analyse(ctx, cell, pr, path, rates, mult))
    except Exception as e:  # a failure after passing stays in the denominator as a miss
        out["error"] = f"{type(e).__name__}: {e}"
    return out


def _analyse(ctx: Context, cell: dict, pr: ev.Problem, path, rates, mult) -> dict:
    t0 = cell["t0"]
    out = dict(tau=pr.tau)
    trivial = t0 <= pr.tau or pr.exposure(t0) <= 0
    crit0 = ev.count_crit(pr.n_older_detections(t0), pr.spec.alpha)
    crit = crit0 + pr.spec.crit_shift
    first = pr.s_star - pr.spec.reference_stages + 1
    is_ref = (ctx.units.old <= pr.s_star) & (ctx.units.young >= first) & np.isin(ctx.units.cls, pr.calibrated)
    w = rates[ctx.units.cls[is_ref]] * mult[is_ref]
    a_ref = float(w @ va.range_mean(path, ctx.lo[is_ref], ctx.hi[is_ref]) / w.sum())
    # the target: the true path's mean over (tau, t0], weighted by the declared exposure (true rates times
    # the declared multipliers), relative to the realised reference intensity
    abar = math.nan if trivial else pr.abar_truth(path, t0, rates[pr.calibrated]) / a_ref
    out.update(a_ref=a_ref, abar_rel=abar)
    m = members(cell)
    for K in sorted(m):
        if trivial:
            out[f"m_f_{K}"], out[f"c_f_{K}"] = -math.inf, True
            continue
        b = pr.fstar(K, t0)
        st = pr.lr(K, t0, abar)
        good = b.converged and st.converged
        contains = b.state != "finite" or b.value >= abar - TOL * (1 + abar)
        out[f"fstar_{K}"], out[f"state_{K}"] = b.value, b.state
        out[f"m_f_{K}"] = math.inf if (not good or (st.value <= crit and not contains)) else st.value - crit0
        out[f"c_f_{K}"] = bool(good and st.value <= crit and contains)
    grid = pr.grid(STEP)
    below = grid[grid <= t0 + 1e-9]
    g_below = float(below.max()) if len(below) else t0
    lag = pr.spec.h0m_lag_ma
    for K in ("H0c", "H0m", "H0"):
        if K in m:
            for f in applicable(cell, path, ctx.tau0, 1.0, None, lag if K == "H0m" else 0.0):
                out.update(_point(pr, f"o_{K}_{f:g}", K, f, t0, g_below, crit0, crit, None, trivial))
    if "H0" in m:
        for f in applicable(cell, path, ctx.tau0, 1.0, 459.1, 0.0):
            out.update(_point(pr, f"w_{f:g}", "H0", f, t0, g_below, crit0, crit, 459.1, trivial))
    out["n_fits"], out["n_failed"] = pr.n_fits, pr.n_failed
    return out


def _point(pr, key, K, f, t0, g_below, crit0, crit, start, trivial) -> dict:
    if trivial:
        return {f"m_{key}": -math.inf, f"c_{key}": True}
    st = pr.origin_stat(K, t0, f, start)
    sg = pr.origin_stat(K, g_below, f, start)
    good = st.converged and sg.converged
    cg = ev.count_crit(pr.n_older_detections(g_below), pr.spec.alpha)
    margin = max(st.value - crit0, sg.value - cg) if good else math.inf
    return {f"m_{key}": margin, f"c_{key}": bool(good and st.value <= crit and sg.value <= cg + pr.spec.crit_shift)}


_CTX: dict = {}


def _ctx(design_id: str, rho: float) -> Context:
    key = (design_id, rho)
    if key not in _CTX:
        c = Context(design_id, rho)
        ids = [d["id"] for d in c.decl["design"]]
        c.design_index, c.rho_index = ids.index(design_id), c.decl["common"]["rho"].index(rho)
        _CTX[key] = c
    return _CTX[key]


# --- driver ------------------------------------------------------------------------------------------

def cells(decl: dict, diagnostics: bool = True) -> list[dict]:
    q = decl["qualification"]
    out = [dict(c, kind="acceptance") for c in q["cells"]]
    if diagnostics:
        out += [dict(c, kind="diagnostic") for c in q["diagnostics"] + decl["amendment_1"]["diagnostics_added"]]
    return [dict(c, index=i) for i, c in enumerate(out)]


def run_cell(pool, design_id, rho, cell, root, shift, target, cap, first_rep=0) -> tuple[list[dict], int]:
    """Replicates first_rep, first_rep+1, ... until `target` pass or `cap` attempts; returns the passing rows
    (in index order, cut at target) and the attempts used."""
    passing, attempts, rep, batch = [], 0, first_rep, 256
    while len(passing) < target and attempts < cap:
        n = min(batch, cap - attempts)
        rows = pool.map(replicate, [(design_id, rho, cell, rep + i, root, shift) for i in range(n)], chunksize=4)
        for r in rows:
            attempts += 1
            if r["passed"]:
                passing.append(r)
                if len(passing) == target:
                    break
        rep += n
        batch = max(256, int(1.2 * (target - len(passing)) * attempts / max(len(passing), 1)))
    return passing, attempts


def quantities(rows: list[dict], cell: dict) -> list[str]:
    keys = sorted({k[2:] for r in rows for k in r if k.startswith("c_")})
    return keys


def summarise(rows: list[dict], cell: dict, attempts: int, target: int) -> dict:
    s = dict(cell=cell["name"], kind=cell["kind"], attempts=attempts, passes=len(rows),
             pass_rate=len(rows) / attempts if attempts else math.nan, complete=len(rows) >= target,
             errors=sum(bool(r["error"]) for r in rows))
    for q in quantities(rows, cell):
        hits = [r.get(f"c_{q}", True) and not r["error"] for r in rows]
        s[f"cover_{q}"] = sum(hits)
        margins = [math.inf if r["error"] else r.get(f"m_{q}", -math.inf) for r in rows]
        s[f"delta_{q}"] = va.shift_to_target(margins) if rows else math.nan
    return s


def code_hashes() -> dict:
    here = Path(__file__).resolve().parent
    return {p: hashlib.sha256((here / p).read_bytes()).hexdigest() for p in
            ("envelope.py", "designs.py", "m2.py", "qualify.py", "designs/m2.toml")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", required=True)
    ap.add_argument("--rho", type=float, required=True)
    ap.add_argument("--phase", choices=("calibrate", "accept", "stage2", "dev"), required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--target", type=int, default=None)
    ap.add_argument("--no-diagnostics", action="store_true")
    a = ap.parse_args()
    decl = dz.declarations()
    q = decl["qualification"]
    target = a.target or q["target_passing"]
    cap = q["max_attempts"] if a.target is None else 20 * target
    tag = f"{a.design}_rho{a.rho:g}"
    OUT.mkdir(parents=True, exist_ok=True)
    seeds = q["root_seeds"]
    shift, first_rep, todo = 0.0, 0, cells(decl, not a.no_diagnostics)
    if a.phase == "dev":
        root = 20261100
    elif a.phase == "calibrate":
        root = seeds["calibrate"]
    else:
        rec = json.loads((OUT / f"{tag}_calibrate.json").read_text())
        if rec["code"] != code_hashes():
            raise SystemExit("calibration receipt does not match the code")
        shift = rec["delta"]
        root = seeds["accept"] if a.phase == "accept" else seeds["stage2"]
        if a.phase == "stage2":
            acc = json.loads((OUT / f"{tag}_accept.json").read_text())
            if acc["code"] != code_hashes():
                raise SystemExit("acceptance receipt does not match the code")
            todo = [c for c in todo if c["name"] in acc["borderline_cells"]]
    t_start = time.time()
    summaries, reps = [], []
    with Pool(a.workers) as pool:
        for cell in todo:
            rows, attempts = run_cell(pool, a.design, a.rho, cell, root, shift, target, cap, first_rep)
            summaries.append(summarise(rows, cell, attempts, target))
            reps += rows
            print(json.dumps({k: v for k, v in summaries[-1].items() if not k.startswith("delta")}), flush=True)
    rec = dict(design=a.design, rho=a.rho, phase=a.phase, root=root, shift=shift, target=target, cap=cap,
               code=code_hashes(), python=platform.python_version(), numpy=np.__version__,
               seconds=round(time.time() - t_start, 1), cells=summaries)
    acc_cells = [s for s in summaries if s["kind"] == "acceptance"]
    if a.phase == "calibrate":
        deltas = [v for s in acc_cells for k, v in s.items() if k.startswith("delta_")]
        rec["delta"] = max(deltas) if deltas else 0.0
        rec["complete"] = all(s["complete"] for s in acc_cells)
    elif a.phase in ("accept", "stage2"):
        verdicts = {}
        for s in acc_cells:
            for k, v in s.items():
                if k.startswith("cover_"):
                    verdicts[f"{s['cell']}:{k[6:]}"] = va.stage1(v, s["passes"]) if s["complete"] else "incomplete"
        if a.phase == "stage2":
            acc = json.loads((OUT / f"{tag}_accept.json").read_text())
            first = {f"{s['cell']}:{k[6:]}": (v, s["passes"]) for s in acc["cells"] for k, v in s.items() if k.startswith("cover_")}
            now = {f"{s['cell']}:{k[6:]}": (v, s["passes"]) for s in acc_cells for k, v in s.items() if k.startswith("cover_")}
            verdicts = {}
            for key, v in acc["verdicts"].items():
                if v != "borderline":
                    verdicts[key] = v
                elif key in now and now[key][1] + first[key][1] >= 2 * target:
                    verdicts[key] = va.stage2(first[key][0] + now[key][0])
                else:
                    verdicts[key] = "incomplete"
        rec["verdicts"] = verdicts
        rec["borderline_cells"] = sorted({k.split(":")[0] for k, v in verdicts.items() if v == "borderline"})
        rec["result"] = ("pass" if all(v == "pass" for v in verdicts.values()) else
                         "fail" if any(v == "fail" for v in verdicts.values()) else
                         "incomplete" if any(v == "incomplete" for v in verdicts.values()) else "borderline")
    (OUT / f"{tag}_{a.phase}.json").write_text(json.dumps(rec, indent=1, default=float))
    buf = io.StringIO()
    keys = list(dict.fromkeys(k for r in reps for k in r))
    w = csv.DictWriter(buf, keys, lineterminator="\n")
    w.writeheader()
    w.writerows(reps)
    with gzip.open(OUT / f"{tag}_{a.phase}_reps.csv.gz", "wt") as f:
        f.write(buf.getvalue())
    print(json.dumps({k: rec[k] for k in rec if k in ("delta", "complete", "result", "seconds", "borderline_cells")}))


if __name__ == "__main__":
    main()
