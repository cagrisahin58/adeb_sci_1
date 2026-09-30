"""Atif-baglam duzeltmeleri (raporlar/atif_2026-09-30/rapor.md, Bolum 4.1: A1-A13, O1).
EN el yazmasi. Her eski dize TAM BIR kez gecmeli; aksi halde durur, dosya yazilmaz.
Yeniden calistirmaya karsi guvenli: eski dize yoksa ve yeni dize varsa 'zaten uygulandi' der.
Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_atif_baglam_en.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
SEC = ROOT / "paper" / "manuscript" / "sections"

PATCHES = {
    "01_introduction.tex": [
        # A1: TREND (ravikumar2023trend) hic ViT icermiyor; Mahmood/Benz/Shao ayni yonu bildiriyor.
        (
            "whereas Benz et al.~\\cite{benz2021adversarial} report ViTs to be more robust for standardly trained models; "
            "studies of cross-architecture transfer likewise disagree on whether attacks move more easily from CNNs to ViTs "
            "or the reverse~\\cite{mahmood2021robustness, ravikumar2023trend, naseer2022improving}. ",
            "whereas Benz et al.~\\cite{benz2021adversarial} report ViTs to be more robust for standardly trained models. "
            "Transfer studies add a disagreement of their own: several report that attacks move more easily from ViTs to CNNs "
            "than the reverse~\\cite{mahmood2021robustness, benz2021adversarial, shao2022adversarial}, whereas Naseer et "
            "al.~\\cite{naseer2022improving} find that perturbations crafted on ViTs transfer poorly under conventional attacks, "
            "and the direction measured in this paper is the opposite of the first group's, a point "
            "Section~\\ref{sec:discussion} returns to. ",
        ),
    ],
    "02_related_work.tex": [
        # A8: ARS sertifika yaricapi iddiasi kaynakta yok.
        (
            "Recent advances in certified robustness include Adaptive Randomized Smoothing~\\cite{lyu2024adaptive}, "
            "which improves certification radii through multi-step defenses.",
            "Recent advances in certified robustness include Adaptive Randomized Smoothing~\\cite{lyu2024adaptive}, "
            "which extends randomized smoothing to certify test-time adaptive, multi-step models.",
        ),
        # A12: lider tablosu mimariden bagimsiz.
        (
            "The RobustBench leaderboard~\\cite{croce2021robustbench} tracks state-of-the-art CNN robustness, "
            "with WideResNet variants achieving the highest robust accuracy on CIFAR-10.",
            "The RobustBench leaderboard~\\cite{croce2021robustbench} tracks robust accuracy across architectures, "
            "and WideResNet variants occupy the top of its CIFAR-10 ranking.",
        ),
        # A7: Chalasani oznitelik atiflarini olcer, ham gradyani degil.
        (
            "yielding more perceptually aligned~\\cite{tsipras2019robustness} and sparser~\\cite{chalasani2020concise} gradients.",
            "yielding more perceptually aligned gradients~\\cite{tsipras2019robustness} and sparser feature "
            "attributions~\\cite{chalasani2020concise}.",
        ),
        # A3: Bhojanapalli 'kuresel alici alan' demiyor; on-egitim kosulu dusmus.
        (
            "Initial studies suggested that ViTs exhibit some inherent robustness properties due to their global "
            "receptive field~\\cite{bhojanapalli2021understanding}.",
            "Bhojanapalli et al.~\\cite{bhojanapalli2021understanding} found ViTs at least as robust as ResNets across "
            "a broad range of perturbations when pre-trained on enough data.",
        ),
        # A2: Shao'da 'egitim kararsizligi' yok; manset sonuc anilmiyordu.
        (
            "Shao et al.~\\cite{shao2022adversarial} demonstrated that adversarial training can improve ViT robustness "
            "and that ViT features rely less on high-frequency content, though challenges remain due to training instability.",
            "Shao et al.~\\cite{shao2022adversarial} found ViTs more robust than CNNs and MLP-Mixers in white-box and "
            "transfer settings, with features that carry less high-frequency content, and showed that adversarial "
            "training applies to ViTs, although in their preliminary CIFAR-10 run the adversarially trained ViT did not "
            "improve on a large CNN.",
        ),
        # A4: Jain'in katkisi gradyan maskeleme teshisi; 'state-of-the-art' iddiasi yok.
        (
            "More recently, Jain et al.~\\cite{jain2024towards} proposed Adaptive Attention Scaling Adversarial Training "
            "(AAS-AT) to address ViT-specific training challenges, achieving state-of-the-art robustness on CIFAR-10 and "
            "ImageNet-100;",
            "More recently, Jain et al.~\\cite{jain2024towards} traced a form of gradient masking in ViTs to softmax "
            "underflow in attention, which leaves PGD-style attacks sub-optimal on them, a caveat for PGD-only ViT "
            "evaluations that AutoAttack, with its gradient-free Square component, partly guards against; the "
            "adversarial-training recipe they build on the corrected attack improves on existing ViT recipes on "
            "CIFAR-10 and ImageNet-100;",
        ),
        # A6: Demontis'in iki etkeni: hedefin ickin kirilganligi ve vekil modelin karmasikligi.
        (
            "The transferability depends on factors including model architecture, training data, and attack "
            "methods~\\cite{demontis2019adversarial}.",
            "Demontis et al.~\\cite{demontis2019adversarial} trace transferability to two factors, the intrinsic "
            "vulnerability of the target model and the complexity of the surrogate, and connect it to the alignment "
            "of the two models' input gradients.",
        ),
        # A10: Zhao'nun kilavuzlari kosullama kumesiyle ilgili degil; havuz secimi deney duzenegi.
        (
            "recent evaluation guidelines make such protocol choices explicit~\\cite{zhao2025revisiting}.",
            "systematic re-evaluations of transfer attacks likewise restrict the pool to samples that every model "
            "classifies correctly~\\cite{zhao2025revisiting}.",
        ),
        # A5: Chen ozeti erisilemedi; saldiri makalesi olarak anilir, frekans tercihi Benz/Shao'ya baglanir.
        (
            "Chen et al.~\\cite{chen2023understanding} systematically analyze the factors affecting cross-architecture "
            "transferability, finding that architectural inductive biases, with CNNs preferring high-frequency "
            "information while ViTs favor low-frequency patterns, shape transfer success.",
            "Chen et al.~\\cite{chen2023understanding} propose a transfer attack that exploits the differing inductive "
            "biases of CNNs and ViTs; the frequency preferences behind that difference, CNNs leaning on high-frequency "
            "and ViTs on low-frequency content, are documented by Benz et al.~\\cite{benz2021adversarial} and Shao et "
            "al.~\\cite{shao2022adversarial}.",
        ),
        # A9 (02:74): kaynaklar ortak-dogru havuz kullaniyor.
        (
            "Conditioning transfer evaluation on correctly classified samples is established "
            "practice~\\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend}, and "
            "individual papers pick one protocol and proceed.",
            "Conditioning transfer evaluation on samples the models classify correctly is established "
            "practice~\\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend}, and "
            "individual papers pick one conditioning set and proceed.",
        ),
    ],
    "03_methodology.tex": [
        # A11: BN kipi Rice'in makalesinde degil, referans gerceklemesinde.
        (
            "see consistent batch-normalization statistics, following standard adversarial-training "
            "implementations~\\cite{rice2020overfitting}.",
            "see consistent batch-normalization statistics, as in the reference implementation of Rice et "
            "al.~\\cite{rice2020overfitting}.",
        ),
        # A9 (03:118): bes kaynak da ortak-dogru havuz; hedef-dogru oran onun tek yanli gevsetmesi.
        (
            "Conditioning transfer evaluation on correctly classified samples follows established "
            "practice~\\cite{liu2017delving, dong2018boosting, mahmood2021robustness, ravikumar2023trend, "
            "zhao2025revisiting} and matters most in cross-architecture comparisons:",
            "Conditioning transfer evaluation on correctly classified samples is established practice, usually on "
            "the samples that every model in the study classifies correctly~\\cite{liu2017delving, dong2018boosting, "
            "mahmood2021robustness, ravikumar2023trend, zhao2025revisiting}; the target-correct rate is the one-sided "
            "relaxation of that pool, and conditioning matters most in cross-architecture comparisons:",
        ),
    ],
    "04_experiments.tex": [
        # A7 (04:303): nesne adlandirildi.
        (
            "so adversarial training sparsifies CNN gradients far more strongly, consistent "
            "with~\\cite{chalasani2020concise}.",
            "so adversarial training sparsifies CNN gradients far more strongly, in line with the sparser feature "
            "attributions that Chalasani et al.~\\cite{chalasani2020concise} report for adversarially trained models.",
        ),
    ],
    "05_discussion.tex": [
        # O1 + A6: Benz ve Shao da ters yonu bildiriyor; Demontis hedef-kirilganligi etkenini destekliyor.
        (
            "report the opposite direction on a different architecture pair, finding transfer into the transformer "
            "weaker than transfer out of it. Our mechanism is compatible with that result: we attribute the asymmetry "
            "to the target's own vulnerability rather than to any special strength of CNN-crafted perturbations, and "
            "the weaker target in their pair is not the weaker target in ours.",
            "report the opposite direction on a different architecture pair, finding transfer into the transformer "
            "weaker than transfer out of it, and Benz et al.~\\cite{benz2021adversarial} and Shao et "
            "al.~\\cite{shao2022adversarial} report the same ordering on their own model sets. Our mechanism is "
            "compatible with those results: we attribute the asymmetry to the target's own vulnerability rather than "
            "to any special strength of CNN-crafted perturbations, which is also the first of the two factors "
            "Demontis et al.~\\cite{demontis2019adversarial} identify, and the weaker target in Mahmood et al.'s pair "
            "is not the weaker target in ours.",
        ),
        # A13: yalniz Wu ViT'in WRN'i gectigini bildiriyor; Wang WRN taban cizgisi.
        (
            "with diffusion-generated synthetic data ViTs have been reported to surpass WideResNets on "
            "CIFAR-10~\\cite{wang2023better, wu2025vision}.",
            "and a ViT trained with the diffusion-generated data recipe of Wang et al.~\\cite{wang2023better} has "
            "been reported to surpass WideResNets on CIFAR-10~\\cite{wu2025vision}.",
        ),
    ],
}


def main():
    hata = 0
    for fname, pairs in PATCHES.items():
        path = SEC / fname
        text = io.open(path, encoding="utf-8").read()
        new_text = text
        for i, (old, new) in enumerate(pairs, 1):
            n_old = new_text.count(old)
            if n_old == 1:
                new_text = new_text.replace(old, new)
                print(f"OK    {fname} #{i}")
            elif n_old == 0 and new_text.count(new) == 1:
                print(f"ZATEN {fname} #{i} (yeni dize mevcut)")
            else:
                print(f"HATA  {fname} #{i}: eski dize {n_old} kez gecti")
                hata += 1
        if new_text != text and not hata:
            io.open(path, "w", encoding="utf-8", newline="\n").write(new_text)
    if hata:
        print(f"\n{hata} yama uygulanamadi; HICBIR dosya yazilmadi (hatali dosyalar).")
        sys.exit(1)
    print("\nTum EN atif-baglam yamalari tamam.")


if __name__ == "__main__":
    main()
