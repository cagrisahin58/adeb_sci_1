"""C1 kontrol noktalariyla gradyan ve blok bazli oznitelik kaymasi analizleri.

Transfer icin scripts/c1_transfer_rerun.py kullanilir; bu betik kalan iki
davranissal analizi her tohum cifti icin yeniden uretir.

Kullanim (konteyner icinde):
    python scripts/c1_analyses_rerun.py --only gradient --pairs 1 2 3
    python scripts/c1_analyses_rerun.py --only drift --pairs 1 2 3
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch  # noqa: E402

import experiments.run_all_analyses_run2 as R  # noqa: E402
from scripts.c1_transfer_rerun import paths  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["gradient", "drift", "all"], default="all")
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
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

        if args.only in ("gradient", "all"):
            print(f"\n########## C1 GRADYAN: cift {pair} ##########", flush=True)
            R.set_seed(args.seed)
            R.run_gradient_analysis(device, seed=args.seed, output_dir=f"results/c1_gradient/pair{pair}")

        if args.only in ("drift", "all"):
            print(f"\n########## C1 KAYMA: cift {pair} ##########", flush=True)
            R.set_seed(args.seed)
            R.run_feature_degradation_analysis(device, seed=args.seed, output_dir=f"results/c1_drift/pair{pair}")


if __name__ == "__main__":
    main()
