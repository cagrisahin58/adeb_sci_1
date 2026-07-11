# UYGULAYICI PROMPT — 2026-07-10 Hakem Paneli Revizyonu

> Bu dosyayı yeni bir Claude Code oturumuna olduğu gibi yapıştırın (veya "paper/review/UYGULAYICI_PROMPT_2026-07-10.md dosyasını oku ve uygula" deyin).

---

10 Temmuz 2026 tarihli çok ajanlı hakem paneli bu makale için MAJOR REVISION kararı verdi (3/3 hakem). Görevin: panelin doğrulanmış bulgularını makaleye, bib dosyasına, figürlere ve gönderim paketine uygulamak.

## Kaynak dosyalar (önce bunları oku)

1. `paper/review/HAKEM_RAPORU_2026-07-10.md` — özellikle **(c) Doğrulanmış Bulgular** (37 bulgu: 4 kritik, 10 major, 23 minor; her birinde Konum/Detay/Öneri/Kanıt), **(d) Literatür** (15 must-cite künye + atıf-iddia düzeltmeleri) ve **(g) Aksiyon Listesi**.
2. `paper/review/hakem_bulgular_2026-07-10.json` — aynı verinin makine-okur hali + 3 tam hakem raporu (`reviews` alanı: R1/R2/R3'ün tüm major/minor yorumları ve sorular) + 3 literatür raporu (`literature` alanı: tüm künyeler ve URL'ler).

## Kapsam

- **YAP:** Aksiyon listesindeki **A maddeleri (1–13)**: metin/bib/figür/gönderim-paketi düzeltmeleri — GPU gerektirmez.
- **YAP:** **B maddeleri (14–18)**: mevcut `results/` artefaktlarından hesaplanan istatistik eklemeleri (TOST/iki-oran testi, Tablo 3–4'e ±std ve eşleştirilmiş testler, fig5b entropi nicelemesi, 10k bootstrap). Bunlar için `experiments/` altına küçük analiz betikleri yaz, çıktıları `results/` altına kaydet, sonra tabloları/metni güncelle. Ham veri: `results/autoattack_run3_full/per_sample_*.npz`, `results/transfer_analysis_run3/`, `results/gradient_analysis_run3/gradient_summary.json`, `results/attention_analysis_run3/attention_feature_analysis.csv`.
- **YAPMA:** **C maddeleri (19–24)** yeni GPU deneyi gerektirir (clean-model transfer matrisi, ResNet feature-degradation, clean alignment, MI-FGSM, 3 eğitim seed'i, seed'li FGSM/PGD tekrarı). Bunları UYGULAMA; iş sonunda kullanıcıya onay listesi olarak sun.

## Değişmezler (ground truth — bunlara dokunma, metni BUNLARA hizala)

Run3 final sayıları (tam test n=10.000): ResNet-18 AT clean 85.42 / PGD-10 40.91 / AA **35.74**; ViT-Tiny AT 75.65 / 35.99 / **32.94**; AA farkı 2.80pp, McNemar p=3.1e-12. Koşullu transfer 20.95 [20.08–21.92] vs 20.32 [19.46–21.21] → **asimetri yok** (ham metrik 8.3pp sahte asimetri üretir — ana metodolojik bulgu). Gradient: Hoyer 0.474±0.009 vs 0.449±0.011; alignment ViT **1.36×** (0.052 vs 0.038). Feature degradation: erken düşüş + orta-ağ platosu (min 0.955 @ Blok 8, son bloklarda 0.965'e toparlanma), monotonik DEĞİL.

Bilinçli tasarım kararları (hata değildir, "düzeltme"ye kalkışma): AT saldırı üretimi TRAIN modda (Rice et al. uyumlu; eval-mod üretim BN çöküşü yaratıyor); gradyanlar per-sample loss ile (reduction='sum').

## Çalışma sırası

1. **Faz 1 — Kritik metin düzeltmeleri** (aksiyon 1–5): Conclusion satır 11+16, Introduction satır 21, Discussion satır 75, gönderim paketi (cover_letter.tex / highlights.txt / suggested_reviewers.md run3 anlatısıyla sıfırdan), wang2023understanding→chen2023understanding bib düzeltmesi.
2. **Faz 2 — Yeniden konumlandırma + atıflar** (aksiyon 6–9): koşullu metrik anlatısı ("established practice + confound nicelemesi" çerçevesi), 15 must-cite bib girdisi (raporun (d) tablosundaki künyelerle; **her yeni girdiyi eklemeden önce WebSearch ile künyeyi teyit et** — bu projede daha önce uydurma-yazar vakaları yaşandı), atıf-iddia düzeltmeleri, overclaim yumuşatmaları ("mechanistic", WRN confound, nedensel iddialar, hibrit RQ, Abstract reçete kaydı, simetri kapsam daraltması).
3. **Faz 3 — Metodoloji/tekrarlanabilirlik metni** (aksiyon 10, 13): koşu anlatısı, eğitim seed'leri (ResNet 42 / ViT 123 → farklı val bölmeleri) beyanı, `reproduce_paper.sh` (at_run3 checkpoint yollarıyla tam komut zinciri), `sections/*.bak|*.tmp` ve depo hijyeni, statistical_validation_run3 metadata etiketi.
4. **Faz 4 — İstatistik eklemeleri** (B maddeleri 14–18).
5. **Faz 5 — Figürler** (aksiyon 11): `paper/figures/generate_*.py` ile YALNIZ gerçek artefakttan üret (eksik artefakta karşı raise davranışını koru); fig4 (Hoyer anotasyonu, ortak görüntü/skala, eski panel başlığı), fig_adversarial_examples (gerçekten yanılan ViT örneği), fig5a satır etiketleri, fig5 referans/kaldırma kararı, figür numaralama sırası.
6. **Faz 6 — Biçim** (aksiyon 12): Tablo 1 overfull (56.9pt), abstract ≤250 kelime, Index Terms alfabetik, IEEE Access yazar bloğu, `\balance`, notasyon tutarlılığı.

## Doğrulama (her fazdan sonra; en sonunda tamamı)

- LaTeX: WSL'de `bash -lc "cd ~/projects/adeb_sci_1/paper/manuscript && latexmk -pdf main.tex"` (login shell şart, latexmk ~/.local/bin'de). Hedef: 0 undefined reference, 0 citation error, Tablo 1 overfull uyarısı yok.
- Eski anlatı süpürmesi — şu kalıpların hiçbiri `paper/` altında (manuscript + submission) kalmamalı: `near-identical`, `alignment convergence`, `intensifies with network depth`, `progressive semantic`, `fundamental vulnerability mechanism`, `47.5`, `33.5`, `2.2x`, `4.5x`, `0.917`, `14-percentage`, `41.2`, `36.1`, `5.1pp`, `run1 and run2`.
- Abstract kelime sayısı ≤250; her figür metinde referanslı; her \cite bib'de, her bib girdisi metinde.
- CLI notu: click multiple flag'leri tekrarlanmalı (`-a fgsm -a pgd`), boşluklu liste parse edilmez.

## Kurallar

- Sayıları asla metne uydurma; metni artefakta uydur. Bir sayı artefaktta yoksa ve hesaplanamıyorsa cümleyi kaldır/yumuşat, sayı uydurma.
- Repo URL'si (aksiyon 12): gerçek URL sende yok — kullanıcıya sor; cevap gelmezse üç yerdeki erişilebilirlik dilini "will be made publicly available upon acceptance" olarak birleştir ve TEK bir açık `% TODO(submission): repo URL` bırak.
- Git: commit atma; iş bitince önerilen commit mesajını sun (kullanıcı onaylayınca commit).
- GPU'ya dokunma (eğitim/attack koşusu yok); `nvidia-smi` gerektiren hiçbir şey çalıştırma.
- Karar veremediğin (metin yorumu gerektiren) bulgularda raporun "Öneri" alanındaki ifadeyi temel al; hakem raporlarındaki (JSON `reviews`) alternatif ifadeler ikincil kaynak.

## Bitiş raporu

İş sonunda şunları sun: (1) bulgu-id bazlı tablo — 37 confirmed + 1 uncertain (bicim-11; elle kontrol edip uygulanabilenleri uygula) için `uygulandı / kısmen / atlandı(neden) / kullanıcı-kararı-gerekli`; (2) eklenen bib girdileri listesi (web-teyit durumuyla); (3) latexmk + süpürme kontrol çıktıları; (4) C maddeleri (19–24) için tahmini maliyet/etki tablosuyla kullanıcı onay listesi; (5) önerilen commit mesajı.
