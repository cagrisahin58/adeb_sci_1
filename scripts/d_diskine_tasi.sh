#!/usr/bin/env bash
# d_diskine_tasi.sh - konteynerin OKUMADIGI buyuk klasorleri D diskine tasir
# (rapor: raporlar/konsey_2026-10-29/07_disk_D_plani.md).
#
# WSL tarafinda, firat kullanicisiyla calistirilir; adeb_eval konteynerinde
# CALISTIRILMAZ (konteynerde /mnt/d yoktur). Her oge icin:
#   1) guvenlik denetimi (oge var mi, zaten bag mi, calisan bir surec yolu
#      komut satirinda aniyor mu, D'de yer var mi)
#   2) rsync ile /mnt/d/adeb_sci_1_veri/<ayni_goreli_yol> altina kopya
#      (drvfs izin/sahiplik tutmadigi icin --no-perms --no-owner --no-group)
#   3) kaynakta sha256 manifesti, D'de sha256sum -c ile dogrulama,
#      dosya sayisi ve bayt toplami esitligi
#   4) kaynak <yol>.__silinecek adina tasinir (atomik), ayni yola sembolik
#      bag konur, bag uzerinden ornek dosya okunur, sonra eski kopya silinir
# Bag WSL'de calisir, konteyner icinden KIRIKTIR (konteyner yeniden
# olusturulup /mnt/d/adeb_sci_1_veri ayni yola baglanana kadar).
#
# Kullanim:
#   bash scripts/d_diskine_tasi.sh --dry-run            # yalniz plan, hicbir sey degismez
#   bash scripts/d_diskine_tasi.sh                      # grup 1 (sudo gerekmez)
#   bash scripts/d_diskine_tasi.sh --grup 2 --dry-run   # karantina, root sahipli (sudo ister)
#   bash scripts/d_diskine_tasi.sh --yalniz results/q1/adv_archive   # tek oge
#
# Cikis kodlari: 0 tamam, 2 kullanim, 3 ortam (konteyner icinde / D yok),
# 4 dogrulama hatasi (kaynak SILINMEZ), 5 yer yetersiz.

set -euo pipefail

KOK=/home/firat/projects/adeb_sci_1
HEDEF=/mnt/d/adeb_sci_1_veri
MANIFEST_DIR="$HEDEF/_manifest"
DRY=0
GRUP=1
YALNIZ=""

while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run) DRY=1 ;;
        --grup) GRUP="$2"; shift ;;
        --yalniz) YALNIZ="$2"; shift ;;
        -h|--help) sed -n 2,26p "$0"; exit 0 ;;
        *) echo "bilinmeyen bayrak: $1" >&2; exit 2 ;;
    esac
    shift
done

# --- ortam denetimi -------------------------------------------------------
if [ -f /.dockerenv ]; then
    echo "HATA: konteyner icinde calistirilmaz (WSL kabugunda calistir)." >&2; exit 3
fi
if ! mountpoint -q /mnt/d; then
    echo "HATA: /mnt/d bagli degil." >&2; exit 3
fi
cd "$KOK"

# --- oge listeleri (goreli yol) ------------------------------------------
# Grup 1: firat sahipli, git disi, B2/B3/B4/B5/B6 tarafindan okunmayan.
#  - q1 E2, CIFAR-100, SVHN AT yorungelerinin epok kontrol noktalari
#    (best.pth/last.pth C'de KALIR, konteyner onlari okumaya devam eder)
#  - results/q1/adv_archive (q1 E1/E2 cekismeli ornek arsivi, bitmis)
#  - data/*.mat.1 (SVHN .mat dosyalarinin bayt bayt ayni wget kopyalari)
#  - models/densenet121 (Subat 2026 kampanyasi, kullanilmiyor)
grup1() {
    find models/q1/e2 models/q1/cifar100 models/q1/svhn \
        -mindepth 5 -maxdepth 5 -type d -name epochs -path '*/adv/adversarial_training/epochs' | sort
    echo results/q1/adv_archive
    echo data/train_32x32.mat.1
    echo data/test_32x32.mat.1
    echo models/densenet121
}
# Grup 2: C1 oncesi karantina kontrol noktalari; dizinler root sahipli,
# silme icin sudo gerekir.
grup2() {
    echo models/resnet18
    echo models/vit_tiny
    echo models/vit_cifar_tiny
}

if [ -n "$YALNIZ" ]; then
    OGELER="$YALNIZ"
elif [ "$GRUP" = 1 ]; then
    OGELER="$(grup1)"
elif [ "$GRUP" = 2 ]; then
    OGELER="$(grup2)"
else
    echo "--grup 1 ya da 2" >&2; exit 2
fi

ZAMAN=$(date +%Y%m%d_%H%M%S)
LOG="$KOK/logs/d_tasima_${ZAMAN}.log"
log() { echo "[$(date '+%F %T')] $*" | { if [ "$DRY" = 1 ]; then cat; else tee -a "$LOG"; fi; }; }

boyut_b() { du -sb "$1" | cut -f1; }
insan() { numfmt --to=iec-i --suffix=B "$1"; }

# Calisan bir surecin komut satirinda yol geciyorsa dokunma. Docker motoru
# WSL icinde yerel calistigi icin konteyner surecleri de ps'te gorunur.
kullaniliyor_mu() {
    local rel="$1" kosu kampanya
    local desen=(-e "$rel")
    case "$rel" in
        */adv/adversarial_training/epochs)
            kosu="${rel%/*/adv/adversarial_training/epochs}"   # models/q1/e2/resnet18_s1001
            kampanya="${kosu%/*}"                               # models/q1/e2
            desen+=(-e "$kosu" -e "$kampanya") ;;
    esac
    env -u COLUMNS ps -ww -eo args= 2>/dev/null | grep -v -e "d_diskine_tasi" -e "grep" | grep -q -F "${desen[@]}"
}

TOPLAM=0
for rel in $OGELER; do
    if [ ! -e "$rel" ]; then log "ATLA  $rel (yok)"; continue; fi
    if [ -L "$rel" ]; then log "ATLA  $rel (zaten bag -> $(readlink "$rel"))"; continue; fi
    if [ -n "$(git ls-files -- "$rel" | head -1)" ]; then
        log "ATLA  $rel (git izliyor)"; continue
    fi
    if kullaniliyor_mu "$rel"; then
        log "ATLA  $rel (calisan bir surecin komut satirinda geciyor)"; continue
    fi
    B=$(boyut_b "$rel")
    TOPLAM=$((TOPLAM + B))
    hedef="$HEDEF/$rel"
    if [ "$DRY" = 1 ]; then
        echo "PLAN  $(insan "$B")  $rel  ->  $hedef  (sonra: ln -s $hedef $rel)"
        continue
    fi

    BOS=$(df -B1 --output=avail /mnt/d | tail -1 | tr -dc '0-9')
    if [ "$BOS" -lt $((B + B / 10 + 1073741824)) ]; then
        log "HATA  D'de yer yok: $rel icin $(insan "$B") + pay gerekli"; exit 5
    fi

    log "KOPYA $rel ($(insan "$B"))"
    mkdir -p "$(dirname "$hedef")" "$MANIFEST_DIR"
    if [ -d "$rel" ]; then
        rsync -rt --no-perms --no-owner --no-group "$rel/" "$hedef/"
    else
        rsync -t --no-perms --no-owner --no-group "$rel" "$hedef"
    fi

    # sha256 manifesti kaynaktan uretilir, hedefte denetlenir
    man="$MANIFEST_DIR/$(echo "$rel" | tr '/' '_').sha256"
    find "$rel" -type f -print0 | sort -z | xargs -0 sha256sum > "$man"
    if ! ( cd "$HEDEF" && sha256sum -c --quiet "$man" ); then
        log "HATA  sha256 tutmadi: $rel (kaynak SILINMEDI, hedef: $hedef)"; exit 4
    fi
    n_k=$(find "$rel" -type f | wc -l); n_h=$(find "$hedef" -type f | wc -l)
    b_h=$(boyut_b "$hedef")
    if [ "$n_k" != "$n_h" ]; then
        log "HATA  dosya sayisi farkli: kaynak $n_k hedef $n_h ($rel, kaynak SILINMEDI)"; exit 4
    fi
    log "DOGRU $rel: $n_k dosya, sha256 tamam (kaynak $B B, hedef $b_h B)"

    # atomik yer degistirme: once yeniden adlandir, bagi koy, bag uzerinden oku, sonra sil
    mv "$rel" "$rel.__silinecek"
    ln -s "$hedef" "$rel"
    ornek=$(head -1 "$man" | cut -d' ' -f3-)
    if ! sha256sum "$ornek" | cmp -s - <(head -1 "$man"); then
        rm -f "$rel"; mv "$rel.__silinecek" "$rel"
        log "HATA  bag uzerinden okuma tutmadi, geri alindi: $rel"; exit 4
    fi
    if [ "$GRUP" = 2 ]; then
        sudo rm -rf "$rel.__silinecek"
    else
        rm -rf "$rel.__silinecek"
    fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$(date '+%F %T')" "$rel" "$hedef" "$B" "$n_k" \
        >> "$MANIFEST_DIR/tasima_defteri.tsv"
    log "TAMAM $rel -> $hedef"
done

if [ "$DRY" = 1 ]; then
    echo "TOPLAM (kuru): $(insan "$TOPLAM")   C bos: $(df -h --output=avail "$KOK" | tail -1)   D bos: $(df -h --output=avail /mnt/d | tail -1)"
else
    log "TOPLAM tasinan: $(insan "$TOPLAM")   C bos: $(df -h --output=avail "$KOK" | tail -1)"
fi
