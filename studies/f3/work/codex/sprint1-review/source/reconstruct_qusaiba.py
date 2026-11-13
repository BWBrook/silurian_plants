from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict
import csv,re,subprocess
ROOT=Path('/Users/bwbrook/papers/silurian_plants')
OUT=Path(__file__).resolve().parent
subprocess.run(['pdftotext','-bbox','-f','6','-l','6',str(ROOT/'library/closed/wellman2015_firststudy.pdf'),str(OUT/'qusaiba-table2.html')],check=True)
words=[(float(w.attrib['xMin']),float(w.attrib['yMin']),w.text or '') for w in ET.parse(OUT/'qusaiba-table2.html').iter() if w.tag.endswith('word')]
labelrow=defaultdict(list)
for x,y,t in words:
 if x<130 and 415<y<482:labelrow[round(y,2)].append((x,t))
labels={y:' '.join(t for x,t in sorted(v)) for y,v in labelrow.items()}
assert len(labels)==8
headers=sorted((x,t) for x,y,t in words if 135<y<150 and re.fullmatch(r'\??\d+(\.\d+)?m',t))
assert len(headers)==37
reports={label:set() for x,label in headers}
for x,y,t in words:
 if t=='X' and 415<y<482:
  cx,depth=min(headers,key=lambda h:abs(h[0]-x))
  ty=min(labels,key=lambda yy:abs(yy-y))
  assert abs(cx-x)<4 and abs(ty-y)<1.2
  reports[depth].add(labels[ty])
source=list(csv.DictReader((ROOT/'data/units/qusaiba_inventory.csv').open()))
source={r['wellman_literal_depth_label']:r for r in source if r['wellman_table2_member']=='yes'}
rows=[]
for x,dep in headers:
 r=source[dep];observed=reports[dep];registered=set(r['e1_table2_taxa'].split(';')) if r['e1_table2_taxa'] else set()
 rows.append(dict(literal_depth=dep,taxa_from_pdf=';'.join(sorted(observed)),taxa_in_csv=';'.join(sorted(registered)),match=observed==registered))
assert all(r['match'] for r in rows)
with (OUT/'qusaiba_primary_reconstruction.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('8 trilete rows,37 columns,',sum(bool(r['taxa_from_pdf']) for r in rows),'positive columns; all per-column taxon sets match.')
