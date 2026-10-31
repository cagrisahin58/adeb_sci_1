Doğrulama: 31.10.2026, doğrulayıcı kararı KABUL (437 sayı doğrulandı, 0 yanlış), 7 bulgu işlendi.

# B2-B6 ön kayıtlı sonuç raporu (31.10.2026)

Bu rapor deney sonuç analisti (opus alt ajan) tarafından hazırlanmış olup dondurulmuş ön kaydın (`raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md`, bundan sonra ÖK) B2, B4, B5 ve B6 bloklarını ÖK §5 ile §6'daki karar kurallarına göre okur ve B3 eğitim defterini ÖK §4 denetimlerinden geçirir. Bu raporda hiçbir çözümleme betiği yeniden koşulmamış, dondurulmuş `experiments/q1_konsey_ayrisim.py` betiğinin zincir sırasında ürettiği JSON çıktıları okunmuştur. Ham matristen yapılan tek yeniden hesap B6 köşegeninin ve 46,40 çakışmasının denetimidir; bunun için yazılan salt okur yardımcılar `arsiv/b2_yardimci/_rapor_kosegen.py` (konteynerde, numpy ile), `_rapor_gunluk.py`, `_rapor_turetilmis.py` ve `_rapor_govde_ozet.py` dosyalarıdır. Ön kayıt dışındaki her yorum yalnız §8'de, "keşifsel" başlığı altında verilmiştir.

Metinde kaynaklar aşağıdaki kısaltmalarla anılır; tam yollar sondaki sayı kaynak dizinindedir.

| Kısaltma | Dosya |
|---|---|
| J2 | `results/q1/konsey_ayrisim_b2.json` |
| J4 | `results/q1/konsey_ayrisim_b4.json` |
| J5 | `results/q1/konsey_ayrisim_b5.json` |
| M6 | `results/q1/konsey_b6_maskeleme.json` |
| AA | `results/q1/konsey_b6_aa/autoattack_results.csv` |
| DF | `results/q1/konsey_b3_defter.tsv` (satır numarası başlık satırı 1 sayılarak) |
| ZL | `logs/konsey_zincir.log` |
| ZD | `results/q1/konsey_zincir_durum.tsv` |
| GL | `logs/konsey_b3/<takma ad>_AT.log` ve `_temiz.log` |
| NV | `logs/konsey_b3/nvidia_smi_df.log` |
| KS | `results/q1/konsey_b4_matris/per_sample_<m>_to_<m>.npz` üzerinde `_rapor_kosegen.py` çıktısı |
| TR | J2, J4 ya da J5 anahtarlarından aritmetik türetme (`_rapor_turetilmis.py`), formül dizinde |
| ÖK | `raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md` |
| FÖY | `results/C1_REFERANS_FOYU.md` |

## 0. Bütünlük denetimi ve sınama eşlemesi

Dondurulmuş çözümleme betiğinin bugünkü SHA-256 özeti `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`, hücre tablosununki `2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500`'dür ve ikisi de ÖK Dondurma eki (a) ile üç JSON'un `meta.betik_sha256` ve `meta.hucre_tablosu_sha256` alanlarıyla aynıdır. ÖK gövdesinin Dondurma eki (b) tanımıyla yeniden hesaplanan özeti `46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5`'tir ve ekteki değerle aynıdır (`_rapor_govde_ozet.py`). ÖK §7'nin adını verdiği `results/q1_research/ONKAYIT_SAPMALAR.md` dosyasında yalnız ek ön kayda (B8-B10) ait kayıtlar bulunmakta, ana ön kayda ait sapma kaydı bulunmamaktadır. Böylece ÖK §7'deki ölçütle B2, B4 ve B5 çözümlemeleri ön kayıtlı çözümleme sayılır. Birincil panelin yedi üyesi de yüklenmiş (`panel.birincil_eksik` boş), birleştirilen matris klasörlerinde hücre çakışması çıkmamış (`veri.cakismalar` boş) ve hedef maskeleri bütün hedeflerde tutarlıdır (J2 ve J4'te `veri.tutarlilik.hedef_maskesi_tutarli` = true; J5'te aynı alan `veri.pgd`, `veri.mi` ve `veri.tgr` altında).

Rapor yazılmadan önce JSON anahtarları listelenmiş ve ÖK'deki sınama adlarıyla eşlenmiştir. Bulunamayan iki çıktı açıkça işaretlenmiştir.

| ÖK sınaması ya da çözümlemesi | ÖK yeri | JSON anahtarı | Durum |
|---|---|---|---|
| K-a, simetrik oran | §5 B2 | J2 `b2.F_B2.K-a`, `b2.F_B2.p_ham[0]`, `p_holm[0]`, `karar.K-a` | bulundu |
| K-b, ViT yönlü terimi | §5 B2 | J2 `b2.F_B2.K-b`, `p_ham[1]`, `p_holm[1]`, `karar.K-b` | bulundu |
| K-c, tür içi benzerlik | §5 B2 | J2 `b2.F_B2.K-c`, `p_ham[2]`, `p_holm[2]`, `karar.K-c` | bulundu |
| F_B2, δ = 0,06 duyarlılığı | §5 | J2 `b2.F_B2.duyarlilik_delta_0.06` | bulundu |
| B2 tam örneklem, logit, oran, jackknife, ikincil panel | §5 Duyarlılıklar | J2 `b2.duyarlilik.{tam_log, yari_logit, yari_oran, panel_jackknife, ikincil_panel}` | bulundu |
| B2'de K-a ve K-b için hiyerarşik bootstrap duyarlılığı | §5 Duyarlılıklar | yok | bu sınamanın çıktısı JSON'da bulunamadı |
| B2'de Welch aralığı | §5 Duyarlılıklar | yok | K-a ve K-b tek örneklem t olduğundan uygulanmaz; JSON'da da yoktur |
| H1, H2, H3 | §5 B4 | J4 `b4.F_B4.karsitliklar.H1/H2/H3`, `b4.F_B4.p_ham`, `p_holm`, `karar` | bulundu |
| Sonuç bölgesi ve O4 | §6 | J4 `b4.F_B4.karar.sonuc_bolgesi`, `O4_niteleme` | bulundu |
| B4 duyarlılıkları | §5 Duyarlılıklar | J4 `b4.duyarlilik.{delta_0.06, tam_log, yari_logit, yari_oran, welch, panel_jackknife, hiyerarsik_bootstrap}` | bulundu |
| S1-S7 | §5 İkincil | J4 `b4.ikincil.S1` ... `S7` | bulundu |
| B5 korunma oranı | §5 B5 | J5 `b5.birincil_C1-R32_V-scr` | bulundu |
| B5 tam örneklem seçim duyarlılığı ve yeni çiftler | §5 B5 | J5 `...duyarlilik_tam_orneklem_secim`, `b5.betimsel` | bulundu |
| B6 maskeleme kuralı | §5 B6 | M6 `modeller.*`, `isaretli`; J4 `b4.F_B4.maskeleme_kurali` | bulundu |
| B6 sonrası işaretlilerle H1-H3 yeniden hesabı | §5 B6 | gerekmedi (`isaretli` boş) | uygulanmadı, kural tetiklenmedi |

## 1. Yönetici özeti

Ön kaydın §6'daki sıralı sonuç haritası (O2, O5, O1, O3, O3 varyantı, O5a) uygulandığında sonuç O1 bölgesine düşmektedir (J4 `b4.F_B4.karar.sonuc_bolgesi` = "O1"); B6'da maskeleme şüphesiyle işaretlenen model çıkmadığından bölge değişmemiş (J4 `b4.F_B4.maskeleme_kurali.uygulanan_bolge` = "O1"), O4 ek nitelemesi de tetiklenmemiştir (`b4.F_B4.karar.O4_niteleme` = false). Geçerli önceden yazılmış manşet bu nedenle O1 manşetidir: "ViT'nin CNN'lere karşı zayıf kaynak görünümü simetrik ve mimariye ait bir benzemezliktir; ImageNet başlatması bu benzemezliği ViT'de ResNet'tekinden fazla azaltır; asimetri hedef kırılganlığı ve küçük, mimariden bağımsız bir yönlü terimle taşınır" (ÖK §6). Kararı taşıyan en önemli dört sayı şunlardır. Girdi hattı eşitlenmiş sıfırdan eğitimde mimarinin panel benzerliğine etkisi A^σ_scr = −0,364'tür (%90 aralık −0,415 ile −0,314; Holm sonrası p = 4,09e-05; J4 `b4.F_B4.karsitliklar.H1.kestirim`, `.ci90`, `b4.F_B4.p_holm[0]`). Başlatma ile mimarinin etkileşimi I^σ = +0,260'tır (%90 aralık 0,186 ile 0,335; Holm sonrası p = 9,00e-04; logit ölçekte de pozitif, 0,354; J4 `...H2.kestirim`, `...H2.ci90`, `b4.F_B4.p_holm[1]`, `b4.F_B4.karar.H2_logit_kestirim`). B2'de C1 ResNet-18 ile C1 ViT-Tiny arasındaki panel kaynak açığının simetrik oranı üç tohum ortalamasında 0,936'dır (%90 aralık 0,925 ile 0,948; J2 `b2.F_B2.K-a.sinama.ort`, `.ci90`). Yönlü terimin mimari ana etkisi A^ρ = 0,003 ile ±0,10 sınırında eşdeğer bulunmuştur (%90 aralık −0,020 ile 0,026; Holm sonrası TOST p = 3,79e-04; J4 `...H3.kestirim`, `...H3.ci90`, `b4.F_B4.p_holm[2]`). B2 ailesinin üç sınaması (K-a, K-b, K-c) da destek almış; K-a, K-c, H1 ve H2'nin ayrı satırda raporlanan öngörülen büyüklükleri de tutmuştur.

Saldırı tarafında (B5) ResNet ile ViT arasındaki panel kaynak açığı her kaynağın en iyi saldırısı altında da korunmaktadır: korunma oranı 0,960'tır ve %90 aralığının alt sınırı (0,941) ön kayıtlı 0,5 eşiğinin çok üzerindedir (J5 `b5.birincil_C1-R32_V-scr.oran`, `.bootstrap.ci90`). ViT'ye özgü TGR saldırısı hiçbir ViT kaynağında en iyi saldırı olarak seçilmemiş, CNN paneline PGD-10'dan daha zayıf transfer etmiştir. AutoAttack denetiminde (B6) altı yeni modelin PGD-10 ile AutoAttack farkı 3,2 ile 7,4 puan arasında kalmış, 10 puanlık maskeleme eşiğini hiçbiri aşmamıştır (M6 `modeller.*.fark_puan`). B3'te hiçbir koşu dışlanmamış, AT çöküş kuralı tetiklenmemiş, 80 epokluk tavana çarpan olmamış, toplam eğitim 17,79 saat sürmüştür (ZL satır 77). Kararı değiştirmeyen ama manşetin yazımını sınırlayan dört nokta vardır: ViT'nin yönlü terimi logit ölçekte işaret değiştirmekte (B2'de ρ(V-scr) log ölçekte +0,012, logit ölçekte −0,304; J2 `b2.F_B2.K-b.ort`, `b2.duyarlilik.yari_logit.rho_V.ort`), H3'ün ön kayıt kuralı logit ölçekte uygulansaydı sonuç kararsız çıkmaktadır (§4; J4 `b4.duyarlilik.yari_logit.H3`); ImageNet başlatmalı ViT'nin yönlü terimi (hücre ortalaması −0,118) δ = 0,10 sınırının dışındadır (J4 `...H3.hucre_ort.V-IN`); sıfırdan eğitilmiş ViT'nin temiz test doğruluğu (yüzde 73,0-74,1) öteki üç hücrenin (yüzde 83,4-86,4) çok altındadır (KS); IN hücrelerinde ve R224-scr'de hücre başına yalnız iki koşu vardır.

## 2. B3 eğitim defteri ve ÖK §4 denetimleri

Altı yeni koşunun eğitim özeti aşağıdadır. Temiz aşama ilk epok doğruluğu ve referansı DF'nin `denetim_temiz` satırlarından ve GL temiz günlüklerinin `Epoch 1/...` satırlarından, AT değerleri DF'nin `at_ozet` satırlarından (ZL'deki `OZET` satırlarıyla aynı), 5. epok doğrulama PGD doğruluğu DF'nin AT satırlarındaki "cokus denetimi" notundan ve GL AT günlüklerinin `Epoch 5/100` satırlarından alınmıştır.

| Takma ad | Hücre | Temiz epok | Temiz ilk epok doğrulama (referans; fark) | AT koşulan epok | Seçilen epok | Doğrulama PGD (seçilen) | Erken durma | 5. AT epoğu doğrulama PGD | Kırpılmış olabilir |
|---|---|---|---|---|---|---|---|---|---|
| V_IN_s2101 | V-IN | 30 (DF 2) | 93,95 (25,22; +68,73) (DF 3) | 38 | 18 | 45,15 | evet | 34,90 (DF 4) | hayır (DF 5) |
| R224_IN_s1301 | R224-IN | 30 (DF 6) | 87,25 (38,85; +48,40) (DF 9) | 36 | 16 | 46,40 | evet | 41,90 (DF 10) | hayır (DF 11) |
| R224_scr_s1201 | R224-scr | 200 (DF 8) | 38,85 (referans koşusu; GL satır 11) | 42 | 22 | 46,40 | evet | 40,10 (GL satır 7303; kural IN dışı) | hayır (DF 13) |
| V_IN_s2102 | V-IN | 30 (DF 14) | 94,60 (25,22; +69,38) (DF 15) | 47 | 27 | 42,90 | evet | 33,35 (DF 16) | hayır (DF 17) |
| R224_IN_s1302 | R224-IN | 30 (DF 18) | 87,85 (38,85; +49,00) (DF 19) | 37 | 17 | 46,95 | evet | 42,55 (DF 20) | hayır (DF 21) |
| R224_scr_s1202 | R224-scr | 200 (DF 22) | 36,65 (GL satır 11) | 58 | 38 | 45,85 | evet | 40,75 (GL satır 7536; kural IN dışı) | hayır (DF 24) |

Temiz aşama denetimi dört IN koşusunun dördünde de geçmiştir. ViT-Tiny referansı C1 temiz koşularının ilk epok ortalaması 25,22'dir (üç değer 23,75; 26,55; 25,35; `logs/C1_clean_vit_2001.log`, `_2002.log`, `_2003.log` satır 9) ve IN koşularının farkı +68,73 ile +69,38 arasındadır. ResNet-18 224 referansı denetim anında ilk epoğu tamamlanmış tek R224-scr koşusu olan R224_scr_s1201'in ilk epoğudur (38,85; n = 1); R224_IN_s1301'in denetimi ÖK §4'teki kurala uygun biçimde önce ertelenmiş (DF 7; ZL satır 49), R224-scr temiz aşaması bittikten sonra geçmiştir (DF 9; ZL satır 53). R224_IN_s1302 denetlendiğinde R224_scr_s1202'nin temiz aşaması henüz başlamadığından referans yine n = 1 ile kurulmuştur (DF 19); bu durum ÖK §4'ün "denetim anında en az bir epoğu tamamlanmış" ifadesiyle uyumludur. Temiz aşamanın son epok doğrulukları ÖK §4 gereği yalnız betimseldir: V-IN 97,25 ve 97,45, R224-IN 96,05 ve 96,15 (DF 3, 15, 9, 19, `betimsel best_val`), R224-scr 94,65 ve 94,70'tir (GL `R224_scr_s1201_temiz.log` satır 105244, `R224_scr_s1202_temiz.log` satır 100925).

AT çöküş kuralı tetiklenmemiştir. Dört IN koşusunun 5. epok doğrulama PGD doğruluğu 33,35 ile 42,55 arasındadır ve %15 eşiğinin üzerindedir (DF 4, 10, 16, 20; `logs/konsey_b3/*_cokus.txt` dosyalarının dördü de "TAMAM" yazar). Bütün AT'ler lr 1e-3 ile koşmuştur (ZD `B3_kuyruk` satırı, not "lr 0.001"; DF AT satırları). Kırpılma işareti hiçbir koşuda konmamıştır: en büyük seçilen epok 38'dir ve tavan eksi 5'in (75) çok altındadır. AT tavanı 80'e çarpan koşu yoktur; en uzun koşu 58 epoktur ve altı koşuda da `tavanda_durdu=False` yazılıdır (DF 5, 11, 13, 17, 21, 24; ZL satır 46, 56, 59, 65, 71, 76). ÖK §4'teki dışlama kuralına göre hiçbir koşu dışlanmamış, çökme ya da NaN nedeniyle yeniden başlatma olmamış (bütün eğitim satırlarında, yani temiz ve AT satırlarında durum "OK", not "bastan"; DF 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 23), hiçbir hücre iki koşunun altına düşmemiştir. 2x2 bu nedenle ÖK §3'teki tasarımın tamamıyla (3, 2, 2, 2 koşu) çözümlenmiştir (J4 `b4.F_B4.karsitliklar.H2.hucre_n`).

Bütçe tarafında B3 kuyruğu toplam 17,79 saatte bitmiştir (ZL satır 77); bu değer ÖK Dondurma eki (d)'deki pilotun W(80) = 20,47 saatinin ve 38,15 saatlik eğitim payının altındadır. AT epok süreleri DF'deki süre ve epoktan türetildiğinde V_IN_s2101'de 148,1, R224_IN_s1301'de 195,8, R224_scr_s1201'de 312,5, V_IN_s2102'de 266,6, R224_IN_s1302'de 182,9 ve R224_scr_s1202'de 149,7 saniyedir (DF 4, 10, 12, 16, 20, 23; TR). Pilotun ölçtüğü değerler V_IN AT için 125,8 s, R224_IN AT için 142,7 s ve R224_scr AT için 142,5 s olduğundan (ÖK Dondurma eki (d)) aynı sırayla koşular pilotun 1,18, 1,37, 2,19, 2,12, 1,28 ve 1,05 katı sürmüştür (TR). Aşama başı `nvidia-smi` anlık görüntülerinin üçünde 10882-11045 MiB bellek ve %89-100 kullanım görülmüştür: R224_IN_s1301 AT'sinin başında 11045 MiB ve %100 (NV satır 103; DF 10), R224_IN_s1302 temiz aşamasının başında 10886 MiB ve %100, AT aşamasının başında 10882 MiB ve %89 (NV satır 195, 218; DF 18, 20). Ancak en yavaş iki AT aşamasının, yani R224_scr_s1201 (pilotun 2,19 katı) ile V_IN_s2102'nin (2,12 katı) başında paylaşım görünmemektedir (3953 MiB ve %0, 3964 MiB ve %0; NV satır 126, 172; DF 12, 16). Dolu görünen üç anlık görüntü de B3 kuyruğunun bir önceki aşaması bittikten 1-2 s sonra alınmıştır (DF 8, 16, 18 bitiş saatleri 04:51:10, 14:03:24, 14:22:02; NV satır 94, 186, 209 saatleri 04:51:12, 14:03:25, 14:22:03). Süreç listesi ilk görüntüde boş (NV satır 112), öteki ikisinde yalnız PID 1 olarak görünen bir `/python3.12` sürecidir (NV satır 204, 227); bu sürecin konteynerin kendi eğitim süreci olması dışlanamaz. Yavaşlamanın nedeni bu kayıtlardan belirlenemez. ÖK §3'e göre paylaşım yalnız süreyi uzatır ve tavan değişmemiştir; ÖK §4'e göre yalnız bütçe aşımı sapma sayılır, aşım olmadığından bu durum sapma değildir ama epok sürelerinin pilotun üzerine çıktığı makalenin hesaplama ayrıntılarında beyan edilmelidir (§7).

## 3. B2 sınamaları (aile F_B2, Holm α = 0,05)

| Sınama | Ön kayıtlı öngörü ve ölçüt | Gözlenen | Aralık | Ham p | Holm p | Karar | Öngörülen büyüklük |
|---|---|---|---|---|---|---|---|
| K-a | q_s ≥ 0,75; H0: ort q ≤ 0,50, tek yönlü t (df 2); çürütme: %90 üst sınır < 0,50 | ort q = 0,936 (q_s: 0,940; 0,928; 0,940) | %90 [0,925; 0,948], %95 [0,919; 0,953] | 4,19e-05 | 1,26e-04 | destek | tuttu (her tohumda q_s ≥ 0,75) |
| K-b | \|ρ(V-scr)\| < 0,10; TOST ±0,10; çürütme: %95 aralık sıfırı dışlar ve \|kestirim\| > 0,10 | ort ρ = 0,012 (0,025; 0,007; 0,004) | %90 [−0,007; 0,031], %95 [−0,016; 0,040] | TOST 2,73e-03 | 2,73e-03 | destek (Holm sonrası TOST p < 0,05) | ham %90 aralık ±0,10 içinde |
| K-c | Δ_w ≥ +0,30; H0: Δ_w ≤ 0, hiyerarşik bootstrap; çürütme (önce): %90 üst sınır < +0,10 | Δ_w = 0,566 | bootstrap %90 [0,537; 0,604], %95 [0,533; 0,608] | 5,00e-04 | 1,00e-03 | destek | tuttu (Δ_w ≥ 0,30) |

Tablodaki değerler J2'nin şu anahtarlarından alınmıştır: K-a satırı `b2.F_B2.K-a.q`, `.sinama.ort`, `.sinama.ci90`, `.sinama.ci95` ve `.p_tek_H0_q_le_0.5` alanlarından, K-b satırı `b2.F_B2.K-b.degerler`, `.ort`, `.ci90`, `.ci95` ve `.tost_p` alanlarından, K-c satırı ise `b2.F_B2.K-c.Delta_w`, `.bootstrap.ci90`, `.bootstrap.ci95` ve `.p_tek_H0_Delta_le_0` alanlarından gelir. Holm değerleri `b2.F_B2.p_holm`, kararlar da `b2.F_B2.karar` alanında bulunmaktadır.

K-a'nın payda kuralı tetiklenmemiştir: üç tohumda D_s 0,391; 0,387 ve 0,390'dır, yani 0,10'un üzerindedir (J2 `b2.F_B2.K-a.D`; `payda_kucuk_tohumlar` boş). Açığın simetrik payı 0,368; 0,360 ve 0,367, yönlü payı 0,023; 0,028 ve 0,023'tür (`b2.F_B2.K-a.simetrik_pay`, `.yonlu_pay`); ayrışım özdeşliğinin en büyük sayısal artığı 4,3e-16'dır (`.ozdeslik_artik_max`). K-b'nin çürütme koşulu tutmamıştır, çünkü %95 aralık sıfırı içerir. K-c'de çürütme koşulu önce denetlenmiş ve tutmamıştır (%90 üst sınır 0,604 > 0,10); bootstrap 2000 kopyada 284 tek tohumlu örneği yeniden çekmiştir (`b2.F_B2.K-c.bootstrap.yeniden_cekilen_tek_tohumlu_ornek`). ViT tohum çiftlerinin tür içi log τ̄ değerleri −0,453, −0,466 ve −0,410, ViT tohumlarının panel benzerliği σ ise −1,015, −1,000 ve −1,011'dir (`b2.F_B2.K-c.log_tau_tur_ici`, `.sigma_V`).

Duyarlılıklar ÖK §5 gereği kararı değiştirmez ve aşağıda raporlanmıştır. δ = 0,06 ile bütün kararlar aynı kalmış, K-b'nin Holm sonrası TOST p değeri 8,98e-03 olmuştur (J2 `b2.F_B2.duyarlilik_delta_0.06.p_holm[1]`, `.karar`). Tam örneklemde ort q 0,937, ort ρ(V-scr) 0,012'dir (`b2.duyarlilik.tam_log.q_ort`, `.rho_V.ort`). Logit ölçekte ort q 1,101'e çıkmakta, ρ(V-scr) −0,304'e dönmektedir (%90 [−0,320; −0,289]; `b2.duyarlilik.yari_logit.q_ort`, `.rho_V.ort`, `.rho_V.ci90`); oran ölçeğinde ort q 1,542, ρ(V-scr) −14,66 puandır (`b2.duyarlilik.yari_oran.q_ort`, `.rho_V.ort`). Logit ölçekte q'nun 1'i aşması, yönlü payın orada açığı küçültecek yönde olduğunu, açığın tamamının simetrik paydan geldiğini gösterir; log ölçekteki "küçük pozitif yönlü pay" okuması bu yüzden ölçeğe bağlıdır. Panel üyesi bırakmalı jackknife'ta ort q 0,931 (Sehwag2021Proxy_R18 çıkınca) ile 0,941 (Carmon2019Unlabeled çıkınca), ort ρ(V-scr) 0,001 (Engstrom2019Robustness çıkınca) ile 0,022 (Gowal2020Uncovering_28_10_extra çıkınca) arasındadır (`b2.duyarlilik.panel_jackknife.*`). Tek üyeli ikincil panelde (Debenedetti2022Light_XCiT-S12) q 0,899; 0,825 ve 0,842, ρ(V-scr) 0,198; 0,202 ve 0,204'tür (`b2.duyarlilik.ikincil_panel.q`, `.rho_V`). K-a ve K-b için ÖK §5'te sayılan hiyerarşik bootstrap duyarlılığının çıktısı JSON'da bulunamamıştır; dondurulmuş betik bu duyarlılığı B2'de yalnız K-c'nin birincil aralığı olarak üretmektedir (§7).

## 4. B4 sınamaları (2x2; aile F_B4, Holm α = 0,05, birleşik varyanslı t, df 5)

Hücre düzeyi model nicelikleri (bölünmüş yarı, log ölçek) aşağıdadır. Hücre ortalamaları J4 `b4.F_B4.karsitliklar.H2.hucre_ort` (σ), `...H3.hucre_ort` (ρ) ve `b4.ikincil.S3.etkilesim.hucre_ort` (ω) anahtarlarından, koşu değerleri `b4.F_B4.degerler.{sigma, rho, omega}` anahtarlarından alınmıştır.

| Hücre | n | σ ortalama (koşular) | ρ ortalama (koşular) | ω ortalama | w = exp(ω), koşular (yüzde) |
|---|---|---|---|---|---|
| V-scr | 3 | −1,009 (−1,015; −1,000; −1,011) | 0,012 (0,025; 0,007; 0,004) | 4,019 | 55,91; 55,86; 55,12 |
| V-IN | 2 | −0,739 (−0,702; −0,776) | −0,118 (−0,131; −0,105) | 3,905 | 48,24; 51,11 |
| R224-scr | 2 | −0,645 (−0,625; −0,664) | −0,058 (−0,038; −0,079) | 3,890 | 49,33; 48,47 |
| R224-IN | 2 | −0,635 (−0,642; −0,628) | −0,054 (−0,056; −0,052) | 3,872 | 48,34; 47,73 |

| Sınama | Ön kayıtlı öngörü ve sıra | Kestirim | %90 aralık | %95 aralık | t (df 5) | Ham p | Holm p | Karar |
|---|---|---|---|---|---|---|---|---|
| H1, A^σ_scr = σ(V-scr) − σ(R224-scr) | ≤ −0,20; H0: A ≥ 0 tek yönlü; (i) %90 ±0,10 içinde ise çürütüldü, (ii) Holm p < 0,05 ise destek, (iii) pozitif ve %95 sıfırı dışlarsa çürütüldü | −0,364 | [−0,415; −0,314] | [−0,428; −0,300] | −14,60 | 1,36e-05 | 4,09e-05 | destek; öngörülen büyüklük (≤ −0,20) tuttu |
| H2, I^σ | ≥ +0,10; iki yönlü; (i) %90 ±0,10 içinde ise çürütüldü, (ii) Holm p < 0,05, kestirim ve logit I^σ pozitifse destek | +0,260 | [0,186; 0,335] | [0,165; 0,355] | 7,03 | 9,00e-04 | 9,00e-04 | destek; logit I^σ = 0,354; öngörülen büyüklük (≥ +0,10) tuttu |
| H3, A^ρ | eşdeğer; TOST ±0,10; çürütme: %95 sıfırı dışlar ve \|kestirim\| > 0,10 | 0,003 | [−0,020; 0,026] | [−0,026; 0,033] | 0,29 | TOST 1,89e-04 | 3,79e-04 | destek (eşdeğer); ham %90 aralık ±0,10 içinde |

Tablodaki değerler J4'ün `b4.F_B4.karsitliklar.H{1,2,3}` altındaki `kestirim`, `ci90`, `ci95`, `t`, `p_tek_kucuk`, `p_iki` ve `tost_p` alanlarından, ham ve Holm sonrası p değerleri `b4.F_B4.p_ham` ile `b4.F_B4.p_holm` alanlarından, kararlar da `b4.F_B4.karar` alanından alınmıştır. Hiçbir aile sınaması hesaplanamaz duruma düşmemiştir (`b4.F_B4.p_1_sayilan_hesaplanamayan` boş). Kural sırası işletildiğinde H1'in (i) koşulu tutmamıştır, çünkü %90 aralık tümüyle −0,10'un altındadır; (ii) koşulu tutmuştur. H2'nin (i) koşulu tutmamış, (ii) koşulu üç bileşeniyle tutmuştur; ters yön anlamlılığı yoktur (`b4.F_B4.karar.H2_negatif_anlamli_holm` = false). H3'ün çürütme koşulu %95 aralık sıfırı içerdiğinden tutmamıştır. Bileşim (H1 destek, H2 destek, H3 eşdeğer) §6 sırasında O2 ve O5'e uymamakta, O1'e uymaktadır.

Ön kayıtlı kesinlik planıyla karşılaştırma için gözlenen %90 yarı genişlikler H1'de 0,050, H2'de 0,075, H3'te 0,023'tür (TR). Plan log τ̄ için 2x2 karşıtlıkta 0,044 yarı genişlik ve etkileşimde √(1/3 + 3/2) ≈ 1,354 çarpanı öngörmüş, model düzeyi SD'nin ölçülmediğini ve çift düzeyi vekilin yalnız büyüklük sırası verdiğini yazmıştı (ÖK §5). Gözlenen genişlikler bu büyüklük sırasındadır; birleşik varyansa en büyük katkı V-IN'in iki tohumu arasındaki 0,074'lük σ farkından gelir (TR; birleşik SD 0,0273, `b4.F_B4.karsitliklar.H1.sp_birlesik`).

B4 duyarlılıkları kararı değiştirmemiştir:

| Duyarlılık | H1 | H2 | H3 | Anahtar |
|---|---|---|---|---|
| δ = 0,06 | destek (Holm p 4,09e-05) | destek (Holm p 1,80e-03) | destek, eşdeğer (Holm TOST p 2,13e-03); bölge O1 | J4 `b4.duyarlilik.delta_0.06` |
| Tam örneklem | −0,364 [−0,414; −0,314] | 0,260 [0,186; 0,334] | 0,004 [−0,020; 0,027] | `b4.duyarlilik.tam_log.H*` |
| Logit ölçek | −0,498 [−0,570; −0,426] | 0,354 [0,247; 0,461] | −0,087 [−0,110; −0,064] | `b4.duyarlilik.yari_logit.H*` |
| Oran ölçeği (puan) | −8,50 [−9,85; −7,14] | 5,85 [3,83; 7,86] | −4,13 [−4,90; −3,37] | `b4.duyarlilik.yari_oran.H*` |
| Welch, %95 (df) | [−0,569; −0,160] (1,10) | [0,029; 0,491] (1,63) | [−0,052; 0,059] (1,95) | `b4.duyarlilik.welch.H*` |
| Panel jackknife, aralık | −0,376 ile −0,346 | 0,249 ile 0,266 | 0,001 ile 0,006 | `b4.duyarlilik.panel_jackknife.*` |
| Hiyerarşik bootstrap, %90 | [−0,393; −0,335] | [0,204; 0,316] | [−0,024; 0,031] | `b4.duyarlilik.hiyerarsik_bootstrap.H*.ci90` |

Parantez içindeki aralıklar, aksi yazılmadıkça %90 aralıklardır. Jackknife'ta H1'in en uç değerleri Sehwag2021Proxy_R18 (−0,376) ve Engstrom2019Robustness (−0,346), H2'ninkiler Engstrom2019Robustness (0,249) ve Wong2020Fast (0,266), H3'ünkiler Wong2020Fast (0,001) ve Sehwag2021Proxy_R18 (0,006) çıkarıldığında elde edilir. Duyarlılıklar arasında dikkat isteyen satırlar logit ve oran ölçekleridir, çünkü H3'ün eşdeğerliği log ölçeğe bağlıdır. Logit ölçekte H3'ün kestirimi −0,087, %95 aralığı [−0,116; −0,058]'dir ve sıfırı dışlar; %90 aralığın alt sınırı (−0,110) ise −0,10'u aşar (J4 `b4.duyarlilik.yari_logit.H3.kestirim`, `.ci90`, `.ci95`). Ön kayıt kuralı bu ölçekte uygulansaydı TOST eşdeğerliği tutmayacak, |kestirim| 0,10'un altında kaldığı için çürütme koşulu da tutmayacak, H3 kararsız olacaktı. Oran ölçeğinde de mimari yönlü etki −4,13 puandır (%90 [−4,90; −3,37], %95 [−5,11; −3,16]; `b4.duyarlilik.yari_oran.H3`) ve %95 aralığı sıfırı dışlar; bu ölçekte birimler puan olduğundan δ ile doğrudan karşılaştırılamaz. ÖK §5 gereği duyarlılıklar kararı değiştirmez ve birincil karar log ölçekte eşdeğer olarak kalır; ancak bu sonuç, §7'de önerilen "log ölçekte, CNN panelinde" nitelemesinin zorunlu olduğunu gösterir.

Ön kayıtlı ikincil çözümlemeler ÖK §5 gereği keşifsel etiketlidir, çoklu düzeltme içermez ve aralıklarıyla verilir.

| Çözümleme | Öngörü | Gözlenen | Öngörü tuttu mu | Anahtar |
|---|---|---|---|---|
| S1, köprü σ: σ(R224-scr) − σ(C1 ResNet-18) | ±0,10 içinde | −0,0003, %90 [−0,035; 0,034] (birleşik varyanslı, df 3; Welch %90 [−0,120; 0,119], df 1,02) | evet, ÖK §5'in S1 için öngördüğü birleşik varyanslı aralıkla; Welch aralığı (df 1,02) bandı aşar | J4 `b4.ikincil.S1.sigma` |
| S1, köprü ρ | ±0,10 içinde | −0,021, %90 [−0,064; 0,023] | evet (`ongoru_ikisi_de_esdeger` = true) | `b4.ikincil.S1.rho` |
| S2, ρ(V-IN) − ρ(V-scr) | negatif | −0,130, %90 [−0,161; −0,099] | evet | `b4.ikincil.S2` |
| S3, ω başlatma etkisi ViT'de | ω(V-IN) < ω(V-scr) | −0,114, %90 [−0,151; −0,077] | evet | `b4.ikincil.S3.V_baslatma` |
| S3, ω başlatma etkisi ResNet'te | (yalnız raporlanır) | −0,018, %90 [−0,058; 0,023] | betimsel | `b4.ikincil.S3.R224_baslatma` |
| S3, ω etkileşimi | (yalnız raporlanır) | −0,096, %90 [−0,151; −0,041] | betimsel | `b4.ikincil.S3.etkilesim` |
| S5, protokol katmanı örnek dışı sapma | ort sapma ±1,5 puan içinde; çürütme: %90 aralık bandın tümüyle dışında | ort −0,181 puan, %90 [−0,500; 0,138] | evet; çürütme yok | `b4.ikincil.S5.ozet` |
| S6, XCiT panelinde işaret | A^σ_scr ve I^σ birincille aynı işaretli | A^σ_scr −0,284, I^σ 0,254 | evet | `b4.ikincil.S6` |
| S7, Hodge | (betimsel) | K = 20, potansiyel payı 0,919 (rastgele beklenti 0,10), dolaşım RMS 0,022, r RMS 0,078 | betimsel | `b4.ikincil.S7` |

S4 betimseldir ve tohum indeksiyle eşleşmiş dört çifti verir (J4 `b4.ikincil.S4[k].tam`). Sıfırdan satırında (R224_scr_s1201 ile ViT_Tiny_AT_s2001; R224_scr_s1202 ile ViT_Tiny_AT_s2002) hedef doğru asimetri 4,18 ve 4,43 puan, log oran 0,248 ve 0,266, potansiyel (w) bileşeni 0,125 ve 0,142, yönlü artık r 0,123 ve 0,124, potansiyel payı 0,504 ve 0,534'tür. IN satırında (R224_IN_s1301 ile V_IN_s2101; R224_IN_s1302 ile V_IN_s2102) asimetri −1,28 ve 0,78 puan, log oran −0,056 ve 0,036, potansiyel bileşeni −0,002 ve 0,068, r −0,054 ve −0,032'dir; log oran sıfıra yakın olduğundan potansiyel payı oranı (0,037 ve 1,896) bu satırda kararsızdır ve yorumlanmamalıdır. S5'in dört çift sapması −0,309, −0,473, 0,151 ve −0,093 puandır (`b4.ikincil.S5.ozet.degerler`); dayandığı ilişki eğim 0,796 ve kesişim −0,01'dir (`b4.ikincil.S5.egim_kesisim`).

## 5. B5: saldırı tarafı (tek sınamalı ayrı aile)

Ön kayıtlı öngörü, C1 ResNet-18 ile V-scr arasındaki panel kaynak açığının her kaynağın en iyi izinli saldırısı altında en az yarısının korunmasıdır (korunma oranı ≥ 0,5); destek ölçütü hiyerarşik bootstrap %90 aralığının alt sınırının 0,5 ya da üstünde olması, çürütme ölçütü üst sınırın 0,5'in altında kalmasıdır (ÖK §5 B5). G_PGD 0,389'dur (bootstrap %90 [0,370; 0,409]) ve 0,10'luk hesaplanabilirlik eşiğinin üzerindedir; çapraz uydurmalı seçimle G_best 0,374, korunma oranı 0,960, %90 aralığı [0,941; 0,976], %95 aralığı [0,937; 0,981]'dir ve 2000 kopyanın tamamı geçerlidir (J5 `b5.birincil_C1-R32_V-scr.G_PGD`, `.G_best`, `.oran`, `.bootstrap.ci90`, `.bootstrap.ci95`, `.bootstrap.G_PGD_ci90`, `.bootstrap.gecerli`). Karar destektir (`b5.birincil_C1-R32_V-scr.karar` = "destek"). Tam örneklemle seçim duyarlılığında oran 0,960'tır (`.duyarlilik_tam_orneklem_secim.oran`).

Seçilen saldırılar şöyledir: C1 ResNet-18 kaynaklarından s1001 ve s1002'de PGD-10, s1003'te MI-PGD; üç V-scr kaynağında da MI-PGD (`.kaynaklar.*.secilen_cift_tek`, `.secilen_tam_orneklem`). TGR hiçbir kaynakta seçilmemiştir. Panel üzerindeki S_k farkları bunu açıklar: V-scr kaynaklarında S_TGR − S_PGD −0,147, −0,188 ve −0,218, S_MI − S_PGD 0,018, 0,015 ve 0,016; V-IN kaynaklarında S_TGR − S_PGD −0,217 ve −0,168'dir (TR; `.kaynaklar.*.S_tam`). En iyi saldırı seçimi açığı yalnız 0,016 log birimi kapatmış (G_PGD − G_best; TR), TGR ise seçilseydi açığı büyütecekti.

Yeni hücre çiftleri ÖK gereği betimseldir. R224-scr ile V-scr arasında G_PGD 0,399, G_best 0,383, oran 0,959'dur (J5 `b5.betimsel.R224-scr_V-scr`). R224-IN ile V-IN arasında G_PGD 0,072'dir (`b5.betimsel.R224-IN_V-IN.G_PGD`) ve 0,10 eşiğinin altında kaldığından betiğin bu çift için yazdığı oran (`.oran`) yorumlanmaz.

## 6. B6: AutoAttack ve maskeleme kuralı

Kural, test kümesinin ilk 1000 görüntüsünde PGD-10 doğruluğu ile AutoAttack doğruluğu arasındaki fark 10 puanı aşan modeli maskeleme şüphesiyle işaretler (ÖK §5 B6; M6 `esik_puan` = 10.0, `n` = 1000).

| Model | Temiz (ilk 1000) | PGD-10 (B4 köşegeni, ilk 1000) | AutoAttack | Fark (puan) | İşaretli |
|---|---|---|---|---|---|
| V_IN_s2101 | 85,8 | 43,3 | 40,1 | 3,2 | hayır |
| V_IN_s2102 | 83,7 | 42,2 | 38,8 | 3,4 | hayır |
| R224_IN_s1301 | 87,4 | 45,8 | 38,4 | 7,4 | hayır |
| R224_IN_s1302 | 86,9 | 47,4 | 41,8 | 5,6 | hayır |
| R224_scr_s1201 | 87,2 | 43,9 | 39,5 | 4,4 | hayır |
| R224_scr_s1202 | 85,7 | 45,1 | 41,1 | 4,0 | hayır |

Tablodaki değerler M6'nın `modeller.<m>` altındaki `temiz_dogruluk_aa`, `pgd10_dogruluk`, `aa_dogruluk`, `fark_puan` ve `isaretli` alanlarından alınmıştır. AutoAttack değerleri AA dosyasındaki `clean_accuracy` ve `robust_accuracy` sütunlarıyla aynıdır ve ZL satır 94-99 da aynı değerleri basmaktadır. Aynı örneklem koşulu denetlenmiştir: altı modelde de AA ile matrisin temiz doğru maskeleri arasında uyuşmazlık sıfırdır (`temiz_maske_uyusmazligi` = 0) ve AA altında doğru kalıp PGD-10'da yanılan görüntü yoktur (`aa_robust_pgd_yanilmis` = 0). PGD-10 sütunu bu raporda B4 köşegen npz dosyalarından bağımsız olarak yeniden hesaplanmış ve altı modelde birebir aynı çıkmıştır (KS). İşaretli model olmadığından (`isaretli` boş, `maskeleme_isaretli_arg` boş) H1-H3'ün işaretlilersiz yeniden hesabı gerekmemiş, bölge O1 olarak kalmıştır (J4 `b4.F_B4.maskeleme_kurali`). En büyük fark R224_IN_s1301'dedir (7,4 puan) ve eşiğin 2,6 puan altındadır.

ÖK Dondurma eki (i) madde 7 gereği V-scr ve C1 ResNet-18 modelleri için B6 maskeleme kuralı tanımlanmamıştır. Betimsel karşılaştırma için FÖY Tablo I, C1 kampanyasının üç tohum ortalamasında (n = 10000) AT'li ResNet-18 için PGD-10 44,11 ve AA 37,93, AT'li ViT-Tiny için PGD-10 32,69 ve AA 29,14 verir (FÖY satır 16 ve 17). Bu farklar da 10 puanın altındadır, ancak örneklem ve kestirim yöntemi B6 kuralınınkiyle aynı olmadığından karar kuralının yerine geçmez.

## 7. Sapmalar ve şüpheler

Ana ön kayda ait, çözümlemeden önce yazılmış bir sapma kaydı yoktur ve bu rapor sırasında ÖK §7 anlamında sapma sayılması gereken bir durum bulunmamıştır. Aşağıdaki maddeler `results/q1_research/ONKAYIT_SAPMALAR.md` dosyasına ana oturum tarafından "sapma değil, beyan" ya da "eksik duyarlılık" olarak işlenmelidir; makaleye etkileri her maddede yazılıdır.

1. B3'teki AT epok süreleri pilotun 1,05 ile 2,19 katı arasındadır (DF 4, 10, 12, 16, 20, 23; TR). Aşama başı `nvidia-smi` anlık görüntülerinin üçünde GPU dolu görünmüştür (NV satır 103, 195, 218; DF 10, 18, 20), ancak en yavaş iki AT aşamasının başında böyle bir yük görünmediğinden yavaşlamanın nedeni kayıtlardan belirlenemez (§2). Tavan değişmemiş, bütçe aşılmamıştır (17,79 sa; ZL satır 77). ÖK §4'e göre bu bir sapma değildir. Makalenin "Computational Details" bölümüne RTX 5090 notuyla birlikte "AT epok süreleri pilot ölçümünün 1,05-2,19 katıdır; GPU aşama başı kayıtlarında zaman zaman dolu görünmüştür" düzeyinde bir beyan yazılmalı, paylaşım yavaşlamanın nedeni olarak sunulmamalıdır.
2. R224-IN temiz aşama denetiminin referansı iki koşuda da tek R224-scr koşusunun (s1201) ilk epoğudur (n = 1; DF 9 ve 19). Bu, ÖK §4'ün "denetim anında en az bir epoğu tamamlanmış" ifadesine uygundur; R224_scr_s1202'nin ilk epoğu (36,65; GL satır 11) referansa eklenseydi referans 37,75, iki IN koşusunun farkı 49,50 ve 50,10 olurdu (TR); karar değişmezdi. Beyan yeterlidir.
3. ÖK §5'in duyarlılık listesindeki hiyerarşik bootstrap B2'de K-a ve K-b için üretilmemiştir; J2'de karşılığı yoktur. Dondurulmuş betik değiştirilemeyeceğinden bu duyarlılık ya ayrı, keşifsel etiketli bir betikle koşulmalı ya da makalede "yapılmadı" diye beyan edilmelidir. Kararlar etkilenmez, çünkü ÖK §5 gereği duyarlılıklar karar değiştirmez.
4. B5'in betimsel IN çiftinde G_PGD 0,10'un altındadır (0,072) ve betik buna rağmen bir oran (0,937) yazmıştır. Birincil sınamanın kuralı betimsel çifte de uygulanmalı, bu oran föye ve makaleye taşınmamalıdır.
5. R224_IN_s1301 ile R224_scr_s1201'in seçilen epok doğrulama PGD doğruluğu ikisinde de 46,40'tır (ZL satır 56 ve 59; GL `R224_IN_s1301_AT.log` satır 23476, `R224_scr_s1201_AT.log` satır 32425). Çakışmanın bir günlük ya da kontrol noktası karışmasından gelip gelmediği B4 köşegeninden denetlenmiştir. İki modelin test kümesindeki beyaz kutu PGD-10 doğruluğu 44,30 ve 43,75 (4430 ve 4375 görüntü), hedef doğru beyaz kutu kırılganlığı w 48,344 ve 49,334, ilk 1000 görüntüdeki PGD-10 doğruluğu 45,8 ve 43,9, AutoAttack doğruluğu 38,4 ve 39,5'tir (KS; M6). Görüntü bazında PGD-10 doğruluk durumları yalnız 0,842 oranında örtüşür: 3613 görüntüde ikisi de doğru, 817 görüntüde yalnız R224_IN_s1301, 762 görüntüde yalnız R224_scr_s1201 doğrudur. Birbirlerine transfer 27,15 ve 26,34'tür, iki kontrol noktasının SHA-256 özetleri farklıdır (`84eef038...` ve `e8f5fb58...`), seçilen epoklar (16 ve 22) ve ilk AT epoğu doğrulama PGD değerleri (31,45 ve 31,95; GL satır 1490 ve 1471) de farklıdır. Doğrulama bölmesi 2000 görüntülük olduğundan 46,40, 928 doğru görüntüye karşılık gelir ve doğruluk 0,05 puanlık adımlarla değişir; dört R224 koşusunun seçilen doğrulama PGD değerleri 45,85 ile 46,95 arasında, yani 23 adımlık bir bantta toplanmıştır. Çakışma bu nedenle tesadüftür; föye ve makaleye etkisi yoktur.
6. ÖK Dondurma eki (i) madde 9'daki açık sürmektedir: iki ImageNet başlatma kontrol noktasının ImageNet top-1 değerleri henüz kayda geçmemiştir; makalenin yöntem bölümü için gereklidir.
7. Föy otomatik üretilmektedir (`scripts/build_reference_sheet.py`); bu rapordaki sayılar makaleye ancak föye "M9 konsey" bölümü bu betik üzerinden eklendikten sonra girebilir (KONSEY_PLANI §9).

Beklenmedik gözlemler ve föye ya da makaleye etkileri şunlardır. Sıfırdan eğitilmiş ViT'nin temiz test doğruluğu yüzde 73,01-74,10, öteki dokuz C1 ve B3 modelininki yüzde 83,39-86,35'tir (KS); V-scr'nin beyaz kutu kırılganlığı w de (55,12-55,91) öteki hücrelerden (47,73-51,11) yüksektir (TR, exp(ω)). H1'in "mimariye ait benzemezlik" yorumu bu doğruluk farkıyla aynı tasarım hücresinde birlikte değiştiğinden makalede sınırlılık olarak yazılmalıdır (bkz. §8). Yönlü terimin işareti ve büyüklüğü ölçeğe bağlıdır: B2'de ρ(V-scr) logit ölçekte −0,304'tür (§3); H3'ün logit kestirimi −0,087'dir, %95 aralığı sıfırı dışlar, %90 aralığı −0,10'u aşar ve ön kayıt kuralı bu ölçekte uygulansaydı H3 kararsız olurdu; oran ölçeğinde de mimari yönlü etki −4,13 puandır ve %95 aralığı sıfırı dışlar (§4). O1 manşetindeki "küçük, mimariden bağımsız bir yönlü terim" ifadesi bu nedenle metinde "log ölçekte, CNN panelinde" nitelemesiyle yazılmalıdır (panel nitelemesinin gerekçesi §8'dedir). ImageNet başlatmalı ViT hücresinin ρ ortalaması −0,118'dir ve δ'nın dışındadır (J4 `...H3.hucre_ort.V-IN`); H3'ün eşdeğerliği bir ana etki eşdeğerliğidir, her hücrede küçük yönlü terim anlamına gelmez (§8). TGR'nin CNN paneline PGD-10'dan zayıf transfer etmesi beklenmedik değildir ama metinde "ViT'ye özgü saldırı açığı kapatmamıştır, büyütmüştür" biçiminde açıkça yazılmalıdır (§5).

## 8. Keşifsel notlar (ön kayıt dışı)

Bu bölümdeki her yorum ön kayıt dışıdır, hiçbir karar kuralına bağlı değildir ve makalede "keşifsel" etiketiyle yer alabilir.

H3'ün eşdeğerliği iki satırdaki zıt işaretli farkların birbirini götürmesinden doğmaktadır. Sıfırdan satırında ρ(V-scr) − ρ(R224-scr) = +0,070, IN satırında ρ(V-IN) − ρ(R224-IN) = −0,064'tür; yönlü terimde mimari ile başlatmanın etkileşimi bu iki farkın farkı olarak −0,134'tür (TR; J4 `...H3.hucre_ort`). Her satır farkı tek başına ±0,10 içinde kaldığı için "mimariye ait büyük bir yönlü terim yoktur" okuması korunur; ancak başlatmanın ViT yönlü terimini değiştirdiği (S2: −0,130) ve bu değişimin ResNet'te görülmediği söylenebilir. Bu etkileşim ön kayıtta sınanmamıştır, aralığı da hesaplanmamıştır.

Başlatmanın panel benzerliğine etkisi neredeyse yalnız ViT satırındadır: σ(V-IN) − σ(V-scr) = +0,270, σ(R224-IN) − σ(R224-scr) = +0,009'dur (TR; J4 `...H2.hucre_ort`). ImageNet başlatmasından sonra da ViT, CNN paneline ResNet'ten daha az benzemektedir: σ(V-IN) − σ(R224-IN) = −0,104 (TR). Bu değer ek ön kaydın B8 için H1 ve H2'nin öngörü sınırlarından türettiği yaklaşık −0,10'luk beklentiyle (KONSEY_PLANI §13) sayısal olarak örtüşmektedir; B8 bağımsız bir veri kümesinde koşulmadan bu örtüşmeye anlam yüklenmemelidir. Çarpımsal okumada A^σ_scr = −0,364, exp(−0,364) ≈ 0,69 demektir (TR): sıfırdan eğitimde ViT'nin CNN paneliyle simetrik transfer verimi (panel üzerinden geometrik ortalama), girdi hattı eşitlenmiş ResNet'inkinin yaklaşık yüzde 69'udur.

Saldırı tarafındaki betimsel hücre çiftlerinde de benzer bir örüntü görülmektedir. B5'te ResNet ile ViT arasındaki kaynak açığı sıfırdan satırında G_PGD = 0,399 iken IN satırında 0,072'ye inmektedir (J5 `b5.betimsel.R224-scr_V-scr.G_PGD`, `b5.betimsel.R224-IN_V-IN.G_PGD`). IN satırında kaynak açığının neredeyse kapanması H2'nin σ ölçeğindeki sonucuyla aynı yöndedir; ancak bu karşılaştırma ön kayıtta tanımlanmamış, iki değer arasındaki fark için aralık da hesaplanmamıştır.

V-scr hücresinin temiz doğruluk ve kırılganlık bakımından öteki hücrelerden ayrışması (§7), H1'in mimari karşıtlığının bir kısmının "daha az yakınsamış çözüm" etkisi olabileceğini düşündürür. Tasarım bu iki açıklamayı ayıramaz. V-IN'in temiz doğruluğu (yüzde 83,39 ve 83,47; KS) R224 hücreleriyle aynı düzeye çıktığı halde σ(V-IN) − σ(R224-IN) farkının −0,104 olarak kalması, benzemezliğin tamamının doğruluk düzeyine indirgenemeyeceğine işaret etse de bu tek karşılaştırma bir sınama değildir. Yirmi model üzerinde σ ile temiz doğruluk ya da ω arasındaki ilişkinin masa düzeyinde, keşifsel etiketiyle betimlenmesi hakem itirazına karşı yararlı olur.

ViT tohumları birbirine en az ResNet tohumları kadar benzemektedir: tür içi log τ̄ ortalaması ViT'de −0,443, ResNet'te −0,489'dur (TR; J2 `b2.F_B2.K-c.log_tau_tur_ici`, `b2.tur_ici_resnet_log_tau`). Bu gözlem, ViT'nin CNN paneline benzemezliğinin tohumlar arası gürültüden değil aileler arası farktan geldiği yorumunu destekler.

Yönlü terim panel bileşimine de bağlıdır: tek üyeli XCiT panelinde ρ(V-scr) yaklaşık +0,20'dir (§3), yani ViT bir dönüştürücü referansa göre yönlü olarak belirgin biçimde zayıf kaynaktır. "Küçük yönlü terim" ifadesi bu yüzden "CNN panelinde" nitelemesiyle yazılmalıdır.

## 9. Makale için sonraki adımlar (KONSEY_PLANI §9, O1 bölgesi)

KONSEY_PLANI §9 tablosunun O1'e karşılık gelen maddeleri şunlardır ve bu sonuçla geçerlidir.

1. Başlık (`main.tex:62-63`) O1 önerisine çevrilir: "Not a Weak Source but a Different One: Vulnerability, Similarity and Direction in CNN-to-ViT Adversarial Transfer under an Architecture × Initialisation Design". Başlıkta ölçek ya da panel nitelemesi bulunmadığından §7 ve §8'deki "log ölçekte, CNN panelinde" nitelemesi özet ve katkılarda yapılmalıdır.
2. Özet (`main.tex:108`) soru, ayrışım ve masa sonucu (simetrik oran, potansiyel payı), 2x2 karşıtlıkları (H1, H2, H3) aralıklarıyla ve protokol katmanını tek cümleyle verir; B5'in korunma oranı ve B6'nın maskeleme sonucu birer yan cümleyle eklenebilir.
3. Katkılar (`01_introduction.tex:29-45`) dörde iner: tanımlanabilirlik (Önerme 1c ve tez uzlaşması), w-τ̄-r ayrışımı ve ölçülen büyüklükler, 2x2 müdahale, protokol ve h ölçeği ayarı (Önerme 3).
4. `02_related_work.tex` KONSEY_PLANI §9'daki kaynak listesiyle genişler; atıflar eklenmeden önce DOI ya da arXiv kimliğiyle doğrulanmalıdır.
5. `03_methodology.tex` ayrışım tanımlarını, yedi üyeli paneli, 2x2 tarifini, bölünmüş yarı kestirimini ve ön kaydı (dondurma karması dahil) verir; `fig:study_overview` yenilenir.
6. `04_experiments.tex`'te `tab:source_target` ayrışım tablosuyla değişir; yeni tablolar 2x2 hücreleri (temiz, AA, ω, σ, ρ), tür içi benzerlik ve saldırı tarafıdır; `tab:external_pool` σ ve ρ sütunları alır.
7. `05_discussion.tex` tez uzlaşmasını, yörünge sonucunu ölçüm sınırı olarak, sınırlılıkları (CIFAR, Tiny ölçeği, hücrede n = 2) ve bu raporun §7-§8'inden doğan üç ek sınırlılığı (logit ölçekte yönlü terimin işaret değiştirmesi, V-scr'nin düşük temiz doğruluğu, V-IN'in δ dışındaki yönlü terimi) yazar.
8. `06_conclusion.tex` ve TR aynası manşetle eşitlenir; sayılar yalnız föyün yeni M9 bölümünden alınır.

Bunlardan önce yapılması gerekenler sırasıyla şunlardır: §7'deki maddelerin `ONKAYIT_SAPMALAR.md`'ye işlenmesi; föye M9 bölümünün `scripts/build_reference_sheet.py` üzerinden eklenmesi; iki ImageNet kontrol noktasının top-1 değerlerinin kaydı; zincir sonrasında planlanan n = 200 regresyon koşusu ve ek bloklar B8-B10 (ek ön kayıt; bu rapordaki sonuçlar onların öngörülerini değiştirmez); ardından makale revizyonu, tek turlu hakem paneli ve KONSEY_PLANI §11'deki şekil görevi.

## Sayı kaynak dizini

Her satır (değer, dosya, anahtar ya da satır) üçlüsüdür. Değer raporda görüldüğü biçimdedir; JSON'daki ham değer gösterilen basamağa yuvarlanmıştır. TR satırlarında anahtar sütunu formülü verir; KS satırlarında dosya npz, anahtar sütunu hesaplamayı verir (`target_clean_correct` ve `target_adv_wrong` dizileri).

| Değer | Dosya | Anahtar ya da satır |
|---|---|---|
| 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 | results/q1/konsey_ayrisim_b2.json | meta.betik_sha256 (J4 ve J5'te aynı alan) |
| 2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500 | results/q1/konsey_ayrisim_b2.json | meta.hucre_tablosu_sha256 (J4 ve J5'te aynı alan) |
| 46ab58fb4843a30265f44c04c8fc4831b7a3601df57aa520da1efd7e03a663a5 | raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | Dondurma eki (b); yeniden hesap arsiv/b2_yardimci/_rapor_govde_ozet.py |
| O1 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karar.sonuc_bolgesi |
| O1 (maskeleme sonrası) | results/q1/konsey_ayrisim_b4.json | b4.F_B4.maskeleme_kurali.uygulanan_bolge |
| −0,364 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H1.kestirim |
| [−0,415; −0,314] | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H1.ci90 |
| [−0,428; −0,300] | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H1.ci95 |
| −14,60 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H1.t |
| 1,36e-05 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H1.p_tek_kucuk; b4.F_B4.p_ham[0] |
| 4,09e-05 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.p_holm[0] |
| +0,260 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.kestirim |
| [0,186; 0,335] | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.ci90 |
| [0,165; 0,355] | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.ci95 |
| 7,03 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.t |
| 9,00e-04 (ham) | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.p_iki; b4.F_B4.p_ham[1] |
| 9,00e-04 (Holm) | results/q1/konsey_ayrisim_b4.json | b4.F_B4.p_holm[1] |
| 0,354 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karar.H2_logit_kestirim |
| 0,003 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.kestirim |
| [−0,020; 0,026] | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.ci90 |
| [−0,026; 0,033] | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.ci95 |
| 0,29 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.t |
| 1,89e-04 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.tost_p; b4.F_B4.p_ham[2] |
| 3,79e-04 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.p_holm[2] |
| 3 / 2 / 2 / 2 (hücre n) | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.hucre_n |
| 0,0273 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H1.sp_birlesik |
| 0,050 | results/q1/konsey_ayrisim_b4.json | TR: (H1.ci90[1] − H1.ci90[0]) / 2 |
| 0,075 | results/q1/konsey_ayrisim_b4.json | TR: (H2.ci90[1] − H2.ci90[0]) / 2 |
| 0,023 | results/q1/konsey_ayrisim_b4.json | TR: (H3.ci90[1] − H3.ci90[0]) / 2 |
| 0,074 | results/q1/konsey_ayrisim_b4.json | TR: \|b4.F_B4.degerler.sigma.V-IN[0] − [1]\| |
| −1,009 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.hucre_ort.V-scr |
| −0,739 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.hucre_ort.V-IN |
| −0,645 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.hucre_ort.R224-scr |
| −0,635 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H2.hucre_ort.R224-IN |
| −1,015; −1,000; −1,011 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.sigma.V-scr (J2 b2.F_B2.K-c.sigma_V ile aynı) |
| −0,702; −0,776 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.sigma.V-IN |
| −0,625; −0,664 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.sigma.R224-scr |
| −0,642; −0,628 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.sigma.R224-IN |
| 0,012 (ρ V-scr) | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.hucre_ort.V-scr |
| −0,118 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.hucre_ort.V-IN |
| −0,058 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.hucre_ort.R224-scr |
| −0,054 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H3.hucre_ort.R224-IN |
| 0,025; 0,007; 0,004 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.rho.V-scr (J2 b2.F_B2.K-b.degerler ile aynı) |
| −0,131; −0,105 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.rho.V-IN |
| −0,038; −0,079 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.rho.R224-scr |
| −0,056; −0,052 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.degerler.rho.R224-IN |
| 4,019 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S3.etkilesim.hucre_ort.V-scr |
| 3,905 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S3.etkilesim.hucre_ort.V-IN |
| 3,890 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S3.etkilesim.hucre_ort.R224-scr |
| 3,872 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S3.etkilesim.hucre_ort.R224-IN |
| 55,91; 55,86; 55,12 | results/q1/konsey_ayrisim_b4.json | TR: exp(b4.F_B4.degerler.omega.V-scr[k]) |
| 48,24; 51,11 | results/q1/konsey_ayrisim_b4.json | TR: exp(b4.F_B4.degerler.omega.V-IN[k]) |
| 49,33; 48,47 | results/q1/konsey_ayrisim_b4.json | TR: exp(b4.F_B4.degerler.omega.R224-scr[k]) |
| 48,34; 47,73 | results/q1/konsey_ayrisim_b4.json | TR: exp(b4.F_B4.degerler.omega.R224-IN[k]) |
| 55,12-55,91 ve 47,73-51,11 | results/q1/konsey_ayrisim_b4.json | TR: yukarıdaki dört satırın uçları |
| 4,09e-05; 1,80e-03; 2,13e-03 | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.delta_0.06.p_holm |
| O1 (δ = 0,06) | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.delta_0.06.sonuc_bolgesi |
| −0,364 [−0,414; −0,314] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.tam_log.H1.kestirim, .ci90 |
| 0,260 [0,186; 0,334] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.tam_log.H2.kestirim, .ci90 |
| 0,004 [−0,020; 0,027] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.tam_log.H3.kestirim, .ci90 |
| −0,498 [−0,570; −0,426] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_logit.H1.kestirim, .ci90 |
| 0,354 [0,247; 0,461] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_logit.H2.kestirim, .ci90 |
| −0,087 [−0,110; −0,064] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_logit.H3.kestirim, .ci90 |
| −8,50 [−9,85; −7,14] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_oran.H1.kestirim, .ci90 |
| 5,85 [3,83; 7,86] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_oran.H2.kestirim, .ci90 |
| −4,13 [−4,90; −3,37] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_oran.H3.kestirim, .ci90 |
| [−0,569; −0,160] (df 1,10) | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.welch.H1.ci95, .df |
| [0,029; 0,491] (df 1,63) | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.welch.H2.ci95, .df |
| [−0,052; 0,059] (df 1,95) | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.welch.H3.ci95, .df |
| −0,376; −0,346 | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.panel_jackknife.Sehwag2021Proxy_R18.H1; .Engstrom2019Robustness.H1 |
| 0,249; 0,266 | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.panel_jackknife.Engstrom2019Robustness.H2; .Wong2020Fast.H2 |
| 0,001; 0,006 | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.panel_jackknife.Wong2020Fast.H3; .Sehwag2021Proxy_R18.H3 |
| [−0,393; −0,335] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.hiyerarsik_bootstrap.H1.ci90 |
| [0,204; 0,316] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.hiyerarsik_bootstrap.H2.ci90 |
| [−0,024; 0,031] | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.hiyerarsik_bootstrap.H3.ci90 |
| −0,0003 [−0,035; 0,034] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S1.sigma.kestirim, .ci90 |
| [−0,120; 0,119] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S1.sigma.welch.ci90 |
| −0,021 [−0,064; 0,023] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S1.rho.kestirim, .ci90 |
| −0,130 [−0,161; −0,099] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S2.kestirim, .ci90 |
| −0,114 [−0,151; −0,077] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S3.V_baslatma.kestirim, .ci90 |
| −0,018 [−0,058; 0,023] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S3.R224_baslatma.kestirim, .ci90 |
| −0,096 [−0,151; −0,041] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S3.etkilesim.kestirim, .ci90 |
| −0,181 [−0,500; 0,138] | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S5.ozet.ort, .ci90 |
| −0,309; −0,473; 0,151; −0,093 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S5.ozet.degerler |
| 0,796; −0,01 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S5.egim_kesisim |
| −0,284 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S6.A_sigma_scr |
| 0,254 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S6.I_sigma |
| 20 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S7.K |
| 0,919 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S7.G_potansiyel_payi |
| 0,10 (rastgele beklenti) | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S7.G_rastgele_beklenti_2_bolu_K |
| 0,022 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S7.dolasim_rms |
| 0,078 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S7.r_rms |
| 4,18; 4,43 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[0].tam.asimetri_puan; S4[1].tam.asimetri_puan |
| 0,248; 0,266 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[0].tam.log_oran; S4[1].tam.log_oran |
| 0,125; 0,142 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[0].tam.log_w_potansiyel; S4[1].tam.log_w_potansiyel |
| 0,123; 0,124 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[0].tam.r; S4[1].tam.r |
| 0,504; 0,534 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[0].tam.potansiyel_payi; S4[1].tam.potansiyel_payi |
| −1,28; 0,78 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[2].tam.asimetri_puan; S4[3].tam.asimetri_puan |
| −0,056; 0,036 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[2].tam.log_oran; S4[3].tam.log_oran |
| −0,002; 0,068 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[2].tam.log_w_potansiyel; S4[3].tam.log_w_potansiyel |
| −0,054; −0,032 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[2].tam.r; S4[3].tam.r |
| 0,037; 1,896 | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S4[2].tam.potansiyel_payi; S4[3].tam.potansiyel_payi |
| +0,070 | results/q1/konsey_ayrisim_b4.json | TR: H3.hucre_ort.V-scr − H3.hucre_ort.R224-scr |
| −0,064 | results/q1/konsey_ayrisim_b4.json | TR: H3.hucre_ort.V-IN − H3.hucre_ort.R224-IN |
| −0,134 | results/q1/konsey_ayrisim_b4.json | TR: (V-IN − R224-IN) − (V-scr − R224-scr), H3.hucre_ort |
| +0,270 | results/q1/konsey_ayrisim_b4.json | TR: H2.hucre_ort.V-IN − H2.hucre_ort.V-scr |
| +0,009 | results/q1/konsey_ayrisim_b4.json | TR: H2.hucre_ort.R224-IN − H2.hucre_ort.R224-scr |
| −0,104 | results/q1/konsey_ayrisim_b4.json | TR: H2.hucre_ort.V-IN − H2.hucre_ort.R224-IN |
| 0,69 | results/q1/konsey_ayrisim_b4.json | TR: exp(b4.F_B4.karsitliklar.H1.kestirim) |
| 0,936 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.sinama.ort |
| 0,940; 0,928; 0,940 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.q |
| [0,925; 0,948] | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.sinama.ci90 |
| [0,919; 0,953] | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.sinama.ci95 |
| 4,19e-05 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.p_tek_H0_q_le_0.5; b2.F_B2.p_ham[0] |
| 1,26e-04 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.p_holm[0] |
| 0,391; 0,387; 0,390 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.D |
| 0,368; 0,360; 0,367 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.simetrik_pay |
| 0,023; 0,028; 0,023 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.yonlu_pay |
| 4,3e-16 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.ozdeslik_artik_max |
| 0,012 (K-b) | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-b.ort |
| [−0,007; 0,031] | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-b.ci90 |
| [−0,016; 0,040] | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-b.ci95 |
| 2,73e-03 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-b.tost_p; b2.F_B2.p_ham[1]; b2.F_B2.p_holm[1] |
| 0,566 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-c.Delta_w |
| [0,537; 0,604] | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-c.bootstrap.ci90 |
| [0,533; 0,608] | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-c.bootstrap.ci95 |
| 5,00e-04 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-c.p_tek_H0_Delta_le_0; b2.F_B2.p_ham[2] |
| 1,00e-03 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.p_holm[2] |
| 284 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-c.bootstrap.yeniden_cekilen_tek_tohumlu_ornek |
| 2000 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-c.bootstrap.B |
| −0,453; −0,466; −0,410 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-c.log_tau_tur_ici (üç çift) |
| −0,443 | results/q1/konsey_ayrisim_b2.json | TR: b2.F_B2.K-c.log_tau_tur_ici ortalaması |
| −0,489 | results/q1/konsey_ayrisim_b2.json | TR: b2.tur_ici_resnet_log_tau ortalaması |
| 8,98e-03 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.duyarlilik_delta_0.06.p_holm[1] |
| 0,937; 0,012 | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.tam_log.q_ort; .rho_V.ort |
| 1,101 | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.yari_logit.q_ort |
| −0,304 [−0,320; −0,289] | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.yari_logit.rho_V.ort, .ci90 |
| 1,542; −14,66 | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.yari_oran.q_ort; .rho_V.ort |
| 0,931; 0,941 | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.panel_jackknife.Sehwag2021Proxy_R18.q_ort; .Carmon2019Unlabeled.q_ort |
| 0,001; 0,022 | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.panel_jackknife.Engstrom2019Robustness.rho_V_ort; .Gowal2020Uncovering_28_10_extra.rho_V_ort |
| 0,899; 0,825; 0,842 | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.ikincil_panel.q |
| 0,198; 0,202; 0,204 | results/q1/konsey_ayrisim_b2.json | b2.duyarlilik.ikincil_panel.rho_V |
| 0,389 | results/q1/konsey_ayrisim_b5.json | b5.birincil_C1-R32_V-scr.G_PGD |
| [0,370; 0,409] | results/q1/konsey_ayrisim_b5.json | b5.birincil_C1-R32_V-scr.bootstrap.G_PGD_ci90 |
| 0,374 | results/q1/konsey_ayrisim_b5.json | b5.birincil_C1-R32_V-scr.G_best |
| 0,960 | results/q1/konsey_ayrisim_b5.json | b5.birincil_C1-R32_V-scr.oran (tam örneklem: .duyarlilik_tam_orneklem_secim.oran) |
| [0,941; 0,976] | results/q1/konsey_ayrisim_b5.json | b5.birincil_C1-R32_V-scr.bootstrap.ci90 |
| [0,937; 0,981] | results/q1/konsey_ayrisim_b5.json | b5.birincil_C1-R32_V-scr.bootstrap.ci95 |
| 2000 (geçerli kopya) | results/q1/konsey_ayrisim_b5.json | b5.birincil_C1-R32_V-scr.bootstrap.gecerli |
| −0,147; −0,188; −0,218 | results/q1/konsey_ayrisim_b5.json | TR: kaynaklar.ViT_Tiny_AT_s200{1,2,3}.S_tam.tgr − .S_tam.pgd |
| 0,018; 0,015; 0,016 | results/q1/konsey_ayrisim_b5.json | TR: kaynaklar.ViT_Tiny_AT_s200{1,2,3}.S_tam.mi − .S_tam.pgd |
| −0,217; −0,168 | results/q1/konsey_ayrisim_b5.json | TR: b5.betimsel.R224-IN_V-IN.kaynaklar.V_IN_s210{1,2}.S_tam.tgr − .pgd |
| 0,399; 0,383; 0,959 | results/q1/konsey_ayrisim_b5.json | b5.betimsel.R224-scr_V-scr.G_PGD; .G_best; .oran |
| 0,072 | results/q1/konsey_ayrisim_b5.json | b5.betimsel.R224-IN_V-IN.G_PGD (§5 ve §8) |
| 0,937 (yorumlanmaz) | results/q1/konsey_ayrisim_b5.json | b5.betimsel.R224-IN_V-IN.oran |
| 10 (eşik) | results/q1/konsey_b6_maskeleme.json | esik_puan |
| 1000 (n) | results/q1/konsey_b6_maskeleme.json | n |
| 85,8; 43,3; 40,1; 3,2 | results/q1/konsey_b6_maskeleme.json | modeller.V_IN_s2101.{temiz_dogruluk_aa, pgd10_dogruluk, aa_dogruluk, fark_puan}; logs/konsey_zincir.log satır 94 |
| 83,7; 42,2; 38,8; 3,4 | results/q1/konsey_b6_maskeleme.json | modeller.V_IN_s2102.{...}; logs/konsey_zincir.log satır 95 |
| 87,4; 45,8; 38,4; 7,4 | results/q1/konsey_b6_maskeleme.json | modeller.R224_IN_s1301.{...}; logs/konsey_zincir.log satır 96 |
| 86,9; 47,4; 41,8; 5,6 | results/q1/konsey_b6_maskeleme.json | modeller.R224_IN_s1302.{...}; logs/konsey_zincir.log satır 97 |
| 87,2; 43,9; 39,5; 4,4 | results/q1/konsey_b6_maskeleme.json | modeller.R224_scr_s1201.{...}; logs/konsey_zincir.log satır 98 |
| 85,7; 45,1; 41,1; 4,0 | results/q1/konsey_b6_maskeleme.json | modeller.R224_scr_s1202.{...}; logs/konsey_zincir.log satır 99 |
| 3,2-7,4 | results/q1/konsey_b6_maskeleme.json | modeller.*.fark_puan (en küçük ve en büyük) |
| 2,6 | results/q1/konsey_b6_maskeleme.json | TR: esik_puan − modeller.R224_IN_s1301.fark_puan |
| 0 (maske uyuşmazlığı) | results/q1/konsey_b6_maskeleme.json | modeller.*.temiz_maske_uyusmazligi; modeller.*.aa_robust_pgd_yanilmis |
| 40,1 / 38,8 / 38,4 / 41,8 / 39,5 / 41,1 | results/q1/konsey_b6_aa/autoattack_results.csv | robust_accuracy sütunu, satır 2-7 |
| 44,11; 37,93 | results/C1_REFERANS_FOYU.md | satır 16 (Tablo I, ResNet-18 AT, PGD-10 ve AA) |
| 32,69; 29,14 | results/C1_REFERANS_FOYU.md | satır 17 (Tablo I, ViT-Tiny AT, PGD-10 ve AA) |
| 44,30; 43,75 | results/q1/konsey_b4_matris/per_sample_R224_IN_s1301_to_R224_IN_s1301.npz; ..._R224_scr_s1201_to_R224_scr_s1201.npz | KS: ort(target_clean_correct ∧ ¬target_adv_wrong) × 100 |
| 4430; 4375 | aynı iki npz | KS: toplam(target_clean_correct ∧ ¬target_adv_wrong) |
| 48,344; 49,334 | aynı iki npz | KS: toplam(target_adv_wrong ∧ target_clean_correct) / toplam(target_clean_correct) × 100 (J4 b4.ikincil.S4[2].tam.w_i ve S4[0].tam.w_i ile aynı) |
| 45,8; 43,9 | aynı iki npz | KS: ilk 1000 görüntüde PGD-10 doğruluğu (M6 pgd10_dogruluk ile aynı) |
| 0,842 | aynı iki npz | KS: PGD-10 doğruluk durumlarının görüntü bazında eşleşme oranı |
| 3613; 817; 762 | aynı iki npz | KS: ikisi doğru; yalnız R224_IN_s1301 doğru; yalnız R224_scr_s1201 doğru |
| 27,15; 26,34 | results/q1/konsey_b4_matris/per_sample_R224_IN_s1301_to_R224_scr_s1201.npz; ..._R224_scr_s1201_to_R224_IN_s1301.npz | KS: hedef doğru transfer oranı |
| 84eef038...; e8f5fb58... | models/q1/konsey/R224_IN_s1301/resnet18_224_in1k/adv/adversarial_training/best.pth; models/q1/konsey/R224_scr_s1201/resnet18_224/adv/adversarial_training/best.pth | KS: SHA-256 ilk 16 hane |
| 73,01-74,10 | results/q1/konsey_b4_matris/per_sample_ViT_Tiny_AT_s200{1,2,3}_to_ViT_Tiny_AT_s200{1,2,3}.npz | KS: ort(target_clean_correct) × 100 (73,01; 73,47; 74,10) |
| 83,39-86,35 | results/q1/konsey_b4_matris/per_sample_<m>_to_<m>.npz, m ∈ V_IN, R224_IN, R224_scr, ResNet18_AT | KS: ort(target_clean_correct) × 100, en küçük V_IN_s2101 83,39, en büyük R224_scr_s1201 86,35 |
| 83,39; 83,47 | results/q1/konsey_b4_matris/per_sample_V_IN_s210{1,2}_to_V_IN_s210{1,2}.npz | KS: ort(target_clean_correct) × 100 |
| 0,05 ve 928 | raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | §2 ("sabit 2000 örneklik doğrulama bölmesi"); TR: 100/2000; 46,40 × 2000 / 100 |
| 37,75; 49,50; 50,10 | results/q1/konsey_b3_defter.tsv; logs/konsey_b3/R224_scr_s1202_temiz.log | TR: (38,85 + 36,65)/2; 87,25 − 37,75 (defter satır 9); 87,85 − 37,75 (defter satır 19) |
| 0,016 | results/q1/konsey_ayrisim_b5.json | TR: b5.birincil_C1-R32_V-scr.G_PGD − .G_best |
| 69 (yüzde) | results/q1/konsey_ayrisim_b4.json | TR: exp(b4.F_B4.karsitliklar.H1.kestirim) × 100 |
| 23 adım | logs/konsey_zincir.log satır 56, 59, 71, 76 | TR: (46,95 − 45,85) / 0,05 + 1 |
| 46,40 | logs/konsey_zincir.log | satır 56 ve 59 (`val_pgd=46.40`); GL R224_IN_s1301_AT.log satır 23476, R224_scr_s1201_AT.log satır 32425 |
| 31,45; 31,95 | logs/konsey_b3/R224_IN_s1301_AT.log; logs/konsey_b3/R224_scr_s1201_AT.log | satır 1490; satır 1471 (`Epoch 1/100`, Adv) |
| 30; 38; 18; 45,15 | results/q1/konsey_b3_defter.tsv | satır 2 (epok); satır 5 (`kosulan_epok`, `secilen_epok`, `val_pgd`); logs/konsey_zincir.log satır 46 |
| 30; 36; 16; 46,40 | results/q1/konsey_b3_defter.tsv | satır 6; satır 11; logs/konsey_zincir.log satır 56 |
| 200; 42; 22; 46,40 | results/q1/konsey_b3_defter.tsv | satır 8; satır 13; logs/konsey_zincir.log satır 59 |
| 30; 47; 27; 42,90 | results/q1/konsey_b3_defter.tsv | satır 14; satır 17; logs/konsey_zincir.log satır 65 |
| 30; 37; 17; 46,95 | results/q1/konsey_b3_defter.tsv | satır 18; satır 21; logs/konsey_zincir.log satır 71 |
| 200; 58; 38; 45,85 | results/q1/konsey_b3_defter.tsv | satır 22; satır 24; logs/konsey_zincir.log satır 76 |
| 93,95 (25,22; +68,73); 97,25 | results/q1/konsey_b3_defter.tsv | satır 3; logs/konsey_zincir.log satır 39 |
| 87,25 (38,85; +48,40); 96,05 | results/q1/konsey_b3_defter.tsv | satır 9 (erteleme satır 7); logs/konsey_zincir.log satır 49 ve 53 |
| 94,60 (25,22; +69,38); 97,45 | results/q1/konsey_b3_defter.tsv | satır 15; logs/konsey_zincir.log satır 62 |
| 87,85 (38,85; +49,00); 96,15 | results/q1/konsey_b3_defter.tsv | satır 19; logs/konsey_zincir.log satır 68 |
| 38,85 | logs/konsey_b3/R224_scr_s1201_temiz.log | satır 11 (`Epoch 1/200`, Test Acc) |
| 36,65 | logs/konsey_b3/R224_scr_s1202_temiz.log | satır 11 (`Epoch 1/200`, Test Acc) |
| 94,65 | logs/konsey_b3/R224_scr_s1201_temiz.log | satır 105244 (`Best accuracy`) |
| 94,70 | logs/konsey_b3/R224_scr_s1202_temiz.log | satır 100925 (`Best accuracy`) |
| 23,75; 26,55; 25,35 | logs/C1_clean_vit_2001.log; _2002.log; _2003.log | satır 9 (`Epoch 1/200`, Test Acc) |
| 34,90 | results/q1/konsey_b3_defter.tsv | satır 4 (`cokus denetimi TAMAM 34.90`); logs/konsey_zincir.log satır 44; logs/konsey_b3/V_IN_s2101_cokus.txt |
| 41,90 | results/q1/konsey_b3_defter.tsv | satır 10; logs/konsey_b3/R224_IN_s1301_cokus.txt |
| 33,35 | results/q1/konsey_b3_defter.tsv | satır 16; logs/konsey_b3/V_IN_s2102_cokus.txt |
| 42,55 | results/q1/konsey_b3_defter.tsv | satır 20; logs/konsey_b3/R224_IN_s1302_cokus.txt |
| 40,10 | logs/konsey_b3/R224_scr_s1201_AT.log | satır 7303 (`Epoch 5/100`, Adv) |
| 40,75 | logs/konsey_b3/R224_scr_s1202_AT.log | satır 7536 (`Epoch 5/100`, Adv) |
| 15 (çöküş eşiği), 80 (tavan), 75 (tavan eksi 5) | raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | §4; §3 |
| 17,79 | logs/konsey_zincir.log | satır 77 (`KUYRUK TAMAM; toplam egitim 17.79 sa`) |
| 38,15 | logs/konsey_zincir.log | satır 77 (`pay 38.15 sa`); ÖK Dondurma eki (e) |
| 20,47 | raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | Dondurma eki (d), `W_sa.80` |
| 125,8; 142,7; 142,5 | raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | Dondurma eki (d), `t_V_at_epok_s`, `t_R224_IN_at_epok_s`, `t_R224_scr_at_epok_s` |
| 148,1; 195,8; 312,5; 266,6; 182,9; 149,7 | results/q1/konsey_b3_defter.tsv | TR: AT satırlarında sure_s / epok (satır 4: 5628/38; satır 10: 7050/36; satır 12: 13126/42; satır 16: 12530/47; satır 20: 6766/37; satır 23: 8685/58); `arsiv/b2_yardimci/_rapor_duzelt_dogrula.py` |
| 1,18; 1,37; 2,19; 2,12; 1,28; 1,05 | results/q1/konsey_b3_defter.tsv; raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | TR: yukarıdaki epok süresi / pilot epok süresi (V_IN 125,8; R224_IN 142,7; R224_scr 142,5; Dondurma eki (d)); `_rapor_duzelt_dogrula.py` |
| 1,05-2,19 (kat) | results/q1/konsey_b3_defter.tsv | TR: yukarıdaki altı katsayının en küçüğü (R224_scr_s1202) ve en büyüğü (R224_scr_s1201) |
| 11045 MiB, %100 | logs/konsey_b3/nvidia_smi_df.log | satır 103; results/q1/konsey_b3_defter.tsv satır 10 |
| 10886 MiB, %100; python3.12 | logs/konsey_b3/nvidia_smi_df.log | satır 195 ve 204; defter satır 18 |
| 10882 MiB, %89 | logs/konsey_b3/nvidia_smi_df.log | satır 218 ve 227; defter satır 20 |
| 10882-11045 MiB, %89-100 | logs/konsey_b3/nvidia_smi_df.log | satır 103, 195, 218 (en küçük ve en büyük) |
| 3953 MiB, %0 | logs/konsey_b3/nvidia_smi_df.log | satır 126 (R224_scr_s1201 AT başı); defter satır 12 |
| 3964 MiB, %0 | logs/konsey_b3/nvidia_smi_df.log | satır 172 (V_IN_s2102 AT başı); defter satır 16 |
| 04:51:10; 14:03:24; 14:22:02 | results/q1/konsey_b3_defter.tsv | satır 8, 16, 18 (`bitis`) |
| 04:51:12; 14:03:25; 14:22:03 | logs/konsey_b3/nvidia_smi_df.log | satır 94, 186, 209 (anlık görüntü saati) |
| 1-2 s | results/q1/konsey_b3_defter.tsv; logs/konsey_b3/nvidia_smi_df.log | TR: anlık görüntü saati − önceki aşamanın bitişi (2, 1, 1 s) |
| PID 1 (`/python3.12`); süreç yok | logs/konsey_b3/nvidia_smi_df.log | satır 204 ve 227; satır 112 (`No running processes found`) |
| −0,087; [−0,116; −0,058] (%95); −0,110 (%90 alt sınır) | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_logit.H3.kestirim, .ci95, .ci90[0] |
| −4,13; [−4,90; −3,37] (%90); [−5,11; −3,16] (%95) | results/q1/konsey_ayrisim_b4.json | b4.duyarlilik.yari_oran.H3.kestirim, .ci90, .ci95 |
| df 3 (S1, birleşik varyans) | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S1.sigma.df |
| df 1,02 (S1, Welch) | results/q1/konsey_ayrisim_b4.json | b4.ikincil.S1.sigma.welch.df |
| DF 5, 11, 13, 17, 21, 24; ZL 46, 56, 59, 65, 71, 76 (`tavanda_durdu=False`) | results/q1/konsey_b3_defter.tsv; logs/konsey_zincir.log | `at_ozet` satırları; `OZET` satırları |
| 0,10 (δ), 0,06 (δ duyarlılığı), 0,5 (B5 eşiği), 0,75 ve 0,30 (öngörülen büyüklükler) | raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | §5 |
| 0,044 ve 1,354 | raporlar/konsey_2026-10-29/ON_KAYIT_2026-10-29.md | §5, önceden kesinlik planı |

## Doğrulayıcı ile uyuşmazlık

Doğrulayıcının yedi bulgusunun yedisi de rapora işlenmiştir; birinci bulgunun ayrıntısında üç noktada kaynakla uyuşmayan ifade bulunduğundan rapor bu noktalarda doğrulayıcının önerdiği metinden ayrılmıştır.

Doğrulayıcı makale beyanı için "epok süreleri pilotun 1,2-2,2 katıdır" ifadesini önermiştir. Defterden yeniden hesaplanan altı katsayının en küçüğü R224_scr_s1202'ye aittir ve 8685/58 = 149,7 s ile pilotun 142,5 s'lik değerine oranla 1,05'tir (`results/q1/konsey_b3_defter.tsv` satır 23; ÖK Dondurma eki (d)). Doğrulayıcının kendi listesindeki 149,7 s de aynı sonucu verir. Raporda bu nedenle 1,05-2,19 aralığı yazılmıştır.

Doğrulayıcı R224_IN_s1301'i paylaşım görünen tek AT aşaması olarak anmıştır. R224_IN_s1302 AT aşamasının başında da 10882 MiB bellek ve %89 kullanım kayıtlıdır (`logs/konsey_b3/nvidia_smi_df.log` satır 218; defter satır 20); bu aşama pilotun 1,28 katı sürmüştür. Dolu görünen üç anlık görüntünün ikisi bu yüzden AT aşamalarına aittir. Bu fark doğrulayıcının vardığı sonucu değiştirmez, çünkü en yavaş iki AT aşamasının başında yük görünmemektedir.

Doğrulayıcı makale beyanını "GPU zaman zaman paylaşılmıştır" düzeyinde önermiştir. Doğrulayıcının da işaret ettiği gibi dolu görünen anlık görüntüler bir önceki aşamanın bitişinden 1-2 s sonra alınmıştır ve görünen `/python3.12` sürecinin konteynerin kendi süreci olması dışlanamaz (NV satır 94, 186, 204, 209, 227; defter satır 8, 16, 18). Kayıtlar paylaşımı kanıtlamadığından raporda "GPU aşama başı kayıtlarında zaman zaman dolu görünmüştür" ifadesi kullanılmıştır.
