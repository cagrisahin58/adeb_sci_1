#!/usr/bin/env python3
"""Ardisik YINELENEN cumleyi tekillestirir (EN 2x, TR 3x).

Neden: tur 4'teki "0.3 birincil tahmin beyani" yamasinda eski metin yeni
metnin ONEKIYDI; betik yeniden kosuldugunda 'eski in t' yine dogru oldu ve
cumle bir daha eklendi (TR'de iki kez). Idempotentlik dersi: yeni metin
eskisini ICERIYORSA imza kontrolu yeni metnin TAMAMINA bakmali.
"""
import io
import re
import sys
from pathlib import Path

KOK = Path("/home/firat/projects/adeb_sci_1/paper")
HEDEF = [
    (KOK / "manuscript/sections/03_methodology.tex",
     r"For directional claims we take the both-correct rate as the primary estimate, "
     r"because it scores both directions on identical samples and therefore supports "
     r"paired inference; the other three are reported beside it throughout\."),
    (KOK / "manuscript_tr/sections/03_yontem.tex",
     r"Yönlü iddialar için birincil tahmin olarak her ikisi doğru oranını alıyoruz, "
     r"çünkü iki yönü de aynı örnekler üzerinde puanlar ve bu yüzden eşleştirilmiş "
     r"çıkarımı destekler; diğer üçü baştan sona onun yanında raporlanır\."),
]
for yol, cumle in HEDEF:
    t = yol.read_text(encoding="utf-8")
    once = len(re.findall(cumle, t))
    # ayni cumlenin bosluk/yeni satirla ayrilmis ardisik tekrarlarini tek biraka indir
    t2, n = re.subn(r"(" + cumle + r")(\s+" + cumle + r")+", r"\1", t)
    sonra = len(re.findall(cumle, t2))
    if n:
        io.open(yol, "w", encoding="utf-8", newline="\n").write(t2)
    print(f"{yol.name}: {once} -> {sonra} ({'yazildi' if n else 'degisiklik yok'})")
    if sonra != 1:
        print("  UYARI: hala 1 degil; ardisik olmayan tekrar olabilir")
        sys.exit(1)
