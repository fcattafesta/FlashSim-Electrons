import numpy as np
import pandas as pd
import h5py

import corner
from matplotlib import pyplot as plt
from matplotlib import lines as mlines


def make_corner(reco, samples, labels, title, ranges=None, *args, **kwargs):
    blue_line = mlines.Line2D([], [], color="tab:blue", label="FullSim")
    red_line = mlines.Line2D([], [], color="tab:orange", label="FlashSim")
    fig = corner.corner(
        reco[labels],
        range=ranges,
        labels=labels,
        color="tab:blue",
        levels=[0.5, 0.9, 0.99],
        hist_bin_factor=3,
        scale_hist=True,
        plot_datapoints=False,
        *args,
        **kwargs
    )
    corner.corner(
        samples[labels],
        range=ranges,
        fig=fig,
        color="tab:orange",
        levels=[0.5, 0.9, 0.99],
        hist_bin_factor=3,
        scale_hist=True,
        plot_datapoints=False,
        *args,
        **kwargs
    )
    plt.legend(
        fontsize=24,
        frameon=False,
        handles=[blue_line, red_line],
        bbox_to_anchor=(0.0, 1.0, 1.0, 4.0),
        loc="upper right",
    )
    plt.suptitle(title, fontsize=20)
    plt.close()
    return fig
