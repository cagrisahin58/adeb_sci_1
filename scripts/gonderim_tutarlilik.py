#!/usr/bin/env python3
"""YEDINCI KAPI: gonderim malzemeleri makaleyle ve artefaktlarla tutuyor mu?

NEDEN VAR. Alti kapinin hicbiri `paper/submission/` altini taramiyordu ve o
bosluk gercek bir kusur uretti: 2026-08-25'te goruldu ki kapak mektubu,
one cikanlar, beyanlar ve gonderim oncesi kontrol listesi 2026-02-16
tarihliydi -- yani C1 sizinti duzeltmesinden de Q1 kampanyasindan da ONCE.
Editore gidecek belgeler:

  - ESKI BASLIGI tasiyordu ("A Comparative Study of ..."),
  - KARANTINADAKI run2 sayilarini basiyordu (AutoAttack 35,74 / 32,94),
  - ve makalenin sonradan CURUTTUGU bir sonucu iddia ediyordu
    ("the asymmetry vanishes entirely ... 20.95% vs 20.32%").

Bir belge editore gidiyorsa karantina kurali ona da uygulanir.

Kapi uc sey denetler:
  1. BASLIK, makale ile gonderim malzemeleri arasinda AYNI mi,
  2. KARANTINADAKI degerlerden hicbiri gecmiyor mu,
  3. Tasiyici sayilar ARTEFAKTLARLA tutuyor mu.

Cikis kodu: uyusmazlik varsa 1, yoksa 0.
"""
import json
import os
import re
import sys
from pathlib import Path

_kok = os.environ.get("MANUSCRIPT_ROOT")
_avar = os.environ.get("ARTEFAKT_ROOT")
_VARSAYILAN = (Path("/workspace") if Path("/workspace/results").is_dir()
               else Path(__file__).resolve().parents[1])
ROOT = Path(_kok) if _kok else _VARSAYILAN
ARTEFAKT_ROOT = Path(_avar) if _avar else _VARSAYILAN

S = ROOT / "paper/submission"
DOSYALAR = ["cover_letter.tex", "highlights.txt", "declarations.txt",
            "pre_submission_checklist.md"]

metinler = {}
for f in DOSYALAR:
    p = S / f
    if not p.exists():
        sys.exit(f"KAPI HATASI: {p} yok; denetim yapilmadi.")
    t = p.read_text(encoding="utf-8")
    if not t.strip():
        sys.exit(f"KAPI HATASI: {p} bos; denetim yapilmadi.")
    metinler[f] = t

ana = (ROOT / "paper/manuscript/main.tex").read_text(encoding="utf-8")
_m = re.search(r"\\title\{(.+?)\}\s*\n", ana, re.S)
if not _m:
    sys.exit("KAPI HATASI: makalenin basligi okunamadi.")
BASLIK = " ".join(_m.group(1).split())

kusur = []


def jl(p):
    return json.loads((ARTEFAKT_ROOT / p).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 1. BASLIK
print("=== 1. BASLIK UYUMU ===")
print(f"  makale: {BASLIK[:78]}...")
# baslik LaTeX kacislari tasiyabilir; sadelestirerek karsilastir
_sade = re.sub(r"[^a-zA-Z0-9 ]", "", BASLIK).lower()
for f in ("cover_letter.tex", "highlights.txt", "declarations.txt",
          "pre_submission_checklist.md"):
    _mt = re.sub(r"[^a-zA-Z0-9 ]", " ", metinler[f]).lower()
    _mt = " ".join(_mt.split())
    var = _sade in _mt
    print(f"  {f:32s} {'tutuyor' if var else 'TUTMUYOR'}")
    if not var:
        kusur.append(f"{f}: makalenin basligini tasimiyor")

# ------------------------------------------------------------ 2. KARANTINA
# CLAUDE.md'nin KARANTINA kurali: run1/run2 sayilari hicbir yere giremez.
KARANTINA = [
    ("35.74", "run2 AutoAttack ResNet"),
    ("32.94", "run2 AutoAttack ViT"),
    ("40.97", "run2 PGD ResNet"),
    ("36.87", "run2 PGD ViT"),
    ("20.95", "curutulmus 'kosullu parite' degeri"),
    ("20.32", "curutulmus 'kosullu parite' degeri"),
    ("0.474", "tek kosum Hoyer ResNet"),
    ("0.449", "tek kosum Hoyer ViT"),
]
CURUK_IFADE = [
    ("vanishes entirely", "asimetrinin tamamen kayboldugu iddiasi CURUTULDU"),
    ("is symmetric", "kosullu transferin simetrik oldugu iddiasi CURUTULDU"),
    ("not a conference extension", "makale ARTIK bir konferans genisletmesidir"),
]

print("\n=== 2. KARANTINA VE CURUTULMUS IDDIA ===")
for f, t in metinler.items():
    for d, ne in KARANTINA:
        if re.search(r"(?<![\d.])" + re.escape(d) + r"(?!\d)", t):
            print(f"  {f}: KARANTINA DEGERI {d} ({ne})")
            kusur.append(f"{f}: karantinadaki {d} gecyor -- {ne}")
    for ifade, ne in CURUK_IFADE:
        if ifade in t:
            print(f"  {f}: CURUK IFADE '{ifade}' ({ne})")
            kusur.append(f"{f}: '{ifade}' -- {ne}")
if not any("KARANTINA DEGERI" in x or "CURUK" in x for x in kusur):
    print("  temiz: karantinadaki deger ya da curutulmus iddia YOK")

# --------------------------------------------------- 3. TASIYICI SAYILAR
seed = jl("results/c1_seeds/c1_seed_summary.json")["aggregate"]
trs = jl("results/c1_transfer/c1_transfer_summary.json")
e7 = jl("results/q1/svhn/transfer/e7_transfer_summary.json")
vr = jl("results/q1/variance_ratio.json")
P4 = ["raw", "target_correct", "both_correct", "successful_source"]
_d = [trs["protocols"][p]["diff"]["mean"] for p in P4]

SAYILAR = [
    ("AA ResNet", f"{seed['resnet']['aa']['mean']:.2f}"),
    ("AA ViT", f"{seed['vit']['aa']['mean']:.2f}"),
    ("protokol yayilimi", f"{trs['protocol_spread_pp']['mean']:.2f}"),
    ("yayilim sd", f"{trs['protocol_spread_pp']['std']:.2f}"),
    ("asimetri alt", f"{min(_d):.1f}"),
    ("asimetri ust", f"{max(_d):.1f}"),
    ("kosum sd min", f"{vr['PAYDA_kosum_etkisi_AYNI_NICELIK']['sd_min']:.2f}"),
    ("kosum sd max", f"{vr['PAYDA_kosum_etkisi_AYNI_NICELIK']['sd_max']:.2f}"),
]

print("\n=== 3. TASIYICI SAYILAR (kapak mektubu + one cikanlar) ===")
govde = metinler["cover_letter.tex"] + "\n" + metinler["highlights.txt"]
for ad, v in SAYILAR:
    var = re.search(r"(?<![\d.,])" + re.escape(v) + r"(?!\d)", govde) is not None
    print(f"  {ad:22s} {v:>8s}  {'OK' if var else 'YOK'}")
    if not var:
        kusur.append(f"tasiyici sayi {ad} = {v} gonderim metninde YOK")

print("\n" + "-" * 62)
if kusur:
    print("SONUC: KALDI -- gonderim malzemeleri makaleyle tutmuyor:")
    for x in kusur:
        print("  -", x)
    print("Editore giden bir belge de karantina kuralina tabidir.")
    sys.exit(1)
print("SONUC: GECTI -- gonderim malzemeleri makaleyle ve artefaktlarla tutuyor,")
print("karantinadaki deger ya da curutulmus iddia yok.")
sys.exit(0)
