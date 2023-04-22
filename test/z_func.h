#ifndef Z_FUNC_H
#define Z_FUNC_H

template <typename T>
auto InvariantMass(ROOT::VecOps::RVec<T> &pt, ROOT::VecOps::RVec<T> &eta,
                   ROOT::VecOps::RVec<T> &phi) {

  auto m = 0.51099895000e-3; // GeV

  ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], m);
  ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], m);

  return (p1 + p2).mass();
}

template <typename T>
auto Zpt(ROOT::VecOps::RVec<T> &pt, ROOT::VecOps::RVec<T> &eta,
         ROOT::VecOps::RVec<T> &phi) {

  auto m = 0.51099895000e-3; // GeV

  ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], m);
  ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], m);

  return (p1 + p2).pt();
}

#endif