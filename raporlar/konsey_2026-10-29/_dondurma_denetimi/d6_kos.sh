#!/bin/bash
# Konteynerde runbook ayristirma ve kuyruk kuru kosusu
D=raporlar/konsey_2026-10-29/_dondurma_denetimi
docker start adeb_eval >/dev/null
docker exec -w /workspace adeb_eval timeout 240 python $D/d6_runbook_ayristir.py > /home/firat/projects/adeb_sci_1/$D/d6_ayristirma.txt 2>&1
echo "ayristirma cikis: $?"
docker exec -w /workspace adeb_eval timeout 120 bash scripts/konsey_b3_kuyruk.sh --dry-run --pilot results/q1/konsey_pilot_zaman.json > /home/firat/projects/adeb_sci_1/$D/d6_kuyruk_dry_run.txt 2>&1
echo "kuyruk dry-run cikis: $?"
head -3 /home/firat/projects/adeb_sci_1/$D/d6_kuyruk_dry_run.txt
grep -c -- "--stop-epoch 80" /home/firat/projects/adeb_sci_1/$D/d6_kuyruk_dry_run.txt
grep -- "--stop-epoch" /home/firat/projects/adeb_sci_1/$D/d6_kuyruk_dry_run.txt | grep -v -- "--stop-epoch 80" | head
echo "--- denetim tavan alt komutu ---"
docker exec -w /workspace adeb_eval timeout 60 python scripts/konsey_b3_denetim.py tavan --pilot results/q1/konsey_pilot_zaman.json
echo "--- yeni dosya var mi (defter/log) ---"
ls -la /home/firat/projects/adeb_sci_1/results/q1/konsey_b3_defter.tsv /home/firat/projects/adeb_sci_1/logs/konsey_b3 2>&1 | head
