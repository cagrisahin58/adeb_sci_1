#!/bin/bash
# Celisik dogrulayici, D6: kuyrugun temiz denetim kapisi KALDI kaydindan sonra
# yeniden calistirmada atlaniyor mu? Kuyrugun defter satiri bicimi ve
# scripts/konsey_b3_kuyruk.sh:196 ile :201'deki grep kosulu birebir kopyalanir.
set -uo pipefail
T=$(mktemp -d)
DEFTER="$T/defter.tsv"
DISK=50; GMEM=3700; GUTIL=1
defter() {  # kuyruktaki fonksiyonun aynisi (satir 134-136)
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$DISK" "$GMEM" "$GUTIL" "$8" >> "$DEFTER"
}
printf "baslangic\tbitis\ttakma_ad\tasama\tsure_s\tepok\tdurum\tdisk_bos_gb\tgpu_bellek_mib\tgpu_kullanim_yuzde\tnot\n" > "$DEFTER"
t=V_IN_s2101
r="KALDI V_IN_s2101 val=85.00 ref=83.00 (n=3, C1 ViT-Tiny temiz best.pth) fark=+2.00"
defter "2026-10-29 07:00:00" "2026-10-29 07:00:00" "$t" "denetim_temiz" "" "" "${r%% *}" "${r#* }"
cat "$DEFTER"
if ! grep -q -P "\t$t\tdenetim_temiz\t\t\t(GECTI|KALDI)\t" "$DEFTER"; then
    echo "SONUC: denetim yeniden yapilir (kapi calisir)"
else
    echo "SONUC: KALDI kaydi var -> temiz_denetim CAGRILMAZ, kuyruk AT asamasina gecer (kapi atlanir)"
fi
rm -rf "$T"
