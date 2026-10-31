#!/usr/bin/env bash
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
F="main.tex sections/*.tex"
yorumsuz() { for f in $F; do sed 's/\([^\\]\)%.*$/\1/; s/^%.*$//' "$f" | awk -v f="$f" '{print f":"NR":"$0}'; done; }
yorumsuz > /tmp/bt_metin.txt
echo "=== source effect / weak source"
grep -inE 'source[- ]effect|weak(er)? source|source side decides|fixed third model' /tmp/bt_metin.txt | cut -c1-260
echo "=== uzun tire / --- / paragraph / liste"
grep -nP '\x{2014}|---|\\paragraph|\\begin\{itemize|\\begin\{enumerate' /tmp/bt_metin.txt | cut -c1-160
echo "=== paragraf basi koyu/italik"
grep -nE ':[0-9]+:\\(textbf|emph|textit)\{' /tmp/bt_metin.txt | cut -c1-140
echo "=== yasakli sozcukler"
grep -inwE 'moreover|furthermore|additionally|notably|importantly|leverage[sd]?|utili[sz]e[sd]?|delve|crucial|robustly|pivotal|underscores?|novel|state-of-the-art|comprehensive' /tmp/bt_metin.txt | grep -v 'cite{[^}]*comprehensive' | cut -c1-200
grep -inE 'it is worth noting|it should be noted|shed light|pave the way|we deliberately|we are careful|to our knowledge|for the first time' /tmp/bt_metin.txt | cut -c1-200
echo "=== rather than / instead of (dosya basina)"
grep -icE 'rather than|instead of' $F
grep -inE 'rather than|instead of' /tmp/bt_metin.txt | cut -c1-220
echo "=== Ingiliz imlasi"
grep -inE 'initialis|normalis|behaviour|analys(e|ed|ing)\b|modell|colour|favour|organis|recognis|generalis|characteris' /tmp/bt_metin.txt | cut -c1-160
echo "=== eski etiketler"
for e in subsubsec:matrix subsec:source_target subsec:cifar100 subsec:svhn subsec:l2 subsubsec:spread_gap subsec:external subsec:readings subsec:gradient subsubsec:spatial subsec:attention subsec:tgr subsec:statistics_results subsec:threat_model subsec:architectures subsec:defense_methods subsec:attacks subsec:defenses subsec:cnn_robustness subsec:vit_robustness subsec:transfer_related subsec:gap fig:gradient_analysis fig:gradient_heatmap fig:attention_layers tab:conditional tab:transfer_protocols tab:transfer_matrix tab:source_target tab:cifar100_results tab:l2_results tab:tgr; do grep -n "{$e}" $F; done
echo "=== Delta_w / Delta_{w}"
grep -nE 'Delta_\{?w|Delta_w' /tmp/bt_metin.txt | cut -c1-160
echo "=== etiket gonderme denetimi"
python3 - <<'EOF'
import re, glob
fs = ["main.tex"] + sorted(glob.glob("sections/*.tex"))
txt = ""
for f in fs:
    t = open(f, encoding="utf-8").read()
    t = "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in t.split("\n"))
    txt += t
labels = re.findall(r"\\label\{([^}]+)\}", txt)
from collections import Counter
c = Counter(labels)
print("cift:", [k for k, v in c.items() if v > 1])
refs = set()
for m in re.finditer(r"\\(?:ref|eqref|pageref)\{([^}]+)\}", txt):
    for k in m.group(1).split(","):
        refs.add(k.strip())
print("gonderilmeyen:", [l for l in c if l not in refs])
print("tanimsiz:", [r for r in refs if r not in c])
cites = set()
for m in re.finditer(r"\\cite\{([^}]+)\}", txt):
    for k in m.group(1).split(","):
        cites.add(k.strip())
bib = open("references.bib", encoding="utf-8").read()
keys = set(re.findall(r"@\w+\{([^,]+),", bib))
print("bib'de olmayan cite:", sorted(cites - keys))
print("cite sayisi", len(cites), "bib girdi", len(keys))
EOF
