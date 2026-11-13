import csv, hashlib, json, math
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent

def rows(p,delimiter=','):
 with (ROOT/p).open(newline='') as f: return list(csv.DictReader(f,delimiter=delimiter))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator="\n"); w.writeheader(); w.writerows(data)

integrity=[]
def check(rel,expected,register,limitation=''):
 p=ROOT/rel; actual=sha(p)
 integrity.append(dict(path=rel,bytes=p.stat().st_size,sha256=actual,registered_sha256=expected,match=actual==expected,register=register,verification_scope=limitation or 'Current local file matches held register; no re-download'))
 assert actual==expected,rel

used={
'data/eprp/record/pbdb_plant_occurrences.csv','data/eprp/record/pbdb_plant_collections.csv','data/eprp/record/pbdb_plant_references.csv',
'data/external/gbdb/gbdb_plant_fossils.csv','data/external/gbdb/gbdb_plant_sections.csv','data/external/gbdb/gbdb_window_sections_all.csv',
'data/external/gbdb/gbdb_plant_no_age_candidates.csv','data/external/gbdb/gbdb_plant_fossils_table_only.csv',
'data/external/gbdb/provenance.tsv','data/external/gbdb/gbdb_fields.csv'}
for manifest,base in [('data/eprp/record/MANIFEST.tsv','data/eprp'),('data/external/gbdb/MANIFEST.tsv','data/external')]:
 for r in rows(manifest,'\t'):
  rel=str(Path(base)/r['path'])
  if rel in used:
   check(rel,r['sha256'],manifest,'Held derived extract hash verified. Remote upstream snapshot/member bytes not re-read in this bounded local audit.')
check('data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv','e0d1f772c1617c218948d1d2605661e93edcfe75e0fe8ce92afee91d3350a8b8','data/occurrences/README.md:91-95')
pdfs=['closed/edwardsfeehan1980.pdf','closed/libertin2018.pdf','closed/libertin2018_SI.pdf','closed/al1983_oup.pdf','closed/libertin2018a_tier2.pdf','closed/strulluderrien2010.pdf']
registry=rows('library/closed.tsv','\t')
for rel in pdfs:
 hits=[r for r in registry if r['file']==rel]; assert len(hits)==1,rel
 check('library/'+rel,hits[0]['sha256'],'library/closed.tsv',('Held PDF hash matches register; supplement original acquisition route unproven' if rel.endswith('_SI.pdf') else 'Held PDF hash matches register'))
write('source_integrity.csv',integrity)
assert {r['path'] for r in integrity}.issuperset(used)

pbdo=rows('data/eprp/record/pbdb_plant_occurrences.csv'); pbdc=rows('data/eprp/record/pbdb_plant_collections.csv'); pbdr=rows('data/eprp/record/pbdb_plant_references.csv')
pbda=rows('data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv')
gbdf=rows('data/external/gbdb/gbdb_plant_fossils.csv'); gbds=rows('data/external/gbdb/gbdb_plant_sections.csv'); gbda=rows('data/external/gbdb/gbdb_window_sections_all.csv')
gbdn=rows('data/external/gbdb/gbdb_plant_no_age_candidates.csv'); gbdt=rows('data/external/gbdb/gbdb_plant_fossils_table_only.csv')

def uniq(rs,k): return len({r[k] for r in rs if r[k].strip()})
def blank(r,k): return not r[k].strip()
summary=[]
def add(file,rs,grain,coverage,keys,gap):
 summary.append(dict(path=file,rows=len(rs),record_grain=grain,coverage=coverage,key_counts=keys,admission='not_admitted_as_E3_trial_denominator',missing_denominator=gap))
add('data/eprp/record/pbdb_plant_occurrences.csv',pbdo,'taxon occurrence assigned to a PBDB collection; not a specimen or searched-material unit','Plant-filter-selected public occurrence rows overlapping 485-383 Ma in 2026-10-23 snapshot',f"collections={uniq(pbdo,'collection_no')}; occurrence_ids={uniq(pbdo,'occurrence_no')}; cited_references={uniq(pbdo,'reference_no')}; core_rows={sum(r['d_in_core']=='yes' for r in pbdo)}",'Selected on plant-record presence; no complete field-search list or E3-negative search declaration')
add('data/eprp/record/pbdb_plant_collections.csv',pbdc,'database collection; potentially pooled taxa, horizons or collecting visits','Collections selected through the plant occurrence filter',f"collection_ids={uniq(pbdc,'collection_no')}; primary_references={uniq(pbdc,'reference_no')}",'Plant-selected frame; collection size/coverage fields need primary verification; no event-specific completeness contract')
add('data/eprp/record/pbdb_plant_references.csv',pbdr,'publication/reference','References cited by plant occurrences or primary collection records',f"reference_ids={uniq(pbdr,'reference_no')}",'Repeated publications and re-examinations are not independent trials')
add('data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv',pbda,'database collection from an all-taxon query','Darriwilian-Emsian interval query retrieved 2026-10-28; collection-level location/stratigraphy/environment fields',f"collection_ids={uniq(pbda,'collection_no')}; primary_references={uniq(pbda,'reference_no')}",'Independent of plant filter but selected on database fossil collections, not declared compression-search opportunities. Query lacks collection_methods, collection_coverage, collection_size and rock_censused; omission is not a searched negative')
add('data/external/gbdb/gbdb_plant_fossils.csv',gbdf,'sections-workbook taxon-list row, with optional fossils-workbook joins','485-383 Ma on GBDB ages plus 2 younger anchor rows; core and flagged',f"sections={uniq(gbdf,'sectionID')}; units={uniq(gbdf,'unit_id')}; references={uniq(gbdf,'ReferenceID')}; core_rows={sum(r['derived_in_core']=='yes' for r in gbdf)}",'Presence-selected records; list entries are not specimens or complete collections; weak formation-level ages and taxonomic flags')
add('data/external/gbdb/gbdb_plant_sections.csv',gbds,'section x formation entry x unit','All units of sections selected by retained plant records, including out-of-window units',f"sections={uniq(gbds,'sectionID')}; nonblank_unit_id_labels={uniq(gbds,'unit_id')}; composite_section_formation_unit_rows={len({(r['sectionID'],r['fromation_id'],r['unit_id']) for r in gbds})}; missing_unit_id_rows={sum(not r['unit_id'] for r in gbds)}; zero_core_record_rows={sum(float(r['derived_n_core_plant_records_window_or_anchor'])==0 for r in gbds)}",'A zero plant count means no recorded taxon row under this filter; no proof that the unit was searched for megafossils; section selection depends on plant record')
add('data/external/gbdb/gbdb_window_sections_all.csv',gbda,'section summary with taxon/collection/unit counts','All sections containing at least one unit aged within 485-383 Ma on GBDB scale',f"sections={uniq(gbda,'sectionID')}; summed_window_units={sum(int(r['derived_n_units_window']) for r in gbda)}; zero_core_record_sections={sum(int(r['derived_n_plants_core'])==0 for r in gbda)}",'Summary covers all fossil groups but lacks sampled-negative unit inventory, megafossil search method/effort and complete event reporting')
add('data/external/gbdb/gbdb_plant_no_age_candidates.csv',gbdn,'taxon-list row without numeric age','Potential window plants selected using reference/title/name information',f"sections={uniq(gbdn,'sectionID')}; references={uniq(gbdn,'ReferenceID')}",'No numeric age and no searched-material denominator; cannot assign older/reference trials')
add('data/external/gbdb/gbdb_plant_fossils_table_only.csv',gbdt,'fossils-workbook row without a matching sections row','Plant-classified unmatched rows; no age available','', 'No age or shared section key and no search-negative inventory')
write('database_grain_coverage.csv',summary)

coverage=[]
for rel,rs,fields in [
 ('data/eprp/record/pbdb_plant_collections.csv',pbdc,['localsection','localbed','localbedunit','environment','collection_type','collection_methods','collection_coverage','collection_size','rock_censused','collection_dates','collection_comments']),
 ('data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv',pbda,['localsection','localbed','localbedunit','environment','collection_type','collection_methods','collection_coverage','collection_size','rock_censused']),
 ('data/external/gbdb/gbdb_plant_sections.csv',gbds,['unit_no','bed','Thickness','ThicknessUnit','Facies','Environment','Details','derived_reference_ids']),
 ('data/external/gbdb/gbdb_plant_fossils.csv',gbdf,['CollectionNo','collection_depthlower','collection_depthupper','collection_thicknessunit','early_age','late_age','derived_flag','ReferenceID'])]:
 for field in fields:
  present=field in rs[0]
  nonblank=sum(bool(r[field].strip()) for r in rs) if present else None
  counts=Counter(r[field] for r in rs if r[field].strip()) if present else Counter()
  coverage.append(dict(path=rel,field=field,field_present=present,rows=len(rs),nonblank=nonblank,top_values=json.dumps(counts.most_common(5),ensure_ascii=False),interpretation='Field population is not validation of E3 search/reporting completeness'))
write('field_coverage.csv',coverage)

irish=[r for r in pbdc if r['collection_no']=='10594']; assert len(irish)==1
write('pbdb_irish_collection_10594.csv',irish)
write('pbdb_rock_censused_metadata.csv',[dict(collection_no=r['collection_no'],reference_no=r['reference_no'],early_interval=r['early_interval'],late_interval=r['late_interval'],rock_censused=r['rock_censused'],collection_coverage=r['collection_coverage'],collection_methods=r['collection_methods'],reftitle=next(x['reftitle'] for x in pbdr if x['reference_no']==r['reference_no']),scope='Metadata inventory only; no additional primary-source admission or source reading') for r in pbdc if r['rock_censused']])
write('pbdb_irish_occurrences_10594.csv',[r for r in pbdo if r['collection_no']=='10594'])
write('pbdb_irish_references.csv',[r for r in pbdr if r['reference_no'] in ['3918','3940']])

prospective=[]
for p in [.01,.05,.10,.20,.50]:
 n=math.ceil(math.log(.05)/math.log1p(-p))
 prospective.append(dict(conditional_per_independent_block_detection=p,alpha=.05,independent_blocks_required=n,zero_detection_probability=(1-p)**n,previous_n_probability=(1-p)**(n-1),status='hypothetical_design_scenario_not_fitted_from_current_sources',assumptions='Known per-block detection probability under the specified lineage/persistence scenario; independent blocks; complete search and reporting; preselected comparable facies; defensible older-age assignment; no claim about crown-node timing'))
write('prospective_scenarios.csv',prospective)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'base_commit':'d17d033cc2bb7f083a61e31228d30919f2406beb','inputs_checked':len(integrity),'input_hashes':{r['path']:r['sha256'] for r in integrity},'upstream_limit':'PBDB EPRP remote raw and GBDB remote workbooks not re-opened; held derivative hashes checked against manifests. All-taxon PBDB raw CSV checked locally.','no_network_acquisition':True,'integration':'Parent integrated derived evidence during authorised sprint2','outputs':{str(p.relative_to(OUT)):sha(p) for p in OUT.glob('*.csv')},'code_sha256':{p.name:sha(p) for p in [Path(__file__)]},'definition_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'docs/sprint2-source-roster.md',ROOT/'docs/f3-shape.md',ROOT/'data/eprp/record/README.md',ROOT/'data/external/gbdb/README.md',ROOT/'data/occurrences/README.md',ROOT/'data/eprp/record/MANIFEST.tsv',ROOT/'data/external/gbdb/MANIFEST.tsv',ROOT/'library/closed.tsv']},'review_sha256':sha(ROOT/'docs/audits/2026-10-31-sprint2-m3.md'),'selection_criteria_sha256':sha(OUT/'selection-criteria.md')}
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'inputs_verified':len(integrity),'rows':[(r['path'],r['rows'],r['key_counts']) for r in summary]},indent=2))
