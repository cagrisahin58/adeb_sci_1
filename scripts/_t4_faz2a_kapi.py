#!/usr/bin/env python3
"""FAZ 2A kapi tamamlamasi.

1) A kolunun dort protokollu NOKTA tahmini (+0,273) metinden dusmustu;
   araligi aniyorsak noktayi da anmaliyiz (kapi yakaladi).
2) Blok cikisi serisinin tasiyici degerleri kapiya baglanir: yeni CLS
   minimumu, yama-jetonu minimumu, oran ve norm siniri.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

EN = Path("/home/firat/projects/adeb_sci_1/paper/manuscript/sections")
TR = Path("/home/firat/projects/adeb_sci_1/paper/manuscript_tr/sections")

if not uygula([
    ("04_experiments.tex",
     r"contains the controlled arm's $[+0.219, +0.371]$ entirely",
     r"contains the controlled arm's $+0.273$ (CI $[+0.219, +0.371]$) entirely",
     "0.273 geri"),
], EN):
    sys.exit(1)

if not uygula([
    ("04_deneyler.tex",
     r"kontrollü kolun $[+0{,}219;\ +0{,}371]$ aralığını bütünüyle kapsar",
     r"kontrollü kolun $+0{,}273$ (GA $[+0{,}219;\ +0{,}371]$) değerini "
     r"bütünüyle kapsar",
     "TR 0.273 geri"),
], TR):
    sys.exit(1)

# ---------------------------------------------------------------- kapi eki
P = Path("/home/firat/projects/adeb_sci_1/scripts/verify_manuscript_numbers.py")
t = P.read_text(encoding="utf-8")
IMZA = "# --- T4: blok cikisi derinlik profili ---"
if IMZA in t:
    print("  [=] blok cikisi kontrolleri zaten var")
else:
    EK = '''
# --- T4: blok cikisi derinlik profili ---
# ViT ozetleri artik ARTIK BLOK CIKISINDA aliniyor (siniflandiricinin
# okudugu tensor). Onceki surumde CLS yalniz .mlp alt-blogunda
# hesaplaniyordu ve Tablo VII denk olmayan nicelikleri karsilastiriyordu.
try:
    import glob as _g2
    _c4 = [json.loads(Path(_f).read_text(encoding="utf-8"))
           for _f in sorted(_g2.glob(str(ROOT / "results/c1_c4/pair*/c4_summary.json")))]

    def _blokser(_key):
        _yig = []
        for _d in _c4:
            _o = {}
            for _k, _v in _d["vit"].get(_key, {}).items():
                if _k.startswith("block") and ".mlp" not in _k:
                    _o[int(_k[5:])] = _v["mean"]
            if _o:
                _yig.append([_o[_i] for _i in sorted(_o)])
        return np.array(_yig).mean(0) if _yig else None

    _cls = _blokser("cos_block_cls")
    _pm = _blokser("cos_block_token_mean")
    _al = _blokser("cos_block_output")
    if _cls is not None and _pm is not None:
        chk("T4 blok CLS minimumu", float(_cls.min()), 4)
        chk("T4 blok yama-ort minimumu", float(_pm.min()), 4)
        chk("T4 blok tum-jeton minimumu", float(_al.min()), 4)
        chk("T4 CLS/yama kayma orani",
            float((1 - _cls.min()) / (1 - _pm.min())), 2)
except Exception as _e:
    print(f"  [uyari] blok cikisi serisi okunamadi: {_e}")
'''
    m = t.rfind("\nrows = []")
    if m < 0:
        sys.exit("BASARISIZ: 'rows = []' bulunamadi")
    t = t[:m] + EK + t[m:]
    P.write_text(t, encoding="utf-8")
    print("  [+] blok cikisi kontrolleri eklendi")
