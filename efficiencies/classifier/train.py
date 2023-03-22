import os

import torch
from torch import nn

from model import Classifier, train, test
from data import isReco_Dataset


def training_loop():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model = Classifier(38).to(device)
    print(model)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    datapath = os.path.join(
        os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5"
    )
    train_dataset = isReco_Dataset(datapath, 0, 1000)
    test_dataset = isReco_Dataset(datapath, 1000, 2000)

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
