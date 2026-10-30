#!/bin/bash
# =============================================================================
# Konsey tam zinciri (30.10.2026)
#   B2 bitisini bekle -> B2 cozumlemesi -> B3 on denetimi -> B3 kuru kosu ve
#   kuyruk -> B4 -> B6 AutoAttack -> B5 MI ve TGR -> B6 maskeleme ->
#   B4 cozumlemesi -> B5 cozumlemesi -> chown.
#
# Komutlar raporlar/konsey_2026-10-29/KONSEY_RUNBOOK.md sira 3-15'ten BIREBIR
# alinmistir (bayrak ve yol degismez). Yalniz "docker exec [-d] -w /workspace
# adeb_eval" oneki ve B3'teki tmux sarmali kaldirilmistir, cunku zincir
# konteynerin ICINDE tek bir ayrik bash sureci olarak kosar:
#
#   docker exec -d -w /workspace adeb_eval bash -c "bash scripts/konsey_tam_zincir.sh > logs/konsey_zincir.log 2>&1"
#
# Kuru kosu (hicbir sey calismaz, dosya yazilmaz; her adimin komutu ve bitis
# isaretinin su anki durumu basilir):
#   docker exec -w /workspace adeb_eval bash scripts/konsey_tam_zincir.sh --dry-run
#
# Idempotent: bitis isareti olan adim atlanir; zincir ayni komutla yeniden
#   baslatilabilir. Ayni anda iki zincir kosamaz (logs/konsey_zincir.lock).
# Durum defteri: results/q1/konsey_zincir_durum.tsv
#   (adim, baslangic, bitis, cikis_kodu, durum, not)
# Izleme:  tail -f logs/konsey_zincir.log
# Durdurma: docker exec adeb_eval pkill -f konsey_tam_zincir.sh
#   (o an kosan alt is, ornegin kuyruk ya da matris, ayrica durdurulmalidir;
#    bkz. dondurulen rapor)
#
# Hata politikasi:
#   B2 logunda Traceback ya da B2 sureci bitis isareti olmadan yok -> kod 7
#   B3 oncesi GPU 2 saat icinde bosalmadi (kullanim >= %10) -> kod 8
#   B3 oncesi bos disk < 30 GB -> kod 4
#   Kuyruk kodlari 2/3/4/6 -> zincir ayni kodla durur; kod 5 (AT cokus kurali)
#     -> kuyruk --in-at-lr 0.0005 ile BIR KEZ yeniden baslatilir, yine 5 ise
#     zincir 5 ile durur. Kuyruk 0 dondugu halde bitis isareti yoksa -> kod 6.
#   B2 cozumlemesi hatasi zinciri durdurmaz (KONSEY_PLANI satir 77: B2, B3'un
#     kapisi degildir). B4, B6 AA ve B5 GPU bloklari birbirinden bagimsizdir;
#     biri basarisiz olursa digerleri kosar, ona bagli cozumlemeler atlanir.
#     Sonda hata varsa "ZINCIR EKSIK" yazilir ve kod 9 ile cikilir; hata
#     yoksa "ZINCIR TAMAM".
# =============================================================================
set -uo pipefail

# KONSEY_ZINCIR_KOK yalniz sinama icindir (sahne dizini); bos ise /workspace
KOK="${KONSEY_ZINCIR_KOK:-/workspace}"
cd "$KOK" 2>/dev/null || { echo "kok dizine gecilemedi: $KOK"; exit 1; }

DRY=0
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run) DRY=1; shift ;;
        *) echo "bilinmeyen arguman: $1"; exit 1 ;;
    esac
done

DURUM=results/q1/konsey_zincir_durum.tsv
B2_DIR=results/q1/konsey_b2_panel
B2_LOG=logs/konsey_b2.log
B3_LOG=logs/konsey_b3_kuyruk.log
B3_KURU_LOG=logs/konsey_b3_kuru_kosu.log
B3_DEFTER=results/q1/konsey_b3_defter.tsv
B4_DIR=results/q1/konsey_b4_matris
B4_LOG=logs/konsey_b4.log
B6_AA_DIR=results/q1/konsey_b6_aa
B5_DIR=results/q1/konsey_b5_saldiri
B6_MASKE=results/q1/konsey_b6_maskeleme.json
B2_YOKLAMA_S=60
GPU_YOKLAMA_S=120
GPU_BEKLE_TAVAN_S=7200
GPU_ESIK_YUZDE=10
DISK_ESIK_GB=30
COKUS_YOKLAMA_S=300
YENI6=(V_IN_s2101 V_IN_s2102 R224_IN_s1301 R224_IN_s1302 R224_scr_s1201 R224_scr_s1202)

zaman() { date '+%F %T'; }
say() { echo "[$(zaman)] $*"; }

# --- runbook komutlari (birebir) ---------------------------------------------
# sira 4: B2 cozumlemesi
CMD_B2C='python experiments/q1_konsey_ayrisim.py --mod b2 \
  --matris-dizini results/q1/konsey_b2_panel \
  --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json \
  --cikti results/q1/konsey_ayrisim_b2.json'
# sira 5-6: B3 kuru kosu ve asil kosu; cokus kurali sonrasi --in-at-lr 0.0005
CMD_B3_KURU='bash scripts/konsey_b3_kuyruk.sh --dry-run --pilot results/q1/konsey_pilot_zaman.json'
CMD_B3='bash scripts/konsey_b3_kuyruk.sh --pilot results/q1/konsey_pilot_zaman.json 2>&1 | tee -a logs/konsey_b3_kuyruk.log'
CMD_B3_LR='bash scripts/konsey_b3_kuyruk.sh --pilot results/q1/konsey_pilot_zaman.json --in-at-lr 0.0005 2>&1 | tee -a logs/konsey_b3_kuyruk.log'
# sira 7-8: B4 kopya ve son matris
CMD_B4_KOPYA='mkdir -p results/q1/konsey_b4_matris && cp -n results/q1/konsey_b2_panel/per_sample_*.npz results/q1/konsey_b2_panel/cells_meta.json results/q1/konsey_b4_matris/'
CMD_B4='python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 \
  --model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
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
  --rb-model Debenedetti2022Light_XCiT-S12 \
  --cache-adv results/q1/konsey_adv_onbellek --skip-existing --out-dir results/q1/konsey_b4_matris > logs/konsey_b4.log 2>&1'
# sira 9-10: B5 (M12, P7, S12 runbook ile ayni)
M12="--model ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth \
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
 --model R224_scr_s1202:resnet18_224:models/q1/konsey/R224_scr_s1202/resnet18_224/adv/adversarial_training/best.pth"
P7="--rb-model Wong2020Fast --rb-model Engstrom2019Robustness --rb-model Carmon2019Unlabeled \
 --rb-model Gowal2020Uncovering_28_10_extra --rb-model Sehwag2021Proxy_R18 \
 --rb-model Addepalli2022Efficient_RN18 --rb-model Rade2021Helper_R18_ddpm"
S12="--sources ResNet18_AT_s1001 ResNet18_AT_s1002 ResNet18_AT_s1003 ViT_Tiny_AT_s2001 ViT_Tiny_AT_s2002 ViT_Tiny_AT_s2003 V_IN_s2101 V_IN_s2102 R224_IN_s1301 R224_IN_s1302 R224_scr_s1201 R224_scr_s1202"
# runbook'taki "A && B" zinciri, yarida kalan TGR'nin MI'yi yeniden kosturmamasi icin iki adima bolunmustur
CMD_B5_MI='python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 $M12 $P7 $S12 --attack mi --out-dir results/q1/konsey_b5_saldiri/mi > logs/konsey_b5_mi.log 2>&1'
CMD_B5_TGR='python experiments/c1_c3_transfer_matrix.py --dataset cifar10 --n-samples 10000 --seed 42 $M12 $P7 $S12 --attack tgr --out-dir results/q1/konsey_b5_saldiri/tgr > logs/konsey_b5_tgr.log 2>&1'
# sira 11: B6 AutoAttack
CMD_B6_AA='python experiments/run_autoattack_run2.py --n-samples 1000 --seed 42 \
  --model V_IN_s2101:vit_tiny_in1k:models/q1/konsey/V_IN_s2101/vit_tiny_in1k/adv/adversarial_training/best.pth \
  --model V_IN_s2102:vit_tiny_in1k:models/q1/konsey/V_IN_s2102/vit_tiny_in1k/adv/adversarial_training/best.pth \
  --model R224_IN_s1301:resnet18_224_in1k:models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training/best.pth \
  --model R224_IN_s1302:resnet18_224_in1k:models/q1/konsey/R224_IN_s1302/resnet18_224_in1k/adv/adversarial_training/best.pth \
  --model R224_scr_s1201:resnet18_224:models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training/best.pth \
  --model R224_scr_s1202:resnet18_224:models/q1/konsey/R224_scr_s1202/resnet18_224/adv/adversarial_training/best.pth \
  --output-dir results/q1/konsey_b6_aa > logs/konsey_b6_aa.log 2>&1'
# sira 12: B6 maskeleme
CMD_B6_MASKE='python scripts/konsey_b6_maskeleme.py \
  --aa-dizini results/q1/konsey_b6_aa --matris-dizini results/q1/konsey_b4_matris --n 1000 \
  --cikti results/q1/konsey_b6_maskeleme.json'
# sira 13: B4 cozumlemesi (maskeleme_isaretli_arg bos degilse sona eklenir)
CMD_B4C='python experiments/q1_konsey_ayrisim.py --mod b4 \
  --matris-dizini results/q1/konsey_b4_matris \
  --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json \
  --cikti results/q1/konsey_ayrisim_b4.json'
# sira 14: B5 cozumlemesi
CMD_B5C='python experiments/q1_konsey_ayrisim.py --mod b5 --matris-dizini results/q1/konsey_b4_matris --matris-dizini results/q1/konsey_b5_saldiri/mi --matris-dizini results/q1/konsey_b5_saldiri/tgr --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json --cikti results/q1/konsey_ayrisim_b5.json'
# sira 15: sahiplik
CMD_CHOWN='chown -R 1000:1000 /workspace/results/q1 /workspace/models/q1 /workspace/logs'

# --- bitis isaretleri ----------------------------------------------------------
npz_say() { find "$1" -maxdepth 1 -name 'per_sample_*.npz' 2>/dev/null | wc -l; }
onb_say() { local n; n=$(grep -c onbellege "$B2_LOG" 2>/dev/null); echo "${n:-0}"; }
b2_bitti() { [ -f "$B2_DIR/transfer_matrix.json" ] && grep -q "custom kaydedildi: results/q1/konsey_b2_panel" "$B2_LOG" 2>/dev/null; }
b2c_bitti() { [ -f results/q1/konsey_ayrisim_b2.json ]; }
b3_at_tamam_say() {
    local n=0 t m
    for t in "${YENI6[@]}"; do
        case "${t%_s*}" in V_IN) m=vit_tiny_in1k ;; R224_IN) m=resnet18_224_in1k ;; R224_scr) m=resnet18_224 ;; esac
        [ -f "models/q1/konsey/$t/$m/adv/adversarial_training/TRAINING_COMPLETE" ] && n=$((n + 1))
    done
    echo "$n"
}
b3_bitti() { [ -f "$B3_LOG" ] && tail -1 "$B3_LOG" | grep -q "KUYRUK TAMAM" && [ "$(b3_at_tamam_say)" -eq 6 ]; }
b4_bitti() { [ -f "$B4_DIR/transfer_matrix.json" ] && [ "$(npz_say "$B4_DIR")" -eq 400 ] && grep -q "custom kaydedildi: results/q1/konsey_b4_matris" "$B4_LOG" 2>/dev/null; }
b6aa_bitti() { [ -f "$B6_AA_DIR/autoattack_summary.json" ]; }
b5mi_bitti() { [ -f "$B5_DIR/mi/transfer_matrix.json" ]; }
b5tgr_bitti() { [ -f "$B5_DIR/tgr/transfer_matrix.json" ]; }
b6m_bitti() { [ -f "$B6_MASKE" ]; }
b4c_bitti() { [ -f results/q1/konsey_ayrisim_b4.json ]; }
b5c_bitti() { [ -f results/q1/konsey_ayrisim_b5.json ]; }

# --- durum defteri -------------------------------------------------------------
HATALAR=()
durum_yaz() {  # adim bas bit kod durum not
    [ "$DRY" = 1 ] && return 0
    printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$1" "$2" "$3" "$4" "$5" "$6" >> "$DURUM"
}

isaret_durumu() {  # isaret_fn -> "BITTI (atlanir)" | "BEKLIYOR"
    if "$1"; then echo "BITTI (atlanir)"; else echo "BEKLIYOR (bitis isareti yok)"; fi
}

# Genel adim: ad isaret_fn komut_degiskeni [bagimlilik_fn ...]
adim() {
    local ad="$1" isaret="$2" cmdvar="$3" bas rc b
    shift 3
    if "$isaret"; then
        say "ATLA $ad (bitis isareti var)"
        durum_yaz "$ad" "$(zaman)" "$(zaman)" 0 ATLANDI "bitis isareti mevcut"
        return 0
    fi
    for b in "$@"; do
        if ! "$b"; then
            if [ "$DRY" = 1 ]; then
                echo "  [$ad] on kosul $b henuz saglanmiyor (gercek kosuda o adim once biter)"
            else
                say "ATLA $ad: on kosul saglanmiyor ($b)"
                durum_yaz "$ad" "$(zaman)" "$(zaman)" "" BAGIMLILIK_YOK "$b saglanmiyor"
                HATALAR+=("$ad(bagimlilik)")
                return 1
            fi
        fi
    done
    if [ "$DRY" = 1 ]; then
        echo "  [$ad] durum: $(isaret_durumu "$isaret")"
        echo "  [$ad] komut: ${!cmdvar}"
        return 0
    fi
    bas=$(zaman)
    say "BASLA $ad"
    eval "${!cmdvar}"
    rc=$?
    if [ "$rc" -eq 0 ] && "$isaret"; then
        say "BITTI $ad (rc=0, bitis isareti var)"
        durum_yaz "$ad" "$bas" "$(zaman)" "$rc" OK ""
        return 0
    fi
    say "HATA $ad (rc=$rc, bitis isareti $("$isaret" && echo var || echo yok))"
    durum_yaz "$ad" "$bas" "$(zaman)" "$rc" HATA "bitis isareti $("$isaret" && echo var || echo yok)"
    HATALAR+=("$ad")
    return 1
}

dur() {  # kod mesaj [adim bas]
    local kod="$1" msg="$2"
    say "ZINCIR DURDU (kod $kod): $msg"
    [ -n "${3:-}" ] && durum_yaz "$3" "${4:-$(zaman)}" "$(zaman)" "$kod" DURDU "$msg"
    exit "$kod"
}

son_islem() {  # cikista (basarili ya da degil) sahipligi firat'a ver
    say "chown: $CMD_CHOWN"
    eval "$CMD_CHOWN" 2>&1 | tail -3
}

# ==============================================================================
if [ "$DRY" = 1 ]; then
    echo "# KURU KOSU (--dry-run): komutlar yalniz basilir, hicbir sey calismaz, dosya yazilmaz"
    echo "# kok: $KOK   zaman: $(zaman)"
    echo "# durum defteri (gercek kosuda): $DURUM ; log: logs/konsey_zincir.log"
else
    mkdir -p logs results/q1
    exec 9> logs/konsey_zincir.lock
    if ! flock -n 9; then echo "Baska bir zincir kosuyor (logs/konsey_zincir.lock); cikiliyor."; exit 1; fi
    [ -f "$DURUM" ] || printf "adim\tbaslangic\tbitis\tcikis_kodu\tdurum\tnot\n" > "$DURUM"
    trap son_islem EXIT
    say "ZINCIR BASLADI (kok $KOK, pid $$)"
    durum_yaz "zincir" "$(zaman)" "" "" BASLADI "pid $$"
fi

# --- 1. B2 bitisini bekle --------------------------------------------------------
echo "== 1. B2 bitisi (isaret: $B2_DIR/transfer_matrix.json ve $B2_LOG icinde 'custom kaydedildi: results/q1/konsey_b2_panel')"
if b2_bitti; then
    say "ATLA B2_bekle (B2 bitmis)"
    durum_yaz B2_bekle "$(zaman)" "$(zaman)" 0 ATLANDI "bitis isareti mevcut"
elif [ "$DRY" = 1 ]; then
    if [ ! -d "$B2_DIR" ]; then
        echo "  [B2_bekle] durum: BEKLIYOR ($B2_DIR klasoru henuz yok)"
    else
        echo "  [B2_bekle] durum: BEKLIYOR (klasor var, transfer_matrix.json yok; $(npz_say "$B2_DIR")/196 hucre npz, $(onb_say)/14 kaynak onbellekte)"
    fi
    echo "  [B2_bekle] gercek kosuda: ${B2_YOKLAMA_S} s aralikla yoklanir; logda Traceback ya da B2 sureci 3 yoklama boyunca yok ise kod 7"
else
    bas=$(zaman); yok=0; tur=0
    say "BEKLE B2 (her ${B2_YOKLAMA_S} s)"
    while ! b2_bitti; do
        if grep -q Traceback "$B2_LOG" 2>/dev/null; then
            grep -n -A3 Traceback "$B2_LOG" | tail -8
            dur 7 "B2 logunda Traceback ($B2_LOG)" B2_bekle "$bas"
        fi
        if pgrep -f "c1_c3_transfer_matrix.py.*konsey_b2_panel" > /dev/null; then
            yok=0
        else
            yok=$((yok + 1))
            if [ "$yok" -ge 3 ]; then
                dur 7 "B2 sureci yok ve bitis isareti olusmadi (3 yoklama); $B2_LOG son satir: $(tail -1 "$B2_LOG" 2>/dev/null)" B2_bekle "$bas"
            fi
        fi
        if [ $((tur % 10)) -eq 0 ]; then
            say "B2 bekliyor: $(npz_say "$B2_DIR")/196 hucre npz, $(onb_say)/14 kaynak onbellekte"
        fi
        tur=$((tur + 1))
        sleep "$B2_YOKLAMA_S"
    done
    say "B2 bitti"
    durum_yaz B2_bekle "$bas" "$(zaman)" 0 OK "transfer_matrix.json ve kayit satiri var"
fi

# --- 2. B2 cozumlemesi (B3'un kapisi degil; hata zinciri durdurmaz) ---------------
echo "== 2. B2 cozumlemesi (isaret: results/q1/konsey_ayrisim_b2.json)"
adim B2_cozumleme b2c_bitti CMD_B2C || say "UYARI: B2 cozumlemesi basarisiz; B2 B3'un kapisi olmadigindan zincir devam ediyor"

# --- 3-4. B3 ------------------------------------------------------------------------
echo "== 3. B3 on denetimi ve 4. B3 kuyrugu (isaret: $B3_LOG son satiri 'KUYRUK TAMAM' ve 6 AT TRAINING_COMPLETE; su an $(b3_at_tamam_say)/6)"
IN_LR_ONCEDEN=0
if [ -f "$B3_DEFTER" ] && awk -F'\t' '$7=="COKUS"{f=1} END{exit !f}' "$B3_DEFTER"; then IN_LR_ONCEDEN=1; fi

gpu_kullanim() {  # 5 ornegin ortalamasi (yuzde, tamsayi); okunamazsa bos
    local s=0 n=0 u i
    for i in 1 2 3 4 5; do
        u=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -dc '0-9')
        [ -n "$u" ] && { s=$((s + u)); n=$((n + 1)); }
        [ "$i" -lt 5 ] && sleep 2
    done
    [ "$n" -gt 0 ] && echo $((s / n))
}

cokus_izle() {  # bilgi amacli: V_IN_s2101 AT 5. epok val PGD (durdurma karari kuyrukta)
    local son="" r
    while :; do
        sleep "$COKUS_YOKLAMA_S"
        r=$(python scripts/konsey_b3_denetim.py cokus --takma V_IN_s2101 2>&1 | tail -1)
        if [ "$r" != "$son" ]; then say "COKUS-IZLEME V_IN_s2101: $r"; son="$r"; fi
        case "$r" in
            TAMAM*|COKUS*) say "COKUS-IZLEME V_IN_s2101 son deger: $r (bilgi amacli; durdurma karari kuyrugun kendisinde)"; break ;;
        esac
    done
}

kuyruk_kos() {  # komut_degiskeni -> kuyruk cikis kodu
    local cmdvar="$1" rc izpid
    cokus_izle &
    izpid=$!
    eval "${!cmdvar}"
    rc=$?
    kill "$izpid" 2>/dev/null; wait "$izpid" 2>/dev/null
    return "$rc"
}

if b3_bitti; then
    say "ATLA B3 (KUYRUK TAMAM ve 6/6 AT TRAINING_COMPLETE)"
    durum_yaz B3_kuyruk "$(zaman)" "$(zaman)" 0 ATLANDI "bitis isareti mevcut"
elif [ "$DRY" = 1 ]; then
    echo "  [B3_on_denetim] nvidia-smi kullanim (5 ornek ort.) < %$GPU_ESIK_YUZDE olana dek ${GPU_YOKLAMA_S} s aralikla en cok $((GPU_BEKLE_TAVAN_S / 3600)) sa beklenir, olmazsa kod 8; nvidia-smi calismazsa yoklama atlanir ve loga yazilir"
    echo "  [B3_on_denetim] df -BG --output=avail /workspace < $DISK_ESIK_GB GB ise kod 4; df calismazsa atlanir ve loga yazilir"
    if command -v nvidia-smi > /dev/null 2>&1 && nvidia-smi > /dev/null 2>&1; then
        echo "  [B3_on_denetim] su an (bilgi): nvidia-smi calisiyor, kullanim $(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -1)%, bos disk $(df -BG --output=avail "$KOK" 2>/dev/null | tail -1 | tr -d ' ')"
    else
        echo "  [B3_on_denetim] su an (bilgi): nvidia-smi bu ortamda calismiyor; gercek kosuda yoklama atlanir"
    fi
    echo "  [B3_kuru] komut: $CMD_B3_KURU > $B3_KURU_LOG 2>&1"
    if [ "$IN_LR_ONCEDEN" = 1 ]; then
        echo "  [B3_kuyruk] defterde COKUS satiri var -> dogrudan: $CMD_B3_LR"
    else
        echo "  [B3_kuyruk] komut: $CMD_B3"
        echo "  [B3_kuyruk] kod 5 ise bir kez: $CMD_B3_LR"
    fi
    echo "  [B3_kuyruk] kod 2/3/4/6 (ya da ikinci kez 5) ise zincir ayni kodla durur"
    echo "  [B3_cokus_izleme] kuyruk kosarken her ${COKUS_YOKLAMA_S} s: python scripts/konsey_b3_denetim.py cokus --takma V_IN_s2101 (degisen cikti loga; TAMAM/COKUS gorulunce biter)"
    echo "  [B3_kuyruk] durum: $(isaret_durumu b3_bitti)"
else
    # 3. on denetim
    bas=$(zaman)
    if command -v nvidia-smi > /dev/null 2>&1 && nvidia-smi > /dev/null 2>&1; then
        bekle_bas=$(date +%s)
        while :; do
            u=$(gpu_kullanim)
            if [ -z "$u" ]; then say "nvidia-smi kullanim okunamadi; GPU yoklamasi atlandi"; break; fi
            if [ "$u" -lt "$GPU_ESIK_YUZDE" ]; then say "GPU kullanim %$u < %$GPU_ESIK_YUZDE; B3 baslayabilir"; break; fi
            gecen=$(( $(date +%s) - bekle_bas ))
            if [ "$gecen" -ge "$GPU_BEKLE_TAVAN_S" ]; then
                nvidia-smi
                dur 8 "GPU $((GPU_BEKLE_TAVAN_S / 3600)) sa icinde bosalmadi (son kullanim %$u); runbook: baska egitim varken B3 baslamaz" B3_on_denetim "$bas"
            fi
            say "GPU kullanim %$u >= %$GPU_ESIK_YUZDE (baska is?); ${GPU_YOKLAMA_S} s sonra yeniden (gecen ${gecen} s)"
            sleep "$GPU_YOKLAMA_S"
        done
        nvidia-smi
    else
        say "nvidia-smi konteynerde calismiyor; GPU yoklamasi ATLANDI"
    fi
    disk=$(df -BG --output=avail "$KOK" 2>/dev/null | tail -1 | tr -dc '0-9')
    if [ -z "$disk" ]; then
        say "df calismiyor; disk denetimi ATLANDI"
    elif [ "$disk" -lt "$DISK_ESIK_GB" ]; then
        dur 4 "bos disk ${disk} GB < ${DISK_ESIK_GB} GB; B3 baslamaz" B3_on_denetim "$bas"
    else
        say "bos disk ${disk} GB >= ${DISK_ESIK_GB} GB"
    fi
    durum_yaz B3_on_denetim "$bas" "$(zaman)" 0 OK "gpu %${u:-?}; disk ${disk:-?} GB"

    # 4a. kuru kosu
    bas=$(zaman)
    say "BASLA B3_kuru: $CMD_B3_KURU > $B3_KURU_LOG"
    eval "$CMD_B3_KURU" > "$B3_KURU_LOG" 2>&1
    rc=$?
    head -3 "$B3_KURU_LOG"
    durum_yaz B3_kuru "$bas" "$(zaman)" "$rc" "$([ "$rc" -eq 0 ] && echo OK || echo HATA)" "$B3_KURU_LOG"
    [ "$rc" -eq 0 ] || dur "$rc" "B3 kuru kosusu basarisiz ($B3_KURU_LOG)"

    # 4b. asil kosu
    bas=$(zaman)
    if [ "$IN_LR_ONCEDEN" = 1 ]; then
        say "BASLA B3_kuyruk (defterde COKUS var; runbook: bundan sonra her baslatista --in-at-lr 0.0005): $CMD_B3_LR"
        kuyruk_kos CMD_B3_LR; rc=$?
        not_="--in-at-lr 0.0005 (onceden)"
    else
        say "BASLA B3_kuyruk: $CMD_B3"
        kuyruk_kos CMD_B3; rc=$?
        not_="lr 0.001"
        if [ "$rc" -eq 5 ]; then
            durum_yaz B3_kuyruk "$bas" "$(zaman)" 5 COKUS "AT cokus kurali; --in-at-lr 0.0005 ile bir kez yeniden"
            say "Kuyruk kod 5 (AT cokus kurali, ON_KAYIT 4). Bir kez yeniden: $CMD_B3_LR"
            bas=$(zaman)
            kuyruk_kos CMD_B3_LR; rc=$?
            not_="--in-at-lr 0.0005 (cokus sonrasi yeniden)"
        fi
    fi
    if [ "$rc" -ne 0 ]; then
        dur "$rc" "B3 kuyrugu kod $rc ile durdu ($not_); bkz. $B3_LOG ve $B3_DEFTER" B3_kuyruk "$bas"
    fi
    if ! b3_bitti; then
        dur 6 "kuyruk 0 dondu ama bitis isareti yok ($(b3_at_tamam_say)/6 AT TRAINING_COMPLETE)" B3_kuyruk "$bas"
    fi
    say "BITTI B3_kuyruk"
    durum_yaz B3_kuyruk "$bas" "$(zaman)" 0 OK "$not_"
fi

# --- 5. B4 ---------------------------------------------------------------------------
echo "== 5. B4 son matris (isaret: $B4_DIR/transfer_matrix.json, 400 npz, $B4_LOG icinde 'custom kaydedildi: results/q1/konsey_b4_matris'; su an $(npz_say "$B4_DIR") npz)"
b4_kopya_ve_kos() {
    local rc
    eval "$CMD_B4_KOPYA"; rc=$?
    say "B4 kopya rc=$rc (cp -n var olan dosyada sifir disi donebilir; bilgi), $(npz_say "$B4_DIR") npz"
    eval "$CMD_B4"
}
CMD_B4_TAM='b4_kopya_ve_kos'
if [ "$DRY" = 1 ] && ! b4_bitti; then
    echo "  [B4] kopya komutu: $CMD_B4_KOPYA"
fi
CMD_B4_GOSTER="$CMD_B4"
if [ "$DRY" = 1 ]; then adim B4 b4_bitti CMD_B4_GOSTER b3_bitti b2_bitti; else adim B4 b4_bitti CMD_B4_TAM b3_bitti b2_bitti; fi

# --- 6. B6 AutoAttack ------------------------------------------------------------------
echo "== 6. B6 AutoAttack (isaret: $B6_AA_DIR/autoattack_summary.json)"
adim B6_AA b6aa_bitti CMD_B6_AA b3_bitti

# --- 7. B5 MI ve TGR -------------------------------------------------------------------
echo "== 7. B5 MI-PGD ve TGR (isaret: $B5_DIR/mi/transfer_matrix.json, $B5_DIR/tgr/transfer_matrix.json)"
if [ "$DRY" = 1 ]; then
    echo "  [B5] M12=\"$M12\""
    echo "  [B5] P7=\"$P7\""
    echo "  [B5] S12=\"$S12\""
fi
adim B5_MI b5mi_bitti CMD_B5_MI b3_bitti
adim B5_TGR b5tgr_bitti CMD_B5_TGR b3_bitti

# --- 8. B6 maskeleme ------------------------------------------------------------------
echo "== 8. B6 maskeleme (isaret: $B6_MASKE)"
adim B6_maskeleme b6m_bitti CMD_B6_MASKE b4_bitti b6aa_bitti
MASKE_ARG=""
MASKE_OKUNAMADI=0
maske_okundu() { [ "$MASKE_OKUNAMADI" = 0 ]; }
if b6m_bitti; then
    # okunamazsa B4 cozumlemesi maskeleme kurali olmadan KOSMAZ (bagimlilik hatasi)
    if MASKE_ARG=$(python -c "import json,sys; print(json.load(open(sys.argv[1]))['maskeleme_isaretli_arg'] or '')" "$B6_MASKE"); then
        say "B6 maskeleme_isaretli_arg: '${MASKE_ARG}'"
    else
        MASKE_OKUNAMADI=1; MASKE_ARG=""
        say "HATA: $B6_MASKE icinden maskeleme_isaretli_arg okunamadi; B4 cozumlemesi atlanacak"
    fi
elif [ "$DRY" = 1 ]; then
    echo "  [B6_maskeleme] gercek kosuda 'maskeleme_isaretli_arg' bos degilse B4 cozumlemesinin sonuna eklenir"
fi

# --- 9. B4 ve B5 cozumlemeleri -----------------------------------------------------------
echo "== 9. B4 cozumlemesi (isaret: results/q1/konsey_ayrisim_b4.json) ve B5 cozumlemesi (isaret: results/q1/konsey_ayrisim_b5.json)"
if [ -n "$MASKE_ARG" ]; then
    CMD_B4C_TAM="$CMD_B4C $MASKE_ARG"
else
    CMD_B4C_TAM="$CMD_B4C"
fi
adim B4_cozumleme b4c_bitti CMD_B4C_TAM b4_bitti b6m_bitti maske_okundu
adim B5_cozumleme b5c_bitti CMD_B5C b4_bitti b5mi_bitti b5tgr_bitti

# --- 10. son ----------------------------------------------------------------------------
echo "== 10. chown ve son satir"
if [ "$DRY" = 1 ]; then
    echo "  [chown] komut (cikista her durumda): $CMD_CHOWN"
    echo "  [son] hata yoksa logs/konsey_zincir.log sonuna 'ZINCIR TAMAM', varsa 'ZINCIR EKSIK: ...' ve kod 9"
    echo "# KURU KOSU BITTI"
    exit 0
fi
trap - EXIT
son_islem
if [ "${#HATALAR[@]}" -gt 0 ]; then
    durum_yaz zincir "" "$(zaman)" 9 EKSIK "${HATALAR[*]}"
    say "ZINCIR EKSIK: ${HATALAR[*]}"
    exit 9
fi
durum_yaz zincir "" "$(zaman)" 0 TAMAM ""
say "ZINCIR TAMAM"
