#!/usr/bin/env bash
# LeCun plani Faz 2.1 + 2.2 (2026-10-04). Egitim yok; yalniz transfer degerlendirmesi, ornek bazinda kayit.
#  2.1 Temiz egitilmis C1 ciftleri (3 cift) + standart egitimli RobustBench 'Standard' WRN-28-10
#      -> p (standart hedefte), ozdeslik artigi, dort protokol.   results/q1/temiz_ciftler/pair{1,2,3}
#  2.2 Genisletilmis CIFAR-10 havuzu: C1 cift 1 (AT) + alti RobustBench modeli (farkli mimari ve temiz
#      dogruluk) -> tum ciftlerde dort protokol, p, artik, yayilim-temiz fark iliskisi.
#      results/q1/havuz_cifar10
# Konteynerde arka planda: docker exec -d -w /workspace adeb_eval bash scripts/q1_temiz_ve_havuz_run.sh
set -u
cd /workspace || exit 1
LOG=logs/q1_temiz_ve_havuz.log
mkdir -p logs
{
echo "BASLADI $(date -u +%FT%TZ)"
for p in 1 2 3; do
    rs=$((1000 + p)); vs=$((2000 + p))
    out="results/q1/temiz_ciftler/pair${p}"
    echo "== 2.1 pair${p} -> ${out}"
    python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 \
        --model "ResNet18_clean:resnet18:models/c1/resnet18_s${rs}/resnet18/clean/best.pth" \
        --model "ViT_Tiny_clean:vit_tiny:models/c1/vit_tiny_s${vs}/vit_tiny/clean/best.pth" \
        --rb-model "Standard:Standard_WRN28_10" \
        --out-dir "$out"
done
echo "== 2.2 havuz -> results/q1/havuz_cifar10"
python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 \
    --model "ResNet18_AT:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth" \
    --model "ViT_Tiny_AT:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth" \
    --rb-model "Standard:Standard_WRN28_10" \
    --rb-model "Wong2020Fast:Wong2020_PRN18" \
    --rb-model "Engstrom2019Robustness:Engstrom2019_RN50" \
    --rb-model "Carmon2019Unlabeled:Carmon2019_WRN28_10" \
    --rb-model "Debenedetti2022Light_XCiT-S12:Debenedetti2022_XCiT_S12" \
    --rb-model "Gowal2020Uncovering_28_10_extra:Gowal2020_WRN28_10" \
    --out-dir results/q1/havuz_cifar10
echo "BITTI $(date -u +%FT%TZ)"
} >> "$LOG" 2>&1
