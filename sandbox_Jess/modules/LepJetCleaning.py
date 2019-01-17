#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
# from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

class LepJetCleaning:
  def __init__(self, jetCollection, SelmuCollection, SelelCollection, lepjetDR):
    # 'Running singleLepEventSelector module'
    self.jets=jetCollection
    self.Selmu = SelmuCollection
    self.Selel = SelelCollection
    self.LepJetCleaning_DR = lepjetDR
    # setattr( self, "CleanedJetP4", CleanedJetP4)
    pass

  def run(self):
    #Selection
    CleanedJetP4 = []
    """process event, return True (go to next module) or False (fail, go to next event)"""
    for jet in self.jets:
      jetP4=0
      jetP4=jet.p4()
      for imu in self.Selmu:
        if jetP4.DeltaR(imu.p4())< self.LepJetCleaning_DR:
          jetP4 = jetP4 - imu.p4()
      for iel in self.Selel:
        if jetP4.DeltaR(iel.p4())< self.LepJetCleaning_DR:
          jetP4 = jetP4 - iel.p4()
      CleanedJetP4.append(jetP4) # fill new branch

    return CleanedJetP4

