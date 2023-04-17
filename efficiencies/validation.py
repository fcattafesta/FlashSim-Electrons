import os
import sys

import numpy as np

import torch
from torch import nn
from torch.optim.lr_scheduler import ReduceLROnPlateau
from captum.attr import IntegratedGradients

import seaborn as sns
from matplotlib import pyplot as plt

from sklearn.metrics import (
    roc_curve,
    roc_auc_score,
    confusion_matrix,
)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

from columns import eff_ele, eff_jet, eff_pho


def visualize_importances(
    importances,
    tag,
    title="Average Feature Importances",
    plot=True,
):
    if tag == "electrons":
        feature_names = eff_ele[:-1]
    elif tag == "jets":
        feature_names = eff_jet[:-1]
    elif tag == "photons":
        feature_names = eff_pho[:-1]

    x_pos = np.arange(len(feature_names))
    if plot:
        plt.figure(figsize=(12, 12))
        plt.bar(x_pos, importances, align="center")
        plt.xticks(x_pos, feature_names, wrap=True, rotation=45, ha="right")
        plt.title(title)
        plt.savefig(
            os.path.join(os.path.dirname(__file__), "figures", tag, "importances.pdf"),
            format="pdf",
        )


def validation(validation_dataloader, model, device, tag):
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
            torch.cuda.empty_cache()

    y_pred_list = np.array(y_pred_list).flatten()
    y_true_list = np.array(y_true_list).flatten()
    y_pred_tag_list = np.array(y_pred_tag_list).flatten()

    X, _ = validation_dataloader.dataset[:10000]
    X = X.to(device)

    ig = IntegratedGradients(model)
    attributions = ig.attribute(X, return_convergence_delta=False)
    attributions = attributions.cpu().numpy()

    visualize_importances(np.mean(attributions, axis=0), tag)

    cm = confusion_matrix(y_true_list, y_pred_tag_list, normalize="true")

    # Plot confusion matrix
    plt.figure(figsize=(10, 10))
    sns.heatmap(cm, annot=True, fmt="f", cmap="viridis")
    plt.title("Confusion matrix")
    plt.ylabel("Actual label")
    plt.xlabel("Predicted label")
    plt.savefig(
        os.path.join(os.path.dirname(__file__), "figures", tag, "confusion_matrix.pdf"),
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
    plt.savefig(
        os.path.join(os.path.dirname(__file__), "figures", tag, "roc_curve.pdf"),
        format="pdf",
    )
    plt.close()

    # histogram of predictions
    positive = y_pred_list[y_true_list == 1]
    negative = y_pred_list[y_true_list == 0]

    plt.figure(figsize=(10, 10))
    plt.title("Predictions")
    plt.hist(
        positive,
        bins=20,
        histtype="step",
        label="isReco",
        linewidth=2,
        edgecolor="b",
        fc=(0, 0, 1, 0.3),
        fill=True,
        range=(0, 1),
    )
    plt.hist(
        negative,
        bins=20,
        histtype="step",
        label="isNotReco",
        linewidth=2,
        edgecolor="r",
        fc=(1, 0, 0, 0.3),
        fill=True,
        range=(0, 1),
    )
    plt.yscale("log")
    plt.xlabel("Classifier output")
    plt.legend(frameon=False)
    plt.savefig(
        os.path.join(os.path.dirname(__file__), "figures", tag, "predictions.pdf")
    )


def loss_plot(train_history, test_history, tag):
    plt.figure(figsize=(10, 10))
    plt.plot(train_history, label="Train loss")
    plt.plot(test_history, label="Test loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend(frameon=False)
    plt.savefig(
        os.path.join(os.path.dirname(__file__), "figures", tag, "loss.pdf"),
        format="pdf",
    )
    plt.close()


def accuracy_plot(train_history, test_history, tag):
    plt.figure(figsize=(10, 10))
    plt.plot(train_history, label="Train accuracy")
    plt.plot(test_history, label="Test accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend(frameon=False)
    plt.savefig(
        os.path.join(os.path.dirname(__file__), "figures", tag, "accuracy.pdf"),
        format="pdf",
    )
    plt.close()
