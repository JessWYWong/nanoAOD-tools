#!/usr/bin/env python
import time
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from singleLepEventSelector import *
from CommonCalc import *
from singleLepCalc import *
#from Plotter import *
start_time = time.time() #probably not the most accurate, but sufficient. 

files=["root://cmsxrootd.fnal.gov//store/mc/RunIIFall17NanoAOD/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/70000/C6AABB0E-33AC-E811-8B63-0CC47A7C3404.root"]

for inputFileName in files:
  isSig  = ("prime" in inputFileName or "X53" in inputFileName or "ChargedHiggs_Hplus" in inputFileName)
  isMadgraphBkg = (("WJetsToLNu" in inputFileName or "DYJetsToLL_M-50" in inputFileName or "QCD" in inputFileName) and "madgraph" in inputFileName)
  isTOP = ("Mtt" in inputFileName or "ST" in inputFileName or "TTZ" in inputFileName or "TTW" in inputFileName or "TTTo" in inputFileName)
  isTT = ("TT_Tune" in inputFileName or "Mtt" in inputFileName or "TTTo" in inputFileName)
  isSTt = "ST_t-channel" in inputFileName
  isSTtW = "ST_tW" in inputFileName
  isTTV = ("TTZ" in inputFileName or "TTW" in inputFileName)
  isVV = ("WW_" in inputFileName or "WZ_" in inputFileName or "ZZ_" in inputFileName)
  isMC = not "Single" in inputFileName
  isSM = "SingleMuon" in inputFileName
  isSE = "SingleElectron" in inputFileName
killHF=False

histFileName_ = None
histDirName_ = None

#Preselection Cuts
npvsCut=0 # more than _ good PV
#FlagMETCut=1 # boolean : 1 for true and 0 for false
metCut=30
nJetsCut=2 # >=
JetLeadPtCut=20
nlepCut=1 # mu/el
lepPtCut=50
lepLeadptCut=50 # corresponds to nlep
nAK8jetsCut=0

MC_triggers = "(HLT_Ele35_WPTight_Gsf==1 || HLT_Ele38_WPTight_Gsf==1 || HLT_Ele40_WPTight_Gsf==1 || HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1 || HLT_Ele15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Ele15_IsoVVVL_PFHT450==1 || HLT_Ele50_IsoVVVL_PFHT450==1 || HLT_Ele15_IsoVVVL_PFHT600==1 || HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165==1 || HLT_Ele115_CaloIdVT_GsfTrkIdT==1 || HLT_IsoMu24==1 || HLT_IsoMu24_eta2p1==1 || HLT_IsoMu27==1 || HLT_IsoMu30==1 || HLT_Mu50==1 || HLT_Mu55==1 || HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5==1 || HLT_Mu15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Mu15_IsoVVVL_PFHT450==1 || HLT_Mu50_IsoVVVL_PFHT450==1 || HLT_Mu15_IsoVVVL_PFHT600==1)"
data_triggers = "(HLT_Ele35_WPTight_Gsf==1 || HLT_Ele38_WPTight_Gsf==1 || HLT_Ele40_WPTight_Gsf==1 || HLT_Ele28_eta2p1_WPTight_Gsf_HT150==1 || HLT_Ele15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Ele15_IsoVVVL_PFHT450==1 || HLT_Ele50_IsoVVVL_PFHT450==1 || HLT_Ele15_IsoVVVL_PFHT600==1 || HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165==1 || HLT_Ele115_CaloIdVT_GsfTrkIdT==1 || HLT_IsoMu24==1 || HLT_IsoMu24_eta2p1==1 || HLT_IsoMu27==1 || HLT_IsoMu30==1 || HLT_Mu50==1 || HLT_Mu55==1 || HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5==1 || HLT_Mu15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Mu15_IsoVVVL_PFHT450==1 || HLT_Mu50_IsoVVVL_PFHT450==1 || HLT_Mu15_IsoVVVL_PFHT600==1)"

#MC_triggers = "(HLT_Ele15_IsoVVVL_PFHT450==1 || HLT_Ele15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Ele50_IsoVVVL_PFHT450==1 || HLT_Ele15_IsoVVVL_PFHT600==1 || HLT_Ele35_WPTight_Gsf==1 || HLT_Ele38_WPTight_Gsf==1  || HLT_Mu50==1 || HLT_Mu15_IsoVVVL_PFHT450==1 || HLT_Mu15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5==1 || HLT_Mu50_IsoVVVL_PFHT450==1 || HLT_Mu15_IsoVVVL_PFHT600==1)"
#data_triggers ="(HLT_Ele15_IsoVVVL_PFHT450==1 || HLT_Ele15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Ele50_IsoVVVL_PFHT450==1 || HLT_Ele15_IsoVVVL_PFHT600==1 || HLT_Ele35_WPTight_Gsf==1 || HLT_Ele38_WPTight_Gsf==1 || HLT_Mu50==1 || HLT_Mu15_IsoVVVL_PFHT450==1 || HLT_Mu15_IsoVVVL_PFHT450_PFMET50==1 || HLT_Mu15_IsoVVVL_PFHT450_CaloBTagCSV_4p5==1 || HLT_Mu50_IsoVVVL_PFHT450==1 || HLT_Mu15_IsoVVVL_PFHT600==1)"
if isMC:
  triggers=MC_triggers
else:
  triggers=data_triggers

modules_to_run =[singleLepEventSelector()]#,CommonCalc(),singleLepCalc()]

preselection="PV_npvsGood > "+str(npvsCut)+" && Flag_METFilters"+" && MET_pt > "+str(metCut)+" && nJet>="+str(nJetsCut)+" && (nMuon>="+str(nlepCut)+" || nElectron>="+str(nlepCut)+" ) && nFatJet>="+str(nAK8jetsCut)


p=PostProcessor("nanoAODSkim",files,cut=triggers+" && "+preselection,branchsel="keep_and_drop_input.txt",modules=modules_to_run,noOut=False,histFileName=histFileName_,histDirName=histDirName_)
p.run()

total_time_seconds = time.time() - start_time
hours =  math.floor(total_time_seconds/3600.)
minutes = int( (total_time_seconds - hours*3600) / 60 )
seconds = int(total_time_seconds - hours*3600 - minutes*60) 
print("--- PostProcessor took %s hours %s mins %s seconds ---" % (hours,minutes,seconds))
