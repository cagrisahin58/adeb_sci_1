#!/bin/bash
# R1 egitim logunda N epoch ozeti bekle, sonra ozetleri bas.
F=/home/firat/projects/adeb_sci_1/logs/R1_resnet_at_run3.log
N=${1:-3}
while true; do
    C=$(grep -ac 'Epoch [0-9]*/100 - Loss' "$F" 2>/dev/null)
    C=${C:-0}
    if [ "$C" -ge "$N" ]; then break; fi
    if grep -aq Traceback "$F" 2>/dev/null; then echo TRACEBACK_DETECTED; break; fi
    sleep 20
done
grep -a -oE 'Epoch [0-9]+/100 - Loss.*|Best model saved.*|Resuming from epoch.*' "$F" | tail -10
nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader
