# Mimari/Genel-Bakış Figürü — AI Çizim Prompt'u (İNGİLİZCE etiketli)

Bildiri ATEEC 2026 için İngilizce'ye çevrildi ve tüm sayılar C1 (3 tohum, sızıntı
düzeltmeli) koşusundan geliyor; figür etiketleri de bu yüzden İngilizce ve tasarım
3 tohumlu protokolü yansıtıyor. Aşağıdaki prompt'u görsel üreten bir yapay zekaya
olduğu gibi ver. Çıktıyı `paper/bildiri/figures/fig_b0_overview.pdf` (tercihen vektör
PDF/SVG; olmazsa ≥300 dpi PNG — PNG gelirse söyle, çeviririm) olarak kaydet;
bildiri.tex'te hazır bekleyen yorum bloğunu açacağım.

> Not: Bu dosyanın önceki sürümü Türkçe etiketliydi ve üç protokolden söz ediyordu.
> Türkçe sürüme geri dönersek (TR Dizin dergi versiyonu) etiketleri çeviririm.

**Figürün amacı (önemli):** Bu yalnızca "hangi modeller, nasıl eğitildi" şeması
değil. O bilgi zaten §III'te yazılı; onu tekrarlayan bir figür 6/6 dolu bir
bildiride yerini hak etmez. Figürün taşıması gereken şey, tabloda
**gösterilemeyen** yapı: dört koşullama protokolünün aynı test kümesini iç içe
geçmiş alt kümelere daraltması ve ölçülen asimetrinin bununla 3,3 kat değişmesi.
Bu yüzden 4. aşama iç içe kutulardan oluşuyor ve figürün görsel ağırlık merkezi
orası. Sayılar Tablo III ile birebir aynı (C1, 3 tohum).

---

## PROMPT

Draw a clean, flat, vector-style scientific pipeline diagram for an academic paper
(white background, sans-serif fonts, no 3D, no gradients, no clip-art; single-column
figure, aspect ratio about 16:10). All labels are in ENGLISH and must be written
EXACTLY as given below.

Layout, left to right, four stages connected by thin dark-grey arrows:

1) INPUT (leftmost, single box):
   "CIFAR-10 (32x32x3), fixed 2,000-image validation split held out before training"
   with a small stylized thumbnail grid icon.

2) TWO PARALLEL ARCHITECTURE BRANCHES (stacked vertically, visually parallel):
   - Top branch, blue (#0F62FE) rounded box chain titled "ResNet-18 (11.2M params)"
     containing three inner blocks in sequence:
     "3x3 conv stem" -> "8 residual blocks (4 stages)" -> "GAP + FC (10 classes)".
   - Bottom branch, red (#DA1E28) rounded box chain titled "ViT-Tiny (5.7M params)"
     containing four inner blocks in sequence:
     "bilinear upsample 32->224" -> "16x16 patches (196 tokens + CLS)" ->
     "12 Transformer blocks (dim 192, 3 heads)" -> "CLS head (10 classes)".

3) SHARED TRAINING STAGE (both branches converge into one grey rounded box):
   Title "Matched adversarial training, 3 seeds per architecture", three sub-lines:
   "inner attack: PGD-10, eps = 8/255, alpha = 2/255",
   "mixed loss: (1-lambda) CE(clean) + lambda CE(adversarial), lambda = 0.5",
   "selection: best PGD-10 accuracy on the held-out validation split".

4) EVALUATION AND CONDITIONING (rightmost, and the point of the figure). Draw a
   light-grey box titled "Full test set, per-sample logging (n = 10,000)". Inside it,
   draw FOUR NESTED RECTANGLES, each smaller than and contained in the previous one,
   like a set-inclusion diagram, each labelled on its own top edge and annotated on
   the right with the transfer asymmetry measured on that set:

   - Outermost, light grey fill: "All samples, N = 10,000"        -> "+13.6 pts"
   - Second, pale blue fill:     "Target correct, N = 7,353"       -> "+4.4 pts"
   - Third, medium blue fill:    "Both correct, N = 7,061"         -> "+8.3 pts"
   - Innermost, dark blue fill:  "Successful source, N = 3,122"    -> "+14.6 pts"

   Put a short vertical caption to the right of the four annotations, rotated or
   stacked: "measured CNN->ViT asymmetry". Under the nested boxes add one line in
   italics: "Same models, same data: the conditioning set changes the answer 3.3x".

   Below that box, a thin row of four small labelled chips (no nesting), to show the
   other analyses: "Conditional decomposition", "Gradient structure",
   "Block-wise feature drift", "Spatial locality".

Style notes: thin dark-grey arrows; consistent corner radius; branch colors only for
the two architecture chains (blue top, red bottom) and for the nested conditioning
sets (blue shades, getting darker inward); everything else neutral grey/black on
white; font sizes readable when printed 8.8 cm wide. The nested-set panel should be
the visually dominant element, roughly 40% of the figure area.

---

## Teknik gereksinimler
- Tercih: SVG veya PDF (vektör). PNG ise en az 300 dpi ve ~2600 px genişlik.
- Etiketler YUKARIDAKİ İngilizce yazımla birebir (bildiri metniyle tutarlılık).
- Renkler: mavi #0F62FE (ResNet), kırmızı #DA1E28 (ViT) — bildirideki figürlerle aynı.
- Kenarlık/gölge/3B efekt yok; tek sütuna (8.8 cm) küçülünce okunmalı.

## Entegrasyon
Dosya `paper/bildiri/figures/fig_b0_overview.pdf` olarak geldiğinde bildiri.tex'teki
yorumlu \begin{figure} bloğunu açacağım (Yöntem bölümünün başında hazır bekliyor).
Bildiri şu an 6/6 sayfada olduğu için figür eklenince taşma olmaması adına metinden
2-3 satır kısaltmam gerekebilir; onu ben hallederim.
