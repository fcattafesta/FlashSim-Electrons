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


def search_z(df, pt_cut, tag):

    if tag == "flash":
        z_pt = "z_pt"
        invariant_mass = "InvariantMass"
    elif tag == "full":
        z_pt = "z_pt_float"
        invariant_mass = "InvariantMass_float"

    df_cut = (
        df.Filter("nElectron == 2")
        .Filter("All(abs(Electron_eta) < 2.5)")
        .Filter("All(Electron_pt > 20)")
        .Filter("Sum(Electron_charge) == 0")
        .Define("Z_pt", f"{z_pt}(Electron_pt, Electron_eta, Electron_phi)")
        .Filter(pt_cut)
        .Define("Z_mass", f"{invariant_mass}(Electron_pt, Electron_eta, Electron_phi)")
    )

    return df_cut


def fit(df):
    h = df.Histo1D(("Z_mass", "Z_mass", 50, 60, 120), "Z_mass")
    h.Scale(1 / h.Integral())

    f = ROOT.TF1("f", "gaus", 87, 93)
    f.SetParameters(0.1, 90, 3)

    res = h.Fit(f, "LQISR")
    f.SetParameters(*res.Get().Parameters())

    return f, h


def plot(h_full, f_full, h_flash, f_flash, bias, label):
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
    legend.AddEntry(h_full, "FullSim", "l")
    legend.AddEntry(h_flash, "FlashSim", "l")
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


def analysis(full_path, flash_path, pt_cut, label, filename):

    ROOT.EnableImplicitMT()

    df_full = ROOT.RDataFrame("Events", full_path)
    df_flash = ROOT.RDataFrame("Events", flash_path)

    df_full = ROOT.match(df_full)

    df_full = search_z(df_full, pt_cut, "full")
    df_flash = search_z(df_flash, pt_cut, "flash")

    f_full, h_full = fit(df_full)
    f_flash, h_flash = fit(df_flash)

    bias = (f_flash.GetParameter(1) - f_full.GetParameter(1)) / f_full.GetParameter(1)

    c = plot(h_full, f_full, h_flash, f_flash, bias, label)
    c.SaveAs(filename)


if __name__ == "__main__":

    file = "2E88EB28-11AB-414B-8485-E239270F1F94"
    full_path = f"/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/230000/{file}.root"
    flash_path = f"/gpfs/ddn/cms/user/cattafe/DYJets/EM1_190/230000/{file}_synth.root"

    for i, (cut, label) in enumerate(zip(cuts, labels)):
        filename = f"figures/190/z_{i}_bins.pdf"
        analysis(full_path, flash_path, cut, label, filename)
