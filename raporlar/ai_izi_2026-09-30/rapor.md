# Üslup ve yapay zekâ izi denetimi — `paper/manuscript` (EN, IEEE Access), 2026-09-30

Denetçi: uslup-denetci (sonnet, salt-okunur). Ana oturum kaydetti. Sayım
betiği: `ai_izi_tara.py` (parmak izi `oncesi.json`). Kapsam: özet +
teşekkür (`main.tex`), §1–§6. ~17,7k kelime gövde.

Şiddet: **[K]** makine izi belirgin · **[S]** düzeltilse iyi olur · **[Y]** not.
Kategori: **U** "X, not Y" tiki · **D** tekrar/kopya · **M** meta/öz-açıklama ·
**H** revizyon tarihçesi · **W** "We" dizisi · **T** üçleme · **B/4** koyu etiket ·
**P** paragraf biçimi · 1–11 yazarın listesi.

## Genel

- Temiz: uzun tire yok; `itemize/enumerate` yok; leverage/utilize/delve/
  comprehensive/crucial/robustly/novel/Moreover/Furthermore/Notably/
  Importantly/"It is worth noting" sıfır.
- Asıl iz cümle ve paragraf kalıplarında: (1) "X, not Y"; (2) yazarın
  dürüstlüğünü duyuran meta cümleler; (3) aynı sonucun 6–7 kez yinelenmesi;
  (4) paragraf sonu vecizeleri; (5) ana sayıların (15,01/9,21/5,79/3,91/
  <1,5) yedi yerde tekrarı.
- §4 `koyu_etiket` 12: yalnız 4:459 `\textbf{Computational Details:}` gövde
  etiketi; kalan 11 tablo başlığı (yanlış pozitif). §3 44/46/50 üç koyu
  model etiketi.
- "X, not Y" sayımı (rather than + instead of + and not + ", not"):
  özet 2 · §1 6 · §2 3 · §3 12 · §4 64 (~6,7/1000 kelime) · §5 19 · §6 3.
  "property of X and not of Y" biçimi 1:27, 4:242, 4:303 ×2, 4:457, 5:21,
  5:31, 6:9, 6:13; "created by adversarial training and not by architecture"
  dört yerde (1:27, 4:303, 5:31, 6:13).
- `rather than` 18 (17 kapsamda). Kalsın (gerçek karşıtlık, 8): 3:137 ×2,
  4:204, 4:269 (ilk yarı), 4:392, 5:17, 5:69, özet. Kesilmeli (9): 2:72,
  2:76, 4:145 ×2, 4:187, 4:206, 5:13, 5:41, 5:55. Gereksiz `instead of`:
  1:23, 4:135, 4:204, 5:61.
- first_second §4: 388/390 "Two results follow… Second", 392/394 "A third…
  Finally", 455 "A fourth" → yanlış numaralama.
- Noktalı virgül yığını gerçek sorun: 4:117 (5 tane), 4:127.

## main.tex (özet 249 kelime; sınır 250)

| Yer | Kat | Şid | Snippet | Öneri |
|---|---|---|---|---|
| 89 | U/9 | S | "That 15.01-point spread is not one thing:" | "The 15.01-point spread has two parts: …" |
| 89 | 9 | Y | "We show that much of it comes from" | "it" belirsiz → "much of the disagreement" |
| 89 | 8 | S | "Three further readings fail to replicate" | ikisi yayın iddiası değil → "do not hold under direct measurement" |
| 89 | U | Y | "a premise we measure rather than assume" | kalsın; kalıbı yalnız burada bırak (bkz. 4:145) |
| 126–128 | – | Y | Claude beyanı | bulgu değil; bilgilendirme, silinmez |

## §1 Introduction

| Yer | Kat | Şid | Snippet | Öneri |
|---|---|---|---|---|
| 11 | 9/P | S | "makes a different observation, which is that…" | doğrudan: "Even when the models, the data, the threat model, and the attack budget are held fixed, the conclusion still depends on a rarely reported choice: the measurement protocol." |
| 11 | D/T | S | dört ögeli liste özet/1:11/2:74/6:7'de aynı | yalnız §1'de tam; diğerlerinde "with everything else held fixed" |
| 11 | P/U | Y | "treated as reporting details. We show that they are part of the result." | "part of the result" 3:118, 4:117, 4:457'de de; bir yerde kalsın |
| 16/23/25 | W | S | üç "We then" açılışı | 23 "The spread decomposes as follows:", 25 "A confound analysis…" |
| 18 | U | S | "as measurable hypotheses, not as interpretation" | "as measurable hypotheses" |
| 23 | P/D | K | 220 kelime, ~14 sayı; özetin kopyası | 4,4–19,4, <1,5, 9,21/5,79/3,91 kalsın; CIFAR-100 ve kontrol noktası cümlelerini kaldır |
| 23 | U | S | "separate that spread instead of leaving it as one number" | "We then decompose that spread:" |
| 25 | U | K | "not an empirical correlation but an identity" | aynı hamle 2:74, 4:145, 5:41; karşıtlığı yalnız §4.2.1'de bırak |
| 25 | U | S | ardışık iki "not" | "…tracks the target's own vulnerability (r = 0.986 across three targets), which makes the asymmetry a property of the weaker target." |
| 27 | U | S | "created by adversarial training and not by architecture" | "created by adversarial training" |
| 29 | 9 | S | tek cümlelik "We close with…" paragrafı | 1:36 ile yineleniyor; sil |
| 36 | 9/P | S | beş cümle "Section~…" ile | tek cümlede birleştir |

## §2 Related Work

| Yer | Kat | Şid | Snippet | Öneri |
|---|---|---|---|---|
| 42 | 2/9 | S | "Extensive research has characterized…" | sil; "Madry et al. demonstrated…" ile başla |
| 52 | 9/10 | S | "Our work extends this line of inquiry…" | sil; konumlandırma §2.6'da |
| 54 | 2/9 | S | "Despite these advances, behavioral comparisons…" | "…under a single evaluation protocol remain scarce." |
| 64 | 2 | Y | "has received increasing attention" | sil |
| 64 | 9 | S | "These transfer patterns bear directly on ensemble design…" | sil |
| 72 | U | S | "rather than pairing the comparison…" | "…and rarely pair the comparison with behavioral analysis." |
| 74 | D/P | K | 300 kelime, sonuç sayıları (15,01±0,84; 3,91; 0,41; 36) | "What is missing is a controlled estimate…" sonrası → "We supply one by varying only the protocol, with models, data, threat model and attack budget fixed (Section~\ref{sec:experiments})." |
| 74 | U/10 | S | "not a tendency but an identity" / "engages that question directly and makes it the object of study" | ikincisi boş; sil |
| 76 | U/M | K | "test rather than assume… exactly what a protocol-sensitive comparison cannot afford" | "…that our design lets us test:"; vecize sil |
| 76 | tutarsızlık | S | "Three further claims recur in this literature" | §4:313 ve §6:13 bunları hiçbir çalışmaya atfetmiyor → "Three readings that architecture-comparison papers often suggest" |

## §3 Methodology (en temiz)

| Yer | Kat | Şid | Snippet | Öneri |
|---|---|---|---|---|
| 44/46/50 | 4 | S | `\textbf{ResNet-18}:` üç koyu etiket | düz nesir |
| 46 | 10 | Y | "representing the state-of-the-art architecture" | "commonly used as a reference architecture" |
| 72 | 2 | Y | "standardized… standardized" | ikinci cümleyi sil |
| 85 | 10 | Y | "widely adopted in practice" | atıf ya da sil |
| 102 | U | S | "as a contrast, not as results" | "We report them explicitly as a contrast because…" |
| 110–139 | 4/P | S | sekiz ardışık `\paragraph{}` | gruplama (yapısal; bu turda yapılmadı) |
| 118 | P/U | S | 330 kelime; "part of the reported result, not an implementation detail" | "…so we treat the protocol as part of the reported result." |
| 137 | M/U | Y | "bounds this adaptation and not the method" | "bounds our adaptation only" |
| 156 | 4 | S | dört italik etiket (`\emph{Training-run variance}`…) | sıradan cümle |
| 158 | tutarsızlık | S | "so every reported number is reproducible from the released pipeline" | §6/main:120 "will be released" → "will be reproducible from the pipeline we release" |

## §4 Experiments (en yoğun)

| Yer | Kat | Şid | Snippet | Öneri |
|---|---|---|---|---|
| 41 | 10 | S | "decisively" (41, 240, 439) | sil |
| 41 | 9 | Y | "confirming the value of the stronger ensemble" | sil |
| 41 | T | Y | "capacity, extra training data and a stronger recipe" | 5:45'te aynı; birini kısalt |
| 66 | U/P | K | "The defensible conclusion is narrower and more useful than a mechanism:" | 6:9'da da; "An attribution of this kind should therefore not be drawn from a single training run, and an absolute score alone hides which factor is doing the work." |
| 84 | 9 | S | "This section contains the paper's central measurement." | sil |
| 117 | P/U | K | 500 kelime, 5 noktalı virgül, 6 konu | "That spread is not a single quantity, and separating it is part of the result." sil; "The protocol, not the model, dominates…" sil (dört kez söylendi); "A reader given only one of these numbers…" sil. (Paragraf bölme yapısal; bu turda yapılmadı.) |
| 117 | olgusal | Y | "differing in the third decimal from the ±0.23" | 8,27±0,24 vs ±0,23 İKİNCİ ondalık → "differing slightly from" |
| 119 | U/P | S | "A protocol name is not by itself a specification." | "Protocol names leave a sub-choice open." |
| 123–127 | P | S | ~850 kelime kol karşılaştırması | yerleşim (yapısal; bu turda yapılmadı) |
| 125/127/212/240/457 | M | K | "belong(s) with" 7 kez | "Two limits apply: …" |
| 135/145/147 | U/D | K | bir paragrafta dört tik: "stronger than a correlation: it is an identity"; "does not merely correlate… it is that error"; "measured rather than assumed"; "measure it rather than assume it" | "rather than assume" ikisini sil; "To quantify the confound directly instead of arguing it" → "To quantify the confound, we extend…" |
| 145 | H | S | "We previously reported this as a Pearson correlation (r = 0.997), which understated it…" | ya `\cite{sahin2026behavioral}` (bildiri 0,997 veriyorsa) ya sil |
| 172/206 | U/8 | S | "suggestive rather than conclusive, and we report it as such" ×2 + 5:21 | tek "The correlation is suggestive." |
| 187 | U/M | S | "we say so rather than let ``pre-registered'' be read as preceding the run" | "The registration does not precede the start of training; it precedes the first reported number, an epoch-5 pilot gate, by sixty-six minutes." |
| 204 | U | Y | "instead of above it" | "slightly below the CIFAR-10 value" |
| 206/269 | D/P | S | "One of the three registered predictions…" / "Two of the three…" simetrik | ikincisini farklı kur |
| 206 | U | S | "We report the failure rather than the reading that would rescue it, because…" | "We report the failure: the registration named the CIFAR-10 spread, not the number." |
| 212 | 9 | Y | "a reader should weigh the pre-registration accordingly" | sil |
| 220 | 9/P | S | "…not the one a reader of the previous sections would expect." | "This is the regime in which the protocol should matter most." |
| 240 | U/10 | S | "The split is not arbitrary."; "Both would be arithmetically correct and neither would be reproducible by the other." | ikisini sil |
| 242 | U | S | üç tik bir paragrafta | ilk ikisini kes |
| 252, 5:59 | tutarsızlık | Y | "measures the measurement axis" | "probes how the protocol affects the conclusion, not L2 robustness" |
| 271 | tutarsızlık | S | "That check passes." | 4:269 "estimates 1−r_cond rather than testing anything" ile çelişir → "The measured slope agrees with the value the identity predicts." |
| 279/303 | D | S | "Holm-corrected p<10^-11 and paired Cohen's d 0.32–1.23" iki kez aynen | ilkinden sil |
| 303 | U | K | dört tik | ilk ikisi yeter |
| 313 | M/D | K | "We do not attribute that reading to a particular study; …our own earlier figures encouraged it." | aynı savunma 4:313, 4:392, 6:13; bir yerde bırak, 4:392'dekini sil |
| 313 | P | S | "The measures do not support it. We therefore measure…" | sonuç yöntemden önce; "We therefore test it directly…" |
| 333 | P/2 | S | 90 kelimelik cümle; "the disagreement is informative" | ikiye böl; "and the disagreement is informative" sil |
| 342/351 | 11/9 | K | şekil-işaretçisi kalıpları; 351 altyazıyla çelişir | 342 sil, cümleye "(Figure~\ref{fig:gradient_analysis})"; 351: "shows the corresponding magnitude maps; as its caption notes, they illustrate sparsity, not localization." |
| 359 | 9 | Y | "usually left implicit and turn out to matter" (5 yerde) | birine indir |
| 388/390/392/394 | 5/P | S | "Two results follow… Second… A third… Finally" | "Two results follow." ve "Second," sil |
| 388 | T/D | S | "late, localized, magnitude-changing event; … distributed, direction-only rotation" 5:31, 6:13'te aynen | birinde bırak |
| 390 | U | K | "this is not a nuisance but a result" | "this difference is itself a result:" |
| 392 | M/U | S | "We flag this explicitly because…"; "We raise this against our own preliminary version…" | ikincisini sil; "An earlier 8-sample figure batch suggested a visible attention effect that the larger measurement does not support." |
| 413 | P/9 | S | konu cümlesi yok | "We also measure penultimate-space geometry directly…"; "The measurable statement is therefore" → "In aggregate terms," |
| 441 | U/T/W | K | dört karşıtlık + üçleme; "narrow(ly)" 7 kez | "The claim we can support is that TGR's transfer advantage does not carry over to this regime"; "makes it weaker, not stronger" → "makes it weaker." |
| 449–453 | D | S | dört varyans kaynağı 3:156'nın yinelenmesi; "We deliberately do not headline the ratio" (M); "quantitative form of the paper's argument" vecizesi | sil |
| 453 | tutarsızlık | Y | 1:23 "4.4-fold spread" vs "do not headline the ratio" | "max/min protocol ratio" diye tanımla veya 1:23'tekini kaldır |
| 457 | U/P | Y | "path was unstable while the outcome was not" | kalabilir; "Neither observation generalizes without the other:" ve aforizmayı kes |
| 459 | 4 | K | `\textbf{Computational Details:}` | düz nesir / `\paragraph{}` |

§4 bileşik: paragraf uzunluğu + `\emph` (51) + "X, not Y" yoğunluğu → monoton ritim; "we report/state/treat" 32 kez.

## §5 Discussion

| Yer | Kat | Şid | Snippet | Öneri |
|---|---|---|---|---|
| 13 | D/U | S | "absolute units rather than as a fold-change" üçüncü kez | sil |
| 15–17 | M/U | K | olumsuzlamayla açılan ardışık paragraflar; 8 cümlede 5 olumsuzlama | "We agree that the distance between protocols is not a variance. It is a bound on what the omission costs." |
| 17 | 10 | Y | "the sharpest external test the mechanism admits" | "a direct external test" |
| 19 | 10 | Y | "hyper-vulnerable" | "highly vulnerable" |
| 21 | D/U | S | 4:240–242'nin yeniden anlatımı | yarıya indir |
| 23/43/6:11 | D | S | "mechanism-level claims need more training runs" üç kez | 5:43'te bırak |
| 25–29 | P | K | üç simetrik paragraf (negatif sonuç → sayı → rejim uyarısı) | tek paragrafa kat (yapısal; bu turda yapılmadı) |
| 29 | 9 | S | "exactly the kind of claim that a single untested assumption would otherwise import" | sil |
| 31 | D | S | davranışsal farklar dördüncü anlatım | kısalt |
| 39 | 2 | Y | "a short and concrete set of requirements" | sadeleştir |
| 41/43 | W | Y | "Studies should… Studies should also…" | çeşitle |
| 43 | 2 | S | "is the interesting part, which is not recoverable" | "…is not recoverable from the score alone." |
| 43 | olgusal | Y | "both of the null results we report would have looked positive on a small figure batch" | yalnız dikkat için belgeli (4:392); lokalite için değil |
| 45 | 2/T | S | "worth weighing before investing in architecture selection as a robustness strategy" | danışmanlık dili; sadeleştir |
| 53 | 9 | S | "deliberately narrow" tekrarı | sil |
| 55 | U/M | K | "we state the limit rather than the slogan" | "That account is incomplete: …" |
| 59/61 | D | S | tek tehdit modeli sınırlılığı iki kez | sonuncuyu sil |
| 71 | H | K | "Two extensions we previously listed as future work have since been run." | "The second dataset (Section~\ref{subsec:cifar100}) and the leakage ablation have been run." |

## §6 Conclusion

| Yer | Kat | Şid | Snippet | Öneri |
|---|---|---|---|---|
| 9 | D/P | K | 260 kelime; 10 sayı; özet/giriş/§2.6'nın dördüncü nüshası | en fazla üç sayı; CIFAR-100 ve kontrol noktası cümlelerini sil |
| 9 | 2/T | S | "narrower and more useful than a ranking" | 4:66 ile aynı; sil |
| 9 | U | S | "not with any special potency of CNN-crafted perturbations" | beşinci anlatım |
| 11 | D | S | "mechanism-level claims are more fragile…" | sil |
| 13 | D/M | K | "Only the third is a published claim; the first two are natural readings…" | §2:76 ve 1:18 ile çelişki; girişte doğru yaz |
| 15 | 9 | Y | "distilled" | kabul |

## Kategori özeti

| # | Kategori | Şiddet |
|---|---|---|
| 1 | Geçişler | LOW |
| 2 | Klişe sözlük | LOW ("decisively", "narrow", "informative" tekrarı) |
| 3 | Noktalama | LOW (4:117, 4:127 noktalı virgül) |
| 4 | Koyu etiket / sahte başlık | MED (3:44/46/50; 3:156; 4:459) |
| 5 | Liste | LOW |
| 6 | Simetrik paragraf / kopya | HIGH |
| 7 | Üçleme | LOW-MED |
| 8 | Hedging | LOW |
| 9 | Meta / öz-açıklama | HIGH |
| 10 | Öz-tanıtım | LOW |
| 11 | Uzun altyazı | MED (4:113 ~170 kelime; 4:342/351) |
| U | "X, not Y" | HIGH (~109, yarısı gereksiz) |
| W | "We" dizileri | MED |

**En yoğun üç kategori:** U · M/H · D. **En kötü üç bölüm:** §4, §5, §6 (6:9).
**Tavsiye:** hedefli yeniden yazım.

## Ana oturumun kararı (2026-09-30)

Hedefli, **cümle düzeyi** yeniden yazım (makale-yazari): paragraf ve yüzen
nesne yapısı SABİT (EN/TR ayna kapısı ve TR çevirisi bozulmasın);
sayılar/\cite/\ref/\label/denklemler değişmez; her bölümden sonra
`ai_izi_tara.py --karsilastir`. Yapısal öneriler (4:117 bölme, 5:25–29
birleştirme, 3:110–139 gruplama, 4:123–127 taşıma) ayrı karar; TR
aynalaması gerektirir.
