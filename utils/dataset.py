import h5py
import torch
from torch.utils.data import Dataset


class ElectronDataset(Dataset):
    """Dataset for Electron training

    Args:
        Dataset (Dataset): _description_
    """

    def __init__(self, h5_paths, start, limit, z_dim, y_dim):

        self.h5_paths = h5_paths
        self._archives = [h5py.File(h5_path, "r") for h5_path in self.h5_paths]
        self._archives = None

        y = self.archives[0]["data"][start : (start + limit), 0:y_dim]
        z = self.archives[0]["data"][start : (start + limit), y_dim : (y_dim + z_dim)]
        self.z_train = torch.tensor(z, dtype=torch.float32)
        self.y_train = torch.tensor(y, dtype=torch.float32)

    @property
    def archives(self):
        if self._archives is None:
            self._archives = [h5py.File(h5_path, "r") for h5_path in self.h5_paths]
        return self._archives

    def __len__(self):
        return len(self.y_train)

    def __getitem__(self, idx):
        return self.z_train[idx], self.y_train[idx]
