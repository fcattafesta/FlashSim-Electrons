import os
import h5py
import pandas as pd
import ROOT
import uproot


def dataset(tree, *args, **kwargs):

    df = (
        tree.arrays(library="pd", *args, **kwargs)
        .reset_index(drop=True)
        .astype("float32")
        .dropna()
    )

    return df


ROOT.gInterpreter.ProcessLine('#include "extraction.h"')

root = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20_ext1-v1/"

ttbar_training_files = [
    "250000/047F4368-97D4-1A4E-B896-23C6C72DD2BE.root",
    "240000/B38E7351-C9E4-5642-90A2-F075E2411B00.root",
    "230000/DA422D8F-6198-EE47-8B00-1D94D97950B6.root",
]

file_paths = [os.path.join(root, f) for f in ttbar_training_files]

outputs = [
    os.path.join(os.path.dirname(__file__), "dataset", f"MGenElectrons_{i}.root")
    for i in range(len(file_paths))
]

for file, output in zip(file_paths, outputs):
    ROOT.extract(file, output)

root_files = [f"{output}:GenElectrons" for output in outputs]

tree = uproot.open(root_files[0], num_workers=20)
df = dataset(tree)

for file in root_files[1:]:
    tree = uproot.open(file, num_workers=20)
    df = pd.concat([df, dataset(tree)], axis=0)
    df.reset_index(drop=True)

print(df.columns)

file = h5py.File(os.path.join(os.path.dirname(__file__), f"GenElectrons.hdf5"), "w")
file.create_dataset("GenElectrons", data=df.values, dtype="f4")
file.close()

# 1405944 GenElectrons