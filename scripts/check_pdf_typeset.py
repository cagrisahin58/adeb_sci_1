"""Dizgi denetimi (render kapisi eki, 2026-10-04): PDF'de
(1) gomulu yazi tipleri arasinda kalin ve italik Times var mi, govde CM'e dusmus mu,
(2) metin satirlari sutun kenarini asiyor mu (sutun kenarlari TUM sayfalardaki satir
    baslangiclarindan kestirilir; tam genislik float'lar ve son sayfa biyografileri disarida),
(3) LaTeX gunlugunde 'Font shape T1/times ... undefined' uyarisi var mi.
Konteynerde: docker exec -w /workspace adeb_eval python scripts/check_pdf_typeset.py [main.pdf] [main.log] [--ayrinti]
Cikis kodu 0 = GECTI, 1 = KALDI.
"""
import collections
import re
import sys

import fitz  # type: ignore

args = [a for a in sys.argv[1:] if not a.startswith("--")]
AYRINTI = "--ayrinti" in sys.argv
pdf = args[0] if len(args) > 0 else "paper/manuscript/main.pdf"
log = args[1] if len(args) > 1 else "paper/manuscript/main.log"
TOL = 2.0  # pt

doc = fitz.open(pdf)
hata = []

# (1) yazi tipleri
fonts = set()
for page in doc:
    for f in page.get_fonts():
        fonts.add(f[3])
names = " ".join(sorted(fonts)).lower()
kalin = any(k in names for k in ("timesltstd-bold", "times-bold", "timesbold", "nimbusromno9l-medi", "ptmb"))
italik = any(k in names for k in ("timesltstd-italic", "times-italic", "timesitalic", "nimbusromno9l-regui", "ptmri"))
times_govde = any(k in names for k in ("timesltstd-roman", "times-roman", "nimbusromno9l-regu", "ptmr"))
cm_govde = any(k in names for k in ("sfrm1000", "sfrm0900"))  # cm-super govde = Times yuklenememis
print(f"yazi tipleri ({len(fonts)}): {sorted(fonts)}")
if not kalin:
    hata.append("gomulu KALIN Times yok (textbf basilmiyor)")
if not italik:
    hata.append("gomulu ITALIK Times yok (emph basilmiyor)")
if not times_govde or cm_govde:
    hata.append("govde Times degil (cm-super/CM'e dusmus)")

# (2) sutun kenarlari: tum sayfalardan
W = doc[0].rect.width
all_lines = []  # (pno, x0, x1, y0, text)
for pno, page in enumerate(doc, 1):
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b["lines"]:
            x0, y0, x1, y1 = l["bbox"]
            if x1 - x0 < 20:
                continue
            # sekil ici metin (LMSans, DejaVu vb.) sutun denetimine girmez; govde/tablo
            # metni Times, Formata ya da CM/Nimbus ile dizilir
            fontlar = " ".join(s.get("font", "") for s in l["spans"]).lower()
            if not any(k in fontlar for k in ("times", "formata", "cm", "nimbus", "giovanni")):
                continue
            all_lines.append((pno, x0, x1, y0, "".join(s["text"] for s in l["spans"])))
cnt = collections.Counter(round(x0) for _, x0, _, _, _ in all_lines)
common = [x for x, _ in cnt.most_common(8)]
left = min(common)
right_cands = [x for x in common if x > left + 150]
right = min(right_cands) if right_cands else None
if right is None:
    print("sutun kenarlari kestirilemedi; tasma denetimi atlandi")
    tasma = []
else:
    col_w = (W - 2 * left - (right - left - 0)) if False else None
    # sol sutunun sag kenari = sag sutunun sol kenari - ara bosluk; ara bosluk sayfa
    # genisliginden: iki sutun + bosluk = W - 2*left  =>  sutun = right - left - gutter.
    # IEEE Access'te ara bosluk ~ 0.2in = 14.4pt; onu metinden kestirmek yerine sabit al.
    GUTTER = 14.0
    col1_r = right - GUTTER
    page_r = W - left
    if AYRINTI:
        print(f"kenarlar: sol={left} sag_sutun_baslangic={right} sol_sutun_sag={col1_r:.1f} sag_kenar={page_r:.1f}")
    # Tam genislik float (table*/figure*) tasiyan sayfalarda, iki sutunlu govde metninin
    # basladigi y'nin ustu float alanidir ve denetim disi kalir ([!t] yerlesimi).
    float_pages = set()
    for pno, x0, x1, y0, txt in all_lines:
        if x0 < right - 20 and x1 > right + 20:
            float_pages.add(pno)
    body_start = {}
    for pno, x0, x1, y0, txt in all_lines:
        if pno in float_pages and x0 < left + 3 and col1_r - 40 < x1 <= col1_r + TOL:
            body_start[pno] = min(body_start.get(pno, 1e9), y0)
    tasma = []
    for pno, x0, x1, y0, txt in all_lines:
        # ara boslugu asan ve sag sutunun icine 20 pt'den fazla giren satir tam genislik
        # (ozet, anahtar kelimeler, table*/figure* basligi) sayilir ve denetim disi kalir
        tam_genislik = x0 < right - 20 and x1 > right + 20
        if tam_genislik:
            continue
        if pno in body_start and y0 < body_start[pno] - 2:
            continue
        if x0 < col1_r - 5 and x1 > col1_r + TOL and x1 < right + 40:
            tasma.append((pno, "sol sutun -> ara bosluk", round(x1 - col1_r, 1), txt[:60]))
        if x1 > page_r + TOL:
            tasma.append((pno, "sag kenar", round(x1 - page_r, 1), txt[:60]))
for t in tasma[:60]:
    print("TASMA", t)
if tasma:
    sayfalar = sorted({t[0] for t in tasma})
    hata.append(f"{len(tasma)} satir sutun kenarini asiyor (sayfalar {sayfalar})")

# (3) gunluk
try:
    with open(log, encoding="utf-8", errors="ignore") as fh:
        L = fh.read()
    undef = re.findall(r"Font shape `T1/times[^']*' undefined", L)
    if undef:
        hata.append(f"gunlukte {len(undef)} 'T1/times ... undefined' uyarisi")
except FileNotFoundError:
    print("gunluk yok, atlandi")

if hata:
    print("SONUC: KALDI --", "; ".join(hata))
    sys.exit(1)
print("SONUC: GECTI -- kalin/italik Times gomulu, sutun tasmasi yok, yazi tipi uyarisi yok.")
