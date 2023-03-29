import os
from training_loop import training_loop

# GenElectron classifier


def GenElectron_efficiency():
    input_dim = 38
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenElectron.hdf5")
    train_size = 4000000
    epochs = 100
    lr = 0.001
    batch_size = 10000
    tag = "electrons"

    training_loop(input_dim, datapath, train_size, epochs, lr, batch_size, tag)


# GenJet classifier


def GenJet_efficiency():
    input_dim = 18
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenJet.hdf5")
    train_size = 4000000
    epochs = 100
    lr = 0.001
    batch_size = 10000
    tag = "jets"

    training_loop(input_dim, datapath, train_size, epochs, lr, batch_size, tag)


# GenPhoton classifier


def GenPhoton_efficiency():
    input_dim = 24
    datapath = os.path.join(os.path.dirname(__file__), "dataset", "GenPhoton.hdf5")
    train_size = 4000000
    epochs = 100
    lr = 0.001
    batch_size = 10000
    tag = "photons"

    training_loop(input_dim, datapath, train_size, epochs, lr, batch_size, tag)


if __name__ == "__main__":
    GenElectron_efficiency()
    GenJet_efficiency()
    GenPhoton_efficiency()
