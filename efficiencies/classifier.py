import h5py
import os
import torch
from torch import nn

# Define the model


class dataset(torch.utils.data.Dataset):
    def __init__(self, filepath, start, stop):

        h5py_file = h5py.File(filepath, "r")
        self.X = torch.tensor(
            h5py_file["GenElectrons"][start : (start + stop), 0:38], dtype=torch.float32
        )
        self.y = torch.tensor(
            h5py_file["GenElectrons"][start : (start + stop), -1], dtype=torch.long
        )

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class Classifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.softmax(x)
        return x


# Define the training loop


def train(dataloader, model, loss, optimizer, device):

    model.train()

    size = len(dataloader.dataset)

    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        pred = model(X)
        loss = loss(pred, y)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(dataloader, model, loss_fn, device):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(
        f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n"
    )


def main_loop():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Classifier(38, 128, 1).to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenElectrons.hdf5")
    train_dataset = dataset(datapath, 0, 1300000)
    test_dataset = dataset(datapath, 1300000, 1400000)

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
    main_loop()
