# scripts/update_scholar.py
from scholarly import scholarly, ProxyGenerator
import json, pathlib

AUTHOR_ID = "phhix_AAAAAJ"          # ← your Google Scholar ID

# ---- Set up a rotating proxy -------------------------------------------
pg = ProxyGenerator()
# grabs a fresh list from https://free-proxy-list.net,
# keeps only HTTPS ones that succeeded a quick test
if not pg.FreeProxies():
    print("❌  No working free proxies right now. Try again later.")
    sys.exit(0)                         # exit *cleanly* so CI doesn't turn red
scholarly.use_proxy(pg)

# ---- polite delay so you don’t hammer the same proxy cluster ------------
time.sleep(random.uniform(2, 6))


try:
     author = scholarly.fill(
                 scholarly.search_author_id(AUTHOR_ID),
                 sections=['indices'])
 except Exception as e:
    print("❌  Scholar fetch failed:", e)
    sys.exit(0)                         # fail soft


metrics = {
    "citations": author["citedby"],
    "hindex":    author["hindex"],
}

out = pathlib.Path("public/data")
out.mkdir(parents=True, exist_ok=True)
out.joinpath("scholar.json").write_text(json.dumps(metrics))
print("Wrote", out/"scholar.json", "→", metrics)
