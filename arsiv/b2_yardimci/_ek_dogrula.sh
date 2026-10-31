#!/bin/bash
# IS 1, adim 5: dogrulama (tarifteki bes komut + iki ek)
set -uo pipefail
cd /home/firat/projects/adeb_sci_1
ts() { echo "[$(date '+%F %T')] $*"; }
GEC=0; KAL=0
sonuc() { if [ "$1" -eq 0 ]; then echo "SONUC $2: GECTI"; GEC=$((GEC+1)); else echo "SONUC $2: GECMEDI (rc=$1)"; KAL=$((KAL+1)); fi; }

ts "D1 nvidia-smi"
docker exec adeb_eval nvidia-smi; sonuc $? D1

ts "D2 import"
docker exec -w /workspace adeb_eval python -c "import torch, timm, robustbench, autoattack; print(torch.__version__, timm.__version__, torch.cuda.is_available())"; sonuc $? D2

ts "D3 epochs ls -L"
docker exec -w /workspace adeb_eval bash -c 'set -o pipefail; ls -L models/q1/e2/resnet18_s1001/resnet18/adv/adversarial_training/epochs | head -3'; sonuc $? D3

ts "D4 epoch_100.pth yukleme"
docker exec -w /workspace adeb_eval python -c "import torch; d=torch.load('models/q1/e2/resnet18_s1001/resnet18/adv/adversarial_training/epochs/epoch_100.pth', map_location='cpu', weights_only=False); print(d['epoch'], d['adv_acc'])"; sonuc $? D4

ts "D5 /veri 1 GB dd yaz-sil"
docker exec adeb_eval bash -c 'dd if=/dev/zero of=/veri/_dd_sinama bs=1M count=1024 conv=fdatasync && rm /veri/_dd_sinama'; sonuc $? D5
docker exec adeb_eval bash -c 'test ! -e /veri/_dd_sinama && echo dd_dosyasi_silindi'

ts "D6 imagenetv2 gorunur"
docker exec -w /workspace adeb_eval test -r data/imagenetv2/imagenetv2-matched-frequency-format-val/0 && echo D_GORUNUR; sonuc $? D6

ts "D7 robustbench_zoo imagenet/Linf (15 bekleniyor)"
n=$(docker exec -w /workspace adeb_eval ls -L models/robustbench_zoo/imagenet/Linf | wc -l); echo "$n"
[ "$n" -eq 15 ]; sonuc $? D7
docker exec -w /workspace adeb_eval ls -lL models/robustbench_zoo/imagenet/Linf

ts "D8 robustbench_zoo cifar100/Linf (11 bekleniyor)"
n=$(docker exec -w /workspace adeb_eval ls -L models/robustbench_zoo/cifar100/Linf | wc -l); echo "$n"
[ "$n" -eq 11 ]; sonuc $? D8
docker exec -w /workspace adeb_eval ls -lL models/robustbench_zoo/cifar100/Linf

ts "OZET gecen=$GEC kalan=$KAL"
