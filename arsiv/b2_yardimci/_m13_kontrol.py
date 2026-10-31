# -*- coding: utf-8 -*-
"""Foy M13 denetimi (31.10.2026): results/C1_REFERANS_FOYU.md icinden '## M13:' bolumu cikarilinca M13 oncesi foyun
sha256'si (00cc422f...) geri geliyor mu; yeni sha256, satir sayisi, M13 satir araligi ve alt basliklari; M13 icinde
'ARTEFAKT YOK', 'SATIR DEGISTI', 'FARKLI' ya da 'bulunamadi' geciyor mu.

Cikarma kurali: foy L listesinin '\\n'.join'idir; M13 bolumu '\\n## M13:' ile baslar ve '\\n## Sabit dizgeler' oncesinde
biter. Bu aralik silinince eski foy bayt bayt geri gelmelidir."""
import hashlib
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
ESKI_SHA = "00cc422f01c0d9641d46bebd544eea0cb2a915256906bacf77d7f898f937979f"
f = (KOK / "results/C1_REFERANS_FOYU.md").read_bytes()
bas, son = b"\n## M13:", b"\n## Sabit dizgeler"
if f.count(bas) != 1 or f.count(son) != 1:
    raise SystemExit("M13 ya da Sabit dizgeler basligi tekil degil")
p, q = f.index(bas), f.index(son)
cikarilmis = f[:p] + f[q:]
h_yeni = hashlib.sha256(f).hexdigest()
h_cik = hashlib.sha256(cikarilmis).hexdigest()
ilk = f[:p + 1].count(b"\n") + 1
sonsatir = f[:q].count(b"\n")
print("yeni foy sha256           :", h_yeni)
print("yeni foy satir sayisi     :", f.count(b"\n"))
print("M13 cikarilinca sha256    :", h_cik)
print("M13 cikarilinca satir     :", cikarilmis.count(b"\n"))
print("eski sha256 geri geldi    :", h_cik == ESKI_SHA)
print("M13 satir araligi (1 tabanli, bas ve son dahil):", ilk, "-", sonsatir)
print("M13 alt basliklari:")
satirlar = f.split(b"\n")
for i, s in enumerate(satirlar, 1):
    if ilk <= i <= sonsatir and (s.startswith(b"## ") or s.startswith(b"### ")):
        print("  ", i, s.decode("utf-8"))
uyari = [(i, s.decode("utf-8")[:120]) for i, s in enumerate(satirlar, 1) if ilk <= i <= sonsatir
         and any(w in s for w in (b"ARTEFAKT YOK", b"SATIR DEGISTI", b"FARKLI", b"bulunamadi"))]
print("M13 icinde uyari sozcugu gecen satir:", len(uyari))
for i, s in uyari:
    print("  ", i, s)
# 31.10.2026 duzeltme turu (bulgu 3): uc JSON'un foy ozeti (meta.foy_ozeti.m13_haric_sha256 ve kaynaklar_sha256 icindeki
# foy degeri) M13 cikarilmis foyun sha256'siyla ayni mi
import json  # noqa: E402
ozet_ok = True
for rel in ("results/q1/konsey_b3_tarif.json", "results/q1/konsey_kayit_kurallari.json", "results/q1/konsey_zaman_cizelgesi.json"):
    m = json.loads((KOK / rel).read_text(encoding="utf-8"))["meta"]
    a = (m.get("foy_ozeti") or {}).get("m13_haric_sha256")
    b = m["kaynaklar_sha256"].get("results/C1_REFERANS_FOYU.md")
    ok = a == h_cik and b == h_cik
    ozet_ok &= ok
    print(f"JSON foy ozeti M13 cikarilmis foyle ayni ({rel}):", ok)
sys.exit(0 if h_cik == ESKI_SHA and not uyari and ozet_ok else 1)
