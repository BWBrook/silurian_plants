# /// script
# requires-python = ">=3.12"
# dependencies = ["Markdown==3.10.2", "PyYAML==6.0.3", "beautifulsoup4==4.14.3"]
# ///
"""Generate the private reading portal from repository Markdown. Run with uv run portal/build.py."""

import argparse
import csv
import hashlib
import html
import json
import math
import posixpath
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

import markdown
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
PORTAL = ROOT / "portal"
OUT = PORTAL / "dist"
REPO = "https://github.com/BWBrook/silurian_plants"
CORE = [
    ("primer", "The primer", "The period, its plants and the nature of the fossil record.", "01"),
    ("framings", "Research framings", "Seven candidate questions, their evidence and their trade-offs.", "02"),
    ("precedents", "Modelling precedents", "What has already been modelled, and where the gaps remain.", "03"),
    ("sources", "The evidence base", "A register of the data held, needed and ruled out.", "04"),
]
SUPPORT = [("charter", "Project charter"), ("decisions", "Decision record"),
           ("spore-compilation-plan", "Spore compilation plan")]
GROUP_NAMES = {"incertae-sedis": "Uncertain affinity", "lycopsid": "Lycopsids",
               "rhyniophytoid": "Rhyniophytoids", "zosterophyll": "Zosterophylls",
               "cryptospore-plant": "Cryptospore plants", "nematophyte": "Nematophytes",
               "basal-euphyllophyte": "Basal euphyllophytes", "protracheophyte": "Protracheophytes",
               "streptophyte-alga": "Streptophyte algae", "chlorophyte-alga": "Chlorophyte algae",
               "bryophyte": "Bryophytes", "fern": "Ferns", "fungus": "Fungi", "lichen": "Lichens",
               "progymnosperm": "Progymnosperms", "cladoxylopsid": "Cladoxylopsids",
               "tracheophyte-other": "Other tracheophytes"}
KIND_NAMES = {"megafossil": "Megafossil", "mesofossil": "Mesofossil", "dispersed_spores": "Dispersed spores",
              "assemblage": "Assemblage", "group": "Group", "extant": "Living comparison"}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def esc(value):
    return html.escape(str(value), quote=True)


def pretty(value):
    return str(value).replace("_", " ").replace("-", " ").capitalize()


def write(path, content):
    destination = OUT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="store_true", help="Also copy the generated site into .site-publish/ for Sites publication")
    args = parser.parse_args()
    tracked = [Path(p) for p in git("ls-files", "-z").split("\0") if p]
    paths = sorted(ROOT / p for p in tracked if p.parts[0] == "docs" and p.suffix == ".md")
    paths += sorted(ROOT / p for p in tracked if p.parts[0] == "data" and p.name == "README.md"
                    and not {"local", "closed", "work"}.intersection(p.parts))
    paths += [ROOT / "README.md"]
    cards = sorted(ROOT / p for p in tracked if p.parent == Path("taxa") and p.suffix == ".md"
                   and not p.name.startswith(("_", "README")))
    source_paths = paths + cards + [ROOT / "data/timescale.csv"]
    revision = git("rev-parse", "HEAD")
    content_revision = git("log", "-1", "--format=%H", "--", *[str(p.relative_to(ROOT)) for p in source_paths])
    dirty = bool(git("status", "--porcelain", "--", "docs", "taxa", "README.md", "data/timescale.csv",
                     *[str(p.relative_to(ROOT)) for p in paths if p.is_relative_to(ROOT / "data")]))
    if dirty:
        raise SystemExit("Commit the authoritative Markdown/timescale changes before building a source-linked portal.")
    generated = datetime.now(ZoneInfo("Australia/Hobart")).strftime("%d %b %Y, %H:%M %Z")
    images = json.loads((PORTAL / "images.json").read_text()) if (PORTAL / "images.json").exists() else {}
    stages = {r["stage"]: r for r in csv.DictReader((ROOT / "data/timescale.csv").open())}
    stage_order = list(stages)
    routes = {p.relative_to(ROOT).as_posix(): p.relative_to(ROOT).with_suffix(".html").as_posix() for p in paths + cards}
    routes["taxa/README.md"] = "atlas.html"
    routes["README.md"] = "docs/project-readme.html"
    search = []
    provenance = {}
    metadata = {}
    for p in source_paths:
        relative = p.relative_to(ROOT).as_posix()
        provenance[relative] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                                "updated": git("log", "-1", "--format=%cs", "--", relative)}
    for p in cards:
        text = p.read_text()
        match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
        if not match:
            raise ValueError(f"Missing card front matter: {p}")
        meta = yaml.safe_load(match[1])
        metadata[p.stem] = (meta, match[2])
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for name in ("style.css", "app.js", "favicon.svg"):
        shutil.copy2(PORTAL / name, OUT / name)
    if (PORTAL / "assets").exists():
        shutil.copytree(PORTAL / "assets", OUT / "assets")

    def root_link(target, current):
        return posixpath.relpath(target, posixpath.dirname(current) or ".")

    def source_link(path, fragment=""):
        return f"{REPO}/blob/{revision}/{quote(path, safe='/')}" + ("#" + fragment if fragment else "")

    def mapped_link(href, source, current):
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or not parts.path:
            return href
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parts.path)))
        if target in routes:
            return urlunsplit(("", "", root_link(routes[target], current), parts.query, parts.fragment))
        return source_link(target, parts.fragment)

    def render(body, source, current):
        md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"], extension_configs={
            "toc": {"permalink": False, "toc_depth": "2-3"}})
        rendered = md.convert(body)
        soup = BeautifulSoup(rendered, "html.parser")
        for link in soup.find_all("a", href=True):
            link["href"] = mapped_link(link["href"], source, current)
        for table in soup.find_all("table"):
            wrapper = soup.new_tag("div", attrs={"class": "table-scroll", "tabindex": "0", "role": "region", "aria-label": "Scrollable table"})
            table.wrap(wrapper)
        for heading in soup.find_all(["h2", "h3"]):
            if heading.get("id"):
                anchor = soup.new_tag("a", attrs={"class": "heading-anchor", "href": "#" + heading["id"], "aria-label": "Link to " + heading.get_text()})
                anchor.string = "#"
                heading.append(anchor)
        title = soup.h1.get_text() if soup.h1 else None
        if soup.h1:
            soup.h1.decompose()
        plain = soup.get_text(" ", strip=True)
        return str(soup), md.toc, plain, title

    def picture(key, current, css="", caption=True, eager=False):
        item = images.get(key)
        if not item:
            return ""
        credit = f'{esc(item["creator"])} · <a href="{esc(item["license_url"])}">{esc(item["license"])}</a> · {esc(item.get("changes", ""))}'
        label = f'<span class="image-kind">{esc(item["kind"])}</span>'
        figcaption = f'<figcaption>{label}{esc(item["caption"])} <span class="credit"><a href="{esc(item["source_url"])}">Image source</a> · {credit}</span></figcaption>' if caption else (f'<span class="thumbnail-label">{esc(item["kind"])}</span>' if css == "tile-image" else "")
        return f'<figure class="{css}"><img src="{root_link(item["file"], current)}" alt="{esc(item["alt"])}" loading="{"eager" if eager else "lazy"}" decoding="async">{figcaption}</figure>'

    def page(title, content, current, section="home", toc="", source=None, extra_class=""):
        def url(path):
            return root_link(path, current)
        menu = "".join(f'<a class="{"active" if section == key else ""}" href="{url(path)}"{" aria-current=\"page\"" if current == path else ""}>{label}</a>' for key, path, label in [
            ("home", "index.html", "Overview"), ("reading", "reading.html", "Reading room"), ("atlas", "atlas.html", "Taxon atlas")])
        side = ""
        if section == "reading" and current != "reading.html":
            links = [(f"docs/{slug}.html", label) for slug, label, *_ in CORE] + [(f"docs/{slug}.html", label) for slug, label in SUPPORT]
            side = '<aside class="book-nav"><p class="eyebrow">Reading room</p>' + "".join(f'<a href="{url(path)}" class="{"active" if path == current else ""}"{" aria-current=\"page\"" if path == current else ""}>{label}</a>' for path, label in links) + f'<a class="back-link" href="{url("reading.html")}">All documents ↗</a></aside>'
        elif section == "atlas" and source:
            side = f'<aside class="book-nav"><a class="back-link" href="{url("atlas.html")}">← Browse the atlas</a><p class="eyebrow">Nearby in the collection</p>'
            slug = Path(source).stem
            group = metadata[slug][0]["group"]
            related = [(s, m["name"]) for s, (m, _) in metadata.items() if m["group"] == group and s != slug][:6]
            side += "".join(f'<a href="{url("taxa/" + s + ".html")}">{esc(name)}</a>' for s, name in related) + "</aside>"
        source_meta = ""
        if source:
            source_meta = f'<div class="source-meta"><a href="{source_link(source)}">View Markdown source ↗</a><span>Source updated {provenance[source]["updated"]}</span><span>Revision <a href="{REPO}/commit/{revision}">{revision[:7]}</a></span></div>'
        toc_html = f'<aside class="page-toc"><p class="eyebrow">On this page</p>{toc}<a class="back-link" href="#top">Back to top ↑</a></aside>' if toc else ""
        layout = f'<div class="reading-layout {"has-side" if side else ""} {"has-toc" if toc else ""}">{side}<main id="main" class="{extra_class}">{content}{source_meta}</main>{toc_html}</div>' if side or toc else f'<main id="main" class="wide-main {extra_class}">{content}{source_meta}</main>'
        full = f'''<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="Private research reading room and taxon atlas for early land-plant evolution."><title>{esc(title)} · Early Land Plants</title><link rel="icon" href="{url("favicon.svg")}" type="image/svg+xml"><link rel="stylesheet" href="{url("style.css")}"><script src="{url("app.js")}" defer></script></head>
<body id="top" data-base="{url("index.html").removesuffix("index.html")}" data-page="{section}"><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="{url("index.html")}"><span class="brand-mark" aria-hidden="true">✳</span><span>Early Land Plants<small>A research library</small></span></a><nav aria-label="Main navigation">{menu}</nav><form action="{url("search.html")}" class="header-search" role="search"><label class="sr-only" for="global-search">Search the library</label><span aria-hidden="true">⌕</span><input id="global-search" name="q" placeholder="Search the library" type="search"><kbd>/</kbd></form></header>
{layout}
<footer class="site-footer"><div><strong>Early Land Plants</strong><span>Barry W. Brook · Research in progress</span></div><div><a href="{url("about.html")}">About & image credits</a><a href="{REPO}">GitHub source ↗</a><span class="private-label">Private library</span></div><p>Generated {generated} · Content {content_revision[:7]} · Markdown is authoritative.</p></footer></body></html>'''
        write(current, full)

    summaries = {}
    for slug, (meta, body) in metadata.items():
        brief = re.search(r"## In brief\s*\n(.*?)(?=\n## |\Z)", body, re.S)
        summaries[slug] = BeautifulSoup(markdown.markdown(brief[1] if brief else body[:400]), "html.parser").get_text(" ", strip=True)

    def range_label(meta):
        first, last = meta["range"].get("first"), meta["range"].get("last")
        if not first:
            return "Extant only"
        return first if first == last else f'{first} – {last or "Recent"}'

    def tile(slug, current, featured=False):
        meta, _ = metadata[slug]
        image = picture(slug, current, css="tile-image", caption=False)
        if not image:
            image = '<div class="specimen-placeholder" aria-hidden="true"><span>✳</span><small>' + esc(KIND_NAMES[meta["kind"]]) + '</small></div>'
        first = meta["range"].get("first")
        first_index = stage_order.index(first) if first in stages else -1
        last = meta["range"].get("last")
        last_index = stage_order.index(last) if last in stages else 0
        periods = sorted({stages[s]["period"] for s in stage_order[last_index:first_index + 1]}) if first_index >= 0 else []
        search_text = f'{meta["name"]} {meta["group"]} {meta.get("authority", "")} {" ".join(meta.get("regions") or [])} {summaries[slug]}'
        return f'''<a class="taxon-tile" href="{root_link("taxa/" + slug + ".html", current)}" data-name="{esc(meta["name"])}" data-group="{esc(meta["group"])}" data-kind="{esc(meta["kind"])}" data-periods="{esc(" ".join(periods))}" data-age="{stages[first]["base_ma"] if first in stages else 0}" data-search="{esc(search_text)}">{image}<div class="tile-body"><span class="eyebrow">{esc(GROUP_NAMES.get(meta["group"], pretty(meta["group"])))}</span><h3>{esc(meta["name"])}</h3><p>{esc(summaries[slug][:155])}{"…" if len(summaries[slug]) > 155 else ""}</p><div class="tile-meta"><span>{esc(range_label(meta))}</span><span>{esc(meta["status"])}</span></div></div></a>'''

    for p in paths:
        source = p.relative_to(ROOT).as_posix()
        current = routes[source]
        body = p.read_text()
        rendered, toc, plain, title = render(body, source, current)
        title = title or p.stem.replace("-", " ").title()
        words = len(plain.split())
        label = "Audit & evidence" if "/audits/" in source else "Source documentation" if source.startswith("data/") else "Reading room"
        content = f'<div class="article-header"><p class="eyebrow">{label}</p><h1>{esc(title)}</h1><p class="article-meta">{max(1, math.ceil(words / 220))} min read <span>·</span> Research in progress</p></div><article class="prose">{rendered}</article>'
        page(title, content, current, "reading", toc, source)
        search.append({"title": title, "type": label, "url": current, "text": plain})

    for slug, (meta, body) in metadata.items():
        source = f"taxa/{slug}.md"
        current = routes[source]
        rendered, toc, plain, _ = render(body, source, current)
        traits = []
        for key, value in (meta.get("traits") or {}).items():
            if not value:
                continue
            if "state" in value:
                state = value["state"]
            else:
                unit = " cm" if key == "height_cm" else " mm" if key == "axis_diameter_mm" else ""
                low, high = value.get("min"), value.get("max")
                state = str(low) if low == high else f'{low if low is not None else "?"}–{high if high is not None else "?"}'
                state += unit
            traits.append(f'<tr><th scope="row">{esc(pretty(key.removesuffix("_cm").removesuffix("_mm")))}</th><td>{esc(state)}</td><td>{esc(value.get("note", ""))}</td></tr>')
        traits_html = f'<section class="card-data"><h2 id="trait-record">Structured trait record</h2><p class="data-note">Absent = observed absent; unknown = not preserved or not reported; na = not applicable.</p><div class="table-scroll" tabindex="0" role="region" aria-label="Structured traits"><table><thead><tr><th>Trait</th><th>Record</th><th>Source notes</th></tr></thead><tbody>{"".join(traits)}</tbody></table></div></section>' if traits else ""
        localities = meta.get("localities") or []
        locals_html = '<h3>Localities</h3><ul>' + "".join(f'<li>{esc(x)}</li>' for x in localities) + '</ul>' if localities else ""
        refs = []
        for ref in meta.get("references") or []:
            doi = ref.get("doi")
            refs.append(f'<li>{esc(ref.get("cite", ""))}' + (f' <a href="https://doi.org/{quote(str(doi), safe="/[]():;.-")}">{esc(doi)}</a>' if doi else "") + '</li>')
        source_data = f'<section class="prose card-data"><h2 id="card-metadata">Card metadata</h2><p>{esc(meta.get("lineage", ""))}</p><dl class="detail-list"><dt>Rank</dt><dd>{esc(meta.get("rank", ""))}</dd><dt>Age notes</dt><dd>{esc(meta["range"].get("notes", ""))}</dd><dt>Regions</dt><dd>{esc(", ".join(meta.get("regions") or []))}</dd><dt>Preservation</dt><dd>{esc(", ".join(meta.get("preservation") or [])) or "Not specified"}</dd><dt>Habitat</dt><dd>{esc(meta.get("habitat", ""))}</dd><dt>Placement confidence</dt><dd>{esc(meta["placement_confidence"])}</dd><dt>Card updated</dt><dd>{esc(meta.get("updated", ""))}</dd></dl>{locals_html}</section>'
        toc_soup = BeautifulSoup(toc, "html.parser")
        ul = toc_soup.find("ul")
        if ul:
            for anchor, label in [("trait-record", "Structured traits"), ("card-metadata", "Card metadata"), ("references", "References")]:
                if anchor == "trait-record" and not traits:
                    continue
                li = toc_soup.new_tag("li")
                a = toc_soup.new_tag("a", href="#" + anchor)
                a.string = label
                li.append(a)
                ul.append(li)
        content = f'<div class="article-header taxon-heading"><p class="eyebrow">Taxon atlas / {esc(GROUP_NAMES.get(meta["group"], pretty(meta["group"])))}</p><h1>{esc(meta["name"])}</h1><p class="authority">{esc(meta.get("authority", ""))}</p><div class="badges"><span>{esc(KIND_NAMES[meta["kind"]])}</span><span class="status">{esc(meta["status"])}</span></div><p class="age-range">{esc(range_label(meta))}</p></div>{picture(slug, current, "taxon-figure", eager=True)}<article class="prose">{rendered}</article>{traits_html}{source_data}<section class="prose card-data"><h2 id="references">References</h2><ol class="references">{"".join(refs)}</ol></section>'
        page(meta["name"], content, current, "atlas", str(toc_soup), source)
        search.append({"title": meta["name"], "type": "Taxon card", "url": current,
                       "text": BeautifulSoup(content, "html.parser").get_text(" ", strip=True)})

    reading_cards = "".join(f'<a class="reading-card" href="docs/{slug}.html"><span class="chapter">{number}</span><h2>{label}</h2><p>{description}</p><span class="text-link">Start reading ↗</span></a>' for slug, label, description, number in CORE)
    support_cards = "".join(f'<a href="docs/{slug}.html">{label}<span>↗</span></a>' for slug, label in SUPPORT)
    doc_rows = []
    for entry in search:
        if entry["type"] in ("Audit & evidence", "Source documentation"):
            doc_rows.append(f'<a class="document-row" href="{entry["url"]}"><span>{esc(entry["title"])}</span><small>{entry["type"]}</small><span aria-hidden="true">↗</span></a>')
    page("Reading room", f'<div class="section-heading"><p class="eyebrow">The reading room</p><h1>A foundation for the science.</h1><p class="lede">The period, the competing questions and the evidence behind them. Read the project as a connected collection.</p></div><div class="reading-grid">{reading_cards}</div><section class="section-block"><div class="section-title"><h2>How the programme is taking shape</h2><p>Purpose, decisions and working plans</p></div><div class="support-links">{support_cards}</div></section><section class="section-block"><div class="section-title"><h2>Audits & source documentation</h2><p>Trace the work back to its evidence.</p></div><div class="document-list">{"".join(doc_rows)}</div></section>', "reading.html", "reading")
    groups = sorted({m["group"] for m, _ in metadata.values()}, key=lambda g: GROUP_NAMES.get(g, g))
    kinds = sorted({m["kind"] for m, _ in metadata.values()})
    group_options = "".join(f'<option value="{g}">{GROUP_NAMES.get(g, pretty(g))}</option>' for g in groups)
    kind_options = "".join(f'<option value="{k}">{KIND_NAMES[k]}</option>' for k in kinds)
    tiles = "".join(tile(slug, "atlas.html") for slug in sorted(metadata, key=lambda s: metadata[s][0]["name"].casefold()))
    page("Taxon atlas", f'''<div class="section-heading atlas-heading"><p class="eyebrow">The taxon atlas</p><h1>Meet the early terrestrial world.</h1><p class="lede">{len(cards)} cards spanning fossil plants, associated organisms, assemblages and living comparisons. All retain their source status.</p></div><form class="atlas-filters" id="atlas-filters"><label class="atlas-query">Find a taxon<input type="search" name="q" id="atlas-query" placeholder="Name, region or keyword…"></label><label>Group<select name="group">{ '<option value="">All groups</option>' + group_options}</select></label><label>Record type<select name="kind"><option value="">All types</option>{kind_options}</select></label><label>Interval<select name="period"><option value="">All intervals</option><option>Ordovician</option><option>Silurian</option><option>Devonian</option><option value="extant">Living comparisons</option></select></label><label>Order<select name="sort"><option value="name">Name A–Z</option><option value="age">First appearance</option></select></label><button class="reset-button" type="reset">Reset</button></form><div class="atlas-summary"><p id="atlas-count" role="status" aria-live="polite">{len(cards)} cards</p><p>Interval filters use the card’s recorded range; living taxa may also have fossil ranges.</p></div><div id="atlas-grid" class="atlas-grid">{tiles}</div><div id="atlas-empty" class="empty-state" hidden><h2>No cards match these filters.</h2><p>Try a broader keyword, or reset the filters to see the full collection.</p><button data-reset-atlas>Reset filters</button></div><noscript><p>Enable JavaScript to filter the atlas. All cards are displayed above.</p></noscript>''', "atlas.html", "atlas")
    page("Search the library", '<div class="section-heading"><p class="eyebrow">Across the collection</p><h1>Search the library.</h1><p class="lede">Find names, concepts and evidence across the documents and taxon cards.</p></div><form id="library-search" class="library-search" role="search"><label class="sr-only" for="search-query">Search query</label><input type="search" id="search-query" name="q" placeholder="Try sporophyte, Cooksonia or sampling…"><button type="submit">Search ↗</button></form><p id="search-count" role="status" aria-live="polite">Enter a word or phrase to search.</p><div id="search-results" class="search-results"></div><noscript><p>Full-text search needs JavaScript. Browse the reading room and atlas using the navigation above.</p></noscript>', "search.html", "search")
    hero = picture("hero", "index.html", "hero-image", eager=True)
    featured = [s for s in ("cooksonia", "asteroxylon-mackiei", "marchantia-polymorpha") if s in metadata]
    home = f'''<section class="home-hero"><div class="hero-copy"><p class="eyebrow">Late Ordovician → Early Devonian</p><h1>The first chapters<br>of life on land.</h1><p class="lede">An evolving research library on early land plants: their forms, their world and the questions we can test.</p><div class="hero-actions"><a class="button" href="reading.html">Enter the reading room <span>↗</span></a><a class="quiet-link" href="atlas.html">Explore the atlas →</a></div><p class="hero-note">Exploratory research · A working collection</p></div>{hero or '<div class="hero-botanical" aria-hidden="true">✳</div>'}</section><div class="collection-strip"><span><strong>{len(cards):02d}</strong> taxon & assemblage cards</span><span><strong>{len(CORE):02d}</strong> core reading documents</span><span><strong>01</strong> evolving evidence base</span><span class="strip-note">A private working collection</span></div><section class="section-block"><div class="section-title"><div><p class="eyebrow">Begin with the context</p><h2>Four ways into the project.</h2></div><a href="reading.html">All documents ↗</a></div><div class="reading-grid">{reading_cards}</div></section><section class="section-block"><div class="section-title"><div><p class="eyebrow">From the atlas</p><h2>Forms that changed the story.</h2></div><a href="atlas.html">Browse all {len(cards)} cards ↗</a></div><div class="featured-grid">{"".join(tile(s, "index.html", True) for s in featured)}</div></section><section class="project-note"><p class="eyebrow">An evolving programme</p><h2>Follow the evidence and the decisions.</h2><p>Read the project charter and decision record alongside the evidence. Card status, source dates and uncertainty are carried through from the Markdown.</p><a href="docs/charter.html">Read the project charter ↗</a></section>'''
    page("Research library", home, "index.html")
    credits = []
    seen = set()
    for key, item in images.items():
        if item["file"] in seen:
            continue
        seen.add(item["file"])
        credits.append(f'<div class="credit-row">{picture(key, "about.html", caption=False)}<div><h3>{esc(item["title"])}</h3><p>{esc(item["caption"])}</p><p>{esc(item["creator"])} · <a href="{esc(item["license_url"])}">{esc(item["license"])}</a> · <a href="{esc(item["source_url"])}">Original source ↗</a></p><p>{esc(item.get("changes", ""))}</p></div></div>')
    about = f'<div class="section-heading"><p class="eyebrow">About this library</p><h1>A reading view of the research.</h1><p class="lede">The Markdown in the private GitHub repository remains authoritative. This portal is generated from it, without rewriting the scientific text.</p></div><article class="prose"><h2>Sources and refreshes</h2><p>Each document and taxon card links to its exact source revision. The portal is refreshed on request, rather than after every GitHub push. This edition was generated {generated} from repository revision <a href="{REPO}/commit/{revision}">{revision[:7]}</a>. The latest content commit included is {content_revision[:7]}.</p><p>The portal includes project documents, audit notes, source README files and the taxon cards. Data files and other repository material link back to GitHub. Untracked full texts, closed literature and bulky remote datasets are not included.</p><h2>Scientific status</h2><p>Rendering is not scientific validation. Draft status, source dates, disputes and uncertainty are preserved. Some source documents describe earlier stages of the work; their dates and linked decision records should be read together.</p><h2>People and systems</h2><p>The research contributors and their roles are recorded in the <a href="docs/charter.html#contributors-and-ai-roles">project charter</a>. The reading portal was implemented with OpenAI Codex; its code and refresh instructions are versioned with the project.</p><h2>Images</h2><p>Images are supplementary illustrations. Captions identify specimens, reconstructions and living comparisons. They do not add observations or trait scores to the authoritative cards. Image attribution and licence links follow below; web copies may be resized or re-encoded.</p></article><div class="image-credits">{"".join(credits)}</div>'
    page("About & image credits", about, "about.html")
    write("search-index.json", json.dumps(search, ensure_ascii=False))
    write("provenance.json", json.dumps({"repository": REPO, "revision": revision, "content_revision": content_revision,
          "generated": generated, "sources": provenance, "image_manifest_sha256": hashlib.sha256((PORTAL / "images.json").read_bytes()).hexdigest() if images else None}, indent=2))
    write("robots.txt", "User-agent: *\nDisallow: /\n")
    if args.stage:
        destination = ROOT / ".site-publish"
        destination.mkdir(exist_ok=True)
        if (destination / "dist").exists():
            shutil.rmtree(destination / "dist")
        shutil.copytree(OUT, destination / "dist")
        (destination / ".openai").mkdir(exist_ok=True)
        shutil.copy2(PORTAL / ".openai/hosting.json", destination / ".openai/hosting.json")
        (destination / "README.md").write_text("# Early Land Plants — generated private portal\n\nGenerated from https://github.com/BWBrook/silurian_plants\n\n"
            f"Source revision: {revision}\nContent revision: {content_revision}\n\n"
            "Do not edit generated files here. Edit the Markdown or portal renderer in the authoritative repository, then refresh.\n")
    print(f"Generated {len(paths)} documents, {len(cards)} taxon cards and {len(seen)} images in {OUT}")
    print(f"Source revision: {revision}; content revision: {content_revision}")


if __name__ == "__main__":
    main()
