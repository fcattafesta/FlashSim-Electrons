import torch
from torch import nn


class ElectronClassifier(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 32)
        self.fc4 = nn.Linear(32, 1)
        self.drop = nn.Dropout(0.1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        return x

    def predict(self, x):
        pred = torch.sigmoid(self.forward(x))
        return pred


class PhotonClassifier(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 512)
        self.fc2 = nn.Linear(512, 512)
        self.fc2_1 = nn.Linear(512, 128)
        self.fc2_2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, 32)
        self.fc4 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc2_1(x)
        x = self.relu(x)
        x = self.fc2_2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        return x

    def predict(self, x):
        pred = torch.sigmoid(self.forward(x))
        return pred


class JetClassifier(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 512)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 32)
        self.fc4 = nn.Linear(32, 1)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)
        x = self.fc4(x)
        return x

    def predict(self, x):
        pred = torch.sigmoid(self.forward(x))
        return pred


def accuracy(y_pred, y_true):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))
    correct_results_sum = (y_pred_tag == y_true).sum().float()
    acc = correct_results_sum / y_true.shape[0]
    acc = torch.round(acc * 100)
    return acc


def train(
    train_dataloader, test_dataloader, model, loss_fn, optimizer, scheduler, device
):
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

    avg_loss = epoch_loss / len(train_dataloader)
    avg_acc = epoch_acc / len(train_dataloader)

    scheduler.step(avg_loss)

    print(f"Train | Loss = {avg_loss:.4f} | Acc. = {avg_acc:.2f} | ")

    model.eval()
    test_loss = 0
    test_accuracy = 0
    with torch.no_grad():
        for X, y in test_dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            test_accuracy += accuracy(pred, y).item()

    avg_test_loss = test_loss / len(test_dataloader)
    avg_test_acc = test_accuracy / len(test_dataloader)

    print(f"Test  | Loss = {avg_test_loss:.4f} | Acc. = {avg_test_acc:.2f} |")
    print("--------------------------------------")

    return (avg_loss, avg_acc, avg_test_loss, avg_test_acc)
