"""Exact comparison of the historical and final same-seed statistical evidence."""

import gzip
import hashlib
import json
from pathlib import Path

OLD=Path('/private/tmp/sp-sprint1-rerun/qual')
NEW=Path('/private/tmp/sp-sprint1-rerun-final/qual')
OUT=Path('/private/tmp/sp-sprint1-new-evidence-review/final-31fab51')
STATISTICS=('phase','root','shift','target','cap','cells','complete','delta','verdicts','borderline_cells','result')

def digest(payload):return hashlib.sha256(payload).hexdigest()

def differences(a,b,path=''):
    if type(a) is not type(b):return [path+': type differs']
    if isinstance(a,dict):
        result=[path+': keys differ'] if set(a)!=set(b) else []
        for key in sorted(set(a)&set(b)):
            result.extend(differences(a[key],b[key],path+'/'+key))
        return result
    if isinstance(a,list):
        result=[path+': length differs'] if len(a)!=len(b) else []
        for i,(x,y) in enumerate(zip(a,b)):result.extend(differences(x,y,f'{path}/{i}'))
        return result
    return [] if a==b else [path+': value differs']

old_names={p.name for p in OLD.glob('*.json') if p.name.endswith(('_calibrate.json','_accept.json','_stage2.json'))}
new_names={p.name for p in NEW.glob('*.json') if p.name.endswith(('_calibrate.json','_accept.json','_stage2.json'))}
assert old_names==new_names and len(new_names)==28,(old_names-new_names,new_names-old_names)
records=[]
for name in sorted(new_names):
    old_bytes=(OLD/name).read_bytes();new_bytes=(NEW/name).read_bytes()
    old=json.loads(old_bytes);new=json.loads(new_bytes)
    old_stats={k:old[k] for k in STATISTICS if k in old}
    new_stats={k:new[k] for k in STATISTICS if k in new}
    summary_differences=differences(old_stats,new_stats)
    old_binding={k:v for k,v in old['binding'].items() if k!='files'}
    new_binding={k:v for k,v in new['binding'].items() if k!='files'}
    binding_differences=differences(old_binding,new_binding)
    old_file=OLD/old['replicates']['file'];new_file=NEW/new['replicates']['file']
    old_gz=old_file.read_bytes();new_gz=new_file.read_bytes()
    old_csv=gzip.decompress(old_gz);new_csv=gzip.decompress(new_gz)
    changed={k:dict(historical=old['binding']['files'].get(k),final=new['binding']['files'].get(k))
             for k in sorted(set(old['binding']['files'])|set(new['binding']['files']))
             if old['binding']['files'].get(k)!=new['binding']['files'].get(k)}
    records.append(dict(file=name,phase=new['phase'],historical_receipt_sha256=digest(old_bytes),final_receipt_sha256=digest(new_bytes),
        historical_ledger_sha256=digest(old_gz),final_ledger_sha256=digest(new_gz),
        compressed_ledgers_identical=old_gz==new_gz,decompressed_statistical_records_identical=old_csv==new_csv,
        statistical_summaries_identical=not summary_differences,statistical_binding_values_identical=not binding_differences,
        summary_differences=summary_differences,binding_differences=binding_differences,changed_file_bindings=changed))
result=dict(historical_revision='5fcee58',final_revision='31fab51',receipts=len(records),
    all_compressed_ledgers_identical=all(r['compressed_ledgers_identical'] for r in records),
    all_statistical_records_identical=all(r['decompressed_statistical_records_identical'] for r in records),
    all_statistical_summaries_identical=all(r['statistical_summaries_identical'] for r in records),
    all_statistical_binding_values_identical=all(r['statistical_binding_values_identical'] for r in records),
    only_portability_contract_hash_changed=all(set(r['changed_file_bindings'])=={'models/f3/qualification_contract.py'} for r in records),
    records=records,comparison_script_sha256=digest(Path(__file__).read_bytes()))
(OUT/'exact-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'records','comparison_script_sha256'}},indent=2))
assert all(result[k] for k in ('all_statistical_records_identical','all_statistical_summaries_identical',
                              'all_statistical_binding_values_identical','only_portability_contract_hash_changed'))
