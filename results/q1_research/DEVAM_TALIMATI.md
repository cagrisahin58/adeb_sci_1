# DEVAM TALİMATI — Q1 kampanyasını bitirme kılavuzu

**Son güncelleme: 2026-08-20 (akşam). Dal: `q1`. Son commit: `54e8b6e`.**

> ## GÜNCEL DURUM — 2026-08-21, KAMPANYA TAMAMLANDI
>
> **Altı işin altısı da bitti. Koşan iş yok, GPU boş.**
>
> | iş | durum | commit |
> |---|---|---|
> | İŞ-1 `r=0,997` nitelemesi | bitti | `fe86f48` |
> | İŞ-2 E1+E2 makaleye | bitti | `9707337` |
> | İŞ-3 E7 (SVHN) | bitti — 8/8 eğitim + analiz | `c24bb22`, `8c01e47` |
> | İŞ-4 E3 (kalibrasyon) | bitti — 116 nokta / 8 küme, iki kol | `7148fd9` |
> | İŞ-5 E6 (L2) | bitti — PGD + AutoAttack | `920a646` |
> | İŞ-6 sekiz kalem | bitti (B.8 dahil) | `784e52d`, `f608cbb` |
>
> ### Planda olmayan üç bulgu (hepsi ölçümle çıktı)
> 1. **`r = 0,997` korelasyon değil ÖZDEŞLİK** (EK J) — iddia zayıflamadı,
>    her çalışmaya uygulanabilir hale geldi.
> 2. **Protokol yayılımının İKİ sürücüsü var** (EK C) — başarılı-kaynak
>    protokolü ayrı bir sürücü ve tek başına işareti çeviriyor.
> 3. **SVHN'de asimetrinin İŞARETİ protokole bağlı** — makalenin "yön veri
>    kümeleri boyunca kararlıdır" iddiası düzeltildi.
>
> ### Deney kanıtları (K6)
> E1 6/6 · E7 8/8 eğitim + 4/4 değerlendirme · E3 116 nokta ·
> E6 3/3 AutoAttack çifti · B.8 6/6 test eğrisi
>
> ### Dört kapı (hepsi kendi sınamasına sahip)
> | kapı | durum |
> |---|---|
> | `verify_manuscript_numbers.py` | **137/137**, iki dil, çıkış kodu üretir |
> | `check_manuscript_claims.py` | **31/31**; `test_claim_guards.sh` 4/4 yakalıyor |
> | `check_abstract_body.py` | geçiyor; `test_abstract_body_check.sh` ile sınandı |
> | `q1_tr_decimal_check.py` | temiz (aralık istisnalı) |
>
> Derleme: EN 20 s. · TR 18 s. · 0 undefined · 0 overfull.
> Takipsiz ham artefakt: **0** (K7).
>
> ### GERİYE KALAN: yalnızca geri dönüşsüz adımlar (KULLANICI KARARI)
> | adım | durum |
> |---|---|
> | arXiv ön-baskısı | teknik engel YOK; içerik hazır |
> | dergi gönderimi | teknik engel YOK; üç veri kümesi tamam |
> | repo public | artefakt paylaşım politikası kararı bekliyor (`models/` 36 GB) |
>
> Ayrıca hâlâ açık olan iki kalem: **iThenticate intihal kontrolü** ve
> **E5** (kapasite çifti, K-01'de ERTELENDİ — düşürülmediyse yeniden
> değerlendirilmeli).
---

## 0. Otuz saniyede durum

Bu proje CNN (ResNet-18) ile ViT (ViT-Tiny) modellerinin *çekişmeli
saldırılara* dayanıklılığını karşılaştırıyor. Ama makalenin asıl tezi
"hangisi daha dayanıklı" değil: **"ölçüm yöntemi sonucu belirliyor."**

Bitenler: C1 (CIFAR-10 ana ölçümler), E2 (seçim protokolü ablasyonu),
E1 (CIFAR-100 genelleme), **makaleye yazım** (E1+E2 iki dilde içeride).
Bitmeyenler: E7 (SVHN — **koşuyor**), E3 (kod hazır, koşum bekliyor),
E6 (kod + ön-kayıt hazır, koşum bekliyor).

**Bu oturumda tezin en kırılgan iddiası düzeltildi.** `r = 0,997` ampirik bir
korelasyon değil, cebirsel bir özdeşlikmiş: temiz-yanlış örnekler saldırı
altında yanlış kaldığı için (36 yönde ölçüm 0,989-1,000) `ham = hata +
koşullu·(1−hata)` zorunlu olarak çıkar; artık en fazla 0,41 puan. Bu iddiayı
**güçlendirdi** — artık üç hedefe dayanmıyor ve her çalışmaya uygulanabilir.
Ayrıntı: `E1_PILOT_KAPISI.md` EK J.

---

## 1. BOZULMAZ KURALLAR

Bu kurallar tekrar tekrar ihlal edildiği için buraya yazılmıştır.

### K1 — Hiçbir sayı düzyazıda yalnız yaşayamaz
Makaleye veya belgeye giren her sayının, onu üreten bir **artefakt dosyası**
(JSON/npz) ve o dosyayı üreten bir **betik** olmalı. "Hesapladım, şu çıktı"
kabul edilmez. Bu depoda daha önce, üretici kodu olmayan sayılar metne girdi
ve yanlış çıktı.

### K2a — Bire çok yakın bir korelasyon ÖNCE özdeşlik mi diye sınanır
Bir niceliğin **kendi baskın bileşeniyle** korelasyonu bir bulgu değildir.
`r = 0,997` tam bu yüzden yanlış çerçevelenmişti: bağımlı değişken bağımsız
değişkeni tanım gereği içeriyordu. Yüksek bir korelasyon raporlanmadan önce
cebirsel olarak türetilip türetilemeyeceği sorulacaktır. Bu oturumun
denetimleri ölçünün *kesinliğini* sorguladı, *kendisini* sorgulamadı.

### K2 — "X kat" biçimindeki hiçbir iddia üç sınavı geçmeden manşete konmaz
1. Pay ve payda **aynı nicelik** ve aynı cetvelde mi?
2. İkisi de **aynı yayılım ölçüsü** mü? (aralık/aralık veya sd/sd —
   **aralık ÷ sd YASAK**)
3. Payda n=3'ten geliyorsa **χ² %95 güven aralığı 1'i içeriyor mu?**
   İçeriyorsa oran gövdede *duyarlılık* olarak kalır, manşete çıkmaz.

Şüphede **mutlak birimlerle** yaz ("10 puana karşı 1,5 puan"), kat değeriyle
değil. Bu hata bu projede **dört kez** yapıldı.

### K3 — Az sayıda bağımsız birimden hesaplanan istatistik nitelenmeden yazılmaz
Örnek: `r = 0,997` altı noktadan hesaplanıyor ama o altı nokta **üç hedeften**
geliyor. "Üç hedef üzerinde" nitelemesi zorunludur.

### K4 — Ön-kayıt belgeleri SALT-EKLEMEDİR
`results/q1_research/E1_PILOT_KAPISI.md` gibi ön-kayıt belgelerinde eski
satırlar **düzeltilmez**. Hata varsa yeni bir EK yazılır ve eskisine açıkça
atıf yapılır. Sebep: belgenin salt-ekleme geçmişi, sonuçlara göre kural
değiştirmediğimizin (kapı alışverişi yapmadığımızın) kanıtıdır.

### K5 — Veri görüldükten sonra yeni durdurma eşiği kurulmaz
Buna "kapı alışverişi" denir ve ön-kaydı anlamsızlaştırır. Veri görüldükten
sonra yalnız **analiz-uygunluk kuralları** yazılabilir (henüz ölçülmemiş uç
noktalar hakkında).

### K6 — Bitmemiş koşumdan analiz üretilmez
`best.pth` dosyasının **varlığı bitmişlik kanıtı DEĞİLDİR** — eğitim sürerken
de vardır (ilk epoktan itibaren yazılır). Bitmişlik kanıtı:
`TRAINING_COMPLETE` dosyası veya `pgd_summary_*.json`. Bu hata iki kez yapıldı
(bir kez yakalandı, bir kez bayat artefakt üretti).

### K7 — Ham artefaktlar git'e eklenir
`results/` altındaki `*.npz` ve `*.json` sonuç dosyaları `git add -f` ile
eklenmelidir. Kabul ölçütü:
`git status --porcelain -uall | grep '^??' | grep results/` → **boş**.

### K8 — Sonuç beğenilmese de raporlanır
Dosya-çekmecesi taahhüdü. Tezi zayıflatan bulgular da yazılır (örnek:
EK E.3 ve EK I.4).

---

## 2. ORTAM TUZAKLARI

**Depo:** WSL içinde `/home/firat/projects/adeb_sci_1`
**Konteyner:** `adeb_eval` (repoyu `/workspace` olarak görür)

### T1 — Bash aracı Windows Git Bash'tir, WSL değil
WSL komutları şöyle koşulur:
```
wsl.exe -d Ubuntu-22.04 bash -c "cd /home/firat/projects/adeb_sci_1 && ..."
```
Komut **çift tırnak içinde** olmalı; yoksa Git Bash `/home/...` yolunu
`C:/Program Files/Git/home/...` yapar.

### T2 — İç içe tırnak sürekli bozuluyor
`$degisken`, `$(...)`, `awk '{...}'`, heredoc gibi şeyler wsl.exe üzerinden
geçerken bozulur. **Çözüm:** kodu bir dosyaya yaz (`Write` aracıyla), sonra
`bash /home/firat/dosya.sh` diye koştur.

### T3 — Çıkış kodları kayboluyor
Git Bash → wsl.exe yolunda `exit 1` yapan betik bile **0** döndürüyor.
Doğrulamayı çıkış koduna değil **çıktıya** dayandır.

### T4 — Windows satır sonu (CRLF)
`Write` aracıyla yazılan dosyalar CRLF olabilir ve bash bunu kabul etmez.
Her yazımdan sonra: `sed -i 's/\r$//' dosya`

### T5 — Koşan bash betiği düzenlenmez
Bash betiği artımlı okur; koşarken düzenlemek yürütmeyi bozar.
`scripts/q1_pipeline.sh` koşuyorsa **bekle**.

### T6 — Konteyner root olarak yazıyor
Yeni dizinlerde "Permission denied" alırsan:
`docker exec adeb_eval chown -R 1000:1000 /workspace/<dizin>`

### T7 — Makine uykuya girerse eğitim ölür (ve BOZUK DOSYA bırakır)
**Kesinti yalnız zaman kaybettirmez, 0 baytlık checkpoint bırakabilir.**
Ölçülen örnek: `models/q1/cifar100/vit_tiny_s2002/.../epoch_009.pth` **0 bayt**.
Zaman çizelgesi kesintiyi doğruluyor: epoch_008 22:06:23, epoch_009 22:08:43
(0 bayt), epoch_010 **22:37:40** — normal ritim 2 dk 20 sn iken araya **29
dakikalık** boşluk girmiş. `metrics.jsonl`'de epok 9 kaydı VAR, yani metrik
yazılmış ama checkpoint tamamlanamamış; koşum sonra `--resume` ile bitmiş.
Tarama sonucu: E1/E2/E7'nin **tüm** checkpointleri arasında bozuk olan
YALNIZ BU. Yayımlanmış hiçbir sayı etkilenmemiştir (E3 A kolu stride 10 ile
o epoğu kullanmadı; `e3_coverage` ve `q1_e1_summary` `.pth` değil
`metrics.jsonl` okuyor). `q1_e2_test_curve.py` artık okunamayan checkpoint'i
ATLAYIP uyarı basıyor ve atlanan epokları çıktı npz'sine yazıyor.

Uzun koşumlarda Windows uyku/hibernate kapatılmalı. Bir kez ~3,5 saat
GPU zamanı bu yüzden boşa gitti. Bekçi de çare değil (o da uyur).

---

## 3. YAPILACAK İŞLER — öncelik sırasıyla

### İŞ-1 · ~~`r = 0,997` iddiasını 14 konumda nitele~~ — **BİTTİ** (`fe86f48`)

> Sonradan ortaya çıktı ki bu korelasyon bir **özdeşlik**; §4.2.1 yeniden
> yazıldı (`68b6a74`). Niteleme, korelasyonun hâlâ anıldığı tek yerde duruyor.

**Sorun nedir:** Makale, ham transfer oranı ile koşullu oran arasındaki
sapmanın hedefin temiz hatasıyla açıklandığını `r = 0,997` diye söylüyor. Bu
korelasyon altı noktadan hesaplanıyor **ama o altı nokta üç hedeften geliyor**
(her hedef iki kez, farklı kaynakla). Yani gerçek bağımsız birim sayısı 3.
Nokta kestirimi sağlam (hedef düzeyinde r = 0,9985), **abartılan yalnız
kesinlik**.

**Kanıt dosyası:** `results/q1/c3_precision.json` — kendi HÜKÜM alanında
"bu değer 3 hedefe dayandığı için kesinliği abartılmış olabilir ve böyle
nitelenmelidir" yazıyor. `E1_PILOT_KAPISI.md` §G.5 bunu **makale için
zorunlu** ilan etmiş.

**Neden acil:** Aynı alt bölüm iki paragraf sonra *zayıf* bir korelasyonu
("With only three targets this correlation is suggestive rather than
conclusive") nitelendiriyor ama manşet korelasyonu nitelendirmiyor. Bu iç
tutarsızlığı hakem hemen görür.

**Konumlar:**
```
EN: main.tex:49 (öz) · 01_introduction.tex:28 · 02_related_work.tex:74
    04_experiments.tex:132 · 05_discussion.tex:17 · 05_discussion.tex:49
    06_conclusion.tex:9
TR: main.tex:53 · 01_giris.tex:28 · 02_ilgili_calismalar.tex:74
    04_deneyler.tex:132 · 05_tartisma.tex:17 · 05_tartisma.tex:49
    06_sonuc.tex:9
```

**Nasıl:** her konuma "üç hedef üzerinde" (EN: "across three targets")
nitelemesi ekle. Öz (`main.tex`) için kısa biçim yeterli.

**Kabul ölçütü:** 14 konumun tamamı nitelenmiş; iki dil de temiz derleniyor
(0 undefined); `scripts/verify_manuscript_numbers.py` hâlâ 29/29 geçiyor.

---

### İŞ-2 · ~~E1 ve E2'yi makaleye yaz~~ — **BİTTİ** (`9707337`)

**Sorun nedir:** `paper/` ağacında "CIFAR-100" kelimesi **hiç geçmiyor**.
E1 ve E2 bitti ama makaleye tek satır girmedi. Dahası iki cümle artık
**olgusal olarak yanlış**:

- `05_discussion.tex:66` (+TR `05_tartisma.tex:66`): "…we have not measured
  that dependence" → **ölçtük** (E1).
- `05_discussion.tex:80` (+TR): sızıntı ablasyonunu ve ikinci veri kümesini
  *gelecek çalışma* diye vaat ediyor → **ikisi de bitti**.
- `03_methodology.tex:142` ve `04_experiments.tex:369`: "**three** sources of
  variance" → E2 **dördüncüsünü** ölçtü (checkpoint seçimi).

**Yazılacak sayılar (hepsi artefaktta):**

*E1 — CIFAR-100, n=3* (`results/q1/e1_cifar100_summary.json`):
| | ResNet-18 | ViT-Tiny |
|---|---|---|
| Temiz | 63,86 ± 1,05 | 43,17 ± 1,10 |
| PGD-10 | 19,30 ± 0,32 | 11,15 ± 0,60 |
| AutoAttack | 15,04 ± 0,54 | 8,87 ± 0,83 |

*E1 — protokol yayılımı* (`results/q1/cifar100/transfer/e1_transfer_summary.json`):
ham +18,53 · hedef-doğru +4,96 · her-ikisi-doğru +10,92 · başarılı-kaynak
+11,44 → **yayılım 13,58 ± 1,71 puan** (CIFAR-10'da 10,45).

*E2 — seçim protokolü yayılımı* (`results/q1/e2/E2_SONUC_VE_DENETIM.md`):
ResNet 2,62-2,85 · ViT 1,58-2,09 puan (mutlak yayılım; **oran manşeti YASAK**,
bkz. K2).

**ZORUNLU NİTELEMELER** (yoksa hakem bulur):
1. **E1 marj sınırlaması** (EK I.4): ön-kayıtlı bantlar 0,22-0,48 puan marjla
   tuttu, oysa E2 seçim genliğini 1,58-2,85 puan ölçtü. "Tuttu" hükmü bu
   genlikle birlikte okunmalı.
2. **E2 karşı-ağırlığı** (EK E.3): CIFAR-100'de seçilen checkpoint tohumlar
   arasında 25 epok kayıyor ama test PGD sd'si 0,32 puan. Seçim yolu oynak,
   sonuç değil.
3. **B.4 madde 3** (EK I.3): "üçü de doğrulandı" **YAZMA**. Doğrusu: iki
   ön-kestirim doğrulandı, üçüncüsü bu tasarımda **test edilemedi**
   (CIFAR-100'de iki hedefin temiz hatası çakışık → etkin ayrık x = 2).
4. **E2 taahhüdü kısmen karşılandı** (E2 belgesi §3): E2, discussion'daki
   taahhüdün *daha zayıf* bir sürümünü cevaplıyor.

**Kabul ölçütü:** E1 alt-bölümü + E2 alt-bölümü yazıldı; yukarıdaki üç yanlış
cümle düzeltildi; dört niteleme metinde; iki dil temiz derleniyor; yeni
sayılar `verify_manuscript_numbers.py`'ye kontrol olarak eklendi.

---

### İŞ-3 · E7-kısa'yı başlat — **KOŞUYOR** (hazırlık `c24bb22`, başlangıç 13:41)

**Ne bu:** SVHN veri kümesinde küçük bir koşum. **Neden gerekli:** E3'ün
kurduğu regresyonun x ekseni "modelin temiz hatası". Elimizdeki bütün noktalar
%12'nin **üstünde**; %5-12 bandı tamamen boş. SVHN o boşluğu dolduran **tek**
çapa (bkz. `E3_YENIDEN_TASARIM.md` §2).

**Karar kaydı:** `KAMPANYA_KARARLARI.md` K-01 — kullanıcı onayladı.

**Başlatmadan ÖNCE kapatılacak üç kusur** (`E7_KOSUM_ONCESI_KONTROL.md`):
1. `scripts/q1_e1_analysis.sh:21` `DS=cifar100` **sabit** → `--dataset`
   parametresi gerekiyor.
2. `c1_c3_transfer_matrix.py` SVHN'de WRN referansını **otomatik eklemez**
   (`has_rb` yalnız cifar10/cifar100 için doğru) → referans model
   `--model` listesine **elle** verilmeli, yoksa matris 3×3 değil 2×2 çıkar
   ve karıştırıcı analizi kurulamaz.
3. `q1_pipeline.sh` `TRAINING_COMPLETE` muhafızı **epok bütçesini okumuyor**
   → önce kısa koşulup sonra `E7_FULL=1` verilirse karışık kohort oluşur.

**Koşum:**
```
docker exec -d -e STAGE=e7 -w /workspace adeb_eval bash scripts/q1_pipeline.sh
```
`E7_FULL` **VERME** (varsayılan kısa sürüm = K-01 kararı).
`--stratified` **EKLEME** (SVHN dengesizdir; eşit-sınıf bölmesi doğrulama
kümesini dengeli yapar, test dengesiz kalır → seçim ile raporlama uyuşmaz.
Ayrıntı: `E7_KOSUM_ONCESI_KONTROL.md` §3).

**Not:** "~11 GPU-saat" tahmini temiz ön-eğitimi **dışarıda bırakıyor**
(iki modda da 200 epok, SVHN 73k görüntü). Gerçek maliyet daha yüksek.

**Kabul ölçütü:** `logs/q1_e7.log` içinde `Q1-E7 TAMAM`; 4 eğitim +
4 `pgd_summary`; analiz zinciri SVHN'de koşmuş; sınıf-bileşimi kontrolü
raporlanmış (SVHN dengesiz olduğu için bileşim payının CIFAR'daki
%1-19'dan büyük çıkması beklenir — büyürse **raporla**).

---

### İŞ-4 · E3 — **B KOLU KOŞULDU** (`35d41fd`); A kolu GPU bekliyor

> B kolunun (gözlemsel) GPU gerektirmediği fark edildi: final modellerden
> gelir ve gereken örnek-bazlı maskeler zaten diskte.
> **Sonuç:** 24 nokta / 5 küme, temiz hata %13,95-58,06; protokol
> yayılımının eğimi **0,608**, küme bootstrap GA'sı **[0,364; 1,275]** —
> sıfırı içermiyor. Özdeşlik artığı 0,129 / 0,41 puan (bağımsız ölçümle
> tutarlı). Doğrusal-olmama işareti var (mse 9,61 → 5,82 karesel terimle);
> hüküm A kolu gelmeden verilmiyor.
> **Manşet (iki kolun eğimlerinin uyuşması) HENÜZ KURULAMAZ** ve kod da
> kurmuyor. A kolu için: `bash scripts/q1_e3_run.sh` (GPU boşken).

**Ne bu:** Tezin omurgası. "Ham transfer oranı ile koşullu oran arasındaki
fark, hedefin temiz hatasıyla ne kadar açıklanıyor?" sorusunun kalibrasyon
eğrisi.

**Durum:** Tasarım yazıldı (`E3_YENIDEN_TASARIM.md`) ama **kod yok**:
`scripts/q1_e3_calibration.py` 13 Ağustos'tan kalma; tasarımın istediği
`--all-checkpoints`, `--stride`, `--quantile-mode`, kol etiketi (A/B)
bayraklarının **hiçbiri** yok. Üretilmiş tek nokta yok.

**Tasarımın özeti:**
- Kantil seçimi **terk edildi** (72 hedef yalnız 38 ayrı checkpoint üretiyordu)
  → yörüngenin **tüm** checkpointleri kullanılacak (863 nokta).
- Çıkarım **yörünge düzeyi küme bootstrap** ile (B=10.000). Nokta sayısı
  863 olsa da **serbestlik derecesini yörünge sayısı belirler** — metinde
  açıkça yazılacak, yoksa "n=863" sahte kesinlik izlenimi verir.
- **İki kol ayrı raporlanacak, havuzlama YASAK:** A = yörünge-içi (kontrollü,
  nedensel yorum), B = gözlemsel (zoo + WRN + veri kümeleri). Manşet iki kolun
  **eğimlerinin uyuşması**.
- Sapma beyanı `E3_YENIDEN_TASARIM.md` §4'te hazır, makaleye girecek.

**Kabul ölçütü:** `results/q1/e3_points/` dolu; `e3_fit.json` iki kol için
ayrı eğim + küme bootstrap GA'sı içeriyor; havuzlanmış fit **üretilmiyor**
(kodda o çıktı yolu bulunmayacak).

---

### İŞ-5 · ~~E6 hakkında karar ver~~ — **BİTTİ** (`b2f38c0`, K-02)

**Ne bu:** L2 tehdit modeli — saldırıyı farklı bir "mesafe ölçüsüyle"
sınırlamak. Şu ana kadar her şey L∞ ile yapıldı.

**Sorun:** K-01'de "TUT" dendi ama `q1_pipeline.sh`'ta **`e6` aşaması yok**,
ön-kayıt belgesi yok, hiçbir çıktı yok. Yani karar kâğıt üstünde.

**İki meşru seçenek:**
- Yaz ve koş (~5 GPU-saat; `PGDL2Attack` kodda hazır: `src/attacks/pgd.py:135`)
- **Açıkça düşür** ve `KAMPANYA_KARARLARI.md`'ye **K-02** olarak yaz.

Sessiz bırakmak **kabul edilmez**.

---

### İŞ-6 · ~~Küçük kalemler~~ — **TAMAMI BİTTİ**: a,d,e,f,g,h (`784e52d`) + b,c (`db03fdb`)

| # | İş | Süre |
|---|---|---|
| a | `q1_e2_test_curve.py:73` `dataset="cifar10"` sabit → `--dataset` bayrağı. Bu, **B.8 borcu**: CIFAR-100'de seçim bandını gerçek test üzerinde ölçmeyi sağlar ve İŞ-2'nin 1. nitelemesini sayıya çevirir | 1-2 sa + 1 GPU-sa |
| b | `q1_pipeline.sh` `e5pilot` dalında **ölü kapı** duruyor ("ViT-S ilk-5-epok adv<%15 ise LR düşür") — E1'de tam bu tür kapının işe yaramadığı görüldü, E7'de ders uygulandı, E5'te uygulanmadı | 10 dk |
| c | `q1_pipeline.sh:137,144` yorumlarında terk edilmiş "%5 kapısı" anılıyor (EK B.1 onu ÖLÜ ilan etti) | 10 dk |
| d | `verify_manuscript_numbers.py` kapsama dar (~%9) ve **eksik bulsa bile 0 ile çıkıyor** → kapı olarak kullanılamıyor. Çıkış kodu ekle + Tablo I, ham transfer, 3×3 matris sayılarını kapsa | 2-3 sa |
| e | `results/q1/cifar100/transfer/C1_TRANSFER_RAPORU.md` — CIFAR-100 raporu **"C1"** başlığıyla üretiliyor (`c1_transfer_aggregate.py` sabit başlık); karantina kuralı açısından karışıklık riski | 20 dk |
| f | `q1_tr_decimal_check.py` desenine **aralık istisnası** ekle (`$[0,1]$` yanlış pozitif veriyor) | 15 dk |
| g | `E3_YENIDEN_TASARIM.md` §2'nin vaat ettiği ek yazılmadı: E1 noktaları %19,4-23,5 boşluğunu kapattı mı? | 1 sa |
| h | E1 baş artefaktlarında **köken bilgisi yok** (git SHA, tarih, tohum listesi, torch sürümü). Kıyas: `e2_report.json`'da `generated_utc` var | 1 sa |

---

## 4. GERİ DÖNÜŞSÜZ ADIMLAR — hiçbiri bugün atılamaz

| Adım | Engel |
|---|---|
| **arXiv ön-baskısı** | İŞ-1 (r=0,997) + İŞ-4 (E3). Araştırma raporu ön-baskının içeriğini "protokol denetimi + **kalibrasyon çekirdeği**" diye tanımlamış; kalibrasyon çekirdeği = E3. |
| **Dergi gönderimi** | İŞ-2 (makale) + İŞ-3 (üçüncü veri kümesi). Q1 eşiği "2-3 veri kümesi"; elde 2 var. |
| **Repo public** | Artefakt paylaşım politikası kararı (`models/` 36 GB izlenmiyor; LFS mi, yalnız `best.pth` mi, hiç mi?). |

---

## 5. DOĞRULAMA KOMUTLARI

```bash
# Depo temiz mi (ham artefakt takipsiz kalmamış mı)?
wsl.exe -d Ubuntu-22.04 bash -c "cd /home/firat/projects/adeb_sci_1 && git status --porcelain -uall | grep '^??' | grep results/ | wc -l"
# -> 0 olmalı

# Makale sayıları artefaktla tutuyor mu (iki dil)?
wsl.exe -d Ubuntu-22.04 bash -c "cd /home/firat/projects/adeb_sci_1 && docker exec -w /workspace adeb_eval python scripts/verify_manuscript_numbers.py | tail -3"
# -> EN_EKSIK=0 TR_EKSIK=0

# Koşum var mı?
wsl.exe -d Ubuntu-22.04 bash -c "docker exec adeb_eval bash -lc 'pgrep -af \"q1_pipeline|cli.main\"'"

# Derleme (Windows PowerShell)
latexmk -pdf -interaction=nonstopmode -halt-on-error -cd "\\wsl.localhost\Ubuntu-22.04\home\firat\projects\adeb_sci_1\paper\manuscript\main.tex"
```

---

## 6. ANA BELGELER

| Dosya | Ne için |
|---|---|
| `results/q1_research/E1_PILOT_KAPISI.md` | E1'in ön-kaydı ve EK A-I kapanış kayıtları. **Salt-ekleme.** |
| `results/q1/e2/E2_SONUC_VE_DENETIM.md` | E2 hükmü, yasak cümleler listesi, kanoniklik kuralı |
| `results/q1_research/KAMPANYA_KARARLARI.md` | K-01 kararı (E7 evet / E5 ertele) ve gerekçesi |
| `results/q1_research/E3_YENIDEN_TASARIM.md` | E3 tasarımı ve ön-kayıt sapma beyanı |
| `results/q1_research/E7_KOSUM_ONCESI_KONTROL.md` | E7 kontrol listesi ve SVHN tuzağı |
| `results/C1_REFERANS_FOYU.md` | KARANTINA: dışarı çıkan sayıların tek kaynağı (**Q1'i henüz kapsamıyor — açık borç**) |
