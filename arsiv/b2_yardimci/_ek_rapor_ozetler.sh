#!/bin/bash
# Salt okur: B8-B10 raporu icin dondurulmus dosya ozetlerini yeniden hesaplar.
cd /home/firat/projects/adeb_sci_1
sha256sum experiments/q1_konsey_ayrisim.py
printf 'ek_govde '; sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md | sha256sum
printf 'ana_govde '; sed '/^## Dondurma eki$/,$d' raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | sha256sum
sha256sum results/q1_research/ONKAYIT_SAPMALAR.md
sha256sum results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json
ls results/q1/konsey_b9_c100/matris | wc -l
ls results/q1/konsey_b8_imagenetv2/matris | wc -l
ls results/q1/konsey_b8_imagenetv2/matris | grep -v per_sample
ls results/q1/konsey_b9_c100/matris | grep -v per_sample
stat -c '%y %n' results/q1/konsey_b9_c100/matris/transfer_matrix.json results/q1/konsey_b8_imagenetv2/matris/transfer_matrix.json
ls -la --time-style=full-iso results/q1/konsey_b9_c100/matris | sort -k7 | head -5
