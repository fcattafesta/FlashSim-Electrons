import ROOT
import numpy as np

ROOT.gInterpreter.ProcessLine('#include "jet_func.h"')

ROOT.EnableImplicitMT()


def matching(path):

    d = ROOT.RDataFrame("Events", path)

    # Cleaning GenJet collection from GenElectrons and GenMuons

    d_jet = (
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
            "clean_genjet_mask(GenJet_pt , GenJet_eta, GenJet_phi, GenElectron_pt, GenElectron_eta, GenElectron_phi)",
        )
        .Define(
            "CleanGenJet_mask_muon",
            "clean_genjet_mask(GenJet_pt, GenJet_eta, GenJet_phi, GenMuon_pt, GenMuon_eta, GenMuon_phi)",
        )
        .Define("CleanGenJetMask", "CleanGenJet_mask_ele && CleanGenJet_mask_muon")
        .Define("CleanGenJet_pt", "GenJet_pt[CleanGenJetMask]")
        .Define("CleanGenJet_eta", "GenJet_eta[CleanGenJetMask]")
        .Define("CleanGenJet_phi", "GenJet_phi[CleanGenJetMask]")
    )

    # Matching RecoElectron to GenPart

    d_part = (
        d.Define("MGenPartIdx", "Electron_genPartIdx[Electron_genPartIdx>=0]")
        .Define("MGenPart_pdgId", "Take(GenPart_pdgId, MGenPartIdx)")
        .Define("MGenElectronMask", "abs(MGenPart_pdgId) == 11")
        .Define("MGenElectronIdx", "MGenPartIdx[MGenElectronMask]")
        .Define("MGenElectron_pt", "Take(GenPart_pt, MGenElectronIdx)")
        .Define("MGenPhotonMask", "abs(MGenPart_pdgId) == 22")
        .Define("MGenPhotonIdx", "MGenPartIdx[MGenPhotonMask]")
        .Define("MGenPhoton_pt", "Take(GenPart_pt, MGenPhotonIdx)")
    )
    n_genele = d_part.Histo1D("MGenElectron_pt").GetEntries()
    n_genpho = d_part.Histo1D("MGenPhoton_pt").GetEntries()

    # Matching RecoElectron to GenJet

    d_jet_part = (
        d_jet.Define("UnmatchedGenPart_ElectronMask", "Electron_genPartIdx < 0")
        .Define("UGenPart_Electron_pt", "Electron_pt[UnmatchedGenPart_ElectronMask]")
        .Define("UGenPart_Electron_eta", "Electron_eta[UnmatchedGenPart_ElectronMask]")
        .Define("UGenPart_Electron_phi", "Electron_phi[UnmatchedGenPart_ElectronMask]")
        .Define(
            "ClosestGenJet_dr",
            "closest_jet_dr( CleanGenJet_eta, CleanGenJet_phi, UGenPart_Electron_eta, UGenPart_Electron_phi)",
        )
        .Define("MGenJetMask", "ClosestGenJet_dr < 0.4")
        .Define("MGenJet_Electron_pt", "UGenPart_Electron_pt[MGenJetMask]")
    )
    n_genjet = d_jet_part.Histo1D("MGenJet_Electron_pt").GetEntries()

    # Unmatched RecoElectron

    d_unmatched = d_jet_part.Define("UnmatchedElectronMask", "!MGenJetMask").Define(
        "UnmatchedElectron_pt", "UGenPart_Electron_pt[UnmatchedElectronMask]"
    )

    n_unmatched = d_unmatched.Histo1D("UnmatchedElectron_pt").GetEntries()

    h_unmatched_ele_pt = d_unmatched.Histo1D(
        ("", "", 10, 0, 50), "UnmatchedElectron_pt"
    )

    h_ele_pt = d.Histo1D(("", "", 10, 0, 50), "Electron_pt")

    h_norm_unmatched_ele_pt = ROOT.TH1D("", "", 10, 0, 50)

    for i in range(1, 11):
        h_norm_unmatched_ele_pt.SetBinContent(
            i, h_unmatched_ele_pt.GetBinContent(i) / h_ele_pt.GetBinContent(i)
        )

    # h_norm_unmatched_ele_pt.DrawCopy()
    # input()

    n_ele = h_ele_pt.GetEntries()

    # print(f"Matched RECO/GenElectron: {n_genele/n_ele}")
    # print(f"Matched RECO/GenPhoton: {n_genpho/n_ele}")
    # print(f"Matched RECO/GenJet: {n_genjet/n_ele}")
    # print(f"Unmatched RECO: {n_unmatched/n_ele}")

    return np.array([n_genele, n_genpho, n_genjet, n_unmatched, n_ele])


if __name__ == "__main__":

    paths = ["047F4368-97D4-1A4E-B896-23C6C72DD2BE.root"]

    n = np.zeros(5)
    for path in paths:
        n = n + matching(path)

    fraction_matched = n[0:4] / n[4]

    dict = {
        "Matched_RECO/GenElectron": fraction_matched[0],
        "Matched_RECO/GenPhoton": fraction_matched[1],
        "Matched_RECO/GenJet": fraction_matched[2],
        "Unmatched_RECO": fraction_matched[3],
    }

    print(dict)
