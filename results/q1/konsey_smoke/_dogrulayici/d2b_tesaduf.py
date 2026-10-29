"""D2 yan kontrol: ResNet->ViT ile WRN->ViT hucrelerinin ayni sayilari
tesaduf mu, yoksa ayni ornek dizisi mi?"""
import numpy as np

D = "results/q1/konsey_smoke/_dogrulayici/reg_yeni/"
a = np.load(D + "per_sample_ResNet18_AT_s1001_to_ViT_Tiny_AT_s2001.npz")
b = np.load(D + "per_sample_WRN_28_10_to_ViT_Tiny_AT_s2001.npz")
aw, bw = a["target_adv_wrong"], b["target_adv_wrong"]
print("toplam", int(aw.sum()), int(bw.sum()), "dizi_ayni", bool(np.array_equal(aw, bw)),
      "farkli_ornek", int((aw != bw).sum()))
c = a["target_clean_correct"]
print("kosullu", int(aw[c].sum()), int(bw[c].sum()), "n_cond", int(c.sum()))
