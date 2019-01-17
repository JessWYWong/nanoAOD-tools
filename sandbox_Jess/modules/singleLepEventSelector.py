#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math
from modules.LepJetCleaning import *

class singleLepEventSelector(Module):
  def __init__(self, muSelCond, elSelCond, jetSelCond, jetP4SelCond, fatJetSelCond, fatJetP4SelCond, lepjetDR):
    print 'Running singleLepEventSelector module'
    self.nLep = 1
    self.muSelection = muSelCond
    self.elSelection = elSelCond
    self.jetSelection = jetSelCond
    self.jetP4Selection = jetP4SelCond
    self.jetAK8Selection = fatJetSelCond
    self.jetAK8P4Selection = fatJetP4SelCond
    self.LepJetCleaning_DR = lepjetDR
    pass
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    inputFileName=inputFile.GetName()
    self.isSM = "SingleMuon" in inputFileName
    self.isSE = "SingleElectron" in inputFileName
    
  def beginJob(self,histFile=None,histDirName=None):    
    Module.beginJob(self,histFile,histDirName)
    

  def analyze(self, event):
    Selmu = []
    Selel = []
    JetsP4 = []
    Seljet = []
    SeljetP4 = []
    JetAK8sP4 = []
    SeljetAK8 = []
    SeljetAK8P4 = []
    leadingJetpt = 0
    leadingJetAK8pt = 0
    #Selection
    """process event, return True (go to next module) or False (fail, go to next event)"""
    electrons = list(Collection(event, "Electron"))
    muons = list(Collection(event, "Muon"))
    jets = Collection(event, "Jet")
    jetAK8s = Collection(event, "FatJet")

    #select tight muons
    for mu in muons :
      passed_selection = True
      for attr in self.muSelection.keys():
        x = mu.__getattr__(attr)
        if attr=="eta" or attr=="Eta" :
          x = math.fabs(x)
        if eval("x "+self.muSelection[attr]):
          continue
        else:
          passed_selection = False
      if passed_selection:
        Selmu.append(mu)

    for el in electrons :
      passed_selection = True
      for attr in self.elSelection.keys():
        x = el.__getattr__(attr)
        if attr=="eta" or attr=="Eta" :
          x = math.fabs(x+el.deltaEtaSC)
        if eval("x "+self.elSelection[attr]):
          continue
        else:
          passed_selection = False
          break
      if not (math.fabs(el.eta+el.deltaEtaSC)<1.4442 or math.fabs(el.eta+el.deltaEtaSC)>1.566):
      	passed_selection = False
      if passed_selection:
        Selel.append(el)

    #select events with only 1 lepton
    isElectron=0
    isMuon=0
    if len(Selel) == 1 and len(Selmu)== 0:
      isElecton=1
    elif len(Selmu) == 1 and len(Selel) == 0:
      isMuon=1
    else:
      return False
   
    if(self.isSM and isElectron == 1):
     return False
    if(self.isSE and isMuon == 1):
     return False

    #lep-jet cleaning
    Cleaned = False
    if self.LepJetCleaning_DR > 0:
      CleanJetModule = LepJetCleaning(jets, Selmu, Selel, self.LepJetCleaning_DR)
      CleanJetAk8Module = LepJetCleaning(jetAK8s, Selmu, Selel, self.LepJetCleaning_DR)
      JetsP4 = CleanJetModule.run()
      JetAK8sP4 = CleanJetAk8Module.run()
      Cleaned = True

    for i,jet in enumerate(jets):
      passed_selection = True
      if Cleaned:
        jetP4 = JetsP4[i]
      else:
        jetP4 = jet.p4()

      for attr in self.jetSelection.keys():
        x = jet.__getattr__(attr)
        if attr=="eta" or attr=="Eta" :
          x = math.fabs(x)
        if eval("x "+self.jetSelection[attr]):
          continue
        else:
          passed_selection = False
          break

      Pt , Eta, Phi, E, mass = jetP4.Pt(), math.fabs(jetP4.Eta()), jetP4.Phi(), jetP4.E(), jetP4.M()
      for attr in self.jetP4Selection.keys():        
        if eval(attr+self.jetP4Selection[attr]):
          continue
        else:
          passed_selection = False
          break

      if passed_selection:
        Seljet.append(jet)
        SeljetP4.append(jetP4)
        if jetP4.Pt() > leadingJetpt:
          leadingJetpt=jetP4.Pt()

    #select events with at least 2 jets and leading jet Pt >20
    if not (len(Seljet)>=2 and leadingJetpt>20):
      return False

    for i,jetak8 in enumerate(jetAK8s):
      passed_selection = True
      if Cleaned:
        jetak8P4 = JetAK8sP4[i]
      else:
        jetak8P4 = jetak8.p4()

      for attr in self.jetAK8Selection.keys():
        x = jetak8.__getattr__(attr)
        if attr=="eta" or attr=="Eta" :
          x = math.fabs(x)
        if eval("x "+self.jetAK8Selection[attr]):
          continue
        else:
          passed_selection = False
          break

      Pt , Eta, Phi, E, mass = jetak8P4.Pt(), math.fabs(jetak8P4.Eta()), jetak8P4.Phi(), jetak8P4.E(), jetak8P4.M()
      for attr in self.jetAK8P4Selection.keys():        
        if eval(attr+self.jetAK8P4Selection[attr]):
          continue
        else:
          passed_selection = False
          break

      if passed_selection:
        SeljetAK8.append(jetak8)
        SeljetAK8P4.append(jetak8P4)
        if jetak8P4.Pt() > leadingJetAK8pt:
          leadingJetAK8pt=jetak8P4.Pt()

    
    event.isElectron = isElectron
    event.isMuon = isMuon
    event.Selel = Selel
    event.nSelel = len(Selel)
    event.Selmu = Selmu
    event.nSelmu = len(Selmu)
    event.Seljet = Seljet
    event.nSeljet = len(Seljet)
    event.SeljetP4 = SeljetP4
    event.nSeljetP4 = len(SeljetP4)
    event.SeljetAK8 = SeljetAK8
    event.nSeljetAK8 = len(SeljetAK8)
    event.SeljetAK8P4 = SeljetAK8P4
    event.nSeljetAK8P4 = len(SeljetAK8P4)


    return True



