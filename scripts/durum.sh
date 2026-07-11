#!/bin/bash
# Tek bakista pipeline durumu.
# Kullanim: wsl -d Ubuntu-22.04 -- bash ~/projects/adeb_sci_1/scripts/durum.sh
cd /home/firat/projects/adeb_sci_1

echo "==================== PIPELINE DURUM ===================="
echo "--- Adim gecisleri (son 5):"
grep -E 'START|DONE|SKIP|FAIL|TAMAM' logs/revision_pipeline.log 2>/dev/null | tail -5

echo
echo "--- Aktif egitim (son 3 epoch ozeti):"
for L in logs/R1_resnet_at_run3.log logs/R2_vit_at_run3.log; do
    if [ -f "$L" ]; then
        echo "  [$L]"
        grep -a -oE 'Epoch [0-9]+/100 - Loss.*' "$L" | tail -3 | sed 's/^/    /'
        tail -c 800 "$L" | tr '\r' '\n' | grep -aE 'Epoch .*it/s' | tail -1 | sed 's/^/    ANLIK: /'
    fi
done

echo
echo "--- Tamamlanan artefaktlar:"
for f in models/resnet18/adv/at_run3/*/adv/*/TRAINING_COMPLETE \
         models/vit_tiny/adv/at_run3/*/adv/*/TRAINING_COMPLETE \
         results/final_eval/*/*.csv \
         results/epsilon_sweep_run3/*/*.csv \
         results/transfer_analysis_run3/transfer_summary.json \
         results/gradient_analysis_run3/gradient_summary.json \
         results/attention_analysis_run3/attention_summary.json \
         results/statistical_validation_run3/statistical_validation.json \
         results/wrn_eval/wrn_eval_summary.json \
         results/autoattack_run3_full/autoattack_summary.json; do
    [ -e "$f" ] && echo "  OK $f"
done
ls results/autoattack_run3_full/aa_chunk_*.npz 2>/dev/null | wc -l | xargs -I{} echo "  AutoAttack chunk: {}/20"

echo
echo "--- GPU:"
nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader
echo "========================================================"
