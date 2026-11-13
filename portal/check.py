# /// script
# requires-python = ">=3.12"
# dependencies = ["beautifulsoup4==4.14.3", "Markdown==3.10.2", "PyYAML==6.0.3"]
# ///
"""Check generated links, source coverage, freshness and preservation of the scientific text."""

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import markdown
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "portal/dist"


def normalise(value):
    return re.sub(r"\s+", " ", value).strip()


def main():
    manifest = json.loads((OUT / "provenance.json").read_text())
    pages = {p: BeautifulSoup(p.read_text(), "html.parser") for p in OUT.rglob("*.html")}
    errors = []
    count_links = 0
    ids = {p: {tag["id"] for tag in soup.find_all(id=True)} for p, soup in pages.items()}
    for path, soup in pages.items():
        label = path.relative_to(OUT)
        if len(soup.find_all("h1")) != 1 or not soup.select_one("main"):
            errors.append(f"{label}: must have one h1 and a main element")
        for tag in soup.find_all(["a", "img", "link", "script", "form"]):
            attribute = "src" if tag.name in ("img", "script") else "action" if tag.name == "form" else "href"
            url = tag.get(attribute)
            if not url:
                continue
            parts = urlsplit(url)
            if parts.scheme or parts.netloc:
                continue
            target = (path.parent / unquote(parts.path)).resolve() if parts.path else path
            count_links += 1
            if not target.is_relative_to(OUT) or not target.is_file():
                errors.append(f"{label}: missing local target {url}")
            elif parts.fragment and target.suffix == ".html" and unquote(parts.fragment) not in ids[target]:
                errors.append(f"{label}: missing anchor {url}")
        for image in soup.find_all("img"):
            if not image.get("alt"):
                errors.append(f"{label}: missing image description")
    for relative, source in manifest["sources"].items():
        path = ROOT / relative
        if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
            errors.append(f"Stale content: {relative}")
        if not relative.endswith(".md"):
            if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}:
                copied = OUT / relative
                if not copied.is_file() or hashlib.sha256(copied.read_bytes()).hexdigest() != source["sha256"]:
                    errors.append(f"Illustration differs from source: {relative}")
            continue
        output = OUT / ("docs/project-readme.html" if relative == "README.md" else str(Path(relative).with_suffix(".html")))
        if output not in pages:
            errors.append(f"Missing rendered source: {relative}")
            continue
        soup = pages[output]
        body = path.read_text()
        if body.startswith("---\n"):
            front, body = re.split(r"\n---\n", body, maxsplit=1)
            meta = yaml.safe_load(front.removeprefix("---\n"))
            if set(meta.get("contrasts") or []) != {tag["data-contrast"] for tag in soup.select("[data-contrast]")}:
                errors.append(f"Contrasts differ from source: {relative}")
            for trait, record in (meta.get("traits") or {}).items():
                if record and record.get("from"):
                    origin = soup.select_one(f'tr[data-trait="{trait}"] .trait-origin')
                    if origin is None or record["from"] not in origin.get_text():
                        errors.append(f"Missing borrowed trait origin: {relative} / {trait}")
        expected = BeautifulSoup(markdown.markdown(body, extensions=["extra", "toc", "sane_lists"]), "html.parser")
        if expected.h1:
            expected.h1.decompose()
        actual = BeautifulSoup(str(soup.select_one("article.prose")), "html.parser")
        for anchor in actual.select(".heading-anchor"):
            anchor.decompose()
        if normalise(expected.get_text(" ")) != normalise(actual.get_text(" ")):
            errors.append(f"Scientific body text differs from source: {relative}")
        source_url = f'{manifest["repository"]}/blob/{manifest["revision"]}/{relative}'
        if not any(a["href"] == source_url for a in soup.select(".source-meta a")):
            errors.append(f"Missing versioned Markdown source link: {relative}")
    cards = {p.name for p in (ROOT / "taxa").glob("*.md") if not p.name.startswith(("README", "_"))}
    rendered_cards = {p.with_suffix(".md").name for p in (OUT / "taxa").glob("*.html")}
    if cards != rendered_cards:
        errors.append("Rendered atlas does not contain exactly the source cards")
    index = json.loads((OUT / "search-index.json").read_text())
    indexed = {entry["url"] for entry in index}
    reading_links = {a["href"] for a in pages[OUT / "reading.html"].select("main a[href]")}
    for relative in manifest["sources"]:
        if relative.startswith(("docs/", "studies/")) and "/docs/" in "/" + relative and relative.endswith(".md") and str(Path(relative).with_suffix(".html")) not in reading_links:
            errors.append(f"Document missing from reading room: {relative}")
    for path in pages:
        relative = path.relative_to(OUT).as_posix()
        if relative.startswith(("docs/", "taxa/", "data/", "studies/")) and relative not in indexed:
            errors.append(f"Missing from search index: {relative}")
    assets = json.loads((ROOT / "portal/images.json").read_text())
    for key, image in assets.items():
        for field in ("file", "title", "caption", "creator", "license", "license_url", "source_url", "alt", "kind", "changes"):
            if not image.get(field):
                errors.append(f"Image {key}: missing {field}")
        if not (OUT / image["file"]).is_file():
            errors.append(f"Image {key}: missing asset")
    forbidden = [p for p in OUT.rglob("*") if p.is_file() and ("local" in p.relative_to(OUT).parts or "closed" in p.relative_to(OUT).parts or p.suffix.lower() in (".pdf", ".sqlite", ".env"))]
    if forbidden:
        errors.append(f"Unexpected private payloads: {forbidden}")
    for error in errors:
        print(error)
    print(f"{len(pages)} pages, {len(cards)} cards, {len(index)} searchable sources, {count_links} local links: {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
