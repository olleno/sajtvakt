"""Kollar att varje sajt svarar. Öppnar ett ärende (= mejl) när en sajt ligger nere och stänger det när den är uppe igen."""
import json, subprocess, time, urllib.request, urllib.error
from sajter import sajter

def svarar(url):
    fel = ""
    for forsok in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (sajtvakt; +https://github.com/olleno/sajtvakt)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status < 400:
                    return True, ""
                fel = f"svarade {r.status}"
        except urllib.error.HTTPError as e:
            fel = f"svarade {e.code}"
        except Exception as e:
            fel = f"svarade inte ({type(e).__name__}: {e})"
        time.sleep(10)
    return False, fel

def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout

def oppna_arenden():
    data = json.loads(gh("issue", "list", "--label", "nere", "--state", "open", "--json", "number,title", "--limit", "100"))
    return {a["title"].removeprefix("NERE: "): a["number"] for a in data}

def main():
    oppna = oppna_arenden()
    for url in sajter():
        namn = url.split("//")[1].rstrip("/")
        ok, fel = svarar(url)
        print(f"{'OK  ' if ok else 'NERE'} {namn} {fel}")
        if not ok and namn not in oppna:
            gh("issue", "create", "--label", "nere", "--title", f"NERE: {namn}",
               "--body", f"{url} {fel}, tre försök med tio sekunders mellanrum.\n\nÄrendet stängs av sig självt när sajten svarar igen.")
        elif ok and namn in oppna:
            gh("issue", "close", str(oppna[namn]), "--comment", f"{namn} svarar igen. Allt ok.")

main()
