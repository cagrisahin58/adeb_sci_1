# Toplama C2: literatür boşluğu web taraması (mercek C, 2026-10-04)

## Özet (10 satır)
1. Tarama 5 konu başlığı için WebSearch ile yapıldı; aday başına arXiv özet sayfası WebFetch ile çekildi (VERIFIED = sayfa çekildi, başlık/yazar/tarih okundu).
2. Konu 1 (örnek kümesi/payda): kayda geçen tek doğrulanmış metin deepfake dedektörleri üzerine 2609.10002; ASR'yi hedefin önceden doğru sınıflandırdığı küme üzerinde tanımlıyor (Sec. 3.2, html sürümü).
3. Konu 1: payda seçimini ayrı bir metodolojik değişken olarak ölçen makale BULUNAMADI. Reliable Evaluation (2306.08565) ve TA-Bench (2311.01323) zaten references.bib içinde.
4. Konu 2: ViT-CNN transfer yönü için arama yalnız saldırı-yöntemi makaleleri döndürdü (TESSER 2505.19613, Springer 2021, Defense That Attacks 2512.02830); CIFAR'da çekişmeli eğitimli çift için yön asimetrisi ölçen yeni makale BULUNAMADI.
5. Konu 3: robust = clean x koşullu eşitliğini ve raw = clean_err + cond*(1-clean_err) kimliğini türetilmiş halde yazan makale BULUNAMADI. Arama motoru özeti çarpımı tanımladı ama kaynak belirtmedi (UNVERIFIED); GF-Score (2604.12757) çekildi, bu ilişkiyi içermediği fetch çıktısında belirtildi.
6. Konu 4: 2023-2026 değerlendirme/benchmark: TAA-Bench, SoK Pitfalls, BlackboxBench, Cox&Bunzel 2511.05102 doğrulandı; Reliable Evaluation, TA-Bench, TPAMI Revisiting zaten bib'de.
7. Konu 5: IEEE Access/TPAMI/TIFS 2025-26 CNN-ViT + AutoAttack + CIFAR-10 karşılaştırması için doğrudan eşleşen yayın BULUNAMADI; en yakın doğrulanan TIFS 2025 PIAT (2511.00836, yöntem makalesi; AutoAttack/CIFAR-10 içeriği özetten teyit edilemedi).
8. 64 bib girdisinin başlıkları tarandı; Tablo A adaylarının hiçbiri bib'de yok, bib'de olanlar Tablo B'de.
9. Tam metin çekimi PDF ikili içerik/boyut nedeniyle başarısız oldu (2306.08565, 2112.14337); bu ikisinin örnek-seçimi cümleleri doğrulanamadı.
10. Hiçbir referans uydurulmadı; UNVERIFIED etiketli satırlar yalnız arama motoru özetine dayanır.

## Tablo A: doğrulanmış adaylar (arXiv sayfası çekildi)
| # | Başlık | Yazarlar | Yıl/Mecra | ID | Durum | İki cümle özet | bib'de mi |
|---|---|---|---|---|---|---|---|
| A1 | What Makes Adversarial Examples Transfer Across Deepfake Detectors? | Mamede, Neto, Sequeira | 2026-09-09, arXiv | 2609.10002 | VERIFIED | 60 dedektörde uyumluluk etkenlerini (ortak omurga, ön eğitim, veri) inceler; çoklu kaynak 64.48% ASR, önceki tek kaynak ortalamaları 7.21-19.52%. Sec. 3.2 (html): "Transfer success is defined as ASR = 1/\|C_t\| sum_{i in C_t}[...]", C_t = hedefin pertürbasyondan önce doğru sınıflandırdığı görüntüler. | Hayır |
| A2 | Quantifying the Risk of Transferred Black Box Attacks | Cox, Bunzel | 2025-11-07, arXiv cs.CR | 2511.05102 | VERIFIED | Aktarılan saldırı riskini CKA ile seçilen vekil modellerle tahmin eden test çerçevesi önerir. Özette koşullu örnek kümesi tartışması yok. | Hayır |
| A3 | Benchmarking Transferable Adversarial Attacks | Jin, Zhang, Zhu, Chen | 2024, NDSS Workshop | 2402.00418 | VERIFIED | Aktarılabilirlik yöntemlerini sınıflandırır, on yöntemi birleştiren TAA-Bench sunar. Payda tartışması özette yok. | Hayır |
| A4 | SoK: Pitfalls in Evaluating Black-Box Attacks | Suya, Suri, Zhang, Hong, Tian, Evans | SaTML 2024 | 2310.17534 | VERIFIED | Kara kutu saldırılar için taksonomi (geri bildirim, sorgu erişimi, yardımcı veri) ve güçlü taban çizgiler; çalışma maliyetinin raporlanmasını ister. Doğrudan transfer paydası değil. | Hayır |
| A5 | BlackboxBench: A Comprehensive Benchmark of Black-box Adversarial Attacks | Zheng, Yan, Zhu, Chen, Wu | arXiv 2023-12, rev. 2025-05 | 2312.16979 | VERIFIED | 29 sorgu-tabanlı ve 30 transfer-tabanlı saldırı, 14,950 değerlendirme. | Hayır |
| A6 | TESSER: Transfer-Enhancing Adversarial Attacks from Vision Transformers via Spectral and Semantic Regularization | Guesmi, Ouni, Shafique | arXiv 2025-05 (rev. 2025-09) | 2505.19613 | VERIFIED | ViT kaynaklı saldırıların CNN ve çekişmeli eğitimli hedeflere aktarımını FSGS ve spektral düzgünlük ile artırır. Arama özeti: geleneksel saldırılarda ViT'ten CNN'e aktarım bozulur (tam metin UNVERIFIED). | Hayır |
| A7 | Defense That Attacks: How Robust Models Become Better Attackers | Awad, Akrm, Gomaa | arXiv 2025-12 (v3) | 2512.02830 | VERIFIED | 36 CNN/ViT modelde çekişmeli eğitimli modellerin daha aktarılabilir pertürbasyon ürettiğini bildirir; robustluk değerlendirmesine "saldırgan olma eğilimi" eklenmesini önerir. | Hayır |
| A8 | VanillaBench: The Hidden Accuracy Cost of Adversarial Robustness | Bunzel | arXiv 2026-07-14 | 2607.12545 | VERIFIED | 186 çekişmeli eğitimli modeli vanilla tabanla karşılaştırır; temiz doğruluk farkı -7.7 ile -29.5 puan. Temiz doğruluk ile robustluk ayrışımına komşu. | Hayır |
| A9 | GF-Score: Certified Class-Conditional Robustness Evaluation with Fairness Guarantees | Shah, Visavadiya, Padala | arXiv 2026-04-14 | 2604.12757 | VERIFIED | Sertifikalı robustluğu sınıf profillerine ayırır. Fetch çıktısı: temiz doğruluk x koşullu robustluk çarpım formülünü yazmaz. | Hayır |
| A10 | A Little Robustness Goes a Long Way: Leveraging Robust Features for Targeted Transfer Attacks | Springer, Mitchell, Kenyon | NeurIPS 2021 | 2106.02105 | VERIFIED | Hafif robust kaynak sınıflandırıcılar hedefli aktarımı artırır; etki CNN-transformer arasında da sürer. | Hayır |
| A11 | Parameter Interpolation Adversarial Training for Robust Image Classification | Liu, Yang, He, Hopcroft | IEEE TIFS 2025 | 2511.00836 | VERIFIED (özet) | CNN ve ViT için çekişmeli eğitim çerçevesi (PIAT). AutoAttack/CIFAR-10 içeriği özetten doğrulanamadı; karşılaştırma değil yöntem makalesi. | Hayır |
| A12 | Measuring the Transferability of Adversarial Examples | Petrov, Hospedales | arXiv 2019-07 | 1907.06291 | VERIFIED | VGG/Inception ailelerinde FGSM/BIM/CW aktarılabilirliğini güçlü parametrelerle yeniden ölçer. 2021 öncesi, kayıt için. | Hayır |
| A13 | Properties that allow or prohibit transferability of adversarial attacks among quantized networks | Shrestha, Grossmann | arXiv 2024-05 | 2405.09598 | VERIFIED | Nicelenmiş ağlar arası aktarım. Arama özeti kaynak ve hedefin ikisinin doğru sınıflandırdığı 1000 örneklik alt küme kullanıldığını söyler (tam metin UNVERIFIED). | Hayır |
| A14 | The Space of Transferable Adversarial Examples | Tramèr, Papernot, Goodfellow, Boneh, McDaniel | arXiv 2017 | 1704.03453 | VERIFIED | Aktarılabilirliği ~25 boyutlu ortak alt uzayla açıklar. 2021 öncesi. | Hayır |

## Tablo B: bib'de zaten bulunan, aramada görülen ilgili makaleler
| Başlık | ID (bib) | bib anahtarı | Not |
|---|---|---|---|
| Reliable Evaluation of Adversarial Transferability | 2306.08565 | yu2025reliable (references.bib:460-467, SaTML 2025) | Arama özeti: üç protokol, aktarılabilirliğin abartıldığı. Örnek-seçimi cümlesi tam metinden doğrulanamadı. |
| Towards Evaluating Transfer-based Attacks Systematically, Practically, and Fairly | 2311.01323 | li2023tabench (:439-447) | TA-Bench, 30+ yöntem, 25 model. |
| Revisiting Transferable Adversarial Images | 2310.11850 | zhao2025revisiting (:470-479, TPAMI) | 23 saldırı, 9 savunma; adil hiperparametre. |
| Closer Look at the Transferability of Adversarial Examples | 2112.14337 | waseda2023closer (:450-457) | Arama özeti kaynak ve hedefin doğru sınıflandırdığı, kaynağı aldatan örnekler üzerinde ölçüm der (alıntı doğrulanamadı). |
| Adversarial Robustness Comparison of Vision Transformer and MLP-Mixer to CNNs | 2110.02797 | benz2021adversarial (:388-394) | Yön iddiası makalede atıflı. |
| On Improving Adversarial Transferability of Vision Transformers | 2106.04169 | naseer2022improving (:213-218) | |
| Towards Transferable Adversarial Attacks on Vision Transformers | 2109.04176 | bib'de başlık var | |
| On the Robustness of Vision Transformers to Adversarial Examples | 2104.02610 | bib'de eprint var (:190) | |

## Tablo C: bulunamayan içerik (negatif sonuçlar)
| Konu | Arama | Sonuç |
|---|---|---|
| (1) payda/koşullama seçimi metodolojik değişken | 3 sorgu | Yalnız koşullamayı kullanan makaleler (A1, A13, Waseda); seçimi değişken olarak ölçen çıkmadı |
| (2) CIFAR'da çekişmeli eğitimli ResNet/ViT çifti, yön asimetrisi | 2 sorgu | Saldırı-yöntemi makaleleri; ölçüm makalesi çıkmadı |
| (3) robust = clean x cond ve raw = e + c(1-e) kimliği | 1 sorgu | Arama özeti çarpımı anlatıyor, kaynak yok (UNVERIFIED); GF-Score teyit etmedi |
| (5) 2025-26 IEEE Access/TPAMI/TIFS CNN-ViT AutoAttack CIFAR-10 | 2 sorgu | Doğrudan eşleşen yok; sonuçlar PIAT (TIFS 2025) ve bib'deki 2021 makaleleri |

## Tablo D: manuscript bağlamı (karşılaştırma için)
| Olgu | Konum |
|---|---|
| Payda seçimi dört seçenek olarak sayılır (tüm örnek, hedef-doğru, ikisi doğru, kaynak saldırısı başarılı) | paper/manuscript/sections/01_introduction.tex:11 |
| İlk katkı: asimetri +4.4 ile +19.4 puan, dört koşullama protokolü | 01_introduction.tex:23 |
| İkinci katkı: raw = clean_err + cond*(1-clean_err), 0.41 puan içinde; mutlak robustluk temiz doğruluk ve koşullu duyarlılığa tam ayrışır | 01_introduction.tex:25 |
| Yön tartışması atıfları: mahmood2021robustness, benz2021adversarial, shao2022adversarial, naseer2022improving | 01_introduction.tex:9 |
| Önceki sürüm ATEEC 2026'ya gönderildi | 01_introduction.tex:31 |
