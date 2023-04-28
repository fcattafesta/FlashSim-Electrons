import os
import ROOT
from z_boson import analysis
from collection_comparison import comparison

ROOT.gInterpreter.ProcessLine('#include "match.h"')


if __name__ == "__main__":
    path = "/gpfs/ddn/cms/user/cattafe/FlashSim/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root"
    save_path = os.path.join(os.path.dirname(__file__), "figures", "EEM_90")

    ROOT.EnableImplicitMT()

    file = ROOT.TFile.Open(path)

    events = file.Events
    full = file.FullSim

    events.AddFriend(full, "FullSim")

    rdf = ROOT.RDataFrame(events)

    rdf = (
        rdf.Define(
            "GenPart_ElectronIdx",
            "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, FullSim.Electron_pt, FullSim.Electron_eta, FullSim.Electron_phi, FullSim.Electron_charge)",
        )
        .Define("MatchedIdx", "GenPart_ElectronIdx[GenPart_ElectronIdx >= 0]")
        .Define("MElectron_pt", "Take(FullSim.Electron_pt, MatchedIdx)")
    )

    c_pt = comparison(rdf, "Electron_pt", [0, 100], 100)
    c_pt.SaveAs(os.path.join(save_path, "Electron_pt.pdf"))

    # Z boson

    # cuts = [
    #     "Z_pt < 50",
    #     "Z_pt >= 50 && Z_pt < 100",
    #     "Z_pt >= 100 && Z_pt < 150",
    #     "Z_pt >= 150",
    #     "1",
    # ]

    # labels = [
    #     "p^{Z}_{T} < 50",
    #     "50 #leq p^{Z}_{T} < 100",
    #     "100 #leq p^{Z}_{T} < 150",
    #     "p^{Z}_{T} #geq 150",
    #     "",
    # ]

    # df_full = ROOT.RDataFrame(full)

    # for i, (cut, label) in enumerate(zip(cuts, labels)):
    #     filename = f"z_{i}_bin.pdf"
    #     c_z = analysis(df_full, rdf, cut, label)
    #     c_z.SaveAs(os.path.join(save_path, filename))
