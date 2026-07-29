#!/bin/bash
# Host sarmalayicisi: konteyneri ayaga kaldirip kurtarmayi KONTEYNER ICINDE kosar.
docker start adeb_eval >/dev/null 2>&1 || true
sleep 3
exec docker exec adeb_eval bash /workspace/scripts/c1_resume_inner.sh
