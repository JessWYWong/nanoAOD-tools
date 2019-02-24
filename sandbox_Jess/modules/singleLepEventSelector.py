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
    # print 'Running singleLepEventSelector module'
    self.Jet_nMax = 999
    self.Jet_nMin = 2
    self.Jet_leadingPt = 20
    self.Lep_nMax = 1
    self.Lep_nMin = 1
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
    """process event, return True (go to next module) or False (fail, go to next event)"""
    electrons = list(Collection(event, "Electron"))
    muons = list(Collection(event, "Muon"))
    jets = Collection(event, "Jet")
    jetAK8s = Collection(event, "FatJet")
    subjets = Collection(event, "SubJet")

    #Selection
    Selmu = []
    Selel = []
    JetsP4 = []
    Seljet = []
    SeljetP4 = []
    JetAK8sP4 = []
    SeljetAK8 = []
    SeljetAK8P4 = []
    Selsubjet = []
    theJetAK8SDSubjetIndex = []
    theJetAK8SDSubjetSize = []
    leadingJetpt = 0
    leadingJetAK8pt = 0
    
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

    nLep = len(Selel)+len(Selmu)

    #select events with only desired number of leptons
    if nLep<self.Lep_nMin or nLep>self.Lep_nMax:
      return False

    isElectron=0
    isMuon=0
    if nLep == 1:
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

    #select events with desired number of jets and leading jet Pt > cut value
    if not (len(Seljet)>=self.Jet_nMin and len(Seljet)<=self.Jet_nMax and leadingJetpt>self.Jet_leadingPt):
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

        theJetAK8SDSubjetIndex.append(len(Selsubjet))
        count = 0
        if jetak8.subJetIdx1 >=0 and jetak8.subJetIdx1 < event.nSubJet:
          Selsubjet.append(subjets.__getitem__(jetak8.subJetIdx1))
          count += 1
        if jetak8.subJetIdx2 >=0 and jetak8.subJetIdx2 < event.nSubJet:
          Selsubjet.append(subjets.__getitem__(jetak8.subJetIdx2))
          count +=1
        theJetAK8SDSubjetSize.append(count)


    
    event.isElectron = isElectron
    event.isMuon = isMuon
    event.Selel = Selel
    event.nSelel = len(Selel)
    event.Selmu = Selmu
    event.nSelmu = len(Selmu)
    event.Seljet = Seljet
    event.nSeljet = len(Seljet)
    event.SeljetP4 = SeljetP4
    event.SeljetAK8 = SeljetAK8
    event.nSeljetAK8 = len(SeljetAK8)
    event.SeljetAK8P4 = SeljetAK8P4
    event.Selsubjet = Selsubjet
    event.nSelsubjet = len(Selsubjet)
    event.theJetAK8SDSubjetIndex = theJetAK8SDSubjetIndex
    event.theJetAK8SDSubjetSize = theJetAK8SDSubjetSize

    return True



