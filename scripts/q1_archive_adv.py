"""E0/E3: kaynak modelin PGD cekismeli orneklerini diske arsivler.

Kalibrasyon egrisinde (E3) onlarca hedef-checkpoint degerlendirilir; saldiri
her hedef icin yeniden uretilmek yerine KAYNAK modelde BIR kez uretilip
arsivlenir, hedef degerlendirmesi salt ileri gecise iner.

uint8 kaydi: adv goruntuler [0,1] araliginda, 255 ile olceklenip uint8
saklanir (~31MB / 10k goruntu). Geri yuklemede /255. Kayip, 1/255'lik
kuantalama adiminin altinda kaldigi icin eps=8/255 butcesini bozmaz;
yine de dogrulama icin max |delta| kaydedilir.

Kullanim:
    python scripts/q1_archive_adv.py --model-type resnet18 \
        --ckpt models/c1/resnet18_s1001/.../best.pth \
        --dataset cifar10 --out results/q1/adv_archive/rn18_s1001_pgd10.npz
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path("/workspace") if Path("/workspace/results").is_dir() else Path.home() / "projects/adeb_sci_1"
sys.path.insert(0, str(ROOT))

from src.attacks.pgd import PGDAttack, PGDL2Attack  # noqa: E402
from src.data import DATASETS, get_loaders  # noqa: E402
from src.utils.load_model_auto import load_model_auto  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-type", required=True)
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-samples", type=int, default=10000)
    ap.add_argument("--eps", type=float, default=8 / 255)
    ap.add_argument("--alpha", type=float, default=2 / 255)
    ap.add_argument("--steps", type=int, default=10)
    ap.add_argument("--norm", choices=["linf", "l2"], default="linf")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    torch.backends.cudnn.deterministic = True
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = load_model_auto(args.model_type, args.ckpt, device)
    if args.norm == "linf":
        attack = PGDAttack(model, eps=args.eps, alpha=args.alpha, steps=args.steps)
    else:
        attack = PGDL2Attack(model, eps=args.eps, alpha=args.alpha, steps=args.steps)

    _, loader = get_loaders(dataset=args.dataset, data_dir=str(ROOT / "data"),
                            test_batch_size=100)

    advs, labels_all, src_wrong, src_clean = [], [], [], []
    max_delta = 0.0
    seen = 0
    for images, labels in loader:
        if seen >= args.n_samples:
            break
        if seen + labels.size(0) > args.n_samples:
            keep = args.n_samples - seen
            images, labels = images[:keep], labels[:keep]
        images, labels = images.to(device), labels.to(device)
        adv = attack(images, labels)
        with torch.no_grad():
            src_clean.append((model(images).argmax(1) == labels).cpu().numpy())
            src_wrong.append((model(adv).argmax(1) != labels).cpu().numpy())
        # KUANTALANMIS arsivin deltasini olc (diske giden budur); L2'de
        # yuvarlama normu eps'in ~%1 uzerine tasiyabilir - kayda gecirilir
        adv_q = (adv.clamp(0, 1) * 255).round() / 255.0
        if args.norm == "linf":
            max_delta = max(max_delta, float((adv_q - images).abs().max()))
        else:
            max_delta = max(max_delta, float(
                (adv_q - images).flatten(1).norm(p=2, dim=1).max()))
        advs.append((adv_q * 255).to(torch.uint8).cpu().numpy())
        labels_all.append(labels.cpu().numpy())
        seen += labels.size(0)
        if seen % 2000 == 0:
            print(f"  {seen}/{args.n_samples}", flush=True)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out_path,
        adv_uint8=np.concatenate(advs),
        labels=np.concatenate(labels_all),
        source_adv_wrong=np.concatenate(src_wrong),
        source_clean_correct=np.concatenate(src_clean),
        meta=np.array([f"model={args.model_type}", f"ckpt={args.ckpt}",
                       f"dataset={args.dataset}", f"norm={args.norm}",
                       f"eps={args.eps}", f"alpha={args.alpha}",
                       f"steps={args.steps}", f"seed={args.seed}",
                       f"max_{args.norm}_delta_quantized={max_delta:.6f}"]),
    )
    print(f"kaydedildi: {out_path} (n={seen}, max|delta|={max_delta:.6f}, "
          f"kaynak-yaniltma %{100 * np.concatenate(src_wrong).mean():.2f})")


if __name__ == "__main__":
    main()
