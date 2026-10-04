#!/usr/bin/env bash
# 2026-10-04 dizgi adim 10: commit (Co-Authored-By YOK, 30.09 karari) + teslim paketi.
cd /home/firat/projects/adeb_sci_1 || exit 1
git add paper/manuscript/main.tex paper/manuscript/main.pdf paper/manuscript/references.bib \
        paper/manuscript/sections paper/manuscript/t1times.fd paper/manuscript/T1times.fd \
        paper/manuscript_tr/main.pdf paper/manuscript_tr/sections \
        paper/figures/overview/fig_study_overview.tex paper/figures/overview/derle.sh \
        paper/figures/overview/cifar_thumbs.py paper/figures/overview/cifar_thumbs.png \
        paper/figures/overview/cifar_thumbs.kanit.json paper/figures/overview/fig_study_overview.pdf \
        paper/figures/overview/fig_study_overview.png \
        scripts/build_reference_sheet.py scripts/generate_journal_figs_c1.py scripts/kapilar.sh \
        scripts/verify_manuscript_numbers.py scripts/check_pdf_typeset.py scripts/test_pdf_typeset.sh \
        scripts/render_sayfalar.py scripts/pdf2png.py \
        results/C1_REFERANS_FOYU.md results/q1_research/TUR4_EYLEM_PLANI.md \
        arsiv/b2_yardimci/_lecun_metin1.py arsiv/b2_yardimci/_lecun_metin2.py arsiv/b2_yardimci/_lecun_metin3.py \
        arsiv/b2_yardimci/_lecun_metin4.py arsiv/b2_yardimci/_render_duzeltmeleri.py arsiv/b2_yardimci/_sekil_betik_yama.py \
        arsiv/b2_yardimci/_dizgi_adim1.sh arsiv/b2_yardimci/_dizgi_adim2.sh arsiv/b2_yardimci/_dizgi_adim3.sh \
        arsiv/b2_yardimci/_dizgi_adim4.sh arsiv/b2_yardimci/_dizgi_adim5.sh arsiv/b2_yardimci/_dizgi_adim6.sh \
        arsiv/b2_yardimci/_dizgi_adim7.sh arsiv/b2_yardimci/_dizgi_adim8.sh arsiv/b2_yardimci/_dizgi_adim9.sh \
        arsiv/b2_yardimci/_dizgi_adim10.sh arsiv/b2_yardimci/_fi_sil.py arsiv/b2_yardimci/_font_kesif.sh \
        arsiv/b2_yardimci/_sekil_cumle_bul.sh
git add raporlar/hakem_lecun_2026-10-04/*.md
git commit -q -F - <<'MSG'
LeCun paneli (16 ajan) + render temelli sekil/tablo gecisi; dizgi arizasi giderildi, dokuzuncu kapi

Hakem paneli: 10 sonnet toplayici -> 5 opus mercek -> 1 fable hukum (raporlar/hakem_lecun_2026-10-04).
Hukum Major revision: bes engelleyici (baslik/ozet iddiasi, 9,21+5,79 ayrisimi, zayif-hedef okumasi,
veri/kod beyani ve artefakt eksikleri, dizgi + yapay zeka sekli). Metin duzeyi kararlar kullanicida.

Dizgi: ieeeaccess.cls 'times' ailesini tanimlamiyordu; govde Computer Modern'di, kalin/italik hic
basilmiyordu, bes tablo sutunu asiyordu. t1times.fd (+T1times.fd) eklendi; govde TimesLTStd.
Dokuzuncu kapi scripts/check_pdf_typeset.py (Times gomulu, sutun tasmasi, gunluk); sinama
scripts/test_pdf_typeset.sh. EN 24 -> 22 sayfa.

Sekiller: Sekil 1 yapay zeka rasteri yerine vektor TikZ (paper/figures/overview, gercek CIFAR-10
test goruntuleri, iki asamali egitim, yineleme seridi); isi haritasi (Tablo 4 kopyasi) kaldirildi;
Sekil 2/4/5/6/7 son sutun genisliginde 8 pt yaziyla yeniden uretildi (ECDF ornek basina kayip,
uc cift; ortak renk cubuklari; Δentropi + TOST marji ve TV yer degistirmesi); Sekil 3'e satir ve
panel harfleri. TR sekilleri de uretildi; kanit JSON'lari eklendi.

Tablolar: Tablo 2 alt baslik; Tablo 3 besinci sutun dipnota; Tablo 4 ayri kosu beyani; Tablo 6
yerine protokol x ayar table* (CIFAR-10 Linf / CIFAR-100 / SVHN iki cift ayri / CIFAR-10 L2) ve
yanlis Tablo 7 gondermesi duzeltildi; Tablo 8 tekduze ondalik, isaretli hizalanma uc kosum ort±SD;
Tablo 9 Fark±SD, p (Holm); Tablo 10 dikey cizgi kaldirildi, Stage.block, SD cumlesi; Tablo 11
kisaltmalar ve butce. McNemar sinirlari 2x10^-84 / 2x10^-120; 03:7 'her analizin icinde'.

Referans foyu genisletildi (protokol x ayar, turetilmis sayilar, Tablo 8/9/10 ek, entropi, epsilon
taramasi, literal etiketleri); sayi kapisi 158 -> 180. Yazar isareti 1,2; biyografi Turkiye; url
paketi; \vol{14}; kaynakcada ilk ad kumesi. Dokuz kapi geciyor.
MSG
git log -1 --format='%h %s'
git log -1 --format=%B | grep -c 'Co-Authored' || true
echo '=== teslim paketi'
timeout 500 bash scripts/teslim_paketi.sh 2>&1 | tail -4
echo '=== kalan (izlenmeyen, bugune ait)'
git status --short | grep -v -E '^\?\? (logs|models|x$|dates.sh|CLAUDE.md.bak|\.claude|arsiv/b2_yardimci/_(beyan|gonderim|kapilar|kontrol|ozet|paket|sinama))' | head -20
