"""Export the screened candidates (title, abstract, rule, decision) for the Codex screen check.

Usage (on deep-server, from _tools/): python3 library_codex_export.py  -> STORE/_build/screen_export.json
Reads _build/screen.tsv (decisions) and the store's OpenAlex records (abstracts). The export includes decisions;
library_codex.py strips them from what Codex sees.
"""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import library as L  # noqa: E402

store = Path("/data/codex/silurian_plants/library")
recs = L.load_records(store)
rows = [r for r in L.read_tsv(store / "_build" / "screen.tsv") if r["kind"] == "screen"]
out = [{"openalex_id": r["openalex_id"], "canonical_id": r["canonical_id"], "year": r["year"], "type": r["type"],
        "rule": r["rule"], "decision": r["decision"], "title": r["title"],
        "abstract": re.sub(r"\s+", " ", L.abstract_text(recs[r["openalex_id"]])).strip()} for r in rows]
(store / "_build" / "screen_export.json").write_text(json.dumps(out, ensure_ascii=False))
print(len(out), "screened records exported")
