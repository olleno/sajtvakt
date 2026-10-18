"""Sammanställer Lighthouse-resultat: tabell i ett ärende och varning om något blivit klart sämre."""
import json, sys
from pathlib import Path

GRANS_TAPP = 15   # så många poäng ska något tappa på en vecka innan vi varnar
GRANS_SEO = 90
KAT = [("performance", "Fart"), ("seo", "SEO"), ("accessibility", "Tillgänglighet"), ("best-practices", "Kvalitet")]

def poang(fil):
    d = json.loads(Path(fil).read_text())
    return {k: round((d["categories"][k]["score"] or 0) * 100) for k, _ in KAT}

nu = {}
for fil in sorted(Path(sys.argv[1]).glob("*.json")):
    try:
        nu[fil.stem] = poang(fil)
    except Exception:
        nu[fil.stem] = None

forra_fil = Path("resultat/fart.json")
forra = json.loads(forra_fil.read_text()) if forra_fil.exists() else {}

rader = ["| Sajt | " + " | ".join(n for _, n in KAT) + " |", "|---" * (len(KAT) + 1) + "|"]
varningar = []
for sajt, p in nu.items():
    if p is None:
        rader.append(f"| {sajt} | kunde inte mätas |" + " |" * (len(KAT) - 1))
        continue
    celler = []
    for k, namn in KAT:
        f = (forra.get(sajt) or {}).get(k)
        diff = f" ({p[k] - f:+d})" if f is not None and p[k] != f else ""
        celler.append(f"{p[k]}{diff}")
        if f is not None and f - p[k] >= GRANS_TAPP:
            varningar.append(f"- **{sajt}**: {namn} föll från {f} till {p[k]}")
    if p["seo"] < GRANS_SEO:
        varningar.append(f"- **{sajt}**: SEO-grunderna ger bara {p['seo']} av 100")
    rader.append(f"| {sajt} | " + " | ".join(celler) + " |")

forra_fil.write_text(json.dumps(nu, indent=1, ensure_ascii=False))
Path("rapport.md").write_text(
    "Mätt på mobil med Google Lighthouse, 0–100 där 100 är bäst. Siffran inom parentes är ändringen sedan förra veckan.\n\n"
    + "\n".join(rader) + "\n")
Path("varningar.md").write_text("\n".join(varningar))
print(Path("rapport.md").read_text()); print("\n".join(varningar))
