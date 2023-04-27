import os
import numpy as np
import torch


from data import isReco_Dataset
from model import ElectronClassifier


def isReco(y_pred):
    p = np.random.rand(y_pred.size)

    # Temporary fix for efficiency model
    # p = np.random.uniform(0, 0.6, y_pred.size)
    return y_pred > p


def compute_efficiency(model, model_path, datapath, device="cuda", batch_size=10000):
    model.load_state_dict(torch.load(model_path))
    model = model.to(device)
    model.eval()
    X = isReco_Dataset(datapath, input_dim, train_size + 3000000, 3000000)
    loader = torch.utils.data.DataLoader(X, batch_size=batch_size, shuffle=False)
    y_pred = np.array([])
    y_true = np.array([])
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device)
            out = model.predict(x)  # predict
            y_pred = np.concatenate((y_pred, out.cpu().numpy().flatten()))
            y_true = np.concatenate((y_true, y.cpu().numpy().flatten()))


    return y_pred, y_true


if __name__ == "__main__":
    input_dim = 32
    model = ElectronClassifier(input_dim)
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenElectrons.hdf5")
    train_size = 10000000
    model_path = os.path.join(os.path.dirname(__file__), "models", "efficiency_electrons.pt")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    y_pred, y_true = compute_efficiency(model, model_path, datapath, device=device)
    
    mask = isReco(y_pred)

    cut = 100

    y_pred = y_pred[:cut]
    y_true = y_true[:cut]
    mask = mask[:cut]

    for a, b, c in zip(y_pred, mask, y_true):
        print(f"Prob:{a} -> Mask:{b} | True {c}")