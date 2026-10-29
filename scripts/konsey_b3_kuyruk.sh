#!/bin/bash
# =============================================================================
# Konsey B3 kuyrugu: 2x2 (mimari x baslatma) egitimleri, 6 kosu (29.10.2026)
#   Sira (tohumlar arasinda orulu): V_IN_s2101 R224_IN_s1301 R224_scr_s1201
#                                   V_IN_s2102 R224_IN_s1302 R224_scr_s1202
#   Her kosu: temiz asama -> AT. Tarifler KONSEY_PLANI.md §4 B3 tablosu:
#     V_IN     vit_tiny_in1k     --init-weights deit_tiny_in1k   AdamW 1e-4 cosine 30 ep
#     R224_IN  resnet18_224_in1k --init-weights resnet18_a1_in1k AdamW 1e-4 cosine 30 ep
#     R224_scr resnet18_224      rastgele, C1 ViT temiz komutu: AdamW 1e-3 cosine 200 ep, b128
#     AT (dort hucrede C1 ViT ile ayni): karisik kayipli AT, PGD-10, eps 8/255,
#       alpha 2/255, AdamW (wd 0.05) lr 1e-3, b 64, sabir 20, sabit val bolmesi,
#       LR cizelgesi C1 gibi 100 epok uzerinden (cosine T_max=100), egitim
#       bekcinin tavaninda durur (--stop-epoch TAVAN), --save-every 10.
#   Tavan: pilot JSON'daki secilen_tavan (scripts/konsey_pilot_zaman.py).
#
# Calistirma (konteynerde; tmux icinden):
#   tmux new -s konsey_b3 "docker exec -w /workspace adeb_eval bash scripts/konsey_b3_kuyruk.sh --pilot results/q1/konsey_pilot_zaman.json"
#   Kuru kosu:  docker exec -w /workspace adeb_eval bash scripts/konsey_b3_kuyruk.sh --dry-run
#   AT cokus kurali tetiklendikten sonra (ON_KAYIT §4): ayni komut + --in-at-lr 0.0005
#
# Temiz asama denetimi (ON_KAYIT §4): IN kosusunun AT'si, denetimi GECTI
#   olmadan HICBIR KOSUDA baslamaz. Denetim, AT'si bitmemis her IN kosusunda
#   kuyruk her baslatildiginda yeniden yapilir (defterdeki eski satira
#   bakilmaz); KALDI ise kuyruk kod 3 ile durur. R224_IN referansi (R224_scr
#   temiz asamasinin ilk epogu) henuz yoksa denetim ERTELENDI verir ve o
#   kosunun AT'si R224_scr temiz asamasi bitene kadar bekletilir; R224_scr
#   temiz asamasindan sonra bekleyen denetim yapilir, GECTI ise bekletilen AT
#   kosulur, ardindan R224_scr AT'si.
#
# AT cokus kurali (ON_KAYIT §4): bir IN kosusunda AT 5. epok val PGD < %15
#   ise kuyruk durur (kod 5). Kullanici kuyrugu --in-at-lr 0.0005 ile yeniden
#   baslatir: lr'si farkli bir IN AT klasoru (bitmis ya da yarim) silinmeden
#   adversarial_training__lr<eski>_<zaman> adiyla yanina tasinir ve o AT
#   yeni lr ile bastan kosulur; temiz asamalar yeniden kullanilir. R224_scr
#   AT lr'si her zaman 0.001'dir. Her AT klasorune kullanilan lr at_lr.txt
#   olarak yazilir (dosya yoksa 0.001 sayilir).
#
# Devam: ayni komut. Asamasinda TRAINING_COMPLETE olan atlanir. Yarida kalan
#   asama BASTAN BASLAMAZ, --resume ile last.pth'tan (son biten epoktan sonra)
#   devam eder; yarida kalan epok yeniden kosulur. RNG durumu last.pth'ta
#   saklanmadigi icin devam eden kosu kesintisiz kosuyla bit duzeyinde ayni
#   degildir (veri sirasi ve PGD rastgele baslangici farkli).
# Defter: results/q1/konsey_b3_defter.tsv (baslangic, bitis, sure, epok, durum,
#   bos disk, GPU bellegi/kullanimi, not). Loglar: logs/konsey_b3/.
# Durma kodlari: 2 pilot egitim baslamaz | 3 temiz asama denetimi KALDI ya da
#   hesaplanamadi | 4 disk < 15 GB | 5 AT cokus kurali (ON_KAYIT §4) |
#   6 egitim hatasi
# =============================================================================
set -uo pipefail
# KONSEY_B3_KOK yalniz sinama icindir (sahte egiticili sahne dizini); bos ise /workspace
KOK="${KONSEY_B3_KOK:-/workspace}"
cd "$KOK" 2>/dev/null || { KOK="$(cd "$(dirname "$0")/.." && pwd)"; cd "$KOK"; }

PILOT=results/q1/konsey_pilot_zaman.json
DRY=0
IN_AT_LR=0.001
while [ $# -gt 0 ]; do
    case "$1" in
        --pilot) PILOT="$2"; shift 2 ;;
        --dry-run) DRY=1; shift ;;
        --in-at-lr) IN_AT_LR="$2"; shift 2 ;;
        *) echo "bilinmeyen arguman: $1"; exit 1 ;;
    esac
done

DEFTER=results/q1/konsey_b3_defter.tsv
LOGDIR=logs/konsey_b3
VAL=data/val_split_indices.json
PAY_SA=38.15
DISK_ESIK_GB=15
SCR_AT_LR=0.001
SIRA=(V_IN_s2101 R224_IN_s1301 R224_scr_s1201 V_IN_s2102 R224_IN_s1302 R224_scr_s1202)

hucre() { echo "${1%_s*}"; }
tohum() { echo "${1##*_s}"; }
tip() {
    case "$(hucre "$1")" in
        V_IN) echo vit_tiny_in1k ;;
        R224_IN) echo resnet18_224_in1k ;;
        R224_scr) echo resnet18_224 ;;
    esac
}
at_lr() { if [ "$(hucre "$1")" = R224_scr ]; then echo "$SCR_AT_LR"; else echo "$IN_AT_LR"; fi; }
ayni_sayi() { awk -v a="$1" -v b="$2" 'BEGIN { exit !((a + 0) == (b + 0)) }'; }

temiz_cmd() {
    local t="$1" m s
    m=$(tip "$t"); s=$(tohum "$t")
    case "$(hucre "$t")" in
        V_IN) echo "python -m cli.main train clean -m $m --init-weights deit_tiny_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed $s --val-indices $VAL -o models/q1/konsey/$t" ;;
        R224_IN) echo "python -m cli.main train clean -m $m --init-weights resnet18_a1_in1k --optimizer adamw --lr-schedule cosine -e 30 --lr 0.0001 -b 128 --seed $s --val-indices $VAL -o models/q1/konsey/$t" ;;
        R224_scr) echo "python -m cli.main train clean -m $m --init-weights none --optimizer adamw --lr-schedule cosine -e 200 --lr 0.001 -b 128 --seed $s --val-indices $VAL -o models/q1/konsey/$t" ;;
    esac
}

at_cmd() {
    local t="$1" cap="$2" m s
    m=$(tip "$t"); s=$(tohum "$t")
    echo "python -m cli.main train adversarial -m $m -d adversarial_training -p models/q1/konsey/$t/$m/clean/best.pth --optimizer adamw -e 100 --stop-epoch $cap --lr $(at_lr "$t") -b 64 --patience 20 --val-indices $VAL --save-every 10 --seed $s -o models/q1/konsey/$t"
}

ckdir() {  # takma asama -> checkpoint dizini
    local m; m=$(tip "$1")
    if [ "$2" = temiz ]; then echo "models/q1/konsey/$1/$m/clean"; else echo "models/q1/konsey/$1/$m/adv/adversarial_training"; fi
}

# --- tavan -------------------------------------------------------------------
if [ -f "$PILOT" ]; then
    CAP=$(python scripts/konsey_b3_denetim.py tavan --pilot "$PILOT")
else
    CAP="<TAVAN>"
fi

if [ "$DRY" = 1 ]; then
    echo "# KURU KOSU (--dry-run): komutlar yalniz basilir, hicbir sey calismaz"
    echo "# pilot: $PILOT  tavan: $CAP  egitim payi: $PAY_SA sa  disk esigi: $DISK_ESIK_GB GB  IN AT lr: $IN_AT_LR  R224_scr AT lr: $SCR_AT_LR"
    echo "# her asamadan once: df -BG /workspace (< $DISK_ESIK_GB GB ise dur) ve nvidia-smi kaydi"
    echo "# IN kosularinda AT'den once denetim her baslatmada yeniden yapilir; GECTI olmadan AT baslamaz"
    for t in "${SIRA[@]}"; do
        echo "## $t"
        echo "[temiz] $(temiz_cmd "$t") --resume   # atla: $(ckdir "$t" temiz)/TRAINING_COMPLETE varsa"
        case "$(hucre "$t")" in
            V_IN) echo "[denetim] python scripts/konsey_b3_denetim.py temiz --takma $t   # ilk epok val >= C1 ViT ilk epok ort. + 5; KALDI ise dur (kod 3)" ;;
            R224_IN) echo "[denetim] python scripts/konsey_b3_denetim.py temiz --takma $t   # ilk epok val >= R224_scr ilk epok ort. + 5; ERTELENDI ise AT, R224_scr temiz asamasindan sonraya kalir; KALDI ise dur (kod 3)" ;;
            R224_scr) echo "[denetim] ertelenmis R224_IN denetimleri yapilir; GECTI olanlarin AT'si bu noktada kosulur, KALDI ise dur (kod 3)" ;;
        esac
        case "$(hucre "$t")" in
            V_IN|R224_IN) echo "[AT-on] $(ckdir "$t" at)/at_lr.txt (yoksa 0.001) != $IN_AT_LR ise klasor adversarial_training__lr<eski>_<zaman> adiyla tasinir" ;;
        esac
        echo "[AT]    $(at_cmd "$t" "$CAP") --resume   # atla: $(ckdir "$t" at)/TRAINING_COMPLETE varsa"
        case "$(hucre "$t")" in
            V_IN|R224_IN) echo "[izleme] her 5 dk: python scripts/konsey_b3_denetim.py cokus --takma $t   # 5. epok val PGD < %15 ise egitim durdurulur (kod 5); yeniden baslatma: --in-at-lr 0.0005" ;;
        esac
        echo "[ozet]  python scripts/konsey_b3_denetim.py ozet --takma $t --tavan $CAP"
    done
    exit 0
fi

if [ "$CAP" = "YOK" ]; then
    echo "Pilot: egitim baslamaz (bekci). Karar kullanicida. $PILOT"; exit 2
fi
if [ "$CAP" = "<TAVAN>" ]; then
    echo "Pilot JSON yok: $PILOT (once scripts/konsey_pilot_zaman.py)"; exit 2
fi

mkdir -p "$LOGDIR" "$(dirname "$DEFTER")"
[ -f "$DEFTER" ] || printf "baslangic\tbitis\ttakma_ad\tasama\tsure_s\tepok\tdurum\tdisk_bos_gb\tgpu_bellek_mib\tgpu_kullanim_yuzde\tnot\n" > "$DEFTER"

DISK=""; GMEM=""; GUTIL=""
kaynak_kontrol() {
    DISK=$(df -BG --output=avail "$KOK" | tail -1 | tr -dc '0-9')
    local q
    q=$(nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
    GMEM=$(echo "$q" | cut -d, -f1 | tr -d ' '); GUTIL=$(echo "$q" | cut -d, -f2 | tr -d ' ')
    { echo "=== $(date '+%F %T') $1"; nvidia-smi 2>&1; df -h "$KOK"; } >> "$LOGDIR/nvidia_smi_df.log"
    if [ "${DISK:-0}" -lt "$DISK_ESIK_GB" ]; then
        printf "%s\t%s\t%s\t%s\t\t\tDISK_DUR\t%s\t%s\t%s\tdisk < %s GB\n" "$(date '+%F %T')" "$(date '+%F %T')" "$2" "$3" "$DISK" "$GMEM" "$GUTIL" "$DISK_ESIK_GB" >> "$DEFTER"
        echo "DUR: bos disk ${DISK} GB < ${DISK_ESIK_GB} GB"; exit 4
    fi
    if [ "${GMEM:-0}" -gt 12288 ]; then
        echo "NOT: egitim oncesi GPU bellegi ${GMEM} MiB (> 12 GB; baska konteyner?)"
    fi
}

defter() {  # bas bit takma asama sure epok durum not
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$DISK" "$GMEM" "$GUTIL" "$8" >> "$DEFTER"
}

toplam_sa() {
    awk -F'\t' 'NR>1 && ($4=="temiz" || $4=="AT") && $5!="" {s+=$5} END {printf "%.2f", s/3600}' "$DEFTER"
}

asama() {  # takma asama(temiz|AT) komut
    local t="$1" a="$2" cmd="$3" d mode bas bas_s rc ep durum pid wpid flag
    d=$(ckdir "$t" "$([ "$a" = temiz ] && echo temiz || echo at)")
    if [ -f "$d/TRAINING_COMPLETE" ]; then
        echo "[$(date '+%F %T')] ATLA $t $a (TRAINING_COMPLETE var)"; return 0
    fi
    kaynak_kontrol "$t $a" "$t" "$a"
    if [ -f "$d/last.pth" ]; then mode="devam (last.pth)"; else mode="bastan"; fi
    if [ "$a" = AT ]; then
        mkdir -p "$d"; at_lr "$t" > "$d/at_lr.txt"
        mode="$mode; AT lr $(at_lr "$t")"
    fi
    bas=$(date '+%F %T'); bas_s=$(date +%s)
    echo "[$bas] BASLA $t $a ($mode): $cmd --resume"
    flag="$LOGDIR/${t}_cokus.txt"; rm -f "$flag"
    $cmd --resume >> "$LOGDIR/${t}_${a}.log" 2>&1 &
    pid=$!
    wpid=""
    if [ "$a" = AT ] && [ "$(hucre "$t")" != R224_scr ]; then
        (
            while kill -0 "$pid" 2>/dev/null; do
                sleep 300
                r=$(python scripts/konsey_b3_denetim.py cokus --takma "$t" 2>/dev/null)
                case "$r" in
                    COKUS*) echo "$r" > "$flag"; kill "$pid"; break ;;
                    TAMAM*) echo "$r" > "$flag"; break ;;
                esac
            done
        ) &
        wpid=$!
    fi
    wait "$pid"; rc=$?
    [ -n "$wpid" ] && { kill "$wpid" 2>/dev/null; wait "$wpid" 2>/dev/null; }
    ep=$(grep -s '^epochs_run=' "$d/TRAINING_COMPLETE" | cut -d= -f2)
    if [ -f "$flag" ] && grep -q '^COKUS' "$flag"; then
        defter "$bas" "$(date '+%F %T')" "$t" "$a" "$(( $(date +%s) - bas_s ))" "$ep" "COKUS" "AT lr $(at_lr "$t"); 5. epok val PGD $(cut -d' ' -f2 "$flag") < 15; ON_KAYIT §4: kuyruk --in-at-lr 0.0005 ile yeniden baslatilir"
        echo "DUR: AT cokus kurali tetiklendi ($t, $(cat "$flag"), AT lr $(at_lr "$t")). Kuyruk durdu."
        echo "     ON_KAYIT §4: ayni komutu --in-at-lr 0.0005 ekleyerek yeniden verin; lr'si farkli IN AT klasorleri tasinip yeniden egitilir."
        exit 5
    fi
    if [ "$rc" -eq 0 ] && [ -f "$d/TRAINING_COMPLETE" ]; then durum=OK; else durum="HATA rc=$rc"; fi
    local not="$mode"
    [ -f "$flag" ] && not="$not; cokus denetimi $(cat "$flag")"
    defter "$bas" "$(date '+%F %T')" "$t" "$a" "$(( $(date +%s) - bas_s ))" "$ep" "$durum" "$not"
    echo "[$(date '+%F %T')] BITTI $t $a: $durum, epok=$ep; toplam egitim $(toplam_sa) / $PAY_SA sa"
    [ "$durum" = OK ] || { echo "DUR: egitim hatasi, log: $LOGDIR/${t}_${a}.log"; exit 6; }
}

at_hazirla() {  # takma: AT klasorunun lr'si istenen lr'den farkliysa klasoru yanina tasi
    local t="$1" d eski hedef
    d=$(ckdir "$t" at)
    [ -d "$d" ] || return 0
    if [ -f "$d/at_lr.txt" ]; then eski=$(tr -d ' \n' < "$d/at_lr.txt"); else eski=0.001; fi
    ayni_sayi "$eski" "$(at_lr "$t")" && return 0
    hedef="${d}__lr${eski}_$(date +%Y%m%d%H%M%S)"
    mv "$d" "$hedef"
    DISK=""; GMEM=""; GUTIL=""
    defter "$(date '+%F %T')" "$(date '+%F %T')" "$t" "AT_tasindi" "" "" "TASINDI" "AT lr $eski -> $(at_lr "$t") (ON_KAYIT §4 cokus kurali); eski klasor $hedef"
    echo "[$(date '+%F %T')] TASINDI $t AT klasoru (lr $eski) -> $hedef; AT lr $(at_lr "$t") ile bastan kosulacak"
}

DENETIM=""
temiz_denetim() {  # takma -> DENETIM: GECTI | ERTELENDI ; KALDI/HATA ise exit 3
    local r
    r=$(python scripts/konsey_b3_denetim.py temiz --takma "$1")
    DISK=""; GMEM=""; GUTIL=""
    echo "[$(date '+%F %T')] DENETIM $r"
    defter "$(date '+%F %T')" "$(date '+%F %T')" "$1" "denetim_temiz" "" "" "${r%% *}" "${r#* }"
    case "$r" in
        GECTI*) DENETIM=GECTI ;;
        ERTELENDI*) DENETIM=ERTELENDI ;;
        *) echo "DUR: temiz asama denetimi ${r%% *} ($1); AT baslamaz, yukleme/normalizasyon hatasi aranmali, duzeltilmis kosu ayni tohumla yeniden baslar (ON_KAYIT §4)"; exit 3 ;;
    esac
}

at_ve_ozet() {  # takma
    local t="$1" o
    asama "$t" AT "$(at_cmd "$t" "$CAP")"
    o="AT_lr=$(at_lr "$t") $(python scripts/konsey_b3_denetim.py ozet --takma "$t" --tavan "$CAP")"
    # her (kosu, AT lr) icin bir ozet satiri; lr degisip AT yeniden egitilince yenisi eklenir
    if ! grep -P "\t$t\tat_ozet\t" "$DEFTER" | grep -q -F "AT_lr=$(at_lr "$t") "; then
        DISK=""; GMEM=""; GUTIL=""
        defter "$(date '+%F %T')" "$(date '+%F %T')" "$t" "at_ozet" "" "" "OK" "$o"
    fi
    echo "[$(date '+%F %T')] OZET $t: $o"
}

in_at() {  # takma (IN kosusu): denetim + AT; ERTELENDI ise 1 doner
    local t="$1"
    at_hazirla "$t"
    if [ -f "$(ckdir "$t" at)/TRAINING_COMPLETE" ]; then
        echo "[$(date '+%F %T')] ATLA $t AT (TRAINING_COMPLETE var; denetim AT'den once GECTI vermisti)"
        at_ve_ozet "$t"; return 0
    fi
    temiz_denetim "$t"
    [ "$DENETIM" = ERTELENDI ] && return 1
    at_ve_ozet "$t"; return 0
}

BEKLEYEN=()
for t in "${SIRA[@]}"; do
    asama "$t" temiz "$(temiz_cmd "$t")"
    case "$(hucre "$t")" in
        V_IN|R224_IN)
            if ! in_at "$t"; then
                BEKLEYEN+=("$t")
                echo "[$(date '+%F %T')] BEKLET $t AT: referans (R224_scr temiz ilk epogu) yok; R224_scr temiz asamasindan sonra kosulacak"
            fi ;;
        R224_scr)
            for r in ${BEKLEYEN[@]+"${BEKLEYEN[@]}"}; do
                if ! in_at "$r"; then
                    echo "DUR: $r denetimi R224_scr temiz asamasindan sonra da ERTELENDI (referans okunamadi)"; exit 3
                fi
            done
            BEKLEYEN=()
            at_ve_ozet "$t" ;;
    esac
done
if [ "${#BEKLEYEN[@]}" -gt 0 ]; then
    echo "DUR: AT'si bekletilen kosu kaldi: ${BEKLEYEN[*]}"; exit 3
fi
echo "[$(date '+%F %T')] KUYRUK TAMAM; toplam egitim $(toplam_sa) sa (pay $PAY_SA sa). Defter: $DEFTER"
