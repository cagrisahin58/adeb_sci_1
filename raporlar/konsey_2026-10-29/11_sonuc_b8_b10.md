Doğrulama: 31.10.2026, doğrulayıcı kararı KABUL (560 sayı doğrulandı, 0 yanlış), 9 bulgu işlendi.

# B8-B10 ek ön kayıtlı sonuç raporu (31.10.2026)

Bu rapor deney sonuç analisti (opus alt ajan) tarafından hazırlanmış olup dondurulmuş ek ön kaydın (`raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md`, bundan sonra EK; commit 7325419) B8, B9 ve B10 bloklarını EK §4-§6 ile §11'deki karar kurallarına ve önceden yazılmış cümlelere göre okur. Çözümleme betiklerinin hiçbiri yeniden koşulmamış, 31.10.2026'da `scripts/ek_zincir_komutlari.sh` zincirinin ürettiği JSON çıktıları okunmuştur. Ham çıktılardan yapılan yeniden hesaplar iki türdür. Birincisi B8 ve B9 köşegenlerinden temiz ve PGD-10 doğruluklarının bağımsız hesabıdır (`arsiv/b2_yardimci/_ek_rapor_kosegen.py`, konteynerde). İkincisi B10'un ham ve ana etki artıklı Spearman istatistiklerinin Mantel dosyalarındaki matrislerden bağımsız yeniden hesabıdır (`arsiv/b2_yardimci/_ek_rapor_b10_yeniden.py`, konteynerde); üç veri kümesinde de altı istatistik altı basamağa kadar aynı çıkmıştır. Aynı betik ön kayıt dışı birkaç keşifsel hesabı da yapar ve bunlar yalnız §7'de, "keşifsel" başlığı altında kullanılmıştır. Öteki salt okur yardımcılar `_ek_rapor_anahtar.py`, `_ek_rapor_al.py`, `_ek_rapor_model_tablosu.py`, `_ek_rapor_b9_karsilastir.py`, `_ek_rapor_b10.py`, `_ek_rapor_r18.py`, `_ek_rapor_ozetler.sh` ve `_ek_rapor_v2say.sh` dosyalarıdır (hepsi `arsiv/b2_yardimci/` altında). Hiçbir sonuç dosyası değiştirilmemiştir.

Metinde kaynaklar aşağıdaki kısaltmalarla anılır; tam yollar sondaki sayı kaynak dizinindedir.

| Kısaltma | Dosya |
|---|---|
| J9 | `results/q1/konsey_b9_c100/b9_dondurulmus_b2.json` (B9'un bağlayıcı çıktısı) |
| J9S | `results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json` |
| J2 | `results/q1/konsey_ayrisim_b2.json` (CIFAR-10 B2) |
| J4 | `results/q1/konsey_ayrisim_b4.json` (CIFAR-10 2x2) |
| J8 | `results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json` |
| B8B | `results/q1/konsey_b8_imagenetv2/b8_betimsel.json` |
| OD | `results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json` |
| MF | `results/q1/konsey_b8_imagenetv2/denetim/imagenetv2_manifest.json` |
| MC10, MC100, MIN | `results/q1/konsey_b10_gradyan/mantel_cifar10.json`, `mantel_cifar100.json`, `mantel_imagenetv2.json` |
| A10 | `results/q1/konsey_b10_gradyan/b10_aile.json` |
| KO10, KO100, KOIN | `results/q1/konsey_b10_gradyan/{cifar10,cifar100,imagenetv2}/kosinus_ozet.json` |
| Z1, Z2 | `results/q1/ek_loglar/ek_zincir_1.log`, `ek_zincir_2.log` (satır numarasıyla) |
| DL | `results/q1/ek_loglar/b8_denetim.log` |
| RG | `results/q1/ek_regresyon/gpu_n200/karsilastirma_ozgun_catal.json` ve `karsilastirma_ozgun_onb_catal_onb.json` |
| KS | `per_sample_<m>_to_<m>.npz` köşegen dosyaları üzerinde `_ek_rapor_kosegen.py` çıktısı (B8 ve B9 matris klasörleri) |
| KY | Mantel ve kosinüs dosyaları üzerinde `_ek_rapor_b10_yeniden.py` çıktısı |
| HT8, HT9 | `raporlar/konsey_2026-10-29/hucre_tablosu_b8.json`, `hucre_tablosu_b9.json` |
| SK | `raporlar/konsey_2026-10-29/_ek_sure_kestirimi.json` |
| TR | yukarıdaki dosyaların anahtarlarından aritmetik türetme, formül dizinde |

## 0. Bütünlük denetimi ve sınama eşlemesi

Dondurulmuş çözümleme betiğinin (`experiments/q1_konsey_ayrisim.py`) bugünkü SHA-256 özeti `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`, iki yeni hücre tablosununki `4afa5fbc3f661632cf3e08c66ce56064fbde01424c352b2ab66a482d390a388d` (HT8) ve `be778f4286289a744b88a052d234a4fbf93c616e125b5977b2f38a2f40dde3bd` (HT9) olup EK Dondurma eki (a) ve (b) ile, ayrıca J9 ve J8'in `meta.betik_sha256` ve `meta.hucre_tablosu_sha256` alanlarıyla aynıdır (`_ek_rapor_ozetler.sh`). EK gövdesinin Dondurma eki (d) tanımıyla yeniden hesaplanan özeti `76d05f111371230495c95b757e46dccdb84123264034cc8432cb0a31403df595`'tir ve ekteki değerle örtüşür. Özgün matris betiğinin özeti `f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7`'dir; zincirin bekçisi bu özeti her adımdan önce denetlemiş, B9 sarmalayıcısı da aynı değeri `meta.ozgun_matris_betigi_sha256_simdi` alanına yazmıştır (J9S). Üç yeni betiğin bugünkü özetleri (`q1_ek_transfer_matrix.py` `edec356a...`, `q1_ek_ayrisim.py` `d264c4e5...`, `q1_ek_gradyan_kosinus.py` `c82a66d1...`) `results/q1_research/ONKAYIT_SAPMALAR.md` dosyasındaki kod ekiyle aynıdır ve koşu çıktılarındaki `ek_betik_sha256` (B8 `transfer_matrix.json`), `meta.sarmalayici_sha256` (J9S, B8B, A10) ve `betik_sha256` (KO10, KO100, KOIN, MC10, MC100, MIN) alanlarında da aynı değerler bulunmaktadır. EK §3 ve §12'deki ölçütle B9, B8 ve B10 çözümlemeleri ön kayıtlı çözümleme sayılır. B9'da birincil panelin yedi üyesi, B8'de altı üyesi yüklenmiş (`panel.birincil_eksik` boş), hücre çakışması çıkmamış (`veri.cakismalar` boş), hedef maskeleri tutarlıdır (`veri.tutarlilik.hedef_maskesi_tutarli` = true; J9, J8, B8B).

Rapor yazılmadan önce JSON anahtarları listelenmiş ve EK'teki sınama adlarıyla eşlenmiştir.

| EK sınaması ya da çözümlemesi | EK yeri | JSON anahtarı | Durum |
|---|---|---|---|
| K-a(B9), K-b(B9), K-c(B9) | §4.2 | J9 `b2.F_B2.K-a`, `.K-b`, `.K-c`, `p_ham`, `p_holm`, `karar` | bulundu |
| F_B9, δ = 0,06 duyarlılığı | §4.2 | J9 `b2.F_B2.duyarlilik_delta_0.06` | bulundu |
| S9-1 ikincil panel | §4.4 | J9 `b2.duyarlilik.ikincil_panel` | bulundu |
| S9-2 r'nin Hodge ayrışımı ve potansiyel payı | §4.4 | yok | bulunamadı (B9 için üretilmemiş) |
| S9-3 tam örneklem, logit, oran, panel jackknife | §4.4 | J9 `b2.duyarlilik.{tam_log, yari_logit, yari_oran, panel_jackknife}` | bulundu |
| S9-4 her-ikisi-doğru koşullama protokolü | §4.4 | yok | bulunamadı |
| S9-5 XCiT ile Hendrycks2019Using | §4.4 | J9 `b2.model_tablosu.<takma ad>.yari_log` | bulundu |
| B9 temiz doğruluk yan bilgisi | §9 | J9S `temiz_dogruluk_yuzde` | bulundu |
| Ā^σ_IN (iki Singh çifti) | §5.6 | B8B `A_sigma_IN` | bulundu |
| A^σ_scr,Liu | §5.6 | B8B `A_sigma_scr_Liu` | bulundu |
| B8 K-a, K-b, K-c (betimsel) | §5.6 | J8 `b2.F_B2` | bulundu |
| ρ ayrı ayrı (Singh, Liu Swin-B, Mo) | §5.6 | B8B `donusturucu_rho_ayri_ayri` | bulundu |
| S8-1 çift başına aralıklar | §5.7 | B8B `ciftler[k].goruntu_bootstrap_ci90/ci95` (yalnız A^σ_k) | A^σ_k için bulundu; D_k ve q_k aralıkları bulunamadı |
| S8-2 Hodge ve potansiyel payı | §5.7 | B8B `hodge_r_kesifsel` | bulundu |
| S8-3 tam, logit, oran, δ, panel jackknife | §5.7 | J8 `b2.duyarlilik`, `b2.F_B2.duyarlilik_delta_0.06` | bulundu; grup (Salman) bırakmalı jackknife bulunamadı |
| S8-4 işaretliler çıkarılarak Ā^σ_IN | §5.7 | OD `isaretli` boş | uygulanmadı, işaretli model yok |
| S8-5, S8-6 | §5.7 | B8B `model_tablosu_ozet`, `hodge_r_kesifsel.r_matrisi` | türetilebilir (TR) |
| S8-7 dört koşullama protokolü | §5.7 | yok | bulunamadı |
| S8-8 w ile RobustBench AA yan yana | §5.7 | B8B `model_tablosu_ozet.<m>.w_yuzde` (AA yok) | tablo üretilmemiş |
| H10-d, H10k-d (F_B10) | §6.2-§6.3 | A10 `F_B10.sinamalar[0..5]`; MC10, MC100, MIN `sinamalar.ham`, `.ana_etki_artik` | bulundu |
| kismi_omega, kismi_omega_gradnorm | §6.2 (aile dışı) | A10 `kesifsel_kismi_omega`, `kesifsel_kismi_omega_gradnorm` | bulundu |
| Her-ikisi-doğru c_ij duyarlılığı | §6.1 | KO `c_iki_model_dogru` var; Mantel çıktısı yok (`c_turu` = "tum") | Mantel sınaması bulunamadı; §7'de keşifsel yeniden hesap |
| S10-1 ile S10-7 | §6.4 | yok | bulunamadı (S10-3'ün kodu yazılmamıştır; S10-2 §7'de keşifsel hesaplandı) |

## 1. Yönetici özeti

B9'da, yani ana ön kaydın B2 sınamalarının CIFAR-100 panelinde bağlayıcı yinelemesinde, üç sınamanın ikisi destek almış, biri çürütülmüştür (J9 `b2.F_B2.karar`). ResNet-18 ile ViT-Tiny arasındaki panel kaynak açığının simetrik oranı üç tohum ortalamasında 0,840'tır (%90 aralık 0,795 ile 0,885; Holm sonrası p = 2,05e-03; J9 `b2.F_B2.K-a.sinama.ort`, `.ci90`, `b2.F_B2.p_holm[0]`) ve her tohumda 0,75'in üzerindedir; ViT tohumlarının birbirine panelden daha çok benzediğini ölçen Δ_w 0,519'dur (%90 aralık 0,469 ile 0,599; Holm sonrası p = 1,50e-03; J9 `b2.F_B2.K-c.Delta_w`, `.bootstrap.ci90`, `b2.F_B2.p_holm[2]`). Buna karşılık ViT'nin yönlü terimi CIFAR-100'de küçük değildir: ρ(V-scr) üç tohum ortalamasında 0,143'tür, %95 aralığı (0,082 ile 0,203) sıfırı dışlar ve kestirim ±0,10 sınırını aşar, dolayısıyla K-b(B9) EK §8'deki ölçütle çürütülmüştür (J9 `b2.F_B2.K-b.ort`, `.ci95`; `karar.K-b` = "curutuldu (pozitif yon)"). EK §11'e göre metne iki önceden yazılmış cümle girer: "ViT'nin kaynak açığının simetrik payla taşınması ve ViT tohumlarının birbirine panelden çok benzemesi CIFAR-100'de üç tohumla yinelenir" ve "Yönlü terim veri kümesine bağlıdır (CIFAR-100'de büyük, SVHN'de ters işaretli); 'küçük yönlü terim' cümlesi CIFAR-10 ile sınırlanır". K-b(B9) birincil log ölçekte çürütülmüştür; ön kayıtlı logit duyarlılığında ρ(V-scr) −0,413'tür (%95 aralık −0,609 ile −0,217; J9 `b2.duyarlilik.yari_logit.rho_V.ort`, `.ci95`), yani yönlü terim iki ölçekte de δ'nın dışındadır ve yalnız işareti ölçeğe bağlıdır. ÖK §5 gereği bu duyarlılık kararı değiştirmez. EK §11 gereği ek bloklar ana ön kaydın O1 sonuç bölgesini değiştirmez.

B8, yani ImageNetV2 paneli, EK §5.6 gereği betimsel ve keşifseldir; Holm ailesi ve bağlayıcı karar yoktur ve bu bölümdeki hiçbir sayı "destek" ya da "çürütüldü" diye okunamaz. Temiz modelden başlatılmış ve aynı tarifle eğitilmiş iki Singh çiftinde dönüştürücünün CNN paneline benzerliği CNN eşininkinden düşüktür: Ā^σ_IN = −0,142'dir (görüntü bootstrap %90 aralığı −0,197 ile −0,090; çiftler −0,167 ve −0,118; B8B `A_sigma_IN.kestirim`, `.goruntu_bootstrap.ci90`, `.cift_degerleri`) ve EK §5.6'daki sıralı etiket kuralı "beklentiyle uyumlu" etiketini verir (B8B `A_sigma_IN.betimsel_etiket`). Dolaylı kanıtla sıfırdan eğitilmiş tek Liu çiftinde ise A^σ_scr,Liu = −0,055'tir (%90 aralık −0,137 ile 0,022), H1'in öngörülen büyüklüğünden (≤ −0,20) uzaktır ve etiket "belirsiz"dir (B8B `A_sigma_scr_Liu`). B10'da F_B10 ailesinin altı sınamasının altısı da destek almıştır: girdi gradyanı kosinüsü c_ij ile log τ̄ arasındaki Spearman korelasyonu ham olarak CIFAR-10'da 0,943, CIFAR-100'de 0,981, ImageNetV2'de 0,694, model ana etkileri ayıklandıktan sonra sırasıyla 0,944, 0,912 ve 0,893'tür; altı sınamada da 9999 permütasyonun hiçbiri gözlenen değere ulaşmamış (p = 1e-04, mümkün en küçük değer) ve Holm sonrası p 6,0e-04 olmuştur (A10 `F_B10.sinamalar[0..5]`). EK §11'in "en az iki veri kümesinde H10k destek ve hiçbir H10k çürütülmedi" satırı tetiklenmiştir. Raporun en önemli üç sayısı şunlardır: CIFAR-100'de ρ(V-scr) = 0,143 (K-b çürütüldü; J9 `b2.F_B2.K-b.ort`), ImageNetV2'de Ā^σ_IN = −0,142 (betimsel; B8B `A_sigma_IN.kestirim`), ana etki artıklı gradyan hizalanması korelasyonu 0,893 ile 0,944 arası, Holm sonrası p = 6,0e-04 (A10 `F_B10.sinamalar[1,3,5].istatistik`, `.p_holm`).

## 2. Ön koşullar

EK §3'ün istediği GPU çatal regresyonu ilk adım olarak koşulmuş ve iki karşılaştırmada da birebir çıkmıştır. Önbelleksiz karşılaştırmada 9 hücre ve 9 npz dosyasında, önbellekli karşılaştırmada yine 9 hücre ve 9 npz dosyasında fark yoktur; iki dosyada da `json_farkli_hucreler`, `npz_farklari` ve `ust_alan_farklari` boştur ve `BIREBIR` alanı true'dur (RG). Önbellekli koşunun üç önbellek dosyası bayt düzeyinde aynıdır (Z1 satır 15-17, `ayni ...npy`). Regresyon sırasında özgün betiğin ve çatalın özetleri kod ekiyle aynıdır (Z1 satır 3-4). Özgün betik ile çatalın koşu süreleri önbelleksiz 24 ve 24 s, önbellekli 22 ve 23 s'dir (Z1 satır 5-6, 10-11).

B8 ön işleme denetimi (B8-0, EK §5.5) B8 matrisinden önce ve T görülmeden yapılmıştır. On beş modelin (on dört panel üyesi ve yedek IN_Wong2020Fast) on beşi de kuralı geçmiştir; `kalan` ve `isaretli` listeleri boştur (OD). Kural (i) kendi hatla temiz doğruluğun en az %25 ve RobustBench temiz doğruluğunun 0,6 katı olmasını ister. En düşük kendi hat doğruluğu IN_Salman2020Do_R18'dedir (41,55; eşik 31,752; OD `modeller.IN_Salman2020Do_R18.temiz_dogruluk_kendi`, `.esik.esik_i`), en dar pay ise yine bu modeldedir (9,80 puan; TR). Kural (ii) ortak hat ile kendi hat arasındaki mutlak farkın en çok 5 puan olmasını ister. En büyük mutlak fark yedek IN_Wong2020Fast'te 1,20 puan, panel üyeleri arasında IN_Mo_ViT-B'de 0,95 puandır (OD `.esik.mutlak_fark_puan`); 3 ile 5 puan arasında işaretlenen model yoktur (`.esik.isaretli_3_5` = false). Kendi hattı ortak hatla aynı olan altı Singh ve Liu modelinde fark sıfırdır. Kararların aynı olduğu ve RobustBench değerlerinin bağımsız olarak denetlendiği `10_konteyner_yeniden_kurulum.md` §6'da kayıtlıdır. Bu raporda EK §5.1'in seçim öncesi denetimi de bağımsız olarak yinelenmiştir: ImageNetV2 klasöründe 1000 sınıf klasörü vardır ve her birinde 10 dosya bulunmaktadır; manifestte 1000 sınıfın her birinden 2 dosya alınmıştır (`_ek_rapor_v2say.sh`; MF `dosyalar`). Bu denetimin sonucu manifest dosyasına yazılmamıştır (§6, madde 6).

Seçilen 2000 görüntülük listenin özeti denetim koşusunda ve B8 matris koşusunda aynıdır: iki manifestte de `liste_sha256` = `25db498ba8b2c710618e76e8a2dfe5492c9f75be0be1b7f63c253acc4f27d1a8`'dir (Z2 satır 6-7; MF ve `results/q1/konsey_b8_imagenetv2/matris/imagenetv2_manifest.json`). İki manifestin dosya listeleri de alan alan aynıdır. Aynı özet B8 matrisinin `transfer_matrix.json` dosyasındaki `manifest_liste_sha256` alanında ve B10 ImageNetV2 kosinüs özetindeki `imagenetv2_liste_sha256` alanında da bulunmaktadır (KS; KOIN). B8 matrisi EK §5.2'deki saldırıyla koşulmuştur: ε = 4/255, α = 1/255, 10 adım, tohum 42, n = 2000, ortak hat `BicubicRes256Crop224`, float32 önbellek (`cells_meta.json`; `transfer_matrix.json` `eps_255`, `alpha_255`, `cache_f16` = false). B9 matrisi özgün betikle, CIFAR-100, n = 10000, ε = 8/255, α = 2/255 ile koşulmuştur (`results/q1/konsey_b9_c100/matris/cells_meta.json`).

Koşu süreleri zincir günlüklerinden alınmıştır. Regresyon 06:58:56-07:00:31 (1 dk 35 s), ön işleme denetimi 07:00:31-07:07:58 (7 dk 27 s), B9 matrisi 07:08:49-07:22:42 (13 dk 53 s), B8 matrisi 07:22:42-07:38:55 (16 dk 13 s), B10 gradyanları 07:38:55-07:43:46 (4 dk 51 s), çözümleme 07:43:46-07:44:09 (23 s) sürmüştür (Z1 satır 1, 19, 23; Z2 satır 1, 3, 8, 12, 22; TR). Bu süreler kestirimin altındadır: B9 için kestirim 28,5 ile 36,1 dk (SK `B9_n10000.dk_hiz_a`, `.dk_hiz_b`), B8 için n = 1000 kestiriminin (11,5 ile 14,6 dk; SK `B8_n1000`) n = 2000'e doğrusal ölçeklenmesi 23,0 ile 29,2 dk'dır (TR). Zincir başladığında GPU'da 2804 MiB bellek kullanılmaktaydı (Z1 satır 2); bu, konteyner dışındaki bir sürecin GPU'yu paylaştığını gösterir (§6, madde 5).

## 3. B9: CIFAR-100 paneli (aile F_B9, Holm α = 0,05, bağlayıcı)

B9'un çift tanımları ve paneli HT9'dan okunmuştur: "C1-R32" hücresi C1 CIFAR-100 ResNet-18 AT tohumları 1001, 1002, 1003, "V-scr" hücresi C1 CIFAR-100 ViT-Tiny AT tohumları 2001, 2002, 2003'tür; tohum çiftleri (1001, 2001), (1002, 2002), (1003, 2003)'tür (J9 `b2.hucreler`, `b2.tohum_ciftleri`). Birincil panel yedi CNN'den, ikincil panel Debenedetti2022Light_XCiT-S12 ve Hendrycks2019Using'den oluşur (J9 `panel`).

| Sınama | Ön kayıtlı öngörü ve ölçüt | Gözlenen | Aralık | Ham p | Holm p | Karar | Öngörülen büyüklük |
|---|---|---|---|---|---|---|---|
| K-a(B9) | q_s ≥ 0,75; H0: ort q ≤ 0,50, tek yönlü t (df 2); çürütme: %90 üst sınır < 0,50; payda kuralı D_s ≤ 0,10 | ort q = 0,840 (q_s: 0,848; 0,861; 0,810) | %90 [0,795; 0,885], %95 [0,773; 0,906] | 1,02e-03 | 2,05e-03 | destek | tuttu (her tohumda q_s ≥ 0,75) |
| K-b(B9) | \|ρ(V-scr)\| < 0,10; TOST ±0,10; çürütme: %95 aralık sıfırı dışlar ve \|kestirim\| > 0,10 | ort ρ = 0,143 (0,134; 0,123; 0,170) | %90 [0,101; 0,184], %95 [0,082; 0,203] | TOST 0,953 | 0,953 | çürütüldü (pozitif yön) | ham %90 aralık ±0,10 dışında |
| K-c(B9) | Δ_w ≥ +0,30; H0: Δ_w ≤ 0, hiyerarşik bootstrap; çürütme (önce): %90 üst sınır < +0,10 | Δ_w = 0,519 | bootstrap %90 [0,469; 0,599], %95 [0,463; 0,604] | 5,00e-04 | 1,50e-03 | destek | tuttu (Δ_w ≥ 0,30) |

Tablodaki değerler J9'un şu anahtarlarından alınmıştır: K-a satırı `b2.F_B2.K-a.q`, `.sinama.ort`, `.sinama.ci90`, `.sinama.ci95` ve `.p_tek_H0_q_le_0.5`; K-b satırı `b2.F_B2.K-b.degerler`, `.ort`, `.ci90`, `.ci95` ve `.tost_p`; K-c satırı `b2.F_B2.K-c.Delta_w`, `.bootstrap.ci90`, `.bootstrap.ci95` ve `.p_tek_H0_Delta_le_0`. Holm değerleri `b2.F_B2.p_holm`, kararlar `b2.F_B2.karar` alanındadır; hesaplanamayıp p = 1 sayılan sınama yoktur (`p_1_sayilan_hesaplanamayan` boş). Kararlar EK §2'deki ilkeyle, yani destek Holm sonrası p ile, çürütme ham aralıkla okunmuştur. K-b'de TOST'un iki tek yönlü p'sinden alt sınır p'si 1,69e-03, üst sınır p'si 0,953'tür (`.tost_p_alt`, `.tost_p_ust`); eşdeğerliği taşıyan büyük p üst sınırdan gelir, yani kestirim +0,10 sınırının üzerine taşmaktadır. EK §4.3, K-b(B9) için gerçekçi sonuçları önceden "çürütüldü" ya da "kararsız" diye yazmıştı; gözlenen sonuç bu iki seçenekten ilkidir. Çürütme koşulu dondurulmuş betiğin `b2_karar` işlevinde mutlak değerle denetlenmektedir (`(ci95[0] > 0 or ci95[1] < 0) and abs(ort) > delta`) ve EK §8'deki tanımla örtüşmektedir.

K-a'nın payda kuralı tetiklenmemiştir: üç tohumda D_s 0,388; 0,459 ve 0,448'dir (J9 `b2.F_B2.K-a.D`; `payda_kucuk_tohumlar` boş). Açığın simetrik payı 0,329; 0,395 ve 0,363, yönlü payı 0,059; 0,064 ve 0,085'tir (`.simetrik_pay`, `.yonlu_pay`); ayrışım özdeşliğinin en büyük sayısal artığı 7,8e-16'dır (`.ozdeslik_artik_max`). K-c'de çürütme koşulu önce denetlenmiş ve tutmamıştır (%90 üst sınır 0,599 > 0,10); bootstrap 2000 kopyada 284 tek tohumlu örneği yeniden çekmiştir (`b2.F_B2.K-c.bootstrap.yeniden_cekilen_tek_tohumlu_ornek`). ViT tohum çiftlerinin tür içi log τ̄ değerleri −0,417, −0,514 ve −0,529, ViT tohumlarının panel benzerliği σ ise −0,971, −1,031 ve −1,015'tir (`.log_tau_tur_ici`, `.sigma_V`). δ = 0,06 duyarlılığında bütün kararlar aynı kalmış, K-b'nin Holm sonrası TOST p değeri 0,986 olmuştur (`b2.F_B2.duyarlilik_delta_0.06.p_holm[1]`, `.karar`).

Aynı betiğin CIFAR-10'daki B2 çıktısı (J2) ile yan yana karşılaştırma aşağıdadır. CIFAR-10 değerleri `09_sonuc_b2_b6.md` raporundan değil, doğrudan J2'nin aynı anahtarlarından okunmuştur.

| Nicelik | CIFAR-10 B2 (J2) | CIFAR-100 B9 (J9) | Anahtar |
|---|---|---|---|
| ort q (K-a) | 0,936 [0,925; 0,948] | 0,840 [0,795; 0,885] | `b2.F_B2.K-a.sinama.ort`, `.ci90` |
| q_s | 0,940; 0,928; 0,940 | 0,848; 0,861; 0,810 | `b2.F_B2.K-a.q` |
| D_s | 0,391; 0,387; 0,390 | 0,388; 0,459; 0,448 | `b2.F_B2.K-a.D` |
| simetrik pay | 0,368; 0,360; 0,367 | 0,329; 0,395; 0,363 | `b2.F_B2.K-a.simetrik_pay` |
| yönlü pay | 0,023; 0,028; 0,023 | 0,059; 0,064; 0,085 | `b2.F_B2.K-a.yonlu_pay` |
| ort ρ(V-scr) (K-b) | 0,012 [−0,007; 0,031] | 0,143 [0,101; 0,184] | `b2.F_B2.K-b.ort`, `.ci90` |
| K-b %95 aralık | [−0,016; 0,040] | [0,082; 0,203] | `b2.F_B2.K-b.ci95` |
| Δ_w (K-c) | 0,566 [0,537; 0,604] | 0,519 [0,469; 0,599] | `b2.F_B2.K-c.Delta_w`, `.bootstrap.ci90` |
| Ham p (K-a; K-b; K-c) | 4,19e-05; 2,73e-03; 5,00e-04 | 1,02e-03; 0,953; 5,00e-04 | `b2.F_B2.p_ham` |
| Holm p (K-a; K-b; K-c) | 1,26e-04; 2,73e-03; 1,00e-03 | 2,05e-03; 0,953; 1,50e-03 | `b2.F_B2.p_holm` |
| Kararlar | destek; destek; destek | destek; çürütüldü (pozitif yön); destek | `b2.F_B2.karar` |
| ρ(V-scr) logit ölçek | −0,304 | −0,413 [%95 −0,609; −0,217] | `b2.duyarlilik.yari_logit.rho_V.ort`, `.ci95` |
| ρ(V-scr) oran ölçeği (puan) | −14,66 | −14,61 | `b2.duyarlilik.yari_oran.rho_V.ort` |
| ort q logit; oran | 1,101; 1,542 | 1,026; 1,216 | `b2.duyarlilik.yari_logit.q_ort`, `yari_oran.q_ort` |
| ikincil panel q | 0,899; 0,825; 0,842 | 0,799; 0,834; 0,771 | `b2.duyarlilik.ikincil_panel.q` |
| ikincil panel ρ(V-scr) | 0,198; 0,202; 0,204 | 0,129; 0,136; 0,221 | `b2.duyarlilik.ikincil_panel.rho_V` |
| ViT tür içi log τ̄ | −0,453; −0,466; −0,410 | −0,417; −0,514; −0,529 | `b2.F_B2.K-c.log_tau_tur_ici` |
| ResNet tür içi log τ̄ | −0,496; −0,494; −0,476 | −0,468; −0,520; −0,514 | `b2.tur_ici_resnet_log_tau` |
| σ_V (ViT tohumları) | −1,015; −1,000; −1,011 | −0,971; −1,031; −1,015 | `b2.F_B2.K-c.sigma_V` |

EK §4.4'teki ön kayıtlı keşifsel çözümlemelerden üretilmiş olanlar şunlardır. Tam örneklemde ort q 0,840, ort ρ(V-scr) 0,143'tür (`b2.duyarlilik.tam_log.q_ort`, `.rho_V.ort`), yani bölünmüş yarı kestirimiyle aynıdır. Panel üyesi bırakmalı jackknife'ta ort q 0,831 (Jia2022LAS-AT_34_10 çıkınca) ile 0,847 (Wang2023Better_WRN-28-10 çıkınca), ort ρ(V-scr) 0,127 (Wang2023Better_WRN-28-10 çıkınca) ile 0,150 (Rice2020Overfitting çıkınca) arasındadır (`b2.duyarlilik.panel_jackknife.*`); hiçbir üyenin çıkarılması ρ'yu 0,10'un altına indirmemektedir. İki ImageNet ön eğitimli üyeden oluşan ikincil panelde (S9-1) q her tohumda 0,75'in üzerinde kalmakta, ρ(V-scr) 0,129 ile 0,221 arasında yer almaktadır. S9-5 için tek modellik karşılaştırma şöyledir: XCiT-S12'nin σ'sı −0,489, ρ'su 0,000; Hendrycks2019Using'in σ'sı −0,567, ρ'su 0,009'dur (J9 `b2.model_tablosu.C100_Debenedetti2022Light_XCiT-S12.yari_log`, `C100_Hendrycks2019Using.yari_log`). İki model de C1 ViT-Tiny'den (σ −0,971 ile −1,031) panele çok daha yakındır ve aralarındaki fark (0,078; TR) "dönüştürücü mü, ön eğitim mi" sorusuna yalnız kaba bir işaret verir. S9-2 ve S9-4'ün çıktısı bulunamamıştır.

B9 matrisindeki model düzeyi nicelikler aşağıdadır. Temiz doğruluk, PGD-10 doğruluğu (temiz doğru ve saldırı sonrası doğru görüntülerin oranı) ve w köşegen npz dosyalarından bağımsız olarak yeniden hesaplanmış (KS), temiz doğruluk ve w değerleri `transfer_matrix.json`'daki `target_clean_acc` ve `cond_fooling` alanlarıyla ve exp(ω) ile birebir aynı çıkmıştır. σ ve ρ J9 `b2.model_tablosu.<m>.yari_log` alanından alınmıştır.

| Model | Hücre (HT9) | Temiz (%) | PGD-10 doğru (%) | w (%) | σ | ρ |
|---|---|---|---|---|---|---|
| C100_ResNet18_AT_s1001 | C1-R32 | 64,23 | 19,16 | 70,17 | −0,642 | 0,016 |
| C100_ResNet18_AT_s1002 | C1-R32 | 64,65 | 19,17 | 70,35 | −0,636 | −0,004 |
| C100_ResNet18_AT_s1003 | C1-R32 | 62,68 | 19,58 | 68,76 | −0,653 | 0,000 |
| C100_ViT_Tiny_AT_s2001 | V-scr | 41,94 | 11,39 | 72,84 | −0,971 | 0,134 |
| C100_ViT_Tiny_AT_s2002 | V-scr | 43,50 | 10,46 | 75,95 | −1,031 | 0,123 |
| C100_ViT_Tiny_AT_s2003 | V-scr | 44,06 | 11,58 | 73,72 | −1,015 | 0,170 |
| C100_Rice2020Overfitting | panel | 53,82 | 21,85 | 59,40 | −0,670 | 0,024 |
| C100_Rade2021Helper_R18_ddpm | panel | 61,50 | 32,96 | 46,41 | −0,388 | −0,053 |
| C100_Addepalli2022Efficient_RN18 | panel | 65,45 | 34,43 | 47,39 | −0,439 | 0,106 |
| C100_Sehwag2021Proxy | panel | 65,93 | 36,64 | 44,43 | −0,407 | 0,003 |
| C100_Pang2022Robustness_WRN28_10 | panel | 63,64 | 35,61 | 44,04 | −0,396 | −0,033 |
| C100_Wang2023Better_WRN-28-10 | panel | 72,57 | 44,49 | 38,69 | −0,468 | −0,048 |
| C100_Jia2022LAS-AT_34_10 | panel | 64,89 | 37,14 | 42,76 | −0,421 | 0,002 |
| C100_Debenedetti2022Light_XCiT-S12 | ikincil panel | 67,34 | 37,79 | 43,88 | −0,489 | 0,000 |
| C100_Hendrycks2019Using | ikincil panel | 59,22 | 34,12 | 42,38 | −0,567 | 0,009 |

Sarmalayıcının yan dosyası (J9S) temiz doğrulukları `temiz_dogruluk_yuzde` alanında betimsel olarak verir ve değerler yukarıdaki köşegen hesabıyla aynıdır. EK §9'un önceden yazdığı karıştırıcı burada açıkça görülmektedir: ViT-Tiny tohumlarının temiz doğruluğu 41,94 ile 44,06, ResNet-18 tohumlarınınki 62,68 ile 64,65, birincil panel üyelerininki 53,82 ile 72,57 arasındadır (J9S). ViT'nin w'su ve hedef-doğru paydası bu yüzden daha küçük ve farklı bir görüntü alt kümesine dayanır; K-b'deki pozitif yönlü terimin bir kısmı bu farktan gelebilir ve tasarım bu iki açıklamayı ayıramaz. S9-4'ün (her-ikisi-doğru protokolü) üretilmemiş olması bu nedenle önemli bir eksiktir (§6, madde 4).

## 4. B8: ImageNetV2 paneli (betimsel ve keşifsel)

B8'de EK §5.6 ve fable kararı E2 gereği Holm ailesi yoktur ve hiçbir bağlayıcı karar verilmez. Bu bölümdeki bütün nicelikler "IN satırının doğal ölçekte kestirimi" ve keşifsel etiketiyle okunur; dondurulmuş betiğin B8 tablosuyla ürettiği p değerleri, Holm sonuçları ve "kararsiz" gibi karar etiketleri yalnız betimsel sayı olarak aktarılmıştır. Aralıklar görüntü bootstrap'ıdır (B = 2000, tohum 20261030; B8B `meta.bootstrap_B`, `.bootstrap_tohum`) ve yalnız görüntü örneklemi kaynaklı belirsizliği taşır; kontrol noktaları tek eğitimdir.

On dört modelin hücre tablosu ataması, ortak hatta ölçülen temiz ve PGD-10 doğrulukları, w, σ ve ρ değerleri aşağıdadır. Hücre, çift numarası (`tohum` alanı) ve aile HT8'den, satır (IN ya da scr) B8B `ciftler[k].satir` alanından ve HT8 `eslesme_notu`'ndan, temiz doğruluk, PGD-10 ve w köşegen npz dosyalarından (KS; `transfer_matrix.json` ile aynı), σ ve ρ B8B `model_tablosu_ozet.<m>` alanından alınmıştır. Panel üyelerinin σ'sı kendi değerleri panelden çıkarılarak beş üye üzerinden, öteki modellerinki altı üye üzerinden hesaplanmıştır (`panel_n`).

| Model | Hücre etiketi, çift, aile (HT8) | Satır | Temiz (%) | PGD-10 doğru (%) | w (%) | σ | ρ |
|---|---|---|---|---|---|---|---|
| IN_Salman2020Do_R18 | panel, CNN | P8 | 41,35 | 22,90 | 44,62 | −1,070 | 0,202 |
| IN_Salman2020Do_R50 | panel, CNN | P8 | 51,90 | 29,80 | 42,58 | −0,819 | 0,003 |
| IN_Salman2020Do_50_2 | panel, CNN | P8 | 56,75 | 31,30 | 44,85 | −0,895 | −0,120 |
| IN_Engstrom2019Robustness | panel, CNN | P8 | 51,05 | 25,65 | 49,76 | −0,890 | −0,043 |
| IN_Chen2024Data_WRN_50_2 | panel, CNN | P8 | 57,60 | 35,90 | 37,67 | −0,813 | 0,025 |
| IN_Peng2023Robust | panel, CNN | P8 | 60,45 | 40,45 | 33,09 | −1,039 | −0,067 |
| IN_Singh_ConvNeXt-T-CvSt | C1-R32, çift 1, CNN | IN | 60,90 | 39,85 | 34,56 | −0,963 | −0,122 |
| IN_Singh_ViT-S-CvSt | V-scr, çift 1, ViT | IN | 61,00 | 39,90 | 34,59 | −1,130 | −0,211 |
| IN_Singh_ConvNeXt-B-CvSt | C1-R32, çift 2, CNN | IN | 63,20 | 44,05 | 30,30 | −1,118 | −0,298 |
| IN_Singh_ViT-B-CvSt | V-scr, çift 2, ViT | IN | 64,85 | 44,20 | 31,84 | −1,237 | −0,188 |
| IN_Liu_ConvNeXt-B | C1-R32, çift 3, CNN | scr | 65,50 | 45,60 | 30,38 | −1,148 | −0,140 |
| IN_Liu_Swin-B | V-scr, çift 3, Swin | scr | 64,80 | 45,40 | 29,94 | −1,203 | −0,049 |
| IN_Mo_ViT-B | V-scr, 4 (çiftsiz), ViT | IN, çiftsiz | 56,75 | 28,05 | 50,57 | −1,184 | 0,024 |
| IN_Debenedetti_XCiT-S12 | ikincil panel, XCiT | ikincil | 60,35 | 35,60 | 41,01 | −1,112 | −0,194 |

Birincil nicelik olan çift başına A^σ_IN,k ve IN satırı ortalaması aşağıdadır (B8B `ciftler[k]`, `A_sigma_IN`, `A_sigma_scr_Liu`).

| Satır | Çift | A^σ (log) | %90 aralık | %95 aralık | A^σ logit | A^ρ | A^ω (log w) | EK §5.6 beklentisi | Betimsel etiket |
|---|---|---|---|---|---|---|---|---|---|
| IN | 1: ConvNeXt-T-CvSt, ViT-S-CvSt | −0,167 | [−0,234; −0,096] | [−0,246; −0,084] | −0,193 | −0,089 | 0,001 | negatif | - |
| IN | 2: ConvNeXt-B-CvSt, ViT-B-CvSt | −0,118 | [−0,202; −0,038] | [−0,217; −0,023] | −0,147 | 0,110 | 0,050 | negatif | - |
| IN | Ā^σ_IN (1 ve 2) | −0,142 | [−0,197; −0,090] | [−0,207; −0,081] | | | | ≤ −0,10, iki çiftte negatif | beklentiyle uyumlu |
| scr | 3: Liu ConvNeXt-B, Swin-B | −0,055 | [−0,137; 0,022] | [−0,153; 0,034] | −0,061 | 0,091 | −0,015 | ≤ −0,20 | belirsiz |

Ā^σ_IN için EK §5.6'daki sıralı kural aynen uygulanmıştır. %90 aralık (−0,10; 0,10) içinde değildir; nokta kestirimi −0,142 ≤ −0,10'dur, iki çiftte de değer negatiftir (−0,167 ve −0,118) ve %90 aralığın üst sınırı (−0,090) sıfırın altındadır; bu yüzden etiket "beklentiyle uyumlu"dur (B8B `A_sigma_IN.betimsel_etiket`, `.nokta_beklenti_esiginde_ya_da_altinda` = true). İki çiftin farkı 0,048'dir (`A_sigma_IN.iki_cift_farki`); iki çiftle df 1 olduğundan çiftler arası t aralığı kurulmamıştır. EK §11'in bu etikete karşılık gelen önceden yazılmış cümlesi şudur: "ImageNet ölçeğinde, temiz modelden başlatılarak aynı tarifle eğitilmiş iki CNN-dönüştürücü çiftinde dönüştürücüler klasik CNN paneline daha az benzer; bu, IN satırının doğal ölçekteki betimsel karşılığıdır ve 2x2'nin sınaması değildir". EK §5.6, bu türetmenin H1 ve H2'yi sınamadığını, ne desteklediğini ne çürüttüğünü açıkça yazmaktadır. EK §5.8, etkinin 0,1 düzeyinde kalması durumunda B8'in büyük olasılıkla "belirsiz" etiketi alacağını önceden yazmıştı; görüntü kaynaklı aralık beklenenden dar çıkmış ve etiket "belirsiz" olmamıştır.

Liu çiftinde aynı kural −0,20 beklenti eşiğiyle uygulanmıştır. Nokta kestirimi (−0,055) −0,20'nin üzerindedir, kestirim pozitif değildir ve %90 aralık (−0,137 ile 0,022) (−0,10; 0,10) bandının içinde de değildir; etiket bu yüzden "belirsiz"dir (B8B `A_sigma_scr_Liu.betimsel_etiket`). İhmal edilebilirlik bandının Liu satırında da ±0,10 olduğu EK §11'deki "A^σ_scr,Liu %90 aralığı (−0,10; 0,10) içinde" satırından okunmaktadır; EK §5.6'daki "−0,10 yerine −0,20 eşiğiyle" ifadesi yalnız beklenti eşiğini değiştirir. Bu okuma sonuç görülmeden kod ekiyle dondurulmuş sarmalayıcıda da böyledir: `experiments/q1_ek_ayrisim.py` (`d264c4e5...`) içindeki `b8_etiket` işlevi ihmal edilebilirlik bandını `delta` (= 0,10, dondurulmuş betiğin `DELTA` sabiti) ile, beklenti eşiğini ayrı bir `esik` bağımsız değişkeniyle (Liu için −0,20; B8B `A_sigma_scr_Liu.beklenti_esigi`) denetler. Bant −0,20 eşiğiyle (±0,20) okunsaydı %90 aralık (−0,137 ile 0,022) bandın içinde kalır, etiket "ihmal edilebilir" olur ve EK §11'in olumsuz Liu cümlesi tetiklenirdi; bu okuma rapordaki etiketle birlikte makalenin ek tablosunda dipnot olarak verilir. Liu satırının EK §11'deki iki cümlesinden hiçbiri tetiklenmediği için "Diğer bütün durumlar" satırı uygulanır: kestirim aralığıyla ek tabloda verilir, manşet değişmez. Üç çiftin ortalaması satırları karıştırdığından EK §5.6 gereği yalnız dipnotta verilebilir; bu raporda hesaplanmamıştır.

Dondurulmuş betiğin B8 tablosuyla ürettiği K-a, K-b ve K-c çıktısı yalnız karşılaştırma için aşağıdadır; p değerleri, Holm sonuçları ve karar etiketleri B8'de karar değildir (EK §5.6) ve metinde "destek" ya da "çürütüldü" sözcükleriyle anılamaz.

| Betimsel nicelik | Değerler | Aralık | Betiğin ham ve Holm p'si (karar değil) | J8 anahtarı |
|---|---|---|---|---|
| K-a q_k (çift 1, 2, 3) | 1,364; 0,682; 0,547 (ort 0,864) | %90 [0,126; 1,603] | ham p hesaplanmamış (payda kuralı), Holm 1,0 | `b2.F_B2.K-a.q`, `.sinama.ort`, `.sinama.ci90`, `p_holm[0]` |
| K-a D_k | 0,122; 0,173; 0,0999 | | | `b2.F_B2.K-a.D`; `payda_kucuk_tohumlar` = [2] |
| simetrik pay (= −A^σ_k) | 0,167; 0,118; 0,055 | | | `b2.F_B2.K-a.simetrik_pay` |
| yönlü pay | −0,044; 0,055; 0,045 | | | `b2.F_B2.K-a.yonlu_pay` |
| K-b ρ, dört dönüştürücü (Singh ViT-S, Singh ViT-B, Liu Swin-B, Mo ViT-B) | −0,211; −0,188; −0,049; 0,024 (ort −0,106) | %90 [−0,238; 0,026], %95 [−0,285; 0,073] | TOST 0,540; Holm 1,0 | `b2.F_B2.K-b.degerler`, `.ort`, `.ci90`, `.ci95`, `.tost_p`, `p_holm[1]` |
| K-c Δ_w (dönüştürücüler arası aile benzerliği) | 0,228 | %90 [−0,063; 0,513] | 0,0655; Holm 0,196 | `b2.F_B2.K-c.Delta_w`, `.bootstrap.ci90`, `p_ham[2]`, `p_holm[2]` |

Üçüncü çiftin paydası D = 0,0999 ile 0,10 sınırının hemen altında kaldığından betik K-a'yı payda kuralıyla "kararsiz" saymış ve p'yi 1 olarak aileye koymuştur (`p_1_sayilan_hesaplanamayan` = [0]). Birinci çiftte yönlü pay negatif olduğundan q 1'i aşmıştır. EK §5.6'nın istediği ayrı ρ değerleri B8B `donusturucu_rho_ayri_ayri` alanında da aynıdır: Singh dönüştürücüleri −0,211 ve −0,188, Liu Swin-B −0,049, Mo ViT-B 0,024'tür. K-b'nin dört dönüştürücüsü farklı başlatma satırlarını karıştırdığı için ortalama −0,106 yalnız betimseldir. K-c burada tohum içi değil, farklı grupların dönüştürücüleri arasındaki aile benzerliğini ölçer; dönüştürücüler arası log τ̄ değerleri −0,659 (Singh ViT-S ile ViT-B) ile −1,301 (Liu Swin-B ile Mo ViT-B) arasındadır (`b2.F_B2.K-c.log_tau_tur_ici`). Duyarlılık alanlarında tam örneklem ort ρ −0,107, logit ölçekte −0,052, oran ölçeğinde +2,71 puandır (J8 `b2.duyarlilik.tam_log.rho_V.ort`, `yari_logit.rho_V.ort`, `yari_oran.rho_V.ort`); panel üyesi bırakmalı jackknife'ta ort ρ −0,126 (Salman2020Do_50_2 çıkınca) ile −0,068 (Salman2020Do_R18 çıkınca) arasındadır (`b2.duyarlilik.panel_jackknife.*`). Salman grubunun üç üyesini birlikte çıkaran grup jackknife'ı bulunamamıştır.

EK §5.7'deki ön kayıtlı keşifsel çözümlemelerden üretilmiş ya da türetilebilir olanlar şunlardır. S8-2'de r matrisinin potansiyel payı 0,890'dır; rastgele beklenti 2/K = 0,143, dolaşım RMS'i 0,059, r RMS'i 0,177'dir (B8B `hodge_r_kesifsel.G_potansiyel_payi`, `.G_rastgele_beklenti_2_bolu_K`, `.dolasim_rms`, `.r_rms`). S8-5'te conv gövdeli Singh ViT-B ile yama gövdeli Mo ViT-B arasında σ farkı −0,053, ρ farkı −0,212'dir (TR; B8B `model_tablosu_ozet`). S8-6'da IN_Salman2020Do_R18 ile IN_Singh_ViT-S-CvSt arasındaki r değeri −0,433'tür (B8B `hodge_r_kesifsel.r_matrisi[8][13]`). S8-1'in D_k ve q_k aralıkları, S8-3'ün grup jackknife'ı, S8-7 ve S8-8'in çıktıları bulunamamıştır. S8-4 uygulanmamıştır, çünkü ön işleme denetiminde işaretlenen model yoktur.

## 5. B10: girdi gradyanı hizalanması (aile F_B10, altı sınama, Holm α = 0,05, bağlayıcı)

B10'da c_ij, iki modelin aynı temiz görüntü ve doğru etiket için çapraz entropi kaybının girdi gradyanları arasındaki kosinüsün görüntü ortalamasıdır (KO `tanim`); CIFAR-10'da B4 matrisinin 20 modeli, CIFAR-100'de B9'un 15 modeli, ImageNetV2'de B8'in 14 modeli kullanılmıştır (MC10, MC100, MIN `modeller_ortak`, `dislanan` boş). CIFAR-10 kolunda log τ̄ matrisi `results/q1/konsey_b4_matris`'ten okunmuştur (MC10 `matris_dizinleri`), EK §6.1 ile uyumludur. Sırasız çift sayıları 190, 105 ve 91'dir; görüntü başına kosinüslerde NaN yoktur (KO `nan_kosinus_sayisi` = 0). Anlamlılık Mantel permütasyon sınamasıyla, 9999 permütasyon ve tohum 20261030 ile verilmiştir (A10 `F_B10.sinamalar[k].perm`; MC `sinamalar.*.tohum`). Tek yönlü p = (1 + #{istatistik_perm ≥ gözlenen})/10000 olduğundan mümkün en küçük p 1e-04'tür; altı sınamanın altısında da gözlenen değere ulaşan permütasyon çıkmamış ve p bu alt sınıra oturmuştur. Bu nedenle p değerleri etkinin büyüklüğü hakkında bilgi taşımaz; büyüklük istatistiğin kendisinden ve permütasyon dağılımının yayılımından okunmalıdır (permütasyon SD'si 0,075 ile 0,169 arası; MC `sinamalar.*.perm_sd`).

| Sınama | Veri kümesi | Öngörü (büyüklük) | Spearman | Ham p | Holm p | EK §6.3 kural sırası | Karar | Öngörülen büyüklük |
|---|---|---|---|---|---|---|---|---|
| H10-cifar10 | CIFAR-10 (K = 20) | > 0 (≥ 0,50) | 0,943 | 1e-04 | 6,0e-04 | (i) tutmadı, (ii) tuttu | destek | tuttu |
| H10k-cifar10 | CIFAR-10 | artık > 0 (≥ 0,30) | 0,944 | 1e-04 | 6,0e-04 | (i) tutmadı, (ii) tuttu | destek | tuttu |
| H10-cifar100 | CIFAR-100 (K = 15) | > 0 (≥ 0,50) | 0,981 | 1e-04 | 6,0e-04 | (i) tutmadı, (ii) tuttu | destek | tuttu |
| H10k-cifar100 | CIFAR-100 | artık > 0 (≥ 0,30) | 0,912 | 1e-04 | 6,0e-04 | (i) tutmadı, (ii) tuttu | destek | tuttu |
| H10-imagenetv2 | ImageNetV2 (K = 14) | > 0 (≥ 0,50) | 0,694 | 1e-04 | 6,0e-04 | (i) tutmadı, (ii) tuttu | destek | tuttu |
| H10k-imagenetv2 | ImageNetV2 | artık > 0 (≥ 0,30) | 0,893 | 1e-04 | 6,0e-04 | (i) tutmadı, (ii) tuttu | destek | tuttu |

Tablodaki değerler A10'un `F_B10.sinamalar[0..5]` alanlarından (`istatistik`, `p_tek_ham`, `p_holm`, `karar`, `ongorulen_buyukluk_tuttu`) alınmıştır; aynı istatistikler MC10, MC100 ve MIN'in `sinamalar.ham.istatistik` ve `sinamalar.ana_etki_artik.istatistik` alanlarında ve Z2 satır 18-20'de de bulunmaktadır. Aile büyüklüğü 6'dır ve p = 1 sayılan sınama yoktur (A10 `F_B10.aile_buyuklugu`, `p_1_sayilan`). Holm'da altı eşit p'nin en küçüğü 6 ile çarpıldığından ve sonraki adımlar monotonluk gereği aynı değeri aldığından Holm sonrası p'lerin hepsi 6,0e-04'tür. Kural (i), yani çürütme, nokta kestirimi ≤ 0,20 ve ham p ≥ 0,20 ister; en küçük kestirim 0,694 olduğundan hiçbir sınamada tutmamıştır. Altı istatistik Mantel dosyalarındaki `c_matrisi` ve `log_tau_matrisi`'nden EK §6.2 tanımıyla (sırasız çiftler üzerinde Spearman; X_ij = μ + a_i + a_j + e_ij toplamsal modelinin en küçük kareler artıkları) bağımsız olarak yeniden hesaplanmış ve altı basamağa kadar aynı çıkmıştır; Mantel'deki c matrisinin kosinüs özetindeki `c_tum` ile model sırası eşlenerek aynı olduğu da denetlenmiştir (KY). EK §11'deki "F_B10'da en az iki veri kümesinde H10k destek ve hiçbir H10k çürütülmedi" satırı tetiklenmiştir ve metne şu cümle girer: "Simetrik terim, model düzeyi ana etkiler ayrıldıktan sonra da transferden ve saldırıdan bağımsız ölçülen girdi gradyanı hizalanmasıyla öngörülür (Zhang ve ark.'nın gradyan benzerliği tanımıyla)". EK §9'un sınırlılığı aynen geçerlidir: c_ij temiz görüntü üzerinde tek noktadaki hizalanmadır, PGD yolu boyunca değildir; τ̄ ile ilişkisi bir mekanizmanın gerekli koşuludur, yeterli kanıtı değildir ve toplamsal artıklama çarpımsal ya da etkileşimli model etkilerini ayırmaz.

Gradyan betiğinin çıktısındaki iki kısmi Mantel sınaması EK §6.2 gereği ön kayıt dışı keşifseldir, F_B10'a girmez ve Holm hesabına katılmaz. `kismi_omega` (ortak değişkenler log w_i + log w_j ve |log w_i − log w_j|) CIFAR-10'da 0,936, CIFAR-100'de 0,954, ImageNetV2'de 0,532'dir (ham p sırasıyla 1e-04, 1e-04, 2e-04); `kismi_omega_gradnorm` (bunlara ek olarak log gradyan normlarının toplamı) sırasıyla 0,937, 0,941 ve 0,597'dir (p 1e-04; A10 `kesifsel_kismi_omega.<d>`, `kesifsel_kismi_omega_gradnorm.<d>`). ImageNetV2'de ω ortak değişkenleri korelasyonu belirgin biçimde düşürmektedir (0,694'ten 0,532'ye), toplamsal ana etki artıklaması ise yükseltmektedir (0,893); iki kısmi istatistiğin aynı nesneyi ölçmediği bu farktan da görülmektedir.

c_ij dağılımının betimsel özeti aşağıdadır. Kosinüs özetlerinde mimari içi ve mimariler arası ortalama alanı bulunmadığından bu değerler `c_tum` matrisinden, aile ataması hücre tablolarının `aile` alanından (CNN ile ViT, Swin ya da XCiT) türetilmiştir (`_ek_rapor_b10.py`; TR). "Dönüştürücü" grubu ViT, Swin ve XCiT modellerini içerir.

| Veri kümesi | Bütün çiftler: ort (min; maks), n | CNN-CNN ort (n) | Dönüştürücü-dönüştürücü ort (n) | Karma ort (n) |
|---|---|---|---|---|
| CIFAR-10 | 0,460 (0,231; 0,746), 190 | 0,543 (91) | 0,464 (15) | 0,370 (84) |
| CIFAR-100 | 0,376 (0,169; 0,692), 105 | 0,462 (55) | 0,359 (6) | 0,271 (44) |
| ImageNetV2 | 0,218 (0,003; 0,486), 91 | 0,187 (36) | 0,318 (10) | 0,221 (45) |

CIFAR'da en düşük c değerleri ViT-Tiny tohumları ile CNN'ler arasında, en yüksekleri CNN panel üyeleri arasındadır; ImageNetV2'de en yüksek üç değer Singh grubunun kendi içindedir (0,419 ile 0,486), en düşük değer ise Salman2020Do_R18 ile Salman2020Do_R50 arasındadır (0,0034; §6'da şüphe olarak işlenmiştir).

## 6. Sapmalar ve şüpheler

EK §12'ye göre dondurmadan sonraki her değişiklik sapmadır; EK'te tanımlı kurallardan doğan kayıtlar sapma sayılmaz ama yazılır. Bu rapor sırasında EK §12 anlamında sapma sayılması gereken bir değişiklik bulunmamıştır: çözümleme betiğinin, iki hücre tablosunun, özgün matris betiğinin ve üç yeni betiğin özetleri dondurma ve kod eki kayıtlarıyla aynıdır (§0). Aşağıdaki maddeler `results/q1_research/ONKAYIT_SAPMALAR.md` dosyasının sonuna, mevcut metne dokunulmadan, "31.10.2026, ek ön kayıt §12 kayıtları (B8-B10 sonrası)" başlığıyla "not" olarak eklenmiştir; aynı işlemde `09_sonuc_b2_b6.md` §7'nin maddeleri de "31.10.2026, ana ön kayıt §7 kayıtları (B2-B6 sonrası)" başlığıyla eklenmiştir. Dosyanın özeti ekten önce `853429e1...`, ilk ekten sonra `df7eacf75a4b8e176bba142221d274d69c90327afcc461936a1ee8a7b6f08774` idi. Doğrulama turunda (31.10.2026) yalnız bu iki 31.10 başlığı düzeltilmiştir: ana başlığa 7. ve 8. maddeler eklenmiş, 1. madde düzeltilmiş; ek başlığın 3. ve 8. maddeleri genişletilmiş, 9. madde eklenmiştir. Dosyanın bugünkü özeti `06ac9ff351aaaec729d5cc5c5cbf6ae857078c169ecb1fce92d4fb705504fe3a`'tür ve ilk 38 satırın özeti hâlâ eski dosyanın özetiyle (`853429e1...`) aynıdır. Her maddede kaynağı ve makaleye etkisi yazılıdır.

1. B9 çözümlemesi zincirde iki kez çağrılmıştır. Bağlayıcı çıktı EK §4.2'deki tek çağrının ürünü olan J9'dur. Ardından `q1_ek_ayrisim.py --mod b9` sarmalayıcısı dondurulmuş betiği aynı matris ve hücre tablosuyla, varsayılan `--bootstrap 2000 --panel-en-az 5` bayraklarıyla ikinci kez çağırmış (J9S `meta.dondurulmus_cagri_argv`), çıktıyı `b9_sarmalayici_b2.json` adıyla yazmış ve yan dosyasını kendi eklediği `.sarmalayici.json` ekiyle `b9_sarmalayici_b2.json.sarmalayici.json` adıyla kaydetmiştir (Z2 satır 13-15). İki dondurulmuş betik çıktısı alan alan karşılaştırılmış, yalnız `meta.uretildi_utc` alanının farklı olduğu görülmüştür (`_ek_rapor_b9_karsilastir.py`; özetler `762d62b4...` ve `75dbfeab...`). Sonuç değişmediğinden ve bağlayıcı çağrı EK'e uygun olduğundan bu bir not niteliğindedir; föye sayılar yalnız J9'dan alınmalı, ikinci dosya yinelenen kopya olarak anılmalıdır.
2. B9 matrisi koşarken, başlatma doğrulaması sırasında `_ek_baslat2.sh` betiği `b9_matris.log` dosyasının son 15 satırını ekrana yazdırmış ve bu satırlar C100_ResNet18_AT_s1003 kaynağının 15 hedefe transfer hücrelerini göstermiştir (`10_konteyner_yeniden_kurulum.md` §8). Görülen değerler çözümlemeden önce görülmüş ama hiçbir çözümleme seçimine girmemiştir, çünkü B9 dondurulmuş betik ve dondurulmuş hücre tablosuyla, seçim bırakmayan tek çağrıyla çözümlenmiştir. EK §1 son paragrafı gereği bu bir görülme beyanıdır ve not olarak kayda geçirilmelidir; makalenin ön kayıt paragrafında tek cümleyle beyan edilmesi yeterlidir.
3. B9 ve B8 matris komutları EK §10'daki metinden iki noktada ayrılır. İki komuta da `--skip-existing` bayrağı eklenmiştir (`scripts/ek_zincir_komutlari.sh` satır 92 ve 95); ancak iki çıktı klasörü de boş başlamıştır, çünkü B9 klasöründeki en eski dosya 07:09:00'da, B8 klasöründeki 07:23:01'de, ilgili adımların başlamasından (07:08:49 ve 07:22:42; Z2 satır 1 ve 3) sonra yazılmıştır (`_ek_rapor_ozetler.sh`). B9'dan önce de CIFAR-100 XCiT kontrol noktası depodaki kopyadan torch hub önbelleğine konmuştur (satır 89-90); betik yorumu bu dosyanın SHA-256'sının doğrulandığını belirtir, kopyalama anında ayrıca denetim yapılmamıştır. B9 özgün betikle koşulduğundan (EK §12'nin sapma tanımı dışında) ve bayrak etkisiz kaldığından her iki nokta da nottur. Üçüncü bir ayrılık koşu sırasındadır. EK §10 madde 2'nin aksine B9 çözümlemesi B9 matrisinin hemen ardından değil, zincirin sonundaki çözümleme adımında (`scripts/ek_zincir_komutlari.sh` satır 106-125, `adim_cozumleme`), B8 matrisi ve B10 gradyanları üretildikten sonra ve B8 çözümlemesinden yaklaşık 4 s önce yapılmıştır (Z2 satır 3, 8, 12; J9 `meta.uretildi_utc` 04:43:48Z, J8 `meta.uretildi_utc` 04:43:51Z). Çağrı seçim bırakmadığından ve arada sonuç açılmadığından EK §10'un gerekçesi olan bağlayıcı yinelemenin B8'in betimsel sonucundan önce sabitlenmesi zedelenmemiştir ve bu durum da nottur.
4. Ön kayıtlı duyarlılık ve keşifsel çözümlemelerin bir kısmı üretilmemiştir: B10'un her-ikisi-doğru c_ij duyarlılığı (EK §6.1; KO'da `c_iki_model_dogru` matrisi vardır ama Mantel çıktıları yalnız `c_turu` = "tum" ile üretilmiştir), S9-2, S9-4, S8-1'in D_k ve q_k aralıkları, S8-3'ün grup jackknife'ı, S8-7, S8-8 ve S10-1 ile S10-7 arası (S10-3'ün kodu dondurmada yazılmamıştır). Bunlar eksik keşifsel çözümleme ya da eksik duyarlılık olarak nottur; kararları etkilemez. Her-ikisi-doğru c duyarlılığı ve S10-2 bu raporda keşifsel olarak yeniden hesaplanmıştır (§7). S9-4'ün eksikliği B9'daki temiz doğruluk karıştırıcısı nedeniyle önemlidir ve makaleye girmeden önce keşifsel etiketle tamamlanması önerilir.
5. Zincir başında GPU'da 2804 MiB bellek kullanılmaktaydı (not; Z1 satır 2; konteyner yeniden kurulumunda da 2893 MiB kullanılan bellek görülmüştür, `10_konteyner_yeniden_kurulum.md` §1). Bekçi kuralının boş VRAM eşiği (12000 MiB) her adımda geçilmiştir. GPU regresyonu birebir çıktığından sonuçlar etkilenmemiştir; makalenin hesaplama ayrıntılarında RTX 5090'ın başka bir süreçle paylaşıldığı beyan edilebilir.
6. EK §5.1'in istediği seçim öncesi klasör ve dosya sayısı denetiminin sonucu manifest dosyasına yazılmamıştır (MF yalnız `kok`, `secim_kurali`, `onisleme`, `n`, `tensor_sekli`, `liste_sha256` ve `dosyalar` alanlarını taşır). Bu raporda yapılan bağımsız sayım 1000 klasör ve her klasörde 10 dosya, manifestte de sınıf başına 2 dosya vermiştir (`_ek_rapor_v2say.sh`). Koşul sağlandığından not.

Beklenmedik gözlemler ve şüpheler ayrıca kayda geçirilmiştir; bunlar sapma değildir, ama makalenin yazımını etkiler. İlk ve en önemli şüphe ImageNetV2 kosinüs matrisindedir: IN_Salman2020Do_R18 ile IN_Salman2020Do_R50 arasındaki c değeri 0,0034'tür (KOIN `c_tum[0][1]`) ve görüntü başına kosinüslerin standart sapması yalnız 0,0015'tir; 2000 görüntünün hepsinde mutlak değer 0,02'nin altındadır (`results/q1/konsey_b10_gradyan/imagenetv2/kosinus.npz`, `_ek_rapor_r18.py`). 150528 boyutlu iki ilişkisiz vektörün kosinüsü de bu düzeydedir; oysa aynı iki modelin üçüncü modellerle kosinüsleri olağandır (R18 ile Engstrom2019Robustness 0,130, R50 ile Engstrom2019Robustness 0,240, R18 ile Salman2020Do_50_2 0,175) ve aynı çiftin log τ̄ değeri (−0,936; MIN `log_tau_matrisi[0][1]`) R18'in en yüksek benzerliklerinden biridir. İki modelin gradyan normları olağandır (medyan 0,881 ve 0,833, sıfır norm yok). Bu örüntü gerçek bir özellik olabileceği gibi bir yükleme ya da hesap yapaylığına da işaret edebilir ve bu rapordaki verilerle ayrılamaz. B10 kararını etkilemediği keşifsel olarak denetlenmiştir: R18 çıkarılınca ham ve artık Spearman 0,672 ve 0,898, R50 çıkarılınca 0,794 ve 0,910 olmaktadır (KY; permütasyonsuz nokta kestirimi). Kısa bir GPU denetimi (iki modelin birkaç görüntüde gradyanlarını yeniden yükleyip kosinüsünü ölçmek) makaleden önce yapılmalıdır.

İkinci beklenmedik sonuç K-b(B9)'un çürütülmesidir. ViT'nin CIFAR-100'deki yönlü terimi log ölçekte 0,143 ile CIFAR-10'dakinin (0,012) on katından büyüktür; buna karşılık logit ölçekte −0,413, oran ölçeğinde −14,61 puandır (J9 `b2.duyarlilik.yari_logit.rho_V.ort`, `yari_oran.rho_V.ort`). Yönlü terimin yalnız büyüklüğü değil işareti de ölçeğe bağlıdır ve CIFAR-100'deki pozitif log değerin bir kısmı ViT'nin düşük temiz doğruluğundan (41,94-44,06) gelebilir. Önceden yazılmış K-b cümlesindeki "SVHN'de ters işaretli" yan cümlesinin kaynağı bu raporda doğrulanmamıştır; metne girmeden önce föyün SVHN bölümünden (`results/C1_REFERANS_FOYU.md`, "Uc-protokol egimi, SVHN dahil") kaynağıyla bağlanmalıdır. Üçüncü olarak, ImageNetV2'de sıfırdan satırını temsil eden tek Liu çiftinin A^σ'sı (−0,055) CIFAR-10 2x2'deki H1 kestiriminin (−0,364; J4 `b4.F_B4.karsitliklar.H1.kestirim`) yaklaşık altıda biridir; bu fark ölçek, mimari (Swin-B ile ViT-Tiny) ve başlatma kanıtının dolaylılığı nedeniyle yorumlanamaz, ama "sıfırdan eğitimde büyük mimari benzemezliği" cümlesinin ImageNet ölçeğine genellenmemesi gerektiğini gösterir. Dördüncü olarak B8'de yönlü terim dönüştürücüye özgü görünmemektedir: Singh grubunun CNN'leri de negatif ρ taşır (ConvNeXt-T −0,122, ConvNeXt-B −0,298), çift içi A^ρ ise bir çiftte negatif (−0,089), ötekinde pozitiftir (0,110). Son olarak OD'nin normalizasyon taraması Chen2024Data_WRN_50_2, Singh ConvNeXt-T ve ConvNeXt-B, Singh ViT-B ve XCiT-S12'de model içi normalizasyon katmanı bulamamış, Singh ViT-S'te ise bulmuştur (OD `normalizasyon.<m>.model_ici_normalizasyon_var`). Bu modellerin temiz doğrulukları denetimi rahatça geçtiğinden (57,60-64,85) yükleme hatası beklenmez; tarama adlara dayalı olduğundan bu tutarsızlık büyük olasılıkla katman adlandırmasından gelir, ama yöntem bölümünde normalizasyonun RobustBench nesnesinde nasılsa öyle kullanıldığı açıkça yazılmalıdır.

## 7. Keşifsel notlar (ön kayıt dışı)

Bu bölümdeki her yorum ön kayıt dışıdır, hiçbir karar kuralına bağlı değildir ve makalede ancak "keşifsel" etiketiyle yer alabilir.

CIFAR-100'de ViT-Tiny ile ResNet-18 arasındaki simetrik pay üç tohum ortalamasında 0,362'dir (TR; J9 `b2.F_B2.K-a.simetrik_pay`), CIFAR-10'da 0,365'tir (TR; J2 aynı alan). ViT tohumlarının panel benzerliği σ_V iki veri kümesinde neredeyse aynı düzeydedir (CIFAR-100'de ortalama −1,006, CIFAR-10'da −1,009; TR). Açığın simetrik bileşeni veri kümesinden bağımsız görünürken K-a'daki q'nun 0,936'dan 0,840'a inmesi büyük ölçüde yönlü payın büyümesinden (ortalama 0,025'ten 0,069'a; TR) kaynaklanmaktadır. Bu örüntü, simetrik benzemezliğin mimariye ait, yönlü terimin ise veri kümesine ve doğruluk düzeyine bağlı olduğu okumasıyla uyumludur; ancak bu ayrım ön kayıtta sınanmamıştır.

ImageNetV2'deki Ā^σ_IN (−0,142) CIFAR-10 2x2'nin IN satırındaki σ(V-IN) − σ(R224-IN) farkına (−0,104; TR, J4 `b4.F_B4.karsitliklar.H2.hucre_ort`) yakındır. İki nicelik farklı veri kümesi, mimari ve başlatma anlamında tanımlandığından (EK §9) bu yakınlık bir yineleme sayılamaz. Singh çiftlerinde dönüştürücü ile CNN eşinin temiz doğruluğu (60,90 ile 61,00; 63,20 ile 64,85) ve w'su (34,56 ile 34,59; 30,30 ile 31,84) neredeyse aynıdır (KS; B8B `ciftler[k].A_omega_log_w` 0,001 ve 0,050); dolayısıyla IN satırındaki σ farkı bu iki çiftte doğruluk ya da kırılganlık farkıyla açıklanamaz. Bu eşleşme, CIFAR-100'deki ViT-Tiny karıştırıcısının tersine, B8'in temiz doğruluk bakımından iyi eşlenmiş bir karşılaştırma sunduğunu gösterir.

B10'da EK §6.1'in tanımladığı ama Mantel çıktısına girmeyen her-ikisi-doğru duyarlılığı bu raporda yeniden hesaplanmıştır: c yalnız iki modelin de temiz doğru olduğu görüntülerle sınırlandığında ham ve artık Spearman CIFAR-10'da 0,927 ve 0,928, CIFAR-100'de 0,972 ve 0,906, ImageNetV2'de 0,720 ve 0,879'dur; altısında da 9999 permütasyonlu p = 1e-04'tür (KY). EK §6.4'teki S10-3 (aile göstergesi) için kod yazılmamıştır; ona yakın bir hesapta ana etki artıklarından aile eşleşmesi (CNN-CNN, dönüştürücü-dönüştürücü, karma) de ayıklandığında kalan Spearman (ana etki artıklarının sıraları çift türü göstergesine göre ayıklanarak hesaplanan sıra kısmi korelasyonu; ayıklama değer ölçeğinde yapılsaydı sonuç en çok ±0,012 farklı olurdu) CIFAR-10'da 0,905, CIFAR-100'de 0,892, ImageNetV2'de 0,888'dir; yalnız CNN-CNN çiftleriyle sınırlanan artık Spearman sırasıyla 0,963, 0,929 ve 0,843'tür (KY, permütasyonsuz nokta kestirimleri). Ham korelasyonun 0,98'e çıkmasında blok yapısının payı olsa da ilişkinin aile ayrımına indirgenmediği bu hesaptan anlaşılmaktadır. S10-2'de C1 çiftlerinde γ(ViT) − γ(ResNet) farkı CIFAR-10'da −0,217, −0,225 ve −0,213, CIFAR-100'de −0,179, −0,188 ve −0,192'dir (KY); beklenen yön (negatif) altı tohumda da gözlenmiştir. ImageNetV2'deki aynı tarifli çiftlerde benzer fark çok küçüktür (Singh −0,015 ve −0,029, Liu +0,007; KY).

## 8. Makale için sonraki adımlar

Föyün (`results/C1_REFERANS_FOYU.md`) M9 bölümü şu anda M9.1-M9.9 alt başlıklarını taşımaktadır ve otomatik üretildiği için (`scripts/build_reference_sheet.py`) aşağıdaki sayılar ancak bu betiğe eklenen yeni alt bölümlerle metne girebilir. Önerilen ekler şunlardır: M9.10 B9 F_B9 tablosu (§3'teki üç satır, Holm ve kararlar, δ = 0,06), B9 model tablosu (temiz, w, σ, ρ) ve logit ile oran ölçeği ρ(V-scr) değerleri, kaynak yalnız J9 ve köşegen npz'ler; M9.11 B8 betimsel tablosu (Ā^σ_IN, çift değerleri, A^σ_scr,Liu, aralıklar ve etiketler, on dört modelin temiz ve PGD-10 doğrulukları ile w, σ, ρ), ön işleme denetimi özeti (OD) ve "betimsel, Holm yok" ibaresi; M9.12 B10 F_B10 tablosu (altı istatistik, ham ve Holm p, permütasyon sayısı ve p tabanı), aile dışı `kismi_omega` değerleri "keşifsel" ibaresiyle; M9.13 bütünlük (dondurulmuş betik, iki hücre tablosu, EK gövdesi, üç kod eki özeti, liste özeti). Bulunamayan kalemler (S9-2, S9-4, S8-1'in D_k ve q_k aralıkları, S8-3 grup jackknife'ı, S8-7, S8-8, S10-1 ile S10-7, B10 her-ikisi-doğru Mantel'i) föyde de "bulunamadı" diye yazılmalıdır.

Ek blokların sonuçlarıyla iki iddia güçlenmiştir. ViT kaynak açığının simetrik payla taşınması ve ViT tohumlarının birbirine panelden çok benzemesi, ikinci bir veri kümesinde bağlayıcı olarak yinelenmiştir (K-a ve K-c, B9). Simetrik terimin transferden ve saldırıdan bağımsız bir ölçüyle, gradyan hizalanmasıyla, üç veri kümesinde ve model ana etkileri ayrıldıktan sonra da öngörülmesi bağlayıcı olarak desteklenmiştir (F_B10). Bu sonuç EK §11'deki cümleyi tetikler; EK §9 gereği gradyan hizalanması bir mekanizmanın gerekli koşulu olarak okunur, yeterli kanıtı sayılmaz. Kanıtın gücüne ilişkin daha ileri bir değerlendirme ön kayıt dışıdır ve IN_Salman2020Do_R18 ile IN_Salman2020Do_R50 kosinüsünün GPU denetimi bitene kadar yapılmaz. Daralan iddia "küçük yönlü terim" cümlesidir: K-b(B9)'un çürütülmesiyle bu cümle EK §11 gereği CIFAR-10 ile sınırlanır; ana ön kaydın O1 manşetindeki "küçük, mimariden bağımsız bir yönlü terim" ifadesi özet ve tartışmada "CIFAR-10'da, log ölçekte, CNN panelinde" nitelemesiyle yazılmalı ve CIFAR-100 sonucu açıkça verilmelidir. Yalnız betimsel kalması gerekenler B8'in bütün nicelikleridir: Ā^σ_IN "beklentiyle uyumlu" etiketiyle ve 2x2'nin sınaması olmadığı vurgulanarak, Liu satırı "belirsiz" etiketiyle ve tek çifte dayandığı belirtilerek ek tabloda verilmeli, B8'in K-a, K-b ve K-c çıktısı karar diliyle anılmamalıdır. B10'un mekanizma yorumu EK §9'daki sınırla, yani "gerekli koşul, yeterli kanıt değil" çerçevesinde kalmalıdır.

Bunlardan önce yapılması gerekenler sırasıyla şunlardır: §6'daki maddelerin sapma kaydına işlenmesi (bu raporla birlikte yapılmıştır); IN_Salman2020Do_R18 ile IN_Salman2020Do_R50 kosinüsünün kısa bir GPU denetimiyle doğrulanması; önceden yazılmış K-b(B9) cümlesindeki "SVHN'de ters işaretli" yan cümlesinin föyün SVHN bölümüne bağlanması ve yöntem bölümüne normalizasyonun RobustBench nesnesindeki haliyle kullanıldığının yazılması; S9-4 her-ikisi-doğru protokolünün B9 için keşifsel olarak üretilmesi; föye M9.10-M9.13 bölümlerinin betik üzerinden eklenmesi; ardından makale revizyonu ve tek turlu hakem paneli.

## Sayı kaynak dizini

Her satır (değer, dosya, anahtar ya da satır) üçlüsüdür. Değer raporda görüldüğü biçimdedir; JSON'daki ham değer gösterilen basamağa yuvarlanmıştır. TR satırlarında anahtar sütunu formülü verir; KS satırlarında dosya köşegen npz'dir, hesap `target_clean_correct` ve `target_adv_wrong` dizilerinden yapılmıştır; KY satırları `arsiv/b2_yardimci/_ek_rapor_b10_yeniden.py` çıktısıdır.

| Değer | Dosya | Anahtar ya da satır |
|---|---|---|
| 4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389 | results/q1/konsey_b9_c100/b9_dondurulmus_b2.json | meta.betik_sha256 (J8'de aynı alan); sha256sum experiments/q1_konsey_ayrisim.py |
| 4afa5fbc...a390a388d | results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json | meta.hucre_tablosu_sha256; sha256sum hucre_tablosu_b8.json |
| be778f42...f40dde3bd | results/q1/konsey_b9_c100/b9_dondurulmus_b2.json | meta.hucre_tablosu_sha256; sha256sum hucre_tablosu_b9.json |
| 76d05f111371230495c95b757e46dccdb84123264034cc8432cb0a31403df595 | raporlar/konsey_2026-10-29/ON_KAYIT_EK_B8_B10_2026-10-30.md | Dondurma eki (d); yeniden hesap arsiv/b2_yardimci/_ek_rapor_ozetler.sh |
| f25d9062c958a296353059639398f0a0a8eb18cd48182b1afa5ec4e3986140b7 | results/q1/konsey_b9_c100/b9_sarmalayici_b2.json.sarmalayici.json | meta.ozgun_matris_betigi_sha256_simdi; Z1 satır 3 |
| edec356a... | results/q1/konsey_b8_imagenetv2/matris/transfer_matrix.json | ek_betik_sha256; Z1 satır 4 |
| d264c4e5... | results/q1/konsey_b10_gradyan/b10_aile.json | meta.sarmalayici_sha256 (J9S, B8B'de aynı) |
| c82a66d1... | results/q1/konsey_b10_gradyan/imagenetv2/kosinus_ozet.json | betik_sha256 (KO10, KO100, MC10, MC100, MIN'de aynı) |
| 9 hücre, 9 npz, BIREBIR true (iki karşılaştırma) | results/q1/ek_regresyon/gpu_n200/karsilastirma_ozgun_catal.json, karsilastirma_ozgun_onb_catal_onb.json | hucre_sayisi, npz_sayisi, BIREBIR |
| 24 s; 24 s; 22 s; 23 s | results/q1/ek_loglar/ek_zincir_1.log | satır 5, 6, 10, 11 |
| 2804 MiB | results/q1/ek_loglar/ek_zincir_1.log | satır 2 |
| 41,55; 31,752 | results/q1/konsey_b8_imagenetv2/denetim/onisleme_denetimi.json | modeller.IN_Salman2020Do_R18.temiz_dogruluk_kendi; .esik.esik_i |
| 9,80 puan | TR | 41,55 − 31,752 |
| 1,20 puan | onisleme_denetimi.json | modeller.IN_Wong2020Fast.esik.mutlak_fark_puan |
| 0,95 puan | onisleme_denetimi.json | modeller.IN_Mo_ViT-B.esik.mutlak_fark_puan |
| kalan [], isaretli [] | onisleme_denetimi.json | kalan; isaretli |
| 1000 klasör × 10 dosya; 1000 sınıf × 2 | data/imagenetv2/imagenetv2-matched-frequency-format-val; imagenetv2_manifest.json | _ek_rapor_v2say.sh; dosyalar[*].etiket |
| 25db498ba8b2c710618e76e8a2dfe5492c9f75be0be1b7f63c253acc4f27d1a8 | denetim/imagenetv2_manifest.json ve matris/imagenetv2_manifest.json | liste_sha256; Z2 satır 6-7 |
| ε 4/255, α 1/255, 10 adım, n 2000, batch 25 | results/q1/konsey_b8_imagenetv2/matris/cells_meta.json; transfer_matrix.json | eps, alpha, steps, n_samples; eps_255, alpha_255, batch_size |
| ε 8/255, α 2/255, n 10000 | results/q1/konsey_b9_c100/matris/cells_meta.json | eps, alpha, n_samples |
| 06:58:56; 07:00:31; 07:07:58 | ek_zincir_1.log | satır 1, 19, 23 |
| 07:08:49; 07:22:42; 07:38:55; 07:43:46; 07:44:09 | ek_zincir_2.log | satır 1, 3, 8, 12, 22 |
| 1 dk 35 s; 7 dk 27 s; 13 dk 53 s; 16 dk 13 s; 4 dk 51 s; 23 s | TR | bitiş − başlangıç (Z1, Z2 saatleri) |
| 28,5; 36,1 dk | raporlar/konsey_2026-10-29/_ek_sure_kestirimi.json | B9_n10000.dk_hiz_a; .dk_hiz_b |
| 11,5; 14,6 dk | _ek_sure_kestirimi.json | B8_n1000.dk_hiz_a; .dk_hiz_b |
| 23,0; 29,2 dk | TR | 2 × 11,5; 2 × 14,6 |
| 0,840 [0,795; 0,885], %95 [0,773; 0,906] | b9_dondurulmus_b2.json | b2.F_B2.K-a.sinama.ort; .ci90; .ci95 |
| 0,848; 0,861; 0,810 | b9_dondurulmus_b2.json | b2.F_B2.K-a.q |
| 1,02e-03; 0,953; 5,00e-04 | b9_dondurulmus_b2.json | b2.F_B2.p_ham[0..2] |
| 2,05e-03; 0,953; 1,50e-03 | b9_dondurulmus_b2.json | b2.F_B2.p_holm[0..2] |
| destek; curutuldu (pozitif yon); destek | b9_dondurulmus_b2.json | b2.F_B2.karar.K-a, .K-b, .K-c |
| 0,143 (0,134; 0,123; 0,170) | b9_dondurulmus_b2.json | b2.F_B2.K-b.ort; .degerler |
| [0,101; 0,184]; [0,082; 0,203] | b9_dondurulmus_b2.json | b2.F_B2.K-b.ci90; .ci95 |
| 1,69e-03; 0,953 | b9_dondurulmus_b2.json | b2.F_B2.K-b.tost_p_alt; .tost_p_ust |
| 0,519 [0,469; 0,599], %95 [0,463; 0,604] | b9_dondurulmus_b2.json | b2.F_B2.K-c.Delta_w; .bootstrap.ci90; .ci95 |
| 284 | b9_dondurulmus_b2.json | b2.F_B2.K-c.bootstrap.yeniden_cekilen_tek_tohumlu_ornek |
| 0,388; 0,459; 0,448 | b9_dondurulmus_b2.json | b2.F_B2.K-a.D |
| 0,329; 0,395; 0,363 | b9_dondurulmus_b2.json | b2.F_B2.K-a.simetrik_pay |
| 0,059; 0,064; 0,085 | b9_dondurulmus_b2.json | b2.F_B2.K-a.yonlu_pay |
| 7,8e-16 | b9_dondurulmus_b2.json | b2.F_B2.K-a.ozdeslik_artik_max |
| −0,417; −0,514; −0,529 | b9_dondurulmus_b2.json | b2.F_B2.K-c.log_tau_tur_ici |
| −0,971; −1,031; −1,015 | b9_dondurulmus_b2.json | b2.F_B2.K-c.sigma_V |
| −0,468; −0,520; −0,514 | b9_dondurulmus_b2.json | b2.tur_ici_resnet_log_tau |
| 0,986 | b9_dondurulmus_b2.json | b2.F_B2.duyarlilik_delta_0.06.p_holm[1] |
| 0,840; 0,143 (tam örneklem) | b9_dondurulmus_b2.json | b2.duyarlilik.tam_log.q_ort; .rho_V.ort |
| 1,026; −0,413 [−0,609; −0,217] | b9_dondurulmus_b2.json | b2.duyarlilik.yari_logit.q_ort; .rho_V.ort; .rho_V.ci95 |
| 1,216; −14,61 | b9_dondurulmus_b2.json | b2.duyarlilik.yari_oran.q_ort; .rho_V.ort |
| 0,831; 0,847; 0,127; 0,150 | b9_dondurulmus_b2.json | b2.duyarlilik.panel_jackknife.{C100_Jia2022LAS-AT_34_10.q_ort, C100_Wang2023Better_WRN-28-10.q_ort, C100_Wang2023Better_WRN-28-10.rho_V_ort, C100_Rice2020Overfitting.rho_V_ort} |
| 0,799; 0,834; 0,771 | b9_dondurulmus_b2.json | b2.duyarlilik.ikincil_panel.q |
| 0,129; 0,136; 0,221 | b9_dondurulmus_b2.json | b2.duyarlilik.ikincil_panel.rho_V |
| −0,489; 0,000; −0,567; 0,009 | b9_dondurulmus_b2.json | b2.model_tablosu.C100_Debenedetti2022Light_XCiT-S12.yari_log.sigma, .rho; C100_Hendrycks2019Using.yari_log.sigma, .rho |
| 0,078 | TR | −0,489 − (−0,567) |
| B9 model tablosu σ ve ρ (15 satır) | b9_dondurulmus_b2.json | b2.model_tablosu.<m>.yari_log.sigma, .rho |
| B9 temiz, PGD-10, w (15 satır) | results/q1/konsey_b9_c100/matris/per_sample_<m>_to_<m>.npz | KS; transfer_matrix.json results.<m>-><m>.target_clean_acc, .cond_fooling |
| 41,94; 43,50; 44,06; 62,68-64,65; 53,82-72,57 | b9_sarmalayici_b2.json.sarmalayici.json | temiz_dogruluk_yuzde.<m> |
| 0,936 [0,925; 0,948]; 0,940; 0,928; 0,940 | results/q1/konsey_ayrisim_b2.json | b2.F_B2.K-a.sinama.ort; .ci90; .q |
| 0,391; 0,387; 0,390 | konsey_ayrisim_b2.json | b2.F_B2.K-a.D |
| 0,368; 0,360; 0,367; 0,023; 0,028; 0,023 | konsey_ayrisim_b2.json | b2.F_B2.K-a.simetrik_pay; .yonlu_pay |
| 0,012 [−0,007; 0,031]; [−0,016; 0,040] | konsey_ayrisim_b2.json | b2.F_B2.K-b.ort; .ci90; .ci95 |
| 0,566 [0,537; 0,604] | konsey_ayrisim_b2.json | b2.F_B2.K-c.Delta_w; .bootstrap.ci90 |
| 4,19e-05; 2,73e-03; 5,00e-04 | konsey_ayrisim_b2.json | b2.F_B2.p_ham |
| 1,26e-04; 2,73e-03; 1,00e-03 | konsey_ayrisim_b2.json | b2.F_B2.p_holm |
| −0,304; −14,66; 1,101; 1,542 | konsey_ayrisim_b2.json | b2.duyarlilik.yari_logit.rho_V.ort; yari_oran.rho_V.ort; yari_logit.q_ort; yari_oran.q_ort |
| 0,899; 0,825; 0,842; 0,198; 0,202; 0,204 | konsey_ayrisim_b2.json | b2.duyarlilik.ikincil_panel.q; .rho_V |
| −0,453; −0,466; −0,410 | konsey_ayrisim_b2.json | b2.F_B2.K-c.log_tau_tur_ici |
| −0,496; −0,494; −0,476 | konsey_ayrisim_b2.json | b2.tur_ici_resnet_log_tau |
| −1,015; −1,000; −1,011 | konsey_ayrisim_b2.json | b2.F_B2.K-c.sigma_V |
| −0,364 | results/q1/konsey_ayrisim_b4.json | b4.F_B4.karsitliklar.H1.kestirim |
| −0,104 | TR | J4 b4.F_B4.karsitliklar.H2.hucre_ort: V-IN (−0,739) − R224-IN (−0,635) |
| −0,142 [−0,197; −0,090], %95 [−0,207; −0,081] | results/q1/konsey_b8_imagenetv2/b8_betimsel.json | A_sigma_IN.kestirim; .goruntu_bootstrap.ci90; .ci95 |
| −0,167; −0,118 | b8_betimsel.json | A_sigma_IN.cift_degerleri |
| 0,048 | b8_betimsel.json | A_sigma_IN.iki_cift_farki |
| beklentiyle uyumlu | b8_betimsel.json | A_sigma_IN.betimsel_etiket |
| [−0,234; −0,096]; [−0,246; −0,084] | b8_betimsel.json | ciftler[0].goruntu_bootstrap_ci90; ci95 |
| [−0,202; −0,038]; [−0,217; −0,023] | b8_betimsel.json | ciftler[1].goruntu_bootstrap_ci90; ci95 |
| −0,193; −0,089; 0,001 | b8_betimsel.json | ciftler[0].A_sigma_logit; .A_rho; .A_omega_log_w |
| −0,147; 0,110; 0,050 | b8_betimsel.json | ciftler[1].A_sigma_logit; .A_rho; .A_omega_log_w |
| −0,055 [−0,137; 0,022], %95 [−0,153; 0,034] | b8_betimsel.json | A_sigma_scr_Liu.kestirim; .goruntu_bootstrap.ci90; .ci95 |
| −0,061; 0,091; −0,015 | b8_betimsel.json | ciftler[2].A_sigma_logit; .A_rho; .A_omega_log_w |
| belirsiz | b8_betimsel.json | A_sigma_scr_Liu.betimsel_etiket |
| B = 2000, tohum 20261030 | b8_betimsel.json | meta.bootstrap_B; meta.bootstrap_tohum |
| B8 model tablosu σ, ρ, w (14 satır) | b8_betimsel.json | model_tablosu_ozet.<m>.sigma, .rho, .w_yuzde |
| B8 temiz ve PGD-10 (14 satır) | results/q1/konsey_b8_imagenetv2/matris/per_sample_<m>_to_<m>.npz | KS; transfer_matrix.json temiz_dogruluk.<m> |
| 1,364; 0,682; 0,547; 0,864; [0,126; 1,603] | b8_dondurulmus_b2.json | b2.F_B2.K-a.q; .sinama.ort; .sinama.ci90 |
| 0,122; 0,173; 0,0999; [2] | b8_dondurulmus_b2.json | b2.F_B2.K-a.D; .payda_kucuk_tohumlar |
| 0,167; 0,118; 0,055; −0,044; 0,055; 0,045 | b8_dondurulmus_b2.json | b2.F_B2.K-a.simetrik_pay; .yonlu_pay |
| −0,211; −0,188; −0,049; 0,024; −0,106 | b8_dondurulmus_b2.json | b2.F_B2.K-b.degerler; .ort (B8B donusturucu_rho_ayri_ayri ile aynı) |
| [−0,238; 0,026]; [−0,285; 0,073]; 0,540 | b8_dondurulmus_b2.json | b2.F_B2.K-b.ci90; .ci95; .tost_p |
| 0,228 [−0,063; 0,513]; 0,0655; 0,196 | b8_dondurulmus_b2.json | b2.F_B2.K-c.Delta_w; .bootstrap.ci90; p_ham[2]; p_holm[2] |
| Holm 1,0; 1,0 | b8_dondurulmus_b2.json | b2.F_B2.p_holm[0]; [1] |
| −0,659; −1,301 | b8_dondurulmus_b2.json | b2.F_B2.K-c.log_tau_tur_ici (Singh ViT-S|ViT-B; Liu Swin-B|Mo ViT-B) |
| −0,107; −0,052; +2,71 | b8_dondurulmus_b2.json | b2.duyarlilik.tam_log.rho_V.ort; yari_logit.rho_V.ort; yari_oran.rho_V.ort |
| −0,126; −0,068 | b8_dondurulmus_b2.json | b2.duyarlilik.panel_jackknife.IN_Salman2020Do_50_2.rho_V_ort; IN_Salman2020Do_R18.rho_V_ort |
| 0,890; 0,143; 0,059; 0,177 | b8_betimsel.json | hodge_r_kesifsel.G_potansiyel_payi; .G_rastgele_beklenti_2_bolu_K; .dolasim_rms; .r_rms |
| −0,053; −0,212 | TR | B8B model_tablosu_ozet: σ(Singh ViT-B) − σ(Mo ViT-B); ρ(Singh ViT-B) − ρ(Mo ViT-B) |
| −0,433 | b8_betimsel.json | hodge_r_kesifsel.r_matrisi[8][13] |
| 0,943; 0,944; 0,981; 0,912; 0,694; 0,893 | results/q1/konsey_b10_gradyan/b10_aile.json | F_B10.sinamalar[0..5].istatistik (MC10, MC100, MIN sinamalar.ham/.ana_etki_artik.istatistik; Z2 satır 18-20) |
| p 1e-04 (altı sınama) | b10_aile.json | F_B10.sinamalar[k].p_tek_ham |
| Holm 6,0e-04 (altı sınama) | b10_aile.json | F_B10.sinamalar[k].p_holm |
| 9999; 20261030 | b10_aile.json; mantel_*.json | F_B10.sinamalar[k].perm; sinamalar.*.tohum |
| 6; [] | b10_aile.json | F_B10.aile_buyuklugu; F_B10.p_1_sayilan |
| 20; 15; 14; 190; 105; 91 | mantel_cifar10.json, mantel_cifar100.json, mantel_imagenetv2.json | sinamalar.ham.K; .cift_sayisi |
| 0,075-0,169 | mantel_*.json | sinamalar.*.perm_sd (en küçük MC10 ana_etki_artik 0,0753; en büyük MC100 ham 0,1689) |
| 0,936; 0,954; 0,532; p 1e-04, 1e-04, 2e-04 | b10_aile.json | kesifsel_kismi_omega.{cifar10, cifar100, imagenetv2}.istatistik; .p_tek |
| 0,937; 0,941; 0,597 | b10_aile.json | kesifsel_kismi_omega_gradnorm.<d>.istatistik |
| c dağılım tablosu (ortalamalar, min, maks, n) | kosinus_ozet.json (üç veri kümesi) ve hücre tabloları | TR, _ek_rapor_b10.py: c_tum üst üçgen, aile alanına göre gruplama |
| 0,419-0,486 (Singh içi en yüksek üç) | results/q1/konsey_b10_gradyan/imagenetv2/kosinus_ozet.json | c_tum, _ek_rapor_b10.py |
| 0,0034 | imagenetv2/kosinus_ozet.json | c_tum[0][1] (IN_Salman2020Do_R18, IN_Salman2020Do_R50) |
| SD 0,0015; \|v\| < 0,02 oranı 1,000 | results/q1/konsey_b10_gradyan/imagenetv2/kosinus.npz | cos[:, (0,1)]; _ek_rapor_r18.py |
| 0,130; 0,240; 0,175 | imagenetv2/kosinus.npz | cos ortalamaları; _ek_rapor_r18.py |
| medyan norm 0,881; 0,833 | imagenetv2/kosinus.npz | norm; _ek_rapor_r18.py |
| −0,936 | mantel_imagenetv2.json | log_tau_matrisi[0][1] |
| 0,672; 0,898; 0,794; 0,910 | KY | IN_Salman2020Do_R18 ya da IN_Salman2020Do_R50 çıkarılınca ham ve artık Spearman |
| 0,927; 0,928; 0,972; 0,906; 0,720; 0,879; p 1e-04 | KY | c_iki_model_dogru ile ham ve artık Spearman, 9999 permütasyon |
| 0,905; 0,892; 0,888; 0,963; 0,929; 0,843 | KY | aile eşleşmesi ayıklanmış artık Spearman; yalnız CNN-CNN artık Spearman |
| −0,217; −0,225; −0,213; −0,179; −0,188; −0,192 | KY | S10-2 γ(ViT) − γ(ResNet), CIFAR-10 ve CIFAR-100 tohum çiftleri |
| −0,015; −0,029; +0,007 | KY | ImageNetV2 aynı tarifli çiftlerde γ(dönüştürücü) − γ(CNN) |
| 0,362; 0,365 | TR | J9 ve J2 b2.F_B2.K-a.simetrik_pay ortalaması |
| 0,069; 0,025 | TR | J9 ve J2 b2.F_B2.K-a.yonlu_pay ortalaması |
| −1,006; −1,009 | TR; J4 | J9 b2.F_B2.K-c.sigma_V ortalaması; J4 b4.F_B4.karsitliklar.H2.hucre_ort.V-scr |
| 762d62b4...; 75dbfeab... | b9_dondurulmus_b2.json; b9_sarmalayici_b2.json | sha256sum; _ek_rapor_b9_karsilastir.py (tek fark meta.uretildi_utc) |
| 07:09:00; 07:23:01 | results/q1/konsey_b9_c100/matris/cells_meta.json; results/q1/konsey_b8_imagenetv2/matris/cells_meta.json | dosya değişiklik zamanı (ls --time-style=full-iso) |
| 2893 MiB | raporlar/konsey_2026-10-29/10_konteyner_yeniden_kurulum.md | §1 (nvidia-smi, 06:57) |
| 57,60-64,85 | b8_betimsel.json | model_tablosu_ozet.<m>.temiz_dogruluk_yuzde (normalizasyon katmanı bulunmayan beş model) |
| 0,318 (10) | results/q1/konsey_b10_gradyan/mantel_imagenetv2.json | c_matrisi üst üçgen, HT8 aile ≠ CNN olan çiftlerin ortalaması 0,318452; arsiv/b2_yardimci/_ek_rapor_duzeltme.py (doğrulama turu) |
| −0,609; −0,217 | b9_dondurulmus_b2.json | b2.duyarlilik.yari_logit.rho_V.ci95 |
| satır 106-125 | scripts/ek_zincir_komutlari.sh | adim_cozumleme işlevi |
| 04:43:48Z; 04:43:51Z | b9_dondurulmus_b2.json; b8_dondurulmus_b2.json | meta.uretildi_utc (2026-10-31T04:43:48.044428+00:00; 2026-10-31T04:43:51.751189+00:00) |
| yaklaşık 4 s | TR | 04:43:51,751 − 04:43:48,044 = 3,7 s |
| 0,10 (bant); −0,20 (Liu beklenti eşiği) | experiments/q1_ek_ayrisim.py; experiments/q1_konsey_ayrisim.py; b8_betimsel.json | b8_etiket(…, esik, delta) satır 162-172; DELTA satır 58; A_sigma_scr_Liu.beklenti_esigi |
| ±0,012 | KY ve arsiv/b2_yardimci/_ek_rapor_aile_deger.py | sıra ölçeğinde 0,9047; 0,8923; 0,8878, değer ölçeğinde 0,9169; 0,8817; 0,8783; en büyük mutlak fark 0,0123 |
| 06ac9ff351aaaec729d5cc5c5cbf6ae857078c169ecb1fce92d4fb705504fe3a; 853429e1... | results/q1_research/ONKAYIT_SAPMALAR.md | sha256sum (doğrulama turu sonrası); head -38 \| sha256sum |

## Doğrulayıcı ile uyuşmazlık

Doğrulayıcının dokuz bulgusunun kanıtı kaynaktan yeniden okunmuş ve dokuzu da esas bakımından haklı bulunarak işlenmiştir. Yalnız üç bulguda önerilen düzeltme aynen değil, kanıta uydurularak uygulanmıştır ve gerekçeleri aşağıdadır.

Birinci bulguda doğrulayıcı B9 çözümlemesinin B8 çözümlemesinden "3 s önce" yapıldığını yazmaktadır. İki dosyanın `meta.uretildi_utc` alanları 2026-10-31T04:43:48.044428+00:00 ve 2026-10-31T04:43:51.751189+00:00'dır (J9, J8), fark 3,7 s'dir; raporda ve sapma kaydında bu nedenle "yaklaşık 4 s" yazılmıştır. Bulgunun özü, yani EK §10 madde 2'deki sıradan kayda geçmemiş ayrılık, aynen kabul edilmiştir.

Dördüncü bulguda önerilen cümle eklenmiştir. Bununla birlikte raporun ±0,10 okuması yalnız EK §11 tablosunun lafzına değil, sonuç görülmeden dondurulmuş koda da dayanmaktadır: kod ekindeki `experiments/q1_ek_ayrisim.py` (`d264c4e5...`, koşudan sonra da aynı) içinde `b8_etiket` işlevi ihmal edilebilirlik bandını dondurulmuş betiğin `DELTA` sabitiyle (0,10), beklenti eşiğini ise ayrı bir `esik` bağımsız değişkeniyle denetler ve B8B `A_sigma_scr_Liu.betimsel_etiket` = "belirsiz" bu işlevin çıktısıdır. ±0,20 okuması bu yüzden ön kayıtlı uygulamanın değil, metnin olası ikinci okumasının sonucudur; dipnotta da böyle adlandırılmalıdır.

Sekizinci bulgu, sapma kaydının 30.10.2026 tarihli indirme kaydındaki eskimiş 15. satırın altına bir gönderme notu düşülmesini önermektedir. Sapma kaydı yalnız sona ekleme yapılan bir kayıttır ve §6'da ilk 38 satırın özetinin değişmediği beyan edilmiştir; 15. satırın altına satır eklemek hem 30.10 kaydının bütünlüğünü hem de bu denetlenebilir özelliği bozardı. Gönderme notu bu yüzden 31.10.2026 tarihli ek ön kayıt başlığına 9. madde olarak yazılmıştır; ilk 38 satırın özeti `853429e1...` olarak kalmıştır.

## Düzeltme notu (31.10.2026)

§7'de ve sayı kaynak dizininde yalnız CNN-CNN çiftleriyle sınırlanan artık Spearman için ImageNetV2 değeri 0,843 olarak yazılmıştır. Hakem paneli sonrası aynı çözümleme `experiments/q1_ek_masa.py` (`--mod kesifsel`) ile permütasyonlu olarak yeniden üretilmiş ve doğru değerin 0,842 olduğu görülmüştür (tam matris artığı, tek yönlü p 3,0×10⁻⁴; `results/q1/konsey_ek_masa/kesifsel.json`, `veri.imagenetv2.cnn_cnn_artik_spearman`; föy M11.3, satır 2192). CIFAR-10 ve CIFAR-100 değerleri (0,963 ve 0,929) ile aile ayıklamalı artık Spearman değerleri (0,905, 0,892 ve 0,888) yeniden üretimle aynıdır (föy M11.3, satır 2182-2184 ve 2190-2191). Raporun özgün metni değiştirilmemiştir; makaleye 0,842 girmiştir.
