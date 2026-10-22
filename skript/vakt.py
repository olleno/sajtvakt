"""Kollar att varje sajt svarar.

Nere  -> ett tyst ärende öppnas direkt (etiketten `nere`).
Nere i mer än 15 minuter -> larm: Olle nämns (@olleno) och tilldelas ärendet, vilket ger
    ett mejl från GitHub med ämnet "🔴 NERE: <sajt>" och vad han ska göra. Upprepas var 6:e timme.
Uppe igen -> ärendet byter namn till "✅ UPPE IGEN: <sajt>", Olle nämns (mejl) och ärendet stängs.
    Var sajten nere kortare än 15 minuter stängs ärendet tyst.
"""
import json, os, subprocess, time, urllib.request, urllib.error
from datetime import datetime, timezone
from sajter import sajter

OLLE = "olleno"
VANTA_MIN = int(os.environ.get("VANTA_MIN", "15"))      # så länge innan första larmet
UPPREPA_H = float(os.environ.get("UPPREPA_H", "6"))     # nytt larm så här ofta
LARM = "<!-- larm -->"                                  # märker våra larmkommentarer
NERE, UPPE = "🔴 NERE: ", "✅ UPPE IGEN: "


def svarar(url):
    """(ok, felbeskrivning, vercel-felkod)"""
    fel, kod = "", ""
    for forsok in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (sajtvakt; +https://github.com/olleno/sajtvakt)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status < 400:
                    return True, "", ""
                fel = f"svarade {r.status}"
        except urllib.error.HTTPError as e:
            fel, kod = f"svarade {e.code}", e.headers.get("x-vercel-error", "")
        except Exception as e:
            fel, kod = f"svarade inte ({type(e).__name__}: {e})", ""
        time.sleep(10)
    return False, fel + (f" {kod}" if kod else ""), kod


def vad_gora(fel, kod):
    """Vad Olle ska göra, på enkel svenska."""
    if kod in ("DEPLOYMENT_DISABLED", "DEPLOYMENT_BLOCKED") or "402" in fel:
        return ("**Vercel har stängt av sajten.** Det beror nästan alltid på en obetald faktura.\n\n"
                "Gör så här (bara du kan, det gäller ditt kort):\n"
                "1. Gå till https://vercel.com och logga in.\n"
                "2. Välj teamet **saasverket** uppe till vänster.\n"
                "3. Settings → Billing → betala fakturan eller byt kort.\n\n"
                "Sajterna kommer tillbaka av sig själva inom några minuter, och då får du ett ✅-mejl.")
    if "svarade inte" in fel:
        return ("**Sajten svarar inte alls.** Det kan vara domänen (utgången eller fel DNS) eller värden.\n\n"
                "Kolla först att domänen är betald hos den du köpte den av. Claude försöker också "
                "hitta felet i morgonkollen kl 07. Är det bråttom: öppna en Claude-chatt och skriv "
                "\"sajten är nere, laga\" och klistra in den här länken.")
    return ("**Sajten svarar med ett fel.** Det sitter troligen i koden eller hos Vercel.\n\n"
            "Du behöver inte göra något nu: morgonkollen kl 07 lagar det. Är det bråttom: öppna en "
            "Claude-chatt och skriv \"sajten är nere, laga\" och klistra in den här länken.")


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def tid(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def oppna_arenden():
    data = json.loads(gh("issue", "list", "--label", "nere", "--state", "open",
                         "--json", "number,title,createdAt", "--limit", "100"))
    ut = {}
    for a in data:
        namn = a["title"].removeprefix(NERE).removeprefix("NERE: ").strip()
        ut[namn] = a
    return ut


def senaste_larm(nr):
    """Tidpunkt för senaste larmkommentaren, eller None."""
    kommentarer = json.loads(gh("api", f"repos/{{owner}}/{{repo}}/issues/{nr}/comments?per_page=100"))
    tider = [tid(k["created_at"]) for k in kommentarer if LARM in (k.get("body") or "")]
    return max(tider) if tider else None


def main():
    nu = datetime.now(timezone.utc)
    oppna = oppna_arenden()
    vaktade = set()
    for url in sajter():
        namn = url.split("//")[1].rstrip("/")
        vaktade.add(namn)
        ok, fel, kod = svarar(url)
        print(f"{'OK  ' if ok else 'NERE'} {namn} {fel}")
        arende = oppna.get(namn)

        if not ok and not arende:
            gh("issue", "create", "--label", "nere", "--title", f"{NERE}{namn}",
               "--body", f"{url} {fel} (tre försök med tio sekunders mellanrum).\n\n"
                         f"Ligger den nere i {VANTA_MIN} minuter mejlas Olle. Ärendet stängs av sig självt när sajten svarar igen.")

        elif not ok and arende:
            nr = str(arende["number"])
            if not arende["title"].startswith(NERE):
                gh("issue", "edit", nr, "--title", f"{NERE}{namn}")
            nere_min = (nu - tid(arende["createdAt"])).total_seconds() / 60
            sist = senaste_larm(nr)
            if nere_min < VANTA_MIN:
                continue
            if sist and (nu - sist).total_seconds() < UPPREPA_H * 3600:
                continue
            timmar = int(nere_min // 60)
            langd = f"{timmar} timmar" if timmar >= 1 else f"{int(nere_min)} minuter"
            gh("issue", "edit", nr, "--add-assignee", OLLE)
            gh("issue", "comment", nr, "--body",
               f"{LARM}\n@{OLLE} 🔴 **{namn} är nere** och har varit det i ungefär {langd}.\n\n"
               f"Felet: {url} {fel}.\n\n{vad_gora(fel, kod)}\n\n"
               f"_Du får ett nytt mejl var {UPPREPA_H:g}:e timme tills sajten är uppe igen._")

        elif ok and arende:
            nr = str(arende["number"])
            if senaste_larm(nr):
                gh("issue", "edit", nr, "--title", f"{UPPE}{namn}")
                gh("issue", "close", nr, "--comment",
                   f"{LARM}\n@{OLLE} ✅ **{namn} är uppe igen.** Allt ok, du behöver inte göra något.")
            else:
                gh("issue", "close", nr, "--comment", f"{namn} svarar igen (var nere kort tid, inget larm skickades).")

    # Ärenden för sajter som tagits bort ur listan stängs tyst.
    for namn, arende in oppna.items():
        if namn not in vaktade:
            gh("issue", "close", str(arende["number"]), "--comment", f"{namn} vaktas inte längre.")


main()
