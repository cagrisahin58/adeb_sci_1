#!/usr/bin/env python3
"""AutoAttack evaluation for run2/run3 models.

Seedli, olceklenebilir ve ornek-bazli log ureten surum (M6/M15):
- --n-samples ile tam test seti (10000) degerlendirilebilir
- AutoAttack'e acik seed verilir (Square/FAB rastgeleligi sabitlenir)
- Ornek bazinda clean/robust gosterge vektorleri kaydedilir (McNemar
  esli testi ve tam tekrarlanabilirlik icin)
"""

import argparse
import random
import torch
import numpy as np
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import gc

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models import ModelRegistry
from src.data import get_cifar10_loaders, get_loaders, DATASETS
from src.utils.load_model_auto import load_model_auto
from src.utils.checkpoint import load_model_weights

try:
    from autoattack import AutoAttack
    AUTOATTACK_AVAILABLE = True
except ImportError:
    AUTOATTACK_AVAILABLE = False
    print("WARNING: AutoAttack not available")


def clear_gpu():
    """Clear GPU memory."""
    gc.collect()
    torch.cuda.empty_cache()


def set_seed(seed):
    """Full seeding for reproducibility (M15)."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def evaluate_with_autoattack(model, test_loader, device, eps=8/255, n_samples=500,
                             batch_size=100, seed=42, chunk_size=1000,
                             chunk_dir=None, model_name="", aa_norm="Linf"):
    """Evaluate model with AutoAttack.

    Kesintiye dayaniklilik: degerlendirme `chunk_size`'lik parcalara bolunur,
    her parcanin sonucu aninda .npz olarak kaydedilir. Elektrik kesintisi
    sonrasi ayni komut yeniden calistirildiginda tamamlanan parcalar atlanir,
    yalnizca yarim kalan parca tekrarlanir. Her parca kendi deterministik
    seed'ini (seed + chunk_idx) kullanir, bu yuzden parca sinirlari sonucu
    degistirmez ve resume tam tekrarlanabilirdir.
    """

    model.eval()

    # Collect samples
    all_images = []
    all_labels = []
    total = 0

    for images, labels in test_loader:
        all_images.append(images)
        all_labels.append(labels)
        total += images.size(0)
        if total >= n_samples:
            break

    images = torch.cat(all_images, dim=0)[:n_samples]
    labels = torch.cat(all_labels, dim=0)[:n_samples]

    # Clean accuracy (per-sample indicators for paired tests, M6)
    clean_chunks = []
    with torch.no_grad():
        for i in range(0, len(labels), batch_size):
            xb = images[i:i + batch_size].to(device)
            yb = labels[i:i + batch_size].to(device)
            clean_chunks.append((model(xb).argmax(1) == yb).cpu())
    clean_indicator = torch.cat(clean_chunks)
    clean_correct = clean_indicator.sum().item()

    clean_acc = 100 * clean_correct / len(labels)
    print(f"  Clean accuracy: {clean_acc:.2f}%")

    # AutoAttack, parca parca (kesinti-guvenli)
    n_chunks = (len(labels) + chunk_size - 1) // chunk_size
    robust_parts = []

    for k in range(n_chunks):
        lo, hi = k * chunk_size, min((k + 1) * chunk_size, len(labels))
        chunk_file = None
        if chunk_dir is not None:
            # Cache anahtari degerlendirme konfigurasyonunu ICERIR: farkli
            # norm/eps/seed kosulari birbirinin parcalarini yeniden kullanamaz.
            # (Geriye uyum: eski Linf-8/255-seed42 kosularinin adlari degisir;
            # C1 sonuclari zaten tamamlandigi icin sorun degil.)
            cfg_tag = f"{aa_norm}_eps{eps:.5f}_s{seed}_n{n_samples}"
            chunk_file = Path(chunk_dir) / f"aa_chunk_{model_name}_{cfg_tag}_{k:03d}.npz"
            if chunk_file.exists():
                cached = np.load(chunk_file)["robust_correct"]
                if len(cached) == hi - lo:
                    print(f"  Chunk {k + 1}/{n_chunks}: cached, skipping")
                    robust_parts.append(cached)
                    continue

        print(f"  Chunk {k + 1}/{n_chunks}: samples {lo}-{hi}")
        xb = images[lo:hi].to(device)
        yb = labels[lo:hi].to(device)

        adversary = AutoAttack(model, norm=aa_norm, eps=eps, version='standard',
                               seed=seed + k, verbose=True)
        adv_images = adversary.run_standard_evaluation(xb, yb, bs=batch_size)

        with torch.no_grad():
            robust = (model(adv_images).argmax(1) == yb).cpu().numpy()

        if chunk_file is not None:
            # Gecici ad .npz ile BITMELI: np.savez, .npz ile bitmeyen ada
            # kendisi .npz ekler ve replace hedefi bulamaz (R5 ilk kosusunun
            # dusme nedeni buydu)
            tmp = chunk_file.with_name(chunk_file.name + ".tmp.npz")
            np.savez(tmp, robust_correct=robust)
            tmp.replace(chunk_file)
        robust_parts.append(robust)

        del xb, yb, adv_images
        clear_gpu()

    robust_indicator = np.concatenate(robust_parts)
    robust_correct = int(robust_indicator.sum())
    robust_acc = 100 * robust_correct / len(labels)

    return {
        'n_samples': len(labels),
        'clean_accuracy': clean_acc,
        'robust_accuracy': robust_acc,
        'clean_correct': clean_correct,
        'robust_correct': robust_correct,
        'seed': seed,
        'chunk_size': chunk_size,
        'per_sample': {
            'clean_correct': clean_indicator.numpy(),
            'robust_correct': robust_indicator,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="AutoAttack evaluation (seeded, per-sample logging)")
    parser.add_argument("--n-samples", type=int, default=10000,
                        help="Number of test samples (default: full test set)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (data + AutoAttack)")
    parser.add_argument("--batch-size", type=int, default=100, help="AutoAttack batch size")
    parser.add_argument("--chunk-size", type=int, default=1000,
                        help="Kesinti-guvenli parca boyutu (her parca ayri npz'ye kaydedilir)")
    parser.add_argument("--output-dir", type=str, default="results/autoattack_run3_full",
                        help="Output directory")
    parser.add_argument("--resnet-path", type=str,
                        default="models/resnet18/adv/at_run2/resnet18/adv/adversarial_training/best.pth")
    parser.add_argument("--vit-path", type=str,
                        default="models/vit_tiny/adv/at_run2/vit_tiny/adv/adversarial_training/best.pth")
    parser.add_argument("--dataset", choices=sorted(DATASETS), default="cifar10",
                        help="Degerlendirme veri kumesi (num_classes ckpt'ten otomatik)")
    parser.add_argument("--eps", type=float, default=8/255)
    parser.add_argument("--norm", choices=["Linf", "L2"], default="Linf")
    parser.add_argument("--model", action="append", default=None, metavar="AD:TIP:YOL",
                        help="Ek/alternatif model tanimi (tekrarlanabilir). Verilirse "
                             "--resnet-path/--vit-path yoksayilir. Ornek: "
                             "--model R50_AT:resnet50:models/q1/.../best.pth")
    args = parser.parse_args()

    if not AUTOATTACK_AVAILABLE:
        print("AutoAttack not available. Skipping evaluation.")
        return

    set_seed(args.seed)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    print(f"Seed: {args.seed}, n_samples: {args.n_samples}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load data (Q1: dataset-parametrik)
    print(f"\nLoading {args.dataset}...")
    _, test_loader = get_loaders(dataset=args.dataset, data_dir='./data',
                                 test_batch_size=100)

    # Q1: --model AD:TIP:YOL verilirse varsayilan cift yerine o liste kullanilir
    if args.model:
        models_config = []
        for spec in args.model:
            parts = spec.split(":", 2)
            if len(parts) != 3:
                sys.exit(f"FATAL: gecersiz --model spec '{spec}' (AD:TIP:YOL bekleniyor)")
            models_config.append(tuple(parts))
    else:
        models_config = [
            ("ResNet18_AT", "resnet18", args.resnet_path),
            ("ViT_Tiny_AT", "vit_tiny", args.vit_path),
        ]

    eps = args.eps
    if args.norm == "L2" and eps < 0.1:
        print(f"UYARI: L2 normu ile eps={eps:.4f} cok kucuk gorunuyor "
              f"(L2 standardi 0.5); Linf butcesi mi verildi?")
    n_samples = args.n_samples
    batch_size = args.batch_size

    results = []
    per_sample_store = {}

    for name, model_type, model_path in models_config:
        print(f"\n{'='*60}")
        print(f"Evaluating: {name}")
        print(f"{'='*60}")

        # Eksik checkpoint = SERT hata: guard dosyasi kismi degerlendirmeyle
        # olusup pipeline'i yanlis DONE'a dusurmesin
        if not Path(model_path).exists():
            sys.exit(f"FATAL: checkpoint bulunamadi: {model_path}")

        clear_gpu()

        # Load model
        # num_classes checkpoint'ten otomatik (CIFAR-100 icin sart)
        model = load_model_auto(model_type, model_path, device)
        model.eval()

        # Evaluate (chunk'li: kesinti sonrasi tamamlanan parcalar atlanir)
        result = evaluate_with_autoattack(
            model, test_loader, device,
            eps=eps, n_samples=n_samples, batch_size=batch_size, seed=args.seed,
            aa_norm=args.norm,
            chunk_size=args.chunk_size, chunk_dir=output_dir, model_name=name,
        )
        result['model'] = name
        result['model_type'] = model_type
        result['eps'] = eps
        result['model_path'] = model_path

        # Ornek-bazli gostergeleri npz olarak kaydet (McNemar icin, M6);
        # JSON'a yalnizca ozet girer
        per_sample = result.pop('per_sample')
        np.savez(
            output_dir / f"per_sample_{name}.npz",
            clean_correct=per_sample['clean_correct'],
            robust_correct=per_sample['robust_correct'],
        )
        per_sample_store[name] = per_sample
        results.append(result)

        print(f"\n  Results for {name}:")
        print(f"    Clean Accuracy: {result['clean_accuracy']:.2f}%")
        print(f"    AutoAttack Accuracy: {result['robust_accuracy']:.2f}%")

        del model
        clear_gpu()

    # Save results
    df = pd.DataFrame(results)
    df.to_csv(output_dir / "autoattack_results.csv", index=False)

    # McNemar esli testi: iki model ayni orneklerde degerlendirildiginde
    # robust-accuracy farkinin anlamliligi (M6)
    mcnemar = None
    if len(per_sample_store) == 2:
        import math
        (name_a, ps_a), (name_b, ps_b) = per_sample_store.items()
        ra, rb = ps_a['robust_correct'], ps_b['robust_correct']
        b = int(np.sum(ra & ~rb))
        c = int(np.sum(~ra & rb))
        if b + c > 0:
            stat = (abs(b - c) - 1) ** 2 / (b + c)
            p_value = math.erfc(math.sqrt(stat / 2))  # chi2 sf, 1 dof
        else:
            stat, p_value = 0.0, 1.0
        mcnemar = {
            'model_a': name_a, 'model_b': name_b,
            'a_only_correct': b, 'b_only_correct': c,
            'statistic': stat, 'p_value': p_value,
        }
        print(f"\nMcNemar (robust): b={b}, c={c}, stat={stat:.3f}, p={p_value:.4f}")

    # Kemer-aski: istenen her model degerlendirilmis olmali; kismi/bos
    # degerlendirme guard dosyasi uretmemeli (pipeline yanlis DONE olmasin)
    if len(results) != len(models_config):
        sys.exit(f"FATAL: {len(models_config)} model istendi, {len(results)} "
                 f"degerlendirildi; autoattack_summary.json YAZILMADI")

    summary = {
        'timestamp': datetime.now().isoformat(),
        'dataset': args.dataset,
        'norm': args.norm,
        'eps': eps,
        'n_samples': n_samples,
        'seed': args.seed,
        'mcnemar_robust': mcnemar,
        'results': results,
    }

    # Atomik yaz: guard dosyasi yarim halde asla gorunmesin
    _tmp = output_dir / "autoattack_summary.json.tmp"
    with open(_tmp, 'w') as f:
        json.dump(summary, f, indent=2)
    _tmp.replace(output_dir / "autoattack_summary.json")

    # Print summary
    print("\n" + "="*60)
    print("AUTOATTACK RUN2 EVALUATION SUMMARY")
    print("="*60)
    print(f"\nEpsilon: {eps:.4f} ({eps*255:.0f}/255)")
    print(f"Samples: {n_samples}")
    print("\n" + "-"*50)
    print(f"{'Model':<25} {'Clean':<12} {'AutoAttack':<12}")
    print("-"*50)

    for r in results:
        print(f"{r['model']:<25} {r['clean_accuracy']:.2f}%{'':<6} {r['robust_accuracy']:.2f}%")

    print("-"*50)
    print(f"\nResults saved to {output_dir}")


if __name__ == "__main__":
    main()
