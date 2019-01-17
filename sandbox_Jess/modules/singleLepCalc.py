#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math


class singleLepCalc(Module):
  def __init__(self, isMC, trig, cleangenjets, keepPDGID, keepMomPDGID, keepPDGIDForce, keepStatusForce):
    # print 'Running singleLepCalc module'
    self.isMC = isMC
    self.triggers = trig
    self.CleanGenJets = cleangenjets
    self.keepPDGID = keepPDGID
    self.keepMomPDGID = keepMomPDGID
    self.keepPDGIDForce = keepPDGIDForce
    self.keepStatusForce = keepStatusForce
    pass

  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch("nPV_singleLepCalc",  "I")
    self.out.branch("nTrueInteractions_singleLepCalc",  "F")
    self.out.branch("MCWeight_singleLepCalc",  "F")
    self.out.branch("corr_met_singleLepCalc",  "F")
    self.out.branch("corr_met_phi_singleLepCalc",  "F")
    self.out.branch("HTfromHEPUEP_singleLepCalc", "F")
    self.out.branch("LHEweights_singleLepCalc", "F", lenVar="nLHEPdfWeight")
    self.out.branch("LHEweightids_singleLepCalc", "I", lenVar="nLHEPdfWeight")
    self.out.branch("isTau_singleLepCalc", "B")

    # self.out.branch("vsSelMCTriggersMu_singleLepCalc", "B")
    # self.out.branch("viSelMCTriggersMu_singleLepCalc", "I")
    # self.out.branch("vsSelMCTriggersEl_singleLepCalc", "B")
    # self.out.branch("viSelMCTriggersEl_singleLepCalc", "I")
    # self.out.branch("vsSelTriggersMu_singleLepCalc", "B")
    # self.out.branch("viSelTriggersMu_singleLepCalc", "I")
    # self.out.branch("vsSelTriggersEl_singleLepCalc", "B")
    # self.out.branch("viSelTriggersEl_singleLepCalc", "I")

    self.out.branch("muPt_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muEta_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muPhi_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muEnergy_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muMiniIso_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muRelIso_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muDxy_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muDz_singleLepCalc", "F", lenVar="nSelmu")
    self.out.branch("muCharge_singleLepCalc", "I", lenVar="nSelmu")

    self.out.branch("elPt_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elEta_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elPFEta_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elPhi_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elEnergy_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elMVAValue_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elMiniIso_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elRelIso_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elDxy_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elDz_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elCharge_singleLepCalc", "I", lenVar="nSelel")
    self.out.branch("elDEtaSCTkAtVtx_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elDR03TkSumPt_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elSihih_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elHoE_singleLepCalc", "F", lenVar="nSelel")
    self.out.branch("elisTightIso_singleLepCalc", "B", lenVar="nSelel")
    self.out.branch("elisLooseIso_singleLepCalc", "B", lenVar="nSelel")
    self.out.branch("elisTight_singleLepCalc", "B", lenVar="nSelel")
    self.out.branch("elisLoose_singleLepCalc", "B", lenVar="nSelel")

    self.out.branch("genPt_singleLepCalc", "F", lenVar="nGenPart")
    self.out.branch("genEta_singleLepCalc", "F", lenVar="nGenPart")
    self.out.branch("genPhi_singleLepCalc", "F", lenVar="nGenPart")
    self.out.branch("genEnergy_singleLepCalc", "F", lenVar="nGenPart")
    self.out.branch("genStatus_singleLepCalc", "I", lenVar="nGenPart")
    self.out.branch("genID_singleLepCalc", "I", lenVar="nGenPart")
    self.out.branch("genMotherID_singleLepCalc", "I", lenVar="nGenPart")
    self.out.branch("genJetPt_singleLepCalc", "F", lenVar="nGenJet")
    self.out.branch("genJetEta_singleLepCalc", "F", lenVar="nGenJet")
    self.out.branch("genJetPhi_singleLepCalc", "F", lenVar="nGenJet")
    self.out.branch("genJetEnergy_singleLepCalc", "F", lenVar="nGenJet")


  def beginJob(self,histFile=None,histDirName=None):    
    Module.beginJob(self,histFile,histDirName)

  def analyze(self, event):
    """process event, return True (go to next module) or False (fail, go to next event)"""
    Sel_electrons = event.Selel
    Sel_muons = event.Selmu
    genparts = list(Collection(event, "GenPart"))
    genjets = list(Collection(event, "GenJet"))
    taus = list(Collection(event, "Tau"))
    vGenLep = []
    
    self.out.fillBranch("nPV_singleLepCalc",event.PV_npvsGood) 
    self.out.fillBranch("nTrueInteractions_singleLepCalc",event.Pileup_nTrueInt)
    self.out.fillBranch("MCWeight_singleLepCalc",event.Generator_weight)
    self.out.fillBranch("corr_met_singleLepCalc",event.MET_pt) 
    self.out.fillBranch("corr_met_phi_singleLepCalc",event.MET_phi) 
    self.out.fillBranch("HTfromHEPUEP_singleLepCalc", event.LHE_HT)
    self.out.fillBranch("LHEweights_singleLepCalc", event.LHEPdfWeight)
    LHEweightids = []
    LHEweightids = [i+91400 for i in range(event.nLHEPdfWeight)]
    self.out.fillBranch("LHEweightids_singleLepCalc", LHEweightids)

    isTau = 0
    for tau in taus:
      if not tau.idDecayModeNewDMs:
        continue
      if tau.pt > 20. and math.fabs(tau.eta) < 2.4:
        isTau = 1
    self.out.fillBranch("isTau_singleLepCalc", isTau)

    # vsSelMCTriggersEl = []
    # viSelMCTriggersEl = []
    # vsSelTriggersEl = []
    # viSelTriggersEl = []
    # vsSelMCTriggersMu = []
    # viSelMCTriggersMu = []
    # vsSelTriggersMu = []
    # viSelTriggersMu = []
    # for trig in self.triggers:
    #   if self.isMC:      
    #     if "Mu" in trig or "mu" in trig:
    #       vsSelMCTriggersMu.append(trig)
    #       viSelMCTriggersMu.append(eval("event."+trig))
    #     elif "Ele" in trig or "ele" in trig:
    #       vsSelMCTriggersEl.append(trig)
    #       viSelMCTriggersEl.append(eval("event."+trig))
    #   else:
    #     if "Mu" in trig or "mu" in trig:
    #       vsSelTriggersMu.append(trig)
    #       viSelTriggersMu.append(eval("event."+trig))
    #     elif "Ele" in trig or "ele" in trig:
    #       vsSelTriggersEl.append(trig)
    #       viSelTriggersEl.append(eval("event."+trig))

    # #fill branches
    # self.out.fillBranch("vsSelMCTriggersMu_singleLepCalc",vsSelMCTriggersMu)
    # self.out.fillBranch("viSelMCTriggersMu_singleLepCalc",viSelMCTriggersMu)
    # self.out.fillBranch("vsSelMCTriggersEl_singleLepCalc",vsSelMCTriggersEl)
    # self.out.fillBranch("viSelMCTriggersEl_singleLepCalc",viSelMCTriggersEl)
    # self.out.fillBranch("vsSelTriggersMu_singleLepCalc",vsSelTriggersMu)
    # self.out.fillBranch("viSelTriggersMu_singleLepCalc",viSelTriggersMu)
    # self.out.fillBranch("vsSelTriggersEl_singleLepCalc",vsSelTriggersEl)
    # self.out.fillBranch("viSelTriggersEl_singleLepCalc",viSelTriggersEl)

    mu_Pt = []
    mu_Eta = []
    mu_Phi = []
    mu_Energy = []
    mu_MiniIso = []
    mu_RelIso = []
    mu_Dxy = []
    mu_Dz = []
    mu_Charge = []

    for mu in Sel_muons:
      mu_p4 = mu.p4()
      mu_Pt.append(mu.pt)
      mu_Eta.append(mu.eta)
      mu_Phi.append(mu.phi)
      mu_Energy.append(mu_p4.E())
      mu_MiniIso.append(mu.miniPFRelIso_all)
      mu_RelIso.append(mu.pfRelIso03_all)
      mu_Dxy.append(mu.dxy)
      mu_Dz.append(mu.dz)
      mu_Charge.append(mu.charge)
      if mu.genPartIdx>=0 and self.isMC:
        genMu=genparts.__getitem__(mu.genPartIdx)
        vGenLep.append(genMu.p4())

    #fill branches
    self.out.fillBranch("muPt_singleLepCalc",mu_Pt) 
    self.out.fillBranch("muEta_singleLepCalc",mu_Eta) 
    self.out.fillBranch("muPhi_singleLepCalc",mu_Phi) 
    self.out.fillBranch("muEnergy_singleLepCalc",mu_Energy) 
    self.out.fillBranch("muMiniIso_singleLepCalc",mu_MiniIso) 
    self.out.fillBranch("muRelIso_singleLepCalc",mu_RelIso) 
    self.out.fillBranch("muDxy_singleLepCalc",mu_Dxy) 
    self.out.fillBranch("muDz_singleLepCalc",mu_Dz) 
    self.out.fillBranch("muCharge_singleLepCalc",mu_Charge) 

    el_Pt = []
    el_Eta = []
    el_PFEta = []
    el_Phi = []
    el_Energy = []
    el_MVAValue = []
    el_MiniIso = []
    el_RelIso = []
    el_Dxy = []
    el_Dz = []
    el_Charge = []
    el_DEtaSCTkAtVtx = []
    el_DR03TkSumPt = []
    el_Sihih = []
    el_HoE = []
    el_isTightIso = []
    el_isLooseIso = []
    el_isTight = []
    el_isLoose = []

    for el in Sel_electrons:
      el_p4 = el.p4()
      el_Pt.append(el.pt)
      el_Eta.append(el.eta+el.deltaEtaSC)
      el_PFEta.append(el.eta)
      el_Phi.append(el.phi)
      el_Energy.append(el_p4.E())
      el_MVAValue.append(el.mvaFall17noIso)
      el_MiniIso.append(el.miniPFRelIso_all)
      el_RelIso.append(el.pfRelIso03_all)
      el_Dxy.append(el.dxy)
      el_Dz.append(el.dz)
      el_Charge.append(el.charge)
      el_DEtaSCTkAtVtx.append(el.deltaEtaSC)
      el_DR03TkSumPt.append(el.dr03TkSumPt)
      el_Sihih.append(el.sieie)
      el_HoE.append(el.hoe)
      el_isTightIso.append(el.mvaFall17Iso_WP90)
      el_isLooseIso.append(el.mvaFall17Iso_WPL)
      el_isTight.append(el.mvaFall17noIso_WP90)
      el_isLoose.append(el.mvaFall17noIso_WPL)
      if el.genPartIdx>=0 and self.isMC:
        genEl=genparts.__getitem__(el.genPartIdx)
        vGenLep.append(genEl.p4())

    #fill branches
    self.out.fillBranch("elPt_singleLepCalc", el_Pt)
    self.out.fillBranch("elEta_singleLepCalc", el_Eta)
    self.out.fillBranch("elPFEta_singleLepCalc", el_PFEta)
    self.out.fillBranch("elPhi_singleLepCalc", el_Phi)
    self.out.fillBranch("elEnergy_singleLepCalc", el_Energy)
    self.out.fillBranch("elMVAValue_singleLepCalc", el_MVAValue)
    self.out.fillBranch("elMiniIso_singleLepCalc", el_MiniIso)
    self.out.fillBranch("elRelIso_singleLepCalc", el_RelIso)
    self.out.fillBranch("elDxy_singleLepCalc", el_Dxy)
    self.out.fillBranch("elDz_singleLepCalc", el_Dz)
    self.out.fillBranch("elCharge_singleLepCalc", el_Charge)
    self.out.fillBranch("elDEtaSCTkAtVtx_singleLepCalc", el_DEtaSCTkAtVtx)
    self.out.fillBranch("elDR03TkSumPt_singleLepCalc", el_DR03TkSumPt)
    self.out.fillBranch("elSihih_singleLepCalc", el_Sihih)
    self.out.fillBranch("elHoE_singleLepCalc", el_HoE)
    self.out.fillBranch("elisTightIso_singleLepCalc", el_isTightIso)
    self.out.fillBranch("elisLooseIso_singleLepCalc", el_isLooseIso)
    self.out.fillBranch("elisTight_singleLepCalc", el_isTight)
    self.out.fillBranch("elisLoose_singleLepCalc", el_isLoose)

    gen_Pt = []
    gen_Eta = []
    gen_Phi = []
    gen_Energy = []
    gen_Status = []
    gen_ID = []
    gen_MotherID = []

    for part in genparts:
      part_p4 = part.p4()
      forceSave = False
      for ii in range(len(self.keepPDGIDForce)):
        if abs(part.pdgId) == self.keepPDGIDForce[ii] and part.status == self.keepStatusForce[ii]:
          forceSave = True
          break

      if abs(part.pdgId) == 23 :
        if part.genPartIdxMother < 0:
          continue
        bKeep = False
        if abs(event.GenPart_pdgId[part.genPartIdxMother]) in self.keepMomPDGID:
          bKeep = True
        elif abs(part.pdgId) in self.keepPDGID:
          bKeep = True     
        if not bKeep:
          continue
        gen_Pt.append(part.pt)
        gen_Eta.append(part.eta)
        gen_Phi.append(part.phi)
        gen_Energy.append(part_p4.E())
        gen_Status.append(part.status)
        gen_ID.append(part.pdgId)
        gen_MotherID.append(event.GenPart_pdgId[part.genPartIdxMother])
      elif forceSave :
        gen_Pt.append(part.pt)
        gen_Eta.append(part.eta)
        gen_Phi.append(part.phi)
        gen_Energy.append(part_p4.E())
        gen_Status.append(part.status)
        gen_ID.append(part.pdgId)
        gen_MotherID.append(0)

    self.out.fillBranch("genPt_singleLepCalc", gen_Pt)
    self.out.fillBranch("genEta_singleLepCalc", gen_Eta)
    self.out.fillBranch("genPhi_singleLepCalc", gen_Phi)
    self.out.fillBranch("genEnergy_singleLepCalc", gen_Energy)
    self.out.fillBranch("genStatus_singleLepCalc", gen_Status)
    self.out.fillBranch("genID_singleLepCalc", gen_ID)
    self.out.fillBranch("genMotherID_singleLepCalc", gen_MotherID)

    genjet_Pt = []
    genjet_Eta = []
    genjet_Phi = []
    genjet_Energy = []

    for jet in genjets:
      jet_p4 = jet.p4()
      if self.CleanGenJets:
        for lep in vGenLep:
          if lep.DeltaR(jet_p4) < 0.001 and ( abs(jet.partonFlavour)==13 or abs(jet.partonFlavour)==11) :
            jet_p4 = jet_p4-lep
    genjet_Pt.append(jet_p4.Pt())
    genjet_Eta.append(jet_p4.Eta())
    genjet_Phi.append(jet_p4.Phi())
    genjet_Energy.append(jet_p4.E())

    self.out.fillBranch("genJetPt_singleLepCalc", genjet_Pt)
    self.out.fillBranch("genJetEta_singleLepCalc", genjet_Eta)
    self.out.fillBranch("genJetPhi_singleLepCalc", genjet_Phi)
    self.out.fillBranch("genJetEnergy_singleLepCalc", genjet_Energy)

    event.vGenLep = vGenLep 

    return True



