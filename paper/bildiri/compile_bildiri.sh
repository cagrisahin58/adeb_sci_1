#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
cd "$HOME/projects/adeb_sci_1/paper/bildiri" || exit 1
latexmk -pdf -interaction=nonstopmode bildiri.tex >/tmp/bildiri_lm.log 2>&1
echo "LATEXMK_EXIT=$?"
echo "undefined=$(grep -c 'undefined' bildiri.log)"
echo "overfull=$(grep -c 'Overfull' bildiri.log)"
grep "LaTeX Warning: Citation" bildiri.log | head -3
python3 - <<'EOF'
import re
log = open('bildiri.log', encoding='utf-8', errors='ignore').read()
pages = re.findall(r'Output written on bildiri.pdf \((\d+) page', log)
print(f"SAYFA={pages[-1] if pages else '?'}")
EOF
