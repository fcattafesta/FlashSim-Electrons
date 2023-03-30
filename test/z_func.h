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