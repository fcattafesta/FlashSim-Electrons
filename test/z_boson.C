#include "match.h"

auto InvariantMass(ROOT::VecOps::RVec<double> &pt,
                   ROOT::VecOps::RVec<double> &eta,
                   ROOT::VecOps::RVec<double> &phi) {

  auto m = 0.51099895000e-3; // GeV

  ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], m);
  ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], m);

  return (p1 + p2).mass();
}

auto InvariantMass_float(ROOT::VecOps::RVec<float> &pt,
                   ROOT::VecOps::RVec<float> &eta,
                   ROOT::VecOps::RVec<float> &phi) {

  auto m = 0.51099895000e-3; // GeV

  ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], m);
  ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], m);

  return (p1 + p2).mass();
}

void z_boson() {

  ROOT::EnableImplicitMT();

  auto g =
      TFile::Open("/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/"
                  "DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/"
                  "NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/"
                  "230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root",
                  "r");

  auto d_tmp = ROOT::RDataFrame("Events", g);
  auto d_full = match(d_tmp);

  auto f = TFile::Open("/gpfs/ddn/cms/user/cattafe/DYJets/EM1/230000/"
                       "8244ED99-0F95-9D4F-B393-22EBC589A46D_synth.root",
                       "r");

  auto d_flash = ROOT::RDataFrame("Events", f);

  auto d_flash_z = d_flash.Filter("nElectron == 2")
                 .Filter("All(abs(Electron_eta) < 2.5)")
                 .Filter("All(Electron_pt > 20)")
                 .Filter("Sum(Electron_charge) == 0")
                 .Filter("All(Electron_ip3d < 0.015)")
                 .Define("Z_mass", InvariantMass,
                         {"Electron_pt", "Electron_eta", "Electron_phi"});

  auto d_full_z = d_full.Filter("MnElectron == 2")
                       .Filter("All(abs(MElectron_eta) < 2.5)")
                       .Filter("All(MElectron_pt > 20)")
                       .Filter("Sum(MElectron_charge) == 0")
                       .Filter("All(MElectron_ip3d < 0.015)")
                       .Define("Z_mass", InvariantMass_float,
                               {"MElectron_pt", "MElectron_eta", "MElectron_phi"});

  auto h_flash = d_flash_z.Histo1D({"", "", 50, 60, 110}, "Z_mass");
  auto h_full = d_full_z.Histo1D({"", "", 50, 60, 110}, "Z_mass");

  h_flash->Scale(1. / h_flash->Integral());
  h_full->Scale(1. / h_full->Integral());
  
  gStyle->SetOptStat(0);
  gStyle->SetTextFont(42);
  auto c = new TCanvas("", "", 800, 700);
  c->SetLeftMargin(0.15);

  h_full->SetTitle("");
  h_full->GetXaxis()->SetTitle("#m_{ee} [GeV]");
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

  c->SaveAs("figures/z_boson.pdf");

}