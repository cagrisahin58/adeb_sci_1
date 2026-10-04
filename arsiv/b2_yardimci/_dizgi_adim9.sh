#!/usr/bin/env bash
# 2026-10-04 dizgi adim 9: root sahipli TR sekil dosyalarini konteyner uzerinden arsive tasi, git'e kaydet.
cd /home/firat/projects/adeb_sci_1 || exit 1
DX=(docker exec -w /workspace adeb_eval)
"${DX[@]}" mkdir -p paper/figures/arsiv/final_tr_2026-10-04
for f in fig1_robustness_comparison.pdf fig3_transfer_heatmap.pdf fig4a_gradient_visualization.pdf \
         fig5a_attention_comparison.pdf fig_adversarial_examples.pdf fig_tsne_features.pdf; do
    [ -f "paper/figures/final_tr/$f" ] && "${DX[@]}" mv -f "paper/figures/final_tr/$f" "paper/figures/arsiv/final_tr_2026-10-04/$f" && echo "  arsiv <- final_tr/$f"
done
for f in fig3_transfer_heatmap.pdf fig4a_gradient_visualization.pdf fig5a_attention_comparison.pdf \
         fig_protocol_sets_v1.kanit.json fig_protocol_sets_v1.pdf fig_protocol_sets_v1.png; do
    [ -f "paper/figures/final/$f" ] && "${DX[@]}" mv -f "paper/figures/final/$f" "paper/figures/arsiv/$f" && echo "  arsiv <- final/$f"
done
# sahiplik: konteynerin yazdigi dosyalar root; depo kullanicisina cevir (chown icin konteyner)
"${DX[@]}" chown -R "$(id -u):$(id -g)" paper/figures/final paper/figures/final_tr paper/figures/arsiv paper/figures/overview 2>/dev/null
echo '=== final / final_tr icerigi'
ls paper/figures/final/ | tr '\n' ' '; echo
ls paper/figures/final_tr/ | tr '\n' ' '; echo
git add -A paper/figures
echo '=== git status paper/figures'
git status --short paper/figures | head -40
