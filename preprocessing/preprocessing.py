import os
import sys
import json
import h5py
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import uproot

import warnings

warnings.filterwarnings("ignore")  # temporary for MatPlotLibDeprecationWarning bug

 # operation dictionary

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

from columns import reco_columns


np.random.seed(0)  # fixed seed for random smearing

# NOTE: uproot 5 update has changed the way to access the TTree
# as a multiindex pandas dataframe, in case of future errors the sintax should be:
# df = ak.to_dataframe(tree.arrays(library="ak", *args, **kwargs))
def dataset(tree, cols, version=0, dictionary=False, *args, **kwargs):
    """
    Given the TTree, returns the corresponding pandas dataframe.
    If dictionary is True, an empty dictionary of TTree variables is dumped on .txt file (to be copied on dictionary.py).
    """
    df = (
        tree.arrays(expressions=cols, library="pd", *args, **kwargs)
        .reset_index(drop=True)
        .astype("float32")
        .dropna()
    )

    if dictionary:
        val = input("Are you sure to make a new empty vars_dictionary? (y/n)\n")
        if val == "y":
            print("Rewriting...")
            vars_to_save = tree.keys()
            d = {name: [] for name in vars_to_save}

            with open(f"vars_dictionary_v{version}.txt", "w") as file:
                for key, value in d.items():
                    file.write(f'"{key}": {value},\n')

            file.close()
        else:
            print("Aborting...")
            return df
        print("Done.")
    return df


def saturation(df, column_name, interval):
    """
    Performs saturation on given column.
    """
    print(f"Saturating in range {interval}...")
    val = df[column_name].values
    df[column_name] = np.where(val < interval[0], interval[0], val)
    val = df[column_name].values
    df[column_name] = np.where(val > interval[1], interval[1], val)
    return df[column_name]


def gaus_smearing(df, column_name, sigma, interval):
    """
    Performs gaussian smearing on given column. If interval is specified, random gaussian data are assigned to column in interval.
    """
    val = df[column_name].values
    if interval != None:
        mask_condition = np.logical_and(val >= interval[0], val <= interval[1])
        loc = np.mean(val[mask_condition])
        print(
            f"Creating gaussian data (loc={loc}, scale={sigma}) in range {interval}..."
        )
        val[mask_condition] = np.random.normal(
            loc=loc, scale=sigma, size=val[mask_condition].shape
        )
    else:
        print(f"Smearing with sigma={sigma}...")
        df[column_name] = df[column_name].apply(
            lambda x: x + sigma * np.random.normal()
        )
    return df[column_name]


def unif_smearing(df, column_name, half_width, interval):
    """
    Performs uniform smearing on given column. If interval is specified, random uniform data are assigned to column in interval.
    """
    val = df[column_name].values
    if interval != None:
        mask_condition = np.logical_and(val >= interval[0], val <= interval[1])
        loc = np.mean(val[mask_condition])
        print(
            f"Creating uniform data (loc={loc}, half_width={half_width}) in range {interval}..."
        )
        val[mask_condition] = np.random.uniform(
            low=loc - half_width, high=loc + half_width, size=val[mask_condition].shape
        )
    else:
        print(f"Unifrom smearing with half_width={half_width}...")
        df[column_name] = df[column_name].apply(
            lambda x: x + half_width * np.random.uniform(-1, 1)
        )
    return df[column_name]


def transform(df, column_name, function, p):
    """
    Performs a function tranformation on column
    """
    print(f"Applying {function} with parameters {p}...")
    df[column_name] = df[column_name].apply(lambda x: function(x * p[0] + p[1]))
    return df[column_name]


def fix_range(column_name, df):

    scale_factor = np.nanmax(np.abs(df[column_name].values))

    print(f"Scale factor = {scale_factor}")

    if scale_factor != 0:
        df[column_name] = df[column_name] / scale_factor

    return df[column_name], scale_factor


def process_column_var(column_name, operations, df):
    """
    Processes single dataframe column. Operation type is specified by string.
    """
    print(f"Processing {column_name}...")

    for op in operations:
        if op[0] == "s":
            interval = op[1]
            df[column_name] = saturation(df, column_name, interval)

        elif op[0] == "g":
            sigma = op[1]
            mask_condition = op[2]
            df[column_name] = gaus_smearing(df, column_name, sigma, mask_condition)

        elif op[0] == "u":
            half_width = op[1]
            mask_condition = op[2]
            df[column_name] = unif_smearing(df, column_name, half_width, mask_condition)

        elif op[0] == "t":
            function = op[1]
            p = op[2]
            df[column_name] = transform(df, column_name, function, p)

        else:
            return df[column_name]
    print("Done.")
    return df[column_name]


def preprocessing(df, vars_dictionary, scale_factor_name):
    """
    Preprocessing general function given any dataframe and its dictionary
    """
    dict_to_save = {}

    if "ele" in scale_factor_name:
        tag = "ele"
    elif "pho" in scale_factor_name:
        tag = "pho"
    else:
        tag = "jet"

    print(f"Num. before processing: {df.shape}")

    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis="columns")]

    for column_name, operation in vars_dictionary.items():
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        plt.suptitle(f"{column_name}")
        axs[0].hist(df[column_name], bins=30, histtype="step")
        df[column_name] = process_column_var(column_name, operation, df)
        df[column_name], scale = fix_range(column_name, df)
        dict_to_save[column_name] = float(scale)
        axs[1].hist(df[column_name], bins=30, histtype="step")
        plt.savefig(f"figures/{tag}/{column_name}.pdf", format="pdf")
        plt.close()  # produces MatplotlibDeprecationWarning. It is a bug (https://github.com/matplotlib/matplotlib/issues/23921)

    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis="columns")]

    print(f"Num. after processing: {df.shape}")

    f = open(scale_factor_name, "w")
    f.write(json.dumps(dict_to_save))
    f.close()

    return df


def make_dataset(files, outname, target_dictionary, scale_factors_name, gen_cols):
    """
    Makes dataset from given files and saves it to outname
    """
    cols = gen_cols + reco_columns

    tree = uproot.open(files[0], num_workers=20)
    df = dataset(tree, cols)

    for file in files[1:]:
        tree = uproot.open(file, num_workers=20)
        df = pd.concat([df, dataset(tree, cols)], axis=0)
        df.reset_index(drop=True)

    df = preprocessing(df, target_dictionary, scale_factors_name)

    print(df.columns)
    file = h5py.File(f"{outname}.hdf5", "w")

    dset = file.create_dataset("data", data=df.values, dtype="f4")

    file.close()

    os.system(f"mv {outname}.hdf5 ../training")
