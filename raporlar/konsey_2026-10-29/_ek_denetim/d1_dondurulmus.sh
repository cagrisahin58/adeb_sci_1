#!/bin/bash
cd /home/firat/projects/adeb_sci_1
echo "== sha256 dondurulmus =="
sha256sum experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md experiments/c1_c3_transfer_matrix.py scripts/konsey_tam_zincir.sh scripts/konsey_b3_* 
echo "== git diff HEAD c1_c3 / q1_konsey_ayrisim / hucre / ON_KAYIT =="
git diff --stat HEAD -- experiments/c1_c3_transfer_matrix.py experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md scripts/
echo "rc=$?"
echo "== git ls-files konsey_b3 / zincir =="
git ls-files scripts/konsey_b3_* scripts/konsey_tam_zincir.sh
echo "== stat mtimes =="
stat -c '%y %s %n' experiments/c1_c3_transfer_matrix.py experiments/q1_konsey_ayrisim.py raporlar/konsey_2026-10-29/hucre_tablosu.json raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md scripts/konsey_tam_zincir.sh scripts/konsey_b3_*
echo "== zincir =="
docker exec adeb_eval pgrep -af konsey_tam_zincir
docker exec adeb_eval pgrep -af python | head
nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv
echo "== git log -3 =="
git log --oneline -3
