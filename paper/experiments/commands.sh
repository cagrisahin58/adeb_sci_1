#!/bin/bash
# Reproducibility Commands for SCI Paper
# CNN vs ViT Adversarial Robustness Comparison
#
# All commands should be run from the project root directory
# Environment: PyTorch 2.6.0, CUDA 12.8

# =============================================================================
# SECTION 1: MODEL TRAINING
# =============================================================================

# --- ResNet18 Clean Training ---
python -m cli.main train clean \
    --model resnet18 \
    --epochs 200 \
    --lr 0.1 \
    --batch-size 128 \
    --output-dir models/resnet18/clean

# --- ResNet18 Adversarial Training ---
python -m cli.main train adversarial \
    --model resnet18 \
    --defense adversarial_training \
    --pretrained models/resnet18/clean/best.pth \
    --epochs 100 \
    --lr 0.001 \
    --eps 0.0314 \
    --alpha 0.00784 \
    --steps 10 \
    --output-dir models/resnet18/adv/adversarial_training

# --- ResNet18 TRADES Training (Fixed) ---
python -m cli.main train adversarial \
    --model resnet18 \
    --defense trades \
    --pretrained models/resnet18/clean/best.pth \
    --epochs 100 \
    --lr 0.001 \
    --beta 6.0 \
    --eps 0.0314 \
    --alpha 0.00784 \
    --steps 10 \
    --output-dir models/resnet18/adv/trades

# --- ViT-CIFAR-Tiny Clean Training ---
python -m cli.main train clean \
    --model vit_cifar_tiny \
    --epochs 200 \
    --lr 0.001 \
    --batch-size 128 \
    --output-dir models/vit_cifar_tiny/clean

# --- ViT-CIFAR-Tiny Adversarial Training ---
python -m cli.main train adversarial \
    --model vit_cifar_tiny \
    --defense adversarial_training \
    --pretrained models/vit_cifar_tiny/clean/best.pth \
    --epochs 100 \
    --lr 0.001 \
    --eps 0.0314 \
    --alpha 0.00784 \
    --steps 10 \
    --output-dir models/vit_cifar_tiny/adv/adversarial_training

# =============================================================================
# SECTION 2: STATISTICAL VALIDATION (3 RUNS)
# =============================================================================

SEEDS=(42 123 456)

# --- ResNet18 AT (3 runs) ---
for seed in "${SEEDS[@]}"; do
    python -m cli.main train adversarial \
        --model resnet18 \
        --defense adversarial_training \
        --pretrained models/resnet18/clean/best.pth \
        --epochs 100 \
        --lr 0.001 \
        --seed $seed \
        --output-dir models/resnet18/adv/at_seed${seed}
done

# --- ViT-CIFAR-Tiny AT (3 runs) ---
for seed in "${SEEDS[@]}"; do
    python -m cli.main train adversarial \
        --model vit_cifar_tiny \
        --defense adversarial_training \
        --pretrained models/vit_cifar_tiny/clean/best.pth \
        --epochs 100 \
        --lr 0.001 \
        --seed $seed \
        --output-dir models/vit_cifar_tiny/adv/at_seed${seed}
done

# =============================================================================
# SECTION 3: ROBUSTNESS EVALUATION
# =============================================================================

MODELS=(
    "models/resnet18/clean/best.pth:resnet18"
    "models/resnet18/adv/adversarial_training/best.pth:resnet18"
    "models/vit_cifar_tiny/clean/best.pth:vit_cifar_tiny"
    "models/vit_cifar_tiny/adv/adversarial_training/best.pth:vit_cifar_tiny"
)

for model in "${MODELS[@]}"; do
    IFS=":" read -r path type <<< "$model"
    echo "Evaluating: $path"
    python -m cli.main evaluate robustness \
        --model-path "$path" \
        --model-type "$type" \
        --attacks fgsm pgd autoattack \
        --epsilons 0.00784 0.01569 0.0314 0.0627
done

# =============================================================================
# SECTION 4: ANALYSIS SCRIPTS
# =============================================================================

# --- Gradient Analysis ---
python experiments/run_sci_analysis.py --analysis gradient \
    --output-dir results/sci_analysis/gradient

# --- Transfer Attack Analysis ---
python experiments/run_sci_analysis.py --analysis transfer \
    --output-dir results/sci_analysis/transfer

# --- Attention Analysis ---
python experiments/run_sci_analysis.py --analysis attention \
    --output-dir results/sci_analysis/attention

# =============================================================================
# SECTION 5: FIGURE GENERATION
# =============================================================================

# --- Main Robustness Figure ---
python experiments/generate_figures.py --figure robustness \
    --output-path paper/figures/raw/robustness_comparison.pdf

# --- Epsilon Sweep Figure ---
python experiments/generate_figures.py --figure epsilon_sweep \
    --output-path paper/figures/raw/epsilon_sweep.pdf

# --- Transfer Heatmap ---
python experiments/generate_figures.py --figure transfer_heatmap \
    --output-path paper/figures/raw/transfer_heatmap.pdf

# --- Gradient Visualization ---
python experiments/generate_figures.py --figure gradient_viz \
    --output-path paper/figures/raw/gradient_viz.pdf

# --- Attention Comparison ---
python experiments/generate_figures.py --figure attention \
    --output-path paper/figures/raw/attention_comparison.pdf

# =============================================================================
# SECTION 6: STATISTICAL ANALYSIS
# =============================================================================

python experiments/run_statistical_analysis.py \
    --results-dir results/sci_analysis \
    --output-dir paper/supplementary

# =============================================================================
# Notes
# =============================================================================
# - All adversarial training uses: eps=8/255, alpha=2/255, steps=10
# - AutoAttack uses default parameters (Linf)
# - GPU: RTX 5060 Ti (16GB VRAM)
# - Expected total runtime: ~24-30 hours (sequential)
