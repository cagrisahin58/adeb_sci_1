#!/usr/bin/env python3
"""IKI KAPIYI SERTLESTIRIR (denetim panelinin MAJOR bulgulari).

(1) verify_manuscript_numbers.py CIPLAK ALT DIZE eslestiriyordu:
    '19.37' -> '119.37' yapildiginda kapi yine GECTI dedi, cunku dize hala
    icinde geciyor. Ustelik iki kontrol (E7 esli GA ust = 0.07 ve E6 O1 r =
    0.999) YALNIZ daha uzun bir sayinin ICINDE eslesiyordu, yani hic
    dogrulanmiyorlardi ve gercek bir hatayi ortuyorlardi.
    Duzeltme: eslesme SAYI SINIRINA baglanir (once/sonra rakam ya da ondalik
    ayraci gelemez) ve TAM eslesme sayisi raporlanir; sifirsa KALDI.

(2) check_abstract_body.py govde sayi havuzuna LaTeX UZUNLUKLARINI aliyordu:
    ozdeki uydurma '2.5 points' iddiasi, govdedeki
    \\setlength{\\tabcolsep}{2.5pt} sayesinde 'bulundu' sayildi.
    Duzeltme: govdeden once bicimlendirme komutlari ve uzunluk birimleri
    ayiklanir. Ayrica ozet BULUNAMAZSA kapi artik SESSIZ GECMEZ.
"""
import sys
from pathlib import Path

ROOT = Path("/home/firat/projects/adeb_sci_1")
hata = []


def yama(rel, ciftler, imza):
    p = ROOT / rel
    t = orig = p.read_text(encoding="utf-8")
    if imza in t:
        print(f"  atlandi (yamali): {rel}")
        return
    for eski, yeni, ad in ciftler:
        if t.count(eski) != 1:
            hata.append(f"{rel} :: {ad}: {t.count(eski)} eslesme")
            return
        t = t.replace(eski, yeni, 1)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        print(f"  yamalandi: {rel}")


# ------------------------------------------------------------------ (1)
V_ESKI = '''# --- rapor ---
rows = []
for label, val in CHECKS:
    found = {lang: (val in txt) for lang, txt in LANGS.items()}
    rows.append((label, val, found))'''

V_YENI = '''# --- rapor ---
def tam_eslesme(val, txt):
    """SAYI SINIRINA bagli eslesme sayisi.

    Ciplak `val in txt` yetmez: '19.37' dizesi '119.37' icinde de gecer ve
    manset sayiya rakam eklense bile kapi GECER (2026-08-25 denetimi bunu
    olctu). Ayrica bazi kontroller YALNIZ daha uzun bir sayinin icinde
    eslesip hic dogrulanmadan 'OK' aliyordu. Bu yuzden eslesmenin oncesinde
    ve sonrasinda rakam ya da ondalik ayraci OLMAMALIDIR.
    """
    return len(re.findall(r"(?<![\\d.,])" + re.escape(val) + r"(?![\\d])", txt))


rows = []
for label, val in CHECKS:
    found = {lang: (tam_eslesme(val, txt) > 0) for lang, txt in LANGS.items()}
    sayim = {lang: tam_eslesme(val, txt) for lang, txt in LANGS.items()}
    rows.append((label, val, found, sayim))'''

V_ESKI2 = '''missing = 0
print(f"{'KONTROL':36s} {'DEGER':>9s}  EN   TR")
print("-" * 60)
for label, val, found in rows:
    en = "OK " if found["EN"] else "YOK"
    trk = "OK " if found["TR"] else "YOK"
    if not (found["EN"] and found["TR"]):
        missing += 1
    print(f"{label:36s} {val:>9s}  {en}  {trk}")'''

V_YENI2 = '''missing = 0
print(f"{'KONTROL':36s} {'DEGER':>9s}  EN   TR")
print("-" * 60)
for label, val, found, sayim in rows:
    en = "OK " if found["EN"] else "YOK"
    trk = "OK " if found["TR"] else "YOK"
    if not (found["EN"] and found["TR"]):
        missing += 1
    ek = ""
    if found["EN"] and found["TR"] and (sayim["EN"] > 3 or sayim["TR"] > 3):
        ek = f"   ({sayim['EN']}/{sayim['TR']} yerde)"
    print(f"{label:36s} {val:>9s}  {en}  {trk}{ek}")'''

yama("scripts/verify_manuscript_numbers.py",
     [(V_ESKI, V_YENI, "eslesme"), (V_ESKI2, V_YENI2, "rapor")],
     "tam_eslesme")

# ------------------------------------------------------------------ (2)
O_ESKI = '''    a = re.search(r"\\\\maketitle(.+?)\\\\begin\\{IEEE", m, re.DOTALL)
    return a.group(1) if a else ""'''
O_YENI = '''    a = re.search(r"\\\\maketitle(.+?)\\\\begin\\{IEEE", m, re.DOTALL)
    if a:
        return a.group(1)
    # SESSIZ GECIS YOK: ozet bulunamazsa denetim YAPILMAMIS demektir.
    sys.exit(f"KAPI HATASI: {base}/main.tex icinde ozet bulunamadi; "
             "denetim yapilmadi.")'''

O_ESKI2 = '''    govde_sayilari = [float(x) for x in SAYI.findall(govde)]'''
O_YENI2 = '''    # LaTeX UZUNLUKLARI govde havuzuna GIRMEZ. Bunlar dizgi ayarlaridir,
    # makalenin iddialari degil; girerlerse ozdeki uydurma bir sayi
    # (ornegin "2.5 points") \\setlength{\\tabcolsep}{2.5pt} sayesinde
    # "govdede var" sayilir -- 2026-08-25 denetimi bunu olctu.
    _govde_temiz = re.sub(
        r"\\\\(?:setlength|hspace|vspace|addtolength|tabcolsep|arraystretch|"
        r"columnsep|includegraphics|scalebox|resizebox)\\b[^\\n]*", " ", govde)
    _govde_temiz = re.sub(r"\\d+(?:\\.\\d+)?\\s*(?:pt|pc|in|cm|mm|em|ex|bp|dd|sp)\\b",
                          " ", _govde_temiz)
    govde_sayilari = [float(x) for x in SAYI.findall(_govde_temiz)]'''

yama("scripts/check_abstract_body.py",
     [(O_ESKI, O_YENI, "sessiz gecis"), (O_ESKI2, O_YENI2, "uzunluk havuzu")],
     "_govde_temiz")

if hata:
    print("BASARISIZ:", *hata, sep="\n  ")
    sys.exit(1)
print("tamam")
