# -*- coding: utf-8 -*-
"""Curutme B kod degisikligi icin regresyon duzenegi (08.11.2026).

Amac: cli/train.py ve src/training/trainer.py'ye eklenen temiz asama bayraklari
VERILMEDIGINDE egitimin eski kodla birebir ayni oldugunu gostermek. Ayni komut iki kod
kokunden (eski: `git archive HEAD cli src` ile ayri dizine cikarilmis surum; yeni:
calisma agaci) ayni tohumla kosulur ve her `Tensor.backward()` cagrisindaki skaler kayip
(ilk 50 egitim iterasyonu; AT kipinde PGD icindeki geri yayilimlar da dahil) dosyaya yazilir.
Test edilen kod degistirilmez: kayit, torch.Tensor.backward sarmalanarak alinir.

Kullanim (konteyner, /workspace):
  python scripts/curutme_regresyon.py --kok <kod_koku> --durum <clean_vit|clean_r224in|at_r224scr> \\
      --cikti <kayip.txt> --is-dizini <gecici_cikti_dizini>
"""
import argparse
import os
import sys

DURUMLAR = {
    # C1 V-scr temiz komutu (scripts/run_c1_pipeline.sh:58-60), -e 1 ve 50 batch ile
    "clean_vit": ["clean", "-m", "vit_tiny", "-e", "1", "--lr", "0.001", "-b", "128",
                  "--seed", "2001", "--max-train-batches", "50"],
    # B3 V-IN temiz komutu (logs/konsey_zincir.log:36), ImageNet baslatma yolu dahil
    "clean_vin": ["clean", "-m", "vit_tiny_in1k", "--init-weights", "deit_tiny_in1k",
                  "--optimizer", "adamw", "--lr-schedule", "cosine", "-e", "1", "--lr", "0.0001",
                  "-b", "128", "--seed", "2101", "--max-train-batches", "50"],
    # B3 R224-scr AT komutu (logs/konsey_zincir.log:57), --stop-epoch 1 ve 50 batch ile
    "at_r224scr": ["adversarial", "-m", "resnet18_224", "-d", "adversarial_training",
                   "-p", "/workspace/models/q1/konsey/R224_scr_s1201/resnet18_224/clean/best.pth",
                   "--optimizer", "adamw", "-e", "100", "--stop-epoch", "1", "--lr", "0.001",
                   "-b", "64", "--patience", "20", "--seed", "1201", "--max-train-batches", "50"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kok", required=True)
    ap.add_argument("--durum", required=True, choices=sorted(DURUMLAR))
    ap.add_argument("--cikti", required=True)
    ap.add_argument("--is-dizini", required=True)
    ap.add_argument("--n-iter", type=int, default=50)
    ap.add_argument("--cihaz", default="auto", help="auto | cuda | cpu (CPU bit duzeyinde belirlenimli)")
    ap.add_argument("--belirlenimli", action="store_true",
                    help="GPU'da belirlenimli kip: CUBLAS_WORKSPACE_CONFIG=:4096:8, "
                         "torch.use_deterministic_algorithms(True, warn_only=True), flash ve "
                         "mem-efficient SDPA kapali (test edilen kod degismez, ayar sarmalayicidadir)")
    a = ap.parse_args()
    if a.belirlenimli:
        os.environ.setdefault("CUBLAS_WORKSPACE_CONFIG", ":4096:8")

    kok = os.path.abspath(a.kok)
    sys.path.insert(0, kok)
    os.chdir(kok)
    import torch

    if a.belirlenimli:
        torch.use_deterministic_algorithms(True, warn_only=True)
        torch.backends.cuda.enable_flash_sdp(False)
        torch.backends.cuda.enable_mem_efficient_sdp(False)
        torch.backends.cuda.enable_math_sdp(True)

    kayit = []
    _ozgun = torch.Tensor.backward

    def _sar(self, *args, **kw):
        if self.dim() == 0:
            kayit.append(float(self.detach().item()))
        return _ozgun(self, *args, **kw)

    torch.Tensor.backward = _sar
    from cli.train import train  # noqa: E402

    argv = list(DURUMLAR[a.durum]) + ["--data-dir", "/workspace/data",
                                      "--val-indices", "/workspace/data/val_split_indices.json",
                                      "-o", a.is_dizini, "--device", a.cihaz]
    try:
        train.main(args=argv, standalone_mode=False)
    finally:
        torch.Tensor.backward = _ozgun
    os.makedirs(os.path.dirname(os.path.abspath(a.cikti)), exist_ok=True)
    with open(a.cikti, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"# kok={kok} durum={a.durum} argv={' '.join(argv)}\n")
        fh.write(f"# backward_cagri_sayisi={len(kayit)}\n")
        for i, v in enumerate(kayit):
            fh.write(f"{i}\t{v!r}\n")
    print(f"yazildi {a.cikti} ({len(kayit)} kayip)")


if __name__ == "__main__":
    main()
