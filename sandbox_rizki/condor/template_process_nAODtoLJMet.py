#!/usr/bin/env python
import time
import os, sys, math
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

workDir=os.environ['CMSSW_BASE']+'/src/PhysicsTools/NanoAODTools/sandbox_rizki/'
sys.path.append(workDir)

# from TestCalc import *
# from Plotter import *
from ljmet_modules.EventSelector import *
from ljmet_modules.CommonCalc import *
from ljmet_modules.singleLepCalc import *


modules_to_run =[EventSelector(),CommonCalc(),singleLepCalc()]
histFileName_	= None
histDirName_ 	= None


#define preselection
presel_el	= "( Electron_pt[0] > 30 )"
presel_mu	= "( Muon_pt[0] > 30 )"
presel_jet	= "( Jet_pt[0] > 30 )"
preselection	= presel_el + " && " + presel_mu + " && " + presel_jet


def put_together_trig_ROOT_string(trigger_paths):
	triggers = '( '
	for trig in trigger_paths:
		triggers = triggers + trig + '==1'
		if trig!=trigger_paths[-1]:  
			triggers = triggers + ' || '
	triggers = triggers + ' )'
	print '\nTRIGGERS=',triggers,'\n'	
	return triggers	

trigger_paths =[

	'HLT_Ele35_WPTight_Gsf',
	'HLT_Ele38_WPTight_Gsf',
	'HLT_Ele40_WPTight_Gsf',
	'HLT_Ele28_eta2p1_WPTight_Gsf_HT150',
	'HLT_Ele15_IsoVVVL_PFHT450_PFMET50',
	'HLT_Ele15_IsoVVVL_PFHT450',
	'HLT_Ele50_IsoVVVL_PFHT450',
	'HLT_Ele15_IsoVVVL_PFHT600',
	'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165',
	'HLT_Ele115_CaloIdVT_GsfTrkIdT',

	'HLT_IsoMu24',
	'HLT_IsoMu24_eta2p1',
	'HLT_IsoMu27',
	'HLT_IsoMu30',
	'HLT_Mu50',
	'HLT_Mu55',
	'HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5',
	'HLT_Mu15_IsoVVVL_PFHT450_PFMET50',
	'HLT_Mu15_IsoVVVL_PFHT450',
	'HLT_Mu50_IsoVVVL_PFHT450',
	'HLT_Mu15_IsoVVVL_PFHT600',

	]

triggers = put_together_trig_ROOT_string(trigger_paths)

outputDir_	= 'OUTPUTDIR'
isMC = ISMC
inputFiles_	= [
				INPUTFILES
				]
								
if (isMC): 
	print 'isMC',isMC
	jsonFile = None
else: 
	print 'isMC',isMC
	jsonFile = workDir+'/data/json/'+'JSON'
	print 'Using jsonFile:',jsonFile

haddFileName_	= outputDir_+'.root'
os.system('cp -v '+workDir+'../scripts/haddnano.py .')

start_time = time.time() #probably not the most accurate, but sufficient. 

p=PostProcessor(outputDir=outputDir_,
				inputFiles=inputFiles_,
				postfix="_nAODtoLJMet",
				haddFileName=haddFileName_,
				jsonInput=jsonFile,
				cut=preselection+" && "+triggers,
				branchsel=workDir+"/condor/keep_and_drop_input.txt",
				outputbranchsel=workDir+"/condor/keep_and_drop_output.txt",
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