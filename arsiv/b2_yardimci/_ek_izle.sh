#!/bin/bash
# Gunluk izleyici: yeni olay satirlarini basar, bitti/DUR gorunce cikar. Kullanim: _ek_izle.sh <log>
L=$1
onceki=0
while true; do
    if [ -f "$L" ]; then
        n=$(wc -l < "$L")
        if [ "$n" -gt "$onceki" ]; then
            sed -n "$((onceki+1)),${n}p" "$L" | grep -E 'rc=|basliyor|DUR|bitti|Traceback|Error|FARKLI|ayni|BIREBIR|Killed|denetim|Sonuc'
            onceki=$n
        fi
        if grep -qE '^DUR:|[0-9] bitti$' "$L"; then echo "IZLEYICI: son satir goruldu"; exit 0; fi
        if ! pgrep -f "ek_zincir_komutlari.sh" >/dev/null; then echo "IZLEYICI: zincir sureci yok, son: $(tail -1 "$L")"; exit 0; fi
    fi
    sleep 20
done
