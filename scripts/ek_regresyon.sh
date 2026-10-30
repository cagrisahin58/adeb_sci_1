#!/bin/bash
# Ek catal regresyonu (30.10.2026): experiments/q1_ek_transfer_matrix.py varsayilan bayraklarla
# ozgun experiments/c1_c3_transfer_matrix.py ile hucre hucre ve ornek ornek ayni ciktiyi vermeli.
# Ozgun betik dondurulmustur; bu betik ona yalniz okumak ve calistirmak icin dokunur.
#
# WSL'de firat olarak, depo kokunden:
#   bash scripts/ek_regresyon.sh cpu 200 onb  # GPU mesgulken (B3 zinciri) CPU; onb: onbellekli ikinci karsilastirma
#   bash scripts/ek_regresyon.sh gpu 200    # zincir bittikten sonra, B4/B5 ile ayni kosullarda
# gpu kipi ayrica konsey bayraklariyla (--cache-adv, kaynak basina tohum) ikinci bir karsilastirma yapar.
# Cikti: results/q1/ek_regresyon/<kip>_n<N>/{ozgun,catal,...}, karsilastirma_*.json (BIREBIR alani).
set -uo pipefail
cd /home/firat/projects/adeb_sci_1
KIP=${1:-gpu}
N=${2:-200}
OUT=results/q1/ek_regresyon/${KIP}_n${N}
ENVS=(-e PYTHONDONTWRITEBYTECODE=1)
if [ "$KIP" = "cpu" ]; then
    ENVS+=(-e CUDA_VISIBLE_DEVICES= -e OMP_NUM_THREADS=4)
else
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader
    if pgrep -f "konsey_tam_zincir|konsey_b3|cli.main train" >/dev/null; then
        echo "UYARI: egitim sureci calisiyor gibi; GPU kipini zincir bittikten sonra kosun"; exit 2
    fi
fi
echo "ozgun sha256: $(sha256sum experiments/c1_c3_transfer_matrix.py | cut -c1-64)"
echo "catal sha256: $(sha256sum experiments/q1_ek_transfer_matrix.py | cut -c1-64)"
ARGS="--dataset cifar10 --n-samples $N --seed 42 \
 --model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"
mkdir -p "$OUT"
run() {  # etiket betik [ek argumanlar]
    local t0=$(date +%s) tag=$1 sc=$2; shift 2
    docker exec "${ENVS[@]}" -w /workspace adeb_eval nice -n 10 python -B "$sc" $ARGS "$@" --out-dir "$OUT/$tag" > "$OUT/$tag.log" 2>&1
    echo "$tag: rc=$? sure=$(( $(date +%s) - t0 )) s"
}
cmp_() {
    docker exec "${ENVS[@]}" -w /workspace adeb_eval python -B scripts/konsey_smoke_karsilastir.py \
        "$OUT/$1" "$OUT/$2" --json "$OUT/karsilastirma_$1_$2.json" | tail -3
}
run ozgun experiments/c1_c3_transfer_matrix.py
run catal experiments/q1_ek_transfer_matrix.py
cmp_ ozgun catal
if [ "$KIP" = "gpu" ] || [ "${3:-}" = "onb" ]; then
    run ozgun_onb experiments/c1_c3_transfer_matrix.py --cache-adv "$OUT/onb_ozgun"
    run catal_onb experiments/q1_ek_transfer_matrix.py --cache-adv "$OUT/onb_catal"
    cmp_ ozgun_onb catal_onb
    # onbellek dosyalari da ayni olmali (ayni ad, ayni bayt)
    (cd "$OUT" && for f in onb_ozgun/*.npy; do b=$(basename "$f"); cmp -s "$f" "onb_catal/$b" && echo "ayni $b" || echo "FARKLI $b"; done)
fi
docker exec adeb_eval chown -R 1000:1000 /workspace/results/q1/ek_regresyon
echo "bitti: $OUT"
