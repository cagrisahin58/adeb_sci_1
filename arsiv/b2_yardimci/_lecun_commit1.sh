#!/usr/bin/env bash
# LeCun turu ara commit 1: yeni olcumler, masa basi cozumlemeler, foy genisletmesi (metin ve sekiller haric,
# onlar ajanlarda). Co-Authored-By YOK (30.09 karari).
cd /home/firat/projects/adeb_sci_1 || exit 1
git add results/q1/kaynak_hedef_ayristirma.json results/q1/secim_asimetri_etkisi.json \
        results/q1/e3_uc_protokol_svhnli_fit.json results/q1/fig_yayilim_temiz_fark_veri.json \
        results/q1/dis_veri/mahmood2021_tablolar.json results/q1/dis_veri/mahmood2021_ozdeslik.json \
        results/q1/dis_veri/mahmood2021_metin.txt results/c1_c4/c4_entropy_tost.json \
        results/q1/temiz_ciftler results/q1/son_kontrol_noktasi results/q1/havuz_cifar10 \
        results/c1_c3/pair1/havuz_protokoller.json results/c1_c3/pair2/havuz_protokoller.json results/c1_c3/pair3/havuz_protokoller.json \
        results/C1_REFERANS_FOYU.md results/q1_research/LECUN_PLANI_2026-10-04.md results/q1_research/LECUN_YAZIM_BRIEF.md \
        experiments/c1_c3_transfer_matrix.py experiments/q1_havuz_analiz.py experiments/q1_kaynak_hedef_ayristirma.py \
        experiments/q1_mahmood2021_tablolar.py experiments/q1_secim_asimetri_etkisi.py experiments/q1_e3_uc_protokol_svhnli_fit.py \
        experiments/c1_c4_entropy_tost.py \
        scripts/build_reference_sheet.py scripts/fig_yayilim_temiz_fark_veri.py scripts/q1_havuz_analiz_hepsi.sh \
        scripts/q1_havuz_indir.py scripts/q1_son_kontrol_noktasi_run.sh scripts/q1_temiz_ve_havuz_run.sh scripts/dis_veri_mahmood.py \
        arsiv/b2_yardimci/_yapi_kesif.py arsiv/b2_yardimci/_lecun_commit1.sh 2>&1 | grep -v 'warning' | head -5
# buyuk PDF'i (Mahmood makalesi, 1.5 MB) depoya alma
git reset -q results/q1/dis_veri/mahmood2021.pdf 2>/dev/null
git status --short --cached | wc -l
git commit -q -F - <<'MSG'
LeCun turu Faz 1-2: kaynak-hedef ayristirma, Mahmood dis verisi, secim etkisi, temiz ciftlerde p, RobustBench havuzu, foy genisletmesi

Masa basi (deney-takibi): hedef-dogru oranlarda toplamsal kaynak+hedef ayristirmasi (CIFAR-10 kaynak farki
+5,13, hedef farki -2,03; CIFAR-100 +9,54 / -6,19) -> yon kaynak etkisi; Mahmood ve ark. (ICCV 2021)
Tablo 1-2 metinden programla okundu (CIFAR-10'da ViT guclu kaynak 12/12; CIFAR-100 sifirdan ResNet'lerde
CNN->ViT yonu 6/6 ama hedef terimi tasir; BiT/ViT-L ciftinde ozdeslik ongorulu protokol etkisi -0,59);
saklı yorungelerde secim kuralinin asimetriye etkisi; SVHN-dahil uc-protokol egimi +0,4697 [+0,3606;
+0,6649] artefaktli; dikkat entropisi TOST 12/12, en buyuk p 0,00611.

Yeni olcumler (GPU, egitim yok): temiz egitilmis C1 ciftleri + RobustBench Standard WRN (p standart
hedeflerde 0,877-0,996, p=1 artigi en cok 1,58; 0,3 puan temiz farkli ciftte yayilim 0,2); son kontrol
noktasi (last.pth) ciftleri (yayilim 12,84 vs 15,01); sekiz modellik RobustBench havuzu (28 cift, p
0,933-1,000; uc-protokol yayilim-temiz fark egimi +0,872 [+0,534; +1,274]). c1_c3_transfer_matrix.py'ye
--rb-model eklendi; experiments/q1_havuz_analiz.py; scripts/fig_yayilim_temiz_fark_veri.py (60 cift,
ozdeslik paritesi r 0,9996).

Referans foyu sekiz yeni bolum (kod-mimar). Metin ve sekiller ayri committe.
MSG
git log -1 --format='%h %s'
git log -1 --format=%B | grep -c 'Co-Authored' || true
