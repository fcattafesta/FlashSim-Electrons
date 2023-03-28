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
# ]

# file_paths = [os.path.join(root, f) for f in ttbar_training_files]

file_paths = [
    "root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL18NanoAODv2/"
    "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/"
    "106X_upgrade2018_realistic_v15_L1v1-v1/230000/"
    "0088F3A1-0457-AB4D-836B-AC3022A0E34F.root",
    "root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAOD/"
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/"
    "106X_mcRun2_asymptotic_v13-v1/00000/"
    "28FE3773-9C94-5E42-B6FB-64C997636881.root",
    "root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAOD/"
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/"
    "106X_mcRun2_asymptotic_v13-v1/00000/"
    "89142AF0-003E-5549-A6C9-5C0A3FA912A4.root",
    "root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAOD/"
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/"
    "106X_mcRun2_asymptotic_v13-v1/10000/"
    "C600FF22-6CBA-6E4B-8FCF-192910F79D84.root",
    "root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAOD/"
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/"
    "106X_mcRun2_asymptotic_v13-v1/10000/"
    "E1688267-29A9-D049-8B5F-FE4910D3A262.root",
    "root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAOD/"
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/"
    "106X_mcRun2_asymptotic_v13-v1/20000/"
    "3A2B272C-E0EB-1748-A658-E5B58BBCFCBF.root",
    "root://cmsxrootd.fnal.gov///store/mc/RunIISummer20UL16NanoAOD/"
    "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/"
    "106X_mcRun2_asymptotic_v13-v1/20000/"
    "40E28BE3-1A22-9D40-A482-2BAA3E9ABC24.root",
]

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

    with open(os.path.join(os.path.dirname(__file__)), "match_dict.json", "w") as f:
        json.dump(d, f)
