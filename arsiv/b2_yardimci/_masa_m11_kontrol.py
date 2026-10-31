# -*- coding: utf-8 -*-
"""Foy M11 denetimi (31.10.2026): results/C1_REFERANS_FOYU.md icinden '## M11:' bolumu cikarilinca eski foyun
sha256'si (21b2597a...) geri geliyor mu; yeni sha256, satir sayisi ve M11 satir araligi.

Cikarma kurali: foy L listesinin '\\n'.join'idir; M11 bolumu '\\n## M11:' ile baslar ve '\\n## Sabit dizgeler' oncesinde
biter. Bu aralik silinince eski foy bayt bayt geri gelmelidir. Yedek: arsiv/b2_yardimci/_masa_foy_yedek_21b2597.md."""
import hashlib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
ESKI_SHA = "21b2597ae9f995dffb24117d3bd4ef26f1335730c6dbc9567579e0d52dbeee06"
f = (KOK / "results/C1_REFERANS_FOYU.md").read_bytes()
yedek = KOK / "arsiv/b2_yardimci/_masa_foy_yedek_21b2597.md"
bas, son = b"\n## M11:", b"\n## Sabit dizgeler"
if f.count(bas) != 1 or f.count(son) != 1:
    raise SystemExit("M11 ya da Sabit dizgeler basligi tekil degil")
p, q = f.index(bas), f.index(son)
cikarilmis = f[:p] + f[q:]
h_yeni = hashlib.sha256(f).hexdigest()
h_cik = hashlib.sha256(cikarilmis).hexdigest()
ilk = f[:p + 1].count(b"\n") + 1
sonsatir = f[:q].count(b"\n")
print("yeni foy sha256           :", h_yeni)
print("yeni foy satir sayisi     :", f.count(b"\n"))
print("M11 cikarilinca sha256    :", h_cik)
print("eski sha256 geri geldi    :", h_cik == ESKI_SHA)
if yedek.exists():
    print("yedekle bayt bayt ayni    :", cikarilmis == yedek.read_bytes())
print("M11 satir araligi (1 tabanli, bas ve son dahil):", ilk, "-", sonsatir)
print("M11 alt basliklari:")
for i, s in enumerate(f.split(b"\n"), 1):
    if ilk <= i <= sonsatir and (s.startswith(b"## ") or s.startswith(b"### ")):
        print("  ", i, s.decode("utf-8"))
sys.exit(0 if h_cik == ESKI_SHA else 1)
