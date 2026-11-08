#!/bin/bash
# =============================================================================
# Curutme zinciri (08.11.2026): ek on kayit ON_KAYIT_EK_CURUTME_2026-11-08.md
#   indirme_denetimi -> A -> B -> C1 -> C2 -> D -> G -> B1-09 -> B1-18
# Tier 2 (E, E2, F) bu zincirde YOKTUR.
#
# Kalip scripts/konsey_tam_zincir.sh: sirali bloklar, durum TSV, blok logu,
# bitis isareti olan blok atlanir (ayni komutla yeniden baslatilabilir), ayni
# anda iki zincir kosamaz (logs/curutme_2026-11-08/zincir.lock).
#
# Calistirma (WSL'den, ayrik tmux):
#   tmux new-session -d -s curutme_zincir "docker exec -w /workspace adeb_eval bash scripts/curutme_zincir.sh 2>&1 | tee -a logs/curutme_2026-11-08/zincir.log"
# Kuru kosu (hicbir sey calismaz, dosya yazilmaz; komutlar basilir):
#   docker exec -w /workspace adeb_eval bash scripts/curutme_zincir.sh --dry-run
# Izleme:
#   tail -f logs/curutme_2026-11-08/zincir.log ; cat results/q1/curutme_2026-11-08/zincir_durum.tsv
# Durdurma:
#   docker exec adeb_eval pkill -f curutme_zincir.sh ; ardindan o an kosan python sureci
#   (docker exec adeb_eval pkill -f "cli.main train" ya da ilgili betik)
#
# Durum defteri: results/q1/curutme_2026-11-08/zincir_durum.tsv
#   (blok, durum, baslangic_utc, bitis_utc, cikis_kodu, log)
# Blok loglari: logs/curutme_2026-11-08/<blok>.log ; adim alt loglari ayni dizinde.
# Kontrol noktalari: models/q1/curutme/<takma>/... (sembolik bag ->
#   /mnt/d/adeb_sci_1_veri/models/curutme_2026-11-08). Cekismeli ornek onbellegi
#   /mnt/d/adeb_sci_1_veri/onbellek/curutme_adv (B1-18 son kontrol noktasi icin ayri:
#   curutme_adv_b118_son).
#
# Hata politikasi (bir blok coker ise sonrakine gecilmez, zincir durur):
#   2 hesaplanamadi / bilinmeyen hata, 3 denetim KALDI (SHA, agirlik kaydi, best.pth),
#   5 AT cokus kurali (C1/C2: AT 5. epok dogrulama PGD < %15), 8 GPU bekcisi tavani,
#   124 degerlendirme zaman asimi (bir kez --skip-existing ile yinelenir, ikincisinde durur),
#   diger sifir disi kodlar aynen. B'de manipulasyon denetimi KALDI ise o tohumun AT'si
#   kosulmaz (on kayitli sonuc, cokus degil), zincir devam eder ve D --eksik-atla ile kosar.
#   Egitimde tohum duvar saati siniri dolarsa (timeout, kod 124) o ana kadarki en iyi
#   dogrulama kontrol noktasi kullanilir, SURE_SINIRI isareti yazilir, zincir devam eder.
#
# Toplam tahmini sure (GPU-saat; kaynak 02_deney_adaylari.json gpu_saat ve
# gpu_saat_beklenen alanlari, B1-09/B1-18 icin 01_ic_gecerlilik.md:81, :191 ve
# B9 kalibrasyonu 0.244 s/birim; GPU bekleme suresi, B pilotu oncesi en cok 2 sa kullanim beklemesi
# ve pilotun 3600 s zaman asimi DAHIL DEGIL; zincir baslatilirken GPU kullanimini yardimci Fable gozetir):
#   blok              beklenen   tavan   kumulatif beklenen   kumulatif tavan
#   indirme_denetimi    0.05      0.25        0.05                 0.25
#   A                   0.28      1.0         0.33                 1.25
#   B (pilot dahil)     7.7       10.0        8.03                11.25
#   C1                  5.3       7.4        13.33                18.65
#   C2                  4.3       5.0        17.63                23.65
#   D                   1.24      2.5        18.87                26.15
#   G                   0.1       0.3        18.97                26.45
#   B1-09               1.11      4.0        20.08                30.45
#   B1-18               0.61      2.5        20.69                32.95
# =============================================================================
set -uo pipefail

KOK="${CURUTME_ZINCIR_KOK:-/workspace}"
cd "$KOK" 2>/dev/null || { echo "kok dizine gecilemedi: $KOK"; exit 1; }

DRY=0
while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run) DRY=1; shift ;;
        *) echo "bilinmeyen arguman: $1"; exit 1 ;;
    esac
done

export TORCH_HOME=/mnt/d/adeb_sci_1_veri/onbellek/torch
export HF_HOME=/mnt/d/adeb_sci_1_veri/onbellek/hf

OUT=results/q1/curutme_2026-11-08
LOGD=logs/curutme_2026-11-08
DURUM=$OUT/zincir_durum.tsv
ISARET=$OUT/isaret
MODELD=models/q1/curutme
MODELD_HEDEF=/mnt/d/adeb_sci_1_veri/models/curutme_2026-11-08
ONB=/mnt/d/adeb_sci_1_veri/onbellek/curutme_adv
ONB_B118=/mnt/d/adeb_sci_1_veri/onbellek/curutme_adv_b118_son
KONSEY_ONB=results/q1/konsey_adv_onbellek
VAL=data/val_split_indices.json
TM="python experiments/q1_curutme_transfer_matrix.py"
COZ="python experiments/q1_curutme_cozumleme.py"
DEN="python scripts/curutme_denetim.py"
HT_ESKI=raporlar/konsey_2026-10-29/hucre_tablosu.json

# GPU bekcisi: bos bellek GPU_BOS_MB altindaysa 60 s bekle, en cok GPU_BEKLE_TAVAN_S
GPU_BOS_MB="${CURUTME_GPU_BOS_MB:-20480}"
GPU_YOKLAMA_S=60
GPU_BEKLE_TAVAN_S="${CURUTME_GPU_BEKLE_TAVAN_S:-43200}"
# B pilotu oncesi: kullanim < %10 icin en cok 2 sa beklenir; olmazsa pilot paylasimli GPU'da kosar ve isaretlenir
PILOT_KULLANIM_ESIK=10
PILOT_BEKLE_TAVAN_S=7200
COKUS_YOKLAMA_S=300

# Tohum basina duvar saati siniri (s) ve degerlendirme zaman asimlari (s)
SINIR_B=18000        # 5.0 sa (02_deney_adaylari.json B.durdurma_kurali)
SINIR_C1=13320       # 3.7 sa (C1.durdurma_kurali)
SINIR_C2=9000        # 2.5 sa (C2.durdurma_kurali)
ZA_A=3600            # 1.0 sa (A.gpu_saat)
ZA_D_MATRIS=4200; ZA_D_AA=3600; ZA_D_B10=900     # toplam 2.425 sa <= 2.5 sa (D.gpu_saat)
ZA_G=1080            # 0.3 sa (G.gpu_saat)
ZA_B109_E=3600; ZA_B109_P50=7200                  # 1 + 1 + 2 = 4 sa (01_ic_gecerlilik.md:81)
ZA_B118_SON=3600; ZA_B118_ARA=5400                # 1 + 1.5 = 2.5 sa (01_ic_gecerlilik.md:191)
ZA_COZ=1800          # cozumleme (CPU) adimi basina

# sahiplik: cikista (basarili ya da degil) dosyalar firat'a (uid 1000) verilir
CMD_CHOWN="chown -R 1000:1000 /workspace/$OUT /workspace/$LOGD $MODELD_HEDEF $ONB $ONB_B118"

B_TEMIZ_BAYRAK="--trivial-augment --random-erasing 0.25 --mixup 0.8 --cutmix 1.0 --label-smoothing 0.1 --lr-warmup 10"

utc() { date -u '+%FT%TZ'; }
say() { echo "[$(utc)] $*"; }

mkdir_dry() { [ "$DRY" = 1 ] || mkdir -p "$@"; }

durum_yaz() {  # blok durum bas bit kod log
    [ "$DRY" = 1 ] && return 0
    printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$1" "$2" "$3" "$4" "$5" "$6" >> "$DURUM"
}

dur() {  # kod mesaj blok bas log
    local kod="$1" msg="$2"
    say "ZINCIR DURDU (kod $kod): $msg"
    durum_yaz "${3:-zincir}" DURDU "${4:-$(utc)}" "$(utc)" "$kod" "${5:-}"
    durum_yaz zincir DURDU "" "$(utc)" "$kod" "$msg"
    exit "$kod"
}

bitti_mi() { [ -f "$ISARET/$1.tamam" ]; }
bitti_yaz() { [ "$DRY" = 1 ] || { mkdir -p "$ISARET"; utc > "$ISARET/$1.tamam"; }; }

# --- GPU bekcisi ---------------------------------------------------------------
gpu_bos_mb() { nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -dc '0-9'; }
gpu_kullanim() {
    local s=0 n=0 u i
    for i in 1 2 3 4 5; do
        u=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -dc '0-9')
        [ -n "$u" ] && { s=$((s + u)); n=$((n + 1)); }
        [ "$i" -lt 5 ] && sleep 2
    done
    [ "$n" -gt 0 ] && echo $((s / n))
}
gpu_bekle() {  # etiket
    [ "$DRY" = 1 ] && { echo "  [bekci] $1 oncesi: bos GPU bellegi >= $GPU_BOS_MB MiB olana dek ${GPU_YOKLAMA_S} s aralikla, en cok ${GPU_BEKLE_TAVAN_S} s (su an $(gpu_bos_mb) MiB bos)"; return 0; }
    local bas_s b gecen
    bas_s=$(date +%s)
    while :; do
        b=$(gpu_bos_mb)
        if [ -z "$b" ]; then say "bekci: nvidia-smi okunamadi, yoklama atlandi ($1)"; return 0; fi
        if [ "$b" -ge "$GPU_BOS_MB" ]; then return 0; fi
        gecen=$(( $(date +%s) - bas_s ))
        if [ "$gecen" -ge "$GPU_BEKLE_TAVAN_S" ]; then
            nvidia-smi
            dur 8 "GPU bekcisi: ${GPU_BEKLE_TAVAN_S} s icinde ${GPU_BOS_MB} MiB bos bellek olmadi ($1; son $b MiB)" "$1"
        fi
        [ $(( gecen % 600 )) -lt "$GPU_YOKLAMA_S" ] && say "bekci: $1 icin bos bellek $b MiB < $GPU_BOS_MB MiB, bekleniyor (gecen ${gecen} s)"
        sleep "$GPU_YOKLAMA_S"
    done
}

# --- genel komut kosucusu ------------------------------------------------------
# kos ETIKET ZAMAN_ASIMI_S ALT_LOG KOMUT  -> komutun cikis kodu
kos() {
    local etiket="$1" za="$2" alog="$3" cmd="$4" rc
    if [ "$DRY" = 1 ]; then
        echo "  [$etiket] timeout ${za}s: $cmd >> $alog"
        return 0
    fi
    say "BASLA $etiket (timeout ${za}s, log $alog): $cmd"
    echo "[$(utc)] KOMUT $cmd" >> "$alog"
    timeout --kill-after=120 "$za" bash -c "exec $cmd" >> "$alog" 2>&1
    rc=$?
    say "BITTI $etiket rc=$rc"
    return "$rc"
}

# Degerlendirme adimi: zaman asiminda bir kez yinelenir (onbellek ve --skip-existing ile devam)
deger_kos() {  # blok etiket za alog cmd
    local blok="$1" etiket="$2" za="$3" alog="$4" cmd="$5" rc bas
    bas=$(utc)
    gpu_bekle "$etiket"
    kos "$etiket" "$za" "$alog" "$cmd"; rc=$?
    if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then
        say "SAPMA $etiket: zaman asimi (rc=$rc); on kayit sapma politikasi geregi bir kez yineleniyor"
        durum_yaz "$etiket" ZAMAN_ASIMI_YINELE "$bas" "$(utc)" "$rc" "$alog"
        bas=$(utc)
        gpu_bekle "$etiket"
        kos "$etiket(yineleme)" "$za" "$alog" "$cmd"; rc=$?
    fi
    if [ "$rc" -ne 0 ]; then
        tail -15 "$alog" 2>/dev/null
        dur "$rc" "$etiket basarisiz (bkz. $alog)" "$etiket" "$bas" "$alog"
    fi
    durum_yaz "$etiket" OK "$bas" "$(utc)" 0 "$alog"
}

coz_kos() {  # etiket alog cmd  (CPU cozumleme)
    local etiket="$1" alog="$2" cmd="$3" rc bas
    bas=$(utc)
    kos "$etiket" "$ZA_COZ" "$alog" "$cmd"; rc=$?
    if [ "$rc" -ne 0 ]; then
        tail -15 "$alog" 2>/dev/null
        dur "$rc" "$etiket basarisiz (bkz. $alog)" "$etiket" "$bas" "$alog"
    fi
    durum_yaz "$etiket" OK "$bas" "$(utc)" 0 "$alog"
}

# B6 maskeleme ciktisindan --dislanan listesi (bos olabilir)
dislanan_arg() {
    [ -f "$OUT/D_maskeleme.json" ] || { echo ""; return; }
    python -c "import json,sys; a=json.load(open(sys.argv[1]))['maskeleme_isaretli_arg'] or ''; a=a.replace('--maskeleme-isaretli','').strip(); print(('--dislanan '+a) if a else '')" "$OUT/D_maskeleme.json"
}

# AT cokus izleyicisi (C1/C2): AT logunda 5. epok satiri gorulunce Adv < 15 ise egitimi durdurur
cokus_izle() {  # alt_log bayrak_dosyasi
    local alog="$1" bayrak="$2" satir adv
    while :; do
        sleep "$COKUS_YOKLAMA_S"
        satir=$(grep -a -o "Epoch 5/[0-9]* - Loss: [0-9.]*, Clean: [0-9.]*%, Adv: [0-9.]*%" "$alog" 2>/dev/null | tail -1)
        if [ -n "$satir" ]; then
            adv=$(echo "$satir" | sed -E 's/.*Adv: ([0-9.]+)%.*/\1/')
            if python -c "import sys; sys.exit(0 if float(sys.argv[1]) < 15.0 else 1)" "$adv"; then
                echo "COKUS $adv" > "$bayrak"
                pkill -f "cli.main train adversarial.*$3" 2>/dev/null
            else
                echo "TAMAM $adv" > "$bayrak"
            fi
            break
        fi
    done
}

# --- egitim adimi (tohum basina temiz + AT, duvar saati siniri) -------------------
# egitim BLOK TAKMA MODEL TOHUM SINIR_S TEMIZ_CMD AT_CMD INIT_AD COKUS(0/1) MANIP_ESIK(bos=yok)
egitim() {
    local blok="$1" t="$2" m="$3" s="$4" sinir="$5" tcmd="$6" acmd="$7" init_ad="$8" cokus="$9" esik="${10}"
    local cdir="$MODELD/$t/$m/clean" adir="$MODELD/$t/$m/adv/adversarial_training"
    local tlog="$LOGD/${blok}_${t}_temiz.log" alog="$LOGD/${blok}_${t}_at.log"
    local bas bas_s rc kalan bayrak izpid
    if [ -f "$adir/TRAINING_COMPLETE" ] || [ -f "$adir/SURE_SINIRI" ]; then
        say "ATLA $blok:$t (AT bitmis)"; durum_yaz "$blok:$t" ATLANDI "$(utc)" "$(utc)" 0 "$alog"; return 0
    fi
    if [ -f "$MODELD/$t/MANIP_KALDI" ]; then
        say "ATLA $blok:$t (manipulasyon denetimi daha once KALDI)"; durum_yaz "$blok:$t" MANIP_KALDI "$(utc)" "$(utc)" 3 "$tlog"; return 0
    fi
    # tohum duvar saati sinirinin baslangici dosyada tutulur; yeniden baslatmada oradan okunur, boylece
    # toplam sinir (temiz + AT, bekci beklemesi dahil) korunur
    local bas_dosya="$MODELD/$t/_baslangic_epoch.txt"
    if [ -f "$bas_dosya" ]; then
        bas_s=$(tr -dc '0-9' < "$bas_dosya")
        [ "$DRY" = 1 ] || say "$blok:$t tohum siniri baslangici dosyadan: $bas_s ($bas_dosya)"
    else
        bas_s=$(date +%s)
        [ "$DRY" = 1 ] || { mkdir -p "$MODELD/$t"; echo "$bas_s" > "$bas_dosya"; }
    fi
    [ "$DRY" = 1 ] && echo "  [$blok:$t:sinir] tohum siniri baslangici $bas_dosya (yoksa simdi yazilir; yeniden baslatmada okunur)"
    # temiz asama
    if [ -f "$cdir/TRAINING_COMPLETE" ]; then
        say "ATLA $blok:$t:temiz (TRAINING_COMPLETE var)"
    else
        bas=$(utc)
        gpu_bekle "$blok:$t:temiz"
        kos "$blok:$t:temiz" "$sinir" "$tlog" "$tcmd"; rc=$?
        if [ "$DRY" = 0 ]; then
            [ "$rc" -eq 0 ] && [ -f "$cdir/TRAINING_COMPLETE" ] || dur "${rc/#0/2}" "$blok:$t temiz asama basarisiz ya da tohum siniri temiz asamada doldu (rc=$rc)" "$blok:$t:temiz" "$bas" "$tlog"
            durum_yaz "$blok:$t:temiz" OK "$bas" "$(utc)" 0 "$tlog"
        fi
    fi
    # C1/C2 agirlik denetimi
    if [ -n "$init_ad" ]; then
        bas=$(utc)
        if [ "$DRY" = 1 ]; then
            echo "  [$blok:$t:init] $DEN init --log $tlog --ad $init_ad   (KALDI -> kod 3)"
        else
            $DEN init --log "$tlog" --ad "$init_ad" | tee "$OUT/${t}_init_denetimi.json"; rc=${PIPESTATUS[0]}
            [ "$rc" -eq 0 ] || dur 3 "$blok:$t agirlik denetimi KALDI ya da hesaplanamadi (rc=$rc)" "$blok:$t:init" "$bas" "$tlog"
            durum_yaz "$blok:$t:init" GECTI "$bas" "$(utc)" 0 "$OUT/${t}_init_denetimi.json"
        fi
    fi
    # B manipulasyon denetimi
    if [ -n "$esik" ]; then
        bas=$(utc)
        if [ "$DRY" = 1 ]; then
            echo "  [$blok:$t:manip] $DEN manip --temiz-dir $cdir --esik <B_esik.json esik>   (KALDI -> bu tohumun AT'si kosulmaz)"
        else
            $DEN manip --temiz-dir "$cdir" --esik "$esik" | tee "$OUT/${t}_manip.json"; rc=${PIPESTATUS[0]}
            if [ "$rc" -eq 3 ]; then
                touch "$MODELD/$t/MANIP_KALDI"
                say "MANIP KALDI $blok:$t: AT baslamaz (on kayit), zincir devam ediyor"
                durum_yaz "$blok:$t:manip" MANIP_KALDI "$bas" "$(utc)" 3 "$OUT/${t}_manip.json"
                return 0
            fi
            [ "$rc" -eq 0 ] || dur 2 "$blok:$t manipulasyon denetimi hesaplanamadi (rc=$rc)" "$blok:$t:manip" "$bas" "$tlog"
            durum_yaz "$blok:$t:manip" GECTI "$bas" "$(utc)" 0 "$OUT/${t}_manip.json"
        fi
    fi
    # AT asamasi: kalan tohum suresi kadar
    kalan=$(( sinir - ( $(date +%s) - bas_s ) ))
    [ "$kalan" -lt 600 ] && kalan=600
    bas=$(utc)
    gpu_bekle "$blok:$t:at"
    bayrak="$LOGD/${blok}_${t}_cokus.txt"
    if [ "$DRY" = 1 ]; then
        kos "$blok:$t:at" "<sinir $sinir s - temiz suresi>" "$alog" "$acmd"
        [ "$cokus" = 1 ] && echo "  [$blok:$t:cokus] her ${COKUS_YOKLAMA_S} s: $alog icinde 'Epoch 5/...Adv: X%'; X < 15 ise AT durdurulur ve zincir kod 5 ile durur"
        echo "  [$blok:$t:sinir] AT timeout (kod 124) ise: $DEN kirpilma --at-dir $adir --takma $t --sinir-s $sinir ; SURE_SINIRI yazilir, zincir devam eder"
        return 0
    fi
    rm -f "$bayrak"
    if [ "$cokus" = 1 ]; then cokus_izle "$alog" "$bayrak" "$t" & izpid=$!; fi
    kos "$blok:$t:at" "$kalan" "$alog" "$acmd"; rc=$?
    [ -n "${izpid:-}" ] && { kill "$izpid" 2>/dev/null; wait "$izpid" 2>/dev/null; }
    if [ -f "$bayrak" ] && grep -q '^COKUS' "$bayrak"; then
        dur 5 "$blok:$t AT cokus kurali ($(cat "$bayrak")); on kayit: karar kullaniciya (lr 5e-4 ile yeniden baslatma elle)" "$blok:$t:at" "$bas" "$alog"
    fi
    if [ "$rc" -eq 124 ] || [ "$rc" -eq 137 ]; then
        $DEN kirpilma --at-dir "$adir" --takma "$t" --sinir-s "$sinir" | tee "$OUT/${t}_sure_siniri.json"; local krc=${PIPESTATUS[0]}
        [ "$krc" -eq 0 ] || dur 3 "$blok:$t tohum siniri doldu ama best.pth okunamadi (kirpilma rc=$krc)" "$blok:$t:at" "$bas" "$alog"
        durum_yaz "$blok:$t:at" SURE_SINIRI "$bas" "$(utc)" "$rc" "$alog"
        return 0
    fi
    [ "$rc" -eq 0 ] && [ -f "$adir/TRAINING_COMPLETE" ] || dur "${rc/#0/2}" "$blok:$t AT basarisiz (rc=$rc)" "$blok:$t:at" "$bas" "$alog"
    durum_yaz "$blok:$t:at" OK "$bas" "$(utc)" 0 "$alog"
}

at_cmd() {  # model takma tohum   (B3 AT tarifi, logs/konsey_zincir.log:40 kalibi)
    echo "python -m cli.main train adversarial -m $1 -d adversarial_training -p $MODELD/$2/$1/clean/best.pth --optimizer adamw -e 100 --stop-epoch 80 --lr 0.001 -b 64 --patience 20 --val-indices $VAL --save-every 10 --seed $3 -o $MODELD/$2 --resume"
}

blok_basla() {  # blok
    echo "== $1"
    if bitti_mi "$1"; then say "ATLA $1 (bitis isareti $ISARET/$1.tamam)"; durum_yaz "$1" ATLANDI "$(utc)" "$(utc)" 0 "$LOGD/$1.log"; return 1; fi
    BLOK_BAS=$(utc)
    [ "$DRY" = 1 ] || { say "BLOK BASLADI $1"; durum_yaz "$1" BASLADI "$BLOK_BAS" "" "" "$LOGD/$1.log"; }
    return 0
}
blok_bitir() { bitti_yaz "$1"; [ "$DRY" = 1 ] || { say "BLOK BITTI $1"; durum_yaz "$1" TAMAM "$BLOK_BAS" "$(utc)" 0 "$LOGD/$1.log"; }; }

# ==============================================================================
if [ "$DRY" = 1 ]; then
    echo "# KURU KOSU (--dry-run): komutlar yalniz basilir, hicbir sey calismaz, dosya yazilmaz"
    echo "# kok: $KOK   zaman: $(utc)   TORCH_HOME=$TORCH_HOME HF_HOME=$HF_HOME"
    echo "# durum defteri: $DURUM ; zincir logu: $LOGD/zincir.log ; kontrol noktalari: $MODELD -> $(readlink -f "$MODELD" 2>/dev/null)"
else
    mkdir -p "$LOGD" "$OUT" "$ISARET" "$ONB"
    exec 9> "$LOGD/zincir.lock"
    if ! flock -n 9; then echo "Baska bir curutme zinciri kosuyor ($LOGD/zincir.lock); cikiliyor."; exit 1; fi
    trap 'eval "$CMD_CHOWN" 2>/dev/null' EXIT
    [ -f "$DURUM" ] || printf "blok\tdurum\tbaslangic_utc\tbitis_utc\tcikis_kodu\tlog\n" > "$DURUM"
    say "ZINCIR BASLADI (kok $KOK, pid $$)"
    durum_yaz zincir BASLADI "$(utc)" "" "" "$LOGD/zincir.log"
fi

# --- 0. indirme denetimi -----------------------------------------------------------
if blok_basla indirme_denetimi; then
    L="$LOGD/indirme_denetimi.log"
    CMD_SHA="sha256sum -c $OUT/indirme_sha256.txt"
    CMD_BAG="test -L $MODELD && test -d $MODELD_HEDEF && test -f models/timm_agirliklar/vit_tiny_patch16_224.augreg_in21k_ft_in1k/model.safetensors && test -f models/timm_agirliklar/resnet18.fb_swsl_ig1b_ft_in1k/model.safetensors"
    if [ "$DRY" = 1 ]; then
        echo "  [indirme_denetimi] $CMD_SHA   (bes dosya: XCiT S/M/L, AugReg ViT-Tiny, SWSL ResNet-18; uyusmazlik -> kod 3)"
        echo "  [indirme_denetimi] $CMD_BAG"
    else
        bas=$(utc)
        { echo "[$(utc)] $CMD_SHA"; eval "$CMD_SHA"; } >> "$L" 2>&1 || dur 3 "SHA-256 denetimi KALDI (bkz. $L)" indirme_denetimi "$bas" "$L"
        { echo "[$(utc)] $CMD_BAG"; eval "$CMD_BAG"; } >> "$L" 2>&1 || dur 3 "sembolik bag ya da timm agirlik dosyasi yok (bkz. $L)" indirme_denetimi "$bas" "$L"
        tail -6 "$L"
    fi
    blok_bitir indirme_denetimi
fi

# --- 1. A: XCiT ayna paneli (yalniz degerlendirme) -------------------------------------
if blok_basla A; then
    L="$LOGD/A.log"
    CMD_A_KOPYA="cp -n $KONSEY_ONB/*.npy $KONSEY_ONB/*.json $ONB/ ; mkdir -p $OUT/A_matris && cp -n results/q1/konsey_b4_matris/per_sample_*.npz results/q1/konsey_b4_matris/cells_meta.json $OUT/A_matris/"
    if [ "$DRY" = 1 ]; then echo "  [A:kopya] $CMD_A_KOPYA"; else eval "$CMD_A_KOPYA" >> "$L" 2>&1; say "A kopya: $(ls $OUT/A_matris/per_sample_*.npz 2>/dev/null | wc -l) npz, $(ls $ONB/*.npy 2>/dev/null | wc -l) onbellek"; fi
    deger_kos A A:matris "$ZA_A" "$L" "$TM --model-seti a22 --dataset cifar10 --n-samples 10000 --seed 42 --cache-adv $ONB --skip-existing --out-dir $OUT/A_matris --zaman-asimi-s $((ZA_A - 60))"
    coz_kos A:cozumleme "$L" "$COZ --blok A --matris-dizini $OUT/A_matris --cikti $OUT/cozumleme_A.json"
    blok_bitir A
fi

# --- 2. B: V-scr+ (sifirdan ViT-Tiny, guclu temiz tarif), tohum 2401 2402 ----------------
if blok_basla B; then
    L="$LOGD/B.log"
    # manipulasyon esigi (C1 V-scr temiz dogrulama ortalamasi + 5 puan)
    if [ "$DRY" = 1 ]; then
        echo "  [B:esik] $DEN esik > $OUT/B_esik.json"
        ESIK="<esik>"
    else
        [ -f "$OUT/B_esik.json" ] || $DEN esik > "$OUT/B_esik.json" || dur 2 "B esigi hesaplanamadi" B:esik "$(utc)" "$OUT/B_esik.json"
        ESIK=$(python -c "import json; print(json.load(open('$OUT/B_esik.json'))['esik'])")
        say "B manipulasyon esigi: $ESIK ($OUT/B_esik.json)"
    fi
    # iki epokluk pilot -> E_temiz (bir kez, ilk tohumla; iki tohum icin kilitlenir)
    CMD_PILOT="python -m cli.main train clean -m vit_tiny --optimizer adamw --lr-schedule cosine -e 200 --stop-epoch 2 --lr 0.001 -b 128 --seed 2401 --val-indices $VAL $B_TEMIZ_BAYRAK -o $MODELD/_pilot_B_s2401"
    if [ "$DRY" = 1 ]; then
        echo "  [B:pilot] once kullanim < %$PILOT_KULLANIM_ESIK icin en cok ${PILOT_BEKLE_TAVAN_S} s beklenir (olmazsa gpu_paylasimli=true isaretlenir)"
        kos B:pilot 3600 "$LOGD/B_pilot.log" "$CMD_PILOT"
        echo "  [B:epok] $DEN epok --log $LOGD/B_pilot.log --pilot-epok 2 --pilot-s <duvar suresi, bilgi> > $OUT/B_pilot.json  (t = 2. epogun egitim cubugu + dogrulama payi, baslatma haric; E_temiz = min(200, floor(6300 / t)))"
        E_TEMIZ="<E_temiz>"
    else
        if [ ! -f "$OUT/B_pilot.json" ]; then
            pb=$(date +%s); paylasimli=false
            while :; do
                u=$(gpu_kullanim)
                { [ -z "$u" ] || [ "$u" -lt "$PILOT_KULLANIM_ESIK" ]; } && break
                if [ $(( $(date +%s) - pb )) -ge "$PILOT_BEKLE_TAVAN_S" ]; then paylasimli=true; say "B pilotu: GPU kullanimi %$u, 2 sa icinde bosalmadi; pilot paylasimli GPU'da kosuyor (isaretlenir)"; break; fi
                sleep "$GPU_YOKLAMA_S"
            done
            gpu_bekle B:pilot
            rm -rf "$MODELD/_pilot_B_s2401"; rm -f "$LOGD/B_pilot.log"
            t0=$(date +%s)
            kos B:pilot 3600 "$LOGD/B_pilot.log" "$CMD_PILOT" || dur 2 "B pilotu basarisiz" B:pilot "$(utc)" "$LOGD/B_pilot.log"
            ps_=$(( $(date +%s) - t0 ))
            $DEN epok --log "$LOGD/B_pilot.log" --pilot-epok 2 --pilot-s "$ps_" > "$OUT/B_pilot_ham.json" || dur 2 "E_temiz hesaplanamadi" B:epok "$(utc)" "$OUT/B_pilot_ham.json"
            python -c "import json,sys; d=json.load(open(sys.argv[1])); d['gpu_paylasimli']=sys.argv[2]=='true'; d['gpu_kullanim_pilot_oncesi']=sys.argv[3]; json.dump(d,open(sys.argv[4],'w'),ensure_ascii=False)" "$OUT/B_pilot_ham.json" "$paylasimli" "${u:-}" "$OUT/B_pilot.json"
            durum_yaz B:pilot OK "$(utc)" "$(utc)" 0 "$OUT/B_pilot.json"
        fi
        E_TEMIZ=$(python -c "import json; print(json.load(open('$OUT/B_pilot.json'))['E_temiz'])")
        say "B E_temiz = $E_TEMIZ ($OUT/B_pilot.json)"
    fi
    for s in 2401 2402; do
        t=V_scrp_s$s
        TC="python -m cli.main train clean -m vit_tiny --optimizer adamw --lr-schedule cosine -e $E_TEMIZ --lr 0.001 -b 128 --seed $s --val-indices $VAL $B_TEMIZ_BAYRAK -o $MODELD/$t --resume"
        egitim B "$t" vit_tiny "$s" "$SINIR_B" "$TC" "$(at_cmd vit_tiny "$t" "$s")" "" 0 "$ESIK"
    done
    blok_bitir B
fi

# --- 3. C1: V-IN21k (AugReg IN-21k baslatma), tohum 2501 2502 ----------------------------
if blok_basla C1; then
    for s in 2501 2502; do
        t=V_IN21k_s$s
        TC="python -m cli.main train clean -m vit_tiny_in21k --init-weights augreg_in21k_ft_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed $s --val-indices $VAL -o $MODELD/$t --resume"
        egitim C1 "$t" vit_tiny_in21k "$s" "$SINIR_C1" "$TC" "$(at_cmd vit_tiny_in21k "$t" "$s")" vit_tiny_patch16_224.augreg_in21k_ft_in1k 1 ""
    done
    blok_bitir C1
fi

# --- 4. C2: R224-SWSL (IG-1B SWSL baslatma; CC-BY-NC, agirlik dagitilmaz), tohum 1501 1502 --
if blok_basla C2; then
    for s in 1501 1502; do
        t=R224_SWSL_s$s
        TC="python -m cli.main train clean -m resnet18_224_swsl --init-weights fb_swsl_ig1b_ft_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed $s --val-indices $VAL -o $MODELD/$t --resume"
        egitim C2 "$t" resnet18_224_swsl "$s" "$SINIR_C2" "$TC" "$(at_cmd resnet18_224_swsl "$t" "$s")" resnet18.fb_swsl_ig1b_ft_in1k 1 ""
    done
    blok_bitir C2
fi

# --- 5. D: ortak degerlendirme (28 model PGD-10 matrisi, AA ilk 1000 + B6 kurali, B10) -----
if blok_basla D; then
    L="$LOGD/D.log"
    CMD_D_KOPYA="mkdir -p $OUT/D_matris && cp -n $OUT/A_matris/per_sample_*.npz $OUT/A_matris/cells_meta.json $OUT/D_matris/"
    if [ "$DRY" = 1 ]; then echo "  [D:kopya] $CMD_D_KOPYA"; else eval "$CMD_D_KOPYA" >> "$L" 2>&1; fi
    deger_kos D D:matris "$ZA_D_MATRIS" "$L" "$TM --model-seti d28 --eksik-atla --dataset cifar10 --n-samples 10000 --seed 42 --cache-adv $ONB --skip-existing --out-dir $OUT/D_matris --zaman-asimi-s $((ZA_D_MATRIS - 60))"
    if [ "$DRY" = 1 ]; then YENI_ARG='$('"$TM"' --model-seti d28 --eksik-atla --yalniz-arguman --yalniz-yeni)'; TUM_ARG='$('"$TM"' --model-seti d28 --eksik-atla --yalniz-arguman)'
    else YENI_ARG=$($TM --model-seti d28 --eksik-atla --yalniz-arguman --yalniz-yeni); TUM_ARG=$($TM --model-seti d28 --eksik-atla --yalniz-arguman); fi
    deger_kos D D:aa "$ZA_D_AA" "$L" "python experiments/run_autoattack_run2.py --n-samples 1000 --seed 42 $YENI_ARG --output-dir $OUT/D_aa"
    coz_kos D:maskeleme "$L" "python scripts/konsey_b6_maskeleme.py --aa-dizini $OUT/D_aa --matris-dizini $OUT/D_matris --n 1000 --cikti $OUT/D_maskeleme.json"
    deger_kos D D:b10 "$ZA_D_B10" "$L" "python experiments/q1_ek_gradyan_kosinus.py gradyan --dataset cifar10 --n-samples 10000 $TUM_ARG --cikti $OUT/D_b10"
    coz_kos D:b10_mantel "$L" "python experiments/q1_ek_gradyan_kosinus.py mantel --kosinus $OUT/D_b10/kosinus_ozet.json --matris-dizini $OUT/D_matris --veri-kumesi cifar10 --perm 9999 --cikti $OUT/D_b10/mantel_cifar10.json"
    if [ "$DRY" = 1 ]; then DIS="<D_maskeleme.json maskeleme_isaretli_arg -> --dislanan ...>"; else DIS=$(dislanan_arg); say "D dislanan: '${DIS}'"; fi
    for b in B C1 C2; do
        coz_kos "D:cozumleme_$b" "$L" "$COZ --blok $b --matris-dizini $OUT/D_matris $DIS --cikti $OUT/cozumleme_$b.json"
    done
    coz_kos D:cozumleme_A28 "$L" "$COZ --blok A --matris-dizini $OUT/D_matris $DIS --cikti $OUT/cozumleme_A_d28.json"
    blok_bitir D
fi

# --- 6. G: dogrusal CKA ve omega duzeltmeli benzerlik ----------------------------------------
if blok_basla G; then
    L="$LOGD/G.log"
    deger_kos G G:cka "$ZA_G" "$L" "python experiments/q1_curutme_cka.py --model-seti d28 --eksik-atla --n 5000 --n-pgd 1000 --onbellek $ONB --cikti $OUT/G --zaman-asimi-s $((ZA_G - 60))"
    for k in temiz pgd; do
        coz_kos "G:mantel_$k" "$L" "python experiments/q1_ek_gradyan_kosinus.py mantel --kosinus $OUT/G/cka_${k}_ozet.json --matris-dizini $OUT/D_matris --veri-kumesi cifar10 --perm 9999 --cikti $OUT/G/mantel_cka_$k.json"
    done
    if [ "$DRY" = 1 ]; then DIS="<D dislanan>"; else DIS=$(dislanan_arg); fi
    coz_kos G:cozumleme "$L" "$COZ --blok G --matris-dizini $OUT/D_matris $DIS --mantel $OUT/G/mantel_cka_temiz.json --cikti $OUT/cozumleme_G.json"
    coz_kos G:cozumleme_pgd "$L" "$COZ --blok G --matris-dizini $OUT/D_matris $DIS --mantel $OUT/G/mantel_cka_pgd.json --cikti $OUT/cozumleme_G_pgdcka.json"
    blok_bitir G
fi

# --- 7. B1-09: 20 modelli matris eps 4/255 ve 16/255, PGD-50 kaynak saldirisi ----------------
if blok_basla B1-09; then
    L="$LOGD/B1-09.log"
    deger_kos B1-09 B1-09:e4 "$ZA_B109_E" "$L" "$TM --model-seti b4_20 --dataset cifar10 --n-samples 10000 --seed 42 --eps 4 --alpha 1 --cache-adv $ONB --skip-existing --out-dir $OUT/B109_e4 --zaman-asimi-s $((ZA_B109_E - 60))"
    deger_kos B1-09 B1-09:e16 "$ZA_B109_E" "$L" "$TM --model-seti b4_20 --dataset cifar10 --n-samples 10000 --seed 42 --eps 16 --alpha 4 --cache-adv $ONB --skip-existing --out-dir $OUT/B109_e16 --zaman-asimi-s $((ZA_B109_E - 60))"
    deger_kos B1-09 B1-09:pgd50 "$ZA_B109_P50" "$L" "$TM --model-seti b4_20 --dataset cifar10 --n-samples 10000 --seed 42 --steps 50 --cache-adv $ONB --skip-existing --out-dir $OUT/B109_pgd50 --zaman-asimi-s $((ZA_B109_P50 - 60))"
    for k in e4 e16 pgd50; do
        coz_kos "B1-09:ayrisim_$k" "$L" "python experiments/q1_konsey_ayrisim.py --mod b4 --matris-dizini $OUT/B109_$k --hucre-tablosu $HT_ESKI --cikti $OUT/B109_ayrisim_$k.json"
    done
    blok_bitir B1-09
fi

# --- 8. B1-18: B3 kosularinin son ve ara kontrol noktalari ----------------------------------
if blok_basla B1-18; then
    L="$LOGD/B1-18.log"
    # son kontrol noktasi (egitilmis 12 modelin hepsi last.pth: C1 ve B3) ayni takma adlari tasidigi icin ayri
    # onbellek; egitilmis kaynaklarin best onbellegi kopyalanmaz, yalniz panel ve XCiT-S12 kopyalanir
    CMD_B118_KOPYA="mkdir -p $ONB_B118 && for f in $KONSEY_ONB/*; do case \$(basename \$f) in V_IN_s21*|R224_IN_s13*|R224_scr_s12*|ResNet18_AT_s100*|ViT_Tiny_AT_s200*) ;; *) cp -n \$f $ONB_B118/ ;; esac; done"
    if [ "$DRY" = 1 ]; then echo "  [B1-18:kopya] $CMD_B118_KOPYA"; else eval "$CMD_B118_KOPYA" >> "$L" 2>&1; fi
    deger_kos B1-18 B1-18:son "$ZA_B118_SON" "$L" "$TM --model-seti b118_son_tum --dataset cifar10 --n-samples 10000 --seed 42 --cache-adv $ONB_B118 --skip-existing --out-dir $OUT/B118_son --zaman-asimi-s $((ZA_B118_SON - 60))"
    coz_kos B1-18:ayrisim_son "$L" "python experiments/q1_konsey_ayrisim.py --mod b4 --matris-dizini $OUT/B118_son --hucre-tablosu $HT_ESKI --cikti $OUT/B118_ayrisim_son.json"
    deger_kos B1-18 B1-18:ara "$ZA_B118_ARA" "$L" "$TM --model-seti b118_ara --dataset cifar10 --n-samples 10000 --seed 42 --cache-adv $ONB --skip-existing --out-dir $OUT/B118_ara --zaman-asimi-s $((ZA_B118_ARA - 60))"
    coz_kos B1-18:cozumleme_ara "$L" "$COZ --blok B118 --matris-dizini $OUT/B118_ara --cikti $OUT/cozumleme_B118.json"
    blok_bitir B1-18
fi

# --- son ----------------------------------------------------------------------------------
if [ "$DRY" = 1 ]; then
    echo "== son"
    echo "  [chown] $CMD_CHOWN"
    echo "  [son] hata yoksa $LOGD/zincir.log sonuna 'ZINCIR TAMAM'"
    echo "# KURU KOSU BITTI"
    exit 0
fi
durum_yaz zincir TAMAM "" "$(utc)" 0 "$LOGD/zincir.log"
say "ZINCIR TAMAM"
