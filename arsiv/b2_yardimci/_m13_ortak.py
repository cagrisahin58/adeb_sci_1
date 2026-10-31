# -*- coding: utf-8 -*-
"""M13 ureticilerinin ortak yardimcilari (31.10.2026, deney-takibi).

Uc uretici (_m13_tarif.py, _m13_kayit.py, _m13_zaman.py) sayilari elle yazmaz; her degeri bir kaynak dosyanin
belirli bir satirindan ya da JSON anahtarindan okur ve kanit olarak (dosya, satir, satir metni) birlikte yazar.
Bu modul o okuma islerini ve cikti meta'sini toplar. Depo kokunden ya da herhangi bir yerden calisir.
"""
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
FOY = "results/C1_REFERANS_FOYU.md"
_SATIR = {}
_OKUNAN = set()
_GIT = {}  # "git:<commit>:<yol>" -> blob kimligi (git rev-parse <commit>:<yol>)

# 31.10.2026 duzeltme turu (bulgu 3): foy M13 bolumunde bu JSON'larin meta'sini yazdigi icin ham foy sha256'si kaynak
# olarak kaydedilirse uretim sabit noktaya oturmaz. Foyun kaynak ozeti '## M13:' bolumu cikarilmis metnin sha256'sidir.
FOY_M13_BAS, FOY_M13_SON = b"\n## M13:", b"\n## Sabit dizgeler"
FOY_OZETI_TANIMI = ("results/C1_REFERANS_FOYU.md icin kaynaklar_sha256 degeri (ve foy_ozeti.m13_haric_sha256) ham dosyanin "
                    "degil, '\\n## M13:' ile '\\n## Sabit dizgeler' arasindaki bayt araligi cikarilmis metnin sha256'sidir "
                    "(arsiv/b2_yardimci/_m13_kontrol.py ile ayni kural). Foyde M13 yoksa ham sha256 ile aynidir.")
YENIDEN_URETIM_NOTU = ("Foyun M13 bolumu bu JSON'un meta'sini (uretildi_utc, betik sha256) basar; ham foy sha256'si kaynak "
                       "olarak yazilsaydi her JSON uretimi foyu, her foy uretimi JSON'u degistirirdi ve uretim sabit noktaya "
                       "oturmazdi (onceki surumdeki 'yalniz uretildi_utc degisir' notu bu yuzden yanlisti). Duzeltmeden sonra "
                       "JSON'lar foyun yalniz M13 disi metnine baglidir: M13 disi foy ve kaynak dosyalar degismedikce JSON "
                       "yeniden uretildiginde JSON'da yalniz meta.uretildi_utc, foyde yalniz M13 meta satirlarindaki "
                       "uretildi_utc degisir (31.10.2026'da iki ardisik uretimle denetlendi; bkz. "
                       "results/q1/konsey_kayit_kurallari.DEGISIKLIK.md).")


def foy_m13_haric_bayt():
    f = (KOK / FOY).read_bytes()
    if f.count(FOY_M13_BAS) == 0:
        return f
    if f.count(FOY_M13_BAS) != 1 or f.count(FOY_M13_SON) != 1:
        raise SystemExit("foyde M13 ya da Sabit dizgeler basligi tekil degil")
    return f[:f.index(FOY_M13_BAS)] + f[f.index(FOY_M13_SON):]


def sha(rel):
    p = KOK / rel
    _OKUNAN.add(rel)
    if rel == FOY:
        return hashlib.sha256(foy_m13_haric_bayt()).hexdigest()
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _git(*arg):
    import subprocess
    r = subprocess.run(["git", "-C", str(KOK), *arg], capture_output=True)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(arg)}: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8")


def git(*arg):
    """Salt okur git cagrisi (show, log, rev-parse); depo durumunu degistirmez."""
    return _git(*arg)


def satirlar(rel):
    """Calisma agacindaki dosya ya da 'git:<commit>:<yol>' bicimiyle bir commit'teki surumu."""
    if rel not in _SATIR:
        if rel.startswith("git:"):
            _, c, yol = rel.split(":", 2)
            _SATIR[rel] = _git("show", f"{c}:{yol}").split("\n")
            _GIT[rel] = _git("rev-parse", f"{c}:{yol}").strip()
        else:
            _SATIR[rel] = (KOK / rel).read_text(encoding="utf-8").split("\n")
            _OKUNAN.add(rel)
    return _SATIR[rel]


# 31.10.2026 duzeltme turu (bulgu 4): on kayit metninde deger arama. Eski arama mutlak degerin iki ve bir ondalikli
# yuvarlanmis bicimlerini satirda alt dizge olarak ariyordu (isaret, sozcuk siniri ve yuvarlama denetimi yoktu; ornegin
# 0,06 icin '0,1' ya da '0,0605' icindeki '0,06' kabul ediliyordu).
ON_KAYIT_ARAMA_KURALI = (
    "Deger yalniz yuvarlamasiz yazimlarla aranir: en kisa ondalik gosterim ve sonuna sifir eklenmis bicimleri (en cok uc "
    "ondalik; ornegin 0.1 icin 0,1 / 0,10 / 0,100; 0.796 icin yalniz 0,796), ondalik ayirac virgul. Sozcuk siniri: "
    "eslesmenin oncesinde rakam, virgul ya da nokta; sonrasinda rakam ya da ayiracla baslayan rakam olamaz. Isaret: negatif "
    "deger icin hemen onde eksi (U+2212, '-' ya da '–') zorunlu; pozitif deger icin hemen onde eksi olamaz ('+' ve '±' "
    "serbest). En az bir eslesme yoksa uretim durur.")
_EKSI = "−\\-–"


def ondalik_yazimlari(x):
    a = abs(float(x))
    s = format(a, "f") if "e" in repr(a) else repr(a)
    if s.endswith(".0"):
        s = s[:-2]
    tam, _, ond = s.partition(".")
    out = [s.replace(".", ",")]
    if ond:
        for k_ in range(len(ond) + 1, 4):
            out.append(f"{tam},{ond.ljust(k_, '0')}")
    return out


def on_kayit_ara(rel, n, x):
    """On kayit satiri n'de x degerinin isaretli, sozcuk sinirli, yuvarlamasiz yazimlari. Donus: eslesme listesi."""
    s = satirlar(rel)[n - 1]
    es = []
    for c in ondalik_yazimlari(x):
        if float(x) < 0:
            d = rf"(?<![0-9.,])[{_EKSI}]{re.escape(c)}(?![0-9]|[.,][0-9])"
        else:
            d = rf"(?<![0-9.,{_EKSI}])\+?{re.escape(c)}(?![0-9]|[.,][0-9])"
        for m in re.finditer(d, s):
            es.append({"yazim": m.group(0), "sutun": m.start() + 1})
    es.sort(key=lambda e: e["sutun"])
    return es


def jyukle(rel):
    _OKUNAN.add(rel)
    return json.loads((KOK / rel).read_text(encoding="utf-8"))


def bul(rel, parca, sira=None, bas=1, son=None):
    """`parca` gecen satirin 1 tabanli numarasi. sira None ise tekil olmali; degilse sira'inci (0 tabanli) eslesme."""
    L = satirlar(rel)
    son = son or len(L)
    es = [i for i in range(bas, son + 1) if parca in L[i - 1]]
    if sira is None:
        if len(es) != 1:
            raise SystemExit(f"{rel}: '{parca}' {len(es)} kez geciyor (satir {bas}-{son}); tekil olmali")
        return es[0]
    if len(es) <= sira:
        raise SystemExit(f"{rel}: '{parca}' icin {sira + 1}. eslesme yok")
    return es[sira]


def kanit(rel, parca, desen=None, tip=float, sira=None, bas=1, son=None, grup=1):
    """Satiri bulur; desen verilirse ilk eslesmenin `grup` grubunu `tip` ile cevirir."""
    n = bul(rel, parca, sira, bas, son)
    s = satirlar(rel)[n - 1]
    o = {"dosya": rel, "satir": n, "metin": s.strip()[:240]}
    if desen is not None:
        m = re.search(desen, s)
        if not m:
            raise SystemExit(f"{rel}:{n}: desen {desen!r} eslesmedi: {s.strip()[:120]}")
        o["deger"] = tip(m.group(grup))
    return o


def kesir(ifade):
    """'8/255' gibi bir kaynak ifadesini sayiya cevirir (yalniz a/b ya da ondalik)."""
    ifade = ifade.strip()
    m = re.fullmatch(r"([0-9.]+)\s*/\s*([0-9.]+)", ifade)
    return float(m.group(1)) / float(m.group(2)) if m else float(ifade)


def tr_ondalik(x):
    """Sayiyi on kayit metnindeki gibi ondalik virgulle yazar (metin denetimi icin; deger uretmez)."""
    s = repr(float(x))
    if s.endswith(".0"):
        s = s[:-2]
    return s.replace(".", ",")


def metinde_var(rel, n, *parcalar):
    s = satirlar(rel)[n - 1]
    eksik = [p for p in parcalar if p not in s]
    if eksik:
        raise SystemExit(f"{rel}:{n}: beklenen parcalar yok: {eksik}")
    return True


def bolum_araligi(rel, baslik_bas):
    """'### M9.3' gibi bir basligin satiri ile bir sonraki ayni ya da ust duzey basliktan onceki satir."""
    L = satirlar(rel)
    n = bul(rel, baslik_bas)
    duzey = len(baslik_bas) - len(baslik_bas.lstrip("#"))
    for i in range(n + 1, len(L) + 1):
        s = L[i - 1]
        if s.startswith("#"):
            d = len(s) - len(s.lstrip("#"))
            if d <= duzey:
                return n, i - 1
    return n, len(L)


def md_hucreler(s):
    s = s.strip()
    if not (s.startswith("|") and s.endswith("|")):
        raise ValueError(f"tablo satiri degil: {s[:80]}")
    return [c.strip() for c in s[1:-1].split("|")]


def foy_tablo_hucresi(bolum, satir_bas, sutun, sira=None):
    """Foyde `bolum` basligi altindaki tabloda `satir_bas` ile baslayan satirin `sutun` adli hucresi.
    Donus: {"foy_satiri", "foy_baslik_satiri", "sutun", "deger", "satir_metni_sha256"}."""
    a, b = bolum_araligi(FOY, bolum)
    n = bul(FOY, satir_bas, sira, a, b)
    L = satirlar(FOY)
    if not L[n - 1].startswith(satir_bas):
        raise SystemExit(f"foy:{n} '{satir_bas}' ile baslamiyor")
    h = n
    while h > a and not L[h - 2].startswith("|---"):
        h -= 1
    bas_n = h - 2  # ayrac satirinin ustu
    basliklar = md_hucreler(L[bas_n - 1])
    hucre = md_hucreler(L[n - 1])
    if sutun not in basliklar:
        raise SystemExit(f"foy:{bas_n}: '{sutun}' sutunu yok: {basliklar}")
    return {"foy_satiri": n, "foy_baslik_satiri": bas_n, "sutun": sutun, "deger": hucre[basliklar.index(sutun)],
            "satir_metni_sha256": hashlib.sha256(L[n - 1].encode("utf-8")).hexdigest()}


def foy_satiri(bolum, parca, sira=None):
    a, b = bolum_araligi(FOY, bolum)
    n = bul(FOY, parca, sira, a, b)
    L = satirlar(FOY)
    return {"foy_satiri": n, "satir_metni_sha256": hashlib.sha256(L[n - 1].encode("utf-8")).hexdigest(),
            "parca": parca}


def yaz(cikti_rel, govde, betik_path, etiket, tanim):
    """Ciktiyi meta ile yazar. meta.kaynaklar: okunan her dosyanin sha256'si (cikti haric)."""
    betik_rel = str(Path(betik_path).resolve().relative_to(KOK))
    ortak_rel = str(Path(__file__).resolve().relative_to(KOK))
    kaynaklar = {}
    for rel in sorted(_OKUNAN):
        if rel == cikti_rel:
            continue
        kaynaklar[rel] = sha(rel)  # foy icin M13 haric ozet (bulgu 3)
    meta = {"betik": betik_rel, "betik_sha256": hashlib.sha256((KOK / betik_rel).read_bytes()).hexdigest(),
            "ortak_modul": ortak_rel,
            "ortak_modul_sha256": hashlib.sha256((KOK / ortak_rel).read_bytes()).hexdigest(),
            "uretildi_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
            "python": sys.version.split()[0],
            "kaynak_sayisi": len(kaynaklar), "kaynaklar_sha256": kaynaklar}
    if FOY in kaynaklar:
        meta["foy_ozeti"] = {"dosya": FOY, "m13_haric_sha256": kaynaklar[FOY], "tanim": FOY_OZETI_TANIMI}
        meta["yeniden_uretim_notu"] = YENIDEN_URETIM_NOTU
    if _GIT:
        meta["git_kaynaklari"] = {"tanim": "salt okur 'git show <commit>:<yol>' ile okunan surumler; deger git blob kimligi",
                                  "blob": dict(sorted(_GIT.items()))}
    out = {"etiket": etiket, "tanim": tanim, "meta": meta, **govde}
    p = KOK / cikti_rel
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"yazildi: {cikti_rel} ({len(kaynaklar)} kaynak)")
    return out
