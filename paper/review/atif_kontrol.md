# Referans Dogrulama Raporu (Guncellenmis)

**Tarih:** 2026-02-16
**Onceki Rapor:** 2026-02-03
**Dosya:** `paper/manuscript/references.bib`
**Toplam Referans:** 34 (bib dosyasinda)
**Metin Ici Atif:** 30 (benzersiz cite key)
**Hedef Dergi:** IEEE Access

---

## Ozet

| Kategori | Sayi |
|----------|------|
| Dogrulanmis | 29 |
| Duzeltildi (bu revizyonda) | 3 |
| Ghost Citation (bib'de var, cite yok) | 5 |
| Hallucinated (onceki seferde kaldirilmis) | 1 (adbm2025iclr) |

---

## Bu Revizyonda Yapilan Duzeltmeler

### 1. `ars2024neurips` -> `lyu2024adaptive` [KRITIK]

**Sorun:** Bib key yanlis (`ars2024neurips`), yazar listesi TAMAMEN yanlis.

**Onceki (YANLIS):**
```bibtex
@inproceedings{ars2024neurips,
  author={Lyu, Saiyue and Gowal, Sven and Sherborne, Tom and Dvijotham, Krishnamurthy},
  ...
}
```

**Duzeltilmis:**
```bibtex
@inproceedings{lyu2024adaptive,
  title={Adaptive Randomized Smoothing: Certified Adversarial Robustness for Multi-Step Defences},
  author={Lyu, Saiyue and Shaikh, Shadab and Shpilevskiy, Frederick and Shelhamer, Evan and L{\'e}cuyer, Mathias},
  booktitle={Advances in Neural Information Processing Systems},
  volume={37},
  year={2024}
}
```

**Dogrulama:** NeurIPS 2024 proceedings, arXiv:2406.10427
**Metin ici guncelleme:** `02_related_work.tex` -- `\cite{ars2024neurips}` -> `\cite{lyu2024adaptive}`

---

### 2. `wei2024enhancing` -> `zhu2024enhancing` [KRITIK]

**Sorun:** Yazar listesi TAMAMEN yanlis. "Wei, Zhiyu and Chen, Haoyu and Goldstein, Tom" hicbiri bu makalenin yazari degil.

**Onceki (YANLIS):**
```bibtex
@inproceedings{wei2024enhancing,
  author={Wei, Zhiyu and Chen, Haoyu and Goldstein, Tom},
  ...
}
```

**Duzeltilmis:**
```bibtex
@inproceedings{zhu2024enhancing,
  title={Enhancing Transferable Adversarial Attacks on Vision Transformers through Gradient Normalization Scaling and High-Frequency Adaptation},
  author={Zhu, Zhiyu and Wang, Xinyi and Jin, Zhibo and Zhang, Jiayu and Chen, Huaming},
  booktitle={International Conference on Learning Representations},
  year={2024}
}
```

**Dogrulama:** ICLR 2024 proceedings, OpenReview (id=1BuWv9poWz)
**Metin ici guncelleme:** `02_related_work.tex` -- `\cite{wei2024enhancing}` -> `\cite{zhu2024enhancing}`

---

### 3. `jain2024towards` [ORTA]

**Sorun:** 4 yazar listeleniyordu, gercekte 2 yazar. "Addepalli, Sravanti", "Saha, Prem", "Venkatesh, Babu R." bu makalenin yazarlari degil.

**Onceki (YANLIS):**
```bibtex
  author={Jain, Samyak and Addepalli, Sravanti and Saha, Prem and Venkatesh, Babu R.},
```

**Duzeltilmis:**
```bibtex
  author={Jain, Samyak and Dutta, Tanima},
  pages={24736--24745},
```

**Dogrulama:** CVPR 2024 Open Access, CVF proceedings

---

## Onceki Revizyonda Duzeltilmis (Dogrulandi)

### 4. `demontis2019adversarial` -- DOGRULANDI
- Venue: 28th USENIX Security Symposium, pages 321--338, 2019
- Dogrulama: usenix.org/conference/usenixsecurity19/presentation/demontis

### 5. `mahmood2021robustness` -- DOGRULANDI
- Yazarlar: Mahmood, Kaleel and Mahmood, Rigel and Van Dijk, Marten
- Venue: IEEE/CVF International Conference on Computer Vision, pages 7838--7847, 2021
- Dogrulama: openaccess.thecvf.com, arXiv:2104.02610

### 6. `naseer2022improving` -- DOGRULANDI
- Yazarlar: Naseer, Muzammal and Ranasinghe, Kanchana and Khan, Salman and Khan, Fahad Shahbaz and Porikli, Fatih
- Venue: International Conference on Learning Representations, 2022 (Spotlight)
- Not: "Salman H. Khan" -> "Salman Khan" olarak duzeltildi (arXiv ve OpenReview'daki haliyle)
- Dogrulama: openreview.net/forum?id=D6nH3719vZy, github.com/Muzammal-Naseer/ATViT

### 7. `adbm2025iclr` -- KALDIRILDI (onceki revizyon)
- Hallucinated referans, bib dosyasindan silinmis
- Metin icinden de silinmis
- Alternatif `nie2022diffusion` onerilmisti ama eklenmedi (metin icinde kullanilmiyor)

---

## Ghost Citation Analizi

Asagidaki referanslar bib dosyasinda mevcut ancak hicbir tex dosyasinda cite edilmiyor:

| Key | Aciklama | Oneri |
|-----|----------|-------|
| `krizhevsky2009learning` | CIFAR-10 dataset referansi | Metodoloji bolumunde cite edilmeli |
| `loshchilov2017decoupled` | AdamW optimizer | Training protocol'de cite edilmeli |
| `loshchilov2016sgdr` | Cosine annealing LR | Training protocol'de cite edilmeli |
| `vaswani2017attention` | Transformer mimarisi | ViT tanitiminda cite edilmeli |
| `zheng2024towards` | ViT transfer attack | Transfer bolumunde cite edilebilir |

**Oneri:** Ilk 4 referans temel kaynaklardir ve metin icinde uygun yerlerde cite edilmelidir. `zheng2024towards` istege bagli.

---

## Tum Referans Dogrulama Tablosu

| # | Key | Durum | Yil | Venue | Sorun |
|---|-----|-------|-----|-------|-------|
| 1 | szegedy2014intriguing | DOGRULANDI | 2014 | arXiv/ICLR 2014 | - |
| 2 | goodfellow2015explaining | DOGRULANDI | 2015 | arXiv/ICLR 2015 | - |
| 3 | madry2018towards | DOGRULANDI | 2018 | ICLR 2018 | - |
| 4 | carlini2017towards | DOGRULANDI | 2017 | IEEE S&P 2017 | - |
| 5 | croce2020reliable | DOGRULANDI | 2020 | ICML 2020 | - |
| 6 | papernot2016transferability | DOGRULANDI | 2016 | arXiv 2016 | - |
| 7 | demontis2019adversarial | DUZELTILDI | 2019 | USENIX Security 2019 | Onceki revizyonda duzeltildi |
| 8 | zhang2019theoretically | DOGRULANDI | 2019 | ICML 2019 | - |
| 9 | wang2020improving | DOGRULANDI | 2020 | ICLR 2020 | - |
| 10 | tramer2018ensemble | DOGRULANDI | 2018 | ICLR 2018 | - |
| 11 | guo2018countering | DOGRULANDI | 2018 | ICLR 2018 | - |
| 12 | cohen2019certified | DOGRULANDI | 2019 | ICML 2019 | - |
| 13 | he2016deep | DOGRULANDI | 2016 | CVPR 2016 | - |
| 14 | zagoruyko2016wide | DOGRULANDI | 2016 | arXiv (BMVC 2016) | Opsiyonel: BMVC venue ekle |
| 15 | xie2020adversarial | DOGRULANDI | 2020 | CVPR 2020 | - |
| 16 | dosovitskiy2021image | DOGRULANDI | 2021 | ICLR 2021 | - |
| 17 | vaswani2017attention | DOGRULANDI | 2017 | NeurIPS 2017 | GHOST: Cite edilmiyor |
| 18 | bhojanapalli2021understanding | DOGRULANDI | 2021 | ICCV 2021 | - |
| 19 | mahmood2021robustness | DUZELTILDI | 2021 | ICCV 2021 | Onceki revizyonda duzeltildi |
| 20 | shao2022adversarial | DOGRULANDI | 2022 | ECCV 2022 | - |
| 21 | paul2022vision | DOGRULANDI | 2022 | AAAI 2022 | - |
| 22 | naseer2022improving | DUZELTILDI | 2022 | ICLR 2022 | Onceki revizyonda duzeltildi |
| 23 | croce2021robustbench | DOGRULANDI | 2021 | arXiv (NeurIPS 2021) | Opsiyonel: NeurIPS venue ekle |
| 24 | krizhevsky2009learning | DOGRULANDI | 2009 | Tech Report | GHOST: Cite edilmiyor |
| 25 | loshchilov2017decoupled | DOGRULANDI | 2017/2019 | arXiv (ICLR 2019) | GHOST: Cite edilmiyor |
| 26 | loshchilov2016sgdr | DOGRULANDI | 2016/2017 | arXiv (ICLR 2017) | GHOST: Cite edilmiyor |
| 27 | rw2019timm | DOGRULANDI | 2019 | GitHub/Zenodo | - |
| 28 | moosavi2017universal | DOGRULANDI | 2017 | CVPR 2017 | - |
| 29 | jain2024towards | DUZELTILDI | 2024 | CVPR 2024 | Bu revizyonda duzeltildi |
| 30 | zhang2023tgr | DOGRULANDI | 2023 | CVPR 2023 | - |
| 31 | ma2023transferable | DOGRULANDI | 2023 | ICCV 2023 | - |
| 32 | zhu2024enhancing | DUZELTILDI | 2024 | ICLR 2024 | Bu revizyonda duzeltildi |
| 33 | lyu2024adaptive | DUZELTILDI | 2024 | NeurIPS 2024 | Bu revizyonda duzeltildi |
| 34 | wang2023understanding | DOGRULANDI | 2023 | Information Sciences | - |
| 35 | zheng2024towards | DOGRULANDI | 2024 | J. Systems Arch. | GHOST: Cite edilmiyor |

---

## IEEE Access Formatlama Notlari

IEEE Access, IEEE citation style kullanir (numerik, siralama giris sirasina gore). Dikkat edilecek noktalar:

1. **Konferans adlari:** "Proc." kisaltmasi ve tam ad gerekli olabilir
2. **arXiv referanslari:** IEEE Access arXiv preprint'leri kabul eder ancak mumkunse yayinlanmis versiyonu tercih edin
3. **DOI:** Mumkun olan tum referanslara DOI ekleyin
4. **Entry type tutarliligi:** `@inproceedings` vs `@article` dogru kullanilmali

---

## Sonuc

### Tamamlanan Duzeltmeler
1. `ars2024neurips` -> `lyu2024adaptive` (key + yazarlar duzeltildi)
2. `wei2024enhancing` -> `zhu2024enhancing` (key + yazarlar duzeltildi)
3. `jain2024towards` (yazarlar + sayfalar duzeltildi)
4. `naseer2022improving` (yazar adi kucuk duzeltme: "Salman H. Khan" -> "Salman Khan")

### Onerilen Islemler (kullaniciya birakildi)
1. Ghost citation'lari ya cite edin ya da bib'den kaldirin
2. Opsiyonel venue guncellemeleri (zagoruyko, croce2021, loshchilov'lar)
3. DOI'lerin eklenmesi

*Rapor guncelleme tarihi: 2026-02-16*
