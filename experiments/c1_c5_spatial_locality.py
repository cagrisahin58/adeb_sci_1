"""C5: girdi gradyanlarinin MEKANSAL lokalitesi (C1 kontrol noktalari).

Seyreklik olculeri (Hoyer/Gini) "kac bilesen buyuk" sorusunu yanitlar ama
bu bilesenlerin uzamda toplu olup olmadigini soylemez. Makalede "daha
yogunlasmis/lokalize" denebilmesi icin mekansal olcutler gerekir:

  * top-k% enerji alani: gradyan enerjisinin %k'sini tasiyan en kucuk piksel
    kumesinin, toplam piksele orani (k = 50, 90; kucuk = daha lokalize)
  * mekansal entropi: kanal-toplami enerji haritasi olasilik dagilimi olarak
    normalize edilir, Shannon entropisi (dusuk = daha lokalize); log(HW)'ye
    gore normalize edilmis hali de raporlanir
  * komsuluk otokorelasyonu (Moran's I, 4-komsuluk): pozitif = enerji
    bitisik piksellerde kumeleniyor

Tum olcutler olcekten bagimsizdir (enerji haritasi toplama normalize edilir).

Cikti: results/c1_c5/pair{N}/c5_spatial.json
Kullanim: python experiments/c1_c5_spatial_locality.py --pairs 1 2 3 [--n-samples 500]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import get_cifar10_loaders  # noqa: E402
from src.models import ModelRegistry  # noqa: E402
from src.utils.checkpoint import load_model_weights  # noqa: E402

PAIRS = {1: (1001, 2001), 2: (1002, 2002), 3: (1003, 2003)}


def set_seed(seed):
    import random

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def load(model_type, path, device):
    m = ModelRegistry.get(model_type)
    load_model_weights(m, path, device)
    return m.to(device).eval()


def energy_maps(model, images, labels):
    """Girdi gradyanindan kanal-toplami enerji haritasi (B, H, W), toplama normalize."""
    images = images.clone().requires_grad_(True)
    loss = nn.CrossEntropyLoss()(model(images), labels)
    grad = torch.autograd.grad(loss, images)[0]
    e = (grad ** 2).sum(dim=1)  # (B, H, W)
    e = e / e.flatten(1).sum(1).view(-1, 1, 1).clamp_min(1e-12)
    return e.detach()


def topk_area(e, frac):
    """Enerjinin frac kadarini tasiyan en kucuk piksel kumesinin oransal alani."""
    B = e.shape[0]
    flat = e.flatten(1)
    srt, _ = torch.sort(flat, dim=1, descending=True)
    csum = srt.cumsum(1)
    idx = (csum < frac).sum(1) + 1  # frac'i asan ilk indeks (1-tabanli)
    return (idx.float() / flat.shape[1]).cpu().numpy()


def spatial_entropy(e):
    flat = e.flatten(1).clamp_min(1e-12)
    ent = -(flat * flat.log()).sum(1)
    return ent.cpu().numpy(), float(np.log(flat.shape[1]))


def morans_i(e):
    """4-komsuluk Moran's I (her ornek icin)."""
    x = e
    B, H, W = x.shape
    mu = x.flatten(1).mean(1).view(-1, 1, 1)
    d = x - mu
    num = torch.zeros(B, device=x.device)
    # yatay ve dikey komsu ciftleri (her cift bir kez, W matrisi simetrik -> 2x)
    num += (d[:, :, :-1] * d[:, :, 1:]).flatten(1).sum(1) * 2
    num += (d[:, :-1, :] * d[:, 1:, :]).flatten(1).sum(1) * 2
    den = (d ** 2).flatten(1).sum(1).clamp_min(1e-12)
    n_pairs = 2 * (H * (W - 1) + W * (H - 1))
    n = H * W
    return ((n / n_pairs) * num / den).cpu().numpy()


def summarize(v):
    v = np.asarray(v, dtype=float)
    return {"mean": float(v.mean()), "std": float(v.std(ddof=1)), "n": int(v.size)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, nargs="+", default=[1, 2, 3])
    ap.add_argument("--n-samples", type=int, default=500)
    ap.add_argument("--batch", type=int, default=50)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for pair in args.pairs:
        rs, vs = PAIRS[pair]
        out_dir = Path(f"results/c1_c5/pair{pair}")
        out_dir.mkdir(parents=True, exist_ok=True)
        if (out_dir / "c5_spatial.json").exists():
            print(f"cift {pair}: artefakt mevcut, atlandi")
            continue
        set_seed(args.seed)

        models = {
            "ResNet18_AT": load("resnet18", f"models/c1/resnet18_s{rs}/resnet18/adv/adversarial_training/best.pth", device),
            "ViT_Tiny_AT": load("vit_tiny", f"models/c1/vit_tiny_s{vs}/vit_tiny/adv/adversarial_training/best.pth", device),
        }
        out = {"pair": pair, "seed": args.seed, "n_samples": args.n_samples, "models": {}}
        per_sample = {}

        for name, model in models.items():
            _, loader = get_cifar10_loaders(data_dir="./data", test_batch_size=args.batch)
            a50, a90, ents, mis = [], [], [], []
            seen = 0
            for images, labels in loader:
                if seen >= args.n_samples:
                    break
                if seen + labels.size(0) > args.n_samples:
                    k = args.n_samples - seen
                    images, labels = images[:k], labels[:k]
                images, labels = images.to(device), labels.to(device)
                e = energy_maps(model, images, labels)
                a50.append(topk_area(e, 0.50))
                a90.append(topk_area(e, 0.90))
                ent, ent_max = spatial_entropy(e)
                ents.append(ent)
                mis.append(morans_i(e))
                seen += labels.size(0)
            a50, a90 = np.concatenate(a50), np.concatenate(a90)
            ents, mis = np.concatenate(ents), np.concatenate(mis)
            per_sample[name] = {"area50": a50, "area90": a90, "entropy": ents, "morans_i": mis}
            out["models"][name] = {
                "energy_area_50pct": summarize(a50),
                "energy_area_90pct": summarize(a90),
                "spatial_entropy": summarize(ents),
                "spatial_entropy_normalized": summarize(ents / ent_max),
                "morans_i": summarize(mis),
                "entropy_max_log_HW": ent_max,
            }
            print(f"  {name}: area50={a50.mean():.4f} area90={a90.mean():.4f} "
                  f"ent={ents.mean():.3f}/{ent_max:.3f} moran={mis.mean():.4f}")

        # Eslesmis farklar (ayni ornekler): ResNet - ViT
        r, v = per_sample["ResNet18_AT"], per_sample["ViT_Tiny_AT"]
        out["paired_diff_ResNet_minus_ViT"] = {
            k: summarize(r[k] - v[k]) for k in ("area50", "area90", "entropy", "morans_i")
        }
        try:
            from scipy.stats import wilcoxon

            out["paired_wilcoxon_p"] = {
                k: float(wilcoxon(r[k], v[k]).pvalue) for k in ("area50", "area90", "entropy", "morans_i")
            }
        except Exception as exc:  # scipy yoksa atla
            out["paired_wilcoxon_p"] = f"hesaplanamadi: {exc}"

        np.savez(out_dir / "c5_per_sample.npz",
                 **{f"{m}_{k}": val for m, d in per_sample.items() for k, val in d.items()})
        with open(out_dir / "c5_spatial.json", "w") as f:
            json.dump(out, f, indent=2)
        print(f"cift {pair} kaydedildi: {out_dir}/c5_spatial.json")


if __name__ == "__main__":
    main()
