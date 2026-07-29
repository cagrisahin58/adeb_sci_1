"""rev2 C1: tek checkpoint icin full-test clean + PGD-10 per-sample degerlendirme.

Kullanim (container icinde):
  python scripts/c1_pgd_eval.py --model-type resnet18 --ckpt <path> --out <dir> [--tag <ad>]
Cikti: <out>/pgd_per_sample_<tag>.npz + <out>/pgd_summary_<tag>.json
"""
import argparse
import json
import os
import sys

import numpy as np
import torch

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from src.attacks.pgd import PGDAttack  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-type", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default=None)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    tag = args.tag or args.model_type

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    np.random.seed(args.seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = ModelRegistry.get(args.model_type)
    load_model_weights(model, args.ckpt, device)
    model = model.to(device).eval()
    attack = PGDAttack(model, eps=8 / 255, alpha=2 / 255, steps=10)

    _, test_loader = get_cifar10_loaders(data_dir="./data", test_batch_size=100)
    clean_ok, robust_ok = [], []
    n = 0
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        with torch.no_grad():
            clean_pred = model(images).argmax(1)
        adv = attack.attack(images, labels)
        with torch.no_grad():
            adv_pred = model(adv).argmax(1)
        clean_ok.append((clean_pred == labels).cpu().numpy())
        robust_ok.append((adv_pred == labels).cpu().numpy())
        n += labels.size(0)
        if n % 2000 == 0:
            print(f"  {n}/10000")
    clean_ok = np.concatenate(clean_ok)
    robust_ok = np.concatenate(robust_ok)

    os.makedirs(args.out, exist_ok=True)
    np.savez_compressed(os.path.join(args.out, f"pgd_per_sample_{tag}.npz"),
                        clean_correct=clean_ok, robust_correct=robust_ok)
    summary = {
        "model_type": args.model_type,
        "ckpt": args.ckpt,
        "seed": args.seed,
        "n": int(n),
        "attack": "PGD-10 eps=8/255 alpha=2/255",
        "clean_acc": round(float(clean_ok.mean() * 100), 2),
        "pgd10_acc": round(float(robust_ok.mean() * 100), 2),
    }
    with open(os.path.join(args.out, f"pgd_summary_{tag}.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
