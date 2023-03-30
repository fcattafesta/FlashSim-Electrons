import os
import sys
import ROOT

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

from columns import (
    ele_names,
    reco_columns,
    gen_ele,
    gen_pho,
    gen_jet,
    eff_ele,
    eff_pho,
    eff_jet,
)

ROOT.gInterpreter.ProcessLine('#include "extraction.h"')


def jet_cleaning(d):
    cleaned = (
        d.Define("TMPGenElectronMask", "abs(GenPart_pdgId) == 11")
        .Define("TMPGenElectron_pt", "GenPart_pt[TMPGenElectronMask]")
        .Define("TMPGenElectron_eta", "GenPart_eta[TMPGenElectronMask]")
        .Define("TMPGenElectron_phi", "GenPart_phi[TMPGenElectronMask]")
        .Define("GenMuonMask", "abs(GenPart_pdgId) == 13")
        .Define("GenMuon_pt", "GenPart_pt[GenMuonMask]")
        .Define("GenMuon_eta", "GenPart_eta[GenMuonMask]")
        .Define("GenMuon_phi", "GenPart_phi[GenMuonMask]")
        .Define(
            "CleanGenJet_mask_ele",
            "clean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, TMPGenElectron_pt, TMPGenElectron_eta, TMPGenElectron_phi)",
        )
        .Define(
            "CleanGenJet_mask_muon",
            "clean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, GenMuon_pt, GenMuon_eta, GenMuon_phi)",
        )
        .Define("CleanGenJetMask", "CleanGenJet_mask_ele && CleanGenJet_mask_muon")
        .Define("CleanGenJet_pt", "GenJet_pt[CleanGenJetMask]")
        .Define("CleanGenJet_eta", "GenJet_eta[CleanGenJetMask]")
        .Define("CleanGenJet_phi", "GenJet_phi[CleanGenJetMask]")
        .Define("CleanGenJet_mass", "GenJet_mass[CleanGenJetMask]")
        .Define(
            "CleanGenJet_hadronFlavour_uchar", "GenJet_hadronFlavour[CleanGenJetMask]"
        )
        .Define(
            "CleanGenJet_hadronFlavour",
            "static_cast<ROOT::VecOps::RVec<int>>(CleanGenJet_hadronFlavour_uchar)",
        )
        .Define("CleanGenJet_partonFlavour", "GenJet_partonFlavour[CleanGenJetMask]")
    )

    return cleaned


def match(cleaned):
    matched = (
        cleaned.Define(
            "Electron_genObjMatch_empty", "Electron_genObjMatchMaker(Electron_pt)"
        )
        .Define(
            "Electron_genObjMatch_ele",
            "Electron_genObjMatch(GenPart_pt, GenPart_eta, GenPart_phi, Electron_pt, Electron_eta, Electron_phi,  Electron_genObjMatch_empty, 0, GenPart_pdgId, GenPart_statusFlags, CleanGenJetMask, Electron_charge)",
        )
        .Define(
            "Electron_genObjMatch_photon",
            "Electron_genObjMatch(GenPart_pt, GenPart_eta, GenPart_phi, Electron_pt, Electron_eta, Electron_phi,  Electron_genObjMatch_ele, 1, GenPart_pdgId, GenPart_statusFlags, CleanGenJetMask, Electron_charge)",
        )
        .Define(
            "Electron_genObjMatch",
            "Electron_genObjMatch(GenJet_pt, GenJet_eta, GenJet_phi, Electron_pt, Electron_eta, Electron_phi,  Electron_genObjMatch_photon, 2, GenPart_pdgId, GenPart_statusFlags, CleanGenJetMask, Electron_charge)",
        )
        .Define(
            "Electron_genPart_ElectronIdx",
            "Electron_genObjIdx(GenPart_pt, GenPart_eta, GenPart_phi, Electron_pt, Electron_eta, Electron_phi, 0, GenPart_pdgId, GenPart_statusFlags, CleanGenJetMask, Electron_charge)",
        )
        .Define(
            "Electron_genPart_PhotonIdx",
            "Electron_genObjIdx(GenPart_pt, GenPart_eta, GenPart_phi, Electron_pt, Electron_eta, Electron_phi, 1, GenPart_pdgId, GenPart_statusFlags, CleanGenJetMask, Electron_charge)",
        )
        .Define(
            "Electron_genJetIdx",
            "Electron_genObjIdx(GenJet_pt, GenJet_eta, GenJet_phi, Electron_pt, Electron_eta, Electron_phi, 2, GenPart_pdgId, GenPart_statusFlags, CleanGenJetMask, Electron_charge)",
        )
    )

    return matched


def ele_match(matched):
    ele_matched = (
        matched.Define("MElectronMask", "Electron_genObjMatch == 0")
        .Define("MGenElectronIdx", "Electron_genPart_ElectronIdx[MElectronMask]")
        .Define("MGenElectron_pt", "Take(GenPart_pt, MGenElectronIdx)")
        .Define("MGenElectron_eta", "Take(GenPart_eta, MGenElectronIdx)")
        .Define("MGenElectron_phi", "Take(GenPart_phi, MGenElectronIdx)")
        .Define("MGenElectron_pdgId", "Take(GenPart_pdgId, MGenElectronIdx)")
        .Define("MGenElectron_charge", "charge(MGenElectron_pdgId)")
        .Define(
            "MGenElectron_statusFlags", "Take(GenPart_statusFlags, MGenElectronIdx)"
        )
        .Define(
            "MGenElectron_statusFlag0", "BitwiseDecoder(MGenElectron_statusFlags, 0)"
        )
        .Define(
            "MGenElectron_statusFlag1", "BitwiseDecoder(MGenElectron_statusFlags, 1)"
        )
        .Define(
            "MGenElectron_statusFlag2", "BitwiseDecoder(MGenElectron_statusFlags, 2)"
        )
        .Define(
            "MGenElectron_statusFlag3", "BitwiseDecoder(MGenElectron_statusFlags, 3)"
        )
        .Define(
            "MGenElectron_statusFlag4", "BitwiseDecoder(MGenElectron_statusFlags, 4)"
        )
        .Define(
            "MGenElectron_statusFlag5", "BitwiseDecoder(MGenElectron_statusFlags, 5)"
        )
        .Define(
            "MGenElectron_statusFlag6", "BitwiseDecoder(MGenElectron_statusFlags, 6)"
        )
        .Define(
            "MGenElectron_statusFlag7", "BitwiseDecoder(MGenElectron_statusFlags, 7)"
        )
        .Define(
            "MGenElectron_statusFlag8", "BitwiseDecoder(MGenElectron_statusFlags, 8)"
        )
        .Define(
            "MGenElectron_statusFlag9", "BitwiseDecoder(MGenElectron_statusFlags, 9)"
        )
        .Define(
            "MGenElectron_statusFlag10", "BitwiseDecoder(MGenElectron_statusFlags, 10)"
        )
        .Define(
            "MGenElectron_statusFlag11", "BitwiseDecoder(MGenElectron_statusFlags, 11)"
        )
        .Define(
            "MGenElectron_statusFlag12", "BitwiseDecoder(MGenElectron_statusFlags, 12)"
        )
        .Define(
            "MGenElectron_statusFlag13", "BitwiseDecoder(MGenElectron_statusFlags, 13)"
        )
        .Define(
            "MGenElectron_statusFlag14", "BitwiseDecoder(MGenElectron_statusFlags, 14)"
        )
        .Define(
            "ClosestJet_dr",
            "closest_jet_dr(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi)",
        )
        .Define(
            "ClosestJet_dphi",
            "closest_jet_dphi(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi)",
        )
        .Define(
            "ClosestJet_deta",
            "closest_jet_deta(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi)",
        )
        .Define(
            "ClosestJet_pt",
            "closest_jet_pt(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_pt)",
        )
        .Define(
            "ClosestJet_mass",
            "closest_jet_mass(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_mass)",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_light",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{1,2,3})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_gluon",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_c",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_b",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "ClosestJet_EncodedPartonFlavour_undefined",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_b",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_c",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "ClosestJet_EncodedHadronFlavour_light",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, MGenElectron_eta, MGenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{0})",
        )
    )

    return ele_matched


def pho_match(matched):
    pho_matched = (
        matched.Define("MPhotonMask", "Electron_genObjMatch == 1")
        .Define("MGenPhotonIdx", "Electron_genPart_PhotonIdx[MPhotonMask]")
        .Define("MGenPhoton_pt", "Take(GenPart_pt, MGenPhotonIdx)")
        .Define("MGenPhoton_eta", "Take(GenPart_eta, MGenPhotonIdx)")
        .Define("MGenPhoton_phi", "Take(GenPart_phi, MGenPhotonIdx)")
        .Define("MGenPhoton_statusFlags", "Take(GenPart_statusFlags, MGenPhotonIdx)")
        .Define("MGenPhoton_statusFlag0", "BitwiseDecoder(MGenPhoton_statusFlags, 0)")
        .Define("MGenPhoton_statusFlag1", "BitwiseDecoder(MGenPhoton_statusFlags, 1)")
        .Define("MGenPhoton_statusFlag2", "BitwiseDecoder(MGenPhoton_statusFlags, 2)")
        .Define("MGenPhoton_statusFlag3", "BitwiseDecoder(MGenPhoton_statusFlags, 3)")
        .Define("MGenPhoton_statusFlag4", "BitwiseDecoder(MGenPhoton_statusFlags, 4)")
        .Define("MGenPhoton_statusFlag5", "BitwiseDecoder(MGenPhoton_statusFlags, 5)")
        .Define("MGenPhoton_statusFlag6", "BitwiseDecoder(MGenPhoton_statusFlags, 6)")
        .Define("MGenPhoton_statusFlag7", "BitwiseDecoder(MGenPhoton_statusFlags, 7)")
        .Define("MGenPhoton_statusFlag8", "BitwiseDecoder(MGenPhoton_statusFlags, 8)")
        .Define("MGenPhoton_statusFlag9", "BitwiseDecoder(MGenPhoton_statusFlags, 9)")
        .Define("MGenPhoton_statusFlag10", "BitwiseDecoder(MGenPhoton_statusFlags, 10)")
        .Define("MGenPhoton_statusFlag11", "BitwiseDecoder(MGenPhoton_statusFlags, 11)")
        .Define("MGenPhoton_statusFlag12", "BitwiseDecoder(MGenPhoton_statusFlags, 12)")
        .Define("MGenPhoton_statusFlag13", "BitwiseDecoder(MGenPhoton_statusFlags, 13)")
        .Define("MGenPhoton_statusFlag14", "BitwiseDecoder(MGenPhoton_statusFlags, 14)")
    )

    return pho_matched


def jet_match(matched):
    jet_matched = (
        matched.Define("MJetMask", "Electron_genObjMatch == 2")
        .Define("MGenJetIdx", "Electron_genJetIdx[MJetMask]")
        .Define("MGenJet_pt", "Take(GenJet_pt, MGenJetIdx)")
        .Define("MGenJet_eta", "Take(GenJet_eta, MGenJetIdx)")
        .Define("MGenJet_phi", "Take(GenJet_phi, MGenJetIdx)")
        .Define("MGenJet_mass", "Take(GenJet_mass, MGenJetIdx)")
        .Define("MGenJet_partonFlavour", "Take(GenJet_partonFlavour, MGenJetIdx)")
        .Define(
            "MGenJet_EncodedPartonFlavour_light",
            "flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{1, 2, 3})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_gluon",
            "flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_c",
            "flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_b",
            "flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "MGenJet_EncodedPartonFlavour_undefined",
            "flavour_encoder(MGenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define("MGenJet_hadronFlavour_uchar", "Take(GenJet_hadronFlavour, MGenJetIdx)")
        .Define(
            "MGenJet_hadronFlavour",
            "static_cast<ROOT::VecOps::RVec<int>>(MGenJet_hadronFlavour_uchar)",
        )
        .Define(
            "MGenJet_EncodedHadronFlavour_b",
            "flavour_encoder(MGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "MGenJet_EncodedHadronFlavour_c",
            "flavour_encoder(MGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "MGenJet_EncodedHadronFlavour_light",
            "flavour_encoder(MGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{0})",
        )
    )
    return jet_matched


def reco_match(d, mask):
    ops = [f"Electron_{var}[{mask}]" for var in ele_names]
    names = [f"MElectron_{var}" for var in ele_names]

    for op, name in zip(ops, names):
        d = d.Define(name, op)

    if mask == "Electron_genObjMatch == 0":
        d = (
            d.Define("MElectron_ptRatio", "MElectron_pt / MGenElectron_pt")
            .Define(
                "MElectron_phiMinusGen", "DeltaPhi(MElectron_phi, MGenElectron_phi)"
            )
            .Define("MElectron_etaMinusGen", "MElectron_eta - MGenElectron_eta")
        )
    elif mask == "Electron_genObjMatch == 1":
        d = (
            d.Define("MElectron_ptRatio", "MElectron_pt / MGenPhoton_pt")
            .Define("MElectron_phiMinusGen", "DeltaPhi(MElectron_phi, MGenPhoton_phi)")
            .Define("MElectron_etaMinusGen", "MElectron_eta - MGenPhoton_eta")
        )
    elif mask == "Electron_genObjMatch == 2":
        d = (
            d.Define("MElectron_ptRatio", "MElectron_pt / MGenJet_pt")
            .Define("MElectron_phiMinusGen", "DeltaPhi(MElectron_phi, MGenJet_phi)")
            .Define("MElectron_etaMinusGen", "MElectron_eta - MGenJet_eta")
        )

    return d


def gen_to_reco(cleaned):
    matched = (
        cleaned.Define(
            "GenPart_ElectronIdx_empty", "Electron_genObjMatchMaker(GenPart_pt)"
        )
        .Define(
            "GenPart_genElectron_ElectronIdx",
            "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, Electron_pt, Electron_eta, Electron_phi, Electron_charge, GenPart_ElectronIdx_empty, 0)",
        )
        .Define(
            "GenPart_all_ElectronIdx",
            "GenPart_ElectronIdx(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_statusFlags, Electron_pt, Electron_eta, Electron_phi, Electron_charge, GenPart_genElectron_ElectronIdx, 1)",
        )
        .Define(
            "GenJet_ElectronIdx",
            "GenJet_ElectronIdx(GenJet_pt, GenJet_eta, GenJet_phi, CleanGenJetMask, Electron_pt, Electron_eta, Electron_phi, GenPart_all_ElectronIdx)",
        )
    )

    return matched


def ele_ele(matched):
    to_reco = (
        matched.Define(
            "GenElectronMask",
            "abs(GenPart_pdgId) == 11",
        )
        .Define(
            "GenElectron_isReco",
            "GenPart_genElectron_ElectronIdx[GenElectronMask] >= 0",
        )
        .Define("GenElectron_pt", "GenPart_pt[GenElectronMask]")
        .Define("GenElectron_eta", "GenPart_eta[GenElectronMask]")
        .Define("GenElectron_phi", "GenPart_phi[GenElectronMask]")
        .Define("GenElectron_pdgId", "GenPart_pdgId[GenElectronMask]")
        .Define("GenElectron_charge", "charge(GenElectron_pdgId)")
        .Define("GenElectron_statusFlags", "GenPart_statusFlags[GenElectronMask]")
        .Define("GenElectron_statusFlag0", "BitwiseDecoder(GenElectron_statusFlags, 0)")
        .Define("GenElectron_statusFlag1", "BitwiseDecoder(GenElectron_statusFlags, 1)")
        .Define("GenElectron_statusFlag2", "BitwiseDecoder(GenElectron_statusFlags, 2)")
        .Define("GenElectron_statusFlag3", "BitwiseDecoder(GenElectron_statusFlags, 3)")
        .Define("GenElectron_statusFlag4", "BitwiseDecoder(GenElectron_statusFlags, 4)")
        .Define("GenElectron_statusFlag5", "BitwiseDecoder(GenElectron_statusFlags, 5)")
        .Define("GenElectron_statusFlag6", "BitwiseDecoder(GenElectron_statusFlags, 6)")
        .Define("GenElectron_statusFlag7", "BitwiseDecoder(GenElectron_statusFlags, 7)")
        .Define("GenElectron_statusFlag8", "BitwiseDecoder(GenElectron_statusFlags, 8)")
        .Define("GenElectron_statusFlag9", "BitwiseDecoder(GenElectron_statusFlags, 9)")
        .Define(
            "GenElectron_statusFlag10", "BitwiseDecoder(GenElectron_statusFlags, 10)"
        )
        .Define(
            "GenElectron_statusFlag11", "BitwiseDecoder(GenElectron_statusFlags, 11)"
        )
        .Define(
            "GenElectron_statusFlag12", "BitwiseDecoder(GenElectron_statusFlags, 12)"
        )
        .Define(
            "GenElectron_statusFlag13", "BitwiseDecoder(GenElectron_statusFlags, 13)"
        )
        .Define(
            "GenElectron_statusFlag14", "BitwiseDecoder(GenElectron_statusFlags, 14)"
        )
        .Define(
            "GClosestJet_dr",
            "closest_jet_dr(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi)",
        )
        .Define(
            "GClosestJet_dphi",
            "closest_jet_dphi(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi)",
        )
        .Define(
            "GClosestJet_deta",
            "closest_jet_deta(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi)",
        )
        .Define(
            "GClosestJet_pt",
            "closest_jet_pt(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_pt)",
        )
        .Define(
            "GClosestJet_mass",
            "closest_jet_mass(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_mass)",
        )
        .Define(
            "GClosestJet_EncodedPartonFlavour_light",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{1,2,3})",
        )
        .Define(
            "GClosestJet_EncodedPartonFlavour_gluon",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "GClosestJet_EncodedPartonFlavour_c",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "GClosestJet_EncodedPartonFlavour_b",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "GClosestJet_EncodedPartonFlavour_undefined",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define(
            "GClosestJet_EncodedHadronFlavour_b",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "GClosestJet_EncodedHadronFlavour_c",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "GClosestJet_EncodedHadronFlavour_light",
            "closest_jet_flavour_encoder(CleanGenJet_eta, CleanGenJet_phi, GenElectron_eta, GenElectron_phi, CleanGenJet_hadronFlavour, ROOT::VecOps::RVec<int>{0})",
        )
    )

    return to_reco


def pho_ele(matched):
    to_reco = (
        matched.Define(
            "GenPhotonMask",
            "GenPart_pdgId == 22",
        )
        .Define("GenPhoton_isReco", "GenPart_all_ElectronIdx[GenPhotonMask] >= 0")
        .Define("GenPhoton_pt", "GenPart_pt[GenPhotonMask]")
        .Define("GenPhoton_eta", "GenPart_eta[GenPhotonMask]")
        .Define("GenPhoton_phi", "GenPart_phi[GenPhotonMask]")
        .Define("GenPhoton_statusFlags", "GenPart_statusFlags[GenPhotonMask]")
        .Define("GenPhoton_statusFlag0", "BitwiseDecoder(GenPhoton_statusFlags, 0)")
        .Define("GenPhoton_statusFlag1", "BitwiseDecoder(GenPhoton_statusFlags, 1)")
        .Define("GenPhoton_statusFlag2", "BitwiseDecoder(GenPhoton_statusFlags, 2)")
        .Define("GenPhoton_statusFlag3", "BitwiseDecoder(GenPhoton_statusFlags, 3)")
        .Define("GenPhoton_statusFlag4", "BitwiseDecoder(GenPhoton_statusFlags, 4)")
        .Define("GenPhoton_statusFlag5", "BitwiseDecoder(GenPhoton_statusFlags, 5)")
        .Define("GenPhoton_statusFlag6", "BitwiseDecoder(GenPhoton_statusFlags, 6)")
        .Define("GenPhoton_statusFlag7", "BitwiseDecoder(GenPhoton_statusFlags, 7)")
        .Define("GenPhoton_statusFlag8", "BitwiseDecoder(GenPhoton_statusFlags, 8)")
        .Define("GenPhoton_statusFlag9", "BitwiseDecoder(GenPhoton_statusFlags, 9)")
        .Define("GenPhoton_statusFlag10", "BitwiseDecoder(GenPhoton_statusFlags, 10)")
        .Define("GenPhoton_statusFlag11", "BitwiseDecoder(GenPhoton_statusFlags, 11)")
        .Define("GenPhoton_statusFlag12", "BitwiseDecoder(GenPhoton_statusFlags, 12)")
        .Define("GenPhoton_statusFlag13", "BitwiseDecoder(GenPhoton_statusFlags, 13)")
        .Define("GenPhoton_statusFlag14", "BitwiseDecoder(GenPhoton_statusFlags, 14)")
    )

    return to_reco


def jet_ele(matched):
    to_reco = (
        matched.Define("GenJet_isReco", "GenJet_ElectronIdx >= 0")
        .Define(
            "GenJet_EncodedPartonFlavour_light",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{1,2,3})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_gluon",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{21})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_c",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_b",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "GenJet_EncodedPartonFlavour_undefined",
            "flavour_encoder(GenJet_partonFlavour, ROOT::VecOps::RVec<int>{0})",
        )
        .Define("GenJet_hadronFlavour_uchar", "GenJet_hadronFlavour")
        .Define(
            "GenJet_hadronFlavour_int",
            "static_cast<ROOT::VecOps::RVec<int>>(GenJet_hadronFlavour_uchar)",
        )
        .Define(
            "GenJet_EncodedHadronFlavour_b",
            "flavour_encoder(GenJet_hadronFlavour_int, ROOT::VecOps::RVec<int>{5})",
        )
        .Define(
            "GenJet_EncodedHadronFlavour_c",
            "flavour_encoder(GenJet_hadronFlavour_int, ROOT::VecOps::RVec<int>{4})",
        )
        .Define(
            "GenJet_EncodedHadronFlavour_light",
            "flavour_encoder(GenJet_hadronFlavour_int, ROOT::VecOps::RVec<int>{0})",
        )
    )

    return to_reco


def make_files(inputname, outname, dict):

    ROOT.EnableImplicitMT()

    print(f"Processing {inputname}...")

    d = ROOT.RDataFrame("Events", inputname)

    d = jet_cleaning(d)
    d = match(d)
    d = gen_to_reco(d)

    ele = ele_match(d)
    ele = reco_match(ele, "Electron_genObjMatch == 0")
    ele = ele_ele(ele)

    n_reco_match, n_reco = dict["RECOELE_GENELE"]

    n_reco_match += ele.Histo1D("MElectron_ptRatio").GetEntries()
    n_reco += ele.Histo1D("Electron_pt").GetEntries()

    dict["RECOELE_GENELE"] = (n_reco_match, n_reco)

    n_gen_match, n_gen = dict["GENELE_RECOELE"]

    n_gen_match += (
        ele.Define("tmp", "GenElectron_pt[GenElectron_isReco]")
        .Histo1D("tmp")
        .GetEntries()
    )
    n_gen += ele.Histo1D("GenElectron_pt").GetEntries()

    dict["GENELE_RECOELE"] = (n_gen_match, n_gen)

    cols = gen_ele + reco_columns + eff_ele
    ele.Snapshot("MElectrons", f"{outname}_ele.root", cols)

    print(f"{outname}_ele.root saved")

    pho = pho_match(d)
    pho = reco_match(pho, "Electron_genObjMatch == 1")
    pho = pho_ele(pho)

    n_reco_match, _ = dict["RECOELE_GENPHO"]

    n_reco_match += pho.Histo1D("MElectron_ptRatio").GetEntries()

    dict["RECOELE_GENPHO"] = (n_reco_match, n_reco)

    n_gen_match, n_gen = dict["GENPHO_RECOELE"]

    n_gen_match += (
        pho.Define("tmp", "GenPhoton_pt[GenPhoton_isReco]").Histo1D("tmp").GetEntries()
    )
    n_gen += pho.Histo1D("GenPhoton_pt").GetEntries()

    dict["GENPHO_RECOELE"] = (n_gen_match, n_gen)

    cols = gen_pho + reco_columns + eff_pho
    pho.Snapshot("MElectrons", f"{outname}_pho.root", cols)

    print(f"{outname}_pho.root saved")

    jet = jet_match(d)
    jet = reco_match(jet, "Electron_genObjMatch == 2")
    jet = jet_ele(jet)

    n_reco_match, _ = dict["RECOELE_GENJET"]

    n_reco_match += jet.Histo1D("MElectron_ptRatio").GetEntries()

    dict["RECOELE_GENJET"] = (n_reco_match, n_reco)

    n_gen_match, n_gen = dict["GENJET_RECOELE"]

    n_gen_match += (
        jet.Define("tmp", "GenJet_pt[GenJet_isReco]").Histo1D("tmp").GetEntries()
    )
    n_gen += jet.Histo1D("GenJet_pt").GetEntries()

    dict["GENJET_RECOELE"] = (n_gen_match, n_gen)

    cols = gen_jet + reco_columns + eff_jet
    jet.Snapshot("MElectrons", f"{outname}_jet.root", cols)

    print(f"{outname}_jet.root saved")
