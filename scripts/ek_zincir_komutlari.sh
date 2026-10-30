#!/bin/bash
# Ek bloklar B8, B9, B10 icin kosu sirasi (30.10.2026). KULLANICI tmux'ta baslatir; ajan baslatmaz.
# Belirtim: raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md §10 (sira: B8 denetimi, B9, B8, B10).
# On kosullar (fable karari E7):
#   1) scripts/konsey_tam_zincir.sh (B3-B6) bitmis olmali;
#   2) adeb_eval konteyneri /mnt/d/adeb_sci_1_veri baglamasiyla yeniden kurulmus olmali
#      (raporlar/konsey_2026-10-29/07_disk_D_plani.md §4);
#   3) ek on kayit ve hucre_tablosu_b8.json / hucre_tablosu_b9.json dondurulmus (commit edilmis) olmali.
# Kullanim (WSL, depo koku):  bash scripts/ek_zincir_komutlari.sh [adim ...]
#   adimlar: regresyon b8denetim b9 b8 b10 cozumleme   (bossa hepsi, bu sirayla)
# b8denetim'den sonra durup denetim sonucunu ek on kayit §5.5 kuralina gore okumak ve sapma kaydina
# yazmak gerekir; bu yuzden onerilen kullanim iki parcadir:
#   bash scripts/ek_zincir_komutlari.sh regresyon b8denetim
#   bash scripts/ek_zincir_komutlari.sh b9 b8 b10 cozumleme
# Gunlukler: results/q1/ek_loglar/ (logs/ klasorune yazilmaz). Onbellekler D diskinde (float32).
set -uo pipefail
cd /home/firat/projects/adeb_sci_1
LOG=results/q1/ek_loglar
ONB=/mnt/d/adeb_sci_1_veri/onbellek
mkdir -p "$LOG" "$ONB"
DX="docker exec -w /workspace adeb_eval"
B8D=results/q1/konsey_b8_imagenetv2
B9D=results/q1/konsey_b9_c100
B10D=results/q1/konsey_b10_gradyan

bekci() {
    if pgrep -f "konsey_tam_zincir|konsey_b3|cli.main train" >/dev/null; then
        echo "DUR: egitim/zincir sureci calisiyor"; exit 2; fi
    $DX test -r /workspace/data/imagenetv2/imagenetv2-matched-frequency-format-val/0 \
        || { echo "DUR: konteyner /mnt/d'yi gormuyor (07_disk_D_plani.md §4)"; exit 3; }
    bos=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
    [ "${bos:-0}" -ge 12000 ] || { echo "DUR: bos VRAM ${bos} MiB < 12000"; exit 4; }
    [ "$(sha256sum experiments/c1_c3_transfer_matrix.py | cut -c1-64)" = f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7 ] \
        || { echo "DUR: ozgun matris betigi degismis"; exit 5; }
    [ "$(sha256sum experiments/q1_konsey_ayrisim.py | cut -c1-64)" = 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 ] \
        || { echo "DUR: dondurulmus cozumleme betigi degismis"; exit 5; }
}

C100="--model C100_ResNet18_AT_s1001:resnet18:models/q1/cifar100/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
 --model C100_ResNet18_AT_s1002:resnet18:models/q1/cifar100/resnet18_s1002/resnet18/adv/adversarial_training/best.pth \
 --model C100_ResNet18_AT_s1003:resnet18:models/q1/cifar100/resnet18_s1003/resnet18/adv/adversarial_training/best.pth \
 --model C100_ViT_Tiny_AT_s2001:vit_tiny:models/q1/cifar100/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth \
 --model C100_ViT_Tiny_AT_s2002:vit_tiny:models/q1/cifar100/vit_tiny_s2002/vit_tiny/adv/adversarial_training/best.pth \
 --model C100_ViT_Tiny_AT_s2003:vit_tiny:models/q1/cifar100/vit_tiny_s2003/vit_tiny/adv/adversarial_training/best.pth \
 --rb-model Rice2020Overfitting:C100_Rice2020Overfitting --rb-model Rade2021Helper_R18_ddpm:C100_Rade2021Helper_R18_ddpm \
 --rb-model Addepalli2022Efficient_RN18:C100_Addepalli2022Efficient_RN18 --rb-model Sehwag2021Proxy:C100_Sehwag2021Proxy \
 --rb-model Pang2022Robustness_WRN28_10:C100_Pang2022Robustness_WRN28_10 \
 --rb-model Wang2023Better_WRN-28-10:C100_Wang2023Better_WRN-28-10 --rb-model Jia2022LAS-AT_34_10:C100_Jia2022LAS-AT_34_10 \
 --rb-model Debenedetti2022Light_XCiT-S12:C100_Debenedetti2022Light_XCiT-S12 --rb-model Hendrycks2019Using:C100_Hendrycks2019Using"
# B8: 14 model (denetimde biri elenirse bu liste T gorulmeden duzeltilir; yedek IN_Wong2020Fast)
IN14="--rb-model Salman2020Do_R18:IN_Salman2020Do_R18 --rb-model Salman2020Do_R50:IN_Salman2020Do_R50 \
 --rb-model Salman2020Do_50_2:IN_Salman2020Do_50_2 --rb-model Engstrom2019Robustness:IN_Engstrom2019Robustness \
 --rb-model Chen2024Data_WRN_50_2:IN_Chen2024Data_WRN_50_2 --rb-model Peng2023Robust:IN_Peng2023Robust \
 --rb-model Singh2023Revisiting_ConvNeXt-T-ConvStem:IN_Singh_ConvNeXt-T-CvSt \
 --rb-model Singh2023Revisiting_ViT-S-ConvStem:IN_Singh_ViT-S-CvSt \
 --rb-model Singh2023Revisiting_ConvNeXt-B-ConvStem:IN_Singh_ConvNeXt-B-CvSt \
 --rb-model Singh2023Revisiting_ViT-B-ConvStem:IN_Singh_ViT-B-CvSt \
 --rb-model Liu2023Comprehensive_ConvNeXt-B:IN_Liu_ConvNeXt-B --rb-model Liu2023Comprehensive_Swin-B:IN_Liu_Swin-B \
 --rb-model Mo2022When_ViT-B:IN_Mo_ViT-B --rb-model Debenedetti2022Light_XCiT-S12:IN_Debenedetti_XCiT-S12"
YEDEK_IN="--rb-model Wong2020Fast:IN_Wong2020Fast"
IN_ORTAK="--dataset imagenetv2 --v2-kok data/imagenetv2 --in-onisleme BicubicRes256Crop224 --n-samples 2000 --seed 42 --eps 4 --alpha 1 --batch-size 25"
# B10 CIFAR-10: B4'un 20 modeli (scripts/konsey_tam_zincir.sh CMD_B4 ile ayni liste ve takma adlar)
C10="--model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
 --model ResNet18_AT_s1002:resnet18:models/c1/resnet18_s1002/resnet18/adv/adversarial_training/best.pth \
 --model ResNet18_AT_s1003:resnet18:models/c1/resnet18_s1003/resnet18/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2002:vit_tiny:models/c1/vit_tiny_s2002/vit_tiny/adv/adversarial_training/best.pth \
 --model ViT_Tiny_AT_s2003:vit_tiny:models/c1/vit_tiny_s2003/vit_tiny/adv/adversarial_training/best.pth \
 --model V_IN_s2101:vit_tiny_in1k:models/q1/konsey/V_IN_s2101/vit_tiny_in1k/adv/adversarial_training/best.pth \
 --model V_IN_s2102:vit_tiny_in1k:models/q1/konsey/V_IN_s2102/vit_tiny_in1k/adv/adversarial_training/best.pth \
 --model R224_IN_s1301:resnet18_224_in1k:models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training/best.pth \
 --model R224_IN_s1302:resnet18_224_in1k:models/q1/konsey/R224_IN_s1302/resnet18_224_in1k/adv/adversarial_training/best.pth \
 --model R224_scr_s1201:resnet18_224:models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training/best.pth \
 --model R224_scr_s1202:resnet18_224:models/q1/konsey/R224_scr_s1202/resnet18_224/adv/adversarial_training/best.pth \
 --rb-model Wong2020Fast --rb-model Engstrom2019Robustness --rb-model Carmon2019Unlabeled \
 --rb-model Gowal2020Uncovering_28_10_extra --rb-model Sehwag2021Proxy_R18 \
 --rb-model Addepalli2022Efficient_RN18 --rb-model Rade2021Helper_R18_ddpm \
 --rb-model Debenedetti2022Light_XCiT-S12"

adim_regresyon() { bash scripts/ek_regresyon.sh gpu 200 | tee "$LOG/regresyon_gpu200.txt"; }
adim_b8denetim() {
    $DX bash -c "python experiments/q1_ek_transfer_matrix.py $IN_ORTAK $IN14 $YEDEK_IN --onisleme-denetimi --yalniz-denetim \
      --out-dir $B8D/denetim" > "$LOG/b8_denetim.log" 2>&1; echo "b8 denetim rc=$?"
    echo "Sonuc: $B8D/denetim/onisleme_denetimi.json ve imagenetv2_manifest.json (liste_sha256)."
    echo "Ek on kayit §5.5 kurali T gorulmeden uygulanir; eleme varsa IN14 bu betikte duzeltilir ve sapma kaydina yazilir."; }
adim_b9() {
    # Ozgun betik (ek on kayit §3). Ozgun betigin XCiT onbellek geri koyma islevi yalniz CIFAR-10 dosya adini
    # bilir; sha256'si dogrulanmis CIFAR-100 XCiT dosyasi hub onbellegine onceden konur (yoksa timm GitHub'dan indirir).
    $DX bash -c 'h=$(python -c "import torch;print(torch.hub.get_dir())")/checkpoints; mkdir -p $h; \
      [ -f $h/debenedetti2022light-xcit-s-cifar100-linf.pth.tar ] || cp models/robustbench_zoo/cifar100/Linf/Debenedetti2022Light_XCiT-S12.pth.tar $h/debenedetti2022light-xcit-s-cifar100-linf.pth.tar'
    $DX bash -c "python experiments/c1_c3_transfer_matrix.py --dataset cifar100 --n-samples 10000 --seed 42 $C100 \
      --cache-adv $ONB/b9_c100 --skip-existing --out-dir $B9D/matris" > "$LOG/b9_matris.log" 2>&1; echo "b9 rc=$?"; }
adim_b8() {
    $DX bash -c "python experiments/q1_ek_transfer_matrix.py $IN_ORTAK $IN14 \
      --cache-adv $ONB/b8_imagenetv2 --skip-existing --out-dir $B8D/matris" > "$LOG/b8_matris.log" 2>&1; echo "b8 rc=$?"
    echo "Denetimdeki ve matristeki liste ozeti ayni olmali:"
    grep -h -o '"liste_sha256": "[0-9a-f]*"' $B8D/denetim/imagenetv2_manifest.json $B8D/matris/imagenetv2_manifest.json; }
adim_b10() {
    $DX bash -c "python experiments/q1_ek_gradyan_kosinus.py gradyan --dataset cifar10 --n-samples 10000 $C10 \
      --cikti $B10D/cifar10" > "$LOG/b10_cifar10.log" 2>&1; echo "b10 c10 rc=$?"
    $DX bash -c "python experiments/q1_ek_gradyan_kosinus.py gradyan --dataset cifar100 --n-samples 10000 $C100 \
      --cikti $B10D/cifar100" > "$LOG/b10_cifar100.log" 2>&1; echo "b10 c100 rc=$?"
    $DX bash -c "python experiments/q1_ek_gradyan_kosinus.py gradyan --dataset imagenetv2 --v2-kok data/imagenetv2 \
      --in-onisleme BicubicRes256Crop224 --n-samples 2000 --batch-size 25 $IN14 --cikti $B10D/imagenetv2" \
      > "$LOG/b10_imagenetv2.log" 2>&1; echo "b10 in rc=$?"; }
adim_cozumleme() {
    # B9: baglayici, dondurulmus betik tek cagri (ek on kayit §4.2); sarmalayici ayrica temiz dogruluk yan dosyasi yazar
    $DX python experiments/q1_konsey_ayrisim.py --mod b2 --matris-dizini $B9D/matris \
      --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b9.json --cikti $B9D/b9_dondurulmus_b2.json
    $DX python experiments/q1_ek_ayrisim.py --mod b9 --matris-dizini $B9D/matris \
      --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b9.json --cikti $B9D/b9_sarmalayici_b2.json
    # B8: betimsel (ek on kayit §5.6)
    $DX python experiments/q1_konsey_ayrisim.py --mod b2 --matris-dizini $B8D/matris \
      --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b8.json --cikti $B8D/b8_dondurulmus_b2.json
    $DX python experiments/q1_ek_ayrisim.py --mod b8 --matris-dizini $B8D/matris \
      --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu_b8.json --cikti $B8D/b8_betimsel.json
    # B10 (ek on kayit §6.2: 9999 permutasyon, tohum 20261030)
    $DX python experiments/q1_ek_gradyan_kosinus.py mantel --kosinus $B10D/cifar10/kosinus_ozet.json \
      --matris-dizini results/q1/konsey_b4_matris --veri-kumesi cifar10 --perm 9999 --cikti $B10D/mantel_cifar10.json
    $DX python experiments/q1_ek_gradyan_kosinus.py mantel --kosinus $B10D/cifar100/kosinus_ozet.json \
      --matris-dizini $B9D/matris --veri-kumesi cifar100 --perm 9999 --cikti $B10D/mantel_cifar100.json
    $DX python experiments/q1_ek_gradyan_kosinus.py mantel --kosinus $B10D/imagenetv2/kosinus_ozet.json \
      --matris-dizini $B8D/matris --veri-kumesi imagenetv2 --perm 9999 --cikti $B10D/mantel_imagenetv2.json
    $DX python experiments/q1_ek_ayrisim.py --mod b10 --mantel $B10D/mantel_cifar10.json \
      $B10D/mantel_cifar100.json $B10D/mantel_imagenetv2.json --cikti $B10D/b10_aile.json; }

ADIMLAR=${*:-regresyon b8denetim b9 b8 b10 cozumleme}
for a in $ADIMLAR; do
    bekci
    echo "$(date '+%F %T') adim $a basliyor"
    "adim_$a"
done
$DX chown -R 1000:1000 /workspace/results/q1
echo "$(date '+%F %T') bitti"
