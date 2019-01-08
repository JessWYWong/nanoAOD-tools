#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

class singleLepEventSelector(Module):
  def __init__(self):
    print 'Running singleLepEventSelector module'
    pass
  def analyze(self, event):
    #Selection

    """process event, return True (go to next module) or False (fail, go to next event)"""
    electrons = list(Collection(event, "Electron"))
    muons = list(Collection(event, "Muon"))
    jets = Collection(event, "Jet")
    jetAK8s = Collection(event, "FatJet")

    #select tight muons
    SelmuP4=[]
    Selmu=[]
    SelelP4=[]
    Selel=[]
    for mu in muons :     #loop on muons
      if mu.tightId>0 and mu.miniPFRelIso_all<0.1 and mu.dxy<0.2 and mu.dz<0.5 and mu.pt>30. and math.fabs(mu.eta)<2.4:
        Selmu.append(mu)
        SelmuP4.append(mu.p4())
    for el in electrons :     #loop on muons
      elSCeta=math.fabs(el.eta+el.deltaEtaSC)
      if el.mvaFall17noIso_WP90>0 and el.miniPFRelIso_all<0.1 and elSCeta<2.5 and (elSCeta<1.4442 or elSCeta>1.566) and el.pt>30.:
        Selel.append(el)
        SelelP4.append(el.p4())
    #select events with only 1 lepton
    isElecton=0
    isMuon=0
    if len(SelelP4) == 1 and len(SelmuP4)== 0:
      isElecton=1
    elif len(SelmuP4) == 1 and len(SelelP4) == 0:
      isMuon=1
    else:
      return False

    #if(isSM and isElectron == 1):
    #  return False
    #if(isSE and isMuon == 1):
    #  return False

    #lep-jet cleaning
    SeljetP4=[]
    Seljet=[]
    leadingJetpt=0
    for jet in jets:
      jetP4=jet.p4()
      for imu in SelmuP4:
        if jet.p4().DeltaR(imu)< 0.4:
          jetP4 = jet.p4() - imu
      for iel in SelelP4:
      	if jet.p4().DeltaR(iel)< 0.4:
      	  jetP4 = jet.p4() - iel
      if jet.jetId>0 and jetP4.Pt()>30 and math.fabs(jetP4.Eta())<3.0: # or (killHF and math.fabs(jetP4.Eta()) > 2.4)):
        SeljetP4.append(jetP4)
        Seljet.append(jet)
        if jetP4.Pt() > leadingJetpt:
          leadingJetpt=jetP4.Pt()
    #select events with at least 2 jets and leading jet Pt >20
    if not (len(Seljet)>=2 and leadingJetpt>20):
      return False
    
    return True

