#!/usr/bin/env bash
# ieeeaccess.cls'in kendi cizdigi gorselleri (logo, bullet vb.) depoya alir.
set -u
SRC=/tmp/accesstpl/ACCESS_latex_template_20260513
DST=/home/firat/projects/adeb_sci_1/paper/manuscript
cd "$DST" || exit 1
for f in bullet.png jtehmLogo.png logo.png notaglinelogo.png; do
    if [ ! -f "$f" ]; then
        if [ -f "$SRC/$f" ]; then cp "$SRC/$f" . && echo "  + $f"
        else echo "  ! $f sablonda yok"; fi
    else
        echo "  = $f zaten var"
    fi
done
