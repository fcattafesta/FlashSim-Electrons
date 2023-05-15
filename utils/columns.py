ele_cond = [
    "GenElectron_eta",
    "GenElectron_phi",
    "GenElectron_pt",
    "GenElectron_charge",
    "GenElectron_statusFlag0",
    "GenElectron_statusFlag1",
    "GenElectron_statusFlag2",
    "GenElectron_statusFlag3",
    "GenElectron_statusFlag4",
    "GenElectron_statusFlag5",
    "GenElectron_statusFlag6",
    "GenElectron_statusFlag7",
    "GenElectron_statusFlag8",
    "GenElectron_statusFlag9",
    "GenElectron_statusFlag10",
    "GenElectron_statusFlag11",
    "GenElectron_statusFlag12",
    "GenElectron_statusFlag13",
    "GenElectron_statusFlag14",
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

eff_ele = [var.replace("C", "GC", 1) for var in ele_cond] + [
    "GenElectron_isReco"
]  # for efficiency

gen_ele = [var.replace("G", "MG", 1) for var in ele_cond]  # for flow

pho_cond = [
    "GenPhoton_eta",
    "GenPhoton_phi",
    "GenPhoton_pt",
    "GenPhoton_statusFlag0",
    "GenPhoton_statusFlag1",
    "GenPhoton_statusFlag2",
    "GenPhoton_statusFlag3",
    "GenPhoton_statusFlag4",
    "GenPhoton_statusFlag5",
    "GenPhoton_statusFlag6",
    "GenPhoton_statusFlag7",
    "GenPhoton_statusFlag8",
    "GenPhoton_statusFlag9",
    "GenPhoton_statusFlag10",
    "GenPhoton_statusFlag11",
    "GenPhoton_statusFlag12",
    "GenPhoton_statusFlag13",
    "GenPhoton_statusFlag14",
]

eff_pho = pho_cond + ["GenPhoton_isReco"]  # for efficiency

gen_pho = [var.replace("G", "MG", 1) for var in pho_cond]  # for flow

jet_cond = [
    "GenJet_eta",
    "GenJet_phi",
    "GenJet_pt",
    "GenJet_mass",
    "GenJet_EncodedPartonFlavour_light",
    "GenJet_EncodedPartonFlavour_gluon",
    "GenJet_EncodedPartonFlavour_c",
    "GenJet_EncodedPartonFlavour_b",
    "GenJet_EncodedPartonFlavour_undefined",
    "GenJet_EncodedHadronFlavour_b",
    "GenJet_EncodedHadronFlavour_c",
    "GenJet_EncodedHadronFlavour_light",
]

eff_jet = jet_cond + ["GenJet_isReco"]  # for efficiency

gen_jet = [var.replace("G", "MG", 1) for var in jet_cond]  # for flow

ele_names = [
    "convVeto",
    "deltaEtaSC",
    "dr03EcalRecHitSumEt",
    "dr03HcalDepth1TowerSumEt",
    "dr03TkSumPt",
    "dr03TkSumPtHEEP",
    "dxy",
    "dxyErr",
    "dz",
    "dzErr",
    "eInvMinusPInv",
    "energyErr",
    "eta",
    "hoe",
    "ip3d",
    "isPFcand",
    "jetPtRelv2",
    "jetRelIso",
    "lostHits",
    "miniPFRelIso_all",
    "miniPFRelIso_chg",
    # "mvaFall17V1Iso",
    # "mvaFall17V1Iso_WP80",
    # "mvaFall17V1Iso_WP90",
    # "mvaFall17V1Iso_WPL",
    # "mvaFall17V1noIso",
    # "mvaFall17V1noIso_WP80",
    # "mvaFall17V1noIso_WP90",
    # "mvaFall17V1noIso_WPL",
    "mvaFall17V2Iso",
    "mvaFall17V2Iso_WP80",
    "mvaFall17V2Iso_WP90",
    "mvaFall17V2Iso_WPL",
    "mvaFall17V2noIso",
    "mvaFall17V2noIso_WP80",
    "mvaFall17V2noIso_WP90",
    "mvaFall17V2noIso_WPL",
    "mvaTTH",
    "pfRelIso03_all",
    "pfRelIso03_chg",
    "phi",
    "pt",
    "r9",
    "seedGain",
    "sieie",
    "sip3d",
    "tightCharge",
    "charge",
]

reco_columns = [f"MElectron_{name}" for name in ele_names]

for i, name in enumerate(reco_columns):
    if name == "MElectron_pt":
        reco_columns[i] = "MElectron_ptRatio"
    elif name == "MElectron_phi":
        reco_columns[i] = "MElectron_phiMinusGen"
    elif name == "MElectron_eta":
        reco_columns[i] = "MElectron_etaMinusGen"


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
