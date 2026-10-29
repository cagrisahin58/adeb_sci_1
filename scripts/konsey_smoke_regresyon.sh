#!/bin/bash
# Konsey B1 regresyon: degisiklik oncesi (HEAD, git worktree) ve sonrasi
# c1_c3_transfer_matrix.py, varsayilan bayraklarla, n=200, ayni iki C1 modeli.
# WSL'de firat olarak: bash scripts/konsey_smoke_regresyon.sh
# Worktree depo icinde (_regresyon_wt) cunku konteyner yalniz depoyu goruyor;
# is bitince kaldirilir. Cikti: results/q1/konsey_smoke/regresyon/{eski,yeni,eski2}
set -uo pipefail
cd /home/firat/projects/adeb_sci_1
WT=_regresyon_wt
OUT=results/q1/konsey_smoke/regresyon
git worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "worktree kurulamadi"; exit 1; }
echo "worktree HEAD: $(git -C "$WT" rev-parse --short HEAD)"
ARGS="--dataset cifar10 --n-samples 200 --seed 42 \
 --model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"
run() {  # etiket betik
    local t0=$(date +%s)
    timeout 280 docker exec -w /workspace adeb_eval python "$2" $ARGS --out-dir "$OUT/$1" > "$OUT/$1.log" 2>&1
    echo "$1: rc=$? sure=$(( $(date +%s) - t0 )) s"
}
mkdir -p "$OUT"
run eski "$WT/experiments/c1_c3_transfer_matrix.py"
run yeni experiments/c1_c3_transfer_matrix.py
run eski2 "$WT/experiments/c1_c3_transfer_matrix.py"
git worktree remove --force "$WT" && echo "worktree kaldirildi"
git worktree prune
docker exec -w /workspace adeb_eval python scripts/konsey_smoke_karsilastir.py "$OUT/eski" "$OUT/yeni" --json "$OUT/karsilastirma_eski_yeni.json" | tail -4
docker exec -w /workspace adeb_eval python scripts/konsey_smoke_karsilastir.py "$OUT/eski" "$OUT/eski2" --json "$OUT/karsilastirma_eski_eski2.json" | tail -4
