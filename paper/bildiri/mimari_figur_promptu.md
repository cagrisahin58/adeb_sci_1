# Mimari/Genel-Bakış Figürü — AI Çizim Prompt'u

Aşağıdaki prompt'u görsel üreten bir yapay zekaya (veya diyagram aracına) olduğu gibi verebilirsin.
Çıktıyı `paper/bildiri/figures/fig_b0_overview.pdf` (tercihen vektör PDF/SVG; olmazsa ≥300 dpi PNG)
olarak kaydedersen bildiri.tex'teki hazır bekleyen yorum bloğunu açmam yeterli.

---

## PROMPT (İngilizce etiketli teknik şema)

Draw a clean, flat, vector-style scientific pipeline diagram for an IEEE conference paper
(white background, sans-serif fonts, no 3D, no gradients, no clip-art; single-column
figure, aspect ratio about 16:10). All labels in English, exactly as written below.

Layout, left to right, four stages connected by thin arrows:

1) INPUT (leftmost, single box):
   "CIFAR-10 test image (32×32×3)" with a small stylized thumbnail grid icon.

2) TWO PARALLEL ARCHITECTURE BRANCHES (stacked vertically, visually parallel):
   - Top branch, blue (#0F62FE) rounded box chain:
     "ResNet-18 (11.2M params)" containing three inner blocks in sequence:
     "3×3 conv stem" → "8 residual blocks (4 stages)" → "GAP + FC (10 classes)".
   - Bottom branch, red (#DA1E28) rounded box chain:
     "ViT-Tiny (5.7M params)" containing four inner blocks in sequence:
     "bilinear upsample 32→224" → "16×16 patchify (196 tokens + CLS)" →
     "12 Transformer blocks (192-dim, 3 heads)" → "CLS head (10 classes)".

3) SHARED TRAINING STAGE (both branches converge into one grey rounded box):
   "Matched adversarial training" with two sub-lines:
   "inner attack: PGD-10, ε = 8/255, α = 2/255" and
   "mixed loss: (1−λ)·CE(clean) + λ·CE(adv), λ = 0.5".

4) EVALUATION BATTERY (rightmost, one tall light-grey box with five small
   stacked items, each with a tiny icon):
   "Full test set, per-sample logged (n = 10,000)" as the box title, items:
   • "AutoAttack & PGD-10 robust accuracy"
   • "Conditional decomposition (clean × survival)"
   • "Transfer under 3 conditioning protocols"
   • "Gradient structure (sparsity, alignment)"
   • "Layer-wise feature drift"

Style notes: thin dark-grey arrows; consistent corner radius; branch colors only
for the two architecture chains (blue top, red bottom), everything else neutral
grey/black on white; font sizes readable when printed 8.8 cm wide.

---

## Teknik gereksinimler (araç ne olursa olsun)
- Tercih: SVG veya PDF (vektör). PNG ise en az 300 dpi ve ~2600 px genişlik.
- Metinler İngilizce ve YUKARIDAKİ yazımla birebir (bildiri metniyle tutarlılık).
- Renkler: mavi #0F62FE (ResNet), kırmızı #DA1E28 (ViT) — bildirideki figürlerle aynı palet.
- Kenarlık/gölge/3B efekt yok; IEEE baskısında tek sütuna (8.8 cm) küçülünce okunmalı.

## Entegrasyon
Dosyayı `paper/bildiri/figures/fig_b0_overview.pdf` olarak koy (PNG geldiyse bana söyle,
ben PDF'e çevirip yerleştiririm). bildiri.tex'te yorum satırıyla hazır duran
\begin{figure}...fig_b0_overview... bloğunu açacağım.
