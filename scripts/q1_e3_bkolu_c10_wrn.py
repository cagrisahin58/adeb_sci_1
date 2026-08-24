#!/usr/bin/env python3
"""E3 B kolu: CIFAR-10'un WRN yonlerini EKLE (dengesizligi giderir).

SORUN. B kolunda WRN iceren TUM ciftler CIFAR-100'den geliyordu; CIFAR-10
yalniz ana cifti (ResNet<->ViT) katiyordu. Boylece "basarili-kaynak protokolu
yayilimi suruyor" bulgusu VERI KUMESIYLE KARISIYOR: butun WRN noktalari tek
bir veri kumesinden.

SEBEP (q1_e3_bkolu.py icinde belgeli): results/c1_c3/pair* dosyalarinda
`source_adv_wrong` ALANI YOK (eski sema; 4fb006a duzeltmesinden onceki
kosum). O alan olmadan basarili-kaynak protokolu hesaplanamiyor.

COZUM. Alan KOSEGENDEN yeniden kurulabilir: src->tgt yonu icin
`source_adv_wrong` = src'nin KENDI cekismeli ornegine yenilmesi
= per_sample_{src}_to_{src}.npz icindeki `target_adv_wrong`.
(Kosegen beyaz kutudur ve AYNI cekismeli ornekleri kullanir.)

ONCE DOGRULANIR: CIFAR-100'de hem acik `source_adv_wrong` hem kosegen var.
Ikisi BAYT-ESIT degilse yeniden kurma YAPILMAZ ve betik durur.

Orijinal npz'ler DEGISTIRILMEZ; yalniz yeni nokta json'lari uretilir.
Cikti: results/q1/e3_points/B_c10_*__WRN_28_10*.json (ve tersi)
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))
from src.analysis import protokoller as PROTO  # noqa: E402


def oranlar(tc, aw, sc, sa):
    """Tanimlar src/analysis/protokoller.py'den (TEK KAYNAK)."""
    return PROTO.protokol_oranlari(tc, aw, sc, sa, tani=True)


def dogrula_kosegen_yeniden_kurma():
    """CIFAR-100'de acik alan ile kosegen BAYT-ESIT mi?"""
    kontrol, uyusmaz = 0, []
    for i in (1, 2, 3):
        d = ROOT / f"results/q1/cifar100/transfer/pair{i}"
        if not d.is_dir():
            continue
        for npz in sorted(d.glob("per_sample_*_to_*.npz")):
            ad = npz.stem[len("per_sample_"):]
            src, tgt = ad.split("_to_")
            if src == tgt:
                continue
            z = np.load(npz)
            if "source_adv_wrong" not in z.files:
                continue
            kos = d / f"per_sample_{src}_to_{src}.npz"
            if not kos.exists():
                continue
            acik = z["source_adv_wrong"].astype(bool)
            kosegen = np.load(kos)["target_adv_wrong"].astype(bool)
            kontrol += 1
            if not np.array_equal(acik, kosegen):
                uyusmaz.append(f"{d.name}/{ad}: {int((acik != kosegen).sum())} ornek farkli")
    return kontrol, uyusmaz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(ROOT / "results/q1/e3_points"))
    args = ap.parse_args()

    print("=== 1) KOSEGEN YENIDEN KURMA DOGRULAMASI (CIFAR-100) ===")
    n, uyusmaz = dogrula_kosegen_yeniden_kurma()
    if n == 0:
        sys.exit("HATA: dogrulama yapilamadi (acik alanli yon bulunamadi)")
    if uyusmaz:
        print(f"  UYUSMAZLIK ({len(uyusmaz)}):")
        for u in uyusmaz[:5]:
            print("   ", u)
        sys.exit("DURDURULDU: kosegen yeniden kurma GECERSIZ; nokta uretilmedi.")
    print(f"  GECTI: {n}/{n} yonde acik alan ile kosegen BAYT-ESIT.")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== 2) CIFAR-10 3x3'ten WRN yonleri uretiliyor ===")
    uretilen, atlanan = 0, []
    for i in (1, 2, 3):
        d = ROOT / f"results/c1_c3/pair{i}"
        if not d.is_dir():
            atlanan.append(f"{d} yok")
            continue
        for npz in sorted(d.glob("per_sample_*_to_*.npz")):
            ad = npz.stem[len("per_sample_"):]
            src, tgt = ad.split("_to_")
            if src == tgt:
                continue
            # ANA CIFT ZATEN VAR (c1_transfer'dan) -> cift sayma
            if "WRN_28_10" not in (src, tgt):
                continue
            z = np.load(npz)
            kos = d / f"per_sample_{src}_to_{src}.npz"
            if not kos.exists():
                atlanan.append(f"{d.name}/{ad}: kosegen yok")
                continue
            tc = z["target_clean_correct"].astype(bool)
            aw = z["target_adv_wrong"].astype(bool)
            sc = z["source_clean_correct"].astype(bool)
            sa = np.load(kos)["target_adv_wrong"].astype(bool)   # yeniden kuruldu

            o = oranlar(tc, aw, sc, sa)
            e = float(100 * (1 - tc.mean()))
            ham_tahmin = e + o["target_correct"] * (1 - e / 100.0)
            nokta = {
                "trajectory_id": f"B_c10_{tgt}",
                "arm": "B",
                "secim_kipi": "final-model (gozlemsel)",
                "stride": None, "epoch": None,
                "kaynak_dizin": str(d.relative_to(ROOT)),
                "yon": f"{src}->{tgt}",
                "dataset": "c10",
                "n": int(tc.size),
                "source_adv_wrong_KAYNAGI": "KOSEGENDEN YENIDEN KURULDU "
                                            f"(per_sample_{src}_to_{src}.npz/target_adv_wrong); "
                                            "yontem CIFAR-100'de bayt-esit dogrulandi",
                "target_clean_acc": float(100 * tc.mean()),
                "target_clean_err": e,
                "source_archive": str(npz.relative_to(ROOT)),
                "ozdeslik_ham_tahmin": ham_tahmin,
                "ozdeslik_artik": o["raw"] - ham_tahmin,
                **o,
                "raw_minus_cond": o["raw"] - o["target_correct"],
                "spread": max(o.values()) - min(o.values()),
            }
            f = out_dir / f"B_c10_{tgt}__pair{i}__{src}.json"
            f.write_text(json.dumps(nokta, indent=1, ensure_ascii=False), encoding="utf-8")
            uretilen += 1
            print(f"  {f.name:44s} e={e:5.2f}  yayilim={nokta['spread']:6.2f}  "
                  f"ozdeslik_artik={nokta['ozdeslik_artik']:+.3f}")

    print(f"\nuretilen nokta: {uretilen}")
    if atlanan:
        print("atlanan:", atlanan[:5])


if __name__ == "__main__":
    main()
