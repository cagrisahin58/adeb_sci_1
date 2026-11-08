#!/usr/bin/env python
"""Build the Drawing drafts v2 package (paper/submission/Drawing_drafts_v2) from the installed v2 figures.

    python paper/figures_v2/_paket_v2.py

For every installed figN_<kok>: the Visio draft yapim/z_<kok>.vsdx (only if the build PDF beside it is
byte-identical to the installed PDF, i.e. the draft is the drawing of the printed figure), the installed figure
manifest (.fig.json) and evidence file (.kanit.json). Writes SHA256SUMS.txt and an English README.md and lists
the author fields of the .vsdx document properties (double-blind review). The original package
paper/submission/Drawing_drafts is not touched.
"""
import hashlib
import io
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PKG = ROOT / "paper" / "submission" / "Drawing_drafts_v2"
TITLE = ("Less a Weak Source than a Different One: Vulnerability, Similarity and Direction in CNN-ViT Adversarial "
         "Transfer under an Architecture-by-Initialization Design")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    if PKG.exists():
        shutil.rmtree(PKG)
    (PKG / "visio").mkdir(parents=True)
    (PKG / "evidence").mkdir()
    rows, authors = [], {}
    figs = sorted(HERE.glob("fig*_*.pdf"), key=lambda p: int(re.match(r"fig(\d+)_", p.name).group(1)))
    for pdf in figs:
        name = pdf.stem
        n = int(re.match(r"fig(\d+)_", name).group(1))
        kok = name.split("_", 1)[1]
        bpdf = HERE / "yapim" / f"z_{kok}.pdf"
        vsdx = HERE / "yapim" / f"z_{kok}.vsdx"
        if sha(bpdf) != sha(pdf):
            sys.exit(f"{name}: build PDF differs from the installed PDF; the .vsdx is not its draft")
        dst = PKG / "visio" / f"{name}.vsdx"
        shutil.copy2(vsdx, dst)
        with zipfile.ZipFile(dst) as z:
            core = z.read("docProps/core.xml").decode("utf-8", "replace") if "docProps/core.xml" in z.namelist() else ""
        authors[name] = sorted(set(re.findall(r"<dc:creator>(.*?)</dc:creator>|<cp:lastModifiedBy>(.*?)</cp:lastModifiedBy>",
                                              core)))
        rows.append((n, f"visio/{name}.vsdx", "Visio drawing (style Z, one dimetric view)"))
        for ext, what in ((".fig.json", "figure manifest"), (".kanit.json", "evidence file (every printed number)")):
            shutil.copy2(HERE / f"{name}{ext}", PKG / "evidence" / f"{name}{ext}")
            rows.append((n, f"evidence/{name}{ext}", what))
    lines = []
    for n, rel, what in rows:
        lines.append(f"{sha(PKG / rel)}  {rel}")
    io.open(PKG / "SHA256SUMS.txt", "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    tab = "\n".join(f"| Figure {n} | {rel} | {what} | {sha(PKG / rel)} |" for n, rel, what in rows)
    readme = f"""# Drawing drafts (figure set v2)

This supplementary package holds the drawing files of the alternative figure set (v2) of the manuscript
"{TITLE}". All seventeen figures of this set were drawn in Microsoft Visio as vector drawings, shape by shape on a
0.25 mm grid, in one dimetric parallel view (depth axis 36 degrees, width axis 18 degrees); every shape was read
back from Visio by a millimetre controller before the figure was exported, and the printed PDF was measured again.
Each .vsdx file is the drawing of the printed figure of the same name: the PDF exported with it is byte-identical
to the figure placed in the manuscript. For every figure the figure manifest (.fig.json: venue, size, panels,
colours, naming, 3D records) and the evidence file (.kanit.json: every printed number with its source file and key)
are given. In the data figures a measured value is always read from a flat encoding (a position or length on a
flat face, a cell colour or a printed number); where a height also shows a value, it is a true length on the one
vertical axis and the value is printed as well. Figure 1 embeds the first four test images of CIFAR-10 and of
CIFAR-100 on its data-set cards, enlarged by pixel repetition; no image in any figure was generated or edited.
The files are the drafts as drawn; nothing was edited for this package.

| Figure | File | Content | SHA-256 |
| --- | --- | --- | --- |
{tab}

SHA256SUMS.txt lists the same digests (`sha256sum -c SHA256SUMS.txt`).
"""
    io.open(PKG / "README.md", "w", encoding="utf-8", newline="\n").write(readme)
    files = [p for p in PKG.rglob("*") if p.is_file()]
    print("files", len(files))
    print("authors", authors)


if __name__ == "__main__":
    main()
