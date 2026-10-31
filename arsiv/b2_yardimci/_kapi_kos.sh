#!/usr/bin/env bash
# Oz-sinama ve sayi kapisini kosar, cikis kodlarini acikca basar (2026-10-31).
cd /home/firat/projects/adeb_sci_1 || exit 2
docker exec -w /workspace adeb_eval python -B scripts/test_verify_manuscript_numbers.py
echo "OZ_SINAMA_CIKIS=$?"
docker exec -w /workspace adeb_eval python -B scripts/verify_manuscript_numbers.py > /tmp/vmn_kapi.log 2>&1
echo "KAPI_CIKIS=$?"
