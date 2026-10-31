"""Foyden M10 blogunu gecici olarak cikarip kalanin eski foyle bayt bayt ayni oldugunu denetler.

Kullanim (depo kokunden, WSL):
    python3 -I arsiv/b2_yardimci/_foy_m10_kontrol.py results/C1_REFERANS_FOYU.md <eski_sha256> [eski_foy_kopyasi]

M10 blogu, "\\n## M10: " ile baslayan satirin onundeki satir sonundan "\\n## Sabit dizgeler" satirinin
onundeki satir sonuna kadar olan baytlardir. Dosyaya yazmaz; yalniz okur.
"""
import hashlib
import sys

sys.stdout.reconfigure(encoding="utf-8")

yol, eski_sha = sys.argv[1], sys.argv[2]
with open(yol, "rb") as fh:
    b = fh.read()
a = b.find(b"\n## M10: ")
s = b.find(b"\n## Sabit dizgeler")
if a < 0 or s < 0 or not a < s:
    sys.exit(f"HATA: M10 ({a}) ya da Sabit dizgeler ({s}) basligi bulunamadi / sira yanlis")
if b.count(b"\n## M10: ") != 1:
    sys.exit("HATA: birden fazla M10 basligi")
kalan = b[:a] + b[s:]
yeni_sha = hashlib.sha256(b).hexdigest()
kalan_sha = hashlib.sha256(kalan).hexdigest()
NL = b"\n"
ilk = b[:a].count(NL) + 2   # "## M10: " satiri
son = b[:s].count(NL)       # "## Sabit dizgeler" oncesindeki bos satirdan bir onceki satir
print(f"yeni foy sha256       : {yeni_sha} ({len(b.splitlines())} satir)")
print(f"M10 blogu satirlari   : {ilk}-{son} (1 tabanli; '## M10:' basligindan Sabit dizgeler oncesi son satira)")
print(f"M10 cikarilinca sha256: {kalan_sha}")
print(f"beklenen eski sha256  : {eski_sha}")
ayni = kalan_sha == eski_sha
if len(sys.argv) > 3:
    with open(sys.argv[3], "rb") as fh:
        eski = fh.read()
    ayni = ayni and eski == kalan
    print(f"eski kopya ile bayt karsilastirmasi: {'AYNI' if eski == kalan else 'FARKLI'}")
print("SONUC:", "BIREBIR AYNI" if ayni else "FARKLI")
sys.exit(0 if ayni else 1)
