# C56 independent check: outside rulers

Reviewer: Codex (OpenAI), 13 November 2026. Reviewed source state: `75f2bb0`.

## Verdict

**The defined proxy calculations pass an independent numerical and input-table check. Retain C56 as
provisional as written until its maximum is restricted to the intended 444–452 Ma interval and the
Results (g) comparison is expressed as numerical correspondence, rather than proxy sufficiency.**
After these bounded wording changes, C56 can be supported for its declared descriptive estimand:
time-weighted ratios of the named proxies, and the algebraic independent-count equivalents. This
review supplies no evidence that these proxies measure the body-fossil finding rate.

Only this audit was edited. No canonical data were rebuilt; no source tables, code, claims or products
were changed. The review did not inspect private outreach material or contact anyone.

## Findings and disposition

| Finding | Evidence and implication | Recommended disposition | Owner |
|---|---|---|---|
| C56's maximum lacks its domain | “largest among the computed candidate ages 3.5031 at 445.5 Ma” is false for the full computed 427–456 Ma grid: Q is infinite at 427–428 Ma and 66.3962 at 428.5 Ma. The stated 3.5031 maximum is correct **within 444–452 Ma**. | Add that interval to the ledger wording. | Integrator |
| Results (g) shifts from proxy magnitude to sufficiency | “Rock alone matches the reduction needed” and “the spore share alone” can be read as saying either factor supplies the required body-record reduction. No transfer relationship from North American column area or global trilete-reporting share to the global crown-vascular-body finding rate was estimated. The heading “Outside measures reach the cautious requirements” encourages the same reading. | State that the ratios are **numerically as large as** the required finding-rate ratios for the stated counts, explicitly as a comparison of magnitudes. Avoid describing a proxy as sufficient or explanatory. Retain the zero-delay and no-confidence-status limits. | Integrator |
| Rock wording should retain its actual object | Methods (h) and S5.8 accurately define column area. Results (g)'s “mapped non-marine rock ... covers ... area” can imply measured outcrop or rock surface area. The input is summed area of active columns holding a qualifying unit, not the mapped area of that unit's outcrop. | Use “mean area of columns holding non-marine units” or equivalent. | Integrator |
| “Distinct documents” means distinct database IDs | Distinct TDOC identifiers correctly remove taxon-row and cross-region repetition, but the source index contains duplicate publication entries. Fifteen exact normalized-title/year/author pairs were found; three touch the usable trilete numerator. Merging all fifteen as a bounded sensitivity changes Q from 5.14034/7.10489 to 5.13446/7.09547, less than 0.14%. | Clarify “distinct Palynodata document IDs” in the methodological description; no broad source cleanup is needed for C56. | Integrator |
| Four decimal places exceed the rock integration accuracy | `rulers.py` uses midpoint quadrature at 0.01 Myr. Exact integration of the input interval steps gives rock Q 3.293788/3.188699 rather than 3.2941/3.1889, and n 20.41446/13.99106 rather than 20.42/13.99. Across the full grid the largest absolute Q error is 0.004872 at 439.5 Ma. | Treat the four-decimal ledger values as approximate computed outputs. Published table precision and all count comparisons are unaffected. Exact interval integration is optional, not a scientific blocker. | Integrator |

An allowed replacement for the key Results sentence is: “The rock ratios are numerically as large as
the required finding-rate ratios for about 14–20 or fewer independent finds, and the spore-reporting
ratios for about 29–31 or fewer; neither proxy estimates the body-record finding rate.” The
comparison is scientifically useful as scale context, provided that conditional analogy remains
explicit. Averaging each proxy over exactly the same two windows is appropriate for that comparison.
If a proxy were proportional to finding intensity throughout both windows, its ratio of means would
also yield the relevant ratio of integrated intensities. That proportionality is the unverified link.

## Independent numerical results

I integrated each piecewise-constant input exactly over the window intersections, without importing
or executing `rulers.py`. The later interval is 393.47–426.7 Ma, duration 33.23 Myr. The earlier
intervals are 426.7–444 Ma and 426.7–452 Ma, durations 17.3 and 25.3 Myr. For stage series the weight
is the overlap duration, not one vote per stage and not a pooled fraction of all stage counts.
Macrostrat uses its individual unit endpoints and distinct active column IDs at every interval.

| Proxy | Exact Q at 444 Ma | Exact Q at 452 Ma | Exact largest n, 444 / 452 Ma |
|---|---:|---:|---:|
| North America non-marine column area | 3.293788 | 3.188699 | 20.41446 / 13.99106 |
| North America non-marine or mixed column area | 3.391920 | 3.414916 | 20.98012 / 14.88436 |
| North America non-marine unit count | 1.796357 | 2.226470 | 11.77105 / 10.18506 |
| South America non-marine or mixed column area | 1.009079 | 0.780794 | 7.20078 / 4.40145 |
| Global PBDB land and marginal collections | 1.352814 | 1.414318 | 9.20113 / 6.95561 |
| Same, plant-filter matches removed | 1.068487 | 1.120474 | 7.54735 / 5.77774 |
| Palynodata usable, non-rejected trilete document-ID share | 5.140343 | 7.104890 | 31.05250 / 29.42814 |

The exact non-marine-area maximum among stored candidate ages **within 444–452 Ma** is 3.502742 at
445.5 Ma. All published two-decimal proxy ratios and one-decimal matching counts agree with the
independent results, apart from immaterial rounding at the second decimal of the unrounded rock n.

The inversion has a closed form. With L = A − c, D = t − A and alpha = 0.05,

    n_max = −log(alpha) / log(1 + D / (Q L)).

This independently confirms the bisection in `rulers_matching_n.csv`. Its values are continuous
algebraic equivalents, not estimated counts; for an integer count the largest qualifying count is its
floor. The comparison concerns zero delay only.

## Input identity, coverage and plan adherence

- The Macrostrat input's SHA-256 is
  `8a0d36ba4304ba5562b331a69919d1b8ef1f061a1bd8e569ac80faa22098b788`, matching
  `data/eprp/record/MANIFEST.tsv`. The registered source is the Macrostrat API v2.5.0 snapshot
  `2026-10-25T0011Z_url`. North America, active status and `non-marine` match the plan, as do the
  `both` variant and secondary South America calculation. There are 54 qualifying North American
  input units in 36 columns, of which 29 overlap 393.47–456 Ma. Distinct-column area prevents
  simultaneous units in one column from inflating area. The unit-count variant intentionally counts
  those units separately. Gaps in qualifying rock are exactly 420.39–428.25 and 443.1–445.2 Ma.
  About 99% of the later area-time is Early Devonian, so the ruler mostly contrasts that later rock
  inventory with a sparse older record. It is not global rock availability.
- The held raw PBDB collection file, the plant-filter collection file, the reviewed effort table and
  the timescale all match `data/macro/build_receipt.json`. Independently allocating the age-range
  overlap of the 27,830 unique raw collections reproduces all fifteen global stage collection
  equivalents to within 1.71e-13. Filtering to the declared land/marginal environment sets and removing
  plant-filter IDs reproduces both series. This matches the pre-specified proxy. The older comparison
  windows are dominated by marginal environments: 184.86 marginal versus 12.84 land collection
  equivalents at 444 Ma, and 260.75 versus 14.00 at 452 Ma. Plant exclusion does not establish
  response-independent effort, as the repository already states.
- The raw Palynodata window table's SHA-256 is
  `e2df76f1414b33e4106c5836a02598b7b8522ad5ff0a8b5043b054e9b386b6a1`, matching its manifest.
  The numerator uses only Palynodata, excluding Wellman and post-2006 additions. That matches the
  fixed plan. “2006 version” is the source release label: its registered README notes some citation
  years through 2007, so “2006-version index” is more exact than a literal publication-year cutoff.
- I reconstructed age confidence, range <=25 Myr, known-location and exclusion filters from raw
  Palynodata plus the crosswalks. I then applied trilete classification, reworked/caved and synonym-list
  exclusions and group-over-document vetting. All 27 denominator and trilete numerator stage counts
  match exactly; at every stage the numerator is a subset of the denominator. This verifies the
  correction against the plan independently of `tools/spores.py` execution.

## Spore numerator, duplicates and qualifiers

The corrected numerator comes from 3,676 usable non-rejected raw trilete rows belonging to 288
Palynodata document IDs over the full extracted window. These are not 3,676 samples. For example,
Katian has 24 qualifying taxon rows but five document IDs; Lochkovian has 2,070 rows but 126 IDs.
Summing regional denominators would also inflate the count: Katian would become 498 instead of
417, Homerian 640 instead of 492, Lochkovian 303 instead of 251 and Emsian 125 instead of 103.
The actual global output correctly takes distinct IDs across regions.

At Katian, Hirnantian, Rhuddanian, Homerian and Emsian respectively, the corrected trilete numerator
is 5, 5, 43, 67 and 66 against denominators 417, 307, 482, 492 and 103. The later mean share is
0.5173075085; the earlier means are 0.1006367622 and 0.07281006845. I also reproduced the original
numerator rule, which omitted synonym-list and group-rejection exclusions: its ratios are 4.975571
and 6.671845, confirming the correction history described in S5.8.

There are no literal question marks in surviving raw trilete taxon labels. Palynodata `TIDR=X`
means cf./aff. at genus or species level and is retained in 780 of the qualifying raw rows; it does
not automatically defeat the broad trilete classification. Dropping all X rows as a sensitivity gives
5.209767/7.185290, so it does not explain the reported rise. This is different from a Wellman row
whose taxon itself has a leading question mark. The present review did not adjudicate every cf./aff.
identification from its original paper.

The source-review concern about Burgess (1991) does not enter the corrected Ordovician numerator:
Palynodata 05703's *Ambitisporites vavrdovae*, Hirnantian–Aeronian, has `usable=true` but
`vetting=reject` and is excluded. Its Aeronian–Telychian *A. dilutus* is accepted and retained.
Burgess (1991) document 05704 contributes only Sheinwoodian–Homerian triletes. C56 does not use the
Wellman rows under review for C54.

Three duplicate publication pairs touch the usable trilete numerator: Moreau-Benoit (1994), IDs
18253/17875; Edwards (1995), 18895/18985; Rubinstein (2002), 21884/22139. The first two have
identical author/year/journal/volume/issue/pages as well as normalized titles; the third has the
same journal/title/author/year but a one-page endpoint discrepancy. The sensitivity above merges all
fifteen matching title/year/author pairs, rather than silently deciding that all are accepted merges.

Finally, the pre-specified “non-rejected” set includes doubtful records. All five Katian/Hirnantian
trilete document IDs are doubtful under current vetting; an accepted-or-unvetted-only sensitivity has
zero in those two stages and raises Q to 12.66143/18.51643. This is not the declared ruler and does
not invalidate its arithmetic. It illustrates why reporting share, source vetting and producer
prevalence must not be exchanged as nouns in the interpretation.

## Reproduction

The following independent standard-library check reads the current repository and writes no files.
Save it outside the repository and run it from the repository root. It computes the exact integrals,
closed-form n, raw-document filters and duplicate-ID sensitivities, verifies the source hashes and
reconstructs the PBDB effort table. It imports neither production analysis script.

```python
import csv, math, hashlib, json, collections, re
from pathlib import Path
R=Path.cwd()
def read(p, sep=','):
    with (R/p).open(newline='') as f: return list(csv.DictReader(f,delimiter=sep))
def overlap(a,b,c,d): return max(0,min(b,d)-max(a,c))
st=read('data/timescale.csv'); bounds={r['stage']:(float(st[i-1]['base_ma']) if i else 0,float(r['base_ma'])) for i,r in enumerate(st)}
A,c,alpha=426.7,393.47,.05
units=read('data/eprp/record/macrostrat_units_window.csv')
def rock(env,project='North America',count=False):
    u=[r for r in units if r['j_project_name']==project and r['j_status_code']=='active' and r['d_env_class'] in env]
    def mean(lo,hi):
        knots=sorted({lo,hi}|{float(r[k]) for r in u for k in ['t_age','b_age'] if lo<float(r[k])<hi})
        val=0
        for l,h in zip(knots,knots[1:]):
            x=(l+h)/2; active=[r for r in u if float(r['t_age'])<x<float(r['b_age'])]
            density=len(active) if count else sum({r['col_id']:float(r['j_col_area_km2']) for r in active}.values())
            val+=(h-l)*density
        return val/(hi-lo)
    return mean,u
proxies={}
for key,env,project,count in [('rock_nonmarine_area',{'non-marine'},'North America',False),('rock_nonmarine_both_area',{'non-marine','both'},'North America',False),('rock_nonmarine_count',{'non-marine'},'North America',True),('rock_south_america_area',{'non-marine','both'},'South America',False)]:
    fn,u=rock(env,project,count);proxies[key]=fn
    if key=='rock_nonmarine_area':
        print('NA ROCK',len(u),'units,',len({r['col_id'] for r in u}),'columns;',sum(overlap(c,456,float(r['t_age']),float(r['b_age']))>0 for r in u),'overlap; later area-Myr',fn(c,A)*(A-c))
        print('ROCK LATER STAGE CONTRIBUTIONS',[(name,round(fn(max(c,l),min(A,h))*(min(A,h)-max(c,l)),2)) for name,(l,h) in bounds.items() if overlap(c,A,l,h)>0])
        print('NA rock same-column simultaneous duplicates?',any(len([r for r in u if float(r['t_age'])<s<float(r['b_age'])])>len({r['col_id'] for r in u if float(r['t_age'])<s<float(r['b_age'])}) for s in [c+i*.01 for i in range(round((456-c)/.01))]))
eff=[r for r in read('data/macro/effort_reviewed.csv') if r['region']=='global']
def stage_mean(rows,col,lo,hi):
    return sum(overlap(lo,hi,l,h)*v for l,h,v in rows)/(hi-lo)
for key,col in [('search_all','all_density_per_myr'),('search_plant_excluded','plant_excluded_density_per_myr')]:
    rows=[(float(r['young_ma']),float(r['old_ma']),float(r[col])) for r in eff]
    proxies[key]=lambda lo,hi,rows=rows: stage_mean(rows,None,lo,hi)
spore=read('data/spores/effort_global_by_stage.csv')
rows=[(*bounds[r['stage']],int(r['n_docs_with_triletes'])/int(r['n_docs'])) for r in spore]
proxies['spores_trilete_share']=lambda lo,hi,rows=rows: stage_mean(rows,None,lo,hi)
out=read('models/f3/loop3/out/rulers.csv')
worst={}
for r in out:
    fn=proxies[r['ruler']]; t=float(r['candidate_ma']);den=fn(A,t);q=fn(c,A)/den if den else math.inf
    error=abs(q-float(r['later_to_earlier'])) if math.isfinite(q) else 0
    if error>worst.get(r['ruler'],(0,None))[0]:worst[r['ruler']]=(error,t)
print('EXACT-INTEGRAL vs output maximum absolute Q difference',worst)
for key,fn in proxies.items():
    print('EXACT',key,'later_mean',fn(c,A),[(t,fn(c,A)/fn(A,t), -math.log(alpha)/math.log1p((t-A)/((fn(c,A)/fn(A,t))*(A-c)))) for t in [444,452]])
print('ROCK exact peak on stored candidates',max((proxies['rock_nonmarine_area'](c,A)/proxies['rock_nonmarine_area'](A,float(r['candidate_ma'])),float(r['candidate_ma'])) for r in out if r['ruler']=='rock_nonmarine_area' and float(r['candidate_ma'])>=444))
# Independent raw Palynodata filter, with group verdict overriding document verdict.
raw=read('data/external/spores/palynodata_taxon_window.csv')
age={r['age_name']:r for r in read('data/spores/crosswalks/age_names.csv')}
loc={r['tloc']:r['palaeo_unit'] for r in read('data/spores/crosswalks/locations.csv')}
gen={r['genus']:r['spore_class'] for r in read('data/spores/crosswalks/spore_genera.csv')}
ex={r['doc'] for r in read('data/spores/crosswalks/exclusions.csv')}
dv={r['doc']:r['verdict'] for r in read('data/spores/crosswalks/doc_vetting.csv')}
gv={(r['doc'],r['ics_oldest'],r['ics_youngest'],r['location'],r['class_group']):r['verdict'] for r in read('data/spores/crosswalks/group_vetting.csv')}
sets={s:{k:set() for k in ['all','spores','tri','tri_allow_syn','tri_allow_rej','tri_allow_syn_rej','tri_no_X','tri_no_question','tri_strict']} for s in bounds}
row_counts=collections.Counter();filtered=[]; question=[]; raw_idr=collections.Counter()
for r in raw:
    if r['TDOC'] in ex or loc.get(r['TLOC'],'unknown')=='unknown': continue
    ao=age.get(r['oldage']);ay=age.get(r['youngage'].strip() or r['oldage'])
    if not ao or not ay or ao['confidence'] not in ['high','medium'] or ay['confidence'] not in ['high','medium']:continue
    if ao['ics_oldest'] not in bounds or ay['ics_youngest'] not in bounds:continue
    old=bounds[ao['ics_oldest']][1];young=bounds[ay['ics_youngest']][0]
    if old-young>25:continue
    stages=[s for s,(l,h) in bounds.items() if overlap(l,h,young,old)>0]
    cls=gen.get(r['TGEN'],''); tri=r['TMIC']=='S' and cls.startswith('trilete')
    verdict=gv.get((r['TDOC'],ao['ics_oldest'],ay['ics_youngest'],r['TLOC'],'trilete'),dv.get(r['TDOC'],'not-vetted'))
    no_rework=r['TIDR'] not in ['A','B','C','R']; no_syn=r['TSYN']!='X'; no_rej=verdict!='reject'
    literal_question='?' in (r['TGEN']+' '+r['TSPE']+' '+r['TSSPEC'])
    if tri and no_rework and no_syn and no_rej:
        filtered.append((r,old,young,verdict));raw_idr[r['TIDR']]+=1
        if literal_question: question.append((r['TDOC'],r['TGEN'],r['TSPE'],r['TSSPEC']))
    for s in stages:
        S=sets[s];S['all'].add(r['TDOC'])
        if r['TMIC']=='S' and dv.get(r['TDOC'])!='reject':S['spores'].add(r['TDOC'])
        if tri and no_rework:
            if no_syn and no_rej:
                S['tri'].add(r['TDOC']);row_counts[s]+=1
                if r['TIDR']!='X':S['tri_no_X'].add(r['TDOC'])
                if not literal_question:S['tri_no_question'].add(r['TDOC'])
                if verdict in ['accept','not-vetted','curated']:S['tri_strict'].add(r['TDOC'])
            if no_rej:S['tri_allow_syn'].add(r['TDOC'])
            if no_syn:S['tri_allow_rej'].add(r['TDOC'])
            S['tri_allow_syn_rej'].add(r['TDOC'])
for r in spore:
    s=r['stage'];S=sets[s]
    assert len(S['all'])==int(r['n_docs']),(s,'denom',len(S['all']),r['n_docs'])
    assert len(S['tri'])==int(r['n_docs_with_triletes']),(s,'tri',len(S['tri']),r['n_docs_with_triletes'])
    assert S['tri']<=S['all']
print('RAW SPORE all',len(spore),'stages exactly match denominator and corrected distinct-doc numerator; subset property passes')
print('TRI raw source rows/unique docs',len(filtered),len({r['TDOC'] for r,_,_,_ in filtered}),'TIDR',raw_idr,'literal question taxa',question)
print('SPORE STAGE DETAIL stage/all/tri/rowcounts/allow-syn/allow-rej/allow-both/no-X/no-question/strict')
for r in spore:
    if r['stage'] in ['Katian','Hirnantian','Rhuddanian','Aeronian','Telychian','Sheinwoodian','Homerian','Gorstian','Ludfordian','Pridoli','Lochkovian','Pragian','Emsian']:
        s=r['stage'];S=sets[s];print(s,len(S['all']),len(S['tri']),row_counts[s],*[len(S[k]) for k in ['tri_allow_syn','tri_allow_rej','tri_allow_syn_rej','tri_no_X','tri_no_question','tri_strict']])
for field in ['tri','tri_allow_syn','tri_allow_rej','tri_allow_syn_rej','tri_no_X','tri_no_question','tri_strict']:
    rows=[(*bounds[s],len(d[field])/len(d['all'])) for s,d in sets.items() if len(d['all'])]
    fn=lambda lo,hi: stage_mean(rows,None,lo,hi)
    print('SPORE FILTER EFFECT',field,[(t,fn(c,A)/fn(A,t)) for t in [444,452]])
regional=read('data/spores/effort_by_stage.csv')
print('REGIONAL DENOM DUPLICATION',[(s,len(sets[s]['all']),sum(int(r['n_docs']) for r in regional if r['stage']==s)) for s in ['Katian','Homerian','Lochkovian','Emsian']])
# Verify recorded identity bindings, without regenerating anything.
for p,manifest in [('data/eprp/record/macrostrat_units_window.csv','data/eprp/record/MANIFEST.tsv'),('data/external/spores/palynodata_taxon_window.csv','data/external/spores/MANIFEST.tsv')]:
    digest=hashlib.sha256((R/p).read_bytes()).hexdigest();matches=[m for m in read(manifest,'\t') if m['path'].endswith(Path(p).name)]
    print('SOURCE SHA',p,digest,'manifest match',any(m['sha256']==digest for m in matches))
receipt=json.loads((R/'data/macro/build_receipt.json').read_text())
for p in ['data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv','data/eprp/record/pbdb_plant_collections.csv','data/macro/effort_reviewed.csv','data/timescale.csv']:
    digest=hashlib.sha256((R/p).read_bytes()).hexdigest();expected=receipt['inputs'].get(p,receipt['outputs'].get(p));print('RECEIPT SHA',p,digest==expected)
# Recompute all global stage collection-equivalents directly from held raw collection rows.
land={'terrestrial indet.','fluvial indet.','fluvial-lacustrine indet.','lacustrine indet.','lacustrine - large','pond','"floodplain"','wet floodplain','fine channel fill','"channel"','alluvial fan','crevasse splay','mire/swamp','fluvial-deltaic indet.','delta plain'}
marginal={'coastal indet.','marginal marine indet.','lagoonal','estuary/bay','interdistributary bay','paralic indet.','deltaic indet.','delta front','prodelta','peritidal','foreshore'}
pbdb=read('data/occurrences/raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv')
plant_ids={r['collection_no'] for r in read('data/eprp/record/pbdb_plant_collections.csv')}
max_error=0
for e in eff:
    l,h=float(e['young_ma']),float(e['old_ma']);tot=exc=0
    for r in pbdb:
        if r['environment'] not in land|marginal:continue
        a,b=float(r['min_ma']),float(r['max_ma']);w=overlap(l,h,a,b)/(b-a) if b>a else 0
        tot+=w
        if r['collection_no'] not in plant_ids:exc+=w
    max_error=max(max_error,abs(tot-float(e['all_collection_equivalents'])),abs(exc-float(e['plant_excluded_equivalents'])))
print('RAW PBDB all',len(eff),'global stage equivalents reproduce; max absolute discrepancy',max_error,'rows',len(pbdb),'unique collections',len({r['collection_no'] for r in pbdb}))
# Reproduce the first spore numerator (excluding document-level rejects but not synonym/group rejects).
oldtri={s:set() for s in bounds}
for r in raw:
    if r['TMIC']!='S' or not gen.get(r['TGEN'],'').startswith('trilete') or r['TIDR'] in ['A','B','C','R'] or r['TDOC'] in ex or dv.get(r['TDOC'])=='reject' or loc.get(r['TLOC'],'unknown')=='unknown':continue
    ao=age.get(r['oldage']);ay=age.get(r['youngage'].strip() or r['oldage'])
    if not ao or not ay or ao['confidence'] not in ['high','medium'] or ay['confidence'] not in ['high','medium']:continue
    if ao['ics_oldest'] not in bounds or ay['ics_youngest'] not in bounds:continue
    old=bounds[ao['ics_oldest']][1];young=bounds[ay['ics_youngest']][0]
    if old-young>25:continue
    for s,(l,h) in bounds.items():
        if overlap(l,h,young,old)>0:oldtri[s].add(r['TDOC'])
rows=[(*bounds[s],len(oldtri[s])/len(d['all'])) for s,d in sets.items() if len(d['all'])]
fn=lambda lo,hi:stage_mean(rows,None,lo,hi)
print('FIRST SPORE numerator ratio',[(t,fn(c,A)/fn(A,t)) for t in [444,452]])
# Coverage by land and marginal environments across each comparison window (collection equivalents).
for l,h in [(c,A),(A,444),(A,452)]:
    counts=collections.Counter()
    for r in pbdb:
        if r['environment'] not in land|marginal:continue
        a,b=float(r['min_ma']),float(r['max_ma']);w=overlap(l,h,a,b)/(b-a) if b>a else 0
        counts['land' if r['environment'] in land else 'marginal']+=w
    print('PBDB ENV EQUIVALENTS',l,h,dict(counts))
# Exact duplicate publication titles/year/author in Palynodata source index.
docrows=read('data/external/spores/palynodata_documents_window.csv');groups=collections.defaultdict(list)
for r in docrows:
    title=re.sub(r'\W+','',r['ENGTITLE'].casefold())
    if title:groups[(title,r['PALYDATE'],r['PALYAUTH'])].append(r['AUTHDOCNUM'])
dups=[v for v in groups.values() if len(v)>1]
tridocs={r['TDOC'] for r,_,_,_ in filtered}
print('PALYNODATA duplicate exact normalized title/year/author groups',dups,'touching usable trilete numerator', [v for v in dups if tridocs&set(v)])
canon={d:min(v) for v in dups for d in v}
rows=[(*bounds[s],len({canon.get(d,d) for d in S['tri']})/len({canon.get(d,d) for d in S['all']})) for s,S in sets.items() if S['all']]
fn=lambda lo,hi:stage_mean(rows,None,lo,hi)
print('PUBLICATION-ID dedup Q',[(t,fn(c,A)/fn(A,t)) for t in [444,452]])
for ids in dups:
    if not tridocs&set(ids):continue
    for r in docrows:
        if r['AUTHDOCNUM'] in ids: print('TRILETE duplicate bibliography', {k:r[k] for k in ['AUTHDOCNUM','ENGTITLE','PALYDATE','PALYAUTH','Journal','Volume','Issue','Pages']})
print('PUBLICATION-ID dedup stage count changes',[(s,len(S['all'])-len({canon.get(d,d) for d in S['all']}),len(S['tri'])-len({canon.get(d,d) for d in S['tri']})) for s,S in sets.items() if (len(S['all'])>len({canon.get(d,d) for d in S['all']}) or len(S['tri'])>len({canon.get(d,d) for d in S['tri']})) and bounds[s][1]<=458.2])
u=[r for r in units if r['j_project_name']=='North America' and r['j_status_code']=='active' and r['d_env_class']=='non-marine']
segments=sorted((float(r['t_age']),float(r['b_age'])) for r in u)
merged=[]
for l,h in segments:
    if merged and l<=merged[-1][1]: merged[-1]=(merged[-1][0],max(h,merged[-1][1]))
    else:merged.append((l,h))
print('NA ROCK gaps intersecting analysis',[ (h,l2) for (_,h),(l2,_) in zip(merged,merged[1:]) if overlap(c,456,h,l2)>0])
print('SPORE exact means',proxies['spores_trilete_share'](c,A),[(t,proxies['spores_trilete_share'](A,t)) for t in [444,452]])
```

## Acceptance read of the integrated revision

13 November 2026, subsequent focused read of the uncommitted C56 integration. Methods (h), Results
(g), the relevant Discussion paragraph, Conclusion, S5.8, the new estimands section and the C56 ledger
were checked together. **C56 is accepted as supported for the descriptive proxy ratios and their
algebraic count equivalents.** The ledger now restricts its rock maximum to 444–452 Ma. The prose
keeps the column-area object, identifies the spore document-ID measure in the method, and explicitly
limits its comparison to numerical magnitudes. S5.8 discloses both duplicate publication IDs and
quadrature. The passages no longer claim that a proxy supplies or explains the body-record change.
No source tables were rechecked in this acceptance pass; no new result or data correction was needed.

One small specification refinement remains advisable, without blocking this acceptance: the
estimands sentence “Such transfer would need proportionality ... across both windows” describes a
sufficient condition as necessary. The endpoint comparison depends on ratios of window integrals;
pointwise proportionality is sufficient, but other histories can have the same integral ratio. Use,
for example, “Such a transfer is not established; proportionality to finding intensity throughout
both windows would be one sufficient assumption.” Methods (h) and S5.8 already use the correct
conditional formulation.
