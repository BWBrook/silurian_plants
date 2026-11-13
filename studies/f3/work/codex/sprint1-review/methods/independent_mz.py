import sys,json,math
import numpy as np
from scipy import optimize, special
sys.path.insert(0,'/Users/bwbrook/papers/silurian_plants/models/f3')
import qualify as q

ctx=q.Context('LY-MZ-CU',1.0)
u=ctx.units
tau=ctx.tau0
isref=ctx.hi<=tau
old=~isref
clu=u.cluster
k=2.0
nodes,weights=special.roots_genlaguerre(120,k-1)
gnodes=nodes/k
logw=np.log(weights)-special.gammaln(k)

def loglik(logr,h,intensity=1.):
    r=np.exp(logr)
    x=r*gnodes
    total=0.
    for c in np.unique(clu):
        refs=isref&(clu==c)
        ds=u.d[refs]
        ll=float(ds.sum())*np.log(-np.expm1(-x)) - float(len(ds)-ds.sum())*x
        for hh in h[clu[old]==c]:
            ll+=np.log1p(-hh*(-np.expm1(-x*intensity)))
        total+=special.logsumexp(logw+ll)
    return float(total)

def rateprofile(h,intensity=1.):
    res=optimize.minimize_scalar(lambda z:-loglik(z,h,intensity),bounds=(math.log(1e-5),math.log(8)),method='bounded',options={'xatol':1e-11})
    return -res.fun,np.exp(res.x)

alt,ar=rateprofile(np.zeros(old.sum()))
crit=5.991464547107979
def Wfor(T):
    edges=np.unique(np.r_[tau,ctx.age.base[(ctx.age.base>tau)&(ctx.age.base<T)],T])
    lo,hi=ctx.lo[old],ctx.hi[old]
    W=np.maximum(0,np.minimum(hi[:,None],edges[1:])-np.maximum(lo[:,None],edges[:-1]))/(hi-lo)[:,None]
    return W[:,W.sum(axis=0)>1e-10]

def h0prof(f,T):
    W=Wfor(T)
    a=W.sum(axis=0)/W.sum()
    starts=[np.r_[np.log(ar),np.full(W.shape[1],f)]]
    for i in range(W.shape[1]):
        x=np.full(W.shape[1],f)
        x[i]=min(1,f/a[i])
        starts.append(np.r_[np.log(ar),x])
    fits=[]
    for s in starts:
        r=optimize.minimize(lambda z:-loglik(z[0],W@z[1:]),s,method='SLSQP',bounds=[(math.log(1e-5),math.log(8))]+[(0,1)]*W.shape[1],constraints={'type':'ineq','fun':lambda z:a@z[1:]-f},options={'ftol':1e-10,'maxiter':300})
        fits.append(r)
    best=min(fits,key=lambda r:r.fun)
    return 2*(alt+best.fun)

fc=optimize.brentq(lambda f:2*(alt-rateprofile(np.ones(old.sum()),f)[0])-crit,0,1,xtol=1e-9)
fh=optimize.brentq(lambda f:h0prof(f,459.1)-crit,0,1,xtol=1e-8)
def window(T):
    h=np.maximum(0,np.minimum(ctx.hi[old],T)-np.maximum(ctx.lo[old],459.1))/(ctx.hi[old]-ctx.lo[old])
    return 2*(alt-rateprofile(h)[0])
win=optimize.brentq(lambda T:window(T)-crit,459.1,469.4,xtol=1e-8)
fpre=optimize.brentq(lambda f:2*(alt-rateprofile(np.maximum(0,ctx.hi[old]-np.maximum(ctx.lo[old],459.1))/(ctx.hi[old]-ctx.lo[old]),f)[0])-crit,0,1,xtol=1e-8)
strict=optimize.brentq(lambda f:ctx.data.lr('H0',459.1,f).value-crit,0,1,xtol=1e-9)
spec96=q.ev.Spec(**{**ctx.spec0.__dict__,'nodes':96})
pr96=q.ev.Problem(ctx.units,spec96,ctx.age)
strict96=optimize.brentq(lambda f:pr96.lr('H0',459.1,f).value-crit,0,1,xtol=1e-9)
print(json.dumps(dict(reference_counts=[dict(cluster=int(c),n=int(sum(isref&(clu==c))),det=int(sum(u.d[isref&(clu==c)]))) for c in np.unique(clu)],direct_r=ar,direct_alt=alt,H0c_far=fc,H0_459p1=fh,window_endpoint_exact=win,window_f_all_Darriwilian=fpre,engine_H0c_far=ctx.data.fstar('H0c',560).value,engine_H0_459p1=ctx.data.fstar('H0',459.1).value,engine_strict_root_48=strict,engine_strict_root_96=strict96,engine_lr_at_direct_root=ctx.data.lr('H0',459.1,fh).value),indent=2))
