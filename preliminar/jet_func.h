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

auto closest_jet_dr(ROOT::VecOps::RVec<float> &etaj,
                    ROOT::VecOps::RVec<float> &phij,
                    ROOT::VecOps::RVec<float> &etae,
                    ROOT::VecOps::RVec<float> &phie) {
  /* Calculates the DeltaR from the closest Jet object,
          if none present within 10, sets DR to 10
  */
  auto size_outer = etae.size();
  auto size_inner = etaj.size();
  ROOT::VecOps::RVec<float> distances;
  distances.reserve(size_outer);
  for (size_t i = 0; i < size_outer; i++) {
    distances.emplace_back(10);
    float closest = 10;
    for (size_t j = 0; j < size_inner; j++) {
      Double_t deta = etae[i] - etaj[j];
      Double_t dphi = TVector2::Phi_mpi_pi(phie[i] - phij[j]);
      float dr = TMath::Sqrt(deta * deta + dphi * dphi);
      if (dr < closest) {
        closest = dr;
      }
    }
    if (closest < 10) {
      distances[i] = closest;
    }
  }
  return distances;
}