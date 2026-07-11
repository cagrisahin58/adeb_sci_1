#!/usr/bin/env python3
"""
Generate Publication Figures from Actual Experiment Results

Bu script YALNIZCA gercek deney artefaktlarindan figur uretir. Eksik bir
artefakt varsa sessizce demo/sentetik veriye dusmek yerine FileNotFoundError
ile durur (M1/M2/M4/M5: onceki surum np.random demo verisi, '# Interpolated'
hardcoded degerler ve run1 kalintisi matrislerle figur uretiyordu — bunlarin
tamami kaldirildi).

Gerekli artefaktlar ve ureten komutlar:
  - results/final_eval/{resnet18_at,vit_tiny_at,resnet18_clean,vit_tiny_clean}/
        <type>_robustness_results.csv           (R3: cli evaluate robustness)
  - results/autoattack_run3_full/autoattack_summary.json
                                                (R5: experiments/run_autoattack_run2.py)
  - results/wrn_eval/wrn_eval_summary.json      (R9: experiments/run_wrn_eval.py)
  - results/epsilon_sweep_run3/{resnet18,vit_tiny}/<type>_robustness_results.csv
                                                (R4: cli evaluate robustness, 4 epsilon)
  - results/transfer_analysis_run3/transfer_summary.json
                                                (R6: run_all_analyses_run2.py --only transfer)

Usage:
    python paper/figures/generate_from_experiments.py --all
    python paper/figures/generate_from_experiments.py --figure 1
"""

import os
import sys
import json
import argparse
import torch
import numpy as np
import pandas as pd
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent))

from generate_figures import (
    figure1_robustness_comparison,
    figure2_epsilon_sweep,
    figure3_transfer_heatmap,
    figure4_gradient_analysis,
    figure4b_gradient_distribution,
    figure5_attention_degradation,
    figure5b_attention_entropy,
)

EPS_MAIN = 8 / 255
EPS_SWEEP = [2 / 255, 4 / 255, 8 / 255, 16 / 255]

# Tablolarin tanimladigi (degerlendirilen) checkpoint'ler: run3 varsa run3,
# yoksa run2 (ikisi de gercek egitim ciktisi - fabrikasyon fallback DEGIL).
def _pick_checkpoint(model_key: str) -> Path:
    candidates = [
        PROJECT_ROOT / f'models/{model_key}/adv/at_run3/{model_key}/adv/adversarial_training/best.pth',
        PROJECT_ROOT / f'models/{model_key}/adv/at_run2/{model_key}/adv/adversarial_training/best.pth',
    ]
    for c in candidates:
        if c.exists():
            print(f"Checkpoint [{model_key}]: {c}")
            return c
    raise FileNotFoundError(f"{model_key} icin at_run3/at_run2 checkpoint'i yok: {candidates}")


CHECKPOINTS = {
    'resnet18': _pick_checkpoint('resnet18'),
    'vit_tiny': _pick_checkpoint('vit_tiny'),
}

ARTIFACTS = {
    'final_eval': PROJECT_ROOT / 'results/final_eval',
    'autoattack': PROJECT_ROOT / 'results/autoattack_run3_full/autoattack_summary.json',
    'wrn_eval': PROJECT_ROOT / 'results/wrn_eval/wrn_eval_summary.json',
    'epsilon_sweep': PROJECT_ROOT / 'results/epsilon_sweep_run3',
    'transfer': PROJECT_ROOT / 'results/transfer_analysis_run3/transfer_summary.json',
}

# RobustBench leaderboard degeri (Gowal2020Uncovering_28_10_extra, n=10000).
# Yerel AutoAttack kosusu yapilmadigi icin kaynak acikca budur; makalede
# dipnotla beyan edilir (M14).
WRN_AA_ROBUSTBENCH_REPORTED = 62.76


def _require(path: Path, produced_by: str) -> Path:
    """Fail loudly if an artifact is missing - no fallbacks (M1)."""
    if not Path(path).exists():
        raise FileNotFoundError(
            f"Gerekli artefakt yok: {path}\n"
            f"Once su komutu calistirin: {produced_by}"
        )
    return Path(path)


# =============================================================================
# DATA LOADING FUNCTIONS
# =============================================================================

def read_eval_csv(csv_path: Path) -> dict:
    """Read a cli-evaluate robustness CSV into {(attack, eps): accuracy}.

    CSVReporter kolonlari buyuk harfle yazar (Model,Attack,Epsilon,Accuracy);
    kucuk harfe normalize edip eps/epsilon adlarinin ikisini de kabul ederiz.
    """
    df = pd.read_csv(csv_path)
    df.columns = [c.strip().lower() for c in df.columns]
    eps_col = 'eps' if 'eps' in df.columns else 'epsilon'
    out = {}
    for _, row in df.iterrows():
        out[(str(row['attack']), float(row[eps_col]))] = float(row['accuracy'])
    return out


def _lookup(evals: dict, attack: str, eps: float) -> float:
    """Find accuracy for (attack, eps) with float tolerance."""
    for (a, e), acc in evals.items():
        if a == attack and (abs(e - eps) < 1e-6 or (attack == 'clean')):
            return acc
    raise KeyError(f"CSV icinde bulunamadi: attack={attack}, eps={eps:.5f}")


# =============================================================================
# FIGURE DATA COLLECTION
# =============================================================================

def collect_robustness_data() -> dict:
    """Collect Figure 1 data from saved evaluation artifacts only (M5)."""

    fe = ARTIFACTS['final_eval']
    resnet_at = read_eval_csv(_require(
        fe / 'resnet18_at' / 'resnet18_robustness_results.csv',
        "cli evaluate robustness (R3, resnet18 AT)"))
    vit_at = read_eval_csv(_require(
        fe / 'vit_tiny_at' / 'vit_tiny_robustness_results.csv',
        "cli evaluate robustness (R3, vit_tiny AT)"))
    resnet_clean = read_eval_csv(_require(
        fe / 'resnet18_clean' / 'resnet18_robustness_results.csv',
        "cli evaluate robustness (R3, resnet18 clean)"))
    vit_clean = read_eval_csv(_require(
        fe / 'vit_tiny_clean' / 'vit_tiny_robustness_results.csv',
        "cli evaluate robustness (R3, vit_tiny clean)"))

    with open(_require(ARTIFACTS['autoattack'],
                       "python experiments/run_autoattack_run2.py --n-samples 10000 (R5)")) as f:
        aa = json.load(f)
    aa_by_model = {r['model']: r['robust_accuracy'] for r in aa['results']}

    with open(_require(ARTIFACTS['wrn_eval'],
                       "python experiments/run_wrn_eval.py (R9)")) as f:
        wrn = json.load(f)['results']

    def wrn_metric(key):
        return wrn[key]['accuracy']

    wrn_pgd_key = None
    for key in wrn:
        if key.startswith('pgd10_eps') and abs(float(key.split('eps')[1]) - EPS_MAIN) < 1e-4:
            wrn_pgd_key = key
    if wrn_pgd_key is None:
        raise KeyError("WRN eval icinde eps=8/255 PGD-10 sonucu yok")

    return {
        'ResNet-18\n(Clean)': {
            'clean': _lookup(resnet_clean, 'clean', 0.0),
            'fgsm': _lookup(resnet_clean, 'fgsm', EPS_MAIN),
            'pgd10': _lookup(resnet_clean, 'pgd', EPS_MAIN),
        },
        'ResNet-18\n(AT)': {
            'clean': _lookup(resnet_at, 'clean', 0.0),
            'fgsm': _lookup(resnet_at, 'fgsm', EPS_MAIN),
            'pgd10': _lookup(resnet_at, 'pgd', EPS_MAIN),
            'aa': aa_by_model['ResNet18_AT'],
        },
        'WRN-28-10': {
            'clean': wrn_metric('clean'),
            'fgsm': wrn_metric('fgsm'),
            'pgd10': wrn_metric(wrn_pgd_key),
            # Yerel AA kosulmadi; RobustBench leaderboard degeri (dipnotla)
            'aa': WRN_AA_ROBUSTBENCH_REPORTED,
        },
        'ViT-Tiny\n(AT)': {
            'clean': _lookup(vit_at, 'clean', 0.0),
            'fgsm': _lookup(vit_at, 'fgsm', EPS_MAIN),
            'pgd10': _lookup(vit_at, 'pgd', EPS_MAIN),
            'aa': aa_by_model['ViT_Tiny_AT'],
        },
        'ViT-Tiny\n(Clean)': {
            'clean': _lookup(vit_clean, 'clean', 0.0),
            'fgsm': _lookup(vit_clean, 'fgsm', EPS_MAIN),
            'pgd10': _lookup(vit_clean, 'pgd', EPS_MAIN),
        },
    }


def collect_epsilon_sweep_data() -> dict:
    """Collect Figure 2 data from real epsilon-sweep runs only (M2).

    Onceki surumdeki '# Interpolated' hardcoded sozlugu kaldirildi: gercek
    tarama (results/bildiri_eps_sweep) eski cizilen degerlerin 9-11pp yanlis
    oldugunu gostermisti. Fallback yok.
    """
    sweep_dir = ARTIFACTS['epsilon_sweep']
    data = {}

    for label, mtype in [('ResNet-18 (AT)', 'resnet18'), ('ViT-Tiny (AT)', 'vit_tiny')]:
        csv_path = _require(
            sweep_dir / mtype / f'{mtype}_robustness_results.csv',
            f"cli evaluate robustness, 4 epsilon PGD (R4, {mtype})")
        evals = read_eval_csv(csv_path)
        curve = {0.0: _lookup(evals, 'clean', 0.0)}
        for eps in EPS_SWEEP:
            curve[eps] = _lookup(evals, 'pgd', eps)
        data[label] = curve

    # WRN curve from the local WRN evaluation (R9). JSON anahtarlarindaki
    # epsilon 5 haneye yuvarlanmis (0.00784); CSV'lerdeki tam-hassasiyetli
    # epsilon'larla ayni x-noktasina dusmesi icin kanonik degere esle
    # (aksi halde cizim fonksiyonu eslesmeyen eps'lere 0 basar).
    with open(_require(ARTIFACTS['wrn_eval'],
                       "python experiments/run_wrn_eval.py (R9)")) as f:
        wrn = json.load(f)['results']
    curve = {0.0: wrn['clean']['accuracy']}
    for key, val in wrn.items():
        if key.startswith('pgd10_eps'):
            raw_eps = float(key.split('eps')[1])
            canonical = min(EPS_SWEEP, key=lambda e: abs(e - raw_eps))
            if abs(canonical - raw_eps) > 1e-4:
                raise ValueError(f"WRN eps {raw_eps} kanonik listeyle eslesmiyor")
            curve[canonical] = val['accuracy']
    data['WRN-28-10'] = curve

    return data


def collect_transfer_data() -> tuple:
    """Collect Figure 3 data from the conditioned transfer analysis (M3/M4).

    Yalnizca run3 (kosullu fooling-rate metrikli) ozetini okur. Onceki
    surumdeki run1 dosyasi ve placeholder matris kaldirildi; matris,
    Tablo 2 ve figur basligi ayni JSON'dan beslenir.
    """
    results_json = _require(
        ARTIFACTS['transfer'],
        "python experiments/run_all_analyses_run2.py --only transfer --n-samples 10000 (R6)")

    with open(results_json) as f:
        data = json.load(f)

    if data.get('metric') != 'conditioned_fooling_rate':
        raise ValueError(
            f"{results_json} kosullu metrik icermiyor "
            f"(metric={data.get('metric')!r}); R6 kosusunu yeni kodla tekrarlayin.")

    # Metinle tutarli adlandirma: 'ResNet-18 AT' / 'ViT-Tiny AT' (bicim-11)
    display_names = {'ResNet18_AT': 'ResNet-18 AT', 'ViT_Tiny_AT': 'ViT-Tiny AT'}
    model_names = [display_names.get(name, name.replace('_', '-')) for name in data['models']]
    transfer_matrix = np.array(data['matrix'])

    return transfer_matrix, model_names


# =============================================================================
# GRADIENT AND ATTENTION DATA COLLECTION (real forward/backward passes)
# =============================================================================

def _load_model(model_type: str, checkpoint_path: Path, device):
    from src.models import ModelRegistry
    from src.utils.checkpoint import load_model_weights

    _require(checkpoint_path, "adversarial training (checkpoint eksik)")
    model = ModelRegistry.get(model_type)
    load_model_weights(model, str(checkpoint_path), device)
    return model.to(device).eval()


def compute_gradients_for_figure(model_type: str, checkpoint_path: Path,
                                 n_vis: int = 3, n_norm_samples: int = 256):
    """Compute real input-gradient data for fig4a/fig4b.

    Returns:
        images_np: (n_vis, 32, 32, 3) gorsellestirme goruntuleri
        grad_maps: (n_vis, 32, 32) kanal-maks |grad| haritalari
        l2_norms: (n_norm_samples,) ornek-basi gradyan L2 normlari
            (per-sample sum-reduction tanimi; sanity: AT modellerde ~0.6-0.8,
            bkz. gradient_summary.json)
    """
    from src.data import get_cifar10_loaders

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = _load_model(model_type, checkpoint_path, device)

    _, test_loader = get_cifar10_loaders(data_dir=str(PROJECT_ROOT / 'data'),
                                         test_batch_size=n_norm_samples, num_workers=0)
    images, labels = next(iter(test_loader))
    images, labels = images.to(device), labels.to(device)

    images_g = images.clone().detach().requires_grad_(True)
    outputs = model(images_g)
    # reduction='sum': ornek-basina gradyan (batch boyutundan bagimsiz olcek,
    # gradient_summary.json ile ayni tanim)
    loss = torch.nn.functional.cross_entropy(outputs, labels, reduction='sum')
    grads = torch.autograd.grad(loss, images_g)[0]

    grad_maps = grads.abs().max(dim=1)[0][:n_vis].cpu().numpy()
    l2_norms = torch.norm(grads.view(grads.shape[0], -1), p=2, dim=1).cpu().numpy()
    images_np = images[:n_vis].detach().cpu().numpy().transpose(0, 2, 3, 1)

    return images_np, grad_maps, l2_norms, (images[:n_vis], labels[:n_vis], model, device)


def compute_attention_for_figure(checkpoint_path: Path, layers=(0, 5, 11)):
    """Compute REAL attention maps (clean vs adversarial) for fig5a/5b.

    Degerlendirilen timm ViT-Tiny modelinin get_attention_maps() metodunu
    kullanir (fused SDPA devre disi birakilip post-softmax attention hook'la
    yakalanir). Onceki surumun torch.rand tabanli sahte attention'i kaldirildi.
    """
    from src.data import get_cifar10_loaders
    from src.attacks import PGDAttack

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = _load_model('vit_tiny', checkpoint_path, device)

    if not hasattr(model, 'get_attention_maps'):
        raise AttributeError(
            "vit_tiny modelinde get_attention_maps yok; src/models/vit.py "
            "guncel degil (M1 attention-extraction edit'i gerekli).")

    _, test_loader = get_cifar10_loaders(data_dir=str(PROJECT_ROOT / 'data'),
                                         test_batch_size=8, num_workers=0)
    images, labels = next(iter(test_loader))
    images, labels = images.to(device), labels.to(device)

    # Makale protokolu: PGD-10, alpha=2/255 (eski kod steps=20 kullaniyordu)
    attack = PGDAttack(model, eps=EPS_MAIN, alpha=2 / 255, steps=10, device=device)
    adv_images = attack(images, labels)

    clean = model.get_attention_maps(images)
    adv = model.get_attention_maps(adv_images)

    sample_idx = 0
    clean_attn_dict = {l: clean['cls_maps'][sample_idx, l].cpu().numpy() for l in layers}
    adv_attn_dict = {l: adv['cls_maps'][sample_idx, l].cpu().numpy() for l in layers}
    sample_image = images[sample_idx].permute(1, 2, 0).cpu().numpy()

    entropy_data = {
        'clean': clean['entropy'].cpu().numpy().tolist(),
        'adversarial': adv['entropy'].cpu().numpy().tolist(),
    }

    # Entropi verisini artefakt olarak kaydet (B17: metinde nicelenebilsin).
    # NOT: batch=8 ornekten hesaplanir; n>=100'luk kesin niceleme icin ayri
    # kosu gerekir (C-madde onayina tabi).
    ent_out = PROJECT_ROOT / 'results/attention_analysis_run3/attention_entropy_fig.json'
    ent_out.parent.mkdir(parents=True, exist_ok=True)
    with open(ent_out, 'w') as f:
        json.dump({'n_samples': int(images.shape[0]), 'note': 'figure batch only',
                   **entropy_data}, f, indent=2)

    return clean_attn_dict, adv_attn_dict, sample_image, entropy_data


# =============================================================================
# MAIN GENERATION FUNCTIONS
# =============================================================================

def generate_figure1(output_dir: Path):
    """Generate Figure 1: Robustness Comparison."""
    print("[1/5] Generating Robustness Comparison...")
    data = collect_robustness_data()
    figure1_robustness_comparison(data, str(output_dir / 'fig1_robustness_comparison.pdf'))


def generate_figure2(output_dir: Path):
    """Generate Figure 2: Epsilon Sweep."""
    print("[2/5] Generating Epsilon Sweep...")
    data = collect_epsilon_sweep_data()
    figure2_epsilon_sweep(data, str(output_dir / 'fig2_epsilon_sweep.pdf'))


def generate_figure3(output_dir: Path):
    """Generate Figure 3: Transfer Heatmap."""
    print("[3/5] Generating Transfer Heatmap...")
    matrix, names = collect_transfer_data()
    figure3_transfer_heatmap(matrix, names, str(output_dir / 'fig3_transfer_heatmap.pdf'))
    print("  KONTROL: heatmap hucrelerinin Tablo 2 ve figur basligiyla "
          "ayni degerler oldugunu gorsel olarak dogrulayin (M4)")


def generate_figure4(output_dir: Path):
    """Generate Figure 4: Gradient Analysis (real gradients + real PGD perturbations)."""
    print("[4/5] Generating Gradient Analysis...")

    from src.attacks import PGDAttack

    images_np, cnn_grads, cnn_norms, (vis_images, vis_labels, cnn_model, device) = \
        compute_gradients_for_figure('resnet18', CHECKPOINTS['resnet18'])
    _, vit_grads, vit_norms, _ = \
        compute_gradients_for_figure('vit_tiny', CHECKPOINTS['vit_tiny'])

    # Gercek PGD-10 pertubasyonlari (onceki surum np.random placeholder idi, M1c)
    attack = PGDAttack(cnn_model, eps=EPS_MAIN, alpha=2 / 255, steps=10, device=device)
    adv = attack(vis_images, vis_labels)
    perturbations = (adv - vis_images).detach().cpu().numpy().transpose(0, 2, 3, 1)

    figure4_gradient_analysis(
        images_np, cnn_grads, vit_grads, perturbations,
        str(output_dir / 'fig4a_gradient_visualization.pdf')
    )

    print(f"  Sanity: CNN L2 norm ort={cnn_norms.mean():.4f}, "
          f"ViT L2 norm ort={vit_norms.mean():.4f} "
          f"(per-sample tanim; gradient_summary.json ile eslesmali)")
    figure4b_gradient_distribution(
        cnn_norms, vit_norms,
        str(output_dir / 'fig4b_gradient_distribution.pdf')
    )


def generate_figure5(output_dir: Path):
    """Generate Figure 5: Attention Analysis (real attention extraction)."""
    print("[5/5] Generating Attention Analysis...")

    clean_attn, adv_attn, sample_img, entropy_data = \
        compute_attention_for_figure(CHECKPOINTS['vit_tiny'])

    figure5_attention_degradation(clean_attn, adv_attn, sample_img,
                                  str(output_dir / 'fig5a_attention_comparison.pdf'))
    figure5b_attention_entropy(entropy_data, str(output_dir / 'fig5b_attention_entropy.pdf'))


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Generate publication figures from experiments')
    parser.add_argument('--all', action='store_true', help='Generate all figures')
    parser.add_argument('--figure', type=int, choices=[1, 2, 3, 4, 5], help='Generate specific figure')
    parser.add_argument('--output-dir', type=str, default='paper/figures/raw',
                        help='Output directory for figures')
    args = parser.parse_args()

    output_dir = PROJECT_ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Generating Publication Figures from Experiment Results")
    print("(no fallbacks: eksik artefakt = hata, M1)")
    print("=" * 60)

    if args.all or args.figure is None:
        generate_figure1(output_dir)
        generate_figure2(output_dir)
        generate_figure3(output_dir)
        generate_figure4(output_dir)
        generate_figure5(output_dir)
    else:
        generators = {
            1: generate_figure1,
            2: generate_figure2,
            3: generate_figure3,
            4: generate_figure4,
            5: generate_figure5,
        }
        generators[args.figure](output_dir)

    print("\n" + "=" * 60)
    print(f"Figures saved to: {output_dir}")
    print("Her PDF'i kaynak JSON/CSV degerlerine karsi gorsel olarak dogrulayin")
    print("=" * 60)


if __name__ == '__main__':
    main()
