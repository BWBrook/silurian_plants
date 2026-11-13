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
  w_<f>         the window read-out (H0, start = [common] window_start_ma) likewise, when a >= f on (start, t0].
A replicate whose first appearance reaches t0 makes no claim there and covers. Margins (statistic minus
the unshifted critical value; inf for a failed output) give the calibration shift, as in validate.py.
"""

import argparse
import json
import math
import platform
import time
from dataclasses import asdict
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import scipy
from scipy import stats

import designs as dz
import envelope as ev
import m2
import qualification_contract as qc
import validate as va

OUT = Path(__file__).resolve().parent / "out" / "qual"
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
        mid = lambda t: np.where(t <= ctx["start"], cell["after"], f)
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
    if h == "window":
        return {"H0m", "H0", "H1"} if cell["after"] >= cell["f"] else {"H0", "H1"}
    if h == "ramp":
        return {"H0m", "H0", "H1"}
    if h == "hide":
        return {"H0", "H1"}
    return {"H1"}


class Context:
    """The fixed design, its data fit and the truth settings shared by a cell's replicates."""

    def __init__(self, design_id: str, rho: float):
        self.decl = dz.declarations(dz.DESIGNS)
        self.design = next(d for d in self.decl["design"] if d["id"] == design_id)
        qc.require(self.design.get("qualify", True) and "primary" in self.design, "design has no binding primary variant")
        qc.require(rho in self.decl["common"]["rho"], "rho is not declared")
        p = self.design["primary"]
        self.variant = {k: p[k] for k in p if k != "min_ref_units"}
        self.min_ref, self.k = p["min_ref_units"], p["cluster_k"]
        self.rho = rho
        self.start = self.decl["common"]["window_start_ma"]
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
        self.qualification_classes = tuple(self.design.get("qualification_classes", self.spec0.classes))
        qc.require(bool(self.qualification_classes) and len(set(self.qualification_classes)) == len(self.qualification_classes)
                   and set(self.qualification_classes) <= set(self.spec0.classes), "invalid qualification class scope")
        self.step = self.decl["common"]["origin_step_ma"]
        qc.require(type(self.step) in (int, float) and math.isfinite(self.step) and self.step > 0,
                   "origin_step_ma must be finite and positive")

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
    path = path_for(cell, ctx.tau0, dict(bases=ctx.age.base, density=ctx.density(rates, mult), start=ctx.start))
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

def applicable(cell: dict, path, tau0: float, a_ref: float, start: float | None, lag: float,
               readouts) -> list[float]:
    t0 = cell["t0"]
    lo = tau0 if start is None else start
    hi = t0 - lag
    if hi <= lo:
        return []
    grid = np.linspace(lo + 1e-6, hi, 2000)
    m = float(path(grid).min()) / a_ref
    return [f for f in readouts if f <= m + 1e-9]


def expected_quantities(ctx: Context, cell: dict) -> list[str]:
    rates = ctx.rates(cell)
    mult = ctx.units.mult * np.where(ctx.transported, cell.get("rho_true_factor", 1.0), 1.0)
    path = path_for(cell, ctx.tau0, dict(bases=ctx.age.base, density=ctx.density(rates, mult), start=ctx.start))
    membership = members(cell) & set(ctx.qualification_classes)
    keys = [f"f_{K}" for K in sorted(membership)]
    for K in ("H0c", "H0m", "H0"):
        if K in membership:
            keys += [f"o_{K}_{f:g}" for f in applicable(cell, path, ctx.tau0, 1.0, None,
                     ctx.spec0.h0m_lag_ma if K == "H0m" else 0.0, ctx.spec0.readouts)]
    if "H0" in membership:
        keys += [f"w_{f:g}" for f in applicable(cell, path, ctx.tau0, 1.0, ctx.start, 0.0, ctx.spec0.readouts)]
    return sorted(keys)


def replicate(job) -> dict:
    design_id, rho, cell, rep, root, shift, reference_rates = job
    ctx = _ctx(design_id, rho)
    ctx.r_data = np.asarray(reference_rates, float)
    ss = np.random.SeedSequence(root, spawn_key=(ctx.design_index, ctx.rho_index, cell["index"], rep))
    rng = np.random.default_rng(ss)
    out = dict(cell=cell["name"], rep=rep, passed=False, error="")
    try:
        units, path, rates, mult = simulate(ctx, cell, rng)
        out["n_old_det"] = int(units.d[ctx.transported].sum())
        try:
            pot = ev.Problem(m2.potential(units, ctx.transported), ctx.spec0, ctx.age)
            ok, lr1, critical = m2.screen(pot)
            out.update(screen_status="evaluated", screen_converged=True, screen_lr=lr1, screen_crit=critical,
                       screen_n_older_detections=pot.n_older_detections(pot.spec.domain_ma[1]))
        except ev.NoFirstAppearance:
            ok = False
            out["screen_status"] = "no-first-appearance"
        if not ok:
            return out
        out["passed"] = True
        spec = ev.Spec(**{**ctx.spec0.__dict__, "crit_shift": shift})
        try:
            pr = ev.Problem(units, spec, ctx.age)
        except ev.NoFirstAppearance:
            out.update(trivial=True, abstain_reason="no-calibrated-first-appearance")
            for q in cell["quantities"]:
                out[f"c_{q}"], out[f"m_{q}"] = True, -math.inf
            return out
        out.update(_analyse(ctx, cell, pr, path, rates, mult))
    except Exception as e:  # a failure after passing stays in the denominator as a miss
        out["error"] = f"{type(e).__name__}: {e}"
        if not out["passed"]:
            out.update(screen_status="error", screen_converged=False)
        if out["passed"]:
            out["trivial"] = False
            for q in cell["quantities"]:
                out[f"c_{q}"], out[f"m_{q}"] = False, math.inf
    return out


def _analyse(ctx: Context, cell: dict, pr: ev.Problem, path, rates, mult) -> dict:
    t0 = cell["t0"]
    trivial = t0 <= pr.tau or pr.exposure(t0) <= 0
    out = dict(tau=pr.tau, trivial=trivial)
    crit0 = ev.count_crit(pr.n_older_detections(t0), pr.spec.alpha)
    crit = crit0 + pr.spec.crit_shift
    first = pr.s_star - pr.spec.reference_stages + 1
    is_ref = (ctx.units.old <= pr.s_star) & (ctx.units.young >= first) & np.isin(ctx.units.cls, pr.calibrated)
    w = rates[ctx.units.cls[is_ref]] * mult[is_ref]
    a_ref = float(w @ va.range_mean(path, ctx.lo[is_ref], ctx.hi[is_ref]) / w.sum())
    # the target: the true path's mean over (tau, t0], weighted by the declared exposure (true rates times
    # the declared multipliers), relative to the realised reference intensity
    abar = None if trivial else pr.abar_truth(path, t0, rates[pr.calibrated]) / a_ref
    out["a_ref"] = a_ref
    if abar is not None:
        out["abar_rel"] = abar
    m = members(cell) & set(ctx.qualification_classes)
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
    grid = pr.grid(ctx.step)
    below = grid[grid <= t0 + 1e-9]
    g_below = float(below.max()) if len(below) else t0
    lag = pr.spec.h0m_lag_ma
    for K in ("H0c", "H0m", "H0"):
        if K in m:
            for f in applicable(cell, path, ctx.tau0, 1.0, None, lag if K == "H0m" else 0.0, pr.spec.readouts):
                out.update(_point(pr, f"o_{K}_{f:g}", K, f, t0, g_below, crit0, crit, None, trivial))
    if "H0" in m:
        for f in applicable(cell, path, ctx.tau0, 1.0, ctx.start, 0.0, pr.spec.readouts):
            out.update(_point(pr, f"w_{f:g}", "H0", f, t0, g_below, crit0, crit, ctx.start, trivial))
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
    amendments = [decl[k] for k in sorted((k for k in decl if k.startswith("amendment_")),
                                         key=lambda k: int(k.removeprefix("amendment_")))]
    added = [c for amendment in amendments for c in amendment.get("cells_added", [])]
    out = [dict(c, kind="acceptance") for c in q["cells"] + added]
    if diagnostics:
        added = [c for amendment in amendments for c in amendment.get("diagnostics_added", [])]
        out += [dict(c, kind="diagnostic") for c in q["diagnostics"] + added]
    return [dict(c, index=i) for i, c in enumerate(out)]


def run_cell(pool, design_id, rho, cell, root, shift, target, cap, reference_rates, first_rep=0) -> tuple[list[dict], int]:
    """Return every consumed attempt in index order, stopping at the target pass or attempt cap."""
    consumed, passing, attempts, rep, batch = [], 0, 0, first_rep, 256
    while passing < target and attempts < cap:
        n = min(batch, cap - attempts)
        rows = pool.map(replicate, [(design_id, rho, cell, rep + i, root, shift, reference_rates) for i in range(n)], chunksize=4)
        for r in rows:
            attempts += 1
            consumed.append(r)
            if r["passed"]:
                passing += 1
                if passing == target:
                    break
        rep += n
        batch = max(256, int(1.2 * (target - passing) * attempts / max(passing, 1)))
    return consumed, attempts


def resolve(cell: dict, ctx: "Context") -> dict:
    """Boundary cells (amendment 2): the truth's f is the data's own reported f* at shift 0."""
    if "f_data" not in cell:
        return cell
    data = cell["f_data"]
    qc.require(isinstance(data, dict) and set(data) == {"class", "at"}, "f_data needs an explicit class and age")
    K = data["class"]
    T = ctx.decl["common"]["domain_ma"] if data["at"] == "domain" else data["at"]
    qc.require(K in ctx.spec0.classes and type(T) in (int, float) and math.isfinite(T)
               and ctx.tau0 < T <= ctx.decl["common"]["domain_ma"], "invalid boundary-class age")
    b = ctx.data.fstar(K, T)
    qc.require(b.converged and math.isfinite(b.value) and b.value >= 0, "boundary fit did not converge to a usable intensity")
    return dict(cell, f=float(min(b.value, 1.0)))


def bound_paths(design_id: str) -> dict[str, Path]:
    here = Path(__file__).resolve().parent
    paths = {f"models/f3/{p}": here / p for p in
             ("envelope.py", "designs.py", "m2.py", "qualify.py", "qualification_contract.py", "validate.py", "sim.py", "units_sim.py")}
    paths["active_declaration"] = dz.DESIGNS.resolve()
    paths["data/timescale.csv"] = ev.sim.TIMESCALE_CSV
    if design_id.startswith("LY-"):
        source_tables = ("libya_appendix1.csv", "libya_chart_reports.csv", "libya_prose_support.csv")
    elif design_id == "QB-CO":
        source_tables = ("qusaiba_inventory.csv", "outcomes.csv", "borenshult_ages.csv")
    else:
        raise qc.EvidenceError(f"no source-input contract for {design_id}")
    for name in source_tables + ("source_files.csv", "reporting-rule.md"):
        paths[f"data/units/{name}"] = dz.UNITS / name
    return paths


def capture(paths: dict[str, Path]) -> dict:
    out = {}
    for name, path in paths.items():
        before = path.stat()
        sha = qc.file_hash(path)
        after = path.stat()
        qc.require((before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), f"input changed while hashing: {name}")
        out[name] = (sha, after.st_size, after.st_mtime_ns)
    return out


def build_binding(design_id: str, rho: float) -> tuple[Context, dict, dict]:
    paths = bound_paths(design_id)
    before = capture(paths)
    ctx = Context(design_id, rho)
    grid = [resolve(c, ctx) for c in cells(ctx.decl)]
    qc.require(len({c["name"] for c in grid}) == len(grid), "qualification cell names are not unique")
    for c in grid:
        c["quantities"] = expected_quantities(ctx, c)
    binding = dict(design=design_id, rho=rho, declaration_id=ctx.decl["freeze"]["id"],
                   files={name: state[0] for name, state in before.items()},
                   generated_units=asdict(ctx.built), specification=asdict(ctx.spec0),
                   age_bases=ctx.age.base.tolist(), fitted_reference_rates=ctx.r_data.tolist(),
                   origin_step_ma=ctx.step, qualification_classes=list(ctx.qualification_classes),
                   runtime_contract=dict(python=".".join(platform.python_version_tuple()[:2]),
                                         numpy=np.__version__, scipy=scipy.__version__),
                   derived_tolerance=qc.DERIVED_TOLERANCE, protocol=qc.protocol(ctx.decl), grid=grid)
    qc.require(capture(paths) == before, "qualification inputs changed while the design was built")
    return ctx, binding, before


def load_qualification(design_id: str, rho: float, directory: Path) -> tuple[float | None, str, str, dict]:
    """Validate the whole evidence chain before attaching a qualification to current empirical outputs."""
    ctx, binding, before = build_binding(design_id, rho)
    cal_path, _ = qc.paths(directory, binding, "calibrate")
    if not cal_path.exists():
        return None, "not qualified", "", binding
    potential = m2.problem(ctx.built, ctx.decl, rho, ctx.k, ctx.min_ref, screened=True)
    qc.require(m2.screen(potential)[0], "primary data do not pass the current frame-potential screen")
    cal = qc.load(directory, binding, "calibrate")
    qc.require(cal.record["complete"], "calibration is incomplete; no empirical shift can be attached")
    delta = qc.finite_shift(cal.record["delta"], "calibration delta")
    accepted_path, _ = qc.paths(directory, binding, "accept")
    final, status = cal, "calibrated only"
    if accepted_path.exists():
        final = qc.load(directory, binding, "accept")
        status = final.record["result"]
        stage2_path, _ = qc.paths(directory, binding, "stage2")
        if stage2_path.exists():
            final = qc.load(directory, binding, "stage2")
            status = final.record["result"]
    qc.require(capture(bound_paths(design_id)) == before, "qualification inputs changed while evidence was checked")
    return delta, status, final.sha256, qc.restored(final.record["binding"])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--design", required=True)
    ap.add_argument("--rho", type=float, required=True)
    ap.add_argument("--phase", choices=("calibrate", "accept", "stage2", "dev"), required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--target", type=int, default=None)
    ap.add_argument("--no-diagnostics", action="store_true")
    ap.add_argument("--out-dir", type=Path, default=OUT)
    a = ap.parse_args(argv)
    if a.phase != "dev" and (a.target is not None or a.no_diagnostics):
        ap.error("--target and --no-diagnostics are development-only options")
    if a.workers < 1 or (a.target is not None and a.target < 1):
        ap.error("workers and development target must be positive")
    _CTX.clear()
    ctx, binding, before = build_binding(a.design, a.rho)
    if a.phase != "dev":
        potential = m2.problem(ctx.built, ctx.decl, a.rho, ctx.k, ctx.min_ref, screened=True)
        qc.require(m2.screen(potential)[0], "primary data do not pass the current frame-potential screen")
    _CTX[(a.design, a.rho)] = ctx
    ctx.design_index = [d["id"] for d in ctx.decl["design"]].index(a.design)
    ctx.rho_index = ctx.decl["common"]["rho"].index(a.rho)
    p = binding["protocol"]
    target = a.target if a.target is not None else p["target_passing"]
    cap = 20 * target if a.phase == "dev" else p["max_attempts"]
    path, reps_path = qc.paths(a.out_dir, binding, a.phase)
    qc.require(not path.exists() and not reps_path.exists(), "output already exists; select a fresh --out-dir")
    shift, dependencies, first = 0.0, {}, None
    if a.phase == "dev":
        root = 20261100
    else:
        root = p["root_seeds"][a.phase]
        if a.phase != "calibrate":
            cal = qc.load(a.out_dir, binding, "calibrate")
            qc.require(cal.record["complete"], "calibration is incomplete")
            shift = qc.finite_shift(cal.record["delta"], "calibration delta")
            binding = qc.restored(cal.record["binding"])
            ctx.r_data = np.asarray(binding["fitted_reference_rates"], float)
            dependencies["calibrate"] = cal.sha256
            if a.phase == "stage2":
                accepted = qc.load(a.out_dir, binding, "accept")
                first = accepted.record
                dependencies["accept"] = accepted.sha256
    todo = qc.phase_cells(binding, a.phase, first, not a.no_diagnostics)
    t_start = time.time()
    reps = []
    with Pool(a.workers) as pool:
        for cell in todo:
            rows, attempts = run_cell(pool, a.design, a.rho, cell, root, shift, target, cap, ctx.r_data.tolist())
            summary = qc.summarise(rows, cell, target, cap, shift, p["calibration_target"])
            reps += rows
            print(json.dumps({k: v for k, v in summary.items() if not k.startswith("delta")}), flush=True)
    qc.require(capture(bound_paths(a.design)) == before, "qualification inputs changed during the run; outputs were not sealed")
    written = qc.write(a.out_dir, binding, a.phase, reps, root, target, cap, shift, dependencies,
                       dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
                            platform=platform.platform()), round(time.time() - t_start, 1), first, not a.no_diagnostics)
    if a.phase != "dev":
        qc.load(a.out_dir, binding, a.phase)
    print(json.dumps({k: v for k, v in written.record.items() if k in
                      ("delta", "complete", "result", "seconds", "borderline_cells", "payload_sha256")}))


if __name__ == "__main__":
    main()
