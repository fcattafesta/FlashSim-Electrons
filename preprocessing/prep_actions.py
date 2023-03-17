import numpy as np

"""
Dictionary of preprocessing operations for conditioning and target variables.
It is generated make_dataset function. Values of dictionary are list objects in which
sepcify preprocessing operation. Every operation has the following template

                       ["string", *pars]

where "string" tells which operation to perform and *pars its parameters. Such operations are

saturation: ["s", [inf, sup]]
gaussian smearing: ["g", sigma, [inf, sup]]
transformation: ["t", func, [a, b]]  # func(a * x + b)

In the case of multiple operations, order follows the operation list indexing.
"""

context_dictionary = {
    "MGenElectron_eta": [],
    "MGenElectron_phi": [],
    "MGenElectron_pt": [],
    "MGenElectron_charge": [],
    "MGenElectron_statusFlag0": [],
    "MGenElectron_statusFlag1": [],
    "MGenElectron_statusFlag2": [],
    "MGenElectron_statusFlag3": [],
    "MGenElectron_statusFlag4": [],
    "MGenElectron_statusFlag5": [],
    "MGenElectron_statusFlag6": [],
    "MGenElectron_statusFlag7": [],
    "MGenElectron_statusFlag8": [],
    "MGenElectron_statusFlag9": [],
    "MGenElectron_statusFlag10": [],
    "MGenElectron_statusFlag11": [],
    "MGenElectron_statusFlag12": [],
    "MGenElectron_statusFlag13": [],
    "MGenElectron_statusFlag14": [],
    "ClosestJet_dr": [],
    "ClosestJet_dphi": [],
    "ClosestJet_deta": [],
    "ClosestJet_pt": [],
    "ClosestJet_mass": [],
    "ClosestJet_EncodedPartonFlavour_light": [],
    "ClosestJet_EncodedPartonFlavour_gluon": [],
    "ClosestJet_EncodedPartonFlavour_c": [],
    "ClosestJet_EncodedPartonFlavour_b": [],
    "ClosestJet_EncodedPartonFlavour_undefined": [],
    "ClosestJet_EncodedHadronFlavour_b": [],
    "ClosestJet_EncodedHadronFlavour_c": [],
    "ClosestJet_EncodedHadronFlavour_light": [],
    "Pileup_gpudensity": [],
    "Pileup_nPU": [],
    "Pileup_nTrueInt": [],
    "Pileup_pudensity": [],
    "Pileup_sumEOOT": [],
    "Pileup_sumLOOT": [],
}

target_dictionary = {
    "MElectron_convVeto": [["u", 0.5, None]],
    "MElectron_deltaEtaSC": [],
    "MElectron_dr03EcalRecHitSumEt": [
        ["t", np.log, [1, 1e-3]],
        ["g", 1.3, [-np.inf, -2]],
    ],
    "MElectron_dr03HcalDepth1TowerSumEt": [
        ["t", np.log, [1, 1e-3]],
        ["g", 1.3, [-np.inf, -2]],
    ],
    "MElectron_dr03TkSumPt": [["t", np.log, [1, 1e-3]], ["g", 1.3, [-np.inf, -2]]],
    "MElectron_dr03TkSumPtHEEP": [["t", np.log, [1, 1e-3]], ["g", 1.3, [-np.inf, -2]]],
    "MElectron_dxy": [["t", np.arctan, [150, 0]]],
    "MElectron_dxyErr": [["t", np.log, [1, 1e-3]]],
    "MElectron_dz": [["t", np.arctan, [50, 0]]],
    "MElectron_dzErr": [["t", np.log, [1, 1e-3]]],
    "MElectron_eInvMinusPInv": [["t", np.arctan, [150, 0]]],
    "MElectron_energyErr": [["t", np.log1p, [1, 0]]],
    "MElectron_etaMinusGen": [["t", np.arctan, [100, 0]]],
    "MElectron_hoe": [["t", np.log, [1, 1e-3]], ["g", 0.5, [-np.inf, -6]]],
    "MElectron_ip3d": [["t", np.log, [1, 1e-3]]],
    "MElectron_isPFcand": [["u", 0.5, None]],
    "MElectron_jetPtRelv2": [["t", np.log1p, [1, 0]]],
    "MElectron_jetRelIso": [["t", np.log, [10, 1e-2]]],
    "MElectron_lostHits": [["u", 0.5, None]],
    "MElectron_miniPFRelIso_all": [
        ["t", np.log, [1, 1e-3]],
        ["g", 0.5, [-np.inf, -5.5]],
    ],
    "MElectron_miniPFRelIso_chg": [
        ["t", np.log, [1, 1e-3]],
        ["g", 0.5, [-np.inf, -5.5]],
    ],
    "MElectron_mvaFall17V1Iso": [],
    "MElectron_mvaFall17V1Iso_WP80": [["u", 0.5, None]],
    "MElectron_mvaFall17V1Iso_WP90": [["u", 0.5, None]],
    "MElectron_mvaFall17V1Iso_WPL": [["u", 0.5, None]],
    "MElectron_mvaFall17V1noIso": [],
    "MElectron_mvaFall17V1noIso_WP80": [["u", 0.5, None]],
    "MElectron_mvaFall17V1noIso_WP90": [["u", 0.5, None]],
    "MElectron_mvaFall17V1noIso_WPL": [["u", 0.5, None]],
    "MElectron_mvaFall17V2Iso": [],
    "MElectron_mvaFall17V2Iso_WP80": [["u", 0.5, None]],
    "MElectron_mvaFall17V2Iso_WP90": [["u", 0.5, None]],
    "MElectron_mvaFall17V2Iso_WPL": [["u", 0.5, None]],
    "MElectron_mvaFall17V2noIso": [],
    "MElectron_mvaFall17V2noIso_WP80": [["u", 0.5, None]],
    "MElectron_mvaFall17V2noIso_WP90": [["u", 0.5, None]],
    "MElectron_mvaFall17V2noIso_WPL": [["u", 0.5, None]],
    "MElectron_mvaTTH": [],
    "MElectron_pfRelIso03_all": [["t", np.log, [1, 1e-3]], ["g", 0.5, [-np.inf, -5.5]]],
    "MElectron_pfRelIso03_chg": [["t", np.log, [1, 1e-3]], ["g", 0.5, [-np.inf, -5.5]]],
    "MElectron_phiMinusGen": [["t", np.arctan, [80, 0]]],
    "MElectron_ptRatio": [["t", np.arctan, [10, -10]]],
    "MElectron_r9": [["t", np.log, [1, 1e-2]], ["t", np.arctan, [10, -0.15]]],
    "MElectron_seedGain": [["u", 0.5, None]],
    "MElectron_sieie": [["t", np.log, [10, 1e-1]], ["t", np.arctan, [1, -1.25]]],
    "MElectron_sip3d": [["t", np.log1p, [1, 0]]],
    "MElectron_tightCharge": [["u", 0.5, None]],
}
