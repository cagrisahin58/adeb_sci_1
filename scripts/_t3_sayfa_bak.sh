#!/usr/bin/env bash
# Son sayfalarda ne var? (metin / yalniz yuzen nesne / bos)
cd /home/firat/projects/adeb_sci_1/paper/manuscript || exit 1
N=$(pdfinfo main.pdf | awk '/^Pages/{print $2}')
echo "toplam $N sayfa"
for p in $((N-2)) $((N-1)) "$N"; do
    k=$(pdftotext -f "$p" -l "$p" main.pdf - 2>/dev/null | tr -s '[:space:]' ' ' | wc -w)
    echo "--- sayfa $p : $k kelime"
    pdftotext -f "$p" -l "$p" main.pdf - 2>/dev/null | tr -s '\n' ' ' | cut -c1-260
    echo
done
