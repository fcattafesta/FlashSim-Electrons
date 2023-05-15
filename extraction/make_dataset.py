import os
import json
import ROOT

from extract import make_files

# root = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/"
# ttbar_training_files = [
#     "250000/047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
#     "240000/B38E7351-C9E4-5642-90A2-F075E2411B00.root",
#     "230000/DA422D8F-6198-EE47-8B00-1D94D97950B6.root",
#     "230000/393066F3-390A-EC4A-9873-BF4D4D7FBE4F.root",
#     "230000/12C9A5BF-1608-DA48-82E9-36F18051CE31.root",
#     "230000/12C8AFA5-B554-9540-8603-2DF948304880.root",
#     "250000/02B1F58F-7798-FB44-BF80-56C3DC1B6E52.root",
#     "230000/78137863-DAD0-E740-B357-D88AF92BE59F.root",
#     "230000/91456D0B-2FDE-2B4F-8C7A-8E60260480CD.root",
#     "230000/9BD59340-8248-8A40-8770-769383734408.root",
#     "230000/7C934D1C-CA3C-5248-8C5B-96FD0A4A7651.root",
#     "230000/C159CB51-6BC4-E448-AD9E-59CC2A5920F5.root",
# ]

root = "/gpfs/ddn/srm/cms/store/mc/RunIISummer20UL18NanoAODv9/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/"

ttbar_training_files = [
    "120000/0520A050-AF68-EF43-AA5B-5AA77C74ED73.root",
    "120000/0E9EA19A-AE0E-3149-88C3-D733240FF5AB.root",
    "120000/143F7726-375A-3D48-9D53-D6B071CED8F6.root",
    "120000/15FC5EA3-70AA-B640-8748-BD5E1BB84CAC.root",
    "120000/1CD61F25-9DE8-D741-9200-CCBBA61E5A0A.root",
    "120000/1D885366-E280-1243-AE4F-532D326C2386.root",
    "120000/23AD2392-C48B-D643-9E16-C93730AA4A02.root",
    "120000/245961C8-DE06-8F4F-9E92-ED6F30A097C4.root",
    "120000/262EAEE2-14CC-2A44-8F4B-B1A339882B25.root",
]


file_paths = [os.path.join(root, f) for f in ttbar_training_files]

extracted = [os.path.join("dataset", f"MElectrons_{i}") for i in range(len(file_paths))]

d = {
    "RECOELE_GENELE": (0, 0),
    "GENELE_RECOELE": (0, 0),
    "RECOELE_GENPHO": (0, 0),
    "GENPHO_RECOELE": (0, 0),
    "RECOELE_GENJET": (0, 0),
    "GENJET_RECOELE": (0, 0),
}

if __name__ == "__main__":
    for file_in, file_out in zip(file_paths, extracted):
        make_files(file_in, file_out, d)

    with open(os.path.join(os.path.dirname(__file__), "match_dict.json"), "w") as f:
        json.dump(d, f)
