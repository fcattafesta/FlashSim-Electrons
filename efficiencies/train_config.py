import os
from training_loop import training_loop
from model import ElectronClassifier, JetClassifier, PhotonClassifier

# GenElectron classifier


def GenElectron_efficiency():
    input_dim = 32
    model = ElectronClassifier(input_dim)
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenElectrons.hdf5")
    train_size = 10000000
    epochs = 500
    lr = 1e-4
    batch_size = 10000
    weight = 10.0
    tag = "electrons"

    training_loop(
        model, input_dim, datapath, train_size, epochs, lr, batch_size, weight, tag
    )


# GenJet classifier


def GenJet_efficiency():
    input_dim = 12
    model = JetClassifier(input_dim)
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenJets.hdf5")
    train_size = 10000000
    epochs = 500
    lr = 1e-4
    batch_size = 10000
    weight = 20.0
    tag = "jets"

    training_loop(
        model, input_dim, datapath, train_size, epochs, lr, batch_size, weight, tag
    )


# GenPhoton classifier


def GenPhoton_efficiency():
    input_dim = 18
    model = PhotonClassifier(input_dim)
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenPhotons.hdf5")
    train_size = 10000000
    epochs = 500
    lr = 1e-4
    batch_size = 10000
    weight = 7.0
    tag = "photons"

    training_loop(
        model, input_dim, datapath, train_size, epochs, lr, batch_size, weight, tag
    )
