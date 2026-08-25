#!/usr/bin/env python3
"""Iddia kapisinda METIN koku ile ARTEFAKT koku ayrilir.

Sorun: oz-sinama yalniz paper/ dizinini gecici bir kopyaya alip
MANUSCRIPT_ROOT'u oraya cevirir. H1/H2 muhafizlari ARTEFAKT okudugu icin
(results/q1/e3_akolu_v2, results/q1/e3_iki_kol_fit.json) o gecici kokte
hicbir sey bulamaz ve BOZULMAMIS kopyada bile KALDI verir. Kapi dogru,
oz-sinamanin tabani kirli: bir sonraki okuyucu KALAN=2'yi gorup gercek mi
sahte mi ayirt edemez.

Cozum (besinci kapida uygulanan ayni desen): MANUSCRIPT_ROOT yalniz METNI
tasir; artefaktlar ARTEFAKT_ROOT'tan (varsayilan: gercek depo) okunur.
"""
import sys
from pathlib import Path

p = Path("/home/firat/projects/adeb_sci_1/scripts/check_manuscript_claims.py")
t = p.read_text(encoding="utf-8")

if "ARTEFAKT_ROOT" in t:
    print("zaten yamali")
    sys.exit(0)

ESKI = '''# MANUSCRIPT_ROOT: oz-sinama kirilmis bir KOPYAYI denetlemek icin kullanir.
_kok = os.environ.get("MANUSCRIPT_ROOT")'''
YENI = '''# MANUSCRIPT_ROOT: oz-sinama kirilmis bir METIN KOPYASINI denetlemek icin
# kullanir. ARTEFAKT okuyan muhafizlar (H1/H2) bu koke BAKMAZ; onlar
# ARTEFAKT_ROOT'tan okur ve varsayilani gercek depodur. Ayrilmasaydi
# oz-sinama, yalniz paper/ kopyalandigi icin bozulmamis kopyada bile
# KALDI verirdi (2026-08-25'te tam bu oldu).
_kok = os.environ.get("MANUSCRIPT_ROOT")'''

if t.count(ESKI) != 1:
    print(f"BASARISIZ (yorum): {t.count(ESKI)} eslesme")
    sys.exit(1)
t = t.replace(ESKI, YENI, 1)

# ARTEFAKT_ROOT tanimi: R = ROOT / "paper" satirindan hemen once
ESKI2 = 'R = ROOT / "paper"'
YENI2 = ('_avar = os.environ.get("ARTEFAKT_ROOT")\n'
         'ARTEFAKT_ROOT = Path(_avar) if _avar else (\n'
         '    Path("/workspace") if Path("/workspace/results").is_dir()\n'
         '    else Path(__file__).resolve().parents[1])\n'
         '\n'
         'R = ROOT / "paper"')
if t.count(ESKI2) != 1:
    print(f"BASARISIZ (R): {t.count(ESKI2)} eslesme")
    sys.exit(1)
t = t.replace(ESKI2, YENI2, 1)

# H1/H2 artik ARTEFAKT_ROOT okur
for eski, yeni in (
    ('_av2 = ROOT / "results/q1/e3_akolu_v2"',
     '_av2 = ARTEFAKT_ROOT / "results/q1/e3_akolu_v2"'),
    ('_ikk = ROOT / "results/q1/e3_iki_kol_fit.json"',
     '_ikk = ARTEFAKT_ROOT / "results/q1/e3_iki_kol_fit.json"'),
):
    if t.count(eski) != 1:
        print(f"BASARISIZ (H): {t.count(eski)} eslesme -- {eski}")
        sys.exit(1)
    t = t.replace(eski, yeni, 1)

p.write_text(t, encoding="utf-8")
print("metin koku ile artefakt koku ayrildi")
