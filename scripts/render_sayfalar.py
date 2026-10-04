"""Makale PDF'ini ve sekil PDF'lerini PNG'ye rasterize eder (gorsel denetim icin).
Konteynerde kosulur:  docker exec -w /workspace adeb_eval python scripts/render_sayfalar.py [cikti_klasoru]
Oncelik: PyMuPDF (fitz); yoksa pdftoppm; o da yoksa pdf2image.
Cikti: <cikti>/sayfa_XX.png (110 dpi), <cikti>/sekil/<ad>.png (200 dpi), <cikti>/INDEKS.md
"""
import io
import os
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "teslim" / "render_2026-10-04"
(OUT / "sekil").mkdir(parents=True, exist_ok=True)
MAIN = ROOT / "paper" / "manuscript" / "main.pdf"
FIGS = sorted((ROOT / "paper" / "figures" / "final").glob("*.pdf"))


def render_fitz(pdf, out_prefix, dpi):
    import fitz  # type: ignore
    doc = fitz.open(str(pdf))
    paths = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=dpi)
        p = f"{out_prefix}_{i:02d}.png" if len(doc) > 1 else f"{out_prefix}.png"
        pix.save(p)
        paths.append(p)
    return paths


def render_pdftoppm(pdf, out_prefix, dpi):
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), out_prefix], check=True)
    return sorted(str(p) for p in Path(out_prefix).parent.glob(Path(out_prefix).name + "*.png"))


def render(pdf, out_prefix, dpi):
    try:
        return render_fitz(pdf, out_prefix, dpi), "pymupdf"
    except ImportError:
        pass
    try:
        return render_pdftoppm(pdf, out_prefix, dpi), "pdftoppm"
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass
    from pdf2image import convert_from_path  # type: ignore
    paths = []
    for i, im in enumerate(convert_from_path(str(pdf), dpi=dpi), 1):
        p = f"{out_prefix}_{i:02d}.png"
        im.save(p)
        paths.append(p)
    return paths, "pdf2image"


sayfalar, arac = render(MAIN, str(OUT / "sayfa"), 110)
print(f"{arac}: {len(sayfalar)} sayfa -> {OUT}")
sekiller = []
for f in FIGS:
    ps, _ = render(f, str(OUT / "sekil" / f.stem), 200)
    sekiller.extend(ps)
print(f"{len(sekiller)} sekil PNG")

# Etiket -> sayfa haritasi (main.aux)
aux = ROOT / "paper" / "manuscript" / "main.aux"
harita = []
if aux.exists():
    for m in re.finditer(r"\\newlabel\{((?:tab|fig|eq|sec|subsec):[^}]*)\}\{\{([^}]*)\}\{(\d+)\}", aux.read_text(encoding="utf-8", errors="ignore")):
        harita.append((m.group(1), m.group(2), int(m.group(3))))
with io.open(OUT / "INDEKS.md", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(f"# Render indeksi\n\nKaynak: {MAIN} ({len(sayfalar)} sayfa, 110 dpi); sekiller 200 dpi.\n\n")
    fh.write("| etiket | numara | sayfa | PNG |\n|---|---|---|---|\n")
    for et, num, sf in sorted(harita, key=lambda x: (x[2], x[0])):
        fh.write(f"| {et} | {num} | {sf} | sayfa_{sf:02d}.png |\n")
    fh.write("\n## Sekil dosyalari\n\n")
    for p in sekiller:
        fh.write(f"- {Path(p).name}\n")
print("INDEKS.md yazildi; etiket sayisi", len(harita))
