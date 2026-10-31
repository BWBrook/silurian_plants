from pathlib import Path
import sys
import pymupdf,csv,re,hashlib,json,collections
root=Path(sys.argv[1]);root.mkdir(parents=True,exist_ok=True);repo=Path(__file__).resolve().parents[3];base=repo/'data/units'
pdf=pymupdf.open(repo/'library/closed/abuhmida2013-thesis-related_macbook20261030.pdf')
rows=list(csv.DictReader((base/'libya_chart_reports.csv').open()))
checks=[];headers=[]
for num,well in ((630,'A28i-NC186'),(632,'B2-NC186'),(634,'D1-200'),(636,'E1-NC174'),(638,'H2-NC186'),(640,'I3-NC186')):
 page=pdf[num-1];words=page.get_text('words');hs=[w for w in words if w[4]=='Ambitisporites' and w[1]<350];dils=[w for w in words if w[4]=='dilutus' and w[1]<350]
 headers.append({'well':well,'target_header_count_upper':len(hs),'dilutus_tokens_upper':len(dils)})
 if not hs:continue
 assert len(hs)==len(dils)==1
 h=hs[0];x=(h[0]+h[2])/2
 assert abs(x-(dils[0][0]+dils[0][2])/2)<.01
 for row in [r for r in rows if r['well']==well]:
  label=f"{float(row['depth_ft']):.2f}'"
  matches=[w for w in words if w[4]==label]
  m=min(matches,key=lambda w:(w[1],w[0]));y=(m[1]+m[3])/2
  pix=page.get_pixmap(matrix=pymupdf.Matrix(24,24),clip=pymupdf.Rect(x-.45,y-.28,x+.45,y+.28),alpha=False)
  samples=pix.samples;greens=sum(samples[i+1]>80 and samples[i+1]>samples[i]+40 and samples[i+1]>samples[i+2]+40 for i in range(0,len(samples),pix.n))
  raster='mark-present' if greens>3 else 'no-mark'
  checks.append({'well':well,'depth_ft':row['depth_ft'],'raster_green_pixels':greens,'raster_status':raster,'csv_status':row['ambitisporites_dilutus_report'],'agree':raster==row['ambitisporites_dilutus_report']})
with(root/'raster_target_checks.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]),lineterminator='\n');w.writeheader();w.writerows(checks)
a=list(csv.DictReader((base/'libya_appendix1.csv').open()));e=list(csv.DictReader((base/'libya_enclosures.csv').open()))
key=lambda r:(r['well'],float(r['depth_ft']))
ak={key(r):r for r in a};ek={key(r):r for r in e};rk={key(r):r for r in rows}
receipt=json.loads((base/'libya_chart_receipt.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashes={'source':sha(repo/receipt['source_path'])==receipt['source_sha256'],'script':sha(repo/'tools/libya_charts.py')==receipt['script_sha256']}
for k,v in (receipt['input_sha256']|receipt['output_sha256']).items():hashes[k]=sha(base/k)==v
summary={'raster_checks':len(checks),'raster_agree':sum(x['agree']for x in checks),'raster_mark_counts':dict(collections.Counter(x['raster_status']for x in checks)),'target_headers':headers,'hashes_match':hashes,'chart_rows':len(rows),'unique_chart_keys':len(rk),'exact_appendix_keys':len(set(ak)&set(rk)),'appendix_only':sorted(set(ak)-set(rk)),'chart_only':sorted(set(rk)-set(ak)),'enclosure_keys_and_types_match':set(ek)==set(rk) and all(ek[k]['type_code']==rk[k]['type_code']for k in rk),'appendix_join_flag_mismatches':[key(r)for r in rows if (r['exact_appendix_match']=='yes')!=(key(r)in ak)],'all_blank_rows':[{k:r[k]for k in('well','depth_ft','type_code')}for r in rows if int(r['total_symbols'])==0],'core_target_marks':[key(r)for r in rows if r['ambitisporites_dilutus_report']=='mark-present' and key(r)in ak and ak[key(r)]['type']=='Core'],'scope':'Independent rendered-pixel target detection, header check and CSV/source receipt joins; no production extractor imported or called.'}
(root/'independent_receipt.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2));print('Raster disagreements:',[x for x in checks if not x['agree']])
