# B0 masa çözümlemeleri: ön kayıtlı betik, regresyon, sahte 2x2 ve altı masa çözümlemesi (29.10.2026)

Hazırlayan: deney analisti (opus alt ajan, B0 bloğu). GPU kullanılmamış, yeni ölçüm yapılmamıştır. Bütün girdiler `results/c1_c3/*` ve `results/q1/*` altındaki örnek bazlı npz dosyalarıdır; karantinadaki klasörlerden sayı alınmamıştır. Bu rapordaki her sayının yanında kaynak dosya ve JSON anahtarı verilmiştir. Kısaltmalar: AYRIŞIM = `results/q1/konsey_masa/konsey_ayrisim_masa.json`, MASA = `results/q1/konsey_masa/konsey_masa_cozumlemeleri.json`, SAHTE = `results/q1/konsey_sahte_2x2_sinama.json`, SENTEZ = `results/q1/konsey_sentez_r_tau_masa.json`.

En önemli üç nokta şunlardır. Birincisi, ön kayıtlı çözümleme betiği SENTEZ'in 223 sayısal değerini en çok 7,8e-16 farkla yeniden üretmektedir; sahte 2x2 sınaması da B2 ve B4 kod yollarının uçtan uca çalıştığını ve eksik hücrelerin doğru raporlandığını göstermiştir. İkincisi, masada yönlü terimin ölçeğe bağlı olduğu görülmüştür: havuzda ViT-Tiny'nin ρ değeri log ölçekte +0,043 iken logit ölçekte −0,265'tir ve ResNet ile ViT arasındaki ρ farkı işaret değiştirmektedir; simetrik oran ise iki ölçekte de 0,93'ün üstündedir. Bu durum H3'ün ve K-b'nin logit duyarlılığında farklı sonuç verebileceği anlamına gelir. Üçüncüsü, ön kayıt taslağı ile fable kararı K3 arasında doğrudan bir çelişki vardır (R224-scr hücresinin normalizasyonu) ve taslakta dondurmadan önce kapatılması gereken on dokuz tanım ya da ölçüt boşluğu bulunmuştur (Bölüm 6). Ön kayıttaki öngörülere dokunulmamıştır.

## 1. Yazılan dosyalar ve betiğin yaptığı iş

| Dosya | İş |
|---|---|
| `experiments/q1_konsey_ayrisim.py` (SHA-256 `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`) | Ön kayıtlı çözümleme; arayüz K6 |
| `raporlar/konsey_2026-10-29/hucre_tablosu.json` (SHA-256 `2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500`) | K5'teki 20 takma ad: hücre, tohum, aile, birincil ve ikincil panel üyeliği, B2 tohum çiftleri, S4 eşleşik çiftleri |
| `experiments/q1_konsey_sahte_sinama.py` | Sahte 2x2 uçtan uca sınama ve istatistik yardımcılarının birim sınamaları |
| `experiments/q1_konsey_masa.py` | Plan §5 masa çözümlemeleri (1)-(5) |
| `experiments/q1_konsey_masa_yeniden_kos.py` | Planda sayı kaynağı olarak anılan `_p3_*` betiklerini çıktıları `results/q1/konsey_masa/` altına yazacak biçimde yeniden koşar ve eskiyle karşılaştırır |

Betik, ON_KAYIT §2'deki tanımları birebir uygular. T_ij hedef-doğru koşullu yanıltma oranıdır (yüzde), w_j = T_jj, r_ij = log(T_ij/T_ji) − log(w_j/w_i), log τ̄_ij = ½[log(T_ij T_ji) − log(w_i w_j)]; model düzeyinde σ_m, ρ_m, ω_m ve yalnız betimsel S_m panel P üzerinden ortalanır. Birincil kestirim bölünmüş yarıdır: w çift indeksli, T tek indeksli görüntülerden ve tersi hesaplanır, iki yarının değeri ortalanır. Tam örneklem, logit ve oran ölçekleri duyarlılık olarak aynı kod yolundan geçer. Logit ve oran ölçeklerinde r ve τ̄ formüllerinde log yerine sırasıyla logit(T/100) ve T konmuştur (bu tanım ön kayıtta yoktur, Bölüm 6 madde 9).

`--mod b2` K-a (simetrik oran q_s için tek yönlü t, H0: ort q ≤ 0,50), K-b (ρ(V-scr) için TOST ±0,10) ve K-c (tür içi benzerlik Δ_w için tohum ve görüntü üzerinden hiyerarşik bootstrap, B = 2000) sınamalarını yapar, üç p değerine Holm düzeltmesi uygular ve ön kayıttaki destek, çürütme ve kararsız kurallarını yazar. Duyarlılık olarak tam örneklem, logit ve oran ölçekleri, panel üyesi bırakmalı jackknife ve ikincil panel (XCiT) verilir; C1 ResNet tohumları arasındaki log τ̄ betimsel olarak eklenir. `--mod b4` H1 (tek yönlü), H2 (iki yönlü, logit işaret koşuluyla) ve H3 (TOST) karşıtlıklarını dört hücrenin birleşik varyansıyla (hücreler 3, 2, 2, 2 iken df 5) hesaplar, Holm uygular, kararları ve ON_KAYIT §6 sonuç bölgesini yazar. Duyarlılık olarak tam örneklem, logit, oran, Welch-Satterthwaite aralıkları, panel jackknife ve hiyerarşik bootstrap (hücre içinde koşular, görüntüler ortak ağırlıkla, B = 2000) verilir. İkincil S1-S7 maddeleri keşifsel etiketiyle, çoklu düzeltme yapılmadan hesaplanır; S5 protokol oranlarını `src/analysis/protokoller.py` üzerinden alır. Birden çok `--matris-dizini` birleştirilir; aynı (kaynak, hedef) hücresi iki klasörde varsa ilki kullanılır ve iki kopyanın özdeş olup olmadığı çıktıya yazılır. Aynı hedefin temiz-doğru maskesinin bütün kaynak dosyalarında aynı olması, görüntü sırasının ortak olduğunu denetlemek için ayrıca sınanır. Birincil panelde beşten az üye varsa (`--panel-en-az`, varsayılan 5) B2 ve B4 sınaması yapılmaz ve hata yazılır. `--mod masa` her klasörü kendi bağlamında çözümler; eski takma adları K5 adlarına çeviren eşleme tablosu (`HAVUZ_ESLEME`, `cift_esleme`) betiğin içindedir. Havuz için eşleme `scripts/q1_temiz_ve_havuz_run.sh:26-35`'teki `--rb-model AD:TAKMA_AD` satırlarından alınmıştır; havuzdaki ResNet ve ViT'nin s1001 ve s2001 kontrol noktaları olduğu aynı satırlardan doğrulanmıştır.

Hücre tablosunda B2 tohum çiftleri C1 numaralandırmasıdır (1001-2001, 1002-2002, 1003-2003). S4 ve S5 için "tohum indeksiyle eşleşmiş çiftler" açık bir listeye çevrilmiştir: (R224_scr_s1201, ViT_Tiny_AT_s2001), (R224_scr_s1202, ViT_Tiny_AT_s2002), (R224_IN_s1301, V_IN_s2101), (R224_IN_s1302, V_IN_s2102). Bu seçimle V-scr'nin 2003 tohumu S4 ve S5'e girmez; bu bir yorum olduğundan dondurmadan önce onaylanmalıdır.

Yeni modellerin kontrol noktası yolları K5'e göre `models/q1/konsey/<takma ad>/` olarak yazılmıştır. Plan §7'deki komut taslağı ise `models/q1/konsey/vit_in1k_s2101` gibi başka bir adlandırma kullanmaktadır; kuyruk betiği K5 adlarına çekilmelidir.

## 2. Regresyon: `--mod masa` ile SENTEZ'in yeniden üretimi

Komut (konteynerde, depo kökünden): `python experiments/q1_konsey_ayrisim.py --mod masa --matris-dizini results/q1/havuz_cifar10 --matris-dizini results/c1_c3/pair{1,2,3} --matris-dizini results/q1/son_kontrol_noktasi/pair{1,2,3} --matris-dizini results/q1/cifar100/transfer/pair{1,2,3} --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json --cikti results/q1/konsey_masa/konsey_ayrisim_masa.json` (süre 2,1 s).

Sonuç: SENTEZ'teki 223 sayısal yaprağın tamamı karşılaştırılmış, en büyük mutlak fark 7,77e-16 bulunmuş, SENTEZ'te olup yeni çıktıda olmayan anahtar kalmamıştır (AYRIŞIM `regresyon.karsilastirilan` = 223, `regresyon.en_buyuk_mutlak_fark`, `regresyon.gecti` = true). Görüntü bootstrap'ı SENTEZ'teki RNG sırasıyla (`default_rng(0)`, B = 300) birebir yeniden kurulduğundan o satırlar da sıfır farkla tutmuştur. Bölüm bazında özet aşağıdadır; satır satır tablo `regresyon.satirlar` içindedir.

| SENTEZ bölümü | Yaprak | En büyük mutlak fark |
|---|---|---|
| `kumeler.c10_c1_secilen` (tam örneklem, bölünmüş yarı, bootstrap) | 53 | 0 |
| `kumeler.c10_son_kontrol_noktasi` | 53 | 0 |
| `kumeler.c100_c1_secilen` | 53 | 0 |
| `havuz_tohum1.ViT_Tiny_AT`, `.ResNet18_AT`, `.Debenedetti2022_XCiT_S12` | 30 | 0 |
| `havuz_tohum1.panel_ici_log_tau`, `.ResNet18_ViT_cifti` | 17 | 0 |
| `havuz_tohum1.kaynak_acigi_ayristirma_log` | 5 | 7,8e-16 |
| `havuz_tohum1.hedef_farki_ayristirma_log` | 5 | 3,3e-16 |
| `kesinlik_plani` | 7 | 0 |

Seçilmiş değerler (SENTEZ ile yeni çıktı aynıdır): `kumeler.c10_c1_secilen.tam_orneklem.r.ort` 0,114669, `.r.sd_kosum` 0,010389, `.bolunmus_yari.r.ort` 0,114590; `havuz_tohum1.ViT_Tiny_AT.log_tau_ort` −1,085928, `.r_ort` +0,042927; `havuz_tohum1.Debenedetti2022_XCiT_S12.r_ort` −0,095199; `havuz_tohum1.kaynak_acigi_ayristirma_log.simetrik_oran` 0,927983; `kesinlik_plani.yari_genislik_r_2e2` 0,020935. SENTEZ'in kesinlik planında kullandığı t_0,95(df 5) = 2,015 yuvarlanmış değerdir; kesin değer 2,01505'tir (AYRIŞIM `sentez_uyumlu.kesinlik_plani.t_0.95_df5_kesin`), fark yarı genişliklerde 1e-5 mertebesindedir.

Havuzda ön kayıtlı birincil kestiriciyle (bölünmüş yarı) elde edilen değerler SENTEZ'in tam örneklem değerlerinden en çok 0,001 farklıdır: ViT için σ −1,0862 (tam örneklem −1,0859), ρ +0,0434 (+0,0429), kaynak açığı D 0,4227, simetrik pay 0,3920, yönlü pay +0,0308, q 0,927 (AYRIŞIM `havuz_on_kayit_tanimlari.b2_nokta_tohum1.yari_log` ve `.tam_log`). Havuzdaki dört panel üyesi ön kaydın en az beş üye koşulunu sağlamaz (`panel_en_az_saglaniyor_mu` = false); bu değerler sınama değil, ON_KAYIT §1'de beyan edilen görülmüş veridir. Bütün havuz hedeflerinde temiz-doğru maskesi kaynaklar arasında tutarlıdır (`baglamlar.havuz_cifar10.tutarlilik`).

## 3. Sahte 2x2 uçtan uca kod sınaması

Bu bölümdeki sayılar SONUÇ DEĞİLDİR; hücre etiketleri sahtedir. SAHTE dosyasının en üst anahtarı `SINAMA_SONUC_DEGIL: true`'dur. Kurgu şöyledir: `results/c1_c3/pair1-3` (seçilen kontrol noktası) ve `results/q1/son_kontrol_noktasi/pair1-3` (son kontrol noktası) birleştirilmiş, ResNet ve ViT kontrol noktaları geçici takma adlarla hücrelere yerleştirilmiştir. V-scr gerçek C1 ViT'leridir (2001-2003, seçilen); sahte V-IN iki ViT'nin son kontrol noktası, sahte R224-scr iki ResNet'in seçilen, sahte R224-IN iki ResNet'in son kontrol noktası, C1-R32 ise s1003'ün seçilen ve son kontrol noktasıdır. Bu klasörlerde ortak tek panel üyesi Gowal2020Uncovering_28_10_extra olduğundan sınama `--panel-en-az 1` ile koşulmuştur. Sahte hücre tablosu `results/q1/_konsey_sahte/sahte_hucre_tablosu.json` içindedir.

| Denetim | Sonuç | Anahtar |
|---|---|---|
| Holm, bilinen örnek (0,01; 0,04; 0,03 → 0,03; 0,06; 0,06) | geçti | `birim_sinamalari.holm` |
| Birleşik varyanslı iki hücre karşıtlığı = `scipy.stats.ttest_ind` (eşit varyans) | geçti (fark < 1e-12) | `birim_sinamalari.birlesik_t` |
| Welch karşıtlığı = `ttest_ind(equal_var=False)` | geçti | `birim_sinamalari.welch` |
| 3, 2, 2, 2 hücrede etkileşim çarpanı √(1/3 + 3/2) ve df 5 | geçti | `birim_sinamalari.etkilesim_carpani` |
| TOST p < 0,05 ile %90 aralığın ±0,10 içinde olması denk | geçti | `birim_sinamalari.tost_aralik_denkligi` |
| Kaynak açığı özdeşliği D = Δσ − ½Δρ | artık en çok 5,6e-16 | `ozdeslik_artik_max_Ka` |
| Gowal→Gowal hücresi altı klasörde; ilki kullanıldı, beşi özdeş | 5/5 özdeş | `b2.veri.cakismalar` |
| Hedef maskesi tutarlılığı | tutarlı | `b2.veri.tutarlilik` |
| K-c (ViT tohumları arası hücre yok) | "hesaplanamadi", eksik hücreler listelendi | `b2.b2.F_B2.K-c.eksik_hucreler` |
| K-c kod yolu (tek klasörde iki model sahte V-scr) | bootstrap ve karar üretildi | `b2_kc_yolu.b2.F_B2.K-c` |
| B4: H1-H3, Holm, karar, sonuç bölgesi, Welch, hiyerarşik bootstrap | üretildi | `b4.b4.F_B4`, `b4.b4.duyarlilik` |
| S1-S7 | S1-S5 ve S7 üretildi; S6 eksik hücreyi raporladı (sahte ikincil üye) | `b4.b4.ikincil` |

Kodun kendi içinde tutarlılığını gösteren iki ek kontrol yapılmıştır. Sahte S4'teki (SAHTE_R224_scr_a, ViT_Tiny_AT_s2001) çiftinin tam örneklem r'si 0,1189'dur ve SENTEZ'teki C1 çift 1 değeri (0,11886) ile aynıdır; sahte K-c yolundaki tür içi log τ̄ (−1,0997) SENTEZ'in çift 1 bölünmüş yarı log τ̄'sı (−1,09974) ile aynıdır. Sınama iki kod kusurunu ortaya çıkarmış ve bunlar düzeltilmiştir: tek üyeli panelde panel üyesinin kendi satırı ve panel jackknife'ı boş panelle çöküyordu. Sahte koşunun sayıları (örneğin sahte H1 kestirimi −0,335) hiçbir hipotez için kanıt değildir ve hiçbir metne girmemelidir.

Sınamanın kapsamadığı iki yol vardır. Birincisi, gerçek beş ya da yedi üyeli panelle B2 ve B4; bunun verisi B2 koşulmadan oluşmaz. İkincisi, K-c bootstrap'ının üç tohumlu davranışı; sahte K-c yolunda yalnız iki tohum vardı ve yerine koyarak çekilen tohumların yarısı aynı tohuma düştüğü için 2029 kez yeniden çekim yapılmıştır (`b2_kc_yolu.b2.F_B2.K-c.bootstrap.yeniden_cekilen_tek_tohumlu_ornek`).

## 4. Altı masa çözümlemesi

### (1) Havuzun yedi AT modelinde σ, ρ, ω, S ve kaynak açığı

Panel dört IN ön eğitimsiz gürbüz CNN'dir (Wong2020Fast, Engstrom2019Robustness, Carmon2019Unlabeled, Gowal2020Uncovering_28_10_extra); her model için kendisi panelden çıkarılmıştır. Kaynak açığı D = S(ResNet18_AT_s1001) − S(m), iki model için ortak olan P ∖ {m, ResNet} paneli üzerinde hesaplanmıştır; böylece özdeşlik her satırda kesin tutar. Kaynak: MASA `1_havuz_model_tablosu.modeller.<model>.yari_log`, `.yari_logit` ve `.kaynak_acigi_R_eksi_m_yari_log`.

| Model | σ (log) | ρ (log) | w (%) | σ (logit) | ρ (logit) | D | Simetrik pay | Yönlü pay | q (log) | q (logit) |
|---|---|---|---|---|---|---|---|---|---|---|
| ResNet18_AT_s1001 | −0,694 | −0,018 | 47,56 | −0,994 | −0,170 | | | | | |
| ViT_Tiny_AT_s2001 | −1,086 | +0,043 | 55,83 | −1,534 | −0,265 | 0,423 | 0,392 | +0,031 | 0,927 | 1,097 |
| Wong2020Fast | −0,656 | −0,033 | 42,10 | −0,902 | −0,147 | −0,078 | −0,075 | −0,003 | 0,961 | 1,339 |
| Engstrom2019Robustness | −0,566 | −0,058 | 37,68 | −0,777 | −0,114 | −0,147 | −0,136 | −0,012 | 0,921 | 1,258 |
| Carmon2019Unlabeled | −0,519 | +0,008 | 28,68 | −0,698 | +0,071 | −0,140 | −0,152 | +0,012 | 1,087 | 1,674 |
| Debenedetti2022Light_XCiT-S12 | −0,609 | −0,096 | 32,76 | −0,815 | −0,103 | −0,124 | −0,085 | −0,039 | 0,688 | 1,232 |
| Gowal2020Uncovering_28_10_extra | −0,521 | +0,083 | 25,25 | −0,693 | +0,191 | −0,114 | −0,152 | +0,039 | 1,341 | 2,137 |

Panel üyelerinin satırları üç üyeli panelden hesaplanmıştır (ResNet ve kendisi çıkınca). ViT için kaynak açığının simetrik oranı log ölçekte 0,927'dir; panel üyesi bırakmalı jackknife'ta 0,919 ile 0,935, σ −1,119 ile −1,071, ρ +0,031 ile +0,070 arasında kalmaktadır (MASA `1_havuz_model_tablosu.jackknife_aralik.ViT_Tiny_AT_s2001`). Bu oran, açığın büyük olduğu tek model olan ViT için kararlıdır. XCiT'te oran 0,43 ile 0,80 arasında oynamaktadır, çünkü açık küçüktür (D = −0,124) ve oran paydası küçük olduğunda kararsızdır. Panel üyelerinin q değerleri de aynı nedenle 0,92 ile 1,34 arasında dağılmaktadır.

Bu tablonun en önemli sonucu ölçek bağımlılığıdır. Simetrik pay her iki ölçekte açığın neredeyse tamamını taşır (ViT için q 0,93 ve 1,10); ancak yönlü terimin işareti log ile logit arasında değişir. ViT'nin ρ değeri log ölçekte +0,043 (yönlü olarak zayıf kaynak), logit ölçekte −0,265'tir (yönlü olarak güçlü kaynak) ve ResNet ile farkı ρ_V − ρ_R log ölçekte +0,061, logit ölçekte −0,095'tir. Oran ölçeğinde ViT'nin ρ değeri −14,2 puandır (AYRIŞIM `havuz_on_kayit_tanimlari.b2_nokta_tohum1.yari_oran.rho_V`). Bunun nedeni w'nin 25-56 aralığında değişmesi ve logit dönüşümünün bu aralıkta log'dan farklı eğrilik taşımasıdır. Ön kayıt logiti yalnız duyarlılık sayar ve H2 desteğine logit işaret koşulu koyar; H3 ve K-b için ise logit duyarlılığının yönü değiştirebileceği bu masada görülmüştür. Bu gözlem öngörüleri değiştirme gerekçesi değildir, ama "küçük yönlü terim" cümlesinin ölçeğe göre nitelenmesi gerektiğini gösterir.

### (2) r matrisinin Hodge ayrışımı

Yedi AT modelinde bölünmüş yarı ile hesaplanan r matrisinde potansiyel payı G 0,940'tır, görüntü bootstrap %95 aralığı 0,870 ile 0,961 arasındadır ve rastgele ters-simetrik matris beklentisi 2/K = 0,286'dır. Dolaşımın RMS değeri 0,0221, aynı bootstrap'tan kestirilen örnekleme gürültüsü 0,0126'dır (oran 1,75; dolaşım serbestliği 15). C1 çiftinde r_RV = 0,1192'nin 0,0802'si model potansiyeli farkı (δ_R − δ_V), 0,0390'ı dolaşımdır. Kaynak: MASA `2_hodge_r.yari_log.G_potansiyel_payi`, `.G_bootstrap_95`, `.dolasim_rms`, `.dolasim_gurultu_rms`, `.RV_cifti`. Model potansiyelleri δ şöyledir: ViT −0,072 (SD 0,019), Gowal2020 −0,073, Carmon2019 −0,011, ResNet +0,008, Wong2020 +0,015, Engstrom2019 +0,029, XCiT +0,104 (`2_hodge_r.yari_log.delta_potansiyel`, `.delta_bootstrap_sd`). Tam örneklemle değerler 0,001 içinde aynıdır.

Plan §1 ve §5(2), "r_RV 0,119 iken model düzeyi fark ρ_V − ρ_R 0,061'dir, yarısı çifte özgüdür" demektedir. Hodge ayrışımı bu payı yaklaşık üçte bir (0,039/0,119) olarak vermektedir; fark, ρ'nun yalnız dört CNN'lik panel üzerinden, Hodge potansiyelinin ise XCiT dahil yedi modelin tamamı üzerinden ortalanmasından gelir. İki sayı aynı soruya farklı referans kümesiyle yanıt verdiğinden metinde hangisinin kullanılacağı tanımıyla birlikte yazılmalıdır. Logit ölçekte G 0,971'dir, ama r_RV 0,006'ya iner ve potansiyel farkı −0,064 ile işaret değiştirir (`2_hodge_r.yari_logit.RV_cifti`); bu, (1)'deki ölçek bağımlılığının çift düzeyindeki karşılığıdır.

### (3) Mahmood ve ark. 2021, 8x8 dış karşılaştırma

Bu veri her-ikisi-doğru protokolündedir (m = 1000), modeller standart eğitimlidir ve köşegen beyaz kutu değil, bağımsız eğitilmiş ikinci kopyaya transferdir (`results/q1/dis_veri/mahmood2021_tablolar.json`, `kosegen_notu`). w bu yüzden tanımsızdır ve ön kayıtlı w-τ̄-r ayrışımı bu veride kurulamaz; bu olumsuz sonuç açıkça kaydedilmiştir. Kurulabilen nicelikler yalnız T'den gelen log asimetri ile simetrik geometrik ortalamadır. Köşegeni vekil w sayan bir ayrışım da hesaplanmış, fakat beyaz kutu anlamında okunamayacağı etiketlenmiştir (MASA `3_mahmood.etiket`).

| Nicelik (CIFAR-10; CIFAR-100) | Değer | Anahtar |
|---|---|---|
| Log asimetri Hodge G | 0,973; 0,961 (2/K = 0,25) | `3_mahmood.<ds>.log_asimetri_hodge.G_potansiyel_payi` |
| Log geometrik ortalama, ViT-ViT | 4,278; 4,401 | `.log_geometrik_ortalama_aile.ViT-ViT.ort` |
| Aynı, CNN-CNN | 3,058; 3,035 | `.CNN-CNN.ort` |
| Aynı, CNN-ViT | 2,691; 3,108 | `.CNN-ViT.ort` |
| Vekil ayrışım, ViT ailesi ort. σ ve ρ (CNN paneli) | −1,850 ve −1,276; −1,406 ve −0,187 | `.aile_ortalamasi_vekil` |

CIFAR-10'da CNN-ViT benzerliği CNN-CNN ve ViT-ViT'nin altındadır; bu, bizim AT havuzundaki simetrik benzemezlik okumasıyla aynı yöndedir. CIFAR-100'de ise CNN-ViT (3,108) CNN-CNN'in (3,035) altında değildir, yani bu yön veri kümesine göre değişmektedir. Standart eğitimde ViT'ler net güçlü kaynaktır (CIFAR-10'da δ ViT-B-32 +0,907, BiT-M-R50x1 −1,378; `3_mahmood.CIFAR-10.log_asimetri_hodge.delta`) ve vekil ρ negatiftir. Mahmood verisi standart rejimde ve köşegeni beyaz kutu olmadığından ön kayıtlı tanımlarla doğrudan karşılaştırılamaz; yalnız dış bağlam olarak kullanılabilir. Tablo 2'nin yön kuralında makale metniyle çelişki notu kaynak dosyada kayıtlıdır (`yon_dogrulamasi`); transpoz G'yi ve simetrik ortalamayı değiştirmez, δ ve vekil ρ'nun işaretini çevirir.

### (4) Potansiyel payı tablosu (ResNet→ViT çifti)

Potansiyel payı log(w_V/w_R)/log(T_RV/T_VR)'dir. Kaynak: MASA `4_potansiyel_payi.ozet.<küme>`; çift değerleri `4_potansiyel_payi.ciftler`.

| Küme | Çift | Log asimetri ort. (SD) | Potansiyel payı ort. (SD) | r ort. (SD) | r çift değerleri |
|---|---|---|---|---|---|
| CIFAR-10 L∞, seçilen | 3 | 0,251 (0,032) | 0,541 (0,029) | 0,115 (0,010) | 0,119; 0,122; 0,103 |
| CIFAR-10 L∞, son kontrol noktası | 3 | 0,273 (0,029) | 0,531 (0,134) | 0,129 (0,044) | 0,084; 0,130; 0,172 |
| CIFAR-10 L2, seçilen | 3 | 0,279 (0,022) | 0,500 (0,157) | 0,139 (0,044) | 0,094; 0,142; 0,181 |
| CIFAR-100 L∞, seçilen | 3 | 0,215 (0,048) | 0,283 (0,087) | 0,154 (0,041) | 0,141; 0,122; 0,200 |
| SVHN L∞, seçilen | 2 | −0,038 (0,009) | −1,421 (0,002) | −0,091 (0,021) | −0,106; −0,076 |

Bölünmüş yarı payları tam örneklemden en çok 0,001 farklıdır (`potansiyel_payi_bolunmus_yari`). SVHN'de log asimetri ters işaretlidir ve r her iki çiftte negatiftir; payın −1,42 çıkması oranın küçük paydayla tanımsızlaşmasındandır ve yorumlanmamalıdır. SVHN satırı, yönlü terimin üç CIFAR kümesinde pozitif olduğunu ama veri kümesine göre işaret değiştirebildiğini gösteren olumsuz bir sonuçtur. ResNet→WRN ve ViT→WRN çiftlerinin değerleri de `ciftler` altında verilmiştir; örneğin CIFAR-10 seçilen çiftlerde ViT→WRN r'si 0,035, 0,042 ve 0,078'dir.

### (5) Önerme 3'ün h ölçeği sınaması C1 3x3'lerde

`_p3_potansiyel_masa.py`'nin `ayar_testi` fonksiyonu değiştirilmeden C1 3x3 matrislerine uygulanmıştır. K = 3'te toplamsal uydurmanın bir, Hodge dolaşımının bir serbestliği vardır; bu yüzden sonuçlar havuzdakinden zayıf bir sınamadır. Kaynak: MASA `5_onerme3_h_olcegi.kumeler.<küme>/pairk`.

| Küme | En büyük g | Kaynak etkisi farkı (ham − tc) / tc SD, h ölçeği | Aynı, oran ölçeği | bc − tc / tc SD, h ölçeği |
|---|---|---|---|---|
| CIFAR-10 seçilen, çift 1-3 | 0,0012-0,0018 | 0,008-0,013 | 0,134-0,141 | 0,444-0,574 |
| CIFAR-10 son kontrol noktası | 0,0016-0,0032 | 0,007-0,015 | 0,132-0,137 | 0,217-0,336 |
| CIFAR-10 L2 | 0,0006-0,0009 | 0,005-0,010 | 0,132-0,138 | 0,162-0,291 |
| CIFAR-100 seçilen | 0,0077-0,0104 | 0,020-0,035 | 0,372-0,379 | 0,021-0,136 |

Önerme 3'ün öngördüğü desen C1 3x3'lerde de tutmaktadır: h ölçeğinde ham ile hedef-doğru arasındaki kaynak etkisi farkı tc kaynak etkilerinin yayılımının %0,5-3,5'i iken oran ölçeğinde %13-38'idir; bc ise bir ayar dönüşümü değildir (h ölçeğinde %2-57). Havuzdaki karşılıkları %1,6 ve %31,6'dır (`results/q1/konsey_masa/_p3_potansiyel_masa.json`, `havuz_cifar10.ayar_testi.h` ve `.oran`).

### (6) Ön kayıtlı betiğin havuz regresyonu

Bölüm 2'de verilmiştir: 223 anahtar, en büyük fark 7,8e-16, geçti.

## 5. Planda anılan masa betiklerinin yeniden koşulması

Planda sayı kaynağı olarak anılan iki betik `_p3_carpimsal_yasa_masa.py` (w 55,83 ve 47,56, τ simetri ihlali RMS 0,0897, A kolu R² 0,201 ve λ 1,878) ile `_p3_potansiyel_masa.py`'dir (en büyük |g| 0,0044, oran 0,316). Birincisi A kolu için `_p3_yorunge_gurbuzluk_masa.json`'u okuduğundan o da yeniden koşulmuştur. Betik dosyalarına dokunulmamış; `experiments/q1_konsey_masa_yeniden_kos.py` kaynak metni okuyup yalnız çıktı (ve çarpımsal betikte yörünge girdisi) yolunu ikame ederek ve ikame sayısını denetleyerek çalıştırmıştır. `_P2_*.py`, `_p3_havuz_gurbuzluk_yasasi.py` ve `_rb_*.py` planda sayı kaynağı olarak anılmadığından yeniden koşulmamıştır (`_rb_liste.json` yalnız model adlarının satır numarası için anılır).

| Betik | Sayısal yaprak | En büyük mutlak fark (zaman damgası hariç) | Anahtar seti | Yeni çıktı |
|---|---|---|---|---|
| `_p3_yorunge_gurbuzluk_masa.py` | 1715 | 4,3e-14 | aynı | `results/q1/konsey_masa/_p3_yorunge_gurbuzluk_masa.json` |
| `_p3_carpimsal_yasa_masa.py` | 411 | 4,4e-16 | aynı | `results/q1/konsey_masa/_p3_carpimsal_yasa_masa.json` |
| `_p3_potansiyel_masa.py` | 4282 | 1,1e-13 | aynı | `results/q1/konsey_masa/_p3_potansiyel_masa.json` |

Kaynak: `results/q1/konsey_masa/yeniden_kos_karsilastirma.json`, `isler.<betik>.karsilastirma_uretildi_utc_haric`. Farklar kayan nokta düzeyindedir (eski çıktılar büyük olasılıkla başka bir numpy sürümüyle üretilmiştir; konteynerde 1.26.4); bootstrap'lı potansiyel betiği de aynı RNG sırasını vermiştir. Plan ve ön kayıtta anılan değerler yeni yollarda aynıdır: `havuz_AT7.w_beyaz_kutu` ViT 55,830 ve ResNet 47,558, `havuz_AT7.log_tau_simetri_ihlali_rms` 0,08967, `A_kolu.R2_lambda_1` 0,2011, `A_kolu.lambda_kesisimsiz` 1,8780, `havuz_cifar10.ayar_testi.g_mutlak_en_buyuk` 0,004393, `havuz_cifar10.ayar_testi.oran.kaynak_alfa_raw_eksi_tc_bolu_tc_alfa_SD` 0,3163. Karantina kuralı açısından plan ve ön kayıttaki `raporlar/konsey_2026-10-29/_p3_*.json` atıfları bu yeni `results/q1/konsey_masa/` yollarına çevrilmelidir. Yeni çıktıların içindeki `betik` alanı özgün betik yolunu göstermeye devam eder; ikame kaydı karşılaştırma dosyasındadır.

## 6. Ön kayıt taslağı ile betik arasındaki uyuşmazlıklar ve boşluklar

Aşağıdakilerin hiçbiri ön kayıt metninde değiştirilmemiştir; betik her birinde metnin harfiyen okunuşunu uygulamış, belirsiz durumda iki okumayı da çıktıya yazmıştır. Dondurmadan önce ana oturumun karar vermesi gerekir.

1. Fable kararı K3 ile çelişki. ON_KAYIT §3 tablosu R224-scr için "model içi ImageNet normalizasyonu" yazar; KONSEY_PLANI §2 ve §4 B3 tablosu da aynı şeyi söyler. K3 ise R224-scr'nin V-scr ile birebir aynı girdi hattını (normalizasyonsuz) kullanacağını ve ImageNet normalizasyonunun yalnız IN hücrelerinde başlatma demetinin parçası olduğunu bağlar. Ayrıca ON_KAYIT §3'teki "V-scr'de girdi normalizasyonu yoktur; bu fark beyan edilir" cümlesi ve "başlatma etmeni ağırlık ile temiz aşama uzunluğunun demetidir" tanımı K3'e göre "ağırlık, temiz aşama uzunluğu ve normalizasyon" olarak genişlemelidir. Betik normalizasyona bakmaz; çelişki eğitim tarafındadır.
2. K-a'da öngörü (her tohumda q_s ≥ 0,75) ile destek ölçütü (ort q > 0,50, Holm sonrası) arasında boşluk vardır: ort q = 0,60 ve anlamlı bir sonuç "destek" sayılır ama öngörüyü tutturmaz. Betik iki bilgiyi ayrı yazar (`ongoru_her_tohumda_q_ge_0.75`).
3. K-a'da D_s sıfıra yakın ya da negatifse q_s tanımsız ya da anlamsızdır; kural yoktur. C1'de D yaklaşık 0,42 olduğundan beklenen bir sorun değildir, ama (1)'deki panel üyelerinde payda küçüldüğünde q'nun 0,69 ile 1,34 arasında dağıldığı görülmüştür.
4. K-b çürütme ölçütü "nokta kestirimi 0,10'u aşar" yalnız pozitif yönü kapsar; ρ = −0,20 ve anlamlı bir sonuç harfiyen "kararsız" olur. Betik mutlak değer okumasını ayrıca yazar (`K-b_mutlak_deger_okumasi_curutme`). (1)'deki logit bulgusu bu boşluğun gerçek bir olasılık olduğunu göstermektedir.
5. K-b ve H3'te destek "%90 aralık ±0,10 içinde" diye tanımlanmışken aile düzeyinde Holm uygulanacağı söylenir. Holm sonrası TOST p < 0,05, aralık ölçütünden daha katıdır. Betik kararı aralıkla verir, Holm sonucunu ayrı bayrakla yazar (`K-b_holm_tost_p_lt_0.05`, `H3_holm_tost_p_lt_0.05`); hangisinin bağlayıcı olduğu yazılmalıdır.
6. K-c'nin hiyerarşik bootstrap'ı üç tohumla yerine koyarak çekildiğinde aynı tohum iki kez gelebilir; aynı tohumun kendisiyle log τ̄'sı tanım gereği sıfırdır. Betik özdeş kökenli çiftleri dışarıda bırakır ve yalnız bir tohum çekilen örneği yeniden çeker (sayısı çıktıya yazılır). Üç tohumda yalnız on farklı çoklu küme vardır; aralığın tohum bileşeni bu yüzden kabadır. Bootstrap p'sinin çözünürlüğü 1/2001'dir. Öngörü (Δ_w ≥ +0,30) ile sınanan H0 (Δ_w ≤ 0) arasında K-a'dakine benzer bir boşluk vardır.
7. Bir F_B2 ya da F_B4 sınaması hesaplanamazsa (eksik hücre, n < 2) Holm ailesinin büyüklüğü tanımsızdır. Betik hesaplanabilenler üzerinden Holm uygular; ön kayıt, hesaplanamayan sınamanın p = 1 sayılıp ailede tutulacağını yazmalıdır.
8. H2 çürütmesindeki "negatif ve anlamlı" ifadesinin düzeyi (ham iki yönlü p ya da Holm sonrası) yazılmamıştır. Betik çürütmeyi ham p ile verir, Holm okumasını `H2_negatif_anlamli_holm` olarak ayrıca yazar.
9. Logit ve oran ölçeklerinde r ve τ̄ tanımı yoktur. H2'nin destek ölçütü logit işaretine bağlı olduğundan bu tanım birincil kararın parçasıdır. Betik log yerine logit(T/100) ve T koyar; ön kayda aynen yazılmalıdır.
10. ω_m'nin bölünmüş yarıda nasıl hesaplanacağı yazılmamıştır; ω yalnız w içerdiğinden betik tam örneklem w kullanır.
11. Panel üyesinin kendi σ ve ρ değerinde kendisinin panelden çıkarılacağı yazılmamıştır; betik çıkarır. Yalnız betimsel tabloyu etkiler.
12. Sonuç haritası (ON_KAYIT §6) ne ayrık ne kapsayıcıdır. O4 (H3 çürütüldü) O1-O3 ile birlikte gerçekleşebilir; "H1 destek, H2 kararsız, H3 eşdeğer" hiçbir bölgeye düşmez; H1'in "pozitif ve anlamlı" çürütme kolunun bölgesi yoktur. Betik eşleşen bütün bölgeleri yazar, hiçbiri eşleşmezse O5 der; öncelik sırası ve eksik bölgeler ön kayda eklenmelidir.
13. S1, S2 ve S3'te aralık yöntemi yazılmamıştır. Betik S1'de iki hücrenin birleşik varyansını (df = 3), S2 ve S3'te 2x2'nin dört hücreli birleşik varyansını (df 5) kullanır.
14. S4 ve S5 için "tohum indeksiyle eşleşmiş çiftler" hücre tablosunda açık listeye çevrilmiştir (Bölüm 1); V-scr'nin 2003 tohumu dışarıda kalır. Onay gerekir.
15. S5'te eğim ve kesişim FÖY'deki yuvarlanmış değerlerdir (+0,796, −0,01); "üç protokol yayılımı" `scripts/fig_yayilim_temiz_fark_veri.py`'deki tanımla (ham, hedef-doğru ve her-ikisi-doğru asimetrilerinin en büyüğü eksi en küçüğü, temiz farkın mutlak değeri) uygulanmıştır. Dört çiftle aralık df 3'tür.
16. Duyarlılık listesindeki "son kontrol noktası" için B4'te yeni altı modelin son kontrol noktası matrisi planlanmamıştır; bütçede yeri yoktur. Bu duyarlılık ya B4'e eklenmeli (yaklaşık 6 kaynak daha) ya da listeden çıkarılmalıdır. Betik ayrı bir çağrıyla, son kontrol noktası matrisleri verilirse aynı çözümlemeyi yapar.
17. B5'in korunma oranı G_best/G_PGD K6 arayüzünde bir mod olarak yoktur ve betikte uygulanmamıştır; aralık yöntemi (oran için) de ön kayıtta tanımsızdır. B5 başlamadan önce mod ya da ayrı betik ve aralık yöntemi eklenmelidir.
18. ON_KAYIT §1 ve plan §1'deki havuz sayıları tam örneklemdir, birincil kestirici ise bölünmüş yarıdır. Fark en çok 0,001'dir (Bölüm 2); metinde hangi kestiricinin kullanıldığı belirtilmelidir.
19. Kesinlik planındaki t_0,95(df 5) = 2,015 yuvarlanmış değerdir (kesin 2,01505); etkisi önemsizdir, betik scipy'nin kesin değerini kullanır.

Masadan çıkan ve öngörülerle ilgili ama öngörü değişikliği gerektirmeyen üç gözlem de kayda geçirilmelidir. Yönlü terim ölçeğe bağlıdır ((1) ve (2)); r_RV SVHN'de negatiftir ((4)); Hodge ayrışımı r_RV'nin çifte özgü payını plan metnindeki "yarısı" yerine yaklaşık üçte bir olarak verir ((2)).

## 7. Dondurma satırı için değerler

`experiments/q1_konsey_ayrisim.py` SHA-256: `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`. `raporlar/konsey_2026-10-29/hucre_tablosu.json` SHA-256: `2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500`. Bölüm 6'daki maddeler için betik değişirse karma yeniden alınmalı ve regresyon ile sahte sınama yeniden koşulmalıdır (ikisi birlikte 10 saniyenin altında sürer):

```
docker exec -w /workspace adeb_eval python experiments/q1_konsey_ayrisim.py --mod masa --matris-dizini results/q1/havuz_cifar10 --matris-dizini results/c1_c3/pair1 --matris-dizini results/c1_c3/pair2 --matris-dizini results/c1_c3/pair3 --matris-dizini results/q1/son_kontrol_noktasi/pair1 --matris-dizini results/q1/son_kontrol_noktasi/pair2 --matris-dizini results/q1/son_kontrol_noktasi/pair3 --matris-dizini results/q1/cifar100/transfer/pair1 --matris-dizini results/q1/cifar100/transfer/pair2 --matris-dizini results/q1/cifar100/transfer/pair3 --hucre-tablosu raporlar/konsey_2026-10-29/hucre_tablosu.json --cikti results/q1/konsey_masa/konsey_ayrisim_masa.json
docker exec -w /workspace adeb_eval python experiments/q1_konsey_sahte_sinama.py
docker exec -w /workspace adeb_eval python experiments/q1_konsey_masa.py
docker exec -w /workspace adeb_eval python experiments/q1_konsey_masa_yeniden_kos.py
```

Konteynerin yazdığı dosyalar `chown 1000:1000` ile firat'a verilmiştir. Bu iş sırasında depoda başka bir ajanın oluşturduğu root sahipli dosyalar görülmüştür (`models/timm_agirliklar/`, `models/q1/konsey_smoke/`, `cli/__pycache__/train.cpython-312.pyc`); bunlara dokunulmamıştır.

## Doğrulayıcı düzeltmeleri (ikinci tur, 29.10.2026)

Çelişik doğrulayıcının on yedi bulgusu bu turda ele alınmıştır. Ön kayıttaki öngörülere (sayısal öngörü değerleri ve beklenen yönler) dokunulmamış; değişiklikler tanım, karar kuralı ve kapsam düzeyinde kalmıştır ve her biri `ON_KAYIT_TASLAGI.md` içine yeni açılan §8 "Dondurma öncesi taslak değişiklik kaydı" bölümüne de yazılmıştır. Bu değişiklikler masa sonuçları ve smoke çıktıları görüldükten sonra yapıldığından ön kaydın §1'inde bu veriler listelenmiş, desteği zorlaştıran ya da çürütmeyi kolaylaştıran yöndeki değişiklikler orada ayrıca işaretlenmiştir. Bölüm 6'daki on dokuz maddenin büyük kısmı da bu turla kapanmıştır; kapanmayanlar aşağıda açıkça yazılıdır.

Betik ve hücre tablosu değiştiği için karmalar yenilenmiştir: `experiments/q1_konsey_ayrisim.py` SHA-256 `4bce2c983ace1d2ce877af7fa9406d3bdb5cd137f422bcd5f55b11d91b667389`, `raporlar/konsey_2026-10-29/hucre_tablosu.json` SHA-256 `2a891331f8c59897db14b30fb27a46c836ad391957aa4ff54a0ffef00bfe5500` (Bölüm 1 ve 7'deki eski karmalar bunlarla değiştirilmiştir). Regresyon yeniden koşulmuş ve SENTEZ'in 223 yaprağı yine en çok 7,77e-16 farkla üretilmiştir (AYRIŞIM `regresyon.karsilastirilan`, `.en_buyuk_mutlak_fark`, `.gecti` = true); karar kuralı değişiklikleri masa yolunu etkilememektedir. Sahte 2x2 sınaması da yeniden koşulmuştur (SAHTE, en üst anahtar `SINAMA_SONUC_DEGIL: true`); yeniden koşu komutları `results/q1/konsey_masa/_dogrulayici/tur2_kos.sh` içindedir.

1. K3 ile normalizasyon çelişkisi düzeltildi. ON_KAYIT §3 tablosunda R224-scr artık "V-scr ile birebir aynı girdi hattı (32→224 bilinear büyütme, [0, 1] değer aralığı, normalizasyon yok)", V-IN ve R224-IN "büyütmeden sonra model içi ImageNet normalizasyonu (başlatma demetinin parçası)" diye tanımlıdır. Başlatma demeti "ağırlık, temiz aşama uzunluğu ve girdi normalizasyonu" olarak genişletilmiş, demetin iki mimaride özdeş olduğu ve normalizasyonun başlatmadan ayrı etkisinin bu tasarımda tanımlanamadığı yazılmıştır. Böylece H1 başlığındaki "girdi hattı eşitlenmişken" ifadesi doğru hale gelmiştir. Aynı düzeltme KONSEY_PLANI §2 (saldırı tablosundaki normalizasyon satırı), §4 B3 tablosu ve B3 paragrafına da uygulanmıştır. Kod tarafı (`src/models/r224.py`) zaten K3'e uygundu ve değiştirilmemiştir.
2. H1, H2 ve K-c'de destek ile çürütmenin örtüşmesi bir karar ilkesi ve öncelik sırasıyla giderildi. İlke şudur: destek Holm sonrası p ile, çürütme ve eşdeğerlik ham aralıklarla okunur; H1, H2 ve K-c'de çürütme ya da eşdeğerlik koşulu destekten önce denetlenir, yani anlamlı ama aralığı ±δ içinde kalan etki ihmal edilebilir sayılır. Betikte `b2_karar` ve `b4_karar` bu sırayla yeniden yazılmıştır. Doğrulayıcının iki sentetik örneği birim sınamaya eklenmiş ve artık tek karar vermektedir: A^σ_scr = −0,0575, %90 aralık (−0,070; −0,045), Holm p 0,0003 için karar "çürütüldü (eşdeğer)" ve bölge yalnız O2; I^σ = +0,0495, %90 aralık (0,041; 0,058) için H2 "çürütüldü (eşdeğer)" ve bölge yalnız O3 (SAHTE `birim_sinamalari.H1_ortusme_ayrik`, `.H2_ortusme_ayrik`, ikisinde de `gecti` = true). Öngörülen büyüklüğün (≤ −0,20, ≥ +0,10, q_s ≥ 0,75, Δ_w ≥ 0,30) tutup tutmadığı her sınamada ayrı bir alan olarak yazılmaktadır.
3. Görülmüş veri listesi genişletildi. ON_KAYIT §1'e 05:55 sonrası çıktılar eklenmiştir: sahte sınamadaki gerçek ViT tohumlarının Gowal panelli ρ değerleri (−0,035; −0,042; −0,078; SAHTE `b2.b2.F_B2.K-b.degerler`) ve gerçek s1003-s2003 çiftinde q = 0,953 (`b2.b2.F_B2.K-a.q[0]`), MASA'da logit ölçekte ρ_V = −0,265 (`1_havuz_model_tablosu.modeller.ViT_Tiny_AT_s2001.yari_logit.rho`), B1 smoke matrisleri (`results/q1/konsey_smoke/matris_panel`, `matris_ekle`, `matris_taze`, `matris_uc`; son üçünde R224_scr_smoke ve V_IN_smoke bulunduğu `transfer_matrix.json` `models` alanından doğrulanmıştır) ve smoke temiz doğrulukları (V_IN 92,85, R224_IN 79,25; `results/q1/konsey_smoke/denetim_yardimcisi.txt`). "B3 hücrelerinin hiçbir verisi görülmemiştir" cümlesi, görülen verinin yalnız birkaç epokluk smoke modellerinin n = 200'lük matrisleri ve smoke temiz doğrulukları olduğu biçiminde nitelenmiştir.
4. Panel bileşimi yedi üye olarak donduruldu. Yedi üyenin `models/robustbench_zoo/cifar10/Linf/` altında olduğu `ls` ile, smoke matrisinde yüklendiği `results/q1/konsey_smoke/matris_panel.log` ile doğrulanmıştır. ON_KAYIT §2 ve dondurma satırı "B2 sonuçlarından önce" diye düzeltilmiş, "yüklenemeyen üye" işlemsel olarak tanımlanmıştır (yüklemede istisna ya da B2 matrisinde en az bir hücresi üretilemeyen üye). Aynı düzeltme KONSEY_PLANI §4 B2, risk tablosu, `KONSEY_RUNBOOK.md` §2 ve `hucre_tablosu.json` (`panel_dondurma` alanı) içine işlenmiştir.
5. δ gerekçesi düzeltildi. ON_KAYIT §5 ve KONSEY_PLANI §2 artık 0,0897'nin yedi AT modelinin 21 çiftindeki r'nin RMS'si olduğunu, bunun ViT'li 6 çifti de kapsadığını (RMS 0,112) ve yalnız CNN çiftlerinde değerin 0,0605, ViT'siz 15 çiftte 0,0788 olduğunu söylemektedir (`results/q1/konsey_masa/_dogrulayici/delta_kaynagi.json`, `hepsi_21`, `vit_li_6`, `yalniz_cnn_10`, `vit_disi_15`). Birincil δ = 0,10 korunmuş, bütün eşdeğerlik ve ihmal edilebilirlik kollarına δ = 0,06 duyarlılığı eklenmiştir; betik bunu B2'de `F_B2.duyarlilik_delta_0.06`, B4'te `duyarlilik.delta_0.06` olarak yazar. σ ölçekli karşıtlıklar için ampirik dayanak bulunmadığı, δ'nın orada uzlaşım olduğu açıkça yazılmış ve karşılaştırma için log τ̄ koşum SD'si (0,021-0,023) verilmiştir. Sahte sınamada δ = 0,06 duyarlılığı sonuç bölgesini O3'ten O5a'ya çevirmektedir (SAHTE `b4.b4.duyarlilik.delta_0.06.sonuc_bolgesi`); bu, duyarlılığın gerçek veride de karar okumasını değiştirebileceğini gösteren bir kod gözlemidir, kanıt değildir.
6. Sayı kaynağı yolları karantina kuralına çevrildi. ON_KAYIT §1 ve §5 ile KONSEY_PLANI §1-§3'teki `_p3_carpimsal_yasa_masa.json` ve `_p3_potansiyel_masa.json` atıfları `results/q1/konsey_masa/` yollarını göstermektedir. Ayrıca raporlar klasöründe çıktı bırakan diğer altı masa betiği de `experiments/q1_konsey_masa_yeniden_kos.py` ile çıktısı `results/q1/konsey_masa/` altına yazılacak biçimde yeniden koşulmuştur (betiklerin kendisine dokunulmamıştır). Sonuç aşağıdaki tablodadır (kaynak `results/q1/konsey_masa/yeniden_kos_karsilastirma.json`, `isler.<betik>.karsilastirma_uretildi_utc_haric`). `_P2_panel_masa` ve `_P2_panel_logit` dosyalarındaki tek basamaklık farkın nedeni belirlenmiştir: bu betikler sonucu üç ve dört basamağa yuvarlar ve örneğin `S.raw.ResNet18_AT.ort` için kesin toplam 27,3925 sınırındadır; konteynerdeki Python 3.12'nin `sum()` işlevi kayan nokta toplamında telafili toplama kullandığından değer 27,3925'e, eski koşudaki Python ise 27,392500000000002'ye ulaşır ve yuvarlama 27,392 ile 27,393 arasında ayrışır. Bu bir hesap hatası değil yuvarlama sınırı etkisidir. Eski `raporlar/` altındaki JSON dosyaları silinmemiştir; yeni metinlerde sayı kaynağı olarak gösterilmemektedir.

| Betik | Sayısal yaprak | En büyük mutlak fark | Durum |
|---|---|---|---|
| `_p3_havuz_gurbuzluk_yasasi.py` | 678 | 0 | özdeş |
| `_P2_panel_masa.py` | 321 | 0,001 (`S.raw.ResNet18_AT.ort`, 27,393 ve 27,392) | yuvarlama sınırı |
| `_P2_panel_logit.py` | 288 | 1e-4 (`sonuc.target_correct/oran.CNN_CNN_mutlak_artik_ozet.ortalama`) | yuvarlama sınırı |
| `_P2_panel_logit_ayri.py` | 56 | 0 | özdeş |
| `_rb_liste.py` | 0 (yalnız metin) | 0 | özdeş |
| `_rb_imagenet_P2.py` | 0 (yalnız metin) | 0 | özdeş |

7. K-b'nin çürütmesi iki yöne genişletildi: "%95 aralık sıfırı dışlar ve |nokta kestirimi| > 0,10". Betik işareti karar etiketine yazar ("çürütüldü (negatif yön)" ya da "(pozitif yön)") ve eski yalnız pozitif okumayı `K-b_eski_yalniz_pozitif_okuma_curutme` alanında saklar. Birim sınamada [−0,20; −0,21; −0,19] için karar "çürütüldü (negatif yön)" çıkmıştır (SAHTE `birim_sinamalari.K-b_negatif_curutme`). Bu değişiklik görülmüş veriden sonra yapıldığı ve çürütmeyi kolaylaştırdığı için ON_KAYIT §1'de ayrıca beyan edilmiştir.
8. Logit ve oran ölçeklerinde r ve τ̄'nın tanımı ON_KAYIT §2'ye yazıldı: L(x) = log[(x/100)/(1 − x/100)], x/100 [10⁻⁶; 1 − 10⁻⁶] aralığına kırpılır, r^logit ve log τ̄^logit log yerine L ile kurulur; oran ölçeğinde yüzde değerin kendisi kullanılır. Bu, betiğin `olcek_f` işleviyle aynıdır. H2'deki "negatif ve anlamlı" ifadesi kararın içinde "ham iki yönlü p < 0,05" olarak, O3 varyantının manşete girmesi ise "Holm sonrası p < 0,05" olarak yazılmıştır; betik bu ikisini zaten böyle ayırıyordu (`H2` ve `H2_negatif_anlamli_holm`).
9. K-b ve H3'te bağlayıcı ölçüt Holm sonrası TOST p < 0,05 olarak yazıldı; ham %90 aralığın ±0,10 içinde kalıp kalmadığı `K-b_ham_ci90_delta_icinde` ve `H3_ham_ci90_delta_icinde` alanlarında ayrıca verilir. Bu değişiklik desteği zorlaştırır: sahte B2'de K-b'nin kararı eski kuralla "destek (%90 aralık ±0,10 içinde)" iken, Holm sonrası TOST p 0,102 olduğundan yeni kuralla "kararsız"dır (SAHTE `b2.b2.F_B2.p_holm[1]`, `.karar.K-b`). Sahte panel tek üyeli olduğundan bu bir kanıt değil, kuralın davranışını gösteren bir kod gözlemidir.
10. K-c'nin destek ölçütü ("çürütme tutmuyorsa Holm sonrası p < 0,05") ve bootstrap ayrıntıları (görüntülerde ortak ağırlık, tohumlarda yerine koyarak çekim, özdeş kökenli çiftlerin dışlanması, tek farklı tohumlu örneğin yeniden çekilmesi, p'nin (1 + #{Δ*_w ≤ 0})/(B + 1) tanımı, üç tohumda on çoklu küme sınırlılığı) ON_KAYIT §5'e yazıldı. Öngörü (Δ_w ≥ 0,30) ile sıfır hipotezi (Δ_w ≤ 0) arasındaki fark, karar ilkesindeki "öngörülen büyüklük ayrı raporlanır" kuralıyla okunur.
11. K-a için payda kuralı eklendi: bir tohumda D_s ≤ 0,10 ise K-a kararsız sayılır, Holm ailesinde p = 1 ile kalır ve simetrik ile yönlü pay ayrı raporlanır. Birim sınamada bu yol "kararsız (payda küçük)" vermiştir (SAHTE `birim_sinamalari.K-a_payda_kurali`). Öngörü (her tohumda q_s ≥ 0,75) ile destek ölçütü (ort q > 0,50) arasındaki ilişki 2. maddedeki büyüklük kuralıyla bağlanmıştır.
12. B5 A önceliğine alındı ve tanımlandı. ON_KAYIT §5 B5 artık izinli saldırıları, en iyi saldırının çapraz uydurmalı bölünmüş yarı seçimini, hiyerarşik bootstrap yüzdelik aralığını (B = 2000, seçim her kopyada yeniden), destek, çürütme ve kararsız kurallarını, G_PGD ≤ 0,10 için payda kuralını ve B5'in Holm dışı ayrı aile olduğunu yazmaktadır. Betiğe `--mod b5` eklenmiştir; saldırı türü her klasörün `transfer_matrix.json` dosyasındaki `attack` alanından okunur (alan yoksa PGD sayılır). Bu, fable kararı K6'daki arayüzün bir eklentisidir ve mevcut üç mod değişmemiştir; ana oturumun onayına sunulur. Kod yolu, C1 seçilen kontrol noktası matrisleri "pgd" ve son kontrol noktası matrisleri SAHTE olarak "mi" etiketlenerek sınanmıştır: G_PGD 0,367, G_best 0,371, oran 1,013, %90 aralık (0,958; 1,056) (SAHTE `b5_yolu.b5.birincil_C1-R32_V-scr`). Bu sayılar MI-PGD sonucu değildir. KONSEY_PLANI §4 tablosunda B5 ve B6 "A (K2)" olmuş, bekçi paragrafı ve toplam satırı K2'ye göre düzeltilmiş (en kötü durum 42,2 GPU-saat), takvim ve özet paragrafı da buna uydurulmuştur. `KONSEY_RUNBOOK.md` §5 ve §6'daki "yalnız defterde pay kalırsa" cümleleri de düzeltilmiş, §5'e B5 çözümleme komutu eklenmiştir.
13. B6 maskeleme işaretinin sonucu bir karar kuralı olarak yazıldı: işaretli modeller çıkarılarak H1-H3 yeniden hesaplanır; bir hipotezin kararı değişirse ya da bir hücre iki koşunun altına düşerse o hipotezin manşet cümlesi kararsız sayılır (H1 için bölge O5, H2 ya da H3 için O1, O3 ve O3 varyantı O5a'ya iner). Betiğe `--maskeleme-isaretli` bayrağı eklenmiştir. İki sahte yol sınanmıştır: ViT_Tiny_AT_s2003 işaretlenince H2 değişmiş ve bölge O3'ten O5a'ya inmiştir; SAHTE_V_IN_a işaretlenince V-IN hücresi tek koşuya düşmüş, kural H2 ve H3'ü manşet dışı bırakmıştır (SAHTE `b4_maskeleme_yolu`).
14. Sonuç haritası sıralı ve kapsayıcı hale getirildi. Denetim sırası O2, O5, O1, O3, O3 varyantı, O5a'dır; O2 H1'in ters yön çürütmesini de kapsar, O5 H1'in kararsız ya da hesaplanamadığı durumdur, yeni O5a bölgesi "H1 destek, H2 ve H3 için diğer bölgelerin hiçbiri" durumudur, O4 ayrık bölge değil ek nitelemedir. Birim sınamada 240 etiket bileşiminin her biri tek bir bölgeye düşmüştür (SAHTE `birim_sinamalari.sonuc_haritasi_kapsam`). Betik artık tek bölge (`sonuc_bolgesi`) ve ayrı bir `O4_niteleme` alanı yazmaktadır.
15. Bölüm 6'nın açık kalan beş maddesi kapatıldı. Eksik p, Holm ailesinde p = 1 sayılır ve aile büyüklüğü üç kalır (betikte `holm_aile`; birim sınama [0,01; yok; 0,02] → [0,03; 1; 0,04]). ω her kestiricide tam örneklem w'den hesaplanır ve bu ON_KAYIT §2'ye yazılmıştır. S1-S3'ün aralık yöntemi (S1 iki hücreli birleşik varyans, S2 ve S3 dört hücreli birleşik varyans, df 5) ON_KAYIT'a yazılmıştır. S4 ve S5 çiftleri açık liste olarak ON_KAYIT'a geçirilmiş ve 2003 tohumunun dışarıda kaldığı yazılmıştır; bu bir yorum olduğundan dondurmadan önce ana oturumun onayına açıktır. Son kontrol noktası duyarlılığı yalnız masa düzeyinde tutulmuş, B2 ve B4 duyarlılık listesinden çıkarılmıştır.
16. Kesinlik planına, model düzeyi σ ve ρ karşıtlıklarının koşum SD'si yerine çift düzeyi r_RV ve log τ̄_RV SD'lerinin vekil olarak kullanıldığı ve gerçek SD'nin bundan küçük ya da büyük olabileceği cümlesi eklendi. Doğrulayıcının sayıları SENTEZ'te yeniden okunmuştur: r için 0,010389, 0,044032, 0,040864; log τ̄ için 0,021664, 0,020982, 0,022819 (`kumeler.*.tam_orneklem.r.sd_kosum` ve `.log_tau.sd_kosum`).
17. KONSEY_PLANI §7'deki kuyruk komutu K5 yoluna çekildi (`models/q1/konsey/V_IN_s2101`; dosyada `vit_in1k_s2101` kalmamıştır). `hucre_tablosu.json` içindeki üç "(indirilecek)" notu "(diskte: models/robustbench_zoo/cifar10/Linf/)" olarak, KONSEY_PLANI §4'teki "indirilecek" ifadesi de "B1'de indirildi" olarak güncellenmiştir.

Düzeltilemeyen ya da bu turun dışında kalan noktalar şunlardır. Birincisi, `--mod b5` ve `--maskeleme-isaretli` K6 arayüzünü genişletmektedir; fable kararı bu genişlemeyi açıkça kapsamadığından onay gerekir. İkincisi, ON_KAYIT'ın dondurma satırındaki tarih, işleme karması ve iki SHA-256 alanı boş bırakılmıştır, çünkü dondurma ve git işlemi ana oturumun işidir; bu rapordaki karmalar ancak betik ve hücre tablosu bir daha değişmezse geçerli kalır. Üçüncüsü, doğrulayıcının kendi sınama betiği (`results/q1/konsey_masa/_dogrulayici/istatistik_sinama.py`) eski karar etiketlerine göre yazılmıştır ve yeniden koşulmamıştır; yeni kurallar onun yerine SAHTE `birim_sinamalari` altında sınanmıştır. Dördüncüsü, `KONSEY_RUNBOOK.md` §6, PGD-10 ile AA arasındaki farkı B4 köşegeninden (n = 10000) almayı önerirken AA n = 1000 alt kümesinde koşulmaktadır; iki doğruluğun aynı görüntülerde hesaplanması gerekir. Bu doğrulayıcının listesinde olmadığından düzeltilmemiş, yalnız kayda geçirilmiştir. Beşincisi, `raporlar/konsey_2026-10-29/` altındaki eski masa çıktıları silinmemiştir; silme kararı ana oturuma bırakılmıştır. Konteynerin yazdığı yeni dosyalar `chown 1000:1000` ile firat'a verilmiştir.
