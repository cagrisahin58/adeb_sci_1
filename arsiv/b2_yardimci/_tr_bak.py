"""turkce-yazi denetimi sonrasi hedefli bakis (salt okur).
Kullanim: python3 arsiv/b2_yardimci/_tr_bak.py
"""
import io
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
TR = ROOT / "paper" / "manuscript_tr" / "sections"
EN = ROOT / "paper" / "manuscript" / "sections"


def lines(p):
    return io.open(p, encoding="utf-8").read().splitlines()


print("=== ref uyusmazligi: subsec:attacks / subsec:attack_methods / tab:tgr")
for d, tag in ((EN, "EN"), (TR, "TR")):
    for p in sorted(d.glob("0?_*.tex")):
        for i, l in enumerate(lines(p), 1):
            for key in ("subsec:attacks}", "subsec:attack_methods}", "tab:tgr}"):
                for m in re.finditer(re.escape(key), l):
                    s = max(0, m.start() - 140)
                    print(f"[{tag} {p.name}:{i}] ...{l[s:m.end() + 40]}...")

print("\n=== duzeltme isaretli sozcukler (TR)")
cnt = {}
for p in sorted(TR.glob("0?_*.tex")) + [ROOT / "paper" / "manuscript_tr" / "main.tex"]:
    for w in re.findall(r"[\wâîûÂÎÛ'’]*[âîûÂÎÛ][\wâîûÂÎÛ'’]*", io.open(p, encoding="utf-8").read()):
        cnt[w] = cnt.get(w, 0) + 1
for w, c in sorted(cnt.items(), key=lambda x: -x[1]):
    print(f"{c:3d}  {w}")

print("\n=== isaretli cumleler")
ARA = [
    ("02_ilgili_calismalar.tex", "yalnız üçüncüsü iddia edilmektedir"),
    ("03_yontem.tex", "Bu, mutlak bir doğruluk için doğru ölçek"),
    ("05_tartisma.tex", "Ablasyonun sağladığı şey"),
    ("05_tartisma.tex", "sıralaması ile"),
    ("06_sonuc.tex", "sıralaması ile"),
    ("05_tartisma.tex", "kapasitesi eşlenmiş çifttir"),
    ("01_giris.tex", "sonuçlandırmaktadır"),
]
for fname, key in ARA:
    for i, l in enumerate(lines(TR / fname), 1):
        j = l.find(key)
        if j >= 0:
            s = max(0, j - 260)
            print(f"[{fname}:{i}] ...{l[s:j + len(key) + 200]}...\n")

print("\n=== 01_giris.tex tam metin")
for i, l in enumerate(lines(TR / "01_giris.tex"), 1):
    if l.strip() and not l.lstrip().startswith("%"):
        print(f"{i}: {l}")
print("\n=== 06_sonuc.tex tam metin")
for i, l in enumerate(lines(TR / "06_sonuc.tex"), 1):
    if l.strip() and not l.lstrip().startswith("%"):
        print(f"{i}: {l}")
