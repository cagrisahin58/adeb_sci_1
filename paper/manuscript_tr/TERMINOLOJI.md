# Terminoloji Sözlüğü (EN → TR)

Türkçe makale (`paper/manuscript_tr/`) boyunca tutarlı kullanılan karşılıklar.
İlk kullanımda İngilizcesi parantezle verilir; sonrası yalnız Türkçe.

| İngilizce | Türkçe | Not |
|---|---|---|
| adversarial example | çekişmeli örnek | ilk geçişte "(adversarial examples)" |
| adversarial training (AT) | çekişmeli eğitim (AT) | kısaltma AT korunur |
| robustness / robust accuracy | gürbüzlük / gürbüz doğruluk | |
| clean accuracy | temiz doğruluk | |
| perturbation | pertürbasyon | |
| threat model | tehdit modeli | |
| measurement protocol | ölçüm protokolü | makalenin merkez terimi |
| conditioning protocol | koşullama protokolü | |
| conditional fooling rate | koşullu yanıltma oranı | kısaltma KYO (denklemde) |
| conditioned survival | koşullu sağkalım | |
| unconditioned (raw) | koşulsuz (ham) | |
| target-correct | hedef doğru | |
| both-correct | her ikisi doğru | |
| successful-source | başarılı kaynak | |
| transfer attack | transfer saldırısı | |
| transferability | transfer edilebilirlik | |
| white-box / black-box | beyaz kutu / kara kutu | |
| gradient sparsity | gradyan seyrekliği | |
| (gradient) alignment | hizalanma | mutlak/işaretli kosinüs |
| spatial locality | mekânsal lokalite | "uzamsal" DEĞİL (tutarlılık) |
| feature drift | öznitelik kayması | |
| block-wise | blok bazlı | |
| attention | dikkat | öz-dikkat = self-attention |
| attention entropy | dikkat entropisi | |
| token | jeton | "belirteç" DEĞİL |
| token aggregation | jeton agregasyonu | |
| patch | yama | |
| CLS token | CLS jetonu | |
| upsampling | büyütme / yukarı örnekleme | çift doğrusal büyütme |
| validation split | doğrulama bölmesi | |
| (training) seed | tohum | |
| checkpoint | kontrol noktası | |
| selection leakage | seçim sızıntısı | |
| paired (test/statistics) | eşleştirilmiş | |
| equivalence test (TOST) | eşdeğerlik testi (TOST) | |
| sign-flip permutation test | işaret çevirme permütasyon testi | |
| bootstrap CI | bootstrap güven aralığı (GA) | |
| effect size (Cohen's d) | etki büyüklüğü (Cohen d) | |
| confound | karıştırıcı | |
| ablation | ablasyon | |
| epoch | epok | |
| batch | parti | batch norm = parti normalizasyonu |
| early stopping | erken durdurma | |
| weight decay | ağırlık sönümü | |
| cosine annealing | kosinüs tavlama | |
| residual block | artık blok | |
| Vision Transformer (ViT) | Görü Dönüştürücüsü (ViT) | |
| universal adversarial perturbation | evrensel çekişmeli pertürbasyon | |
| Token Gradient Regularization (TGR) | Jeton Gradyanı Düzenlileştirme (TGR) | |

## Sayı biçimi
- Ondalık ayırıcı: virgül, LaTeX'te `{,}` (ör. `85{,}78`)
- Binlik ayırıcı: nokta (ör. `10.000`)
- Yüzde işareti sayının önünde: `\%37{,}93`

## Kaynaklar
- Bildirinin Türkçe arşiv sürümü: git etiketi `bildiri-tr-arsiv` (çeviri referansı)
- Figür Türkçe varyantları: `python scripts/generate_journal_figs_c1.py --lang tr`
  → `paper/figures/final_tr/`
