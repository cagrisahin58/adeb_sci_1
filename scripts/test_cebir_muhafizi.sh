#!/usr/bin/env bash
# T4 CEBIR MUHAFIZI SINAMASI
#
# "Gecen bir kontrol, yakaladigini kanitlamaz." Bu betik, Denklem 1'in
# YANLIS bicimini (e(1-p)) gecici olarak metne enjekte eder ve kapinin
# GERCEKTEN KALDIGINI dogrular. Sonra metni geri alir.
#
# Enjekte edilen hata, uc hakem turu gecen gercek hatanin ta kendisidir.
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
EN=paper/manuscript/sections/04_experiments.tex
TR=paper/manuscript_tr/sections/04_deneyler.tex
YON=paper/manuscript/sections/03_methodology.tex
YEDEK=$(mktemp -d)
# GERI ALMA DOSYADAN, git'ten DEGIL: git checkout, HENUZ ISLENMEMIS
# degisiklikleri de siler (bu betik bir kez tam da oyle yapti).
trap 'cp "$YEDEK/en.tex" "$EN"; cp "$YEDEK/tr.tex" "$TR"; cp "$YEDEK/yon.tex" "$YON"; rm -rf "$YEDEK"' EXIT
cp "$EN" "$YEDEK/en.tex"; cp "$TR" "$YEDEK/tr.tex"; cp "$YON" "$YEDEK/yon.tex"

kapi() {
    docker exec -w /workspace adeb_eval python scripts/check_manuscript_claims.py \
        >/dev/null 2>&1 && echo GECTI || echo KALDI
}

echo "=== KOL 0: dokunulmamis metin (GECTI beklenir) ==="
echo -n "  sonuc: "; kapi

echo
echo "=== KOL 1: EN'e yanlis bicim enjekte (KALDI beklenmeli) ==="
python3 - "$EN" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
assert r"e\,p + r_{\text{cond}}" in t
p.write_text(t.replace(r"e\,p + r_{\text{cond}}",
                       r"e\,(1-p) + r_{\text{cond}}", 1), encoding="utf-8")
PY
echo -n "  sonuc: "; k1=$(kapi); echo "$k1"
cp "$YEDEK/en.tex" "$EN"

echo
echo "=== KOL 2: TR'ye yanlis bicim enjekte (KALDI beklenmeli) ==="
python3 - "$TR" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
assert r"e\,p + r_{\text{koş}}" in t
p.write_text(t.replace(r"e\,p + r_{\text{koş}}",
                       r"e\,(1-p) + r_{\text{koş}}", 1), encoding="utf-8")
PY
echo -n "  sonuc: "; k2=$(kapi); echo "$k2"
cp "$YEDEK/tr.tex" "$TR"

echo
echo "=== KOL 3: 'primary transfer metric' geri getirilir (KALDI beklenmeli) ==="
python3 - "$YON" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); t = p.read_text(encoding="utf-8")
p.write_text(t.replace("Our transfer metrics are a family",
                       "Our primary transfer metric is the family", 1),
             encoding="utf-8")
PY
echo -n "  sonuc: "; k3=$(kapi); echo "$k3"
cp "$YEDEK/yon.tex" "$YON"

echo
if [ "$k1" = KALDI ] && [ "$k2" = KALDI ] && [ "$k3" = KALDI ]; then
    echo "SINAMA GECTI: muhafiz uc hata bicimini de yakaliyor."
else
    echo "SINAMA BASARISIZ: muhafiz sessiz kaldi (k1=$k1 k2=$k2 k3=$k3)"
    exit 1
fi
