#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from EventSelector import *
from TestCalc import *
from Plotter import *

preselection="(Jet_pt[0] > 30 && Electron_pt[0] > 40 && Electron_pt[1] > 35 && Muon_pt[0] > 40 && Muon_pt[1] > 35)"

triggers = "(HLT_Mu37_Ele27_CaloIdL_MW==1 || HLT_Mu27_Ele37_CaloIdL_MW==1 || HLT_Mu37_TkMu27==1|| HLT_Ele27_Ele37_CaloIdL_MW==1)"

files=["root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_pilot_94X_mc2017_realistic_v14-v1/90000/EA11BEB7-B732-E811-A77A-0CC47AA992AC.root"]

modules_to_run =[EventSelector(),TestCalc()]
histFileName_ = None
histDirName_  = None

# modules_to_run =[EventSelector(),TestCalc(),Plotter()]
# histFileName_="histOut.root",
# histDirName_="plots",

p=PostProcessor("nanoAODSkim",
				files,
				cut=preselection+" && "+triggers,
				branchsel="keep_and_drop_input.txt",
				outputbranchsel="keep_and_drop_output.txt",
				modules=modules_to_run,
				noOut=False,
				histFileName=histFileName_,
				histDirName=histDirName_,
				)
p.run()
