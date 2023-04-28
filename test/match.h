auto GenEleMatch(float dr, float closest_dr, float pt_rel, float closest_pt_rel,
                 int pdgid, int status, int chg) {
  int num = pow(2, 13);
  int bAND = status & num;
  if (dr < closest_dr && pt_rel < closest_pt_rel && abs(pdgid) == 11 &&
      chg == -TMath::Sign(1, pdgid) && num == bAND) {
    return 1;
  }
  return 0;
}

template <typename T, typename U>
auto GenPart_ElectronIdx(
    ROOT::VecOps::RVec<float> &gen_pt, ROOT::VecOps::RVec<float> &gen_eta,
    ROOT::VecOps::RVec<float> &gen_phi, ROOT::VecOps::RVec<int> &gen_pdgid,
    ROOT::VecOps::RVec<int> &gen_status, ROOT::VecOps::RVec<T> &ele_pt,
    ROOT::VecOps::RVec<T> &ele_eta, ROOT::VecOps::RVec<T> &ele_phi,
    ROOT::VecOps::RVec<U> &ele_charge) {

  auto size_outer = gen_pt.size();
  auto size_inner = ele_pt.size();
  ROOT::VecOps::RVec<int> idx;
  idx.reserve(size_outer);

  for (auto i = 0; i < size_outer; i++) {
    auto closest_dr = 0.3;
    auto closest_pt_rel = 0.5;
    idx.emplace_back(-1);
    for (auto j = 0; j < size_inner; j++) {
      auto dpt_rel = abs(ele_pt[j] - gen_pt[i]) / gen_pt[i];
      auto deta = ele_eta[j] - gen_eta[i];
      auto dphi = TVector2::Phi_mpi_pi(ele_phi[j] - gen_phi[i]);
      auto dr = TMath::Sqrt(deta * deta + dphi * dphi);

      if (GenEleMatch(dr, closest_dr, dpt_rel, closest_pt_rel, gen_pdgid[i],
                      gen_status[i], ele_charge[j]) == 1) {
        closest_dr = dr;
        closest_pt_rel = dpt_rel;
        idx[i] = j;
      }
    }
  }
  return idx;
}