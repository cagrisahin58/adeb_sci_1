#!/bin/bash
# Celisik dogrulayici, D7: --skip-existing ile yarida kalmis bir satirin
# tamamlanmasi. Onbelleksiz ve onbellekli iki kosu: bir hucre silinip yeniden
# uretilir, yeni hucre ilk kosudaki hucreyle ornek ornek karsilastirilir.
set -euo pipefail
cd /workspace
D=results/q1/konsey_smoke/_dogrulayici
M1="ResNet18_AT_s1001:resnet18:models/c1/resnet18_s1001/resnet18/adv/adversarial_training/best.pth"
M2="ViT_Tiny_AT_s2001:vit_tiny:models/c1/vit_tiny_s2001/vit_tiny/adv/adversarial_training/best.pth"
HUCRE=per_sample_ViT_Tiny_AT_s2001_to_ResNet18_AT_s1001.npz
for kip in onbelleksiz onbellekli; do
    O="$D/d7_$kip"; C="$D/d7_onbellek"
    rm -rf "$O" "$C"
    EK=""
    [ "$kip" = onbellekli ] && EK="--cache-adv $C"
    python experiments/c1_c3_transfer_matrix.py --model "$M1" --model "$M2" --n-samples 100 --seed 42 \
        --skip-existing $EK --out-dir "$O" 2>&1 | grep -v 'it/s' | tail -2
    cp "$O/$HUCRE" "$O/ilk_$HUCRE"
    rm "$O/$HUCRE"
    python experiments/c1_c3_transfer_matrix.py --model "$M1" --model "$M2" --n-samples 100 --seed 42 \
        --skip-existing $EK --out-dir "$O" 2>&1 | grep -v 'it/s' | grep -i 'ViT_Tiny_AT_s2001->\|atlandi\|onbellek' | head -5
    python - "$O/ilk_$HUCRE" "$O/$HUCRE" "$kip" <<'PY'
import sys
import numpy as np
a, b = np.load(sys.argv[1]), np.load(sys.argv[2])
fark = {f: int((a[f] != b[f]).sum()) for f in a.files}
print(sys.argv[3], "yeniden uretilen hucre ile ilk hucre arasindaki farkli ornek sayisi:", fark)
PY
done
