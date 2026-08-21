"""E2 P0: her yorungenin 100 checkpoint'i icin TAM 10k TEST egrisi.

Neden (curutme denetimi, 2026-08-17): E2'nin tum kesifsel analizleri 2000'lik
val bolmelerini test icin VEKIL olarak kullaniyordu; val->test aktarimi zayif
(9 epok ciftinde egim 0.457, artik sd 0.790 puan - iddia edilen etkilerin
mertebesinde). Bu betik vekili ortadan kaldirir: her checkpoint'in gercek 10k
test clean/PGD-10 dogrulugu ve ornek-bazli maskeleri kaydedilir. Boylece
  - kural duyarliligi, secim-protokolu varyansi ve "oracle kaybi" analizleri
    dogrudan BIRINCIL UC NOKTADA yapilir,
  - herhangi iki epok arasinda McNemar bedava hesaplanir,
  - gercek test-optimal epok bilinir (secim kurallarinin ne kadar kaybettirdigi).
On-kayitli birincil analizi (q1_e2_report.py) DEGISTIRMEZ; betimleyici.

Cikti: results/q1/e2/testcurve_<arch>_s<seed>.npz
  epochs (E,), clean_acc (E,), adv_acc (E,), clean_mask (E,N) bool,
  adv_mask (E,N) bool, meta alanlari

Kullanim (konteyner icinde, arka planda):
    python scripts/q1_e2_test_curve.py
    python scripts/q1_e2_test_curve.py --only vit_tiny_s2001
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))

from src.attacks.pgd import PGDAttack  # noqa: E402
from src.data import get_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.load_model_auto import infer_num_classes  # noqa: E402

TRAJ = [("resnet18", s) for s in (1001, 1002, 1003)] + \
       [("vit_tiny", s) for s in (2001, 2002, 2003)]


def eval_masks(model, loader, device, eps, alpha, steps):
    model.eval()
    attack = PGDAttack(model, eps=eps, alpha=alpha, steps=steps)
    c_ok, a_ok = [], []
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        adv = attack(images, labels)
        with torch.no_grad():
            c_ok.append((model(images).argmax(1) == labels).cpu())
            a_ok.append((model(adv).argmax(1) == labels).cpu())
    return (torch.cat(c_ok).numpy().astype(bool),
            torch.cat(a_ok).numpy().astype(bool))


def main():
    ap = argparse.ArgumentParser()
    # IS-6(a) / B.8 borcu: veri kumesi artik SABIT DEGIL. CIFAR-100 secim
    # bandini VEKIL (val) yerine GERCEK TEST uzerinde olcebilmek icin gerekli.
    ap.add_argument("--dataset", default="cifar10", choices=["cifar10", "cifar100", "svhn"])
    ap.add_argument("--traj-root", default=None,
                    help="yorunge koku; verilmezse veri kumesinden turetilir")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--only", default="", help="ornek: vit_tiny_s2001")
    ap.add_argument("--eps", type=float, default=8 / 255)
    ap.add_argument("--alpha", type=float, default=2 / 255)
    ap.add_argument("--steps", type=int, default=10)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--batch-size", type=int, default=256)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        sys.exit("CUDA yok - P0 test egrisi CPU'da makul surede bitmez")
    # Yorunge koku ve cikti dizini veri kumesinden turetilir (acikca verilmezse)
    TRAJ_ROOTS = {"cifar10": "models/q1/e2", "cifar100": "models/q1/cifar100",
                  "svhn": "models/q1/svhn"}
    OUT_DIRS = {"cifar10": "results/q1/e2", "cifar100": "results/q1/cifar100/testcurve",
                "svhn": "results/q1/svhn/testcurve"}
    traj_root = args.traj_root or TRAJ_ROOTS[args.dataset]
    _, test_loader = get_loaders(dataset=args.dataset, data_dir=str(ROOT / "data"),
                                 test_batch_size=args.batch_size)
    out_dir = Path(args.out_dir or str(ROOT / OUT_DIRS[args.dataset]))
    out_dir.mkdir(parents=True, exist_ok=True)

    for arch, seed in TRAJ:
        tag = f"{arch}_s{seed}"
        if args.only and args.only != tag:
            continue
        out_path = out_dir / f"testcurve_{tag}.npz"
        if out_path.exists():
            print(f"SKIP {tag} (zaten var)", flush=True)
            continue
        ep_dir = (ROOT / f"{traj_root}/{tag}/{arch}/adv/adversarial_training/epochs")
        ckpts = sorted(ep_dir.glob("epoch_*.pth"),
                       key=lambda p: int(re.search(r"epoch_(\d+)", p.name).group(1)))
        if not ckpts:
            print(f"ATLA {tag}: checkpoint yok ({ep_dir})", flush=True)
            continue

        first = torch.load(ckpts[0], map_location="cpu", weights_only=False)
        nc = infer_num_classes(first["model_state_dict"])
        model = ModelRegistry.get(arch, num_classes=nc).to(device)

        epochs, cl_acc, ad_acc, cl_masks, ad_masks = [], [], [], [], []
        atlanan = []
        t0 = time.time()
        for ck in ckpts:
            ep = int(re.search(r"epoch_(\d+)", ck.name).group(1))
            # OKUNAMAYAN CHECKPOINT: tum kosumu oldurmesin ama SESSIZ gecilmesin.
            # (models/q1/cifar100/vit_tiny_s2002/.../epoch_009.pth 0 BAYT cikti
            #  ve bu kosumu EOFError ile oldurmustu.)
            try:
                payload = torch.load(ck, map_location="cpu", weights_only=False)
            except Exception as e:
                atlanan.append(ep)
                print(f"  UYARI {tag}: epoch_{ep:03d} OKUNAMADI ({type(e).__name__}) "
                      f"-- ATLANDI, egride bu epok YOK", flush=True)
                continue
            model.load_state_dict(payload["model_state_dict"])
            # Secim kosumlariyla AYNI tohumlama semasi (karsilastirilabilirlik)
            torch.manual_seed(args.seed * 100000 + ep)
            cm, am = eval_masks(model, test_loader, device, args.eps, args.alpha, args.steps)
            epochs.append(ep)
            cl_masks.append(cm)
            ad_masks.append(am)
            cl_acc.append(100.0 * int(cm.sum()) / cm.size)
            ad_acc.append(100.0 * int(am.sum()) / am.size)
            if ep % 20 == 0:
                el = time.time() - t0
                print(f"{tag} epoch {ep:3d}: clean {cl_acc[-1]:6.2f} adv {ad_acc[-1]:6.2f} "
                      f"({el/60:.1f} dk)", flush=True)

        np.savez_compressed(
            str(out_path) + ".tmp.npz",
            epochs=np.array(epochs, dtype=np.int32),
            atlanan_epoklar=np.array(atlanan, dtype=np.int32),
            clean_acc=np.array(cl_acc), adv_acc=np.array(ad_acc),
            clean_mask=np.stack(cl_masks), adv_mask=np.stack(ad_masks),
            attack=np.array(json.dumps({"eps": args.eps, "alpha": args.alpha,
                                        "steps": args.steps, "seed": args.seed})),
        )
        os.replace(str(out_path) + ".tmp.npz", str(out_path))
        best_i = int(np.argmax(ad_acc))
        print(f"DONE {tag}: {len(epochs)} epok, {(time.time()-t0)/60:.1f} dk | "
              f"TEST-optimal ep{epochs[best_i]} adv {ad_acc[best_i]:.2f} | "
              f"-> {out_path}", flush=True)


if __name__ == "__main__":
    main()
