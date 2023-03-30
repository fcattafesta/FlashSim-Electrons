# the NanoBuilder function, takings as input a NanoAOD file, extracting gen-level information for conditionig,
# generating a new event with the same topology and saving results in a NanoAOD-like .root file
import os
import sys
import json
import time

import ROOT
import uproot
import awkward as ak

import numpy as np
import pandas as pd

import torch
from torch.utils.data import Dataset, DataLoader

dirpath = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(dirpath, "..", "models"))
sys.path.insert(0, os.path.join(dirpath, "..", "utils"))
sys.path.insert(0, os.path.join(dirpath, "..", "training"))
# sys.path.insert(0, os.path.join(dirpath, "..", "postprocessing"))

# from columns import reco_columns, ele_names, ele_cond
from postprocessing import postprocessing, reco_columns, gen_columns
from post_actions import target_dictionary


class GenDS(Dataset):
    """A dumb dataset for storing gen-conditioning for generation

    Args:
            Dataset (Pytorch Dataset): Pytorch Dataset class
    """

    def __init__(self, df, cond_vars):

        y = df.loc[:, cond_vars].values
        self.y_train = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.y_train)

    def __getitem__(self, idx):
        return self.y_train[idx]


# really important step: use ROOT interpreter to call c++ code directly from python
# execute only selection of Gen objects (no longer requires matching as we are not training)
ROOT.gInterpreter.ProcessLine('#include "gens.h"')

STOP = None


def nbd(ele_model, root, file_path, new_root):
    """The NanoBuilder function

    Args:
            ele_model (pytorch model): the trained NF net for jet generation
            root (string): old root for file providing the gen conditioning and event topology
            file_path (string): gen inputs file name
            new_root (string): new root for saving output file
    """
    # select nano aod, process and save intermmediate files to disk
    s = str(os.path.join(root, file_path))
    print(f"Processing file: {s}")
    ROOT.gens(s)
    print("Intermediate files saved")

    # read processed files for jets and save event structure
    tree = uproot.open("testGens.root:Gens", num_workers=20)

    # read jet data to df
    df = (
        tree.arrays(gen_columns, library="pd", entry_stop=STOP)
        .astype("float32")
        .dropna()
    )
    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis="columns")]
    # crucial step: save original multiindex structure to restructure outputs later
    ele_ev_index = np.unique(df.index.get_level_values(0).values)
    events_structure_ele = (
        df.reset_index(level=1).index.value_counts().sort_index().values
    )
    print(f"Number of events: {len(events_structure_ele)}")
    print(f"Number of objects: {sum(events_structure_ele)}")

    # reset dataframe index for performing 1to1 generation
    df.reset_index(drop=True)

    # save gen-level charges for matching them later to the event
    charges = np.reshape(
        df["GenElectron_charge"].values, (len(df["GenElectron_charge"].values), 1)
    )

    # read global event info to df
    dfe = (
        tree.arrays(["event", "run"], library="pd", entry_stop=STOP)
        .astype(np.longlong)
        .dropna()
    )
    dfe = dfe[~dfe.isin([np.nan, np.inf, -np.inf]).any(axis="columns")]
    # in this case we are directly saving the values (only 1 value per event)
    events_structure = dfe.values

    # if some event is missing an object, we must set the missing entry to 0 manually
    # to keep a consistent structure
    # adjust structure if some events have no jets

    zeros = np.zeros(len(dfe), dtype=int)
    print(len(ele_ev_index), len(events_structure_ele))
    np.put(zeros, ele_ev_index, events_structure_ele, mode="rise")
    events_structure_ele = zeros
    print(events_structure_ele.shape, events_structure_ele)
    print(sum(events_structure_ele))

    # define datasets
    ele_dataset = GenDS(df, gen_columns)

    # start electrons 1to1 generation
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    batch_size = 10000
    ele_loader = DataLoader(
        ele_dataset,
        batch_size=batch_size,
        shuffle=False,
        pin_memory=True,
        num_workers=20,
    )

    flow = ele_model
    flow.eval()

    tot_sample = []
    leftover_sample = []
    times = []

    print(f"Batch size:  {batch_size}")

    with torch.no_grad():
        for batch_idx, y in enumerate(ele_loader):

            print(f"Batch: {batch_idx}/{len(ele_loader)}    ", end="")

            y = y.float().to(device, non_blocking=True)
            if len(y) == batch_size:
                start = time.time()
                while True:
                    try:
                        sample = flow.sample(1, context=y)
                        break
                    except AssertionError:
                        print("Error, retrying")
                taken = time.time() - start
                print(f"{(batch_size / taken):.0f} Hz")
                times.append(taken)
                sample = sample.detach().cpu().numpy()
                sample = np.squeeze(sample, axis=1)
                tot_sample.append(sample)

            else:
                leftover_shape = len(y)
                sample = flow.sample(1, context=y)
                sample = sample.detach().cpu().numpy()
                sample = np.squeeze(sample, axis=1)
                leftover_sample.append(sample)

    print(f"Mean rate: {batch_size / np.mean(times)}")

    tot_sample = np.array(tot_sample)
    tot_sample = np.reshape(tot_sample, ((len(ele_loader) - 1) * batch_size, 47))
    leftover_sample = np.array(leftover_sample)
    leftover_sample = np.reshape(leftover_sample, (leftover_shape, 47))
    total = np.concatenate((tot_sample, leftover_sample), axis=0)

    total = pd.DataFrame(total, columns=reco_columns)

    total = postprocessing(total, target_dictionary)

    with open(os.path.join(os.path.dirname(__file__), "range_dict.json"), "r") as file:
        ranges_dict = json.load(file)

    for col in total.columns:
        if col in ranges_dict.keys():
            min = ranges_dict[col][0]
            max = ranges_dict[col][1]
            val = total[col].values
            saturated = np.where(val < min, min, val)
            saturated = np.where(saturated > max, max, saturated)
            total[col] = saturated

    total["MElectron_ptRatio"] = (
        total["MElectron_ptRatio"].values * df["GenElectron_pt"].values
    )
    total["MElectron_etaMinusGen"] = (
        total["MElectron_etaMinusGen"].values + df["GenElectron_eta"].values
    )
    total["MElectron_phiMinusGen"] = (
        total["MElectron_phiMinusGen"].values + df["GenElectron_phi"].values
    )

    # Charge: in this branch charge is also a target variable, so we already have it in total dataframe

    total = total.values

    total = np.concatenate((total, charges), axis=1)

    # convert to akw arrays for saving to file with correct event structure

    to_ttree = dict(zip(ele_names, total.T))
    to_ttree = ak.unflatten(ak.Array(to_ttree), events_structure_ele)

    to_ttreee = dict(zip(["event", "run"], events_structure.T))
    to_ttreee = ak.Array(to_ttreee)

    # use uproot recreate to save directly akw arrays to .root file
    new_path = str(os.path.join(new_root, file_path))
    new_path = os.path.splitext(new_path)[0]
    with uproot.recreate(f"{new_path}_synth.root") as file:
        file["Events"] = {
            "Electron": to_ttree,
            "event": to_ttreee.event,
            "run": to_ttreee.run,
        }

    print(f"{new_path}_synth.root saved")

    return
