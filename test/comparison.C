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

  h_flash->SetLineColor(kOrange + 7);
  h_flash->SetLineWidth(2);

  h_full->DrawClone("hist");
  h_flash->DrawClone("hist same");

  auto legend = new TLegend(0.72, 0.70, 0.92, 0.88);
  legend->SetFillColor(0);
  legend->SetBorderSize(0);
  legend->SetTextSize(0.02);
  legend->AddEntry(h_full.GetPtr(), "FullSim", "f");
  legend->AddEntry(h_flash.GetPtr(), "FlashSim", "f");
  legend->DrawClone();

  TLatex cms_label;
  cms_label.SetTextSize(0.04);
  cms_label.DrawLatexNDC(0.16, 0.92, "#bf{CMS} #it{Private Work}");
  TLatex header;
  header.SetTextSize(0.03);
 
  std::string filename = "comparison_" + col + ".pdf";
  c->SaveAs(filename.c_str());
}

void comparison() {
  compare("Electron_eta", -4, 4);
}