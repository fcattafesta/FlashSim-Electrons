import os

import torch
import torch.onnx
import onnxruntime as ort

from data import isReco_Dataset
from model import BinaryClassifier

datapath = os.path.join(os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5")

dataset = isReco_Dataset(datapath, 3400000, 4400000)

# model = BinaryClassifier(38, 512)
# model.load_state_dict(torch.load("model.pt"))
# model.eval()

example, _ = dataset[0]

# torch.onnx.export(model, example, "Efficiency.onnx")

sess = ort.InferenceSession("Efficiency.onnx")

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

ort_inputs = {sess.get_inputs()[0].name: to_numpy(example)}
ort_outs = sess.run(None, ort_inputs)

print(ort_outs)