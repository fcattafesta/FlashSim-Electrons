import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import torch
from model import ElectronClassifier

ele_cond = [
    "GenElectron_eta",
    "GenElectron_phi",
    "GenElectron_pt",
    "GenElectron_charge",
    "GenElectron_statusFlag0",
    "GenElectron_statusFlag1",
    "GenElectron_statusFlag2",
    "GenElectron_statusFlag3",
    "GenElectron_statusFlag4",
    "GenElectron_statusFlag5",
    "GenElectron_statusFlag6",
    "GenElectron_statusFlag7",
    "GenElectron_statusFlag8",
    "GenElectron_statusFlag9",
    "GenElectron_statusFlag10",
    "GenElectron_statusFlag11",
    "GenElectron_statusFlag12",
    "GenElectron_statusFlag13",
    "GenElectron_statusFlag14",
    "ClosestJet_dr",
    "ClosestJet_dphi",
    "ClosestJet_deta",
    "ClosestJet_pt",
    "ClosestJet_mass",
    "ClosestJet_EncodedPartonFlavour_light",
    "ClosestJet_EncodedPartonFlavour_gluon",
    "ClosestJet_EncodedPartonFlavour_c",
    "ClosestJet_EncodedPartonFlavour_b",
    "ClosestJet_EncodedPartonFlavour_undefined",
    "ClosestJet_EncodedHadronFlavour_b",
    "ClosestJet_EncodedHadronFlavour_c",
    "ClosestJet_EncodedHadronFlavour_light",
]

eff_ele = ele_cond + ["GenElectron_isReco"]

# open the file
f = h5py.File("dataset/GenElectrons.hdf5", "r")

# make a dataframe
df = pd.DataFrame(f["data"][:], columns=eff_ele)

# take 1M electrons
df = df[:10000]

df["Full_Efficency"] = df["GenElectron_isReco"] / df["GenElectron_isReco"].sum()

# load the model
model = ElectronClassifier(32)
model.load_state_dict(torch.load("models/efficiency_electrons.pt"))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

# make the prediction
X = torch.tensor(df[eff_ele[0:-1]].values, dtype=torch.float32).to(device)
y_pred = model.predict(X)
y_pred = y_pred.detach().cpu().numpy().flatten()
p = np.random.rand(y_pred.size)
tmp = np.ones(y_pred.size)
df["Flash_Efficiency"] = (
    np.where(y_pred > p, tmp, 0) / np.where(y_pred > p, tmp, 0).sum()
)

# Make an heatmap of the efficiency in function of "GenElectron_pt" and "ClosestJet_dr"

# define the bins
pt_bins = np.linspace(0, 100, 10)
dr_bins = np.linspace(0, 10, 10)

# compute the efficiency
eff = np.zeros((len(pt_bins) - 1, len(dr_bins) - 1))
for i in range(len(pt_bins) - 1):
    for j in range(len(dr_bins) - 1):
        mask = (
            (df["GenElectron_pt"] > pt_bins[i])
            & (df["GenElectron_pt"] < pt_bins[i + 1])
            & (df["ClosestJet_dr"] > dr_bins[j])
            & (df["ClosestJet_dr"] < dr_bins[j + 1])
        )
        eff[i, j] = df[mask]["GenElectron_isReco"].sum() / mask.sum()

# plot the efficiency
plt.figure(figsize=(10, 10))
plt.imshow(eff, cmap="viridis", interpolation="nearest")
plt.colorbar()
plt.xlabel("GenElectron_pt")
plt.ylabel("ClosestJet_dr")
plt.xticks(np.arange(len(pt_bins) - 1), pt_bins)
plt.yticks(np.arange(len(dr_bins) - 1), dr_bins)
plt.title("Efficiency")
plt.savefig("efficiency_ptVSdr.png")
