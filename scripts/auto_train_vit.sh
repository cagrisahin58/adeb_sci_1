#!/bin/bash
# Auto ViT-Tiny Training Script
# 5 saat bekle, sonra GPU boşalınca eğitimi başlat

LOG_FILE="/workspace/adeb_sci_1/logs/auto_train_vit.log"
LOCK_FILE="/workspace/adeb_sci_1/logs/auto_train_vit.lock"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Lock file kontrolü (çift çalışmayı önle)
if [ -f "$LOCK_FILE" ]; then
    log "Script zaten çalışıyor (lock file mevcut). Çıkılıyor."
    exit 1
fi
touch "$LOCK_FILE"

# Cleanup on exit
cleanup() {
    rm -f "$LOCK_FILE"
    log "Script sonlandırıldı."
}
trap cleanup EXIT

log "=== Auto ViT-Tiny Training Script Başlatıldı ==="
log "5 saat bekleniyor..."

# 5 saat bekle (18000 saniye)
sleep 18000

log "Bekleme tamamlandı. GPU kontrol döngüsü başlıyor."

check_gpu() {
    # GPU kullanımı %30'un altındaysa ve bizim dışımızda python process yoksa boş say
    GPU_UTIL=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits 2>/dev/null | tr -d ' ')
    PYTHON_PROCS=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | wc -l)

    log "GPU Kullanım: ${GPU_UTIL}%, Aktif Python Process: ${PYTHON_PROCS}"

    if [ "$GPU_UTIL" -lt 30 ] && [ "$PYTHON_PROCS" -eq 0 ]; then
        return 0  # GPU boş
    else
        return 1  # GPU meşgul
    fi
}

# GPU kontrol döngüsü
MAX_CHECKS=48  # Maksimum 48 saat bekle
CHECK_COUNT=0

while [ $CHECK_COUNT -lt $MAX_CHECKS ]; do
    if check_gpu; then
        log "GPU BOŞ! Eğitim başlatılıyor..."

        cd /workspace/adeb_sci_1

        # ViT-Tiny AT eğitimini başlat
        python -m cli.main train adversarial \
            --model vit_tiny \
            --defense adversarial_training \
            --pretrained models/vit_tiny/clean/best.pth \
            --epochs 100 \
            --lr 0.001 \
            --batch-size 64 \
            --eps 0.03137 \
            --alpha 0.00784 \
            --steps 10 \
            --patience 20 \
            --output-dir models/vit_tiny/adv/at_run2 \
            --seed 123 \
            --device cuda \
            2>&1 | tee -a /workspace/adeb_sci_1/logs/vit_tiny_at_run2.log

        log "Eğitim tamamlandı!"
        exit 0
    else
        log "GPU meşgul. 1 saat sonra tekrar kontrol edilecek."
        CHECK_COUNT=$((CHECK_COUNT + 1))
        sleep 3600  # 1 saat bekle
    fi
done

log "Maksimum bekleme süresi aşıldı (48 saat). Script sonlandırılıyor."
exit 1
