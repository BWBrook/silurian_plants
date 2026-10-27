#!/usr/bin/env python3
"""Build specimens_scope_names.csv: every name the specimen harvest searches for.

Reads the card front matter in taxa/*.md (name, authority, rank, group), adds the anchor genera, the nematophyte
and charophyte names, the member genera that the EPRP PBDB filter used for assemblage cards, spelling variants
and synonyms that the cards or EPRP name, and the tranche-2 cards that docs/decisions.md plans but taxa/ does not
yet hold. Nothing here is merged silently: every row keeps its role and the reason it is on the list.

usage: python3 specimens_scope.py [PROJECT_ROOT] > specimens_scope_names.csv   (stdlib only; PROJECT_ROOT default ~/papers/silurian_plants)
"""
import csv
import glob
import os
import re
import sys

root = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/papers/silurian_plants")

rows = []


def add(name, role, slug="", reason="", synonym_of="", rank_override="", kind=""):
    parts = name.replace("?", "").split()
    genus = parts[0] if parts else ""
    epithet = parts[1] if len(parts) > 1 else ""
    rank = "species" if epithet else "genus"
    if name.endswith("aceae") or name.endswith("ales") or name.endswith("phyceae") or name.endswith("opsida"):
        rank = "higher"
    if rank_override:
        rank = rank_override
        genus = epithet = ""
    rows.append({"name": name, "name_rank": rank, "genus": genus, "epithet": epithet, "role": role,
                 "card_slug": slug, "synonym_of": synonym_of, "kind": kind, "reason": reason})


card_files = sorted(f for f in glob.glob(os.path.join(root, "taxa", "*.md"))
                    if os.path.basename(f) not in ("README.md", "_template.md"))
cards = []
for f in card_files:
    slug = os.path.basename(f)[:-3]
    head = open(f, encoding="utf-8").read().split("---")[1]
    fm = {}
    for line in head.splitlines():
        m = re.match(r"^(name|authority|rank|kind|group):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
    cards.append((slug, fm))

ASSEMBLY = {
    "ordovician-cryptospores": ["Tetrahedraletes", "Cryptospora", "Dyadospora", "Pseudodyadospora", "Hispanaediscus",
                                "Laevolancis", "Rimosotetras", "Segestrespora", "Artemopyra", "Cheilotetras",
                                "Velatitetras", "Cymbohilates", "Abditodyadus", "Tetraplanarisporites"],
    "early-glomeromycotan-fungi": ["Palaeoglomus", "Paleoglomus", "Glomites", "Archaeosporites", "Palaeoendogone",
                                   "Rugososporomyces"],
    "rhynie-chert-gametophytes": ["Lyonophyton", "Langiophyton", "Kidstonophyton", "Remyophyton"],
}
VARIANTS = {
    "aglaophyton-majus": [("Aglaophyton major", "orthographic variant; card: originally spelt 'major'"),
                          ("Rhynia major", "basionym named in the card authority")],
    "horneophyton-lignieri": [("Hornea lignieri", "EPRP card match rule; earlier genus name")],
    "rhynia-gwynne-vaughanii": [("Rhynia gwynnevaughani", "EPRP card match rule; spelling"),
                                ("Rhynia gwynnevaughanii", "EPRP card match rule; spelling")],
    "baragwanathia-brevifolioides": [("Baragwanathia brevifolia", "card authority: replaced name, a later homonym")],
}

card_names = set()
for slug, fm in cards:
    name = fm.get("name", "")
    rank = fm.get("rank", "")
    card_names.add(name)
    kind = fm.get("kind", "")
    if rank not in ("genus", "species") and slug not in ASSEMBLY:
        add(name, "card_group", slug, "card rank '%s' (group, clade, grade, site or assemblage); not searched by name" % rank,
            rank_override="higher", kind=kind)
        continue
    if slug in ASSEMBLY:
        add(name, "card_assemblage", slug, "card is an assemblage or morphogroup; members listed as card_member rows", kind=kind)
        for g in ASSEMBLY[slug]:
            add(g, "card_member", slug, "member genus used by the EPRP PBDB card match rule", kind=kind)
        continue
    add(name, "card", slug, "card name (%s)" % rank, kind=kind)
    if rank == "species":
        add(name.split()[0], "card_genus", slug, "genus of species card, for genus-level counts", kind=kind)
    for v, why in VARIANTS.get(slug, []):
        add(v, "card_variant", slug, why, synonym_of=name, kind=kind)

for g, why in [("Archaeopteris", "anchor genus"), ("Callixylon", "anchor genus (Archaeopteris wood)"),
               ("Eospermatopteris", "anchor genus (Gilboa)"), ("Wattieza", "anchor genus (Gilboa)"),
               ("Elkinsia", "anchor genus (earliest seed plant)"),
               ("Leclercqia", "anchor genus, added by the project 2026-10-27")]:
    add(g, "anchor", "", why)

for g, why in [("Prototaxites", "nematophyte; card"), ("Nematothallus", "nematophyte; card"),
               ("Nematophyton", "nematophyte named in the brief"), ("Pachytheca", "nematophyte named in the brief"),
               ("Nematasketum", "nematophyte named on the Prototaxites and Nematothallus cards"),
               ("Nematoplexus", "nematophyte named on the Nematothallus card"),
               ("Nematophycus", "older name of Nematophyton and Prototaxites in the literature; search aid, analyst knowledge"),
               ("Parka", "thalloid problematicum grouped with nematophytes by EPRP PBDB filter; Parka card planned"),
               ("Cosmochlaina", "cuticle type of Nematothallus named on the Nematothallus card"),
               ]:
    add(g, "nematophyte", "", why)
add("Spongiophyton", "problematicum", "", "thalloid problematicum that the EPRP PBDB filter flags under streptophytes; not a nematophyte named on a card")
for sp, why in [("Prototaxites taiti", "species named on the Prototaxites card"),
                ("Prototaxites loganii", "species named on the Prototaxites card"),
                ("Prototaxites southworthii", "species of Prototaxites; search aid, analyst knowledge"),
                ("Nematothallus williamii", "species named on the Nematothallus card")]:
    add(sp, "nematophyte", "", why)

for g, why in [("Palaeonitella", "charophyte named on a card"), ("Moellerina", "fossil charophyte; search aid, analyst knowledge"),
               ("Sycidium", "fossil charophyte; search aid, analyst knowledge"),
               ("Trochiliscus", "fossil charophyte; search aid, analyst knowledge"),
               ("Eochara", "fossil charophyte; search aid, analyst knowledge"),
               ("Octochara", "fossil charophyte; search aid, analyst knowledge"),
               ("Praechara", "fossil charophyte; search aid, analyst knowledge"),
               ("Chovanella", "fossil charophyte; search aid, analyst knowledge"),
               ("Mesochara", "fossil charophyte; search aid, analyst knowledge")]:
    add(g, "charophyte", "", why)

PLANNED = [("Yarravia", "Victorian taxon"), ("Hedeia", "Victorian taxon"), ("Pluricaulis biformis", "Victorian taxon"),
           ("Dawsonites", "planned card"), ("Palaeostigma", "planned card"), ("Psilotum", "living comparison taxon"),
           ("Tmesipteris", "living comparison taxon"), ("Lycopodium squarrosum", "living comparison taxon"),
           ("Ulothrix", "theory exemplar"), ("Ulva", "theory exemplar"), ("Coleochaete", "streptophyte relative"),
           ("Chara", "streptophyte relative"), ("Marchantia", "planned card"), ("Metzgeriothallus", "flagged by tranche-1 agents"),
           ("Franhueberia", "flagged by tranche-1 agents"), ("Salopella", "flagged by tranche-1 agents"),
           ("Taeniocrada", "genus named on cards"), ("Hedeia", "Victorian taxon")]
seen = set()
for n, why in PLANNED:
    if n in seen or n in card_names:
        continue
    seen.add(n)
    add(n, "planned_card", "", "planned in docs/decisions.md 2026-10-27 (%s); no card in taxa/ when this list was built" % why, kind="planned")

dedup = {}
for r in rows:
    k = (r["name"], r["role"], r["card_slug"])
    dedup.setdefault(k, r)
w = csv.DictWriter(sys.stdout, fieldnames=["name", "name_rank", "genus", "epithet", "role", "card_slug", "synonym_of", "kind", "reason"],
                   lineterminator="\n")
w.writeheader()
for r in dedup.values():
    w.writerow(r)
