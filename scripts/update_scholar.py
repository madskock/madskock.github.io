# scripts/update_scholar.py
from scholarly import scholarly
import json, pathlib

AUTHOR_ID = "phhix_AAAAAJ"          # ← your Google Scholar ID

author = scholarly.fill(
            scholarly.search_author_id(AUTHOR_ID),
            sections=['indices'])

metrics = {
    "citations": author["citedby"],
    "hindex":    author["hindex"],
}

out = pathlib.Path("public/data")
out.mkdir(parents=True, exist_ok=True)
out.joinpath("scholar.json").write_text(json.dumps(metrics))
print("Wrote", out/"scholar.json", "→", metrics)
