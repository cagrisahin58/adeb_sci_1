#!/usr/bin/env python3
"""Iddia oz-sinamasina ARTEFAKT_ROOT verir.

Sinama kapiyi $TMP/chk.py olarak KOPYALAYIP calistiriyor; bu yuzden kapinin
artefakt koku (dosya konumundan turetilir) /tmp'ye dusuyor ve artefakt okuyan
muhafizlar (H1/H2) bozulmamis kopyada bile KALDI veriyordu. Artefakt koku
acikca GERCEK DEPOYA baglanir; metin koku gecici kopyada kalir.

Ayrica UCUNCU bir kol eklenir: artefakt koku BOS bir dizine cevrilirse kapi
KALMALIDIR -- yani artefakt muhafizlari sessizce gecmemelidir.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/test_claim_guards.sh")
t = p.read_text(encoding="utf-8")

if "ARTEFAKT_ROOT" in t:
    print("zaten yamali")
    sys.exit(0)

ESKI = 'export MANUSCRIPT_ROOT="$TMP"\necho "MANUSCRIPT_ROOT=$MANUSCRIPT_ROOT"'
YENI = ('export MANUSCRIPT_ROOT="$TMP"\n'
        '# Kapi $TMP/chk.py olarak KOPYALANIP calistirildigi icin artefakt koku\n'
        '# dosya konumundan /tmp diye turetilirdi ve artefakt okuyan muhafizlar\n'
        '# (H1/H2) bozulmamis kopyada bile KALIRDI. Artefakt koku GERCEK depodur.\n'
        'export ARTEFAKT_ROOT="/home/firat/projects/adeb_sci_1"\n'
        'echo "MANUSCRIPT_ROOT=$MANUSCRIPT_ROOT"\n'
        'echo "ARTEFAKT_ROOT=$ARTEFAKT_ROOT"')

if t.count(ESKI) != 1:
    print(f"BASARISIZ: {t.count(ESKI)} eslesme")
    sys.exit(1)
t = t.replace(ESKI, YENI, 1)

# sona artefakt kolu
EK = '''
echo
echo "=== A) ARTEFAKT koku BOS dizine cevrilsin -> H1/H2 KALMALI ==="
BOS=$(mktemp -d)
ARTEFAKT_ROOT="$BOS" python3 "$TMP/chk.py" 2>&1 | grep -E "^H1|^H2|TOPLAM"
rm -rf "$BOS"
'''
t = t.rstrip("\n") + "\n" + EK
p.write_text(t, encoding="utf-8")
print("oz-sinamaya artefakt koku ve ucuncu kol eklendi")
