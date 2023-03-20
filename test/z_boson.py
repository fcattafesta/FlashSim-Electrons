import ROOT

ROOT.gROOT.ProcessLine('#include "z_func.h"')

cuts = [
    "Z_pt < 50",
    "Z_pt >= 50 && Z_pt < 100",
    "Z_pt >= 100 && Z_pt < 150",
    "Z_pt >= 150",
]

labels = [
    "p^{Z}_{T} < 50",
    "50 #le p^{Z}_{T} < 100",
    "100 #le p^{Z}_{T} < 150",
    "p^{Z}_{T} #ge 150",
]

filenames = [f"figures/z_boson_{i}bin.pdf" for i in range(1, len(cuts) + 1)]

for cut, label, filename in zip(cuts, labels, filenames):
    ROOT.z_boson(cut, label, filename)
