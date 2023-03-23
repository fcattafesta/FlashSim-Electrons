import os

import numpy as np

import torch
from torch import nn
from torch.optim.lr_scheduler import ReduceLROnPlateau

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

    loss_fn = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([9.]))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    scheduler = ReduceLROnPlateau(optimizer, "max", patience=3)

    datapath = os.path.join(
        os.path.dirname(__file__), "..", "dataset", "GenElectrons.hdf5"
    )
    train_dataset = isReco_Dataset(datapath, 0, 2000000)
    test_dataset = isReco_Dataset(datapath, 2000000, 2400000)
    validation_dataset = isReco_Dataset(datapath, 2400000, 3400000)

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset, batch_size=10000, shuffle=True
    )
    test_dataloader = torch.utils.data.DataLoader(
        test_dataset, batch_size=10000, shuffle=True
    )
    validation_dataloader = torch.utils.data.DataLoader(
        validation_dataset, batch_size=100000, shuffle=True
    )

    test_history = []
    train_history = []
    test_acc_history = []
    train_acc_history = []
    epochs = 100
    for epoch in range(epochs):
        print(f"Epoch {(epoch + 1):03}:")
        tr_loss, tr_acc, te_loss, te_acc = train(
            train_dataloader, test_dataloader, model, loss_fn, optimizer, scheduler, device
        )
        test_history.append(te_loss)
        train_history.append(tr_loss)
        test_acc_history.append(te_acc)
        train_acc_history.append(tr_acc)

        if epoch % 10 == 0:
            # Save the model
            torch.save(model.state_dict(), "model.pt")

            # Plot the loss
            plt.figure(figsize=(12, 8))
            plt.plot(train_history, label="Train")
            plt.plot(test_history, label="Test")
            plt.legend()
            plt.savefig(
                os.path.join(os.path.dirname(__file__), "figures", "loss.pdf"),
                format="pdf",
            )
            plt.close()

            # Plot the accuracy
            plt.figure(figsize=(12, 8))
            plt.plot(train_acc_history, label="Train")
            plt.plot(test_acc_history, label="Test")
            plt.legend()
            plt.savefig(
                os.path.join(os.path.dirname(__file__), "figures", "accuracy.pdf"),
                format="pdf",
            )
            plt.close()

            # Test the model

            model.eval()
            y_pred_list = []
            y_true_list = []
            y_pred_tag_list = []
            with torch.no_grad():
                for X, y in validation_dataloader:
                    X, y = X.to(device), y.to(device)
                    y_pred = model(X)
                    y_pred = torch.sigmoid(y_pred)
                    y_pred_list.append(y_pred.cpu().numpy())
                    y_pred_tag = torch.round(y_pred)
                    y_pred_tag_list.append(y_pred_tag.cpu().numpy())
                    y_true_list.append(y.cpu().numpy())

            y_pred_list = np.array(y_pred_list).flatten()
            y_true_list = np.array(y_true_list).flatten()
            y_pred_tag_list = np.array(y_pred_tag_list).flatten()

            cm = confusion_matrix(y_true_list, y_pred_tag_list, normalize="true")

            # Plot confusion matrix
            plt.figure(figsize=(10, 10))
            sns.heatmap(cm, annot=True, fmt="f", cmap="viridis")
            plt.title("Confusion matrix")
            plt.ylabel("Actual label")
            plt.xlabel("Predicted label")
            plt.savefig(
                os.path.join(
                    os.path.dirname(__file__), "figures", "confusion_matrix.pdf"
                ),
                format="pdf",
            )
            plt.close()

            # auc
            auc = roc_auc_score(y_true_list, y_pred_list)

            fpr, tpr, thresholds = roc_curve(y_true_list, y_pred_list)

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
                os.path.join(os.path.dirname(__file__), "figures", "roc_curve.pdf"),
                format="pdf",
            )
            plt.close()

            # histogram of predictions
            positive = y_pred_list[y_true_list == 1]
            negative = y_pred_list[y_true_list == 0]

            plt.figure(figsize=(10, 10))
            plt.hist(
                positive, bins=20, histtype="step", label="Positive", color="b"
            )
            plt.hist(
                negative, bins=20, histtype="step", label="Negative", color="r"
            )
            plt.savefig(
                os.path.join(os.path.dirname(__file__), "figures", "predictions.pdf")
            )


if __name__ == "__main__":
    training_loop()
