#!/bin/bash
cd /home/firat/projects/adeb_sci_1
O=raporlar/konsey_2026-10-29/_ek_denetim
docker exec -u 1000:1000 -w /workspace -e HOME=/tmp -e CUDA_VISIBLE_DEVICES= -e OMP_NUM_THREADS=2 -e PYTHONDONTWRITEBYTECODE=1 adeb_eval nice -n 10 python -m pytest -v -o addopts= -p no:cacheprovider tests/test_q1_ek.py > $O/d3_pytest.txt 2>&1
echo "pytest rc=$?"
tail -30 $O/d3_pytest.txt
echo "== ek_regresyon icerik =="
ls -la results/q1/ek_regresyon/
find results/q1/ek_regresyon -maxdepth 2 -name 'karsilastirma_*.json' -o -maxdepth 2 -name '*.txt' | head
