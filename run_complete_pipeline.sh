#!/bin/bash
#
# Complete Pipeline for SCI Publication
#
# This script trains all necessary models and runs comprehensive analysis
# for the adversarial robustness study comparing CNNs and ViTs.
#
# Requirements:
#   - CUDA-enabled GPU
#   - conda environment with dependencies installed
#
# Usage:
#   chmod +x run_complete_pipeline.sh
#   ./run_complete_pipeline.sh
#

set -e  # Exit on error

echo "========================================"
echo "ADVERSARIAL ROBUSTNESS STUDY PIPELINE"
echo "========================================"
echo ""

# Configuration
EPOCHS_CLEAN=50
EPOCHS_ADV=25
BATCH_SIZE=128
DATA_DIR="./data"
MODEL_DIR="./models"
RESULTS_DIR="./results/sci_paper"

# Check CUDA availability
if ! python3 -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    echo "WARNING: CUDA not available! Training will be very slow on CPU."
    echo "Press Ctrl+C to cancel or wait 5 seconds to continue..."
    sleep 5
fi

# Step 1: Train Clean Models
echo ""
echo "========================================"
echo "STEP 1: TRAINING CLEAN MODELS"
echo "========================================"
echo ""

echo "[1/4] Training ResNet18 (clean)..."
advdefense train clean \
    --model resnet18 \
    --epochs $EPOCHS_CLEAN \
    --batch-size $BATCH_SIZE \
    --data-dir $DATA_DIR \
    --output-dir $MODEL_DIR

echo ""
echo "[2/4] Training ViT-Tiny (clean)..."
advdefense train clean \
    --model vit_tiny \
    --epochs $EPOCHS_CLEAN \
    --batch-size $BATCH_SIZE \
    --data-dir $DATA_DIR \
    --output-dir $MODEL_DIR

echo ""
echo "[3/4] Training DenseNet121 (clean)..."
advdefense train clean \
    --model densenet121 \
    --epochs $EPOCHS_CLEAN \
    --batch-size $BATCH_SIZE \
    --data-dir $DATA_DIR \
    --output-dir $MODEL_DIR

echo ""
echo "Clean models training complete!"
echo ""

# Step 2: Train Adversarial Models
echo "========================================"
echo "STEP 2: TRAINING ADVERSARIAL MODELS"
echo "========================================"
echo ""

echo "[1/3] Training ResNet18 (adversarial)..."
advdefense train adversarial \
    --model resnet18 \
    --defense adversarial_training \
    --epochs $EPOCHS_ADV \
    --batch-size $BATCH_SIZE \
    --eps 0.031372549 \
    --data-dir $DATA_DIR \
    --output-dir $MODEL_DIR

echo ""
echo "[2/3] Training ViT-Tiny (adversarial)..."
advdefense train adversarial \
    --model vit_tiny \
    --defense adversarial_training \
    --epochs $EPOCHS_ADV \
    --batch-size $BATCH_SIZE \
    --eps 0.031372549 \
    --data-dir $DATA_DIR \
    --output-dir $MODEL_DIR

echo ""
echo "[3/3] Training ResNet18 (TRADES)..."
advdefense train adversarial \
    --model resnet18 \
    --defense trades \
    --epochs $EPOCHS_ADV \
    --batch-size $BATCH_SIZE \
    --eps 0.031372549 \
    --beta 6.0 \
    --data-dir $DATA_DIR \
    --output-dir $MODEL_DIR

echo ""
echo "Adversarial models training complete!"
echo ""

# Step 3: Basic Robustness Evaluation
echo "========================================"
echo "STEP 3: BASIC ROBUSTNESS EVALUATION"
echo "========================================"
echo ""

echo "[1/2] Evaluating ResNet18 (clean)..."
advdefense evaluate robustness \
    --model-path $MODEL_DIR/resnet18/clean/best.pth \
    --model-type resnet18 \
    -a fgsm -a pgd -a autoattack \
    --output-dir $RESULTS_DIR/evaluation

echo ""
echo "[2/2] Evaluating ResNet18 (adversarial)..."
advdefense evaluate robustness \
    --model-path $MODEL_DIR/resnet18/adv/adversarial_training/best.pth \
    --model-type resnet18 \
    -a fgsm -a pgd -a autoattack \
    --output-dir $RESULTS_DIR/evaluation

echo ""
echo "Basic evaluation complete!"
echo ""

# Step 4: Comprehensive SCI Analysis
echo "========================================"
echo "STEP 4: COMPREHENSIVE SCI ANALYSIS"
echo "========================================"
echo ""

echo "Running gradient analysis, transfer analysis, and attention analysis..."
python3 experiments/run_sci_analysis.py \
    --experiment all \
    --model-dir $MODEL_DIR \
    --output-dir $RESULTS_DIR \
    --batch-size 64 \
    --num-batches 50 \
    --epsilon 0.031372549 \
    --visualize

echo ""
echo "========================================"
echo "PIPELINE COMPLETE!"
echo "========================================"
echo ""
echo "Results saved to: $RESULTS_DIR"
echo ""
echo "Model checkpoints:"
echo "  - $MODEL_DIR/resnet18/clean/best.pth"
echo "  - $MODEL_DIR/resnet18/adv/adversarial_training/best.pth"
echo "  - $MODEL_DIR/vit_tiny/clean/best.pth"
echo "  - $MODEL_DIR/vit_tiny/adv/adversarial_training/best.pth"
echo ""
echo "Analysis results:"
echo "  - $RESULTS_DIR/gradient_analysis.json"
echo "  - $RESULTS_DIR/transfer_analysis.json"
echo "  - $RESULTS_DIR/attention_analysis.json"
echo "  - $RESULTS_DIR/figures/"
echo ""
echo "You can now use these results for your SCI publication!"
echo ""
