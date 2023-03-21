import ROOT

# ROOT.gInterpreter.ProcessLine('#include "z_func.h"')
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

filenames = [f"figures/z_boson_{i}bin.pdf" for i in range(1, len(cuts))]
filenames.append(f"figures/z_boson_all.pdf")

ROOT.pt_bias()

# for cut, label, filename in zip(cuts, labels, filenames):
#     ROOT.z_boson(cut, label, filename)
