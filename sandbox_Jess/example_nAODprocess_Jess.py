#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from config import *
from SF_Eff_cfg import *
from modules.singleLepEventSelector import *
from modules.GenPartDaughterMap import *
from modules.CommonCalc import *
from modules.singleLepCalc import *
from modules.JetSubCalc import *
from modules.btagSFProducerForLJMet import *
from modules.TpTpCalc import *
from modules.TTbarMassCalc import *
from modules.BestCalc import *
from modules.DeepAK8Calc import *

def put_together_trig_ROOT_string(trigger_paths):
  triggers = '( '
  for trig in trigger_paths:
    triggers = triggers + trig + '==1'
    if trig!=trigger_paths[-1]:  
      triggers = triggers + ' || '
  triggers = triggers + ' )'
  print '\nTRIGGERS =',triggers,'\n'  
  return triggers 

if isMC and MC_trigger_list:
  triggers = put_together_trig_ROOT_string(MC_trigger_list)
else: 
  triggers = put_together_trig_ROOT_string(data_trigger_list)

preselection = ""
for presel in Preselection_list:
  preselection = preselection + presel
  if presel!=Preselection_list[-1]: 
    preselection = preselection + " && "

if DoLepJetCleaning:
  lepjetDR = LepJetCleaning_DR
else:
  lepjetDR = -1

# customized module constructors
singleLepEventSelectorConstr = lambda : singleLepEventSelector(muSelCond, elSelCond, jetSelCond, jetP4SelCond, fatJetSelCond, fatJetP4SelCond, lepjetDR)
GenPartDaughterMapConstr = lambda : GenPartDaughterMap(isMC)
singleLepCalcConstr = lambda : singleLepCalc(isMC, MC_trigger_list, data_trigger_list, cleanGenJets, keepPDGID, keepMomPDGID, keepPDGIDForce, keepStatusForce)
btagSFProducerForLJMetConstr = lambda : btagSFProducerForLJMet(era, algo, btagOP)
JetSubCalcConstr = lambda : JetSubCalc(isMC, btagOP, bTagCut, puppiCorrfilepath, FatJetSD_JMS_sd, FatJetSD_JMS_sd_up, FatJetSD_JMS_sd_dn)
modules_to_run =[singleLepEventSelectorConstr(),GenPartDaughterMapConstr(),CommonCalc(), singleLepCalcConstr(), btagSFProducerForLJMetConstr(), JetSubCalcConstr(), TpTpCalc(), TTbarMassCalc(), BestCalc(), DeepAK8Calc()]

p=PostProcessor("nanoAODSkim",files,cut=triggers+" && "+preselection,branchsel="keep_and_drop_input.txt", outputbranchsel="keep_and_drop_output.txt",modules=modules_to_run,noOut=False,histFileName=histFileName_,histDirName=histDirName_)
p.run()



