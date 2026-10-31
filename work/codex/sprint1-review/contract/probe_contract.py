import copy,json,math,sys,types
from pathlib import Path
sys.path.insert(0,'/Users/bwbrook/papers/silurian_plants/models/f3')
import qualification_contract as qc
import qualify as q
import m2

base=Path(sys.argv[1])
cell=dict(name='T',kind='acceptance',quantities=['f_H0'])
protocol=dict(calibration_target=.955,target_passing=1000,max_attempts=20000,
              root_seeds=dict(calibrate=100,accept=200,stage2=300))
binding=dict(design='AUDIT-TOY',rho=1.,grid=[cell],protocol=protocol,
             fitted_reference_rates=[1.],derived_tolerance=qc.DERIVED_TOLERANCE)
critical=q.ev.count_crit(0)
def rows():
    return [dict(cell='T',rep=i,passed=True,error='',trivial=False,
                 screen_status='evaluated',screen_converged=True,screen_lr=7.,
                 screen_crit=critical,screen_n_older_detections=0,
                 c_f_H0=True,m_f_H0=-1.) for i in range(1000)]
def rejects(call):
    try:
        call()
    except (qc.EvidenceError, RuntimeError) as e:
        return dict(rejected=True,error=str(e))
    return dict(rejected=False)

results={}
failed=dict(cell='T',rep=0,passed=False,error='RuntimeError: simulator failed',screen_status='error',screen_converged=False)
rr=rows()
for r in rr:r['rep']+=1
a=qc.assessment(binding,'accept',[failed]+rr,1000,20000,0.)
results['prescreen_error']=dict(complete=a['complete'],result=a['result'],errors_before_screen=a['cells'][0]['errors_before_screen'])
assert not a['complete'] and a['result']=='incomplete'
rr=rows();rr[0]['screen_lr']=0.
results['contradictory_screen']=rejects(lambda:qc.assessment(binding,'accept',rr,1000,20000,0.))
assert results['contradictory_screen']['rejected']
pr=types.SimpleNamespace(n_old=1,spec=types.SimpleNamespace(domain_ma=(0.,560.),alpha=.05),
                         exposure=lambda T:1.,n_older_detections=lambda T:0,
                         lr=lambda *a:q.ev.Statistic(7.,False,0.))
results['unconverged_screen']=rejects(lambda:m2.screen(pr))
assert results['unconverged_screen']['rejected']

runtime=dict(python='audit-toy',numpy='audit-toy',scipy='audit-toy',platform='audit-toy')
cal=qc.write(base,binding,'calibrate',rows(),100,1000,20000,0.,{},runtime,0.)
assert qc.load(base,binding,'calibrate').record['complete']
first=dict(complete=True,borderline_cells=['T'],verdicts={'T:f_H0':'borderline'},
           cells=[dict(cell='T',cover_f_H0=940,passes=1000)])
stage2=qc.write(base,binding,'stage2',rows(),300,1000,20000,0.,
                dict(calibrate=cal.sha256,accept='missing'),runtime,0.,first)
results['orphan_stage2_low_level']=rejects(lambda:qc.load(base,binding,'stage2'))
assert results['orphan_stage2_low_level']['rejected']
old_build,old_paths=q.build_binding,q.bound_paths
ctx=q.Context('LY-H2-CU',1.)
q.build_binding=lambda *a:(ctx,binding,{})
q.bound_paths=lambda *a:{}
try:
    delta,status,sha,bound=q.load_qualification('AUDIT-TOY',1.,base)
    results['orphan_stage2_attachment']=dict(status=status,delta=delta)
    assert status=='calibrated only'
finally:
    q.build_binding,q.bound_paths=old_build,old_paths
before=qc.file_hash(cal.path)
results['immutable_rewrite']=rejects(lambda:qc.write(base,binding,'calibrate',rows(),100,1000,20000,0.,{},runtime,0.))
assert results['immutable_rewrite']['rejected'] and qc.file_hash(cal.path)==before

close=copy.deepcopy(binding);close['fitted_reference_rates'][0]+=1e-10
qc.check_binding(close,binding)
far=copy.deepcopy(binding);far['fitted_reference_rates'][0]+=1e-5
results['derived_tolerance']=dict(small_change_accepted=True,large_change=rejects(lambda:qc.check_binding(far,binding)))
assert results['derived_tolerance']['large_change']['rejected']
print(json.dumps(results,indent=2))
