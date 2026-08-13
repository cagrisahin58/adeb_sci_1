"""Ortak sabit validasyon bolmesi uret (leak fix; dataset-parametrik).

Egitim setinden VAL_SIZE indekslik SABIT validasyon kumesi. Egitim
seed'lerinden bagimsizdir (split seed tek seferlik); ayni dosya hem clean
pretraining hem adversarial fine-tuning tarafindan kullanilir, boylece
validasyon ornekleri hicbir egitim asamasinda gorulmez.

Q1 genellemesi: --dataset ile CIFAR-100 (n=50000) ve SVHN (n=73257) icin
AYRI indeks dosyalari uretilir; dosyaya "dataset" alani yazilir ve
get_loaders_with_val yanlis kumeyle kullanildiginda hata verir.

Kullanim:
    python experiments/rev2/make_val_split.py                     # cifar10 (eski davranis)
    python experiments/rev2/make_val_split.py --dataset cifar100
    python experiments/rev2/make_val_split.py --dataset svhn
Cikti: data/val_split_indices.json (cifar10, geriye uyum) veya
       data/val_split_indices_<dataset>.json
"""
import argparse
import json
import os
import sys

import torch

ROOT = "/workspace" if os.path.isdir("/workspace/results") else os.path.expanduser("~/projects/adeb_sci_1")
sys.path.insert(0, ROOT)

from src.data import DATASETS  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--val-size", type=int, default=2000)
    ap.add_argument("--split-seed", type=int, default=777)
    ap.add_argument("--out", type=str, default=None,
                    help="Cikti yolu (varsayilan: data/val_split_indices[_<dataset>].json)")
    args = ap.parse_args()

    n_train = DATASETS[args.dataset]["n_train"]
    if args.out:
        out = args.out
    elif args.dataset == "cifar10":
        out = os.path.join(ROOT, "data/val_split_indices.json")  # geriye uyum (C1)
    else:
        out = os.path.join(ROOT, f"data/val_split_indices_{args.dataset}.json")

    if os.path.exists(out):
        with open(out) as f:
            existing = json.load(f)
        print(f"ZATEN VAR: {out} (dataset={existing.get('dataset', 'cifar10')}, "
              f"split_seed={existing.get('split_seed')}, "
              f"n={len(existing['val_indices'])}) — degistirilmedi (idempotent)")
        return

    generator = torch.Generator().manual_seed(args.split_seed)
    perm = torch.randperm(n_train, generator=generator).tolist()
    val_indices = sorted(perm[:args.val_size])

    payload = {
        "dataset": args.dataset,
        "split_seed": args.split_seed,
        "n_train_total": n_train,
        "val_size": args.val_size,
        "note": "Ortak sabit val bolmesi; clean pretraining VE adversarial "
                "fine-tuning bu ornekleri egitimden cikarir (leak fix). Egitim "
                "seed'lerinden bagimsizdir.",
        "val_indices": val_indices,
    }
    with open(out, "w") as f:
        json.dump(payload, f)
    print(f"yazildi: {out} ({args.val_size} indeks, dataset={args.dataset}, "
          f"n_train={n_train}, split_seed={args.split_seed})")


if __name__ == "__main__":
    main()
