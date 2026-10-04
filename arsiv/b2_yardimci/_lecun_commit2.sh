#!/usr/bin/env bash
# LeCun turu ara commit 2: EN metin yeni omurgada, yeni sekiller, gonderim belgeleri, kapi betikleri.
# TR ayna ayri committe (ayna kapisi su an KALIR). Co-Authored-By YOK.
cd /home/firat/projects/adeb_sci_1 || exit 1
git add paper/manuscript/main.tex paper/manuscript/main.pdf paper/manuscript/sections \
        paper/figures/fig_protocol_sets.py paper/figures/fig_yayilim_temiz_fark.py \
        paper/figures/final paper/figures/final_tr paper/figures/arsiv \
        paper/submission/cover_letter.tex paper/submission/cover_letter.pdf paper/submission/declarations.txt \
        paper/submission/highlights.txt paper/submission/pre_submission_checklist.md \
        scripts/acik_depo_kur.sh scripts/check_pdf_render.py scripts/fig_protokol_kumeleri_veri.py \
        scripts/gonderim_tutarlilik.py scripts/verify_manuscript_numbers.py \
        results/q1/fig_protokol_kumeleri_veri.json results/q1_research/LECUN_PLANI_2026-10-04.md \
        results/q1_research/LECUN_TR_AYNA_BRIEF.md arsiv/b2_yardimci/_v1_arsivle.sh arsiv/b2_yardimci/_lecun_commit2.sh
git commit -q -F - <<'MSG'
LeCun turu Faz 3 (EN): metin yeni omurgada, kaynak-hedef ve dis havuz tablolari, yayilim-temiz fark sekli, Sekil 3 ikili uzakliklar

Baslik: "The Conditioning Set Decides the Measured Transfer Asymmetry: An Exact Correction and a
Matched-Pair Prediction for CNN versus Vision Transformer Robustness Comparisons". Ozet 249 kelime,
literatur duzeyi iddia yok; uc ayri olgu (9,21 ozdeslik terimi / 11,10 farkli nicelik / 3,91 onaylanan
ikili [3,12; 4,70]) toplanmadan yazildi. Yon kaynak etkisi (yeni tab:source_target, Mahmood 8x8 dis
sinamasi, kismi uzlasma); eslenmis cift ongorusu (yeni fig:spread_clean_gap, 60 cift; yeni
tab:external_pool: standart hedeflerde p 0,877-1,000, RobustBench havuzu egimi +0,872 [+0,534; +1,274]);
secim kurali (son kontrol noktasi yayilim 12,84 vs 15,01). Yontemde tab:protocol_masks ve genel ozdeslik
denklemi; davranissal olcumler tek alt bolumde (olumsuz sonuclar kalir, manset degil). Karantina
literalleri (Tablo 2 alt blok, Tablo 3 dipnotu, 77,50, ±2 kabul, p=0,88) cikarildi; donanim cumlesi
duzeltildi (C1 5060 Ti, Q1 ve havuz 5090). Kapak mektubu, one cikanlar, beyanlar ve veri bildirimi yeni
omurgada. 24 sayfa, 0 hata; ayna disi sekiz kapi geciyor (TR ayna sonraki committe).
MSG
git log -1 --format='%h %s'
git log -1 --format=%B | grep -c 'Co-Authored' || true
