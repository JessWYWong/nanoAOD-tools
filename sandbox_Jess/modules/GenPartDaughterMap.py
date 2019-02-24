#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

class GenPartDaughterMap(Module):
  def __init__(self, isMC):
    # print 'Running GenPartDautherMap module'
    self.isMC = isMC
    pass
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    
  def beginJob(self,histFile=None,histDirName=None):    
    Module.beginJob(self,histFile,histDirName)

  def analyze(self, event):
    genparts = list(Collection(event, "GenPart"))

    genPartDaughters = {}
    for i in range(event.nGenPart):
      genPartDaughters[i] = []
    for Idx,part in enumerate(genparts):
      if part.genPartIdxMother>= 0:
        genPartDaughters[part.genPartIdxMother].append([Idx,part])

    event.genPartDaughters = genPartDaughters
    return True



