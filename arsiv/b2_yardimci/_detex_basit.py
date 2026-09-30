"""LaTeX bolum dosyasini duz metne indirger (detex yoksa yedek).
Kullanim: python3 _detex_basit.py girdi.tex cikti.txt
Yorum satirlari, tablo/sekil/denklem ortamlari, \\cite/\\ref/\\label komutlari atilir;
\\emph{...} icerigi korunur; matematik $...$ 'M' ile degistirilir (cumle sayimi bozulmasin).
"""
import io
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
text = io.open(src, encoding="utf-8").read()

# yorumlar
text = re.sub(r"(?m)^%.*\n", "", text)
text = re.sub(r"(?<!\\)%.*", "", text)
# kayan ortamlar ve denklemler
for env in ("table", "table*", "figure", "figure*", "equation", "equation*", "align", "align*", "tabular", "abstract"):
    e = re.escape(env)
    if env == "abstract":
        continue
    text = re.sub(r"\\begin\{" + e + r"\}.*?\\end\{" + e + r"\}", " ", text, flags=re.S)
# baslik komutlari: icerigi tut
text = re.sub(r"\\(section|subsection|subsubsection|paragraph)\*?\{([^}]*)\}", r"\n\n\2\n\n", text)
# atif, gonderme, etiket
text = re.sub(r"~?\\(cite|ref|eqref|label|autoref)\{[^}]*\}", "", text)
# vurgu ve font komutlari: icerik kalsin
text = re.sub(r"\\(emph|textbf|textit|texttt|mbox)\{([^{}]*)\}", r"\2", text)
# satir ici matematik
text = re.sub(r"\$[^$]*\$", "M", text)
# kalan komutlar
text = re.sub(r"\\[A-Za-z@]+\*?(\[[^\]]*\])?", "", text)
text = text.replace("~", " ").replace("``", '"').replace("''", '"')
text = re.sub(r"[{}]", "", text)
text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n{3,}", "\n\n", text)
io.open(dst, "w", encoding="utf-8", newline="\n").write(text.strip() + "\n")
