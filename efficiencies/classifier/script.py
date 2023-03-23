import os
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, classification_report
import torch

from data import isReco_Dataset
from model import BinaryClassifier

datapath = os.path.join(os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5")
dataset = isReco_Dataset(datapath, 3400000, 4400000)

model = BinaryClassifier(38, 512)
model.load_state_dict(torch.load("model.pt"))

example, _ = dataset[0]

inputs = {"forward": example, "predict": example}

traced_script_module = torch.jit.trace_module(model, inputs)

# tests 

X, y_true = dataset

print(X.shape, y_true.shape)

pred = traced_script_module.predict()

