import os

import numpy as np

import torch
from torch import nn
from torch.optim.lr_scheduler import ReduceLROnPlateau

import seaborn as sns
from matplotlib import pyplot as plt

from model import BinaryClassifier, train
from data import isReco_Dataset
from validation import validation, loss_plot, accuracy_plot


def training_loop(
    model, input_dim, datapath, train_size, epochs, lr, batch_size, weight, tag
):

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Initialize model
    model.to(device)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([weight], device=device))
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = ReduceLROnPlateau(optimizer, "min", patience=3)
    print(
        f"Parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad)}"
    )

    # Load data
    train_dataset = isReco_Dataset(datapath, input_dim, 0, train_size)
    test_dataset = isReco_Dataset(datapath, input_dim, train_size, 500000)
    validation_dataset = isReco_Dataset(
        datapath, input_dim, train_size + 500000, 1000000
    )
    print(f"Train size: {len(train_dataset)}")
    print(f"Test size: {len(test_dataset)}")
    print(f"Validation size: {len(validation_dataset)}")

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True
    )
    test_dataloader = torch.utils.data.DataLoader(
        test_dataset, batch_size=batch_size, shuffle=True
    )
    validation_dataloader = torch.utils.data.DataLoader(
        validation_dataset, batch_size=100000, shuffle=True
    )

    # Train the model
    test_history = []
    train_history = []
    test_acc_history = []
    train_acc_history = []

    for epoch in range(epochs):
        print(f"Epoch {(epoch + 1):03}:")
        tr_loss, tr_acc, te_loss, te_acc = train(
            train_dataloader,
            test_dataloader,
            model,
            loss_fn,
            optimizer,
            scheduler,
            device,
        )
        test_history.append(te_loss)
        train_history.append(tr_loss)
        test_acc_history.append(te_acc)
        train_acc_history.append(tr_acc)

        if epoch % 10 == 0:
            # Save the model
            torch.save(
                model.state_dict(),
                os.path.join(
                    os.path.dirname(__file__), "models", f"efficiency_{tag}.pt"
                ),
            )
            # Plot loss and accuracy
            loss_plot(train_history, test_history, tag)
            accuracy_plot(train_acc_history, test_acc_history, tag)
            # Validation
            validation(
                model=model,
                validation_dataloader=validation_dataloader,
                device=device,
                tag=tag,
            )
