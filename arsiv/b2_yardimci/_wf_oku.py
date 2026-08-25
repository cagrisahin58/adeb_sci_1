#!/usr/bin/env python3
"""Calisan denetim akisinin bulgularini ozetler."""
import json
from pathlib import Path

J = Path("/mnt/c/Users/cagri/.claude/projects/"
         "--wsl-localhost-Ubuntu-22-04-home-firat-projects-adeb-sci-1/"
         "0d0fab82-c6b8-472d-a420-d8ffb5857ab2/subagents/workflows/"
         "wf_86262297-186/journal.jsonl")

n = 0
for satir in J.read_text(encoding="utf-8", errors="replace").splitlines():
    try:
        d = json.loads(satir)
    except Exception:
        continue
    n += 1
    etiket = d.get("label") or d.get("agentLabel") or "?"
    r = d.get("result")
    if isinstance(r, str):
        try:
            r = json.loads(r)
        except Exception:
            pass
    if isinstance(r, dict) and "bulgular" in r:
        b = r["bulgular"]
        print(f"\n===== {etiket}: {len(b)} bulgu =====")
        for x in b:
            print(f"  [{x.get('agirlik'):7s}] {x.get('baslik')}")
            print(f"      dosya  : {x.get('dosya')}:{x.get('satir', '')}")
            print(f"      iddia  : {str(x.get('iddia'))[:150]}")
            print(f"      olculen: {str(x.get('olculen'))[:150]}")
    elif isinstance(r, dict):
        print(f"\n===== {etiket} =====")
        print(json.dumps(r, ensure_ascii=False)[:400])
print(f"\ntoplam kayit: {n}")
