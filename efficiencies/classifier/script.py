import os
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, classification_report
import torch

from data import isReco_Dataset

datapath = os.path.join(os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5")
dataset = isReco_Dataset(datapath, 3400000, 4400000)

model = torch.load("model.pt")

example, _ = dataset[0]

traced_script_module = torch.jit.trace(model, example)

# tests 

test, _ = dataset[1]

pred = traced_script_module(test)

print(pred)

