from pathlib import Path
import csv, hashlib, json, re, zipfile
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
source_hashes = json.load((OUT/'source_hashes.json').open())
for entry in source_hashes:
    assert hashlib.sha256((ROOT/entry['file']).read_bytes()).hexdigest() == entry['registered_sha256'], entry['file']
NS = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def write_csv(name, rows):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)

xlsx = ROOT / 'library/closed/wang2022_tier2_SI1.xlsx'
with zipfile.ZipFile(xlsx) as z:
    shared = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
    sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    sheet_rows = sheet.findall('s:sheetData/s:row', NS)
    parsed = []
    for row in sheet_rows:
        cells = {}
        for cell in row.findall('s:c', NS):
            value = cell.find('s:v', NS)
            text = '' if value is None else value.text or ''
            if cell.get('t') == 's' and text:
                text = shared[int(text)]
            cells[re.sub(r'\d+', '', cell.get('r'))] = text
        if cells.get('A', '').startswith('PB'):
            parsed.append((int(row.get('r')), cells))
cryptotaxa = {'Adinosporus bullatus','Adinosporus geminus','Adinosporus voluminosus','Spissuspora laevigata','Vidalgea masculata'}
specimens = []
for n, cells in parsed:
    original = cells['B']
    prefix = re.match(r'(LGZZSD-Y\d+)', original).group(1)
    specimens.append(dict(source='Wang2022_SI1',sheet='Sheet1',row=n,specimen_no=cells['A'],original_collection_no=original,taxon_literal=cells['C'],locality_literal=cells['D'],horizon_literal=cells['E'],inferred_collection_prefix=prefix,prefix_status='inferred from original collection number; no full sample roster',named_cambrian_cryptospore_sensu_lato='yes' if cells['C'].strip() in cryptotaxa else 'no',quantitative_status='specimen catalogue; no random or exhaustive sample-count denominator',source_locator=f'Sheet1!A{n}:E{n}'))
assert len(specimens) == 463
assert len({x['specimen_no'] for x in specimens}) == len({x['original_collection_no'] for x in specimens}) == 463
write_csv('wang2022_specimen_catalogue.csv', specimens)
summary = []
for prefix in sorted({x['inferred_collection_prefix'] for x in specimens}):
    rr = [x for x in specimens if x['inferred_collection_prefix'] == prefix]
    crypton = sum(x['named_cambrian_cryptospore_sensu_lato'] == 'yes' for x in rr)
    acro = sum(x['taxon_literal'].strip().startswith(('Leiosphaeridia','Synsphaeridium','Symplassosphaeridium')) for x in rr)
    summary.append(dict(collection_prefix=prefix,catalogue_records=len(rr),named_cambrian_cryptospore_records=crypton,named_sphaeromorph_acritarch_records=acro,other_records=len(rr)-crypton-acro,identity_status='inferred prefix; not authenticated as complete processed-material inventory',e2_main='affinity alternative; no secure embryophyte identification inferred',e2_inclusive='named Cambrian cryptospore-like forms present',productivity='co-catalogued acritarchs; catalogue does not establish full processing/effort scope',reference='Wang2022 SI1 Sheet1'))
assert [x['catalogue_records'] for x in summary] == [72,363,28]
write_csv('wang2022_prefix_summary.csv', summary)
write_csv('wang2022_catalogue_taxon_counts.csv', [dict(taxon_literal=k,catalogue_records=v) for k,v in sorted(Counter(x['taxon_literal'] for x in specimens).items())])
composition=[]
for label,pct in [('cryptospores','15.4'),('clustered forms','31.5'),('acritarchs','20.1'),('filaments','30.3'),('other indeterminate specimens','2.7')]:
    compatible = [n for n in range(257) if (Decimal(100*n)/Decimal(256)).quantize(Decimal('0.1'),rounding=ROUND_HALF_UP)==Decimal(pct)]
    composition.append(dict(group_literal=label,percentage_literal=pct,reported_total_specimens=256,sample_identifier='not reported',integer_counts_compatible_with_reported_percentage=';'.join(map(str,compatible)) if compatible else 'none',status='preserve published percentages; do not reconstruct counts or map to catalogue prefixes',source_locator='Wang2022 p.2 section 3'))
write_csv('wang2022_reported_composition.csv',composition)

tennessee=[]
for sample,area,form,age,plates,notes in [
('J2-1518','JOY No. 2 core, eastern Tennessee','Rogersville Shale','Series 3 Stage 5 (figure estimate)','Plate I 12-13',''),
('J2-1541','JOY No. 2 core, eastern Tennessee','Rogersville Shale','Series 3 Stage 5 (figure estimate)','Plate I 26',''),
('J2-1571','JOY No. 2 core, eastern Tennessee','Rogersville Shale','Series 3 Stage 5 (figure estimate)','Plate I 3-4,11,14; Plate II 1-2','Plate II 1-2 print slide J2-1517/B alongside sample J2-1571; retain discrepancy, no new unit'),
('J2-1578','JOY No. 2 core, eastern Tennessee','Rogersville Shale','Series 3 Stage 5 (figure estimate)','Plate I 5,10,15-18; Plate II 3,6,10-11',''),
('J2-1580s','JOY No. 2 core, eastern Tennessee','Rogersville Shale','Series 3 Stage 5 (figure estimate)','Plate I 2','s suffix denotes Sheffield-processed split; do not add as independent material'),
('J2-1587s','JOY No. 2 core, eastern Tennessee','Rogersville Shale','Series 3 Stage 5 (figure estimate)','Plate I 1,6-7','s suffix denotes Sheffield-processed split; do not add as independent material'),
('J2-1803','JOY No. 2 core, eastern Tennessee','Pumpkin Valley Shale','Series 3 Stage 5 (figure estimate)','Plate V 1-18','50-specimen size population from slide J2-1803/A3 is taxon morphometrics, not sample productivity denominator'),
('SB01-14','Thorn Hill section, eastern Tennessee','Rome Formation','Series 2, Stage 4 in text p.33; Fig.1 caption: Olenellus biozone, probably Series 2 (521.0-506.5 Ma if Stage 4 not accepted)','Plate II 4-5','No authenticated allocation before 515.5 Ma from broad Series 2 constraint'),
('SB01-17','Thorn Hill section, eastern Tennessee','Rogersville Shale','Series 3 Stage 5 (figure estimate)','Plate I 8-9; Plate II 7-8',''),
('GC96-10A','Thunder Falls, Tapeats Creek drainage, Grand Canyon, Arizona','Bright Angel Shale','Series 3 Stage 5 probable (Fig.1 caption)','Plate II 12','Methods give GC96-10A; Plate II 12 prints GC96-10. Probable linked material, spelling not silently repaired'),
('GC10-3','Red Canyon section, Grand Canyon, Arizona','Bright Angel Shale','Series 3 Stage 5 probable (Fig.1 caption)','Plate II 9','')]:
    tennessee.append(dict(sample_identifier_literal=sample,material_group=area,formation=form,reported_age=age,illustration_locator=plates,inventory_scope='eleven sample identifiers stated as sources for plate illustrations only',e2_author_reading='cryptospores sensu lato; aeroterrestrial charophytic origin',e2_main='no secure embryophyte assignment inferred',e2_inclusive='cryptospore-like forms reported',independent_productivity_status='not established sample by sample independently of focal spore-like material',admission='source lead only; no complete searched-material denominator',notes=notes,source_locator='Strother2016 p.30 methods; p.32 Fig.1 and preparation; plate captions'))
assert len(tennessee)==11
write_csv('strother2016_plate_source_inventory.csv',tennessee)

argentina=[]
ids=['7586','7587','7585','7999','8000','7584','7596','7595','7588','7589']
for n,sid in enumerate(ids,1):
    if sid in ['7586','7587','7585','7999','8000']:
        formation='Zanjon Formation and transition to Laja Morada Member'
        age='early to middle Dapingian (2010 p.367); 7999 middle Dapingian in SI Note S1'
    elif sid=='7584':
        formation='Laja Morada Member, Labrado Formation'; age='Dapingian in 2010 Fig.1; 2011 does not tightly date this low-diversity sample'
    elif sid in ['7596','7595']:
        formation='Lagunilla Member, Labrado Formation'; age='Dapingian in 2010 Fig.1; probably Dapingian in 2011'
    else:
        formation='Capillas Formation'; age='Darriwilian; basal stage boundary marked uncertain in 2010 Fig.1'
    glyph='cryptospore symbol' if sid=='7999' else 'question-mark cryptospore symbol' if sid in ['7596','7595','7588','7589'] else 'no cryptospore symbol plotted'
    argentina.append(dict(sample_id=sid,stratigraphic_order_base_to_top=n,formation=formation,age_source_reading=age,source2010='Fig.1; SI Note S1',source2010_detailed_target_report='five taxa from sample 7999 (p.367; Fig.2)' if sid=='7999' else 'not individually taxonomically resolved',source2010_figure_symbol=glyph,source2010_si_literal_scope='all ten samples said to yield cryptospores and other palynomorph groups',source2011_same_material='yes' if n>5 else 'not included',source2011_quantitative_table='Fig.6' if n>5 else '',e2_main='uncertain; no secure E2 binary assigned',e2_inclusive='reported spore-like forms; table/text ambiguity remains' if n>5 else 'reported broad cryptospores; only 7999 taxonomically detailed',zero_inferred='no',notes='2010 laboratory duplicate is technical preparation, not another material unit' if sid=='7999' else ''))
write_csv('argentina_material_crosswalk.csv',argentina)

sample_order=['7584','7596','7595','7588','7589']
table=[
('Cymatiosphaera',['12.5','1.4','2.3','-','-']),
('Leiosphaeridia',['87.5','35.1','40.8','50.7','17.5']),
('cf. Aremoricanium',['-','1.4','-','-','-']),
('Dictyotidium?',['-','5.4','4.6','-','-']),
('Aremoricanium',['-','-','2.3','-','-']),
('Acritarch gen. et sp. indet.',['-','-','17.7','7.2','-']),
('Veryhachium',['-','-','2.3','1.4','6.0']),
('Ferromia?',['-','-','-','2.9','-']),
('Polygonium',['-','-','-','27.5','39.8']),
('Acanthodiacrodium',['-','-','-','1.4','2.4']),
('Ampullula?',['-','-','-','-','-']),
('Arbusculidium',['-','-','-','-','0.6']),
('Arkonia',['-','-','-','-','3.6']),
('Barakella',['-','-','-','-','1.2']),
('Cymatiogalea',['-','-','-','-','0.6']),
('Ericanthea',['-','-','-','-','0.6']),
('Eupoikilofusa',['-','-','-','-','0.6']),
('Liliosphaeridium',['-','-','-','-','1.2']),
('Michrystridium',['-','-','-','1.4','6.6']),
('Pterospermella',['-','-','-','-','1.2']),
('Rhopaliophora',['-','-','-','-','1.2']),
('Striatotheca',['-','-','-','-','1.2']),
('Tectitheca',['-','-','-','-','1.2']),
('Incertae sedis',['-','56.8','30.0','7.2','13.9']),
('?Morphon D. murusattenuata',['-','-','-','-','0.6'])]
quant=[]
for taxon,vals in table:
    for sid,v in zip(sample_order,vals):
        quant.append(dict(sample_id=sid,taxon_literal=taxon,reported_percentage_literal=v,cell_semantics='source dash; not converted to an E2 non-detection' if v=='-' else 'reported relative abundance',source_locator='Rubinstein2011 p.129 Fig.6',transcription_notes='Decimal comma printed as 7,2 in source' if taxon=='Acritarch gen. et sp. indet.' and sid=='7588' else ''))
assert len(quant)==125
write_csv('rubinstein2011_fig6_percentages.csv',quant)
qsummary=[]
for sid,ncount,div,slides in zip(sample_order,[8,74,130,69,166],[2,5,8,9,21],[3,3,1,3,1]):
    vals=[r for r in quant if r['sample_id']==sid]
    total=sum(Decimal(r['reported_percentage_literal']) for r in vals if r['reported_percentage_literal']!='-')
    qsummary.append(dict(sample_id=sid,total_counted_specimens=ncount,total_species_diversity=div,slides_counted=slides,percentage_sum=str(total),independent_nontarget_recovery='yes; named marine palynomorphs in quantitative table',e2_broad_report='Incertae sedis and/or questionably assigned dyad' if sid!='7584' else 'no spore-like table entry; conflicts with general all-levels prose',e2_strict_report='uncertain; no secure positive or searched-negative coding',source_locator='Rubinstein2011 p.129 Fig.6 and caption'))
write_csv('rubinstein2011_quantitative_sample_summary.csv',qsummary)

checks={
 'source_hashes_match':True,
 'wang_xml_rows_including_header_and_styled_blanks':len(sheet_rows),
 'wang_nonblank_specimen_records':len(specimens),
 'wang_unique_specimen_ids':len({x['specimen_no'] for x in specimens}),
 'wang_unique_original_ids':len({x['original_collection_no'] for x in specimens}),
 'wang_prefix_counts':{x['collection_prefix']:x['catalogue_records'] for x in summary},
 'wang_named_cambrian_cryptospore_records':sum(x['named_cambrian_cryptospore_sensu_lato']=='yes' for x in specimens),
 'wang_named_cryptospore_taxa_n':len(cryptotaxa),
 'wang_percentage_compatibility':{x['group_literal']:x['integer_counts_compatible_with_reported_percentage'] for x in composition},
 'tennessee_plate_source_identifiers':len(tennessee),
 'argentina_unique_material_identifiers':len(argentina),
 'argentina_2011_overlap_materials':sum(x['source2011_same_material']=='yes' for x in argentina),
 'argentina_fig6_cells':len(quant),
 'argentina_fig6_percentage_sums':{x['sample_id']:x['percentage_sum'] for x in qsummary},
 'argentina_fig6_reported_specimen_total':sum(x['total_counted_specimens'] for x in qsummary),
 'binary_e2_zeros_created':0,
 'integration':'Derived evidence only; raw sources unchanged',
}
(OUT/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps(checks,indent=2))
