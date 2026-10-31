#!/bin/bash
# Kullanim: _ek_bekle.sh <log> <desen> <en_cok_saniye>; desen gorulene ya da sure dolana kadar bekler.
L=$1; P=$2; T=${3:-540}
s=0
while [ "$s" -lt "$T" ]; do
    grep -qE "$P" "$L" 2>/dev/null && { echo "DESEN_GORULDU ($s s)"; break; }
    pgrep -f ek_zincir_komutlari.sh >/dev/null || { echo "ZINCIR_SURECI_YOK ($s s)"; break; }
    sleep 10; s=$((s+10))
done
[ "$s" -ge "$T" ] && echo "SURE_DOLDU"
date '+%F %T'
tail -30 "$L"
