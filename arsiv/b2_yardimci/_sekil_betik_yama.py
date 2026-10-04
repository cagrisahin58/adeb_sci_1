"""Render denetimi (2026-10-04): scripts/generate_journal_figs_c1.py icin sekil iyilestirmeleri.
- fig4 (gradyan buyukluk haritalari): paylasilan renk cubugu (haritalar zaten ornek basina maksimuma
  normalize), satir etiketleri 9 pt.
- fig5maps (dikkat haritalari): her satir kendi maksimumuna olceklenir, iki paylasilan renk cubugu
  (dikkat 0-1, fark -1..1), sutun basliklari 9 pt. Baslik metni (EN/TR) ayrica guncellenir.
Her eski dize TAM BIR kez gecmeli. Kullanim (depo kokunden): python3 arsiv/b2_yardimci/_sekil_betik_yama.py
"""
import io
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "scripts" / "generate_journal_figs_c1.py"

PATCHES = [
    # ---- fig4: gradyan haritalari ----
    (
        "    imgs, gr, gv = first\n"
        "    fig, axes = plt.subplots(3, 4, figsize=(5.4, 4.2))\n"
        "    for k in range(4):\n"
        "        axes[0, k].imshow(imgs[k].permute(1, 2, 0).numpy(), interpolation=\"nearest\")\n"
        "        for r, g, color in ((1, gr, \"CNN\"), (2, gv, \"ViT\")):\n"
        "            e = (g[k] ** 2).sum(0).numpy()\n"
        "            e = e / (e.max() + 1e-12)\n"
        "            axes[r, k].imshow(e, cmap=\"inferno\", interpolation=\"nearest\")\n"
        "        for r in range(3):\n"
        "            axes[r, k].set_xticks([])\n"
        "            axes[r, k].set_yticks([])\n"
        "    for r, lab in enumerate([L[\"input\"], \"ResNet-18 (AT)\", \"ViT-Tiny (AT)\"]):\n"
        "        axes[r, 0].set_ylabel(lab, fontsize=8)\n"
        "    fig.tight_layout()\n",
        "    imgs, gr, gv = first\n"
        "    fig, axes = plt.subplots(3, 4, figsize=(5.4, 4.2))\n"
        "    im = None\n"
        "    for k in range(4):\n"
        "        axes[0, k].imshow(imgs[k].permute(1, 2, 0).numpy(), interpolation=\"nearest\")\n"
        "        for r, g, color in ((1, gr, \"CNN\"), (2, gv, \"ViT\")):\n"
        "            e = (g[k] ** 2).sum(0).numpy()\n"
        "            e = e / (e.max() + 1e-12)\n"
        "            im = axes[r, k].imshow(e, cmap=\"inferno\", interpolation=\"nearest\", vmin=0, vmax=1)\n"
        "        for r in range(3):\n"
        "            axes[r, k].set_xticks([])\n"
        "            axes[r, k].set_yticks([])\n"
        "    for r, lab in enumerate([L[\"input\"], \"ResNet-18 (AT)\", \"ViT-Tiny (AT)\"]):\n"
        "        axes[r, 0].set_ylabel(lab, fontsize=9)\n"
        "    fig.tight_layout(rect=(0, 0, 0.92, 1))\n"
        "    # 2026-10-04: paylasilan renk cubugu (her harita ornek basina maksimumuna normalize)\n"
        "    cax = fig.add_axes([0.93, 0.08, 0.018, 0.56])\n"
        "    cb = fig.colorbar(im, cax=cax)\n"
        "    cb.set_label(L[\"grad_cbar\"], fontsize=8)\n"
        "    cb.ax.tick_params(labelsize=7)\n",
    ),
    # ---- fig5maps: dikkat haritalari ----
    (
        "    layers = [0, 5, 11]\n"
        "    fig, axes = plt.subplots(len(layers), 3, figsize=(4.6, 4.4))\n"
        "    for r, l in enumerate(layers):\n"
        "        d = am[l] - cm[l]\n"
        "        vmax = max(cm[l].max(), am[l].max())\n"
        "        for c, (arr, title, kw) in enumerate([\n"
        "            (cm[l], L[\"att_clean\"], {\"cmap\": \"viridis\", \"vmin\": 0, \"vmax\": vmax}),\n"
        "            (am[l], L[\"att_adv\"], {\"cmap\": \"viridis\", \"vmin\": 0, \"vmax\": vmax}),\n"
        "            (d, L[\"att_diff\"], {\"cmap\": \"coolwarm\", \"vmin\": -np.abs(d).max(), \"vmax\": np.abs(d).max()}),\n"
        "        ]):\n"
        "            axes[r, c].imshow(arr, interpolation=\"nearest\", **kw)\n"
        "            if r == 0:\n"
        "                axes[r, c].set_title(title, fontsize=8)\n"
        "            axes[r, c].set_xticks([])\n"
        "            axes[r, c].set_yticks([])\n"
        "        axes[r, 0].set_ylabel(f\"{L['block']} {l + 1}\", fontsize=8)\n"
        "    fig.tight_layout()\n"
        "    fig.savefig(OUT / \"fig5_attention_comparison.pdf\")\n",
        "    layers = [0, 5, 11]\n"
        "    fig, axes = plt.subplots(len(layers), 3, figsize=(5.0, 4.4))\n"
        "    im_att = im_dif = None\n"
        "    for r, l in enumerate(layers):\n"
        "        d = am[l] - cm[l]\n"
        "        # 2026-10-04: her satir kendi maksimumuna olceklenir, boylece iki paylasilan\n"
        "        # renk cubugu yeter (dikkat 0..1, fark -1..1). Baslik metni bunu soyler.\n"
        "        vmax = max(cm[l].max(), am[l].max()) + 1e-12\n"
        "        dmax = np.abs(d).max() + 1e-12\n"
        "        for c, (arr, title, kw) in enumerate([\n"
        "            (cm[l] / vmax, L[\"att_clean\"], {\"cmap\": \"viridis\", \"vmin\": 0, \"vmax\": 1}),\n"
        "            (am[l] / vmax, L[\"att_adv\"], {\"cmap\": \"viridis\", \"vmin\": 0, \"vmax\": 1}),\n"
        "            (d / dmax, L[\"att_diff\"], {\"cmap\": \"coolwarm\", \"vmin\": -1, \"vmax\": 1}),\n"
        "        ]):\n"
        "            h = axes[r, c].imshow(arr, interpolation=\"nearest\", **kw)\n"
        "            if c < 2:\n"
        "                im_att = h\n"
        "            else:\n"
        "                im_dif = h\n"
        "            if r == 0:\n"
        "                axes[r, c].set_title(title, fontsize=9)\n"
        "            axes[r, c].set_xticks([])\n"
        "            axes[r, c].set_yticks([])\n"
        "        axes[r, 0].set_ylabel(f\"{L['block']} {l + 1}\", fontsize=9)\n"
        "    fig.tight_layout(rect=(0, 0, 0.88, 1))\n"
        "    cax1 = fig.add_axes([0.895, 0.53, 0.02, 0.38])\n"
        "    cb1 = fig.colorbar(im_att, cax=cax1)\n"
        "    cb1.set_label(L[\"att_cbar\"], fontsize=8)\n"
        "    cb1.ax.tick_params(labelsize=7)\n"
        "    cax2 = fig.add_axes([0.895, 0.07, 0.02, 0.38])\n"
        "    cb2 = fig.colorbar(im_dif, cax=cax2)\n"
        "    cb2.set_label(L[\"diff_cbar\"], fontsize=8)\n"
        "    cb2.ax.tick_params(labelsize=7)\n"
        "    fig.savefig(OUT / \"fig5_attention_comparison.pdf\")\n",
    ),
    # ---- etiket sozlukleri (EN ve TR) ----
    (
        "        \"att_clean\": \"clean\", \"att_adv\": \"adversarial\", \"att_diff\": \"difference\",\n",
        "        \"att_clean\": \"clean\", \"att_adv\": \"adversarial\", \"att_diff\": \"difference\",\n"
        "        \"att_cbar\": \"attention / row max\", \"diff_cbar\": r\"difference / row max $|\\Delta|$\",\n"
        "        \"grad_cbar\": \"gradient energy / sample max\",\n",
    ),
    (
        "        \"att_clean\": \"temiz\", \"att_adv\": \"çekişmeli\", \"att_diff\": \"fark\",\n",
        "        \"att_clean\": \"temiz\", \"att_adv\": \"çekişmeli\", \"att_diff\": \"fark\",\n"
        "        \"att_cbar\": \"dikkat / satır maks.\", \"diff_cbar\": r\"fark / satır maks. $|\\Delta|$\",\n"
        "        \"grad_cbar\": \"gradyan enerjisi / örnek maks.\",\n",
    ),
]


def main():
    text = io.open(P, encoding="utf-8").read()
    new_text = text
    hata = 0
    for i, (old, new) in enumerate(PATCHES, 1):
        n = new_text.count(old)
        if n == 1:
            new_text = new_text.replace(old, new)
            print(f"OK    #{i}")
        elif n == 0 and new_text.count(new) == 1:
            print(f"ZATEN #{i}")
        else:
            print(f"HATA  #{i}: eski dize {n} kez gecti")
            hata += 1
    if hata:
        print("yazilmadi")
        sys.exit(1)
    io.open(P, "w", encoding="utf-8", newline="\n").write(new_text)
    print("Sekil betigi yamalari tamam.")


if __name__ == "__main__":
    main()
