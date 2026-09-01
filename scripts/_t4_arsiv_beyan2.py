#!/usr/bin/env python3
"""1.7 TR aynasi + kontrol noktasi boyutu duzeltmesi.

Metin "yaklasik 36 GB" diyordu; olculen deger 40 GB (du -sh models/).
Beyan edilen bir sayidir ve olculebilir, dolayisiyla olculen deger yazilir.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _t3_en_olgu import uygula  # noqa: E402

KOK = Path("/home/firat/projects/adeb_sci_1/paper")

if not uygula([
    ("main.tex",
     r"protokol karşılaştırması yeniden eğitim gerektirmeden "
     r"tekrarlanabilmektedir. Eğitilmiş kontrol noktaları yaklaşık $36$~GB "
     r"tutmaktadır",
     r"protokol karşılaştırması yeniden eğitim gerektirmeden "
     r"tekrarlanabilmektedir. Bu arşivin anonimleştirilmiş bir kopyası, "
     r"inceleme sırasında hakemlerin erişimine \texttt{[ANONYMOUS-ARCHIVE-URL]} "
     r"adresinde açıktır; böylece protokol karşılaştırması kabulden sonra "
     r"değil, kabulden önce denetlenebilir. Eğitilmiş kontrol noktaları "
     r"yaklaşık $40$~GB tutmaktadır",
     "1.7 TR hakem arsivi + 40 GB"),
], KOK / "manuscript_tr"):
    sys.exit(1)

if not uygula([
    ("main.tex",
     r"Trained checkpoints total about $36$~GB",
     r"Trained checkpoints total about $40$~GB",
     "40 GB EN"),
], KOK / "manuscript"):
    sys.exit(1)

# gonderim belgeleri de ayni sayiyi tasiyor
if not uygula([
    ("declarations.txt",
     "Trained checkpoints total\nabout 36 GB and are available from the authors on reasonable request.",
     "Trained checkpoints total\nabout 40 GB and are available from the authors on reasonable request.",
     "40 GB beyanlar"),
], KOK / "submission"):
    sys.exit(1)
