import numpy as np

"""
Dictionary of postprocessing operations for conditioning and target variables.
It is generated make_dataset function. Values of dictionary are list objects in which
sepcify preprocessing operation. Every operation has the following template

                       ["string", *pars]

where "string" tells which operation to perform and *pars its parameters. Such operations are

unsmearing: ["d", [inf, sup]]
transformation: ["i", func, [a, b]]  # func(x - b) / a

In the case of multiple operations, order follows the operation list indexing.
"""

target_dictionary = {
    "MElectron_charge": [["c", 0, [-1, 1]]],
    "MElectron_convVeto": [["d", None]],
    "MElectron_deltaEtaSC": [["i", np.tan, [10, 0]]],
    "MElectron_dr03EcalRecHitSumEt": [["d", [-np.inf, -2]], ["i", np.exp, [1, 1e-3]]],
    "MElectron_dr03HcalDepth1TowerSumEt": [
        ["d", [-np.inf, -2]],
        ["i", np.exp, [1, 1e-3]],
    ],
    "MElectron_dr03TkSumPt": [["d", [-np.inf, -2]], ["i", np.exp, [1, 1e-3]]],
    "MElectron_dr03TkSumPtHEEP": [["d", [-np.inf, -2]], ["i", np.exp, [1, 1e-3]]],
    "MElectron_dxy": [["i", np.tan, [10, 0]]],
    "MElectron_dxyErr": [["i", np.exp, [1, 1e-3]]],
    "MElectron_dz": [["i", np.tan, [10, 0]]],
    "MElectron_dzErr": [["i", np.exp, [1, 1e-3]]],
    "MElectron_eInvMinusPInv": [["i", np.tan, [10, 0]]],
    "MElectron_energyErr": [["i", np.expm1, [1, 0]]],
    "MElectron_etaMinusGen": [["i", np.tan, [10, 0]]],
    "MElectron_hoe": [["d", [-np.inf, -6]], ["i", np.exp, [1, 1e-3]]],
    "MElectron_ip3d": [["i", np.exp, [1, 1e-3]]],
    "MElectron_isPFcand": [["d", None]],
    "MElectron_jetPtRelv2": [["i", np.expm1, [1, 0]]],
    "MElectron_jetRelIso": [["i", np.exp, [10, 1e-2]]],
    "MElectron_lostHits": [["d", None]],
    "MElectron_miniPFRelIso_all": [["d", [-np.inf, -5.5]], ["i", np.exp, [1, 1e-3]]],
    "MElectron_miniPFRelIso_chg": [["d", [-np.inf, -5.5]], ["i", np.exp, [1, 1e-3]]],
    "MElectron_mvaFall17V1Iso": [],
    "MElectron_mvaFall17V1Iso_WP80": [["d", None]],
    "MElectron_mvaFall17V1Iso_WP90": [["d", None]],
    "MElectron_mvaFall17V1Iso_WPL": [["d", None]],
    "MElectron_mvaFall17V1noIso": [],
    "MElectron_mvaFall17V1noIso_WP80": [["d", None]],
    "MElectron_mvaFall17V1noIso_WP90": [["d", None]],
    "MElectron_mvaFall17V1noIso_WPL": [["d", None]],
    "MElectron_mvaFall17V2Iso": [],
    "MElectron_mvaFall17V2Iso_WP80": [["d", None]],
    "MElectron_mvaFall17V2Iso_WP90": [["d", None]],
    "MElectron_mvaFall17V2Iso_WPL": [["d", None]],
    "MElectron_mvaFall17V2noIso": [],
    "MElectron_mvaFall17V2noIso_WP80": [["d", None]],
    "MElectron_mvaFall17V2noIso_WP90": [["d", None]],
    "MElectron_mvaFall17V2noIso_WPL": [["d", None]],
    "MElectron_mvaTTH": [],
    "MElectron_pfRelIso03_all": [
        ["d", [-np.inf, -5.5]],
        ["i", np.exp, [1, 1e-3]],
    ],
    "MElectron_pfRelIso03_chg": [["d", [-np.inf, -5.5]], ["i", np.exp, [1, 1e-3]]],
    "MElectron_phiMinusGen": [["i", np.tan, [10, 0]]],
    "MElectron_ptRatio": [["i", np.expm1, [1, 0]]],
    "MElectron_r9": [["i", np.exp, [1, 1e-2]]],
    "MElectron_seedGain": [["d", None]],
    "MElectron_sieie": [["i", np.exp, [10, 1e-1]]],
    "MElectron_sip3d": [["i", np.expm1, [1, 0]]],
    "MElectron_tightCharge": [["d", None]],
}
