#!/bin/bash
# Sapma kaydina B8-0 notunu ekle, IS 3'u ayrik baslat
set -uo pipefail
cd /home/firat/projects/adeb_sci_1
S=results/q1_research/ONKAYIT_SAPMALAR.md
sha256sum "$S"
grep -q '31.10.2026, not: GPU çatal regresyonu' "$S" || cat arsiv/b2_yardimci/_ek_sapma_ek.md >> "$S"
sha256sum "$S"; tail -c 300 "$S"; echo
[ -e results/q1/ek_loglar/ek_zincir_2.log ] && { echo "UYARI: ek_zincir_2.log zaten var"; exit 1; }
git status --porcelain -- scripts/ek_zincir_komutlari.sh 'raporlar/konsey_2026-10-29/hucre_tablosu*.json'
echo "[$(date '+%F %T')] IS 3 baslatiliyor: b9 b8 b10 cozumleme"
setsid nohup bash scripts/ek_zincir_komutlari.sh b9 b8 b10 cozumleme > results/q1/ek_loglar/ek_zincir_2.log 2>&1 < /dev/null & disown
sleep 150
echo "[$(date '+%F %T')] 150 s sonra"
cat results/q1/ek_loglar/ek_zincir_2.log
echo "== b9_matris.log kuyruk"
tail -15 results/q1/ek_loglar/b9_matris.log
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.free --format=csv
nvidia-smi --query-compute-apps=pid,used_memory --format=csv
docker top adeb_eval -eo pid,etime,args | cut -c1-220
