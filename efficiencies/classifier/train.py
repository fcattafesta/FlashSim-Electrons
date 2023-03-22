import os

import torch
from torch import nn

from model import BinaryClassifier, train, test
from data import isReco_Dataset


def training_loop():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model = BinaryClassifier(38, 128).to(device)
    print(model)
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    datapath = os.path.join(
        os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5"
    )
    train_dataset = isReco_Dataset(datapath, 0, 1300000)
    test_dataset = isReco_Dataset(datapath, 1300000, 1400000)

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset, batch_size=1048, shuffle=True
    )

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset, batch_size=1048, shuffle=True
    )

    epochs = 5
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train(train_dataloader, model, loss_fn, optimizer, device)
        test(test_dataloader, model, loss_fn, device)
    print("Done!")


if __name__ == "__main__":
    training_loop()
