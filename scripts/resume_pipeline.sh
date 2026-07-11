#!/bin/bash
# Elektrik kesintisi sonrasi pipeline'i kaldigi yerden baslatir.
# WSL icinden calistir:  bash ~/projects/adeb_sci_1/scripts/resume_pipeline.sh
# (Windows'tan: wsl -d Ubuntu-22.04 -- bash ~/projects/adeb_sci_1/scripts/resume_pipeline.sh)

set -e

# Acilis sonrasi docker daemon'un hazir olmasini bekle (maks ~5 dk)
for i in $(seq 1 60); do
    if docker info >/dev/null 2>&1; then break; fi
    sleep 5
done
if ! docker info >/dev/null 2>&1; then
    echo "HATA: docker daemon 5 dk icinde hazir olmadi; Docker'i baslatip tekrar deneyin."
    exit 1
fi

# Konteyneri ayaga kaldir
docker start adeb_eval >/dev/null 2>&1 || true
sleep 2

# CRLF temizligi (Windows'tan duzenlenmis olabilir)
sed -i 's/\r$//' ~/projects/adeb_sci_1/run_revision_pipeline.sh ~/projects/adeb_sci_1/scripts/bekci.sh

# Pipeline (zaten calisiyorsa dokunma)
if tmux has-session -t revpipe 2>/dev/null; then
    echo "revpipe tmux oturumu zaten calisiyor. Izlemek icin: tmux attach -t revpipe"
else
    tmux new-session -d -s revpipe \
        "docker exec adeb_eval bash /workspace/run_revision_pipeline.sh; echo 'PIPELINE BITTI (exit '\$?')'; sleep 86400"
    echo "Pipeline tmux 'revpipe' oturumunda baslatildi."
fi

# Bekci: 30 dk'da bir saglik kontrolu (zaten calisiyorsa dokunma)
if ! tmux has-session -t bekci 2>/dev/null; then
    tmux new-session -d -s bekci "bash ~/projects/adeb_sci_1/scripts/bekci.sh"
    echo "Bekci tmux 'bekci' oturumunda baslatildi (30 dk'da bir kontrol)."
fi

echo "  Izle:        tmux attach -t revpipe   (cikis: Ctrl-b d)"
echo "  Log:         tail -f ~/projects/adeb_sci_1/logs/revision_pipeline.log"
echo "  Bekci logu:  tail -f ~/projects/adeb_sci_1/logs/bekci.log"
