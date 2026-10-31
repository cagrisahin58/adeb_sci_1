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

## 31.10.2026 konsey turu eklemeleri (bağlayıcı; bütünleştirme sonrası bütün TR dosyaları bunları kullanıyor)

| İngilizce | Türkçe | Not |
|---|---|---|
| (white-box) vulnerability $w$ | (beyaz kutu) kırılganlığı $w$ | hedef terimi; "hedef kırılganlığı" da olur |
| symmetric similarity $\bar\tau$ | simetrik benzerlik $\bar\tau$ | ikili ise "simetrik ikili benzerlik" |
| directional residual $r$ | yönlü artık $r$ | |
| panel similarity $\sigma$ | panel benzerliği $\sigma$ | |
| directional term $\rho$ | yönlü terim $\rho$ | |
| $\omega = \log w$ | log kırılganlık $\omega$ | EN yalnız simge kullanır |
| weak source | zayıf kaynak | |
| (panel) source gap | (panel) kaynak açığı | "boşluk" DEĞİL |
| symmetric share $q$ | simetrik pay $q$ | |
| directionally weaker source | yönlü olarak daha zayıf kaynak | |
| panel | panel | sabit dış panel |
| split-half | bölünmüş yarı | |
| architecture-by-initialization | mimari $\times$ başlatma | metinde $\times$; başlıkta \texorpdfstring; "iki faktörlü" ve "çaprazlandığı tasarım" KULLANILMAZ |
| two-by-two design | $2\times2$ tasarım | "iki faktörlü" DEĞİL (tutarlılık) |
| initialization (random / ImageNet) | başlatma (rastgele / ImageNet başlatması) | |
| scratch-trained / from scratch | sıfırdan eğitilmiş / sıfırdan | |
| interaction | etkileşim | |
| main effect | ana etki | |
| pre-registration / registered | ön kayıt / önceden kaydedilmiş, kayıtlı | |
| addendum (pre-registration) | ön kayıt eki | "ek ön kayıt" DEĞİL |
| out of sample | örneklem dışı | |
| Holm correction | Holm düzeltmesi | |
| equivalence (bound) | eşdeğerlik (sınırı) | TOST satırıyla tutarlı |
| refuted | çürütüldü / çürütülmüştür | ön kayıt karar statüsü; yalnız bu anlamda |
| supported | desteklendi / desteklenmiştir | ön kayıt karar statüsü |
| descriptive | betimsel | |
| exploratory | keşifsel | |
| identifiability / identifiable | tanımlanabilirlik / tanımlanabilir | |
| accounting identity | muhasebe özdeşliği | "hesap özdeşliği" DEĞİL; "tanım gereği sağlanan" ile açılır |
| quasi-symmetry model | yarı simetri modeli | Caussinus |
| potential / circulation | potansiyel / dolaşım | Hodge ayrışımı |
| contingency table | olumsallık tablosu | |
| Mantel test | Mantel (permütasyon) testi | |
| partial correlation | kısmi korelasyon | |
| input-gradient cosine | girdi gradyanı kosinüsü | |
| input-gradient alignment | girdi gradyanı hizalanması | |
| surrogate | vekil (model) | |
| intrinsic vulnerability | içkin kırılganlık | Demontis vd. |
| momentum PGD | momentumlu PGD | |
| retained fraction $G^{\mathrm{best}}/G^{\mathrm{PGD}}$ | korunan oran | "korunan kesir", "korunma oranı" DEĞİL |
| gradient masking | gradyan maskeleme | |
| log scale / logit scale | log ölçeği / logit ölçeği | |
| net of additive model effects | toplamsal model etkileri arındırıldıktan sonra | |
| matched (pair, pipeline, recipe, budget) | eşlenmiş | "eşleşmiş" DEĞİL; "tohum eşleşmeli" ayrı terim |
| reporting requirements | raporlama gereklilikleri | |
| surrogate complexity | vekil karmaşıklığı | Demontis vd. |
| within-family similarity $\Delta_{\mathrm{seed}}$ | aile içi benzerlik | |
| best attack | en iyi saldırı | kaynağın en iyi saldırısı |
| cell / contrast | hücre / karşıtlık | interaction contrast = etkileşim karşıtlığı |
| initialization bundle | başlatma etkeni / demeti | |
| input pipeline | girdi hattı | preprocessing pipeline = ön işleme hattı |
| stem / patch stem / convolutional stem | giriş katmanı / yama girişi / evrişimli giriş | |
| frozen (script, registration) | dondurulmuş | |
| margin (equivalence) | marj | band = bant |
| undecided | kararsız | ön kayıt karar statüsü |
| masking rule / flag | maskeleme kuralı / işaret eşiği | |
| gauge (Proposition 2) | ayar dönüşümü | |
| Proposition | Önerme | `\newtheorem{proposition}{Önerme}` 03_yontem içinde korumalı |
| desk analysis | masa çözümlemesi | "masa başı analiz" DEĞİL |
| smoke matrix / mock run | duman testi matrisi / deneme koşusu | |
| binding replication | bağlayıcı yineleme | |
| pooled variance / Welch | birleştirilmiş varyans / Welch düzeltmesi | |
| root-mean-square (RMS) | karesel ortalama karekökü (RMS) | |
| cross-fitted selection | çapraz uydurmalı seçim | |
| manipulation checks / collapse rule | manipülasyon denetimleri / çöküş kuralı | |
| hierarchical bootstrap / panel jackknife | hiyerarşik bootstrap / panel jackknife | |
| outcome region O1 | sonuç bölgesi O1 | |
| seed-matched pairs | tohum eşleşmeli çiftler | |
| potential component / share | potansiyel bileşen / potansiyel payı | Hodge ayrışımı |
| premise $p$ | öncül $p$ | |
| $r_{\text{raw}}$, $r_{\text{cond}}$, $h^{\text{raw}}$, $h^{\text{tc}}$ | $r_{\text{ham}}$, $r_{\text{koş}}$, $h^{\text{ham}}$, $h^{\text{koş}}$ | eski TR uzlaşımı |
| mixed-loss PGD adversarial fine-tuning | karma kayıplı PGD çekişmeli ince ayar | Madry AT'si değil |
| transformer (generic) | dönüştürücü | tablolarda "Dön." |
| pair types CNN-CNN / transformer-transformer / mixed | CNN--CNN / Dön.--dön. / karma | |
| CI (tablo) | GA | aralık $[a;\ b]$, noktalı virgülle |

## 31.10.2026 TR düzeltme turu eklemeleri (bağlayıcı)

| İngilizce | Türkçe | Not |
|---|---|---|
| simple effect | basit etki | Ek C, tab:simple_effects; "Mimari, sıfırdan" satır biçimi |
| derived quantity ($2q-1$) | türetilmiş nicelik | "türetilmiş" tabloda da; sınama değildir |
| ResNet-18 variant | ResNet-18 türevi | "varyantı" DEĞİL |
| pooled-variance interval (tablo başlığı) | birleştirilmiş varyanslı aralık; tabloda "Birl.\ \%90 GA" | "havuzlanmış" KULLANILMAZ (metin, altyazı, tablo dipnotu) |
| confounded with X | X'ten ayrıştırılamamak / X karıştırıcı bir etken | "X ile karışmak" KULLANILMAZ (özet düzeltmesi) |
| unpaired (model, tablo rolü) | eşi yok / eşi olmadan | "eşleşmemiş" DEĞİL |
| connector (şekil) | bağlayıcı | fig:protocol_sets |
| crosses A with B (2x2 tasarım) | A ve B'yi iki etken olarak ele alan | "çaprazlayan" mimari $\times$ başlatma için KULLANILMAZ; "çift panelle çaprazlandığında" (05) ayrı kullanım, kalabilir |
| Less a weak source than a different one (başlık) | Zayıf Olmaktan Çok, Farklı Bir Kaynak | virgül "-mekten çok" karşılaştırmasını sabitler |

## Sayı biçimi
- Ondalık ayırıcı: virgül, LaTeX'te `{,}` (ör. `85{,}78`)
- Binlik ayırıcı: nokta (ör. `10.000`)
- Yüzde işareti sayının önünde: `\%37{,}93`

## Kaynaklar
- Bildirinin Türkçe arşiv sürümü: git etiketi `bildiri-tr-arsiv` (çeviri referansı)
- Figür Türkçe varyantları: `python scripts/generate_journal_figs_c1.py --lang tr`
  → `paper/figures/final_tr/`
