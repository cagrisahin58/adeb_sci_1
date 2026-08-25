#!/usr/bin/env bash
# MUHAFIZ SINAMASI: sayi kapisi gercekten YAKALIYOR mu?
#
# 2026-08-25 denetimi olctu: kapi CIPLAK ALT DIZE ariyordu, bu yuzden bir
# tasiyici sayi daha uzun bir sayinin ICINDE eslesse bile 'OK' veriyordu.
# Eslesme artik SAYI SINIRINA bagli. Bu sinama hem duzeltmeyi hem de
# KAPATILAMAYAN SINIRI dogrular -- ikincisi bilerek boyle etiketlenmistir:
# yanlis etiketli bir sinama kolu, kapinin kendisinden daha tehlikelidir.
#
# Kapi numpy gerektirdigi icin KAPSAYICIDA kosar; gecici kopya
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

# boz <deger> <yeni>  : iki dilde TUM yazim bicimlerini degistirir
#   EN "19.37" · TR "19{,}37" ve "19,37"
boz() {
    python3 - "$T" "$1" "$2" <<'PY'
import re
import sys
from pathlib import Path
kok, eski, yeni = sys.argv[1], sys.argv[2], sys.argv[3]
tam, ondalik = eski.split(".")
y_tam, y_ondalik = yeni.split(".")
bicimler = [(f"{tam}.{ondalik}", f"{y_tam}.{y_ondalik}"),
            (f"{tam}{{,}}{ondalik}", f"{y_tam}{{,}}{y_ondalik}"),
            (f"{tam},{ondalik}", f"{y_tam},{y_ondalik}")]
n = 0
for f in Path(kok).rglob("*.tex"):
    t = f.read_text(encoding="utf-8")
    o = t
    for a, b in bicimler:
        t = re.sub(r"(?<![\d.,{])" + re.escape(a) + r"(?![\d])", b, t)
    if t != o:
        f.write_text(t, encoding="utf-8")
        n += len(re.findall(re.escape(y_tam + "." + y_ondalik), t)) or 1
print(f"    bozulan dosya sayisi: {n}")
PY
}

echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
kos | tail -2

echo
echo "=== 1) TUM gecisler bozulsun (19.37 -> 119.37) -> KALMALI ==="
boz 19.37 119.37
kos | grep -E "basarili-kaynak fark|SONUC" | head -2
boz 119.37 19.37 > /dev/null

echo
echo "=== 2) TUM gecisler bozulsun (15.01 -> 15.019) -> KALMALI ==="
boz 15.01 15.019
kos | grep -E "^protokol yayilimi|SONUC" | head -2
boz 15.019 15.01 > /dev/null

echo
echo "=== 3) BILINEN SINIR: TEK bir gecis bozulursa GORULMEZ ==="
echo "    (kapi bir VARLIK denetimidir; bkz. B2_KAPI_KUSURU.md §5.)"
EN="$T/paper/manuscript/sections/04_experiments.tex"
sed -i '0,/+19\.37\\pm1\.27/{s/+19\.37\\pm1\.27/+119.37\\pm1.27/}' "$EN"
grep -c '119\.37' "$EN" | xargs echo "    bozulan gecis sayisi:"
kos | grep -E "SONUC" | head -1
echo "    ^ GECTI demesi BEKLENEN sonuctur; sinir belgelenmistir."
sed -i 's/+119\.37\\pm1\.27/+19.37\\pm1.27/' "$EN"

echo
echo "=== 4) GERI ALINDI -> yine GECMELI ==="
kos | tail -2

echo
echo "NOT: gercek depoya DOKUNULMADI; gecici kopya silindi."
