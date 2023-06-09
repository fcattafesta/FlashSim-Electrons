import os
import sys
from preprocessing import make_dataset

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

from columns import gen_ele, gen_pho, gen_jet

from prep_actions_ele import target_dictionary as target_dictionary_ele
from prep_actions_pho import target_dictionary as target_dictionary_pho
from prep_actions_jet import target_dictionary as target_dictionary_jet

dataset_path = os.path.join(os.path.dirname(__file__), "..", "extraction", "dataset")

nfiles = 9

# GenElectron training dataset

filenames = [f"MElectrons_{i}_ele.root:MElectrons" for i in range(nfiles)]

filepaths = [os.path.join(dataset_path, f) for f in filenames]

scale_name = "scale_factors_ele.json"

make_dataset(filepaths, "MElectrons_ele", target_dictionary_ele, scale_name, gen_ele)


# GenPhoton training dataset

filenames = [f"MElectrons_{i}_pho.root:MElectrons" for i in range(nfiles)]

filepaths = [os.path.join(dataset_path, f) for f in filenames]

scale_name = "scale_factors_pho.json"

make_dataset(filepaths, "MElectrons_pho", target_dictionary_pho, scale_name, gen_pho)


# GenJet training dataset

filenames = [f"MElectrons_{i}_jet.root:MElectrons" for i in range(nfiles)]

filepaths = [os.path.join(dataset_path, f) for f in filenames]

scale_name = "scale_factors_jet.json"

make_dataset(filepaths, "MElectrons_jet", target_dictionary_jet, scale_name, gen_jet)
