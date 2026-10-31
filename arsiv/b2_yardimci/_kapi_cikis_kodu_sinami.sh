#!/usr/bin/env bash
# docker exec cikis kodunu tasiyor mu? (sayi kapisi ucuncu tur, 2026-10-31; wsl.exe uzerinden $? acilmasin diye dosyada)
docker exec adeb_eval false; echo "false_rc=$?"
docker exec adeb_eval sh -c "exit 3"; echo "exit3_rc=$?"
docker exec -w /workspace adeb_eval python -B -c "import sys; sys.exit(1)"; echo "py_rc=$?"
