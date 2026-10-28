"""Check Codex's model-transfer proposals against the cards and apply them.

    uv run --with pyyaml python work/codex/cards-transfer/apply.py check
    uv run --with pyyaml python work/codex/cards-transfer/apply.py apply

check: every support passage must occur in its card (whitespace-normalised); every slug must exist.
apply: insert `contrasts` after placement_confidence, a `from:` key on borrowed traits, and a
"## Model transfer" section before "## Open questions". Cards that already have the section are skipped.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "out"
SKIP = set()  # slugs adjudicated out, with the reason recorded in the audit


def squash(s):
    return re.sub(r"\s+", " ", s.replace("−", "-")).strip()


def proposals():
    items = []
    for p in sorted(OUT.glob("chunk_*.json")):
        items += json.loads(p.read_text())["items"]
    return items


def check(items):
    bad = 0
    for it in items:
        card = ROOT / "taxa" / f"{it['slug']}.md"
        if not card.exists():
            print(f"{it['slug']}: no such card")
            bad += 1
            continue
        text = squash(card.read_text())
        for kind in ("can_transfer", "cannot_transfer", "borrowed"):
            for b in it[kind]:
                if squash(b["support"]) not in text:
                    bad += 1
                    print(f"{it['slug']} {kind}: support not found: {b['support'][:90]!r}")
    print(f"{len(items)} proposals, {bad} problems")
    return bad


def apply(items):
    for it in items:
        if it["slug"] in SKIP:
            continue
        card = ROOT / "taxa" / f"{it['slug']}.md"
        text = card.read_text()
        if "\n## Model transfer\n" in text:
            print(f"{it['slug']}: already has Model transfer; skipped")
            continue
        text = re.sub(r"^(placement_confidence: .*)$", lambda m: f"{m.group(1)}\ncontrasts: [{', '.join(it['contrasts'])}]",
                      text, count=1, flags=re.M)
        for b in it["borrowed"]:
            pat = re.compile(rf"^(  {b['trait']}: \{{.*)\}}\s*$", re.M)
            if not pat.search(text):
                print(f"{it['slug']}: trait line {b['trait']} not found")
                continue
            text = pat.sub(lambda m: f'{m.group(1)}, from: "{b["from_taxon"]}"}}', text, count=1)
        lines = ["## Model transfer", "", f"**Chosen to contrast:** {it['chosen_to_contrast']}", "", "- **Can transfer:**"]
        lines += [f"  - {b['text']}" for b in it["can_transfer"]]
        lines += ["- **Cannot transfer:**"] + [f"  - {b['text']}" for b in it["cannot_transfer"]]
        section = "\n".join(lines) + "\n\n"
        if "\n## Open questions" not in text:
            print(f"{it['slug']}: no Open questions heading")
            continue
        text = text.replace("\n## Open questions", "\n" + section + "## Open questions", 1)
        card.write_text(text)
    return 0


if __name__ == "__main__":
    items = proposals()
    for it in items:
        for kind in ("can_transfer", "cannot_transfer"):
            for b in it[kind]:
                b["text"] = re.sub(r"\b[Tt]he card\b", "this card", b["text"])
    if sys.argv[1] == "check":
        sys.exit(check(items))
    only = set(sys.argv[2:])
    sys.exit(apply([it for it in items if not only or it["slug"] in only]))
