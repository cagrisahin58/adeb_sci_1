#!/usr/bin/env python3
"""E3 B KOLU (gozlemsel) nokta uretimi -- GPU GEREKTIRMEZ.

A kolu (kontrollu) yorunge checkpointlerini degerlendirmek icin GPU ister.
B kolu ise FINAL modellerden gelir ve gereken her sey ZATEN diskte: transfer
analizlerinin ornek-bazli maskeleri (per_sample_*.npz). Bu betik onlardan
E3 nokta json'lari uretir.

Her kosegen-disi yon bir NOKTA verir:
    x = hedefin temiz hatasi
    y = dort protokolun urettigi YAYILIM   (BIRINCIL, EK B)
    ek = ham-kosullu sapmasi + ozdeslik artigi (IKINCIL/saglama)

KUMELEME: B kolunda "yorunge" yoktur; her nokta ayri bir final modeldir.
Kume = veri kumesi x HEDEF mimarisi. Ayni hedef iki farkli kaynaktan iki kez
puanlandigi icin o iki nokta BAGIMSIZ DEGILDIR ve ayni kumeye girmelidir --
kume bootstrap'in serbestlik derecesini bu belirler.

Kullanim: python scripts/q1_e3_bkolu.py --out-dir results/q1/e3_points
"""
import argparse
import json
from pathlib import Path

import sys

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))
from src.analysis import protokoller as PROTO  # noqa: E402

# (etiket, dizin listesi)
# DIKKAT -- CIFAR-10 icin DOGRU DIZIN c1_transfer'dir, c1_c3 DEGIL:
#   results/c1_c3/pair*   (3x3 matris, WRN dahil)  -> source_adv_wrong ALANI YOK
#     Bu artefaktlar 4fb006a sema duzeltmesinden ONCE uretildi ve yalniz ham +
#     hedef-dogru oranini destekler. Makale de zaten 3x3 tablosunda yalniz
#     Raw/Cond. veriyor, yani METINDE HATA YOK; ama 4-PROTOKOL YAYILIMI bu
#     dosyalardan HESAPLANAMAZ. Yeniden uretmek GPU ister (transfer matrisi).
#     Sonuc: CIFAR-10'da WRN hedefi B koluna KATILAMIYOR; bu bir sinirlamadir
#     ve sessizce gecilmez (asagida ATLANAN listesinde gorunur).
#   results/c1_transfer/pair* (2x2, dort protokol analizi) -> sema TAM
KAYNAKLAR = [
    ("c10", [ROOT / f"results/c1_transfer/pair{i}" for i in (1, 2, 3)]),
    ("c100", [ROOT / f"results/q1/cifar100/transfer/pair{i}" for i in (1, 2, 3)]),
    ("svhn", [ROOT / f"results/q1/svhn/transfer/pair{i}" for i in (1, 2)]),
    # asagidaki YALNIZ raporlama icin: eksik semali oldugu ATLANAN'da gorunsun
    ("c10_3x3_EKSIK_SEMA", [ROOT / f"results/c1_c3/pair{i}" for i in (1, 2, 3)]),
]


def protocol_rates(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong):
    """Tanimlar src/analysis/protokoller.py'den (TEK KAYNAK)."""
    r = PROTO.protokol_oranlari(clean_ok, adv_wrong, src_clean_ok, src_adv_wrong,
                                tani=True)
    r["raw_minus_cond"] = r["raw"] - r["target_correct"]
    r["spread"] = PROTO.yayilim(r)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(ROOT / "results/q1/e3_points"))
    args = ap.parse_args()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    yazilan, atlanan = 0, []
    for kume_etiketi, dizinler in KAYNAKLAR:
        for d in dizinler:
            if not d.is_dir():
                atlanan.append(f"{d} (dizin yok)")
                continue
            for npz in sorted(d.glob("per_sample_*_to_*.npz")):
                ad = npz.stem[len("per_sample_"):]
                src, tgt = ad.split("_to_")
                if src == tgt:
                    continue                       # kosegen = beyaz kutu
                z = np.load(npz)
                gerekli = {"target_clean_correct", "target_adv_wrong",
                           "source_clean_correct", "source_adv_wrong"}
                if not gerekli.issubset(set(z.files)):
                    atlanan.append(f"{npz.name} (eksik alan: {gerekli - set(z.files)})")
                    continue
                tc = z["target_clean_correct"].astype(bool)
                aw = z["target_adv_wrong"].astype(bool)
                sc = z["source_clean_correct"].astype(bool)
                sa = z["source_adv_wrong"].astype(bool)
                r = protocol_rates(tc, aw, sc, sa)
                e = float(100 * (1 - tc.mean()))
                ham_tahmin = e + r["target_correct"] * (1 - e / 100.0)

                # KUME: veri kumesi x HEDEF mimarisi (ayni hedef iki kaynaktan
                # puanlaniyor -> o iki nokta bagimsiz DEGIL, ayni kumede)
                tid = f"B_{kume_etiketi}_{tgt}"
                nokta = {
                    "trajectory_id": tid,
                    "arm": "B",
                    "secim_kipi": "final-model (gozlemsel)",
                    "stride": None,
                    "epoch": None,
                    "kaynak_dizin": str(d.relative_to(ROOT)),
                    "yon": f"{src}->{tgt}",
                    "dataset": kume_etiketi,
                    "n": int(tc.size),
                    "target_clean_acc": float(100 * tc.mean()),
                    "target_clean_err": e,
                    "source_archive": str(npz.relative_to(ROOT)),
                    "ozdeslik_ham_tahmin": ham_tahmin,
                    "ozdeslik_artik": r["raw"] - ham_tahmin,
                    **r,
                }
                fname = out_dir / f"{tid}__{d.name}__{src}.json"
                fname.write_text(json.dumps(nokta, indent=1, ensure_ascii=False),
                                 encoding="utf-8")
                yazilan += 1

    kumeler = sorted({p.stem.split("__")[0] for p in out_dir.glob("B_*.json")})
    print(f"B KOLU: {yazilan} nokta yazildi -> {out_dir}")
    print(f"  kume sayisi (kume bootstrap serbestlik derecesi): {len(kumeler)}")
    for k in kumeler:
        n = len(list(out_dir.glob(f"{k}__*.json")))
        print(f"    {k:34s} {n} nokta")
    if atlanan:
        print(f"  ATLANAN ({len(atlanan)}) -- sessiz gecilmedi:")
        for a in atlanan[:10]:
            print(f"    {a}")
    if len(kumeler) < 3:
        print("  UYARI: kume sayisi 3'ten az; kume bootstrap GA'lari cok genis")
        print("  veya dejenere cikar. Bu bir kusur degil, gozlemsel kolun")
        print("  kucuk model havuzunun dogal sonucudur ve RAPORLANMALIDIR.")


if __name__ == "__main__":
    main()
