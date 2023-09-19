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
df = df[:1000000]

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

xbins_ = np.linspace(0, 300, 20)
ybins_ = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 1, 2])

bin_content, xbins, ybins = np.histogram2d(
    df["GenElectron_pt"],
    df["ClosestJet_dr"],
    bins=(xbins_, ybins_),
    range=((0, 300), (0, 2)),
)

bin_content_reco, xbins, ybins = np.histogram2d(
    df["GenElectron_pt"],
    df["ClosestJet_dr"],
    bins=(xbins_, ybins_),
    range=((0, 300), (0, 2)),
    weights=df["isReco"],
)

eff = bin_content_reco / bin_content

eff[np.isnan(eff)] = 0

hep.style.use(hep.style.CMS)
fig, ax = plt.subplots()
hep.cms.text("Private Work", loc=0)
im = ax.imshow(
    eff,
    interpolation="none",
    origin="lower",
    extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
    aspect="auto",
    cmap="cividis",
    vmin=0,
    vmax=1,
)

ax.set_xlabel(r"$p_{T}^{e}$ [GeV]")
ax.set_ylabel(r"$\Delta R^{e-jet}$")

cbar = fig.colorbar(im, ax=ax)

plt.savefig("efficiency_pt_dr.pdf")

# # the same for GenElectron_eta and GenElectron_phi

# xxbins_ = np.linspace(-3, 3, 20)
# yybins_ = np.linspace(-3.14, 3.14, 20)

# bin_content, xbins, ybins = np.histogram2d(
#     df["GenElectron_eta"],
#     df["GenElectron_phi"],
#     bins=(xxbins_, yybins_),
#     range=((-3, 3), (-3.14, 3.14)),
# )

# bin_content_reco, xbins, ybins = np.histogram2d(
#     df["GenElectron_eta"],
#     df["GenElectron_phi"],
#     bins=(xxbins_, yybins_),
#     range=((-3, 3), (-3.14, 3.14)),
#     weights=df["isReco"],
# )

# eff = bin_content_reco / bin_content

# eff[np.isnan(eff)] = 0

# hep.style.use(hep.style.CMS)
# fig, ax = plt.subplots()
# hep.cms.text("Private Work", loc=0)
# im = ax.imshow(
#     eff,
#     interpolation="none",
#     origin="lower",
#     extent=[xxbins_[0], xxbins_[-1], yybins_[0], yybins_[-1]],
#     aspect="equal",
#     cmap="cividis",
#     vmin=0,
#     vmax=1,
# )

# ax.set_xlabel(r"$\eta^{e}$")
# ax.set_ylabel(r"$\phi^{e}$")

# cbar = fig.colorbar(im, ax=ax)

# plt.savefig("efficiency_eta_phi.pdf")
