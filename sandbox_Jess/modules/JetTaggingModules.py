#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
#from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

import SF_Eff_cfg as cfg

class JetTaggingModules:
  def __init__(self, isMC, btagOP, bTagCut):
    # 'Running singleLepEventSelector module'
    self.isMC = isMC
    self.btagOP = btagOP
    self.bTagCut = bTagCut
    if self.btagOP in cfg._defn_heavyEff.keys():
      _Dict_heavyEff = cfg._defn_heavyEff[self.btagOP]
    else:
      _Dict_heavyEff = cfg._defn_heavyEff["default"] 
    if self.btagOP in cfg._defn_lightEff.keys():
      _Dict_lightEff = cfg._defn_lightEff[self.btagOP]
    else:
      _Dict_lightEff = cfg._defn_lightEff["default"]
    self._Dict_heavyEff = _Dict_heavyEff
    self._Dict_lightEff = _Dict_lightEff
    pass

  def GetEfficiency(self, pt):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    _heavyEff = 1.0
    _lightEff = 1.0
    for key in self._Dict_heavyEff.keys():
      if eval(key):
        _heavyEff = self._Dict_heavyEff[key]
        break
    for key in self._Dict_lightEff.keys():
      if eval(key):
        _lightEff = self._Dict_lightEff[key]
        break
    return _heavyEff, _lightEff

  def isJetTagged(self, pt, phi, btagDeepB, hadronFlavour, Index, SFandUncert):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    _isTagged = 0
    if btagDeepB > self.bTagCut[self.btagOP]:
      _isTagged = 1

    theJetBTag = _isTagged
    theJetBTag_bSFup = _isTagged
    theJetBTag_bSFdn = _isTagged
    theJetBTag_lSFup = _isTagged
    theJetBTag_lSFdn = _isTagged

    if self.isMC:
      _jetFlavor = abs(hadronFlavour)
      _heavySf = 1.0
      _heavySf_up = 1.0
      _heavySf_down = 1.0
      _heavyEff = 1.0
      _lightSf = 1.0
      _lightSf_up = 1.0
      _lightSf_down = 1.0
      _lightEff = 1.0
      mNBtagSfCorrJets = 0

      if len(SFandUncert) > 0 : 
        _heavySf = SFandUncert["heavySf_central"][Index]
        _heavySf_up = SFandUncert["heavySf_central"][Index]
        _heavySf_down = SFandUncert["heavySf_central"][Index]
        _lightSf = SFandUncert["heavySf_central"][Index]
        _lightSf_up = SFandUncert["heavySf_central"][Index]
        _lightSf_down = SFandUncert["heavySf_central"][Index]

      _heavyEff, _lightEff = self.GetEfficiency(pt)

      rand_ = ROOT.TRandom3()
      rand_.SetSeed(abs(int(math.sin(phi)*1e5)))
      coin = rand_.Uniform(1.)

      if abs( _jetFlavor ) == 5 or  abs( _jetFlavor ) == 4:
        if _heavySf>1 and _isTagged==0 and ((1.0-_heavySf)/(1.0-(_heavySf/_heavyEff))) > coin:
          theJetBTag = 1
          mNBtagSfCorrJets += 1
        elif _heavySf<1 and _isTagged==1 and coin>_heavySf:
          theJetBTag = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag = _isTagged          
        if _heavySf_up>1 and _isTagged==0 and ((1.0-_heavySf_up)/(1.0-(_heavySf_up/_heavyEff))) > coin:
          theJetBTag_bSFup = 1
          mNBtagSfCorrJets += 1
        elif _heavySf_up<1 and _isTagged==1 and coin>_heavySf_up:
          theJetBTag_bSFup = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_bSFup = _isTagged    
        if _heavySf_down>1 and _isTagged==0 and ((1.0-_heavySf_down)/(1.0-(_heavySf_down/_heavyEff))) > coin:
          theJetBTag_bSFdn = 1
          mNBtagSfCorrJets += 1
        elif _heavySf_down<1 and _isTagged==1 and coin>_heavySf_down:
          theJetBTag_bSFdn = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_bSFdn = _isTagged      
        if _heavySf>1 and _isTagged==0 and ((1.0-_heavySf)/(1.0-(_heavySf/_heavyEff))) > coin:
          theJetBTag_lSFup = 1
          mNBtagSfCorrJets += 1
        elif _heavySf<1 and _isTagged==1 and coin>_heavySf:
          theJetBTag_lSFup = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_lSFup = _isTagged    
        if _heavySf>1 and _isTagged==0 and ((1.0-_heavySf)/(1.0-(_heavySf/_heavyEff))) > coin:
          theJetBTag_lSFdn = 1
          mNBtagSfCorrJets += 1
        elif _heavySf<1 and _isTagged==1 and coin>_heavySf:
          theJetBTag_lSFdn = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_lSFdn = _isTagged
      else:
        if _lightSf>1 and _isTagged==0 and ((1.0-_lightSf)/(1.0-(_lightSf/_lightEff))) > coin :
          theJetBTag = 1
          mNBtagSfCorrJets += 1
        elif _lightSf<1 and _isTagged==1 and coin>_lightSf :
          theJetBTag = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag = _isTagged
        if _lightSf>1 and _isTagged==0 and ((1.0-_lightSf)/(1.0-(_lightSf/_lightEff))) > coin :
          theJetBTag_bSFup = 1
          mNBtagSfCorrJets += 1
        elif _lightSf<1 and _isTagged==1 and coin>_lightSf :
          theJetBTag_bSFup = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_bSFup = _isTagged
        if _lightSf>1 and _isTagged==0 and ((1.0-_lightSf)/(1.0-(_lightSf/_lightEff))) > coin :
          theJetBTag_bSFdn = 1
          mNBtagSfCorrJets += 1
        elif _lightSf<1 and _isTagged==1 and coin>_lightSf :
          theJetBTag_bSFdn = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_bSFdn = _isTagged
        if _lightSf_up>1 and _isTagged==0 and ((1.0-_lightSf_up)/(1.0-(_lightSf_up/_lightEff))) > coin :
          theJetBTag_lSFup = 1
          mNBtagSfCorrJets += 1
        elif _lightSf_up<1 and _isTagged==1 and coin>_lightSf_up :
          theJetBTag_lSFup = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_lSFup = _isTagged
        if _lightSf_down>1 and _isTagged==0 and ((1.0-_lightSf_down)/(1.0-(_lightSf_down/_lightEff))) > coin :
          theJetBTag_lSFdn = 1
          mNBtagSfCorrJets += 1
        elif _lightSf_down<1 and _isTagged==1 and coin>_lightSf_down :
          theJetBTag_lSFdn = 0
          mNBtagSfCorrJets += 1
        else:
          theJetBTag_lSFdn = _isTagged

    return theJetBTag, theJetBTag_bSFup, theJetBTag_bSFdn, theJetBTag_lSFup, theJetBTag_lSFdn 

