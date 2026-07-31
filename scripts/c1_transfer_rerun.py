"""C1 kontrol noktalariyla transfer analizini (ornek-bazli npz) yeniden uretir.

run_all_analyses_run2.run_transfer_analysis fonksiyonunu, modul duzeyindeki
RUN2_MODELS sozlugunu C1 cifti ile degistirerek her cift icin ayri cikti
dizinine kosar. Istatistik/protokol hesaplari sonra a2_transfer_protocols.py
ile (ayni kod) yapilir.

Kullanim (konteyner icinde):
    python scripts/c1_transfer_rerun.py [--pairs 1 2 3] [--n-samples 10000]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch  # noqa: E402

import experiments.run_all_analyses_run2 as R  # noqa: E402

PAIRS = {
    1: (1001, 2001),
    2: (1002, 2002),
    3: (1003, 2003),
}


def paths(pair):
    rs, vs = PAIRS[pair]
    return {
        "ResNet18_AT": ("resnet18", f"models/c1/resnet18_s{rs}/resnet18/adv/adversarial_training/best.pth"),
        "ViT_Tiny_AT": ("vit_tiny", f"models/c1/vit_tiny_s{vs}/vit_tiny/adv/adversarial_training/best.pth"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--n-samples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    for pair in args.pairs:
        cfg = paths(pair)
        for name, (_, p) in cfg.items():
            if not Path(p).exists():
                raise FileNotFoundError(f"cift {pair}: {name} kontrol noktasi yok: {p}")
        R.RUN2_MODELS.clear()
        R.RUN2_MODELS.update(cfg)
        out_dir = f"results/c1_transfer/pair{pair}"
        print(f"\n########## C1 TRANSFER: cift {pair} -> {out_dir} ##########", flush=True)
        R.set_seed(args.seed)
        R.run_transfer_analysis(device, n_samples=args.n_samples, output_dir=out_dir, seed=args.seed)


if __name__ == "__main__":
    main()
