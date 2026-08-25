#!/usr/bin/env bash
set -u
cd /home/firat/projects/adeb_sci_1 || exit 1
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
cp -r paper "$T/paper"
echo "=== bozulmamis metin kopyasi, gercek artefaktlar ==="
MANUSCRIPT_ROOT="$T" python3 scripts/check_manuscript_claims.py 2>&1 | grep -E "KALDI|TOPLAM"
