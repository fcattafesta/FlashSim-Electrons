import os
import sys
from preprocessing import make_dataset

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

from columns import gen_ele, gen_pho, gen_jet

dataset_path = os.path.join(os.path.dirname(__file__), "..", "extraction", "dataset")

# GenElectron training dataset

filenames = [f"MElectrons_{i}_ele.root:MElectrons" for i in range(9)]

filepaths = [os.path.join(dataset_path, f) for f in filenames]

scale_name = "scale_factors_ele.json"

make_dataset(filepaths, "MElectrons_ele", scale_name, gen_ele)


# GenPhoton training dataset

filenames = [f"MElectrons_{i}_pho.root:MElectrons" for i in range(9)]

filepaths = [os.path.join(dataset_path, f) for f in filenames]

scale_name = "scale_factors_pho.json"

make_dataset(filepaths, "MElectrons_pho", scale_name, gen_pho)


# GenJet training dataset

filenames = [f"MElectrons_{i}_jet.root:MElectrons" for i in range(9)]

filepaths = [os.path.join(dataset_path, f) for f in filenames]

scale_name = "scale_factors_jet.json"

make_dataset(filepaths, "MElectrons_jet", scale_name, gen_jet)
