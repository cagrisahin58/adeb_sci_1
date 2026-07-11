#!/usr/bin/env python3
"""Local evaluation of the WRN-28-10 RobustBench baseline (M14).

Makale Tablo 1'deki WRN-28-10 satirinin yerel bir artefakti yoktu ve 66.05
degeri RobustBench'in PGD-20 sayisiyken PGD-10 sutununda raporlaniyordu.
Bu script ayni modeli yerel olarak degerlendirir:
  - Clean, FGSM, PGD-10 (eps=8/255, alpha=2/255) tam test setinde
  - PGD-10 epsilon taramasi (2/255, 4/255, 8/255, 16/255) fig2 icin
  - Ornek-bazli gosterge vektorleri (esli testler icin)

RobustBench modelleri [0,1] girdiler bekler (normalizasyon model icinde),
proje loader'lari ve saldirilariyla uyumludur.

Usage:
    python experiments/run_wrn_eval.py [--n-samples 10000] [--seed 42]
"""

import argparse
import random
import json
import gc
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import torch

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data import get_cifar10_loaders
from src.attacks import FGSMAttack, PGDAttack

MODEL_NAME = "Gowal2020Uncovering_28_10_extra"
EPS_MAIN = 8 / 255
ALPHA = 2 / 255
STEPS = 10
EPS_SWEEP = [2 / 255, 4 / 255, 8 / 255, 16 / 255]


def set_seed(seed):
    """Full seeding for reproducibility (M15)."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load_wrn(device):
    """Load the WRN-28-10 model via the robustbench package.

    src/models altinda WideResNet mimarisi bulunmadigindan yerel .pth dogrudan
    yuklenemez; robustbench paketi mimariyi getirir ve agirliklari indirir /
    cache'ten okur (models/robustbench_zoo).
    """
    from robustbench.utils import load_model
    model = load_model(
        model_name=MODEL_NAME,
        dataset="cifar10",
        threat_model="Linf",
        model_dir="models/robustbench_zoo",
    )
    return model.to(device).eval()


@torch.no_grad()
def predict(model, images):
    return model(images).argmax(1)


def evaluate(model, test_loader, device, n_samples, seed):
    """Clean + FGSM + PGD(eps sweep) evaluation with per-sample logging."""
    results = {}
    per_sample = {}

    attacks = {"fgsm": FGSMAttack(model, eps=EPS_MAIN)}
    for eps in EPS_SWEEP:
        attacks[f"pgd10_eps{eps:.5f}"] = PGDAttack(model, eps=eps, alpha=ALPHA, steps=STEPS)

    indicator = {key: [] for key in ["clean"] + list(attacks.keys())}
    total = 0

    for images, labels in test_loader:
        if total >= n_samples:
            break
        if total + labels.size(0) > n_samples:
            keep = n_samples - total
            images, labels = images[:keep], labels[:keep]

        images, labels = images.to(device), labels.to(device)

        indicator["clean"].append((predict(model, images) == labels).cpu().numpy())

        for key, attack in attacks.items():
            adv = attack(images, labels)
            indicator[key].append((predict(model, adv) == labels).cpu().numpy())

        total += labels.size(0)
        if total % 1000 == 0:
            print(f"  {total}/{n_samples} samples")

    for key, chunks in indicator.items():
        vec = np.concatenate(chunks)
        per_sample[key] = vec
        results[key] = {
            "accuracy": float(100 * vec.mean()),
            "correct": int(vec.sum()),
            "n": int(len(vec)),
        }
        print(f"  {key}: {results[key]['accuracy']:.2f}%")

    return results, per_sample


def main():
    parser = argparse.ArgumentParser(description="WRN-28-10 RobustBench local evaluation")
    parser.add_argument("--n-samples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--output-dir", type=str, default="results/wrn_eval")
    args = parser.parse_args()

    set_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}, seed: {args.seed}, n_samples: {args.n_samples}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nLoading {MODEL_NAME} via robustbench...")
    model = load_wrn(device)

    print("\nLoading CIFAR-10 test set...")
    _, test_loader = get_cifar10_loaders(data_dir="./data", test_batch_size=args.batch_size)

    print("\nEvaluating (clean + FGSM + PGD-10 epsilon sweep)...")
    results, per_sample = evaluate(model, test_loader, device, args.n_samples, args.seed)

    np.savez(output_dir / "per_sample_WRN28_10.npz", **per_sample)

    summary = {
        "timestamp": datetime.now().isoformat(),
        "model": MODEL_NAME,
        "source": "robustbench (local evaluation)",
        "eps_main": EPS_MAIN,
        "alpha": ALPHA,
        "pgd_steps": STEPS,
        "eps_sweep": EPS_SWEEP,
        "n_samples": args.n_samples,
        "seed": args.seed,
        "results": results,
    }
    with open(output_dir / "wrn_eval_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    rows = [{"metric": k, **v} for k, v in results.items()]
    pd.DataFrame(rows).to_csv(output_dir / "wrn_eval_results.csv", index=False)

    print(f"\nSaved to {output_dir}")

    del model
    gc.collect()
    torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
