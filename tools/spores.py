# /// script
# requires-python = ">=3.12"
# dependencies = ["duckdb"]
# ///
"""Build the project's dispersed-spore dataset from Palynodata and the crosswalks.

    uv run tools/spores.py inputs   # write the work lists the crosswalks are built from
    uv run tools/spores.py check    # validate crosswalk files against vocabularies and inputs
    uv run tools/spores.py build    # write data/spores/occurrences.csv and summary tables
"""

import csv
import json
import re
import sys
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
PALY = ROOT / "data" / "external" / "spores"
OUT = ROOT / "data" / "spores"
XW = OUT / "crosswalks"
WORK = OUT / "work"

SPORE_CLASSES = {"cryptospore-monad", "cryptospore-dyad", "cryptospore-tetrad", "trilete-laevigate",
                 "trilete-ornamented", "trilete-unspecified", "other-spore", "not-a-spore", "uncertain"}
UNITS = {"Laurentia", "Baltica", "Avalonia", "peri-Gondwana-Europe", "Gondwana-North-Africa-Arabia",
         "Gondwana-South-America", "Gondwana-Australia-Antarctica", "Gondwana-other", "South-China",
         "North-China", "Tarim", "Kazakhstania", "Siberia", "multiple", "unknown"}
CONFIDENCE = {"high", "medium", "low"}

SPORES = f"read_csv_auto('{PALY / 'palynodata_taxon_window.csv'}', all_varchar=true)"


def stages():
    with open(ROOT / "data" / "timescale.csv") as f:
        rows = list(csv.DictReader(f))
    base = {r["stage"]: float(r["base_ma"]) for r in rows}
    names = [r["stage"] for r in rows]
    top = {names[i]: base[names[i - 1]] for i in range(1, len(names))}
    return base, top


def write(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {path.relative_to(ROOT)} ({len(rows)} rows)")


def cmd_inputs():
    con = duckdb.connect()
    ages = con.execute(f"""
        with s as (select * from {SPORES} where TMIC = 'S'),
        names as (select oldage as age_name, agestart, ageend from s
                  union all select youngage, agestart, ageend from s)
        select age_name, count(*) n_rows,
               min(try_cast(ageend as double)), max(try_cast(agestart as double))
        from names where age_name is not null and age_name <> ''
        group by 1 order by 2 desc""").fetchall()
    write(WORK / "age_names.csv", ["age_name", "n_rows", "palynodata_min_ma", "palynodata_max_ma"], ages)
    locs = con.execute(f"""
        select TLOC, count(*) n_rows, count(distinct TDOC) n_docs
        from {SPORES} where TMIC = 'S' group by 1 order by 2 desc""").fetchall()
    write(WORK / "locations.csv", ["tloc", "n_rows", "n_docs"], locs)
    gens = con.execute(f"""
        select TGEN, count(*) n_rows, count(distinct TDOC) n_docs,
               string_agg(distinct TSPE, '; ') filter (where TSPE is not null and TSPE <> '') species,
               min(try_cast(derived_young_ma as double)), max(try_cast(derived_old_ma as double))
        from {SPORES} where TMIC = 'S' group by 1 order by 2 desc""").fetchall()
    gens = [(g, n, d, (sp or "")[:300], lo, hi) for g, n, d, sp, lo, hi in gens]
    wellman = OUT / "sources" / "wellman2013_taxa.csv"
    if wellman.exists():
        known = {g[0] for g in gens}
        extra = con.execute(f"""
            select genus, count(*), count(distinct entry_id), string_agg(distinct expanded, '; ')
            from read_csv_auto('{wellman}', all_varchar=true)
            where genus <> '' group by 1 order by 2 desc""").fetchall()
        gens += [(g, n, d, (sp or "")[:300], None, None) for g, n, d, sp in extra if g not in known]
    write(WORK / "spore_genera.csv",
          ["genus", "n_rows", "n_docs", "species_sample", "palynodata_min_ma", "palynodata_max_ma"], gens)
    return 0


def cmd_mvdb():
    """Flatten the Codex MVD-B extractions into source tables."""
    out_dir = WORK / "codex" / "mvdb" / "out"
    papers = {r["openalex_id"]: r for r in csv.DictReader(open(WORK / "codex" / "mvdb" / "papers.csv"))}
    asm_rows, taxa_rows, dropped = [], [], []
    squash = lambda x: re.sub(r"[\s\-\u2010-\u2014]+", "", re.sub(r"-\s*\n\s*", "", x)).lower()
    for path in sorted(out_dir.glob("*_sol.json")):
        pid = path.name.split("_")[0]
        doc = json.loads(path.read_text())
        text = Path(ROOT / papers[pid]["text"]).read_text(encoding="utf-8", errors="replace") if pid in papers else ""
        if len(text.split()) < 1500:
            dropped.append((pid, len(text.split())))
            continue
        t = squash(text)
        for k, a in enumerate(doc["items"], 1):
            aid = f"{pid}-A{k:03d}"
            asm_rows.append([aid, pid, papers.get(pid, {}).get("doi", ""), doc["doc"]["citation"], a["scope"], a["locality"],
                             a["country"], a["formation"], a["section_or_core"], a["palaeogeo_unit_reported"], a["palaeo_unit_proposed"],
                             a["age_as_reported"], a["age_basis"], a["age_circular"], a["stage_min_proposed"], a["stage_max_proposed"],
                             a["setting_class"], a["reworking_status"], len(a["occurrences"]), a["locator"], a["notes"]])
            for o in a["occurrences"]:
                g = o["genus"].strip()
                words = [w for w in re.findall(r"[a-z][a-z-]{2,}", o["taxon_as_reported"].lower()) if w != g.lower()]
                ep = words[-1] if words and words[-1] not in ("sp", "spp", "indet", "morphon") else ""
                verified = squash(o["taxon_as_reported"])[:40] in t or (bool(g) and squash(g) in t and (not ep or squash(ep) in t))
                taxa_rows.append([aid, o["taxon_as_reported"], g, o["qualifier"], o["abundance"], o["locator"], verified])
    write(OUT / "sources" / "mvdb_assemblages.csv",
          ["assemblage_id", "paper", "doi", "citation", "scope", "locality", "country", "formation", "section_or_core",
           "palaeogeo_unit_reported", "palaeo_unit_proposed", "age_as_reported", "age_basis", "age_circular",
           "stage_min_proposed", "stage_max_proposed", "setting_class", "reworking_status", "n_taxa", "locator", "notes"], asm_rows)
    write(OUT / "sources" / "mvdb_taxa.csv", ["assemblage_id", "taxon_as_reported", "genus", "qualifier", "abundance", "locator", "verified_in_text"], taxa_rows)
    write(OUT / "sources" / "mvdb_dropped_papers.csv", ["paper", "text_words"], dropped)
    n_ok = sum(1 for r in taxa_rows if r[-1])
    print(f"taxa verified in text: {n_ok}/{len(taxa_rows)}; papers dropped as not full text: {len(dropped)}")
    return 0


def read_xw(name):
    path = XW / name
    if not path.exists():
        return None
    with open(path) as f:
        return list(csv.DictReader(f))


def cmd_check():
    base, _ = stages()
    problems = []
    checks = [
        ("age_names.csv", "age_name", "age_names.csv",
         lambda r: [f"stage {r[k]!r} not in timescale" for k in ("ics_oldest", "ics_youngest")
                    if r[k] and r[k] not in base]
         + ([] if not (r["ics_oldest"] and r["ics_youngest"]) or base[r["ics_oldest"]] >= base[r["ics_youngest"]]
            else ["ics_oldest is younger than ics_youngest"])),
        ("locations.csv", "tloc", "locations.csv",
         lambda r: [] if r["palaeo_unit"] in UNITS else [f"palaeo_unit {r['palaeo_unit']!r}"]),
        ("spore_genera.csv", "genus", "spore_genera.csv",
         lambda r: [] if r["spore_class"] in SPORE_CLASSES else [f"spore_class {r['spore_class']!r}"]),
    ]
    for xw_name, key, work_name, rule in checks:
        rows = read_xw(xw_name)
        if rows is None:
            problems.append(f"{xw_name}: missing")
            continue
        with open(WORK / work_name) as f:
            wanted = {r[key] for r in csv.DictReader(f)}
        have = {r[key] for r in rows}
        if missing := wanted - have:
            problems.append(f"{xw_name}: {len(missing)} input keys not mapped, e.g. {sorted(missing)[:5]}")
        for r in rows:
            if r.get("confidence") not in CONFIDENCE:
                problems.append(f"{xw_name}: {r[key]!r} confidence {r.get('confidence')!r}")
            for p in rule(r):
                problems.append(f"{xw_name}: {r[key]!r}: {p}")
    for p in problems[:60]:
        print(p)
    print(f"{len(problems)} problems")
    return 1 if problems else 0


REAL_CLASSES = ("cryptospore-monad", "cryptospore-dyad", "cryptospore-tetrad", "trilete-laevigate",
                "trilete-ornamented", "trilete-unspecified", "other-spore")
CLASS_GROUP = {"cryptospore-monad": "cryptospore", "cryptospore-dyad": "cryptospore",
               "cryptospore-tetrad": "cryptospore", "trilete-laevigate": "trilete",
               "trilete-ornamented": "trilete", "trilete-unspecified": "trilete", "other-spore": "other"}
RANK = "case {c} when 'high' then 3 when 'medium' then 2 when 'low' then 1 else 0 end"


def cmd_build():
    if cmd_check():
        sys.exit("fix crosswalks first")
    base, top = stages()
    con = duckdb.connect()
    for name in ("age_names", "locations", "spore_genera", "wellman_series", "wellman_regions", "exclusions", "doc_vetting", "group_vetting"):
        con.execute(f"create table {name} as select * from read_csv_auto('{XW / (name + '.csv')}', all_varchar=true)")
    con.execute("create table base as select * from (values " +
                ", ".join(f"('{s}', {b}, {top.get(s, 'null')})" for s, b in base.items()) +
                ") t(stage, base_ma, top_ma)")
    con.execute(f"""
        create table paly as
        select 'palynodata' as source, s.TDOC as record_id, s.TGEN as genus,
               trim(s.TGEN || ' ' || coalesce(s.TSPE, '')) as taxon, s.TLOC as location, l.palaeo_unit,
               g.spore_class, g.confidence as class_confidence, ao.ics_oldest, ay.ics_youngest,
               {RANK.format(c='ao.confidence')} as ra, {RANK.format(c='ay.confidence')} as ry,
               coalesce(s.TIDR in ('A', 'B', 'C', 'R'), false) as flag_reworked_or_caved,
               coalesce(s.TSYN = 'X', false) as flag_synonym_list, coalesce(s.TNEW = 'X', false) as flag_new_taxon, false as flag_questionable,
               coalesce(gv.verdict, v.verdict, 'not-vetted') as vetting
        from {SPORES} s
        left join spore_genera g on g.genus = s.TGEN
        left join locations l on l.tloc = s.TLOC
        left join age_names ao on ao.age_name = s.oldage
        left join age_names ay on ay.age_name = coalesce(nullif(trim(s.youngage), ''), s.oldage)
        left join doc_vetting v on v.doc = s.TDOC
        left join group_vetting gv on gv.doc = s.TDOC and gv.ics_oldest = ao.ics_oldest and gv.ics_youngest = ay.ics_youngest
             and gv.location = s.TLOC and gv.class_group = case when g.spore_class like 'cryptospore%' then 'cryptospore'
                 when g.spore_class like 'trilete%' then 'trilete' else 'other' end
        where s.TMIC = 'S' and s.TDOC not in (select doc from exclusions)""")
    con.execute(f"""
        create table well as
        select 'wellman2013' as source, a.entry_id as record_id, t.genus, t.expanded as taxon,
               a.region_as_given || ' - ' || a.country || coalesce(', ' || nullif(a.locality, ''), '') as location,
               r.palaeo_unit, g.spore_class, g.confidence as class_confidence, w.ics_oldest, w.ics_youngest,
               {RANK.format(c='w.confidence')} as ra, {RANK.format(c='w.confidence')} as ry,
               false, false, false, coalesce(a.questionable_affinity = 'True', false), 'curated' as vetting
        from read_csv_auto('{OUT / 'sources' / 'wellman2013_taxa.csv'}', all_varchar=true) t
        join read_csv_auto('{OUT / 'sources' / 'wellman2013_assemblages.csv'}', all_varchar=true) a using (entry_id)
        left join wellman_regions r on r.region_as_given = a.region_as_given
        left join wellman_series w on w.series_as_given = a.series_as_given
        left join spore_genera g on g.genus = t.genus""")
    con.execute(f"""
        create table mvdb as
        select 'mvdb' as source, a.assemblage_id as record_id, t.genus, t.taxon_as_reported as taxon,
               a.country || coalesce(', ' || nullif(a.locality, ''), '') as location, a.palaeo_unit_proposed as palaeo_unit,
               g.spore_class, g.confidence as class_confidence, nullif(a.stage_min_proposed, '') as ics_oldest,
               nullif(a.stage_max_proposed, '') as ics_youngest,
               case when a.age_basis in ('unstated', 'lithostratigraphic') or a.age_circular = 'true' then 1 else 2 end as ra,
               case when a.age_basis in ('unstated', 'lithostratigraphic') or a.age_circular = 'true' then 1 else 2 end as ry,
               a.reworking_status = 'demonstrated', false, false, coalesce(t.qualifier = '?', false) or t.verified_in_text <> 'True', 'not-vetted' as vetting
        from read_csv_auto('{OUT / 'sources' / 'mvdb_taxa.csv'}', all_varchar=true) t
        join read_csv_auto('{OUT / 'sources' / 'mvdb_assemblages.csv'}', all_varchar=true) a using (assemblage_id)
        left join spore_genera g on g.genus = t.genus""") if (OUT / "sources" / "mvdb_taxa.csv").exists() else None
    has_mvdb = (OUT / "sources" / "mvdb_taxa.csv").exists()
    con.execute(f"""
        create table occ as
        with u as (select * from paly union all select * from well {'union all select * from mvdb' if has_mvdb else ''})
        select u.* exclude (ra, ry),
               case least(ra, ry) when 3 then 'high' when 2 then 'medium' when 1 then 'low' else null end as age_confidence,
               bo.base_ma as oldest_base_ma, by_.top_ma as youngest_top_ma,
               round(bo.base_ma - by_.top_ma, 2) as span_myr,
               (u.spore_class in {REAL_CLASSES} and least(ra, ry) >= 2 and bo.base_ma - by_.top_ma <= 25
                and not u.flag_reworked_or_caved and not u.flag_synonym_list and not u.flag_questionable
                and coalesce(u.palaeo_unit, 'unknown') <> 'unknown') as usable
        from u left join base bo on bo.stage = u.ics_oldest left join base by_ on by_.stage = u.ics_youngest""")
    con.execute(f"copy (select * from occ order by oldest_base_ma desc nulls last, source, record_id) to '{OUT / 'occurrences.csv'}' (header)")
    groups = " union all ".join(f"select '{k}' as spore_class, '{v}' as class_group" for k, v in CLASS_GROUP.items())
    con.execute(f"""
        create table fa as
        with x as (select o.*, g.class_group from occ o join ({groups}) g using (spore_class) where usable),
        sets as (select 'strict' as record_set, * from x where vetting in ('accept', 'curated', 'not-vetted')
                 union all select 'inclusive', * from x where vetting <> 'reject'),
        levels as (
            select record_set, class_group, spore_class, palaeo_unit, record_id, source, youngest_top_ma, oldest_base_ma from sets
            union all select record_set, class_group, '(all)', palaeo_unit, record_id, source, youngest_top_ma, oldest_base_ma from sets
            union all select record_set, class_group, spore_class, '(all)', record_id, source, youngest_top_ma, oldest_base_ma from sets
            union all select record_set, class_group, '(all)', '(all)', record_id, source, youngest_top_ma, oldest_base_ma from sets)
        select record_set, class_group, spore_class, palaeo_unit,
               count(distinct source || ':' || record_id) as n_sources,
               max(youngest_top_ma) as fa_certain_ma,
               arg_max(source || ':' || record_id, youngest_top_ma) as fa_certain_record,
               max(oldest_base_ma) as fa_possible_ma,
               arg_max(source || ':' || record_id, oldest_base_ma) as fa_possible_record
        from levels group by all order by record_set desc, class_group, spore_class, fa_certain_ma desc""")
    con.execute(f"copy fa to '{OUT / 'first_appearances.csv'}' (header)")
    con.execute(f"""
        copy (select o.spore_class, o.palaeo_unit, b.stage, b.base_ma,
                     count(distinct o.source || ':' || o.record_id) as n_sources
              from occ o join base b on b.base_ma > o.youngest_top_ma and coalesce(b.top_ma, 0) < o.oldest_base_ma
              where o.usable and o.vetting <> 'reject' group by all order by b.base_ma desc, o.spore_class, o.palaeo_unit)
        to '{OUT / 'presence_by_stage.csv'}' (header)""")
    con.execute(f"""
        copy (
          with r as (
            select s.TDOC as doc,
                   s.TMIC = 'S' and s.TDOC not in (select doc from doc_vetting where verdict = 'reject') as is_spore,
                   l.palaeo_unit, bo.base_ma as oldest_base_ma, by_.top_ma as youngest_top_ma
            from read_csv_auto('{PALY / 'palynodata_taxon_window.csv'}', all_varchar=true) s
            join locations l on l.tloc = s.TLOC
            join age_names ao on ao.age_name = s.oldage
            join age_names ay on ay.age_name = coalesce(nullif(trim(s.youngage), ''), s.oldage)
            join base bo on bo.stage = ao.ics_oldest join base by_ on by_.stage = ay.ics_youngest
            where s.TDOC not in (select doc from exclusions)
              and least({RANK.format(c='ao.confidence')}, {RANK.format(c='ay.confidence')}) >= 2
              and bo.base_ma - by_.top_ma <= 25 and l.palaeo_unit not in ('unknown'))
          select r.palaeo_unit, b.stage, b.base_ma, count(distinct r.doc) as n_docs,
                 count(distinct r.doc) filter (where r.is_spore) as n_docs_with_spores,
                 count(distinct r.doc) - count(distinct r.doc) filter (where r.is_spore) as n_docs_without_spores
          from r join base b on b.base_ma > r.youngest_top_ma and coalesce(b.top_ma, 0) < r.oldest_base_ma
          group by all order by b.base_ma desc, r.palaeo_unit)
        to '{OUT / 'effort_by_stage.csv'}' (header)""")
    print("wrote data/spores/effort_by_stage.csv")
    for t, f in (("occ", "occurrences.csv"), ("fa", "first_appearances.csv")):
        print(f"wrote data/spores/{f} ({con.execute(f'select count(*) from {t}').fetchone()[0]} rows)")
    print("wrote data/spores/presence_by_stage.csv")
    print("usable records:", con.execute("select source, count(*) from occ where usable group by 1").fetchall())
    return 0


if __name__ == "__main__":
    commands = {"inputs": cmd_inputs, "check": cmd_check, "build": cmd_build, "mvdb": cmd_mvdb}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    sys.exit(commands[sys.argv[1]]())
