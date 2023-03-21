import os
import ROOT

ROOT.gInterpreter.ProcessLine('#include "extraction.h"')

root = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/"

ttbar_training_files = [
    "250000/047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
    "240000/B38E7351-C9E4-5642-90A2-F075E2411B00.root",
]

file_paths = [os.path.join(root, f) for f in ttbar_training_files]

print(file_paths)

outputs = [
    os.path.join(os.path.dirname(__file__), "dataset", f"MGenElectrons_{i}")
    for i in range(len(file_paths))
]

for file, output in zip(file_paths, outputs):
    ROOT.extract(file, output)
