#!/bin/bash
cd /home/firat/projects/adeb_sci_1 || exit 1
echo "=== robustbench_zoo Linf ==="
ls -la models/robustbench_zoo/cifar10/Linf/ 2>&1
echo "=== panel uyeleri dosya varligi ==="
for m in Wong2020Fast Engstrom2019Robustness Carmon2019Unlabeled Gowal2020Uncovering_28_10_extra Sehwag2021Proxy_R18 Addepalli2022Efficient_RN18 Rade2021Helper_R18_ddpm; do
  f=models/robustbench_zoo/cifar10/Linf/$m.pt
  if [ -f "$f" ]; then echo "VAR $f $(stat -c %s "$f")"; else echo "YOK $f"; fi
done
f=models/robustbench_zoo/cifar10/Linf/Debenedetti2022Light_XCiT-S12.pth.tar
if [ -f "$f" ]; then echo "VAR $f $(stat -c %s "$f")"; else echo "YOK $f"; fi
echo "=== matris_panel.log icinde panel uyelerinin yuklenmesi ==="
cat results/q1/konsey_smoke/matris_panel.log
echo "=== C1 kontrol noktalari ==="
for s in 1001 1002 1003; do ls -la models/c1/resnet18_s$s/resnet18/adv/adversarial_training/best.pth 2>&1; done
for s in 2001 2002 2003; do ls -la models/c1/vit_tiny_s$s/vit_tiny/adv/adversarial_training/best.pth 2>&1; done
echo "=== models/q1/konsey ==="
ls -la models/q1/konsey/ 2>&1
echo "=== matris_panel transfer_matrix.json model listesi ==="
python3 -c "import json;d=json.load(open('results/q1/konsey_smoke/matris_panel/transfer_matrix.json'));print(list(d.keys()));print(d.get('models') or d.get('model_names') or d.get('sources'))"
echo "=== WRN_28_10 nedir (kod) ==="
grep -rn "WRN_28_10" --include=*.py experiments scripts src 2>/dev/null | head -10
echo "=== disk ==="
df -h /home/firat/projects/adeb_sci_1 | tail -1
