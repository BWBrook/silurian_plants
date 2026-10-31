import sys, csv, gzip, collections, json
from pathlib import Path
import numpy as np

sys.path.insert(0, '/Users/bwbrook/papers/silurian_plants/models/f3')
import qualify as q

def applicable(cell,path,tau,a_ref,start,lag):
    lo=tau if start is None else start
    hi=cell['t0']-lag
    if hi<=lo:return []
    floor=float(path(np.linspace(lo+1e-6,hi,2000)).min())/a_ref
    return [f for f in (1.,.1,.01) if f<=floor+1e-9]

out = []
for fn in sorted(q.OUT.glob('*_accept_reps.csv.gz')):
    tag = fn.name.removesuffix('_accept_reps.csv.gz')
    design, rho = tag.rsplit('_rho', 1)
    ctx = q.Context(design, float(rho))
    cells = {c['name']: q.resolve(c, ctx) for c in q.cells(ctx.decl, False)}
    rows = list(csv.DictReader(gzip.open(fn, 'rt')))
    grouped = collections.Counter((r['cell'], r.get('tau'), r.get('a_ref'), r.get('trivial')) for r in rows)
    counts = collections.Counter()
    examples = []
    for (name, tau, aref, trivial), n in grouped.items():
        if trivial == 'True' or not tau or not aref:
            continue
        cell = cells[name]
        path = q.path_for(cell, ctx.tau0, dict(bases=ctx.age.base, density=ctx.density(ctx.rates(cell), ctx.units.mult), start=ctx.start))
        tau, aref = float(tau), float(aref)
        t0 = cell['t0']
        grid = np.linspace(tau+1e-6, t0-1e-6, 20000)
        vals = path(grid)/aref
        mem = q.members(cell)
        if 'H0c' in mem and np.ptp(vals)>1e-6:
            counts['nonconstant_h0c'] += n
            examples.append(dict(cell=name,tau=tau,n=n,min=float(vals.min()),max=float(vals.max())))
        if 'H0' in mem and vals.max()>1+1e-6:
            counts['outside_h0_ceiling'] += n
        if 'H0m' in mem and np.diff(vals).max()>1e-6:
            counts['nonmonotone_h0m'] += n
        if 'H1' in mem and vals.max()>3+1e-6:
            counts['outside_h1_ceiling'] += n
        for K in ('H0c','H0m','H0'):
            if K not in mem: continue
            lag = ctx.spec0.h0m_lag_ma if K=='H0m' else 0
            original = applicable(cell,path,ctx.tau0,1,None,lag)
            normalised = applicable(cell,path,ctx.tau0,aref,None,lag)
            if original != normalised:
                counts['origin_normalisation_thresholds_changed'] += n
            corrected = applicable(cell,path,tau,aref,None,lag)
            if original != corrected:
                counts['origin_thresholds_changed'] += n
                examples.append(dict(cell=name,K=K,tau=tau,n=n,original=original,corrected=corrected))
        if 'H0' in mem:
            original = applicable(cell,path,ctx.tau0,1,ctx.start,0)
            corrected = applicable(cell,path,tau,aref,ctx.start,0)
            if original != corrected:
                counts['window_thresholds_changed'] += n
    out.append(dict(tag=tag,counts=dict(counts),examples=examples))
print(json.dumps(out,indent=2))
