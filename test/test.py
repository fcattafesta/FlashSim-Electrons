import os
import ROOT
from z_boson import analysis
from collection_comparison import comparison


if __name__ == "__main__":
    path = "/gpfs/ddn/cms/user/cattafe/FlashSim/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root"
    save_path = os.path.join(os.path.dirname(__file__), "figures", "EEM_90")

    # ROOT.EnableImplicitMT()

    file = ROOT.TFile.Open(path)

    events = file.Events
    full = file.FullSim

    events.AddFriend(full, "FullSim")

    rdf = ROOT.RDataFrame(events)

    inf = 0
    sup = 100
    nbins = 100

    h_full = rdf.Histo1D(("full", "", nbins, inf, sup), "FullSim.Electron_pt")
    h_full.Scale(1.0 / h_full.Integral())

    h_flash = rdf.Histo1D(("FlashSim", "", nbins, inf, sup), "Electron_pt")
    h_flash.Scale(1.0 / h_flash.Integral())

    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "c", 800, 700)
    c.SetLeftMargin(0.15)

    h_full.SetTitle("")
    h_full.GetXaxis().SetTitle("")
    h_full.GetXaxis().SetTitleSize(0.04)
    h_full.GetYaxis().SetTitle("Normalized Events / 1 GeV")  # pt comparison
    h_full.GetYaxis().SetTitleSize(0.04)
    h_full.SetLineColor(ROOT.kBlack)
    h_full.SetLineWidth(2)
    h_full.SetLineStyle(2)

    h_flash.SetLineColor(ROOT.kOrange + 7)
    h_flash.SetLineWidth(2)

    h_full.DrawClone("hist")
    h_flash.DrawClone("hist same")

    legend = ROOT.TLegend(0.72, 0.75, 0.89, 0.88)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.02)
    legend.AddEntry("FullSim", "FullSim", "l")
    legend.AddEntry("FlashSim", "FlashSim", "l")
    legend.DrawClone("NDC NB")

    cms_label = ROOT.TLatex()
    cms_label.SetTextSize(0.04)
    cms_label.DrawLatexNDC(0.16, 0.92, "#bf{CMS} #it{Private Work}")
    c.Update()
    c.SaveAs(os.path.join(save_path, "Electron_pt.pdf"))

    # h = rdf.Histo1D(("h", "", 100, 0, 100), "Electron_pt")
    # h_f = rdf.Histo1D(("h_f", "", 100, 0, 100), "full.Electron_pt")

    # c_pt = comparison(rdf, "Electron_pt", [0, 100], 100)
    # c_pt.SaveAs(os.path.join(save_path, "Electron_pt.pdf"))

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
