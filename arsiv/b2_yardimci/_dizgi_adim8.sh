#!/usr/bin/env bash
# 2026-10-04 dizgi adim 8: kullanilmayan sekil dosyalari arsive, EN+TR derleme, dokuz kapi.
cd /home/firat/projects/adeb_sci_1 || exit 1
mkdir -p paper/figures/arsiv/final_tr_2026-10-04
mv_or_gitmv () {  # $1 kaynak, $2 hedef
    if git ls-files --error-unmatch "$1" > /dev/null 2>&1; then git mv -f "$1" "$2"; else mv -f "$1" "$2"; fi
    echo "  arsiv <- $1"
}
echo '=== kullanilmayan sekil dosyalari'
for f in fig3_transfer_heatmap.pdf fig4a_gradient_visualization.pdf fig5a_attention_comparison.pdf \
         fig_protocol_sets_v1.kanit.json fig_protocol_sets_v1.pdf fig_protocol_sets_v1.png; do
    [ -f "paper/figures/final/$f" ] && mv_or_gitmv "paper/figures/final/$f" "paper/figures/arsiv/$f"
done
for f in fig1_robustness_comparison.pdf fig3_transfer_heatmap.pdf fig4a_gradient_visualization.pdf \
         fig5a_attention_comparison.pdf fig_adversarial_examples.pdf fig_tsne_features.pdf; do
    [ -f "paper/figures/final_tr/$f" ] && mv_or_gitmv "paper/figures/final_tr/$f" "paper/figures/arsiv/final_tr_2026-10-04/$f"
done
echo '=== EN derle'
bash scripts/derle_en.sh
echo '=== TR derle'
( cd paper/manuscript_tr && latexmk -pdf -interaction=nonstopmode main.tex > /tmp/derle_tr.log 2>&1; grep -o 'Output written on.*' main.log | tail -1; echo "hata=$(grep -c '^!' main.log) tanimsiz=$(grep -ci 'undefined' main.log)" )
echo '=== kapilar'
timeout 580 bash scripts/kapilar.sh 2>&1 | tail -3
echo '=== TR sekil fontlari (Type3?)'
docker exec -w /workspace adeb_eval python -c "import fitz,glob; [print(p.split('/')[-1], sorted({f[3] for f in fitz.open(p)[0].get_fonts()})) for p in sorted(glob.glob('paper/figures/final_tr/*.pdf'))]"
echo '=== git status (ozet)'
git status --short | grep -v -E '^\?\? (logs|models|x$|dates.sh|CLAUDE.md.bak|\.claude|arsiv/b2_yardimci/_(beyan|gonderim|kapilar|kontrol|ozet|paket|sinama))' | wc -l
