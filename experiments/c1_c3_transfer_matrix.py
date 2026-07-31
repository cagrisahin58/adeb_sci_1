"""C3: WRN-28-10 dahil 3x3 transfer matrisi (C1 kontrol noktalari).

Amac: transfer asimetrisinin, hedefin temiz hata orani tarafindan ne kadar
aciklandigini olcmek. Uc model (ResNet-18 AT, ViT-Tiny AT, WRN-28-10) icin
ham ve kosullu (target-correct) yaniltma oranlari, ornek bazinda kayitla.

Cikti: results/c1_c3/pair{N}/ (per-sample npz + matrix json)
Kullanim: python experiments/c1_c3_transfer_matrix.py --pairs 1 2 3 [--n-samples 10000]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.attacks import PGDAttack  # noqa: E402
from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

EPS = 8 / 255
ALPHA = 2 / 255
STEPS = 10
PAIRS = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}


def set_seed(seed):
    import random

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load_local(model_type, path, device):
    model = ModelRegistry.get(model_type)
    load_model_weights(model, path, device)
    return model.to(device).eval()


def load_wrn(device):
    from robustbench.utils import load_model

    model = load_model(model_name="Gowal2020Uncovering_28_10_extra",
                       dataset="cifar10", threat_model="Linf",
                       model_dir="models/robustbench_zoo")
    return model.to(device).eval()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--n-samples", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    wrn = load_wrn(device)

    for pair in args.pairs:
        rs, vs = PAIRS[pair]
        out_dir = Path(f"results/c1_c3/pair{pair}")
        out_dir.mkdir(parents=True, exist_ok=True)
        if (out_dir / "transfer_matrix.json").exists():
            print(f"cift {pair}: artefakt mevcut, atlandi")
            continue

        set_seed(args.seed)
        models = {
            "ResNet18_AT": load_local("resnet18", f"models/c1/resnet18_s{rs}/resnet18/adv/adversarial_training/best.pth", device),
            "ViT_Tiny_AT": load_local("vit_tiny", f"models/c1/vit_tiny_s{vs}/vit_tiny/adv/adversarial_training/best.pth", device),
            "WRN_28_10": wrn,
        }
        names = list(models)
        _, test_loader = get_cifar10_loaders(data_dir="./data", test_batch_size=50)

        # Once tum modellerin temiz-dogru maskeleri (ayni ornek sirasi)
        clean_ok = {n: [] for n in names}
        labels_all = []
        seen = 0
        for images, labels in test_loader:
            if seen >= args.n_samples:
                break
            if seen + labels.size(0) > args.n_samples:
                keep = args.n_samples - seen
                images, labels = images[:keep], labels[:keep]
            images, labels = images.to(device), labels.to(device)
            with torch.no_grad():
                for n in names:
                    clean_ok[n].append((models[n](images).argmax(1) == labels).cpu().numpy())
            labels_all.append(labels.cpu().numpy())
            seen += labels.size(0)
        clean_ok = {n: np.concatenate(v) for n, v in clean_ok.items()}
        print(f"cift {pair} temiz dogruluk: " + ", ".join(f"{n}={100 * clean_ok[n].mean():.2f}" for n in names))

        results = {}
        for src in names:
            attack = PGDAttack(models[src], eps=EPS, alpha=ALPHA, steps=STEPS)
            adv_wrong = {n: [] for n in names}
            seen = 0
            for images, labels in test_loader:
                if seen >= args.n_samples:
                    break
                if seen + labels.size(0) > args.n_samples:
                    keep = args.n_samples - seen
                    images, labels = images[:keep], labels[:keep]
                images, labels = images.to(device), labels.to(device)
                adv = attack(images, labels)
                with torch.no_grad():
                    for n in names:
                        adv_wrong[n].append((models[n](adv).argmax(1) != labels).cpu().numpy())
                seen += labels.size(0)
            for tgt in names:
                aw = np.concatenate(adv_wrong[tgt])
                cond = clean_ok[tgt]
                results[f"{src}->{tgt}"] = {
                    "raw_fooling": round(float(100 * aw.mean()), 2),
                    "cond_fooling": round(float(100 * aw[cond].mean()), 2),
                    "n_cond": int(cond.sum()),
                    "target_clean_acc": round(float(100 * cond.mean()), 2),
                }
                np.savez(out_dir / f"per_sample_{src}_to_{tgt}.npz",
                         target_clean_correct=cond, target_adv_wrong=aw,
                         source_clean_correct=clean_ok[src])
                print(f"  {src}->{tgt}: raw={results[f'{src}->{tgt}']['raw_fooling']:.2f} "
                      f"cond={results[f'{src}->{tgt}']['cond_fooling']:.2f}")
            del attack
            torch.cuda.empty_cache()

        with open(out_dir / "transfer_matrix.json", "w") as f:
            json.dump({"pair": pair, "seed": args.seed, "n_samples": args.n_samples,
                       "eps": EPS, "models": names, "results": results}, f, indent=2)
        print(f"cift {pair} kaydedildi: {out_dir}")


if __name__ == "__main__":
    main()
