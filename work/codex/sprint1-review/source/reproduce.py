from pathlib import Path
import csv,json,hashlib,collections,tomllib
ROOT=Path('/Users/bwbrook/papers/silurian_plants')
OUT=Path(__file__).resolve().parent

def read(name):
 return list(csv.DictReader((ROOT/name).open()))
def key(r):return r['well'],float(r['depth_ft'])
def uid(k):return f'{k[0]}:{k[1]:g}'
def dump(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
app=read('data/units/libya_appendix1.csv'); chart=read('data/units/libya_chart_reports.csv');prose=read('data/units/libya_prose_support.csv')
a={key(r):r for r in app};c={key(r):r for r in chart};p={key(r):r for r in prose}
assert len(a)==len(app)==164 and len(c)==len(chart)==158 and len(p)==len(prose)==164
ak,ck=set(a),set(c)
summary={'libya_appendix_rows':len(a),'libya_chart_rows':len(c),'exact_joins':len(ak&ck),'appendix_only':len(ak-ck),'chart_only':len(ck-ak),'all_chart_target_marks':sum(r['ambitisporites_dilutus_report']=='mark-present' for r in chart),'exact_join_target_marks':sum(c[k]['ambitisporites_dilutus_report']=='mark-present' for k in ak&ck),'explicit_barren_appendix':sum(r['productivity_prose_status'].startswith('explicit-barren') for r in prose)}
rows=[]
for k in sorted(ak|ck):
 ar,cr,pr=a.get(k,{}),c.get(k,{}),p.get(k,{})
 rows.append(dict(well=k[0],depth_ft=k[1],appendix_present=bool(ar),chart_present=bool(cr),appendix_type=ar.get('type',''),chart_type=cr.get('type_code',''),formation=ar.get('formation',''),target_report=cr.get('ambitisporites_dilutus_report',''),marine_symbols=cr.get('marine_symbols',''),other_green_symbols=cr.get('other_green_symbols',''),prose_productivity=pr.get('productivity_prose_status',''),e1_context=pr.get('e1_assemblage_context','')))
dump('libya_all_material_joins.csv',rows)

def independent_libya(wells,classes,v):
 included={}; excluded={}
 for k,ar in a.items():
  if k[0] not in wells:continue
  cr=c.get(k);pr=p[k]
  if cr is None:excluded[uid(k)]='no exact chart';continue
  kind=ar['type']
  if kind not in {'Core','Cutting'}:
   if v['material_type']=='appendix-only':excluded[uid(k)]='unspecified appendix material';continue
   kind={'CU':'Cutting','CO':'Core'}[cr['type_code']]
  if kind not in classes:continue
  if pr['productivity_prose_status'].startswith('explicit-barren') or int(cr['marine_symbols'])==0:excluded[uid(k)]='barren/no marine recovery';continue
  if 'ash sh' in ar['formation'].lower():excluded[uid(k)]='possibly caved recovery';continue
  target=cr['ambitisporites_dilutus_report']
  if target=='column-absent' and v.get('a28i')=='column-absent-excluded':excluded[uid(k)]='no target column';continue
  if k==('E1-NC174',7287.0):
   if v.get('e1_7287')=='unresolved':excluded[uid(k)]='prose/chart conflict';continue
   d=1
  else:d=int(target=='mark-present')
  form=ar['formation'].lower();zone=pr['e1_assemblage_context']
  if 'hawaz' in form:young=old='Darriwilian'
  elif 'bir tlacsin' in form:young=old='Hirnantian'
  elif 'shugran' in form or 'memouniat' in form:young,old='Hirnantian','Katian'
  elif 'Cr4' in zone:young,old='Telychian','Rhuddanian'
  elif 'Cr3' in zone:young=old='Rhuddanian'
  else:young,old='Telychian','Rhuddanian'
  transported=old in {'Darriwilian','Katian','Hirnantian'}
  included[uid(k)]={'d':str(d),'cls':kind,'youngest_stage':young,'oldest_stage':old,'transported':str(transported),'formation':ar['formation']}
 return included,excluded

outputs=read('models/f3/out/m2_units.csv')
groups=collections.defaultdict(list)
for r in outputs:groups[(r['design'],r['variant'])].append(r)
decl=tomllib.loads((ROOT/'models/f3/designs/m2.toml').read_text())
designs={x['id']:x for x in decl['design']}
checks=[]; differences=[]
for (design,variant),rr in groups.items():
 v=dict(x.split('=',1) for x in variant.split(';'))
 if not design.startswith('LY-'):continue
 expected,excluded=independent_libya(designs[design]['wells'],designs[design]['classes'],v)
 observed={r['unit_id']:r for r in rr if not r['excluded']}
 if set(expected)!=set(observed):differences.append([design,variant,'included key mismatch',list(set(expected)^set(observed))])
 for id,er in expected.items():
  for field,val in er.items():
   if id in observed and observed[id][field]!=val:differences.append([design,variant,id,field,val,observed[id][field]])
 observed_ex={r['unit_id'] for r in rr if r['excluded']}
 if observed_ex!=set(excluded):differences.append([design,variant,'excluded key mismatch',list(observed_ex^set(excluded))])
 checks.append(dict(design=design,variant=variant,included=len(expected),excluded=len(excluded),positive=sum(int(r['d']) for r in expected.values()),reference_n=sum(r['transported']=='False' for r in expected.values()),reference_positive=sum(int(r['d']) for r in expected.values() if r['transported']=='False'),older_n=sum(r['transported']=='True' for r in expected.values()),older_positive=sum(int(r['d']) for r in expected.values() if r['transported']=='True')))
dump('all_libya_variant_checks.csv',checks)
summary['libya_variant_groups_checked']=len(checks);summary['libya_adapter_differences']=differences

primary=[]
for design in ['LY-H2-CU','LY-D1-CU','LY-I3-CU','LY-MZ-CU']:
 v='allocation=stage;material_type=chart-code'
 primary.extend({**r,'e1_assemblage_context':p[(r['cluster'],float(r['depth']))]['e1_assemblage_context']} for r in groups[(design,v)] if not r['excluded'])
dump('primary_cutting_units.csv',primary)
mz=[r for r in primary if r['design']=='LY-MZ-CU'];ref=[r for r in mz if r['transported']=='False'];old=[r for r in mz if r['transported']=='True']
summary['mz_reference_contexts']=dict(collections.Counter(r['e1_assemblage_context'] for r in ref));summary['mz_older_formations']=dict(collections.Counter(r['formation'] for r in old));summary['mz_by_well']={well:dict(n_ref=sum(r['cluster']==well for r in ref),ref_marks=sum(int(r['d']) for r in ref if r['cluster']==well),n_old=sum(r['cluster']==well for r in old)) for well in sorted({r['cluster'] for r in mz})}
summary['mz_non_Cr4_reference']=[{k:r[k] for k in ['unit_id','d','e1_assemblage_context']} for r in ref if r['e1_assemblage_context']!='Cr4-listed-interval']
summary['all_exact_Hawaz_types']=dict(collections.Counter(a[k]['type'] for k in ak&ck if 'hawaz' in a[k]['formation'].lower()))
summary['all_exact_Hawaz_green_min']=min(int(c[k]['other_green_symbols']) for k in ak&ck if 'hawaz' in a[k]['formation'].lower())
summary['all_exact_Hawaz_green_max']=max(int(c[k]['other_green_symbols']) for k in ak&ck if 'hawaz' in a[k]['formation'].lower())

q=read('data/units/qusaiba_inventory.csv');q=[r for r in q if r['wellman_table2_member']=='yes']
bor=read('data/units/outcomes.csv');bor=[r for r in bor if r['unit_id'].startswith('BOR-') and r['event_id']=='E1']
summary['qusaiba_table2_n']=len(q);summary['qusaiba_table2_states']=dict(collections.Counter(r['e1_table2_status'] for r in q));summary['bor_E1_states_by_reading']={name:dict(collections.Counter(r['outcome'] for r in bor if r['reading_id']==name)) for name in ['main','inclusive','outlier']}
qbchecks=[]
for (design,variant),rr in groups.items():
 if design!='QB-CO':continue
 v=dict(x.split('=',1) for x in variant.split(';'))
 expected={r['record_id']:int(r['e1_table2_status']=='taxon-mark-present') for r in q}
 bx=[r for r in bor if r['reading_id']==v['reading']]
 ex=set()
 for r in bx:
  if r['outcome']=='unresolved' and v['bor_unresolved']=='excluded':ex.add(r['unit_id']);continue
  expected[r['unit_id']]=int(r['outcome']=='detected')
 observed={r['unit_id']:int(r['d']) for r in rr if not r['excluded']}
 assert expected==observed
 assert ex=={r['unit_id'] for r in rr if r['excluded']}
 retained=[r for r in rr if not r['excluded']]
 qbchecks.append(dict(variant=variant,included=len(retained),excluded=len(ex),total_positive=sum(expected.values()),bor_accepted=sum(r['source'].startswith('rubinstein') for r in retained),bor_positive=sum(int(r['d']) for r in retained if r['source'].startswith('rubinstein')),bor_Katian=[r['unit_id'] for r in retained if r['source'].startswith('rubinstein') and r['youngest_stage']=='Katian'],unresolved_as_zero=sum(r['outcome']=='unresolved' and v['bor_unresolved']=='zero' for r in bx)))
dump('qb_variant_checks.csv',qbchecks)
summary['qb_variants_checked']=len(qbchecks)
consumed=['models/f3/designs.py','models/f3/designs/m2.toml','models/f3/out/m2_units.csv','models/f3/out/m2_screen.csv','data/units/libya_appendix1.csv','data/units/libya_chart_reports.csv','data/units/libya_prose_support.csv','data/units/qusaiba_inventory.csv','data/units/borenshult_ages.csv','data/units/borenshult_reporting.csv','data/units/outcomes.csv','data/units/source_files.csv']
summary['inputs']=[dict(file=f,sha256=hashlib.sha256((ROOT/f).read_bytes()).hexdigest()) for f in consumed]
(OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='inputs'},indent=2))
assert not differences
