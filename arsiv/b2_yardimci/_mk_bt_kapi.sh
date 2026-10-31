#!/usr/bin/env bash
# Butunlestirici: kapilar (salt okur). Derlemeden SONRA kosulur.
cd /home/firat/projects/adeb_sci_1 || exit 1
echo "=== compile_check"
bash scripts/compile_check.sh 2>&1 | tail -15
echo "=== check_manuscript_claims"
docker exec -w /workspace adeb_eval python scripts/check_manuscript_claims.py 2>&1 | grep -v ' GECTI' | tail -30
echo "=== check_abstract_body"
docker exec -w /workspace adeb_eval python scripts/check_abstract_body.py 2>&1 | tail -15
echo "=== verify_manuscript_numbers"
docker exec -w /workspace adeb_eval python scripts/verify_manuscript_numbers.py > /tmp/bt_vmn.txt 2>&1; echo "rc=$?"
tail -40 /tmp/bt_vmn.txt
echo "=== kapilar.sh"
bash scripts/kapilar.sh > /tmp/bt_kapilar.txt 2>&1; echo "rc=$?"
grep -iE 'GECTI|KALDI|EKSIK|HATA|FAIL|PASS|OK|sonuc|ozet' /tmp/bt_kapilar.txt | tail -40
