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


def _targets(dataset, root):
    """Egitim kumesinin etiket dizisi (donusum kurulmadan, hizli)."""
    import torchvision.datasets as tvd
    cls = getattr(tvd, DATASETS[dataset]["cls"])
    if dataset == "svhn":
        ds = cls(root=root, split="train", download=False)
        return list(ds.labels)
    ds = cls(root=root, train=True, download=False)
    return list(ds.targets)


def _stratified_indices(dataset, n_train, val_size, generator):
    """Sinif-dengeli val indeksleri: her siniftan val_size/n_class ornek.

    Rastgele bolme 100 sinifli CIFAR-100'de sinif basina 7-35 ornek birakip
    secim metrigini asiri gurultulu yapiyordu; bu, seciciyi (ve dolayisiyla
    raporlanan gurbuzlugu) veri kumesi sinif sayisina bagimli kiliyor.
    """
    import collections
    root = os.path.join(ROOT, "data")
    tg = _targets(dataset, root)
    assert len(tg) == n_train, f"etiket sayisi {len(tg)} != {n_train}"
    by_cls = collections.defaultdict(list)
    for i, y in enumerate(tg):
        by_cls[int(y)].append(i)
    n_cls = len(by_cls)
    base, extra = divmod(val_size, n_cls)
    # Kalan pay, deterministik bir sinif permutasyonuyla dagitilir
    cls_order = [sorted(by_cls)[i] for i in
                 torch.randperm(n_cls, generator=generator).tolist()]
    picked = []
    for k, c in enumerate(cls_order):
        take = base + (1 if k < extra else 0)
        idx = by_cls[c]
        sel = torch.randperm(len(idx), generator=generator)[:take].tolist()
        picked.extend(idx[j] for j in sel)
    counts = collections.Counter(int(tg[i]) for i in picked)
    return sorted(picked), {"n_class": n_cls, "min": min(counts.values()),
                            "max": max(counts.values())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--val-size", type=int, default=2000)
    ap.add_argument("--split-seed", type=int, default=777)
    ap.add_argument("--stratified", action="store_true",
                    help="Sinif-dengeli bolme (CIFAR-100 icin ZORUNLU: 100 sinifta "
                         "rastgele 2000'lik bolme sinif basina 7-35 ornek birakiyor, "
                         "secim metrigi asiri gurultulu olur)")
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
    per_class = None
    if args.stratified:
        val_indices, per_class = _stratified_indices(
            args.dataset, n_train, args.val_size, generator)
    else:
        perm = torch.randperm(n_train, generator=generator).tolist()
        val_indices = sorted(perm[:args.val_size])

    payload = {
        "dataset": args.dataset,
        "split_seed": args.split_seed,
        "n_train_total": n_train,
        "val_size": len(val_indices),
        "stratified": bool(args.stratified),
        "per_class": per_class,
        "note": "Ortak sabit val bolmesi; clean pretraining VE adversarial "
                "fine-tuning bu ornekleri egitimden cikarir (leak fix). Egitim "
                "seed'lerinden bagimsizdir."
                + (" Sinif-dengeli (stratified)." if args.stratified else ""),
        "val_indices": val_indices,
    }
    with open(out, "w") as f:
        json.dump(payload, f)
    print(f"yazildi: {out} ({len(val_indices)} indeks, dataset={args.dataset}, "
          f"n_train={n_train}, split_seed={args.split_seed}"
          + (f", stratified: sinif basina {per_class['min']}-{per_class['max']}"
             f" ({per_class['n_class']} sinif)" if per_class else "") + ")")


if __name__ == "__main__":
    main()
