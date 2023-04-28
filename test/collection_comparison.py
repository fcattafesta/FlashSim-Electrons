import ROOT


def comparison(df_full, df_flash, variable, range, nbins):
    inf = range[0]
    sup = range[1]

    h_full = df_full.Histo1D((variable, variable, nbins, inf, sup), variable)
    h_full = h_full.Scale(1.0 / h_full.Integral())

    h_flash = df_flash.Histo1D((variable, variable, nbins, inf, sup), variable)
    h_flash = h_flash.Scale(1.0 / h_flash.Integral())

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
    legend.AddEntry(h_flash, "FullSim", "l")
    legend.AddEntry(h_full, "FlashSim", "l")
    legend.DrawClone("NDC NB")

    cms_label = ROOT.TLatex()
    cms_label.SetTextSize(0.04)
    cms_label.DrawLatexNDC(0.16, 0.92, "#bf{CMS} #it{Private Work}")
    c.Update()
    return c
