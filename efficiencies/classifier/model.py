import torch
from torch import nn


class BinaryClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x


def accuracy(y_pred, y_true):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))
    correct_results_sum = (y_pred_tag == y_true).sum().float()
    acc = correct_results_sum / y_true.shape[0]
    acc = torch.round(acc * 100)
    return acc


def train(train_dataloader, test_dataloader, model, loss_fn, optimizer, device):
    epoch_loss = 0
    epoch_acc = 0

    model.train()
    size = len(train_dataloader.dataset)
    for batch, (X, y) in enumerate(train_dataloader):
        X, y = X.to(device), y.to(device)

        optimizer.zero_grad()
        pred = model(X)
        loss = loss_fn(pred, y)
        acc = accuracy(pred, y)

        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        epoch_acc += acc.item()

        # if batch % 100 == 0:
        #     loss, current = loss.item(), (batch + 1) * len(X)
        #     print(f"Loss: {loss}  [{current}/{size}]")

    print(
        f"Train | Loss = {epoch_loss/len(train_dataloader):.4f} | Acc. = {epoch_acc/len(train_dataloader):.2f} | "
    )

    model.eval()
    test_loss = 0
    test_accuracy = 0
    with torch.no_grad():
        for X, y in test_dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            test_accuracy += accuracy(pred, y).item()

    print(
        f"Test  | Loss = {test_loss/len(test_dataloader):.4f} | Acc. = {test_accuracy/len(test_dataloader):.2f} |"
    )
    print("--------------------------------------")
