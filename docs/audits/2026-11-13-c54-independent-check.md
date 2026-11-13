# C54 and the Libyan comparison: independent source check

Codex, 13 November 2026. Reviewed snapshot: `75f2bb02b54e8d66cee0476d1f5a309d36a69c6e`.
Scope: C54, its compilation sources, the 18 later-Ordovician Murzuq non-detections, and the
corresponding Results (c), Discussion and Conclusion. No canonical data, code, ledger or product
was changed. No private correspondence or outreach documents were opened.

## Decision

**Do not promote the current C54 to supported as six accepted trilete assemblages in four
countries.** Six is the reproducible number of entries in the strict compilation, and the
digitisation agrees with the original Wellman et al. (2013) supplement. But two British entries
conflict with the primary source they cite, and the Belgian entry remains review-level evidence
in this audit. `curated` describes the source layer; it does not establish primary-source
verification of every age–taxon association.

**The narrower scientific comparison survives.** Primary sources support triletes in Saudi
Arabia and Turkey within age enclosures overlapping those of the 18 Libyan non-detections. The
Saudi sequence includes Hirnantian positives. These establish overlapping stage-age ranges,
not simultaneous deposition and spore production, global biological absence, a producer's
abundance, or crown membership. A narrowed C54 based on this comparison can be supported after
the ledger and wording are changed accordingly. The present four-country wording cannot.

## What the selectors actually return

The C54 command in `manuscript/claims.csv` returns 43 taxon-report rows, representing 28
source–location–record combinations:

| Layer | Taxon-report rows | Distinct record IDs | Age support |
|---|---:|---:|---|
| Wellman 2013 | 13 | 6 | Four Ashgill entries mapped to Katian–Hirnantian; two Hirnantian entries |
| MVD-B, Saudi Arabia | 28 | 21 | Five Katian and 16 Hirnantian sample entries from Qusaiba-1 |
| MVD-B, Iran | 2 | 1 | One Katian–Hirnantian section interval |

The MVD-B Saudi records are from Wellman, Steemans & Miller (2015), DOI
`10.1016/j.revpalbo.2014.09.003`, the later systematic account of the Qusaiba-1 material
reported by Steemans et al. (2009). They are not 21 independent regions or a second independent
Saudi sequence. The Iran record is the Ghelli Formation, Pelmis-gorge interval, paper
`W2336620452`, DOI `10.22059/jsciences.2016.57002`; its compilation state is `not-vetted`.
Its source-level validity was not independently re-audited here and is not needed for the
narrowed comparison.

The six Wellman entries are accurately transcribed from PDF pages 2–4 of
`data/external/spores/wellman2013_supplement/18680.pdf`:

| Entry | Published age and locality | Compiled trilete reports | Source assessment |
|---|---|---|---|
| W13-013 | Ashgill; Avalonia, Belgium | *Ambitisporites avitus* | Review report; primary confirmation unresolved here |
| W13-014 | Ashgill; Avalonia, southern Britain | *A. avitus* | Conflicts with cited primary evidence; not an accepted strict positive |
| W13-017 | Ashgill; Peri-Gondwana (Taurides), Turkey | *A. avitus*, *A. dilutus* | Primary-supported morphon occurrence; broad age retained |
| W13-018 | Ashgill; SW Gondwana, Saudi Arabia | *Ambitisporites*, *Chelinospora*, *Leiotriletes*, queried *Synorisporites* | Primary-supported true triletes; this is a stage summary of the Saudi sequence |
| W13-023 | Hirnantian; Avalonia, UK | *A. avitus* | Conflicts with cited primary evidence; not an accepted strict positive |
| W13-024 | Hirnantian; SW Gondwana, Saudi Arabia | The same four trilete genera, including queried *Synorisporites* | Primary-supported true triletes; another stage summary of the Saudi sequence |

Thus the original entries must be retained as source reports, but the present `curated` and
`usable=true` states must not be treated as an adjudication accepting the two British
age–trilete links. Excluding the British entries leaves four review entries in three countries;
setting the unverified Belgian entry aside leaves three primary-supported review entries in
two countries. Removing the two queried Saudi *Synorisporites* rows also leaves these three
entries intact. They still include eight unqueried taxon rows.

`tools/spores.py:224–233` assigns every Wellman row `vetting=curated`; its questionable flag is
the assemblage-level `questionable_affinity`, not the taxon qualifier. Consequently the two
Saudi queried genus strings remain `flag_questionable=false`. This is a limitation of the flag
semantics, not proof that their trilete marks are doubtful: the original 2009 descriptions
explicitly identify true triletes while discussing uncertain generic placement. The count of
positive assemblage entries does not depend on them.

## Material primary-source conflict: Britain

The published review rows are not transcription errors. The original supplement really lists
*A. avitus* under both Ashgill southern Britain and Hirnantian UK. Their cited sources are:

- W13-014: Burgess (1991); Steemans et al. (1996).
- W13-023: Burgess (1991); Steemans et al. (1996); Steemans et al. (2000).

The held primary Burgess (1991), `library/closed/burgess1991_firststudy.pdf`, distinguishes the
earlier cryptospore assemblage from the true-trilete assemblage:

- Printed p. 575 / PDF p. 1: the older assemblage spans uppermost Ordovician to late Aeronian
  and comprises cryptospores; the younger, late Aeronian–Telychian assemblage is dominated by
  smooth trilete *Ambitisporites*.
- Printed p. 594 / PDF p. 20: *A. dilutus* ranges from late Aeronian to early Telychian.
  *Ambitisporites? vavrdovii* ranges from latest Ordovician to early Aeronian, but its marks are
  simple splits rather than the sutures and lips of *A. avitus*. This is not an unqueried
  Ordovician *A. avitus* occurrence.
- Printed p. 596 / PDF p. 22: the older *A.? vavrdovii* probably derives from mechanically
  fragmented permanent tetrads and is explicitly excluded from the earliest true-trilete
  records. The true *Ambitisporites* assemblage occurs in samples L21–L23, late Aeronian to
  early Telychian. The paper's comparison of other British and Irish records likewise places
  true *Ambitisporites* in the Silurian.

Steemans et al. (1996), `library/closed/al1996_macbook20261030.pdf`, printed p. 71 / PDF p. 37,
cites the late Aeronian–Telychian British *avitus–dilutus* assemblage. Its printed p. 47 / PDF
p. 13 tentatively reinterprets Burgess's Plate 2, figure 18 as an *A. avitus* morphon specimen,
based on the possibility of laesurae. This qualification matters: the 1996 paper does not
simply reject every pre-late-Aeronian British candidate. However, Burgess p. 594 locates that
specific figure in sample L8, Crychan Formation, *cyphus* Zone, which is Rhuddanian, not
Hirnantian. It does not restore either Ordovician British entry. The 2000 reference is
explicitly the Saudi Nuayyim-2 study, not a new British Ordovician primary description.

This supports a specific source conflict, rather than a claim that every conceivable British
Ordovician occurrence has been disproved. No alternative primary locality or specimen is
identified by the review entries. They should be excluded from the strict accepted comparison
unless such evidence is supplied. Combining an Ordovician assemblage age with a later
true-trilete taxon, or conflating *A.? vavrdovii* with true *Ambitisporites*, would generate
this discrepancy; the precise route by which the review acquired it is not established.
This bears on Q5.

An independently located primary paper also states the British first true triletes are latest
Aeronian, citing Burgess: Le Hérissé et al. (2001), printed p. 32,
[author-repository copy](https://orbi.uliege.be/bitstream/2268/17261/1/Le%20Herisse%20et%20al%20%202001.pdf).
The decisive evidence above comes from the held Burgess primary, not this corroboration.

For Belgium, W13-013 cites Martin (1973), Steemans (2001), Steemans et al. (1996) and Wellman &
Richardson (1993). The specific primary Steemans (2001), *Ordovician cryptospores from the
Oostduinkerke borehole, Brabant Massif, Belgium*, DOI `10.1016/S0016-6995(01)80038-3`, has a
[repository record](https://orbi.uliege.be/handle/2268/17262) whose file is explicitly marked
“Request a copy”. I read the record, not the restricted full text. Its cryptospore-focused
abstract does not validate the *A. avitus* association. This is unresolved, not a demonstrated
Belgian false positive. A source request is not proposed.

Steemans et al. (1996), printed p. 47 / PDF p. 13, provides a relevant but insufficient clue:
it reports that two of Martin's 84 *Leiotriletes* sp. I specimens could belong to the
*A. avitus* morphon. The reported collection spans upper Caradocian to lower Llandoverian;
that passage does not locate the two candidates within the range. It therefore cannot
establish a wholly Katian–Hirnantian Belgian true-trilete occurrence.

## Saudi Arabia, Turkey, geography and ages

Steemans et al. (2009), DOI `10.1126/science.1169659`, held at
`library/closed/steemans2009a_firststudy.pdf` and
`library/closed/steemans2009a_firststudy_SI1.pdf`, supports
unornamented and ornamented true triletes in Qusaiba-1. The supplement's age-dating section
(PDF p. 2) dates the Qasim samples to Katian using chitinozoans and acritarchs and the overlying
Sarah Formation to Hirnantian using marine biostratigraphy and glacial stratigraphy. Its spore
descriptions (PDF p. 3) establish the trilete character separately from generic assignment;
main-paper p. 353 / PDF p. 1, Figure 1B–I, shows the figured triletes. Wellman et al. (2015),
`library/closed/wellman2015_firststudy.pdf`, printed p. 113 / PDF p. 3, provides the later
age account, and Table 2, printed p. 116 / PDF p. 6, supplies sample-level reporting for the
same sequence. Neither country's or palaeogeographic label is evidence of a crown-embryophyte
producer.

The Turkish primary Steemans, Le Hérissé & Bozdogan (1996), DOI
`10.1016/0034-6667(95)00119-0`, has unqueried *avitus–dilutus* morphon occurrences and marine
age control. Printed p. 40 / PDF p. 6 places the oldest occurrence possibly from middle
Ashgillian to Hirnantian; printed p. 47 / PDF p. 13 gives the morphon's description and
distribution in samples GH7 and GH6 (well 1), H2 (well 2) and B2 (well 4), plus younger Dadas
samples. Printed p. 71 / PDF p. 37 identifies the basal morphon occurrences and Ashgillian
age control. This permits a broad age enclosure wholly within Katian–Hirnantian under the
adopted crosswalk, not an exclusively Hirnantian occurrence. It does not transfer the
occurrence to every stage or to every age within that enclosure. The primary-supported
review-entry selector is exactly `{'W13-017', 'W13-018', 'W13-024'}`; these are three summary
entries, not three independent sites.

The modern countries and published palaeogeographic labels in the six digitised entries agree
with the supplement. “Southern Britain” and “UK” are two entries, not two countries; neither
should be counted as an independent palaeogeographic replicate. Saudi Arabia and Libya occupy
the same broad Gondwanan regional bin in the compilation, but the source localities are
different basins and catchments. Modern country counts do not measure palaeogeographic
coverage or establish that either producer lay outside the Libyan catchment.

## The 18 Murzuq non-detections

The frozen stage/chart-code design has 28 Ordovician cuttings reporting no triletes: ten
Darriwilian, 13 Katian–Hirnantian and five Hirnantian. The 18 later-Ordovician cuttings are:

| Well | Katian–Hirnantian depths (ft) | Hirnantian depths (ft) |
|---|---|---|
| D1-200 | 4900, 4950, 4960, 4970, 5000, 5130 | — |
| H2-NC186 | — | 4550, 4590 |
| I3-NC186 | 4810, 4850, 4900, 4975, 5040, 5075, 5200 | 4680, 4700, 4740 |

I re-counted these directly from `models/f3/out/m2_units.csv` and inspected the held Abuhmida
(2013) thesis chart pages 618, 622 and 624 (PDF pages 634, 638 and 640), with both display
panels. The target is *Ambitisporites dilutus*, used as the thesis's full true-trilete reporting
category under the adopted `libya-chart-v1` rule. The older target cells are blank while other
palynomorphs are reported. These are reporting non-detections under that rule, not observed
biological absence or grain counts. This check did not requalify the encounter likelihood.

Using `data/timescale.csv`, Katian–Hirnantian means 452.8–443.1 Ma, and Hirnantian
445.2–443.1 Ma (2.1 Myr). Their older edge is younger than the 454.41 Ma Swedish bentonite.
Shared stage labels permit overlapping age ranges, even with the narrower Hirnantian
comparison. They do not require the positive and negative rocks to have the same actual age:
each could lie in a different part of its stage. No exact contemporaneity follows.

An adjacent reproducibility defect: the existing C45 command filters `d==0` but does not
restrict the ages, so it prints **36** non-detections: the 28 Ordovician plus eight Llandovery
reference non-detections. The C45 values are correct once the older-stage restriction is
included. This is a command defect, not a changed 28/18/5/10 result.

## Manuscript implications

- **Results (c), lines 212–215:** remove Britain as an accepted Ordovician/Hirnantian positive.
  Belgium is still a review report in this audit and should not be presented as independently
  verified. Saudi Arabia and Turkey suffice for the stage-range comparison; Saudi Arabia
  supplies the primary-backed Hirnantian example. Cite those primaries, or explicitly
  distinguish the review's report from accepted evidence.
- **Results (c), lines 215–221:** the stage-resolution statement and the conditional supply
  limit are appropriately separated. C54 supplies a comparison of records; C24/C51 supply
  the numerical constraints. C54 does not prove why the Libyan record differs. “Absence can
  be local” is acceptable only as shorthand for local non-reporting, not a demonstrated
  contemporaneous geographic exclusion; a heading that names non-detection would be clearer.
- **Discussion, lines 298–302, and Conclusion, lines 377–382:** their current statement that
  triletes go unreported in rocks from stages with records elsewhere is supported by the
  narrower Saudi/Turkish evidence. The earlier stronger simultaneity inference identified in
  the 12 November audit has been removed. Keep the stage resolution and the distinction
  between spore occurrence and crown membership.
- **Conditions, lines 336–342:** correctly limits the geographic comparison to stage
  resolution and states the extra trait-to-node assumptions. It cannot rescue the specific
  British source conflict in Results.
- **C54 limitation:** prefer “overlapping stage-age ranges do not establish exact
  contemporaneity” to “contemporaneity holds at stage resolution only”. The latter invites
  the earlier inference again.

## Reproduce the counts without regeneration

Run from the repository root:

```bash
uv run --no-project python - <<'PY'
import csv
from collections import Counter

stages = {'Katian', 'Hirnantian'}
rows = [r for r in csv.DictReader(open('data/spores/occurrences.csv'))
        if r['usable'] == 'true'
        and r['spore_class'].startswith('trilete')
        and r['vetting'] in {'accept', 'curated', 'not-vetted'}
        and r['ics_oldest'] in stages and r['ics_youngest'] in stages]
print('taxon rows:', Counter(r['source'] for r in rows))
print('entries:', Counter(s for s, i in {(r['source'], r['record_id']) for r in rows}))
print('Wellman IDs:', sorted({r['record_id'] for r in rows if r['source'] == 'wellman2013'}))
secure_ids = {'W13-017', 'W13-018', 'W13-024'}
secure = [r for r in rows if r['source'] == 'wellman2013' and r['record_id'] in secure_ids]
print('primary-supported review entries:', sorted({r['record_id'] for r in secure}))
print('their taxon rows / unqueried rows:', len(secure), sum('?' not in r['taxon'] for r in secure))
for source in ('wellman2013', 'mvdb'):
    entries = {(r['record_id'], r['ics_oldest'], r['ics_youngest'])
               for r in rows if r['source'] == source}
    print(source, Counter((old, young) for _, old, young in entries))

units = [r for r in csv.DictReader(open('models/f3/out/m2_units.csv'))
         if r['design'] == 'LY-MZ-CU'
         and r['variant'] == 'allocation=stage;material_type=chart-code'
         and not r['excluded'] and r['d'] == '0']
older = [r for r in units if r['oldest_stage'] in stages | {'Darriwilian'}
         and r['youngest_stage'] in stages | {'Darriwilian'}]
later = [r for r in older if r['oldest_stage'] in stages and r['youngest_stage'] in stages]
print('all negatives / Ordovician / later:', len(units), len(older), len(later))
print('older by stage and well:', Counter((r['oldest_stage'], r['youngest_stage'], r['cluster'])
                                         for r in older))
print('later IDs:', sorted(r['unit_id'] for r in later))
assert len(older) == 28 and len(later) == 18
assert sum(r['oldest_stage'] == r['youngest_stage'] == 'Hirnantian' for r in later) == 5
PY
```

Source hashes checked: Wellman supplement
`52a5d76c8867a36277a7bc945b0f183d4b43c7911bae53d5b65ce0e03d4ba585`;
Wellman chapter `8437b385b8debf133ab0b71e7cb9e8e6bd3ff3f7d3c49f6983647e0101588f19`;
Abuhmida thesis `c0e3bf798fb3c27db0bf9cbb155396be5b4b8e003ee2228defb615a65abf3211`.
The relevant source PDFs were rendered to `/tmp`; copyrighted images and extracts were not
added to the repository. No source compilation was regenerated.

Next: Codex — narrow C54 and Results, preserve the British source conflict for Q5.

## Follow-up: narrowed C54 and revised prose accepted

13 November 2026, focused review of the integrating working tree. **The narrowed C54 is
supported.** I executed its exact ledger command: it returns W13-017 (Turkey,
Katian–Hirnantian), W13-018 (Saudi Arabia, Katian–Hirnantian) and W13-024 (Saudi Arabia,
Hirnantian), after excluding queried genus strings. The three review entries and two countries
are correct; the ledger explicitly prevents treating the entries as independent sites.

Results (c) now uses only these primary-supported examples, and its Hirnantian comparison
uses Saudi Arabia. New S2.6 accurately preserves the broad Turkish age, separates stage-range
overlap from simultaneity and crown placement, and explains the British source conflict,
including the Rhuddanian specimen's tentative reinterpretation. The added Burgess reference
matches the held title page; the Steemans reference matches the held primary source identity.
No further retrieval was performed.

One wording qualification: S2.6's “The Belgian entry also lacks a primary-source demonstration”
should say “The Belgian entry remains unverified against primary sources in this audit”. The
audit did not exhaust every cited Belgian primary; it establishes an unresolved association,
not that no demonstration exists. This does not weaken the accepted Saudi/Turkish subset.
The ledger's verification commit should be refreshed when the integrated changes are committed.

Next: Codex — make the Belgian uncertainty explicit and retain the narrowed C54.
