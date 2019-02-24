#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math
from modules.JetTaggingModules import *

class JetSubCalc(Module):
  def __init__(self, isMC, btagOP, bTagCutValue, puppiCorrfilepath, FatJetSD_JMS_sd, FatJetSD_JMS_sd_up, FatJetSD_JMS_sd_dn):
    # print 'Running JetSubCalc module'
    self.isMC = isMC
    self.btagOP = btagOP
    self.bTagCut = bTagCutValue
    puppiCorrfile = ROOT.TFile.Open(puppiCorrfilepath)
    self.puppisd_corrGEN = puppiCorrfile.Get("puppiJECcorr_gen")
    self.puppisd_corrRECO_cen = puppiCorrfile.Get("puppiJECcorr_reco_0eta1v3")
    self.puppisd_corrRECO_for = puppiCorrfile.Get("puppiJECcorr_reco_1v3eta2v5")
    self.FatJetSD_JMS_sd = FatJetSD_JMS_sd
    self.FatJetSD_JMS_sd_up = FatJetSD_JMS_sd_up
    self.FatJetSD_JMS_sd_dn = FatJetSD_JMS_sd_dn
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree

    self.out.branch("theJetHFlav_JetSubCalc", "F", lenVar="nSeljet")
    self.out.branch("theJetPFlav_JetSubCalc", "F", lenVar="nSeljet")
    self.out.branch("theJetPt_JetSubCalc", "F", lenVar="nSeljet")
    self.out.branch("theJetEta_JetSubCalc", "F", lenVar="nSeljet")
    self.out.branch("theJetPhi_JetSubCalc", "F", lenVar="nSeljet")
    self.out.branch("theJetEnergy_JetSubCalc", "F", lenVar="nSeljet")
    self.out.branch("theJetCSV_JetSubCalc", "F", lenVar="nSeljet")
    self.out.branch("theJetBTag_JetSubCalc", "I", lenVar="nSeljet")
    self.out.branch("theJetBTag_bSFup_JetSubCalc", "I", lenVar="nSeljet")
    self.out.branch("theJetBTag_bSFdn_JetSubCalc", "I", lenVar="nSeljet")
    self.out.branch("theJetBTag_lSFup_JetSubCalc", "I", lenVar="nSeljet")
    self.out.branch("theJetBTag_lSFdn_JetSubCalc", "I", lenVar="nSeljet")
    self.out.branch("theJetHT_JetSubCalc", "F")
    # self.out.branch("theJetCSVb_JetSubCalc", "F", lenVar="nSeljet")
    # self.out.branch("theJetCSVbb_JetSubCalc", "F", lenVar="nSeljet")

    self.out.branch("theJetAK8Pt_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8Eta_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8Phi_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8Mass_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8Energy_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8DoubleB_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8NjettinessTau1_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8NjettinessTau2_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8NjettinessTau3_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDropMass_JetSubCalc", "F" , lenVar="nSeljetAK8")

    self.out.branch("theJetAK8SDSubjetPt_JetSubCalc", "F", lenVar="nSelsubjet")
    self.out.branch("theJetAK8SDSubjetEta_JetSubCalc", "F", lenVar="nSelsubjet")
    self.out.branch("theJetAK8SDSubjetPhi_JetSubCalc", "F", lenVar="nSelsubjet")
    self.out.branch("theJetAK8SDSubjetMass_JetSubCalc", "F", lenVar="nSelsubjet")
    self.out.branch("theJetAK8SDSubjetHFlav_JetSubCalc", "I", lenVar="nSelsubjet")
    self.out.branch("theJetAK8SDSubjetCSV_JetSubCalc", "F", lenVar="nSelsubjet")

    self.out.branch("theJetAK8SDSubjetIndex_JetSubCalc", "I", lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SDSubjetSize_JetSubCalc", "I", lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SDSubjetNDeepCSVM_bSFdn_JetSubCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SDSubjetNDeepCSVM_bSFup_JetSubCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SDSubjetNDeepCSVM_lSFdn_JetSubCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SDSubjetNDeepCSVM_lSFup_JetSubCalc", "F", lenVar="nSeljetAK8")

    self.out.branch("maxProb_JetSubCalc", "F", lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDropRaw_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDropCorr_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDrop_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDrop_JMSup_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDrop_JMSdn_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDrop_JMRup_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8SoftDrop_JMRdn_JetSubCalc", "F" , lenVar="nSeljetAK8")

    self.out.branch("theJetAK8CHSTau1_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8CHSTau2_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8CHSTau3_JetSubCalc", "F" , lenVar="nSeljetAK8")
    self.out.branch("theJetAK8CHSSoftDropMass_JetSubCalc", "F" , lenVar="nSeljetAK8")

    self.out.branch("HadronicVHtStatus_JetSubCalc", "I", lenVar="nGenPart")
    self.out.branch("HadronicVHtID_JetSubCalc", "I", lenVar="nGenPart")
    self.out.branch("HadronicVHtPt_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtDeltaR_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtEta_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtPhi_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtEnergy_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD0Pt_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD0Eta_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD0Phi_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD0E_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD1Pt_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD1Eta_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD1Phi_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD1E_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD2Pt_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD2Eta_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD2Phi_JetSubCalc", "F", lenVar="nGenPart")
    self.out.branch("HadronicVHtD2E_JetSubCalc", "F", lenVar="nGenPart")

  def beginJob(self,histFile=None,histDirName=None):    
    Module.beginJob(self,histFile,histDirName)

  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    Sel_jets = event.Seljet
    Sel_jetsP4 = event.SeljetP4
    Sel_jetAK8s = event.SeljetAK8
    Sel_jetAK8sP4 = event.SeljetAK8P4
    Sel_subjet = event.Selsubjet
    Sel_SubjetIndex = event.theJetAK8SDSubjetIndex
    Sel_SubjetSize = event.theJetAK8SDSubjetSize
    genparts = list(Collection(event, "GenPart"))

    try:
      event.SFandUncert
    except NameError:
      SFandUncert={}
    else:
      SFandUncert = event.SFandUncert
    try:
      event.subjet_SFandUncert
    except NameError:
      subjet_SFandUncert={}
    else:
      subjet_SFandUncert = event.subjet_SFandUncert

    ################# Initialize Tool for Tagging Uncertainties ####################
    JetTagging = JetTaggingModules(self.isMC, self.btagOP, self.bTagCut)

    ################# Jets ####################

    thejetHFlav = []
    thejetPFlav = []
    thejetPt = []
    thejetEta = []
    thejetPhi = []
    thejetEnergy = []
    thejetCSV = []
    thejetHT = 0
    theJetBTag = []
    theJetBTag_bSFup = []
    theJetBTag_bSFdn = []
    theJetBTag_lSFup = []
    theJetBTag_lSFdn = []

    for i,jet in enumerate(Sel_jets):
      thejetHFlav.append(jet.hadronFlavour)
      thejetPFlav.append(jet.partonFlavour)
      thejetPt.append(Sel_jetsP4[i].Pt())
      thejetEta.append(Sel_jetsP4[i].Eta())
      thejetPhi.append(Sel_jetsP4[i].Phi())
      thejetEnergy.append(Sel_jetsP4[i].E())
      thejetCSV.append(jet.btagDeepB) # CSVb+ CSVbb
      thejetHT += Sel_jetsP4[i].Pt()

      _isTagged, _isTagged_bSFup, _isTagged_bSFdn, _isTagged_lSFup, _isTagged_lSFdn = JetTaggingModules.isJetTagged(JetTagging,Sel_jetsP4[i].Pt(),Sel_jetsP4[i].Phi(), jet.btagDeepB, jet.hadronFlavour, i, SFandUncert)

      theJetBTag.append(_isTagged)
      theJetBTag_bSFup.append(_isTagged_bSFup)
      theJetBTag_bSFdn.append(_isTagged_bSFdn)
      theJetBTag_lSFup.append(_isTagged_lSFup)
      theJetBTag_lSFdn.append(_isTagged_lSFdn)

    #fill branches
    self.out.fillBranch("theJetHFlav_JetSubCalc", thejetHFlav)
    self.out.fillBranch("theJetPFlav_JetSubCalc", thejetPFlav)
    self.out.fillBranch("theJetPt_JetSubCalc", thejetPt)
    self.out.fillBranch("theJetEta_JetSubCalc", thejetEta)
    self.out.fillBranch("theJetPhi_JetSubCalc", thejetPhi)
    self.out.fillBranch("theJetEnergy_JetSubCalc", thejetEnergy)
    self.out.fillBranch("theJetCSV_JetSubCalc", thejetCSV)
    self.out.fillBranch("theJetHT_JetSubCalc",thejetHT)
    self.out.fillBranch("theJetBTag_JetSubCalc", theJetBTag)
    self.out.fillBranch("theJetBTag_bSFup_JetSubCalc", theJetBTag_bSFup)
    self.out.fillBranch("theJetBTag_bSFdn_JetSubCalc", theJetBTag_bSFdn)
    self.out.fillBranch("theJetBTag_lSFup_JetSubCalc", theJetBTag_lSFup)
    self.out.fillBranch("theJetBTag_lSFdn_JetSubCalc", theJetBTag_lSFdn)


    ################# JetAK8 and SubJets ####################

    theJetAK8Pt = []
    theJetAK8Eta = []
    theJetAK8Phi = []
    theJetAK8Mass = []
    theJetAK8Energy = []
    theJetAK8DoubleB = []
    theJetAK8NjettinessTau1 = []
    theJetAK8NjettinessTau2 = []
    theJetAK8NjettinessTau3 = []
    theJetAK8SoftDropMass = []

    theJetAK8SDSubjetPt = []
    theJetAK8SDSubjetEta = []
    theJetAK8SDSubjetPhi = []
    theJetAK8SDSubjetMass = []
    theJetAK8SDSubjetHFlav = []
    theJetAK8SDSubjetCSV = []
    theJetAK8SDSubjetIndex = []
    theJetAK8SDSubjetSize = []

    theJetAK8SDSubjetNDeepCSVMSF = []
    theJetAK8SDSubjetNDeepCSVM_bSFdn = []
    theJetAK8SDSubjetNDeepCSVM_bSFup = []
    theJetAK8SDSubjetNDeepCSVM_lSFdn = []
    theJetAK8SDSubjetNDeepCSVM_lSFup = []
    maxProb = []
    theJetAK8SoftDropRaw = []
    theJetAK8SoftDropCorr = []
    theJetAK8SoftDrop = []
    theJetAK8SoftDrop_JMSup = []
    theJetAK8SoftDrop_JMSdn = []
    theJetAK8SoftDrop_JMRup = []
    theJetAK8SoftDrop_JMRdn = []
    
    theJetAK8CHSTau1 = []
    theJetAK8CHSTau2 = []
    theJetAK8CHSTau3 = []
    theJetAK8CHSSoftDropMass = []

    for i,jetak8 in enumerate(Sel_jetAK8s):
      theJetAK8Pt.append(Sel_jetAK8sP4[i].Pt())
      theJetAK8Eta.append(Sel_jetAK8sP4[i].Eta())
      theJetAK8Phi.append(Sel_jetAK8sP4[i].Phi())
      theJetAK8Mass.append(Sel_jetAK8sP4[i].M())
      theJetAK8Energy.append(Sel_jetAK8sP4[i].E())
      theJetAK8DoubleB.append(jetak8.btagHbb)
      theJetAK8NjettinessTau1.append(jetak8.tau1)
      theJetAK8NjettinessTau2.append(jetak8.tau2)
      theJetAK8NjettinessTau3.append(jetak8.tau3)
      theJetAK8SoftDropMass.append(jetak8.msoftdrop)

      SDSubJetIndex = Sel_SubjetIndex[i]
      SDSubjetSize = Sel_SubjetSize[i]
      nSDSubsDeepCSVMSF = 0
      nSDSubsDeepCSVM_bSFup = 0
      nSDSubsDeepCSVM_bSFdn = 0
      nSDSubsDeepCSVM_lSFup = 0
      nSDSubsDeepCSVM_lSFdn = 0
      if Sel_SubjetSize > 0 :
        for isubjet in range(SDSubJetIndex, SDSubJetIndex+SDSubjetSize):
          subjet = Sel_subjet[isubjet]
          theJetAK8SDSubjetPt.append(subjet.pt)
          theJetAK8SDSubjetEta.append(subjet.eta)
          theJetAK8SDSubjetPhi.append(subjet.phi)
          theJetAK8SDSubjetMass.append(subjet.mass)
          theJetAK8SDSubjetHFlav.append(0)
          theJetAK8SDSubjetCSV.append(subjet.btagDeepB)
          _isTagged, _isTagged_bSFup, _isTagged_bSFdn, _isTagged_lSFup, _isTagged_lSFdn = JetTaggingModules.isJetTagged(JetTagging,subjet.pt,subjet.phi, subjet.btagDeepB, theJetAK8SDSubjetHFlav[isubjet] , isubjet, subjet_SFandUncert) # subjet.hadronFlavour missing, replaced by 0
          if _isTagged :
            nSDSubsDeepCSVMSF +=1
          if _isTagged_bSFup:
            nSDSubsDeepCSVM_bSFup +=1
          if _isTagged_bSFdn:
            nSDSubsDeepCSVM_bSFdn +=1
          if _isTagged_lSFup:
            nSDSubsDeepCSVM_lSFup +=1
          if _isTagged_lSFdn:
            nSDSubsDeepCSVM_lSFdn +=1

      theJetAK8SDSubjetNDeepCSVMSF.append(nSDSubsDeepCSVMSF)
      theJetAK8SDSubjetNDeepCSVM_bSFdn.append(nSDSubsDeepCSVM_bSFdn)
      theJetAK8SDSubjetNDeepCSVM_bSFup.append(nSDSubsDeepCSVM_bSFup)
      theJetAK8SDSubjetNDeepCSVM_lSFdn.append(nSDSubsDeepCSVM_lSFdn)
      theJetAK8SDSubjetNDeepCSVM_lSFup.append(nSDSubsDeepCSVM_lSFup)

      puppicorr = 1.
      genCorr = 1.
      recoCorr = 1.
      try:
        JetAK8.__getattr__("rawFactor")
      except:
        rawfactor = 0.
      else:
        print 'rawfactor EXISTS!'
        rawfactor = jetak8.rawFactor
      genCorr = self.puppisd_corrGEN.Eval((1-rawfactor)*jetak8.pt)
      if math.fabs(jetak8.eta) <= 1.3 :
        recoCorr = self.puppisd_corrRECO_cen.Eval((1-rawfactor)*jetak8.pt)
      else:
        recoCorr = self.puppisd_corrRECO_for.Eval((1-rawfactor)*jetak8.pt)
      puppicorr = genCorr * recoCorr
      theSoftDropCorrected = jetak8.msoftdrop*puppicorr
      jmr_sd = 1.0
      jmr_sd_up = 1.0
      jmr_sd_dn = 1.0
      jms_sd = 1.0
      jms_sd_up = 1.0
      jms_sd_dn = 1.0
      if self.isMC and not (theSoftDropCorrected ==0):
        res = 8.753/theSoftDropCorrected
        factor_sd = 1.09
        uncert_sd = 0.05
        factor_sd_up = factor_sd + uncert_sd
        factor_sd_dn = factor_sd - uncert_sd
        JERrand = ROOT.TRandom3()
        JERrand.SetSeed(abs(int(jetak8.phi*10000)))  
        if factor_sd>1:
          jmr_sd = 1 + JERrand.Gaus(0,res)*math.sqrt(factor_sd*factor_sd - 1.0)
        if factor_sd_up>1:
          jmr_sd_up = 1 + JERrand.Gaus(0,res)*math.sqrt(factor_sd_up*factor_sd_up - 1.0)
        if factor_sd_dn>1:
          jmr_sd_dn = 1 + JERrand.Gaus(0,res)*math.sqrt(factor_sd_dn*factor_sd_dn - 1.0)

      MaxProb = 10
      if (theSoftDropCorrected > 135 and theSoftDropCorrected < 210 and jetak8.tau3/jetak8.tau2 < 0.65) : 
        MaxProb = 1 # top
      elif (theSoftDropCorrected > 105 and theSoftDropCorrected < 135 and jetak8.btagHbb > 0.6) : 
        MaxProb = 2 # H
      elif (theSoftDropCorrected < 105 and theSoftDropCorrected > 85 and jetak8.tau2/jetak8.tau1 < 0.55) : 
        MaxProb = 3 # Z
      elif (theSoftDropCorrected < 85 and theSoftDropCorrected > 65 and jetak8.tau2/jetak8.tau1 < 0.55) : 
        MaxProb = 4 # W
      elif (nSDSubsDeepCSVMSF > 0) : 
        MaxProb = 5
      elif (nSDSubsDeepCSVMSF == 0) : 
        MaxProb = 0
      else:
        MaxProb = 10
      maxProb.append(MaxProb)

      theJetAK8SoftDropRaw.append(jetak8.msoftdrop)
      theJetAK8SoftDropCorr.append(theSoftDropCorrected)
      theJetAK8SoftDrop.append(theSoftDropCorrected*jmr_sd*self.FatJetSD_JMS_sd)
      theJetAK8SoftDrop_JMSup.append(theSoftDropCorrected*jmr_sd*self.FatJetSD_JMS_sd_up)
      theJetAK8SoftDrop_JMSdn.append(theSoftDropCorrected*jmr_sd*self.FatJetSD_JMS_sd_dn)
      theJetAK8SoftDrop_JMRup.append(theSoftDropCorrected*jmr_sd_up*self.FatJetSD_JMS_sd)
      theJetAK8SoftDrop_JMRdn.append(theSoftDropCorrected*jmr_sd_dn*self.FatJetSD_JMS_sd)

      theJetAK8CHSTau1.append(0.)
      theJetAK8CHSTau2.append(0.)
      theJetAK8CHSTau3.append(0.)
      theJetAK8CHSSoftDropMass.append(0.)

    #fill branches
    self.out.fillBranch("theJetAK8Pt_JetSubCalc", theJetAK8Pt) 
    self.out.fillBranch("theJetAK8Eta_JetSubCalc", theJetAK8Eta) 
    self.out.fillBranch("theJetAK8Phi_JetSubCalc", theJetAK8Phi) 
    self.out.fillBranch("theJetAK8Mass_JetSubCalc", theJetAK8Mass) 
    self.out.fillBranch("theJetAK8Energy_JetSubCalc", theJetAK8Energy) 
    self.out.fillBranch("theJetAK8DoubleB_JetSubCalc", theJetAK8DoubleB) 
    self.out.fillBranch("theJetAK8NjettinessTau1_JetSubCalc", theJetAK8NjettinessTau1) 
    self.out.fillBranch("theJetAK8NjettinessTau2_JetSubCalc", theJetAK8NjettinessTau2) 
    self.out.fillBranch("theJetAK8NjettinessTau3_JetSubCalc", theJetAK8NjettinessTau3) 
    self.out.fillBranch("theJetAK8SoftDropMass_JetSubCalc", theJetAK8SoftDropMass) 

    self.out.fillBranch("theJetAK8SDSubjetPt_JetSubCalc", theJetAK8SDSubjetPt)
    self.out.fillBranch("theJetAK8SDSubjetEta_JetSubCalc", theJetAK8SDSubjetEta)
    self.out.fillBranch("theJetAK8SDSubjetPhi_JetSubCalc", theJetAK8SDSubjetPhi)
    self.out.fillBranch("theJetAK8SDSubjetMass_JetSubCalc", theJetAK8SDSubjetMass)
    self.out.fillBranch("theJetAK8SDSubjetHFlav_JetSubCalc", theJetAK8SDSubjetHFlav)
    self.out.fillBranch("theJetAK8SDSubjetCSV_JetSubCalc", theJetAK8SDSubjetCSV)
    self.out.fillBranch("theJetAK8SDSubjetIndex_JetSubCalc", theJetAK8SDSubjetIndex)
    self.out.fillBranch("theJetAK8SDSubjetSize_JetSubCalc", theJetAK8SDSubjetSize)

    self.out.fillBranch("theJetAK8SDSubjetNDeepCSVMSF_JetSubCalc", theJetAK8SDSubjetNDeepCSVMSF)
    self.out.fillBranch("theJetAK8SDSubjetNDeepCSVM_bSFdn_JetSubCalc", theJetAK8SDSubjetNDeepCSVM_bSFdn)
    self.out.fillBranch("theJetAK8SDSubjetNDeepCSVM_bSFup_JetSubCalc", theJetAK8SDSubjetNDeepCSVM_bSFup)
    self.out.fillBranch("theJetAK8SDSubjetNDeepCSVM_lSFdn_JetSubCalc", theJetAK8SDSubjetNDeepCSVM_lSFdn)
    self.out.fillBranch("theJetAK8SDSubjetNDeepCSVM_lSFup_JetSubCalc", theJetAK8SDSubjetNDeepCSVM_lSFup)
    self.out.fillBranch("maxProb_JetSubCalc", maxProb)
    self.out.fillBranch("theJetAK8SoftDropRaw_JetSubCalc", theJetAK8SoftDropRaw)
    self.out.fillBranch("theJetAK8SoftDropCorr_JetSubCalc", theJetAK8SoftDropCorr)
    self.out.fillBranch("theJetAK8SoftDrop_JetSubCalc", theJetAK8SoftDrop)
    self.out.fillBranch("theJetAK8SoftDrop_JMSup_JetSubCalc", theJetAK8SoftDrop_JMSup)
    self.out.fillBranch("theJetAK8SoftDrop_JMSdn_JetSubCalc", theJetAK8SoftDrop_JMSdn)
    self.out.fillBranch("theJetAK8SoftDrop_JMRup_JetSubCalc", theJetAK8SoftDrop_JMRup)
    self.out.fillBranch("theJetAK8SoftDrop_JMRdn_JetSubCalc", theJetAK8SoftDrop_JMRdn)

    self.out.fillBranch("theJetAK8CHSTau1_JetSubCalc", theJetAK8CHSTau1)
    self.out.fillBranch("theJetAK8CHSTau2_JetSubCalc", theJetAK8CHSTau2)
    self.out.fillBranch("theJetAK8CHSTau3_JetSubCalc", theJetAK8CHSTau3)
    self.out.fillBranch("theJetAK8CHSSoftDropMass_JetSubCalc", theJetAK8CHSSoftDropMass)

    ################# TRUE HADRONIC W/Z/H/Top decays ####################
    HadronicVHtStatus =[]
    HadronicVHtID =[]
    HadronicVHtPt =[]
    HadronicVHtDeltaR =[]
    HadronicVHtEta =[]
    HadronicVHtPhi =[]
    HadronicVHtEnergy =[]
    HadronicVHtD0Pt =[]
    HadronicVHtD0Eta =[]
    HadronicVHtD0Phi =[]
    HadronicVHtD0E =[]
    HadronicVHtD1Pt =[]
    HadronicVHtD1Eta =[]
    HadronicVHtD1Phi =[]
    HadronicVHtD1E =[]
    HadronicVHtD2Pt =[]
    HadronicVHtD2Eta =[]
    HadronicVHtD2Phi =[]
    HadronicVHtD2E =[]

    for Idx,part in enumerate(genparts):
      if not self.isMC:
        break
      Id = part.pdgId
      partp4=part.p4()
      hasRadiation = False
      hasLepton = False
      if abs(Id) == 23 or abs(Id) == 24 or abs(Id) == 25 or abs(Id) == 6 : 
        if part.mass == 0:
          continue
        daughters = []
        daughters = event.genPartDaughters[Idx]
        for dauIdx,dau in daughters:
          if abs(dau.pdgId) == abs(Id):
            hasRadiation = True
          elif abs(dau.pdgId) == 24 or abs(dau.pdgId) ==23:
            ddaughters = []
            ddaughters = event.genPartDaughters[dauIdx]
            while len(ddaughters) == 1:
              i,d = ddaughters[0]
              ddaughters
              ddaughters = event.genPartDaughters[i]
            if len(ddaughters)<2:
              print 'JetSubCalc: W/Z hadronic decay -- less than 2 daughters'
            else:
              count = 0
              for i,d in ddaughters:
                if count>=2:
                  break
                if d.pdgId>10 and d.pdgId<17:
                  hasLepton = True
                count+=1
          elif abs(dau.pdgId)>10 and abs(dau.pdgId)<17:
            hasLepton = True
        if hasRadiation or hasLepton or part.pt<175.:
          continue
        mIdx = part.genPartIdxMother
        mother = genparts.__getitem__(mIdx)
        dr = 1000
        if abs(Id) == 24:
          dRWb = 1000
          dRWW = 1000
          count = 0
          while abs(mother.pdgId) == 24 and count<100:
            mIdx = mother.genPartIdxMother
            mother = genparts.__getitem__(mIdx)
            count +=1
          mdaughters = []
          mdaughters = event.genPartDaughters[mIdx]
          if len(mdaughters) < 2:
            print 'JetSubCalc: W/Z hadronic decay -- mother w/ less than 2 daughters'
          i2,d2 = mdaughters[1]
          i1,d1 = mdaughters[0]
          if abs(mother.pdgId) == 6:
            dr = partp4.DeltaR(d2.p4())
            if abs(d2.pdgId) == 24:
              dr = partp4.DeltaR(d1.p4())
            if dr<dRWb:
              dRWb = dr
          elif abs(mother.pdgId) == 25:
            dr = 1000
            if part.pdgId*d1.pdgId >0:
              dr = partp4.DeltaR(d2.p4())
            else:
              dr = partp4.DeltaR(d1.p4())
            if dr<dRWW:
              dRWW = dr
          if dRWW<0.8:
            print 'Hadronic decay part removed by dr'
            continue
          if dRWb<0.8:
            continue
        if abs(Id) == 23:
          dRZZ = 1000
          count = 0
          while abs(mother.pdgId) ==23 and count<100:
            mIdx = mother.genPartIdxMother
            mother = genparts.__getitem__(mIdx)
            count +=1
          mdaughters = []
          mdaughters = event.genPartDaughters[mIdx]
          i2,d2 = mdaughters[1]
          i1,d1 = mdaughters[0]
          if abs(mother.pdgId) == 25:
            dr = 1000
            if part.pdgId*d1.pdgId >0:
              dr = partp4.DeltaR(d2.p4())
            else:
              dr = partp4.DeltaR(d1.p4())
            if dr < dRZZ:
              dRZZ = dr
          if dRZZ < 0.8:
            continue
        if len(daughters) < 2:
          print str(len(daughters))+' daughters from '+str(part.pdgId)
          continue
        HadronicVHtStatus.append(part.status)
        HadronicVHtID.append(part.pdgId)
        HadronicVHtPt.append(part.pt)
        HadronicVHtDeltaR.append(dr)
        HadronicVHtEta.append(part.eta)
        HadronicVHtPhi.append(part.phi)
        
        HadronicVHtEnergy.append(partp4.E())

        if not abs(Id) == 6:
          if len(daughters)<2:
            print 'JetSubCalc: non t hadronic decay -- less than 2 daughters'
            continue
          i1,d1 = daughters[0]
          d1p4 = d1.p4()
          i2,d2 = daughters[1]
          d2p4 = d2.p4()
          HadronicVHtD0Pt.append(d1.pt)
          HadronicVHtD0Eta.append(d1.eta)
          HadronicVHtD0Phi.append(d1.phi)
          HadronicVHtD0E.append(d1p4.E())
          HadronicVHtD1Pt.append(d2.pt)
          HadronicVHtD1Eta.append(d2.eta)
          HadronicVHtD1Phi.append(d2.phi)
          HadronicVHtD1E.append(d2p4.E())
          HadronicVHtD2Pt.append(-99.9)
          HadronicVHtD2Eta.append(-99.9)
          HadronicVHtD2Phi.append(-99.9)
          HadronicVHtD2E.append(-99.9)
        else:
          if len(daughters)<2:
            print 'JetSubCalc: t hadronic decay -- less than 2 daughters'
            continue
          iW,W = daughters[0]
          ib,b = daughters[1]
          if not abs(W.pdgId) == 24:
            ib,b = daughters[0]
            iW,W = daughters[1]
          bp4 = b.p4()
          Wdaughters = []
          Wdaughters = event.genPartDaughters[iW]
          while len(Wdaughters) == 1 or (len(Wdaughters) >=2 and abs(Wdaughters[1][1].pdgId)==22):
            iW,W = Wdaughters[0]
            Wdaughters = []
            Wdaughters = event.genPartDaughters[iW]
          i1,d1 = daughters[0]
          d1p4 = d1.p4()
          i2,d2 = daughters[1]
          d2p4 = d2.p4()
          HadronicVHtD0Pt.append(b.pt)
          HadronicVHtD0Eta.append(b.eta)
          HadronicVHtD0Phi.append(b.phi)
          HadronicVHtD0E.append(bp4.E())
          HadronicVHtD1Pt.append(d1.pt)
          HadronicVHtD1Eta.append(d1.eta)
          HadronicVHtD1Phi.append(d1.phi)
          HadronicVHtD1E.append(d1p4.E())
          HadronicVHtD2Pt.append(d2.pt)
          HadronicVHtD2Eta.append(d2.eta)
          HadronicVHtD2Phi.append(d2.phi)
          HadronicVHtD2E.append(d2p4.E())
    self.out.fillBranch("HadronicVHtStatus_JetSubCalc", HadronicVHtStatus)
    self.out.fillBranch("HadronicVHtID_JetSubCalc", HadronicVHtID)
    self.out.fillBranch("HadronicVHtPt_JetSubCalc", HadronicVHtPt)
    self.out.fillBranch("HadronicVHtDeltaR_JetSubCalc", HadronicVHtDeltaR)
    self.out.fillBranch("HadronicVHtEta_JetSubCalc", HadronicVHtEta)
    self.out.fillBranch("HadronicVHtPhi_JetSubCalc", HadronicVHtPhi)
    self.out.fillBranch("HadronicVHtEnergy_JetSubCalc", HadronicVHtEnergy)
    self.out.fillBranch("HadronicVHtD0Pt_JetSubCalc", HadronicVHtD0Pt)
    self.out.fillBranch("HadronicVHtD0Eta_JetSubCalc", HadronicVHtD0Eta)
    self.out.fillBranch("HadronicVHtD0Phi_JetSubCalc", HadronicVHtD0Phi)
    self.out.fillBranch("HadronicVHtD0E_JetSubCalc", HadronicVHtD0E)
    self.out.fillBranch("HadronicVHtD1Pt_JetSubCalc", HadronicVHtD1Pt)
    self.out.fillBranch("HadronicVHtD1Eta_JetSubCalc", HadronicVHtD1Eta)
    self.out.fillBranch("HadronicVHtD1Phi_JetSubCalc", HadronicVHtD1Phi)
    self.out.fillBranch("HadronicVHtD1E_JetSubCalc", HadronicVHtD1E)
    self.out.fillBranch("HadronicVHtD2Pt_JetSubCalc", HadronicVHtD2Pt)
    self.out.fillBranch("HadronicVHtD2Eta_JetSubCalc", HadronicVHtD2Eta)
    self.out.fillBranch("HadronicVHtD2Phi_JetSubCalc", HadronicVHtD2Phi)
    self.out.fillBranch("HadronicVHtD2E_JetSubCalc", HadronicVHtD2E)

    return True



