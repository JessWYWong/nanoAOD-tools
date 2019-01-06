#!/usr/bin/env python
import time
import os, sys, math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module


# from TestCalc import *
# from Plotter import *
from ljmet_modules.EventSelector import *
from ljmet_modules.CommonCalc import *
from ljmet_modules.singleLepCalc import *


modules_to_run =[EventSelector(),CommonCalc(),singleLepCalc()]
histFileName_	= None
histDirName_ 	= None

### if running Plotter(), histFileName and histDirName mustbe defined. Eg.:
# modules_to_run =[EventSelector(),TestCalc(),Plotter()]
# histFileName_="histOut.root",
# histDirName_="plots",


#define preselection
presel_el	= "( Electron_pt[0] > 40 && Electron_pt[1] > 35 )"
presel_mu	= "( Muon_pt[0] > 40 && Muon_pt[1] > 35 )"
presel_jet	= "( Jet_pt[0] > 30 )"
preselection	= presel_el + " && " + presel_mu + " && " + presel_jet

triggers	= "( HLT_Mu37_Ele27_CaloIdL_MW==1 || HLT_Mu27_Ele37_CaloIdL_MW==1 || HLT_Mu37_TkMu27==1|| HLT_Ele27_Ele37_CaloIdL_MW==1 )"

outputDir_	= "TTTT_TuneCP5_13TeV-amcatnlo-pythia8"
isMC = True
inputFiles_	= [
				"root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_pilot_94X_mc2017_realistic_v14-v1/90000/EA11BEB7-B732-E811-A77A-0CC47AA992AC.root",
				"root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_pilot_94X_mc2017_realistic_v14-v1/90000/84701630-B732-E811-9DF0-44A842CF058B.root",
				]

# outputDir_	= "SingleElectron_Run2017F-31Mar2018-v1"
# isMC = False
# inputFiles_	= [
# 				"root://cmsxrootd.fnal.gov//store/data/Run2017F/SingleElectron/NANOAOD/31Mar2018-v1/80000/FAA47698-566B-E811-B4D3-FA163E54DF16.root",
# 				"root://cmsxrootd.fnal.gov//store/data/Run2017F/SingleElectron/NANOAOD/31Mar2018-v1/80000/F086F54D-766C-E811-A104-FA163EC00689.root",
# 				"root://cmsxrootd.fnal.gov//store/data/Run2017F/SingleElectron/NANOAOD/31Mar2018-v1/80000/ECE221C9-F36C-E811-93AA-FA163E103522.root",
# 				"root://cmsxrootd.fnal.gov//store/data/Run2017F/SingleElectron/NANOAOD/31Mar2018-v1/80000/E637265C-376B-E811-8E60-FA163E5C6C5F.root",
# 				"root://cmsxrootd.fnal.gov//store/data/Run2017F/SingleElectron/NANOAOD/31Mar2018-v1/80000/E2756E6A-736C-E811-AFE0-FA163E1A0589.root",
# 				]

								
if (isMC): 
	print 'isMC',isMC
	jsonFile = None
else: 
	print 'isMC',isMC
	jsonFile = "Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"
	print 'Using jsonFile:',jsonFile

haddFileName_	= outputDir_+'_hadd.root'

start_time = time.time() #probably not the most accurate, but sufficient. 

p=PostProcessor(outputDir=outputDir_,
				inputFiles=inputFiles_,
				postfix="_nAODtoLJMet",
				haddFileName=haddFileName_,
				jsonInput=jsonFile,
				cut=preselection+" && "+triggers,
				branchsel="keep_and_drop_input.txt",
				outputbranchsel="keep_and_drop_output.txt",
				modules=modules_to_run,
				noOut=False,
				histFileName=histFileName_,
				histDirName=histDirName_,
				fwkJobReport=True
				)
p.run()

### measure time elapsed
total_time_seconds = time.time() - start_time
hours =  math.floor(total_time_seconds/3600.)
minutes = int( (total_time_seconds - hours*3600) / 60 )
seconds = int(total_time_seconds - hours*3600 - minutes*60) 
print("--- PostProcessor took %s mins %s seconds ---" % (minutes,seconds))