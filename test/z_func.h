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

auto z_pt_float(ROOT::VecOps::RVec<float> &pt, ROOT::VecOps::RVec<float> &eta,
                ROOT::VecOps::RVec<float> &phi) {

  auto m = 0.51099895000e-3; // GeV

  ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], m);
  ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], m);

  return (p1 + p2).pt();
}

auto z_pt(ROOT::VecOps::RVec<double> &pt, ROOT::VecOps::RVec<double> &eta,
          ROOT::VecOps::RVec<double> &phi) {

  auto m = 0.51099895000e-3; // GeV

  ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], m);
  ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], m);

  return (p1 + p2).pt();
}

void z_boson(std::string pt_cut, std::string label, std::string filename) {

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

  auto d_flash_z =
      d_flash.Filter("nElectron == 2")
          .Filter("All(abs(Electron_eta) < 2.5)")
          .Filter("All(Electron_pt > 20)")
          .Filter("Sum(Electron_charge) == 0")
          .Define("Z_pt", z_pt, {"Electron_pt", "Electron_eta", "Electron_phi"})
          .Filter(pt_cut.c_str())
          .Define("Z_mass", InvariantMass,
                  {"Electron_pt", "Electron_eta", "Electron_phi"});

  auto d_full_z =
      d_full.Filter("MnElectron == 2")
          .Filter("All(abs(MElectron_eta) < 2.5)")
          .Filter("All(MElectron_pt > 20)")
          .Filter("Sum(MElectron_charge) == 0")
          .Define("Z_pt", z_pt_float,
                  {"MElectron_pt", "MElectron_eta", "MElectron_phi"})
          .Filter(pt_cut.c_str())
          .Define("Z_mass", InvariantMass_float,
                  {"MElectron_pt", "MElectron_eta", "MElectron_phi"});

  auto h_flash = d_flash_z.Histo1D({"", "", 50, 60, 110}, "Z_mass");
  auto h_full = d_full_z.Histo1D({"", "", 50, 60, 110}, "Z_mass");

  auto gaus = new TF1("gaus", "gaus", 80, 100);

  auto res_full = h_full->Fit(gaus, "LISQR");

  h_flash->Scale(1. / h_flash->Integral());
  h_full->Scale(1. / h_full->Integral());

  gStyle->SetOptStat(0);
  gStyle->SetTextFont(42);
  auto c = new TCanvas("", "", 800, 700);
  c->SetLeftMargin(0.15);

  h_full->SetTitle("");
  h_full->GetXaxis()->SetTitle("m_{ee} [GeV]");
  h_full->GetXaxis()->SetTitleSize(0.04);
  h_full->GetYaxis()->SetTitle("Normalized Events / 1 GeV");
  h_full->GetYaxis()->SetTitleSize(0.04);
  h_full->SetLineColor(kBlack);
  h_full->SetLineWidth(2);
  h_full->SetLineStyle(2);

  h_flash->SetLineColor(kOrange + 7);
  h_flash->SetLineWidth(2);

  h_full->DrawClone("hist");
  gaus->DrawClone("same AL");
  gaus->SetLineColor(kRed);
  gaus->SetLineStyle(2);

  auto res_flash = h_flash->Fit(gaus, "LISQR");

  gaus->DrawClone("same AL");
  gaus->SetLineColor(kRed);
  h_flash->DrawClone("hist same");

  auto mean_flash = res_flash->Parameter(1);
  auto mean_full = res_full->Parameter(1);

  cout << "Mean flash: " << mean_flash << endl;
  cout << "Mean full: " << mean_full << endl;

  auto bias = (mean_flash - mean_full) / mean_full;

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
  TLatex bin;
  bin.SetTextSize(0.03);
  bin.DrawLatexNDC(0.2, 0.86, label.c_str());
  TLatex bias_label;
  bias_label.SetTextSize(0.03);
  bias_label.DrawLatexNDC(0.2, 0.82, Form("Bias = %.2f%%", bias * 100));

  c->SaveAs(filename.c_str());
}