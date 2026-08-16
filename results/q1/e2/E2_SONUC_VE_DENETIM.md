# E2 Sızıntı Ablasyonu — Sonuç ve Çürütme Denetimi

**Durum:** kampanya tamam (18/18 hücre, 6 tam-bütçe yörünge), ön-kayıtlı
analiz koşuldu, sonuç 4 mercek + 3 şüpheci hakemden oluşan bir çürütme
denetiminden geçirildi (2026-08-16/17).

**Tek cümlelik hüküm:** Sızıntının checkpoint seçimine etkisi **saptanamadı**;
buna karşılık **seçim protokolünün kendisi** (hangi temiz bölme seçim yapıyor,
eğri yumuşatılıyor mu) sabit bir yörüngede raporlanan PGD-10 doğruluğunu
**1,67 puana kadar** oynatıyor — bu, eğitim-tohumu yayılımının (0,55 puan) üç
katı. E2'nin makaleye giren katkısı budur.

---

## 1. Ham sonuçlar (ön-kayıtlı analiz, `e2_report.json`)

| Kol | Seçilen epok A/B/C | Δ_AB (sızıntı) | Δ_BC (gürültü tabanı) |
|---|---|---|---|
| ResNet s1001 | 63 / 63 / 32 | 0,00 | +0,82 |
| ResNet s1002 | 49 / 49 / 49 | 0,00 | 0,00 |
| ResNet s1003 | 45 / 44 / 60 | +0,30 | −0,32 |
| **ResNet ort.** | | **+0,100 ± 0,173** | **+0,167 ± 0,588** |
| ViT s2001 | 19 / 28 / 18 | −1,04 | +1,67 |
| ViT s2002 | 18 / 20 / 20 | −1,06 | 0,00 |
| ViT s2003 | 36 / 28 / 28 | −1,05 | 0,00 |
| **ViT ort.** | | **−1,050 ± 0,010** | **+0,557 ± 0,964** |

## 2. Çürütme denetiminin hükmü: atıf düzeyinde ARTEFAKT

**Gerçek olan:** e_A ve e_B farklı checkpoint'lerdir ve aralarında ~1,1 puanlık
gerçek bir kalite farkı vardır (bağımsız tahminciler birleşimi θ = −1,108 ±
0,183; homojenlik χ²(5)=7,23, p=0,204). Veri bütünlüğü 18/18 temiz.

**Artefakt olan:** bu farkın **sızıntıya atfedilmesi**. Dürüst kanıt gücü,
tasarımla eşleşen (ortak-bölme, seçicilerden ayrık değerlendirici) null'larda
**iki yönlü p = 0,10–0,19** (dört bağımsız kuruluş) — manşetle 3-4 büyüklük
mertebesi fark var.

### Geri çekilen sayılar
- **s_Δ = 0,010** tekrarlanabilirlik değil **tesadüf**: tek ölçümün eşleşmiş
  SE'si 0,372; P(s ≤ 0,010 | gerçek Δ'lar özdeş) = 7,2×10⁻⁴. Aynı üç
  checkpoint çifti ayrık tahmincilerle ölçüldüğünde sd = 0,97 / 1,13 / 1,32.
- **t_p = 3×10⁻⁵** bu varyans deflasyonunun ürünüdür.
- **Havuzlanmış McNemar p = 10⁻⁶** yanlış niceliği ölçer (checkpoint çiftini
  sabit alır); negatif kontrolde de ateşliyor (§6b'nin önceden ilan ettiği
  %37-56 yanlış-pozitif oranıyla uyumlu).

### Öldürücü üç itiraz
1. **Mekanizmanın tek olası kanalında araç yok.** Yörünge sabit olduğundan
   sızıntı Δ_AB'yi ancak V_A'nın adv eğrisini bozarak etkileyebilir. Ölçülen:
   V_A adv fazlası ViT'te −0,47/−0,55/−0,08 (işaret negatif). **Çift ayrışma:**
   ResNet'te sızıntı izi var (clean fazlası +1,81/+1,59/+2,10, z≈+2,0…+2,3)
   ama etki yok; ViT'te iz yok (z≈0) ama "etki" var.
2. **Manipülasyon kontrolü ViT'te başarısız.** Clean ön-eğitim iki kolda da
   V_A'yı ezberledi (%100 train acc), ama AT epoch 1'de beklenen fazlanın
   ViT'te yalnız **<%7'si** ölçülüyor (+0,45/+0,12/+1,25 vs beklenen ~+19,6),
   ResNet'te ~%50'si (ve 100 epok kalıcı). **ViT kolunda tedavi fiilen
   uygulanmamıştır** — ölçülecek sızıntı yoktur.
3. **Karşılaştırıcı keyfiliği + sahte-tekrarlama.** V_B ↔ V_C takası manşeti
   −1,05 → −0,49'a (p=0,47) taşıyor. V_A/V_B/V_C tek çekiliştir (seed 778,
   altı koşumun hepsi aynı dosya): **bölme düzeyinde etkin n = 1**, üç tohum
   yörüngeyi tekrarlar, tedaviyi değil.

### Çürütülen yan hikâyeler
- "ViT'in tepesi keskin, ResNet'inki düz" **yanlış**: gürültüden arındırılmış
  ölçümde ResNet'in manzarası 2 kat daha engebeli (komşu-epok gerçek kalite
  değişimi ResNet 1,88-2,16 vs ViT 0,94-1,06); iki bölmenin aynı epoğu seçme
  olasılığı ResNet s1001'de 0,371, ViT s2002'de 0,852.
- ResNet'in Δ_AB = +0,10'u "sızıntıya bağışıklık" değil, **seçim çakışması**
  (null'da bu desenin olasılığı ≈0,25).

## 3. Makaleye giren ifadeler

**Kurulabilir (asıl bulgu):** *"Sabit bir eğitim yörüngesi üzerinde, yalnızca
hangi 2000-örneklik doğrulama bölmesinin checkpoint seçtiği değiştirildiğinde
— her iki bölme de eğitimde hiç görülmemişken — aynı 10k test kümesinde
raporlanan PGD-10 doğruluğu ViT-Tiny'de 1,67, ResNet-18'de 0,82 puana kadar
oynamaktadır; aynı eğriye üç-epokluk hareketli ortalama uygulanması seçilen
epoğu ve farkın işaretini değiştirmektedir (V_C üzerinde ortalama Δ: k=1 →
−0,92, k=3 → +0,10, k=5 → +0,30)."*

**Kurulabilir (sızıntı, §4 Kural 3 uyarınca):** ViT'te gözlenen −1,05 puanlık
fark raporlanır ama **sızıntıya atfedilmez**; simetrik tahminci
Δ_{A−(B+C)/2} = −0,77 ± 0,49 sıfırı içerir, dürüst p = 0,10–0,19.

**KURULAMAZ (yasak cümleler):**
- "Seçim sızıntısı ViT'te ~1,05 puan gürbüzlük kaybettiriyor (p=3e−5)."
- "Etki üç tohumda tekrarlanabilir / sd=0,01."
- "|Δ_AB| ≫ |Δ_BC|; sızıntı etkisi nicelenmiştir." (§4 Kural 2 dili —
  eşleşmiş |Δ_AB|−|Δ_BC| = +0,49 ± 0,97, %95 GA sıfırı içeriyor)
- "Sızıntı ViT'i etkiliyor, CNN'i etkilemiyor" (etkileşim p = 0,098-0,109)
- "V_C negatif kontrolü gürültü tabanının küçük olduğunu doğruluyor"
  (negatif kontrol ateşliyor: ViT B-C clean p = 8,9×10⁻¹³)
- Herhangi bir mekanizma cümlesi ("sızıntılı bölme ezberci checkpoint'leri
  ödüllendiriyor")
- "Sızıntı katkısı protokol yayılımının ~1/10'u" (ölçek uyumsuzluğu: 10,45
  puan **transfer asimetrisinin** protokol yayılımı, E2'nin 1,05'i ise
  **mutlak gürbüz doğruluk** farkı — aynı cetvele konulamaz)

## 4. Zorunlu sınırlamalar (makalede beyan)

1. Ortak bölme / sahte-tekrarlama: bölme düzeyinde n=1; s_Δ sızıntı bileşeni
   hakkında sıfır bilgi taşır (ön-kayıt §6'da önceden beyan edilmişti).
2. Varyans deflasyonu: s_Δ=0,010 tek ölçüm SE'sinden 37 kat küçük.
3. n=3 güç tabanı: dürüst σ≈0,53-0,70 ile MDE = 1,32-1,74 puan; n=3'te işaret
   permütasyonunun ulaşabileceği en küçük iki yönlü p = 0,25.
4. δ=1,0 kırılganlığı: δ* = 1,067 — δ=1,05'te "FARKLI", δ=1,07'de "EŞDEĞER".
   Ayrıca δ eğitim-tohumu std'sine (0,55) kalibre edilmişti; ilgili bileşen
   seçim gürültüsüdür (§2'nin kendi hesabı 1,55 puan).
5. Karşılaştırıcı keyfiliği (B↔C takası).
6. Çoklu karşılaştırma: 2 mimari × 3 ikili kontrast × 2 metrik = 12 hücre;
   ön-kayıt suskun. Dürüst p=0,10 ile Bonferroni m=2 → 0,20.
7. Uç nokta bağımsız değil: 18 hücrede seçim ve raporlama **aynı saldırı**
   (PGD-10, eps 8/255, seed 42); AutoAttack yok.
8. Val→test aktarımı zayıf: 9 epok çiftinde eğim +0,457, artık sd 0,790 puan
   → **P0 ile giderildi** (bkz. §5).

## 5. Yapılanlar / yapılacaklar

- **P0 (koşuldu):** `scripts/q1_e2_test_curve.py` — 6 yörünge × 100 checkpoint
  için tam 10k test clean/PGD-10 + örnek maskeleri
  (`testcurve_<arch>_s<seed>.npz`). Tüm betimleyici analizler artık vekil val
  yerine **birincil uç noktada** yapılabilir; gerçek test-optimal epok bilinir.
- **Yapılmayacak:** E4'ün +2 tohumu bu soruna **çare değildir** (aynı bölmeyle
  tohum eklemek deflasyonu tekrarlar; eksik boyut tohum değil **bölme
  çeşitliliği**). Sızıntı iddiası taşınmayacağı için P1 (sızıntı-takası, 21
  GPU-saat), P1b (pozitif kontrol/doz-yanıt, 21 GPU-saat) ve P2 (K bağımsız
  bölme çekilişi, K=5 için ~105 GPU-saat) **şimdilik koşulmayacak**; hakem
  talebi gelirse öncelik P1b → P1 → P2.
- **Düzeltilecek metin:** `paper/manuscript/sections/05_discussion.tex:80`
  taahhüt edilen ablasyonun uç noktasını "koşullu atıf ters dönüyor mu" diye
  tanımlıyor; E2 bunu ölçmüyor (uç nokta: seçilen checkpoint'in test PGD-10
  doğruluğu). Taahhüt metni E2'nin gerçek uç noktasıyla hizalanacak.

## 6. Tez cümlesi (E2'den türetilebilecek en güçlü hali)

> "Ölçüm protokolünün yalnızca checkpoint-seçim bileşeni — hangi hiç
> görülmemiş 2000-örneklik bölmenin seçim yaptığı ve eğrinin yumuşatılıp
> yumuşatılmadığı — sabit bir yörünge üzerinde raporlanan PGD-10 doğruluğunu
> 1,67 puana kadar oynatmaktadır; bu, aynı mimarinin eğitim-tohumu yayılımının
> (0,55 puan) üç katıdır. Seçim sızıntısının bu yayılıma ek katkısı ise tek
> bölme çekilişiyle ayrıştırılamamış ve saptanamamıştır (dürüst iki yönlü
> p = 0,10-0,19)."

Bu bileşen **sıfır-şişkin ve kesiklidir**: iki temiz bölme ya aynı epoğu seçer
(Δ=0) ya da farklı seçer ve 1-2 puan fark üretir — yani gürbüzlük sayısı
sürekli bir gürültüyle değil, **manzara dejenere olduğunda ateşlenen bir
piyangoyla** oynuyor.
