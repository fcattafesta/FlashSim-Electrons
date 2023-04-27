import ROOT

ROOT.gInterpreter.ProcessLine('#include "z_func.h"')

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


def search_z(df, pt_cut):
    df_cut = (
        df.Filter("Electron_pt.size() == 2")
        .Filter("All(abs(Electron_eta) < 2.5)")
        .Filter("All(Electron_pt > 20)")
        .Filter("Sum(Electron_charge) == 0")
        .Define("Z_pt", "Zpt(Electron_pt, Electron_eta, Electron_phi)")
        .Filter(pt_cut)
        .Define("Z_mass", "InvariantMass(Electron_pt, Electron_eta, Electron_phi)")
    )

    return df_cut


def fit(df):
    h = df.Histo1D(("Z_mass", "Z_mass", 50, 60, 120), "Z_mass")
    if h.Integral() > 0:
        h.Scale(1 / h.Integral())

    f = ROOT.TF1("f", "gaus", 87, 93)
    f.SetParameters(0.1, 90, 3)

    res = h.Fit(f, "LQISR")
    f.SetParameters(*res.Get().Parameters())

    return f, h


def plot(h_full, f_full, h_flash, f_flash, bias, label):
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    ROOT.gStyle.SetTextFont(42)
    c = ROOT.TCanvas("c", "c", 800, 700)
    c.SetLeftMargin(0.15)

    h_full.SetTitle("")
    h_full.GetXaxis().SetTitle("m_{ee} [GeV]")
    h_full.GetXaxis().SetTitleSize(0.04)
    h_full.GetYaxis().SetTitle("Normalized Events / 1 GeV")
    h_full.GetYaxis().SetTitleSize(0.04)
    h_full.SetLineColor(ROOT.kBlack)
    h_full.SetLineWidth(2)
    h_full.SetLineStyle(2)

    h_flash.SetLineColor(ROOT.kOrange + 7)
    h_flash.SetLineWidth(2)

    f_full.SetLineColor(ROOT.kBlue)
    f_flash.SetLineColor(ROOT.kBlue)

    h_full.DrawClone("hist")
    h_flash.DrawClone("hist same")
    f_full.DrawClone("same")
    f_flash.DrawClone("same")

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
    bin = ROOT.TLatex()
    bin.SetTextSize(0.03)
    bin.DrawLatexNDC(0.2, 0.86, label)
    bias_label = ROOT.TLatex()
    bias_label.SetTextSize(0.03)
    bias_label.DrawLatexNDC(0.2, 0.80, f"Bias = {bias*100:.2f}%")
    c.Update()

    return c


def analysis(flash_path, pt_cut, label, filename):
    ROOT.EnableImplicitMT()

    df_full = ROOT.RDataFrame("FullSim", flash_path)
    df_flash = ROOT.RDataFrame("Events", flash_path)

    df_full = search_z(df_full, pt_cut)
    df_flash = search_z(df_flash, pt_cut)

    f_full, h_full = fit(df_full)
    f_flash, h_flash = fit(df_flash)

    bias = (f_flash.GetParameter(1) - f_full.GetParameter(1)) / f_full.GetParameter(1)

    c = plot(h_full, f_full, h_flash, f_flash, bias, label)
    c.SaveAs(filename)


if __name__ == "__main__":
    flash_path = "/gpfs/ddn/cms/user/cattafe/FlashSim/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root"
    for i, (cut, label) in enumerate(zip(cuts, labels)):
        filename = f"figures/prova/z_{i}_bins.pdf"
        analysis(flash_path, cut, label, filename)
