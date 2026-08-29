#!/usr/bin/env python3
"""Hakem turu 3'un YENI tasiyici sayilarini sayi kapisina baglar.

Kural (CLAUDE.md KARANTINA): disariya cikan her sayi bir artefakttan
gelmeli ve bir kapiyla korunmali. Bu gecis, revizyonda metne giren
sayilari verify_manuscript_numbers.py'ye ekler.
"""
import sys
from pathlib import Path

P = Path("/home/firat/projects/adeb_sci_1/scripts/verify_manuscript_numbers.py")
t = P.read_text(encoding="utf-8")

IMZA = "# --- T3: hakem turu 3'te metne giren sayilar ---"
if IMZA in t:
    print("zaten eklenmis")
    sys.exit(0)

EK = '''
# --- T3: hakem turu 3'te metne giren sayilar ---
# Manset artik tek bir yayilim degil, UC BITISIK ACIKLIK olarak raporlaniyor.
# Acikliklar protokol ortalamalarindan TUREVDIR; yuvarlanmis tablo
# degerlerinden degil HAM degerlerden hesaplanmalidir (once yuvarlanmislardan
# turetilmis ve 5,30/5,80 yazilmisti; dogrusu 5,31/5,79).
_pd = {k: v["diff"]["mean"] for k, v in tr["protocols"].items()}
chk("T3 aciklik hedef-dogru->her-ikisi-dogru",
    _pd["both_correct"] - _pd["target_correct"])
chk("T3 aciklik her-ikisi-dogru->ham", _pd["raw"] - _pd["both_correct"])
chk("T3 aciklik ham->basarili-kaynak", _pd["successful_source"] - _pd["raw"])

# Her-ikisi-dogru GA'si TANIMLI BIR YORDAM DEGILDIR: makale artik uc tohumun
# kendi araliklarini ve kosumlar arasi t araligini ayri ayri veriyor.
_bcp = tr["both_correct_paired"]
for _i, (_a, _u) in enumerate(zip(_bcp["ci_low"]["values"],
                                  _bcp["ci_high"]["values"])):
    chk(f"T3 tohum{_i+1} GA alt", _a)
    chk(f"T3 tohum{_i+1} GA ust", _u)
_d3 = np.array(_bcp["diff_pp"]["values"])
_t = 4.302652729911275  # t(0,975; sd=2)
_yari = _t * _d3.std(ddof=1) / np.sqrt(len(_d3))
chk("T3 kosumlar arasi t alt", _d3.mean() - _yari)
chk("T3 kosumlar arasi t ust", _d3.mean() + _yari)

# Gradyan seyrekligi KOSUM duzeyinde raporlaniyor (ornek duzeyi degil).
# Tablo VIII'in kendi basligi cikarimin kosum duzeyinde oldugunu soyluyor;
# iddia da orada kurulmali.
import glob as _glob


def _grad_cift(_key):
    _R, _V = [], []
    for _p in sorted(_glob.glob(str(ROOT / "results/c1_gradient/pair*"))):
        _f = Path(_p) / "gradient_summary.json"
        if not _f.exists():
            continue
        _o = json.loads(_f.read_text(encoding="utf-8"))

        def _bul(_x, _m):
            if isinstance(_x, dict):
                if _m in _x and isinstance(_x[_m], dict):
                    _v = _x[_m].get(_key)
                    if isinstance(_v, dict):
                        return _v.get("mean")
                    if _v is not None:
                        return _v
                for _y in _x.values():
                    _r = _bul(_y, _m)
                    if _r is not None:
                        return _r
            return None
        _a, _b = _bul(_o, "ResNet18_AT"), _bul(_o, "ViT_Tiny_AT")
        if _a is not None and _b is not None:
            _R.append(_a); _V.append(_b)
    return np.array(_R), np.array(_V)


try:
    from scipy import stats as _st
    _hamp = {}
    for _ad, _k in (("Hoyer", "sparsity_hoyer"), ("Gini", "sparsity_gini"),
                    ("Frac", "sparsity_rel_threshold"),
                    ("Hiz", "gradient_alignment")):
        _R, _V = _grad_cift(_k)
        if len(_R) >= 2:
            _hamp[_ad] = float(_st.ttest_rel(_R, _V).pvalue)
    if len(_hamp) == 4:
        chk("T3 kosum p Gini", _hamp["Gini"], 3)
        chk("T3 kosum p Frac", _hamp["Frac"], 3)
        chk("T3 kosum p Hoyer", _hamp["Hoyer"], 3)
        chk("T3 kosum p hizalanma", _hamp["Hiz"], 4)
        _sk = sorted((v for k, v in _hamp.items() if k != "Hiz"))
        _onceki, _holm = 0.0, []
        for _i, _p in enumerate(_sk):
            _onceki = max(_onceki, min(1.0, (len(_sk) - _i) * _p))
            _holm.append(_onceki)
        chk("T3 kosum Holm (uc olcu)", max(_holm), 3)
except ImportError:
    pass
'''

# ekleme yeri: CHECKS listesi kullanilmadan HEMEN once
ANAHTAR = "\n# --- raporlama ---"
if ANAHTAR in t:
    t = t.replace(ANAHTAR, EK + ANAHTAR, 1)
else:
    # yedek: dosyanin sonundaki dogrulama dongusunden once
    m = t.rfind("\nfor ")
    if m < 0:
        sys.exit("BASARISIZ: ekleme noktasi bulunamadi")
    t = t[:m] + EK + t[m:]

P.write_text(t, encoding="utf-8")
print("verify_manuscript_numbers.py'ye T3 kontrolleri eklendi")
