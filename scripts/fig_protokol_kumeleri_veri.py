#!/usr/bin/env python3
"""Ic ice kosullama kumeleri sekli icin VERI dosyasi.

Sekil, dort protokolun ayni test kumesini nasil ic ice altkumelere
daralttigini ve olculen CNN->ViT asimetrisinin bununla nasil degistigini
gosterecek. Her sayi C1_REFERANS_FOYU'nun kaynagi olan artefakttan
(results/c1_transfer/c1_transfer_summary.json) okunur; sekil betigi bu
dosyadan baska hicbir yerden sayi almaz (KARANTINA kurali).

Kume ic iceligi (src/analysis/protokoller.py):
  raw               = tum test kumesi
  target_correct    = tc
  both_correct      = tc & sc
  successful_source = tc & sc & sa      -> SS c BC c TC c ALL (yon basina)
"""
import json
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
SRC = ROOT / "results/c1_transfer/c1_transfer_summary.json"
OUT = ROOT / "results/q1/fig_protokol_kumeleri_veri.json"

import hashlib  # noqa: E402

_ham = SRC.read_bytes()
top = json.loads(_ham.decode("utf-8"))
d = top["protocols"]
P = ["raw", "target_correct", "both_correct", "successful_source"]

veri = {"kaynak": str(SRC.relative_to(ROOT)),
        "kaynak_sha256": hashlib.sha256(_ham).hexdigest(),
        "protokoller": {}}
for p in P:
    q = d[p]
    # Hakem (2026-09-29, m6): 'alan yoksa 10000 yaz' sessiz varsayilani
    # karantina deligiydi. Alan yoksa HATA verilir, sayi uydurulmaz.
    veri["protokoller"][p] = {
        "asimetri_ort": round(q["diff"]["mean"], 2),
        "asimetri_sd": round(q["diff"]["std"], 2),
        # tohum-basina degerler: sekil SD cubugu yerine uc noktayi cizebilsin
        # (hakem M1; n=3'te SD cubugu zayif bir ozet)
        "asimetri_tohum_degerleri": [round(v, 2) for v in q["diff"]["values"]],
        "n_CNN_to_ViT": int(round(q["n_cond_CNN_to_ViT"]["mean"])),
        "n_ViT_to_CNN": int(round(q["n_cond_ViT_to_CNN"]["mean"])),
        "CNN_to_ViT": round(q["CNN_to_ViT"]["mean"], 2),
        "ViT_to_CNN": round(q["ViT_to_CNN"]["mean"], 2),
    }

# Ayrisim terimleri HAM ortalamalardan hesaplanir, yuvarlanmislardan DEGIL:
# yuvarlanmis 19,37-13,57 = 5,80 verir, ham deger 5,79'dur ve makale 5,79
# yazar (tur 4'te ayni tuzak duzeltilmisti).
a = {p: d[p]["diff"]["mean"] for p in P}
veri["ayrisim"] = {
    "yayilim": round(max(a.values()) - min(a.values()), 2),
    "ozdeslik_terimi_ham_eksi_hedef_dogru": round(a["raw"] - a["target_correct"], 2),
    "farkli_estimand_bas_kaynak_eksi_ham": round(a["successful_source"] - a["raw"], 2),
    "artik_takdir_her_ikisi_eksi_hedef": round(a["both_correct"] - a["target_correct"], 2),
}
# ic icelik dogrulamasi: n'ler yon basina azalan olmali
n1 = [veri["protokoller"][p]["n_CNN_to_ViT"] for p in P]
n2 = [veri["protokoller"][p]["n_ViT_to_CNN"] for p in P]
veri["ic_icelik_tutuyor"] = (n1 == sorted(n1, reverse=True)) and (n2 == sorted(n2, reverse=True))
if not veri["ic_icelik_tutuyor"]:
    raise SystemExit("KARANTINA: kume ic iceligi bozuk; sekil verisi uretilmedi")

# Hakem (m7): makale "tohum-basina ortalama yayilim" der (protocol_spread_pp),
# sekil ise protokol ORTALAMALARININ farkini basar. Bu veride ikisi cakisir
# (uc tohumda da uclar ayni protokoller); bir sonraki kosuda ayrisirsa
# sekil sessizce yanlis niceligi basmasin.
_tohum_yayilim = round(top["protocol_spread_pp"]["mean"], 2)
if abs(veri["ayrisim"]["yayilim"] - _tohum_yayilim) > 0.005:
    raise SystemExit(f"UYUSMAZLIK: ortalamalarin farki {veri['ayrisim']['yayilim']} "
                     f"!= tohum-basina ortalama yayilim {_tohum_yayilim}; "
                     "sekil metinle ayni niceligi basmaz, uretim durduruldu")
veri["ayrisim"]["tohum_basina_ortalama_yayilim"] = _tohum_yayilim

OUT.write_text(json.dumps(veri, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(veri, indent=2, ensure_ascii=False))
print(f"\nkaydedildi: {OUT}")
