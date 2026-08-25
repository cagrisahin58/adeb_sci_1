#!/usr/bin/env bash
# MUHAFIZ SINAMASI: sayi kapisi gercekten YAKALIYOR mu?
#
# 2026-08-25 denetimi olctu: kapi CIPLAK ALT DIZE ariyordu, bu yuzden
# manset sayiya bir rakam eklendiginde ('19.37' -> '119.37') yine GECTI
# diyordu. Eslesme artik SAYI SINIRINA bagli; bu sinama onu dogrular.
#
# Kapi numpy gerektirdigi icin KAPSAYICIDA kosar; bu yuzden gecici kopya
# kapsayicinin gordugu yere (/workspace altina) konur ve sonunda silinir.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
DEX=(docker exec -w /workspace adeb_eval)
T=.sinama_sayilar
temizle() { "${DEX[@]}" rm -rf "$T" 2>/dev/null; rm -rf "$T" 2>/dev/null; }
trap temizle EXIT
temizle

mkdir -p "$T/paper"
cp -r paper/manuscript paper/manuscript_tr "$T/paper/"
ln -sfn /workspace/results "$T/results"
sed "s|^ROOT = .*|ROOT = Path(\"/workspace/$T\")|" \
    scripts/verify_manuscript_numbers.py > "$T/chk.py"

kos() { "${DEX[@]}" python "$T/chk.py" 2>&1; }
EXP="$T/paper/manuscript/sections/04_experiments.tex"

echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
kos | tail -2

echo
echo "=== 1) MANSET sayiya rakam eklensin (19.37 -> 119.37) -> KALMALI ==="
sed -i 's/+19\.37\\pm1\.27/+119.37\\pm1.27/' "$EXP"
grep -c '119\.37' "$EXP" | xargs echo "  enjekte edilen yer sayisi:"
kos | grep -E "basarili-kaynak fark|SONUC" | head -2
sed -i 's/+119\.37\\pm1\.27/+19.37\\pm1.27/' "$EXP"

echo
echo "=== 2) ONDALIK basamak eklensin (15.01 -> 15.015) -> KALMALI ==="
sed -i 's/15\.01\\pm0\.84/15.015\\pm0.84/g' "$EXP"
kos | grep -E "protokol yayilimi|SONUC" | head -2
sed -i 's/15\.015\\pm0\.84/15.01\\pm0.84/g' "$EXP"

echo
echo "=== 3) GERI ALINDI -> yine GECMELI ==="
kos | tail -2

echo
echo "NOT: gercek depoya DOKUNULMADI; gecici kopya silindi."
