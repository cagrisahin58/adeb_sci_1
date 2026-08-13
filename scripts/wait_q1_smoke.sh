#!/bin/bash
# q1 smoke testinin bitmesini bekler, hukum satirlarini basar.
LOGF="$HOME/projects/adeb_sci_1/logs/q1_smoke.log"
for i in $(seq 1 80); do
  grep -q 'TOPLAM:' "$LOGF" 2>/dev/null && break
  docker exec adeb_eval pgrep -f q1_smoke_test >/dev/null 2>&1 || break
  sleep 15
done
grep -E 'PASS|FAIL|TOPLAM' "$LOGF"
