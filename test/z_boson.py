import ROOT

ROOT.gROOT.ProcessLine('#include "z_func.h"')

cuts = [
    "z_pt < 50",
    "z_pt >= 50 && z_pt < 100",
    "z_pt >= 100 && z_pt < 150",
    "z_pt >= 150",
]

labels = [
    "p^{Z}_{T} < 50",
    "50 \le p^{Z}_{T} < 100",
    "100 \le p_{T} < 150",
    " p_{T} \ge 150",
]

filenames = [f"figures/z_boson_{i}bin.pdf" for i in range(1, len(cuts) + 1)]

for cut, label, filename in zip(cuts, labels, filenames):
    ROOT.z_func(cut, label, filename)