# the loop for generating new events starting from gen-level information in the files
import sys
import os

from tqdm import tqdm
import torch

sys.path.insert(0, os.path.join("..", "..", "models"))

from modded_basic_nflow import load_mixture_model
import nbd_func

if __name__ == "__main__":

    root = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/"
    new_root = "/gpfs/ddn/cms/user/cattafe/DYJets/EM1/"
    files_paths = [
        os.path.join(d, f)
        for d in os.listdir(root)
        for f in os.listdir(os.path.join(root, d))
    ]

    # files_paths = files_paths[:2]

    print(f"We will process a total of {len(files_paths)} files")

    # specify device and load models
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

    ele_flow, _, _, _, trh, tsh = load_mixture_model(
        device=device,
        model_dir=os.path.dirname(__file__),
        filename="EM1/checkpoint-latest.pt",
    )

    ele_flow = ele_flow.to(device)

    # generation loop
    for path in tqdm(files_paths):
        path_str = str(path)
        nbd_func.nbd(ele_flow, root, path_str, new_root)
