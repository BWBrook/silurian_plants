"""Independent audit of the frozen M2 qualification ledgers; imports no F3 code."""

import argparse
import csv
import gzip
import hashlib
import io
import json
import math
import re
import subprocess
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

from scipy.stats import beta, chi2

SCHEMA = 'f3-real-qualification-v1'
EXPECTED_TAGS = {f'LY-{d}-CU_rho{r}' for d in ('H2', 'D1', 'I3') for r in ('1', '0.5', '0.25')}
EXPECTED_TAGS |= {f'LY-MZ-CU_rho{r}' for r in ('1', '0.5', '0.25', '0.1')} | {'QB-CO_rho1'}
SOURCE_CODE = ('envelope.py', 'designs.py', 'm2.py', 'qualify.py', 'qualification_contract.py',
               'validate.py', 'sim.py', 'units_sim.py')
PATTERN = re.compile(r'(.+)_(calibrate|accept|stage2|dev)\.json$')


class AuditFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise AuditFailure(message)


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        return {'nonfinite': 'nan' if math.isnan(value) else 'inf' if value > 0 else '-inf'}
    return value


def decoded(value):
    if isinstance(value, dict):
        if set(value) == {'nonfinite'}:
            return {'nan': math.nan, 'inf': math.inf, '-inf': -math.inf}[value['nonfinite']]
        return {k: decoded(v) for k, v in value.items()}
    if isinstance(value, list):
        return [decoded(v) for v in value]
    return value


def canonical(value):
    return json.dumps(clean(value), sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def same(a, b, label):
    require(canonical(a) == canonical(b), f'{label}: mismatch')


def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, f'duplicate JSON key {k}')
        result[k] = v
    return result


def number(value, label, infinite=False):
    require(type(value) in (int, float) and not math.isnan(value)
            and (infinite or math.isfinite(value)), f'{label}: invalid number')
    return float(value)


def csv_bool(value, label):
    require(value in ('True', 'False'), f'{label}: not a strict Boolean')
    return value == 'True'


def csv_float(value, label, infinite=False):
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise AuditFailure(f'{label}: invalid numeric text {value!r}')
    return number(result, label, infinite)


def count_critical(n):
    upper_mean = float(chi2.ppf(.95, 2 * (n + 1))) / 2
    return 2 * (upper_mean - n + (n * math.log(n / upper_mean) if n else 0))


def verdict1(k, n):
    lower = 0. if k == 0 else float(beta.ppf(.05, k, n-k+1))
    upper = 1. if k == n else float(beta.ppf(.95, k+1, n-k))
    return 'pass' if lower > .93 else 'fail' if upper < .93 else 'borderline'


def quantile_shift(values):
    if not values:
        return math.inf
    return max(0., sorted(values)[math.ceil(.955 * len(values)) - 1])


class Auditor:
    def __init__(self, directory, repository, revision):
        self.directory, self.repository, self.revision = directory, repository, revision
        self.blobs, self.records, self.details, self.quantity_rows = {}, {}, [], []
        self.geometry_cache, self.target_cache, self.target_stats = {}, {}, {}
        self.decl = tomllib.loads(self.blob('models/f3/designs/m2.toml').decode())
        self.designs = {d['id']: d for d in self.decl['design']}
        self.frozen_grid = []
        for c in self.decl['qualification']['cells']:
            self.frozen_grid.append(dict(c, kind='acceptance'))
        amendments = sorted((k for k in self.decl if re.fullmatch(r'amendment_\d+', k)),
                            key=lambda k: int(k.split('_')[-1]))
        for key in amendments:
            self.frozen_grid += [dict(c, kind='acceptance') for c in self.decl[key].get('cells_added', [])]
        self.frozen_grid += [dict(c, kind='diagnostic') for c in self.decl['qualification']['diagnostics']]
        for key in amendments:
            self.frozen_grid += [dict(c, kind='diagnostic') for c in self.decl[key].get('diagnostics_added', [])]
        self.frozen_grid = [dict(c, index=i) for i, c in enumerate(self.frozen_grid)]
        require(len(self.frozen_grid) == 15 and sum(c['kind']=='acceptance' for c in self.frozen_grid)==12,
                'this auditor expects the final 15-cell frozen grid')

    def blob(self, path):
        if path not in self.blobs:
            self.blobs[path] = subprocess.check_output(
                ['git', '-C', str(self.repository), 'show', f'{self.revision}:{path}'])
        return self.blobs[path]

    def geometry(self, cell, binding):
        key=(id(binding),cell['name'])
        if key in self.geometry_cache:return self.geometry_cache[key]
        raw=decoded(binding);rows=raw['generated_units']['rows'];bases=raw['age_bases']
        tau=bases[max(r['old'] for r in rows if r['d']==1)]
        classes=sorted({r['rate_class'] or r['cls_name'] for r in rows})
        rates=list(raw['fitted_reference_rates'])
        indices=[classes.index(r['rate_class'] or r['cls_name']) for r in rows]
        if cell.get('reference_p')=='lower-95':
            for c in range(len(classes)):
                refs=[r for i,r in enumerate(rows) if indices[i]==c and not r['transported']]
                n=len(refs);k=sum(r['d'] for r in refs)
                lower=0. if k==0 else float(beta.ppf(.05,k,n-k+1))
                rates[c]=-math.log1p(-lower)
        lo=[bases[r['young']-1] if math.isnan(r['lo_ma']) else r['lo_ma'] for r in rows]
        hi=[bases[r['old']] if math.isnan(r['hi_ma']) else r['hi_ma'] for r in rows]
        declared=[binding['rho'] if r['transported'] else 1. for r in rows]
        truth=[m*(cell.get('rho_true_factor',1.) if r['transported'] else 1.) for r,m in zip(rows,declared)]
        t0=cell['t0'];f=cell.get('f',1.);history=cell['history'];start=self.decl['common']['window_start_ma']
        intervals=[]
        if history=='H0c':intervals=[(tau,t0,f)]
        elif history=='window':intervals=[(tau,min(t0,start),cell['after']),(max(tau,start),t0,f)]
        elif history in {'hide','hide_h1'}:
            height=cell.get('pulse',1.) if history=='hide_h1' else 1.
            edges=sorted({tau,t0,*[b for b in bases if tau<b<t0]})
            density=[]
            for left,right in zip(edges[:-1],edges[1:]):
                mass=sum(rates[c]*mult*max(0.,min(b,right)-max(a,left))/(b-a)
                         for a,b,c,mult in zip(lo,hi,indices,truth))
                density.append((mass/(right-left),left,right))
            need=f*(t0-tau)/height
            for _,left,right in sorted(density,key=lambda item:item[0]):
                take=min(right-left,need)
                if take<=0:break
                intervals.append((right-take,right,height));need-=take
        def integral(left,right):
            if right<=left:return 0.
            mass=max(0.,min(right,tau)-left)
            a,b=max(left,tau),min(right,t0)
            if b>a:
                if history=='ramp':mass+=(b-a)*((t0-a)+(t0-b))/(2*(t0-tau))
                else:mass+=sum(v*max(0.,min(b,y)-max(a,x)) for x,y,v in intervals)
            return mass
        result=dict(rows=rows,bases=bases,tau=tau,classes=classes,rates=rates,indices=indices,
                    lo=lo,hi=hi,declared=declared,truth=truth,intervals=intervals,integral=integral)
        self.geometry_cache[key]=result
        return result

    def check_targets(self,row,cell,binding):
        if row['error'] or not row.get('tau'):return
        tau=csv_float(row['tau'],'selected tau');key=(id(binding),cell['name'],tau)
        if key not in self.target_cache:
            g=self.geometry(cell,binding);rows=g['rows'];bases=g['bases'];indices=g['indices']
            require(tau in bases,'selected tau is not a declared stage boundary')
            stage=bases.index(tau);first=stage-binding['specification']['reference_stages']+1
            ref=[i for i,r in enumerate(rows) if r['old']<=stage and r['young']>=first]
            counts={c:sum(indices[i]==c for i in ref) for c in set(indices)}
            calibrated={c for c,n in counts.items() if n>=binding['specification']['min_units_per_class']}
            require(calibrated,'scored analysis has no calibrated reference class')
            ref=[i for i in ref if indices[i] in calibrated]
            weights=[g['rates'][indices[i]]*g['truth'][i] for i in ref]
            aref=sum(w*g['integral'](g['lo'][i],g['hi'][i])/(g['hi'][i]-g['lo'][i]) for i,w in zip(ref,weights))/sum(weights)
            mass=exposure=0.
            for i,r in enumerate(rows):
                if r['old']<=stage or indices[i] not in calibrated:continue
                left,right=max(g['lo'][i],tau),min(g['hi'][i],cell['t0'])
                if right<=left:continue
                weight=g['rates'][indices[i]]*g['declared'][i]/(g['hi'][i]-g['lo'][i])
                mass+=weight*g['integral'](left,right);exposure+=weight*(right-left)
            trivial=cell['t0']<=tau or exposure<=0
            abar=None if trivial else mass/exposure/aref
            self.target_cache[key]=(aref,abar,trivial)
        aref,abar,trivial=self.target_cache[key]
        same(csv_bool(row.get('trivial'),'trivial'),trivial,'analysis abstention target')
        observed=csv_float(row.get('a_ref'),'a_ref');err=abs(observed-aref)
        require(err<=.002*(1+abs(aref)),f'{cell["name"]}: reference target differs from exact path integral')
        stats=self.target_stats.setdefault(id(binding),dict(rows_checked=0,max_reference_difference=0.,max_abar_difference=0.))
        stats['rows_checked']+=1;stats['max_reference_difference']=max(stats['max_reference_difference'],err)
        if abar is not None:
            err=abs(csv_float(row.get('abar_rel'),'abar_rel')-abar)
            require(err<=.002*(1+abs(abar)),f'{cell["name"]}: mean target differs from exact path integral')
            stats['max_abar_difference']=max(stats['max_abar_difference'],err)

    def expected_quantities(self, cell, binding):
        raw = decoded(binding)
        rows, bases = raw['generated_units']['rows'], raw['age_bases']
        tau = bases[max(r['old'] for r in rows if r['d'] == 1)]
        start, lag, readouts = (self.decl['common'][k] for k in ('window_start_ma', 'h0m_lag_ma', 'readouts'))
        t0, history, f = cell['t0'], cell['history'], cell.get('f', 1.)
        if history == 'H0c':
            members = {'H0c','H0m','H0','H1'} if f <= 1 else {'H1'}
        elif history == 'ramp':
            members = {'H0m','H0','H1'}
        elif history == 'window':
            members = {'H0','H1'} | ({'H0m'} if cell['after'] >= f else set())
        elif history == 'hide':
            members = {'H0','H1'}
        elif history == 'hide_h1':
            members = {'H1'}
        else:
            raise AuditFailure(f'unknown history {history}')
        members &= set(binding['qualification_classes'])
        pulses = []
        if history in {'hide','hide_h1'}:
            height = cell.get('pulse',1.) if history == 'hide_h1' else 1.
            edges = sorted({tau,t0,*[b for b in bases if tau<b<t0]})
            classes = sorted({r['rate_class'] or r['cls_name'] for r in rows})
            rates = raw['fitted_reference_rates']
            pieces = []
            for lo,hi in zip(edges[:-1],edges[1:]):
                mass=0.
                for r in rows:
                    rl = bases[r['young']-1] if math.isnan(r['lo_ma']) else r['lo_ma']
                    rh = bases[r['old']] if math.isnan(r['hi_ma']) else r['hi_ma']
                    rate=rates[classes.index(r['rate_class'] or r['cls_name'])]
                    multiplier=binding['rho'] if r['transported'] else 1.
                    mass += rate*multiplier*max(0.,min(rh,hi)-max(rl,lo))/(rh-rl)
                pieces.append((mass/(hi-lo),lo,hi))
            needed=f*(t0-tau)/height
            for _,lo,hi in sorted(pieces,key=lambda x:x[0]):
                take=min(hi-lo,needed)
                if take<=0:break
                pulses.append((hi-take,hi))
                needed-=take
        def floor(lo,hi):
            if hi<=lo:return None
            if history=='H0c':return f
            if history=='ramp':return (t0-hi)/(t0-tau)
            if history=='window':
                vals=[]
                if lo<start:vals.append(cell['after'])
                if hi>start:vals.append(f)
                return min(vals)
            covered=sum(max(0.,min(hi,b)-max(lo,a)) for a,b in pulses)
            return height if covered>=hi-lo-1e-10 else 0.
        keys={f'f_{k}' for k in members}
        for k in {'H0c','H0m','H0'} & members:
            m=floor(tau,t0-(lag if k=='H0m' else 0.))
            keys.update(f'o_{k}_{v:g}' for v in readouts if m is not None and v<=m+1e-9)
        if 'H0' in members:
            m=floor(start,t0)
            keys.update(f'w_{v:g}' for v in readouts if m is not None and v<=m+1e-9)
        require(keys, f'{cell["name"]}: empty expected quantity roster')
        return sorted(keys)

    def check_binding(self,b):
        design=self.designs.get(b['design'])
        require(design is not None and design.get('qualify',True), 'unknown or nonqualifying design')
        require(b['rho'] in self.decl['common']['rho'], 'undeclared rho')
        same(b['declaration_id'],self.decl['freeze']['id'],'declaration id')
        classes=design.get('qualification_classes',self.decl['common']['classes'])
        same(b['qualification_classes'],classes,'qualification classes')
        same(b['origin_step_ma'],self.decl['common']['origin_step_ma'],'origin step')
        common=self.decl['common'];primary=design['primary']
        expected_spec=dict(reference_stages=common['reference_stages'],min_units_per_class=primary['min_ref_units'],
            domain_ma=[0.,common['domain_ma']],classes=common['classes'],h1_ceiling=common['h1_ceiling'],
            h0m_lag_ma=common['h0m_lag_ma'],alpha=common['alpha'],readouts=common['readouts'],
            cluster_shape_k=primary['cluster_k'],crit_shift=0.,age_scenario='chart',nodes=common['nodes'],fa_rule='oldest-possible')
        same(b['specification'],expected_spec,'analysis specification')
        same(b['generated_units']['design'],b['design'],'generated design')
        same(b['generated_units']['variant'],{k:v for k,v in primary.items() if k!='min_ref_units'},'primary variant')
        timescale=list(csv.DictReader(io.StringIO(self.blob('data/timescale.csv').decode())))
        same(b['age_bases'],[float(r['base_ma']) for r in timescale],'age boundaries')
        same(b['runtime_contract'],dict(python='3.12',numpy='2.3.4',scipy='1.16.3'),'pinned runtime')
        same(b['derived_tolerance'],dict(absolute=1e-8,relative=1e-8),'derived tolerance')
        paths={f'models/f3/{p}':f'models/f3/{p}' for p in SOURCE_CODE}
        paths.update(active_declaration='models/f3/designs/m2.toml')
        paths['data/timescale.csv']='data/timescale.csv'
        source=('libya_appendix1.csv','libya_chart_reports.csv','libya_prose_support.csv') if b['design'].startswith('LY-') else ('qusaiba_inventory.csv','outcomes.csv','borenshult_ages.csv')
        for p in (*source,'source_files.csv','reporting-rule.md'):paths[f'data/units/{p}']=f'data/units/{p}'
        same(sorted(b['files']),sorted(paths),'bound file roster')
        for key,path in paths.items():same(b['files'][key],sha(self.blob(path)),f'frozen source {path}')
        expected_protocol=dict(target_passing=1000,max_attempts=20000,calibration_target=.955,
            root_seeds=self.decl['qualification']['root_seeds'],stage1_n=1000,stage2_n=1000,
            floor=.93,stage2_pass=1886,first_rep=0,
            criterion='marginal false-claim frequency among screen-passing replicates; abstentions are non-errors')
        same(b['protocol'],expected_protocol,'protocol')
        same(len(b['grid']),len(self.frozen_grid),'grid length')
        for actual,declared in zip(b['grid'],self.frozen_grid):
            extra={'quantities'}|({'f'} if 'f_data' in declared else set())
            same({k:v for k,v in actual.items() if k not in extra},declared,f'{declared["name"]}: frozen truth')
            if 'f_data' in declared:require(0<=number(actual.get('f'),'resolved boundary f')<=1,'boundary f outside [0,1]')
            same(actual['quantities'],self.expected_quantities(actual,b),f'{declared["name"]}: quantity roster')

    def cell_summary(self,rows,cell,target,cap,shift,binding):
        label=cell['name'];qs=cell['quantities'];passing=[];pre_errors=0
        require(0<len(rows)<=cap,f'{label}: invalid attempts')
        for expected_i,r in enumerate(rows):
            require(r['rep']==str(expected_i),f'{label}: nonsequential replicate id')
            require(r['cell']==label,f'{label}: wrong cell')
            passed=csv_bool(r.get('passed'),f'{label}/{expected_i}: passed')
            error=r.get('error');require(isinstance(error,str),f'{label}: missing error field')
            status=r.get('screen_status')
            if status=='evaluated':
                require(csv_bool(r.get('screen_converged'),'screen_converged'),'unconverged screen')
                require(r.get('screen_n_older_detections')=='0','oldest-possible screen has older detections')
                lr=csv_float(r.get('screen_lr'),'screen_lr');crit=csv_float(r.get('screen_crit'),'screen_crit')
                require(lr>=0 and abs(crit-count_critical(0))<1e-12,'invalid screen statistic or critical value')
                require(passed==(lr>crit),'screen decision contradicts statistic')
            else:
                require(not passed and status in {'error','no-first-appearance'},'invalid screen exclusion')
                require(bool(error)==(status=='error'),'screen error/status mismatch')
            ckeys={k[2:] for k,v in r.items() if k.startswith('c_') and v!=''}
            mkeys={k[2:] for k,v in r.items() if k.startswith('m_') and v!=''}
            if not passed:
                require(not ckeys and not mkeys and not r.get('trivial'),'unpassed attempt has scored outputs')
                pre_errors+=bool(error);continue
            require(ckeys==mkeys==set(qs),'missing or extra required quantity')
            trivial=csv_bool(r.get('trivial'),'trivial')
            self.check_targets(r,cell,binding)
            record=dict(error=error,trivial=trivial,cover={},margin={})
            for quantity in qs:
                hit=csv_bool(r[f'c_{quantity}'],quantity)
                margin=csv_float(r[f'm_{quantity}'],quantity,True)
                if error:require(not hit and margin==math.inf and not trivial,'failed analysis escaped denominator')
                elif trivial:require(hit and margin==-math.inf,'invalid abstention')
                else:
                    require((hit and margin<=shift+1e-12) or (not hit and margin>=shift-1e-12),'coverage/margin contradiction')
                    if quantity.startswith('f_'):
                        klass=quantity[2:];value=csv_float(r.get(f'fstar_{klass}'),'fstar')
                        state=r.get(f'state_{klass}');ceiling=3. if klass=='H1' else 1.
                        require(state in {'finite','ceiling-limited'} and 0<=value<=ceiling+1e-8,'invalid fstar state/value')
                        if state=='ceiling-limited':require(abs(value-ceiling)<1e-8,'wrong ceiling-limited value')
                        abar=csv_float(r.get('abar_rel'),'abar_rel')
                        if hit:require(state!='finite' or value>=abar-.002*(1+abar),'covered delivered bound omits its target')
                record['cover'][quantity]=hit;record['margin'][quantity]=margin
            passing.append(record)
        n=len(passing);require(n<=target,'too many passing records')
        reached=n==target
        require((reached and rows[-1]['passed']=='True') or (not reached and len(rows)==cap),'premature stopping')
        result=dict(cell=label,kind=cell['kind'],attempts=len(rows),passes=n,pass_rate=n/len(rows),
                    complete=reached and pre_errors==0,errors=sum(bool(r['error']) for r in passing),errors_before_screen=pre_errors)
        claim_rows=[r for r in passing if r['error'] or not r['trivial']]
        for quantity in qs:
            result[f'cover_{quantity}']=sum(r['cover'][quantity] for r in passing)
            result[f'claims_{quantity}']=len(claim_rows)
            result[f'claimmiss_{quantity}']=sum(not r['cover'][quantity] for r in claim_rows)
            result[f'delta_{quantity}']=quantile_shift([r['margin'][quantity] for r in passing])
        return result

    def audit(self,path):
        name=path.name
        if name in self.records:return self.records[name]
        payload=path.read_bytes();record=json.loads(payload,object_pairs_hook=unique_pairs,
            parse_constant=lambda v:(_ for _ in ()).throw(AuditFailure(f'invalid JSON constant {v}')))
        require(record.get('schema')==SCHEMA,'unsupported receipt schema')
        same(record.get('payload_sha256'),sha(canonical({k:v for k,v in record.items() if k!='payload_sha256'})),'payload hash')
        b=record['binding'];self.check_binding(b)
        same(record['binding_sha256'],sha(canonical(b)),'binding hash')
        phase=record['phase'];tag=f'{b["design"]}_rho{b["rho"]:g}'
        same(name,f'{tag}_{phase}.json','receipt filename')
        require(phase in {'calibrate','accept','stage2','dev'},'unknown phase')
        require(phase=='dev' or tag in EXPECTED_TAGS,'binding evidence for an unselected primary design/rho')
        target,cap=record['target'],record['cap']
        require(type(target) is int and type(cap) is int,'noninteger protocol counts')
        if phase=='dev':
            require(target>0 and cap==20*target and record['root']==20261100,'invalid development protocol')
        else:
            same((target,cap),(1000,20000),'binding target/cap')
            same(record['root'],b['protocol']['root_seeds'][phase],'phase seed')
        shift=number(record['shift'],'critical shift');require(shift>=0,'negative shift')
        deps={};first=None
        if phase in {'accept','stage2'}:
            cal=self.audit(path.with_name(f'{tag}_calibrate.json'))
            require(cal['reconstructed']['complete'],'incomplete calibration attached')
            same(shift,cal['reconstructed']['delta'],'calibrated shift')
            same(record['binding_sha256'],cal['record']['binding_sha256'],'exact calibrated truth')
            deps['calibrate']=cal['file_sha256']
            if phase=='stage2':
                first=self.audit(path.with_name(f'{tag}_accept.json'))
                deps['accept']=first['file_sha256']
                require(first['reconstructed']['complete'] and first['reconstructed']['borderline_cells'],'stage2 without complete borderline stage1')
        else:same(shift,0.,'initial shift')
        same(record['dependencies'],deps,'receipt dependencies')
        rep_name=f'{tag}_{phase}_reps.csv.gz';same(record['replicates']['file'],rep_name,'replicate filename')
        rep_bytes=path.with_name(rep_name).read_bytes();same(sha(rep_bytes),record['replicates']['sha256'],'replicate hash')
        reader=csv.DictReader(io.StringIO(gzip.decompress(rep_bytes).decode()))
        fields=reader.fieldnames or [];require(len(fields)==len(set(fields)),'duplicate CSV columns')
        require({'cell','rep','passed','error'}<=set(fields),'missing CSV identity fields')
        grouped=defaultdict(list)
        for row in reader:
            require(None not in row and all(v is not None for v in row.values()),'malformed CSV row')
            grouped[row['cell']].append(row)
        grid=b['grid']
        if phase=='accept':grid=[c for c in grid if c['kind']=='acceptance']
        elif phase=='stage2':grid=[c for c in grid if c['name'] in first['reconstructed']['borderline_cells']]
        elif phase=='dev' and set(grouped)=={c['name'] for c in grid if c['kind']=='acceptance'}:
            grid=[c for c in grid if c['kind']=='acceptance']
        require(grid and set(grouped)=={c['name'] for c in grid},'missing or unexpected cell evidence')
        summaries=[self.cell_summary(grouped[c['name']],c,target,cap,shift,b) for c in grid]
        acceptance=[s for s in summaries if s['kind']=='acceptance']
        require(acceptance,'vacuous acceptance grid')
        complete=all(s['complete'] for s in acceptance) and not any(s['errors_before_screen'] for s in summaries)
        rebuilt=dict(cells=summaries,complete=complete)
        counts={f'{s["cell"]}:{key[6:]}':(value,s['passes'],s['complete']) for s in acceptance for key,value in s.items() if key.startswith('cover_')}
        if phase=='calibrate':
            delta=max(v for s in acceptance for k,v in s.items() if k.startswith('delta_'))
            rebuilt['delta']=delta if complete and math.isfinite(delta) else None
            rebuilt['complete']=complete and rebuilt['delta'] is not None
        elif phase in {'accept','stage2'}:
            if phase=='accept':verdicts={key:verdict1(k,n) if done else 'incomplete' for key,(k,n,done) in counts.items()}
            else:
                prior=first['reconstructed'];oldcounts={f'{s["cell"]}:{k[6:]}':v for s in prior['cells'] for k,v in s.items() if k.startswith('cover_')}
                verdicts={}
                for key,value in prior['verdicts'].items():
                    if value!='borderline':verdicts[key]=value
                    elif not counts[key][2]:verdicts[key]='incomplete'
                    else:verdicts[key]='pass' if oldcounts[key]+counts[key][0]>=1886 else 'fail'
            rebuilt['verdicts']=verdicts
            rebuilt['borderline_cells']=sorted({k.split(':')[0] for k,v in verdicts.items() if v=='borderline'})
            rebuilt['result']='pass' if set(verdicts.values())=={'pass'} else 'fail' if 'fail' in verdicts.values() else 'incomplete' if 'incomplete' in verdicts.values() else 'borderline'
        for key,value in rebuilt.items():same(record.get(key),value,f'{name}: reconstructed {key}')
        verified=dict(record=record,reconstructed=rebuilt,file_sha256=sha(payload))
        self.records[name]=verified
        rates=[(1-s[k]/s['passes'],f'{s["cell"]}:{k[6:]}') for s in acceptance if s['passes'] for k in s if k.startswith('cover_')]
        per_quantity=[]
        for summary in summaries:
            for key,hits in summary.items():
                if not key.startswith('cover_'):continue
                quantity=key[6:];n=summary['passes'];misses=n-hits
                per_quantity.append(dict(tag=tag,phase=phase,cell=summary['cell'],kind=summary['kind'],quantity=quantity,
                    passing=n,covered=hits,misses=misses,false_claim_frequency=misses/n if n else None,
                    non_abstaining_analyses=summary[f'claims_{quantity}'],non_abstaining_misses=summary[f'claimmiss_{quantity}'],
                    calibration_shift_needed=summary[f'delta_{quantity}'],
                    verdict=rebuilt.get('verdicts',{}).get(f'{summary["cell"]}:{quantity}')))
        self.quantity_rows.extend(per_quantity)
        acceptance_rows=[row for row in per_quantity if row['kind']=='acceptance' and row['passing']]
        self.details.append(dict(file=name,phase=phase,tag=tag,sha256=sha(payload),binding_sha256=record['binding_sha256'],
            complete=rebuilt['complete'],result=rebuilt.get('result'),shift=shift,delta=rebuilt.get('delta'),
            cells=len(summaries),quantities=len(counts),attempts=sum(s['attempts'] for s in summaries),
            passes=sum(s['passes'] for s in summaries),errors=sum(s['errors'] for s in summaries),
            prescreen_errors=sum(s['errors_before_screen'] for s in summaries),
            worst_false_claim_frequency=max(rates,default=(None,None)),
            worst_false_claim=max(acceptance_rows,key=lambda row:(row['false_claim_frequency'],row['cell'],row['quantity'])) if acceptance_rows else None,
            exact_path_target_checks=self.target_stats.get(id(b),{}),
            boundaries=[s for s in summaries if s['cell'] in {'B3','B4'}]))
        return verified


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('directory',type=Path)
    parser.add_argument('--repository',type=Path,default=Path('/Users/bwbrook/papers/silurian_plants'))
    parser.add_argument('--revision',default='5fcee58')
    parser.add_argument('--include-dev',action='store_true')
    parser.add_argument('--expect-all',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    audit=Auditor(args.directory,args.repository,args.revision)
    files=[p for p in sorted(args.directory.glob('*.json')) if PATTERN.fullmatch(p.name)
           and (args.include_dev or not p.name.endswith('_dev.json'))]
    errors=[]
    for path in files:
        try:audit.audit(path)
        except (AuditFailure,OSError,KeyError,ValueError,TypeError) as exc:errors.append(dict(file=path.name,error=f'{type(exc).__name__}: {exc}'))
    if not files:errors.append(dict(error='no matching receipts'))
    tags={d['tag'] for d in audit.details if d['phase']!='dev'}
    final={}
    for tag in sorted(tags):
        available={d['phase']:d for d in audit.details if d['tag']==tag}
        chosen=available.get('stage2',available.get('accept',available.get('calibrate')))
        final[tag]=chosen['result'] or ('calibrated only' if chosen['complete'] else 'calibration incomplete')
    if args.expect_all:
        if tags!=EXPECTED_TAGS:errors.append(dict(error='missing or unexpected design/rho combinations',expected=sorted(EXPECTED_TAGS),actual=sorted(tags)))
        for tag in sorted(EXPECTED_TAGS):
            if final.get(tag) not in {'pass','fail'}:errors.append(dict(error=f'{tag}: no final complete acceptance verdict'))
    report=dict(integrity_ok=not errors,source_revision=args.revision,directory=str(args.directory.resolve()),
                checker_sha256=sha(Path(__file__).read_bytes()),receipts=len(audit.details),final_verdicts=final,
                details=audit.details,errors=errors,
                scope='Independent saved-ledger reconstruction; no simulator, estimator or production contract imports. Does not rerun numerical fits.')
    table=args.output.with_name(args.output.stem+'-quantities.csv')
    if audit.quantity_rows:
        with table.open('w',newline='') as stream:
            writer=csv.DictWriter(stream,list(audit.quantity_rows[0]),lineterminator='\n')
            writer.writeheader();writer.writerows(audit.quantity_rows)
        report['quantity_table']=str(table.resolve())
    args.output.write_text(json.dumps(clean(report),indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(integrity_ok=report['integrity_ok'],receipts=report['receipts'],final_verdicts=final,errors=errors),indent=2))
    return 0 if not errors else 1


if __name__=='__main__':sys.exit(main())
