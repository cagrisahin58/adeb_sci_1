#!/usr/bin/env bash
# Sekil 3'un dunku surumunu (bugun _v1 adiyla saklanan) arsive al; arsivde v1/v2 Eylul surumleri oldugundan v3 adi.
# Konteynerde (dosyalar root sahipli): docker exec -w /workspace adeb_eval bash arsiv/b2_yardimci/_v1_arsivle.sh
set -u
cd /workspace || exit 1
mkdir -p paper/figures/arsiv/final_tr_2026-10-04
for ext in kanit.json pdf png; do
    [ -f "paper/figures/final/fig_protocol_sets_v1.$ext" ] && mv -f "paper/figures/final/fig_protocol_sets_v1.$ext" "paper/figures/arsiv/fig_protocol_sets_v3_2026-10-03.$ext" && echo "arsiv <- final/fig_protocol_sets_v1.$ext"
    [ -f "paper/figures/final_tr/fig_protocol_sets_v1.$ext" ] && mv -f "paper/figures/final_tr/fig_protocol_sets_v1.$ext" "paper/figures/arsiv/final_tr_2026-10-04/fig_protocol_sets_v3_2026-10-03.$ext" && echo "arsiv <- final_tr/fig_protocol_sets_v1.$ext"
done
chown -R 1000:1000 paper/figures results/q1 2>/dev/null
ls paper/figures/final/ | grep -c v1 || true
