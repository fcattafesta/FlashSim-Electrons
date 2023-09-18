import ROOT

ROOT.gInterpreter.ProcessLine('#include "z_func.h"')


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


def fit(df, sim):
    h = df.Histo1D((sim, "", 50, 60, 120), "Z_mass")
    if h.Integral() > 0:
        h.Scale(1 / h.Integral())

    f = ROOT.TF1("f", "gaus", 87, 93)
    f.SetParameters(0.1, 90, 3)

    res = h.Fit(f, "LQISR")
    f.SetParameters(*res.Get().Parameters())

    return f, h


def analysis(df_full, df_flash, pt_cut, label):
    df_full = search_z(df_full, pt_cut)
    df_flash = search_z(df_flash, pt_cut)

    # f_full, h_full = fit(df_full, "FullSim")
    # f_flash, h_flash = fit(df_flash, "FlashSim")

    h_full = df_full.Histo1D(("FullSim", "FullSim", 50, 60, 120), "Z_mass")
    h_flash = df_flash.Histo1D(("FlashSim", "FlashSim", 50, 60, 120), "Z_mass")
    if h_full.Integral() > 0 and h_flash.Integral() > 0:
        h_full.Scale(1 / h_full.Integral())
        h_flash.Scale(1 / h_flash.Integral())

    bias = (h_flash.GetMean() - h_full.GetMean()) / h_full.GetMean()

    widtj = h_flash.GetStdDev() / h_full.GetStdDev()

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

    h_flash.SetLineColor(ROOT.kOrange + 8)
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
    bin = ROOT.TLatex()
    bin.SetTextSize(0.03)
    bin.DrawLatexNDC(0.2, 0.86, label)
    bias_label = ROOT.TLatex()
    bias_label.SetTextSize(0.03)
    bias_label.DrawLatexNDC(
        0.2, 0.80, f"(#mu_{{Flash}} / #mu_{{Full}}) - 1 = {bias*100:.2f}%"
    )
    width_label = ROOT.TLatex()
    width_label.SetTextSize(0.03)
    width_label.DrawLatexNDC(
        0.2, 0.74, f"({{#sigma}}_{{Flash}} / {{#sigma}}_{{Full}}) = {widtj:.2f}"
    )
    c.Update()

    return c
