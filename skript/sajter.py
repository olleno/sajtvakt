from pathlib import Path

def sajter():
    rader = Path(__file__).resolve().parent.parent.joinpath("sajter.txt").read_text().splitlines()
    return [r.strip() for r in rader if r.strip() and not r.startswith("#")]
