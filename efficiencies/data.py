import os
import sys
import h5py
import torch
import pandas as pd
import uproot

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

from columns import eff_ele, eff_pho, eff_jet


class isReco_Dataset(torch.utils.data.Dataset):
    def __init__(self, filepath, input_dim, start, stop):
        h5py_file = h5py.File(filepath, "r")
        self.X = torch.tensor(
            h5py_file["data"][start : (start + stop), 0:input_dim],
            dtype=torch.float32,
        )
        self.y = torch.tensor(
            h5py_file["data"][start : (start + stop), -1], dtype=torch.float32
        ).view(-1, 1)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def make_pd_dataframe(tree, cols, *args, **kwargs):
    df = (
        tree.arrays(expressions=cols, library="pd", *args, **kwargs)
        # .reset_index(drop=True)
        # .astype("float32")
        # .dropna()
    )
    print(df)
    return df


def dataset_from_root(files, cols, name, *args, **kwargs):

    tree = uproot.open(files[0], num_workers=20)
    df = make_pd_dataframe(tree, cols)

    for file in files[1:]:
        tree = uproot.open(file, num_workers=20)
        df = pd.concat([df, make_pd_dataframe(tree, cols)], axis=0)
        df.reset_index(drop=True)

    print(df.columns, df.shape)

    f = h5py.File(
        os.path.join(os.path.dirname(__file__), "dataset", f"{name}.hdf5"), "w"
    )
    f.create_dataset("data", data=df.values, dtype="float32")
    f.close()


files = [
    [
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "extraction",
            "dataset",
            f"MElectrons_{i}_{tag}.root:MElectrons",
        )
        for i in range(11)
    ]
    for tag in ["ele", "pho", "jet"]
]

if __name__ == "__main__":

    #dataset_from_root(files[0], eff_ele, "GenElectrons")

    #dataset_from_root(files[1], eff_pho, "GenPhotons")

    dataset_from_root(files[2], eff_jet, "GenJets")
