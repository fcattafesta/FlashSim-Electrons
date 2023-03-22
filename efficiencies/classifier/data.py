import os
import h5py
import torch


class isReco_Dataset(torch.utils.data.Dataset):
    def __init__(self, filepath, start, stop):
        h5py_file = h5py.File(filepath, "r")
        self.X = torch.tensor(
            h5py_file["GenElectrons"][start : (start + stop), 0:38], dtype=torch.float32
        )
        self.y = torch.tensor(
            h5py_file["GenElectrons"][start : (start + stop), -1], dtype=torch.long
        )

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


if __name__ == "__main__":

    path = os.path.join(os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5")
    data = isReco_Dataset(path, 0, 1000)

    print(data)
