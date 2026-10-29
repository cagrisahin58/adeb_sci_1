import numpy as np, glob, os
for d in ["results/q1/havuz_cifar10", "results/c1_c3/pair1", "results/q1/son_kontrol_noktasi/pair1", "results/q1/cifar100/transfer/pair1"]:
    fs = sorted(glob.glob(os.path.join(d, "per_sample_*.npz")))
    z = np.load(fs[0])
    print(d, len(fs), os.path.basename(fs[0]), {k: (z[k].shape, str(z[k].dtype)) for k in z.files})
