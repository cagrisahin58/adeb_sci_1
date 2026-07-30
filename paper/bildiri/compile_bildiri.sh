#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
# Betigin bulundugu dizin: makine bagimsiz (host / docker farketmez)
cd "$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")" || exit 1
latexmk -pdf -interaction=nonstopmode bildiri.tex >/tmp/bildiri_lm.log 2>&1
echo "LATEXMK_EXIT=$?"
echo "undefined=$(grep -ac 'undefined' bildiri.log)"
echo "overfull=$(grep -ac 'Overfull' bildiri.log)"
grep -a "LaTeX Warning: Citation" bildiri.log | head -3
python3 - <<'EOF'
import re
log = open('bildiri.log', encoding='utf-8', errors='ignore').read()
pages = re.findall(r'Output written on bildiri.pdf \((\d+) page', log)
print(f"SAYFA={pages[-1] if pages else '?'}")
EOF
