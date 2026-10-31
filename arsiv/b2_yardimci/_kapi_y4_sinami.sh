#!/usr/bin/env bash
# Y4 sinami (sayi kapisi ucuncu tur, 2026-10-31): oz-sinama KALDI verirse kapilar.sh zinciri
# "OZ-SINAMA KALDI: sayi kapisi hukmu gecersiz" basip cikis 1 ile HEMEN durmali.
# kapilar.sh'nin gecici kopyasinda python cagrisi her zaman KALDI donen bir taslakla degistirilir;
# gercek kapilar ve makale kosulmaz.
set -u
KOK="$(cd "$(dirname "$0")/../.." && pwd)"
T="$(mktemp -d)"
mkdir -p "$T/scripts"
sed 's|^DEX=(.*)$|DEX=(bash -c '"'"'echo "  KALDI  3 sahte sinama"; echo "SONUC: KALDI -- sahte"; exit 1'"'"' _)|' \
    "$KOK/scripts/kapilar.sh" > "$T/scripts/kapilar.sh"
grep -q '^DEX=(bash -c' "$T/scripts/kapilar.sh" || { echo "Y4 SINAMI: DEX satiri degistirilemedi"; exit 2; }
cikti="$(bash "$T/scripts/kapilar.sh")"; rc=$?
rm -rf "$T"
echo "$cikti"
satir=$(printf '%s\n' "$cikti" | grep -c 'GECTI\|KALDI   ')
if [ "$rc" -eq 1 ] && printf '%s\n' "$cikti" | grep -q '^OZ-SINAMA KALDI: sayi kapisi hukmu gecersiz$' && [ "$satir" -eq 1 ]; then
    echo "Y4 SINAMI: GECTI (cikis $rc, yalniz oz-sinama satiri kosuldu)"
    exit 0
fi
echo "Y4 SINAMI: KALDI (cikis $rc, kapi satiri $satir)"
exit 1
