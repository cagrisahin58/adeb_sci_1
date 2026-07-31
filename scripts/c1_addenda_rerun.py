"""C1 kontrol noktalariyla c_addenda analizleri (C20/C21/C22).

C20: ResNet-18 AT blok bazli oznitelik kaymasi (Sekil B3'un CNN egrisi)
C21: temiz egitilmis modellerde gradyan seyreklik/hizalanma (AT'nin siralamayi
     tersine cevirdigi iddiasi)  -- C1 clean kontrol noktalariyla
C22: MI-FGSM kosullu transfer (momentum altinda kararlilik iddiasi)

Kullanim (konteyner icinde):
    python scripts/c1_addenda_rerun.py --pairs 1 2 3
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch  # noqa: E402

import experiments.run_c_addenda as A  # noqa: E402

PAIRS = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}


def at_models(pair):
    rs, vs = PAIRS[pair]
    return {
        "ResNet18_AT": ("resnet18", f"models/c1/resnet18_s{rs}/resnet18/adv/adversarial_training/best.pth"),
        "ViT_Tiny_AT": ("vit_tiny", f"models/c1/vit_tiny_s{vs}/vit_tiny/adv/adversarial_training/best.pth"),
    }


def clean_models(pair):
    rs, vs = PAIRS[pair]
    return {
        "ResNet18_clean": ("resnet18", f"models/c1/resnet18_s{rs}/resnet18/clean/best.pth"),
        "ViT_Tiny_clean": ("vit_tiny", f"models/c1/vit_tiny_s{vs}/vit_tiny/clean/best.pth"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--steps", nargs="+", default=["c20", "c21", "c22"])
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for pair in args.pairs:
        A.AT_MODELS.clear()
        A.AT_MODELS.update(at_models(pair))
        cm = clean_models(pair)
        missing = [p for _, (_, p) in cm.items() if not Path(p).exists()]
        if missing:
            print(f"UYARI: cift {pair} temiz kontrol noktalari yok, C21 atlaniyor: {missing}")
        else:
            A.CLEAN_MODELS.clear()
            A.CLEAN_MODELS.update(cm)
        A.OUT = Path(f"results/c1_addenda/pair{pair}")
        A.OUT.mkdir(parents=True, exist_ok=True)
        print(f"\n########## C1 ADDENDA: cift {pair} -> {A.OUT} ##########", flush=True)
        if "c21" in args.steps and not missing:
            A.run_c21(device)
        if "c20" in args.steps:
            A.run_c20(device)
        if "c22" in args.steps:
            A.run_c22(device)


if __name__ == "__main__":
    main()
