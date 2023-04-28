import os
import ROOT
from z_boson import analysis
from collection_comparison import comparison


# if name = main

if __name__ == "__main__":
    path = "/gpfs/ddn/cms/user/cattafe/FlashSim/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root"
    save_path = os.path.join(os.path.dirname(__file__), "figures", "EEM_90")

    ROOT.EnableImplicitMT()

    df_flash = ROOT.RDataFrame("Events", path)
    df_full = ROOT.RDataFrame("FullSim", path)

    c_pt = comparison(df_full, df_flash, "Electron_pt", [0, 100], 100)
    c_pt.SaveAs(os.path.join(save_path, "Electron_pt.pdf"))

    # Z boson

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

    for i, (cut, label) in enumerate(zip(cuts, labels)):
        filename = f"z_{i}_bin.pdf"
        c_z = analysis(df_full, df_flash, cut, label)
        c_z.SaveAs(os.path.join(save_path, filename))