#!/usr/bin/env python3
"""TUR 4 kapi guncellemesi.

1) Sayi kapisi: 5,31 acikligi metinden kalkti; yerine OZDESLIK TERIMI
   (ham - hedef-dogru = 9,21) ve CIFAR-100 artiklari (5,97 / 13,58) gelir.
2) YAPISAL MUHAFIZ: Denklem 1'in genel biciminin cebiri. Sayi kapisi
   CEBIRI denetlemedigi icin e(1-p) hatasi uc hakem turu gecmisti;
   bu muhafiz o hata sinifini kilitler.
"""
import sys
from pathlib import Path

BETIK = Path("/home/firat/projects/adeb_sci_1/scripts")

# ---------------------------------------------------------------- 1) sayilar
P = BETIK / "verify_manuscript_numbers.py"
t = P.read_text(encoding="utf-8")

ESKI = 'chk("T3 aciklik her-ikisi-dogru->ham", _pd["raw"] - _pd["both_correct"])'
YENI = ('# Tur 4: Denklem 1 HEDEF-DOGRU orani baglar, dolayisiyla kapali formda\n'
        '# kapattigi aciklik ham <-> hedef-dogru\'dur (9,21). Tur 3\'te yanlislikla\n'
        '# her-ikisi-dogru <-> ham (5,31) acikligi ozdeslige atfedilmisti.\n'
        'chk("T4 OZDESLIK TERIMI (ham - hedef-dogru)", '
        '_pd["raw"] - _pd["target_correct"])')

if ESKI in t:
    t = t.replace(ESKI, YENI, 1)
    print("  [+] 5,31 kontrolu -> 9,21 ozdeslik terimi")
elif "T4 OZDESLIK TERIMI" in t:
    print("  [=] ozdeslik terimi kontrolu zaten var")
else:
    sys.exit("BASARISIZ: T3 aciklik satiri bulunamadi")

# CIFAR-100 artik ve yayilim kontrolleri
IMZA = "# --- T4: CIFAR-100 ayrisimi ---"
if IMZA not in t:
    EK = '''
# --- T4: CIFAR-100 ayrisimi ---
# CIFAR-100'de kosulsuz oran dordun EN BUYUGUDUR; iki-parcali bolumleme
# orada gecerli degildir ve yayilimin TAMAMI ozdeslik payidir. Metin bunu
# soyluyor; kapi da denetler.
try:
    _c100p = jl("results/q1/cifar100/transfer/e1_transfer_summary.json")["protocols"]

    def _dg100(k):
        _v = _c100p[k]
        return _v["diff"]["mean"] if isinstance(_v, dict) and "diff" in _v else _v

    chk("T4 C100 artik (her-ikisi - hedef-dogru)",
        _dg100("both_correct") - _dg100("target_correct"))
    chk("T4 C100 yayilim = ozdeslik payi",
        _dg100("raw") - _dg100("target_correct"))
except Exception as _e:
    print(f"  [uyari] C100 ayrisimi hesaplanamadi: {_e}")
'''
    m = t.rfind("\nrows = []")
    if m < 0:
        sys.exit("BASARISIZ: 'rows = []' bulunamadi")
    t = t[:m] + EK + t[m:]
    print("  [+] CIFAR-100 ayrisim kontrolleri eklendi")
else:
    print("  [=] CIFAR-100 kontrolleri zaten var")

P.write_text(t, encoding="utf-8")

# ------------------------------------------------------- 2) yapisal muhafiz
Q = BETIK / "check_manuscript_claims.py"
q = Q.read_text(encoding="utf-8")

IMZA2 = "# --- T4: DENKLEM 1 CEBIR MUHAFIZI ---"
if IMZA2 in q:
    print("  [=] cebir muhafizi zaten var")
else:
    MUHAFIZ = r'''
# --- T4: DENKLEM 1 CEBIR MUHAFIZI ---
# p = P(adv yanlis | temiz yanlis) oldugu icin toplam olasilik yasasi
#     r_ham = e*p + r_kos*(1-e)
# verir. Metinde uzun sure e*(1-p) yaziliydi; o bicim p=1'de Denklem 1'i
# DEGIL r_kos*(1-e)'yi verir ve olculen orandan 26,99 puana kadar sapar
# (bagimsiz olcum: scripts/_t4_ozdeslik_dogrula.py, 6/6 yon).
# Sayi kapisi CEBIRI denetlemez; bu yuzden hata uc hakem turu gecti.
kontrol("T4. EN genel bicim DOGRU (e\\,p)",
        r"e\,p + r_{\text{cond}}" in en)
kontrol("T4. EN yanlis bicim YOK (e\\,(1-p))",
        r"e\,(1-p) + r_{\text{cond}}" not in en)
kontrol("T4. TR genel bicim DOGRU (e\\,p)",
        r"e\,p + r_{\text{koş}}" in tr)
kontrol("T4. TR yanlis bicim YOK",
        r"e\,(1-p) + r_{\text{koş}}" not in tr)

# Tek "birincil" beyani: Bolum 3'te metrik AILESI tanitilir, birincil TAHMIN
# bir kez ve yalniz her-ikisi-dogru icin ilan edilir.
kontrol("T4. EN 'primary transfer metric' ifadesi YOK",
        "primary transfer metric" not in en)
kontrol("T4. TR 'Birincil transfer metrigimiz' ifadesi YOK",
        "Birincil transfer metriğimiz" not in tr)
'''
    m = q.rfind("\n# ---")
    if m < 0:
        m = len(q)
    q = q[:m] + MUHAFIZ + q[m:]
    Q.write_text(q, encoding="utf-8")
    print("  [+] cebir + birincil muhafizlari eklendi")
