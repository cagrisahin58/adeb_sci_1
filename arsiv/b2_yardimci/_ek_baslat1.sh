#!/bin/bash
# IS 1 adim 6 + IS 2 baslatma
set -uo pipefail
cd /home/firat/projects/adeb_sci_1
echo "[$(date '+%F %T')] 6) docker rm adeb_eval_eski"
docker rm adeb_eval_eski
docker ps -a --filter name=adeb_eval --format '{{.Names}}|{{.Status}}|{{.Image}}'
echo "[$(date '+%F %T')] dondurulmus dosyalar git durumu (bos bekleniyor):"
git status --porcelain -- experiments/q1_konsey_ayrisim.py experiments/c1_c3_transfer_matrix.py scripts/konsey_tam_zincir.sh 'scripts/konsey_b3_*' 'raporlar/konsey_2026-10-29/ON_KAYIT_*.md' 'raporlar/konsey_2026-10-29/hucre_tablosu*.json' scripts/ek_zincir_komutlari.sh
sha256sum experiments/c1_c3_transfer_matrix.py experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu_b8.json raporlar/konsey_2026-10-29/hucre_tablosu_b9.json
mkdir -p results/q1/ek_loglar
if [ -e results/q1/ek_loglar/ek_zincir_1.log ]; then echo "UYARI: ek_zincir_1.log zaten var"; ls -la results/q1/ek_loglar; fi
setsid nohup bash scripts/ek_zincir_komutlari.sh regresyon b8denetim > results/q1/ek_loglar/ek_zincir_1.log 2>&1 < /dev/null & disown
echo "[$(date '+%F %T')] IS 2 baslatildi"
sleep 20
cat results/q1/ek_loglar/ek_zincir_1.log
