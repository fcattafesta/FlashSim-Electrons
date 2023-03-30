import ROOT

ROOT.gInterpreter.ProcessLine('#include "z_func.h"')
ROOT.gInterpreter.ProcessLine('#include "comparison.h"')

cuts = [
    "Z_pt < 50",
    "Z_pt >= 50 && Z_pt < 100",
    "Z_pt >= 100 && Z_pt < 150",
    "Z_pt >= 150",
    "1",
]

labels = [
    "p^{Z}_{T} < 50",
    "50 #leq p^{Z}_{T} < 100",
    "100 #leq p^{Z}_{T} < 150",
    "p^{Z}_{T} #geq 150",
    "",
]

filenames = [f"figures/190/z_boson_{i}bin_@190_1.pdf" for i in range(1, len(cuts))]
filenames.append(f"figures/190/z_boson_all_@190_1.pdf")

ROOT.pt_bias()

for cut, label, filename in zip(cuts, labels, filenames):
     ROOT.z_boson(cut, label, filename)
