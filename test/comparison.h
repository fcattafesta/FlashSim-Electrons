#include "TLatex.h"
#include "TLegend.h"
#include "match.h"
#include <string>

void compare(std::string col, float min, float max, int nbins = 50) {

  ROOT::EnableImplicitMT();

  auto full_path = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/"
                   "DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/"
                   "NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/"
                   "230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root";

  auto flash_path = "/gpfs/ddn/cms/user/cattafe/DYJets/EM1/230000/"
                    "8244ED99-0F95-9D4F-B393-22EBC589A46D_synth.root";

  auto d_tmp = ROOT::RDataFrame("Events", full_path);
  auto d_full = match(d_tmp);

  auto d_flash = ROOT::RDataFrame("Events", flash_path);

  auto h_full =
      d_full.Histo1D({"h_full", "h_full", nbins, min, max}, "M" + col);
  auto h_flash = d_flash.Histo1D({"h_flash", "h_flash", nbins, min, max}, col);

  h_full->Scale(1. / h_full->Integral());
  h_flash->Scale(1. / h_flash->Integral());

  gStyle->SetOptStat(0);
  gStyle->SetTextFont(42);
  auto c = new TCanvas("", "", 800, 700);
  c->SetLeftMargin(0.15);

  h_full->SetTitle("");
  h_full->GetXaxis()->SetTitle("");
  h_full->GetXaxis()->SetTitleSize(0.04);
  h_full->GetYaxis()->SetTitle("Normalized Events");
  h_full->GetYaxis()->SetTitleSize(0.04);
  h_full->SetLineColor(kBlack);
  h_full->SetLineWidth(2);
  h_full->SetLineStyle(2);

  h_flash->SetLineColor(kOrange + 7);
  h_flash->SetLineWidth(2);

  h_full->DrawClone("hist");
  h_flash->DrawClone("hist same");

  auto legend = new TLegend(0.72, 0.75, 0.89, 0.88);
  legend->SetFillColor(0);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.02);
  legend->AddEntry(h_full.GetPtr(), "FullSim", "l");
  legend->AddEntry(h_flash.GetPtr(), "FlashSim", "l");
  legend->SetFillStyle(0);
  legend->DrawClone("NDC NB");

  TLatex cms_label;
  cms_label.SetTextSize(0.04);
  cms_label.DrawLatexNDC(0.16, 0.92, "#bf{CMS} #it{Private Work}");
  TLatex header;
  header.SetTextSize(0.03);

  std::string filename = "figures/comparison_" + col + ".pdf";
  c->SaveAs(filename.c_str());
}

void pt_bias() {

  auto min = 0;
  auto max = 100;
  auto nbins = 100;

  std::string col = "Electron_pt";

  ROOT::EnableImplicitMT();

  auto full_path = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/"
                   "DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/"
                   "NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/"
                   "230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root";

  auto flash_path = "/gpfs/ddn/cms/user/cattafe/DYJets/EM1/230000/"
                    "8244ED99-0F95-9D4F-B393-22EBC589A46D_synth.root";

  auto d_tmp = ROOT::RDataFrame("Events", full_path);
  auto d_full = match(d_tmp);

  auto d_flash = ROOT::RDataFrame("Events", flash_path);

  auto h_full =
      d_full.Histo1D({"h_full", "h_full", nbins, min, max}, "M" + col);
  auto h_flash = d_flash.Histo1D({"h_flash", "h_flash", nbins, min, max}, col);

  h_full->Scale(1. / h_full->Integral());
  h_flash->Scale(1. / h_flash->Integral());

  auto peak_full = new TF1("peak_full", "gaus", 20, 50);
  peak_full->SetParameters(0.1, 32, 10);

  auto peak_flash = new TF1("peak_flash", "gaus", 88, 94);
  peak_flash->SetParameters(0.1, 32, 10);

  auto res_full = h_full->Fit(peak_full, "LQISR");
  auto res_flash = h_flash->Fit(peak_flash, "LIQSR");

  auto mean_flash = res_flash->Parameter(1);
  auto mean_full = res_full->Parameter(1);
  auto bias = (mean_flash - mean_full) / mean_full;

  gStyle->SetOptStat(0);
  gStyle->SetTextFont(42);
  auto c = new TCanvas("", "", 800, 700);
  c->SetLeftMargin(0.15);

  h_full->SetTitle("");
  h_full->GetXaxis()->SetTitle("");
  h_full->GetXaxis()->SetTitleSize(0.04);
  h_full->GetYaxis()->SetTitle("Normalized Events");
  h_full->GetYaxis()->SetTitleSize(0.04);
  h_full->SetLineColor(kBlack);
  h_full->SetLineWidth(2);
  h_full->SetLineStyle(2);

  h_flash->SetLineColor(kOrange + 7);
  h_flash->SetLineWidth(2);

  h_full->DrawClone("hist");

  peak_full->Draw("same AL");
  peak_full->SetLineColor(kBlue);
  peak_full->SetLineStyle(2);

  h_flash->DrawClone("hist same");

  peak_flash->Draw("same AL");
  peak_flash->SetLineColor(kBlue);

  auto legend = new TLegend(0.72, 0.75, 0.89, 0.88);
  legend->SetFillColor(0);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.02);
  legend->AddEntry(h_full.GetPtr(), "FullSim", "l");
  legend->AddEntry(h_flash.GetPtr(), "FlashSim", "l");
  legend->SetFillStyle(0);
  legend->DrawClone("NDC NB");

  TLatex cms_label;
  cms_label.SetTextSize(0.04);
  cms_label.DrawLatexNDC(0.16, 0.92, "#bf{CMS} #it{Private Work}");
  TLatex header;
  header.SetTextSize(0.03);
  TLatex bias_label;
  bias_label.SetTextSize(0.03);
  bias_label.DrawLatexNDC(0.2, 0.80, Form("Bias = %.2f%%", bias * 100));

  std::string filename = "figures/bias_" + col + ".pdf";
  c->SaveAs(filename.c_str());
}