"""Plockar ut sidor att länkkolla: startsidan plus ett jämnt urval ur varje sajts sitemap."""
import re, sys, urllib.request
from sajter import sajter

PER_SAJT = int(sys.argv[1]) if len(sys.argv) > 1 else 30

def hamta(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (sajtvakt)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")

def sidor(sitemap, djup=0):
    try:
        xml = hamta(sitemap)
    except Exception:
        return []
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if "<sitemapindex" in xml and djup < 2:
        ut = []
        for s in locs[:10]:
            ut += sidor(s, djup + 1)
        return ut
    return locs

for start in sajter():
    alla = [u for u in sidor(start + "sitemap.xml") if u.rstrip("/") != start.rstrip("/")]
    steg = max(1, len(alla) // PER_SAJT)
    print(start)
    for u in alla[::steg][:PER_SAJT]:
        print(u)
