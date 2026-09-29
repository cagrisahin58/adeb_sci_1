#!/usr/bin/env bash
# Uzun aradan sonra oryantasyon: devir dosyasi, CLAUDE.md degisimi,
# GENISLETILMIS karantina taramasi (08.09.2026: run3, attention_analysis_run3,
# stat_addendum, rev2_blockA da karantinada; gecerli yollar yalniz
# results/c1_* ve results/q1/*).
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1

echo "=== DEVIR / BAGLAM DOSYALARI ==="
ls -t *.md 2>/dev/null | grep -iE 'handoff|baglam|devir|acik_isler|bekleyen' | head -8
ls -t results/q1_research/*.md 2>/dev/null | head -5 | sed 's/^/  /'

echo
echo "=== CLAUDE.md 09-10 DEGISIMI (ozet) ==="
git diff d8dde55..70e32ee --stat | tail -4
git diff d8dde55..70e32ee -- CLAUDE.md | grep -E '^\+' | grep -iE 'karantina|run3|gecerli yol|quarant' | head -6

echo
echo "=== GENISLETILMIS KARANTINA: makale/betik/paket YASAKLI YOLA deginiyor mu? ==="
DESEN='results/run1|results/run2|results/run3|attention_analysis_run3|stat_addendum|rev2_blockA|c_addenda'
echo "-- paper/ (tex, md, txt, bib):"
grep -rnoE "$DESEN" paper/ --include='*.tex' --include='*.md' --include='*.txt' --include='*.bib' 2>/dev/null | head -10 || true
echo "-- kapi betikleri (verify/check/build):"
grep -noE "$DESEN" scripts/verify_manuscript_numbers.py scripts/check_manuscript_claims.py \
    scripts/build_reference_sheet.py scripts/bildiri_tutarlilik.py scripts/gonderim_tutarlilik.py 2>/dev/null | head -10 || true
echo "-- anonim arsiv betigi:"
grep -noE "$DESEN|c1_addenda|c1_c2" scripts/anonim_arsiv.sh 2>/dev/null || true
echo "-- results/ altinda hangi dizinler var:"
ls results/ | tr '\n' ' '; echo

echo
echo "=== MAKALE GERCEKTEN c1_*/q1 DISI ARTEFAKT OKUYOR MU? (verify betigi jl/load cagrilari) ==="
grep -oE '(jl|load|json.load\(open)\("?[^")]*' scripts/verify_manuscript_numbers.py 2>/dev/null \
    | grep -oE 'results/[a-zA-Z0-9_/.-]+' | sort -u | grep -vE '^results/(c1_|q1/|C1_)' || echo "  (c1_/q1 disi yol yok)"
