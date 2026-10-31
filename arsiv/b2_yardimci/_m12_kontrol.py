# -*- coding: utf-8 -*-
"""Foy M12 denetimi (31.10.2026): results/C1_REFERANS_FOYU.md icinden '## M12:' bolumu cikarilinca eski foyun
sha256'si (42c7dc34...) geri geliyor mu; yeni sha256, satir sayisi ve M12 satir araligi.

Cikarma kurali: foy L listesinin '\\n'.join'idir; M12 bolumu '\\n## M12:' ile baslar ve '\\n## Sabit dizgeler' oncesinde
biter. Bu aralik silinince eski foy bayt bayt geri gelmelidir. Yedek: arsiv/b2_yardimci/_m12_foy_yedek_42c7dc3.md."""
import hashlib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
ESKI_SHA = "42c7dc34ea0671aeda99de493ce1023dbfec728465592a7d32b987fab9ef1801"
f = (KOK / "results/C1_REFERANS_FOYU.md").read_bytes()
yedek = KOK / "arsiv/b2_yardimci/_m12_foy_yedek_42c7dc3.md"
bas, son = b"\n## M12:", b"\n## Sabit dizgeler"
if f.count(bas) != 1 or f.count(son) != 1:
    raise SystemExit("M12 ya da Sabit dizgeler basligi tekil degil")
p, q = f.index(bas), f.index(son)
cikarilmis = f[:p] + f[q:]
h_yeni = hashlib.sha256(f).hexdigest()
h_cik = hashlib.sha256(cikarilmis).hexdigest()
ilk = f[:p + 1].count(b"\n") + 1
sonsatir = f[:q].count(b"\n")
print("yeni foy sha256           :", h_yeni)
print("yeni foy satir sayisi     :", f.count(b"\n"))
print("M12 cikarilinca sha256    :", h_cik)
print("eski sha256 geri geldi    :", h_cik == ESKI_SHA)
if yedek.exists():
    print("yedekle bayt bayt ayni    :", cikarilmis == yedek.read_bytes())
print("M12 satir araligi (1 tabanli, bas ve son dahil):", ilk, "-", sonsatir)
print("M12 alt basliklari:")
for i, s in enumerate(f.split(b"\n"), 1):
    if ilk <= i <= sonsatir and (s.startswith(b"## ") or s.startswith(b"### ")):
        print("  ", i, s.decode("utf-8"))
sys.exit(0 if h_cik == ESKI_SHA else 1)
