#!/usr/bin/env bash
# E3 A KOLU (kontrollu) surucusu -- ASIMETRI yayilimi, yorunge boyunca.
#
# Her tohum cifti icin IKI tarama yapilir:
#   (1) ResNet yorungesi taranir, ViT SABIT es
#   (2) ViT yorungesi taranir, ResNet SABIT es
# Boylece ciftin temiz hata FARKI degisirken mimari cifti, tohum, veri kumesi
# ve saldiri butcesi SABIT kalir -- B kolunun (gozlemsel) saglayamadigi kontrol.
#
# Kosum:  bash scripts/q1_e3_akolu_run.sh [stride]
# Varsayilan stride 10 (yorunge basina ~10-11 nokta).
set -u
cd "$(dirname "$0")/.." || exit 1
DEX=(docker exec -w /workspace adeb_eval)
STRIDE="${1:-10}"
ARC=results/q1/adv_archive
PTS=results/q1/e3_akolu
log() { echo "[$(date '+%F %T')] === $* ==="; }

mkdir -p "$ARC" "$PTS"

arsivle() {  # $1=etiket $2=tip $3=ckpt $4=dataset
    local o="$ARC/$1.npz"
    if [ -f "$o" ]; then echo "  SKIP arsiv $1"; return 0; fi
    if [ ! -f "$3" ]; then echo "  ATLA arsiv $1 (ckpt yok: $3)"; return 1; fi
    "${DEX[@]}" python -B scripts/q1_archive_adv.py --model-type "$2" --ckpt "$3" \
        --dataset "$4" --out "$o" >/dev/null || { echo "  FAIL arsiv $1"; return 1; }
    echo "  arsivlendi $1"
}

tara() {  # $1=traj_id $2=epochs_dir $3=model_type $4=partner_ckpt $5=partner_type
          # $6=partner_arsiv $7=dataset $8=kume
    if [ ! -d "$2" ]; then echo "  ATLA $1 (epochs yok: $2)"; return 1; fi
    if [ ! -f "$ARC/$6.npz" ]; then echo "  ATLA $1 (arsiv yok: $6)"; return 1; fi
    "${DEX[@]}" python -B scripts/q1_e3_akolu.py \
        --epochs-dir "$2" --model-type "$3" \
        --partner-ckpt "$4" --partner-type "$5" \
        --partner-archive "$ARC/$6.npz" \
        --dataset "$7" --trajectory-id "$1" --cluster "$8" \
        --stride "$STRIDE" --out-dir "$PTS" || { echo "  FAIL $1"; return 1; }
}

# ---------------------------------------------------------------- CIFAR-10 (E2)
log "CIFAR-10 (E2 yorungeleri)"
for i in 1 2 3; do
    rs=$((1000 + i)); vs=$((2000 + i))
    RN=models/c1/resnet18_s${rs}/resnet18/adv/adversarial_training/best.pth
    VT=models/c1/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/best.pth
    arsivle "c10_rn18_s${rs}" resnet18 "$RN" cifar10
    arsivle "c10_vit_s${vs}"  vit_tiny "$VT" cifar10
    tara "A_c10_rn18_s${rs}" \
         "models/q1/e2/resnet18_s${rs}/resnet18/adv/adversarial_training/epochs" \
         resnet18 "$VT" vit_tiny "c10_vit_s${vs}" cifar10 "c10_pair${i}"
    tara "A_c10_vit_s${vs}" \
         "models/q1/e2/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/epochs" \
         vit_tiny "$RN" resnet18 "c10_rn18_s${rs}" cifar10 "c10_pair${i}"
done

# --------------------------------------------------------------- CIFAR-100 (E1)
log "CIFAR-100 (E1 yorungeleri)"
for i in 1 2 3; do
    rs=$((1000 + i)); vs=$((2000 + i))
    RN=models/q1/cifar100/resnet18_s${rs}/resnet18/adv/adversarial_training/best.pth
    VT=models/q1/cifar100/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/best.pth
    arsivle "c100_rn18_s${rs}" resnet18 "$RN" cifar100
    arsivle "c100_vit_s${vs}"  vit_tiny "$VT" cifar100
    tara "A_c100_rn18_s${rs}" \
         "models/q1/cifar100/resnet18_s${rs}/resnet18/adv/adversarial_training/epochs" \
         resnet18 "$VT" vit_tiny "c100_vit_s${vs}" cifar100 "c100_pair${i}"
    tara "A_c100_vit_s${vs}" \
         "models/q1/cifar100/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/epochs" \
         vit_tiny "$RN" resnet18 "c100_rn18_s${rs}" cifar100 "c100_pair${i}"
done

# -------------------------------------------------------------------- SVHN (E7)
# E7 bitmemisse SESSIZ atlanmaz; ekrana yazilir (K6: bitmislik kaniti gerekir).
log "SVHN (E7 yorungeleri)"
for i in 1 2; do
    rs=$((1000 + i)); vs=$((2000 + i))
    RN=models/q1/svhn/resnet18_s${rs}/resnet18/adv/adversarial_training/best.pth
    VT=models/q1/svhn/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/best.pth
    RN_OK=models/q1/svhn/resnet18_s${rs}/resnet18/adv/adversarial_training/TRAINING_COMPLETE
    VT_OK=models/q1/svhn/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/TRAINING_COMPLETE
    if [ ! -f "$RN_OK" ] || [ ! -f "$VT_OK" ]; then
        echo "  ATLANDI svhn cift${i}: egitim BITMEMIS (TRAINING_COMPLETE yok)."
        echo "    (best.pth VARLIGI bitmislik kaniti DEGILDIR -- K6)"
        continue
    fi
    arsivle "svhn_rn18_s${rs}" resnet18 "$RN" svhn
    arsivle "svhn_vit_s${vs}"  vit_tiny "$VT" svhn
    tara "A_svhn_rn18_s${rs}" \
         "models/q1/svhn/resnet18_s${rs}/resnet18/adv/adversarial_training/epochs" \
         resnet18 "$VT" vit_tiny "svhn_vit_s${vs}" svhn "svhn_pair${i}"
    tara "A_svhn_vit_s${vs}" \
         "models/q1/svhn/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/epochs" \
         vit_tiny "$RN" resnet18 "svhn_rn18_s${rs}" svhn "svhn_pair${i}"
done

log "A kolu noktalari: $(ls "$PTS"/*.json 2>/dev/null | wc -l)"
log "SIRADAKI: docker exec -w /workspace adeb_eval python -B scripts/q1_e3_iki_kol_fit.py"
