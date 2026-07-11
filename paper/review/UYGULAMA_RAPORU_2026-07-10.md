# Uygulama Raporu — 2026-07-10 Hakem Paneli Revizyonu

Kaynak: `HAKEM_RAPORU_2026-07-10.md` + `UYGULAYICI_PROMPT_2026-07-10.md`.
Kapsam: A maddeleri (1-13) + B maddeleri (14-18) uygulandı; C maddeleri (19-24)
kullanıcı onayına sunuldu (aşağıda).

## 1. Bulgu-bazlı durum (37 confirmed + 1 uncertain)

| ID | Durum | Not |
|----|-------|-----|
| KRT-1 | uygulandı | Conclusion 11+16: "convergence"→"suppression without full equalization"; "near-identical"→1.36× (0.052 vs 0.038) |
| KRT-2 | uygulandı | cover_letter.tex, highlights.txt, suggested_reviewers.md run3 anlatısıyla yeniden yazıldı; cover letter derlendi |
| KRT-3 | uygulandı | chen2023understanding (Chen/Xu/Lv/Liu/Ji, 119474, DOI); metinde "Chen et al." |
| KRT-4 | uygulandı* | Erişilebilirlik dili 3 yerde "will be made publicly available upon acceptance"; placeholder URL+footnote kaldırıldı; TEK TODO main.tex Data&Code Availability'de (*gerçek URL kullanıcıdan) |
| MAJ-1 | uygulandı | Intro katkı paragrafı: early-drop, mid-network-plateau |
| MAJ-2 | uygulandı | §3.7: "two runs (run1/run2)" → "iki ön-implementasyon koşusu + final protokolde birer koşu" (4.5 ile hizalı) |
| MAJ-3 | uygulandı | 4 konum (04:38, fig1 caption, 05:47, 06:9): capacity+extra data+recipe jointly; gowal2020uncovering atıflı |
| MAJ-4 | uygulandı | "suppresses" iddiası hipoteze çevrildi (05:23, 06:16); clean-alignment ölçümü C-21'de |
| MAJ-5 | uygulandı | 05:75: "vulnerability correlates we characterize" + "early-accumulating semantic drift" |
| MAJ-6 | uygulandı | RQ + abstract + conclusion "hybrid design principles" → "mixed-architecture ensemble evaluation/deployment guidance" |
| MAJ-7 | uygulandı | fig4 yeniden: AYNI iki görüntüde CNN|ViT, Hoyer anotasyonu (0.474/0.449), paneller "more concentrated/distributed"; görsel doğrulandı |
| MAJ-8 | uygulandı | §3.5: eğitim seed'leri (42/123) + farklı val bölmeleri açıkça beyan |
| MAJ-9 | uygulandı | gowal2020uncovering eklendi; Tablo1 dipnotu + §3.2 + Data&Code |
| MAJ-10 | uygulandı | naseer yönü düzeltildi (ViT-kaynaklı transfer); CNN↔ViT düşük transfer mahmood'a |
| MIN-1 | uygulandı | §3.7 + Tablo1 caption beyanı daraltıldı (AA seedli; FGSM/PGD ±0.1pp stokastisite); seed'li yeniden koşu → C-24 |
| MIN-2 | uygulandı | wu2020skip + xie2020intriguing eklendi; cümle kaynakların gerçek bulgularına göre yazıldı |
| MIN-3 | uygulandı | shao2022adversarial → @article TMLR 2022 |
| MIN-4 | uygulandı | zagoruyko→BMVC'16; croce→NeurIPS D&B'21; loshchilov'17→ICLR'19; sgdr→ICLR'17 + {SGDR} |
| MIN-5 | uygulandı | Abstract 246 kelime, matematiksiz; Index Terms alfabetik |
| MIN-6 | uygulandı | \IEEEauthorblock* → journal \author{...\thanks{...}}; Access şablonuna geçiş notu (Portal'da access.cls) |
| MIN-7 | uygulandı | fig:attention_layers metinde referanslı (Gu/Fu atıflarıyla) |
| MIN-8 | uygulandı | fig2/fig_adversarial_examples float'ları atıf sırasına dizildi |
| MIN-9 | uygulandı | Örnek seçimi saldırısı-başarılı olanlardan; Row2: ship→automobile; görsel doğrulandı |
| MIN-10 | uygulandı | Kod: summary'lere model_paths; JSON provenance düzeltildi (şeffaf notla); "small" → nicel ifade (0.3/2.2pp) |
| MIN-11 | uygulandı | Tablo 4'e ±std (artefakttan) |
| MIN-12 | uygulandı | AA varyasyon iddiası → PGD ~4pp (4.5'e referanslı) |
| MIN-13 | uygulandı | "magnitude" → "displaces without altering norm or direction" |
| MIN-14 | uygulandı | Diagnostic-tool cümlesi spekülasyon olarak koşullu metriğe bağlandı |
| MIN-15 | uygulandı | fig4 caption + 05:73 dereceli dile çevrildi |
| MIN-16 | uygulandı | 1.7×'e "(preliminary run2 models)" nitelemesi + güncel ≈2.4× notu |
| MIN-17 | uygulandı | §3.5: [0,1] ham piksel + eps bu uzayda cümlesi |
| MIN-18 | uygulandı | §3.5: grad clip L2=10 + non-finite batch atlama cümlesi |
| MIN-19 | uygulandı | run_complete_pipeline.sh DEPRECATED başlığı; reproduce_paper.sh kanonik zincir |
| MIN-20 | uygulandı | moosavi: kavram kaynağa, ViT hipotezi yazarlara |
| MIN-21 | uygulandı | bai2021: fair-recipe eşitlik + OOD üstünlüğü (self-attention) |
| MIN-22 | uygulandı | Diffusion cümlesi wang2023better + wu2025vision atıflı |
| MIN-23 | uygulandı | \mathcal{B} birleştirildi; ‖δ‖∞; RW'deki FGSM/PGD denklemleri kaldırıldı (sözel+§3.3 referansı) |
| bicim-11 | kısmen | fig5a satır etiketleri düzeltildi (fig.text); fig3 model adları metinle eşitlendi ('ResNet-18 AT'); t-SNE üçgen görünürlüğü ve fig4a 12-panel yoğunluğu DOKUNULMADI (öznel/tasarım — istenirse ayrıca) |

## 2. B maddeleri (14-18)

- **B14 TOST:** `experiments/run_stat_addendum.py` → `results/stat_addendum/stat_addendum.json`. Koşullu fark 0.63pp; iki-oran z=0.98 (p=0.325); **TOST ±2pp: p=0.016 → formal eşdeğerlik**. §4.2 + §5.1 + abstract'a işlendi.
- **B15:** Tablo 3'e ±std + caption'a Welch beyanı (Hoyer p=2.4e-5, Gini p=1.1e-7, rel p=6.1e-7, alignment p=4.1e-12).
- **B16:** Tablo 4'e ±std; Blok8-vs-Blok11 Welch t=-4.07, p=0.005 → metne eklendi.
- **B17:** Attention-entropi null'u nicelendi (ort |Δ|≈0.015 nat, ≤%0.8; n=8 figür-batch kaydıyla) → §4.4; artefakt: attention_entropy_fig.json. n≥100 kesin niceleme → C-benzeri koşu.
- **B18:** Bootstrap 10.000 resample (Tablo 2 + CI'lar güncellendi); native-ViT dipnotu (5.4M param, ckpt 62.4/31.8).

## 3. Doğrulama çıktıları

- `latexmk -gg`: **EXIT 0; 0 undefined reference/citation; 0 Overfull \hbox** (Tablo 1/3 overfull'ları giderildi).
- Yasak-kalıp süpürmesi (near-identical, alignment convergence, intensifies with depth, progressive semantic, fundamental vulnerability mechanism, 47.5, 33.5, 2.2x, 4.5x, 0.917, 14-percentage, 41.2, 36.1, 5.1pp, run1 and run2, to-be-released): **paper/ altında 0 eşleşme** (yorum satırları hariç).
- bib↔cite kapanışı: **57 girdi / 57 atıf — iki yönde de eksiksiz**.
- Görsel doğrulama: fig4 (aynı görüntüler + Hoyer 0.474|0.449), fig_adversarial_examples (3 satırda da sınıf değişimi: cat→dog, ship→automobile, horse→automobile).
- cover_letter.tex pdflatex: EXIT 0.

## 4. Eklenen bib girdileri (19, tümü WebSearch-teyitli)

VERIFIED: liu2017delving, dong2018boosting, wei2022towards, gowal2020uncovering,
pinto2022impartial, ali2024adversarial, wu2025vision, raghu2021vision,
benz2021adversarial, wang2023better, hurley2009comparing, tsipras2019robustness,
fu2022patchfool, gu2022vision, wu2020skip, xie2020intriguing.
CORRECTED (teyit sırasında düzeltildi): ravikumar2023trend (başlık "Transferability-Based
Robust ENsemble Design", ss. 534-548), chalasani2020concise (ss. 1383-1391),
zhao2025revisiting (TPAMI cilt 48(1) 2026, ss. 765-780).
Ayrıca düzeltilen mevcut girdiler: chen2023understanding (uydurma yazarlar→gerçek,
119474+DOI), shao2022adversarial (ECCV→TMLR), zagoruyko2016wide (BMVC),
croce2021robustbench (NeurIPS D&B), loshchilov2017decoupled (ICLR 2019),
loshchilov2016sgdr (ICLR 2017, {SGDR}).

## 5. C maddeleri — KULLANICI ONAYI bekleyen GPU koşuları

| # | Deney | Tahmini GPU | Etki |
|---|-------|-------------|------|
| C19 | Clean-model transfer matrisi (mevcut clean ckpt'lerle) | ~1.5-2 sa | Simetrinin AT'ye mi metriğe mi bağlı olduğunu ayırır (R2: "ucuz ve etkili") |
| C20 | ResNet-18 feature degradation (residual blok, aynı 3 metrik) | ~15-30 dk | Profilin ViT'e özgülüğü — Limitations'taki açık soruyu kapatır |
| C21 | Clean modellerde gradient alignment | ~15-20 dk | "AT bastırıyor" hipotezini doğrudan test eder (MAJ-4 tam kapanış) |
| C22 | MI-FGSM ile koşullu transfer tekrarı | ~2-3 sa | Simetrinin saldırı-dayanıklılığı |
| C23 | Final protokolde ≥3 eğitim seed'i | ~40-60 sa | En pahalı; yapılmazsa mevcut kapsam daraltması yeterli (metin buna göre yazıldı) |
| C24 | Tablo 1 FGSM/PGD hücreleri seed'li CLI ile | ~1.5-2 sa | "±0.1pp stokastisite" beyanını kaldırıp tam determinizme geçirir |

Önerilen öncelik: C21+C20 (ucuz, iki hipotezi kapatır) → C19 → C24 → C22; C23 opsiyonel.

## 6. Önerilen commit mesajı

```
Hakem paneli 2026-07-10 revizyonu: 37 bulgu uygulandi (A1-13 + B14-18)

- Kritik: Conclusion/Intro/Discussion eski-anlati kalintilari temizlendi;
  gonderim paketi run3 anlatisiyla yeniden yazildi; chen2023understanding
  kunyesi duzeltildi (uydurma yazar vakasi); kod erisim dili birlestirildi
- 19 web-teyitli must-cite eklendi; kosullu-metrik katkisi "established
  practice + confound nicelemesi" olarak yeniden konumlandi (TREND/Liu/Dong)
- Istatistik: TOST esdegerlik (p=0.016), Tablo 3/4 +-std + Welch testleri,
  10k bootstrap; experiments/run_stat_addendum.py + results/stat_addendum/
- Figurler: fig4 ayni-goruntu karsilastirmasi + Hoyer anotasyonu; adv-ornekler
  figuru 3 satirda da basarili saldiriyla; fig5a satir etiketleri; fig3 adlar
- Metodoloji: egitim seedleri (42/123, farkli val bolmeleri), [0,1] girdi,
  grad-clip/NaN beyanlari; reproduce_paper.sh; run_complete_pipeline DEPRECATED
- Bicim: abstract 246 kelime matematiksiz, keywords alfabetik, journal yazar
  blogu, \balance, notasyon birlestirme; 0 undefined, 0 overfull

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
```
