"""Synthetic audit fixtures only: exercise the independent stage-two reconstruction."""

import copy,csv,gzip,hashlib,io,json,sys
from pathlib import Path
import audit_saved_ledgers as a

ROOT=Path('/private/tmp/sp-sprint1-new-evidence-review')
SOURCE=Path('/private/tmp/sp-sprint1-rerun/qual')
TAG='LY-H2-CU_rho1'

def write_record(directory,record,rows):
    phase=record['phase'];repname=f'{TAG}_{phase}_reps.csv.gz'
    buf=io.StringIO();fields=list(dict.fromkeys(k for row in rows for k in row))
    writer=csv.DictWriter(buf,fields,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    data=gzip.compress(buf.getvalue().encode(),mtime=0)
    record['replicates']=dict(file=repname,sha256=a.sha(data))
    record.pop('payload_sha256',None);record['payload_sha256']=a.sha(a.canonical(record))
    (directory/repname).write_bytes(data)
    path=directory/f'{TAG}_{phase}.json';path.write_text(json.dumps(record,indent=2)+'\n')
    return a.sha(path.read_bytes())

def summary(cell,rows,hits):
    n=len(rows);result=dict(cell=cell['name'],kind='acceptance',attempts=n,passes=n,pass_rate=1.,complete=True,errors=0,errors_before_screen=0)
    for q in cell['quantities']:
        good=hits if q=='f_H0' else n
        result.update({f'cover_{q}':good,f'claims_{q}':n,f'claimmiss_{q}':n-good,f'delta_{q}':1. if n-good>45 and q=='f_H0' else 0.})
    return result

base=json.loads((SOURCE/f'{TAG}_accept.json').read_text())
rows=list(csv.DictReader(io.StringIO(gzip.decompress((SOURCE/f'{TAG}_accept_reps.csv.gz').read_bytes()).decode())))
cell=next(c for c in base['binding']['grid'] if c['name']=='B3')
sample=next(r for r in rows if r['cell']=='B3' and r['passed']=='True' and r['trivial']=='False'
            and all(r[f'c_{q}']=='True' for q in cell['quantities']))

def fabricated(hits):
    result=[]
    for i in range(1000):
        row=copy.deepcopy(sample);row['rep']=str(i)
        row['c_f_H0']='True' if i<hits else 'False';row['m_f_H0']='-1.0' if i<hits else '1.0'
        result.append(row)
    return result

report={}
for hits,expected in [(946,'pass'),(945,'fail')]:
    directory=ROOT/f'SYNTHETIC-stage2-{hits}';directory.mkdir(exist_ok=True)
    for suffix in ('calibrate.json','calibrate_reps.csv.gz'):
        (directory/f'{TAG}_{suffix}').write_bytes((SOURCE/f'{TAG}_{suffix}').read_bytes())
    accept=copy.deepcopy(base);rr=fabricated(940)
    accept['cells']=[summary(cell,rr,940) if s['cell']=='B3' else s for s in accept['cells']]
    accept['verdicts']['B3:f_H0']='borderline';accept['borderline_cells']=['B3'];accept['result']='borderline'
    accept_rows=[]
    for c in accept['binding']['grid']:
        if c['kind']=='acceptance':accept_rows.extend(rr if c['name']=='B3' else [r for r in rows if r['cell']==c['name']])
    accept_sha=write_record(directory,accept,accept_rows)
    second=copy.deepcopy(accept);second.update(phase='stage2',root=second['binding']['protocol']['root_seeds']['stage2'],
        cells=[summary(cell,fabricated(hits),hits)],dependencies=dict(calibrate=a.sha((directory/f'{TAG}_calibrate.json').read_bytes()),accept=accept_sha),
        borderline_cells=[],result=expected)
    second['verdicts']['B3:f_H0']=expected
    write_record(directory,second,fabricated(hits))
    auditor=a.Auditor(directory,Path('/Users/bwbrook/papers/silurian_plants'),'5fcee58')
    verified=auditor.audit(directory/f'{TAG}_stage2.json')
    actual=verified['reconstructed']['result'];assert actual==expected
    report[f'pooled_{940+hits}_of_2000']=actual

directory=ROOT/'SYNTHETIC-contradiction';directory.mkdir(exist_ok=True)
for suffix in ('calibrate.json','calibrate_reps.csv.gz'):
    (directory/f'{TAG}_{suffix}').write_bytes((SOURCE/f'{TAG}_{suffix}').read_bytes())
bad=copy.deepcopy(base);badrows=copy.deepcopy(rows)
next(r for r in badrows if r['passed']=='True')['screen_lr']='0.0'
write_record(directory,bad,badrows)
try:
    a.Auditor(directory,Path('/Users/bwbrook/papers/silurian_plants'),'5fcee58').audit(directory/f'{TAG}_accept.json')
except a.AuditFailure as exc:report['resealed_screen_contradiction']=str(exc)
else:raise AssertionError('contradictory screen escaped independent checker')

(ROOT/'checker-exercise-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
