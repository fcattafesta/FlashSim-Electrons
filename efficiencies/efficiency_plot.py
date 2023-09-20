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
print(len(df))
df = df[df["GenElectron_pt"] > 20]
print(len(df))

# take 1M electrons
# df = df[:5000000]

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

xbins_ = np.linspace(20, 150, 20)
ybins_ = np.linspace(0, 2, 20)

bin_content, xbins, ybins = np.histogram2d(
    df["GenElectron_pt"],
    df["ClosestJet_dr"],
    bins=(xbins_, ybins_),
    range=((20, 150), (0, 2)),
)

bin_content_reco, xbins, ybins = np.histogram2d(
    df["GenElectron_pt"],
    df["ClosestJet_dr"],
    bins=(xbins_, ybins_),
    range=((20, 150), (0, 2)),
    weights=df["isReco"],
)

eff = bin_content_reco / bin_content

# eff[np.isnan(eff)] = 0

full_bin_content_reco, xbins, ybins = np.histogram2d(
    df["GenElectron_pt"],
    df["ClosestJet_dr"],
    bins=(xbins_, ybins_),
    range=((20, 150), (0, 2)),
    weights=df["GenElectron_isReco"],
)

full_eff = full_bin_content_reco / bin_content

# make the plot of the two efficiencies
hep.style.use(hep.style.CMS)
fig, ax = plt.subplots(1, 2, figsize=(30, 15), sharey=True, width_ratios=[1, 1.2])
hep.cms.text("Private Work", loc=0, ax=ax[0])
im = ax[0].imshow(
    eff.T,
    interpolation="none",
    origin="lower",
    extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
    aspect="auto",
    cmap="cividis",
    vmin=0.5,
    vmax=1,
)
ax[0].set_xlabel(r"$p_{T}^{GEN}$ [GeV]")
ax[0].set_ylabel(r"$\Delta R^{GEN}_{e-jet}$")
ax[0].set_title(r"FlashSim ($p_{T}^{GEN}>20$ GeV)", loc="right")

ax[1].imshow(
    full_eff.T,
    interpolation="none",
    origin="lower",
    extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
    aspect="auto",
    cmap="cividis",
    vmin=0.5,
    vmax=1,
)
ax[1].set_xlabel(r"$p_{T}^{GEN}$ [GeV]")
ax[1].set_title(r"FullSim ($p_{T}^{GEN}>20$ GeV)", loc="right")

cbar = fig.colorbar(im, ax=ax[1])

plt.savefig("efficiency_pt_dr.pdf")

# the same for GenElectron_eta and GenElectron_phi

xxbins_ = np.linspace(-2.5, 2.5, 20)
yybins_ = np.linspace(-3.14, 3.14, 20)

bin_content, xbins, ybins = np.histogram2d(
    df["GenElectron_eta"],
    df["GenElectron_phi"],
    bins=(xxbins_, yybins_),
    range=((-2.5, 2.5), (-3.14, 3.14)),
)

bin_content_reco, xbins, ybins = np.histogram2d(
    df["GenElectron_eta"],
    df["GenElectron_phi"],
    bins=(xxbins_, yybins_),
    range=((-2.5, 2.5), (-3.14, 3.14)),
    weights=df["isReco"],
)

eff = bin_content_reco / bin_content

# eff[np.isnan(eff)] = 0

full_bin_content_reco, xbins, ybins = np.histogram2d(
    df["GenElectron_eta"],
    df["GenElectron_phi"],
    bins=(xxbins_, yybins_),
    range=((-2.5, 2.5), (-3.14, 3.14)),
    weights=df["GenElectron_isReco"],
)

full_eff = full_bin_content_reco / bin_content

hep.style.use(hep.style.CMS)
fig, ax = plt.subplots(1, 2, figsize=(30, 15), sharey=True, width_ratios=[1, 1.2])
hep.cms.text("Private Work", loc=0, ax=ax[0])
im = ax[0].imshow(
    eff.T,
    interpolation="none",
    origin="lower",
    extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
    aspect="auto",
    cmap="cividis",
    vmin=0.5,
    vmax=1,
)
ax[0].set_xlabel(r"$\eta^{GEN}$")
ax[0].set_ylabel(r"$\phi^{GEN}$")
ax[0].set_title(r"FlashSim ($p_{T}^{GEN}>20$ GeV)", loc="right")

ax[1].imshow(
    full_eff.T,
    interpolation="none",
    origin="lower",
    extent=[xbins[0], xbins[-1], ybins[0], ybins[-1]],
    aspect="auto",
    cmap="cividis",
    vmin=0.5,
    vmax=1,
)
ax[1].set_xlabel(r"$\eta^{GEN}$")
ax[1].set_title(r"FullSim ($p_{T}^{GEN}>20$ GeV)", loc="right")

cbar = fig.colorbar(im, ax=ax[1])

plt.savefig("efficiency_eta_phi.pdf")

# 1d GenElectron_pt

xbins_ = np.linspace(20, 150, 20)

bin_width = xbins_[1] - xbins_[0] / 2

bin_content, xbins = np.histogram(df["GenElectron_pt"], bins=xbins_, range=(20, 150))

bin_content_reco, xbins = np.histogram(
    df["GenElectron_pt"], bins=xbins_, range=(20, 150), weights=df["isReco"]
)

eff = bin_content_reco / bin_content


full_bin_content_reco, xbins = np.histogram(
    df["GenElectron_pt"], bins=xbins_, range=(20, 150), weights=df["GenElectron_isReco"]
)

full_eff = full_bin_content_reco / bin_content

bin_centers = (xbins[1:] + xbins[:-1]) / 2

hep.style.use(hep.style.CMS)
fig, ax = plt.subplots(figsize=(12, 12))
hep.cms.text("Private Work", loc=0, ax=ax)
ax.errorbar(
    bin_centers,
    full_eff,
    xerr=bin_width,
    label="FullSim",
    color="black",
    lw=2,
    ls="",
    fmt="s",
    markersize=10,
)
ax.errorbar(
    bin_centers,
    eff,
    xerr=bin_width,
    label="FlashSim",
    color="orange",
    lw=2,
    ls="",
    fmt="o",
    markersize=6,
)

ax.set_xlabel(r"$p_{T}^{GEN}$ [GeV]")
ax.set_ylabel(r"Efficiency")
ax.set_title(r"($p_{T}^{GEN}>20$ GeV)", loc="right")
ax.set_ylim(0.5, 1)


ax.legend()

plt.savefig("efficiency_pt.pdf")

# same for GenElectron_eta and GenElectron_phi

xxbins_ = np.linspace(-2.5, 2.5, 20)

bin_width = xxbins_[1] - xxbins_[0] / 2

bin_content, xbins = np.histogram(
    df["GenElectron_eta"], bins=xxbins_, range=(-2.5, 2.5)
)

bin_content_reco, xbins = np.histogram(
    df["GenElectron_eta"], bins=xxbins_, range=(-2.5, 2.5), weights=df["isReco"]
)

eff = bin_content_reco / bin_content


full_bin_content_reco, xbins = np.histogram(
    df["GenElectron_eta"],
    bins=xxbins_,
    range=(-2.5, 2.5),
    weights=df["GenElectron_isReco"],
)

full_eff = full_bin_content_reco / bin_content

bin_centers = (xbins[1:] + xbins[:-1]) / 2

hep.style.use(hep.style.CMS)
fig, ax = plt.subplots(figsize=(12, 12))
hep.cms.text("Private Work", loc=0, ax=ax)
ax.errorbar(
    bin_centers,
    full_eff,
    xerr=bin_width,
    label="FullSim",
    color="black",
    lw=2,
    ls="",
    fmt="s",
    markersize=10,
)
ax.errorbar(
    bin_centers,
    eff,
    xerr=bin_width,
    label="FlashSim",
    color="orange",
    lw=2,
    ls="",
    fmt="o",
    markersize=6,
)

ax.set_xlabel(r"$\eta^{GEN}$")
ax.set_ylabel(r"Efficiency")
ax.set_title(r"($p_{T}^{GEN}>20$ GeV)", loc="right")
ax.set_ylim(0.5, 1)


ax.legend()

plt.savefig("efficiency_eta.pdf")

# same for GenElectron_phi

xxbins_ = np.linspace(-3.14, 3.14, 20)

bin_width = xxbins_[1] - xxbins_[0] / 2

bin_content, xbins = np.histogram(
    df["GenElectron_phi"], bins=xxbins_, range=(-3.14, 3.14)
)

bin_content_reco, xbins = np.histogram(
    df["GenElectron_phi"], bins=xxbins_, range=(-3.14, 3.14), weights=df["isReco"]
)

eff = bin_content_reco / bin_content


full_bin_content_reco, xbins = np.histogram(
    df["GenElectron_phi"],
    bins=xxbins_,
    range=(-3.14, 3.14),
    weights=df["GenElectron_isReco"],
)

full_eff = full_bin_content_reco / bin_content

bin_centers = (xbins[1:] + xbins[:-1]) / 2

hep.style.use(hep.style.CMS)
fig, ax = plt.subplots(figsize=(12, 12))
hep.cms.text("Private Work", loc=0, ax=ax)
ax.errorbar(
    bin_centers,
    full_eff,
    xerr=bin_width,
    label="FullSim",
    color="black",
    lw=2,
    ls="",
    fmt="s",
    markersize=10,
)
ax.errorbar(
    bin_centers,
    eff,
    xerr=bin_width,
    label="FlashSim",
    color="orange",
    lw=2,
    ls="",
    fmt="o",
    markersize=6,
)

ax.set_xlabel(r"$\phi^{GEN}$")
ax.set_ylabel(r"Efficiency")
ax.set_title(r"($p_{T}^{GEN}>20$ GeV)", loc="right")
ax.set_ylim(0.5, 1)


ax.legend()

plt.savefig("efficiency_phi.pdf")
