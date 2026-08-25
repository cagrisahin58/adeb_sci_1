#!/usr/bin/env bash
# check_abstract_body.py GERCEKTEN yakaliyor mu? (F1 dersi: gecen bir kontrol,
# yakaladigini kanitlamaz.) Gecici kopyada oze SAHTE bir sayi enjekte edilir.
#
# 2026-08-25: enjeksiyon capasi METNE civiliydi ("a 3.3-fold spread") ve ozet
# yeniden yazilinca SESSIZCE dustu -- assert patladi, kol kosmadi, betik yine
# "GECTI" gibi gorundu. Kapinin sinanmadigini fark etmek zor olurdu. Capa artik
# ozet ORTAMINA baglanmistir; metin degisse de tutar. Ayrica enjeksiyonun
# GERCEKTEN yapildigi dogrulanir.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

cp -r paper "$TMP/paper"
cp scripts/check_abstract_body.py "$TMP/chk.py"
sed -i "s|^ROOT = .*|ROOT = Path(\"$TMP\")|" "$TMP/chk.py"
grep -n '^ROOT = ' "$TMP/chk.py"

echo
echo "=== 0) BOZULMAMIS kopya -> GECMELI ==="
python3 "$TMP/chk.py" | tail -2

echo
echo "=== 1) oze GOVDEDE OLMAYAN sayi enjekte -> KALMALI ==="
python3 - "$TMP/paper/manuscript/main.tex" ekle <<'PY'
import pathlib
import re
import sys

p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", t, re.S)
if not m:
    sys.exit("SINAMA HATASI: ozet ortami bulunamadi -- kol KOSULMADI")
govde = m.group(1)
nokta = govde.find(". ")
if nokta < 0:
    sys.exit("SINAMA HATASI: ozette cumle siniri yok -- kol KOSULMADI")
yeni = govde[:nokta + 1] + " A headline value of 77.31 points follows." + govde[nokta + 1:]
t = t[:m.start(1)] + yeni + t[m.end(1):]
p.write_text(t, encoding="utf-8")
if "77.31" not in p.read_text(encoding="utf-8"):
    sys.exit("SINAMA HATASI: enjeksiyon YAZILMADI")
print("  (enjekte edildi: 77.31)")
PY
python3 "$TMP/chk.py" | tail -4

echo
echo "=== 2) YUVARLAMA farki -> yanlis alarm VERMEMELI ==="
python3 - "$TMP/paper/manuscript/main.tex" <<'PY'
import pathlib
import sys

p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
t = t.replace(" A headline value of 77.31 points follows.", "", 1)
if "77.31" in t:
    sys.exit("SINAMA HATASI: enjeksiyon geri alinamadi")
p.write_text(t, encoding="utf-8")
PY
python3 "$TMP/chk.py" | tail -2

echo
echo "=== 3) OZET COK UZUN -> uzunluk muhafizi KALMALI ==="
python3 - "$TMP/paper/manuscript/main.tex" <<'PY'
import pathlib
import re
import sys

# SAYI-NOTR uzatma: ozet govdesi IKI KEZ yazilir. Kelime sayisi ikiye
# katlanir, gecen sayilar kumesi DEGISMEZ; boylece yalnizca uzunluk
# muhafizi tetiklenebilir ve kol gercekten uzunlugu sinar.
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding="utf-8")
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", t, re.S)
if not m:
    sys.exit("SINAMA HATASI: ozet ortami bulunamadi -- kol KOSULMADI")
govde = m.group(1)
t = t[:m.start(1)] + govde + " " + govde.strip() + t[m.end(1):]
p.write_text(t, encoding="utf-8")
print(f"  (ozet {len(govde.split())} -> {2 * len(govde.split())} kelimeye cikarildi)")
PY
python3 "$TMP/chk.py" | grep -E "ozet uzunlugu|SONUC"

echo
echo "NOT: gercek depoya DOKUNULMADI."
