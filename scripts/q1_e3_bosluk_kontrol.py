#!/usr/bin/env python3
"""IS-6(g): E3 x-ekseni BOSLUK kontrolu.

E3_YENIDEN_TASARIM.md §2 iki bosluk olcmustu:
  · %12'nin ALTI    -> tamamen bos (E7/SVHN kapatacak)
  · %19,4-23,5      -> ResNet ile ViT yorungeleri arasindaki KOPUKLUK
                       ("E1'in CIFAR-100 noktalariyla kapanmasi BEKLENIYOR")

Bu betik o BEKLENTIYI sinar ve ekseni bastan tarayarak TUM bosluklari bulur.
Beklenti yanlissa oyle raporlanir (K8).

Girdi (mevcut, dogrulanmis artefaktlar):
  results/q1/e3_coverage.json        -- yorunge basina temiz hata araliklari
  results/q1/e1_cifar100_summary.json-- CIFAR-100 final test temiz dogruluklari
Cikti: results/q1/e3_bosluk_kontrol.json
"""
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
BOSLUK = (19.38, 23.47)   # E3_YENIDEN_TASARIM §2'nin adiyla andigi kopukluk


def jl(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))


cov = jl("results/q1/e3_coverage.json")
e1 = jl("results/q1/e1_cifar100_summary.json")

# --- 1. Mevcut yorungelerin kapladigi araliklar (E2/CIFAR-10 + CIFAR-100) ---
araliklar = []
for y in cov["yorungeler"]:
    lo, hi = y["temiz_hata_araligi"]
    araliklar.append({"kaynak": y["yorunge"].split("/")[2] + "/" + y["yorunge"].split("/")[3],
                      "alt": lo, "ust": hi, "n_ckpt": y["n_checkpoint"]})

# --- 2. CIFAR-100 final noktalari (gercek TEST, n=3) ---
c100_final = {}
for arch in ("resnet18", "vit_tiny"):
    vals = e1["mimariler"][arch]["ozet"]["test_clean"]["degerler"]
    c100_final[arch] = {"temiz_dogruluk": vals, "temiz_hata": [round(100 - v, 2) for v in vals]}
c100_hatalar = sorted(h for a in c100_final.values() for h in a["temiz_hata"])


# --- 3. Ekseni tara: birlesim disinda kalan bosluklar ---
def birlestir(ivs):
    if not ivs:
        return []
    ivs = sorted(ivs)
    out = [list(ivs[0])]
    for a, b in ivs[1:]:
        if a <= out[-1][1] + 1e-9:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


kapsanan = birlestir([(a["alt"], a["ust"]) for a in araliklar])
bosluklar = []
for i in range(len(kapsanan) - 1):
    g_lo, g_hi = kapsanan[i][1], kapsanan[i + 1][0]
    if g_hi - g_lo > 0.5:                       # 0,5 puandan kucuk kopukluk sayilmaz
        bosluklar.append({"alt": round(g_lo, 2), "ust": round(g_hi, 2),
                          "genislik": round(g_hi - g_lo, 2)})

lo, hi = BOSLUK
# DIKKAT: "bir yorunge boslukla kesisiyor mu" SORUSU FAZLA GEVSEKTIR --
# boslugun ucuna 0,2 puan degen yorunge de kesisir gorunur. Dogru olcum,
# on-kayitli boslugun YUZDE KACININ kapsandigidir.
_kesisim = 0.0
for _seg in kapsanan:
    _a, _b = max(_seg[0], lo), min(_seg[1], hi)
    if _b > _a:
        _kesisim += _b - _a
kapsanan_oran = round(100.0 * _kesisim / (hi - lo), 1)
kesisen = [a["kaynak"] for a in araliklar if a["alt"] < hi and a["ust"] > lo]
final_bosluga_giren = [h for h in c100_hatalar if lo < h < hi]


def git_sha():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception:
        return None


# Kapanma olcutu: on-kayitli boslugun en az %50si kapsanmis olmali.
kapatildi = kapsanan_oran >= 50.0
sonuc = {
    "uretildi_utc": datetime.now(timezone.utc).isoformat(),
    "git": git_sha(),
    "soru": "E3_YENIDEN_TASARIM §2'nin %19,4-23,5 boslugunu E1 (CIFAR-100) kapatti mi?",
    "bosluk_temiz_hata": {"alt": lo, "ust": hi},
    "yorunge_kapsamasi_birlesim": [[round(a, 2), round(b, 2)] for a, b in kapsanan],
    "OLCULEN_TUM_BOSLUKLAR": bosluklar,
    "cifar100_final_temiz_hata": c100_final,
    "cifar100_final_hata_araligi": [c100_hatalar[0], c100_hatalar[-1]],
    "kaynak_araliklar": araliklar,
    "HUKUM": {
        "bosluk_kapandi_mi": kapatildi,
        "on_kayitli_bosluk_kapsanan_yuzde": kapsanan_oran,
        "bosluga_giren_final_nokta": final_bosluga_giren,
        "boslugun_ucuna_DEGEN_yorunge": kesisen,
        "NOT": "degen yorunge kapsama demek DEGILDIR; olcut kapsanan yuzdedir",
    },
}
sonuc["HUKUM"]["yorum"] = (
    f"BEKLENTI KISMEN KARSILANDI: on-kayitli boslugun %{kapsanan_oran}i kapsaniyor."
    if kapatildi else
    f"BEKLENTI KARSILANMADI (on-kayitli boslugun yalnizca %{kapsanan_oran}i kapsaniyor). "
    "CIFAR-100 modelleri boslugun COK UZERINDE bir hata "
    f"bolgesinde ({c100_hatalar[0]}-{c100_hatalar[-1]}%) yasiyor; %19,4-23,5 araligi "
    "E1'den SONRA DA BOS. E3'un bu bolgedeki egimi hicbir noktayla desteklenmiyor; "
    "regresyon orada INTERPOLASYONDUR ve E3 raporlanirken YAZILMALIDIR (K8). "
    "Boslugu kapatabilecek tek planli kalem E5'tir (R50/ViT-S, ERTELENDI). "
    "NOT: E7 (SVHN) ALT ucu doldurur, bu ORTA boslugu DOLDURMAZ."
)

out = ROOT / "results/q1/e3_bosluk_kontrol.json"
out.write_text(json.dumps(sonuc, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"On-kayitli bosluk       : %{lo}-{hi}")
print(f"Yorunge kapsamasi       : {sonuc['yorunge_kapsamasi_birlesim']}")
print(f"OLCULEN TUM BOSLUKLAR   : {bosluklar or 'yok'}")
print(f"CIFAR-100 final hatalar : {c100_hatalar}")
print(f"  bosluga giren nokta   : {final_bosluga_giren or 'YOK'}")
print(f"  boslugun ucuna degen  : {kesisen or 'YOK'}  (kapsama DEGIL)")
print(f"  on-kayitli bosluktan kapsanan: %{kapsanan_oran}")
print()
print("HUKUM:", sonuc["HUKUM"]["yorum"])
print(f"-> {out}")
