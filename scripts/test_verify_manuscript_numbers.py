#!/usr/bin/env python3
"""verify_manuscript_numbers.py icin oz-sinama: kapi YAKALAMASI gerekeni yakaliyor mu?

"Gecen bir kontrol, yakaladigini kanitlamaz." EN makalenin gecici bir kopyasinda bozmalar yapilir;
her birinde kapinin ilgili kurali EKSIK basmali, EN_EKSIK artmali ve cikis 1 olmalidir. Bozulmamis
kopya gercek makaleyle ayni EN_EKSIK'i vermelidir. Gercek makaleye ve foye dokunulmaz; kopyalar
gecici dizindedir ve sonda silinir.

UCUNCU SURUM (2026-10-31, ikinci dogrulayicinin Y3 bulgusu; ayri dogrulayici yok, bu sinama onun
yerine gecer):
  * Her sinamada uygulanabilen BUTUN adaylar (en cok DENEME = 5) bozulur ve HER BIRI yakalanmalidir;
    tek bir kacirma sinamayi KALDI yapar. Bozma uygulanamazsa (hedef dizgesi yok) aday sayilmaz;
    hic uygulanabilir aday yoksa sinama KALDI.
  * Hedefler SABIT DIZE DEGILDIR: kapinin `--dokum` ciktisindan (bozulmamis kopyada) secilir. Metin
    temizlendikce dogal hedefler kaybolabilecegi icin yeni kurallarin her birinde bir YAPAY aday da
    vardir (sections/06_conclusion.tex sonuna eklenen sinama paragrafi).
  * "Hazirla" adimi: bazi sinamalar once kopyada hedef degeri KAPSANMIS hale getirir (temizlik sonrasi
    metni taklit eder: KAYNAK yorumu + bu degeri iceren sinama belgesi), sonra bozar. Basari olcutu:
    cikis 1, EN_EKSIK hazirlanmis tabandan BUYUK ve beklenen EKSIK satiri tabanda yokken bozmadan sonra
    var. Sinama belgeleri arsiv/b2_yardimci/_kapi_sinama_belgesi_*.md olarak yazilir ve sonda silinir.
  * Kopyalar canli makaleden degil, sinamanin basinda alinan anlik goruntuden yapilir (makale baska
    bir ajan tarafindan duzenlenirken de tutarli).

Sinamalar:
  0  ayristirma: isaret bicimleri (--ayristirma-sinami)
  1  A3 yanlis sayi (atfedilen satirda olmayan, foyde baska satirda olan deger)
  2  A2 uydurma sayi (foyde hic olmayan deger)
  3  A1 kaymis atif (FOY yorumu blogun tasimadigi satiri gosteriyor)
  4  gecersiz satir numarasi
  5  B manset: bir manset degeri metnin HER yerinde degisti
  6  S1 deger takasi: ayni satirdaki iki 'kestirim [alt, ust]' demetinin kestirimleri yer degistirdi
  7  S1 tek kopya: bir manset sayisinin YALNIZ BIR kopyasi bozuldu (B kapisi KALDI vermeli)
  8  K2 isaret cevirme: atfedilen negatif bir deger isaretsiz yazildi
  9  S3 tamsayi bozmasi: atfedilen bir tamsayi (tohum, n, epok) degisti
  10 K1b KAYNAK-yalniz gruba uydurma sayi
  11 K1b KAYNAK-yalniz paragrafta tohum 1001 -> 1004 (hazirla: tohum kapsanir)
  12 K1b bolme tohumu 777 -> 778 (hazirla)
  13 K1b on kayit esigi -0.20 -> -0.15 (hazirla)
  14 K1b GRUPSUZ: hicbir grupta olmayan satira sayi
  15 T1 ters aralik: [a, b] -> [b, a] (foy araligiysa DEMET 'TERS YONDE' de beklenir)
  16 Y1 YON cevirme: excludes <-> includes (ya da araliga ters yon ifadesi eklenir)
  17 Y1 YON denetlenemedi: araliksiz 'excludes zero' cumlesi
  18 S1b ozet tek kopya rakam takasi (0.936 -> 0.963; kalem yorumda anilan govde blogu da aday)
  19 Y2 KAYNAK degeri adlandirilan belgede yok (ya da belge adi yok)

Konteynerde: docker exec -w /workspace adeb_eval python -B scripts/test_verify_manuscript_numbers.py
Cikis 0 = butun sinamalar gecti.
"""
import itertools
import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
KAPI = ROOT / "scripts/verify_manuscript_numbers.py"
EN = ROOT / "paper/manuscript"
FOY = (ROOT / "results/C1_REFERANS_FOYU.md").read_text(encoding="utf-8").split("\n")
FOY_METIN = "\n".join(FOY)
ON_KAYIT = (ROOT / "raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md").read_text(encoding="utf-8")
BELGE_DIZIN = ROOT / "arsiv/b2_yardimci"
YAPAY_DOSYA = "sections/06_conclusion.tex"
DENEME = 5
SRC = None  # anlik goruntu (main() kurar)


def kos(dizin, *ek):
    r = subprocess.run([sys.executable, "-B", str(KAPI), "--en-dizin", str(dizin), *ek],
                       capture_output=True, text=True, cwd=str(ROOT))
    m = re.search(r"EN_EKSIK=(\d+)", r.stdout)
    return r.returncode, (int(m.group(1)) if m else None), r.stdout + r.stderr


def kopya(hedef, kaynak=None):
    shutil.copytree(kaynak or SRC or EN, hedef,
                    ignore=shutil.ignore_patterns("*.pdf", "*.png", "*.pfb", "*.tfm", "*.log", "*.aux", "*.bbl",
                                                  "*.blg", "*.fls", "*.fdb_latexmk", "*.bak"))


def sinir(x):
    """Sayi sinirina bagli duzenli ifade (onunde/arkasinda rakam ya da nokta yok)."""
    return r"(?<![\d.])" + re.escape(x) + r"(?![\d])"


def satirlar(d, dosya):
    return (Path(d) / dosya).read_text(encoding="utf-8").split("\n")


def yaz(d, dosya, L):
    (Path(d) / dosya).write_text("\n".join(L), encoding="utf-8")


def guvenli_ekle(s, ek):
    """ek'i satirin yorum (%) kismindan ONCE ekle."""
    m = re.search(r"(?<!\\)%", s)
    if m:
        return s[:m.start()].rstrip() + ek + " " + s[m.start():]
    return s.rstrip() + ek


def metin_kismi(s):
    m = re.search(r"(?<!\\)%", s)
    return s[:m.start()] if m else s


def foyde_yok(x):
    """x dizesi foyun hicbir yerinde (sinirli) gecmiyor; isaretsiz ve virgullu yazimlar dahil."""
    return not re.search(sinir(x), FOY_METIN) and not re.search(sinir(x.replace(".", ",")), FOY_METIN)


def isaret_once(s, pos):
    """s[pos]'taki sayinin onunde (bosluk, $, {, } atlanarak) eksi isareti var mi?"""
    j = pos - 1
    while j >= 0 and s[j] in " ${}~":
        j -= 1
    if j >= 0 and s[j] in "-−":
        return not (j >= 1 and s[j - 1] == "-")  # '36--58' aralik tiresi
    return s[max(0, j - 9):j + 1].endswith("\\textminus")


def satirlarda_isaretli(L_, v, neg):
    """L_ (dize listesi) icinde v sayisi istenen isaretle geciyor mu (nokta ya da virgul ondalik)."""
    for s in L_:
        for vv in {v, v.replace(".", ",")}:
            for m in re.finditer(sinir(vv), s):
                if isaret_once(s, m.start()) == neg:
                    return True
    return False


def ulp_adaylari(v, nd):
    d, q = Decimal(v), Decimal(1).scaleb(-nd)
    for k in (3, -3, 2, -2, 1, -1, 7, -7):
        w = d + k * q
        if w > 0:
            yield f"{w:.{nd}f}"


def _tex(d):
    return sorted(Path(d).rglob("*.tex"))


def _rel(f, d):
    return str(Path(f).relative_to(d))


_SAYAC = itertools.count(1)  # next() CPython'da atomik: paralel adaylar ayri belge alir


def sinama_belgesi(metin):
    """arsiv/b2_yardimci altina bu adaya ozgu bir sinama belgesi yazar; KAYNAK yorumunda kullanilacak yolu dondurur."""
    p = BELGE_DIZIN / f"_kapi_sinama_belgesi_{next(_SAYAC):03d}.md"
    p.write_text("# Oz-sinama belgesi (gecici, test_verify_manuscript_numbers.py siler)\n\n" + metin + "\n", encoding="utf-8")
    return str(p.relative_to(ROOT))


def yorum_ekle(d, dosya, ln, yorum):
    """ln. satirdan (1 tabanli) ONCE bir yorum satiri ekler; hedef satir ln+1 olur."""
    L = satirlar(d, dosya)
    L.insert(ln - 1, yorum)
    yaz(d, dosya, L)


def yapay_paragraf(d, govde_satirlari):
    """YAPAY_DOSYA sonuna bos satirla ayrilmis bir sinama paragrafi ekler; paragrafin ilk satir numarasini dondurur."""
    L = satirlar(d, YAPAY_DOSYA)
    while L and not L[-1].strip():
        L.pop()
    L += ["", ""]
    bas = len(L) + 1
    L += govde_satirlari + [""]
    yaz(d, YAPAY_DOSYA, L)
    return bas


def yapay_bas():
    """yapay_paragraf'in verecegi ilk satir numarasi (SRC uzerinde, bozmadan once hesaplanir)."""
    L = satirlar(SRC, YAPAY_DOSYA)
    while L and not L[-1].strip():
        L.pop()
    return len(L) + 3


def grup_yorum_metni(g):
    L = satirlar(SRC, g["dosya"])
    bas = [L[i - 1] for i in range(g["satir"], g["blok_bas"])]
    ic = [L[i - 1] for i in range(g["blok_bas"], g["blok_son"] + 1) if L[i - 1].lstrip().startswith("%")]
    return "\n".join(bas + ic)


# --- adaylar: her biri (aciklama, hazirla(d) ya da None, boz(d), [beklenen duzenli ifadeler]) ------------
def aday_a3(D):
    for g in D["gruplar"]:
        if g["sekil"] or not g["atif"]:
            continue
        atif = "\n".join(FOY[s - 1] for s in g["atif"] if 1 <= s <= len(FOY))
        yorum = grup_yorum_metni(g)
        for t in g["tok"]:
            if t["durum"] != "ok" or t["tam"] or t["nd"] != 3 or t["deger"].startswith("-"):
                continue
            bulundu = None
            for satir in FOY:
                for y in re.findall(r"(?<![\d.\-])(\d\.\d{3})(?![\d])", satir):
                    if y == t["deger"] or y[:-1] in atif or y in atif or y in yorum:
                        continue
                    bulundu = y
                    break
                if bulundu:
                    break
            if not bulundu:
                continue

            def boz(d, g=g, t=t, y=bulundu):
                L = satirlar(d, g["dosya"])
                i = t["satir"] - 1
                assert re.search(sinir(t["deger"]), metin_kismi(L[i])), "hedef satirda yok"
                L[i] = re.sub(sinir(t["deger"]), y, L[i], count=1)
                yaz(d, g["dosya"], L)
            yield (f"{g['dosya']}:{t['satir']} {t['deger']} -> {bulundu}", None, boz,
                   [rf"EKSIK  {re.escape(g['dosya'])}:{t['satir']}  {re.escape(bulundu)}  -- ATIF EKSIK"])
            break


def aday_a2(D):
    for g in D["gruplar"]:
        if g["sekil"] or not g["atif"] or not any(t["durum"] == "ok" for t in g["tok"]):
            continue
        ln = next(t["satir"] for t in g["tok"] if t["durum"] == "ok")

        def boz(d, g=g, ln=ln):
            L = satirlar(d, g["dosya"])
            L[ln - 1] = guvenli_ekle(L[ln - 1], r" (or $0.12345$)")
            yaz(d, g["dosya"], L)
        yield (f"{g['dosya']}:{ln} + 0.12345", None, boz, [rf"EKSIK  {re.escape(g['dosya'])}:{ln}  0\.12345  -- FOYDE YOK"])


def _tek_yorumlu(D):
    for g in D["gruplar"]:
        if g["sekil"] or len(g["yorum_satirlari"]) != 1 or not any(t["durum"] == "ok" and not t["tam"] for t in g["tok"]):
            continue
        yield g


def _tasinmis(metin_deger, nd, foy_deger):
    """Kapinin esleme kurali (isaret haric): foy degeri metnin basamagina yuvarlaninca, x100 ya da /100 esit mi."""
    q = Decimal(1).scaleb(-nd)
    m = abs(Decimal(metin_deger))
    for w in (foy_deger, foy_deger * 100, foy_deger / 100):
        if abs(w).quantize(q) == m:
            return True
    return False


def aday_a1(D):
    for g in _tek_yorumlu(D):
        bloklar = {t["deger"].lstrip("-") for t in g["tok"]}
        kanit = [t for t in g["tok"] if not t["tam"] or int(t["deger"].lstrip("-")) >= 100]
        for s in range(len(FOY) // 3, len(FOY)):
            sayi = re.findall(r"(?<![\d.])\d+\.\d{2,}(?![\d])", FOY[s - 1])
            if len(sayi) < 2 or any(x in bloklar or any(b.startswith(x) or x.startswith(b) for b in bloklar) for x in sayi):
                continue
            hepsi = [Decimal(x.replace(",", ".")) for x in re.findall(r"(?<![\w.])\d+(?:[.,]\d+)?(?![\w])", FOY[s - 1])]
            if any(_tasinmis(t["deger"], t["nd"], v) for t in kanit for v in hepsi):
                continue  # bloktaki bir sayi bu satirin bir degerinin tasinmis hali: kaymis atif A1'i tetiklemez

            def boz(d, g=g, s=s):
                L = satirlar(d, g["dosya"])
                L[g["yorum_satirlari"][0] - 1] = f"% FOY:SINAMA:{s}"
                yaz(d, g["dosya"], L)
            yield (f"{g['dosya']}:{g['satir']} FOY -> {s}", None, boz,
                   [rf"EKSIK  {re.escape(g['dosya'])}:{g['satir']}  FOY satirlari {s}  -- blokta bu satirlarin hicbir sayisi yok"])
            break


def aday_gecersiz(D):
    for g in _tek_yorumlu(D):
        def boz(d, g=g):
            L = satirlar(d, g["dosya"])
            L[g["yorum_satirlari"][0] - 1] = "% FOY:SINAMA:99999"
            yaz(d, g["dosya"], L)
        yield (f"{g['dosya']}:{g['satir']} FOY -> 99999", None, boz,
               [rf"EKSIK  {re.escape(g['dosya'])}:{g['satir']}  FOY:SINAMA:99999  -- foy \d+ satir"])


def aday_b_hepsi(D):
    for m in D["manset"]:
        if m["kaynak"] != "json" or m["deger"].startswith("-") or not (m["foy"] and m["metin"]):
            continue
        for y in ulp_adaylari(m["deger"], m["nd"]):
            if not foyde_yok(y):
                continue

            def boz(d, v=m["deger"], y=y):
                n = 0
                for f in _tex(d):
                    t = f.read_text(encoding="utf-8")
                    t2, k = re.subn(sinir(v), y, t)
                    n += k
                    if k:
                        f.write_text(t2, encoding="utf-8")
                assert n, "manset degeri metinde yok"
            yield (f"{m['etiket']} {m['deger']} -> {y} (her yerde)", None, boz,
                   [rf"EKSIK  {re.escape(m['etiket'][:46])}\s+{re.escape(m['deger'])}  foy M9-M10: var  metin: YOK"])
            break


_DEMET_RE = re.compile(r"(?<![\d.])([-+]?\d+\.\d+)\$?\s*\[\s*\$?[-+]?\d")


def aday_takas(D):
    for f in _tex(SRC):
        rel = _rel(f, SRC)
        bloklu = {ln for g in D["gruplar"] if g["dosya"] == rel and g["atif"] for ln in g["blok_satirlari"]}
        for i, s in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            if s.lstrip().startswith("%") or i not in bloklu:
                continue
            ms = [m for m in _DEMET_RE.finditer(metin_kismi(s))]
            ciftler = [(a, b) for a in ms for b in ms if a.start() < b.start() and a.group(1).lstrip("+-") != b.group(1).lstrip("+-")]
            for a, b in ciftler[:2]:
                def boz(d, rel=rel, i=i, a=a, b=b):
                    L = satirlar(d, rel)
                    x = L[i - 1]
                    assert x[a.start(1):a.end(1)] == a.group(1) and x[b.start(1):b.end(1)] == b.group(1)
                    L[i - 1] = x[:a.start(1)] + b.group(1) + x[a.end(1):b.start(1)] + a.group(1) + x[b.end(1):]
                    yaz(d, rel, L)
                yield (f"{rel}:{i} kestirim takasi {a.group(1)} <-> {b.group(1)}", None, boz,
                       [rf"EKSIK  {re.escape(rel)}:{i}  .*-- DEMET"])


def aday_tek_kopya(D):
    for m in D["manset"]:
        if m["kaynak"] != "json" or m["deger"].startswith("-") or not m["metin"]:
            continue
        yerler = []
        for f in _tex(SRC):
            rel = _rel(f, SRC)
            for i, s in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
                if s.lstrip().startswith("%"):
                    continue
                for mm in re.finditer(sinir(m["deger"]), metin_kismi(s)):
                    if not isaret_once(s, mm.start()):
                        yerler.append((rel, i, mm.start()))
        if len(yerler) < 2:
            continue
        rel, i, p = yerler[-1]
        for y in ulp_adaylari(m["deger"], m["nd"]):
            if not foyde_yok(y):
                continue

            def boz(d, rel=rel, i=i, p=p, v=m["deger"], y=y):
                L = satirlar(d, rel)
                assert L[i - 1][p:p + len(v)] == v
                L[i - 1] = L[i - 1][:p] + y + L[i - 1][p + len(v):]
                yaz(d, rel, L)
            yield (f"{m['etiket']} {m['deger']} -> {y} yalniz {rel}:{i} ({len(yerler)} kopyadan biri)", None, boz,
                   [rf"EKSIK  {re.escape(m['etiket'][:46])}\s+{re.escape(m['deger'])}  KOPYA  {re.escape(rel)}:{i}  {re.escape(y)}"])
            break


def aday_isaret(D):
    # once govde (ozet disi) gruplari
    for g in sorted(D["gruplar"], key=lambda g: g["dosya"] == "main.tex"):
        if not g["atif"]:
            continue
        atif = [FOY[s - 1] for s in g["atif"] if 1 <= s <= len(FOY)]
        for t in g["tok"]:
            if t["durum"] != "ok" or not t["deger"].startswith("-") or t["tam"] or t["nd"] < 2:
                continue
            v = t["deger"][1:]
            if satirlarda_isaretli(atif, v, False) or satirlarda_isaretli([grup_yorum_metni(g)], v, False):
                continue  # isaretsiz hali atfedilen satirda da var: cevirme EKSIK uretmez, aday degil

            def boz(d, g=g, t=t, v=v):
                L = satirlar(d, g["dosya"])
                i = t["satir"] - 1
                L2 = re.sub(r"(\$?)-(\$?)" + sinir(v), lambda m: m.group(1) + m.group(2) + v, L[i], count=1)
                assert L2 != L[i], "negatif yazim bulunamadi"
                L[i] = L2
                yaz(d, g["dosya"], L)
            yield (f"{g['dosya']}:{t['satir']} -{v} -> {v}", None, boz,
                   [rf"EKSIK  {re.escape(g['dosya'])}:{t['satir']}  {re.escape(v)}  -- ISARET"])


def _duz_tam(v):
    return r"(?<![\d.,{}\-])" + re.escape(v) + r"(?![\d}])"


def aday_tamsayi(D):
    havuz = [(g, t) for g in D["gruplar"] if not g["sekil"] and g["atif"] for t in g["tok"]
             if t["durum"] == "ok" and t["tam"] and int(t["deger"]) >= 10]
    havuz.sort(key=lambda gt: (gt[0]["dosya"] == "main.tex", int(gt[1]["deger"]) < 100))
    for g, t in havuz:
        v = t["deger"]
        if not re.search(_duz_tam(v), metin_kismi(satirlar(SRC, g["dosya"])[t["satir"] - 1])):
            continue  # '7{,}061' gibi ayracli yazim: duz dizeyle bozulamaz
        y = str(int(v) + 7)
        atif = "\n".join(FOY[s - 1] for s in g["atif"] if 1 <= s <= len(FOY))
        if re.search(sinir(y), atif) or re.search(sinir(y), grup_yorum_metni(g)):
            continue

        def boz(d, g=g, t=t, v=v, y=y):
            L = satirlar(d, g["dosya"])
            i = t["satir"] - 1
            L[i], n = re.subn(_duz_tam(v), y, L[i], count=1)
            assert n == 1, "tamsayi duz yazimda yok"
            yaz(d, g["dosya"], L)
        yield (f"{g['dosya']}:{t['satir']} {v} -> {y}", None, boz,
               [rf"EKSIK  {re.escape(g['dosya'])}:{t['satir']}  {re.escape(y)}  -- (ATIF EKSIK|FOYDE YOK)"])


# --- yeni kurallar (ucuncu surum) -------------------------------------------------------------------
def _metin_satiri(s):
    x = metin_kismi(s).strip()
    return bool(x) and not x.startswith("\\") and len(x) > 30


def aday_kaynak_uydurma(D):
    for g in D["gruplar"]:
        if g["atif"] or not g["kaynak"] or g["sekil"]:
            continue
        L = satirlar(SRC, g["dosya"])
        ln = next((x for x in g["blok_satirlari"] if _metin_satiri(L[x - 1])), None)
        if ln is None:
            continue

        def boz(d, g=g, ln=ln):
            L = satirlar(d, g["dosya"])
            L[ln - 1] = guvenli_ekle(L[ln - 1], r" (or $0.12345$)")
            yaz(d, g["dosya"], L)
        yield (f"{g['dosya']}:{ln} KAYNAK-yalniz grup + 0.12345", None, boz,
               [rf"EKSIK  {re.escape(g['dosya'])}:{ln}  0\.12345  -- KAYNAK DEGER EKSIK"])
    b = yapay_bas()

    def boz_y(d):
        yapay_paragraf(d, ["% KAYNAK: ON_KAYIT Sec. 5 (oz-sinama paragrafi)", "Synthetic check sentence with $0.12345$ in it."])
    yield (f"{YAPAY_DOSYA}:{b + 1} yapay KAYNAK-yalniz paragraf + 0.12345", None, boz_y,
           [rf"EKSIK  {re.escape(YAPAY_DOSYA)}:{b + 1}  0\.12345  -- KAYNAK DEGER EKSIK"])


def _kaynaksiz_hedef_satirlari(D):
    """KAYNAK-yalniz gruplarin blok satirlari ve grupsuz satirlar (FOY atifli bloklar haric): [(dosya, satir)]."""
    out = [(g["dosya"], ln) for g in D["gruplar"] if not g["atif"] for ln in g["blok_satirlari"]]
    out += [tuple(x) for x in D.get("grupsuz_satirlar", [])]
    return sorted(set(out), key=lambda x: (x[0] == "main.tex", x[0], x[1]))


def _tohum_adaylari(D, v, y, etiket):
    for dosya, ln in _kaynaksiz_hedef_satirlari(D):
        s = satirlar(SRC, dosya)[ln - 1]
        if s.lstrip().startswith("%") or not re.search(_duz_tam(v), metin_kismi(s)):
            continue

        def hazirla(d, dosya=dosya, ln=ln):
            yol = sinama_belgesi(f"{etiket} {v}")
            yorum_ekle(d, dosya, ln, f"% KAYNAK: {yol} ({etiket} {v})")

        def boz(d, dosya=dosya, ln=ln):
            L = satirlar(d, dosya)
            L[ln], n = re.subn(_duz_tam(v), y, L[ln], count=1)  # hazirla sonrasi hedef ln+1 (0 tabanli ln)
            assert n == 1, "deger satirda yok"
            yaz(d, dosya, L)
        yield (f"{dosya}:{ln} {v} -> {y} (hazirla: KAYNAK {etiket} {v})", hazirla, boz,
               [rf"EKSIK  {re.escape(dosya)}:{ln + 1}  {re.escape(y)}  --"])
    b = yapay_bas()

    def hazirla_y(d):
        yol = sinama_belgesi(f"{etiket} {v}")
        yapay_paragraf(d, [f"% KAYNAK: {yol} ({etiket} {v})", f"The synthetic {etiket} is {v} for this check."])

    def boz_y(d):
        L = satirlar(d, YAPAY_DOSYA)
        L[b], n = re.subn(_duz_tam(v), y, L[b], count=1)
        assert n == 1
        yaz(d, YAPAY_DOSYA, L)
    yield (f"{YAPAY_DOSYA}:{b + 1} yapay paragraf {v} -> {y}", hazirla_y, boz_y,
           [rf"EKSIK  {re.escape(YAPAY_DOSYA)}:{b + 1}  {re.escape(y)}  -- KAYNAK DEGER EKSIK"])


def aday_tohum_1001(D):
    yield from _tohum_adaylari(D, "1001", "1004", "tohum")


def aday_tohum_777(D):
    yield from _tohum_adaylari(D, "777", "778", "bolme tohumu")


def aday_esik(D):
    adaylar = []
    for g in D["gruplar"]:
        if g["atif"]:
            continue
        for t in g["tok"]:
            if t["deger"].startswith("-") and not t["tam"] and t["nd"] == 2:
                adaylar.append((t["deger"] != "-0.20", g["dosya"], t["satir"], t["deger"]))
    gor = set()
    for _o, dosya, ln, v in sorted(adaylar):
        if (dosya, ln, v) in gor:
            continue
        gor.add((dosya, ln, v))
        ab = v[1:]
        y = f"{Decimal(ab) - Decimal('0.05'):.2f}" if Decimal(ab) > Decimal("0.05") else f"{Decimal(ab) + Decimal('0.05'):.2f}"
        s = satirlar(SRC, dosya)[ln - 1]
        if not re.search(r"-\s*\$?" + sinir(ab), metin_kismi(s)):
            continue

        def hazirla(d, dosya=dosya, ln=ln, v=v):
            yol = sinama_belgesi(f"on kayit esigi {v}")
            yorum_ekle(d, dosya, ln, f"% KAYNAK: {yol} (esik {v})")

        def boz(d, dosya=dosya, ln=ln, ab=ab, y=y):
            L = satirlar(d, dosya)
            L[ln], n = re.subn(r"(-\s*\$?)" + sinir(ab), lambda m: m.group(1) + y, L[ln], count=1)
            assert n == 1
            yaz(d, dosya, L)
        yield (f"{dosya}:{ln} {v} -> -{y} (hazirla: KAYNAK esik {v})", hazirla, boz,
               [rf"EKSIK  {re.escape(dosya)}:{ln + 1}  -{re.escape(y)}  --"])
    b = yapay_bas()

    def hazirla_y(d):
        yol = sinama_belgesi("on kayit esigi -0.20")
        yapay_paragraf(d, [f"% KAYNAK: {yol} (esik -0.20)", r"The synthetic threshold is $\leq -0.20$ here."])

    def boz_y(d):
        L = satirlar(d, YAPAY_DOSYA)
        L[b] = L[b].replace("-0.20", "-0.15")
        yaz(d, YAPAY_DOSYA, L)
    yield (f"{YAPAY_DOSYA}:{b + 1} yapay esik -0.20 -> -0.15", hazirla_y, boz_y,
           [rf"EKSIK  {re.escape(YAPAY_DOSYA)}:{b + 1}  -0\.15  -- KAYNAK DEGER EKSIK"])


def aday_grupsuz(D):
    for dosya, ln in [tuple(x) for x in D.get("grupsuz_satirlar", [])]:
        s = satirlar(SRC, dosya)[ln - 1]
        if not _metin_satiri(s) or dosya == "main.tex":
            continue

        def boz(d, dosya=dosya, ln=ln):
            L = satirlar(d, dosya)
            L[ln - 1] = guvenli_ekle(L[ln - 1], r" (0.4321)")
            yaz(d, dosya, L)
        yield (f"{dosya}:{ln} grupsuz satira 0.4321", None, boz, [rf"EKSIK  {re.escape(dosya)}:{ln}  0\.4321  -- GRUPSUZ"])
    b = yapay_bas()

    def boz_y(d):
        yapay_paragraf(d, ["A synthetic ungrouped sentence carries 0.4321 here."])
    yield (f"{YAPAY_DOSYA}:{b} yapay grupsuz paragraf 0.4321", None, boz_y,
           [rf"EKSIK  {re.escape(YAPAY_DOSYA)}:{b}  0\.4321  -- GRUPSUZ"])


_ARALIK_HAM = re.compile(r"\[\s*(\$?\s*(?:-|\\textminus\s*|−)?\$?\s*\+?\d+\.\d+\s*\$?)\s*,\s*"
                         r"(\$?\s*(?:-|\\textminus\s*|−)?\$?\s*\+?\d+\.\d+\s*\$?)\s*\]")


def _sayi_goster(x):
    x = x.replace("$", "").replace("{", "").replace("}", "").replace("\\textminus", "-").replace("−", "-").replace(" ", "")
    neg = x.startswith("-")
    v = x.lstrip("-+")
    return ("-" if neg and Decimal(v) != 0 else "") + v, (-Decimal(v) if neg else Decimal(v))


def _foy_araligi(atif_sat, a, b):
    """Atfedilen foy satirlarinda [a; b] (ya da [a, b]) araligi aynen var mi?"""
    for s in atif_sat:
        if not (1 <= s <= len(FOY)):
            continue
        for m in re.finditer(r"\[\s*([+-]?\d+[.,]\d+)\s*[;,]\s*([+-]?\d+[.,]\d+)\s*\]", FOY[s - 1]):
            x, y = (Decimal(z.replace(",", ".").lstrip("+")) for z in m.groups())
            if x == a and y == b:
                return True
    return False


def aday_ters(D):
    n = 0
    for g in D["gruplar"]:
        if g["sekil"]:
            continue
        L = satirlar(SRC, g["dosya"])
        for ln in g["blok_satirlari"]:
            s = metin_kismi(L[ln - 1])
            for m in _ARALIK_HAM.finditer(s):
                ga, a = _sayi_goster(m.group(1))
                gb, b = _sayi_goster(m.group(2))
                if not a < b:
                    continue
                desen = [rf"EKSIK  {re.escape(g['dosya'])}:{ln}  {re.escape(f'[{gb}, {ga}]')}  -- TERS ARALIK"]
                foyden = bool(g["atif"]) and _foy_araligi(g["atif"], a, b)
                if foyden:
                    desen.append(rf"EKSIK  {re.escape(g['dosya'])}:{ln}  .*\[{re.escape(gb)}, {re.escape(ga)}\]  -- DEMET: aralik foyde TERS YONDE")

                def boz(d, g=g, ln=ln, m=m):
                    L2 = satirlar(d, g["dosya"])
                    x = L2[ln - 1]
                    assert x[m.start(1):m.end(1)] == m.group(1) and x[m.start(2):m.end(2)] == m.group(2)
                    L2[ln - 1] = x[:m.start(1)] + m.group(2) + x[m.end(1):m.start(2)] + m.group(1) + x[m.end(2):]
                    yaz(d, g["dosya"], L2)
                yield (f"{g['dosya']}:{ln} [{ga}, {gb}] -> [{gb}, {ga}]{' (foy araligi)' if foyden else ''}", None, boz, desen)
                n += 1
                break


_YON_HAM = re.compile(r"\b(exclud|includ)(es|e|ing)\s+(zero|0(?![.\d]))")


def aday_yon_cevir(D, out0):
    eksik_satir = set(re.findall(r"EKSIK  (\S+:\d+)  .*-- YON", out0))
    for g in D["gruplar"]:
        L = satirlar(SRC, g["dosya"])
        for ln in g["blok_satirlari"]:
            s = metin_kismi(L[ln - 1])
            if f"{g['dosya']}:{ln}" in eksik_satir:
                continue
            for m in _YON_HAM.finditer(s):
                # ifadeden once ya da sonra ayni satirda bir [a, b] araligi olmali (denetlenebilir cumle)
                if not _ARALIK_HAM.search(s):
                    continue
                yeni = ("includ" if m.group(1) == "exclud" else "exclud") + m.group(2) + " " + m.group(3)

                def boz(d, g=g, ln=ln, m=m, yeni=yeni):
                    L2 = satirlar(d, g["dosya"])
                    x = L2[ln - 1]
                    assert x[m.start():m.end()] == m.group(0)
                    L2[ln - 1] = x[:m.start()] + yeni + x[m.end():]
                    yaz(d, g["dosya"], L2)
                yield (f"{g['dosya']}:{ln} '{m.group(0)}' -> '{yeni}'", None, boz,
                       [rf"EKSIK  {re.escape(g['dosya'])}:{ln}  .*-- YON: metin"])
                break
    # araliga ters yon ifadesi ekleme (dogal ifade azsa)
    for g in D["gruplar"]:
        if g["sekil"]:
            continue
        L = satirlar(SRC, g["dosya"])
        for ln in g["blok_satirlari"]:
            s = metin_kismi(L[ln - 1])
            if f"{g['dosya']}:{ln}" in eksik_satir or _YON_HAM.search(s):
                continue
            m = _ARALIK_HAM.search(s)
            if not m:
                continue
            _ga, a = _sayi_goster(m.group(1))
            _gb, b = _sayi_goster(m.group(2))
            if not a < b:
                continue
            ifade = ", which excludes zero," if a <= 0 <= b else ", which includes zero,"

            def boz(d, g=g, ln=ln, m=m, ifade=ifade):
                L2 = satirlar(d, g["dosya"])
                x = L2[ln - 1]
                assert x[m.start():m.end()] == m.group(0)
                L2[ln - 1] = x[:m.end()] + ifade + x[m.end():]
                yaz(d, g["dosya"], L2)
            yield (f"{g['dosya']}:{ln} araliga '{ifade.strip(', ')}' eklendi", None, boz,
                   [rf"EKSIK  {re.escape(g['dosya'])}:{ln}  .*-- YON: metin"])
            break


def aday_yon_denetlenemedi(D):
    for g in D["gruplar"]:
        if g["yon_satirlari"] or g["sekil"]:
            continue
        L = satirlar(SRC, g["dosya"])
        bl = g["blok_satirlari"]
        for k, ln in enumerate(bl):
            s = metin_kismi(L[ln - 1]).rstrip()
            sonraki = bl[k + 1] if k + 1 < len(bl) else None
            if not _metin_satiri(s) or not s.endswith(".") or (sonraki == ln + 1) or "%" in L[ln - 1]:
                continue

            def boz(d, g=g, ln=ln):
                L2 = satirlar(d, g["dosya"])
                L2[ln - 1] = L2[ln - 1].rstrip() + " This synthetic contrast excludes zero."
                yaz(d, g["dosya"], L2)
            yield (f"{g['dosya']}:{ln} araliksiz 'excludes zero' cumlesi", None, boz,
                   [rf"EKSIK  {re.escape(g['dosya'])}:{ln}  'excludes zero'  -- YON DENETLENEMEDI"])
            break
    b = yapay_bas()

    def boz_y(d):
        yapay_paragraf(d, ["% FOY:M9.3:1526", "This synthetic interval-free contrast excludes zero."])
    yield (f"{YAPAY_DOSYA}:{b + 1} yapay araliksiz yon cumlesi", None, boz_y,
           [rf"EKSIK  {re.escape(YAPAY_DOSYA)}:{b + 1}  'excludes zero'  -- YON DENETLENEMEDI"])


def _takas_adaylari(v):
    """v'nin (or. '0.936') iki anlamli rakamini yer degistiren dizeler (sondan basa)."""
    ilk = next((i for i, c in enumerate(v) if c not in "0."), len(v))
    poz = [i for i in range(ilk, len(v)) if v[i].isdigit()]
    out = []
    for j in range(len(poz) - 1, 0, -1):
        for i in range(j - 1, -1, -1):
            a, b = poz[i], poz[j]
            if v[a] == v[b]:
                continue
            w = list(v)
            w[a], w[b] = w[b], w[a]
            w = "".join(w)
            if next((k for k, c in enumerate(w) if c not in "0."), len(w)) == ilk:
                out.append(w)
    return out


def aday_ozet_takas(D):
    """Zor durum (takasli deger atfedilen foy satirinda da var: eski KOPYA (i) kurali kacirir) once gelir; sonra ozetteki
    oteki kalemler. Ayrica foyde bir kalemle takasli halinin ayni satirda gectigi bir satiri atfeden YAPAY blok."""
    adaylar = list(_ozet_takas_dogal(D))
    # (zor durum, dogrulayicinin adini verdigi 0.936 -> 0.963, ozet) once
    adaylar.sort(key=lambda a: (not a[0], " 0.936 -> " not in a[2][0], not a[1]))
    for _zor, _oz, aday in adaylar[:DENEME - 1]:
        yield aday
    yield from _ozet_takas_yapay(D)


def _ozet_takas_yapay(D):
    kalemler = sorted({(m["deger"].lstrip("-"), m["deger"].startswith("-")) for m in D["manset"] if m["nd"] == 3})
    for v, neg in kalemler:
        for s, satir in enumerate(FOY, 1):
            if not satirlarda_isaretli([satir], v, neg):
                continue
            for y in _takas_adaylari(v):
                if not satirlarda_isaretli([satir], y, neg):
                    continue
                b = yapay_bas()
                sg = "-" if neg else ""

                def boz(d, s=s, v=v, y=y, sg=sg):
                    yapay_paragraf(d, [f"% FOY:SINAMA:{s} (kalem {sg}{v})", f"The synthetic headline value is ${sg}{y}$ in this check."])
                yield (f"{YAPAY_DOSYA}:{b + 1} yapay blok FOY {s} (kalem {sg}{v}) metinde {sg}{y} (zor durum: {sg}{y} foy {s}'de de var)",
                       None, boz, [rf"KOPYA  {re.escape(YAPAY_DOSYA)}:{b + 1}  {re.escape(sg + y)}  -- olasi bozuk kopya \(rakam takasi\)"])
                return


def _ozet_takas_dogal(D):
    kalemler = [(m["deger"].lstrip("-"), m["deger"].startswith("-"), m["etiket"]) for m in D["manset"]
                if m["nd"] == 3]
    gruplar_ = sorted(D["gruplar"], key=lambda g: g["dosya"] != "main.tex")
    main_L = satirlar(SRC, "main.tex")
    oz_bas = next((i for i, s in enumerate(main_L, 1) if "\\begin{abstract}" in s), None)
    oz_son = next((i for i, s in enumerate(main_L, 1) if "\\end{abstract}" in s), None)
    gor = set()
    for g in gruplar_:
        if not g["atif"]:
            continue
        ozet = g["dosya"] == "main.tex" and oz_bas and any(oz_bas <= x <= oz_son for x in g["blok_satirlari"])
        yorum = grup_yorum_metni(g)
        atif = [FOY[s - 1] for s in g["atif"] if 1 <= s <= len(FOY)]
        L = satirlar(SRC, g["dosya"])
        for v, neg, et in kalemler:
            if (v, neg) in gor:
                continue
            kopyalar = [(ln, m.start()) for ln in g["blok_satirlari"] for m in re.finditer(sinir(v), metin_kismi(L[ln - 1]))
                        if isaret_once(L[ln - 1], m.start()) == neg]
            if not kopyalar or not satirlarda_isaretli(atif, v, neg):
                continue
            yorumda = satirlarda_isaretli([yorum], v, neg)
            if not ((ozet and len(kopyalar) == 1) or yorumda):
                continue
            ys = [y for y in _takas_adaylari(v) if not satirlarda_isaretli([yorum], y, neg)]
            if not ys:
                continue
            ys.sort(key=lambda y: not satirlarda_isaretli(atif, y, neg))  # once atif satirlarinda olan (zor durum)
            y = ys[0]
            ln, p = kopyalar[-1]
            gor.add((v, neg))

            def boz(d, g=g, ln=ln, p=p, v=v, y=y):
                L2 = satirlar(d, g["dosya"])
                assert L2[ln - 1][p:p + len(v)] == v
                L2[ln - 1] = L2[ln - 1][:p] + y + L2[ln - 1][p + len(v):]
                yaz(d, g["dosya"], L2)
            sg = "-" if neg else ""
            zor = satirlarda_isaretli(atif, y, neg)
            yield (zor, bool(ozet), (f"{'OZET ' if ozet else ''}{g['dosya']}:{ln} {et} {sg}{v} -> {sg}{y}"
                                     f"{' (ZOR DURUM: takasli deger atfedilen foy satirinda da var)' if zor else ''}", None, boz,
                                     [rf"KOPYA  {re.escape(g['dosya'])}:{ln}  {re.escape(sg + y)}  -- olasi bozuk kopya"]))


def aday_kaynak_belge(D):
    assert "0.4321" not in ON_KAYIT and "0,4321" not in ON_KAYIT
    n = 0
    for g in D["gruplar"]:
        if not g["kaynak"] or g["sekil"]:
            continue
        L = satirlar(SRC, g["dosya"])
        ln = next((x for x in g["blok_satirlari"] if _metin_satiri(L[x - 1])), None)
        if ln is None:
            continue
        yorum = "% KAYNAK: ON_KAYIT Sec. 5 (deger 0.4321)" if n % 2 == 0 else "% KAYNAK: deger 0.4321 (belge adi yok)"
        neden = r"deger adlandirilan belgede yok \(ON_KAYIT\)" if n % 2 == 0 else "KAYNAK yorumunda belge adi yok"
        n += 1

        def boz(d, g=g, ln=ln, yorum=yorum):
            L2 = satirlar(d, g["dosya"])
            L2[ln - 1] = guvenli_ekle(L2[ln - 1], r" (or $0.4321$)")
            L2.insert(ln - 1, yorum)
            yaz(d, g["dosya"], L2)
        yield (f"{g['dosya']}:{ln} KAYNAK yorumunda 0.4321 ({'ON_KAYIT' if 'ON_KAYIT' in yorum else 'belgesiz'})", None, boz,
               [rf"EKSIK  {re.escape(g['dosya'])}:{ln + 1}  0\.4321  -- KAYNAK BELGEDE YOK: {neden}"])
    b = yapay_bas()

    def boz_y(d):
        yapay_paragraf(d, ["% KAYNAK: CLAUDE.md (deger 0.4321)", "A synthetic sourced value of $0.4321$ appears here."])
    yield (f"{YAPAY_DOSYA}:{b + 1} yapay KAYNAK CLAUDE.md 0.4321", None, boz_y,
           [rf"EKSIK  {re.escape(YAPAY_DOSYA)}:{b + 1}  0\.4321  -- KAYNAK BELGEDE YOK: deger adlandirilan belgede yok \(CLAUDE\.md\)"])


SINAMALAR = [
    ("A3 yanlis sayi (atfedilen satirda yok, foyde baska satirda var)", aday_a3),
    ("A2 uydurma sayi (foyde hic yok)", aday_a2),
    ("A1 kaymis atif", aday_a1),
    ("Gecersiz satir numarasi", aday_gecersiz),
    ("B manset: deger her yerde degisti", aday_b_hepsi),
    ("S1 deger takasi (iki demetin kestirimleri)", aday_takas),
    ("S1 tek kopya bozmasi (B KALDI vermeli)", aday_tek_kopya),
    ("K2 isaret cevirme (negatif -> isaretsiz)", aday_isaret),
    ("S3 tamsayi bozmasi", aday_tamsayi),
    ("K1b KAYNAK-yalniz gruba uydurma sayi", aday_kaynak_uydurma),
    ("K1b KAYNAK-yalniz paragraf tohumu 1001 -> 1004", aday_tohum_1001),
    ("K1b bolme tohumu 777 -> 778", aday_tohum_777),
    ("K1b on kayit esigi -0.20 -> -0.15", aday_esik),
    ("K1b GRUPSUZ satira sayi", aday_grupsuz),
    ("T1 ters aralik (ve foyde ters yon DEMET)", aday_ters),
    ("Y1 YON cevirme (excludes <-> includes)", "yon_cevir"),
    ("Y1 YON denetlenemedi (araliksiz cumle)", aday_yon_denetlenemedi),
    ("S1b ozet tek kopya rakam takasi", aday_ozet_takas),
    ("Y2 KAYNAK degeri adlandirilan belgede yok", aday_kaynak_belge),
]


def dene(tmp, e0, out0, kimlik, aday):
    aciklama, hazirla, boz, desenler = aday
    dd = tmp / kimlik
    kopya(dd)
    taban_e, taban_out = e0, out0
    try:
        if hazirla:
            hazirla(dd)
            rc_t, taban_e, taban_out = kos(dd)
            if taban_e is None:
                return ("hata", aciklama, f"hazirlanmis taban kosmadi:\n{taban_out[-1500:]}")
        boz(dd)
    except AssertionError as ex:
        return ("uygulanamadi", aciklama, str(ex))
    rc, e, out = kos(dd)
    yeni = all(re.search(x, out) for x in desenler) and not re.search(desenler[0], taban_out)
    if rc == 1 and e is not None and taban_e is not None and e > taban_e and yeni:
        return ("yakalandi", aciklama, f"EN_EKSIK {taban_e} -> {e}")
    en = out.split("\n[TR]")[0]
    eks = "\n".join("        " + s for s in en.splitlines() if "EKSIK " in s and s not in taban_out)
    return ("kacti", aciklama, f"cikis {rc}, EN_EKSIK {taban_e} -> {e}; beklenen: {desenler}\n"
                               f"      bozmadan sonra YENI EKSIK satirlari:\n{eks[-2500:]}")


def main():
    global SRC
    hata = []
    rc, _e, out = kos(EN, "--ayristirma-sinami")
    ok = rc == 0
    print(f"  {'GECTI' if ok else 'KALDI'}  0 ayristirma: isaret bicimleri ({out.strip().splitlines()[-1] if out.strip() else '-'})")
    if not ok:
        hata.append("ayristirma")
        print("\n".join("      " + s for s in out.splitlines() if "KALDI" in s))
    tmp = Path(tempfile.mkdtemp(prefix="vmn_sinama_"))
    vaka = 0
    try:
        SRC = tmp / "anlik"
        kopya(SRC, EN)
        rc0, e0, _ = kos(EN)
        d = tmp / "temiz"
        kopya(d)
        dokum = tmp / "dokum.json"
        rc, e, out0 = kos(d, "--dokum", str(dokum))
        ok = (e == e0 and rc == rc0 and dokum.exists())
        print(f"  {'GECTI' if ok else 'KALDI'}  bozulmamis kopya gercek makaleyle ayni (EN_EKSIK {e} / {e0})")
        if not ok:
            hata.append("bozulmamis kopya")
            raise SystemExit(1)
        e0 = e
        D = json.loads(dokum.read_text(encoding="utf-8"))
        isler = []
        for no, (ad, uretec) in enumerate(SINAMALAR, 1):
            gen = aday_yon_cevir(D, out0) if uretec == "yon_cevir" else uretec(D)
            adaylar = []
            for a in gen:
                adaylar.append(a)
                if len(adaylar) >= DENEME:
                    break
            isler.append((no, ad, adaylar))
        with ThreadPoolExecutor(max_workers=6) as ex:
            gelecek = {(no, k): ex.submit(dene, tmp, e0, out0, f"s{no}_{k}", a)
                       for no, _ad, adaylar in isler for k, a in enumerate(adaylar)}
            sonuc = {k: f.result() for k, f in gelecek.items()}
        for no, ad, adaylar in isler:
            sn = [sonuc[(no, k)] for k in range(len(adaylar))]
            uyg = [s for s in sn if s[0] != "uygulanamadi"]
            yak = [s for s in uyg if s[0] == "yakalandi"]
            vaka += len(uyg)
            if uyg and len(yak) == len(uyg):
                print(f"  GECTI  {no} {ad}  ({len(yak)}/{len(uyg)} aday yakalandi)")
                for s in yak:
                    print(f"           + {s[1]}  [{s[2]}]")
            else:
                print(f"  KALDI  {no} {ad}  ({len(yak)}/{len(uyg)} aday yakalandi{'; hedef bulunamadi' if not uyg else ''})")
                for s in sn:
                    if s[0] != "yakalandi":
                        print(f"           - {s[0].upper()}  {s[1]}: {s[2]}")
                hata.append(ad)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        for p in BELGE_DIZIN.glob("_kapi_sinama_belgesi_*.md"):
            p.unlink(missing_ok=True)
    print("-" * 60)
    if hata:
        print(f"SONUC: KALDI -- {len(hata)} oz-sinama: " + "; ".join(hata))
        sys.exit(1)
    print(f"SONUC: GECTI -- kapi {len(SINAMALAR)} sinamanin {vaka} bozmasinin HEPSINI yakaladi; ayristirma ve bozulmamis kopya dogru.")


if __name__ == "__main__":
    main()
