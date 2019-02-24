#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import math

class TTbarMassCalc(Module):
  def __init__(self):
    # print 'Running TTbarMassCalc module'
    pass
  
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree
    self.out.branch("ttbarMass_TTbarMassCalc", "F")
    self.out.branch("topID_TTbarMassCalc", "I", lenVar="nGenPart")
    self.out.branch("topMotherID_TTbarMassCalc", "I", lenVar="nGenPart")
    self.out.branch("topPt_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topEta_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topPhi_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topEnergy_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topMass_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("top62ID_TTbarMassCalc", "I", lenVar="nGenPart")
    self.out.branch("top62MotherID_TTbarMassCalc", "I", lenVar="nGenPart")
    self.out.branch("top62Pt_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("top62Eta_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("top62Phi_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("top62Energy_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("top62Mass_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topbID_TTbarMassCalc", "I", lenVar="nGenPart")
    self.out.branch("topbPt_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topbEta_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topbPhi_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topbEnergy_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topWID_TTbarMassCalc", "I", lenVar="nGenPart")
    self.out.branch("topWPt_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topWEta_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topWPhi_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("topWEnergy_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("allTopsID_TTbarMassCalc", "I", lenVar="nGenPart")
    self.out.branch("allTopsStatus_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("allTopsEnergy_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("allTopsEta_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("allTopsPhi_TTbarMassCalc", "F", lenVar="nGenPart")
    self.out.branch("allTopsPt_TTbarMassCalc", "F", lenVar="nGenPart")

    self.out.branch("isTT_TTbarMassCalc", "B")
    self.out.branch("isTTBB_TTbarMassCalc", "B")
    self.out.branch("isTTbb_TTbarMassCalc", "B")
    self.out.branch("isTTbj_TTbarMassCalc", "B")
    # self.out.branch("isTTcc_TTbarMassCalc", "B")
    # self.out.branch("isTTcj_TTbarMassCalc", "B")
    self.out.branch("isTTcx_TTbarMassCalc", "B")
    self.out.branch("isTTlf_TTbarMassCalc", "B")
    # self.out.branch("isTTll_TTbarMassCalc", "B")
    self.out.branch("genTtbarId_TTbarMassCalc", "I")
    self.out.branch("genTtbarIdCategory_TTbarMassCalc", "I")
    self.out.branch("NExtraBs_TTbarMassCalc", "I")
    self.out.branch("NExtraCs_TTbarMassCalc", "I")
    self.out.branch("NExtraLs_TTbarMassCalc", "I")

  def beginJob(self,histFile=None,histDirName=None):    
    Module.beginJob(self,histFile,histDirName)

  def analyze(self, event):
    genparts = list(Collection(event, "GenPart"))
    genTtbarId = event.genTtbarId

    ttbarMass = -999.9
    topID = []
    topMotherID = []
    topPt = []
    topEta = []
    topPhi = []
    topEnergy = []
    topMass = []
    topp4 = []
    top62ID = []
    top62MotherID = []
    top62Pt = []
    top62Eta = []
    top62Phi = []
    top62Energy = []
    top62Mass = []
    topbID = []
    topbPt = []
    topbEta = []
    topbPhi = []
    topbEnergy = []
    topWID = []
    topWPt = []
    topWEta = []
    topWPhi = []
    topWEnergy = []
    allTopsID = []
    allTopsStatus = []
    allTopsEnergy = []
    allTopsEta = []
    allTopsPhi = []
    allTopsPt = []

    for Idx,part in enumerate(genparts):
      partp4 = part.p4()
      if not (abs(part.pdgId) == 6) :
        continue
      allTopsID.append(part.pdgId)
      allTopsStatus.append(part.status)
      allTopsEnergy.append(partp4.E())
      allTopsEta.append(part.eta)
      allTopsPhi.append(part.phi)
      allTopsPt.append(part.pt)

      if not (part.mass > 10) :
        continue
      t_daughters = []
      t_daughters = event.genPartDaughters[Idx]
      if len(t_daughters) == 2 :
        d1Idx, d1 = t_daughters[0]
        d2Idx, d2 = t_daughters[1]
        if not (abs(d1.pdgId) == 6 or abs(d2.pdgId) == 6) :
          if (abs(d1.pdgId) == 5 or abs(d2.pdgId) == 24) or (abs(d1.pdgId) == 24 or abs(d2.pdgId) == 5) :
            d , W, WIdx = d1, d2, d2Idx
            if abs(d1.pdgId) == 24 :
              d , W, WIdx = d2, d1, d1Idx
            dp4 = d.p4()
            topbID.append(d.pdgId)
            topbPt.append(d.pt)
            topbEta.append(d.eta)
            topbPhi.append(d.phi)
            topbEnergy.append(dp4.E())

            W_daughters = []
            W_daughters = event.genPartDaughters[WIdx]

            while len(W_daughters) == 1 or W_daughters[1][1].pdgId == 22 : 
              W, WIdx = W_daughters[0]
              W_daughters = []
              W_daughters = event.genPartDaughters[WIdx]

            nWDs = len(W_daughters)
            if nWDs > 2 :
              print "W daughters: "+str(nWDs)
            Wd1Idx, Wd1 = W_daughters[0]
            Wd2Idx, Wd2 = W_daughters[1]
            Wd1p4 = Wd1.p4()
            Wd2p4 = Wd2.p4()
            if (abs(Wd1.pdgId) > 10 and abs(Wd1.pdgId) < 17 and abs(Wd2.pdgId) > 10 and abs(Wd2.pdgId) < 17) or (abs(Wd1.pdgId) < 6 and abs(Wd2.pdgId) < 6 ):
              topWID.append[Wd1.pdgId]
              topWID.append[Wd2.pdgId]
              topWPt.append[Wd1.pt]
              topWPt.append[Wd2.pt]
              topWEta.append[Wd1.eta]
              topWEta.append[Wd2.eta]
              topWPhi.append[Wd1.phi]
              topWPhi.append[Wd2.phi]
              topWEnergy.append[Wd1p4.E()]
              topWEnergy.append[Wd2p4.E()]
            else:
              print "Weird W decays: "+str(Wd1.pdgId)+", "+str(Wd2.pdgId)
          else:
            print "2 top daughters are: "+str(d1.pdgId)+", "+str(d2.pdgId)

      mother = genparts.__getitem__(part.genPartIdxMother)
      if not (abs(mother.pdgId) == 6) :
        topID.append(part.pdgId)
        topPt.append(part.pt)
        topEta.append(part.eta)
        topPhi.append(part.phi)
        topMass.append(part.mass)
        topEnergy.append(partp4.E())
        topMotherID.append(mother.pdgId)
        topp4.append(partp4)
      if part.status == 62 :
        top62ID.append(part.pdgId)
        top62Pt.append(part.pt)
        top62Eta.append(part.eta)
        top62Phi.append(part.phi)
        top62Mass.append(part.mass)
        top62Energy.append(partp4.E())
        top62MotherID.append(mother.pdgId)

    if len(topID) == 0 :
      ttbarMass = -999
    elif len(topID) == 2 :
      if topID[0]*topID[1] > 0 :
        print "2 tops have same ID sign!"
      else:
        t1p4 , t2p4= topp4[0], topp4[1]
        ttbarMass = (t1p4+t2p4).M()
    else:
      print 'More than 2 tops!'

    self.out.fillBranch("ttbarMass_TTbarMassCalc", ttbarMass)
    self.out.fillBranch("topID_TTbarMassCalc", topID)
    self.out.fillBranch("topMotherID_TTbarMassCalc", topMotherID)
    self.out.fillBranch("topPt_TTbarMassCalc", topPt)
    self.out.fillBranch("topEta_TTbarMassCalc", topEta)
    self.out.fillBranch("topPhi_TTbarMassCalc", topPhi)
    self.out.fillBranch("topEnergy_TTbarMassCalc", topEnergy)
    self.out.fillBranch("topMass_TTbarMassCalc", topMass)
    self.out.fillBranch("top62ID_TTbarMassCalc", top62ID)
    self.out.fillBranch("top62MotherID_TTbarMassCalc", top62MotherID)
    self.out.fillBranch("top62Pt_TTbarMassCalc", top62Pt)
    self.out.fillBranch("top62Eta_TTbarMassCalc", top62Eta)
    self.out.fillBranch("top62Phi_TTbarMassCalc", top62Phi)
    self.out.fillBranch("top62Energy_TTbarMassCalc", top62Energy)
    self.out.fillBranch("top62Mass_TTbarMassCalc", top62Mass)
    self.out.fillBranch("topbID_TTbarMassCalc", topbID)
    self.out.fillBranch("topbPt_TTbarMassCalc", topbPt)
    self.out.fillBranch("topbEta_TTbarMassCalc", topbEta)
    self.out.fillBranch("topbPhi_TTbarMassCalc", topbPhi)
    self.out.fillBranch("topbEnergy_TTbarMassCalc", topbEnergy)
    self.out.fillBranch("topWID_TTbarMassCalc", topWID)
    self.out.fillBranch("topWPt_TTbarMassCalc", topWPt)
    self.out.fillBranch("topWEta_TTbarMassCalc", topWEta)
    self.out.fillBranch("topWPhi_TTbarMassCalc", topWPhi)
    self.out.fillBranch("topWEnergy_TTbarMassCalc", topWEnergy)
    self.out.fillBranch("allTopsID_TTbarMassCalc", allTopsID)
    self.out.fillBranch("allTopsStatus_TTbarMassCalc", allTopsStatus)
    self.out.fillBranch("allTopsEnergy_TTbarMassCalc", allTopsEnergy)
    self.out.fillBranch("allTopsEta_TTbarMassCalc", allTopsEta)
    self.out.fillBranch("allTopsPhi_TTbarMassCalc", allTopsPhi)
    self.out.fillBranch("allTopsPt_TTbarMassCalc", allTopsPt)



    isTTBB = False
    isTTbb = False
    isTTbj = False
    isTTcx = False
    isTTlf = False
    isTT = True
    genTtbarIdCategory = -1

    if genTtbarId == -1 : 
      genTtbarIdCategory = -1
      isTT = False
    elif genTtbarId == 0 or genTtbarId%100 == 0 :
      genTtbarIdCategory = 0
      isTTlf = True
    elif (genTtbarId+45)%100 == 0 or (genTtbarId+46)%100 == 0 :
      genTtbarIdCategory = 4
      isTTBB = True
    elif (genTtbarId+47)%100 == 0 :
      genTtbarIdCategory = 3
      isTTbb = True
    elif (genTtbarId+48)%100 == 0 or (genTtbarId+49)%100 == 0 :
      genTtbarIdCategory = 2
      isTTbj = True
    else : 
      genTtbarIdCategory = 1
      isTTcj = True

    self.out.fillBranch("isTT_TTbarMassCalc", isTT)
    self.out.fillBranch("isTTBB_TTbarMassCalc", isTTBB)
    self.out.fillBranch("isTTbb_TTbarMassCalc", isTTbb)
    self.out.fillBranch("isTTbj_TTbarMassCalc", isTTbj)
    # self.out.fillBranch("isTTcc_TTbarMassCalc", isTTcc)
    # self.out.fillBranch("isTTcj_TTbarMassCalc", isTTcj)
    self.out.fillBranch("isTTcx_TTbarMassCalc", isTTcx)
    self.out.fillBranch("isTTlf_TTbarMassCalc", isTTlf)
    # self.out.fillBranch("isTTll_TTbarMassCalc", isTTll)
    self.out.fillBranch("genTtbarId_TTbarMassCalc", genTtbarId)
    self.out.fillBranch("genTtbarIdCategory_TTbarMassCalc", genTtbarIdCategory)
    #self.out.fillBranch("NExtraBs_TTbarMassCalc", NExtraBs)
    #self.out.fillBranch("NExtraCs_TTbarMassCalc", NExtraCs)
    #self.out.fillBranch("NExtraLs_TTbarMassCalc", NExtraLs)

    return True



