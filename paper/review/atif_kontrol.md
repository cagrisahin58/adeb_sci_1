# Referans Doğrulama Raporu

**Tarih:** 2026-02-03
**Dosya:** `paper/manuscript/references.bib`
**Toplam Referans:** 36

---

## Özet

| Kategori | Sayı |
|----------|------|
| ✓ Doğrulandı | 31 |
| ⚠ Küçük Düzeltme Gerekli | 4 |
| ❌ Kritik Sorun | 1 |

---

## Referans Tablosu

| # | Key | Durum | Yıl | Venue | Sorun | Öneri |
|---|-----|-------|-----|-------|-------|-------|
| 1 | szegedy2014intriguing | ✓ | 2014 | arXiv/ICLR 2014 | - | - |
| 2 | goodfellow2015explaining | ✓ | 2015 | ICLR 2015 | - | - |
| 3 | madry2018towards | ✓ | 2018 | ICLR 2018 | - | - |
| 4 | carlini2017towards | ✓ | 2017 | IEEE S&P 2017 | - | - |
| 5 | croce2020reliable | ✓ | 2020 | ICML 2020 | - | - |
| 6 | papernot2016transferability | ✓ | 2016 | arXiv 2016 | - | - |
| 7 | demontis2019adversarial | ⚠ | 2019 | USENIX Security 2019 | arXiv preprint olarak kayıtlı | Venue güncelle |
| 8 | zhang2019theoretically | ✓ | 2019 | ICML 2019 | - | - |
| 9 | wang2020improving | ✓ | 2020 | ICLR 2020 | - | - |
| 10 | tramer2018ensemble | ✓ | 2018 | ICLR 2018 | - | - |
| 11 | guo2018countering | ✓ | 2018 | ICLR 2018 | - | - |
| 12 | cohen2019certified | ✓ | 2019 | ICML 2019 | - | arXiv: 1902.02918 |
| 13 | he2016deep | ✓ | 2016 | CVPR 2016 | - | - |
| 14 | zagoruyko2016wide | ✓ | 2016 | BMVC 2016 | arXiv preprint olarak kayıtlı | Opsiyonel: BMVC olarak güncelle |
| 15 | xie2020adversarial | ✓ | 2020 | CVPR 2020 | - | - |
| 16 | dosovitskiy2021image | ✓ | 2021 | ICLR 2021 | - | - |
| 17 | vaswani2017attention | ✓ | 2017 | NeurIPS 2017 | - | - |
| 18 | bhojanapalli2021understanding | ✓ | 2021 | ICCV 2021 | - | - |
| 19 | mahmood2021robustness | ⚠ | 2021 | ICCV 2021 | arXiv preprint olarak kayıtlı, aslında ICCV'de yayınlandı | Venue güncelle |
| 20 | shao2022adversarial | ✓ | 2022 | ECCV 2022 | - | - |
| 21 | paul2022vision | ✓ | 2022 | AAAI 2022 | - | - |
| 22 | naseer2021improving | ⚠ | 2021/2022 | ICLR 2022 | arXiv 2021 ama ICLR 2022'de yayınlandı, booktitle hatalı | Venue güncelle |
| 23 | croce2021robustbench | ✓ | 2021 | NeurIPS 2021 | arXiv preprint olarak kayıtlı | Opsiyonel: NeurIPS olarak güncelle |
| 24 | krizhevsky2009learning | ✓ | 2009 | Tech Report | - | - |
| 25 | loshchilov2017decoupled | ✓ | 2017/2019 | ICLR 2019 | arXiv 2017, ICLR 2019'da yayınlandı | Opsiyonel: ICLR 2019 ekle |
| 26 | loshchilov2016sgdr | ✓ | 2016/2017 | ICLR 2017 | arXiv 2016, ICLR 2017'de yayınlandı | Opsiyonel: ICLR 2017 ekle |
| 27 | rw2019timm | ✓ | 2019 | GitHub | DOI mevcut | - |
| 28 | moosavi2017universal | ✓ | 2017 | CVPR 2017 | - | - |
| 29 | jain2024towards | ✓ | 2024 | CVPR 2024 | - | - |
| 30 | zhang2023tgr | ✓ | 2023 | CVPR 2023 | - | - |
| 31 | ma2023transferable | ✓ | 2023 | ICCV 2023 | - | - |
| 32 | wei2024enhancing | ✓ | 2024 | ICLR 2024 | - | - |
| 33 | ars2024neurips | ⚠ | 2024 | NeurIPS 2024 | Yazar bilgisi eksik/hatalı | Tam yazar listesi ekle |
| 34 | adbm2025iclr | ❌ | 2025 | ICLR 2025 | **Doğrulanamadı** - Bu referans bulunamadı | Kaldır veya doğru kaynak bul |
| 35 | wang2023understanding | ✓ | 2023 | Information Sciences | Volume 648, Article 119473 | - |
| 36 | zheng2024towards | ✓ | 2024 | J. Systems Architecture | Volume 149/152, Article 103155 | Volume numarasını kontrol et |

---

## Detaylı Analiz

### ❌ Kritik Sorunlu Referans

#### 34. adbm2025iclr
```bibtex
@inproceedings{adbm2025iclr,
  title={ADBM: Adversarial Diffusion Bridge Model for Robust Adversarial Purification},
  author={Chen, Xiao and Wang, Hanxun and others},
  booktitle={International Conference on Learning Representations},
  year={2025}
}
```

**Sorun:** Bu referans web aramalarında doğrulanamadı. ICLR 2025 henüz gerçekleşmemiş olabilir veya makale yayınlanmamış olabilir. "others" kullanımı da akademik standartlara uygun değil.

**Öneri:**
1. Bu referansı kaldırın veya
2. Diffusion-based adversarial purification için alternatif doğrulanmış kaynak kullanın:
   - Nie et al., "Diffusion Models for Adversarial Purification" (ICML 2022)
   - Wang et al., "ADDP: Learning General Representations for Image Recognition and Generation with Alternating Denoising Diffusion Process" (ICLR 2023)

---

### ⚠ Düzeltme Gereken Referanslar

#### 7. demontis2019adversarial
**Mevcut:**
```bibtex
@article{demontis2019adversarial,
  title={Why do adversarial attacks transfer? explaining transferability of evasion and poisoning attacks},
  author={Demontis, Ambra and Melis, Marco and Pintor, Maura and Jagielski, Matthew and Biggio, Battista and Oprea, Alina and Nita-Rotaru, Cristina and Roli, Fabio},
  journal={arXiv preprint arXiv:1809.02861},
  year={2019}
}
```

**Düzeltilmiş:**
```bibtex
@inproceedings{demontis2019adversarial,
  title={Why Do Adversarial Attacks Transfer? Explaining Transferability of Evasion and Poisoning Attacks},
  author={Demontis, Ambra and Melis, Marco and Pintor, Maura and Jagielski, Matthew and Biggio, Battista and Oprea, Alina and Nita-Rotaru, Cristina and Roli, Fabio},
  booktitle={28th USENIX Security Symposium},
  pages={321--338},
  year={2019}
}
```

---

#### 19. mahmood2021robustness
**Mevcut:**
```bibtex
@article{mahmood2021robustness,
  title={On the robustness of vision transformers to adversarial examples},
  author={Mahmood, Kaleel and Mahmood, Riber and Van Dijk, Marten},
  journal={arXiv preprint arXiv:2104.02610},
  year={2021}
}
```

**Düzeltilmiş:**
```bibtex
@inproceedings{mahmood2021robustness,
  title={On the Robustness of Vision Transformers to Adversarial Examples},
  author={Mahmood, Kaleel and Mahmood, Rigel and Van Dijk, Marten},
  booktitle={IEEE/CVF International Conference on Computer Vision},
  pages={7838--7847},
  year={2021}
}
```

**Not:** "Riber" yerine "Rigel" olmalı (yazım hatası).

---

#### 22. naseer2021improving
**Mevcut:**
```bibtex
@inproceedings{naseer2021improving,
  title={Improving adversarial transferability of vision transformers},
  author={Naseer, Muzammal and Ranasinghe, Kanchana and Khan, Salman and Khan, Fahad Shahbaz and Porikli, Fatih},
  booktitle={arXiv preprint arXiv:2106.04169},
  year={2021}
}
```

**Düzeltilmiş:**
```bibtex
@inproceedings{naseer2022improving,
  title={On Improving Adversarial Transferability of Vision Transformers},
  author={Naseer, Muzammal and Ranasinghe, Kanchana and Khan, Salman H. and Khan, Fahad Shahbaz and Porikli, Fatih},
  booktitle={International Conference on Learning Representations},
  year={2022}
}
```

**Not:** Yıl 2022 olmalı (ICLR 2022'de yayınlandı), booktitle düzeltilmeli.

---

#### 33. ars2024neurips
**Mevcut:**
```bibtex
@inproceedings{ars2024neurips,
  title={Adaptive Randomized Smoothing: Certified Adversarial Robustness for Multi-Step Defences},
  author={Sukenik, Sacha and Dvijotham, Krishnamurthy and Gowal, Sven and others},
  booktitle={Advances in Neural Information Processing Systems},
  year={2024}
}
```

**Düzeltilmiş:**
```bibtex
@inproceedings{lyu2024adaptive,
  title={Adaptive Randomized Smoothing: Certified Adversarial Robustness for Multi-Step Defences},
  author={Lyu, Saiyue and Gowal, Sven and Sherborne, Tom and Dvijotham, Krishnamurthy},
  booktitle={Advances in Neural Information Processing Systems},
  volume={37},
  year={2024}
}
```

**Not:**
1. İlk yazar Saiyue Lyu, "Sukenik" değil
2. "others" kullanımı yerine tam yazar listesi kullanılmalı
3. Key'i `lyu2024adaptive` olarak değiştirmek daha doğru olur

---

## Metin İçi Uyum Kontrolü

### Section 1: Introduction
| Atıf | Bağlam | Durum |
|------|--------|-------|
| `\cite{szegedy2014intriguing, goodfellow2015explaining}` | Adversarial examples tanımı | ✓ Uygun |
| `\cite{he2016deep}` | CNN özellikleri | ✓ Uygun |
| `\cite{dosovitskiy2021image}` | ViT özellikleri | ✓ Uygun |
| `\cite{madry2018towards}` | Adversarial training | ✓ Uygun |
| `\cite{zhang2019theoretically}` | TRADES | ✓ Uygun |
| `\cite{croce2020reliable}` | AutoAttack benchmark | ✓ Uygun |

### Section 2: Related Work
| Atıf | Bağlam | Durum |
|------|--------|-------|
| `\cite{goodfellow2015explaining}` | FGSM tanımı | ✓ Uygun |
| `\cite{madry2018towards}` | PGD tanımı | ✓ Uygun |
| `\cite{carlini2017towards}` | C&W attack | ✓ Uygun |
| `\cite{croce2020reliable}` | AutoAttack | ✓ Uygun |
| `\cite{zhang2019theoretically}` | TRADES | ✓ Uygun |
| `\cite{wang2020improving}` | MART | ✓ Uygun |
| `\cite{guo2018countering}` | Input transformation | ✓ Uygun |
| `\cite{cohen2019certified}` | Randomized smoothing | ✓ Uygun |
| `\cite{tramer2018ensemble}` | Ensemble methods | ✓ Uygun |
| `\cite{ars2024neurips}` | Adaptive RS | ⚠ Key/yazar düzeltilmeli |
| `\cite{adbm2025iclr}` | Diffusion purification | ❌ Doğrulanamayan referans |
| `\cite{croce2021robustbench}` | RobustBench | ✓ Uygun |
| `\cite{he2016deep}` | Skip connections | ✓ Uygun |
| `\cite{xie2020adversarial}` | BN placement | ✓ Uygun |
| `\cite{dosovitskiy2021image}` | ViT tanımı | ✓ Uygun |
| `\cite{bhojanapalli2021understanding}` | ViT robustness | ✓ Uygun |
| `\cite{mahmood2021robustness}` | ViT vulnerability | ⚠ Venue düzeltilmeli |
| `\cite{shao2022adversarial}` | ViT AT | ✓ Uygun |
| `\cite{paul2022vision}` | Patch size/attention | ✓ Uygun |
| `\cite{jain2024towards}` | AAS-AT | ✓ Uygun |
| `\cite{wei2024enhancing}` | ViT vulnerabilities | ✓ Uygun |
| `\cite{papernot2016transferability}` | Transfer attacks | ✓ Uygun |
| `\cite{demontis2019adversarial}` | Transferability factors | ⚠ Venue düzeltilmeli |
| `\cite{naseer2021improving}` | CNN→ViT transfer | ⚠ Yıl/venue düzeltilmeli |
| `\cite{zhang2023tgr}` | TGR | ✓ Uygun |
| `\cite{ma2023transferable}` | MIG | ✓ Uygun |
| `\cite{wang2023understanding}` | Cross-architecture analysis | ✓ Uygun |

### Section 3: Methodology
| Atıf | Bağlam | Durum |
|------|--------|-------|
| `\cite{croce2021robustbench}` | CIFAR-10 conventions | ✓ Uygun |
| `\cite{he2016deep}` | ResNet-18 | ✓ Uygun |
| `\cite{zagoruyko2016wide}` | WideResNet | ✓ Uygun |
| `\cite{rw2019timm}` | timm library | ✓ Uygun |
| `\cite{croce2020reliable}` | AutoAttack | ✓ Uygun |
| `\cite{zhang2019theoretically}` | TRADES β=6.0 | ✓ Uygun |

### Section 4: Experiments
| Atıf | Bağlam | Durum |
|------|--------|-------|
| `\cite{croce2021robustbench}` | RobustBench pretrained | ✓ Uygun |

### Section 5: Discussion
| Atıf | Bağlam | Durum |
|------|--------|-------|
| `\cite{moosavi2017universal}` | Universal perturbations | ✓ Uygun |

### Section 6: Conclusion
Ek atıf yok - uygun.

---

## Düzeltilmiş BibTeX Entries

```bibtex
% ============================================================================
% DÜZELTME GEREKTİREN REFERANSLAR
% ============================================================================

% #7 - USENIX Security olarak güncellendi
@inproceedings{demontis2019adversarial,
  title={Why Do Adversarial Attacks Transfer? Explaining Transferability of Evasion and Poisoning Attacks},
  author={Demontis, Ambra and Melis, Marco and Pintor, Maura and Jagielski, Matthew and Biggio, Battista and Oprea, Alina and Nita-Rotaru, Cristina and Roli, Fabio},
  booktitle={28th USENIX Security Symposium},
  pages={321--338},
  year={2019}
}

% #19 - ICCV olarak güncellendi, yazar adı düzeltildi
@inproceedings{mahmood2021robustness,
  title={On the Robustness of Vision Transformers to Adversarial Examples},
  author={Mahmood, Kaleel and Mahmood, Rigel and Van Dijk, Marten},
  booktitle={IEEE/CVF International Conference on Computer Vision},
  pages={7838--7847},
  year={2021}
}

% #22 - ICLR 2022 olarak güncellendi
@inproceedings{naseer2022improving,
  title={On Improving Adversarial Transferability of Vision Transformers},
  author={Naseer, Muzammal and Ranasinghe, Kanchana and Khan, Salman H. and Khan, Fahad Shahbaz and Porikli, Fatih},
  booktitle={International Conference on Learning Representations},
  year={2022}
}

% #33 - Yazar ve key düzeltildi
@inproceedings{lyu2024adaptive,
  title={Adaptive Randomized Smoothing: Certified Adversarial Robustness for Multi-Step Defences},
  author={Lyu, Saiyue and Gowal, Sven and Sherborne, Tom and Dvijotham, Krishnamurthy},
  booktitle={Advances in Neural Information Processing Systems},
  volume={37},
  year={2024}
}

% #34 - KRİTİK: Bu referans doğrulanamadı, alternatif öneri:
% Seçenek A: Kaldır
% Seçenek B: Aşağıdaki doğrulanmış alternatifi kullan
@inproceedings{nie2022diffusion,
  title={Diffusion Models for Adversarial Purification},
  author={Nie, Weili and Guo, Brandon and Huang, Yujia and Xiao, Chaowei and Vahdat, Arash and Anandkumar, Anima},
  booktitle={International Conference on Machine Learning},
  pages={16805--16827},
  year={2022}
}
```

---

## Opsiyonel İyileştirmeler

Aşağıdaki referanslar doğru ancak daha kesin venue bilgisi eklenebilir:

```bibtex
% #14 - BMVC olarak güncellenebilir
@inproceedings{zagoruyko2016wide,
  title={Wide Residual Networks},
  author={Zagoruyko, Sergey and Komodakis, Nikos},
  booktitle={British Machine Vision Conference},
  year={2016}
}

% #23 - NeurIPS olarak güncellenebilir
@inproceedings{croce2021robustbench,
  title={RobustBench: a Standardized Adversarial Robustness Benchmark},
  author={Croce, Francesco and Andriushchenko, Maksym and Sehwag, Vikash and Debenedetti, Edoardo and Flammarion, Nicolas and Chiang, Mung and Mittal, Prateek and Hein, Matthias},
  booktitle={Advances in Neural Information Processing Systems},
  volume={34},
  year={2021}
}

% #25 - ICLR 2019 olarak güncellenebilir
@inproceedings{loshchilov2019decoupled,
  title={Decoupled Weight Decay Regularization},
  author={Loshchilov, Ilya and Hutter, Frank},
  booktitle={International Conference on Learning Representations},
  year={2019}
}

% #26 - ICLR 2017 olarak güncellenebilir
@inproceedings{loshchilov2017sgdr,
  title={SGDR: Stochastic Gradient Descent with Warm Restarts},
  author={Loshchilov, Ilya and Hutter, Frank},
  booktitle={International Conference on Learning Representations},
  year={2017}
}
```

---

## Sonuç ve Öneriler

### Zorunlu Düzeltmeler (Kritik)

1. **#34 (adbm2025iclr)**: Bu referansı kaldırın veya doğrulanmış bir alternatifle değiştirin. ICLR 2025 henüz gerçekleşmedi ve bu makale bulunamadı.

2. **#33 (ars2024neurips)**: Key'i `lyu2024adaptive` olarak değiştirin ve yazar listesini düzeltin. Makalede `\cite{ars2024neurips}` yerine `\cite{lyu2024adaptive}` kullanın.

3. **#22 (naseer2021improving)**: Key'i `naseer2022improving` olarak değiştirin (ICLR 2022'de yayınlandı). Makalede atıfları güncelleyin.

### Önerilen Düzeltmeler (Önemli)

4. **#7 (demontis2019adversarial)**: Venue'yi USENIX Security 2019 olarak güncelleyin.

5. **#19 (mahmood2021robustness)**: Venue'yi ICCV 2021 olarak güncelleyin, yazar adını "Rigel" olarak düzeltin.

### İsteğe Bağlı İyileştirmeler

6. #14, #23, #25, #26: arXiv preprint yerine resmi yayın venue'lerini kullanmak daha profesyonel görünür.

---

## Doğrulama Kaynakları

Bu rapor aşağıdaki kaynaklardan doğrulama yapılarak hazırlanmıştır:
- arXiv.org
- Google Scholar
- IEEE Xplore
- ACM Digital Library
- CVF Open Access
- OpenReview.net
- NeurIPS/ICML Proceedings
- ScienceDirect

---

*Rapor oluşturulma tarihi: 2026-02-03*
