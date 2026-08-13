"""E2 cevrimdisi secim araci: kayitli checkpoint dizisine secim kurali uygular.

Sizinti ablasyonunun anahtari: TEK tam-butce egitim (her epoch checkpoint'i
kayitli, patience KAPALI) yapilir; sonra bu arac AYNI yorungeye iki farkli
dogrulama bolmesiyle (V_A: on-egitimde gorulmus, V_B: hic gorulmemis) C1'in
secim kuralini (best-by-adv-val + patience-20 + min_delta 0.1) cevrimdisi
uygular. Iki kosul ayni yorungeyi paylastigindan kosu-ici varyans sifirdir;
fark yalnizca secim kuralindan gelir.

Kullanim (konteyner icinde):
    python scripts/q1_offline_select.py \
        --epochs-dir models/q1/e2/resnet18_s1001/adv/adversarial_training/epochs \
        --model-type resnet18 --dataset cifar10 \
        --val-indices data/e2_val_A.json \
        --out results/q1/e2/select_resnet18_s1001_valA.json
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))

from src.attacks.pgd import PGDAttack  # noqa: E402
from src.data import DATASETS, get_loaders_with_val  # noqa: E402
from src.utils.load_model_auto import infer_num_classes  # noqa: E402
from src.models import ModelRegistry  # noqa: E402


def eval_checkpoint(model, loader, device, eps, alpha, steps):
    """Val kumesinde temiz + PGD dogrulugu."""
    model.eval()
    attack = PGDAttack(model, eps=eps, alpha=alpha, steps=steps)
    n = c_clean = c_adv = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        adv = attack(images, labels)
        with torch.no_grad():
            c_clean += (model(images).argmax(1) == labels).sum().item()
            c_adv += (model(adv).argmax(1) == labels).sum().item()
        n += labels.size(0)
    return 100.0 * c_clean / n, 100.0 * c_adv / n


def simulate_selection(records, patience=20, min_delta=0.1):
    """C1 secim kuralinin birebir simulasyonu (AdversarialTrainer.train ile ayni).

    records: [(epoch, clean, adv)] artan epoch sirasinda.
    Returns: (secilen_epoch, secilen_adv, durdugu_epoch)
    """
    best_adv = 0.0
    best_epoch = None
    counter = 0
    stopped_at = records[-1][0] if records else None
    for epoch, _clean, adv in records:
        if adv > best_adv + min_delta:
            best_adv = adv
            best_epoch = epoch
            counter = 0
        else:
            counter += 1
            if patience > 0 and counter >= patience:
                stopped_at = epoch
                break
    return best_epoch, best_adv, stopped_at


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs-dir", required=True,
                    help="epoch_XXX.pth dosyalarinin dizini")
    ap.add_argument("--model-type", required=True)
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--val-indices", required=True,
                    help="Secimde kullanilacak dogrulama bolmesi JSON'u")
    ap.add_argument("--out", required=True)
    ap.add_argument("--eps", type=float, default=8 / 255)
    ap.add_argument("--alpha", type=float, default=2 / 255)
    ap.add_argument("--steps", type=int, default=10)
    ap.add_argument("--patience", type=int, default=20)
    ap.add_argument("--min-delta", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    ep_dir = Path(args.epochs_dir)
    ckpts = sorted(ep_dir.glob("epoch_*.pth"),
                   key=lambda p: int(re.search(r"epoch_(\d+)", p.name).group(1)))
    if not ckpts:
        raise FileNotFoundError(f"{ep_dir}: epoch_*.pth bulunamadi")

    _, val_loader, _ = get_loaders_with_val(
        dataset=args.dataset, data_dir=str(ROOT / "data"),
        val_indices_path=args.val_indices,
    )

    # Ilk checkpoint'ten num_classes cikar, tek model insa edip agirlik degistir
    first = torch.load(ckpts[0], map_location="cpu", weights_only=False)
    nc = infer_num_classes(first["model_state_dict"])
    model = ModelRegistry.get(args.model_type, num_classes=nc).to(device)

    records = []
    for ck in ckpts:
        payload = torch.load(ck, map_location="cpu", weights_only=False)
        model.load_state_dict(payload["model_state_dict"])
        epoch = int(re.search(r"epoch_(\d+)", ck.name).group(1))
        clean, adv = eval_checkpoint(model, val_loader, device,
                                     args.eps, args.alpha, args.steps)
        records.append((epoch, clean, adv))
        print(f"epoch {epoch:3d}: clean {clean:6.2f}  adv {adv:6.2f}", flush=True)

    best_epoch, best_adv, stopped_at = simulate_selection(
        records, patience=args.patience, min_delta=args.min_delta)

    out = {
        "epochs_dir": str(ep_dir),
        "model_type": args.model_type,
        "dataset": args.dataset,
        "val_indices": args.val_indices,
        "selection_rule": {"patience": args.patience, "min_delta": args.min_delta,
                           "metric": "pgd_adv_acc"},
        "attack": {"eps": args.eps, "alpha": args.alpha, "steps": args.steps,
                   "seed": args.seed},
        "records": [{"epoch": e, "clean": c, "adv": a} for e, c, a in records],
        "selected_epoch": best_epoch,
        "selected_adv_acc": best_adv,
        "early_stop_simulated_at": stopped_at,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out + ".tmp", "w") as f:
        json.dump(out, f, indent=2)
    import os as _os
    _os.replace(args.out + ".tmp", args.out)
    print(f"\nSECIM: epoch {best_epoch} (val adv {best_adv:.2f}); "
          f"patience-durusu epoch {stopped_at}\nkaydedildi: {args.out}")


if __name__ == "__main__":
    main()
