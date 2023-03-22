import os

import torch
from torch import nn

import seaborn as sns

from sklearn.metrics import roc_curve, roc_auc_score, confusion_matrix, classification_report

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
    train_dataset = isReco_Dataset(datapath, 0, 1120000)
    test_dataset = isReco_Dataset(datapath, 1120000, 1400000)

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset, batch_size=10000, shuffle=True
    )

    validation_dataset = isReco_Dataset(datapath, 1400000, 2000000)
    validation_dataloader = torch.utils.data.DataLoader(validation_dataset, batch_size=10000, shuffle=True)


    test_dataloader = torch.utils.data.DataLoader(
        test_dataset, batch_size=10000, shuffle=True
    )

    epochs = 10
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} |", end="")
        train(train_dataloader, test_dataloader, model, loss_fn, optimizer, device)

    
    # Test the model

    model.eval()
    with torch.no_grad():
        y_pred = model(validation_dataset.X)
        y_pred = torch.round(torch.sigmoid(y_pred))
        y_pred = y_pred.cpu().numpy()
        y_true = validation_dataset.y.cpu().numpy()



if __name__ == "__main__":
    training_loop()