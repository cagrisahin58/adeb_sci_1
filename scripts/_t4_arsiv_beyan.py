#!/usr/bin/env python3
"""1.7: hakem inceleme arsivi beyani.

Makale "kabul uzerine yayimlayacagiz" diyordu. Makalenin tezi
"protokolu belirtin"; hakem dort protokolu KENDISI hesaplayabilmelidir.
Anonim arsiv hazir (scripts/anonim_arsiv.sh, 446 MB, kimlik taramasi
temiz); beyan artik inceleme SIRASINDA erisimi de soyluyor.

URL kullanici tarafindan doldurulur (Anonymous-GitHub / Zenodo embargolu).
Yer tutucu TODO olarak birakilir ki kapi ve kontrol listesi yakalasin.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

KOK = Path("/home/firat/projects/adeb_sci_1/paper")

if not uygula([
    ("main.tex",
     r"which together reproduce every number reported here; the four "
     r"conditioning protocols are all computed from the per-sample records, so "
     r"the protocol comparison can be repeated without retraining",
     r"which together reproduce every number reported here; the four "
     r"conditioning protocols are all computed from the per-sample records, so "
     r"the protocol comparison can be repeated without retraining. An "
     r"anonymized copy of that archive is available to reviewers during review "
     r"at \texttt{[ANONYMOUS-ARCHIVE-URL]}, so the protocol comparison can be "
     r"checked before acceptance rather than after it",
     "1.7 EN hakem arsivi"),
], KOK / "manuscript"):
    sys.exit(1)

# TR aynasi
import re  # noqa: E402
p = KOK / "manuscript_tr/main.tex"
t = p.read_text(encoding="utf-8")
if "ANONYMOUS-ARCHIVE-URL" in t:
    print("  [=] TR zaten guncel")
else:
    m = re.search(r"(yeniden ?ürete[^.]*\.|yeniden üretmeye yeter[^.]*\.)", t)
    if not m:
        # tr beyanini bul: 'kabul üzerine' gecen cumle
        m = re.search(r"[^.]*[Kk]abul üzerine[^.]*\.", t)
    if not m:
        sys.exit("BASARISIZ: TR erisim beyani bulunamadi")
    ek = (" İncelemenin kendisi sırasında hakemlerin erişimine açık, "
          "anonimleştirilmiş bir kopya \\texttt{[ANONYMOUS-ARCHIVE-URL]} "
          "adresindedir; böylece protokol karşılaştırması kabulden sonra "
          "değil, kabulden önce denetlenebilir.")
    t = t[:m.end()] + ek + t[m.end():]
    p.write_text(t, encoding="utf-8")
    print("  [+] TR hakem arsivi beyani eklendi")
