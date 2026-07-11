#!/bin/bash
# =============================================================================
# REPRODUCE_PAPER.SH — Makaledeki tum sayilarin kanonik uretim zinciri
#
# Bu betik, IEEE Access makalesindeki Tablo 1-5 ve tum figurlerin uretildigi
# TAM komut zincirini belgeler. run_revision_pipeline.sh ayni zinciri
# kesintiye dayanikli (idempotent, artefakt-korumali) bicimde kosar; bu dosya
# okunabilir referanstir ve dogrudan da calistirilabilir.
#
# NOT: run_complete_pipeline.sh ESKIDIR (on-calisma protokolu: 50/25 epoch,
# patience yok) ve makale protokolunu URETMEZ; kullanmayin.
#
# Ortam: PyTorch 2.6.0 + CUDA 12.8 konteyneri (adeb_eval), /workspace = repo koku.
# Egitim seed'leri: ResNet-18 -> 42, ViT-Tiny -> 123 (validasyon bolmesi
# egitim seed'inden turetilir; iki model FARKLI sabit 2000'lik bolme kullanir).
# Analiz/degerlendirme seed'i: 42. Girdiler [0,1] ham piksel uzayindadir
# (mean/std normalizasyonu YOKTUR); eps butceleri bu uzayda tanimlidir.
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"

EPS8=0.03137254901960784
EPS2=0.00784313725490196
EPS4=0.01568627450980392
EPS16=0.06274509803921569

R3NET=models/resnet18/adv/at_run3/resnet18/adv/adversarial_training/best.pth
V3IT=models/vit_tiny/adv/at_run3/vit_tiny/adv/adversarial_training/best.pth

# --- 1. Adversarial training (Tablo 1 modelleri) -----------------------------
python -m cli.main train adversarial \
    --model resnet18 --defense adversarial_training \
    --pretrained models/resnet18/clean/best.pth \
    --epochs 100 --lr 0.001 --batch-size 128 \
    --eps $EPS8 --alpha $EPS2 --steps 10 \
    --patience 20 --val-split 2000 --seed 42 \
    --output-dir models/resnet18/adv/at_run3 --resume

python -m cli.main train adversarial \
    --model vit_tiny --defense adversarial_training \
    --pretrained models/vit_tiny/clean/best.pth \
    --epochs 100 --lr 0.001 --batch-size 64 \
    --eps $EPS8 --alpha $EPS2 --steps 10 \
    --patience 20 --val-split 2000 --seed 123 \
    --output-dir models/vit_tiny/adv/at_run3 --resume

# --- 2. Tablo 1: tam-test clean/FGSM/PGD-10 ----------------------------------
# NOT: click multiple flag'leri tekrarlanmali (-a fgsm -a pgd); bosluklu liste
# parse edilmez.
python -m cli.main evaluate robustness -m "$R3NET" -t resnet18 \
    -a fgsm -a pgd -e $EPS8 -o results/final_eval/resnet18_at
python -m cli.main evaluate robustness -m "$V3IT" -t vit_tiny \
    -a fgsm -a pgd -e $EPS8 -o results/final_eval/vit_tiny_at
python -m cli.main evaluate robustness -m models/resnet18/clean/best.pth -t resnet18 \
    -a fgsm -a pgd -e $EPS8 -o results/final_eval/resnet18_clean
python -m cli.main evaluate robustness -m models/vit_tiny/clean/best.pth -t vit_tiny \
    -a fgsm -a pgd -e $EPS8 -o results/final_eval/vit_tiny_clean

# --- 3. Sekil 2: epsilon taramasi --------------------------------------------
python -m cli.main evaluate robustness -m "$R3NET" -t resnet18 \
    -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 -o results/epsilon_sweep_run3/resnet18
python -m cli.main evaluate robustness -m "$V3IT" -t vit_tiny \
    -a pgd -e $EPS2 -e $EPS4 -e $EPS8 -e $EPS16 -o results/epsilon_sweep_run3/vit_tiny

# --- 4. Tablo 1 (AA sutunu) + McNemar: tam-test AutoAttack (chunk'li) --------
python experiments/run_autoattack_run2.py \
    --n-samples 10000 --seed 42 --chunk-size 1000 \
    --output-dir results/autoattack_run3_full \
    --resnet-path "$R3NET" --vit-path "$V3IT"

# --- 5. Tablo 2: kosullu transfer (per-sample log + bootstrap CI) ------------
python experiments/run_all_analyses_run2.py --only transfer \
    --n-samples 10000 --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- 6. Tablo 3: gradient analizi (olcek-bagimsiz + native-ViT kontrolu) -----
python experiments/run_all_analyses_run2.py --only gradient \
    --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- 7. Tablo 4: feature degradation -----------------------------------------
python experiments/run_all_analyses_run2.py --only attention \
    --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- 8. Tablo 5: istatistiksel dogrulama (3 saldiri-seed'i) -------------------
python experiments/run_all_analyses_run2.py --only statistical \
    --seed 42 --resnet-path "$R3NET" --vit-path "$V3IT"

# --- 9. Tablo 1 WRN satiri + Sekil 1/2 WRN serileri --------------------------
python experiments/run_wrn_eval.py --n-samples 10000 --seed 42

# --- 10. Ek istatistikler (TOST, Welch, entropi nicelemesi) -------------------
python experiments/run_stat_addendum.py

# --- 11. Figurler (yalniz gercek artefakttan; eksik artefakt = hata) ----------
python paper/figures/generate_advanced_figures.py
python paper/figures/generate_from_experiments.py --all
cp paper/figures/raw/fig*.pdf paper/figures/final/

# --- 12. Makale derleme -------------------------------------------------------
# (WSL host'ta: bash -lc "cd paper/manuscript && latexmk -pdf main.tex")
echo "REPRODUCTION CHAIN COMPLETE"
