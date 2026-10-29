#!/bin/bash
cd /home/firat/projects/adeb_sci_1
echo "=== veri hatti Normalize"
grep -rn -E 'transforms\.Normalize|Normalize\(' src/ cli/ experiments/c1_c3_transfer_matrix.py 2>/dev/null | grep -v '__pycache__' | head -20
echo "=== vit_tiny sarmalayici"
grep -n -E 'class CIFAR10ViTTiny|Upsample|resize|normal' src/models/vit*.py 2>/dev/null | head -20
ls src/models/
echo "=== ON_KAYIT ve PLAN icinde _p3_ ve raporlar yollari"
grep -n -E '_p3_|_P2_|_rb_|raporlar/' raporlar/konsey_2026-10-29/ON_KAYIT_TASLAGI.md
echo "=== ON_KAYIT uzun tire ve koyu"
grep -c '—' raporlar/konsey_2026-10-29/ON_KAYIT_TASLAGI.md
grep -n -E '^\*\*|^- \*\*' raporlar/konsey_2026-10-29/ON_KAYIT_TASLAGI.md | head
echo "=== dosya zamanlari"
ls -la --time-style=full-iso raporlar/konsey_2026-10-29/ON_KAYIT_TASLAGI.md raporlar/konsey_2026-10-29/04_masa_cozumlemeleri.md results/q1/konsey_sahte_2x2_sinama.json results/q1/konsey_masa/konsey_masa_cozumlemeleri.json results/q1/konsey_sentez_r_tau_masa.json src/models/r224.py raporlar/konsey_2026-10-29/hucre_tablosu.json
echo "=== CRLF"
file raporlar/konsey_2026-10-29/ON_KAYIT_TASLAGI.md raporlar/konsey_2026-10-29/hucre_tablosu.json experiments/q1_konsey_ayrisim.py
