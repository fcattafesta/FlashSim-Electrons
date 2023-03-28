gen_ele = [
    "MGenElectron_eta",
    "MGenElectron_phi",
    "MGenElectron_pt",
    "MGenElectron_charge",
    "MGenElectron_statusFlag0",
    "MGenElectron_statusFlag1",
    "MGenElectron_statusFlag2",
    "MGenElectron_statusFlag3",
    "MGenElectron_statusFlag4",
    "MGenElectron_statusFlag5",
    "MGenElectron_statusFlag6",
    "MGenElectron_statusFlag7",
    "MGenElectron_statusFlag8",
    "MGenElectron_statusFlag9",
    "MGenElectron_statusFlag10",
    "MGenElectron_statusFlag11",
    "MGenElectron_statusFlag12",
    "MGenElectron_statusFlag13",
    "MGenElectron_statusFlag14",
    "ClosestJet_dr",
    "ClosestJet_dphi",
    "ClosestJet_deta",
    "ClosestJet_pt",
    "ClosestJet_mass",
    "ClosestJet_EncodedPartonFlavour_light",
    "ClosestJet_EncodedPartonFlavour_gluon",
    "ClosestJet_EncodedPartonFlavour_c",
    "ClosestJet_EncodedPartonFlavour_b",
    "ClosestJet_EncodedPartonFlavour_undefined",
    "ClosestJet_EncodedHadronFlavour_b",
    "ClosestJet_EncodedHadronFlavour_c",
    "ClosestJet_EncodedHadronFlavour_light",
]

eff_ele = [var.replace("M", "", 1) for var in gen_ele if var.startswith("M")]

gen_pho = [
    "MGenPhoton_eta",
    "MGenPhoton_phi",
    "MGenPhoton_pt",
    "MGenPhoton_statusFlag0",
    "MGenPhoton_statusFlag1",
    "MGenPhoton_statusFlag2",
    "MGenPhoton_statusFlag3",
    "MGenPhoton_statusFlag4",
    "MGenPhoton_statusFlag5",
    "MGenPhoton_statusFlag6",
    "MGenPhoton_statusFlag7",
    "MGenPhoton_statusFlag8",
    "MGenPhoton_statusFlag9",
    "MGenPhoton_statusFlag10",
    "MGenPhoton_statusFlag11",
    "MGenPhoton_statusFlag12",
    "MGenPhoton_statusFlag13",
    "MGenPhoton_statusFlag14",
]

eff_pho = [var.replace("M", "", 1) for var in gen_pho if var.startswith("M")]

gen_jet = [
    "MGenJet_eta",
    "MGenJet_phi",
    "MGenJet_pt",
    "MGenJet_mass",
    "MGenJet_EncodedPartonFlavour_light",
    "MGenJet_EncodedPartonFlavour_gluon",
    "MGenJet_EncodedPartonFlavour_c",
    "MGenJet_EncodedPartonFlavour_b",
    "MGenJet_EncodedPartonFlavour_undefined",
    "MGenJet_EncodedHadronFlavour_b",
    "MGenJet_EncodedHadronFlavour_c",
    "MGenJet_EncodedHadronFlavour_light",
]

eff_jet = [var.replace("M", "", 1) for var in gen_jet if var.startswith("M")]

pu = [
    "Pileup_gpudensity",
    "Pileup_nPU",
    "Pileup_nTrueInt",
    "Pileup_pudensity",
    "Pileup_sumEOOT",
    "Pileup_sumLOOT",
]

gen_ele = gen_ele + pu
gen_pho = gen_pho + pu
gen_jet = gen_jet + pu
