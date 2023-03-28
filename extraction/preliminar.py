import os
import json

import numpy as np

import ROOT


with open("match_dict.json", "r") as f:
    match_dict = json.load(f)

match_ele, reco_ele = match_dict["RECOELE_GENELE"]

match_pho, _ = match_dict["RECOELE_GENPHO"]

match_jet, _ = match_dict["RECOELE_GENJET"]

print("RECO to GEN matching fractions:")

print("Electrons:", match_ele / reco_ele)
print("Photons:", match_pho / reco_ele)
print("Jets:", match_jet / reco_ele)
print("Total:", (match_ele + match_pho + match_jet) / reco_ele)


match_ele, gen_ele = match_dict["GENELE_RECOELE"]

match_pho, gen_pho = match_dict["GENPHO_RECOELE"]

match_jet, gen_jet = match_dict["GENJET_RECOELE"]

print("GEN to RECO matching fractions:")
print("Electrons:", match_ele / gen_ele)
print("Photons:", match_pho / gen_pho)
print("Jets:", match_jet / gen_jet)

