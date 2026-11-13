"""Check every quote in a loop1b extraction against its paged source text.

    python3 work/codex/loop1b/verify.py library/closed/extract/misc.json

Writes <out>.verified.json with verified_in_text per finding and prints a summary.
Matching ignores whitespace, line-break hyphens, curly quotes and ligature artefacts.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TEXT = ROOT / "library" / "closed" / "text"


def norm(s):
    s = s.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("­", "")
    s = re.sub(r"[‘’‛`´]", "'", s)
    s = re.sub(r"[“”„]", '"', s)
    s = re.sub(r"[‐-―−]", "-", s)
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"=== PDF page \d+ ===", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def main(path):
    data = json.load(open(path))
    cache, bad = {}, []
    for f in data["items"]:
        name = Path(f["file"]).name
        stem = name.replace(".paged.txt", "").replace(".txt", "").replace(".pdf", "")
        if stem not in cache:
            p = TEXT / f"{stem}.paged.txt"
            cache[stem] = norm(p.read_text()) if p.exists() else None
        text = cache[stem]
        q = norm(f["quote"])
        ok = bool(text) and bool(q) and (q in text or q.replace("-", "") in text.replace("-", ""))
        f["verified_in_text"] = ok
        if not ok:
            bad.append((f["finding_id"], stem, f["quote"][:90]))
    json.dump(data, open(str(path).replace(".json", ".verified.json"), "w"), indent=1, ensure_ascii=False)
    n = len(data["items"])
    print(f"{path}: {n - len(bad)}/{n} quotes verified; {len(data['recommendations'])} recommendations")
    for b in bad:
        print("  UNVERIFIED", *b)


for p in sys.argv[1:]:
    main(p)
