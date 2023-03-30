import os
from training_loop import training_loop

# GenElectron classifier


def GenElectron_efficiency():
    input_dim = 32
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenElectrons.hdf5")
    train_size = 4000000
    epochs = 100
    lr = 0.001
    batch_size = 10000
    weight = 9.0
    tag = "electrons"

    training_loop(input_dim, datapath, train_size, epochs, lr, batch_size, weight, tag)


# GenJet classifier


def GenJet_efficiency():
    input_dim = 12
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenJets.hdf5")
    train_size = 4000000
    epochs = 100
    lr = 0.001
    batch_size = 10000
    weight = 19.0
    tag = "jets"

    training_loop(input_dim, datapath, train_size, epochs, lr, batch_size, weight, tag)


# GenPhoton classifier


def GenPhoton_efficiency():
    input_dim = 18
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenPhotons.hdf5")
    train_size = 4000000
    epochs = 100
    lr = 0.001
    batch_size = 10000
    weight = 6.0
    tag = "photons"

    training_loop(input_dim, datapath, train_size, epochs, lr, batch_size, weight, tag)


if __name__ == "__main__":
    GenElectron_efficiency()
    GenJet_efficiency()
    GenPhoton_efficiency()
