import os
import ROOT
from z_boson import analysis
from collection_comparison import comparison, ratio

ROOT.gInterpreter.ProcessLine('#include "match.h"')


if __name__ == "__main__":
    # path = "/gpfs/ddn/cms/user/cattafe/FlashSim/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root"
    # path = "/gpfs/ddn/cms/user/cattafe/FlashSim/RunIIAutumn18NanoAODv6/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/230000/C159CB51-6BC4-E448-AD9E-59CC2A5920F5.root"
    path = "/scratchnvme/cattafe/FlashSim/RunIISummer20UL18NanoAODv9/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/230000/0CFD79EF-41AB-4B4A-8F62-06393273EEDE.root"
    save_path = os.path.join(os.path.dirname(__file__), "figures", "DYM50")

    # ROOT.EnableImplicitMT()

    file = ROOT.TFile.Open(path)

    events = file.Events

    # reset kEntriesReshuffled
    events.ResetBit(ROOT.TTree.EStatusBits.kEntriesReshuffled)

    full = file.FullSim

    full.ResetBit(ROOT.TTree.EStatusBits.kEntriesReshuffled)

    # events.AddFriend(full, "FullSim")

    # rdf = ROOT.RDataFrame(events)

    # rdf = (
    #     rdf.Define(
    #         "MGenPart_ElectronIdx",
    #         "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, FullSim.Electron_pt, FullSim.Electron_eta, FullSim.Electron_phi, FullSim.Electron_charge)",
    #     )
    #     .Define("MatchedIdx", "MGenPart_ElectronIdx[MGenPart_ElectronIdx >= 0]")
    #     .Define("MGenElectron_pt", "GenPart_pt[MGenPart_ElectronIdx >= 0]")
    #     .Define("MElectron_pt", "Take(FullSim.Electron_pt, MatchedIdx)")
    #     .Define("MRatio", "MElectron_pt / MGenElectron_pt")
    #     .Define("PGenPart_ElectronIdx", "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, Electron_pt, Electron_eta, Electron_phi, Electron_charge)")
    #     .Define("PMatchedIdx", "PGenPart_ElectronIdx[PGenPart_ElectronIdx >= 0]")
    #     .Define("PGenElectron_pt", "GenPart_pt[PGenPart_ElectronIdx >= 0]")
    #     .Define("PElectron_pt", "Take(Electron_pt, PMatchedIdx)")
    #     .Define("PRatio", "PElectron_pt / PGenElectron_pt")
    # )

    # rdf = rdf.Define("MJet_pt", "FullSim.Jet_pt[FullSim.Jet_genJetIdx >= 0]")

    # n = rdf.Histo1D("Jet_pt").GetEntries()
    # print(f"Flash: {n}")

    # n = rdf.Histo1D("FullSim.Jet_pt").GetEntries()
    # print(f"Full: {n}")

    # h_full = rdf.Histo1D(("h_full", "h_full", 100, 0, 200), "MJet_pt")
    # h_full.Scale(1 / h_full.Integral())
    # h_flash = rdf.Histo1D(("h_flash", "h_flash", 100, 0, 200), "Jet_pt")
    # h_flash.Scale(1 / h_flash.Integral())

    # ROOT.gStyle.SetOptStat(0)
    # ROOT.gStyle.SetOptFit(0)
    # ROOT.gStyle.SetTextFont(42)
    # c = ROOT.TCanvas("c", "c", 800, 700)
    # c.SetLeftMargin(0.15)

    # h_full.SetTitle("")
    # h_full.GetXaxis().SetTitle("p_{T}")  # / p_{T}^{G}")
    # h_full.GetXaxis().SetTitleSize(0.04)
    # h_full.GetYaxis().SetTitle("Entries")  # pt comparison
    # h_full.GetYaxis().SetTitleSize(0.04)
    # h_full.SetLineColor(ROOT.kBlack)
    # h_full.SetLineWidth(2)
    # h_full.SetLineStyle(2)

    # h_flash.SetLineColor(ROOT.kOrange + 7)
    # h_flash.SetLineWidth(2)

    # h_full.DrawClone("hist")
    # h_flash.DrawClone("hist same")

    # legend = ROOT.TLegend(0.72, 0.75, 0.89, 0.88)
    # legend.SetFillColor(0)
    # legend.SetFillStyle(0)
    # legend.SetBorderSize(0)
    # legend.SetTextSize(0.02)
    # legend.AddEntry("h_full", "FullSim", "l")
    # legend.AddEntry("h_flash", "FlashSim", "l")
    # legend.DrawClone("NDC NB")

    # cms_label = ROOT.TLatex()
    # cms_label.SetTextSize(0.04)
    # cms_label.DrawLatexNDC(0.16, 0.92, "#bf{CMS} #it{Private Work}")
    # c.Update()

    # c.SaveAs(os.path.join(save_path, "pt_jet_comparison.pdf"))

    # c_pt = comparison(rdf, "Electron_pt", [0, 100], 100)
    # c_pt.SaveAs(os.path.join(save_path, "DY_Electron_pt.pdf"))

    # c_1 = ratio(rdf, "PElectron_pt", "PGenElectron_pt", "FlashSim")
    # c_1.SaveAs(os.path.join(save_path, "TT_2D_pt_Flash.pdf"))

    # c_2 = ratio(rdf, "MElectron_pt", "MGenElectron_pt", "FullSim")
    # c_2.SaveAs(os.path.join(save_path, "TT_2D_pt_Full.pdf"))

    # Z boson

    rdf = ROOT.RDataFrame("Events", path)

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

    df_full = ROOT.RDataFrame("FullSim", path)

    for i, (cut, label) in enumerate(zip(cuts, labels)):
        filename = f"z_{i}_bin_el.pdf"
        c_z = analysis(df_full, rdf, cut, label)
        c_z.SaveAs(os.path.join(save_path, filename))
