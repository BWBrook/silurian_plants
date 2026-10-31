from pathlib import Path
import sys
import pymupdf,csv,json
root=Path(sys.argv[1]);root.mkdir(parents=True,exist_ok=True);repo=Path(__file__).resolve().parents[3];pdf=pymupdf.open(repo/'library/closed/abuhmida2013-thesis-related_macbook20261030.pdf')
r=list(csv.DictReader((repo/'data/units/libya_chart_reports.csv').open()));checks=[]
for n,well,x0,x1 in [(630,'A28i-NC186',253,507),(632,'B2-NC186',402,506),(634,'D1-200',245,492),(636,'E1-NC174',267,456),(638,'H2-NC186',242,456),(640,'I3-NC186',254,529)]:
 p=pdf[n-1];words=p.get_text('words')
 for row in [x for x in r if x['well']==well]:
  token=f"{float(row['depth_ft']):.2f}'";w=min([x for x in words if x[4]==token],key=lambda x:(x[1],x[0]));y=(w[1]+w[3])/2
  pix=p.get_pixmap(matrix=pymupdf.Matrix(15,15),clip=pymupdf.Rect(x0,y-.28,x1,y+.28),alpha=False);v=pix.samples
  c=sum((v[i+2]>100 and v[i+2]>v[i]+40)or(v[i]>100 and v[i+1]>100 and v[i+2]<60)for i in range(0,len(v),pix.n))
  checks.append(dict(well=well,depth_ft=row['depth_ft'],marine_coloured_pixels=c,raster_presence=c>3,csv_presence=int(row['marine_symbols'])>0,agree=(c>3)==(int(row['marine_symbols'])>0)))
with(root/'raster_marine_checks.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]),lineterminator='\n');w.writeheader();w.writerows(checks)
print('Marine row checks',len(checks),'agreement',sum(x['agree']for x in checks),'marine rows',sum(x['raster_presence']for x in checks));print('disagree',[x for x in checks if not x['agree']])
p=pdf[639];words=p.get_text('words');first=[w for w in words if 254<w[0]<260 and 110<w[1]<127 and w[4]in('Leiosphaeridia','Veryhachium')];out=[]
for d in (5250,5320,5340,5400):
 label=f"{d:.2f}'";dw=min([w for w in words if w[4]==label],key=lambda w:(w[1],w[0]));y=(dw[1]+dw[3])/2
 for h in first:
  x=(h[0]+h[2])/2;pix=p.get_pixmap(matrix=pymupdf.Matrix(24,24),clip=pymupdf.Rect(x-.45,y-.28,x+.45,y+.28),alpha=False);v=pix.samples
  c=sum(v[i+2]>100 and v[i+2]>v[i]+40 for i in range(0,len(v),pix.n));out.append(dict(well='I3-NC186',depth_ft=d,header=h[4],header_x=x,marine_pixels=c,mark_present=c>3))
(root/'i3_ash_marine_pixels.json').write_text(json.dumps(out,indent=2));print('I3 Ash marks by row',[(d,sum(x['mark_present']for x in out if x['depth_ft']==d))for d in (5250,5320,5340,5400)])
