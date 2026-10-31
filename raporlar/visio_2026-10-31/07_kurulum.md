# Kurulum raporu (visio-cizici adım 9, kurulum ajanı)

Tarih 31.10.2026. Yazan kurulum ajanıdır (gorsel-uretici rolü); Visio açılmamış, git işlemi yapılmamıştır. Bağlayıcı plan `raporlar/visio_2026-10-31/04_cizim_plani.md` bölüm 8 ve 9'dur, çizim raporları `05_visio_cizim.md` ve `06_kart_cizim.md`'dir.

En önemli üç sonuç şunlardır. Birincisi, planın on yedi şeklinin on yedisi `motor/visio/install.py` ile beş kapıdan geçerek `paper/figures/` altına `fig1_study_overview` ile `fig17_feature_degradation` arasındaki adlarla kurulmuştur; hiçbir kapı reddetmemiş, bu yüzden `fig_mm_pdf` ya da `denge` yeniden koşulmamıştır. İkincisi, kurulu her PDF'in SHA-256'sı yapım klasöründeki PDF'inkine eşittir (17/17; PNG, EPS ve SVG de 17/17 eşit); bu yüzden altı Visio şeklinin yapım klasöründeki `.vsdx`'i kurulu şeklin taslağıdır ve on bir kart şeklinin kurulum adlı `.fig.json` ile `.mm.json`'u Drawing drafts paketine doğrudan girebilir. Üçüncüsü, kurulu JSON dosyalarının hiçbirinde kullanıcı yolu kalmamıştır (`yollar.kullanici_yolu_say` 0); `--yollari-temizle` bu nedenle bir şey değiştirmeyecektir, ancak paketleme adımında skill sırası gereği yine koşulmalıdır.

## 1. Eşleme

`paper/figures/qc/ESLEME.md` elle yazılmıştır, çünkü yapım kökleri bugünkü include adlarından farklıdır ve yeni sıra plandan gelir. Bugünkü basılı numaralar `included_figures.py --tex paper/figures/qc/main_en_duz.tex --tablo` ile okunmuştur: düz kopyada 12 şekil vardır, `fig2_epsilon_sweep` (bugün 11) ve `fig5b_attention_entropy` (bugün 12, etiket `fig:feature_degradation`) "STALE" görünür. Eşleme dosyasının ilk iki sütunu yapım kökü ve kurulum adıdır; motor, hedef sıra, bugünkü numara ve plan notu sütunları okur içindir. `install.read_mapping` dosyadan 17 satır okumuştur.

## 2. Kapılar ve kurulum

Kurulumdan önce `install.py`'nin kendi fonksiyonlarıyla (`manuscript_name`, `find_build`, `gates`, `_targets`, `_check_free`) dosya yazmayan bir ön denetim koşulmuş ve 17 şeklin 17'si "kurulabilir" çıkmıştır. Git sorgusu Windows Python'dan UNC yolunda çalışmış, hedef altında izlenen 574 dosyayı listelemiştir; hiçbir kurulum adı bunlarla çakışmamıştır. Ardından her şekil için şu komut koşulmuştur (Git Bash, depo kökü `VZ_PROJE_KOKU` ile, `MSYS_NO_PATHCONV=1`):

```bash
python "$V/motor/visio/install.py" <kök> --hedef paper/figures
```

Beş kapı şunlardır: K-a denetçi raporu PASS (Visio `<kök>_mm_kontrol.json`, kart `<kök>.mm.json`), K-b PDF rapordan yeni değil, K-c `paper/figures/qc/<kök>/fig_mm_pdf.json` PASS ve PDF'ten eski değil, K-d `paper/figures/qc/<kök>/denge.json` "kurulabilir" ve PDF'ten eski değil, K-e Visio yapısında kayıtlı oturum DPI'ı projeyle tutuyor (`visio.dpi` 120). K-e kart şekillerine uygulanmaz. Her kurulum yedi dosya yazmıştır (PDF, PNG, EPS, SVG, `.fig.json`, `.kanit.json`, denetçi raporu); toplam 119 dosya ve kurulum günlüğünde (`paper/figures/visio_loglari/kurulum.log`) 119 "kur" satırı vardır, Visio PDF satırlarının altısı da `dpi=120` taşır. Manifestin ve kanıt dosyasının `stem` alanı yeni adı taşır, manifestin `formats` alanı yeni adlı dosyaları gösterir; Visio denetçi raporunun `stem` alanı da yeni addır. Kart denetçi raporunda (`.mm.json`) `stem` alanı yoktur, bu motorun biçimidir ve yeniden adlandırılacak alan bulunmamıştır. Kanıt dosyalarındaki `betik` ve `hesap` alanları yapım betiğinin yolunu (`paper/figures/charts/fig_<kök>.py`, `paper/figures/visio/...`) taşımayı sürdürür; bu alanlar kaynak izidir ve değişmemesi doğrudur.

İzlenen özgün dosyalar değişmemiştir: kurulumdan sonra `git status --short --untracked-files=no -- paper/figures` boş çıkmıştır. `figures/final`, `final_tr`, `konsey` ve `overview` klasörlerine dokunulmamıştır.

| Sıra | Kök | Kurulum adı | Motor | K-a | K-b | K-c | K-d | K-e (DPI) | PDF SHA-256 (ilk 16) | PDF SHA eşit | Taslak |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | study_overview | fig1_study_overview | Visio | PASS | tamam | PASS | kurulabilir | 120 | 950f2e2d4e427fc7 | evet | `paper/figures/visio/study_overview.vsdx` |
| 2 | design_recipe | fig2_design_recipe | Visio | PASS | tamam | PASS | kurulabilir | 120 | 405f72d9274ef805 | evet | `paper/figures/visio/design_recipe.vsdx` |
| 3 | decomposition_schematic | fig3_decomposition_schematic | Visio | PASS | tamam | PASS | kurulabilir | 120 | b434d6de3cc1548a | evet | `paper/figures/visio/decomposition_schematic.vsdx` |
| 4 | panel_members | fig4_panel_members | Visio | PASS | tamam | PASS | kurulabilir | 120 | b3eaf0edd435bf3f | evet | `paper/figures/visio/panel_members.vsdx` |
| 5 | registry_map | fig5_registry_map | Visio | PASS | tamam | PASS | kurulabilir | 120 | b4abce0ab38c5ba2 | evet | `paper/figures/visio/registry_map.vsdx` |
| 6 | prereg_chain | fig6_prereg_chain | Visio | PASS | tamam | PASS | kurulabilir | 120 | d5f159b26d8abbea | evet | `paper/figures/visio/prereg_chain.vsdx` |
| 7 | source_gap_split | fig7_source_gap_split | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | d19930a0d4fb29e0 | evet | `fig7_source_gap_split.fig.json`, `.mm.json` |
| 8 | similarity_matrix | fig8_similarity_matrix | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | 36784360c6871257 | evet | `fig8_similarity_matrix.fig.json`, `.mm.json` |
| 9 | cells_interaction | fig9_cells_interaction | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | 6926e96d524f346f | evet | `fig9_cells_interaction.fig.json`, `.mm.json` |
| 10 | attack_side | fig10_attack_side | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | c55c2bf0cf4e04d8 | evet | `fig10_attack_side.fig.json`, `.mm.json` |
| 11 | gradient_alignment | fig11_gradient_alignment | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | cc508c93770da257 | evet | `fig11_gradient_alignment.fig.json`, `.mm.json` |
| 12 | estimates_forest | fig12_estimates_forest | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | 2cee60a1132cb6e1 | evet | `fig12_estimates_forest.fig.json`, `.mm.json` |
| 13 | protocol_settings | fig13_protocol_settings | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | e443d9bf00af0632 | evet | `fig13_protocol_settings.fig.json`, `.mm.json` |
| 14 | protocol_sets | fig14_protocol_sets | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | 28cf9c79366cd08b | evet | `fig14_protocol_sets.fig.json`, `.mm.json` |
| 15 | spread_clean_gap | fig15_spread_clean_gap | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | 1363d40568f807c6 | evet | `fig15_spread_clean_gap.fig.json`, `.mm.json` |
| 16 | epsilon_sweep | fig16_epsilon_sweep | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | 2288750913bb60fa | evet | `fig16_epsilon_sweep.fig.json`, `.mm.json` |
| 17 | feature_degradation | fig17_feature_degradation | kart | PASS | tamam | PASS | kurulabilir | uygulanmaz | af9d1daadcd5489c | evet | `fig17_feature_degradation.fig.json`, `.mm.json` |

Tam SHA-256 değerleri (PDF, PNG, EPS, SVG ve üç JSON için yapım ve kurulu taraf ayrı ayrı) ile `.vsdx` SHA-256'ları `paper/figures/visio_loglari/kurulum_sha_denetimi.json` dosyasındadır. Altı `.vsdx`'in değişiklik zamanı yanındaki PDF'inkinden en çok 0.2 saniye farklıdır; bu, ikisinin aynı Visio koşusunda yazıldığını gösterir ve SHA eşitliğiyle birlikte taslağın kurulu şekle ait olduğunu doğrular (skill adım 9).

## 3. Drawing drafts için notlar

Paket bu ajanın görevi değildir; paketleme adımı için şu bilgiler hazırdır. Visio taslaklarının yazar alanları okunmuş ve değiştirilmemiştir: altı `.vsdx`'in altısında da `docProps/core.xml` içinde `dc:creator` ve `cp:lastModifiedBy` "ÇAĞRI ŞAHİN", `docProps/app.xml` içinde `Company` boştur. IEEE Access'in hakemlik türü (tek kör ya da çift kör) bu oturumda dergi kılavuzundan okunmamıştır; çift kör hakemlikte bu ad kimliği açığa çıkarır, bu yüzden paketin bu hâliyle yüklenip yüklenmeyeceği yazara bırakılmıştır (`references/venue.md` bölüm 7). Paketlemede taslaklar kurulum adıyla kopyalanmalıdır (`study_overview.vsdx` yerine `fig1_study_overview.vsdx` gibi), çünkü kurulum `.vsdx`'i hedefe taşımaz ve yapım klasöründe bırakır. Sıra şudur: `install.py --yollari-temizle fig1_study_overview ... fig17_feature_degradation`, kopyalama, `SHA256SUMS.txt` ve İngilizce `README.md`, ardından `install.py --yollari-tara paper/submission/Drawing_drafts`; tarama 1 verirse paketleme durur ve yol kaynağında giderilir.

## 4. Açık kalanlar

Şekil başına `fig_qc.py` (K4) ve makale düzeyi kapılar (M-K1 `zenginlik.py --makale`, M-K2 `fig_qc.py --consistency`, M-K4 `included_figures.py --tablo` ile 17 şekil) bu adımda koşulmamıştır, çünkü bu kapılar metnin yeni adlarla yeniden yazılmasını ve düz kopyanın yeniden üretilmesini bekler (plan bölüm 11); bugünkü `main_en_duz.tex` hâlâ eski 12 şeklin include adlarını taşımaktadır. Kurulum adlarının makaledeki `\includegraphics` satırlarına işlenmesi, altyazılar, kaldırılacak tablolar ve TR aynası yazım ajanının işidir. TR aynası bu turda aynı İngilizce etiketli PDF'leri kullanır, TR dilli şekiller ise ikinci tura (plan 12.6) kalır ve devir notuna yazılmalıdır. Kart denetçi raporlarında `stem` alanı bulunmadığından yeniden adlandırma bu dosyalarda yalnız dosya adını değiştirmiş, içerik baytları yapım kopyasıyla aynı kalmıştır.

## 5. Yazılan dosyalar ve günlükler

`paper/figures/qc/ESLEME.md`; `paper/figures/fig{1..17}_<kök>.{pdf,png,eps,svg,fig.json,kanit.json}` ve Visio için `_mm_kontrol.json`, kart için `.mm.json` (119 dosya); `paper/figures/visio_loglari/kurulum.log` (motorun günlüğü); `paper/figures/visio_loglari/kurulum_ajani_komutlar.log` (komut günlüğü); `paper/figures/visio_loglari/kurulum_ajani_durum.json`; `paper/figures/visio_loglari/kurulum_sha_denetimi.json`. Ön denetim ve SHA denetimi betikleri ajanın karalama klasöründedir (`on_denetim.py`, `sha_denetim.py`) ve depoya girmez.
