#!/usr/bin/env bash
# Dokuzuncu kapinin (check_pdf_typeset.py) sinamasi: 2026-10-04 oncesi durumu birebir
# yeniden uretir -- T1 'times' yazi tipi tanimlari (t1times.fd / T1times.fd) olmadan
# derlenen PDF'de govde Computer Modern'e duser, kalin/italik hic basilmaz.
#   Kol 0: gercek derleme (fd var)        -> GECTI beklenir
#   Kol 1: fd dosyalari gecici olarak yok -> KALDI beklenir
# Gercek main.pdf'e dokunulmaz: Kol 1, paper/manuscript/_dizgi_sinama/ altina derlenir
# (WSL'deki latexmk Windows TeX Live sarmalayicisidir; /tmp gibi yollari gormez, goreli
# cikti klasoru gerekir).
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
M=paper/manuscript
SUB=_dizgi_sinama
OUT="$M/$SUB"
rm -rf "$OUT"; mkdir -p "$OUT"
DEX=(docker exec -w /workspace adeb_eval python)

echo "== Kol 0: mevcut PDF"
if "${DEX[@]}" scripts/check_pdf_typeset.py "$M/main.pdf" "$M/main.log" > "$OUT/kol0.log" 2>&1; then
    echo "Kol 0 GECTI (beklenen)"; k0=0
else
    echo "Kol 0 KALDI (BEKLENMEYEN)"; tail -3 "$OUT/kol0.log"; k0=1
fi

echo "== Kol 1: fd dosyalari olmadan derleme"
mv "$M/t1times.fd" "$OUT/t1times.fd.yedek"
mv "$M/T1times.fd" "$OUT/T1times.fd.yedek"
trap 'mv -f "$OUT/t1times.fd.yedek" "$M/t1times.fd" 2>/dev/null; mv -f "$OUT/T1times.fd.yedek" "$M/T1times.fd" 2>/dev/null' EXIT
( cd "$M" && latexmk -pdf -interaction=nonstopmode -outdir="$SUB" main.tex > "$SUB/derle.log" 2>&1 )
mv -f "$OUT/t1times.fd.yedek" "$M/t1times.fd"; mv -f "$OUT/T1times.fd.yedek" "$M/T1times.fd"
trap - EXIT
if [ ! -f "$OUT/main.pdf" ]; then
    echo "Kol 1 derlenemedi (sinama gecersiz)"; tail -5 "$OUT/derle.log"; rm -rf "$OUT"; exit 1
fi
if "${DEX[@]}" scripts/check_pdf_typeset.py "$OUT/main.pdf" "$OUT/main.log" > "$OUT/kol1.log" 2>&1; then
    echo "Kol 1 GECTI (BEKLENMEYEN: kapi hatayi yakalamadi)"; k1=1
else
    echo "Kol 1 KALDI (beklenen): $(grep -m1 SONUC "$OUT/kol1.log" | cut -c1-140)"; k1=0
fi
rm -rf "$OUT"
ls "$M"/*.fd
if [ "$k0" -eq 0 ] && [ "$k1" -eq 0 ]; then echo "SINAMA GECTI"; exit 0; fi
echo "SINAMA KALDI"; exit 1
