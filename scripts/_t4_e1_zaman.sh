#!/usr/bin/env bash
# E1 (CIFAR-100) ongorulerinin YAZILDIGI commit ne zaman?
# Makale "we predicted clean accuracy in the 33 to 40% band" diyor.
# Egitim o sirada devam ediyor muydu?
cd /home/firat/projects/adeb_sci_1 || exit 1

echo "=== '33' bandini iceren satiri EKLEYEN commit ==="
git log --format='%ai  %h  %s' -S '33' --pickaxe-regex \
    -- results/q1_research/E1_PILOT_KAPISI.md | tail -3
echo
echo "=== E1_PILOT_KAPISI.md tum commit'leri ==="
git log --format='   %ai  %h  %s' -- results/q1_research/E1_PILOT_KAPISI.md
echo
echo "=== ongoru bandini iceren guncel satirlar ==="
grep -nE '3[0-9] *(-|ile|to) *4[0-9]|%3[0-9]|band' results/q1_research/E1_PILOT_KAPISI.md | head -8
echo
echo "=== CIFAR-100 egitim loglari (varsa) ==="
find logs -iname '*c100*' -o -iname '*cifar100*' 2>/dev/null | head -5
