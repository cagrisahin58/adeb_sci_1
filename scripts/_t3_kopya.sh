#!/usr/bin/env bash
# Teslim ciktilarini scratchpad'e kopyalar (SendUserFile UNC yolu kabul etmiyor).
set -eu
D="/mnt/c/Users/cagri/AppData/Local/Temp/claude/--wsl-localhost-Ubuntu-22-04-home-firat-projects-adeb-sci-1/0d0fab82-c6b8-472d-a420-d8ffb5857ab2/scratchpad"
cd /home/firat/projects/adeb_sci_1
cp paper/manuscript/main.pdf      "$D/makale_EN_rev3.pdf"
cp paper/manuscript_tr/main.pdf   "$D/makale_TR_rev3.pdf"
cp results/q1_research/HAKEM_TURU3_DEFTER.md "$D/HAKEM_TURU3_DEFTER.md"
ls -la "$D" | tail -4
