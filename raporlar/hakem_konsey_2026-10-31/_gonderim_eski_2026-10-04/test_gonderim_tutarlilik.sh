#!/usr/bin/env bash
# MUHAFIZ SINAMASI: gonderim kapisi gercekten YAKALIYOR mu?
#
# Bu kapi, 2026-08-25'te bulunan bir bosluk yuzunden yazildi: alti kapinin
# hicbiri paper/submission/ altini taramiyordu ve o klasordeki dosyalar
# 2026-02-16'dan beri eski basligi, KARANTINADAKI run2 sayilarini ve
# makalenin sonradan CURUTTUGU bir sonucu tasiyordu.
#
# Kapi numpy gerektirdigi icin KAPSAYICIDA kosar; gecici kopya
# kapsayicinin gordugu yere (/workspace altina) konur ve sonunda silinir.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
# -e SART: docker exec ana makinenin ortam degiskenlerini TASIMAZ. Bu
# unutuldugunda enjeksiyonlar kapiya ULASMAZ ve butun kollar sahte
# GECTI verir -- sinama, sinamadigi seyi sinamis gibi gorunur.
DEX=(docker exec -w /workspace -e MANUSCRIPT_ROOT adeb_eval python)
T=.sinama_gonderim
temizle() { docker exec -w /workspace adeb_eval rm -rf "$T" 2>/dev/null; rm -rf "$T" 2>/dev/null; }
trap temizle EXIT
temizle

mkdir -p "$T/paper"
cp -r paper/submission paper/manuscript "$T/paper/"
export MANUSCRIPT_ROOT="/workspace/$T"
kos() { "${DEX[@]}" scripts/gonderim_tutarlilik.py 2>&1; }

KL="$T/paper/submission/cover_letter.tex"
OC="$T/paper/submission/highlights.txt"

echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
kos | tail -2

echo
echo "=== 1) ESKI BASLIK geri gelsin -> KALMALI ==="
python3 - "$KL" <<'PY'
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
e = "The Measurement Protocol Decides the Conclusion: A Methodological Study of CNN and Vision Transformer Adversarial Robustness Comparisons"
if e not in t:
    sys.exit("SINAMA HATASI: guncel baslik bulunamadi -- kol KOSULMADI")
p.write_text(t.replace(e, "A Comparative Study of Convolutional and Transformer Architectures", 1), encoding="utf-8")
PY
kos | grep -E "cover_letter|SONUC" | head -2
cp paper/submission/cover_letter.tex "$KL"

echo
echo "=== 2) KARANTINADAKI run2 sayisi enjekte -> KALMALI ==="
python3 - "$OC" <<'PY'
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
if "37.93" not in t:
    sys.exit("SINAMA HATASI: guncel AA degeri yok -- kol KOSULMADI")
p.write_text(t.replace("37.93", "35.74", 1), encoding="utf-8")
PY
kos | grep -E "KARANTINA DEGERI|SONUC" | head -2
cp paper/submission/highlights.txt "$OC"

echo
echo "=== 3) CURUTULMUS IDDIA geri gelsin -> KALMALI ==="
python3 - "$OC" <<'PY'
import pathlib
import sys
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
p.write_text(t + "\n7. Conditioned transfer between matched AT models is symmetric.\n", encoding="utf-8")
PY
kos | grep -E "CURUK IFADE|SONUC" | head -2
cp paper/submission/highlights.txt "$OC"

echo
echo "=== 4) TASIYICI SAYI silinsin -> KALMALI ==="
python3 - "$OC" "$KL" <<'PY'
import pathlib
import sys
for f in sys.argv[1:]:
    p = pathlib.Path(f)
    t = p.read_text(encoding="utf-8")
    p.write_text(t.replace("15.01", "15.99"), encoding="utf-8")
PY
kos | grep -E "protokol yayilimi|SONUC" | head -2
cp paper/submission/highlights.txt "$OC"
cp paper/submission/cover_letter.tex "$KL"

echo
echo "=== 5) EKSIK DOSYA -> SESSIZ GECMEMELI ==="
rm -f "$T/paper/submission/declarations.txt"
kos | tail -1

echo
echo "=== 6) GERI ALINDI -> yine GECMELI ==="
cp paper/submission/declarations.txt "$T/paper/submission/"
kos | tail -2

echo
echo "NOT: gercek depoya DOKUNULMADI; gecici kopya silindi."
