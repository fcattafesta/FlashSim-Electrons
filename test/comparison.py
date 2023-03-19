import os
import ROOT

ROOT.gInterpreter.ProcessLine('#include "match.h"')

ROOT.EnableImplicitMT()

# Drell-Yan MC

full_path = "/gpfs/ddn/srm/cms//store/mc/RunIIAutumn18NanoAODv6/DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano25Oct2019_102X_upgrade2018_realistic_v20-v1/230000/8244ED99-0F95-9D4F-B393-22EBC589A46D.root"
flash_path = "/gpfs/ddn/cms/user/cattafe/DYJets/EM1/230000/8244ED99-0F95-9D4F-B393-22EBC589A46D_synth.root"

def compare(full, flash, col, range):

    f = ROOT.TFile(full)
    d_full = ROOT.RDataFrame("Events", f)
    ROOT.match(d_full, f"M{col}")
    f.Close()

    f = ROOT.TFile("output.root")
    d_full = ROOT.RDataFrame("Events", f)
    f.Close()

    f = ROOT.TFile(flash)
    d_flash = ROOT.RDataFrame("Events", f)
    f.Close()
    os.system("rm output.root")

    nbins = 50
    
    h_full = d_full.Histo1D({"full", "", nbins, range[0], range[1]}, str(f"M{col})"))
    h_flash = d_flash.Histo1D({"flash", "", nbins, range[0], range[1]}, col)

    c = ROOT.TCanvas()
    h_full.Draw()
    h_flash.Draw("same")

    c.SaveAs(os.path.join("figures", f"comparison_{col}.png"))


if __name__ == "__main__":

    compare(full_path, flash_path, "Electron_pt", (0, 200))