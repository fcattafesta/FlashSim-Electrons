import os
import sys
import ROOT

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

from columns import ele_names, reco_columns

from variables import gen_ele, gen_pho, gen_jet

ROOT.gInterpreter.ProcessLine('#include "extraction.h"')


def jet_cleaning(d):
    cleaned = (
        d.Define("GenElectronMask", "abs(GenPart_pdgId) == 11")
        .Define("GenElectron_pt", "GenPart_pt[GenElectronMask]")
        .Define("GenElectron_eta", "GenPart_eta[GenElectronMask]")
        .Define("GenElectron_phi", "GenPart_phi[GenElectronMask]")
        .Define("GenMuonMask", "abs(GenPart_pdgId) == 13")
        .Define("GenMuon_pt", "GenPart_pt[GenMuonMask]")
        .Define("GenMuon_eta", "GenPart_eta[GenMuonMask]")
        .Define("GenMuon_phi", "GenPart_phi[GenMuonMask]")
        .Define(
            "CleanGenJet_mask_ele",
            "clean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, GenElectron_pt, GenElectron_eta, GenElectron_phi)",
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
            "static_cast<ROOT::VecOps::RVec<int>>(CleanGenJet_" "hadronFlavour_uchar)",
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
        .Define("MGenJetIdx", "Electron_genPart_JetIdx[MJetMask]")
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
        .Define("MGenJet_hadronFlavour", "Take(GenJet_hadronFlavour, MGenJetIdx)")
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

    d.Define("MElectron_ptRatio", "MElectron_pt / MGenElectron_pt")
    d.Define("MElectron_phiMinusGen", "DeltaPhi(MElectron_phi, MGenElectron_phi)")
    d.Define("MElectron_etaMinusGen", "MElectron_eta - MGenElectron_eta")

    return d


def make_file(inputname, outname):

    d = ROOT.RDataFrame("Events", inputname)

    d = jet_cleaning(d)
    d = match(d)

    d = ele_match(d)
    d = reco_match(d, "Electron_genObjMatch == 0")
    cols = gen_ele + reco_columns
    d.Snapshot("MElectrons", f"{outname}_ele.root", cols)

    d = pho_match(d)
    d = reco_match(d, "Electron_genObjMatch == 1")
    cols = gen_pho + reco_columns
    d.Snapshot("MElectrons", f"{outname}_pho.root", cols)

    d = jet_match(d)
    d = reco_match(d, "Electron_genObjMatch == 2")
    cols = gen_jet + reco_columns
    d.Snapshot("MElectrons", f"{outname}_jet.root", cols)
