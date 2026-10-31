# Atıf ve kaynakça denetimi, 31.10.2026

Denetlenen dosya `paper/manuscript/references.bib` (91 girdi), metin `paper/manuscript/main.tex` ile `paper/manuscript/sections/*.tex` (01-07). Dergi IEEE Access, stil `IEEEtran.bst`. Düzeltmeden önceki kopya `paper/manuscript/references.bib.bak` olarak alındı. Betik çıktıları bu klasörde: `betik.json` (düzeltme öncesi koşu) ve `betik_sonra.json` (düzeltme sonrası koşu). Ön kayıt dosyalarına ve makale düzyazısına dokunulmadı.

## Özet

Kaynakçada uydurma künye bulunmadı. Yeni manşet için eklenen ve `x-atifkontrol = {TODO: dogrulanmadi}` taşıyan 12 girdinin 10'u DOI ya da arXiv kimliğiyle, iki bağımsız kaynaktan doğrulandı ve alanları kaldırıldı. Kalan iki girdi, Rade ve Moosavi-Dezfooli (ICLR 2022) ile Mantel (1967), gerçek yayınlardır ve künyeleri doğrudur, ancak ikisinin de DOI'si ya da arXiv kimliği yoktur. Kullanıcı kuralı DOI ya da arXiv istediği için bu ikisi VERIFIED sayılmadı; alanları `GERCEK_KIMLIKSIZ` değerine çevrildi ve kanıt olarak kullanılan kimlik (OpenReview Azh9QBQ4tR7, PubMed PMID 6018555) alana yazıldı. Bu alan IEEEtran tarafından basılmaz; geçici bir dizinde koşulan bibtex 0 uyarı ve 77 kaynak verdi, `main.bbl` içinde "TODO", "atifkontrol" ya da "GERCEK" dizgesi geçmiyor.

RobustBench panel üyelerinin hepsi RobustBench deposundaki `model_info/<veri>/Linf/<kimlik>.json` kayıtlarıyla birebir eşleşti (başlık, yazarlar, bağlantı). Brif §7'deki "doğrulanamazsa yalnız RobustBench kimliği ve `\cite{croce2021robustbench}`" kararının uygulanmasına gerek kalmadı. Brif §7'de verilen beklenen kimliklerin hepsi (Demontis 1809.02861, Adam 1904.07980, Caussinus 10.5802/afst.519, Jiang 0811.1067, Balduzzi 1806.02643, Shao 2103.15670, Mo 2210.07540, Awad 2512.02830, Bai 2111.05464, Zhang 2307.07873, Liu 2302.14301, PubDef 2310.17645, Smouse 10.2307/2413122, Bhojanapalli 2103.14586, Recht 1902.10811, Singh 2303.01870) doğru çıktı.

Bağlam denetiminde atıfların büyük bölümü kaynağın söylediğiyle örtüşüyor. Yazara devredilen bir orta önemde uyumsuzluk var: 02_related_work.tex satır 35'te Awad ve ark. için "36 CNNs and ViTs trained with one ImageNet protocol" ifadesi kaynağın söylediğinden fazlasıdır. Dört düşük önemde not da var (Demontis'in üçüncü etkeni, kısmi Mantel benzetmesi, Debenedetti'nin "small datasets" bağlamı, PubDef'in kaynak bazlı dökümü).

Liu ve ark. (ARES-Bench) ön baskısı IJCV'de yayımlanmış (cilt 133, sayı 2, 567-589, 2025, DOI 10.1007/s11263-024-02196-3); girdi yayımlanmış sürüme çevrildi, anahtar `liu2023comprehensive` korundu.

## Sınıf sayıları

Betik `bib_dogrula.py` SUSPECT ve NO_ID yerine kendi sınıflarını (GRI_LIT, AG_HATASI) kullanıyor. İlk koşuda arXiv API'si HTTP 429 (istek sınırı) döndürdüğü için 11 girdi ağ hatasında kaldı; bunlar Semantic Scholar toplu sorgusu ve arxiv.org/abs sayfalarıyla elle doğrulandı, ikinci koşuda betik de VERIFIED verdi.

| Class (script) | Before (betik.json) | After (betik_sonra.json) |
|---|---|---|
| VERIFIED | 71 | 82 |
| SUSPECT | 0 | 0 |
| NOT_FOUND | 6 | 5 |
| GRI_LIT (≈ NO_ID) | 3 | 4 |
| AG_HATASI (network, not a class) | 11 | 0 |
| Total | 91 | 91 |

| Final manual class | Count | Keys |
|---|---|---|
| HALLUCINATED | 0 | |
| SUSPECT | 0 | |
| VERIFIED (DOI or arXiv, two sources) | 83 | 82 from script + `rw2019timm` (Zenodo concept DOI 10.5281/zenodo.4414861 resolves via DataCite) |
| REAL_NO_ID (exists, correct metadata, no DOI/arXiv; not VERIFIED by rule) | 7 | `rade2022reducing`, `mantel1967detection`, `krizhevsky2009learning`, `netzer2011reading`, `engstrom2019robustness`, `wang2020improving` (ghost), `zhu2024enhancing` (ghost) |
| UNRESOLVED | 1 | `sahin2026behavioral` (own submission to ATEEC 2026, not externally indexable) |

## The 12 x-atifkontrol entries

| Key | Verified identifier | Sources | Result | Change |
|---|---|---|---|---|
| touvron2021training | arXiv 2012.12877; PMLR 139:10347-10357 | arxiv.org/abs, Semantic Scholar, PMLR page | VERIFIED | series/volume/pages/publisher added; flag removed |
| wightman2021resnet | arXiv 2110.00476 | arxiv.org/abs, Semantic Scholar | VERIFIED (preprint only) | flag removed |
| sehwag2022robust | arXiv 2104.09425 (ICLR 2022) | arxiv.org/abs (comment "ICLR 2022 version"), S2, RobustBench Sehwag2021Proxy_R18 and Sehwag2021Proxy | VERIFIED | flag removed |
| addepalli2022efficient | arXiv 2210.15318 (NeurIPS 2022) | arxiv.org/abs, S2, RobustBench Addepalli2022Efficient_RN18 | VERIFIED | flag removed |
| rade2022reducing | OpenReview Azh9QBQ4tR7 (ICLR 2022); no DOI, no arXiv | iclr.cc/virtual/2022/poster/5907, mlanthology.org/iclr/2022/rade2022iclr-reducing, RobustBench Rade2021Helper_R18_ddpm | REAL_NO_ID | `url` added (printed by IEEEtran); flag set to `GERCEK_KIMLIKSIZ: OpenReview Azh9QBQ4tR7; DOI/arXiv yok` |
| pang2022robustness | arXiv 2202.10103; PMLR 162:17258-17277 | arxiv.org/abs, PMLR page, RobustBench Pang2022Robustness_WRN28_10 | VERIFIED | series/volume/pages/publisher added; flag removed. Author "Zhu, Jun" confirmed (S2 wrongly lists "Junyi Zhu") |
| jia2022lasat | arXiv 2203.06616; DOI 10.1109/CVPR52688.2022.01304 | arxiv.org/abs, Crossref, RobustBench Jia2022LAS-AT_34_10 | VERIFIED | pages 13388-13398 and DOI added; flag removed |
| hendrycks2019using | arXiv 1901.09960; PMLR 97:2712-2721 | arxiv.org/abs, PMLR page, RobustBench Hendrycks2019Using | VERIFIED | series/volume/pages/publisher added; flag removed |
| salman2020adversarially | arXiv 2007.08489 (NeurIPS 2020) | arxiv.org/abs, S2, RobustBench Salman2020Do_R18/_R50/_50_2 | VERIFIED | flag removed |
| chen2024data | DOI 10.1016/j.patcog.2024.110394 | Crossref, S2, RobustBench Chen2024Data_WRN_50_2 (links the same DOI) | VERIFIED | comment updated; flag removed |
| peng2023robust | arXiv 2308.16258 (BMVC 2023) | arxiv.org/abs ("Published at BMVC'23"), S2, RobustBench Peng2023Robust | VERIFIED | flag removed |
| mantel1967detection | PubMed PMID 6018555; no DOI, no arXiv | PubMed esummary (Cancer Res 1967 Feb;27(2 Pt 1):209-220), PMC reference lists | REAL_NO_ID | `month = feb` added; flag set to `GERCEK_KIMLIKSIZ: PMID 6018555; DOI/arXiv yok` |

Rade için bir not: RobustBench kaydı aynı çalışmanın ICML 2021 AdvML çalıştay sürümüne bağlanır ("Helper-based Adversarial Training: Reducing Excessive Margin...", OpenReview BuD2LmNaU3a). Makalenin arşivsel ICLR 2022 sürümünü anması doğrudur, değişiklik gerekmez.

## Other metadata fixes applied

| Key | Issue | Fix |
|---|---|---|
| liu2023comprehensive | Cited as arXiv preprint; published in IJCV | `@article`, IJCV 133(2):567-589, 2025, DOI 10.1007/s11263-024-02196-3 (Crossref); arXiv eprint kept |
| recht2019imagenet | Pages missing | PMLR 97:5389-5400 (PMLR page) |
| (header comment) | Block comment still said all flagged entries unverified | One comment paragraph added recording this audit |

Gözden geçirilip değiştirilmeyen ama istenirse eklenebilecek sayfa bilgileri: NeurIPS girdilerinde (salman2020adversarially, addepalli2022efficient, singh2023revisiting, springer2021little, balduzzi2018reevaluating, tramer2020adaptive) sayfa yok; tek kaynaktan (Semantic Scholar) gelen bir değer (springer 9759-9773) olduğu için yazılmadı. awad2025defense için Semantic Scholar VISAPP yerini gösteriyor, ama arXiv sayfasında ve aramada doğrulanamadı; girdi ön baskı olarak bırakıldı.

## Context alignment (brif §7 citations)

| Location | Key | Claim in text | What the source says | Verdict |
|---|---|---|---|---|
| 02:35 | awad2025defense | "extend that observation to 36 CNNs and ViTs trained with one ImageNet protocol, in all four directions between the families" | Zoo of 36 CNNs and ViTs; AT surrogates transfer better; all four directions analysed. But standard models are taken pre-trained from TensorFlow's zoo, AT models trained with Free AT, CNNs and ViTs use different optimizers; the dataset is only implied (ImageNet validation images at 224 px) | MISMATCH (medium): "trained with one ImageNet protocol" overstates |
| 02:35, 03:193, 05:21, 05:68 | demontis2019adversarial | Transferability traced to target vulnerability (surrogate-independent) and gradient alignment (symmetric) | Abstract names two main factors, target's intrinsic vulnerability and surrogate complexity, and three metrics (gradient size, gradient alignment, loss-landscape variability) | Partially aligned (low): the surrogate-complexity factor is omitted; the split "vulnerability + alignment" is a selection, not the paper's own two-factor summary |
| 02:35 | adam2019reducing | Asymmetry between two same-architecture models attributed to gradient-norm difference | Abstract: "consider the asymmetry ... between two models of the same architecture and explain it in terms of differences in gradient norms" | Aligned |
| 02:35, 03:258, 04:437, 05:21 | zhang2024why | Gradient similarity defined per input; trade-off with smoothness explains little-robustness phenomenon; c_ij is its image average | Definition 2: cosine of input gradients of two losses over (x, y); S_D as expectation over D; trade-off of smoothness and gradient similarity | Aligned |
| 02:35 | springer2021little | Slightly robust surrogates transfer well | Title and abstract | Aligned |
| 02:45, 03:193, 01:28, 05:68 | caussinus1965contribution | Quasi-symmetry model π_ij = a_i b_j ψ_ij | Standard attribution in the categorical-data literature; the French original was not read in full | Aligned (metadata verified, content via secondary literature) |
| 02:45, 03:222 | jiang2011statistical | Hodge decomposition, K-1 potential and (K-1)(K-2)/2 circulation dof | HodgeRank on complete graph | Aligned |
| 02:45 | balduzzi2018reevaluating | Use the decomposition to show when Elo-type ratings are adequate | Hodge/Schur decomposition; Elo captures only the transitive part, mElo proposed | Aligned |
| 02:45, 03:260 | mantel1967detection | Mantel permutation test for correspondence of two distance matrices | Original source of the test | Aligned |
| 02:45, 03:260 | smouse1986multiple | Partial correlation extension; "a partial Mantel test covering all main effects at once" | Partial Mantel conditions on further distance matrices | Aligned for 02:45; 03:260 is a loose analogy (low): residualizing an additive row/column fit is not literally Smouse's procedure |
| 02:21 | bhojanapalli2021understanding | ViTs at least as robust as ResNets when pre-trained on enough data | Abstract, verbatim sense | Aligned |
| 01:14, 02:21, 02:37, 05:38 | shao2022adversarial | More robust in white-box and transfer; less high-frequency content; ImageNet-21k ViTs strong sources against CNNs; direction opposite to ours | Abstract; Sec. 5.2.2 and Fig. 4: ViT-source examples transfer better to CNNs; ViTs listed with ImageNet-21K pre-training | Aligned |
| 01:14, 02:21 | bai2021transformers | Matched recipes: no adversarial advantage; more robust under distribution shift | Abstract | Aligned |
| 02:23, 03:89, 03:242, 05:72 | mo2022adversarial | ViT AT depends on pre-training | "pre-training and SGD optimizer are necessary for ViTs' adversarial training" | Aligned |
| 05:60 | mo2022adversarial, debenedetti2023light | "ViT adversarial training is also recipe-sensitive on small datasets" | Mo: CIFAR-10 and Imagenette; Debenedetti: recipe developed on ImageNet | Partially aligned (low) for Debenedetti |
| 02:23, 03:242, 04:380, 05:72 | singh2023revisiting | ConvStem and training scheme matter; ViT and ConvNeXt with ConvStem, same recipe, initialized from clean models | Abstract; Sec. 4.1 "initialize adversarial training from a fully trained (on ImageNet-1k) standard model" | Aligned |
| 02:37, 03:242, 04:386, 05:72 | liu2023comprehensive | Source-by-target heat map among AT ImageNet models; ConvNeXt-B and Swin-B counted as scratch on indirect evidence | Fig. 8 "Black-box transferability across adversarially trained models"; vanilla AT baseline described as "trained from scratch", pre-training studied as separate variants | Aligned (the "indirect evidence" hedge is appropriate) |
| 02:37 | sitawarin2024pubdef | Transfer from 24 public source models, broken down by source | Abstract: 24 public models, 11 attacks, three datasets | Aligned for "24"; per-source breakdown not checked in full text (low uncertainty) |
| main:152, 01:19, 03:242, 04:377 | recht2019imagenet | ImageNetV2 MatchedFrequency | Source of ImageNetV2 | Aligned |
| main:152, 03:52 | touvron2021training | `deit_tiny_patch16_224.fb_in1k` weights | DeiT weights | Aligned |
| main:152, 03:52 | wightman2021resnet | `resnet18.a1_in1k`, A1 recipe | RSB A1 procedure in timm | Aligned |
| 03:238-242 | RobustBench panel keys | Each RobustBench ID cites its paper | RobustBench model_info records match all nine | Aligned |

## Sentences handed to the writer (prose not changed)

1. `sections/02_related_work.tex` satır 35, Awad cümlesi. Mevcut: "Awad et al.~\cite{awad2025defense} extend that observation to 36 CNNs and ViTs trained with one ImageNet protocol, in all four directions between the families." Kaynak tek bir eğitim protokolü söylemiyor (standart modeller hazır alınmış, CNN ve ViT için farklı eniyileyiciler) ve veri kümesini yalnız değerlendirme üzerinden ima ediyor. Önerilen: "Awad et al.~\cite{awad2025defense} report, for a zoo of 36 CNNs and ViTs evaluated on ImageNet, that adversarially trained surrogates transfer better than standard ones in all four directions between the families." Önem: orta.
2. `sections/02_related_work.tex` satır 35 ve `sections/03_methodology.tex` satır 193, Demontis. Kaynağın özetindeki iki ana etken hedefin içsel zafiyeti ve vekil modelin karmaşıklığıdır; gradyan hizalanması üç ölçüden biridir. Metin vekil karmaşıklığını hiç anmıyor. Önerilen ek (02:35): "... a term that is symmetric in the two models, alongside the complexity of the surrogate." 03:193'te "close to the split" ifadesi "close to two of the three factors of Demontis et al." biçiminde daraltılabilir. Önem: düşük.
3. `sections/03_methodology.tex` satır 260: "it is a partial Mantel test~\cite{smouse1986multiple} covering all main effects at once". Smouse ve ark. kısmi Mantel'i başka uzaklık matrislerine koşullayarak tanımlar; toplamsal satır ve sütun etkilerinin artığını almak bunun bir benzeridir. Önerilen: "in the spirit of the partial Mantel test~\cite{smouse1986multiple}, with all model main effects removed at once". Önem: düşük.
4. `sections/05_discussion.tex` satır 60: "ViT adversarial training is also recipe-sensitive on small datasets~\cite{mo2022adversarial, debenedetti2023light}". Mo ve ark. CIFAR-10 ve Imagenette üzerinde çalışır; Debenedetti ve ark. tarifini ImageNet üzerinde geliştirir. "small datasets" yalnız Mo'yu karşılıyor; Debenedetti ya ayrı yan cümleye alınmalı ya da "recipe-sensitive~\cite{mo2022adversarial, debenedetti2023light}, including on small datasets~\cite{mo2022adversarial}" biçimi kullanılmalı. Önem: düşük.
5. `sections/02_related_work.tex` satır 37, PubDef: "broken down by source". Sayı (24 kaynak model) özetle uyumlu; kaynak bazlı dökümün makale gövdesinde yer aldığını yazar kendi okumasıyla teyit etmelidir. Önem: düşük, belirsizlik notu.
6. `sections/01_introduction.tex` satır 48, `sahin2026behavioral`: kendi ATEEC 2026 gönderimi dışarıdan doğrulanamaz. Bildiri kabul edildiyse künye (kitap adı, sayfa, DOI) yazar tarafından güncellenmeli; değilse "submitted" notu doğrudur. Önem: bilgi.

Kapsam dışı bir gözlem: `sections/04_experiments.tex` satır 437'nin son cümlesi "The symmetric term is thus predicted by input-gradient alignment" diyor; revizyon notu özette "predicts" yerine "tracks" kullanıldığını kaydediyor ve 03:260 ile 04:445 aynı ölçünün "necessary condition ... not evidence of a mechanism" olduğunu söylüyor. Atıf hatası değil, ama aynı paragraftaki Zhang atfıyla birlikte okunduğunda nedensel okumaya kapı açıyor; makale yazarının bakması önerilir.

## Ghost and orphan scan

Ghost terimi burada metinde anılmayan .bib girdisi, orphan ise .bib'de olmayan atıf anlamında kullanıldı (görev metnindeki tanım tersine yazılmış, ama iki yön de tarandı).

Cited but missing from .bib (orphan): yok. Yinelenen anahtar: yok. Metin 77 benzersiz anahtar anıyor, bibtex 77 kaynak basıyor, 0 uyarı.

In .bib but never cited (14): `wang2020improving`, `tramer2018ensemble`, `guo2018countering`, `cohen2019certified`, `zagoruyko2016wide`, `xie2020adversarial`, `paul2022vision`, `moosavi2017universal`, `zhu2024enhancing`, `lyu2024adaptive`, `chalasani2020concise`, `tsipras2019robustness`, `fu2022patchfool`, `gu2022vision`. IEEEtran yalnız anılan girdileri bastığı için bunlar kaynakçaya girmiyor; silinmedi. `wang2020improving` (MART, ICLR 2020) ve `zhu2024enhancing` (GNS-HFA, ICLR 2024; iclr.cc poster 19597 ve mlanthology) gerçek, DOI ve arXiv kimlikleri yok.

IEEEtran sırası: stil anılma sırasına göre numaralıyor; sıra sorunu yok. Kendi atıf oranı 1/77 (yüzde 1,3).

## Remaining x-atifkontrol fields

| Key | Value now | Why it stays |
|---|---|---|
| rade2022reducing | `GERCEK_KIMLIKSIZ: OpenReview Azh9QBQ4tR7; DOI/arXiv yok` | ICLR 2022 has no DOI and the paper has no arXiv version; existence confirmed by iclr.cc and mlanthology/OpenReview, metadata correct |
| mantel1967detection | `GERCEK_KIMLIKSIZ: PMID 6018555; DOI/arXiv yok` | Cancer Research 1967 has no DOI in Crossref; PubMed record matches title, author, volume, issue, pages |

İki girdi de basılan kaynakçada sorun çıkarmaz. "DOI ya da arXiv yoksa VERIFIED değil" kuralının bu iki gerçek kaynağa nasıl uygulanacağı ana oturumun kararıdır; atıf denetimi açısından ikisi de PDF'te kalabilir. `TODO: dogrulanmadi` değerini taşıyan girdi kalmadı.

## TR aynası

`paper/manuscript_tr/main.tex` satır 91 aynı dosyayı kullanıyor (`\bibliography{../manuscript/references}`). TR metni 67 anahtar anıyor, hepsi .bib'de var. Bu turda değişen anahtarların (liu2023comprehensive, recht2019imagenet ve 12 panel/DeiT/RSB/Mantel girdisi) hiçbiri TR metninde anılmıyor; brif §7'nin yeni atıflarından TR'de yalnız `demontis2019adversarial` var. TR aynası yeni manşete göre güncellendiğinde bu düzeltmeler otomatik geçer; ayrıca bir işlem gerekmez. Derlenmiş `main.bbl` dosyaları (EN ve TR) bu turda yeniden üretilmedi; sonraki derlemede güncellenir. Bildiri kopyası `paper/bildiri/bildiri.bib` (`extract_bib.py` ile üretilen 26 girdilik alt küme) bu turda değişen anahtarların hiçbirini içermediği için yeniden üretilmesine gerek yok.

## Sources consulted

Crossref REST API (DOI kayıtları), arXiv abstract pages (arxiv.org/abs; export.arxiv.org API'si istek sınırına takıldı), Semantic Scholar Graph API (toplu sorgu), PMLR proceedings pages (v97, v119, v139, v162), PubMed E-utilities (PMID 6018555), DataCite (10.5281/zenodo.4414861), RobustBench model_info JSON kayıtları (github.com/RobustBench/robustbench), iclr.cc ve mlanthology.org (Rade 2022, Zhu 2024), arXiv PDF metinleri (Liu 2302.14301, Singh 2303.01870, Shao 2103.15670, Zhang 2307.07873, Awad 2512.02830 HTML).
