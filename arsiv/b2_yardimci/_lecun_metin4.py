"""LeCun paneli (2026-10-04), 4. parti: yeniden uretilen sekillerin basliklari ve ilgili cumleler, EN + TR.
Sekil 2 (epsilon taramasi: kategorik eksen, eps=0 temiz, ayri kosu, marj sabit degil), Sekil 4 (ECDF, ornek basina
kayip, uc cift), Sekil 5 (gradyan haritalari: cift 1, ilk dort goruntu, harita basina olcek), Sekil 6 (dikkat
haritalari: ortak renk olcegi, 'layer'), Sekil 7 (Δentropi + TOST marji, TV yer degistirmesi). Metin: 4,9 nat ->
4,6-5,1 (foy: katman ortalamalari 4,61-5,11), 'ust uste binen egriler' -> iki panel, 'later layers move more'
ortak olcege baglandi. Kaynaklar: paper/figures/final/*.kanit.json, results/C1_REFERANS_FOYU.md 'Dikkat entropisi'.
Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_lecun_metin4.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]

PATCHES = [
    (ROOT / "paper/manuscript/sections/04_experiments.tex", [
        (
            "\\caption{PGD-10 robust accuracy vs.\\ perturbation budget ($\\eps$), measured on the full test set. Both AT architectures degrade with similar shapes as epsilon increases, with the CNN maintaining a consistent margin.}",
            "\\caption{PGD-10 robust accuracy against the perturbation budget $\\eps$ on the full test set (mean over three runs; the $\\pm$1 std error bars are narrower than the markers). The horizontal axis is categorical and $\\eps=0$ is clean accuracy. The sweep is a separate PGD-10 evaluation, so its $8/255$ point differs from Table~\\ref{tab:main_results} by at most $0.08$ points. The CNN's margin over the ViT is not constant: it is widest at the small budgets and narrows at $16/255$.}",
        ),
        (
            "\\caption{Distribution of per-sample gradient $L_2$ norms for both architectures. The magnitude maps for the same inputs are shown in Figure~\\ref{fig:gradient_heatmap}.}",
            "\\caption{Empirical distribution of per-sample input-gradient $L_2$ norms (per-sample cross-entropy loss, the first $500$ test images, one curve per training run, three runs per architecture; logarithmic axis). Magnitude maps for four of these inputs are shown in Figure~\\ref{fig:gradient_heatmap}.}",
        ),
        (
            "\\caption{Input-gradient magnitude maps for the same test images under both models. CNN gradients place more of their mass on fewer components",
            "\\caption{Input-gradient magnitude maps for the same test images under both models (seed pair 1; the first four test images; each map is scaled to its own maximum, so magnitudes are not comparable across panels). CNN gradients place more of their mass on fewer components",
        ),
        (
            "Each row shows a different layer (1, 6, 12); columns show clean attention, adversarial attention, and their difference. A single sample is shown for illustration; the depth trend in attention displacement is reported quantitatively in the text over $n$=1,000 samples per run.}",
            "Each row shows a different layer (1, 6, 12); columns show clean attention, adversarial attention and their difference, with one shared color scale for the attention columns and one for the difference column. A single sample is shown for illustration (the first test image, seed pair 1); the depth trend in attention displacement is measured over $n$=1,000 samples per run in Figure~\\ref{fig:feature_degradation}(b).}",
        ),
        (
            "\\caption{Per-layer entropy of the CLS attention distribution for clean and adversarial inputs, $n$=1,000 samples per run, mean over three runs with $\\pm$1 s.d. shading. The attention maps themselves are shown in Figure~\\ref{fig:attention_layers}.}",
            "\\caption{(a) Change in CLS attention entropy under attack (adversarial minus clean) per layer, mean over three runs with $95\\%$ $t$ confidence intervals; the dashed lines mark the $\\pm0.05$-nat TOST margin, and every interval lies inside it. (b) CLS attention displacement (total variation between the clean and adversarial maps) per layer, mean$\\pm$std over runs. $n$=1,000 samples per run; single-sample maps are shown in Figure~\\ref{fig:attention_layers}.}",
        ),
        (
            "against layer means near 4.9 nats,",
            "against layer means between $4.6$ and $5.1$ nats,",
        ),
        (
            "Figure~\\ref{fig:feature_degradation} plots the per-layer curves, which lie on top of each other.",
            "Figure~\\ref{fig:feature_degradation}(a) plots the per-layer change against the TOST margin, and panel (b) the displacement.",
        ),
        (
            "It agrees with the displacement measurement, since later layers move more, but single-sample panels of this kind are easy to over-read:",
            "Under one shared color scale the later layers show the larger difference, in agreement with the displacement curve of Figure~\\ref{fig:feature_degradation}(b), but single-sample panels of this kind are easy to over-read:",
        ),
    ]),
    (ROOT / "paper/manuscript_tr/sections/04_deneyler.tex", [
        (
            "\\caption{Pertürbasyon bütçesine ($\\eps$) göre PGD-10 gürbüz doğruluğu; tam test kümesi, üç koşu ortalaması ($\\pm$1 std bantları). İki AT mimarisi de epsilon arttıkça benzer biçimlerle bozulmakta, CNN tutarlı bir marj korumaktadır.}",
            "\\caption{Pertürbasyon bütçesi $\\eps$'a göre PGD-10 gürbüz doğruluğu, tam test kümesi (üç koşu ortalaması; $\\pm$1 std hata çubukları işaretçilerden dardır). Yatay eksen kategoriktir ve $\\eps=0$ temiz doğruluktur. Tarama ayrı bir PGD-10 değerlendirmesidir; bu yüzden $8/255$ noktası Tablo~\\ref{tab:main_results}'den en çok $0{,}08$ puan ayrılır. CNN'in ViT üzerindeki marjı sabit değildir: küçük bütçelerde en geniş, $16/255$'te daralmış hâldedir.}",
        ),
        (
            "\\caption{İki mimaride örnek başına gradyan $L_2$ normlarının dağılımı. Aynı girdiler için enerji haritaları Şekil~\\ref{fig:gradient_heatmap}'te verilmektedir.}",
            "\\caption{Örnek başına girdi gradyanı $L_2$ normlarının deneysel dağılımı (örnek başına çapraz entropi kaybı, ilk $500$ test görüntüsü, eğitim koşusu başına bir eğri, mimari başına üç koşu; logaritmik eksen). Bu girdilerden dördünün büyüklük haritaları Şekil~\\ref{fig:gradient_heatmap}'te verilmektedir.}",
        ),
        (
            "\\caption{Aynı girdiler üzerinde CNN ve ViT gradyan enerji haritalarının karşılaştırması. Farklar",
            "\\caption{Aynı girdiler üzerinde CNN ve ViT gradyan enerji haritalarının karşılaştırması (tohum çifti 1; ilk dört test görüntüsü; her harita kendi en büyük değerine ölçeklendiğinden büyüklükler paneller arasında karşılaştırılamaz). Farklar",
        ),
        (
            "Her satır farklı bir katmanı (1, 6, 12) gösterir; sütunlar temiz dikkat, çekişmeli dikkat ve farklarıdır. Gösterilen tek bir örnektir; dikkat kaymasındaki derinlik eğilimi metinde koşum başına $n=1000$ örnek üzerinden nicel olarak verilmektedir.}",
            "Her satır farklı bir katmanı (1, 6, 12) gösterir; sütunlar temiz dikkat, çekişmeli dikkat ve farklarıdır; dikkat sütunları için bir, fark sütunu için bir ortak renk ölçeği kullanılmıştır. Gösterilen tek bir örnektir (ilk test görüntüsü, tohum çifti 1); dikkat kaymasındaki derinlik eğilimi koşum başına $n=1000$ örnek üzerinden Şekil~\\ref{fig:feature_degradation}(b)'de ölçülmektedir.}",
        ),
        (
            "\\caption{Temiz ve çekişmeli girdiler için CLS dikkat dağılımının katman başına entropisi; koşum başına $n=1000$ örnek, üç koşum ortalaması ve $\\pm$1 std bandı. Dikkat haritalarının kendisi Şekil~\\ref{fig:attention_layers}'te verilmektedir.}",
            "\\caption{(a) Saldırı altında CLS dikkat entropisindeki değişim (çekişmeli eksi temiz), katman başına, üç koşum ortalaması ve \\%95 $t$ güven aralıkları; kesikli çizgiler $\\pm0{,}05$ nat TOST marjını gösterir ve her aralık bu marjın içindedir. (b) CLS dikkat yer değiştirmesi (temiz ile çekişmeli haritalar arasındaki toplam varyasyon), katman başına, koşumlar üzerinden ortalama$\\pm$std. Koşum başına $n=1000$ örnek; tek örnekli haritalar Şekil~\\ref{fig:attention_layers}'te verilmektedir.}",
        ),
        (
            "(katman ortalamaları 4,9 nat civarındayken)",
            "(katman ortalamaları $4{,}6$ ile $5{,}1$ nat arasındayken)",
        ),
        (
            "Şekil~\\ref{fig:feature_degradation} üst üste binen katman başına eğrileri vermektedir.",
            "Şekil~\\ref{fig:feature_degradation}(a) katman başına değişimi TOST marjıyla birlikte, (b) paneli ise yer değiştirmeyi vermektedir.",
        ),
        (
            "Yer değiştirme ölçümüyle uyumludur, çünkü geç katmanlar daha çok hareket eder; ancak bu türden tek örnekli paneller kolayca fazla yorumlanır:",
            "Ortak renk ölçeğinde en büyük fark geç katmanlardadır ve bu, Şekil~\\ref{fig:feature_degradation}(b)'deki yer değiştirme eğrisiyle uyumludur; ancak bu türden tek örnekli paneller kolayca fazla yorumlanır:",
        ),
    ]),
]


def main():
    hata = 0
    for path, pairs in PATCHES:
        text = io.open(path, encoding="utf-8").read()
        new_text = text
        for i, (old, new) in enumerate(pairs, 1):
            n_old = new_text.count(old)
            if n_old == 1:
                new_text = new_text.replace(old, new)
                print(f"OK    {path.name} #{i}")
            elif n_old == 0 and new_text.count(new) == 1:
                print(f"ZATEN {path.name} #{i}")
            else:
                print(f"HATA  {path.name} #{i}: eski dize {n_old} kez gecti")
                hata += 1
        if new_text != text and not hata:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    if hata:
        print(f"\n{hata} yama uygulanamadi; hatali dosya(lar) yazilmadi.")
        sys.exit(1)
    print("\n4. parti tamam.")


if __name__ == "__main__":
    main()
