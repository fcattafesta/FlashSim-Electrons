import os
import ROOT

ROOT.gInterpreter.ProcessLine('#include "extraction.h"')

file = os.path.join(os.path.dirname(__file__), "..", "preliminar", "047F4368-97D4-1A4E-B896-23C6C72DD2BE.root")

ROOT.extract(file)
input()