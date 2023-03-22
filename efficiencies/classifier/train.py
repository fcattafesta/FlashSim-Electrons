import os

import numpy as np

import torch
from torch import nn

import seaborn as sns
from matplotlib import pyplot as plt

from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

from model import BinaryClassifier, train
from data import isReco_Dataset


def training_loop():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model = BinaryClassifier(38, 512).to(device)
    print(
        f"Parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad)}"
    )

    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    datapath = os.path.join(
        os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5"
    )
    train_dataset = isReco_Dataset(datapath, 0, 1000)
    test_dataset = isReco_Dataset(datapath, 1000, 1500)

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset, batch_size=100, shuffle=True
    )

    validation_dataset = isReco_Dataset(datapath, 1500, 2000)
    validation_dataloader = torch.utils.data.DataLoader(
        validation_dataset, batch_size=1000, shuffle=True
    )

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset, batch_size=100, shuffle=True
    )

    epochs = 5
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} |", end="")
        train(train_dataloader, test_dataloader, model, loss_fn, optimizer, device)

    # Test the model

    model.eval()
    y_pred_list = []
    y_true_list = []
    with torch.no_grad():
        for X, y in validation_dataloader:
            X, y = X.to(device), y.to(device)
            y_pred = model(X)
            y_pred = torch.round(torch.sigmoid(y_pred))
            y_pred = y_pred.cpu().numpy()
            y_pred_list.append(y_pred)
            y_true = y.cpu().numpy()
            y_true_list.append(y_true)

    y_pred_list = np.array(y_pred_list).flatten()
    y_true_list = np.array(y_true_list).flatten()

    cm = confusion_matrix(y_true_list, y_pred_list)
    print(cm)


if __name__ == "__main__":
    training_loop()
