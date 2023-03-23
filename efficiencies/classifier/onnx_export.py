import os

import torch
import torch.onnx

from data import isReco_Dataset
from model import BinaryClassifier

datapath = os.path.join(os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5")

dataset = isReco_Dataset(datapath, 3400000, 4400000)

model = BinaryClassifier(38, 512)
model.load_state_dict(torch.load("model.pt"))
model.eval()

example, _ = dataset[0]

torch.export.onnx(model, example, "Efficiency.onnx")

