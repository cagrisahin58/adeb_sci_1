#!/bin/bash
# HEAD (4972738) kodunu dogrulayici klasorune cikarir (WSL'de firat olarak).
set -euo pipefail
cd /home/firat/projects/adeb_sci_1
D=results/q1/konsey_smoke/_dogrulayici
rm -rf "$D/eski_kod"
mkdir -p "$D/eski_kod"
git archive 4972738 src experiments/c1_c3_transfer_matrix.py | tar -x -C "$D/eski_kod"
ls "$D/eski_kod" "$D/eski_kod/src/models"
diff <(git show 4972738:experiments/c1_c3_transfer_matrix.py) "$D/eski_kod/experiments/c1_c3_transfer_matrix.py" && echo ESKI_BETIK_HEAD_ILE_AYNI
test ! -e "$D/eski_kod/src/models/r224.py" && echo ESKI_SRC_R224_YOK
git diff --stat 4972738 -- src | tail -3
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader
