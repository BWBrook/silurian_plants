import csv,hashlib,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[4]
OUT=Path('/private/tmp/sp-sprint2-independent-check'); OUT.mkdir(exist_ok=True)
(OUT/'render').mkdir(exist_ok=True)
subprocess.run(['pdftoppm','-f','6','-l','6','-scale-to','4200','-singlefile',str(ROOT/'library/closed/wellman2015_firststudy.pdf'),str(OUT/'render/qusaiba-raster')],check=True)
with (OUT/'render/qusaiba-raster.ppm').open('rb') as f:
 assert f.readline().strip()==b'P6'
 w,h=map(int,f.readline().split());assert int(f.readline())==255
 a=np.frombuffer(f.read(),np.uint8).reshape(h,w,3)
dark=a.max(axis=2)<80
x0,x1,y0,y1=700,2930,1030,1972
b=dark[y0:y1,x0:x1].copy()
b[:,b.sum(axis=0)>700]=False
b[b.sum(axis=1)>600,:]=False
column_ink=b.sum(axis=0)
inds=np.flatnonzero(column_ink>2)
groups=np.split(inds,np.where(np.diff(inds)>1)[0]+1)
groups=[g for g in groups if len(g)>3]
xs=[x0+(int(g[0])+int(g[-1]))/2 for g in groups]
assert len(xs)==37,xs
# Row centres fixed from the manually inspected raster's 21 equally spaced blue/pink labels.
ys=[1049,1095,1140,1185,1231,1276,1321,1367,1412,1457,1503,1548,1593,1639,1684,1729,1775,1820,1865,1911,1956]
labels=['Dyadospora. murusattenuata','D. murusdensa','Didymospora fucosogranulata','Abditusdyadus chalazus?','A. laevigatus?','Pseudodyadospora laevigata','P. petasus','Segestrespora laevigata','S. membranifera','S. rugosa','Tetrahedraletes medinensis','Cryptotetras mordacis','Cheilotetras spp.','Tetraplanarisporites laevigatus','Tetraplanarisporites sp. A','Tetraplanarisporites sp. B','Velatitetras anatoliensis','V. laevigata','V. reticulata','V. rugulata','Sphaerosaccus glabellus']
manual_depths=['292.3m','294.8m','301.1m','302.11m','305.0m','307.7m','310.2m','318.2m','319.1m','323.1m','325.4m','327.9m','330.3m','333.4m','335.7m','338.4m','?341.0m','342.3m','345.85m','348.8m','350.6m','436.0m','438.7m','452.75m','458.4m','476.7m','479.4m','484.7m','488.3m','497.8m','503.1m','507.15m','518.5m','528.3m','535.2m','536.7m','551.0m']
manual_cores=['C31']*2+['C32']*5+['C33']*2+['C34']*4+['C35']*3+['C36']*5+['C45']+['C47']*3+['C49']*2+['C50']*2+['C51']+['C52']*2+['C53','C54','C55']+['C56']*2
assert len(manual_cores)==37
saved=list(csv.DictReader((ROOT/'data/units/sprint2/qusaiba_e2_reports.csv').open()))
inv=list(csv.DictReader((ROOT/'data/units/qusaiba_inventory.csv').open()))
inv=sorted([r for r in inv if r['wellman_table2_member']=='yes'],key=lambda r:int(r['wellman_table2_order_top_to_base']))
results=[];differences=[];cellrows=[]
for j,x in enumerate(xs):
 present=[]
 for i,y in enumerate(ys):
  patch=b[y-y0-12:y-y0+13,int(round(x))-x0-10:int(round(x))-x0+11]
  count=int(patch.sum()); mark=count>50
  cellrows.append(dict(column=j+1,row=i+1,taxon=labels[i],dark_pixels=count,raster_mark=mark))
  if mark:present.append(labels[i])
 old=set(saved[j]['reported_taxa'].split(';'))
 if old != set(present):differences.append(dict(column=j+1,raster_only=sorted(set(present)-old),text_only=sorted(old-set(present))))
 assert saved[j]['literal_depth_label']==manual_depths[j],(j,saved[j]['literal_depth_label'],manual_depths[j])
 assert saved[j]['reported_core']==manual_cores[j],(j,saved[j]['reported_core'],manual_cores[j])
 assert inv[j]['wellman_core']==manual_cores[j]
 assert saved[j]['record_id']==inv[j]['record_id']
 numeric=float(manual_depths[j].replace('?','').removesuffix('m'))
 assert numeric==float(inv[j]['depth_value_ft_interpretation'])
 results.append(dict(column=j+1,raster_core=manual_cores[j],literal_depth_label=manual_depths[j],record_id=saved[j]['record_id'],raster_positive=bool(present),raster_dyad_tetrad_marks=len(present),source_text_dyad_tetrad_marks=len(old),all_taxon_marks_match=old==set(present),manual_core_depth_join_match=True,raster_taxa=';'.join(present)))
for name,rr in [('qusaiba_raster_check.csv',results),('qusaiba_raster_cells.csv',cellrows)]:
 with (OUT/name).open('w',newline='') as f:
  wr=csv.DictWriter(f,fieldnames=list(rr[0]),lineterminator="\n");wr.writeheader();wr.writerows(rr)
print(json.dumps({'columns':len(results),'raster_positive_columns':sum(r['raster_positive'] for r in results),'matrix_cells':len(cellrows),'marks':sum(r['raster_mark'] for r in cellrows),'minimum_mark_ink':min(r['dark_pixels'] for r in cellrows if r['raster_mark']),'maximum_empty_ink':max(r['dark_pixels'] for r in cellrows if not r['raster_mark']),'differences':differences},indent=2))
