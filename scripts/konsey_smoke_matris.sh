#!/bin/bash
# Konsey B1 smoke: yeni transfer matrisi bayraklari (n=200). Konteynerde:
#   docker exec -w /workspace adeb_eval bash scripts/konsey_smoke_matris.sh <adim>
# adimlar: uc | tekrar | ekle | taze | mi | tgr | mi_esit
# Cikti: results/q1/konsey_smoke/matris_*/ ve .log
set -uo pipefail
cd /workspace
S=results/q1/konsey_smoke
C=$S/adv_onbellek
R224="R224_scr_smoke:resnet18_224:models/q1/konsey_smoke/r_scr/resnet18_224/clean/best.pth"
VIT="ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"
RES="ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth"
VIN="V_IN_smoke:vit_tiny_in1k:models/q1/konsey_smoke/v_in/vit_tiny_in1k/clean/best.pth"
M="python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 200 --seed 42"
t0=$(date +%s)
case "$1" in
  uc)      # 3 model: resnet18_224 + C1 ViT + yeni RobustBench; onbellek yazar
    $M --model "$R224" --model "$VIT" --rb-model Sehwag2021Proxy_R18 \
       --cache-adv $C --out-dir $S/matris_uc > $S/matris_uc.log 2>&1 ;;
  tekrar)  # ayni kosu, onbellekten (saldiri yok) -> matris_uc ile birebir olmali
    $M --model "$R224" --model "$VIT" --rb-model Sehwag2021Proxy_R18 \
       --cache-adv $C --out-dir $S/matris_uc_tekrar > $S/matris_uc_tekrar.log 2>&1 ;;
  ekle)    # B2 -> B4 akisi: matris_uc kopyasina iki model ekle, --skip-existing
    rm -rf $S/matris_ekle; cp -r $S/matris_uc $S/matris_ekle; rm -f $S/matris_ekle/transfer_matrix.json
    $M --model "$R224" --model "$VIT" --rb-model Sehwag2021Proxy_R18 \
       --model "$VIN" --rb-model Debenedetti2022Light_XCiT-S12 \
       --cache-adv $C --skip-existing --out-dir $S/matris_ekle > $S/matris_ekle.log 2>&1 ;;
  taze)    # ayni 5 model, bos klasor, ayni onbellek -> matris_ekle ile birebir olmali
    rm -rf $S/matris_taze
    $M --model "$R224" --model "$VIT" --rb-model Sehwag2021Proxy_R18 \
       --model "$VIN" --rb-model Debenedetti2022Light_XCiT-S12 \
       --cache-adv $C --out-dir $S/matris_taze > $S/matris_taze.log 2>&1 ;;
  mi)      # MI-PGD, tek kaynak (C1 ResNet), hedefler hepsi
    $M --model "$RES" --model "$VIT" --rb-model Sehwag2021Proxy_R18 \
       --attack mi --sources ResNet18_AT_s1001 --out-dir $S/matris_mi > $S/matris_mi.log 2>&1 ;;
  tgr)     # TGR: ViT kaynaklari (C1 ViT ve vit_tiny_in1k); ResNet kaynak listesinden duser
    $M --model "$RES" --model "$VIT" --model "$VIN" \
       --attack tgr --out-dir $S/matris_tgr > $S/matris_tgr.log 2>&1 ;;
  mi_esit) # mifgsm_m84 == run_c_addenda.mifgsm (C22) ve TGR yolu == c1_c2_tgr.mifgsm
    python scripts/konsey_smoke_mi_esit.py > $S/mi_tgr_esitlik.log 2>&1 ;;
esac
rc=$?
echo "$1: rc=$rc sure=$(( $(date +%s) - t0 )) s"
