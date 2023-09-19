import h5py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import torch
from model import ElectronClassifier

np.random.seed(42)

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
df["isReco"] = np.where(y_pred > p, tmp, 0)

bin_content, xbins, ybins, _ = np.histogram2d(
    df["GenElectron_pt"],
    df["ClosestJet_dr"],
    bins=(20, 20),
    range=((0, 300), (0, 10)),
)

bin_content_reco, xbins, ybins, _ = np.histogram2d(
    df["GenElectron_pt"],
    df["ClosestJet_dr"],
    bins=(20, 20),
    range=((0, 300), (0, 10)),
    weights=df["isReco"],
)

eff = bin_content_reco / bin_content

fig, ax = plt.subplots()
im = ax.imshow(
    eff,
    interpolation="nearest",
    origin="lower",
    extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
    aspect="auto",
    cmap="viridis",
)

ax.set_xlabel(r"$p_{T}^{e}$ [GeV]")
ax.set_ylabel(r"$\Delta R^{e-jet}$")

cbar = fig.colorbar(im, ax=ax)

plt.savefig("efficiency_pt_dr.pdf")
