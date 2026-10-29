#!/bin/bash
cd /home/firat/projects/adeb_sci_1
echo "=== delta kaynagi"
grep -n -E 'simetri_ihlali|def matris|AT7|hm =|hm=' raporlar/konsey_2026-10-29/_p3_carpimsal_yasa_masa.py | head -30
echo "=== FOY 1039"
grep -n -E '\+0\.796' results/C1_REFERANS_FOYU.md | head
echo "=== K5 C1 yollari"
for s in 1001 1002 1003; do ls -la "models/c1/resnet18_s${s}/resnet18/adv/adversarial_training/best.pth"; done
for s in 2001 2002 2003; do ls -la "models/c1/vit_tiny_s${s}/vit_tiny/adv/adversarial_training/best.pth"; done
echo "=== robustbench zoo"
ls models/robustbench_zoo/cifar10/Linf/ 2>&1
echo "=== rb_liste adlar"
grep -n -E 'Sehwag2021Proxy_R18|Addepalli2022Efficient_RN18|Rade2021Helper_R18_ddpm|Debenedetti2022Light_XCiT-S12|Wong2020Fast|Engstrom2019Robustness|Carmon2019Unlabeled|Gowal2020Uncovering_28_10_extra' raporlar/konsey_2026-10-29/_rb_liste.json | head -20
echo "=== havuz esleme kaynagi"
sed -n '20,40p' scripts/q1_temiz_ve_havuz_run.sh
echo "=== C1 WRN = Gowal?"
grep -n -E 'Gowal|WRN_28_10|Pang2022' experiments/c1_c3_transfer_matrix.py scripts/run_c1_pipeline.sh 2>/dev/null | head -20
