#!/usr/bin/env bash
# transfer_matrix.json tasiyan her havuz klasorunde q1_havuz_analiz.py kosar (idempotent), sonra
# yayilim-temiz fark verisini toplar. Konteynerde: docker exec -w /workspace adeb_eval bash scripts/q1_havuz_analiz_hepsi.sh
set -u
cd /workspace || exit 1
for d in results/c1_c3/pair1 results/c1_c3/pair2 results/c1_c3/pair3 \
         results/q1/temiz_ciftler/pair1 results/q1/temiz_ciftler/pair2 results/q1/temiz_ciftler/pair3 \
         results/q1/son_kontrol_noktasi/pair1 results/q1/son_kontrol_noktasi/pair2 results/q1/son_kontrol_noktasi/pair3 \
         results/q1/havuz_cifar10; do
    if [ -f "$d/transfer_matrix.json" ]; then
        if python experiments/q1_havuz_analiz.py "$d" --bootstrap 2000 > "$d/havuz_analiz.log" 2>&1; then
            echo "analiz ok   $d"
        else
            echo "analiz HATA $d"; tail -3 "$d/havuz_analiz.log"
        fi
    else
        echo "bekliyor    $d"
    fi
done
python scripts/fig_yayilim_temiz_fark_veri.py 2>&1 | grep -v '^YOK' | tail -12
