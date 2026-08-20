#!/usr/bin/env bash
# E3 TAM KOSUMU — iki kol, havuzlama YOK.
# Tasarim: results/q1_research/E3_YENIDEN_TASARIM.md (§1-§4 + EK A + EK B)
#
# BIRINCIL NICELIK: protokol yayilimi (4 protokolun urettigi asimetri yayilimi).
#   ham-kosullu sapmasi IKINCILDIR: ozdeslikle turetilebilir oldugu icin
#   (EK B) yalnizca SAGLAMA gorevi gorur.
#
# IKI KOL, AYRI RAPORLANIR, HAVUZLAMA YASAK (§B.3):
#   A kolu (kontrollu) : ciftin BIR uyesi SABIT (arsivlenmis saldiri), digeri
#                        kendi yorungesi boyunca taranir. Mimari, tohum, veri
#                        kumesi ve saldiri butcesi DEGISMEZ; yalniz hedefin
#                        temiz dogrulugu degisir. Nedensel yorum bu koldan gelir.
#   B kolu (gozlemsel) : final modeller; mimari/tohum/veri kumesi HEPSI degisir.
#
# Kosum (GPU BOSKEN):
#   bash scripts/q1_e3_run.sh
# Hizli/ucuz deneme:
#   E3_STRIDE=10 E3_N=2000 bash scripts/q1_e3_run.sh
set -u

cd "$(dirname "$0")/.." || exit 1
DEX=(docker exec -w /workspace adeb_eval)
ARC=results/q1/adv_archive
PTS=results/q1/e3_points
OUT=results/q1/e3_fit.json
STRIDE="${E3_STRIDE:-1}"       # 1 = TUM checkpointler (tasarimin varsayilani)
N="${E3_N:-10000}"             # arsiv ornek sayisi
log() { echo "[$(date '+%F %T')] $*"; }

# --- 0. GPU cakismasi muhafizi (E6 ile ayni mantik) ---
if "${DEX[@]}" bash -lc 'pgrep -f "q1_pipeline.sh" >/dev/null'; then
    if [ "${E3_FORCE:-0}" != "1" ]; then
        echo "DURDURULDU: q1_pipeline.sh kosuyor (buyuk olasilikla E7)."
        echo "  Iki GPU isini ust uste bindirmek ikisini de yavaslatir."
        echo "  E7 bitince tekrar calistirin, ya da bilerek E3_FORCE=1 verin."
        exit 1
    fi
    echo "UYARI: q1_pipeline.sh kosuyor ama E3_FORCE=1 verildi; devam ediliyor."
fi

if ! "${DEX[@]}" python -c "import torch,sys; sys.exit(0 if torch.cuda.is_available() else 1)"; then
    echo "HATA: CUDA yok. Sessiz CPU dususune izin verilmiyor."; exit 1
fi

mkdir -p "$ARC" "$PTS"
log "E3 basliyor -- stride=$STRIDE  arsiv n=$N"

# ---------------------------------------------------------------------------
# arsivle <ad> <tip> <ckpt> <veri kumesi>
# Kaynak saldirisi BIR KEZ uretilir; hedef degerlendirmesi salt ileri gecistir.
# ---------------------------------------------------------------------------
arsivle() {
    local ad="$1" tip="$2" ck="$3" ds="$4"
    local out="${ARC}/${ad}.npz"
    if [ -f "$out" ]; then log "SKIP arsiv $ad"; return 0; fi
    if [ ! -f "$ck" ]; then log "ATLA arsiv $ad (ckpt yok: $ck)"; return 1; fi
    log "START arsiv $ad"
    "${DEX[@]}" python -B scripts/q1_archive_adv.py \
        --model-type "$tip" --dataset "$ds" --n-samples "$N" \
        --ckpt "$ck" --out "$out" >/dev/null 2>&1 \
        || { log "FAIL arsiv $ad"; return 1; }
    log "DONE  arsiv $ad"
}

# ---------------------------------------------------------------------------
# noktala <yorunge-id> <epochs-dir> <tip> <veri kumesi> <arsiv-adi> <kol>
# ---------------------------------------------------------------------------
noktala() {
    local tid="$1" epdir="$2" tip="$3" ds="$4" arsiv="$5" kol="$6"
    if [ ! -d "$epdir" ]; then log "ATLA $tid (yorunge yok: $epdir)"; return 1; fi
    if [ ! -f "${ARC}/${arsiv}.npz" ]; then log "ATLA $tid (arsiv yok: $arsiv)"; return 1; fi
    if ls "${PTS}"/"${tid}"_ep*.json >/dev/null 2>&1; then log "SKIP nokta $tid"; return 0; fi
    log "START nokta $tid (kol $kol)"
    "${DEX[@]}" python -B scripts/q1_e3_calibration.py points \
        --epochs-dir "$epdir" --model-type "$tip" --dataset "$ds" \
        --adv-archive "${ARC}/${arsiv}.npz" \
        --trajectory-id "$tid" --arm "$kol" --stride "$STRIDE" \
        --out-dir "$PTS" || { log "FAIL nokta $tid"; return 1; }
}

# ===========================================================================
# A KOLU — KONTROLLU (yorunge-ici)
# Kaynak SABIT: cifttaki KARSI mimarinin final modeli.
# Hedef: ayni ciftin diger uyesinin TUM yorungesi.
# Degisen tek sey hedefin temiz dogrulugudur.
# ===========================================================================
log "=== A KOLU (kontrollu) ==="

for i in 1 2 3; do
    rs=$((1000 + i)); vs=$((2000 + i))
    # kaynaklar (final modeller, C1)
    arsivle "c10_vit_s${vs}"    vit_tiny "models/c1/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/best.pth" cifar10
    arsivle "c10_rn18_s${rs}"   resnet18 "models/c1/resnet18_s${rs}/resnet18/adv/adversarial_training/best.pth" cifar10
    # hedef yorungeleri (E2 kaydi: save_every ile tam yorunge diskte)
    noktala "A_c10_rn18_s${rs}_from_vit" \
        "models/q1/e2/resnet18_s${rs}/resnet18/adv/adversarial_training/epochs" \
        resnet18 cifar10 "c10_vit_s${vs}" A
    noktala "A_c10_vit_s${vs}_from_rn18" \
        "models/q1/e2/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/epochs" \
        vit_tiny cifar10 "c10_rn18_s${rs}" A
done

for i in 1 2 3; do
    rs=$((1000 + i)); vs=$((2000 + i))
    arsivle "c100_vit_s${vs}"  vit_tiny "models/q1/cifar100/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/best.pth" cifar100
    arsivle "c100_rn18_s${rs}" resnet18 "models/q1/cifar100/resnet18_s${rs}/resnet18/adv/adversarial_training/best.pth" cifar100
    noktala "A_c100_rn18_s${rs}_from_vit" \
        "models/q1/cifar100/resnet18_s${rs}/resnet18/adv/adversarial_training/epochs" \
        resnet18 cifar100 "c100_vit_s${vs}" A
    noktala "A_c100_vit_s${vs}_from_rn18" \
        "models/q1/cifar100/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/epochs" \
        vit_tiny cifar100 "c100_rn18_s${rs}" A
done

# SVHN (E7) -- varsa dahil edilir, yoksa SESSIZ DEGIL, ekrana yazilir
for i in 1 2; do
    rs=$((1000 + i)); vs=$((2000 + i))
    arsivle "svhn_vit_s${vs}"  vit_tiny "models/q1/svhn/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/best.pth" svhn
    arsivle "svhn_rn18_s${rs}" resnet18 "models/q1/svhn/resnet18_s${rs}/resnet18/adv/adversarial_training/best.pth" svhn
    noktala "A_svhn_rn18_s${rs}_from_vit" \
        "models/q1/svhn/resnet18_s${rs}/resnet18/adv/adversarial_training/epochs" \
        resnet18 svhn "svhn_vit_s${vs}" A
    noktala "A_svhn_vit_s${vs}_from_rn18" \
        "models/q1/svhn/vit_tiny_s${vs}/vit_tiny/adv/adversarial_training/epochs" \
        vit_tiny svhn "svhn_rn18_s${rs}" A
done

# ===========================================================================
# B KOLU — GOZLEMSEL (final modeller; mimari/tohum/veri kumesi hepsi degisir)
# Kume = veri kumesi x mimari (yorunge degil), cunku bunlar tek noktali
# "yorungeler"dir; kume bootstrap serbestlik derecesini bu kumeler belirler.
# ===========================================================================
log "=== B KOLU (gozlemsel) ==="
log "NOT: B kolu final modellerden gelir; her nokta AYRI bir model/veri"
log "     kumesinden oldugu icin kume sayisi kucuktur ve GA'lari genis cikar."
log "     Bu bir kusur degil, gozlemsel kolun dogasidir."

# B kolu icin final-model 'yorungeleri' yok; noktalar dogrudan mevcut
# transfer artefaktlarindan turetilir. Bu adim ayri bir betikte yapilir
# cunku girdi bicimi farklidir (per_sample npz -> nokta json).
if [ -x scripts/q1_e3_bkolu.py ] || [ -f scripts/q1_e3_bkolu.py ]; then
    "${DEX[@]}" python -B scripts/q1_e3_bkolu.py --out-dir "$PTS" \
        || log "UYARI: B kolu nokta uretimi basarisiz"
else
    log "UYARI: scripts/q1_e3_bkolu.py YOK -> B KOLU URETILMEDI."
    log "  fit yalniz A kolunu raporlayacak ve EGIM_UYUSMASI manseti"
    log "  KURULAMAYACAK. Bu, sessiz bir eksiklik olmasin diye yazildi."
fi

# ===========================================================================
# FIT — kol bazinda, havuzlama YOK
# ===========================================================================
log "=== FIT ==="
n_pts=$(ls "${PTS}"/*.json 2>/dev/null | wc -l)
log "toplam nokta: $n_pts"
if [ "$n_pts" -lt 6 ]; then
    echo "HATA: cok az nokta ($n_pts). points adimlari basarisiz olmus olabilir."
    exit 1
fi
"${DEX[@]}" python -B scripts/q1_e3_calibration.py fit \
    --points-dir "$PTS" --out "$OUT" || { echo "FAIL fit"; exit 1; }

log "=============== Q1-E3 TAMAM -> $OUT ==============="
echo
echo "RAPORLAMA HATIRLATMALARI (E3_YENIDEN_TASARIM):"
echo "  · Havuzlanmis uydurma URETILMEDI; manset iki kolun EGIMLERININ UYUSMASI."
echo "  · Serbestlik derecesini YORUNGE sayisi belirler; 'n=<nokta>' yazma."
echo "  · EK A'nin olctugu IKI DELIK sekilde gorunur kilinacak:"
echo "      %17,68-23,28 (5,60 puan) ve %42,28-56,40 (14,12 puan)."
echo "    O bantlarda egim hicbir noktayla desteklenmiyor -> INTERPOLASYON."
echo "  · Ozdeslik artigi (ozdeslik_artik) sifirdan anlamli saparsa RAPORLA (EK B.5)."
