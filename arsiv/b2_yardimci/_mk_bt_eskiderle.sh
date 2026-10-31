#!/usr/bin/env bash
# Salt okur: HEAD surumunu /tmp/eskd'de derler, overfull parmak izini cikarir.
R=/home/firat/projects/adeb_sci_1
rm -rf /tmp/eskd; mkdir -p /tmp/eskd/manuscript/sections
ln -s $R/paper/figures /tmp/eskd/figures
cd $R
for f in $(git ls-tree -r --name-only HEAD paper/manuscript/); do
  rel=${f#paper/manuscript/}
  mkdir -p "/tmp/eskd/manuscript/$(dirname "$rel")"
  git show "HEAD:$f" > "/tmp/eskd/manuscript/$rel"
done
cp -r $R/paper/manuscript/ieeeaccess /tmp/eskd/manuscript/ 2>/dev/null
cd /tmp/eskd/manuscript
export PATH=/home/firat/.local/bin:$PATH
export TEXINPUTS="/tmp/eskd/manuscript/ieeeaccess//:"
export BSTINPUTS="/tmp/eskd/manuscript/ieeeaccess//:"
export TEXFONTS="/tmp/eskd/manuscript/ieeeaccess//:"
latexmk -pdf -interaction=nonstopmode main.tex > /tmp/eskd/latexmk.out 2>&1
echo "rc=$?"
grep -c 'Overfull \\hbox (505' main.log
grep 'Overfull' main.log | grep -v '505' | head
python3 -c "import pypdf;print('eski derleme sayfa', len(pypdf.PdfReader('main.pdf').pages))"
