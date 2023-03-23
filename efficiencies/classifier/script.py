import os
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
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

X, y_true = dataset[:]

y_pred = traced_script_module.predict(X)

y_pred_tag = torch.round(y_pred)

cm = confusion_matrix(y_true, y_pred_tag, normalize="true")

# Plot confusion matrix
plt.figure(figsize=(10, 10))
sns.heatmap(cm, annot=True, fmt="f", cmap="viridis")
plt.title("Confusion matrix")
plt.ylabel("Actual label")
plt.xlabel("Predicted label")
plt.savefig(
    os.path.join(
        os.path.dirname(__file__), "figures", "script", "confusion_matrix.pdf"
    ),
    format="pdf",
)
plt.close()

# auc
auc = roc_auc_score(y_true, y_pred)

fpr, tpr, thresholds = roc_curve(y_true, y_pred)

plt.figure(figsize=(10, 10))
plt.plot(fpr, tpr, label="ROC Curve")
plt.plot([0, 1], [0, 1], "k--")
# auc on plot
plt.text(0.5, 0.4, f"AUC: {auc:.3f}")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve")
plt.legend()
plt.savefig(
    os.path.join(os.path.dirname(__file__), "figures", "script", "roc_curve.pdf"),
    format="pdf",
)
plt.close()

# histogram of predictions
positive = y_pred[y_true == 1]
negative = y_pred[y_true == 0]

plt.figure(figsize=(10, 10))
plt.hist(positive, bins=20, histtype="step", label="Positive", color="b")
plt.hist(negative, bins=20, histtype="step", label="Negative", color="r")
plt.savefig(
    os.path.join(os.path.dirname(__file__), "figures", "script", "predictions.pdf")
)
