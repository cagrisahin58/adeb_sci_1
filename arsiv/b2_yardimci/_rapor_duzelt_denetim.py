# Salt okur: duzeltilmis 09_sonuc_b2_b6.md icin bicim denetimi (31.10.2026)
import re, sys
sys.stdout.reconfigure(encoding="utf-8")
p = "raporlar/konsey_2026-10-29/09_sonuc_b2_b6.md"
with open(p, encoding="utf-8") as f:
    satirlar = f.read().split("\n")
print("satir sayisi", len(satirlar))
print("ilk satir:", satirlar[0])
for i, s in enumerate(satirlar, 1):
    if "—" in s:
        print("UZUN TIRE", i)
    if re.search(r"\b(biz|bizim|aşamamız|yaptık|ettik|bulduk|gördük)\b", s):
        print("BIRINCI KISI?", i, s[:120])
    if re.match(r"\s*(\*\*|__)", s):
        print("KOYU BASLANGIC", i, s[:80])
    if s.startswith("Anahtarlar:"):
        print("ANAHTARLAR ACILISI", i)
    if "sonuc_bolgesi" in s and "O1" in s:
        print("O1", i, s[:160])
    if "en önemli" in s:
        print("SAYI", i, s[s.find("en önemli"):s.find("en önemli")+40])
