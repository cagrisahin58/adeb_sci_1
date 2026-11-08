#!/usr/bin/env python
"""Build the Drawing drafts v2 package (paper/submission/Drawing_drafts_v2) from the installed v2 figures.

    python paper/figures_v2/_paket_v2.py

For every installed figN_<kok>: the Visio draft yapim/z_<kok>.vsdx (only if the build PDF beside it is
byte-identical to the installed PDF, i.e. the draft is the drawing of the printed figure), the installed figure
manifest (.fig.json) and evidence file (.kanit.json). Writes SHA256SUMS.txt and an English README.md. For
double-blind review the PACKAGE copy of every .vsdx has its document-property author fields emptied
(docProps/core.xml dc:creator and cp:lastModifiedBy; second round, 08.11.2026, bulgu 2): the zip is rewritten
member by member, every other member is byte-identical to the build draft (checked), and the build draft under
yapim/ is not changed. The author fields before and after are printed. The original package
paper/submission/Drawing_drafts is not touched.
"""
import hashlib
import io
import json
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


AUTHOR_RE = re.compile(r"(<dc:creator>)(.*?)(</dc:creator>)|(<cp:lastModifiedBy>)(.*?)(</cp:lastModifiedBy>)", re.S)


def authors_of(path):
    with zipfile.ZipFile(path) as z:
        core = z.read("docProps/core.xml").decode("utf-8") if "docProps/core.xml" in z.namelist() else ""
    return sorted({(m.group(2) if m.group(1) else m.group(5)) for m in AUTHOR_RE.finditer(core)})


def blank_authors(src, dst):
    """Copy the .vsdx zip src to dst with the two author fields of docProps/core.xml emptied; every other member
    is copied byte for byte with its own ZipInfo (name, date, compression, attributes), in the same order."""
    with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, "w") as zo:
        for info in zi.infolist():
            data = zi.read(info.filename)
            if info.filename == "docProps/core.xml":
                txt = data.decode("utf-8")
                txt = AUTHOR_RE.sub(lambda m: (m.group(1) + m.group(3)) if m.group(1) else (m.group(4) + m.group(6)),
                                    txt)
                data = txt.encode("utf-8")
            zo.writestr(info, data, compress_type=info.compress_type)
    with zipfile.ZipFile(src) as a, zipfile.ZipFile(dst) as b:
        na, nb = a.namelist(), b.namelist()
        if na != nb:
            sys.exit(f"{dst.name}: member list changed while blanking the author fields")
        for n in na:
            if n != "docProps/core.xml" and a.read(n) != b.read(n):
                sys.exit(f"{dst.name}: member {n} changed while blanking the author fields")


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
        before = authors_of(vsdx)
        blank_authors(vsdx, dst)
        after = authors_of(dst)
        if any(after):
            sys.exit(f"{name}: author fields still filled after blanking: {after}")
        authors[name] = {"draft (yapim)": before, "package": after}
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
to the figure placed in the manuscript. For double-blind review the two author fields of the document properties
(docProps/core.xml: dc:creator and cp:lastModifiedBy) were emptied in these copies; every other part of each .vsdx
is byte-identical to the draft as drawn. For every figure the figure manifest (.fig.json: venue, size, panels,
colours, naming, 3D records) and the evidence file (.kanit.json: every printed number with its source file and key)
are given. In the data figures a measured value is always read from a flat encoding (a position or length on a
flat face, a cell colour or a printed number); where a height also shows a value, it is a true length on the one
vertical axis and the value is printed as well. Figure 1 embeds the first four test images of CIFAR-10 and of
CIFAR-100 on its data-set cards, enlarged by pixel repetition; no image in any figure was generated or edited.
Apart from the emptied author fields, the files are the drafts as drawn; nothing else was edited for this
package.

| Figure | File | Content | SHA-256 |
| --- | --- | --- | --- |
{tab}

SHA256SUMS.txt lists the same digests (`sha256sum -c SHA256SUMS.txt`).
"""
    io.open(PKG / "README.md", "w", encoding="utf-8", newline="\n").write(readme)
    files = [p for p in PKG.rglob("*") if p.is_file()]
    print("files", len(files))
    print("authors", json.dumps(authors, ensure_ascii=False))


if __name__ == "__main__":
    main()
