auto clean_genjet_mask(ROOT::VecOps::RVec<float> &jet_pt,
                       ROOT::VecOps::RVec<float> &jet_eta,
                       ROOT::VecOps::RVec<float> &jet_phi,
                       ROOT::VecOps::RVec<float> &lep_pt,
                       ROOT::VecOps::RVec<float> &lep_eta,
                       ROOT::VecOps::RVec<float> &lep_phi) {
  /* Mask to remove GenElectrons  and GenMuons from the GenJet collection.*/
  auto lep_size = lep_pt.size();
  auto jet_size = jet_pt.size();

  ROOT::VecOps::RVec<int> clean_jet_mask;
  clean_jet_mask.reserve(jet_size);

  for (size_t i = 0; i < jet_size; i++) {
    clean_jet_mask.push_back(1);
    for (size_t j = 0; j < lep_size; j++) {
      auto dpt = jet_pt[i] - lep_pt[j];
      auto deta = jet_eta[i] - lep_eta[j];
      auto dphi = TVector2::Phi_mpi_pi(jet_phi[i] - lep_phi[j]);
      auto dr = TMath::Sqrt(deta * deta + dphi * dphi);

      if ((dr <= 0.01) && ((dpt / lep_pt[j]) <= 0.001)) {
        clean_jet_mask[i] = 0;
      }
    }
  }
  return clean_jet_mask;
}

auto DeltaPhi(ROOT::VecOps::RVec<float> &Phi1,
              ROOT::VecOps::RVec<float> &Phi2) {
  /* Calculates the DeltaPhi between two RVecs
   */
  auto size = Phi1.size();
  ROOT::VecOps::RVec<float> dphis;
  dphis.reserve(size);
  for (size_t i = 0; i < size; i++) {
    Double_t dphi = TVector2::Phi_mpi_pi(Phi1[i] - Phi2[i]);
    dphis.emplace_back(dphi);
  }
  return dphis;
}

auto Electron_genJetIdx(ROOT::VecOps::RVec<float> &jet_pt,
                        ROOT::VecOps::RVec<float> &jet_eta,
                        ROOT::VecOps::RVec<float> &jet_phi,
                        ROOT::VecOps::RVec<float> &lep_pt,
                        ROOT::VecOps::RVec<float> &lep_eta,
                        ROOT::VecOps::RVec<float> &lep_phi) {

  auto size_outer = lep_pt.size();
  auto size_inner = jet_pt.size();

  ROOT::VecOps::RVec<int> idx;
  idx.reserve(size_outer);

  for (size_t i = 0; i < size_outer; i++) {
    idx.push_back(-1);
    auto closest_pt_rel = 0.5;
    auto closest_dr = 0.3;
    for (size_t j = 0; j < size_inner; j++) {
      auto dpt = jet_pt[j] - lep_pt[i];
      auto deta = jet_eta[j] - lep_eta[i];
      auto dphi = TVector2::Phi_mpi_pi(jet_phi[j] - lep_phi[i]);
      auto dr = TMath::Sqrt(deta * deta + dphi * dphi);

      if ((dr < closest_dr) && ((dpt / lep_pt[i]) < closest_pt_rel)) {
        closest_dr = dr;
        closest_pt_rel = dpt / lep_pt[i];
        idx[i] = j;
      }
    }
  }

  return idx;
}

void extraction(string sample_name, string dataset_name) {

  cout << "Processing " << sample_name << " to " << dataset_name << endl;

  ROOT::EnableImplicitMT();

  TFile *f = TFile::Open(sample_name.c_str(), "READ");

  ROOT::RDataFrame d("Events", f);

  auto pre =
      d.Define("GenElectronMask", "abs(GenPart_pdgId) == 11")
          .Define("GenElectron_pt", "GenPart_pt[GenElectronMask]")
          .Define("GenElectron_eta", "GenPart_eta[GenElectronMask]")
          .Define("GenElectron_phi", "GenPart_phi[GenElectronMask]")
          .Define("GenMuonMask", "abs(GenPart_pdgId) == 13")
          .Define("GenMuon_pt", "GenPart_pt[GenMuonMask]")
          .Define("GenMuon_eta", "GenPart_eta[GenMuonMask]")
          .Define("GenMuon_phi", "GenPart_phi[GenMuonMask]")
          .Define("CleanGenJet_mask_ele", clean_genjet_mask,
                  {"GenJet_pt", "GenJet_eta", "GenJet_phi", "GenElectron_pt",
                   "GenElectron_eta", "GenElectron_phi"})
          .Define("CleanGenJet_mask_muon", clean_genjet_mask,
                  {"GenJet_pt", "GenJet_eta", "GenJet_phi", "GenMuon_pt",
                   "GenMuon_eta", "GenMuon_phi"})
          .Define("CleanGenJetMask",
                  "CleanGenJet_mask_ele && CleanGenJet_mask_muon")
          .Define("CleanGenJet_pt", "GenJet_pt[CleanGenJetMask]")
          .Define("CleanGenJet_eta", "GenJet_eta[CleanGenJetMask]")
          .Define("CleanGenJet_phi", "GenJet_phi[CleanGenJetMask]")
          .Define("CleanGenJet_mass", "GenJet_mass[CleanGenJetMask]")
          .Define("CleanGenJet_hadronFlavour_uchar",
                  "GenJet_hadronFlavour[CleanGenJetMask]")
          .Define("CleanGenJet_hadronFlavour",
                  "static_cast<ROOT::VecOps::RVec<int>>(CleanGenJet_"
                  "hadronFlavour_uchar)")
          .Define("CleanGenJet_partonFlavour",
                  "GenJet_partonFlavour[CleanGenJetMask]");

  auto matched =
      pre.Define("Electron_genJetIdx", Electron_genJetIdx,
                 {"CleanGenJet_pt", "CleanGenJet_eta", "CleanGenJet_phi",
                  "Electron_pt", "Electron_eta", "Electron_phi"})
          .Define("MGenJetIdx", "Electron_genJetIdx[Electron_genJetIdx >= 0]")
          .Define("MGenJet_pt", "Take(CleanGenJet_pt, MGenJetIdx)")
          .Define("MGenJet_eta", "Take(CleanGenJet_eta, MGenJetIdx)")
          .Define("MGenJet_phi", "Take(CleanGenJet_phi, MGenJetIdx)")
          .Define("MGenJet_mass", "Take(CleanGenJet_mass, MGenJetIdx)")
          .Define("MGenJet_hadronFlavour",
                  "Take(CleanGenJet_hadronFlavour, MGenJetIdx)")
          .Define("MGenJet_partonFlavour",
                  "Take(CleanGenJet_partonFlavour, MGenJetIdx)")
          .Define("Electron_MGenJetMask", "Electron_genJetIdx >= 0")
          .Define("MElectron_convVeto",
                  "Electron_convVeto[Electron_MGenJetMask]")
          .Define("MElectron_deltaEtaSC",
                  "Electron_deltaEtaSC[Electron_MGenJetMask]")
          .Define("MElectron_dr03EcalRecHitSumEt",
                  "Electron_dr03EcalRecHitSumEt[Electron_MGenJetMask]")
          .Define("MElectron_dr03HcalDepth1TowerSumEt",
                  "Electron_dr03HcalDepth1TowerSumEt[Electron_MGenJetMask]")
          .Define("MElectron_dr03TkSumPt",
                  "Electron_dr03TkSumPt[Electron_MGenJetMask]")
          .Define("MElectron_dr03TkSumPtHEEP",
                  "Electron_dr03TkSumPtHEEP[Electron_MGenJetMask]")
          .Define("MElectron_dxy", "Electron_dxy[Electron_MGenJetMask]")
          .Define("MElectron_dxyErr", "Electron_dxyErr[Electron_MGenJetMask]")
          .Define("MElectron_dz", "Electron_dz[Electron_MGenJetMask]")
          .Define("MElectron_dzErr", "Electron_dzErr[Electron_MGenJetMask]")
          .Define("MElectron_eInvMinusPInv",
                  "Electron_eInvMinusPInv[Electron_MGenJetMask]")
          .Define("MElectron_energyErr",
                  "Electron_energyErr[Electron_MGenJetMask]")
          .Define("MElectron_etaMinusGen",
                  "Electron_eta[Electron_MGenJetMask] - MGenJet_eta")
          .Define("MElectron_hoe", "Electron_hoe[Electron_MGenJetMask]")
          .Define("MElectron_ip3d", "Electron_ip3d[Electron_MGenJetMask]")
          .Define("MElectron_isPFcand",
                  "Electron_isPFcand[Electron_MGenJetMask]")
          .Define("MElectron_jetPtRelv2",
                  "Electron_jetPtRelv2[Electron_MGenJetMask]")
          .Define("MElectron_jetRelIso",
                  "Electron_jetRelIso[Electron_MGenJetMask]")
          .Define("MElectron_lostHits",
                  "Electron_lostHits[Electron_MGenJetMask]")
          .Define("MElectron_miniPFRelIso_all",
                  "Electron_miniPFRelIso_all[Electron_MGenJetMask]")
          .Define("MElectron_miniPFRelIso_chg",
                  "Electron_miniPFRelIso_chg[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1Iso",
                  "Electron_mvaFall17V1Iso[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1Iso_WP80",
                  "Electron_mvaFall17V1Iso_WP80[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1Iso_WP90",
                  "Electron_mvaFall17V1Iso_WP90[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1Iso_WPL",
                  "Electron_mvaFall17V1Iso_WPL[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1noIso",
                  "Electron_mvaFall17V1noIso[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1noIso_WP80",
                  "Electron_mvaFall17V1noIso_WP80[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1noIso_WP90",
                  "Electron_mvaFall17V1noIso_WP90[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V1noIso_WPL",
                  "Electron_mvaFall17V1noIso_WPL[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2Iso",
                  "Electron_mvaFall17V2Iso[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2Iso_WP80",
                  "Electron_mvaFall17V2Iso_WP80[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2Iso_WP90",
                  "Electron_mvaFall17V2Iso_WP90[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2Iso_WPL",
                  "Electron_mvaFall17V2Iso_WPL[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2noIso",
                  "Electron_mvaFall17V2noIso[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2noIso_WP80",
                  "Electron_mvaFall17V2noIso_WP80[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2noIso_WP90",
                  "Electron_mvaFall17V2noIso_WP90[Electron_MGenJetMask]")
          .Define("MElectron_mvaFall17V2noIso_WPL",
                  "Electron_mvaFall17V2noIso_WPL[Electron_MGenJetMask]")
          .Define("MElectron_mvaTTH", "Electron_mvaTTH[Electron_MGenJetMask]")
          .Define("MElectron_pfRelIso03_all",
                  "Electron_pfRelIso03_all[Electron_MGenJetMask]")
          .Define("MElectron_pfRelIso03_chg",
                  "Electron_pfRelIso03_chg[Electron_MGenJetMask]")
          .Define("MElectron_phi", "Electron_phi[Electron_MGenJetMask]")
          .Define("MElectron_phiMinusGen", DeltaPhi,
                  {"MElectron_phi", "MGenJet_phi"})
          .Define("MElectron_ptRatio",
                  "Electron_pt[Electron_MGenJetMask] / MGenJet_pt")
          .Define("MElectron_r9", "Electron_r9[Electron_MGenJetMask]")
          .Define("MElectron_seedGain",
                  "Electron_seedGain[Electron_MGenJetMask]")
          .Define("MElectron_sieie", "Electron_sieie[Electron_MGenJetMask]")
          .Define("MElectron_sip3d", "Electron_sip3d[Electron_MGenJetMask]")
          .Define("MElectron_tightCharge",
                  "Electron_tightCharge[Electron_MGenJetMask]");

  vector<string> col_to_save = {"MGenJet_eta",
                                "MGenJet_hadronFlavour",
                                "MGenJet_mass",
                                "MGenJet_partonFlavour",
                                "MGenJet_phi",
                                "MGenJet_pt",
                                "Pileup_gpudensity",
                                "Pileup_nPU",
                                "Pileup_nTrueInt",
                                "Pileup_pudensity",
                                "Pileup_sumEOOT",
                                "Pileup_sumLOOT",
                                "MElectron_convVeto",
                                "MElectron_deltaEtaSC",
                                "MElectron_dr03EcalRecHitSumEt",
                                "MElectron_dr03HcalDepth1TowerSumEt",
                                "MElectron_dr03TkSumPt",
                                "MElectron_dr03TkSumPtHEEP",
                                "MElectron_dxy",
                                "MElectron_dxyErr",
                                "MElectron_dz",
                                "MElectron_dzErr",
                                "MElectron_eInvMinusPInv",
                                "MElectron_energyErr",
                                "MElectron_etaMinusGen",
                                "MElectron_hoe",
                                "MElectron_ip3d",
                                "MElectron_isPFcand",
                                "MElectron_jetPtRelv2",
                                "MElectron_jetRelIso",
                                "MElectron_lostHits",
                                "MElectron_miniPFRelIso_all",
                                "MElectron_miniPFRelIso_chg",
                                "MElectron_mvaFall17V1Iso",
                                "MElectron_mvaFall17V1Iso_WP80",
                                "MElectron_mvaFall17V1Iso_WP90",
                                "MElectron_mvaFall17V1Iso_WPL",
                                "MElectron_mvaFall17V1noIso",
                                "MElectron_mvaFall17V1noIso_WP80",
                                "MElectron_mvaFall17V1noIso_WP90",
                                "MElectron_mvaFall17V1noIso_WPL",
                                "MElectron_mvaFall17V2Iso",
                                "MElectron_mvaFall17V2Iso_WP80",
                                "MElectron_mvaFall17V2Iso_WP90",
                                "MElectron_mvaFall17V2Iso_WPL",
                                "MElectron_mvaFall17V2noIso",
                                "MElectron_mvaFall17V2noIso_WP80",
                                "MElectron_mvaFall17V2noIso_WP90",
                                "MElectron_mvaFall17V2noIso_WPL",
                                "MElectron_mvaTTH",
                                "MElectron_pfRelIso03_all",
                                "MElectron_pfRelIso03_chg",
                                "MElectron_phiMinusGen",
                                "MElectron_ptRatio",
                                "MElectron_r9",
                                "MElectron_seedGain",
                                "MElectron_sieie",
                                "MElectron_sip3d",
                                "MElectron_tightCharge"};

  auto n_matched = matched.Histo1D("MElectron_ptRatio")->GetEntries();
  auto reco_tot = matched.Histo1D("Electron_pt")->GetEntries();

  cout << "matched: " << n_matched << endl;
  cout << "reco_tot: " << reco_tot << endl;

  matched.Snapshot("MElectrons", dataset_name.c_str(), col_to_save);
  cout << "Done" << endl;
}