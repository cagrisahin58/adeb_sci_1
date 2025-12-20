#!/bin/bash
#
# Quick Test Script - Test without training
#
# This script tests the analysis pipeline with untrained (random) models
# to verify everything works before spending time on full training.
#
# Usage:
#   chmod +x quick_test.sh
#   ./quick_test.sh
#

set -e

echo "========================================"
echo "QUICK TEST (No Training Required)"
echo "========================================"
echo ""

echo "Testing analysis pipeline with random initialized models..."
echo ""

# Run analysis with random models (no model-dir specified)
python3 experiments/run_sci_analysis.py \
    --experiment all \
    --batch-size 16 \
    --num-batches 2 \
    --epsilon 0.031372549 \
    --visualize

echo ""
echo "========================================"
echo "QUICK TEST COMPLETE!"
echo "========================================"
echo ""
echo "If this ran without errors, you can proceed with full training."
echo "Run: ./run_complete_pipeline.sh"
echo ""
