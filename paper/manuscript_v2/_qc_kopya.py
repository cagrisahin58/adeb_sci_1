"""QC reading copy of main_v2.tex: \InputIfFileExists{X}{}{} -> \input{X}, so the flattener sees the appendix."""
import io
from pathlib import Path
h = Path(__file__).resolve().parent
t = (h / "main_v2.tex").read_text(encoding="utf-8")
for s in ("sections/04z_computational", "sections/07_appendix"):
    t = t.replace("\InputIfFileExists{" + s + "}{}{}", "\input{" + s + "}")
io.open(h / "_main_v2_qc.tex", "w", encoding="utf-8", newline="\n").write(t)
print(t.count("InputIfFileExists"))
