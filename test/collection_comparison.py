import os
import json
import sys
import ROOT

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "generation"))

from nbd_func import ele_names

ROOT.gInterpreter.Declare('#include "comparison.h"')

if __name__ == "__main__":

    ele_aod = [f"Electron_{name}" for name in ele_names]

    with open(
        os.path.join(os.path.dirname(__file__), "..", "generation", "range_dict.json")
    ) as f:
        ranges_dict = json.load(f)

    # Correction for the following variables:
    
    ranges_dict["MElectron_ptRatio"] = [0, 200]
    ranges_dict["MElectron_etaMinusGen"] = [-5, 5]
    ranges_dict["MElectron_phiMinusGen"] = [-3.2, 3.2]
    ranges_dict["MElectron_charge"] = [-1, 1]

    for col, range in zip(ele_aod, ranges_dict.values()):
        ROOT.compare(col, range[0], range[1])
   

