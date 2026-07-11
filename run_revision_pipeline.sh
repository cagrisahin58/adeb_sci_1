#!/bin/bash
# =============================================================================
# KESINTIYE DAYANIKLI REVIZYON PIPELINE'I (R1-R10)  —  Yol A (run3 retrain)
# Kanonik, okunabilir komut zinciri icin bkz. reproduce_paper.sh
#
# Konteyner icinde /workspace'ten calisir:
#   docker exec adeb_eval bash /workspace/run_revision_pipeline.sh
#
# Her adim bir artefakt-korumasi ile sarilidir: artefakt varsa adim atlanir.
# Elektrik kesintisi sonrasi AYNI komutu yeniden calistirmak yeterlidir:
#   - R1/R2 egitimleri last.pth'tan kaldigi epoch'tan devam eder (--resume)
#   - R5 AutoAttack tamamlanan 1000'lik parcalari atlar (chunk npz)
#   - Digerleri ya tamamlanmistir (atlanir) ya bastan kosulur (kisa adimlar)
# =============================================================================
set -uo pipefail
cd /workspace

MASTER_LOG=logs/revision_pipeline.log
mkdir -p logs results

R3NET_DIR=models/resnet18/adv/at_run3/resnet18/adv/adversarial_training
V3IT_DIR=models/vit_tiny/adv/at_run3/vit_tiny/adv/adversarial_training
R3NET=$R3NET_DIR/best.pth
V3IT=$V3IT_DIR/best.pth

EPS8=0.03137254901960784
EPS2=0.00784313725490196
EPS4=0.01568627450980392
EPS16=0.06274509803921569

log() { echo "[$(date '+%F %T')] $*" | tee -a "$MASTER_LOG"; }

# run_step <ad> <koruma-dosyasi> <komut...>
run_step() {
    local name="$1"; local guard="$2"; shift 2
    if [ -e "$guard" ]; then
        log "SKIP  $name (artefakt mevcut: $guard)"
        return 0
    fi
    log "START $name"
    if "$@" >> "logs/${name}.log" 2>&1; then
        if [ -e "$guard" ]; then
            log "DONE  $name"
        else
            log "FAIL  $name: komut bitti ama artefakt olusmadi ($guard). logs/${name}.log kontrol edin."
            exit 1
        fi
    else
        log "FAIL  $name (exit $?). logs/${name}.log kontrol edin."
        exit 1
    fi
}

log "================ PIPELINE BASLANGIC ================"
nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader | tee -a "$MASTER_LOG"

# --- R1: ResNet18 AT run3 (M10 duzeltmesiyle, val-split secimli) ------------
run_step R1_resnet_at_run3 "$R3NET_DIR/TRAINING_COMPLETE" \
    python -m cli.main train adversarial \
        --model resnet18 --defense adversarial_training \
        --pretrained models/resnet18/clean/best.pth \
        --epochs 100 --lr 0.001 --batch-size 128 \
        --eps $EPS8 --alpha $EPS2 --steps 10 \
        --patience 20 --val-split 2000 --seed 42 \
        --output-dir models/resnet18/adv/at_run3 --resume

# --- R2: ViT-Tiny AT run3 ----------------------------------------------------
run_step R2_vit_at_run3 "$V3IT_DIR/TRAINING_COMPLETE" \
    python -m cli.main train adversarial \
        --model vit_tiny --defense adversarial_training \
        --pretrained models/vit_tiny/clean/best.pth \
        --epochs 100 --lr 0.001 --batch-size 64 \
        --eps $EPS8 --alpha $EPS2 --steps 10 \
        --patience 20 --val-split 2000 --seed 123 \
        --output-dir models/vit_tiny/adv/at_run3 --resume

# --- R3: Tek tutarli post-hoc degerlendirme (tam test, clean+FGSM+PGD-10) ---
run_step R3_eval_resnet_at "results/final_eval/resnet18_at/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$R3NET" -t resnet18 \
        -a fgsm -a pgd -e $EPS8 -o results/final_eval/resnet18_at

run_step R3_eval_vit_at "results/final_eval/vit_tiny_at/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$V3IT" -t vit_tiny \
        -a fgsm -a pgd -e $EPS8 -o results/final_eval/vit_tiny_at

run_step R3_eval_resnet_clean "results/final_eval/resnet18_clean/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m models/resnet18/clean/best.pth -t resnet18 \
        -a fgsm -a pgd -e $EPS8 -o results/final_eval/resnet18_clean

run_step R3_eval_vit_clean "results/final_eval/vit_tiny_clean/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m models/vit_tiny/clean/best.pth -t vit_tiny \
        -a fgsm -a pgd -e $EPS8 -o results/final_eval/vit_tiny_clean

# --- R4: Gercek epsilon taramasi (fig2 icin) ---------------------------------
run_step R4_sweep_resnet "results/epsilon_sweep_run3/resnet18/resnet18_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$R3NET" -t resnet18 \
        -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 \
        -o results/epsilon_sweep_run3/resnet18

run_step R4_sweep_vit "results/epsilon_sweep_run3/vit_tiny/vit_tiny_robustness_results.csv" \
    python -m cli.main evaluate robustness -m "$V3IT" -t vit_tiny \
        -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 \
        -o results/epsilon_sweep_run3/vit_tiny

# --- R6: Kosullu transfer analizi (n=10000, per-sample log + bootstrap CI) ---
run_step R6_transfer "results/transfer_analysis_run3/transfer_summary.json" \
    python experiments/run_all_analyses_run2.py --only transfer \
        --n-samples 10000 --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- R7: Gradient analizi (olcek-bagimsiz metrikler + native-ViT kontrolu) ---
run_step R7_gradient "results/gradient_analysis_run3/gradient_summary.json" \
    python experiments/run_all_analyses_run2.py --only gradient \
        --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- R8a: Feature degradation (tam n=100) ------------------------------------
run_step R8a_attention "results/attention_analysis_run3/attention_summary.json" \
    python experiments/run_all_analyses_run2.py --only attention \
        --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- R10: Istatistiksel dogrulama (3 eval seed, run3 modelleri) --------------
run_step R10_statistical "results/statistical_validation_run3/statistical_validation.json" \
    python experiments/run_all_analyses_run2.py --only statistical \
        --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- R9: WRN-28-10 yerel degerlendirme (Tablo 1 satiri + fig1/fig2 WRN) ------
run_step R9_wrn_eval "results/wrn_eval/wrn_eval_summary.json" \
    python experiments/run_wrn_eval.py --n-samples 10000 --seed 42

# --- R5: Tam-test AutoAttack (chunk'li kesinti-guvenli, McNemar dahil) -------
# En uzun adim (~10-14 saat) — bilerek sona alindi: kesintide diger tum
# artefaktlar tamamlanmis olur, AA da kendi chunk'larindan devam eder.
run_step R5_autoattack "results/autoattack_run3_full/autoattack_summary.json" \
    python -u experiments/run_autoattack_run2.py \
        --n-samples 10000 --seed 42 --chunk-size 1000 \
        --output-dir results/autoattack_run3_full \
        --resnet-path "$R3NET" --vit-path "$V3IT"

# --- R8b: Tum figurleri GERCEK artefaktlardan yeniden uret -------------------
log "START R8b_figures"
if python paper/figures/generate_advanced_figures.py >> logs/R8b_figures.log 2>&1 \
   && python paper/figures/generate_from_experiments.py --all >> logs/R8b_figures.log 2>&1; then
    mkdir -p paper/figures/final
    cp -v paper/figures/raw/fig*.pdf paper/figures/final/ >> logs/R8b_figures.log 2>&1 || true
    log "DONE  R8b_figures (final/ guncellendi)"
else
    log "FAIL  R8b_figures. logs/R8b_figures.log kontrol edin."
    exit 1
fi

log "================ PIPELINE TAMAM ================"
log "Ozet artefaktlar:"
for f in results/final_eval/*/*.csv results/transfer_analysis_run3/transfer_summary.json \
         results/gradient_analysis_run3/gradient_summary.json \
         results/autoattack_run3_full/autoattack_summary.json \
         results/wrn_eval/wrn_eval_summary.json; do
    [ -e "$f" ] && log "  OK $f"
done
log "SONRAKI ADIM: makaledeki % TODO(run3) isaretli yerleri yeni sayilarla guncelle."
