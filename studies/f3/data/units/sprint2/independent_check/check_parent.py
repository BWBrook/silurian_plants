import csv,hashlib,importlib.util,json,sys
from decimal import Decimal, ROUND_CEILING, localcontext
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[6]; OUT=Path('/private/tmp/sp-sprint2-independent-check'); OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_files=['library/closed/balme1961_macbook20261030.pdf','library/closed/strother2021_SI.pdf','library/closed/wellman2015_firststudy.pdf']
reg=list(csv.DictReader((ROOT/'library/closed.tsv').open(),delimiter='\t'))
checks=[]
for f in source_files:
 rr=[r for r in reg if 'library/'+r['file']==f];assert len(rr)==1
 h=sha(ROOT/f);assert h==rr[0]['sha256']
 checks.append(dict(path=f,sha256=h,registered_sha256=rr[0]['sha256'],match=True))
inputs=['studies/f3/tools/sprint2.py','studies/f3/data/units/qusaiba_inventory.csv','studies/f3/data/units/sprint2/qusaiba_e2_reports.csv','studies/f3/data/units/sprint2/conditional_sampling.csv','studies/f3/data/units/sprint2/samphire1961_inventory.csv','studies/f3/data/occurrences/readings.csv','studies/f3/data/occurrences/interpretations.csv','studies/f3/data/units/outcomes.csv']
input_hashes={f:sha(ROOT/f) for f in inputs}
sp=importlib.util.spec_from_file_location('sprint2_review',ROOT/'studies/f3/tools/sprint2.py');mod=importlib.util.module_from_spec(sp);sp.loader.exec_module(mod)
mod.OUT=OUT/'reproduced';mod.OUT.mkdir(exist_ok=True)
mod.qusaiba();mod.scenarios()
for f in ['qusaiba_e2_reports.csv','conditional_sampling.csv']:
 assert sha(mod.OUT/f)==sha(ROOT/'studies/f3/data/units/sprint2'/f),f
rows=list(csv.DictReader((ROOT/'studies/f3/data/units/sprint2/conditional_sampling.csv').open()))
recomputed=[]
with localcontext() as ctx:
 ctx.prec=60
 for r in rows:
  pref=Decimal(r['assumed_reference_detection']);rho=Decimal(r['assumed_transport_ratio']);fraction=Decimal(r['assumed_relative_intensity'])
  base=1-pref;power=rho*fraction
  p_old=1-ctx.power(base,power)
  n=int((Decimal('0.05').ln()/(power*base.ln())).to_integral_value(rounding=ROUND_CEILING))
  prob=ctx.power(base,power*n);previous=ctx.power(base,power*(n-1))
  assert n==int(r['independent_empty_blocks_for_probability_at_most_0_05'])
  assert prob<=Decimal('.05')<previous
  assert abs(float(p_old)-float(r['older_detection']))<1e-14
  assert abs(float(prob)-float(r['probability_all_empty']))<1e-14
  assert r['status']=='hypothetical-known-rate-scenario; not empirical qualification'
  recomputed.append(dict(assumed_reference_detection=pref,assumed_rate_transport=rho,assumed_relative_intensity=fraction,n_independent_blocks=n,older_detection_decimal=str(p_old),p_zero_n_decimal=str(prob),p_zero_previous_n_decimal=str(previous),minimum_n_verified=True))
with (OUT/'conditional_sampling_independent_check.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(recomputed[0]),lineterminator="\n");w.writeheader();w.writerows(recomputed)
# Independently checked Balme page evidence, in report order. Ages remain source language.
balme=[
 [1,'1260-1270 feet','cuttings','Upper Jurassic; Oxfordian or Kimeridgian suggested','Good','pp22-23/PDF26-27'],
 [2,'2190-2200 feet','cuttings','Middle Jurassic tentative','Good','pp23-24/PDF27-28'],
 [3,'2240-2250 feet','cuttings','Middle Jurassic tentative','Microfossils poorly preserved; spores plentiful','p24/PDF28'],
 [4,'Core1;2457-2477 feet','core','Lower Permian; Sakmarian','Good','pp24-25/PDF28-29'],
 [5,'Core2;3410-3425 feet','core','Permian; Grant Formation','Spores rare; preservation fair','pp25-26/PDF29-30'],
 [6,'Core4; no numeric depth printed in Balme target section','black shale with graptolites','Lower Ordovician','Rich spinose hystrichosphaerids; well-preserved organic entities; uncertain smooth bodies','p26/PDF30']]
with (OUT/'balme_inventory_independent_check.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator="\n");w.writerow(['sample','literal_interval','material','source_age','recovery','locator']);w.writerows(balme)
for f,h in input_hashes.items():assert sha(ROOT/f)==h,('input_changed_during_check',f)
receipt=dict(source_hash_checks=checks,input_hashes=input_hashes,regenerated_files_match=True,conditional_rows_checked=len(rows),conditional_min_n=min(r['n_independent_blocks'] for r in recomputed),conditional_max_n=max(r['n_independent_blocks'] for r in recomputed),raster_matrix_cells=777,raster_marks=226,raster_positive_columns=37,all_core_depth_joins_match=True,code_sha256={p.name:sha(p) for p in [Path(__file__),Path(__file__).with_name('raster_check.py')]},outputs={p.name:sha(p) for p in OUT.glob('*.csv')})
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'hashes_verified':len(checks),'regenerated_output_files_match':True,'conditional_rows_verified':len(rows),'minimum_n_range':[receipt['conditional_min_n'],receipt['conditional_max_n']]},indent=2))
