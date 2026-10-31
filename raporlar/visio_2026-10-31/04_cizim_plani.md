# Çizim planı (visio-cizici, Faz B öncesi bağlayıcı plan)

Tarih 31.10.2026 akşamı. Hazırlayan görsel üretici ajan (gorsel-uretici). Bu belge Faz A'nın çelişik doğrulamasındaki 17 bulgunun (6 major, 11 minor; `03_faz_a_dogrulama.md`) hepsini kapatır ve çizim fazının tek bağlayıcı planıdır. Bu adımda Visio açılmamış, hiçbir şekil çizilmemiş, `.tex` dosyalarına, şekil betiklerine, föye ve `results/` altına dokunulmamıştır. Yazılan dosyalar şunlardır: bu plan, `paper/figures/panel_yapisi.yaml` (yeniden yazıldı), `paper/figures/qc/panel_atiflari_{en,tr}.{md,json}` (yeniden üretildi), `01_envanter.md` ve `02_uslup_secimi.md` sonundaki düzeltme ekleri. Bölüm 8 ve 9'daki sıra numaraları dışında şekil numaraları bugünkü basılı numaralardır.

En önemli üç sonuç şunlardır. Birincisi, panel üyeleri (Y2) şekil 1'e girmez, ayrı ve tek sütunluk bir şekil (`fig:panel_members`) olur; şekil 1 ise ImageNetV2 metni kısalıp (d) ile (e) boşlukları toplanarak 161.9 mm'lik önizlemeden 142 mm hedefe iner. İkincisi, makaleye beş yeni şekil eklenir (Y1 tasarım ve eğitim tarifi, Y2 panel üyeleri, Y4 kayıt haritası, Y5 ön kayıt zinciri, Y7 protokol ayarları), iki mevcut şekil büyür (şekil 9'a maskeler, şekil 12'ye blok çıkışı kosinüsü) ve şekil sayısı 12'den 17'ye çıkar; tahmini sayfa etkisi yaklaşık 0.65 sayfa kısalmadır, metin hiç kısaltılmasa bile toplam 26 sayfayı aşmaz (bölüm 7). Üçüncüsü, Üslup 8'in 3B blokları artık varlığın anlam rengini ön yüzde taşır; üst ve sağ yüz beyaza doğru açılır, en küçük luminans basamağı 0.105'tir ve lejant ön yüz tonunu gösterir (bölüm 4).

## 1. Doğrulama bulgularının kapanışı

| Bulgu | Konu | Kapandığı yer | Karar özeti |
| --- | --- | --- | --- |
| M1 | 3B küplerde anlam rengi yalnız lejantta | bölüm 4; 02 düzeltme eki D1 | Ön yüz varlık hex'i, üst ve sağ yüz açılır (sağ 0.25, üst 0.50); lejant ön yüz tonu; σ/ρ girdileri şekil 1 lejantından kalkar |
| M2 | Y5 için `sayim_akisi` Üslup 8'de uygulanmaz | bölüm 3, bölüm 9 Y5; `panel_yapisi.yaml` | Y5 Üslup 8 `yontem_semasi` şablonunun üst zemin bandı ve 7 mm şeridiyle çizilir; on yedi şeklin hepsinin şablonu seçili üslupta uygulanır olarak denetlendi |
| M3 | Şekil 9'da rakam adımının ön koşulu yok | bölüm 8; `panel_yapisi.yaml` | Şekil 9 `farkli_analizler`, ad türü şerit (adım 4, kural dalı 5); A-D harfleri ve rakam halkası kalkar, kümelere protokol adları yazılır |
| M4 | Y2 şekil 1'e sığmıyor | bölüm 5 | Y2 ayrı tek sütun şekil; şekil 1 hedefi 142 mm, tavanı 150 mm; Y6 eklenmez |
| M5 | Üslup 7 önizlemesinde veri alanı payı 0.09 | bölüm 6; 02 düzeltme eki D2 | Spearman özet kartı kalkar, r ve n panellerde kalır, çift türü lejantı alt şeride iner, saçılımlar yaklaşık 53.8 mm sütuna çıkar; 0.74 beklentisi varsayımdır, denge.py ölçer |
| M6 | Venue kaydı skill'de yok | bölüm 2 Ö1 | Kayıt başka ajanca yapılmış (`venues.py` satır 336-356), `visio_cizici.yaml`'da `venue: ieee_access` açık; `tests/test_venues_kind.py` bu plan yazılırken koşuldu, 11 test geçti |
| m1 | Harfli pay 0.00 değil 0.08 | bölüm 8; 01 düzeltme eki E1 | 12 şekilde 1/12 = 0.083, 17 şekilde 1/17 = 0.059 (motor yöntemi, `denge.py` satır 692-709) |
| m2 | Şekil 1 beş panelli | bölüm 8, bölüm 9 şekil 1; 01 eki E2 | (a) Trained models, (b) Reference panels, (c) Matrices, (d) Registered before measurement, (e) Exact split and contrasts; harf, beşinden en az üçü metinde ayrı anılırsa kalır |
| m3 | 7 ile 10 harfli şekil, rozet sayıları | 01 eki E3 | Altyazıda harf anan 7 şekil, görüntüde harf taşıyan 10 şekil; 15/18 rozet sayısı sayacın altyazı ayrıştırma sayısıdır |
| m4 | Şekil 10 üst kaynak 17 | 01 eki E4; bölüm 9 şekil 10 | 17 |
| m5 | Y1 veri satırında kaynak yok | bölüm 9 Y1; 01 eki E5 | `scripts/konsey_b3_kuyruk.sh` satır 11 ve 90-99 ile `src/training/trainer.py`; föy satırı şartı korunur |
| m6 | "Alanını adıyla anan tek üslup" abartısı | 02 eki D3 | "En uygun" ifadesi; Üslup 4'ün elenme nedeni görüntü lisansı ve görüntü merkezli şema dili |
| m7 | Üslup 8 harf konumu | bölüm 9 şekil 1; `panel_yapisi.yaml` başlığı | Harf "(a)", düz, 9.0 pt, panelin altında, betikte elle |
| m8 | SECİLİ_USLUP tek satır okunur | bölüm 10; 02 eki D4 | "Üslup N" iki N ister (şematik 8, veri 7); `hepsini_ciz` iki ayrı `--uslup` çağrısıyla ve proje kabuğuyla koşar |
| m9 | Etiket küpe değiyor, boşluklar, altyazı yazı tipi, çift türü rengi | bölüm 6, bölüm 9 şekil 1 ve 7 | Etiket ile küp arası en az 1.0 mm; (c) ve (d) boşlukları toplanır; çift türleri R224 hex'inden ayrılır |
| m10 | Satır başına sözcük 9.8 | bölüm 7; 01 eki E6 | Bütçe 9.8 ile yeniden hesaplandı; eski Y1-Y7 toplamındaki 0.80 sayfanın Y6 payı yalnız eke taşıma olduğu için toplam kazanç o planda yaklaşık 0.5 sayfaya iner |
| m11 | TR şekil 11-12 kaynak klasörü | 01 eki E7 | TR şekil 10, 11 ve 12 `final_tr/` altındadır; kanıtları `final_tr/*.kanit.json` |

Kapanan bulgu sayısı 17'dir. M6 bu planın işi değildi, ama kaydın varlığı ve testi bu plan yazılırken denetlendi.

## 2. Çizimden önce yapılacaklar (ön koşullar)

1. Venue kaydı (Ö1) yapılmıştır ve `motor/figspec/venues.py` satır 336-356'da `IEEE_ACCESS` kaydı vardır (tek sütun 242.67355 pt, tam genişlik 505.12177 pt, metin yüksekliği 672 pt, taban 8.0 pt, yükseklik payı 0.70, altyazı 7 pt) ve `REGISTRY`'ye girmiştir; `paper/figures/visio_cizici.yaml`'da `venue: ieee_access` satırı açıktır. `tests/test_venues_kind.py` 31.10.2026'da 11 geçen testle koşulmuştur. Karar: yeni çizim betikleri `_vz_ortam.kur()` kabuğunu çağırmaz, çünkü venue artık motorun kendisinden gelir; önizleme betikleri tarihsel kayıt olarak değişmeden kalır. Taban punto ve 0.70 payı IEEE kılavuzundan doğrulanmamıştır (karar değeri).
2. Palet üreteci (Ö2), yani `paper/figures/visio/_palet_uret.py`, genişletilir (ayrıntı bölüm 4.3): her varlığa 3B yüz üçlüsü, çift türü ailesi (`cift_cnn`, `cift_vit`, var olan `mixed`), protokol ailesi (dört ton) ve ayar ailesi (şekil 10'un sekiz grubu) eklenir, palet yeniden üretilir. Palet dosyası elle düzenlenmez.
3. Yüz tonu yardımcısı (Ö3) için `paper/figures/visio/_vz_ortam.py`'ye `yuz_tonlari(varlik)` bağlam yöneticisi eklenir (bölüm 4.2).
4. Veri dosyaları (Ö4) hazır olmalıdır. Ayrı ajanın ürettiği üç dosya (`results/q1/konsey_b3_tarif.json`, `results/q1/konsey_kayit_kurallari.json`, `results/q1/konsey_zaman_cizelgesi.json`) ve föyün M13 bölümü yazılmadan Y1, Y4 ve Y5 çizilmez. Bu planda föy satırları "M13.x" yer tutucusuyla anılır; çizim ajanı gerçek satır numaralarını föyden okur ve kanıt dosyasına yazar.
5. Yazı tipi (Ö5) değişmez, Üslup 8 ve 7 DejaVu Sans kullanır; önizlemede Open Sans yüzünden τ yazılan yerlerde τ̄ geri gelir, ⊇ işareti kullanılabilir.
6. Yükseklik kapısı (Ö6) gereği her şeklin yüksekliği 0.70 x 236.181 = 165.33 mm tavanını (T30) ve bölüm 9'daki şekle özgü tavanı aşmaz.

## 3. Şablon uygunluk denetimi

Her şeklin şablonu seçili üslubun `sablonlar.yaml` dosyasında arandı. Üslup 8'de uygulanmayan tek şablon `sayim_akisi`'dır (`styles/uslup_8/sablonlar.yaml` satır 73-74); öteki sekiz şablonun (yontem_semasi satır 7, tasarim_izgarasi 75, tablodan_sekle 103, ortak_satirli_katlar 140, goruntu_kanit_zinciri 195, tek_kart_veri 232, ic_ice_izgara 262, model_acilimi_3b 294) ölçülü ızgarası vardır. Üslup 7'de uygulanmayanlar `sayim_akisi` (satır 76-77) ve `model_acilimi_3b`'dir (satır 303-304); kullanılan dört şablonun ızgarası vardır (tasarim_izgarasi satır 78, ortak_satirli_katlar 141, tek_kart_veri 228; tablodan_sekle 106 kullanılmaz).

| Şekil | Üslup | Şablon | sablonlar.yaml satırı | Durum |
| --- | --- | --- | ---: | --- |
| 1 study_overview | 8 | yontem_semasi | 7 | uygulanır |
| Y1 design_recipe | 8 | tasarim_izgarasi | 75 | uygulanır |
| 2 decomposition_schematic | 8 | yontem_semasi (dikey, tek sütuna uyarlanır) | 7 | uygulanır |
| Y2 panel_members | 8 | tasarim_izgarasi | 75 | uygulanır |
| Y4 registry_map | 8 | tablodan_sekle | 103 | uygulanır |
| Y5 prereg_chain | 8 | yontem_semasi (üst zemin bandı ve şerit) | 7 | uygulanır (sayim_akisi uygulanmaz, terk edildi) |
| 3 source_gap_split | 7 | ortak_satirli_katlar | 141 | uygulanır |
| 4 similarity_matrix | 7 | ortak_satirli_katlar | 141 | uygulanır |
| 5 cells_interaction | 7 | tasarim_izgarasi (üç satır) | 78 | uygulanır |
| 6 attack_side | 7 | tek_kart_veri | 228 | uygulanır |
| 7 gradient_alignment | 7 | ortak_satirli_katlar (2 x 3) | 141 | uygulanır (önizlemedeki ic_ice_izgara bırakıldı) |
| 8 estimates_forest | 7 | tasarim_izgarasi (iki satır) | 78 | uygulanır |
| Y7 protocol_settings | 7 | tek_kart_veri | 228 | uygulanır |
| 9 protocol_sets | 7 | tasarim_izgarasi | 78 | uygulanır |
| 10 spread_clean_gap | 7 | tasarim_izgarasi (iki satır, ortak x) | 78 | uygulanır |
| 11 epsilon_sweep | 7 | tek_kart_veri | 228 | uygulanır |
| 12 feature_degradation | 7 | tasarim_izgarasi (üç satır, Y8 ile) | 78 | uygulanır |

Şablonların yüksekliği başvuru ölçüsüdür. Skill örneklerinde ızgaradan ayrılan şekiller `butce_asimi` kaydıyla "kurulabilir" almıştır (Üslup 8 `yontem_semasi` örneği 143.9 mm, ızgara 107 mm); bu yüzden hedef yükseklikler bölüm 9'daki gibi içerikten alınır ve sapma manifeste yazılır. Envanterdeki Y1 için önerilen `model_acilimi_3b` bırakılmıştır. Karar: Y1 `tasarim_izgarasi` ile çizilir, çünkü Üslup 8'in model açılımı şablonu 107 mm yüksekliğinde ve tam genişliktir, sayfa bütçesine iki sütunluk maliyet getirir; 3B model blokları ızgara hücrelerinde yine çizilir.

## 4. Üslup 8'in 3B ton merdiveni ve palet notu

### 4.1 Kural ve değerler

Karar: 3B nesnenin ön yüzü varlığın anlam hex'idir, sağ yüz hex'in beyaza doğru 0.25, üst yüz 0.50 açılmışıdır, çünkü doğrulayıcının M1 bulgusu anlam renginin şekilde görünmesini ister ve bu seçim `references/uc_boyut.md` bölüm 1 ve 4'ün sırasını (üst > sağ > ön) ve en az 0.05 göreli luminans basamağını yedi varlığın hepsinde iki katından fazla payla sağlar. `uc_boyut.md` bölüm 4 açma yolunu katalog dolgularının açık tonlu olması yüzünden varsayılan yapmamıştır; makalenin varlık tonları doygun Okabe-Ito renkleri olduğu için o gerekçe burada geçerli değildir. Değerler WCAG göreli luminansıyla ve motorun 8 bitlik karıştırma yuvarlamasıyla hesaplanmıştır (hesap betiği karalama klasöründedir; çizim ajanı `bl.face_tones` kaydındaki `steps` alanıyla yeniden doğrular).

| Varlık | Ön yüz (anlam hex'i) | Sağ yüz | Üst yüz | L ön / sağ / üst | Basamak üst-sağ, sağ-ön | Ana hat (ön, 0.30 koyu) |
| --- | --- | --- | --- | --- | --- | --- |
| vit | #D55E00 | #E08640 | #EAAE80 | 0.222 / 0.333 / 0.493 | 0.161, 0.111 | #954200 |
| r224 | #0072B2 | #4095C5 | #80B8D8 | 0.152 / 0.266 / 0.438 | 0.172, 0.114 | #00507D |
| r32 | #56B4E9 | #80C7EE | #AADAF4 | 0.405 / 0.516 / 0.652 | 0.136, 0.111 | #3C7EA3 |
| panel | #999999 | #B2B2B2 | #CCCCCC | 0.319 / 0.445 / 0.604 | 0.159, 0.127 | #6B6B6B |
| xcit | #CC79A7 | #D99ABD | #E6BCD3 | 0.293 / 0.415 / 0.575 | 0.160, 0.122 | #8F5575 |
| sym | #009E73 | #40B696 | #80CEB9 | 0.257 / 0.367 / 0.522 | 0.155, 0.111 | #006F50 |
| dir | #E69F00 | #ECB740 | #F2CF80 | 0.416 / 0.521 / 0.651 | 0.130, 0.105 | #A16F00 |

Lejant karesi ön yüz tonunu, yani anlam hex'ini gösterir; lejantla küp arasında renk farkı kalmaz. Şekil 1'in lejantında σ (simetrik, #009E73) ve ρ (yönlü, #E69F00) girdileri kaldırılır. Karar: σ ve ρ şekil 1'de bir renk kodlaması değil (e) panelinin metin terimleridir, bu yüzden lejantta karşılıksız kalırlar; iki rengin anlam bağı şekil 2, 5 ve 8'de kurulur. Şekil 1'in lejantı dört girdidir: ViT-Tiny, ResNet-18 (224 hattı), ResNet-18 CIFAR kökü (R32), sağlam CNN paneli. sym ve dir satırları 3B nesne çizen bir şekilde bugün kullanılmaz; tabloda yalnız ileride gerekirse aynı merdivenin hazır olması için durur.

### 4.2 Motorda uygulanışı

`bilesenler.face_tones` yüz tonlarını üslubun `three_d.face_tones` tokenından okur ve token üslup geneli tek bir sözlüktür; varlık başına hex üçlüsü için motorda bir parametre yoktur. `Uslup` nesnesi dondurulmamış bir dataclass'tır ve `three_d` değiştirilebilir bir sözlüktür (`motor/figspec/uslup.py` satır 689-696 ve 1205). Karar: proje kabuğuna `yuz_tonlari(varlik)` bağlam yöneticisi eklenir; yönetici `vf.USLUP.three_d["face_tones"]`'u o varlığın üç hex'iyle değiştirir, `bl.iso_box`, `bl.iso_stack` ya da `bl.iso_slab` çağrısından sonra eski değeri geri koyar. Çünkü bu yol skill dosyasına dokunmaz, `face_tones` her çağrıda basamağı yeniden denetler (`face_step_ok`) ve basamak kaydı (`tone_steps`) manifeste olduğu gibi yazılır. Manifestin `three_d.token` alanı yönetici çıktıktan sonra yazıldığı için üslubun özgün tokenını taşır. Skill'e varlık başına `faces=` parametresi eklenmesi skill sahibinin işidir ve açık sorun olarak bölüm 12'ye yazılmıştır.

### 4.3 Palet dosyasına not (talimat; dosya bu adımda değiştirilmedi)

`adeb_konsey_uslup_8.yaml` "do not hand-edit" başlığı taşır ve `_palet_uret.py` ile üretilir. Bu yüzden not ve yeni alanlar üretecin kendisine eklenir. Üreteç şu üç işi yapar.

1. Başlık yorumuna şu satırlar yazılır, "3B yüzleri: ön yüz varlık hex'idir; sağ yüz 0.25, üst yüz 0.50 beyaza açılır (04_cizim_plani.md bölüm 4). Lejant ön yüz tonunu gösterir. Değerler paper/figures/visio/palettes/adeb_konsey_uc_boyut.yaml dosyasındadır ve _vz_ortam.yuz_tonlari ile uygulanır; üslubun three_d.face_tones koyulaştırma değerleri bu makalede 3B varlık nesnelerinde kullanılmaz."
2. Ayrı bir dosya, `paper/figures/visio/palettes/adeb_konsey_uc_boyut.yaml`, her varlık için `on`, `sag`, `ust`, `kenar`, `acma: {sag: 0.25, ust: 0.50}`, üç luminans ve iki basamak yazar; basamaklardan biri 0.05'in altına düşerse üreteç hata verir. Ayrı dosya seçilmiştir, çünkü `palette_mod.load` varlık kaydında bilinmeyen alana nasıl davrandığı bu oturumda sınanmamıştır.
3. Yeni aileler `entities` altına eklenir, yani `cift_cnn` (#000000, işaret o, CNN-CNN çifti), `cift_vit` (#F0E442, işaret ^, 0.4 pt siyah kenar, transformer-transformer çifti), var olan `mixed` (#6E6E6E, işaret s) aynı `cift_turu` ailesine alınır; `protokol` ailesi dört tonla (#E7D4E8, #C2A5CF, #9970AB, #762A83; işaret o, ^, s, D; iç içe sıraya göre açıktan koyuya) ve `ayar` ailesi şekil 10'un sekiz grubu için eklenir. Karar: çift türleri R224 (#0072B2) ve ViT (#D55E00) hex'lerinden ayrılır, çünkü "bir hex bir aile" kuralı makale düzeyinde denetlenir ve şekil 7 önizlemesinde #0072B2 CNN-CNN'i kodluyordu (m9); siyah ve sarı Okabe-Ito'nun makalede kullanılmayan iki tonudur ve işaret biçimi ikinci kanaldır. Protokol ve ayar ailelerinin her tonu yedi anlam renginden CIEDE2000 ile en az 10 ayrılmalıdır (`uslup.GLYPH_ACCENT_DE`); üreteç bunu ölçer, ayar ailesinin sekiz hex'ini bu kuralla seçer ve 10'un altına düşen tonu yalnız koyulaştırarak düzeltir.

## 5. Y2 kararı

Karar: panel üyeleri şekil 1'e değil, ayrı ve tek sütunluk bir şekle (`fig:panel_members`) girer; şekil 1'in (b) paneli üye sayılarını taşımaya devam eder ve ImageNetV2 metni kısalır. Çünkü 161.9 mm'lik Üslup 8 önizlemesine 20 mm eklemek şekli 182 mm'ye çıkarır ve 165.33 mm tavanını aşar; (d) ve (e) boşluklarından kazanılabilecek yaklaşık 16-20 mm ise yalnız şeklin kendi sığma payını kurtarır, otuza yakın RobustBench kimliğini ve iki veri kümesi bloğunu taşımaya yetmez. Tam genişlikte her milimetre iki sütun satırı tüketir; tek sütunluk ayrı şekil aynı içeriği yarı fiyatla taşır.

Maliyet hesabı şöyledir. Üye matrisi 27 satırdır (CIFAR bloğunda iki veri kümesinin birleşimi 13 üye, ImageNetV2 bloğunda 14 model) ve 3.2 mm satır adımıyla 86.4 mm tutar; iki blok başlığı 10 mm, alt şerit 5 mm eklenince hedef 100 mm olur (tavan 110 mm). Şekil (100 + 12 + 7) / 4.233 = 28.1 sütun satırı, altyazıya taşınacak atıf listesi yaklaşık 2 satır tüketir. Serbest kalan metin, 3.6 "Reference Panels" bölümünün 547 sözcüğünden yaklaşık 330 sözcüktür (üye adları ve atıflar; ortak hat kuralları, Δσ_k gösterimi ve Liu ile Mo'nun dolaylı rolü metinde kalır), yani 330 / 9.8 = 33.7 sütun satırı. Net etki yaklaşık -3.6 satırdır. Buna şekil 1'in 161.9 mm yerine 142 mm'ye inmesinin kazancı eklenir: önizleme yüksekliğine göre (161.9 - 142) x 2 / 4.233 = 9.4 satır.

Şekil 1'in yeniden kurulması şu adımlarla yapılır: (b) panelinde ImageNetV2 metni "6 robust CNNs + 8 other models, descriptive" düzeyine iner (sayılar `_icerik_study_overview.py`'nin föyle karşılaştırdığı değerlerden; panel üyeleri Y2'ye gider); (d) ve (e) alt satırı 68 mm'den 50 mm'ye iner, (d)'de kayıt satırları 4.4 mm adımla ve protokol kutusu hemen altında durur, (e)'de dört kutu 2 x 2 düzende birbirine yaslanır; panel başlıkları Üslup 8 kuralıyla panelin altına "(a) Trained models" biçiminde iner ve üstteki başlık satırı kalkar. Y6 (şekil 5'e temiz doğruluk ve AutoAttack kartları) eklenmez. Karar: Y6 reddedilir, çünkü şekil 5 tek sütunda 121 + 35 = 156 mm'ye çıkıp tavana 9 mm kalır ve Tablo 8 eke taşındığında toplam sayfa sayısı azalmaz, şeklin büyümesi kadar (yaklaşık 8 satır) artar.

## 6. Veri üslubu ve şekil 7'nin veri alanı

Önizlemede (`paper/figures/charts/_onizleme_gradient_alignment_uslup_7.png`) solda genişliğin yaklaşık üçte birini alan "Rank correlation" kartı vardır ve sağdaki altı saçılım yaklaşık 28 mm genişliktedir. `pdfolcu.data_area_share` her satırın eksen omurgalarının birleşimini sayfa genişliğine böler ve şeklin payı en dar satırdır; ölçülen 0.09 bu darlığın kendisidir, bir ölçüm hatası olduğuna dair kanıt yoktur. Faz A raporundaki "ölçüm sınırı olabilir" yorumu geri alınmıştır (02 düzeltme eki D2).

Karar: Spearman özet kartı kalkar, çünkü altı r değeri ve n zaten her panelin içinde basılıdır ve kartın tek ek bilgisi (ImageNetV2'de ham 0.694'ten artık 0.893'e geçiş) aynı sütundaki iki panelin r etiketleriyle okunur. Düzen Üslup 7 `ortak_satirli_katlar` şablonunun 2 x 3 uyarlamasıdır: solda 8 mm'lik dar satır şeridi ("raw", "residual"), üstte veri kümesi sütun şeridi (CIFAR-10, CIFAR-100, ImageNetV2, n ile), üç sütun (177.53 - 8 - 2 x 4) / 3 = 53.8 mm genişlikte, altta 6 mm'lik çift türü lejant şeridi (konvansiyon şeridi; adım 4 bunu kabul eder). Hedef yükseklik 110 mm'dir (bugünkü 121.4 mm).

Beklenen veri alanı payı, eksen omurgası sütun başına yaklaşık 44 mm alınırsa 3 x 44 / 177.53 = 0.74'tür. Bu bir varsayımdır, ölçüm değildir; karar çizilmiş PDF'te `motor/host/denge.py` ile verilir ve 0.45'in altında kalırsa şekil kurulmaz, muafiyet yazılmaz. Aynı kural öteki veri şekillerine de uygulanır: bir değer sütunu ya da satır adları ekseni 0.45'in altına itmemelidir (şekil 6, 8, Y7 ve 11 için satır adı sütunu en çok 25 mm).

## 7. Yeni şekiller ve sayfa bütçesi

Varsayımlar şunlardır: gövde satırı 12 pt = 4.233 mm, sütun 56 satır, sayfa 112 sütun satırı; tek sütunda satır başına ölçülmüş 9.8 sözcük (`03` bulgu 16, EN main.pdf sayfa 3-12, 640 satır); şeklin maliyeti yüksekliği, 12 mm altyazı ve 7 mm kayan nesne aralığıdır; tam genişlik iki sütun tüketir; mevcut şekillerin bugünkü basılı yükseklikleri PDF ölçüsünden ve include genişliğinden hesaplanmıştır (şekil 1 172 mm genişlikte çizilip 177.53 mm'ye büyütüldüğü için 133.4 mm basılır; şekil 9-12 88.9 mm'den 85.29 mm'ye küçülür). Serbest kalan metin bir üst sınırdır, çünkü kısaltmayı yazım ajanı yapar.

| Kalem | Maliyet (sütun satırı) | Serbest kalan | Net |
| --- | ---: | ---: | ---: |
| Şekil 1 yeniden çizim (133.4 mm'den 142 mm'ye, tam genişlik) | 4.1 | 0 | +4.1 |
| Şekil 7 yeniden çizim (121.4 mm'den 110 mm'ye, tam genişlik) | -5.4 | 0 | -5.4 |
| Y1 `fig:design_recipe` (tek sütun, 92 mm) | 26.2 | 38.4 (Tablo 1 12.9 ve 250 sözcük) | -12.2 |
| Y2 `fig:panel_members` (tek sütun, 100 mm, altyazı +2) | 30.1 | 33.7 (330 sözcük) | -3.6 |
| Y3 şekil 9'a 15 mm (tek sütun) | 3.5 | 17.7 (Tablo 2 11.6 ve 60 sözcük) | -14.2 |
| Y4 `fig:registry_map` (tam genişlik, 90 mm) | 51.5 | 59.6 (Tablo 3 44.3 ve 150 sözcük) | -8.1 |
| Y5 `fig:prereg_chain` (tam genişlik, 60 mm) | 37.3 | 44.8 (400 sözcük ve altyazı cümlesi) | -7.5 |
| Y7 `fig:protocol_settings` (tek sütun, 80 mm) | 23.4 | 39.9 (Tablo 13 24.6 ve 150 sözcük) | -16.5 |
| Y8 şekil 12'ye 30 mm (tek sütun, ek) | 7.1 | 16.5 (Tablo 16) | -9.4 |
| Toplam | | | -72.8 (yaklaşık -0.65 sayfa) |

Karar: beş yeni şekil (Y1, Y2, Y4, Y5, Y7) eklenir, iki şekil büyür (Y3 şekil 9'da, Y8 şekil 12'de), Y6 ve Y9 eklenmez. Çünkü her kalemin net etkisi eksidir, yani kullanıcının "görsel artsın, metin kısalsın" isteğini sayfa artırmadan karşılar. Y9 net -1 satırla tek başına bir ajan koşusunu karşılamaz.

Sayfa sınırı için IEEE Access yazar kılavuzu bu oturumda okunmamıştır; görev metnindeki 26 sayfa üst sınırı kapı olarak alınmıştır. Bugün EN el yazması 25 sayfadır. Metin kısaltmalarının toplamı yaklaşık 1340 sözcüktür (136.7 satır). Kısaltma yalnız yüzde 60 gerçekleşirse net etki yaklaşık -0.16 sayfaya iner; metin hiç kısaltılmasa bile şekiller ve tablo kaldırmaları +64 satır, yani yaklaşık +0.57 sayfa getirir ve el yazması en çok 26 sayfaya çıkar. Beklenen sonuç 24 ya da 25 sayfadır. Kayan nesne yerleşimi kesikli olduğu için kesin sayı ancak derlemeden sonra bilinir; kapı derlenmiş EN PDF'in 26 sayfayı aşmamasıdır (bölüm 11, M-K5). Doğrulayıcının istediği not da buraya yazılır: Faz A bütçesinin -90 satırlık (0.80 sayfa) toplamında Y6'nın -25 satırı yalnız ana metinden eke taşımaydı, toplam sayfada etkisi yoktu; Y6 dahil o plan toplam sayfada yaklaşık 0.5 sayfa kazandırırdı.

## 8. Adlandırma dizisi ve yan kurallar

Mevcut 12 şeklin düzeltilmiş dizisi "karma akış şerit şerit renk yok şerit renk şerit şerit yok şerit"tir (şekil 9 rakamdan şeride geçti). En uzun aynı tür dizisi 2'dir (3-4 ve 9-10). Harfli pay motorun yöntemiyle 1/12 = 0.083'tür: `denge.py` `adlandirma_dizisi` (satır 692-709) harf içeren karma şekli harfli sayar. Sayacın Markdown çıktısındaki "harfli pay 0.00" sayacın kendi yöntemidir ve karma şekli harfli saymaz; bağlayıcı olan kurulum sonrası `zenginlik.py --makale` ölçüsüdür (motor yöntemi).

On yedi şekillik hedef dizi metindeki yerlere göre şöyledir:

| Sıra | Şekil | Ad türü | Adım |
| ---: | --- | --- | ---: |
| 1 | study_overview | karma (harf ve akış) | 7 |
| 2 | Y1 design_recipe | şerit | 4 |
| 3 | decomposition_schematic | akış | 2 |
| 4 | Y2 panel_members | şerit | 4 |
| 5 | Y4 registry_map | şerit | 4 |
| 6 | Y5 prereg_chain | akış | 2 |
| 7 | source_gap_split | şerit | 4 |
| 8 | similarity_matrix | şerit | 4 |
| 9 | cells_interaction | renk | 4 |
| 10 | attack_side | yok | 1 |
| 11 | gradient_alignment | şerit | 4 |
| 12 | estimates_forest | renk | 4 |
| 13 | Y7 protocol_settings | yok | 1 |
| 14 | protocol_sets | şerit (kural dalı 5) | 4 |
| 15 | spread_clean_gap | şerit | 4 |
| 16 | epsilon_sweep | yok | 1 |
| 17 | feature_degradation | şerit | 4 |

En uzun aynı tür dizisi 2'dir (4-5, 7-8, 14-15); sınır 2. Harfli pay harf kalırsa 1/17 = 0.059, kalmazsa 0'dır; sınır 0.40. Tür adları `motor/figspec/adlandirma.py`'deki `TURLER` ile aynıdır; konvansiyon şeridi hiçbir paneli adlandırmadığı için Y1, Y5 ve şekil 7'nin alt şeritleri türü değiştirmez (`tur_cizilenden`).

Karar: şekil 1'in harfleri kalır ve adım 7 (harf ve akış) ile çizilir, çünkü envanterin kısaltma önerisi 3.1-3.6 paragraflarını şekil 1'in panellerine atıfla kısaltmayı öngörür ve yazım ajanının görevine en az üç ayrı panel atfı (örneğin 3.1'de "Fig. 1(a)", 3.5'te "Fig. 1(e)", 3.6'da "Fig. 1(b)", 3.9'da "Fig. 1(d)") bağlayıcı madde olarak yazılır. Yazım ajanı bunu yapmazsa betikte tek parametre değişir (harf yerine `naming="strip"`), şekil "akış ve şerit" karmasıyla yeniden çizilir ve dizi kurala yine uyar. Harf Üslup 8 tokenıyla "(a)", düz, 9.0 pt basılır ve motor konumu okumadığı için betikte panelin altına elle yerleştirilir (`references/panel_adlandirma.md` bölüm 5).

## 9. Şekil başına çizim kartları

Ortak kurallar şunlardır. Kök adları numarasızdır; betik `paper/figures/visio/fig_<kök>.py` ya da `paper/figures/charts/fig_<kök>.py`'dir, kurulum adı numara kesinleşince `fig<N>_<kök>` olur (T28) ve eşleme `paper/figures/qc/ESLEME.md`'ye elle yazılır. Bütün 3B nesneler tek görünümle, Üslup 8'in eğik 25 derece ve 0.5 derinlik oranıyla çizilir; kart şekillerinde 3B yoktur. Her şekil `--uslup` değerini açıkça alır, kanıt dosyası (`<kök>.kanit.json`) veri yolunu, SHA-256'yı, git commit'ini, okunan anahtarları ve föy karşılaştırmasını yazar; föy bugünkü özetiyle (Faz A'da 00cc422f) yeniden karşılaştırılır. Eski şekil dosyaları (`konsey/`, `final/`, `final_tr/`) kullanıcı onaylayana kadar silinmez.

| No | Kök | Motor | Üslup | Kind | Hedef / tavan (mm) | Şablon | Ad türü (adım) | 3B nesneler | Veri gerekli |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- | --- |
| 1 | study_overview | Visio | 8 | double | 142 / 150 | yontem_semasi | karma (7) | model küpleri (V-scr, V-IN, R224-scr, R224-IN, R32), üç veri kümesi destesi, transfer matrisi bloğu | hayır |
| 2 | design_recipe (Y1) | Visio | 8 | single | 92 / 100 | tasarim_izgarasi | şerit (4) | dört hücre bloğu ve R32 köprü bloğu, düzlem etiketleriyle | evet: `konsey_b3_tarif.json` ve föy M13.x |
| 3 | decomposition_schematic | Visio | 8 | single | 90 / 95 | yontem_semasi (dikey) | akış (2) | ilk aşamada 2 x 2 transfer matrisi levhası (`iso_slab`) | hayır |
| 4 | panel_members (Y2) | Visio | 8 | single | 100 / 110 | tasarim_izgarasi | şerit (4) | blok başlığında veri kümesi destesi (şekil 1 (b) ile aynı nesne ve ölçek) | hayır |
| 5 | registry_map (Y4) | Visio | 8 | double | 90 / 95 | tablodan_sekle | şerit (4) | yok | evet: `konsey_kayit_kurallari.json` ve föy M13.x |
| 6 | prereg_chain (Y5) | Visio | 8 | double | 60 / 66 | yontem_semasi (üst bant ve şerit) | akış (2) | yok | evet: `konsey_zaman_cizelgesi.json` ve föy M13.x |
| 7 | source_gap_split | kart | 7 | double | 66 / 72 | ortak_satirli_katlar | şerit (4) | yok | hayır |
| 8 | similarity_matrix | kart | 7 | double | 64 / 70 | ortak_satirli_katlar | şerit (4) | yok | hayır |
| 9 | cells_interaction | kart | 7 | single | 121 / 125 | tasarim_izgarasi | renk (4) | yok | hayır |
| 10 | attack_side | kart | 7 | single | 95 / 98 | tek_kart_veri | yok (1) | yok | hayır |
| 11 | gradient_alignment | kart | 7 | double | 110 / 118 | ortak_satirli_katlar (2 x 3) | şerit (4) | yok | hayır |
| 12 | estimates_forest | kart | 7 | single | 127 / 130 | tasarim_izgarasi | renk (4) | yok | hayır |
| 13 | protocol_settings (Y7) | kart | 7 | single | 80 / 88 | tek_kart_veri | yok (1) | yok | hayır (föy satır denetimi şart) |
| 14 | protocol_sets | kart | 7 | single | 115 / 120 | tasarim_izgarasi | şerit (4, kural dalı 5) | yok (envanter kararı: iç içe kümeler 2B) | hayır |
| 15 | spread_clean_gap | kart | 7 | single | 119 / 122 | tasarim_izgarasi | şerit (4) | yok | hayır |
| 16 | epsilon_sweep | kart | 7 | single | 62 / 66 | tek_kart_veri | yok (1) | yok | hayır |
| 17 | feature_degradation | kart | 7 | single | 118 / 122 | tasarim_izgarasi (üç satır) | şerit (4) | yok | hayır |

Tablodaki sıra numarası hedef basılı numaradır; bugünkü numaralar parantez içinde aşağıda anılır.

### 9.1 Şekil 1, study_overview (bugün şekil 1)

Düzen `yontem_semasi`'nın kendisidir: üstte açık mavi zemin bandında (a) Trained models, (b) Reference panels, (c) Matrices; altta (d) Registered before measurement ve (e) Exact split and contrasts; en altta 7 mm lejant şeridi. Satır bütçesi üst bant 66 mm, alt başlık satırı 5 mm, aralık 6 mm, alt satır 50 mm, alt başlık 5 mm, aralık 4 mm, şerit 7 mm, toplam yaklaşık 143 mm; hedef 142, tavan 150. Bantlar arası akış "PGD-10" ve "split-half, log scale" etiketli ince oktur. (e) dört kutusundan en az ikisine küçük gömülü glif (2 x 2 matris glifi, kosinüs glifi) eklenir, çünkü önizlemede yalnız metin taşıyan kutu oranı eşik dışıydı. Etiket ile küp arasında en az 1.0 mm boşluk bırakılır (önizlemede "R224-scr" R224-IN küpüne değiyordu); ön denetim bunu çakışma olarak yakalar, ayrıca betikte etiket kutusunun küp sınır kutusuna uzaklığı ölçülüp kanıta yazılır. Küplerin tonları bölüm 4.1'deki tablodandır.

Şeklin veri kaynağı `paper/figures/konsey/fig_study_overview.kanit.json` (`okunan_anahtarlar`, `foy_karsilastirmasi`, 19 karşılaştırma) ve onun girdileri (`raporlar/konsey_2026-10-29/hucre_tablosu.json`, `_b9.json`, `_b8.json`, `results/q1/konsey_b10_gradyan/mantel_{cifar10,cifar100,imagenetv2}.json`, `results/q1/konsey_b8_imagenetv2/b8_dondurulmus_b2.json`) dosyalarıdır; içerik modülü `paper/figures/visio/_icerik_study_overview.py` yeniden kullanılır; karşılaştırılan föy satırları 1496-1499, 1569, 1593, 1741, 1826-1827, 1848, 1873-1887, 1909-1922 ve 1930-1932'dir. Görüntüler CIFAR-10 ve CIFAR-100 test dosyalarının ilk dört görüntüsüdür (SHA-256'ları önizleme kanıtında); ImageNetV2 destesi görüntüsüz kalır.

Altyazı (EN `03_methodology.tex` 37; TR `03_yontem.tex` 29): kalın girişle açılır, (a)-(e) harflerini panel adlarıyla aynı yazar, iki okun ne taşıdığını ve lejantın dört rengini söyler; panel üyelerinin ayrıntısı için Y2'ye atıf yapar. Metin kısaltma: 3.1 ve 3.4'te model listesi "Fig. 1(a)" atfıyla bir cümleye iner; 3.6'nın açılış cümlesi "Fig. 1(b)" ile sayıları verir, üye adları Y2'ye gider.

### 9.2 Y1, design_recipe (yeni; Tablo 1 yerine)

Tek sütunda üstte 2 x 2 hücre ızgarası (satır şeridi ViT-Tiny ve ResNet-18, sütun şeridi scratch ve ImageNet init.), her hücrede bir 3B model bloğu ve düzlemde kılavuz çizgili etiketler (R224: 7 x 7 kök, ViT-Tiny: 16 x 16 yama, 12 blok, genişlik 192, 3 baş; başlatma kaynağı ve temiz evre epokları); yanda R32 köprü bloğu; altta 20 mm'lik ortak AT tarifi şeridi (konvansiyon şeridi). Bütün sayılar `results/q1/konsey_b3_tarif.json`'dan okunur ve föyün M13.x satırlarıyla karşılaştırılır; bu dosyanın kaynağı `scripts/konsey_b3_kuyruk.sh` (satır 11 ve 90-99: AdamW, öğrenme oranı, ağırlık azaltma, epok, batch, patience, temiz evre 200 ve 30 epok) ve `src/training/trainer.py`'dir. Tohum ve batch için föy M9.1 (satır 1446-1489) ve hücre tanımları için satır 1443 ayrıca karşılaştırılır. Altyazı tarifin föyde olduğunu ve AT hiperparametrelerinin dört hücrede ortak olduğunu söyler. Metin kısaltma: EN 03_methodology 72-131 (3.3 tarif kısmı 72-89, Tablo 1 101-131), TR 03_yontem 64-123; Tablo 1 kalkar, tarif paragrafı iki cümleye iner.

### 9.3 Şekil 3, decomposition_schematic (bugün şekil 2)

Şekil tek sütunda dikey bir akıştır ve log T matrisinden w-τ-r ayrışımına, panel ortalamaları σ ve ρ'ya ve kaynak açığına iner; aşamalar etiketli şevronla bağlanır, (a)-(d) harfleri kalkar. İlk aşamadaki matris 2 x 2 `iso_slab` olarak çizilir (köşegende w), terimler σ yeşil (#009E73) ve ρ turuncu (#E69F00) basılır; renk ve terim adı birlikte gider, ton tek kanal olmaz. Veri: `paper/figures/konsey/fig_decomposition_schematic.kanit.json` (sayı çizmez; iki özdeşlik denetimi rastgele matrislerde yeniden koşulur). Altyazı (EN 162; TR 154) "Top to bottom: ..." kalıbıyla aşamaları ve şevronların anlamını anar.

### 9.4 Y2, panel_members (yeni; 3.6 metni yerine)

Üstte CIFAR bloğu (13 satır, iki sütun CIFAR-10 ve CIFAR-100), altta ImageNetV2 bloğu (14 satır, rol sütunu: panel, eşleşmiş çift, Liu, Mo, ikincil). Dolu kare birincil üye, içi boş kare ikincil üye; ResNet-18 türevleri ayrı bir nokta sütunuyla işaretlenir; XCiT satırı xcit hex'iyle (#CC79A7), CNN üyeleri panel hex'iyle (#999999) çizilir, ImageNetV2 transformer üyeleri ViT-Tiny'ye ayrılmış #D55E00'ı kullanmaz, nötr kenarlı üçgen işaret alır. Satır adları RobustBench kimlikleridir. Veri: `hucre_tablosu.json`, `_b9.json`, `_b8.json` içindeki `modeller.<m>.birincil_panel` ve `ikincil_panel`; çizimden önce üye sayıları föydeki 7, 7 ve 6 ile, matris boyları 20, 15 ve 14 ile (föy 1569, 1826, 1827) karşılaştırılır. Altyazı satır sırasıyla atıfları taşır (her üyenin kaynağı `\cite` ile), ortak ImageNetV2 hattını bir cümleyle anar. Metin kısaltma: EN 03_methodology 193-216, TR 03_yontem 185-208; üye adları ve atıfları metinden çıkar, ortak hat kuralları ve gösterim kalır.

### 9.5 Y4, registry_map (yeni; Tablo 3 yerine)

Tam genişlikte `tablodan_sekle` sütun ızgarası şöyle okunur: aile ve sınama (42 mm), nicelik ve öngörü (45 mm), sayı doğrusu (öngörü eşiği ve ±δ bandı, iki sütun birleşik, yaklaşık 87 mm), çürütme kuralı. Yedi aile satırı (C10 paneli, 2 x 2, saldırı tarafı, maskeleme, C100 yinelemesi, gradyan Mantel, IN-V2 betimsel) aile şeridiyle ayrılır. Karar: ölçülen sonuç işareti çizilmez, çünkü Tablo 3 bir kayıt tablosudur ve sonuçlar Tablo 7, Tablo 9 ve şekil 8'dedir; kayıt ile sonuç aynı şekilde birleşirse kayıt şekli sonucu tekrarlar. Bütün eşikler (0.75, 0.50, 0.30, -0.20, 0.10, 0.5, 10 puan, Mantel boyları) `results/q1/konsey_kayit_kurallari.json`'dan okunur ve föy M13.x satırlarıyla karşılaştırılır; eşikler sayı doğrusunun yanında sayı olarak da basılır, böylece hakem değeri şekilden okuyabilir. Metin kısaltma: EN 03_methodology 282-334 (Tablo 3 satır 300), TR 03_yontem 274-326; Tablo 3 kalkar, karar okuma paragrafı iki cümleye iner.

### 9.6 Y5, prereg_chain (yeni; 3.10 metni yerine)

`yontem_semasi`'nın üst zemin bandı üç panele bölünür: kayıttan önce görülen veriler, 29.10 ana kayıt dondurması ve B2-B6 blokları, 30.10 ek kaydı ve B8-B10 blokları; paneller etiketli ince okla bağlanır (etiket dondurma tarihi ve ön kayıt gövdesinin SHA-256 öneki, föy M9.8 satır 1680-1686). Her blokta model, görüntü ve matris sayısı basılır. Altta 7 mm şeritte iki sapma yazılır. Hedef 60 mm (52 mm bant, 1 mm aralık, 7 mm şerit). Veri: `results/q1/konsey_zaman_cizelgesi.json` (kaynakları `ON_KAYIT_2026-10-29.md`, `ON_KAYIT_EK_B8_B10_2026-10-30.md`, `results/q1/konsey_zincir_durum.tsv`, `results/q1/konsey_b3_defter.tsv`) ve föy M13.x. Metin kısaltma: EN 03_methodology 335 sonrası ve `04z_computational.tex`'in blok süreleri, Tablo 3 altyazısındaki blok cümlesi; TR 03_yontem 327 sonrası.

### 9.7 Şekil 7, source_gap_split (bugün şekil 3)

Üç sütun (CIFAR-10, CIFAR-100, ImageNetV2) ortak satırlarda, sütun başlığı şerittir; simetrik ve yönlü pay yığılı çubuk yerine şablonun nokta ve aralık diliyle çizilir, renk σ yeşil ve ρ turuncu. Veri: `paper/figures/konsey/fig_source_gap_split.kanit.json` (`okunan_anahtarlar`, 58 föy karşılaştırması). Metindeki tek panel atfı (EN `04_experiments.tex` 141, TR `04_deneyler.tex` 141) "the CIFAR-10 panel of Figure N" biçimine döner; altyazı (EN 200, TR 201) veri kümesi adlarıyla konum verir.

### 9.8 Şekil 8, similarity_matrix (bugün şekil 4)

Üç ısı matrisi ortak sıralama ve tek renk ölçeğiyle; ısı haritasının eksen omurgası olmadığı için veri alanı payı ölçülmez (`pay` None), bu madde uygulanmaz diye raporlanır. Veri: `fig_similarity_matrix.kanit.json` (93 karşılaştırma). Altyazı (EN 209, TR 210) veri kümesi adlarıyla.

### 9.9 Şekil 9, cells_interaction (bugün şekil 5)

Üç satır (σ, ρ, ω), başlık rengi aileyi taşır (σ yeşil, ρ turuncu, ω nötr); hücre ortalaması çizgi, koşu işaretçi. Veri: `fig_cells_interaction.kanit.json` (78 karşılaştırma), föy M9.2. Altyazı (EN 322, TR 323) "green title, σ; orange title, ρ; grey, ω". Y6 eklenmez (bölüm 5).

### 9.10 Şekil 10, attack_side (bugün şekil 6)

Tek kart, tohum satırları, saldırıya göre işaretçi; satır adı sütunu en çok 25 mm. Veri: `fig_attack_side.kanit.json` (47 karşılaştırma), föy M9.5. Altyazı değişmez, yalnız kalın giriş alır.

### 9.11 Şekil 11, gradient_alignment (bugün şekil 7)

Düzen bölüm 6'da anlatılan 2 x 3 uyarlamadır. Çift türleri `cift_cnn` (#000000, daire), `cift_vit` (#F0E442, üçgen, siyah kenar), `mixed` (#6E6E6E, kare). Veri: `fig_gradient_alignment.kanit.json` (46 karşılaştırma); Spearman değerleri föy 1970-1975, çift türü sayıları ve ortalama c föy 2009-2011 ile karşılaştırılır. Altyazı (EN 492, TR 493) "(a) to (c)" ve "(d) to (f)" yerine "top row, raw; bottom row, residual" der ve r ile n'nin panelde basıldığını söyler.

### 9.12 Şekil 12, estimates_forest (bugün şekil 8)

Üstte σ etkileri (yeşil başlık), altta ρ terimleri (turuncu başlık); %90 ve %95 aralıklar; ±0.10 bandı yalnız log ölçekte. Veri: `fig_estimates_forest.kanit.json` (76 karşılaştırma). Altyazı (EN 518, TR 519) sol ve sağ kart yerine üst ve alt kart ve renk kodu.

### 9.13 Y7, protocol_settings (yeni; Tablo 13 yerine)

Şekil tek karttır; satırları ayarlardır (C10 L∞, C10 L2, C100, SVHN ve tablodaki öteki ayarlar), her satırda dört protokolün noktası ±SD ve tohum çiftleri; işaret ve ton `protokol` ailesinden (bölüm 4.3), sağ kenarda yayılım değer sütunu. Satır adı sütunu 25 mm, değer sütunu 10 mm, eksen yaklaşık 45 mm (pay yaklaşık 0.53, varsayım). Veri: Tablo 13'ün kaynak yorumlarında anılan dosyalar (EN `04_experiments.tex` 553-575'teki KAYNAK ve FOY satırları; `results/c1_transfer/c1_transfer_summary.json` ve q1 ayar özetleri) ve föy satır 151-201; çizim ajanı önce bu yorumları okur, her çizilen değeri föyle karşılaştırır. Metin kısaltma: Tablo 13 (EN 556, TR 557) kalkar, çevresindeki yaklaşık 150 sözcük iki cümleye iner.

### 9.14 Şekil 14, protocol_sets (bugün şekil 9)

Üstte iç içe dört küme (Y3: her kümenin içinde protokol adı ve maske koşulu; Unconditioned, Target-correct, Both-correct, Successful-source), altta basamaklı asimetri grafiği; başlık şeridi iki panelin adını taşır, A-D harfleri ve (a)/(b) kalkar. Kümeler `protokol` ailesinin dört tonuyla doldurulur (mavi tonlar bırakılır, çünkü #0072B2 R224'ü kodlar); ad her kümede yazılı olduğu için ton tek kanal değildir. Genişlik 88.9 mm'den 85.29 mm'ye iner, böylece 8 pt yazı 7.67 pt basılmaz. Veri: `paper/figures/konsey/fig_protocol_sets.kanit.json` (`veri`: `results/q1/fig_protokol_kumeleri_veri.json`; `results/c1_transfer/c1_transfer_summary.json`; 33 föy karşılaştırması). Maskeler tanımdır, sayı değildir; Tablo 2'nin metninden alınır. Altyazı (EN 579, TR 581) "(a; schematic ...)" yerine "top, ...; bottom, ..." ve protokol adları. Metin kısaltma: Tablo 2 (EN 03_methodology 223; TR 03_yontem 209-254 aralığında) kalkar, 3.7 maskeleri "Fig. N" atfıyla bir cümlede anar.

### 9.15 Şekil 15, spread_clean_gap (bugün şekil 10)

Üst ve alt satır ortak x ekseniyle (temiz doğruluk farkı); sekiz grup `ayar` ailesinin hex'leri ve sekiz ayrı işaret biçimiyle (bugünkü turuncu, yeşil, mavi ve kırmızı-turuncu kodlama anlam renkleriyle çakıştığı için bırakılır). Genişlik 85.29 mm. Veri: `paper/figures/final/fig_spread_clean_gap.kanit.json` (`veri`: `results/q1/fig_yayilim_temiz_fark_veri.json` ve 17 üst kaynak, `ust_kaynaklar_sha256`); TR kanıtı `final_tr/fig_spread_clean_gap.kanit.json`. Altyazı (EN 589, TR 592) (a), (b) ve "the term that panel (a) leaves out" yerine konumla atıf.

### 9.16 Şekil 16, epsilon_sweep (bugün şekil 11)

Tek kart, üç seri, ε ekseni. WRN-28-10 çizgisi `results/wrn_eval/wrn_eval_summary.json`'dan gelir; bu yol karantina kuralının açık yollarının (`results/c1_*`, `results/q1/*`) dışındadır, föy aynı dosyayı satır 354'te kaynak gösterir ve değerleri satır 19'da taşır. Karar: çizgi kalır, çünkü değer föydedir; betikte yol `konsey_ortak.ALLOWED`'a gerekçesiyle eklenir ve kanıta föy satırı yazılır. Veri: `final/fig2_epsilon_sweep.kanit.json` (`kaynaklar`: `results/c1_sweep/pair{1,2,3}/{resnet18,vit_tiny}/*_robustness_results.csv`), föy 352-375; TR `final_tr/fig2_epsilon_sweep.kanit.json`.

### 9.17 Şekil 17, feature_degradation (bugün şekil 12)

Üç satır: CLS dikkat entropisi değişimi (±0.05 nat eşdeğerlik bandı), TV yer değiştirmesi, Y8 ile blok çıkışı kosinüsü; ortak katman ekseni. Veri: `final/fig5b_attention_entropy.kanit.json` (`kaynaklar`: `results/c1_c4/pair{1,2,3}/c4_summary.json`), föy 326-351; Y8 için föy 284-325 ve aynı `c4_summary.json`. TR kanıtı `final_tr/fig5b_attention_entropy.kanit.json`. Altyazı (EN `07_appendix.tex` 119, TR `07_ek.tex` 115) konumla atıf ve üçüncü kart. Metin kısaltma: Tablo 16 (EN 07_appendix 87-) kalkar.

## 10. İş dağılımı ve sıra

Karar: Visio işleri tek ajanda ve sıralı yürür, çünkü aynı anda iki Visio örneği yabancı süreci kapatma riskini taşır ve `visio_tasklist.log` tek yazıcı ister; kart işleri ikinci bir ajanda paralel yürür, çünkü Visio açmaz.

Visio ajanı (Üslup 8) şu sırayla çizer: 1) study_overview, 2) decomposition_schematic, 3) panel_members, 4) design_recipe, 5) registry_map, 6) prereg_chain. İlk üçünün verisi hazırdır; son üçü Ö4 tamamlanmadan başlamaz ve ajan bu durumda o şekli "veri gerekli" diye raporlayıp sıradakine geçer. Ajan ilk iş olarak Ö2 ve Ö3'ü yapar (palet üreteci ve yüz tonu yardımcısı), çünkü ikisi de Visio betiklerinin girdisidir.

Kart ajanı (Üslup 7) şu sırayla çizer: 1) gradient_alignment (M5 düzeltmesinin sınaması; veri alanı payı 0.45'i geçmezse durur ve rapor eder), 2) source_gap_split, 3) similarity_matrix, 4) cells_interaction, 5) attack_side, 6) estimates_forest, 7) protocol_sets (Y3 ile), 8) spread_clean_gap, 9) epsilon_sweep, 10) feature_degradation (Y8 ile), 11) protocol_settings (Y7). Kart ajanı paletin yeni ailelerine (çift türü, protokol, ayar) ihtiyaç duyduğu için Ö2'nin bitmesini bekler; Ö2 Visio ajanının ilk işidir ve kısa sürer.

Kullanıcı ileride "üslup N" yazarsa iki N verilmelidir: şematik için (bugün 8) ve veri için (bugün 7). Motor `SECILI_USLUP`'u `<kök>/figures/` altında ve yalnız ilk satırıyla okur (`motor/figspec/uslup.py` satır 111); dosya `paper/figures/` altında olduğu için okunmaz ve tek satır iki seçimi taşıyamaz. Bu yüzden her betik `--uslup`'u açıkça alır.

## 11. Komut taslakları ve kapılar

`hepsini_ciz.py` betikleri `<kök>/figures/visio` ve `<kök>/figures/charts` altında arar; bu depoda klasör `paper/figures` altındadır ve `VZ_PROJE_KOKU`'yu `paper`'a çekmek proje ayarındaki göreli yolları bozar. Karar: proje tarafında ince bir koşturucu (`paper/figures/_hepsini_ciz_proje.py`) yazılır; koşturucu `motor.host.hepsini_ciz` modülünü içe aktarır, `HERE`'i `<depo>/paper/figures`'a çeker ve `main()`'i çağırır. İki çağrı şöyledir (Git Bash, depo kökünden):

```bash
export MSYS_NO_PATHCONV=1
export VZ_PROJE_KOKU=//wsl.localhost/Ubuntu-22.04/home/firat/projects/adeb_sci_1
export VZ_PROJE_AYARI=$VZ_PROJE_KOKU/paper/figures/visio_cizici.yaml
python paper/figures/_hepsini_ciz_proje.py --uslup 8 --yalniz fig_study_overview \
  fig_decomposition_schematic fig_panel_members fig_design_recipe fig_registry_map fig_prereg_chain
python paper/figures/_hepsini_ciz_proje.py --uslup 7 --yalniz fig_gradient_alignment \
  fig_source_gap_split fig_similarity_matrix fig_cells_interaction fig_attack_side \
  fig_estimates_forest fig_protocol_sets fig_spread_clean_gap fig_epsilon_sweep \
  fig_feature_degradation fig_protocol_settings
```

Şekil başına kapılar sırayla şunlardır; biri düşerse şekil kurulmaz.

| Kapı | Komut ya da ölçü | Geçme koşulu | Hangi şekiller |
| --- | --- | --- | --- |
| K1 | Visio kontrolcüsü (`vf.run()`), geri okuma | PASS, en büyük sapma 0.01 mm altı, etiket-küp arası en az 1.0 mm | Visio |
| K1' | kart denetçisi (`mmcheck`) | PASS, 0 sorun, her kartta `n = ...` ya da gerekçe (D6) | kart |
| K2 | `python $V/motor/host/fig_mm_pdf.py --assets <yapım> --figure <kök> --uslup <N> --json-out paper/figures/qc/<kök>/mm_pdf.json` | 0 sorun, en küçük basılı yazı 8.0 pt | hepsi |
| K3 | `python $V/motor/host/denge.py --assets <yapım> --figure <kök> --uslup <N> --out paper/figures/qc/<kök>/denge.json` (yanıt dosyası `<kök>.denge_ajan.json`) | kurulabilir; veri şekillerinde veri alanı payı en az 0.45, muafiyetsiz | hepsi |
| K4 | `python $V/motor/host/fig_qc.py --assets <yapım> --tex paper/figures/qc/main_en_duz.tex --venue ieee_access --figure <kök> --out paper/figures/qc/<kök>`; yeni şekillerde `--tek-sekil-tex --caption "..." --kind single|double` | PASS, bloklayıcı yok | hepsi |
| K5 | kanıt dosyasının föy karşılaştırması | `uyusmayan` 0; föy özeti bugünkü föyün özeti | hepsi |
| K6 | yükseklik | bölüm 9 tavanı ve 165.33 mm | hepsi |
| K7 | manifestin `three_d` kaydı | tek görünüm (eğik 25, 0.5), her nesnede iki basamak en az 0.05 | 1, Y1, 2, Y2 |

Makale düzeyi kapılar bütün şekiller çizilip yazım ajanı metni değiştirdikten sonra koşar: M-K1 `python $V/scripts/zenginlik.py --assets paper/figures --tex paper/figures/qc/main_en_duz.tex --makale` (harfli pay en çok 0.40, ardışık aynı tür en çok 2); M-K2 `fig_qc.py --consistency --assets paper/figures` (tek 3B görünüm, hex-aile ihlali 0); M-K3 düz kopyalar yeniden üretilip `panel_atif_sayaci.py` EN ve TR (`--dil tr`) için yeniden koşulur ve yeni şekillerin yorum satırları `panel_yapisi.yaml`'da açılır; M-K4 `included_figures.py --tablo` düz kopyada 17 şekil verir; M-K5 EN el yazması derlenir ve 26 sayfayı aşmaz; M-K6 kurulum (`motor/visio/install.py`) ve `ESLEME.md`.

## 12. Varsayımlar, doğrulanmamış noktalar ve açık sorunlar

1. Şekil 7'nin 0.74'lük veri alanı payı, Y7'nin 0.53'ü ve öteki hedef yükseklikler çizilmeden önceki kestirimlerdir; karar `denge.py` ve `fig_mm_pdf.py` ölçümüyle verilir.
2. Sayfa bütçesindeki serbest kalan metin yazım ajanının kısaltmasına bağlı bir üst sınırdır; bölüm 7'deki aralık (-0.16 ile -0.65 sayfa arası) bu belirsizliği taşır.
3. IEEE Access'in sayfa sınırı, en küçük punto kuralı ve "Drawing drafts" ek dosya kuralı bu oturumda dergi kılavuzundan okunmamıştır; 26 sayfa görev metninden, 8.0 pt ve 0.70 sınıf ölçüsünden ve LaTeX varsayılanından gelir.
4. `yuz_tonlari` yardımcısı motorun iç sözlüğünü geçici olarak değiştirir; skill'e varlık başına yüz tonu parametresi eklenmesi önerilir (skill sahibine açık sorun).
5. `palette_mod.load`'un varlık kaydındaki bilinmeyen alanlara davranışı sınanmadığı için 3B yüzleri ayrı dosyaya yazılır.
6. TR aynası bugün şekil 1-9'u İngilizce etiketli konsey PDF'leriyle basar (`03_yontem.tex` 28, `04_deneyler.tex` 200-580). Karar: bu çizim fazı EN şekilleri üretir, TR şekilleri aynı betiklerin dil seçeneğiyle ikinci turda üretilir, çünkü etiket metni şeklin ölçüsünü değiştirir ve her dil kendi kapılarından geçmelidir; TR şekil 10-12 için bugün `final_tr/` vardır.
7. CIFAR görüntülerinin basım lisansı bu oturumda denetlenmemiştir; şekil 1 ve Y2 destelerinin ön kartı yalnız test kümesinin ilk dört görüntüsünü gösterir ve kaynağı manifeste yazılır.
8. Föy M13 satır numaraları bilinmiyor; plan "M13.x" yer tutucusunu kullanır ve çizim ajanı gerçek satırı föyden okuyup kanıta yazar.
