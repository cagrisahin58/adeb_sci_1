# E6 Ön-Kaydı — L2 tehdit modeli (yazım: 2026-08-20, HİÇBİR L2 ÖLÇÜMÜ GÖRÜLMEDEN)

**Bu belge SALT EKLEMELİDİR (K4).** Aşağıdaki satırlar herhangi bir L2 sonucu
üretilmeden önce yazılmıştır. Sonuçlar geldikten sonra eski satırlar
düzeltilmez; yeni bir EK yazılır ve eskisine açıkça atıf yapılır.

**Durum:** kod hazır, koşum **E7 bittikten sonra** başlatılacak (GPU çakışması
olmasın diye). Koşucu: `scripts/q1_e6_l2.sh`.

---

## 0. E6 neden var — ve neyi İDDİA ETMEZ

Makalenin tezi "ölçüm protokolü sonucu belirler"dir. Şimdiye kadar protokol
ekseni **koşullama** (hangi örnekler paydaya girer) olarak tanımlandı. E6,
**beşinci bir eksen** ekliyor: tehdit modelinin kendisi. Aynı modeller, aynı
veri, farklı ölçüm aleti.

**E6'nın İDDİA ETMEDİĞİ şey — bu satır bağlayıcıdır:**

> Değerlendirilen modeller **L∞ ile çekişmeli eğitilmiştir** (ε = 8/255).
> E6 onları **L2 bütçesi altında ölçer**. Bu, modellerin L2-gürbüz olduğu
> iddiası **değildir** ve çıkan mutlak sayılar RobustBench'in **L2-eğitilmiş**
> girdileriyle (ör. Engstrom, CIFAR-10 L2: 90,83 temiz / 69,24 AA)
> **karşılaştırılamaz**. Karşılaştırma yapılırsa çapraz-norm bir hatadır.
> E6'nın taşıdığı tek nicelik, **protokol yayılımının** ve **ham−koşullu ~
> temiz-hata ilişkisinin** norm değişince ne yaptığıdır.

---

## 1. Sabitlenen tasarım (değiştirilmeyecek)

| öğe | değer | gerekçe |
|---|---|---|
| veri kümesi | CIFAR-10 **yalnız** | CIFAR-100 için RobustBench L2 tablosu yok (rapor §E6 doğrulama hükmü) |
| modeller | C1 ana çiftin 3 tohumu (L∞-AT final checkpointleri) | L∞ sonuçlarıyla **aynı** ağırlıklar; tek değişen ölçüm aleti |
| norm | L2 | — |
| ε | **0,5** | CIFAR-10 L2 için yerleşik standart (RobustBench / Madry robustness lib) |
| PGD-L2 | steps = 10, α = 2,5·ε/steps = **0,125** | yaygın kural; L∞ tarafındaki steps=10 ile eşlenik |
| PGD-L2 örnek sayısı | **10.000 (tam test kümesi)** | ucuz; L∞ ile birebir karşılaştırılabilir |
| AutoAttack-L2 | standard suite, ε = 0,5 | — |
| AA-L2 örnek sayısı | **5.000** | bütçe indirimi (rapor §E6: n=5k → ~5 GPU-saat) |
| AA-L2 altkümesi | yükleyici sırasının **ilk 5.000'i**, seed 42, karıştırma YOK | önceden sabitlenir ki sonuç görülüp altküme seçilemesin |
| protokoller | L∞ ile **aynı dördü** (ham / hedef-doğru / her-ikisi-doğru / başarılı-kaynak) | — |

**AA-L2'nin n=5.000, PGD-L2'nin n=10.000 olması bir TUTARSIZLIK DEĞİL,
beyan edilmiş bir bütçe kararıdır.** Makaleye böyle yazılacaktır; iki sayı
aynı cümlede aynı örnek kümesinden geliyormuş gibi sunulmayacaktır.

---

## 2. Kayıtlı ön-kestirimler (sonuç görülmeden)

Rapor §E6 tek cümlelik ön-kestirimi şöyle koymuştu: *"ham−koşullu ~ temiz-hata
ilişkisi saldırı-agnostik olmalı."* Burada **sınanabilir** hâle getiriliyor:

**Ö1 (yön).** L2 altında da ham transfer oranı ile koşullu oran arasındaki
sapma, hedefin temiz hatasıyla **pozitif** ilişkili olacaktır (eğim > 0).

**Ö2 (protokol yayılımı sıfırdan farklı).** Dört protokol arasındaki asimetri
yayılımı L2 altında da **en az 2 puan** olacaktır. *(Alt sınır bilinçli olarak
düşük tutuldu: E6'nın işi yayılımın L∞'dakiyle aynı BÜYÜKLÜKTE olduğunu
göstermek değil, norm değişince YOK OLMADIĞINI göstermektir.)*

**Ö3 (işaret).** CNN→ViT asimetrisinin işareti L2 altında da dört protokolün
tamamında **pozitif** kalacaktır.

**Ön-kestirim TUTMAZSA ne olur:** hüküm geri çekilmez, **raporlanır** (K8).
Tutmayan bir ön-kestirim, tezin tehdit modeline duyarlı olduğunu gösterir ve
bu makalenin sonucudur — gizlenecek bir şey değildir.

---

## 3. Analiz-uygunluk kuralları (K5: yeni DURDURMA eşiği DEĞİL)

Bunlar koşumu durdurma kapıları değildir; hangi çıktının analize gireceğini
önceden belirler.

- **U1.** Bir tohum çifti analize girer ancak ve ancak her iki model için de
  PGD-L2 örnek-bazlı çıktısı üretilmişse. Yarım çıktıyla analiz yapılmaz (K6).
- **U2.** AA-L2 üretilemezse (bellek/süre), **PGD-L2 tek başına** raporlanır ve
  AA-L2'nin koşulamadığı **yazılır**. Sessiz düşürme yasaktır.
- **U3.** Mutlak L2 sayıları düşük çıkarsa (L∞-eğitilmiş modeller L2 altında
  zayıf olabilir) bu **beklenen** bir sonuçtur ve iddiayı değiştirmez;
  §0'daki bağlayıcı satır uyarınca L2-eğitilmiş referanslarla kıyaslanmaz.
- **U4.** Eğer temiz doğruluk L2 değerlendirmesinde L∞ koşumundaki değerden
  farklı çıkarsa, bu bir **hata belirtisidir** (temiz doğruluk saldırıdan
  bağımsızdır); analiz durdurulur ve sebep aranır. Bu bir sağlama testidir.

---

## 4. Bu ön-kayıt ne zaman yazıldı — kanıt

Bu dosya, `results/q1/cifar10_l2/` dizini **var olmadan** ve hiçbir L2 çıktısı
üretilmeden önce commit edilmiştir. Git geçmişi bu sıralamanın kanıtıdır.
E6 sonuçları geldiğinde bu belgeye **EK A** olarak eklenecek, yukarıdaki
satırlar değiştirilmeyecektir.
