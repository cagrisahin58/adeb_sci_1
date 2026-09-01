#!/usr/bin/env bash
# IEEE Access sablonunu depoya kurar (sinif + fontlar), ornek/demo dosyalari
# HARIC. IEEE Access sayfasi acikca kendi sablonunu ZORUNLU tutuyor:
#   "The article must be submitted (i) using one of the following IEEE Access
#    templates, submitted as a Word or LaTeX file and (ii) as a PDF file."
# Kaynak: https://ieeeaccess.ieee.org/authors/preparing-your-article/
set -eu
SRC=/tmp/accesstpl/ACCESS_latex_template_20260513
DST=/home/firat/projects/adeb_sci_1/paper/manuscript/ieeeaccess

[ -d "$SRC" ] || { echo "sablon bulunamadi: $SRC"; exit 1; }
mkdir -p "$DST"

# sinif + font/destek dosyalari + logo (kapak bandi icin gerekli)
for f in "$SRC"/*.cls "$SRC"/*.tfm "$SRC"/*.pfb "$SRC"/*.map "$SRC"/*.vf \
         "$SRC"/*.enc "$SRC"/*.bst; do
    [ -e "$f" ] && cp -n "$f" "$DST"/ 2>/dev/null || true
done
for g in logo.png notaglinelogo.png; do
    [ -e "$SRC/$g" ] && cp -n "$SRC/$g" "$DST"/ || true
done

echo "kurulan dosya: $(ls "$DST" | wc -l)"
echo "boyut        : $(du -sh "$DST" | cut -f1)"
ls "$DST" | grep -E '\.(cls|bst)$' | sed 's/^/  /'
