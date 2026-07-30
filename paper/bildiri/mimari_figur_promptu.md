# Mimari/Genel-Bakış Figürü — AI Çizim Prompt'u (TÜRKÇE etiketli)

Bildiri Türkçe olduğu için figür etiketleri de Türkçe. Aşağıdaki prompt'u görsel üreten
bir yapay zekaya olduğu gibi ver. Çıktıyı `paper/bildiri/figures/fig_b0_overview.pdf`
(tercihen vektör PDF/SVG; olmazsa ≥300 dpi PNG — PNG gelirse bana söyle, çeviririm)
olarak kaydet; bildiri.tex'te hazır bekleyen yorum bloğunu açacağım.

---

## PROMPT

Draw a clean, flat, vector-style scientific pipeline diagram for an academic paper
(white background, sans-serif fonts, no 3D, no gradients, no clip-art; single-column
figure, aspect ratio about 16:10). All labels are in TURKISH and must be written
EXACTLY as given below (including accented characters).

Layout, left to right, four stages connected by thin dark-grey arrows:

1) INPUT (leftmost, single box):
   "CIFAR-10 test görüntüsü (32×32×3)" with a small stylized thumbnail grid icon.

2) TWO PARALLEL ARCHITECTURE BRANCHES (stacked vertically, visually parallel):
   - Top branch, blue (#0F62FE) rounded box chain titled "ResNet-18 (11,2M parametre)"
     containing three inner blocks in sequence:
     "3×3 evrişim gövdesi" → "8 artık blok (4 aşama)" → "GAP + FC (10 sınıf)".
   - Bottom branch, red (#DA1E28) rounded box chain titled "ViT-Tiny (5,7M parametre)"
     containing four inner blocks in sequence:
     "çift doğrusal büyütme 32→224" → "16×16 yama bölme (196 jeton + CLS)" →
     "12 Dönüştürücü bloğu (192 boyut, 3 baş)" → "CLS başı (10 sınıf)".

3) SHARED TRAINING STAGE (both branches converge into one grey rounded box):
   Title "Eşleşmiş çekişmeli eğitim", two sub-lines:
   "iç saldırı: PGD-10, ε = 8/255, α = 2/255" and
   "karma kayıp: (1−λ)·CE(temiz) + λ·CE(çekişmeli), λ = 0,5".

4) EVALUATION BATTERY (rightmost, one tall light-grey box with five stacked items,
   each with a tiny icon). Box title:
   "Tam test kümesi, örnek bazında kayıt (n = 10.000)", items:
   • "AutoAttack ve PGD-10 gürbüz doğruluk"
   • "Koşullu ayrıştırma (temiz × sağkalım)"
   • "Üç koşullama protokolüyle transfer"
   • "Gradyan yapısı (seyreklik, hizalanma)"
   • "Katman bazlı öznitelik kayması"

Style notes: thin dark-grey arrows; consistent corner radius; branch colors only for
the two architecture chains (blue top, red bottom), everything else neutral grey/black
on white; font sizes readable when printed 8.8 cm wide; Turkish characters
(ç, ğ, ı, ö, ş, ü, ε, λ) must render correctly.

---

## Teknik gereksinimler
- Tercih: SVG veya PDF (vektör). PNG ise en az 300 dpi ve ~2600 px genişlik.
- Etiketler YUKARIDAKİ Türkçe yazımla birebir (bildiri metniyle tutarlılık).
- Renkler: mavi #0F62FE (ResNet), kırmızı #DA1E28 (ViT) — bildirideki figürlerle aynı.
- Kenarlık/gölge/3B efekt yok; tek sütuna (8.8 cm) küçülünce okunmalı.

## Entegrasyon
Dosya `paper/bildiri/figures/fig_b0_overview.pdf` olarak geldiğinde bildiri.tex'teki
yorumlu \begin{figure} bloğunu açacağım (Yöntem bölümünün başında hazır bekliyor).
