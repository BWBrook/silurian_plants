"""Select community research questions bearing on early land plants from EPRP's question lists.

Usage: python3 scripts/pointers_questions.py [EPRP_CHECKOUT]  (run from data/eprp/)
Sources: the Big Questions in paleontology (Smith, Dowding et al. 2025; final, preliminary and raw
lists) and EPRP's agendas tier (published question lists; repository copy holds only rows whose
licence permits reuse). Writes pointers/community_questions_plants.tsv. Selection is a term match,
so the matched_terms column shows why each row is here; it is not a relevance judgment.
"""

import csv
import re
import subprocess
import sys
from pathlib import Path

eprp = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/bwbrook/git/eprp")
notes = eprp / "resources/library/notes"
out = Path("pointers/community_questions_plants.tsv")

TERMS = re.compile(
    r"\bplants?\b|embryophyt|tracheophyt|bryophyt|lycophyt|lycopsid|\bfloras?\b|floral|"
    r"vegetation|terrestriali[sz]|colonis\w* (of )?(the )?land|coloniz\w* (of )?(the )?land|"
    r"\bon land\b|\bland (biota|ecosystem|animals|life)|terrestrial (biota|ecosystem|life|"
    r"realm|record|environment)|\bspores?\b|palyn|\bforests?\b|\broots?\b|\bleaf|\bleaves\b|"
    r"\bwood|lignin|\bsoils?\b|weathering|\bfung(i|al|us)\b|mycorrh|herbivor|photosynth|"
    r"Ordovician|Silurian|Devonian|Palaeozoic|Paleozoic",
    re.IGNORECASE,
)

SOURCES = [
    ("big-questions-final", "big-questions-2025/final-questions.tsv", "id", "question", "eprp_nearest"),
    ("big-questions-preliminary", "big-questions-2025/preliminary-questions.tsv", "preliminary_id", "question", None),
    ("big-questions-raw", "big-questions-2025/raw-questions.tsv", None, "question", None),
    ("agendas", "question-agendas/questions.tsv", "source_id", "text", "eprp_nearest"),
]

commit = subprocess.run(
    ["git", "-C", str(eprp), "rev-parse", "--short", "HEAD"],
    capture_output=True, text=True, check=True,
).stdout.strip()

out_rows = []
for list_name, rel, id_col, text_col, near_col in SOURCES:
    with (notes / rel).open(newline="") as f:
        for i, r in enumerate(csv.DictReader(f, delimiter="\t"), start=1):
            text = r[text_col] or ""
            hits = sorted({m.group(0).lower() for m in TERMS.finditer(text)})
            if not hits:
                continue
            item = r.get("item", "")
            out_rows.append({
                "list": list_name,
                "id": (r[id_col] if id_col else f"row{i}") + (f"#{item}" if item else ""),
                "group_or_theme": r.get("theme") or r.get("working_group") or r.get("group") or r.get("themes", ""),
                "question": text,
                "eprp_nearest": r[near_col] if near_col else "",
                "matched_terms": " ".join(hits),
                "source_file": f"resources/library/notes/{rel}",
                "eprp_commit": commit,
            })

out.parent.mkdir(exist_ok=True)
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(out_rows)
print(f"{len(out_rows)} questions -> {out}")
