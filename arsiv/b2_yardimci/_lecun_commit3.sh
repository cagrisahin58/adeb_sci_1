#!/usr/bin/env bash
# LeCun turu commit 3: hakem duzeltmeleri (EN), TR ayna, foy M8 bolumu, yeni atiflar, gonderim belgeleri.
# Co-Authored-By YOK (30.09 karari). Once dokuz kapi gecmis olmali.
cd /home/firat/projects/adeb_sci_1 || exit 1
git add paper/manuscript/main.tex paper/manuscript/main.pdf paper/manuscript/references.bib paper/manuscript/sections \
        paper/manuscript_tr/main.tex paper/manuscript_tr/main.pdf paper/manuscript_tr/sections \
        paper/submission/cover_letter.tex paper/submission/cover_letter.pdf paper/submission/declarations.txt \
        paper/submission/highlights.txt paper/submission/pre_submission_checklist.md \
        scripts/build_reference_sheet.py scripts/verify_manuscript_numbers.py scripts/check_pdf_render.py \
        scripts/check_manuscript_claims.py scripts/acik_depo_kur.sh \
        results/C1_REFERANS_FOYU.md results/q1_research/LECUN_PLANI_2026-10-04.md \
        raporlar/hakem_lecun_2026-10-04/hakem_yontem_yeniden_yazim.md \
        arsiv/b2_yardimci/_bib_havuz_ekle.py arsiv/b2_yardimci/_lecun_commit3.sh
git commit -q -F - <<'MSG'
LeCun turu Faz 3 (hakem gecisi + TR ayna): iddia ozdeslik terimine daraltildi, baslik degisti, foy M8 bolumu, TR esitlendi

Yontem mercekli ikinci hakem gecisi (raporlar/hakem_lecun_2026-10-04/hakem_yontem_yeniden_yazim.md): yeni
tablo ve sekil hucrelerinin hepsi dogru; F3: "buyukluk temiz farki izler" iddiasi yalniz uc-protokol
yayilimi (ozdeslik terimi) icin gecerli, basarili-kaynak fazlasi eslenmis gurbuz ciftlerde 6-13 puan kalir.
Baslik: "The Conditioning Set Decides the Measured Transfer Asymmetry: An Exact Correction and a
Source-Effect Reading for CNN versus Vision Transformer Robustness Comparisons". Ozet, katki 4, IV-D4, V, VI
buna gore; Sekil 3 altyazisi (11,10 + 3,91 = 15,01, kosulsuz kestirim icerde); tab:source_target'a
her-ikisi-dogru, CIFAR-100 basarili-kaynak ve temiz cift satirlari (temiz ViT-Tiny en zayif kaynak, yon
hedef terimiyle); Mahmood CIFAR-100 6/12 isaret donusu; gereklilik 2 p-araligi siniri; son kontrol
noktasi epoklari (ViT 45/38/39, ResNet 71/76/77); SVHN farki 1,84; kucuk maddeler (m1-m14).
Foye "Govde metnindeki diger sayilar (hakem M8)" bolumu (16 madde, ~40 sayi artefakta baglandi).
Yeni atiflar (arXiv dogrulandi): carmon2019unlabeled, wong2020fast, engstrom2019robustness.
TR ayna cumle duzeyinde esitlendi (makale-yazari). EN 25 sayfa; DOKUZ KAPI GECIYOR.
MSG
git log -1 --format='%h %s'
git log -1 --format=%B | grep -c 'Co-Authored' || true
echo '=== teslim paketi'
timeout 500 bash scripts/teslim_paketi.sh 2>&1 | tail -3
