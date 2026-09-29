#!/usr/bin/env bash
# SEKIZINCI KAPI SINAMASI (2. surum).
#
# Ilk surum \maketitle'i tasiyordu ve enjeksiyon etkisiz kalip iki kol da
# GECTI verdi -- yani sinama, sinadigini kanitlayamadi. Bu surum 09-01'deki
# GERCEK hatayi birebir uretir: ozet+anahtar kelime blogunu \maketitle'in
# ARKASINA tasir. Sonra GERCEK kapi betigini (check_pdf_render.py) gecici
# PDF uzerinde calistirir. Her kol icin enjeksiyonun tuttugunu satir
# numaralariyla GOSTERIR. Depoya dokunmaz.
set -u
KOK=/home/firat/projects/adeb_sci_1
cd "$KOK/paper" || exit 1
T=$(mktemp -d); trap 'rm -rf "$T" "$KOK"/results/q1_research/_sinama_k[01].pdf' EXIT
cp -r manuscript "$T/m"; cp -r figures "$T/figures"

derle_ve_kopyala() {  # $1 = kol adi
    (cd "$T/m" && latexmk -C >/dev/null 2>&1; latexmk -pdf -interaction=nonstopmode main.tex >/dev/null 2>&1)
    if [ ! -f "$T/m/main.pdf" ]; then echo "  ($1: PDF uretilemedi)"; return 1; fi
    cp "$T/m/main.pdf" "$KOK/results/q1_research/_sinama_$1.pdf"
}
kapi() {  # $1 = kol adi -> GECTI/KALDI (gercek kapi betigi)
    docker exec -w /workspace adeb_eval python scripts/check_pdf_render.py \
        "results/q1_research/_sinama_$1.pdf" >/dev/null 2>&1 && echo GECTI || echo KALDI
}
sira() { grep -n '^\\maketitle\|^\\begin{abstract}\|^\\end{IEEEkeywords}' "$T/m/main.tex" | tr '\n' ' '; }

echo "Kol 0: dokunulmamis kaynak   (GECTI beklenir)"
echo "   sira: $(sira)"
derle_ve_kopyala k0 && k0=$(kapi k0) || k0=HATA
echo "   sonuc: $k0"

echo "Kol 1: ozet blogu \\maketitle'in ARKASINA (09-01 hatasi)   (KALDI beklenir)"
python3 - "$T/m/main.tex" <<'PY'
import pathlib, sys, re
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
m = re.search(r"\\begin\{abstract\}.*?\\end\{IEEEkeywords\}\n", t, re.DOTALL)
assert m, "ozet blogu bulunamadi"
blok = m.group(0); t = t.replace(blok, "", 1)
# SATIR BASINDAKI gercek \maketitle hedeflenir. Ilk iki surum duz
# replace("\\maketitle\n") kullandi ve main.tex'teki bir YORUM satirinin
# icindeki "\maketitle" ile eslesti: blok yoruma girdi, sira degismedi,
# iki kol da GECTI verdi -- sinama sinadigini kanitlayamadi.
t, n = re.subn(r"^\\maketitle\n", lambda _: "\\maketitle\n\n" + blok, t, count=1, flags=re.M)
assert n == 1, "satir basinda \\maketitle bulunamadi"
p.write_text(t, encoding="utf-8")
PY
echo "   sira: $(sira)"
derle_ve_kopyala k1 && k1=$(kapi k1) || k1=HATA
echo "   sonuc: $k1"

echo
if [ "$k0" = GECTI ] && [ "$k1" = KALDI ]; then
    echo "SINAMA GECTI: kapi, ozeti dusuren siralama hatasini yakaliyor."
else
    echo "SINAMA BASARISIZ (k0=$k0 k1=$k1) -- kapiya GUVENILMEZ."; exit 1
fi
