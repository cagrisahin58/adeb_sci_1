"""Celisik dogrulayici, D2 sarmalayicisi: verilen matris betigini runpy ile
calistirir, sonda hangi `src` paketinin yuklendigini basar (eski kodun
gercekten eski src ile kostugunu gostermek icin).

Kullanim: python d2_calistir.py BETIK [betik argumanlari ...]
"""
import runpy
import sys

betik = sys.argv[1]
sys.argv = [betik] + sys.argv[2:]
try:
    runpy.run_path(betik, run_name="__main__")
finally:
    src = sys.modules.get("src")
    print("SRC_PAKETI", getattr(src, "__file__", None))
    mm = sys.modules.get("src.models")
    print("R224_YUKLU", "src.models.r224" in sys.modules)
