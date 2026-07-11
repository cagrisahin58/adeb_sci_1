#!/bin/bash
# BEKCI: 30 dakikada bir pipeline sagligini kontrol eder.
#  - Pipeline (tmux revpipe) olmusse ve is bitmemisse YENIDEN BASLATIR
#  - Durum ozetini logs/bekci.log'a yazar (tail -f ile izlenebilir)
#  - 25+ dk log akmiyorsa UYARI yazar (hicbir seyi oldurmez)
#  - Pipeline TAMAM olunca kendini kapatir
# Kullanim (resume_pipeline.sh otomatik baslatir):
#   tmux new -d -s bekci 'bash ~/projects/adeb_sci_1/scripts/bekci.sh'

cd /home/firat/projects/adeb_sci_1
BLOG=logs/bekci.log
MASTER=logs/revision_pipeline.log
ARALIK=1800  # 30 dk

blog() { echo "[$(date '+%F %T')] $*" >> "$BLOG"; }

blog "BEKCI basladi (kontrol araligi: ${ARALIK}s)"

while true; do
    # Is bitti mi?
    if grep -q "PIPELINE TAMAM" "$MASTER" 2>/dev/null; then
        blog "PIPELINE TAMAM - bekci kapaniyor. Sonraki adim: makale TODO(run3) guncellemeleri."
        exit 0
    fi

    # Pipeline yasiyor mu? Olmusse yeniden baslat
    if ! tmux has-session -t revpipe 2>/dev/null; then
        blog "RESTART: revpipe oturumu yok - yeniden baslatiliyor"
        bash scripts/resume_pipeline.sh >> "$BLOG" 2>&1
    else
        # Son FAIL kontrolu (script FAIL'de exit eder, tmux oturumu sleep'te kalir).
        # Ayni adim icin en fazla 3 otomatik yeniden deneme; hesap suren bir
        # python sureci varken ASLA mudahale edilmez.
        SON=$(grep -E 'START|DONE|SKIP|FAIL' "$MASTER" 2>/dev/null | tail -1)
        if echo "$SON" | grep -q FAIL; then
            ADIM_ADI=$(echo "$SON" | grep -oE 'FAIL  [A-Za-z0-9_]+' | awk '{print $2}')
            FAIL_SAYI=$(grep -c "FAIL  $ADIM_ADI" "$MASTER" 2>/dev/null)
            CALISAN=$(docker exec adeb_eval bash -c "ps -C python --no-headers 2>/dev/null | wc -l" 2>/dev/null || echo 0)
            # Grace period: master log 5 dk'dan taze ise dokunma - pipeline
            # tam su anda (el ile / baska tetikleyiciyle) yeniden baslatilmis
            # olabilir; erken mudahale ikiz surec dogurur (12:10 olayi)
            LOG_YASI=$(( $(date +%s) - $(stat -c %Y "$MASTER" 2>/dev/null || echo 0) ))
            if [ "${CALISAN:-0}" -gt 0 ]; then
                blog "DIKKAT: son adim FAIL ($ADIM_ADI) ama python sureci calisiyor - dokunulmadi"
            elif [ "$LOG_YASI" -lt 300 ]; then
                blog "FAIL taze (${LOG_YASI}s < 300s) - mudahale sonraki tura birakildi ($ADIM_ADI)"
            elif [ "${FAIL_SAYI:-9}" -lt 3 ]; then
                blog "RESTART: $ADIM_ADI FAIL (deneme $FAIL_SAYI/3) - pipeline yeniden baslatiliyor"
                tmux kill-session -t revpipe 2>/dev/null
                bash scripts/resume_pipeline.sh >> "$BLOG" 2>&1
            else
                blog "DIKKAT: $ADIM_ADI 3 kez FAIL - otomatik deneme durduruldu, log inceleyin: logs/${ADIM_ADI}.log"
            fi
        fi

        # Takilma kontrolu: 25 dk'dir hicbir log buyumemisse uyar
        AKTIF=$(find logs -name '*.log' -mmin -25 2>/dev/null | wc -l)
        if [ "$AKTIF" -eq 0 ]; then
            blog "UYARI: 25+ dk'dir log akisi yok - takilma olabilir (mudahale edilmedi)"
        fi
    fi

    # Durum ozeti
    ADIM=$(grep -E 'START|DONE|SKIP' "$MASTER" 2>/dev/null | tail -1 | sed 's/^\[[^]]*\] //')
    EPOCH=$(grep -a -hoE 'Epoch [0-9]+/100 - Loss: [0-9.]+, Clean: [0-9.]+%, Adv: [0-9.]+%' logs/R1_resnet_at_run3.log logs/R2_vit_at_run3.log 2>/dev/null | tail -1)
    GPU=$(nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader 2>/dev/null)
    CHUNK=$(ls results/autoattack_run3_full/aa_chunk_*.npz 2>/dev/null | wc -l)
    blog "DURUM: adim=[$ADIM] son_epoch=[$EPOCH] gpu=[$GPU] aa_chunk=[$CHUNK/20]"

    sleep "$ARALIK"
done
